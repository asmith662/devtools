# Copyright (c) 2026
# ruff: noqa: COM812, PLR2004 -- mechanical fixture constants
"""Pin identifier mechanics independently of usefulness judgments."""

from __future__ import annotations

import pytest

from devtools.context.retrieval.lexical.analysis import iter_lexical_spans
from experiments.identifier_sparse.analysis import (
    compare_terms,
    iter_terms,
    query_terms,
)
from experiments.retrieval_identifier import expand_identifier_terms


@pytest.mark.parametrize(
    ("text", "expected"),
    [
        (
            "CandidateMemberResolution",
            ("candidatememberresolution", "candidate", "member", "resolution"),
        ),
        (
            "candidate_member_resolution",
            ("candidate_member_resolution", "candidate", "member", "resolution"),
        ),
        (
            "acquire_localization_lexical_evidence",
            (
                "acquire_localization_lexical_evidence",
                "acquire",
                "localization",
                "lexical",
                "evidence",
            ),
        ),
        ("HTTPRequest", ("httprequest", "http", "request")),
        ("HTTPRequest2", ("httprequest2", "http", "request", "2")),
        ("parseHTTPResponse", ("parsehttpresponse", "parse", "http", "response")),
        ("ADR0005", ("adr0005", "adr", "0005")),
        ("__all__", ("__all__", "all")),
        ("RepositoryId", ("repositoryid", "repository", "id")),
        ("Python3Parser", ("python3parser", "python", "3", "parser")),
        ("HTTP", ("http",)),
        ("candidate", ("candidate",)),
        ("__candidate__member___", ("__candidate__member___", "candidate", "member")),
        ("candidate_candidate", ("candidate_candidate", "candidate")),
        (
            "\u00c9clairHTTP2Parser",
            ("\u00e9clairhttp2parser", "\u00e9clair", "http", "2", "parser"),
        ),
        ("\u6570\u636e", ("\u6570\u636e",)),
        ("___", ("___",)),
    ],
)
def test_frozen_splitter_examples(text: str, expected: tuple[str, ...]) -> None:
    """Reuse historical behavior exactly, including Unicode and whole forms."""
    assert tuple(iter_terms(text)) == expected
    assert expand_identifier_terms(observed_text=text) == expected
    assert tuple(value[1] for value in iter_lexical_spans(text=text)) == (
        text.casefold(),
    )


def test_occurrence_frequency_and_query_duplicates_are_distinct() -> None:
    """Within-span deduplication must not erase independent source occurrences."""
    assert tuple(iter_terms("candidate candidate")) == ("candidate", "candidate")
    assert tuple(iter_terms("candidate_candidate candidate")) == (
        "candidate_candidate",
        "candidate",
        "candidate",
    )
    assert query_terms("candidate candidate Candidate") == ("candidate",)


def test_plain_prose_and_punctuation_have_no_semantic_expansion() -> None:
    """Preserve existing word boundaries and leave synonyms/inflections alone."""
    prose = "the widgets are running; source-body, Stra\u00dfe"
    assert tuple(iter_terms(prose)) == tuple(
        item[1] for item in iter_lexical_spans(text=prose)
    )
    assert "run" not in query_terms(prose)
    assert "origin" not in query_terms(prose)


def test_query_forms_share_concept_terms_and_diagnostics_are_bounded() -> None:
    """Both caller strings expose components without rewriting their prose."""
    assert set(query_terms("candidate member resolution")) <= set(
        query_terms("CandidateMemberResolution")
    )
    diagnostic = compare_terms(
        "CandidateMemberResolution HTTPRequest quiet", maximum_spans=2
    )
    assert diagnostic["truncated"] is True
    assert len(diagnostic["spans"]) == 2
    with pytest.raises(ValueError, match="positive"):
        compare_terms("quiet", maximum_spans=0)
