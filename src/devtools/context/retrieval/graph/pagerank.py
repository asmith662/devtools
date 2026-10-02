# Copyright (c) 2026
# ruff: noqa: COM812
"""One deterministic weighted Personalized PageRank walk over Retrieval nodes."""

from __future__ import annotations

import math
from dataclasses import dataclass
from typing import TYPE_CHECKING, ClassVar

from devtools.context.retrieval.composition import require_lexical_result_snapshot
from devtools.context.retrieval.graph.view import PythonGraphNodeKind
from devtools.context.retrieval.graph.walk import stationary_distribution

if TYPE_CHECKING:
    from devtools.context.repository.resource import RepositoryResourceAddress
    from devtools.context.repository.snapshot import (
        RepositorySnapshot,
        RepositorySnapshotId,
    )
    from devtools.context.retrieval.graph.view import (
        PythonGraphEdgeContribution,
        PythonGraphNode,
        PythonGraphView,
    )
    from devtools.context.retrieval.lexical.bm25 import (
        RepositoryTextLexicalBm25RetrievalResult,
    )


@dataclass(frozen=True, slots=True)
class GraphRankingSettings:
    """Fixed baseline algorithm parameters, independent of usefulness labels."""

    damping: float = 0.85
    tolerance: float = 1e-10
    maximum_iterations: int = 200
    personalization_rank_constant: int = 60

    def __post_init__(self) -> None:
        """Reject unsupported or nonfinite iteration settings."""
        if not math.isfinite(self.damping) or not 0 < self.damping < 1:
            msg = "Damping must be finite and between zero and one."
            raise ValueError(msg)
        if not math.isfinite(self.tolerance) or self.tolerance <= 0:
            msg = "Tolerance must be finite and positive."
            raise ValueError(msg)
        if self.maximum_iterations <= 0 or self.personalization_rank_constant < 0:
            msg = "Iteration bound must be positive and rank constant nonnegative."
            raise ValueError(msg)


@dataclass(frozen=True, slots=True)
class PythonGraphIncomingSupport:
    """One incoming RI fact's share of stationary graph transition flow."""

    source: PythonGraphNode
    contribution: PythonGraphEdgeContribution
    flow: float


@dataclass(frozen=True, slots=True)
class PythonGraphRankedResource:
    """Native structural ranking evidence, not a relevance probability."""

    resource_address: RepositoryResourceAddress
    rank: int
    score: float
    personalization: float
    winning_node: PythonGraphNode
    incoming_supports: tuple[PythonGraphIncomingSupport, ...]


@dataclass(frozen=True, slots=True)
class PythonGraphNodeScore:
    """Retain the stationary mass of one typed graph endpoint."""

    node: PythonGraphNode
    score: float
    personalization: float


@dataclass(frozen=True, slots=True)
class PythonGraphRankingResult:
    """Retain query, purpose, graph projection, parameters and ranked evidence."""

    snapshot_id: RepositorySnapshotId
    purpose: str
    lexical_result: RepositoryTextLexicalBm25RetrievalResult
    graph_view: PythonGraphView
    settings: GraphRankingSettings
    iterations: int
    converged: bool
    resources: tuple[PythonGraphRankedResource, ...]
    node_scores: tuple[PythonGraphNodeScore, ...] = ()

    MECHANISM: ClassVar[str] = "lexical-rank-personalized-weighted-ppr-v2"


_DEFAULT_SETTINGS = GraphRankingSettings()


def rank_python_repository_resources(
    snapshot: RepositorySnapshot,
    *,
    purpose: str,
    lexical_result: RepositoryTextLexicalBm25RetrievalResult,
    graph_view: PythonGraphView,
    settings: GraphRankingSettings = _DEFAULT_SETTINGS,
) -> PythonGraphRankingResult:
    """Diffuse query-specific lexical rank mass over forward RI transitions.

    The lexical score is never treated as a probability. Reciprocal lexical
    ranks define seed mass. Dangling nodes restart according to that same vector.
    No usable lexical matches means abstention (an empty ranking), not global
    centrality or a negative knowledge claim. All graph nodes come from the
    retained snapshot; no source or working-tree reads occur here.
    """
    if not purpose.strip():
        msg = "Graph ranking requires a nonempty purpose."
        raise ValueError(msg)
    require_graph_view_snapshot(snapshot, graph_view)
    require_lexical_result_snapshot(snapshot, lexical_result)
    nodes = graph_view.nodes
    positions = {node: index for index, node in enumerate(nodes)}
    resource_nodes = {
        node.resource_address: node
        for node in nodes
        if node.kind is PythonGraphNodeKind.RESOURCE
    }
    seed_weights = [0.0] * len(nodes)
    lexical_ranks: dict[RepositoryResourceAddress, int] = {}
    for rank, match in enumerate(lexical_result.matches, start=1):
        address = match.document_statistics.analysis.document.resource.address
        if match.score <= 0 or not math.isfinite(match.score):
            msg = "Graph personalization requires positive finite BM25 matches."
            raise ValueError(msg)
        if address in lexical_ranks:
            msg = "Graph personalization requires distinct lexical matches."
            raise ValueError(msg)
        lexical_ranks[address] = rank
        seed_weights[positions[resource_nodes[address]]] = 1 / (
            settings.personalization_rank_constant + rank
        )
    total = math.fsum(seed_weights)
    if total == 0:
        return PythonGraphRankingResult(
            snapshot_id=snapshot.id,
            purpose=purpose,
            lexical_result=lexical_result,
            graph_view=graph_view,
            settings=settings,
            iterations=0,
            converged=True,
            resources=(),
        )
    seeds = [weight / total for weight in seed_weights]
    outgoing: list[list[tuple[int, float]]] = [[] for _ in nodes]
    for edge in graph_view.edges:
        outgoing[positions[edge.source]].append(
            (positions[edge.target], edge.transition_probability)
        )
    scores, iterations, converged = stationary_distribution(
        outgoing,
        seeds,
        damping=settings.damping,
        tolerance=settings.tolerance,
        maximum_iterations=settings.maximum_iterations,
    )
    incoming: dict[PythonGraphNode, list[PythonGraphIncomingSupport]] = {}
    for edge in graph_view.edges:
        flow = (
            settings.damping
            * scores[positions[edge.source]]
            * edge.transition_probability
        )
        for contribution in edge.contributions:
            incoming.setdefault(edge.target, []).append(
                PythonGraphIncomingSupport(
                    edge.source,
                    contribution,
                    flow * contribution.weight / edge.weight,
                )
            )
    winners = {
        address: max(
            (node for node in nodes if node.resource_address == address),
            key=lambda node: (scores[positions[node]], -positions[node]),
        )
        for address in graph_view.resources
    }
    ranked = sorted(
        (address for address, node in winners.items() if scores[positions[node]] > 0),
        key=lambda address: (
            -scores[positions[winners[address]]],
            lexical_ranks.get(address, math.inf),
            str(address),
        ),
    )
    resources = tuple(
        PythonGraphRankedResource(
            address,
            rank,
            scores[positions[winners[address]]],
            seeds[positions[resource_nodes[address]]],
            winners[address],
            tuple(
                sorted(
                    incoming.get(winners[address], ()),
                    key=lambda item: (
                        -item.flow,
                        item.source.identity,
                        item.contribution.fact.identity,
                    ),
                )
            ),
        )
        for rank, address in enumerate(ranked, start=1)
    )
    return PythonGraphRankingResult(
        snapshot.id,
        purpose,
        lexical_result,
        graph_view,
        settings,
        iterations,
        converged,
        resources,
        tuple(
            PythonGraphNodeScore(node, scores[index], seeds[index])
            for index, node in enumerate(nodes)
        ),
    )


def require_graph_view_snapshot(
    snapshot: RepositorySnapshot,
    graph_view: PythonGraphView,
) -> None:
    """Validate a graph's snapshot frame, typed endpoints, and stochastic rows."""
    if graph_view.snapshot_id != snapshot.id or graph_view.resources != tuple(
        sorted((item.address for item in snapshot.resources), key=str),
    ):
        msg = "Graph view differs from the supplied snapshot."
        raise ValueError(msg)
    nodes = graph_view.nodes
    positions = {node: index for index, node in enumerate(nodes)}
    if len(positions) != len(nodes):
        msg = "Graph view repeats a typed node."
        raise ValueError(msg)
    resource_nodes = {
        node.resource_address: node
        for node in nodes
        if node.kind is PythonGraphNodeKind.RESOURCE
    }
    if set(resource_nodes) != set(graph_view.resources):
        msg = "Graph resource nodes differ from the supplied snapshot."
        raise ValueError(msg)
    if any(node.resource_address not in resource_nodes for node in nodes):
        msg = "Graph declaration node belongs to an unobserved resource."
        raise ValueError(msg)
    row_sums: dict[PythonGraphNode, float] = {}
    for edge in graph_view.edges:
        if (
            edge.source not in positions
            or edge.target not in positions
            or not math.isfinite(edge.transition_probability)
            or edge.transition_probability <= 0
        ):
            msg = "Graph edge has an unknown endpoint or invalid probability."
            raise ValueError(msg)
        row_sums[edge.source] = (
            row_sums.get(edge.source, 0.0) + edge.transition_probability
        )
    if any(not math.isclose(total, 1.0, abs_tol=1e-9) for total in row_sums.values()):
        msg = "Graph outgoing transition probabilities must sum to one."
        raise ValueError(msg)
