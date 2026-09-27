# Copyright (c) 2026
# ruff: noqa: D103, PLR2004
"""Validate frozen neutral judgments without opening candidate origins."""

from __future__ import annotations

from typing import Any, cast

from experiments.increment_27.depth_diagnostic import _read_json, sha256_file
from experiments.increment_27.structural_imports.mechanics import _digest
from experiments.increment_30.judgments import (
    INPUT_IDENTITY,
    INPUT_NAME,
    INPUT_SHA256,
    OUTPUT_NAME,
    ROOT,
    STATES,
    build_judgments,
)


def test_exact_neutral_judgment_coverage_and_blinding() -> None:
    blind = cast("dict[str, Any]", _read_json(ROOT / INPUT_NAME))
    assert blind["content_identity"] == INPUT_IDENTITY == _digest(blind["payload"])
    assert sha256_file(ROOT / INPUT_NAME) == INPUT_SHA256
    built = build_judgments(ROOT)
    frozen = cast("dict[str, Any]", _read_json(ROOT / OUTPUT_NAME))
    assert frozen == built
    assert frozen["content_identity"] == _digest(frozen["payload"])
    payload = frozen["payload"]
    assert payload["blinded_input_content_identity"] == INPUT_IDENTITY
    assert payload["blinded_input_sha256"] == INPUT_SHA256
    assert payload["target_count"] == len(payload["records"]) == 20
    assert set(payload["three_states"]) == set(STATES)
    targets = {
        (case["neutral_case_id"], resource["neutral_resource_id"])
        for case in blind["payload"]["cases"]
        for resource in case["resources"]
    }
    judged = {
        (row["neutral_case_id"], row["neutral_resource_id"])
        for row in payload["records"]
    }
    assert len(targets) == len(judged) == 20
    assert targets == judged
    assert set(payload["state_counts"]) == set(STATES)
    assert sum(payload["state_counts"].values()) == 20
    assert all(
        row["judgment"] in STATES and row["rationale"].strip()
        for row in payload["records"]
    )
    allowed = {
        "neutral_case_id",
        "information_need",
        "parent_snapshot_sha",
        "neutral_resource_id",
        "address",
        "usefulness_semantics",
        "judgment",
        "rationale",
    }
    assert all(set(row) == allowed for row in payload["records"])
