# Copyright (c) 2026
# ruff: noqa: COM812, D103, PLR2004
"""Production RI projection, PPR, and native rank fusion."""

import gzip
import pickle
from dataclasses import replace
from pathlib import Path
from typing import TYPE_CHECKING, cast

import pytest

from devtools.context.python.imports import (
    PythonResolvedModuleImportRelation,
    derive_python_import_declarations,
    derive_python_resolved_module_import_relations,
    resolve_python_import_declaration,
)
from devtools.context.python.modules import (
    PythonModuleRoot,
    define_python_module_interpretation_universe,
    interpret_python_module_resources,
)
from devtools.context.python.references.analysis import (
    PythonFunctionReferenceKnowledge,
)
from devtools.context.repository.identity import Repository, RepositoryId
from devtools.context.repository.observation import observe_repository_resources
from devtools.context.repository.resource import RepositoryResourceAddress
from devtools.context.retrieval.fusion import fuse_lexical_graph_rankings
from devtools.context.retrieval.graph import (
    GraphRankingSettings,
    build_python_resource_graph_view,
    rank_python_repository_resources,
)
from devtools.core.paths import ResolvedPath
from experiments.graph_ranking_baseline.evaluate import ARCHIVE
from tests.context.retrieval.test_composition import _lexical
from tests.context.retrieval.test_structural import _facts

if TYPE_CHECKING:
    from devtools.context.python.references import PythonDeclarationReferenceKnowledge


def test_view_projects_forward_facts_once_and_preserves_occurrences(
    tmp_path: Path,
) -> None:
    snapshot, imported, references, _membership = _facts(tmp_path)
    view = build_python_resource_graph_view(
        snapshot,
        imports=(imported, imported),
        references=(*references, references[0]),
    )
    assert view.snapshot_id == snapshot.id
    assert len(view.resources) == 4
    assert len(view.edges) == 1
    edge = view.edges[0]
    assert (str(edge.source.resource_address), str(edge.target.resource_address)) == (
        "consumer.py",
        "pkg/target.py",
    )
    assert edge.weight == 4
    assert edge.transition_probability == 1
    assert [item.kind for item in edge.contributions] == [
        "direct-call",
        "direct-call",
        "import",
        "reference",
    ]
    assert {item.fact.identity for item in edge.contributions} == {
        imported.identity,
        *(item.identity for item in references),
    }
    assert not any(
        edge.source.resource_address == RepositoryResourceAddress("pkg/target.py")
        for edge in view.edges
    )
    assert view == build_python_resource_graph_view(
        snapshot, imports=(imported,), references=references
    )


def test_resource_view_accepts_frozen_function_reference_value() -> None:
    # Historical input is development-only and tests old-view reproducibility.
    with gzip.open(ARCHIVE, "rb") as stream:
        case = pickle.load(stream)  # noqa: S301
    legacy = case.references[0]
    assert isinstance(legacy, PythonFunctionReferenceKnowledge)
    view = build_python_resource_graph_view(case.snapshot, references=(legacy,))
    assert len(view.edges) == 1
    assert view.edges[0].contributions[0].fact == legacy


def test_weighted_transitions_normalize_distinct_fact_counts(tmp_path: Path) -> None:
    texts = {
        "source.py": "import left\nimport left\nimport right\n",
        "left.py": "",
        "right.py": "",
    }
    for name, content in texts.items():
        (tmp_path / name).write_text(content, encoding="utf-8")
    snapshot = observe_repository_resources(
        repository=Repository(
            RepositoryId.parse("00000000-0000-4000-8000-000000000032")
        ),
        root=ResolvedPath(tmp_path),
        addresses=tuple(RepositoryResourceAddress(name) for name in texts),
        maximum_resource_bytes=1024,
    )
    interpreted = interpret_python_module_resources(
        snapshot,
        module_root=PythonModuleRoot("."),
        resource_addresses=tuple(item.address for item in snapshot.resources),
    )
    universe = define_python_module_interpretation_universe(
        repository_id=snapshot.repository_id,
        interpretations=interpreted.interpretations,
    )
    declarations = derive_python_import_declarations(
        snapshot, resource_address=RepositoryResourceAddress("source.py")
    )
    resolutions = tuple(
        resolve_python_import_declaration(
            declarations, declaration, target_universe=universe
        )
        for declaration in declarations.declarations
    )
    imports = derive_python_resolved_module_import_relations(
        declarations,
        resolutions=resolutions,
        source_interpretations=tuple(
            item
            for item in interpreted.interpretations
            if item.resource.address == RepositoryResourceAddress("source.py")
        ),
    ).relations
    view = build_python_resource_graph_view(snapshot, imports=imports)
    assert len(view.edges) == 2
    assert {str(edge.target.resource_address): edge.weight for edge in view.edges} == {
        "left.py": 2,
        "right.py": 1,
    }
    assert {
        str(edge.target.resource_address): edge.transition_probability
        for edge in view.edges
    } == {
        "left.py": pytest.approx(2 / 3),
        "right.py": pytest.approx(1 / 3),
    }
    assert sum(edge.transition_probability for edge in view.edges) == pytest.approx(1)


def test_query_conditioning_dangling_and_disconnected_resources(tmp_path: Path) -> None:
    snapshot, imported, references, _membership = _facts(tmp_path)
    view = build_python_resource_graph_view(
        snapshot, imports=(imported,), references=references
    )
    consumer = _lexical(tmp_path, snapshot, query_text="consumer")
    unrelated = _lexical(tmp_path, snapshot, query_text="unrelated")
    first = rank_python_repository_resources(
        snapshot,
        purpose="Find consumer dependency",
        lexical_result=consumer,
        graph_view=view,
    )
    second = rank_python_repository_resources(
        snapshot, purpose="Find unrelated", lexical_result=unrelated, graph_view=view
    )
    assert first == rank_python_repository_resources(
        snapshot,
        purpose="Find consumer dependency",
        lexical_result=consumer,
        graph_view=view,
    )
    assert first.converged
    assert second.converged
    assert first.resources[0].resource_address == RepositoryResourceAddress(
        "consumer.py"
    )
    assert first.resources[1].resource_address == RepositoryResourceAddress(
        "pkg/target.py"
    )
    assert first.resources[1].incoming_supports
    assert first.resources[0].score == pytest.approx(1 / 1.85, abs=1e-9)
    assert first.resources[1].score == pytest.approx(0.85 / 1.85, abs=1e-9)
    assert second.resources[0].resource_address == RepositoryResourceAddress(
        "unrelated.py"
    )
    assert RepositoryResourceAddress("pkg/target.py") not in {
        item.resource_address for item in second.resources
    }
    assert sum(item.score for item in first.resources) == pytest.approx(1)
    assert sum(item.score for item in second.resources) == pytest.approx(1)
    assert all(item.score > 0 for item in first.resources)


def test_empty_seeds_abstain_and_snapshot_checks(tmp_path: Path) -> None:
    snapshot, imported, references, _membership = _facts(tmp_path)
    view = build_python_resource_graph_view(
        snapshot, imports=(imported,), references=references
    )
    lexical = _lexical(tmp_path, snapshot, query_text="termthatisabsent")
    assert lexical.matches == ()
    result = rank_python_repository_resources(
        snapshot, purpose="Find absent", lexical_result=lexical, graph_view=view
    )
    assert result.resources == ()
    assert result.iterations == 0
    with pytest.raises(ValueError, match="nonempty purpose"):
        rank_python_repository_resources(
            snapshot, purpose=" ", lexical_result=lexical, graph_view=view
        )
    with pytest.raises(ValueError, match="snapshot"):
        rank_python_repository_resources(
            snapshot,
            purpose="Find absent",
            lexical_result=lexical,
            graph_view=replace(view, snapshot_id=replace(snapshot.id, value="0" * 64)),
        )
    with pytest.raises(ValueError, match="snapshot"):
        build_python_resource_graph_view(
            snapshot,
            imports=(
                replace(
                    imported,
                    source=replace(
                        imported.source,
                        snapshot_id=replace(snapshot.id, value="0" * 64),
                    ),
                ),
            ),
        )
    with pytest.raises(TypeError, match="Imports"):
        build_python_resource_graph_view(
            snapshot,
            imports=(cast("PythonResolvedModuleImportRelation", references[0]),),
        )
    with pytest.raises(TypeError, match="References"):
        build_python_resource_graph_view(
            snapshot,
            references=(cast("PythonDeclarationReferenceKnowledge", imported),),
        )
    assert (
        build_python_resource_graph_view(
            snapshot, imports=(replace(imported, target=imported.source),)
        ).edges
        == ()
    )


def test_fusion_retains_native_results_and_is_deterministic(tmp_path: Path) -> None:
    snapshot, imported, references, _membership = _facts(tmp_path)
    lexical = _lexical(tmp_path, snapshot, query_text="consumer")
    graph = rank_python_repository_resources(
        snapshot,
        purpose="Find dependency",
        lexical_result=lexical,
        graph_view=build_python_resource_graph_view(
            snapshot, imports=(imported,), references=references
        ),
    )
    fused = fuse_lexical_graph_rankings(
        snapshot, purpose="Find dependency", lexical_result=lexical, graph_result=graph
    )
    assert fused == fuse_lexical_graph_rankings(
        snapshot, purpose="Find dependency", lexical_result=lexical, graph_result=graph
    )
    assert fused.graph_result is graph
    assert fused.lexical_result is lexical
    first_graph_rank = fused.resources[0].graph_rank
    assert first_graph_rank is not None
    first_lexical_rank = fused.resources[0].lexical_rank
    expected = 1 / (60 + first_graph_rank)
    if first_lexical_rank is not None:
        expected += 1 / (60 + first_lexical_rank)
    assert fused.resources[0].score == pytest.approx(expected)
    assert any(
        item.graph_rank is not None and item.lexical_rank is None
        for item in fused.resources
    )
    with pytest.raises(ValueError, match="purpose"):
        fuse_lexical_graph_rankings(
            snapshot, purpose="other", lexical_result=lexical, graph_result=graph
        )
    with pytest.raises(ValueError, match="snapshot"):
        fuse_lexical_graph_rankings(
            snapshot,
            purpose="Find dependency",
            lexical_result=lexical,
            graph_result=replace(
                graph, snapshot_id=replace(snapshot.id, value="0" * 64)
            ),
        )


def test_retained_snapshot_ranking_does_not_reread_source(tmp_path: Path) -> None:
    snapshot, imported, references, _membership = _facts(tmp_path)
    lexical = _lexical(tmp_path, snapshot, query_text="consumer")
    view = build_python_resource_graph_view(
        snapshot, imports=(imported,), references=references
    )
    original = rank_python_repository_resources(
        snapshot, purpose="Find dependency", lexical_result=lexical, graph_view=view
    )
    (tmp_path / "consumer.py").write_text("changed\n", encoding="utf-8")
    assert (
        rank_python_repository_resources(
            snapshot, purpose="Find dependency", lexical_result=lexical, graph_view=view
        )
        == original
    )


def test_ranker_rejects_unusable_matches_and_reports_iteration_bound(
    tmp_path: Path,
) -> None:
    snapshot, imported, references, _membership = _facts(tmp_path)
    lexical = _lexical(tmp_path, snapshot, query_text="consumer")
    view = build_python_resource_graph_view(
        snapshot, imports=(imported,), references=references
    )
    invalid = replace(lexical, matches=(replace(lexical.matches[0], score=0),))
    with pytest.raises(ValueError, match="positive finite"):
        rank_python_repository_resources(
            snapshot, purpose="Find", lexical_result=invalid, graph_view=view
        )
    duplicate = replace(lexical, matches=(lexical.matches[0], lexical.matches[0]))
    with pytest.raises(ValueError, match="distinct lexical"):
        rank_python_repository_resources(
            snapshot, purpose="Find", lexical_result=duplicate, graph_view=view
        )
    bounded = rank_python_repository_resources(
        snapshot,
        purpose="Find",
        lexical_result=lexical,
        graph_view=view,
        settings=GraphRankingSettings(maximum_iterations=1),
    )
    assert bounded.iterations == 1
    assert not bounded.converged


@pytest.mark.parametrize(
    ("kwargs", "message"),
    [
        ({"damping": 0}, "Damping"),
        ({"tolerance": float("nan")}, "Tolerance"),
        ({"maximum_iterations": 0}, "Iteration"),
    ],
)
def test_settings_validate(kwargs: dict[str, float | int], message: str) -> None:
    with pytest.raises(ValueError, match=message):
        GraphRankingSettings(**kwargs)  # type: ignore[arg-type]
