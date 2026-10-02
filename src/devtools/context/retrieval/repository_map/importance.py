# Copyright (c) 2026
"""Repository-global importance independent of task and lexical retrieval."""

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING, ClassVar

from devtools.context.retrieval.graph.pagerank import (
    GraphRankingSettings,
    PythonGraphIncomingSupport,
    PythonGraphNodeScore,
    require_graph_view_snapshot,
)
from devtools.context.retrieval.graph.view import PythonGraphNodeKind
from devtools.context.retrieval.graph.walk import stationary_distribution

if TYPE_CHECKING:
    from devtools.context.repository.snapshot import RepositorySnapshot
    from devtools.context.retrieval.repository_map.view import RepositoryMapView


@dataclass(frozen=True, slots=True)
class RepositoryMapImportance:
    """Native stationary masses and incoming RI contribution flow."""

    view: RepositoryMapView
    settings: GraphRankingSettings
    node_scores: tuple[PythonGraphNodeScore, ...]
    incoming_supports: tuple[tuple[PythonGraphIncomingSupport, ...], ...]
    iterations: int
    converged: bool

    MECHANISM: ClassVar[str] = "resource-uniform-dependency-global-pagerank-v1"


_DEFAULT_SETTINGS = GraphRankingSettings()


def calculate_repository_map_importance(
    snapshot: RepositorySnapshot,
    *,
    view: RepositoryMapView,
    settings: GraphRankingSettings = _DEFAULT_SETTINGS,
) -> RepositoryMapImportance:
    """Restart uniformly over resources; declarations receive only dependency flow.

    No query or lexical seeds enter this walk. Declaration count cannot create
    restart mass or outward containment transitions. Repeated reference facts
    retain bounded row-normalized influence and exact provenance.
    """
    graph = view.dependencies
    require_graph_view_snapshot(snapshot, graph)
    positions = {node: index for index, node in enumerate(graph.nodes)}
    seeds = [
        1 / len(graph.resources) if node.kind is PythonGraphNodeKind.RESOURCE else 0.0
        for node in graph.nodes
    ]
    outgoing: list[list[tuple[int, float]]] = [[] for _ in graph.nodes]
    for edge in graph.edges:
        outgoing[positions[edge.source]].append(
            (positions[edge.target], edge.transition_probability),
        )
    scores, iterations, converged = stationary_distribution(
        outgoing,
        seeds,
        damping=settings.damping,
        tolerance=settings.tolerance,
        maximum_iterations=settings.maximum_iterations,
    )
    incoming: list[list[PythonGraphIncomingSupport]] = [[] for _ in graph.nodes]
    for edge in graph.edges:
        for contribution in edge.contributions:
            incoming[positions[edge.target]].append(
                PythonGraphIncomingSupport(
                    edge.source,
                    contribution,
                    settings.damping
                    * scores[positions[edge.source]]
                    * contribution.weight,
                ),
            )
    return RepositoryMapImportance(
        view,
        settings,
        tuple(
            PythonGraphNodeScore(node, scores[i], seeds[i])
            for i, node in enumerate(graph.nodes)
        ),
        tuple(tuple(items) for items in incoming),
        iterations,
        converged,
    )
