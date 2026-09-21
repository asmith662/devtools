# Copyright (c) 2026
# ruff: noqa: D103
"""Tests for declaration-grounded resolved import relations."""

from pathlib import Path

import pytest

from devtools.context.python.imports import (
    PythonImportRelationSourceStatus,
    PythonImportResolutionOutcome,
    derive_python_import_declarations,
    derive_python_resolved_module_import_relations,
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
from devtools.core.paths import ResolvedPath


def test_relations_are_declaration_grounded_and_require_one_source(
    tmp_path: Path,
) -> None:
    for name, text in {
        "a.py": "import b\nimport b as alias\nfrom b import value\nimport missing\n",
        "b.py": "import a\n",
    }.items():
        (tmp_path / name).write_text(text, encoding="utf-8")
    snapshot = observe_repository_resources(
        repository=Repository(
            RepositoryId.parse("00000000-0000-4000-8000-000000000020"),
        ),
        root=ResolvedPath(tmp_path),
        addresses=(
            RepositoryResourceAddress("a.py"),
            RepositoryResourceAddress("b.py"),
        ),
        maximum_resource_bytes=1024,
    )
    analysis = derive_python_import_declarations(
        snapshot,
        resource_address=RepositoryResourceAddress("a.py"),
    )
    values = interpret_python_module_resources(
        snapshot,
        module_root=PythonModuleRoot("."),
        resource_addresses=(
            RepositoryResourceAddress("a.py"),
            RepositoryResourceAddress("b.py"),
        ),
    ).interpretations
    source, target = values
    universe = define_python_module_interpretation_universe(
        repository_id=snapshot.repository_id,
        interpretations=(target,),
    )
    resolutions = tuple(
        resolve_python_import_declaration(analysis, item, target_universe=universe)
        for item in analysis.declarations
    )
    derived = derive_python_resolved_module_import_relations(
        analysis,
        resolutions=resolutions,
        source_interpretations=(source,),
    )
    assert derived.source_status is PythonImportRelationSourceStatus.AVAILABLE
    expected_relation_count = 3
    assert len(derived.relations) == expected_relation_count
    assert all(item.target is target for item in derived.relations)
    assert len({item.identity for item in derived.relations}) == expected_relation_count
    assert (
        derive_python_resolved_module_import_relations(
            analysis,
            resolutions=resolutions,
            source_interpretations=(),
        ).source_status
        is PythonImportRelationSourceStatus.MISSING
    )
    assert (
        derive_python_resolved_module_import_relations(
            analysis,
            resolutions=resolutions,
            source_interpretations=(source, source),
        ).source_status
        is PythonImportRelationSourceStatus.AMBIGUOUS
    )
    with pytest.raises(ValueError, match="Relation source interpretation"):
        derive_python_resolved_module_import_relations(
            analysis,
            resolutions=resolutions,
            source_interpretations=(target,),
        )

    other_analysis = derive_python_import_declarations(
        snapshot,
        resource_address=RepositoryResourceAddress("b.py"),
    )
    source_universe = define_python_module_interpretation_universe(
        repository_id=snapshot.repository_id,
        interpretations=(source,),
    )
    other_resolution = resolve_python_import_declaration(
        other_analysis,
        other_analysis.declarations[0],
        target_universe=source_universe,
    )
    with pytest.raises(ValueError, match="Relation resolution"):
        derive_python_resolved_module_import_relations(
            analysis,
            resolutions=(other_resolution,),
            source_interpretations=(source,),
        )


def test_nested_relative_self_and_non_resolved_outcomes(tmp_path: Path) -> None:
    resources = {
        "package/a.py": (
            "import package.b.c\nfrom . import ignored\nfrom .child import value\n"
        ),
        "package/b/c.py": "",
        "package/child.py": "",
        "package/__init__.py": "from .child import value\n",
        "self.py": "import self\n",
        "foo.py": "",
        "foo/__init__.py": "",
    }
    for name, text in resources.items():
        path = tmp_path / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding="utf-8")
    snapshot = observe_repository_resources(
        repository=Repository(
            RepositoryId.parse("00000000-0000-4000-8000-000000000020"),
        ),
        root=ResolvedPath(tmp_path),
        addresses=tuple(RepositoryResourceAddress(name) for name in resources),
        maximum_resource_bytes=1024,
    )
    addresses = tuple(RepositoryResourceAddress(name) for name in resources)
    interpretations = interpret_python_module_resources(
        snapshot,
        module_root=PythonModuleRoot("."),
        resource_addresses=addresses,
    ).interpretations
    by_name = {item.resource.address.value: item for item in interpretations}
    target_universe = define_python_module_interpretation_universe(
        repository_id=snapshot.repository_id,
        interpretations=(
            by_name["package/b/c.py"],
            by_name["package/child.py"],
            by_name["self.py"],
            by_name["foo.py"],
            by_name["foo/__init__.py"],
        ),
    )
    analysis = derive_python_import_declarations(
        snapshot,
        resource_address=RepositoryResourceAddress("package/a.py"),
    )
    resolutions = tuple(
        resolve_python_import_declaration(
            analysis,
            item,
            target_universe=target_universe,
            source_interpretations=(by_name["package/a.py"],) if item.level else (),
        )
        for item in analysis.declarations
    )
    derived = derive_python_resolved_module_import_relations(
        analysis,
        resolutions=resolutions,
        source_interpretations=(by_name["package/a.py"],),
    )
    assert [item.target.resource.address.value for item in derived.relations] == [
        "package/b/c.py",
        "package/child.py",
    ]
    assert derived.relations[0].declaration is analysis.declarations[0]
    assert derived.relations[0].resolution.target_universe is target_universe
    assert derived.relations[0].source.resource is snapshot.resource_at(
        RepositoryResourceAddress("package/a.py"),
    )

    package_analysis = derive_python_import_declarations(
        snapshot,
        resource_address=RepositoryResourceAddress("package/__init__.py"),
    )
    package_resolution = resolve_python_import_declaration(
        package_analysis,
        package_analysis.declarations[0],
        target_universe=target_universe,
        source_interpretations=(by_name["package/__init__.py"],),
    )
    assert (
        derive_python_resolved_module_import_relations(
            package_analysis,
            resolutions=(package_resolution,),
            source_interpretations=(by_name["package/__init__.py"],),
        )
        .relations[0]
        .target
        is by_name["package/child.py"]
    )

    self_analysis = derive_python_import_declarations(
        snapshot,
        resource_address=RepositoryResourceAddress("self.py"),
    )
    self_resolution = resolve_python_import_declaration(
        self_analysis,
        self_analysis.declarations[0],
        target_universe=target_universe,
    )
    self_relation = derive_python_resolved_module_import_relations(
        self_analysis,
        resolutions=(self_resolution,),
        source_interpretations=(by_name["self.py"],),
    ).relations[0]
    assert self_relation.source is self_relation.target
    assert not any(
        item.outcome is PythonImportResolutionOutcome.AMBIGUOUS for item in resolutions
    )


def test_ambiguous_unsupported_and_multiple_root_relations_are_zero(
    tmp_path: Path,
) -> None:
    resources = {
        "a.py": "import foo\nfrom ..bad import value\n",
        "foo.py": "",
        "foo/__init__.py": "",
        "src/a.py": "import foo\n",
        "src/foo.py": "",
    }
    for name, text in resources.items():
        path = tmp_path / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding="utf-8")
    snapshot = observe_repository_resources(
        repository=Repository(
            RepositoryId.parse("00000000-0000-4000-8000-000000000020"),
        ),
        root=ResolvedPath(tmp_path),
        addresses=tuple(RepositoryResourceAddress(name) for name in resources),
        maximum_resource_bytes=1024,
    )
    root_values = interpret_python_module_resources(
        snapshot,
        module_root=PythonModuleRoot("."),
        resource_addresses=tuple(RepositoryResourceAddress(name) for name in resources),
    ).interpretations
    src_values = interpret_python_module_resources(
        snapshot,
        module_root=PythonModuleRoot("src"),
        resource_addresses=(
            RepositoryResourceAddress("src/a.py"),
            RepositoryResourceAddress("src/foo.py"),
        ),
    ).interpretations
    by_address = {item.resource.address.value: item for item in root_values}
    universe = define_python_module_interpretation_universe(
        repository_id=snapshot.repository_id,
        interpretations=(by_address["foo.py"], by_address["foo/__init__.py"]),
    )
    analysis = derive_python_import_declarations(
        snapshot,
        resource_address=RepositoryResourceAddress("a.py"),
    )
    ambiguous = resolve_python_import_declaration(
        analysis,
        analysis.declarations[0],
        target_universe=universe,
    )
    unsupported = resolve_python_import_declaration(
        analysis,
        analysis.declarations[1],
        target_universe=universe,
        source_interpretations=(by_address["a.py"],),
    )
    assert ambiguous.outcome is PythonImportResolutionOutcome.AMBIGUOUS
    assert unsupported.outcome is PythonImportResolutionOutcome.UNSUPPORTED
    assert (
        derive_python_resolved_module_import_relations(
            analysis,
            resolutions=(ambiguous, unsupported),
            source_interpretations=(by_address["a.py"],),
        ).relations
        == ()
    )
    source_analysis = derive_python_import_declarations(
        snapshot,
        resource_address=RepositoryResourceAddress("src/a.py"),
    )
    root_source = by_address["src/a.py"]
    assert (
        derive_python_resolved_module_import_relations(
            source_analysis,
            resolutions=(),
            source_interpretations=(root_source, src_values[0]),
        ).source_status
        is PythonImportRelationSourceStatus.AMBIGUOUS
    )
    root_target_universe = define_python_module_interpretation_universe(
        repository_id=snapshot.repository_id,
        interpretations=(by_address["foo.py"], src_values[1]),
    )
    root_target_resolution = resolve_python_import_declaration(
        analysis,
        analysis.declarations[0],
        target_universe=root_target_universe,
    )
    assert root_target_resolution.outcome is PythonImportResolutionOutcome.AMBIGUOUS
    expected_ambiguous_target_count = 2
    assert len(root_target_resolution.matches) == expected_ambiguous_target_count
    assert (
        derive_python_resolved_module_import_relations(
            analysis,
            resolutions=(root_target_resolution,),
            source_interpretations=(by_address["a.py"],),
        ).relations
        == ()
    )


def test_relation_identity_tracks_declaration_source_resolution_and_target(
    tmp_path: Path,
) -> None:
    resources = {
        "src/a.py": "import b\nimport b as alias\n",
        "src/b.py": "first target\n",
        "src/utility.py": "",
    }
    for name, text in resources.items():
        path = tmp_path / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding="utf-8")
    repository = Repository(RepositoryId.parse("00000000-0000-4000-8000-000000000020"))
    addresses = tuple(RepositoryResourceAddress(name) for name in resources)
    snapshot = observe_repository_resources(
        repository=repository,
        root=ResolvedPath(tmp_path),
        addresses=addresses,
        maximum_resource_bytes=1024,
    )
    analysis = derive_python_import_declarations(
        snapshot,
        resource_address=RepositoryResourceAddress("src/a.py"),
    )
    src_interpretations = interpret_python_module_resources(
        snapshot,
        module_root=PythonModuleRoot("src"),
        resource_addresses=addresses,
    ).interpretations
    root_interpretations = interpret_python_module_resources(
        snapshot,
        module_root=PythonModuleRoot("."),
        resource_addresses=addresses,
    ).interpretations
    by_src_address = {item.resource.address.value: item for item in src_interpretations}
    by_root_address = {
        item.resource.address.value: item for item in root_interpretations
    }
    source = by_src_address["src/a.py"]
    target = by_src_address["src/b.py"]
    utility = by_src_address["src/utility.py"]
    target_universe = define_python_module_interpretation_universe(
        repository_id=snapshot.repository_id,
        interpretations=(target,),
    )
    first_resolution = resolve_python_import_declaration(
        analysis,
        analysis.declarations[0],
        target_universe=target_universe,
    )
    first_relation = derive_python_resolved_module_import_relations(
        analysis,
        resolutions=(first_resolution,),
        source_interpretations=(source,),
    ).relations[0]

    alias_resolution = resolve_python_import_declaration(
        analysis,
        analysis.declarations[1],
        target_universe=target_universe,
    )
    alias_relation = derive_python_resolved_module_import_relations(
        analysis,
        resolutions=(alias_resolution,),
        source_interpretations=(source,),
    ).relations[0]
    assert first_relation.identity != alias_relation.identity

    root_source_relation = derive_python_resolved_module_import_relations(
        analysis,
        resolutions=(first_resolution,),
        source_interpretations=(by_root_address["src/a.py"],),
    ).relations[0]
    assert first_relation.identity != root_source_relation.identity

    expanded_universe = define_python_module_interpretation_universe(
        repository_id=snapshot.repository_id,
        interpretations=(target, utility),
    )
    expanded_resolution = resolve_python_import_declaration(
        analysis,
        analysis.declarations[0],
        target_universe=expanded_universe,
    )
    expanded_relation = derive_python_resolved_module_import_relations(
        analysis,
        resolutions=(expanded_resolution,),
        source_interpretations=(source,),
    ).relations[0]
    assert first_relation.identity != expanded_relation.identity

    (tmp_path / "src" / "b.py").write_text("second target\n", encoding="utf-8")
    changed_snapshot = observe_repository_resources(
        repository=repository,
        root=ResolvedPath(tmp_path),
        addresses=addresses,
        maximum_resource_bytes=1024,
    )
    changed_analysis = derive_python_import_declarations(
        changed_snapshot,
        resource_address=RepositoryResourceAddress("src/a.py"),
    )
    changed_interpretations = interpret_python_module_resources(
        changed_snapshot,
        module_root=PythonModuleRoot("src"),
        resource_addresses=addresses,
    ).interpretations
    changed_by_address = {
        item.resource.address.value: item for item in changed_interpretations
    }
    changed_target = changed_by_address["src/b.py"]
    changed_universe = define_python_module_interpretation_universe(
        repository_id=changed_snapshot.repository_id,
        interpretations=(changed_target,),
    )
    changed_resolution = resolve_python_import_declaration(
        changed_analysis,
        changed_analysis.declarations[0],
        target_universe=changed_universe,
    )
    changed_relation = derive_python_resolved_module_import_relations(
        changed_analysis,
        resolutions=(changed_resolution,),
        source_interpretations=(changed_by_address["src/a.py"],),
    ).relations[0]
    assert first_relation.identity != changed_relation.identity


def test_relation_identity_excludes_unrelated_observed_state(tmp_path: Path) -> None:
    repository = Repository(RepositoryId.parse("00000000-0000-4000-8000-000000000020"))
    for name, text in {"a.py": "import b\n", "b.py": ""}.items():
        (tmp_path / name).write_text(text, encoding="utf-8")
    addresses = (RepositoryResourceAddress("a.py"), RepositoryResourceAddress("b.py"))
    first_snapshot = observe_repository_resources(
        repository=repository,
        root=ResolvedPath(tmp_path),
        addresses=addresses,
        maximum_resource_bytes=1024,
    )
    (tmp_path / "unrelated.py").write_text("different\n", encoding="utf-8")
    second_snapshot = observe_repository_resources(
        repository=repository,
        root=ResolvedPath(tmp_path),
        addresses=(*addresses, RepositoryResourceAddress("unrelated.py")),
        maximum_resource_bytes=1024,
    )

    first_analysis = derive_python_import_declarations(
        first_snapshot,
        resource_address=RepositoryResourceAddress("a.py"),
    )
    first_values = interpret_python_module_resources(
        first_snapshot,
        module_root=PythonModuleRoot("."),
        resource_addresses=addresses,
    ).interpretations
    first_by_address = {item.resource.address.value: item for item in first_values}
    first_universe = define_python_module_interpretation_universe(
        repository_id=first_snapshot.repository_id,
        interpretations=(first_by_address["b.py"],),
    )
    first_resolution = resolve_python_import_declaration(
        first_analysis,
        first_analysis.declarations[0],
        target_universe=first_universe,
    )
    first_relation = derive_python_resolved_module_import_relations(
        first_analysis,
        resolutions=(first_resolution,),
        source_interpretations=(first_by_address["a.py"],),
    ).relations[0]

    second_analysis = derive_python_import_declarations(
        second_snapshot,
        resource_address=RepositoryResourceAddress("a.py"),
    )
    second_values = interpret_python_module_resources(
        second_snapshot,
        module_root=PythonModuleRoot("."),
        resource_addresses=addresses,
    ).interpretations
    second_by_address = {item.resource.address.value: item for item in second_values}
    second_universe = define_python_module_interpretation_universe(
        repository_id=second_snapshot.repository_id,
        interpretations=(second_by_address["b.py"],),
    )
    second_resolution = resolve_python_import_declaration(
        second_analysis,
        second_analysis.declarations[0],
        target_universe=second_universe,
    )
    second_relation = derive_python_resolved_module_import_relations(
        second_analysis,
        resolutions=(second_resolution,),
        source_interpretations=(second_by_address["a.py"],),
    ).relations[0]
    assert first_snapshot.id != second_snapshot.id
    assert first_relation.identity == second_relation.identity
