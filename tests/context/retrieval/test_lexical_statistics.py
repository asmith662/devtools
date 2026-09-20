# Copyright (c) 2026
"""Tests for deterministic lexical corpus statistics and inverted postings."""

from __future__ import annotations

from typing import TYPE_CHECKING

from devtools.context import (
    analyze_repository_text_document_collection,
    build_repository_text_lexical_inverted_index,
    calculate_repository_text_lexical_corpus_statistics,
)

from .test_lexical import _collection, _document

if TYPE_CHECKING:
    import pytest

    from devtools.context import RepositoryTextLexicalCollectionAnalysis


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


def test_equivalent_collection_analyses_produce_equal_statistics_and_index() -> None:
    """Immutable lexical corpus state is deterministic for equivalent input analysis."""
    first_statistics = calculate_repository_text_lexical_corpus_statistics(
        collection_analysis=_analyzed_collection(),
    )
    second_statistics = calculate_repository_text_lexical_corpus_statistics(
        collection_analysis=_analyzed_collection(),
    )

    assert first_statistics == second_statistics
    assert build_repository_text_lexical_inverted_index(
        corpus_statistics=first_statistics,
    ) == build_repository_text_lexical_inverted_index(
        corpus_statistics=second_statistics,
    )


def test_inverted_index_retains_exact_document_analysis_and_observation_evidence() -> (
    None
):
    """Each posting links an indexed term to exact existing lexical evidence."""
    statistics = calculate_repository_text_lexical_corpus_statistics(
        collection_analysis=_analyzed_collection(),
    )
    index = build_repository_text_lexical_inverted_index(corpus_statistics=statistics)
    repository_postings = index.term_postings[2]

    assert index.corpus_statistics is statistics
    assert index.vocabulary == ("context", "pytest", "repository", "architecture")
    assert repository_postings.normalized_term == "repository"
    assert tuple(
        posting.document_statistics.analysis.document.resource.address.value
        for posting in repository_postings.postings
    ) == (
        "docs/architecture.md",
        "src/devtools/context/repository/corpus.py",
    )
    assert tuple(
        posting.term_frequency.frequency for posting in repository_postings.postings
    ) == (1, 2)
    assert (
        repository_postings.postings[1].document_statistics
        is statistics.document_statistics[3]
    )
    assert tuple(
        observation.observed_text
        for observation in repository_postings.postings[1].term_frequency.observations
    ) == ("repository", "repository")


def test_statistics_and_index_have_explicit_zero_semantics() -> None:
    """Empty and all-empty collections are valid, deterministic lexical corpus state."""
    expected_all_empty_document_count = 2
    empty_statistics = calculate_repository_text_lexical_corpus_statistics(
        collection_analysis=analyze_repository_text_document_collection(
            document_collection=_collection(()),
        ),
    )
    all_empty_statistics = calculate_repository_text_lexical_corpus_statistics(
        collection_analysis=analyze_repository_text_document_collection(
            document_collection=_collection(
                (
                    _document("README.md", "---"),
                    _document("docs/empty.md", "!!!"),
                ),
            ),
        ),
    )

    assert empty_statistics.document_count == 0
    assert empty_statistics.document_statistics == ()
    assert empty_statistics.document_frequencies == ()
    assert empty_statistics.average_document_length == 0.0
    assert (
        build_repository_text_lexical_inverted_index(
            corpus_statistics=empty_statistics,
        ).term_postings
        == ()
    )
    assert all_empty_statistics.document_count == expected_all_empty_document_count
    assert tuple(
        document_statistics.document_length
        for document_statistics in all_empty_statistics.document_statistics
    ) == (0, 0)
    assert all_empty_statistics.document_frequencies == ()
    assert all_empty_statistics.average_document_length == 0.0


def test_statistics_change_with_collection_without_mutating_unchanged_analysis() -> (
    None
):
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
    assert build_repository_text_lexical_inverted_index(
        corpus_statistics=first_statistics,
    ) != build_repository_text_lexical_inverted_index(
        corpus_statistics=second_statistics,
    )


def test_statistics_and_index_perform_no_retokenization_or_external_work(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Statistics consume analyses only and indexing consumes statistics only."""
    collection_analysis = _analyzed_collection()

    def fail(*_args: object, **_kwargs: object) -> None:
        msg = "Lexical statistics and indexing must not perform unrelated work."
        raise AssertionError(msg)

    monkeypatch.setattr(
        "devtools.context.retrieval.lexical.analyze_repository_text_document",
        fail,
    )
    monkeypatch.setattr("devtools.context.repository.observation.read", fail)
    monkeypatch.setattr(
        "devtools.context.repository.discovery.discover_repository_resource_addresses",
        fail,
    )
    monkeypatch.setattr("devtools.context.python.function.declarations.ast.parse", fail)

    statistics = calculate_repository_text_lexical_corpus_statistics(
        collection_analysis=collection_analysis,
    )
    index = build_repository_text_lexical_inverted_index(corpus_statistics=statistics)

    assert index.vocabulary == ("context", "pytest", "repository", "architecture")


def test_statistics_and_index_expose_no_query_scoring_or_retrieval_state() -> None:
    """The new values retain corpus lexical state, not BM25 or retrieval behavior."""
    statistics = calculate_repository_text_lexical_corpus_statistics(
        collection_analysis=_analyzed_collection(),
    )
    index = build_repository_text_lexical_inverted_index(corpus_statistics=statistics)

    assert all(
        not hasattr(value, attribute)
        for value in (statistics, index)
        for attribute in (
            "query",
            "idf",
            "bm25",
            "score",
            "rank",
            "results",
            "retrieval",
        )
    )


def test_paths_are_not_indexed_unless_present_in_document_content() -> None:
    """Address correlation remains separate from content-only lexical indexing."""
    statistics = calculate_repository_text_lexical_corpus_statistics(
        collection_analysis=analyze_repository_text_document_collection(
            document_collection=_collection(
                (_document("src/path_only.py", "repository content"),),
            ),
        ),
    )
    index = build_repository_text_lexical_inverted_index(corpus_statistics=statistics)

    assert index.vocabulary == ("repository", "content")
