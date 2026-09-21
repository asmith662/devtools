# Copyright (c) 2026
# ruff: noqa: D103
"""Tests for qualified repository-scoped Python import resolution."""

from dataclasses import replace
from pathlib import Path

import pytest

from devtools.context.python.imports import (
    PythonImportResolutionOutcome,
    PythonImportResolutionUnsupportedReason,
    derive_python_import_declarations,
    resolve_python_import_declaration,
)
from devtools.context.python.modules import (
    PythonModuleRoot,
    define_python_module_interpretation_universe,
    interpret_python_module_resources,
)
from devtools.context.repository.identity import Repository, RepositoryId
from devtools.context.repository.observation import observe_repository_resources
from devtools.context.repository.resource import RepositoryResourceAddress
from devtools.context.repository.snapshot import RepositorySnapshot
from devtools.core.paths import ResolvedPath


def _snapshot(
    tmp_path: Path, resources: dict[str, str], suffix: str = "19",
) -> RepositorySnapshot:
    for address, content in resources.items():
        path = tmp_path / address
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")
    return observe_repository_resources(
        repository=Repository(
            RepositoryId.parse(f"00000000-0000-4000-8000-0000000000{suffix}"),
        ),
        root=ResolvedPath(tmp_path),
        addresses=tuple(RepositoryResourceAddress(address) for address in resources),
        maximum_resource_bytes=1024 * 1024,
    )


def _interpretations(
    snapshot: RepositorySnapshot,
    resources: dict[str, str],
    *,
    root: str = ".",
) -> tuple[object, ...]:
    return interpret_python_module_resources(
        snapshot,
        module_root=PythonModuleRoot(root),
        resource_addresses=tuple(RepositoryResourceAddress(item) for item in resources),
    ).interpretations


def _declaration(
    snapshot: RepositorySnapshot, address: str, ordinal: int = 0,
) -> object:
    return derive_python_import_declarations(
        snapshot,
        resource_address=RepositoryResourceAddress(address),
    ).declarations[ordinal]


def test_absolute_and_from_imports_resolve_only_eligible_module_portion(
    tmp_path: Path,
) -> None:
    resources = {
        "source.py": (
            "import foo\nimport foo.bar as baz\nimport one, two as local_two\n"
            "from foo import bar\nfrom foo.bar import baz\n"
        ),
        "foo.py": "",
        "foo/bar.py": "",
        "one.py": "",
        "two.py": "",
    }
    snapshot = _snapshot(tmp_path, resources)
    analysis = derive_python_import_declarations(
        snapshot,
        resource_address=RepositoryResourceAddress("source.py"),
    )
    universe = define_python_module_interpretation_universe(
        repository_id=snapshot.repository_id,
        interpretations=_interpretations(snapshot, resources),  # type: ignore[arg-type]
    )
    results = tuple(
        resolve_python_import_declaration(
            analysis, declaration, target_universe=universe,
        )
        for declaration in analysis.declarations
    )
    assert [item.requested_module for item in results] == [
        "foo",
        "foo.bar",
        "one",
        "two",
        "foo",
        "foo.bar",
    ]
    assert all(
        item.outcome is PythonImportResolutionOutcome.RESOLVED for item in results
    )
    assert results[1].matches[0].dotted_name == "foo.bar"
    assert results[4].matches[0].dotted_name == "foo"


def test_empty_unresolved_and_ambiguous_universes_preserve_evidence(
    tmp_path: Path,
) -> None:
    resources = {"source.py": "import foo\n", "foo.py": "", "foo/__init__.py": ""}
    snapshot = _snapshot(tmp_path, resources)
    analysis = derive_python_import_declarations(
        snapshot,
        resource_address=RepositoryResourceAddress("source.py"),
    )
    empty = define_python_module_interpretation_universe(
        repository_id=snapshot.repository_id,
        interpretations=(),
    )
    unresolved = resolve_python_import_declaration(
        analysis,
        analysis.declarations[0],
        target_universe=empty,
    )
    assert unresolved.outcome is PythonImportResolutionOutcome.UNRESOLVED_IN_UNIVERSE
    assert unresolved.requested_module == "foo"
    assert unresolved.matches == ()
    assert unresolved.target_universe is empty

    interpretations = _interpretations(snapshot, resources)
    ambiguous_universe = define_python_module_interpretation_universe(
        repository_id=snapshot.repository_id,
        interpretations=interpretations,  # type: ignore[arg-type]
    )
    ambiguous = resolve_python_import_declaration(
        analysis,
        analysis.declarations[0],
        target_universe=ambiguous_universe,
    )
    assert ambiguous.outcome is PythonImportResolutionOutcome.AMBIGUOUS
    assert [item.resource.address.value for item in ambiguous.matches] == [
        "foo.py",
        "foo/__init__.py",
    ]


def test_multiple_roots_and_relative_imports(tmp_path: Path) -> None:
    resources = {
        "first/foo.py": "",
        "second/foo.py": "",
        "package/current.py": "from . import sibling\nfrom .child import member\n",
        "package/child.py": "",
        "package/nested/current.py": "from ..target import member\n",
        "package/target.py": "",
        "package/__init__.py": "from .child import member\n",
    }
    snapshot = _snapshot(tmp_path, resources)
    first = _interpretations(snapshot, {"first/foo.py": ""}, root="first")
    second = _interpretations(snapshot, {"second/foo.py": ""}, root="second")
    roots = define_python_module_interpretation_universe(
        repository_id=snapshot.repository_id,
        interpretations=(*first, *second),  # type: ignore[arg-type]
    )
    absolute_analysis = derive_python_import_declarations(
        _snapshot(tmp_path, {"absolute.py": "import foo\n", **resources}),
        resource_address=RepositoryResourceAddress("absolute.py"),
    )
    assert (
        resolve_python_import_declaration(
            absolute_analysis,
            absolute_analysis.declarations[0],
            target_universe=roots,
        ).outcome
        is PythonImportResolutionOutcome.AMBIGUOUS
    )

    current = _interpretations(snapshot, {"package/current.py": ""})[0]
    target = _interpretations(snapshot, {"package/child.py": ""})[0]
    current_analysis = derive_python_import_declarations(
        snapshot,
        resource_address=RepositoryResourceAddress("package/current.py"),
    )
    relative_universe = define_python_module_interpretation_universe(
        repository_id=snapshot.repository_id,
        interpretations=(target,),  # type: ignore[arg-type]
    )
    relative = tuple(
        resolve_python_import_declaration(
            current_analysis,
            declaration,
            target_universe=relative_universe,
            source_interpretations=(current,),  # type: ignore[arg-type]
        )
        for declaration in current_analysis.declarations
    )
    assert relative[0].requested_module == "package"
    assert relative[0].outcome is PythonImportResolutionOutcome.UNRESOLVED_IN_UNIVERSE
    assert relative[1].requested_module == "package.child"
    assert relative[1].outcome is PythonImportResolutionOutcome.RESOLVED

    nested = _interpretations(snapshot, {"package/nested/current.py": ""})[0]
    target = _interpretations(snapshot, {"package/target.py": ""})[0]
    nested_analysis = derive_python_import_declarations(
        snapshot,
        resource_address=RepositoryResourceAddress("package/nested/current.py"),
    )
    result = resolve_python_import_declaration(
        nested_analysis,
        nested_analysis.declarations[0],
        target_universe=define_python_module_interpretation_universe(
            repository_id=snapshot.repository_id,
            interpretations=(target,),  # type: ignore[arg-type]
        ),
        source_interpretations=(nested,),  # type: ignore[arg-type]
    )
    assert result.requested_module == "package.target"
    assert result.outcome is PythonImportResolutionOutcome.RESOLVED

    package = _interpretations(snapshot, {"package/__init__.py": ""})[0]
    package_analysis = derive_python_import_declarations(
        snapshot,
        resource_address=RepositoryResourceAddress("package/__init__.py"),
    )
    package_result = resolve_python_import_declaration(
        package_analysis,
        package_analysis.declarations[0],
        target_universe=relative_universe,
        source_interpretations=(package,),  # type: ignore[arg-type]
    )
    assert package_result.requested_module == "package.child"


def test_relative_unsupported_source_and_malformed_inputs(tmp_path: Path) -> None:
    resources = {"package/current.py": "from .child import member\n", "other.py": ""}
    snapshot = _snapshot(tmp_path, resources)
    analysis = derive_python_import_declarations(
        snapshot,
        resource_address=RepositoryResourceAddress("package/current.py"),
    )
    universe = define_python_module_interpretation_universe(
        repository_id=snapshot.repository_id,
        interpretations=(),
    )
    missing = resolve_python_import_declaration(
        analysis,
        analysis.declarations[0],
        target_universe=universe,
    )
    assert (
        missing.unsupported_reason
        is PythonImportResolutionUnsupportedReason.RELATIVE_SOURCE_MISSING
    )

    source_root = _interpretations(snapshot, {"package/current.py": ""})[0]
    source_package_root = _interpretations(
        snapshot,
        {"package/current.py": ""},
        root="package",
    )[0]
    ambiguous = resolve_python_import_declaration(
        analysis,
        analysis.declarations[0],
        target_universe=universe,
        source_interpretations=(source_root, source_package_root),  # type: ignore[arg-type]
    )
    assert (
        ambiguous.unsupported_reason
        is PythonImportResolutionUnsupportedReason.RELATIVE_SOURCE_AMBIGUOUS
    )

    beyond_resources = {"package/current.py": "from ..child import member\n"}
    beyond_snapshot = _snapshot(tmp_path, beyond_resources)
    beyond_analysis = derive_python_import_declarations(
        beyond_snapshot,
        resource_address=RepositoryResourceAddress("package/current.py"),
    )
    beyond_source = _interpretations(beyond_snapshot, beyond_resources)[0]
    beyond = resolve_python_import_declaration(
        beyond_analysis,
        beyond_analysis.declarations[0],
        target_universe=define_python_module_interpretation_universe(
            repository_id=beyond_snapshot.repository_id,
            interpretations=(),
        ),
        source_interpretations=(beyond_source,),  # type: ignore[arg-type]
    )
    assert (
        beyond.unsupported_reason
        is PythonImportResolutionUnsupportedReason.RELATIVE_BEYOND_PACKAGE
    )

    with pytest.raises(ValueError, match="does not match"):
        resolve_python_import_declaration(
            analysis,
            analysis.declarations[0],
            target_universe=universe,
            source_interpretations=(_interpretations(snapshot, {"other.py": ""})[0],),  # type: ignore[arg-type]
        )


def test_repository_mismatch_universe_identity_and_content_dependencies(
    tmp_path: Path,
) -> None:
    resources = {"source.py": "import target\n", "target.py": "first"}
    first = _snapshot(tmp_path, resources)
    first_analysis = derive_python_import_declarations(
        first,
        resource_address=RepositoryResourceAddress("source.py"),
    )
    first_target = _interpretations(first, {"target.py": ""})[0]
    first_universe = define_python_module_interpretation_universe(
        repository_id=first.repository_id,
        interpretations=(first_target,),  # type: ignore[arg-type]
    )
    first_result = resolve_python_import_declaration(
        first_analysis,
        first_analysis.declarations[0],
        target_universe=first_universe,
    )

    second = _snapshot(
        tmp_path,
        {
            "source.py": "import target\n# changed\n",
            "target.py": "second",
            "extra.py": "",
        },
    )
    second_analysis = derive_python_import_declarations(
        second,
        resource_address=RepositoryResourceAddress("source.py"),
    )
    second_target = _interpretations(second, {"target.py": ""})[0]
    second_universe = define_python_module_interpretation_universe(
        repository_id=second.repository_id,
        interpretations=(second_target,),  # type: ignore[arg-type]
    )
    second_result = resolve_python_import_declaration(
        second_analysis,
        second_analysis.declarations[0],
        target_universe=second_universe,
    )
    assert first_result.identity != second_result.identity
    assert (
        first_result.matches[0].resource.content_identity
        != second_result.matches[0].resource.content_identity
    )

    other = _snapshot(tmp_path, {"other.py": ""}, suffix="20")
    other_target = _interpretations(other, {"other.py": ""})[0]
    other_universe = define_python_module_interpretation_universe(
        repository_id=other.repository_id,
        interpretations=(other_target,),  # type: ignore[arg-type]
    )
    with pytest.raises(ValueError, match="does not match"):
        resolve_python_import_declaration(
            first_analysis,
            first_analysis.declarations[0],
            target_universe=other_universe,
        )


def test_malformed_declarations_and_universe_membership_are_rejected(
    tmp_path: Path,
) -> None:
    snapshot = _snapshot(tmp_path, {"source.py": "import target\n", "target.py": ""})
    analysis = derive_python_import_declarations(
        snapshot,
        resource_address=RepositoryResourceAddress("source.py"),
    )
    target = _interpretations(snapshot, {"target.py": ""})[0]
    universe = define_python_module_interpretation_universe(
        repository_id=snapshot.repository_id,
        interpretations=(target,),  # type: ignore[arg-type]
    )
    with pytest.raises(ValueError, match="does not belong"):
        resolve_python_import_declaration(
            analysis,
            replace(analysis.declarations[0], declaration_ordinal=99),
            target_universe=universe,
        )
    malformed = replace(analysis.declarations[0], module=None)
    malformed_analysis = replace(analysis, declarations=(malformed,))
    with pytest.raises(ValueError, match="lacks"):
        resolve_python_import_declaration(
            malformed_analysis,
            malformed,
            target_universe=universe,
        )
    with pytest.raises(ValueError, match="repeats"):
        define_python_module_interpretation_universe(
            repository_id=snapshot.repository_id,
            interpretations=(target, target),  # type: ignore[arg-type]
        )
    other = _snapshot(tmp_path, {"other.py": ""}, suffix="20")
    with pytest.raises(ValueError, match="mixes"):
        define_python_module_interpretation_universe(
            repository_id=snapshot.repository_id,
            interpretations=(_interpretations(other, {"other.py": ""})[0],),  # type: ignore[arg-type]
        )
