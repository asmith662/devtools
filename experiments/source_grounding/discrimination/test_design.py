# Copyright (c) 2026
# ruff: noqa: ANN401, PLR2004, S101, PT018, PT011, ARG005, E731 -- fictional finite candidate populations only
"""One-call scientific contracts, sampling replay and design-based arithmetic."""

import copy
from typing import Any

import pytest

from experiments.orchestration.workers import schema
from experiments.source_grounding import contracts
from experiments.source_grounding.discrimination import (
    analysis,
    estimators,
    gold,
    sampling,
)


def fixture() -> tuple[Any, Any, Any]:
    """No repository task or treatment result is used in these fixtures."""
    rows = [
        {
            "address": f"r{i}.py",
            "content": "aba aba 😀",
            "document_identity": f"doc{i}",
            "content_identity": f"content{i}",
        }
        for i in range(4)
    ]
    design = {
        "case": "SYNTHETIC-DISCRIMINATION",
        "task_text": "Find synthetic relation",
        "obligations": [
            {
                "id": "O1",
                "requirement": "synthetic",
                "satisfaction": [],
                "exclusions": [],
                "gap": None,
            },
        ],
    }
    units = [
        {
            "identity": f"pair{i}",
            "case": design["case"],
            "obligation_id": "O1",
            "source": contracts.endpoint(rows[i]),
            "target": contracts.endpoint(rows[(i + 1) % 4]),
            "references": [],
        }
        for i in range(4)
    ]
    return (
        design,
        rows,
        {"case": design["case"], "units": units, "sha256": "synthetic-universe"},
    )


def judgments(packet: Any) -> Any:
    """Explicit complete independent synthetic label grid."""
    return {
        "representation_complete": True,
        "self_review_complete": True,
        "judgments": [
            {
                "candidate_id": c["candidate_id"],
                "source_usefulness": "USEFUL",
                "target_usefulness": "USEFUL",
                "pursuit_value": "USEFUL",
                "source_evidence": [
                    {"source_key": c["source_key"], "quote": "aba", "occurrence": 2},
                ],
                "target_evidence": [
                    {"source_key": c["target_key"], "quote": "😀", "occurrence": 1},
                ],
                "pursuit_reason": "synthetic relation",
            }
            for c in packet["candidates"]
        ],
    }


def test_census_replay_capacity_and_exact_anchors() -> None:
    """Complete contents once; all labels independent; host derives Unicode spans."""
    d, r, u = fixture()
    selected = sampling.design_sample(d, r, u)
    assert selected == sampling.design_sample(d, r, u)
    assert (
        selected["sampling"] == "CENSUS" and selected["allocation"]["O1"]["weight"] == 1
    )
    assert len(selected["packet"]["resources"]) == 4
    assert selected["output_maximum"]["utf8_bytes"] <= 63357
    payload = judgments(selected["packet"])
    result = gold.project(
        selected["packet"],
        payload,
        selected["response_schema"],
        selected["host"]["resources"],
    )
    assert result["judgments"][0]["source_evidence"][0]["start"] == 4
    assert result["judgments"][0]["target_evidence"][0]["end"] == 9
    for forbidden in ("grounding", "qualified", "rank", "score", "query"):
        assert forbidden not in selected["packet"]
    maximum = schema.maximum(selected["response_schema"], bytes_measure=True)
    assert len(schema.canonical(maximum)) == selected["output_maximum"]["utf8_bytes"]


@pytest.mark.parametrize(
    "change",
    [
        "missing",
        "duplicate",
        "foreign",
        "no_evidence",
        "incomplete",
        "inconsistent",
        "overflow",
    ],
)
def test_gold_fails_closed(change: str) -> None:
    """Absence, uncertainty and inadequate representation are never repaired."""
    d, r, u = fixture()
    selected = sampling.design_sample(d, r, u)
    payload = judgments(selected["packet"])
    if change == "missing":
        payload["judgments"].pop()
    if change == "duplicate":
        payload["judgments"][1] = copy.deepcopy(payload["judgments"][0])
    if change == "foreign":
        payload["judgments"][0]["source_evidence"][0]["source_key"] = selected[
            "packet"
        ]["candidates"][0]["target_key"]
    if change == "no_evidence":
        payload["judgments"][0]["source_evidence"] = []
    if change == "incomplete":
        payload["representation_complete"] = False
    if change == "inconsistent":
        payload["judgments"][1]["source_usefulness"] = "UNCERTAIN"
    if change == "overflow":
        payload["judgments"][0]["pursuit_reason"] = "X" * 33
    with pytest.raises(ValueError):
        gold.project(
            selected["packet"],
            payload,
            selected["response_schema"],
            selected["host"]["resources"],
        )


def test_sampling_output_drives_fixed_stratum_size(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Fixed-size selection precedes content; seed and inclusion weights replay."""
    d, r, u = fixture()
    u["units"] = [{**u["units"][i % 4], "identity": str(i)} for i in range(60)]
    selected = sampling.design_sample(d, r, u)
    assert selected["sampling"] == "OBLIGATION_STRATIFIED_SRSWOR"
    allocation = selected["allocation"]["O1"]
    assert allocation["planning_margin_95"] <= 0.15
    assert allocation["inclusion_probability"] == allocation["n"] / 60
    assert selected == sampling.design_sample(d, r, u)
    monkeypatch.setattr(sampling, "OUTPUT_BYTES", 100)
    with pytest.raises(ValueError, match="Precision target"):
        sampling.design_sample(d, r, u)
    with pytest.raises(ValueError):
        sampling.half_width(4, 0)
    r[0]["content"] = "x" * 700001
    with pytest.raises(ValueError, match="census-input"):
        sampling.design_sample(d, r, u)


def test_finite_population_uncertainty_and_undefined() -> None:
    """Known stratified SRS arithmetic uses finite correction and full samples."""
    rows = [
        {"identity": str(i), "stratum": "h", "x": 1, "y": int(i % 2 == 0)}
        for i in range(10)
    ]
    s = {"h": {"N": 20, "n": 10, "weight": 2}}
    x = lambda r: r["x"]
    y = lambda r: r["y"]
    result = estimators.ratio(rows, s, x, y)
    assert result["estimate"] == 0.5
    assert result["standard_error"] == pytest.approx((0.5 * (2.5 / 9) / 10) ** 0.5)
    assert estimators.ratio(rows, s, lambda r: 0, y)["status"] == "UNDEFINED"
    assert estimators.ratio(rows, s, x, lambda r: 1)["interval_95"] is None
    census = estimators.ratio(rows, {"h": {"N": 10, "n": 10, "weight": 1}}, x, y)
    assert census["status"] == "CENSUS" and census["standard_error"] == 0
    assert (
        estimators.contrast(rows, s, result, result, x, y, x, y)["risk_difference"] == 0
    )
    assert (
        estimators.contrast(rows, s, result, {**result, "estimate": 0}, x, y, x, y)[
            "ratio_status"
        ]
        == "UNDEFINED"
    )
    assert (
        estimators.variance_total(
            rows[:1],
            {"h": {"N": 4, "n": 1, "weight": 4}},
            {"0": 1},
        )
        is None
    )
    assert estimators.inclusion(4, 2, 1) == 0.5
    assert estimators.inclusion(4, 2, 3) == 1


def test_future_join_analysis_uses_only_fictional_labels() -> None:
    """Census and cohort diagnostics retain uncertain denominators explicitly."""
    d, r, u = fixture()
    selected = sampling.design_sample(d, r, u)
    projected = gold.project(
        selected["packet"],
        judgments(selected["packet"]),
        selected["response_schema"],
        selected["host"]["resources"],
    )
    treatment = {
        "cells": [
            {
                "obligation": "O1",
                "source": contracts.endpoint(row),
                "verdict": contracts.VERDICTS[i % 3],
            }
            for i, row in enumerate(r)
        ],
    }
    result = analysis.analyze({d["case"]: (u, selected, treatment, projected)})
    assert result["cohort"]["population_pairs"] == 4
    assert result["cohort"]["candidate_reduction"] == 0.5
    assert result["cohort"]["useful_target_retention"]["status"] == "CENSUS"
    assert "NO_REPOSITORY" in result["claim_boundary"]
    treatment["cells"].pop()
    with pytest.raises(ValueError):
        analysis.joined(u, selected, treatment, projected)
