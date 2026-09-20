# Copyright (c) 2026
"""Tests for bounded content-only Okapi BM25 lexical retrieval."""

from __future__ import annotations

import math
from typing import TYPE_CHECKING

import pytest

from devtools.context.retrieval.lexical.analysis import (
    analyze_repository_text_document_collection,
)
from devtools.context.retrieval.lexical.bm25 import (
    RepositoryTextLexicalBm25Settings,
    analyze_repository_text_lexical_query,
    retrieve_repository_text_documents_by_bm25,
)
from devtools.context.retrieval.lexical.index import (
    RepositoryTextLexicalInvertedIndex,
    build_repository_text_lexical_inverted_index,
)
from devtools.context.retrieval.lexical.statistics import (
    calculate_repository_text_lexical_corpus_statistics,
)

from ._helpers import _collection, _document

if TYPE_CHECKING:
    from devtools.context.retrieval.lexical.bm25 import (
        RepositoryTextLexicalBm25RetrievalResult,
        RepositoryTextLexicalQuery,
    )


def _index() -> RepositoryTextLexicalInvertedIndex:
    """Build a heterogeneous controlled corpus index for BM25 tests."""
    collection_analysis = analyze_repository_text_document_collection(
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
    return build_repository_text_lexical_inverted_index(
        corpus_statistics=calculate_repository_text_lexical_corpus_statistics(
            collection_analysis=collection_analysis,
        ),
    )


def _retrieve(
    query: str | RepositoryTextLexicalQuery,
    *,
    index: RepositoryTextLexicalInvertedIndex | None = None,
    maximum_results: int = 10,
    settings: RepositoryTextLexicalBm25Settings | None = None,
) -> RepositoryTextLexicalBm25RetrievalResult:
    """Analyze text when needed and execute the bounded lexical retrieval."""
    analyzed_query = (
        analyze_repository_text_lexical_query(text=query)
        if isinstance(query, str)
        else query
    )
    return retrieve_repository_text_documents_by_bm25(
        query=analyzed_query,
        index=_index() if index is None else index,
        maximum_results=maximum_results,
        settings=RepositoryTextLexicalBm25Settings() if settings is None else settings,
    )


def test_query_uses_baseline_lexical_spans_and_retains_repeated_evidence() -> None:
    """Query lexicalization matches document rules without treating it as a document."""
    query = analyze_repository_text_lexical_query(
        text="REPOSITORY repository foo-bar Straße",
    )

    assert query.text == "REPOSITORY repository foo-bar Straße"
    assert tuple(observation.observed_text for observation in query.observations) == (
        "REPOSITORY",
        "repository",
        "foo",
        "bar",
        "Straße",
    )
    assert tuple(observation.normalized_term for observation in query.observations) == (
        "repository",
        "repository",
        "foo",
        "bar",
        "strasse",
    )
    assert query.normalized_terms == ("repository", "foo", "bar", "strasse")
    assert tuple(
        observation.encounter_ordinal for observation in query.observations
    ) == (
        0,
        1,
        2,
        3,
        4,
    )


def test_manual_okapi_bm25_score_and_contribution_evidence() -> None:
    """One score independently verifies the documented Okapi BM25 formula."""
    expected_term_frequency = 2
    expected_document_frequency = 2
    expected_document_length = 3
    expected_average_document_length = 2.0
    settings = RepositoryTextLexicalBm25Settings()
    result = _retrieve("repository", settings=settings)
    match = result.matches[0]
    contribution = match.term_contributions[0]
    expected_idf = math.log(
        1
        + (4 - expected_document_frequency + 0.5)
        / (expected_document_frequency + 0.5),
    )
    expected_contribution = expected_idf * (
        expected_term_frequency * (settings.k1 + 1)
    ) / (
        expected_term_frequency
        + settings.k1
        * (
            1
            - settings.b
            + settings.b
            * expected_document_length
            / expected_average_document_length
        )
    )

    assert match.document_statistics.analysis.document.resource.address.value == (
        "src/devtools/context/repository/corpus.py"
    )
    assert contribution.normalized_term == "repository"
    assert contribution.term_frequency == expected_term_frequency
    assert contribution.document_frequency == expected_document_frequency
    assert contribution.inverse_document_frequency == pytest.approx(expected_idf)
    assert contribution.document_length == expected_document_length
    assert contribution.average_document_length == expected_average_document_length
    assert contribution.contribution == pytest.approx(expected_contribution)
    assert match.score == pytest.approx(expected_contribution)


def test_multi_term_scores_sum_contributions_and_casefold_matches() -> None:
    """Known query terms contribute independently and sum into a document score."""
    result = _retrieve("REPOSITORY architecture")
    matching_document = next(
        match
        for match in result.matches
        if match.document_statistics.analysis.document.resource.address.value
        == "docs/architecture.md"
    )

    assert tuple(
        contribution.normalized_term
        for contribution in matching_document.term_contributions
    ) == ("repository", "architecture")
    assert matching_document.score == pytest.approx(
        sum(
            contribution.contribution
            for contribution in matching_document.term_contributions
        ),
    )


def test_repeated_query_terms_are_retained_but_scored_once() -> None:
    """Baseline scoring uses distinct query vocabulary while preserving raw evidence."""
    expected_repeated_observation_count = 2
    single = _retrieve("repository")
    repeated = _retrieve("repository repository")

    assert len(repeated.query.observations) == expected_repeated_observation_count
    assert repeated.query.normalized_terms == ("repository",)
    assert repeated.matches == single.matches


def test_ranking_is_descending_with_upstream_document_order_for_ties() -> None:
    """Score ties preserve established collection order rather than adding a signal."""
    repository_result = _retrieve("repository")
    context_result = _retrieve("context")

    assert [match.score for match in repository_result.matches] == sorted(
        (match.score for match in repository_result.matches),
        reverse=True,
    )
    assert tuple(
        match.document_statistics.analysis.document.resource.address.value
        for match in context_result.matches
    ) == (
        "config/example.yaml",
        "src/devtools/context/repository/corpus.py",
    )
    assert context_result.matches[0].score == context_result.matches[1].score


def test_maximum_results_is_required_positive_and_applied_after_ranking() -> None:
    """The explicit result bound truncates ranked matches but rejects invalid bounds."""
    result = _retrieve("repository", maximum_results=1)

    assert len(result.matches) == 1
    assert result.maximum_results == 1
    with pytest.raises(ValueError, match="Maximum BM25 result count"):
        _retrieve("repository", maximum_results=0)


def test_settings_validate_and_change_bm25_length_normalization() -> None:
    """BM25 settings are finite and bounded while remaining local to this algorithm."""
    default_result = _retrieve("repository")
    configured_settings = RepositoryTextLexicalBm25Settings(k1=0.0, b=0.0)
    configured_result = _retrieve("repository", settings=configured_settings)

    assert default_result.settings == RepositoryTextLexicalBm25Settings()
    assert configured_result.settings is configured_settings
    assert configured_result.matches[0].score != default_result.matches[0].score
    for settings in (
        {"k1": -0.1},
        {"k1": math.inf},
        {"b": -0.1},
        {"b": 1.1},
        {"b": math.nan},
    ):
        with pytest.raises(ValueError, match="BM25"):
            RepositoryTextLexicalBm25Settings(**settings)


def test_empty_oov_and_mixed_query_semantics_are_successful() -> None:
    """Empty and absent terms remain valid query evidence without zero-score matches."""
    empty_result = _retrieve("---")
    oov_result = _retrieve("nonexistent")
    mixed_result = _retrieve("repository nonexistent")

    assert empty_result.query.observations == ()
    assert empty_result.matches == ()
    assert oov_result.query.normalized_terms == ("nonexistent",)
    assert oov_result.matches == ()
    assert mixed_result.query.normalized_terms == ("repository", "nonexistent")
    assert tuple(
        contribution.normalized_term
        for contribution in mixed_result.matches[0].term_contributions
    ) == ("repository",)


def test_empty_index_and_empty_documents_produce_successful_zero_matches() -> None:
    """No vocabulary means no divide-by-zero path or fabricated matches."""
    expected_document_count = 2
    empty_index = build_repository_text_lexical_inverted_index(
        corpus_statistics=calculate_repository_text_lexical_corpus_statistics(
            collection_analysis=analyze_repository_text_document_collection(
                document_collection=_collection(
                    (
                        _document("README.md", "---"),
                        _document("docs/empty.md", "!!!"),
                    ),
                ),
            ),
        ),
    )

    result = _retrieve("repository", index=empty_index)
    empty_corpus_index = build_repository_text_lexical_inverted_index(
        corpus_statistics=calculate_repository_text_lexical_corpus_statistics(
            collection_analysis=analyze_repository_text_document_collection(
                document_collection=_collection(()),
            ),
        ),
    )
    empty_corpus_result = _retrieve("repository", index=empty_corpus_index)

    assert empty_index.corpus_statistics.document_count == expected_document_count
    assert empty_index.corpus_statistics.average_document_length == 0.0
    assert result.matches == ()
    assert empty_corpus_index.corpus_statistics.document_count == 0
    assert empty_corpus_result.matches == ()


def test_retrieval_is_content_only_and_performs_no_external_work(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """BM25 consumes query/index state and never acquires, parses, or scores paths."""
    query = analyze_repository_text_lexical_query(text="src path_only repository")
    index = _index()

    def fail(*_args: object, **_kwargs: object) -> None:
        msg = "BM25 retrieval must not perform unrelated work."
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

    result = _retrieve(query, index=index)

    assert tuple(
        contribution.normalized_term
        for contribution in result.matches[0].term_contributions
    ) == ("repository",)


def test_retrieval_exposes_no_context_or_nonlexical_retrieval_state() -> None:
    """The result is local BM25 evidence, not Context or another retrieval family."""
    result = _retrieve("repository")

    assert all(
        not hasattr(result, attribute)
        for attribute in (
            "context",
            "disclosure",
            "embedding",
            "vector",
            "graph",
            "path_score",
            "package_score",
        )
    )
