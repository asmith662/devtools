# Copyright (c) 2026
"""Tests for the bounded independent filename-stem lexical retrieval field."""

from __future__ import annotations

import pytest

from devtools.context.retrieval.lexical.analysis import (
    analyze_repository_text_document_collection,
)
from devtools.context.retrieval.lexical.bm25 import (
    analyze_repository_text_lexical_query,
    retrieve_repository_text_documents_by_bm25,
)
from devtools.context.retrieval.lexical.evaluation import (
    RepositoryTextLexicalRetrievalEvaluationCase,
    evaluate_repository_text_lexical_bm25_retrieval,
)
from devtools.context.retrieval.lexical.filename import (
    build_repository_text_filename_lexical_index,
)
from devtools.context.retrieval.lexical.index import (
    RepositoryTextLexicalInvertedIndex,
    build_repository_text_lexical_inverted_index,
)
from devtools.context.retrieval.lexical.statistics import (
    calculate_repository_text_lexical_corpus_statistics,
)

from ._helpers import _collection, _document

_FILENAME_WEIGHT = 0.25


def _index(*documents: tuple[str, str]) -> RepositoryTextLexicalInvertedIndex:
    """Build one content index over exact repository document fixtures."""
    collection = _collection(
        tuple(_document(address, text) for address, text in documents),
    )
    return build_repository_text_lexical_inverted_index(
        corpus_statistics=calculate_repository_text_lexical_corpus_statistics(
            collection_analysis=analyze_repository_text_document_collection(
                document_collection=collection,
            ),
        ),
    )


def test_filename_field_uses_stem_only_with_baseline_spans() -> None:
    """Extensions and directories stay outside independently indexed stem evidence."""
    index = _index(
        ("src/Directory/Request_Assembly.py", "content"),
        ("docs/README.md", "content"),
    )
    filename_index = build_repository_text_filename_lexical_index(
        document_collection=index.corpus_statistics.collection_analysis.document_collection,
    )
    first = next(
        item
        for item in filename_index.document_statistics
        if item.analysis.document.resource.address.value
        == "src/Directory/Request_Assembly.py"
    )

    assert first.analysis.filename_stem == "Request_Assembly"
    assert [item.normalized_term for item in first.analysis.observations] == [
        "request_assembly",
    ]
    assert filename_index.average_document_length == 1.0
    assert {item.normalized_term for item in filename_index.document_frequencies} == {
        "readme",
        "request_assembly",
    }
    assert "py" not in {item.normalized_term for item in filename_index.term_postings}
    assert "directory" not in {
        item.normalized_term for item in filename_index.term_postings
    }


def test_filename_field_is_independent_from_content_statistics() -> None:
    """Content changes leave a document's filename observations unchanged."""
    first = _index(("src/same_name.py", "alpha"), ("docs/other.md", "beta"))
    second = _index(
        ("src/same_name.py", "alpha alpha alpha"),
        ("docs/other.md", "beta"),
    )
    first_filename = build_repository_text_filename_lexical_index(
        document_collection=first.corpus_statistics.collection_analysis.document_collection,
    )
    second_filename = build_repository_text_filename_lexical_index(
        document_collection=second.corpus_statistics.collection_analysis.document_collection,
    )

    first_content = next(
        item
        for item in first.corpus_statistics.document_statistics
        if item.analysis.document.resource.address.value == "src/same_name.py"
    )
    second_content = next(
        item
        for item in second.corpus_statistics.document_statistics
        if item.analysis.document.resource.address.value == "src/same_name.py"
    )
    assert first_content.document_length != second_content.document_length
    first_same_name = next(
        item
        for item in first_filename.document_statistics
        if item.analysis.document.resource.address.value == "src/same_name.py"
    )
    second_same_name = next(
        item
        for item in second_filename.document_statistics
        if item.analysis.document.resource.address.value == "src/same_name.py"
    )
    assert (
        first_same_name.analysis.observations
        == second_same_name.analysis.observations
    )
    assert first_same_name.document_length == 1


def test_filename_bm25_combines_separate_evidence_and_preserves_zero_cases() -> None:
    """Canonical retrieval exposes content, filename, and final-score evidence."""
    index = _index(
        ("src/opaque.py", "contentterm"),
        ("docs/filenameonly.md", "quiet"),
        ("tests/test_filenameonly.py", "quiet"),
    )
    filename_result = retrieve_repository_text_documents_by_bm25(
        query=analyze_repository_text_lexical_query(text="filenameonly"),
        index=index,
        maximum_results=5,
    )
    content_result = retrieve_repository_text_documents_by_bm25(
        query=analyze_repository_text_lexical_query(text="contentterm"),
        index=index,
        maximum_results=5,
    )
    oov_result = retrieve_repository_text_documents_by_bm25(
        query=analyze_repository_text_lexical_query(text="missing"),
        index=index,
        maximum_results=5,
    )

    filename_match = filename_result.matches[0]
    assert filename_match.content_score == 0.0
    assert filename_match.filename_score > 0.0
    assert filename_match.filename_weight == _FILENAME_WEIGHT
    assert filename_match.weighted_filename_score == pytest.approx(
        _FILENAME_WEIGHT * filename_match.filename_score,
    )
    assert filename_match.score == pytest.approx(
        filename_match.content_score + filename_match.weighted_filename_score,
    )
    assert (
        filename_match.filename_term_contributions[0].normalized_term
        == "filenameonly"
    )
    assert content_result.matches[0].content_score > 0.0
    assert content_result.matches[0].filename_score == 0.0
    assert oov_result.matches == ()


def test_filename_retrieval_keeps_document_order_for_combined_ties_and_evaluation(
) -> None:
    """Equal field scores retain upstream order and existing evaluation correlation."""
    index = _index(
        ("a/match.md", ""),
        ("b/match.md", ""),
    )
    query = analyze_repository_text_lexical_query(text="match")
    result = retrieve_repository_text_documents_by_bm25(
        query=query,
        index=index,
        maximum_results=1,
    )
    evaluation = evaluate_repository_text_lexical_bm25_retrieval(
        case=RepositoryTextLexicalRetrievalEvaluationCase(
            query=query,
            relevant_resource_addresses=(
                result.matches[0].document_statistics.analysis.document.resource.address,
            ),
            evaluation_k=1,
        ),
        retrieval_result=result,
    )

    assert (
        result.matches[0].document_statistics.analysis.document.resource.address.value
        == "a/match.md"
    )
    assert evaluation.hit_at_k is True
    with pytest.raises(ValueError, match="Maximum BM25 result count"):
        retrieve_repository_text_documents_by_bm25(
            query=query,
            index=index,
            maximum_results=0,
        )
