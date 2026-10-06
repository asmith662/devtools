# Copyright (c) 2026
# ruff: noqa: COM812, FBT001 -- parametrized analyzer fixtures

"""Attribution uses mechanically witnessed representation, never semantic guesses."""

from __future__ import annotations

from dataclasses import replace

import pytest

from experiments.retrieval_diagnostics.comparison import compare
from experiments.retrieval_diagnostics.mechanics import Mechanics
from tests.experiments.retrieval_diagnostics.helpers import capture, judged


@pytest.mark.parametrize(
    ("documents", "query", "source_hidden", "query_hidden"),
    [
        (
            (("a.py", "CandidateMemberResolution"), ("b.py", "other")),
            "candidate member resolution",
            True,
            False,
        ),
        (
            (("a.py", "candidate member resolution"), ("b.py", "other")),
            "CandidateMemberResolution",
            False,
            True,
        ),
        (
            (("a.py", "CandidateMemberResolution"), ("b.py", "other")),
            "CandidateMemberResolution",
            True,
            True,
        ),
        (
            (("candidate_member_resolution.py", ""), ("z.py", "other")),
            "candidate member resolution",
            True,
            False,
        ),
    ],
)
def test_verified_hidden_matching_cues_separate_query_document_and_filename(
    documents: tuple[tuple[str, str], ...],
    query: str,
    source_hidden: bool,
    query_hidden: bool,
) -> None:
    """Partial whole-form reach must not be mislabeled a required reach rescue."""
    a, b = capture(documents, query), capture(documents, query, expanded=True)
    target = a.resources[0]
    pair = compare(Mechanics(a), Mechanics(b), target)
    r = pair["representation"]
    assert r["diagnostic"] == "VERIFIED_REPRESENTATION_FAILURE"
    assert any(
        w["source_hidden"] == source_hidden and w["query_hidden"] == query_hidden
        for w in r["witnesses"]
    )
    assert not r["required_resource"]
    assert r["positive_reach_rescue"] == (pair["status_A"] == "NO_QUERY_TERM_OVERLAP")
    assert pair["mechanics"]["score_delta"] == pytest.approx(
        pair["score_B"] - pair["score_A"]
    )
    reverse = compare(Mechanics(b), Mechanics(a), target)
    assert reverse["representation"]["diagnostic"] == "VERIFIED_REPRESENTATION_FAILURE"
    assert reverse["representation"]["reverse_witnesses"]
    assert (
        reverse["representation"]["positive_reach_loss"] == r["positive_reach_rescue"]
    )


def test_required_whole_form_is_preserved_but_rank_need_not_be() -> None:
    """Whole-form evidence persists while expansion changes DF, TF and lengths."""
    docs = (
        ("a.py", "CandidateMemberResolution extra"),
        ("b.py", "candidate candidate candidate"),
    )
    a, b = (
        capture(docs, "CandidateMemberResolution"),
        capture(docs, "CandidateMemberResolution", expanded=True),
    )
    labels = judged(a, ("REQUIRED", "UNNECESSARY"))
    pair = compare(Mechanics(a, labels), Mechanics(b, labels), a.resources[0])
    assert pair["transition"] == "POSITIVE_TO_POSITIVE"
    assert not pair["representation"]["positive_reach_rescue"]
    whole = next(
        t
        for t in pair["mechanics"]["term_deltas"]
        if t["term"] == "candidatememberresolution"
    )
    assert whole["A"]["tf"] == whole["B"]["tf"] == 1
    assert whole["length_factor_delta"] != 0
    assert pair["configuration_changes"]["analyzer"] == {
        "A": "canonical",
        "B": "identifier",
    }


def test_possible_semantic_mismatch_needs_required_gold_and_all_available_misses() -> (
    None
):
    """Available lexical mismatch is never proof of semantic equivalence."""
    docs = (("a.py", "unrelated"), ("b.py", "other"))
    a, b = capture(docs, "candidate"), capture(docs, "candidate", expanded=True)
    labels = judged(a, ("REQUIRED", "UNNECESSARY"))
    plain = compare(Mechanics(a), Mechanics(b), a.resources[0])
    assert plain["semantic_mismatch"]["diagnostic"] == "NOT_ESTABLISHED"
    pair = compare(Mechanics(a, labels), Mechanics(b, labels), a.resources[0])
    assert (
        pair["semantic_mismatch"]["diagnostic"]
        == "POSSIBLE_VOCABULARY_SEMANTIC_MISMATCH"
    )
    assert pair["semantic_mismatch"]["certainty"] == "POSSIBLE_UNRESOLVED"
    assert pair["transition"] == "MISS_TO_MISS"


def test_pair_rejects_different_lane_frame_judgments_and_bounded_recovery_claim() -> (
    None
):
    """Only the same frozen subject may be compared; top bounds are not reach."""
    docs = (("a.py", "plain plain"), ("b.py", "plain"))
    a = capture(docs, limit=1)
    b = capture(docs, expanded=True)
    pair = compare(Mechanics(a), Mechanics(b), a.resources[1])
    assert pair["status_A"] == "RESULT_BOUND_OMISSION"
    assert not pair["representation"]["positive_reach_rescue"]
    with pytest.raises(ValueError, match="frame/query/judgment"):
        compare(Mechanics(a), Mechanics(replace(b, lane="other")), a.resources[0])
    with pytest.raises(ValueError, match="frame/query/judgment"):
        compare(
            Mechanics(a),
            Mechanics(b, judged(b, ("REQUIRED", "UNNECESSARY"))),
            a.resources[0],
        )
