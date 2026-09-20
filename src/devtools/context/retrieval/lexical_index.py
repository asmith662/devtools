# Copyright (c) 2026
"""Deterministic inverted lexical index over corpus lexical statistics."""

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING, ClassVar

if TYPE_CHECKING:
    from devtools.context.retrieval.lexical_statistics import (
        RepositoryTextLexicalCorpusStatistics,
        RepositoryTextLexicalDocumentStatistics,
        RepositoryTextLexicalTermFrequency,
    )


@dataclass(frozen=True, slots=True)
class RepositoryTextLexicalPosting:
    """Retain one term's exact document-local lexical evidence."""

    normalized_term: str
    document_statistics: RepositoryTextLexicalDocumentStatistics
    term_frequency: RepositoryTextLexicalTermFrequency


@dataclass(frozen=True, slots=True)
class RepositoryTextLexicalTermPostings:
    """Retain ordered postings for one normalized lexical term."""

    normalized_term: str
    postings: tuple[RepositoryTextLexicalPosting, ...]


@dataclass(frozen=True, slots=True)
class RepositoryTextLexicalInvertedIndex:
    """Retain deterministic content-term postings without query or ranking behavior."""

    corpus_statistics: RepositoryTextLexicalCorpusStatistics
    term_postings: tuple[RepositoryTextLexicalTermPostings, ...]

    INDEX_SEMANTICS: ClassVar[str] = "document-order-inverted-postings-v1"

    @property
    def vocabulary(self) -> tuple[str, ...]:
        """Return normalized terms in first corpus encounter order."""
        return tuple(
            term_postings.normalized_term for term_postings in self.term_postings
        )


def build_repository_text_lexical_inverted_index(
    *,
    corpus_statistics: RepositoryTextLexicalCorpusStatistics,
) -> RepositoryTextLexicalInvertedIndex:
    """Build deterministic postings from precomputed lexical corpus statistics."""
    postings_by_term: dict[str, list[RepositoryTextLexicalPosting]] = {}
    for document_statistics in corpus_statistics.document_statistics:
        for term_frequency in document_statistics.term_frequencies:
            term = term_frequency.normalized_term
            postings_by_term.setdefault(term, []).append(
                RepositoryTextLexicalPosting(
                    normalized_term=term,
                    document_statistics=document_statistics,
                    term_frequency=term_frequency,
                ),
            )
    return RepositoryTextLexicalInvertedIndex(
        corpus_statistics=corpus_statistics,
        term_postings=tuple(
            RepositoryTextLexicalTermPostings(
                normalized_term=term,
                postings=tuple(postings),
            )
            for term, postings in postings_by_term.items()
        ),
    )
