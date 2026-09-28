# Copyright (c) 2026
# ruff: noqa: D103, PLR2004
"""Tests for bounded source-grounded function references."""

from pathlib import Path

import pytest

from devtools.context.python.function.declarations import PythonSourceRange
from devtools.context.python.modules import (
    PythonModuleRoot,
    define_python_module_interpretation_universe,
    interpret_python_module_resources,
)
from devtools.context.python.references import (
    PythonFunctionReferenceAnalysis,
    PythonReferenceBindingStatus,
    PythonReferenceResolutionPath,
    derive_python_function_references,
)
from devtools.context.repository.identity import Repository, RepositoryId
from devtools.context.repository.observation import observe_repository_resources
from devtools.context.repository.resource import RepositoryResourceAddress
from devtools.context.repository.snapshot import RepositorySnapshot
from devtools.core.paths import ResolvedPath


def _snapshot(tmp_path: Path, resources: dict[str, str]) -> RepositorySnapshot:
    for name, content in resources.items():
        target = tmp_path / name
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(content, encoding="utf-8")
    return observe_repository_resources(
        repository=Repository(
            RepositoryId.parse("00000000-0000-4000-8000-000000000029"),
        ),
        root=ResolvedPath(tmp_path),
        addresses=tuple(RepositoryResourceAddress(name) for name in resources),
        maximum_resource_bytes=1024 * 1024,
    )


def _derive(snapshot: RepositorySnapshot) -> PythonFunctionReferenceAnalysis:
    universe = define_python_module_interpretation_universe(
        repository_id=snapshot.repository_id,
        interpretations=interpret_python_module_resources(
            snapshot,
            module_root=PythonModuleRoot("."),
            resource_addresses=tuple(item.address for item in snapshot.resources),
        ).interpretations,
    )
    return derive_python_function_references(
        snapshot,
        resource_address=RepositoryResourceAddress("consumer.py"),
        module_universe=universe,
    )


def test_direct_reference_and_call_share_one_fact_with_exact_support(
    tmp_path: Path,
) -> None:
    snapshot = _snapshot(
        tmp_path,
        {
            "consumer.py": "from target import f\nvalue = f\nf()\nf()\n",
            "target.py": "def f():\n    pass\n",
        },
    )
    result = _derive(snapshot)
    assert len(result.references) == 3
    assert [item.direct_call for item in result.references] == [False, True, True]
    assert [item.occurrence.source_range.start_line for item in result.references] == [
        2,
        3,
        4,
    ]
    assert all(item.occurrence.snapshot_id == snapshot.id for item in result.references)
    assert all(
        item.target_declaration.declared_name == "f" for item in result.references
    )
    assert all(
        item.target_subject == result.references[0].target_subject
        for item in result.references
    )
    assert all(
        item.resolution_path is PythonReferenceResolutionPath.DIRECT_MODULE
        for item in result.references
    )
    assert len({item.identity for item in result.references}) == 3
    assert _derive(snapshot) == result
    assert result.coverage.reference_count == 3
    assert result.coverage.IS_EXHAUSTIVE is False


def test_one_facade_and_alias_resolve_to_direct_declaration(tmp_path: Path) -> None:
    result = _derive(
        _snapshot(
            tmp_path,
            {
                "consumer.py": "from package import exported as local\nlocal()\n",
                "package/__init__.py": "from .impl import f as exported\n",
                "package/impl.py": "def f():\n    pass\n",
            },
        ),
    )
    assert len(result.references) == 1
    reference = result.references[0]
    assert reference.direct_call
    assert reference.resolution_path is PythonReferenceResolutionPath.ONE_FACADE
    assert (
        str(reference.target_declaration.support.resource_address) == "package/impl.py"
    )
    assert reference.target_declaration.declared_name == "f"


def test_function_body_call_and_utf8_source_span(tmp_path: Path) -> None:
    result = _derive(
        _snapshot(
            tmp_path,
            {
                "consumer.py": (
                    "from target import f\ndef caller():\n    label = 'π'; f()\n"
                ),
                "target.py": "def f():\n    pass\n",
            },
        ),
    )
    assert len(result.references) == 1
    reference = result.references[0]
    assert reference.direct_call
    assert reference.occurrence.source_range == PythonSourceRange(3, 18, 3, 19)


@pytest.mark.parametrize(
    ("source", "reason"),
    [
        (
            "from target import f\nf = other\nf()\n",
            PythonReferenceBindingStatus.COMPETING_OR_WILDCARD_BINDING,
        ),
        (
            "from target import f\nfrom other import *\nf()\n",
            PythonReferenceBindingStatus.COMPETING_OR_WILDCARD_BINDING,
        ),
        (
            "from target import f\nexec('x=1')\nf()\n",
            PythonReferenceBindingStatus.DYNAMIC_NAMESPACE,
        ),
        (
            "from target import f\ndef caller(f):\n    f()\n",
            PythonReferenceBindingStatus.SHADOWED_OR_UNSUPPORTED_SCOPE,
        ),
        (
            "from target import f\n[f() for x in xs]\n",
            PythonReferenceBindingStatus.SHADOWED_OR_UNSUPPORTED_SCOPE,
        ),
        (
            "from target import f\ntry:\n    pass\nexcept Exception as f:\n    f()\n",
            PythonReferenceBindingStatus.COMPETING_OR_WILDCARD_BINDING,
        ),
        (
            "from target import f\ndef caller():\n    f = other\n    f()\n",
            PythonReferenceBindingStatus.SHADOWED_OR_UNSUPPORTED_SCOPE,
        ),
    ],
)
def test_uncertain_binding_is_not_a_reference(
    tmp_path: Path,
    source: str,
    reason: PythonReferenceBindingStatus,
) -> None:
    result = _derive(
        _snapshot(
            tmp_path,
            {
                "consumer.py": source,
                "target.py": "def f():\n    pass\n",
            },
        ),
    )
    assert not result.references
    assert reason in {item.status for item in result.coverage.unsupported_bindings}


def test_partial_qualified_coverage_retains_positive_and_uncertainty(
    tmp_path: Path,
) -> None:
    result = _derive(
        _snapshot(
            tmp_path,
            {
                "consumer.py": "from target import f\nf()\ndef caller(f):\n    f()\n",
                "target.py": "def f():\n    pass\n",
            },
        ),
    )
    assert len(result.references) == 1
    assert result.references[0].occurrence.source_range.start_line == 2
    assert (
        result.coverage.unsupported_bindings[0].status
        is PythonReferenceBindingStatus.SHADOWED_OR_UNSUPPORTED_SCOPE
    )
    limitation = result.coverage.unsupported_bindings[0]
    assert limitation.module_resolution is not None
    assert limitation.member_resolution is not None
    assert limitation.uncertain_occurrences[0].source_range.start_line == 4


def test_ambiguous_target_and_snapshot_mismatch(tmp_path: Path) -> None:
    snapshot = _snapshot(
        tmp_path,
        {
            "consumer.py": "from target import f\nf()\n",
            "target.py": "def f():\n    pass\ndef f():\n    pass\n",
        },
    )
    result = _derive(snapshot)
    assert not result.references
    assert (
        result.coverage.unsupported_bindings[0].status
        is PythonReferenceBindingStatus.MEMBER_UNRESOLVED
    )
    newer = _snapshot(
        tmp_path,
        {
            "consumer.py": "from target import f\nf()\n# changed\n",
            "target.py": "def f():\n    pass\n",
        },
    )
    universe = define_python_module_interpretation_universe(
        repository_id=snapshot.repository_id,
        interpretations=interpret_python_module_resources(
            snapshot,
            module_root=PythonModuleRoot("."),
            resource_addresses=tuple(item.address for item in snapshot.resources),
        ).interpretations,
    )
    with pytest.raises(ValueError, match="snapshot"):
        derive_python_function_references(
            newer,
            resource_address=RepositoryResourceAddress("consumer.py"),
            module_universe=universe,
        )
