# Copyright (c) 2026
"""Tests for cross-document lexical statistics."""

from __future__ import annotations

from devtools.context.retrieval.lexical.analysis import (
    RepositoryTextLexicalCollectionAnalysis,
    analyze_repository_text_document_collection,
)
from devtools.context.retrieval.lexical.statistics import (
    calculate_repository_text_lexical_corpus_statistics,
)

from ._helpers import _collection, _document


def _analyzed_collection() -> RepositoryTextLexicalCollectionAnalysis:
    """Build a heterogeneous collection with controlled lexical overlap."""
    return analyze_repository_text_document_collection(
        document_collection=_collection(
            (
                _document(
                    "src/devtools/context/repository/corpus.py",
                    "repository context repository",
                ),
                _document("docs/architecture.md", "repository architecture"),
                _document("pyproject.toml", ""),
                _document("config/example.yaml", "context pytest pytest"),
            ),
        ),
    )


def test_statistics_establish_document_counts_lengths_and_average() -> None:
    """Corpus statistics count all documents and every lexical observation."""
    expected_document_count = 4
    expected_average_document_length = 2.0
    statistics = calculate_repository_text_lexical_corpus_statistics(
        collection_analysis=_analyzed_collection(),
    )

    assert statistics.document_count == expected_document_count
    assert tuple(
        document_statistics.document_length
        for document_statistics in statistics.document_statistics
    ) == (3, 2, 0, 3)
    assert statistics.average_document_length == expected_average_document_length


def test_statistics_preserve_term_frequency_and_distinct_document_frequency() -> None:
    """Repeated observations count once for DF but repeatedly for document TF."""
    statistics = calculate_repository_text_lexical_corpus_statistics(
        collection_analysis=_analyzed_collection(),
    )

    assert [
        (term.normalized_term, term.document_frequency)
        for term in statistics.document_frequencies
    ] == [
        ("context", 2),
        ("pytest", 1),
        ("repository", 2),
        ("architecture", 1),
    ]
    first_document_terms = statistics.document_statistics[0].term_frequencies
    assert [
        (term.normalized_term, term.frequency) for term in first_document_terms
    ] == [("context", 1), ("pytest", 2)]
    assert tuple(
        observation.normalized_term
        for observation in first_document_terms[1].observations
    ) == ("pytest", "pytest")


def test_empty_statistics_have_explicit_zero_semantics() -> None:
    """Empty and all-empty collections retain documents and a zero average."""
    expected_all_empty_document_count = 2
    empty_statistics = calculate_repository_text_lexical_corpus_statistics(
        collection_analysis=analyze_repository_text_document_collection(
            document_collection=_collection(()),
        ),
    )
    all_empty_statistics = calculate_repository_text_lexical_corpus_statistics(
        collection_analysis=analyze_repository_text_document_collection(
            document_collection=_collection(
                (_document("README.md", "---"), _document("docs/empty.md", "!!!")),
            ),
        ),
    )

    assert empty_statistics.document_count == 0
    assert empty_statistics.document_statistics == ()
    assert empty_statistics.document_frequencies == ()
    assert empty_statistics.average_document_length == 0.0
    assert all_empty_statistics.document_count == expected_all_empty_document_count
    assert tuple(
        document_statistics.document_length
        for document_statistics in all_empty_statistics.document_statistics
    ) == (0, 0)
    assert all_empty_statistics.document_frequencies == ()
    assert all_empty_statistics.average_document_length == 0.0


def test_statistics_change_with_collection_and_preserve_unchanged_analysis() -> None:
    """Cross-document state changes without changing an unchanged analysis."""
    unchanged = _document("README.md", "repository context")
    first_collection = analyze_repository_text_document_collection(
        document_collection=_collection((unchanged, _document("other.txt", "alpha"))),
    )
    second_collection = analyze_repository_text_document_collection(
        document_collection=_collection(
            (unchanged, _document("other.txt", "beta beta")),
        ),
    )
    first_statistics = calculate_repository_text_lexical_corpus_statistics(
        collection_analysis=first_collection,
    )
    second_statistics = calculate_repository_text_lexical_corpus_statistics(
        collection_analysis=second_collection,
    )

    assert first_collection.analyses[0] == second_collection.analyses[0]
    assert first_statistics != second_statistics
