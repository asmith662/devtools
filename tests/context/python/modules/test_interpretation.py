# Copyright (c) 2026
# ruff: noqa: D103
"""Tests for deterministic explicit-root module interpretation."""

from pathlib import Path

import pytest

from devtools.context.python.modules import (
    PythonModuleInterpretationExclusionReason,
    PythonModuleKind,
    PythonModuleRoot,
    interpret_python_module_resources,
)
from devtools.context.repository.identity import Repository, RepositoryId
from devtools.context.repository.observation import observe_repository_resources
from devtools.context.repository.resource import RepositoryResourceAddress
from devtools.context.repository.snapshot import RepositorySnapshot
from devtools.core.paths import ResolvedPath


def _snapshot(tmp_path: Path, resources: dict[str, str]) -> RepositorySnapshot:
    for address, content in resources.items():
        path = tmp_path / address
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")
    return observe_repository_resources(
        repository=Repository(RepositoryId.parse("00000000-0000-4000-8000-000000000018")),
        root=ResolvedPath(tmp_path),
        addresses=tuple(RepositoryResourceAddress(address) for address in resources),
        maximum_resource_bytes=1024 * 1024,
    )


def _addresses(resources: dict[str, str]) -> tuple[RepositoryResourceAddress, ...]:
    return tuple(RepositoryResourceAddress(address) for address in resources)


def test_root_and_src_modules_packages_and_deterministic_order(tmp_path: Path) -> None:
    resources = {
        "ignored.txt": "x",
        "src/foo.py": "",
        "src/foo/bar.py": "",
        "src/package/__init__.py": "",
        "src/package/nested/__init__.py": "",
    }
    snapshot = _snapshot(tmp_path, resources)
    root = interpret_python_module_resources(
        snapshot,
        module_root=PythonModuleRoot("."),
        resource_addresses=_addresses(resources),
    )
    assert [(item.dotted_name, item.kind) for item in root.interpretations] == [
        ("src.foo", PythonModuleKind.ORDINARY),
        ("src.foo.bar", PythonModuleKind.ORDINARY),
        ("src.package", PythonModuleKind.PACKAGE),
        ("src.package.nested", PythonModuleKind.PACKAGE),
    ]
    src = interpret_python_module_resources(
        snapshot,
        module_root=PythonModuleRoot("src"),
        resource_addresses=_addresses(resources),
    )
    assert [(item.dotted_name, item.kind) for item in src.interpretations] == [
        ("foo", PythonModuleKind.ORDINARY),
        ("foo.bar", PythonModuleKind.ORDINARY),
        ("package", PythonModuleKind.PACKAGE),
        ("package.nested", PythonModuleKind.PACKAGE),
    ]
    assert [item.reason for item in src.exclusions] == [
        PythonModuleInterpretationExclusionReason.OUTSIDE_MODULE_ROOT,
    ]


def test_collisions_multiple_roots_and_explicit_exclusions(tmp_path: Path) -> None:
    resources = {
        "foo.py": "",
        "foo/__init__.py": "",
        "__init__.py": "",
        "bad-name.py": "",
        "readme.md": "",
        "src/foo.py": "",
    }
    snapshot = _snapshot(tmp_path, resources)
    root = interpret_python_module_resources(
        snapshot,
        module_root=PythonModuleRoot("."),
        resource_addresses=_addresses(resources),
    )
    assert [(item.dotted_name, item.kind) for item in root.interpretations] == [
        ("foo", PythonModuleKind.ORDINARY),
        ("foo", PythonModuleKind.PACKAGE),
        ("src.foo", PythonModuleKind.ORDINARY),
    ]
    assert [item.reason for item in root.exclusions] == [
        PythonModuleInterpretationExclusionReason.ROOT_LEVEL_INIT,
        PythonModuleInterpretationExclusionReason.NON_IDENTIFIER_COMPONENT,
        PythonModuleInterpretationExclusionReason.NON_PYTHON_RESOURCE,
    ]
    src = interpret_python_module_resources(
        snapshot,
        module_root=PythonModuleRoot("src"),
        resource_addresses=_addresses(resources),
    )
    assert src.interpretations[0].dotted_name == "foo"
    assert src.interpretations[0].module_root.value == "src"
    assert all(
        item.reason is PythonModuleInterpretationExclusionReason.OUTSIDE_MODULE_ROOT
        for item in src.exclusions
    )


def test_empty_validation_evidence_and_content_dependency(tmp_path: Path) -> None:
    empty = _snapshot(tmp_path, {})
    result = interpret_python_module_resources(
        empty,
        module_root=PythonModuleRoot("."),
        resource_addresses=(),
    )
    assert result.interpretations == ()
    assert result.exclusions == ()
    for invalid_root in ("", "src/../lib", "src\\lib", "src/"):
        with pytest.raises(ValueError, match="canonical"):
            PythonModuleRoot(invalid_root)

    first = _snapshot(tmp_path, {"module.py": "first"})
    second = _snapshot(tmp_path, {"module.py": "second", "other.py": ""})
    address = RepositoryResourceAddress("module.py")
    first_value = interpret_python_module_resources(
        first,
        module_root=PythonModuleRoot("."),
        resource_addresses=(address,),
    ).interpretations[0]
    second_value = interpret_python_module_resources(
        second,
        module_root=PythonModuleRoot("."),
        resource_addresses=(address,),
    ).interpretations[0]
    assert first_value.dotted_name == second_value.dotted_name == "module"
    assert first_value.identity != second_value.identity
    assert first_value.resource.address == address
    assert first_value.snapshot_id != second_value.snapshot_id


def test_unrelated_resource_does_not_change_interpretation_identity(
    tmp_path: Path,
) -> None:
    first = _snapshot(tmp_path, {"module.py": "same"})
    second = _snapshot(tmp_path, {"module.py": "same", "other.py": "different"})
    address = RepositoryResourceAddress("module.py")
    first_value = interpret_python_module_resources(
        first,
        module_root=PythonModuleRoot("."),
        resource_addresses=(address,),
    ).interpretations[0]
    second_value = interpret_python_module_resources(
        second,
        module_root=PythonModuleRoot("."),
        resource_addresses=(address,),
    ).interpretations[0]
    assert first_value.snapshot_id != second_value.snapshot_id
    assert first_value.identity == second_value.identity


def test_multiple_roots_preserve_same_name_without_precedence(tmp_path: Path) -> None:
    resources = {"first/foo.py": "", "second/foo.py": ""}
    snapshot = _snapshot(tmp_path, resources)
    first = interpret_python_module_resources(
        snapshot,
        module_root=PythonModuleRoot("first"),
        resource_addresses=_addresses(resources),
    )
    second = interpret_python_module_resources(
        snapshot,
        module_root=PythonModuleRoot("second"),
        resource_addresses=_addresses(resources),
    )
    assert first.interpretations[0].dotted_name == "foo"
    assert second.interpretations[0].dotted_name == "foo"
    assert first.interpretations[0].module_root != second.interpretations[0].module_root
    assert first.interpretations[0].identity != second.interpretations[0].identity


def test_selection_is_explicit_and_does_not_acquire_resources(tmp_path: Path) -> None:
    snapshot = _snapshot(tmp_path, {"module.py": "", "unused.py": ""})
    address = RepositoryResourceAddress("module.py")
    result = interpret_python_module_resources(
        snapshot,
        module_root=PythonModuleRoot("."),
        resource_addresses=(address,),
    )
    assert [item.resource.address for item in result.interpretations] == [address]
    with pytest.raises(ValueError, match="distinct"):
        interpret_python_module_resources(
            snapshot,
            module_root=PythonModuleRoot("."),
            resource_addresses=(address, address),
        )
