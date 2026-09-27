# Copyright (c) 2026
# ruff: noqa: D103, PLR2004
"""Validate frozen neutral judgments before any candidate-origin join."""

from __future__ import annotations

from typing import Any, cast

from experiments.increment_27.depth_diagnostic import _read_json, sha256_file
from experiments.increment_27.structural_imports.mechanics import _digest
from experiments.increment_29.judgments import (
    INPUT_IDENTITY,
    INPUT_NAME,
    INPUT_SHA256,
    OUTPUT_NAME,
    ROOT,
    SEMANTICS,
    STATES,
    build_judgments,
)


def test_frozen_neutral_judgments_have_exact_coverage_and_no_origin() -> None:
    blind = cast("dict[str, Any]", _read_json(ROOT / INPUT_NAME))
    frozen = cast("dict[str, Any]", _read_json(ROOT / OUTPUT_NAME))
    assert blind["content_identity"] == INPUT_IDENTITY
    assert sha256_file(ROOT / INPUT_NAME) == INPUT_SHA256
    assert frozen == build_judgments()
    assert frozen["content_identity"] == _digest(frozen["payload"])
    payload = frozen["payload"]
    assert payload["blinded_input_content_identity"] == INPUT_IDENTITY
    assert payload["blinded_input_sha256"] == INPUT_SHA256
    assert payload["usefulness_semantics"] == SEMANTICS
    assert payload["three_states"] == list(STATES)
    targets = {
        (case["neutral_case_id"], resource["neutral_resource_id"])
        for case in blind["payload"]["cases"]
        for resource in case["resources"]
    }
    records = payload["records"]
    judged = {(row["neutral_case_id"], row["neutral_resource_id"]) for row in records}
    assert len(targets) == len(judged) == len(records) == payload["target_count"] == 19
    assert judged == targets
    assert all(
        row["judgment"] in STATES and row["rationale"].strip() for row in records
    )
    assert payload["state_counts"] == {
        "USEFUL": 2,
        "NOT_USEFUL": 17,
        "UNJUDGED": 0,
    }
    assert set().union(*(set(row) for row in records)) == {
        "neutral_case_id",
        "information_need",
        "parent_snapshot_sha",
        "neutral_resource_id",
        "address",
        "usefulness_semantics",
        "judgment",
        "rationale",
    }
