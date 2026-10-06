# Copyright (c) 2026
# ruff: noqa: COM812, PLR2004 -- mechanical fixture constants
"""Check unchanged BM25 mechanics, field evidence and canonical isolation."""

from __future__ import annotations

import pytest

from devtools.context.retrieval.lexical.bm25 import (
    analyze_repository_text_lexical_query,
    retrieve_repository_text_documents_by_bm25,
)
from experiments.codex_dogfood.case_0009.freeze import canonical_index
from experiments.identifier_sparse.index import build_index
from experiments.identifier_sparse.retrieval import retrieve
from tests.context.retrieval.lexical._helpers import _collection, _document


def test_plain_terms_match_production_scores_fields_and_tie_order() -> None:
    """When representation adds nothing, scoring architecture must match A."""
    documents = _collection(
        (
            _document("a.py", "quiet quiet plain"),
            _document("b.py", "quiet quiet plain"),
            _document("plain.txt", ""),
        )
    )
    canonical = canonical_index(documents)
    before = retrieve_repository_text_documents_by_bm25(
        query=analyze_repository_text_lexical_query(text="quiet plain"),
        index=canonical,
        maximum_results=3,
    )
    expanded = retrieve(build_index(documents), "quiet plain", maximum_results=3)
    after = retrieve_repository_text_documents_by_bm25(
        query=analyze_repository_text_lexical_query(text="quiet plain"),
        index=canonical,
        maximum_results=3,
    )
    assert before == after
    assert [item.document.resource.address for item in expanded.matches] == [
        item.document_statistics.analysis.document.resource.address
        for item in before.matches
    ]
    for actual, expected in zip(expanded.matches, before.matches, strict=True):
        assert actual.score == pytest.approx(expected.score, abs=1e-12)
        assert actual.content_score == pytest.approx(expected.content_score, abs=1e-12)
        assert actual.filename_score == pytest.approx(
            expected.filename_score, abs=1e-12
        )


def test_identifier_query_content_and_filename_are_explicit_treatment() -> None:
    """Inspect two fields and whole forms without useful-resource labels."""
    documents = _collection(
        (
            _document("a.py", "CandidateMemberResolution"),
            _document("candidate_member_resolution.py", ""),
            _document("b.py", "unrelated"),
        )
    )
    index = build_index(documents)
    result = retrieve(index, "candidate member resolution", maximum_results=3)
    assert len(result.matches) == 2
    assert {item.document.resource.address.value for item in result.matches} == {
        "a.py",
        "candidate_member_resolution.py",
    }
    assert result.query_text == "candidate member resolution"
    assert "candidatememberresolution" in dict(index.content.postings)
    assert "candidate_member_resolution" in dict(result.filename_index.postings)
    assert {term.term for item in result.matches for term in item.content_evidence} == {
        "candidate",
        "member",
        "resolution",
    }
    for item in result.matches:
        assert item.score == item.content_score + 0.25 * item.filename_score
    assert retrieve(index, "CandidateMemberResolution", maximum_results=3).matches
    assert retrieve(index, "missing", maximum_results=3).matches == ()
    with pytest.raises(ValueError, match="positive"):
        retrieve(index, "candidate", maximum_results=0)


def test_frequency_does_not_double_plain_occurrences_or_drop_repetition() -> None:
    """Length/statistics count unique per-span terms with occurrence multiplicity."""
    index = build_index(
        _collection((_document("a.py", "candidate candidate_candidate candidate"),))
    )
    assert dict(index.content.postings)["candidate"] == ((0, 3),)
    assert index.content.lengths == (4,)
