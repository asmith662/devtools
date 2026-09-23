# Copyright (c) 2026
# ruff: noqa: D103, PLR2004
"""Checks for the retained Increment-23 independent-validation report."""

from __future__ import annotations

from copy import deepcopy
from pathlib import Path

import pytest

from experiments.purpose_relative_admission.validation_reporting import (
    build_increment_23_report,
    increment_23_control_conflict_review,
    validate_increment_23_report,
)


def test_report_reconstructs_frozen_metrics_and_disposition() -> None:
    report = build_increment_23_report(repository_root=Path(__file__).parents[3])
    payload = report["payload"]

    assert payload["judgment_coverage"]["total"] == 96
    assert payload["surface_quality"]["known_useful_top_15_recovered"] == 18
    assert payload["admission"] == {
        "total": 2,
        "useful": 1,
        "not_useful": 1,
        "unjudged": 0,
        "precision": 0.5,
        "conditional_recall_over_qualified_useful": 1.0,
    }
    assert payload["capacity"]["useful_final_losses"] == 1
    assert payload["controls"]["validated_negative_after_review"] == 1
    assert payload["controls"]["relationship_exposed"] == 0
    assert payload["disposition"]["shadow_mode"] == "NOT_READY_FOR_SHADOW"
    assert payload["disposition"]["production_promotion"] == "NOT_JUSTIFIED"
    validate_increment_23_report(report)


def test_conflict_review_is_separate_and_report_validation_is_tamper_evident() -> None:
    review = increment_23_control_conflict_review()
    assert review.frozen_blinded_judgment.value == "useful"
    assert review.frozen_control_expectation.value == "not-useful"
    assert review.disposition.value == "control-expectation-unsupported"

    report = build_increment_23_report(repository_root=Path(__file__).parents[3])
    tampered = deepcopy(report)
    tampered["payload"]["admission"]["precision"] = 1.0
    with pytest.raises(ValueError, match="envelope"):
        validate_increment_23_report(tampered)
