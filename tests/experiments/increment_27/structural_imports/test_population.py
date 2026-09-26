# Copyright (c) 2026
# ruff: noqa: COM812, D103, PLR2004
"""Exact new-pair deduplication and origin-blind input boundaries."""

from __future__ import annotations

from pathlib import Path

from experiments.increment_27.depth_diagnostic import _read_json, canonical_json_bytes
from experiments.increment_27.phase1_population import _neutral_id
from experiments.increment_27.structural_imports.mechanics import _digest
from experiments.increment_27.structural_imports.population import (
    BLIND_NAME,
    FREEZE_NAME,
    build_population,
)

ROOT = Path("experiments/increment_27")


def test_saved_population_is_exact_reuse_union_and_blind() -> None:
    freeze, blind = build_population(ROOT)
    assert freeze == _read_json(ROOT / FREEZE_NAME)
    assert blind == _read_json(ROOT / BLIND_NAME)
    assert (ROOT / FREEZE_NAME).read_bytes() == canonical_json_bytes(freeze)
    assert (ROOT / BLIND_NAME).read_bytes() == canonical_json_bytes(blind)
    assert freeze["content_identity"] == _digest(freeze["payload"])
    assert blind["content_identity"] == _digest(blind["payload"])
    payload = freeze["payload"]
    evidence = payload["pair_evidence"]
    reused = payload["reused_judgments"]
    new = payload["new_judgment_pairs"]
    counts = payload["counts"]
    assert len(evidence) == len(reused) + len(new)
    assert len({(row["case_id"], row["address"]) for row in evidence}) == len(evidence)
    assert len({(row["case_id"], row["address"]) for row in new}) == len(new)
    assert (
        sum(
            len(paths)
            for row in evidence
            for paths in row["structural_supports"].values()
        )
        == 652
    )
    structural = {
        (row["case_id"], row["address"])
        for row in evidence
        if row["outgoing_structural"] or row["incoming_structural"]
    }
    control = {
        (row["case_id"], row["address"])
        for row in evidence
        if row["outgoing_lexical_control"] or row["incoming_lexical_control"]
    }
    new_keys = {(row["case_id"], row["address"]) for row in new}
    reused_keys = {(row["case_id"], row["address"]) for row in reused}
    assert structural | control == new_keys | reused_keys
    assert counts == {
        "structural_total": len(structural),
        "structural_reused": len(structural & reused_keys),
        "structural_new": len(structural & new_keys),
        "control_total": len(control),
        "control_reused": len(control & reused_keys),
        "control_new": len(control & new_keys),
        "new_overlap": len(structural & control & new_keys),
        "new_deduplicated": len(new_keys),
    }
    assert set(payload["three_states"]) == {"USEFUL", "NOT_USEFUL", "UNJUDGED"}
    assert {row["judgment"] for row in reused} <= set(payload["three_states"])
    assert all("judgment" not in row for row in new)

    candidate_identity = payload["candidate_content_identity"]
    blinded_keys: set[tuple[str, str]] = set()
    assert set(blind["payload"]) == {"schema", "cases"}
    for case in blind["payload"]["cases"]:
        assert set(case) == {
            "neutral_case_id",
            "information_need",
            "parent_snapshot_sha",
            "resources",
        }
        matching = [
            row
            for row in new
            if _neutral_id("case", f"{candidate_identity}|{row['case_id']}")
            == case["neutral_case_id"]
        ]
        assert matching
        assert case["information_need"] == matching[0]["information_need"]
        assert case["parent_snapshot_sha"] == matching[0]["parent_snapshot_sha"]
        for resource in case["resources"]:
            assert set(resource) == {"neutral_resource_id", "address", "content"}
            row = next(row for row in matching if row["address"] == resource["address"])
            assert resource["neutral_resource_id"] == _neutral_id(
                "resource", f"{candidate_identity}|{row['case_id']}|{row['address']}"
            )
            blinded_keys.add((row["case_id"], row["address"]))
    assert blinded_keys == new_keys
    assert not set(payload["development_case_ids"]) & set(
        payload["heldout_case_ids_sealed"]
    )
    assert payload["heldout_executed"] is False
    assert payload["suspended_increment_26_confirmation_not_executed"] is True
    assert payload["new_usefulness_outcomes"] is False
