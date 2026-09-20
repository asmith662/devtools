# Copyright (c) 2026
"""Deterministic cross-document statistics over lexical document analyses."""

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING, ClassVar

if TYPE_CHECKING:
    from devtools.context.retrieval.lexical import (
        RepositoryTextLexicalCollectionAnalysis,
        RepositoryTextLexicalDocumentAnalysis,
        RepositoryTextLexicalObservation,
    )


@dataclass(frozen=True, slots=True)
class RepositoryTextLexicalTermFrequency:
    """Retain one document-local normalized term and its exact observations."""

    normalized_term: str
    observations: tuple[RepositoryTextLexicalObservation, ...]

    @property
    def frequency(self) -> int:
        """Return the number of observations of this term in the document."""
        return len(self.observations)


@dataclass(frozen=True, slots=True)
class RepositoryTextLexicalDocumentStatistics:
    """Retain lexical length and term frequencies for one document analysis."""

    analysis: RepositoryTextLexicalDocumentAnalysis
    document_length: int
    term_frequencies: tuple[RepositoryTextLexicalTermFrequency, ...]


@dataclass(frozen=True, slots=True)
class RepositoryTextLexicalDocumentFrequency:
    """Retain the number of distinct documents containing one normalized term."""

    normalized_term: str
    document_frequency: int


@dataclass(frozen=True, slots=True)
class RepositoryTextLexicalCorpusStatistics:
    """Retain deterministic corpus-level lexical counts without scoring behavior."""

    collection_analysis: RepositoryTextLexicalCollectionAnalysis
    document_statistics: tuple[RepositoryTextLexicalDocumentStatistics, ...]
    document_frequencies: tuple[RepositoryTextLexicalDocumentFrequency, ...]
    document_count: int
    average_document_length: float

    STATISTICS_SEMANTICS: ClassVar[str] = "observation-count-frequency-v1"


def calculate_repository_text_lexical_corpus_statistics(
    *,
    collection_analysis: RepositoryTextLexicalCollectionAnalysis,
) -> RepositoryTextLexicalCorpusStatistics:
    """Calculate deterministic lexical counts from existing document observations."""
    document_statistics = tuple(
        _calculate_document_statistics(analysis=analysis)
        for analysis in collection_analysis.analyses
    )
    document_count = len(document_statistics)
    total_document_length = sum(
        statistics.document_length for statistics in document_statistics
    )
    average_document_length = (
        total_document_length / document_count if document_count else 0.0
    )
    document_frequency_counts: dict[str, int] = {}
    for statistics in document_statistics:
        for term_frequency in statistics.term_frequencies:
            term = term_frequency.normalized_term
            document_frequency_counts[term] = document_frequency_counts.get(term, 0) + 1

    return RepositoryTextLexicalCorpusStatistics(
        collection_analysis=collection_analysis,
        document_statistics=document_statistics,
        document_frequencies=tuple(
            RepositoryTextLexicalDocumentFrequency(
                normalized_term=term,
                document_frequency=frequency,
            )
            for term, frequency in document_frequency_counts.items()
        ),
        document_count=document_count,
        average_document_length=average_document_length,
    )


def _calculate_document_statistics(
    *,
    analysis: RepositoryTextLexicalDocumentAnalysis,
) -> RepositoryTextLexicalDocumentStatistics:
    """Count one document's pre-existing observations in encounter-term order."""
    observations_by_term: dict[str, list[RepositoryTextLexicalObservation]] = {}
    for observation in analysis.observations:
        observations_by_term.setdefault(observation.normalized_term, []).append(
            observation,
        )
    return RepositoryTextLexicalDocumentStatistics(
        analysis=analysis,
        document_length=len(analysis.observations),
        term_frequencies=tuple(
            RepositoryTextLexicalTermFrequency(
                normalized_term=term,
                observations=tuple(observations),
            )
            for term, observations in observations_by_term.items()
        ),
    )
