# Copyright (c) 2026
"""Independent filename-stem lexical field state for repository retrieval."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import PurePosixPath
from typing import TYPE_CHECKING, ClassVar

from devtools.context.retrieval.lexical.analysis import (
    RepositoryTextLexicalObservation,
    iter_lexical_spans,
)
from devtools.context.retrieval.lexical.scoring import (
    calculate_bm25_inverse_document_frequency,
    calculate_bm25_term_contribution,
)

if TYPE_CHECKING:
    from devtools.context.repository.document import (
        RepositoryTextDocument,
        RepositoryTextDocumentCollection,
    )
    from devtools.context.retrieval.lexical.bm25 import (
        RepositoryTextLexicalBm25Settings,
        RepositoryTextLexicalQuery,
    )


@dataclass(frozen=True, slots=True)
class RepositoryTextFilenameLexicalDocumentAnalysis:
    """Retain filename-stem observations for one exact repository text document."""

    document: RepositoryTextDocument
    filename_stem: str
    observations: tuple[RepositoryTextLexicalObservation, ...]

    ANALYSIS_SEMANTICS: ClassVar[str] = "filename-stem-unicode-word-span-casefold-v1"


@dataclass(frozen=True, slots=True)
class RepositoryTextFilenameLexicalTermFrequency:
    """Retain one filename-field term and its exact lexical observations."""

    normalized_term: str
    observations: tuple[RepositoryTextLexicalObservation, ...]

    @property
    def frequency(self) -> int:
        """Return occurrences of this term in one filename stem."""
        return len(self.observations)


@dataclass(frozen=True, slots=True)
class RepositoryTextFilenameLexicalDocumentStatistics:
    """Retain filename-field length and term frequencies for one document."""

    analysis: RepositoryTextFilenameLexicalDocumentAnalysis
    document_length: int
    term_frequencies: tuple[RepositoryTextFilenameLexicalTermFrequency, ...]


@dataclass(frozen=True, slots=True)
class RepositoryTextFilenameLexicalDocumentFrequency:
    """Retain the count of filename stems containing one normalized term."""

    normalized_term: str
    document_frequency: int


@dataclass(frozen=True, slots=True)
class RepositoryTextFilenameLexicalPosting:
    """Retain one filename term's exact document-local evidence."""

    normalized_term: str
    document_statistics: RepositoryTextFilenameLexicalDocumentStatistics
    term_frequency: RepositoryTextFilenameLexicalTermFrequency


@dataclass(frozen=True, slots=True)
class RepositoryTextFilenameLexicalTermPostings:
    """Retain document-ordered filename postings for one normalized term."""

    normalized_term: str
    postings: tuple[RepositoryTextFilenameLexicalPosting, ...]


@dataclass(frozen=True, slots=True)
class RepositoryTextFilenameLexicalIndex:
    """Retain independently derived filename-field statistics and postings."""

    document_collection: RepositoryTextDocumentCollection
    document_statistics: tuple[RepositoryTextFilenameLexicalDocumentStatistics, ...]
    document_frequencies: tuple[RepositoryTextFilenameLexicalDocumentFrequency, ...]
    term_postings: tuple[RepositoryTextFilenameLexicalTermPostings, ...]
    average_document_length: float

    INDEX_SEMANTICS: ClassVar[str] = "filename-stem-bm25-field-v1"


@dataclass(frozen=True, slots=True)
class RepositoryTextFilenameLexicalBm25TermContribution:
    """Explain one filename-field BM25 contribution to one document score."""

    normalized_term: str
    term_frequency: int
    document_frequency: int
    inverse_document_frequency: float
    document_length: int
    average_document_length: float
    contribution: float


def build_repository_text_filename_lexical_index(
    *,
    document_collection: RepositoryTextDocumentCollection,
) -> RepositoryTextFilenameLexicalIndex:
    """Build independent filename-stem lexical state without content inspection."""
    document_statistics = tuple(
        _document_statistics(document=document)
        for document in document_collection.documents
    )
    frequency_counts: dict[str, int] = {}
    postings_by_term: dict[str, list[RepositoryTextFilenameLexicalPosting]] = {}
    for statistics in document_statistics:
        for term_frequency in statistics.term_frequencies:
            term = term_frequency.normalized_term
            frequency_counts[term] = frequency_counts.get(term, 0) + 1
            postings_by_term.setdefault(term, []).append(
                RepositoryTextFilenameLexicalPosting(
                    normalized_term=term,
                    document_statistics=statistics,
                    term_frequency=term_frequency,
                ),
            )
    return RepositoryTextFilenameLexicalIndex(
        document_collection=document_collection,
        document_statistics=document_statistics,
        document_frequencies=tuple(
            RepositoryTextFilenameLexicalDocumentFrequency(
                normalized_term=term,
                document_frequency=frequency,
            )
            for term, frequency in frequency_counts.items()
        ),
        term_postings=tuple(
            RepositoryTextFilenameLexicalTermPostings(
                normalized_term=term,
                postings=tuple(postings),
            )
            for term, postings in postings_by_term.items()
        ),
        average_document_length=(
            sum(item.document_length for item in document_statistics)
            / len(document_statistics)
            if document_statistics
            else 0.0
        ),
    )


def score_repository_text_filename_lexical_bm25(
    *,
    query: RepositoryTextLexicalQuery,
    index: RepositoryTextFilenameLexicalIndex,
    settings: RepositoryTextLexicalBm25Settings,
) -> dict[
    int,
    tuple[RepositoryTextFilenameLexicalBm25TermContribution, ...],
]:
    """Score filename-field postings with the existing Okapi BM25 mechanics."""
    frequencies = {
        item.normalized_term: item.document_frequency
        for item in index.document_frequencies
    }
    postings = {item.normalized_term: item.postings for item in index.term_postings}
    contributions: dict[
        int,
        list[RepositoryTextFilenameLexicalBm25TermContribution],
    ] = {}
    for term in query.normalized_terms:
        term_postings = postings.get(term)
        if term_postings is None:
            continue
        document_frequency = frequencies[term]
        inverse_document_frequency = calculate_bm25_inverse_document_frequency(
            document_count=len(index.document_statistics),
            document_frequency=document_frequency,
        )
        for posting in term_postings:
            statistics = posting.document_statistics
            contribution = calculate_bm25_term_contribution(
                term_frequency=posting.term_frequency.frequency,
                inverse_document_frequency=inverse_document_frequency,
                document_length=statistics.document_length,
                average_document_length=index.average_document_length,
                settings=settings,
            )
            contributions.setdefault(id(statistics.analysis.document), []).append(
                RepositoryTextFilenameLexicalBm25TermContribution(
                    normalized_term=term,
                    term_frequency=posting.term_frequency.frequency,
                    document_frequency=document_frequency,
                    inverse_document_frequency=inverse_document_frequency,
                    document_length=statistics.document_length,
                    average_document_length=index.average_document_length,
                    contribution=contribution,
                ),
            )
    return {key: tuple(value) for key, value in contributions.items()}


def _document_statistics(
    *,
    document: RepositoryTextDocument,
) -> RepositoryTextFilenameLexicalDocumentStatistics:
    """Analyze one filename stem using the baseline lexical span semantics."""
    address = document.resource.address.value
    stem = PurePosixPath(address).stem
    observations = tuple(
        RepositoryTextLexicalObservation(
            encounter_ordinal=ordinal,
            observed_text=observed_text,
            normalized_term=normalized_term,
            start=start,
            end=end,
        )
        for ordinal, (observed_text, normalized_term, start, end) in enumerate(
            iter_lexical_spans(text=stem),
        )
    )
    by_term: dict[str, list[RepositoryTextLexicalObservation]] = {}
    for observation in observations:
        by_term.setdefault(observation.normalized_term, []).append(observation)
    return RepositoryTextFilenameLexicalDocumentStatistics(
        analysis=RepositoryTextFilenameLexicalDocumentAnalysis(
            document=document,
            filename_stem=stem,
            observations=observations,
        ),
        document_length=len(observations),
        term_frequencies=tuple(
            RepositoryTextFilenameLexicalTermFrequency(
                normalized_term=term,
                observations=tuple(items),
            )
            for term, items in by_term.items()
        ),
    )
