# Copyright (c) 2026
# ruff: noqa: D103, E501, PLR0913, PLR2004
"""Controlled tests for Increment-24 offline ranking mechanics."""

import pytest

from experiments.purpose_relative_ranking import (
    LabeledCandidate,
    RankingArm,
    RankingCase,
    SurfaceCandidate,
    build_surface_candidates,
    evaluate_case,
    rank_case,
    ranking_design_fingerprint,
    validate_grouped_case_split,
)


def _candidate(address: str, *, score: float | None, rank: int | None, profile: int = 0, incoming: int = 0, outgoing: int = 0) -> SurfaceCandidate:
    return SurfaceCandidate(address, score, rank, rank is not None and rank <= 5, rank is not None, incoming, outgoing, profile, 1 if profile else None, profile)


def test_feature_construction_accepts_no_judgments_or_control_status() -> None:
    capture = {"lexical_top_fifteen": [{"address": "a.py", "rank": 1, "score": 1.0}], "lexical_top_five": [{"address": "a.py", "rank": 1, "score": 1.0}], "incoming_surfaces": [], "outgoing_surfaces": [], "profile_eligible_surfaces": []}
    candidate = build_surface_candidates(capture=capture)[0]
    assert not hasattr(candidate, "judgment")
    assert candidate.address == "a.py"


def test_unjudged_is_not_negative_and_purpose_varies_from_same_query() -> None:
    first = RankingCase("one", "same", "local need", "local-definition-or-governance", (LabeledCandidate(_candidate("a.py", score=1.0, rank=1), "unjudged"),))
    second = RankingCase("two", "same", "incoming need", "incoming-consumer-or-test", (LabeledCandidate(_candidate("a.py", score=1.0, rank=1, profile=2), "useful"),))
    assert first.query_text == second.query_text
    assert first.profile != second.profile
    assert evaluate_case(case=first, arm=RankingArm.PURPOSE_RELATIVE_DETERMINISTIC)["selected_unjudged_count"] == 1


def test_directional_evidence_is_separate_and_ties_are_deterministic() -> None:
    incoming = _candidate("a.py", score=None, rank=None, profile=2, incoming=2)
    outgoing = _candidate("b.py", score=None, rank=None, profile=0, outgoing=2)
    case = RankingCase("case", "q", "need", "incoming-consumer-or-test", (LabeledCandidate(outgoing, "not-useful"), LabeledCandidate(incoming, "useful")))
    assert rank_case(case=case, arm=RankingArm.PURPOSE_RELATIVE_DETERMINISTIC)[0].address == "a.py"
    assert rank_case(case=case, arm=RankingArm.PURPOSE_AGNOSTIC_NATIVE_EVIDENCE)[0].address == "a.py"


def test_top_k_and_identity_do_not_create_relevance_feature() -> None:
    values = (_candidate("z.py", score=1.0, rank=2), _candidate("a.py", score=1.0, rank=1), _candidate("x.py", score=0.5, rank=3))
    case = RankingCase("case", "q", "need", "local-definition-or-governance", tuple(LabeledCandidate(value, "not-useful") for value in values))
    ranking = rank_case(case=case, arm=RankingArm.LEXICAL_TOP15_TRUNCATED_TO5)
    assert [item.address for item in ranking] == ["a.py", "z.py", "x.py"]
    assert "address" not in [field for field in SurfaceCandidate.__dataclass_fields__ if field != "address"]


def test_metrics_exclude_unjudged_from_definitive_precision_and_pairwise() -> None:
    candidates = (_candidate("good.py", score=2.0, rank=1), _candidate("unknown.py", score=1.0, rank=2), _candidate("bad.py", score=0.5, rank=3))
    case = RankingCase("case", "q", "need", "local-definition-or-governance", (LabeledCandidate(candidates[0], "useful"), LabeledCandidate(candidates[1], "unjudged"), LabeledCandidate(candidates[2], "not-useful")))
    result = evaluate_case(case=case, arm=RankingArm.CANONICAL_TOP5)
    assert result["precision_at_5_definitive"] == 0.5
    assert result["pairwise_useful_not_useful_accuracy"] == 1.0


def test_design_fingerprint_is_deterministic() -> None:
    assert ranking_design_fingerprint() == ranking_design_fingerprint()


def test_grouped_split_rejects_same_case_leakage() -> None:
    validate_grouped_case_split(calibration=("calibration",), evaluation=("evaluation",))
    with pytest.raises(ValueError, match="cannot be"):
        validate_grouped_case_split(calibration=("same",), evaluation=("same",))
