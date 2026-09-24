# Copyright (c) 2026
# ruff: noqa: PLR2004
"""Falsify the frozen Increment-26 development origin join and accounting."""

from __future__ import annotations

import copy
import json
from pathlib import Path
from typing import Any, cast

import pytest

from experiments.increment_26.development_evaluation import (
    CANDIDATE_SHA256,
    JUDGMENT_IDENTITY,
    JUDGMENT_SHA256,
    evaluate_case,
    evaluate_development,
)
from experiments.increment_26.development_judgments import (
    DEVELOPMENT_CASE_IDS,
    EVIDENCE_IDENTITY,
    FREEZE_IDENTITY,
    INPUT_SHA256,
)
from experiments.purpose_relative_admission.validation_execution import (
    validate_artifact_envelope,
)

_ROOT = Path("experiments/increment_26")


def _bytes() -> tuple[bytes, bytes, bytes]:
    return (
        (_ROOT / "development_candidate_evidence.json").read_bytes(),
        (_ROOT / "development_frozen_judgments.json").read_bytes(),
        (_ROOT / "development_judgment_input.json").read_bytes(),
    )


def _evaluate() -> dict[str, Any]:
    candidate, judgment, blinded = _bytes()
    return evaluate_development(
        candidate_bytes=candidate,
        judgment_bytes=judgment,
        blinded_input_bytes=blinded,
    )


def test_exact_frozen_artifact_binding_and_case_population() -> None:
    """Only the canonical eight-case evidence and judgment freeze can join."""
    result = _evaluate()
    assert validate_artifact_envelope(result)
    payload = result["payload"]
    assert payload["increment_26_freeze_identity"] == FREEZE_IDENTITY
    assert payload["candidate_evidence_sha256"] == CANDIDATE_SHA256
    assert payload["candidate_evidence_identity"] == EVIDENCE_IDENTITY
    assert payload["frozen_judgment_sha256"] == JUDGMENT_SHA256
    assert payload["frozen_judgment_identity"] == JUDGMENT_IDENTITY
    assert payload["blinded_input_sha256"] == INPUT_SHA256
    assert tuple(case["case_id"] for case in payload["cases"]) == DEVELOPMENT_CASE_IDS
    assert payload["aggregate"]["neutral_pair_count"] == 69
    assert payload["aggregate"]["case_count"] == 8


@pytest.mark.parametrize("damaged", ["candidate", "judgment", "blinded"])
def test_modified_canonical_input_is_rejected(damaged: str) -> None:
    """Changing any frozen source invalidates the join before accounting."""
    candidate, judgment, blinded = _bytes()
    values = {"candidate": candidate, "judgment": judgment, "blinded": blinded}
    values[damaged] += b" "
    with pytest.raises(ValueError, match="differ"):
        evaluate_development(
            candidate_bytes=values["candidate"],
            judgment_bytes=values["judgment"],
            blinded_input_bytes=values["blinded"],
        )


def test_join_rejects_wrong_case_neutral_pair_and_arm_accounting() -> None:
    """Case identity, neutral union, and retained overlap must all agree."""
    candidate, judgment, blinded = [
        cast("dict[str, Any]", json.loads(value)) for value in _bytes()
    ]
    c = candidate["cases"][1]
    j = judgment["payload"]["cases"][1]
    b = blinded["cases"][1]
    changed = copy.deepcopy(c)
    changed["case_id"] = "i25-confirmation"
    with pytest.raises(ValueError, match="case identities"):
        evaluate_case(changed, j, b)
    changed = copy.deepcopy(j)
    changed["records"][0]["neutral_id"] = "0" * 64
    with pytest.raises(ValueError, match="neutral pairs"):
        evaluate_case(c, changed, b)
    changed = copy.deepcopy(c)
    changed["overlap"]["intersection"] = []
    with pytest.raises(ValueError, match="overlap"):
        evaluate_case(changed, j, b)
    changed = copy.deepcopy(c)
    changed["semantic_candidates"].pop()
    with pytest.raises(ValueError, match="capacity"):
        evaluate_case(changed, j, b)
    changed = copy.deepcopy(c)
    changed["semantic_candidates"][0]["has_positive_lexical_rank"] = False
    with pytest.raises(ValueError, match="reachability"):
        evaluate_case(changed, j, b)


def test_three_state_per_arm_and_overlap_accounting() -> None:
    """Every retained occurrence keeps its frozen three-state judgment."""
    result = _evaluate()["payload"]
    total = result["aggregate"]
    assert total["candidate_counts"] == {
        "semantic": 40,
        "lexical": 40,
        "overlap": 11,
        "semantic_only": 29,
        "lexical_only": 29,
    }
    assert total["judgment_counts"] == {
        "semantic": {"useful": 18, "not-useful": 20, "unjudged": 2},
        "lexical": {"useful": 16, "not-useful": 24, "unjudged": 0},
        "overlap": {"useful": 10, "not-useful": 1, "unjudged": 0},
        "semantic_only": {"useful": 8, "not-useful": 19, "unjudged": 2},
        "lexical_only": {"useful": 6, "not-useful": 23, "unjudged": 0},
    }
    for case in result["cases"]:
        counts = case["candidate_counts"]
        labels = case["judgment_counts"]
        assert counts["semantic"] == counts["overlap"] + counts["semantic_only"]
        assert counts["lexical"] == counts["overlap"] + counts["lexical_only"]
        for surface, number in counts.items():
            assert sum(labels[surface].values()) == number
            assert len(case["useful_resources"][surface]) == labels[surface]["useful"]
    assert (
        sum(
            case["judgment_counts"]["semantic_only"]["unjudged"]
            for case in result["cases"]
        )
        == 2
    )


def test_lexical_reachability_distinguishes_capacity_from_positive_rank() -> None:
    """Useful semantic-only resources are reachable below lexical top five."""
    reach = _evaluate()["payload"]["aggregate"]["lexical_reachability"]
    assert len(reach["semantic_without_positive_lexical_rank"]) == 6
    assert reach["useful_semantic_without_positive_lexical_rank"] == []
    ranked = reach["useful_semantic_only_ranked_outside_capacity"]
    assert len(ranked) == 8
    assert sorted(item["lexical_rank"] for item in ranked) == [
        6,
        8,
        9,
        11,
        12,
        16,
        51,
        55,
    ]
    assert reach["useful_semantic_only_positive_lexical_rank_distribution"] == {
        str(rank): 1 for rank in (6, 8, 9, 11, 12, 16, 51, 55)
    }


def test_result_serialization_and_identity_are_deterministic() -> None:
    """The same committed artifacts reproduce the retained result byte for byte."""
    first = _evaluate()
    second = _evaluate()
    actual = (_ROOT / "development_results.json").read_bytes()
    assert first == second
    assert (json.dumps(first, indent=2, sort_keys=True) + "\n").encode() == actual
    assert first["content_identity"] == json.loads(actual)["content_identity"]
