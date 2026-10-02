# Copyright (c) 2026
"""Symbol/path BM25 over compact RI metadata using canonical lexical mechanics."""

from __future__ import annotations

from collections import Counter
from dataclasses import dataclass
from typing import TYPE_CHECKING

from devtools.context.retrieval.lexical.analysis import iter_lexical_spans
from devtools.context.retrieval.lexical.bm25 import RepositoryTextLexicalBm25Settings
from devtools.context.retrieval.lexical.scoring import (
    calculate_bm25_inverse_document_frequency,
    calculate_bm25_term_contribution,
)

if TYPE_CHECKING:
    from devtools.context.retrieval.lexical.bm25 import RepositoryTextLexicalQuery
    from devtools.context.retrieval.repository_map.view import (
        RepositoryMapSymbol,
        RepositoryMapView,
    )


@dataclass(frozen=True, slots=True)
class RepositoryMapLexicalMatch:
    """Keep compact metadata, query term contributions, and native BM25 score."""

    symbol: RepositoryMapSymbol
    metadata: str
    score: float
    term_contributions: tuple[tuple[str, float], ...]


_DEFAULT_SETTINGS = RepositoryTextLexicalBm25Settings()


def score_repository_map_symbols(
    view: RepositoryMapView,
    *,
    query: RepositoryTextLexicalQuery,
    settings: RepositoryTextLexicalBm25Settings = _DEFAULT_SETTINGS,
) -> tuple[RepositoryMapLexicalMatch, ...]:
    """Score names, direct class qualification and paths; exclude declaration bodies.

    No inferred module qualification, identifier splitting, stopword system, or
    second tokenizer is introduced. Scores are symbol-corpus BM25, not resource
    BM25; the two corpora have different statistics.
    """
    metadata = tuple(
        f"{item.qualified_name} {item.node.resource_address}" for item in view.symbols
    )
    frequencies = tuple(
        Counter(term for _, term, _, _ in iter_lexical_spans(text=text))
        for text in metadata
    )
    document_frequency = Counter(term for counts in frequencies for term in counts)
    lengths = tuple(sum(counts.values()) for counts in frequencies)
    average = sum(lengths) / len(lengths) if lengths else 0.0
    matches = []
    for symbol, text, counts, length in zip(
        view.symbols,
        metadata,
        frequencies,
        lengths,
        strict=True,
    ):
        contributions = tuple(
            (
                term,
                calculate_bm25_term_contribution(
                    term_frequency=counts[term],
                    inverse_document_frequency=calculate_bm25_inverse_document_frequency(
                        document_count=len(view.symbols),
                        document_frequency=document_frequency[term],
                    ),
                    document_length=length,
                    average_document_length=average,
                    settings=settings,
                ),
            )
            for term in query.normalized_terms
            if counts[term]
        )
        score = sum(value for _, value in contributions)
        if score > 0:
            matches.append(
                RepositoryMapLexicalMatch(symbol, text, score, contributions),
            )
    return tuple(
        sorted(matches, key=lambda item: (-item.score, item.symbol.node.identity)),
    )
