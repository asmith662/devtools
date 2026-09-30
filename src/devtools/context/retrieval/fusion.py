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
    scored = []
    for address in lexical.keys() | graph.keys():
        lexical_item = lexical.get(address)
        graph_item = graph.get(address)
        score = (1 / (60 + lexical_item[0]) if lexical_item else 0) + (
            1 / (60 + graph_item.rank) if graph_item else 0
        )
        scored.append((address, score, lexical_item, graph_item))
    scored.sort(
        key=lambda row: (-row[1], row[2][0] if row[2] else float("inf"), str(row[0]))
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
