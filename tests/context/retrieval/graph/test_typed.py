# Copyright (c) 2026
# ruff: noqa: D103
"""Typed Retrieval projection over exact retained production RI facts."""

from __future__ import annotations

from dataclasses import replace
from typing import TYPE_CHECKING, cast

import pytest

from devtools.context.python.classes.bases import (
    PythonDirectBaseAssessment,
    PythonDirectBaseOutcome,
    derive_python_direct_bases,
)
from devtools.context.python.classes.declarations import (
    PythonClassMethodAnalysisAggregate,
    derive_python_class_method_declarations,
)
from devtools.context.python.function.declarations import (
    PythonFunctionDeclarationKnowledge,
    derive_python_function_declarations,
)
from devtools.context.python.imports import (
    PythonResolvedModuleImportRelation,
    derive_python_import_declarations,
    derive_python_resolved_module_import_relations,
    resolve_python_import_declaration,
)
from devtools.context.python.mirrored_paths import (
    PythonMirroredPathCorrespondence,
    derive_python_mirrored_path_correspondences,
)
from devtools.context.python.modules import (
    PythonImmediatePackageMembership,
    PythonModuleRoot,
    define_python_module_interpretation_universe,
    derive_python_immediate_package_memberships,
    interpret_python_module_resources,
)
from devtools.context.python.references import (
    PythonDeclarationReferenceKnowledge,
    derive_python_declaration_references,
)
from devtools.context.repository.identity import Repository, RepositoryId
from devtools.context.repository.observation import observe_repository_resources
from devtools.context.repository.resource import RepositoryResourceAddress
from devtools.context.retrieval.graph import (
    PythonGraphNode,
    PythonGraphNodeKind,
    PythonGraphProjection,
    PythonGraphView,
    build_python_graph_view,
    rank_python_repository_resources,
)
from devtools.core.paths import ResolvedPath
from tests.context.retrieval.test_composition import _lexical

if TYPE_CHECKING:
    from pathlib import Path

    from devtools.context.repository.snapshot import RepositorySnapshot


def _inputs(
    tmp_path: Path,
) -> tuple[
    RepositorySnapshot,
    tuple[PythonResolvedModuleImportRelation, ...],
    tuple[PythonDeclarationReferenceKnowledge, ...],
    tuple[PythonFunctionDeclarationKnowledge, ...],
    PythonClassMethodAnalysisAggregate,
    tuple[PythonDirectBaseAssessment, ...],
    tuple[PythonImmediatePackageMembership, ...],
    tuple[PythonMirroredPathCorrespondence, ...],
]:
    texts = {
        "src/devtools/__init__.py": "",
        "src/devtools/pkg/__init__.py": "",
        "src/devtools/pkg/base.py": "class Base:\n    def run(self):\n        pass\n",
        "src/devtools/pkg/child.py": (
            "from devtools.pkg.base import Base\n"
            "def helper():\n    pass\n"
            "def caller():\n    helper()\n"
            "class Child(Base):\n"
            "    def call(self):\n        Base.run()\n"
        ),
        "tests/pkg/test_child.py": "def test_child():\n    pass\n",
    }
    for path_text, content in texts.items():
        file = tmp_path / path_text
        file.parent.mkdir(parents=True, exist_ok=True)
        file.write_text(content, encoding="utf-8")
    snapshot = observe_repository_resources(
        repository=Repository(
            RepositoryId.parse("00000000-0000-4000-8000-000000000081"),
        ),
        root=ResolvedPath(tmp_path),
        addresses=tuple(RepositoryResourceAddress(address) for address in texts),
        maximum_resource_bytes=4096,
    )
    source_addresses = tuple(
        item.address
        for item in snapshot.resources
        if item.address.value.startswith("src/")
    )
    interpreted = interpret_python_module_resources(
        snapshot,
        module_root=PythonModuleRoot("src"),
        resource_addresses=source_addresses,
    )
    universe = define_python_module_interpretation_universe(
        repository_id=snapshot.repository_id,
        interpretations=interpreted.interpretations,
    )
    functions = tuple(
        declaration
        for address in source_addresses
        for declaration in derive_python_function_declarations(
            snapshot,
            resource_address=address,
        ).declarations
    )
    aggregate = PythonClassMethodAnalysisAggregate(
        tuple(
            derive_python_class_method_declarations(snapshot, resource_address=address)
            for address in source_addresses
        ),
    )
    address = RepositoryResourceAddress("src/devtools/pkg/child.py")
    imports_analysis = derive_python_import_declarations(
        snapshot,
        resource_address=address,
    )
    resolutions = tuple(
        resolve_python_import_declaration(
            imports_analysis,
            item,
            target_universe=universe,
        )
        for item in imports_analysis.declarations
    )
    source_interpretation = tuple(
        item for item in interpreted.interpretations if item.resource.address == address
    )
    imports = derive_python_resolved_module_import_relations(
        imports_analysis,
        resolutions=resolutions,
        source_interpretations=source_interpretation,
    ).relations
    references = derive_python_declaration_references(
        snapshot,
        resource_address=address,
        module_universe=universe,
        source_interpretations=source_interpretation,
    ).references
    bases = derive_python_direct_bases(
        snapshot,
        aggregate=aggregate,
        module_universe=universe,
    ).direct_bases_of(aggregate.classes[1])
    memberships = derive_python_immediate_package_memberships(
        snapshot,
        interpretation_analysis=interpreted,
    ).memberships
    mirrors = derive_python_mirrored_path_correspondences(snapshot).correspondences
    return (
        snapshot,
        imports,
        references,
        functions,
        aggregate,
        bases,
        memberships,
        mirrors,
    )


def _view(  # noqa: PLR0913, PLR0917
    snapshot: RepositorySnapshot,
    imports: tuple[PythonResolvedModuleImportRelation, ...],
    references: tuple[PythonDeclarationReferenceKnowledge, ...],
    functions: tuple[PythonFunctionDeclarationKnowledge, ...],
    aggregate: PythonClassMethodAnalysisAggregate,
    bases: tuple[PythonDirectBaseAssessment, ...],
    memberships: tuple[PythonImmediatePackageMembership, ...] = (),
    mirrors: tuple[PythonMirroredPathCorrespondence, ...] = (),
    *,
    navigation: bool = False,
) -> PythonGraphView:
    return build_python_graph_view(
        snapshot,
        projection=(
            PythonGraphProjection.TYPED_NAVIGATION
            if navigation
            else PythonGraphProjection.TYPED_CORE
        ),
        imports=imports,
        references=references,
        functions=functions,
        classes=aggregate.classes,
        methods=aggregate.methods,
        direct_bases=bases,
        memberships=memberships,
        mirrored_paths=mirrors,
    )


def test_typed_edges_restore_same_resource_reference_and_provenance(
    tmp_path: Path,
) -> None:
    snapshot, imports, references, functions, aggregate, bases, memberships, mirrors = (
        _inputs(tmp_path)
    )
    core = _view(snapshot, imports, references, functions, aggregate, bases)
    again = _view(snapshot, imports, references, functions, aggregate, bases)
    assert core == again
    assert core == _view(
        snapshot,
        (*imports, *imports),
        (*references, *references),
        functions,
        aggregate,
        (*bases, *bases),
    )
    assert len(core.nodes) > len(core.resources)
    assert {node.kind for node in core.nodes} == set(PythonGraphNodeKind)
    assert len({node.identity for node in core.nodes}) == len(core.nodes)
    assert any(
        edge.source.kind is PythonGraphNodeKind.FUNCTION
        and edge.target.kind is PythonGraphNodeKind.FUNCTION
        and edge.source.resource_address == edge.target.resource_address
        and any(c.family == "reference" for c in edge.contributions)
        for edge in core.edges
    )
    assert any(
        edge.source.kind is PythonGraphNodeKind.METHOD
        and edge.target.kind is PythonGraphNodeKind.METHOD
        and any(c.fact in references for c in edge.contributions)
        for edge in core.edges
    )
    assert any(
        edge.source.kind is PythonGraphNodeKind.CLASS
        and edge.target.kind is PythonGraphNodeKind.CLASS
        and any(c.family == "direct-base" for c in edge.contributions)
        for edge in core.edges
    )
    assert all(base.outcome is PythonDirectBaseOutcome.RESOLVED for base in bases)
    assert {c.family for e in core.edges for c in e.contributions} == {
        "import",
        "reference",
        "containment",
        "containment-return",
        "direct-base",
    }
    assert all(
        sum(edge.transition_probability for edge in core.edges if edge.source == node)
        == pytest.approx(1)
        for node in core.nodes
        if any(edge.source == node for edge in core.edges)
    )
    child_resource = next(
        node
        for node in core.nodes
        if node.kind is PythonGraphNodeKind.RESOURCE
        and node.resource_address.value == "src/devtools/pkg/child.py"
    )
    outgoing = [edge for edge in core.edges if edge.source == child_resource]
    assert sum(
        edge.transition_probability
        for edge in outgoing
        if any(c.family == "import" for c in edge.contributions)
    ) == pytest.approx(0.5)
    assert sum(
        edge.transition_probability
        for edge in outgoing
        if any(c.family == "containment" for c in edge.contributions)
    ) == pytest.approx(0.5)
    navigation = _view(
        snapshot,
        imports,
        references,
        functions,
        aggregate,
        bases,
        memberships,
        mirrors,
        navigation=True,
    )
    assert {"package-membership", "mirrored-path"} <= {
        c.family for edge in navigation.edges for c in edge.contributions
    }
    assert {
        c.direction
        for edge in navigation.edges
        for c in edge.contributions
        if c.family == "mirrored-path"
    } == {
        "source-to-mirrored-test",
        "test-to-mirrored-source",
    }


def test_typed_ppr_resource_personalization_and_max_aggregation(tmp_path: Path) -> None:
    snapshot, imports, references, functions, aggregate, bases, _memberships, _ = (
        _inputs(tmp_path)
    )
    view = _view(snapshot, imports, references, functions, aggregate, bases)
    lexical = _lexical(tmp_path, snapshot, query_text="caller")
    ranked = rank_python_repository_resources(
        snapshot,
        purpose="Find caller",
        lexical_result=lexical,
        graph_view=view,
    )
    assert ranked == rank_python_repository_resources(
        snapshot,
        purpose="Find caller",
        lexical_result=lexical,
        graph_view=view,
    )
    assert ranked.converged
    assert sum(item.score for item in ranked.node_scores) == pytest.approx(1)
    assert all(
        item.personalization == 0
        for item in ranked.node_scores
        if item.node.kind is not PythonGraphNodeKind.RESOURCE
    )
    assert all(
        item.score
        == max(
            node.score
            for node in ranked.node_scores
            if node.node.resource_address == item.resource_address
        )
        for item in ranked.resources
    )
    different = rank_python_repository_resources(
        snapshot,
        purpose="Find Base",
        lexical_result=_lexical(tmp_path, snapshot, query_text="Base"),
        graph_view=view,
    )
    assert ranked.node_scores != different.node_scores


def test_typed_projection_rejects_stale_and_missing_declaration_support(
    tmp_path: Path,
) -> None:
    snapshot, imports, references, functions, aggregate, bases, memberships, _ = (
        _inputs(
            tmp_path,
        )
    )
    with pytest.raises(ValueError, match="absent"):
        _view(snapshot, imports, references, (), aggregate, bases)
    with pytest.raises(ValueError, match="snapshot"):
        _view(
            snapshot,
            imports,
            references,
            (
                replace(
                    functions[0],
                    subject=replace(
                        functions[0].subject,
                        snapshot_id=replace(snapshot.id, value="0" * 64),
                    ),
                ),
                *functions[1:],
            ),
            aggregate,
            bases,
        )
    with pytest.raises(ValueError, match="Core projection"):
        _view(
            snapshot,
            imports,
            references,
            functions,
            aggregate,
            bases,
            memberships=memberships,
        )


def test_typed_ranker_rejects_invalid_graph_rows(tmp_path: Path) -> None:
    snapshot, imports, references, functions, aggregate, bases, _, _ = _inputs(
        tmp_path,
    )
    view = _view(snapshot, imports, references, functions, aggregate, bases)
    lexical = _lexical(tmp_path, snapshot, query_text="caller")

    def rank(invalid: PythonGraphView) -> None:
        rank_python_repository_resources(
            snapshot,
            purpose="Find caller",
            lexical_result=lexical,
            graph_view=invalid,
        )

    with pytest.raises(ValueError, match="repeats a typed node"):
        rank(replace(view, nodes=(*view.nodes, view.nodes[0])))
    with pytest.raises(ValueError, match="resource nodes differ"):
        rank(
            replace(
                view,
                nodes=tuple(node for node in view.nodes if node != view.nodes[0]),
            ),
        )
    orphan = PythonGraphNode(
        PythonGraphNodeKind.METHOD,
        "orphan",
        RepositoryResourceAddress("unobserved.py"),
    )
    with pytest.raises(ValueError, match="unobserved resource"):
        rank(replace(view, nodes=(*view.nodes, orphan)))
    with pytest.raises(ValueError, match="invalid probability"):
        rank(
            replace(
                view,
                edges=(
                    replace(view.edges[0], transition_probability=0),
                    *view.edges[1:],
                ),
            ),
        )
    with pytest.raises(ValueError, match="sum to one"):
        rank(
            replace(
                view,
                edges=(
                    replace(
                        view.edges[0],
                        transition_probability=view.edges[0].transition_probability / 2,
                    ),
                    *view.edges[1:],
                ),
            ),
        )


def test_typed_view_rejects_unsupported_or_inconsistent_facts(tmp_path: Path) -> None:
    snapshot, imports, references, functions, aggregate, bases, memberships, mirrors = (
        _inputs(tmp_path)
    )
    with pytest.raises(ValueError, match="Resource-only"):
        build_python_graph_view(
            snapshot,
            projection=PythonGraphProjection.RESOURCE_FORWARD,
            functions=functions,
        )
    with pytest.raises(ValueError, match="repeat a structural subject"):
        _view(
            snapshot,
            imports,
            references,
            (*functions, functions[0]),
            aggregate,
            bases,
        )
    with pytest.raises(ValueError, match="containing class is absent"):
        build_python_graph_view(
            snapshot,
            projection=PythonGraphProjection.TYPED_CORE,
            methods=aggregate.methods,
        )
    with pytest.raises(TypeError, match="Direct bases"):
        _view(
            snapshot,
            imports,
            references,
            functions,
            aggregate,
            (cast("PythonDirectBaseAssessment", object()),),
        )
    with pytest.raises(ValueError, match="positive resolved"):
        _view(
            snapshot,
            imports,
            references,
            functions,
            aggregate,
            (replace(bases[0], outcome=PythonDirectBaseOutcome.UNRESOLVED_BINDING),),
        )
    with pytest.raises(ValueError, match="snapshot"):
        _view(
            snapshot,
            imports,
            references,
            functions,
            aggregate,
            (
                replace(
                    bases[0],
                    base=replace(
                        bases[0].base,
                        occurrence=replace(
                            bases[0].base.occurrence,
                            snapshot_id=replace(snapshot.id, value="0" * 64),
                        ),
                    ),
                ),
            ),
        )
    with pytest.raises(TypeError, match="Memberships"):
        _view(
            snapshot,
            imports,
            references,
            functions,
            aggregate,
            bases,
            (cast("PythonImmediatePackageMembership", object()),),
            mirrors,
            navigation=True,
        )
    with pytest.raises(TypeError, match="Mirrored paths"):
        _view(
            snapshot,
            imports,
            references,
            functions,
            aggregate,
            bases,
            memberships,
            (cast("PythonMirroredPathCorrespondence", object()),),
            navigation=True,
        )
    with pytest.raises(ValueError, match="another snapshot"):
        _view(
            snapshot,
            imports,
            references,
            functions,
            aggregate,
            bases,
            memberships,
            (replace(mirrors[0], snapshot_id=replace(snapshot.id, value="0" * 64)),),
            navigation=True,
        )
