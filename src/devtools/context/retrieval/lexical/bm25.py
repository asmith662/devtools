# Copyright (c) 2026
"""Bounded content-only Okapi BM25 retrieval over one lexical inverted index."""

from __future__ import annotations

import math
from dataclasses import dataclass
from typing import TYPE_CHECKING, ClassVar

from devtools.context.retrieval.lexical.analysis import iter_lexical_spans

if TYPE_CHECKING:
    from devtools.context.retrieval.lexical.index import (
        RepositoryTextLexicalInvertedIndex,
    )
    from devtools.context.retrieval.lexical.statistics import (
        RepositoryTextLexicalDocumentStatistics,
    )


@dataclass(frozen=True, slots=True)
class RepositoryTextLexicalQueryObservation:
    """Record one exact lexical span observed in retrieval query text."""

    encounter_ordinal: int
    observed_text: str
    normalized_term: str
    start: int
    end: int


@dataclass(frozen=True, slots=True)
class RepositoryTextLexicalQuery:
    """Retain query text and baseline lexical observations for BM25 retrieval."""

    text: str
    observations: tuple[RepositoryTextLexicalQueryObservation, ...]

    QUERY_SEMANTICS: ClassVar[str] = "unicode-word-span-casefold-v1"

    @property
    def normalized_terms(self) -> tuple[str, ...]:
        """Return distinct normalized query terms in first encounter order."""
        return tuple(
            dict.fromkeys(
                observation.normalized_term for observation in self.observations
            ),
        )


@dataclass(frozen=True, slots=True)
class RepositoryTextLexicalBm25Settings:
    """Configure one bounded Okapi BM25 retrieval realization."""

    k1: float = 1.2
    b: float = 0.75

    def __post_init__(self) -> None:
        """Validate finite BM25 saturation and length-normalization parameters."""
        if not math.isfinite(self.k1) or self.k1 < 0:
            msg = "BM25 k1 must be finite and greater than or equal to zero."
            raise ValueError(msg)
        if not math.isfinite(self.b) or not 0 <= self.b <= 1:
            msg = "BM25 b must be finite and between zero and one."
            raise ValueError(msg)


_DEFAULT_BM25_SETTINGS = RepositoryTextLexicalBm25Settings()


@dataclass(frozen=True, slots=True)
class RepositoryTextLexicalBm25TermContribution:
    """Explain one normalized query term's contribution to a document score."""

    normalized_term: str
    term_frequency: int
    document_frequency: int
    inverse_document_frequency: float
    document_length: int
    average_document_length: float
    contribution: float


@dataclass(frozen=True, slots=True)
class RepositoryTextLexicalBm25Match:
    """Retain one positively scored document and its local BM25 evidence."""

    document_statistics: RepositoryTextLexicalDocumentStatistics
    score: float
    term_contributions: tuple[RepositoryTextLexicalBm25TermContribution, ...]


@dataclass(frozen=True, slots=True)
class RepositoryTextLexicalBm25RetrievalResult:
    """Retain bounded ranked BM25 matches for one query and lexical index."""

    query: RepositoryTextLexicalQuery
    index: RepositoryTextLexicalInvertedIndex
    settings: RepositoryTextLexicalBm25Settings
    maximum_results: int
    matches: tuple[RepositoryTextLexicalBm25Match, ...]

    RETRIEVAL_SEMANTICS: ClassVar[str] = "okapi-bm25-distinct-query-terms-v1"


def analyze_repository_text_lexical_query(
    *,
    text: str,
) -> RepositoryTextLexicalQuery:
    """Analyze query text using the exact baseline document lexical semantics."""
    return RepositoryTextLexicalQuery(
        text=text,
        observations=tuple(
            RepositoryTextLexicalQueryObservation(
                encounter_ordinal=ordinal,
                observed_text=observed_text,
                normalized_term=normalized_term,
                start=start,
                end=end,
            )
            for ordinal, (observed_text, normalized_term, start, end) in enumerate(
                iter_lexical_spans(text=text),
            )
        ),
    )


def retrieve_repository_text_documents_by_bm25(
    *,
    query: RepositoryTextLexicalQuery,
    index: RepositoryTextLexicalInvertedIndex,
    maximum_results: int,
    settings: RepositoryTextLexicalBm25Settings = _DEFAULT_BM25_SETTINGS,
) -> RepositoryTextLexicalBm25RetrievalResult:
    """Rank positive content-term matches with Okapi BM25 under an explicit bound.

    For distinct normalized query terms, this uses
    ``ln(1 + (N - df + 0.5) / (df + 0.5)) * tf * (k1 + 1) /``
    ``(tf + k1 * (1 - b + b * document_length / average_document_length))``.
    """
    if maximum_results <= 0:
        msg = "Maximum BM25 result count must be positive."
        raise ValueError(msg)

    document_positions = {
        id(document_statistics): position
        for position, document_statistics in enumerate(
            index.corpus_statistics.document_statistics,
        )
    }
    document_frequency_by_term = {
        frequency.normalized_term: frequency.document_frequency
        for frequency in index.corpus_statistics.document_frequencies
    }
    postings_by_term = {
        term_postings.normalized_term: term_postings.postings
        for term_postings in index.term_postings
    }
    contributions_by_document: dict[
        int,
        list[RepositoryTextLexicalBm25TermContribution],
    ] = {}
    for term in query.normalized_terms:
        postings = postings_by_term.get(term)
        if postings is None:
            continue
        document_frequency = document_frequency_by_term[term]
        inverse_document_frequency = _calculate_bm25_inverse_document_frequency(
            document_count=index.corpus_statistics.document_count,
            document_frequency=document_frequency,
        )
        for posting in postings:
            document_statistics = posting.document_statistics
            average_document_length = index.corpus_statistics.average_document_length
            contribution = _calculate_bm25_term_contribution(
                term_frequency=posting.term_frequency.frequency,
                inverse_document_frequency=inverse_document_frequency,
                document_length=document_statistics.document_length,
                average_document_length=average_document_length,
                settings=settings,
            )
            contributions_by_document.setdefault(id(document_statistics), []).append(
                RepositoryTextLexicalBm25TermContribution(
                    normalized_term=term,
                    term_frequency=posting.term_frequency.frequency,
                    document_frequency=document_frequency,
                    inverse_document_frequency=inverse_document_frequency,
                    document_length=document_statistics.document_length,
                    average_document_length=average_document_length,
                    contribution=contribution,
                ),
            )

    ranked_documents = sorted(
        contributions_by_document.items(),
        key=lambda item: (
            -sum(contribution.contribution for contribution in item[1]),
            document_positions[item[0]],
        ),
    )
    matches = tuple(
        RepositoryTextLexicalBm25Match(
            document_statistics=index.corpus_statistics.document_statistics[
                document_positions[document_identity]
            ],
            score=sum(contribution.contribution for contribution in contributions),
            term_contributions=tuple(contributions),
        )
        for document_identity, contributions in ranked_documents
    )
    return RepositoryTextLexicalBm25RetrievalResult(
        query=query,
        index=index,
        settings=settings,
        maximum_results=maximum_results,
        matches=matches[:maximum_results],
    )


def _calculate_bm25_inverse_document_frequency(
    *,
    document_count: int,
    document_frequency: int,
) -> float:
    """Calculate the bounded Okapi BM25 inverse-document-frequency component."""
    return math.log(
        1 + (document_count - document_frequency + 0.5) / (document_frequency + 0.5),
    )


def _calculate_bm25_term_contribution(
    *,
    term_frequency: int,
    inverse_document_frequency: float,
    document_length: int,
    average_document_length: float,
    settings: RepositoryTextLexicalBm25Settings,
) -> float:
    """Calculate one term's standard Okapi BM25 contribution."""
    numerator = term_frequency * (settings.k1 + 1)
    denominator = term_frequency + settings.k1 * (
        1 - settings.b + settings.b * document_length / average_document_length
    )
    return inverse_document_frequency * numerator / denominator
