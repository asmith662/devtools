# Copyright (c) 2026
# ruff: noqa: D103, PLR2004
"""Direct retrieval consumes qualified production RI facts and keeps provenance."""

from dataclasses import replace
from pathlib import Path
from typing import cast

import pytest

from devtools.context.python.imports import (
    PythonResolvedModuleImportRelation,
    derive_python_import_declarations,
    derive_python_resolved_module_import_relations,
    resolve_python_import_declaration,
)
from devtools.context.python.modules import (
    PythonImmediatePackageMembership,
    PythonModuleRoot,
    define_python_module_interpretation_universe,
    derive_python_immediate_package_memberships,
    interpret_python_module_resources,
)
from devtools.context.python.references import (
    PythonFunctionReferenceKnowledge,
    derive_python_function_references,
)
from devtools.context.repository.identity import Repository, RepositoryId
from devtools.context.repository.observation import observe_repository_resources
from devtools.context.repository.resource import RepositoryResourceAddress
from devtools.context.repository.snapshot import RepositorySnapshot
from devtools.context.retrieval.structural import (
    PythonDirectStructuralRetrievalRequest,
    retrieve_python_direct_structural_resources,
)
from devtools.core.paths import ResolvedPath


def _facts(
    tmp_path: Path,
) -> tuple[
    RepositorySnapshot,
    PythonResolvedModuleImportRelation,
    tuple[PythonFunctionReferenceKnowledge, ...],
    PythonImmediatePackageMembership,
]:
    resources = {
        "pkg/__init__.py": "",
        "pkg/target.py": "def f():\n    pass\n",
        "consumer.py": "from pkg.target import f\nvalue = f\nf()\nf()\n",
        "unrelated.py": "",
    }
    for name, content in resources.items():
        target = tmp_path / name
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(content, encoding="utf-8")
    snapshot = observe_repository_resources(
        repository=Repository(
            RepositoryId.parse("00000000-0000-4000-8000-000000000031"),
        ),
        root=ResolvedPath(tmp_path),
        addresses=tuple(RepositoryResourceAddress(name) for name in resources),
        maximum_resource_bytes=1024,
    )
    interpreted = interpret_python_module_resources(
        snapshot,
        module_root=PythonModuleRoot("."),
        resource_addresses=tuple(item.address for item in snapshot.resources),
    )
    by_address = {
        item.resource.address.value: item for item in interpreted.interpretations
    }
    universe = define_python_module_interpretation_universe(
        repository_id=snapshot.repository_id,
        interpretations=interpreted.interpretations,
    )
    source = RepositoryResourceAddress("consumer.py")
    imports = derive_python_import_declarations(snapshot, resource_address=source)
    resolution = resolve_python_import_declaration(
        imports,
        imports.declarations[0],
        target_universe=universe,
    )
    relation = derive_python_resolved_module_import_relations(
        imports,
        resolutions=(resolution,),
        source_interpretations=(by_address["consumer.py"],),
    ).relations[0]
    references = derive_python_function_references(
        snapshot,
        resource_address=source,
        module_universe=universe,
    ).references
    membership = derive_python_immediate_package_memberships(
        snapshot,
        interpretation_analysis=interpreted,
    ).immediate_package_of(by_address["pkg/target.py"])
    assert membership is not None
    return snapshot, relation, references, membership


def test_direct_projection_retains_native_independent_supports(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    snapshot, relation, references, membership = _facts(tmp_path)
    assert len(references) == 3

    def forbid_parse(*_args: object, **_kwargs: object) -> None:
        msg = "Retrieval must not parse source"
        raise AssertionError(msg)

    monkeypatch.setattr("ast.parse", forbid_parse)
    request = PythonDirectStructuralRetrievalRequest(
        "Find the implementation and its immediate package",
        (
            RepositoryResourceAddress("consumer.py"),
            RepositoryResourceAddress("pkg/__init__.py"),
        ),
    )
    result = retrieve_python_direct_structural_resources(
        snapshot,
        request=request,
        imports=(relation, relation),
        references=references,
        memberships=(membership,),
    )
    assert result.request is request
    assert result.snapshot_id == snapshot.id
    assert len(result.candidates) == 1
    candidate = result.candidates[0]
    assert candidate.resource_address == RepositoryResourceAddress("pkg/target.py")
    assert candidate.snapshot_id == snapshot.id
    assert [item.direction for item in candidate.supports] == [
        "import-to-target",
        "reference-to-definition",
        "reference-to-definition",
        "reference-to-definition",
        "package-to-child",
    ]
    assert [item.fact for item in candidate.supports] == [
        relation,
        *references,
        membership,
    ]
    assert [item.seed_resource.value for item in candidate.supports] == [
        "consumer.py",
        "consumer.py",
        "consumer.py",
        "consumer.py",
        "pkg/__init__.py",
    ]
    assert [item.direct_call for item in references] == [False, True, True]


def test_reverse_projection_and_bounded_zero(tmp_path: Path) -> None:
    snapshot, relation, references, membership = _facts(tmp_path)
    request = PythonDirectStructuralRetrievalRequest(
        "Find direct users and containing package",
        (RepositoryResourceAddress("pkg/target.py"),),
    )
    result = retrieve_python_direct_structural_resources(
        snapshot,
        request=request,
        imports=(relation,),
        references=references,
        memberships=(membership,),
    )
    assert [item.resource_address.value for item in result.candidates] == [
        "consumer.py",
        "pkg/__init__.py",
    ]
    assert [item.direction for item in result.candidates[0].supports] == [
        "import-to-source",
        "definition-to-reference",
        "definition-to-reference",
        "definition-to-reference",
    ]
    assert result.candidates[1].supports[0].direction == "child-to-package"
    empty = retrieve_python_direct_structural_resources(snapshot, request=request)
    assert empty.candidates == ()


def test_request_and_snapshot_mismatch_are_rejected(tmp_path: Path) -> None:
    snapshot, relation, references, membership = _facts(tmp_path)
    with pytest.raises(ValueError, match="purpose"):
        PythonDirectStructuralRetrievalRequest(
            " ",
            (RepositoryResourceAddress("consumer.py"),),
        )
    with pytest.raises(ValueError, match="distinct"):
        PythonDirectStructuralRetrievalRequest("find", ())
    with pytest.raises(ValueError, match="distinct"):
        PythonDirectStructuralRetrievalRequest(
            "find",
            (RepositoryResourceAddress("consumer.py"),) * 2,
        )
    request = PythonDirectStructuralRetrievalRequest(
        "find",
        (RepositoryResourceAddress("consumer.py"),),
    )
    wrong_id = replace(snapshot.id, value="0" * 64)
    with pytest.raises(ValueError, match="snapshot"):
        retrieve_python_direct_structural_resources(
            snapshot,
            request=request,
            imports=(
                replace(
                    relation, source=replace(relation.source, snapshot_id=wrong_id),
                ),
            ),
        )
    with pytest.raises(ValueError, match="snapshot"):
        retrieve_python_direct_structural_resources(
            snapshot,
            request=request,
            references=(
                replace(
                    references[0],
                    occurrence=replace(references[0].occurrence, snapshot_id=wrong_id),
                ),
            ),
        )
    with pytest.raises(ValueError, match="snapshot"):
        retrieve_python_direct_structural_resources(
            snapshot,
            request=request,
            memberships=(
                replace(
                    membership,
                    child=replace(membership.child, snapshot_id=wrong_id),
                ),
            ),
        )


def test_unrelated_and_self_relations_do_not_surface_resources(tmp_path: Path) -> None:
    snapshot, relation, references, membership = _facts(tmp_path)
    unrelated = PythonDirectStructuralRetrievalRequest(
        "Find direct relations of the unrelated file",
        (RepositoryResourceAddress("unrelated.py"),),
    )
    assert not retrieve_python_direct_structural_resources(
        snapshot,
        request=unrelated,
        imports=(relation,),
        references=references,
        memberships=(membership,),
    ).candidates

    self_relation = replace(relation, target=relation.source)
    request = PythonDirectStructuralRetrievalRequest(
        "Find neighbors",
        (RepositoryResourceAddress("consumer.py"),),
    )
    assert not retrieve_python_direct_structural_resources(
        snapshot,
        request=request,
        imports=(self_relation,),
    ).candidates


def test_rejects_fact_family_mixups_and_unknown_seed(tmp_path: Path) -> None:
    snapshot, relation, references, membership = _facts(tmp_path)
    request = PythonDirectStructuralRetrievalRequest(
        "Find direct relations",
        (RepositoryResourceAddress("consumer.py"),),
    )
    with pytest.raises(ValueError, match="does not contain resource"):
        retrieve_python_direct_structural_resources(
            snapshot,
            request=replace(
                request,
                seed_resources=(RepositoryResourceAddress("missing.py"),),
            ),
        )
    with pytest.raises(TypeError, match="Imports"):
        retrieve_python_direct_structural_resources(
            snapshot,
            request=request,
            imports=(cast("PythonResolvedModuleImportRelation", membership),),
        )
    with pytest.raises(TypeError, match="References"):
        retrieve_python_direct_structural_resources(
            snapshot,
            request=request,
            references=(cast("PythonFunctionReferenceKnowledge", relation),),
        )
    with pytest.raises(TypeError, match="Memberships"):
        retrieve_python_direct_structural_resources(
            snapshot,
            request=request,
            memberships=(cast("PythonImmediatePackageMembership", references[0]),),
        )
