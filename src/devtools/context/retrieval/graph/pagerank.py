# Copyright (c) 2026
# ruff: noqa: COM812
"""Deterministic weighted personalized PageRank of snapshot resources."""

from __future__ import annotations

import math
from dataclasses import dataclass
from typing import TYPE_CHECKING, ClassVar

from devtools.context.retrieval.composition import require_lexical_result_snapshot

if TYPE_CHECKING:
    from devtools.context.repository.resource import RepositoryResourceAddress
    from devtools.context.repository.snapshot import (
        RepositorySnapshot,
        RepositorySnapshotId,
    )
    from devtools.context.retrieval.graph.view import (
        PythonGraphEdgeContribution,
        PythonResourceGraphView,
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

    source: RepositoryResourceAddress
    contribution: PythonGraphEdgeContribution
    flow: float


@dataclass(frozen=True, slots=True)
class PythonGraphRankedResource:
    """Native structural ranking evidence, not a relevance probability."""

    resource_address: RepositoryResourceAddress
    rank: int
    score: float
    personalization: float
    incoming_supports: tuple[PythonGraphIncomingSupport, ...]


@dataclass(frozen=True, slots=True)
class PythonGraphRankingResult:
    """Retain query, purpose, graph projection, parameters and ranked evidence."""

    snapshot_id: RepositorySnapshotId
    purpose: str
    lexical_result: RepositoryTextLexicalBm25RetrievalResult
    graph_view: PythonResourceGraphView
    settings: GraphRankingSettings
    iterations: int
    converged: bool
    resources: tuple[PythonGraphRankedResource, ...]

    MECHANISM: ClassVar[str] = "lexical-rank-personalized-weighted-ppr-v1"


_DEFAULT_SETTINGS = GraphRankingSettings()


def rank_python_repository_resources(  # noqa: C901, PLR0912
    snapshot: RepositorySnapshot,
    *,
    purpose: str,
    lexical_result: RepositoryTextLexicalBm25RetrievalResult,
    graph_view: PythonResourceGraphView,
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
    if graph_view.snapshot_id != snapshot.id or graph_view.resources != tuple(
        sorted((item.address for item in snapshot.resources), key=str),
    ):
        msg = "Graph view differs from the supplied snapshot."
        raise ValueError(msg)
    require_lexical_result_snapshot(snapshot, lexical_result)
    addresses = graph_view.resources
    positions = {address: index for index, address in enumerate(addresses)}
    seed_weights = [0.0] * len(addresses)
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
        seed_weights[positions[address]] = 1 / (
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
    outgoing: list[list[tuple[int, float]]] = [[] for _ in addresses]
    for edge in graph_view.edges:
        outgoing[positions[edge.source]].append(
            (positions[edge.target], edge.transition_probability)
        )
    scores = seeds.copy()
    converged = False
    iterations = 0
    for _ in range(settings.maximum_iterations):
        iterations += 1
        next_scores = [(1 - settings.damping) * seed for seed in seeds]
        dangling = math.fsum(scores[i] for i, edges in enumerate(outgoing) if not edges)
        for i, seed in enumerate(seeds):
            next_scores[i] += settings.damping * dangling * seed
        for i, edges in enumerate(outgoing):
            for target, probability in edges:
                next_scores[target] += settings.damping * scores[i] * probability
        delta = math.fsum(abs(a - b) for a, b in zip(scores, next_scores, strict=True))
        scores = next_scores
        if delta <= settings.tolerance:
            converged = True
            break
    # Input order and operation order are fixed; final mass is normalized once.
    mass = math.fsum(scores)
    scores = [score / mass for score in scores]
    incoming: dict[RepositoryResourceAddress, list[PythonGraphIncomingSupport]] = {}
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
    ranked = sorted(
        (i for i, score in enumerate(scores) if score > 0),
        key=lambda i: (
            -scores[i],
            lexical_ranks.get(addresses[i], math.inf),
            str(addresses[i]),
        ),
    )
    resources = tuple(
        PythonGraphRankedResource(
            addresses[i],
            rank,
            scores[i],
            seeds[i],
            tuple(
                sorted(
                    incoming.get(addresses[i], ()),
                    key=lambda item: (
                        -item.flow,
                        str(item.source),
                        item.contribution.fact.identity,
                    ),
                )
            ),
        )
        for rank, i in enumerate(ranked, start=1)
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
    )
