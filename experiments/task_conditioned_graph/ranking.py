# Copyright (c) 2026
# ruff: noqa: EM101, TRY003, COM812
"""Frozen task personalization around production stationary walk and RRF."""

from __future__ import annotations

import math
from dataclasses import dataclass
from typing import TYPE_CHECKING

from devtools.context.retrieval.composition import require_lexical_result_snapshot
from devtools.context.retrieval.fusion import _fused_resource_order
from devtools.context.retrieval.graph.pagerank import GraphRankingSettings
from devtools.context.retrieval.graph.walk import stationary_distribution
from experiments.task_conditioned_graph.view import require_view

if TYPE_CHECKING:
    from collections.abc import Sequence

    from devtools.context.repository.resource import (
        RepositoryResourceAddress,
        RepositoryResourceOccurrence,
    )
    from devtools.context.repository.snapshot import RepositorySnapshot
    from devtools.context.retrieval.lexical.bm25 import (
        RepositoryTextLexicalBm25RetrievalResult,
    )
    from experiments.task_conditioned_graph.view import ReferenceView

LEXICAL_K = 10
SETTINGS = GraphRankingSettings()


@dataclass(frozen=True)
class RankedResource:
    """Positive incoming-reference-flow evidence; stationary mass is internal."""

    address: RepositoryResourceAddress
    rank: int
    score: float
    seed: bool


@dataclass(frozen=True)
class PprResourceState:
    """Complete internal PPR accounting, including seed-only and zero nodes."""

    address: RepositoryResourceAddress
    stationary_mass: float
    seed: bool
    direct_restart_mass: float
    dangling_return_mass: float
    incoming_structural_flow: float
    incoming: tuple[tuple[int, float], ...]


@dataclass(frozen=True)
class Ranking:
    """Native view and lexical/exact seed provenance, never semantic sufficiency."""

    view: ReferenceView
    lexical: RepositoryTextLexicalBm25RetrievalResult
    exact: tuple[RepositoryResourceOccurrence, ...]
    seeds: tuple[RepositoryResourceAddress, ...]
    resources: tuple[RankedResource, ...]
    iterations: int
    settings: GraphRankingSettings
    states: tuple[PprResourceState, ...]


def seed_union(
    snapshot: RepositorySnapshot,
    lexical: RepositoryTextLexicalBm25RetrievalResult,
    exact: Sequence[RepositoryResourceOccurrence],
) -> tuple[RepositoryResourceAddress, ...]:
    """Union native existing exact results with first ten positive BM25 matches.

    Exact resolution itself remains the existing snapshot/module/declaration
    mechanism. Callers retain its native result and project observed resources.
    This operation cannot resolve future paths, fuzzy names or query text.
    """
    require_lexical_result_snapshot(snapshot, lexical)
    for resource in exact:
        if snapshot.resource_at(resource.address) != resource:
            raise ValueError("Exact seed differs from retained occurrence")
    addresses = []
    for match in lexical.matches:
        if match.score <= 0 or not math.isfinite(match.score):
            raise ValueError("Lexical seeds require positive finite matches")
        addresses.append(match.document_statistics.analysis.document.resource.address)
    if len(set(addresses)) != len(addresses):
        raise ValueError("Duplicate lexical resources")
    return tuple(sorted({*(r.address for r in exact), *addresses[:LEXICAL_K]}, key=str))


def rank(
    snapshot: RepositorySnapshot,
    view: ReferenceView,
    lexical: RepositoryTextLexicalBm25RetrievalResult,
    exact: Sequence[RepositoryResourceOccurrence] = (),
    *,
    settings: GraphRankingSettings = SETTINGS,
) -> Ranking:
    """Use production PPR arithmetic with uniform unique-resource seed mass.

    No seeds means an empty graph ranking, never global PageRank. Nonconvergence
    is an application defect, not a silently accepted effectiveness result.
    Retain all node states, but rank only positive incoming reference flow.
    """
    require_view(snapshot, view)
    seeds = seed_union(snapshot, lexical, exact)
    exact_unique = tuple(sorted(set(exact), key=lambda r: str(r.address)))
    positions = {node: i for i, node in enumerate(view.nodes)}
    personalization = [1 / len(seeds) if node in seeds else 0.0 for node in view.nodes]
    outgoing: list[list[tuple[int, float]]] = [[] for _ in view.nodes]
    for edge in view.edges:
        outgoing[positions[edge.source]].append(
            (positions[edge.target], edge.probability)
        )
    if seeds:
        scores, iterations, converged = stationary_distribution(
            outgoing,
            personalization,
            damping=settings.damping,
            tolerance=settings.tolerance,
            maximum_iterations=settings.maximum_iterations,
        )
    else:
        scores, iterations, converged = [0.0] * len(view.nodes), 0, True
    if not converged:
        raise ValueError("PPR did not converge under frozen iteration bound")
    dangling = math.fsum(scores[i] for i, edges in enumerate(outgoing) if not edges)
    incoming: dict[RepositoryResourceAddress, list[tuple[int, float]]] = {}
    for i, edge in enumerate(view.edges):
        incoming.setdefault(edge.target, []).append(
            (i, settings.damping * scores[positions[edge.source]] * edge.probability)
        )
    states = tuple(
        PprResourceState(
            n,
            scores[positions[n]],
            n in seeds,
            (1 - settings.damping) * personalization[positions[n]],
            settings.damping * dangling * personalization[positions[n]],
            math.fsum(flow for _, flow in incoming.get(n, ())),
            tuple(sorted(incoming.get(n, ()), key=lambda x: (-x[1], x[0]))),
        )
        for n in view.nodes
    )
    return Ranking(
        view,
        lexical,
        exact_unique,
        seeds,
        _flow_ranking(states),
        iterations,
        settings,
        states,
    )


def _flow_ranking(states: tuple[PprResourceState, ...]) -> tuple[RankedResource, ...]:
    """Project positive structural flow only, with canonical address ties."""
    ordered = sorted(
        (s for s in states if s.incoming_structural_flow > 0),
        key=lambda s: (-s.incoming_structural_flow, str(s.address)),
    )
    return tuple(
        RankedResource(s.address, i, s.incoming_structural_flow, s.seed)
        for i, s in enumerate(ordered, 1)
    )


def fuse(result: Ranking) -> tuple[tuple[RepositoryResourceAddress, float], ...]:
    """Reuse production equal-view k60 RRF ordering, including missing views."""
    require_ranking(result)
    return _fused_resource_order(
        {
            m.document_statistics.analysis.document.resource.address: i
            for i, m in enumerate(result.lexical.matches, 1)
        },
        {r.address: r.rank for r in result.resources},
    )


def require_ranking(result: Ranking) -> None:
    """Check native frame, seeds, ordered ranks and stationary flow without PPR.

    This is algebraic validation, never another treatment or iterative replay.
    """
    snapshot = result.view.snapshot
    require_view(snapshot, result.view)
    if result.seeds != seed_union(snapshot, result.lexical, result.exact):
        raise ValueError("Ranking personalization provenance mismatch")
    if not result.seeds and (result.resources or result.iterations):
        raise ValueError("Unseeded ranking must abstain")
    if (
        result.seeds
        and not 1 <= result.iterations <= result.settings.maximum_iterations
    ):
        raise ValueError("Invalid PPR iteration account")
    if tuple(s.address for s in result.states) != result.view.nodes or any(
        not math.isfinite(s.stationary_mass) or s.stationary_mass < 0
        for s in result.states
    ):
        raise ValueError("Invalid complete PPR state frame/mass")
    rows = {s.address: s for s in result.states}
    expected_mass = 1 if result.seeds else 0
    if not math.isclose(
        math.fsum(s.stationary_mass for s in rows.values()),
        expected_mass,
        abs_tol=1e-12,
    ):
        raise ValueError("PPR stationary mass mismatch")
    sources = {e.source for e in result.view.edges}
    dangling_mass = math.fsum(
        r.stationary_mass for r in rows.values() if r.address not in sources
    )
    incoming: dict[RepositoryResourceAddress, list[tuple[int, float]]] = {}
    for i, edge in enumerate(result.view.edges):
        flow = (
            result.settings.damping
            * rows[edge.source].stationary_mass
            * edge.probability
        )
        incoming.setdefault(edge.target, []).append((i, flow))
    for row in result.states:
        mass = 1 / len(result.seeds) if row.address in result.seeds else 0
        expected_restart = (1 - result.settings.damping) * mass
        expected_dangling = result.settings.damping * dangling_mass * mass
        expected_incoming = tuple(
            sorted(incoming.get(row.address, ()), key=lambda x: (-x[1], x[0]))
        )
        if (
            row.seed != (row.address in result.seeds)
            or row.direct_restart_mass != expected_restart
            or row.dangling_return_mass != expected_dangling
            or row.incoming != expected_incoming
            or row.incoming_structural_flow
            != math.fsum(f for _, f in expected_incoming)
            or abs(
                row.stationary_mass
                - row.direct_restart_mass
                - row.dangling_return_mass
                - math.fsum(f for _, f in row.incoming)
            )
            > 2 * result.settings.tolerance
        ):
            raise ValueError("Graph ranking stationary/provenance mismatch")
    if result.resources != _flow_ranking(result.states):
        raise ValueError(
            "Invalid graph flow membership/ranks/scores; "
            "seed-only or stationary ranking forbidden"
        )
