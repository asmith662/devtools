# Copyright (c) 2026
"""Task-relative symbol ranking and explicit maximum-symbol resource projection."""

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING, ClassVar

from devtools.context.retrieval.graph.pagerank import require_graph_view_snapshot
from devtools.context.retrieval.repository_map.relevance import (
    score_repository_map_symbols,
)

if TYPE_CHECKING:
    from devtools.context.repository.resource import RepositoryResourceAddress
    from devtools.context.repository.snapshot import (
        RepositorySnapshot,
        RepositorySnapshotId,
    )
    from devtools.context.retrieval.graph.pagerank import PythonGraphIncomingSupport
    from devtools.context.retrieval.lexical.bm25 import RepositoryTextLexicalQuery
    from devtools.context.retrieval.repository_map.importance import (
        RepositoryMapImportance,
    )
    from devtools.context.retrieval.repository_map.relevance import (
        RepositoryMapLexicalMatch,
    )
    from devtools.context.retrieval.repository_map.view import RepositoryMapSymbol


@dataclass(frozen=True, slots=True)
class RepositoryMapRankedSymbol:
    """Native importance and task relevance remain separately inspectable."""

    symbol: RepositoryMapSymbol
    rank: int
    score: float
    importance: float
    importance_rank: int | None
    lexical_rank: int | None
    lexical_match: RepositoryMapLexicalMatch | None
    incoming_supports: tuple[PythonGraphIncomingSupport, ...]


@dataclass(frozen=True, slots=True)
class RepositoryMapRankedResource:
    """Winning symbol supplies resource score; other declarations do not add mass."""

    resource_address: RepositoryResourceAddress
    rank: int
    score: float
    winning_symbol: RepositoryMapRankedSymbol


@dataclass(frozen=True, slots=True)
class RepositoryMapRankingResult:
    """Snapshot-bound ranking evidence, not a selected or rendered repository map."""

    snapshot_id: RepositorySnapshotId
    purpose: str
    query: RepositoryTextLexicalQuery
    importance: RepositoryMapImportance
    symbols: tuple[RepositoryMapRankedSymbol, ...]
    resources: tuple[RepositoryMapRankedResource, ...]

    MECHANISM: ClassVar[str] = "symbol-bm25-global-importance-rrf60-max-resource-v1"


def rank_repository_map(
    snapshot: RepositorySnapshot,
    *,
    purpose: str,
    query: RepositoryTextLexicalQuery,
    importance: RepositoryMapImportance,
) -> RepositoryMapRankingResult:
    """Combine positive symbol BM25 and global symbol importance by equal RRF.

    A task with no symbol lexical support abstains. Otherwise global-only symbols
    remain explicitly visible as structural candidates. No resource BM25 score
    enters this channel. Ties use lexical rank, then canonical symbol identity.
    """
    if not purpose.strip():
        msg = "Repository map ranking requires a nonempty purpose."
        raise ValueError(msg)
    require_graph_view_snapshot(snapshot, importance.view.dependencies)
    lexical = score_repository_map_symbols(importance.view, query=query)
    by_node = {
        item.node: (item, supports)
        for item, supports in zip(
            importance.node_scores,
            importance.incoming_supports,
            strict=True,
        )
    }
    if (
        tuple(item.node for item in importance.node_scores)
        != importance.view.dependencies.nodes
    ):
        msg = "Repository map importance scores differ from view nodes."
        raise ValueError(msg)
    positive = sorted(
        (
            symbol
            for symbol in importance.view.symbols
            if by_node[symbol.node][0].score > 0
        ),
        key=lambda symbol: (-by_node[symbol.node][0].score, symbol.node.identity),
    )
    importance_ranks = {symbol.node: rank for rank, symbol in enumerate(positive, 1)}
    lexical_ranks = {
        item.symbol.node: (rank, item) for rank, item in enumerate(lexical, 1)
    }
    scored = []
    for symbol in importance.view.symbols if lexical else ():
        structural_rank = importance_ranks.get(symbol.node)
        match = lexical_ranks.get(symbol.node)
        score = (1 / (60 + structural_rank) if structural_rank else 0) + (
            1 / (60 + match[0]) if match else 0
        )
        if score > 0:
            scored.append((symbol, score, structural_rank, match))
    scored.sort(
        key=lambda row: (
            -row[1],
            row[3][0] if row[3] else float("inf"),
            row[0].node.identity,
        ),
    )
    symbols = tuple(
        RepositoryMapRankedSymbol(
            symbol,
            rank,
            score,
            by_node[symbol.node][0].score,
            structural_rank,
            match[0] if match else None,
            match[1] if match else None,
            by_node[symbol.node][1],
        )
        for rank, (symbol, score, structural_rank, match) in enumerate(scored, 1)
    )
    winners: dict[RepositoryResourceAddress, RepositoryMapRankedSymbol] = {}
    for item in symbols:
        winners.setdefault(item.symbol.node.resource_address, item)
    resources = tuple(
        RepositoryMapRankedResource(address, rank, winner.score, winner)
        for rank, (address, winner) in enumerate(
            sorted(
                winners.items(),
                key=lambda row: (
                    -row[1].score,
                    row[1].lexical_rank or float("inf"),
                    str(row[0]),
                ),
            ),
            1,
        )
    )
    return RepositoryMapRankingResult(
        snapshot.id,
        purpose,
        query,
        importance,
        symbols,
        resources,
    )
