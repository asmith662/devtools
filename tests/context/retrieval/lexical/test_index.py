# Copyright (c) 2026
"""Tests for content-only inverted lexical postings."""

from __future__ import annotations

from typing import TYPE_CHECKING

from devtools.context.retrieval.lexical.analysis import (
    RepositoryTextLexicalCollectionAnalysis,
    analyze_repository_text_document_collection,
)
from devtools.context.retrieval.lexical.index import (
    RepositoryTextLexicalInvertedIndex,
    build_repository_text_lexical_inverted_index,
)
from devtools.context.retrieval.lexical.statistics import (
    RepositoryTextLexicalCorpusStatistics,
    calculate_repository_text_lexical_corpus_statistics,
)

from ._helpers import _collection, _document

if TYPE_CHECKING:
    import pytest


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


def _statistics() -> RepositoryTextLexicalCorpusStatistics:
    """Calculate statistics for the shared deterministic test collection."""
    return calculate_repository_text_lexical_corpus_statistics(
        collection_analysis=_analyzed_collection(),
    )


def _index(
    statistics: RepositoryTextLexicalCorpusStatistics,
) -> RepositoryTextLexicalInvertedIndex:
    """Build the content-only index for one existing statistics value."""
    return build_repository_text_lexical_inverted_index(
        corpus_statistics=statistics,
    )


def test_equivalent_analyses_produce_equal_statistics_and_index() -> None:
    """Equivalent immutable inputs produce equal statistics and postings."""
    first_statistics = _statistics()
    second_statistics = _statistics()

    assert first_statistics == second_statistics
    assert _index(first_statistics) == _index(second_statistics)


def test_postings_retain_document_and_observation_evidence() -> None:
    """Each posting links a term to exact existing lexical evidence."""
    statistics = _statistics()
    index = _index(statistics)
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


def test_index_changes_with_statistics_without_mutating_analysis() -> None:
    """Changed corpus statistics produce a changed index without rewriting analysis."""
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
    assert _index(first_statistics) != _index(second_statistics)


def test_empty_index_has_no_postings() -> None:
    """An empty collection produces the existing zero-posting index."""
    statistics = calculate_repository_text_lexical_corpus_statistics(
        collection_analysis=analyze_repository_text_document_collection(
            document_collection=_collection(()),
        ),
    )

    assert (
        _index(statistics).term_postings
        == ()
    )


def test_statistics_and_index_do_not_retokenize_or_acquire_resources(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Statistics use analyses and indexing uses statistics only."""
    collection_analysis = _analyzed_collection()

    def fail(*_args: object, **_kwargs: object) -> None:
        msg = "Lexical statistics and indexing must not perform unrelated work."
        raise AssertionError(msg)

    monkeypatch.setattr(
        "devtools.context.retrieval.lexical.analysis.analyze_repository_text_document",
        fail,
    )
    monkeypatch.setattr("devtools.context.repository.observation.read", fail)
    monkeypatch.setattr(
        "devtools.context.repository.discovery.discover_repository_resource_addresses",
        fail,
    )
    monkeypatch.setattr(
        "devtools.context.python.function.declarations.ast.parse",
        fail,
    )

    statistics = calculate_repository_text_lexical_corpus_statistics(
        collection_analysis=collection_analysis,
    )
    index = _index(statistics)

    assert index.vocabulary == ("context", "pytest", "repository", "architecture")


def test_statistics_and_index_expose_no_query_scoring_or_retrieval_state() -> None:
    """Corpus lexical values do not carry query, score, rank, or retrieval state."""
    statistics = _statistics()
    index = _index(statistics)

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
    """Address correlation stays separate from content-only lexical indexing."""
    statistics = calculate_repository_text_lexical_corpus_statistics(
        collection_analysis=analyze_repository_text_document_collection(
            document_collection=_collection(
                (_document("src/path_only.py", "repository content"),),
            ),
        ),
    )
    index = _index(statistics)

    assert index.vocabulary == ("repository", "content")
