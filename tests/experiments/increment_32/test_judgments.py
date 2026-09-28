# Copyright (c) 2026
# ruff: noqa: COM812, D103, PLR2004
"""Exact 128-target blinded judgment coverage."""

from __future__ import annotations

from experiments.increment_30.mechanics import _verified_json
from experiments.increment_32.judgments import JUDGMENTS_NAME, build_judgments
from experiments.increment_32.mechanics import ROOT
from experiments.increment_32.sampling import FREEZE_NAME, SAMPLED_INPUT_NAME
from experiments.retrieval_judgment_coverage import validate_frozen_judgment_coverage


def test_sampled_decisions_cover_only_frozen_neutral_targets() -> None:
    sampling = _verified_json(ROOT / FREEZE_NAME)
    blind = _verified_json(ROOT / SAMPLED_INPUT_NAME)
    judgments = _verified_json(ROOT / JUDGMENTS_NAME)
    assert judgments == build_judgments(ROOT)
    payload = judgments["payload"]
    assert payload["sampling_freeze_content_identity"] == sampling["content_identity"]
    assert payload["sampled_input_content_identity"] == blind["content_identity"]
    assert payload["target_count"] == 128
    assert payload["state_counts"] == {"USEFUL": 2, "NOT_USEFUL": 126, "UNJUDGED": 0}
    assert payload["candidate_origins_accessed_during_adjudication"] is False
    selected = {tuple(row) for row in sampling["payload"]["sampled_neutral_identities"]}
    assert {
        (row["neutral_case_id"], row["neutral_resource_id"])
        for row in payload["records"]
    } == selected
    targets = [
        {
            "neutral_case_id": case["neutral_case_id"],
            "neutral_resource_id": resource["neutral_resource_id"],
            "information_need": case["information_need"],
            "parent_snapshot_sha": case["parent_snapshot_sha"],
            "address": resource["address"],
            "usefulness_semantics": payload["usefulness_semantics"],
        }
        for case in blind["payload"]["cases"]
        for resource in case["resources"]
    ]
    assert (
        len(
            validate_frozen_judgment_coverage(
                targets, payload["records"], payload["three_states"], selected
            )
        )
        == 128
    )
    assert all(row["rationale"].strip() for row in payload["records"])
