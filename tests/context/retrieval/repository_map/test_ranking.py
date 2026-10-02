# Copyright (c) 2026
# ruff: noqa: D103, PLR2004
"""Structural importance, symbol relevance, projection and snapshot invariants."""

from __future__ import annotations

from dataclasses import replace
from typing import TYPE_CHECKING

import pytest

from devtools.context.repository.identity import Repository
from devtools.context.repository.observation import observe_repository_resources
from devtools.context.repository.snapshot import RepositorySnapshotId
from devtools.context.retrieval.fusion import fuse_lexical_repository_map_rankings
from devtools.context.retrieval.graph import (
    GraphRankingSettings,
    PythonGraphNodeKind,
    PythonGraphProjection,
    build_python_graph_view,
)
from devtools.context.retrieval.lexical import analyze_repository_text_lexical_query
from devtools.context.retrieval.repository_map import (
    build_repository_map_view,
    calculate_repository_map_importance,
    rank_repository_map,
)
from devtools.context.retrieval.repository_map.relevance import (
    score_repository_map_symbols,
)
from devtools.core.paths import ResolvedPath
from tests.context.retrieval.graph.test_typed import _inputs, _view
from tests.context.retrieval.test_composition import _lexical

if TYPE_CHECKING:
    from pathlib import Path


def test_reference_flow_symbol_identity_and_reproducibility(tmp_path: Path) -> None:
    inputs = _inputs(tmp_path)
    snapshot = inputs[0]
    core = _view(*inputs[:6])
    view = build_repository_map_view(snapshot, core=core)
    assert view == build_repository_map_view(snapshot, core=core)
    assert len(view.symbols) == 6
    assert {item.qualified_name for item in view.symbols} == {
        "Base",
        "Base.run",
        "Child",
        "Child.call",
        "helper",
        "caller",
    }
    assert {item.node.identity for item in view.symbols} == {
        node.identity
        for node in core.nodes
        if node.kind is not PythonGraphNodeKind.RESOURCE
    }
    assert all(
        item.declaration.subject.identity in item.node.identity for item in view.symbols
    )
    assert all(
        contribution.family != "containment"
        for edge in view.dependencies.edges
        for contribution in edge.contributions
    )
    reference_edges = [
        edge
        for edge in view.dependencies.edges
        if any(item.family == "reference" for item in edge.contributions)
    ]
    assert reference_edges
    assert all(
        edge.source.kind is PythonGraphNodeKind.RESOURCE for edge in reference_edges
    )
    importance = calculate_repository_map_importance(snapshot, view=view)
    assert importance == calculate_repository_map_importance(snapshot, view=view)
    assert importance.converged
    assert sum(item.score for item in importance.node_scores) == pytest.approx(1)
    assert sum(
        item.personalization for item in importance.node_scores
    ) == pytest.approx(1)
    assert all(
        item.personalization == 0
        for item in importance.node_scores
        if item.node.kind is not PythonGraphNodeKind.RESOURCE
    )
    helper = next(item for item in view.symbols if item.qualified_name == "helper")
    index = view.dependencies.nodes.index(helper.node)
    assert importance.node_scores[index].score > 0
    assert any(
        item.contribution.fact in inputs[2] and item.flow > 0
        for item in importance.incoming_supports[index]
    )
    without_references = build_repository_map_view(
        snapshot,
        core=_view(snapshot, inputs[1], (), inputs[3], inputs[4], inputs[5]),
    )
    no_ref = calculate_repository_map_importance(snapshot, view=without_references)
    assert no_ref.node_scores[index].score == 0
    stopped = calculate_repository_map_importance(
        snapshot,
        view=view,
        settings=GraphRankingSettings(maximum_iterations=1),
    )
    assert not stopped.converged


def test_containment_does_not_create_importance_or_size_mass(tmp_path: Path) -> None:
    snapshot, _, _, functions, aggregate, *_ = _inputs(tmp_path)
    plain = build_python_graph_view(
        snapshot,
        projection=PythonGraphProjection.TYPED_CORE,
    )
    declared = build_python_graph_view(
        snapshot,
        projection=PythonGraphProjection.TYPED_CORE,
        functions=functions,
        classes=aggregate.classes,
        methods=aggregate.methods,
    )
    baseline = calculate_repository_map_importance(
        snapshot,
        view=build_repository_map_view(snapshot, core=plain),
    )
    rich = calculate_repository_map_importance(
        snapshot,
        view=build_repository_map_view(snapshot, core=declared),
    )
    assert {
        item.node.resource_address: item.score
        for item in baseline.node_scores
        if item.node.kind is PythonGraphNodeKind.RESOURCE
    } == {
        item.node.resource_address: item.score
        for item in rich.node_scores
        if item.node.kind is PythonGraphNodeKind.RESOURCE
    }
    assert all(
        item.score == 0
        for item in rich.node_scores
        if item.node.kind is not PythonGraphNodeKind.RESOURCE
    )
    edges = rich.view.dependencies.edges
    assert any(
        edge.source.kind is PythonGraphNodeKind.METHOD
        and edge.target.kind is PythonGraphNodeKind.CLASS
        for edge in edges
    )


def test_symbol_relevance_and_maximum_resource_projection(tmp_path: Path) -> None:
    inputs = _inputs(tmp_path)
    snapshot = inputs[0]
    view = build_repository_map_view(snapshot, core=_view(*inputs[:6]))
    importance = calculate_repository_map_importance(snapshot, view=view)
    query = analyze_repository_text_lexical_query(text="helper")
    result = rank_repository_map(
        snapshot,
        purpose="Find bounded declarations",
        query=query,
        importance=importance,
    )
    assert result == rank_repository_map(
        snapshot,
        purpose=result.purpose,
        query=query,
        importance=importance,
    )
    assert result.symbols
    assert result.resources
    for resource in result.resources:
        owned = [
            item
            for item in result.symbols
            if item.symbol.node.resource_address == resource.resource_address
        ]
        assert resource.score == max(item.score for item in owned)
        assert resource.winning_symbol in owned
    assert len({item.resource_address for item in result.resources}) == len(
        result.resources,
    )
    assert any(
        item.lexical_rank is None and item.importance_rank is not None
        for item in result.symbols
    )
    assert any(
        item.lexical_rank is not None and item.importance_rank is None
        for item in rank_repository_map(
            snapshot,
            purpose="Find caller",
            query=analyze_repository_text_lexical_query(text="caller"),
            importance=importance,
        ).symbols
    )
    assert all(
        item.lexical_match.score > 0 for item in result.symbols if item.lexical_match
    )
    assert not any(
        "__init__.py" in str(item.resource_address) for item in result.resources
    )
    # A declaration body term is deliberately absent from compact name/path metadata.
    assert (
        score_repository_map_symbols(
            view,
            query=analyze_repository_text_lexical_query(text="pass"),
        )
        == ()
    )
    path_matches = score_repository_map_symbols(
        view,
        query=analyze_repository_text_lexical_query(text="child"),
    )
    assert path_matches
    assert all("child.py" in item.metadata for item in path_matches)
    tied = score_repository_map_symbols(
        view,
        query=analyze_repository_text_lexical_query(text="src"),
    )
    assert tied == tuple(
        sorted(tied, key=lambda item: (-item.score, item.symbol.node.identity)),
    )
    assert (
        rank_repository_map(
            snapshot,
            purpose="Unknown symbol",
            query=analyze_repository_text_lexical_query(text="zzmissingzz"),
            importance=importance,
        ).resources
        == ()
    )
    assert (
        rank_repository_map(
            snapshot,
            purpose="Empty query",
            query=analyze_repository_text_lexical_query(text=""),
            importance=importance,
        ).symbols
        == ()
    )


def test_invalid_frames_and_declaration_dependencies(tmp_path: Path) -> None:
    inputs = _inputs(tmp_path)
    snapshot = inputs[0]
    core = _view(*inputs[:6])
    with pytest.raises(ValueError, match="typed core"):
        build_repository_map_view(
            snapshot,
            core=replace(core, projection=PythonGraphProjection.TYPED_NAVIGATION),
        )
    with pytest.raises(ValueError, match="subjects"):
        build_repository_map_view(
            snapshot,
            core=replace(
                core,
                edges=(),
            ),
        )
    view = build_repository_map_view(snapshot, core=core)
    importance = calculate_repository_map_importance(snapshot, view=view)
    query = analyze_repository_text_lexical_query(text="helper")
    with pytest.raises(ValueError, match="nonempty purpose"):
        rank_repository_map(snapshot, purpose=" ", query=query, importance=importance)
    with pytest.raises(ValueError, match="scores differ"):
        rank_repository_map(
            snapshot,
            purpose="Find helper",
            query=query,
            importance=replace(importance, node_scores=importance.node_scores[::-1]),
        )
    # Reading a changed resource makes a different snapshot; old evidence cannot drift.
    (tmp_path / "src/devtools/pkg/child.py").write_text(
        "def changed():\n    pass\n",
        encoding="utf-8",
    )
    changed = observe_repository_resources(
        repository=Repository(snapshot.repository_id),
        root=ResolvedPath(tmp_path),
        addresses=tuple(item.address for item in snapshot.resources),
        maximum_resource_bytes=4096,
    )
    with pytest.raises(ValueError, match="snapshot"):
        build_repository_map_view(changed, core=core)
    with pytest.raises(ValueError, match="snapshot"):
        calculate_repository_map_importance(changed, view=view)
    with pytest.raises(ValueError, match="snapshot"):
        rank_repository_map(
            changed,
            purpose="Find helper",
            query=query,
            importance=importance,
        )
    assert rank_repository_map(
        snapshot,
        purpose="Find helper",
        query=query,
        importance=importance,
    ).symbols


def test_empty_snapshot_and_symbol_frame(tmp_path: Path) -> None:
    inputs = _inputs(tmp_path)
    snapshot = inputs[0]
    no_symbols = build_repository_map_view(
        snapshot,
        core=build_python_graph_view(
            snapshot,
            projection=PythonGraphProjection.TYPED_CORE,
        ),
    )
    assert (
        score_repository_map_symbols(
            no_symbols,
            query=analyze_repository_text_lexical_query(text="helper"),
        )
        == ()
    )
    empty = observe_repository_resources(
        repository=Repository(snapshot.repository_id),
        root=ResolvedPath(tmp_path),
        addresses=(),
        maximum_resource_bytes=4096,
    )
    view = build_repository_map_view(
        empty,
        core=build_python_graph_view(
            empty,
            projection=PythonGraphProjection.TYPED_CORE,
        ),
    )
    importance = calculate_repository_map_importance(empty, view=view)
    assert importance.node_scores == ()
    assert importance.iterations == 0
    assert importance.converged
    assert (
        rank_repository_map(
            empty,
            purpose="No resources",
            query=analyze_repository_text_lexical_query(text="helper"),
            importance=importance,
        ).resources
        == ()
    )


def test_resource_fusion_preserves_native_channels_and_missingness(
    tmp_path: Path,
) -> None:
    inputs = _inputs(tmp_path)
    snapshot = inputs[0]
    importance = calculate_repository_map_importance(
        snapshot,
        view=build_repository_map_view(snapshot, core=_view(*inputs[:6])),
    )
    lexical = _lexical(tmp_path, snapshot, query_text="helper")
    result = rank_repository_map(
        snapshot,
        purpose="Find helper",
        query=lexical.query,
        importance=importance,
    )
    fused = fuse_lexical_repository_map_rankings(
        snapshot,
        purpose=result.purpose,
        lexical_result=lexical,
        map_result=result,
    )
    assert fused.lexical_result is lexical
    assert fused.map_result is result
    assert (
        fused.resources
        == fuse_lexical_repository_map_rankings(
            snapshot,
            purpose=result.purpose,
            lexical_result=lexical,
            map_result=result,
        ).resources
    )
    assert any(
        item.lexical_match is None and item.map_evidence is not None
        for item in fused.resources
    )
    for item in fused.resources:
        assert item.score == pytest.approx(
            (1 / (60 + item.lexical_rank) if item.lexical_rank else 0)
            + (1 / (60 + item.map_evidence.rank) if item.map_evidence else 0),
        )
    lexical_only = _lexical(tmp_path, snapshot, query_text="pass")
    abstained = rank_repository_map(
        snapshot,
        purpose="Find source",
        query=lexical_only.query,
        importance=importance,
    )
    fallback = fuse_lexical_repository_map_rankings(
        snapshot,
        purpose=abstained.purpose,
        lexical_result=lexical_only,
        map_result=abstained,
    )
    assert fallback.resources
    assert all(item.map_evidence is None for item in fallback.resources)
    for purpose in ("", "Different purpose"):
        with pytest.raises(ValueError, match="same nonempty purpose"):
            fuse_lexical_repository_map_rankings(
                snapshot,
                purpose=purpose,
                lexical_result=lexical,
                map_result=result,
            )
    with pytest.raises(ValueError, match="snapshot and query"):
        fuse_lexical_repository_map_rankings(
            snapshot,
            purpose=result.purpose,
            lexical_result=lexical_only,
            map_result=result,
        )
    with pytest.raises(ValueError, match="snapshot and query"):
        fuse_lexical_repository_map_rankings(
            snapshot,
            purpose=result.purpose,
            lexical_result=lexical,
            map_result=replace(result, snapshot_id=RepositorySnapshotId("f" * 64)),
        )
