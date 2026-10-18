# Copyright (c) 2026
"""Selectable source retrieval with native evidence and rank-only consolidation."""

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING, cast

from devtools.context.retrieval.fusion import _reciprocal_rank_score
from devtools.context.retrieval.lexical import (
    analyze_repository_text_lexical_query,
    retrieve_repository_text_documents_by_bm25,
)

if TYPE_CHECKING:
    from devtools.context.repository.resource import RepositoryResourceAddress
    from devtools.context.retrieval.lexical import (
        RepositoryTextLexicalBm25Match,
        RepositoryTextLexicalBm25RetrievalResult,
    )
    from devtools.context.retrieval.source.index import SourceSearchIndex
    from devtools.context.retrieval.source.representation import (
        RepositorySourceUnit,
        SourceRepresentation,
        SourceSearchMode,
    )


@dataclass(frozen=True, slots=True)
class SourceSearchEvidence:
    """Keep the originating population, native rank, score and full source unit."""

    view: SourceRepresentation
    rank: int
    unit: RepositorySourceUnit
    match: RepositoryTextLexicalBm25Match


@dataclass(frozen=True, slots=True)
class SourceSearchHit:
    """One primary source representation and lossless supporting retrieval evidence."""

    unit: RepositorySourceUnit
    rank: int
    score: float
    evidence: tuple[SourceSearchEvidence, ...]


@dataclass(frozen=True, slots=True)
class SourceSearchResult:
    """Retain the bound index and native results; mixed scores are k=60 RRF only."""

    index: SourceSearchIndex
    query: str
    mode: SourceSearchMode
    hits: tuple[SourceSearchHit, ...]
    native_results: tuple[RepositoryTextLexicalBm25RetrievalResult, ...]


def search_repository_source(
    index: SourceSearchIndex,
    *,
    query: str,
    mode: SourceSearchMode = "file",
    maximum_results: int = 10,
) -> SourceSearchResult:
    """Search selected populations, retaining scores in their own lexical scale.

    Mixed exact/contained evidence is folded into a narrower primary. Distinct
    symbol declarations stay independently selectable; partially overlapping
    windows retain their novel source. A broad support is assigned once to the
    highest native-ranked eligible symbol (then window), never counted twice.
    """
    if mode not in {"file", "symbol", "window", "mixed"}:
        msg = "Unknown source search mode."
        raise ValueError(msg)
    if maximum_results <= 0:
        msg = "Maximum source search results must be positive."
        raise ValueError(msg)
    analyzed = analyze_repository_text_lexical_query(text=query)
    evidence: list[SourceSearchEvidence] = []
    native_results = []
    for view in index.views:
        if mode not in {"mixed", view.kind}:
            continue
        native = retrieve_repository_text_documents_by_bm25(
            query=analyzed,
            index=view.lexical_index,
            maximum_results=max(1, len(view.units))
            if mode == "mixed"
            else maximum_results,
        )
        native_results.append(native)
        evidence.extend(
            SourceSearchEvidence(
                view.kind,
                rank,
                cast(
                    "RepositorySourceUnit",
                    match.document_statistics.analysis.document,
                ),
                match,
            )
            for rank, match in enumerate(native.matches, 1)
        )
    if mode != "mixed":
        hits = tuple(
            SourceSearchHit(item.unit, item.rank, item.match.score, (item,))
            for item in evidence
        )
    else:
        hits = _consolidate(evidence)[:maximum_results]
    return SourceSearchResult(index, query, mode, hits, tuple(native_results))


def _consolidate(evidence: list[SourceSearchEvidence]) -> tuple[SourceSearchHit, ...]:
    groups: list[list[SourceSearchEvidence]] = []
    by_resource: dict[RepositoryResourceAddress, list[list[SourceSearchEvidence]]] = {}
    for item in sorted(
        evidence,
        key=lambda e: (
            {"symbol": 0, "window": 1, "file": 2}[e.unit.kind],
            e.rank,
            e.unit.end - e.unit.start,
            str(e.unit.resource.address),
            e.unit.start,
            e.view,
        ),
    ):
        unit = item.unit
        resource_groups = by_resource.setdefault(unit.resource.address, [])
        for group in resource_groups:
            anchor = group[0].unit
            exact = (unit.start, unit.end) == (anchor.start, anchor.end)
            contained = (unit.start <= anchor.start and anchor.end <= unit.end) or (
                anchor.start <= unit.start and unit.end <= anchor.end
            )
            if exact or (contained and unit.kind != "symbol"):
                group.append(item)
                break
        else:
            group = [item]
            resource_groups.append(group)
            groups.append(group)
    scored = []
    for group in groups:
        ranks: dict[SourceRepresentation, int] = {}
        for item in group:
            if item.view == "symbol" and item.unit.kind == "file":
                continue
            ranks[item.view] = min(ranks.get(item.view, item.rank), item.rank)
        scored.append((group, _reciprocal_rank_score(*ranks.values())))
    scored.sort(
        key=lambda row: (
            -row[1],
            min(item.rank for item in row[0]),
            str(row[0][0].unit.resource.address),
            row[0][0].unit.start,
            str(row[0][0].unit.id),
        ),
    )
    return tuple(
        SourceSearchHit(group[0].unit, rank, score, tuple(group))
        for rank, (group, score) in enumerate(scored, 1)
    )
