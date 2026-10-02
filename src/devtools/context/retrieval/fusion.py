# Copyright (c) 2026
# ruff: noqa: COM812
"""Deterministic rank-level fusion preserving lexical and graph evidence."""

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING, ClassVar

from devtools.context.retrieval.composition import require_lexical_result_snapshot

if TYPE_CHECKING:
    from devtools.context.repository.resource import RepositoryResourceAddress
    from devtools.context.repository.snapshot import (
        RepositorySnapshot,
        RepositorySnapshotId,
    )
    from devtools.context.retrieval.graph.pagerank import (
        PythonGraphRankedResource,
        PythonGraphRankingResult,
    )
    from devtools.context.retrieval.lexical.bm25 import (
        RepositoryTextLexicalBm25Match,
        RepositoryTextLexicalBm25RetrievalResult,
    )
    from devtools.context.retrieval.repository_map.ranking import (
        RepositoryMapRankedResource,
        RepositoryMapRankingResult,
    )


@dataclass(frozen=True, slots=True)
class LexicalGraphFusedResource:
    """One resource with native channel evidence and rank-level fusion score."""

    resource_address: RepositoryResourceAddress
    rank: int
    score: float
    lexical_rank: int | None
    lexical_match: RepositoryTextLexicalBm25Match | None
    graph_rank: int | None
    graph_evidence: PythonGraphRankedResource | None


@dataclass(frozen=True, slots=True)
class LexicalGraphFusionResult:
    """Ranked resource evidence with both original retrieval results retained."""

    snapshot_id: RepositorySnapshotId
    purpose: str
    lexical_result: RepositoryTextLexicalBm25RetrievalResult
    graph_result: PythonGraphRankingResult
    resources: tuple[LexicalGraphFusedResource, ...]

    FUSION: ClassVar[str] = "equal-channel-rrf-k60-v1"


def fuse_lexical_graph_rankings(
    snapshot: RepositorySnapshot,
    *,
    purpose: str,
    lexical_result: RepositoryTextLexicalBm25RetrievalResult,
    graph_result: PythonGraphRankingResult,
) -> LexicalGraphFusionResult:
    """Apply equal-channel RRF without mixing BM25 and PPR score scales.

    A missing channel contributes zero. The graph's lexical seeds cause channel
    dependence, so this is a transparent rank combination rather than proof of
    independent corroboration. The input rankings are retained for comparison.
    """
    if not purpose.strip() or graph_result.purpose != purpose:
        msg = "Fusion requires the same nonempty purpose as graph ranking."
        raise ValueError(msg)
    if (
        graph_result.snapshot_id != snapshot.id
        or graph_result.lexical_result is not lexical_result
    ):
        msg = "Fusion requires graph ranking from this snapshot and lexical result."
        raise ValueError(msg)
    require_lexical_result_snapshot(snapshot, lexical_result)
    lexical = {
        match.document_statistics.analysis.document.resource.address: (rank, match)
        for rank, match in enumerate(lexical_result.matches, start=1)
    }
    graph = {item.resource_address: item for item in graph_result.resources}
    scored = tuple(
        (address, score, lexical.get(address), graph.get(address))
        for address, score in _fused_resource_order(
            {address: item[0] for address, item in lexical.items()},
            {address: item.rank for address, item in graph.items()},
        )
    )
    resources = tuple(
        LexicalGraphFusedResource(
            address,
            rank,
            score,
            lexical_item[0] if lexical_item else None,
            lexical_item[1] if lexical_item else None,
            graph_item.rank if graph_item else None,
            graph_item,
        )
        for rank, (address, score, lexical_item, graph_item) in enumerate(
            scored, start=1
        )
    )
    return LexicalGraphFusionResult(
        snapshot.id, purpose, lexical_result, graph_result, resources
    )


@dataclass(frozen=True, slots=True)
class LexicalRepositoryMapFusedResource:
    """Preserve both lexical and repository-map native evidence."""

    resource_address: RepositoryResourceAddress
    rank: int
    score: float
    lexical_rank: int | None
    lexical_match: RepositoryTextLexicalBm25Match | None
    map_evidence: RepositoryMapRankedResource | None


@dataclass(frozen=True, slots=True)
class LexicalRepositoryMapFusionResult:
    """Equal-channel rank combination distinct from either native channel."""

    snapshot_id: RepositorySnapshotId
    purpose: str
    lexical_result: RepositoryTextLexicalBm25RetrievalResult
    map_result: RepositoryMapRankingResult
    resources: tuple[LexicalRepositoryMapFusedResource, ...]

    FUSION: ClassVar[str] = "equal-channel-rrf-k60-v1"


def fuse_lexical_repository_map_rankings(
    snapshot: RepositorySnapshot,
    *,
    purpose: str,
    lexical_result: RepositoryTextLexicalBm25RetrievalResult,
    map_result: RepositoryMapRankingResult,
) -> LexicalRepositoryMapFusionResult:
    """Fuse resource ranks without adding BM25 scores to structural masses."""
    if not purpose.strip() or map_result.purpose != purpose:
        msg = "Fusion requires the same nonempty purpose as repository map ranking."
        raise ValueError(msg)
    if (
        map_result.snapshot_id != snapshot.id
        or map_result.query != lexical_result.query
    ):
        msg = "Fusion requires repository map ranking from this snapshot and query."
        raise ValueError(msg)
    require_lexical_result_snapshot(snapshot, lexical_result)
    lexical = {
        match.document_statistics.analysis.document.resource.address: (rank, match)
        for rank, match in enumerate(lexical_result.matches, 1)
    }
    structural = {item.resource_address: item for item in map_result.resources}
    resources = tuple(
        LexicalRepositoryMapFusedResource(
            address,
            rank,
            score,
            lexical[address][0] if address in lexical else None,
            lexical[address][1] if address in lexical else None,
            structural.get(address),
        )
        for rank, (address, score) in enumerate(
            _fused_resource_order(
                {address: item[0] for address, item in lexical.items()},
                {address: item.rank for address, item in structural.items()},
            ),
            1,
        )
    )
    return LexicalRepositoryMapFusionResult(
        snapshot.id, purpose, lexical_result, map_result, resources
    )


def _fused_resource_order(
    lexical: dict[RepositoryResourceAddress, int],
    structural: dict[RepositoryResourceAddress, int],
) -> tuple[tuple[RepositoryResourceAddress, float], ...]:
    scored = (
        (
            address,
            (1 / (60 + lexical[address]) if address in lexical else 0)
            + (1 / (60 + structural[address]) if address in structural else 0),
        )
        for address in lexical.keys() | structural.keys()
    )
    return tuple(
        sorted(
            scored,
            key=lambda row: (-row[1], lexical.get(row[0], float("inf")), str(row[0])),
        )
    )
