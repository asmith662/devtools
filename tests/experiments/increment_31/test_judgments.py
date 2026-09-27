# Copyright (c) 2026
# ruff: noqa: D103, PLR2004
"""Origin-blind exact target coverage of the frozen 12-pair population."""

from __future__ import annotations

from experiments.increment_27.depth_diagnostic import sha256_file
from experiments.increment_30.mechanics import _verified_json
from experiments.increment_31.judgments import (
    INPUT_IDENTITY,
    INPUT_NAME,
    INPUT_SHA256,
    OUTPUT_NAME,
    ROOT,
    STATES,
    build_judgments,
)


def test_neutral_judgments_are_exactly_frozen_before_origin_join() -> None:
    blind = _verified_json(ROOT / INPUT_NAME)
    artifact = _verified_json(ROOT / OUTPUT_NAME)
    assert blind["content_identity"] == INPUT_IDENTITY
    assert sha256_file(ROOT / INPUT_NAME) == INPUT_SHA256
    assert artifact == build_judgments(ROOT)
    payload = artifact["payload"]
    assert payload["target_count"] == 12
    assert payload["state_counts"] == {"USEFUL": 5, "NOT_USEFUL": 7, "UNJUDGED": 0}
    assert payload["blinded_input_content_identity"] == INPUT_IDENTITY
    assert payload["blinded_input_sha256"] == INPUT_SHA256
    assert set(payload["three_states"]) == set(STATES)
    targets = {
        (
            case["neutral_case_id"],
            row["neutral_resource_id"],
            case["parent_snapshot_sha"],
            row["address"],
        )
        for case in blind["payload"]["cases"]
        for row in case["resources"]
    }
    records = {
        (
            row["neutral_case_id"],
            row["neutral_resource_id"],
            row["parent_snapshot_sha"],
            row["address"],
        )
        for row in payload["records"]
    }
    assert len(targets) == len(records) == len(payload["records"]) == 12
    assert targets == records
    assert all(
        row["judgment"] in STATES and row["rationale"].strip()
        for row in payload["records"]
    )
    assert all(
        set(row)
        == {
            "neutral_case_id",
            "information_need",
            "parent_snapshot_sha",
            "neutral_resource_id",
            "address",
            "usefulness_semantics",
            "judgment",
            "rationale",
        }
        for row in payload["records"]
    )
