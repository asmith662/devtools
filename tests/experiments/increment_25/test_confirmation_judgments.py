# Copyright (c) 2026
# ruff: noqa: D103, E501, PLR2004
"""Tests for blinded Increment-25 confirmation judgment freezing and joining."""

from __future__ import annotations

import hashlib
import json
from copy import deepcopy
from pathlib import Path
from typing import cast

import pytest

from experiments.increment_25.confirmation_judgments import (
    audit_frozen_confirmation_judgments,
    evaluate_confirmation,
    freeze_confirmation_judgments,
)

_ROOT = Path(__file__).parents[3]


def _blinded() -> dict[str, object]:
    return {
        "schema": "fixture",
        "execution_identity": "candidate",
        "cases": [
            {
                "case_id": "case",
                "task": {"purpose": "Need"},
                "resources": [
                    {"address": "both.py", "content": "both"},
                    {"address": "structural.py", "content": "structural"},
                    {"address": "lexical.py", "content": "lexical"},
                ],
            },
        ],
    }


def _decisions() -> dict[str, object]:
    return {
        "case": {
            "both.py": {"judgment": "useful", "rationale": "Direct behavior."},
            "structural.py": {
                "judgment": "unjudged",
                "rationale": "Visible evidence is insufficient.",
            },
            "lexical.py": {
                "judgment": "not-useful",
                "rationale": "Unrelated behavior.",
            },
        },
    }


def _candidates() -> dict[str, object]:
    return {
        "cases": [
            {
                "case_id": "case",
                "capacity": {"m": 2, "lexical_exhausted": False},
                "structural_additions": [
                    {"address": "both.py", "positive_lexical_rank": 6},
                    {"address": "structural.py", "positive_lexical_rank": None},
                ],
                "matched_lexical_additions": ["both.py", "lexical.py"],
                "resolution_diagnostics": {"aggregate": {"resolved": 2}},
            },
        ],
    }


def test_freeze_requires_exact_pair_coverage_and_three_state_labels() -> None:
    missing = deepcopy(_decisions())
    del cast("dict[str, object]", missing["case"])["lexical.py"]
    with pytest.raises(ValueError, match="exactly"):
        freeze_confirmation_judgments(blinded=_blinded(), decisions=missing)

    invalid = deepcopy(_decisions())
    cast("dict[str, dict[str, str]]", invalid["case"])["lexical.py"]["judgment"] = "negative"
    with pytest.raises(ValueError, match="not a valid"):
        freeze_confirmation_judgments(blinded=_blinded(), decisions=invalid)


def test_frozen_judgments_hide_address_and_origin_until_join() -> None:
    frozen, mapping = freeze_confirmation_judgments(
        blinded=_blinded(), decisions=_decisions(),
    )
    serialized = str(frozen)

    audit_frozen_confirmation_judgments(frozen)
    assert "both.py" not in serialized
    assert "structural.py" not in serialized
    assert "lexical.py" not in serialized
    assert "structural_additions" not in serialized
    assert "matched_lexical_additions" not in serialized
    assert str(mapping["schema"]).endswith("neutral-mapping-v1")


def test_unblinding_retains_unjudged_and_counts_each_arm_without_scoring() -> None:
    blinded = _blinded()
    frozen, mapping = freeze_confirmation_judgments(
        blinded=blinded, decisions=_decisions(),
    )
    result = evaluate_confirmation(
        candidates=_candidates(),
        blinded=blinded,
        frozen=frozen,
        mapping=mapping,
    )
    payload = cast("dict[str, object]", result["payload"])
    case = cast("list[dict[str, object]]", payload["cases"])[0]
    arms = cast("dict[str, dict[str, int]]", case["judgments_by_arm"])

    assert arms["structural"] == {"useful": 1, "not-useful": 0, "unjudged": 1}
    assert arms["matched_lexical"] == {
        "useful": 1,
        "not-useful": 1,
        "unjudged": 0,
    }
    assert case["useful_overlap"] == ["both.py"]
    assert case["useful_structural_only"] == []
    assert case["useful_matched_lexical_only"] == []


def test_evaluation_rejects_tampered_freeze_before_origin_join() -> None:
    blinded = _blinded()
    frozen, mapping = freeze_confirmation_judgments(
        blinded=blinded, decisions=_decisions(),
    )
    tampered = deepcopy(frozen)
    payload = cast("dict[str, object]", tampered["payload"])
    case = cast("list[dict[str, object]]", payload["cases"])[0]
    record = cast("list[dict[str, object]]", case["records"])[0]
    record["candidate_origin_visible_to_adjudicator"] = True

    with pytest.raises(ValueError, match="invalid"):
        evaluate_confirmation(
            candidates=_candidates(),
            blinded=blinded,
            frozen=tampered,
            mapping=mapping,
        )


def test_retained_confirmation_artifacts_cover_only_frozen_confirmation() -> None:
    freeze = json.loads(
        (_ROOT / "experiments/increment_25/task_population_freeze.json").read_text(
            encoding="utf-8",
        ),
    )
    candidates = json.loads(
        (_ROOT / "experiments/increment_25/confirmation_candidate_evidence.json").read_text(
            encoding="utf-8",
        ),
    )
    blinded = json.loads(
        (_ROOT / "experiments/increment_25/confirmation_judgment_input.json").read_text(
            encoding="utf-8",
        ),
    )
    frozen = json.loads(
        (_ROOT / "experiments/increment_25/confirmation_frozen_judgments.json").read_text(
            encoding="utf-8",
        ),
    )
    results = json.loads(
        (_ROOT / "experiments/increment_25/confirmation_results.json").read_text(
            encoding="utf-8",
        ),
    )
    expected = tuple(freeze["payload"]["split"]["confirmation_case_ids"])
    candidate_ids = tuple(case["case_id"] for case in candidates["cases"])
    blinded_ids = tuple(case["case_id"] for case in blinded["cases"])

    audit_frozen_confirmation_judgments(frozen)
    assert candidate_ids == expected == blinded_ids
    assert not set(candidate_ids) & set(freeze["payload"]["split"]["reserve_case_ids"])
    assert sum(len(case["resources"]) for case in blinded["cases"]) == 51
    assert results["payload"]["aggregate"] == {
        "case_count": 16,
        "cases_with_structural_additions": 12,
        "distinct_structural_additions": 31,
        "lexical_exhaustion_cases": [],
        "matched_lexical_additions": 31,
        "matched_lexical_judgments": {
            "not-useful": 16,
            "unjudged": 0,
            "useful": 15,
        },
        "overlap": 11,
        "structural_judgments": {
            "not-useful": 14,
            "unjudged": 0,
            "useful": 17,
        },
        "useful_matched_lexical_only": 8,
        "useful_overlap": 7,
        "useful_structural_only": 10,
        "useful_structural_without_positive_lexical_rank": 5,
    }


def test_committed_development_artifacts_remain_byte_identical() -> None:
    expected = {
        "development_candidate_evidence.json": "748d135451cdad497b8e892b38b0ab59351777a84a701bd5e3323bfff2622e6f",
        "development_judgment_input.json": "5cb67a13ee4f3278edb21c9a71e051dadc3ec1f3d6968c98d71965f5c6d6c50b",
    }
    for name, digest in expected.items():
        content = (_ROOT / "experiments/increment_25" / name).read_bytes()
        assert hashlib.sha256(content).hexdigest() == digest
