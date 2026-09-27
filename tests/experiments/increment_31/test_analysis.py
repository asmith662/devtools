# Copyright (c) 2026
# ruff: noqa: COM812, D103, PLR2004
"""Exact development result after blind judgments were frozen."""

from __future__ import annotations

from experiments.increment_27.depth_diagnostic import sha256_file
from experiments.increment_30.mechanics import _verified_json
from experiments.increment_31.analysis import (
    EXPECTED_IDENTITIES,
    RESULT_NAME,
    SOURCE_NAMES,
    build_results,
)
from experiments.increment_31.mechanics import CANDIDATES_NAME, ROOT


def test_completed_join_preserves_frozen_mechanics_and_three_states() -> None:
    result = _verified_json(ROOT / RESULT_NAME)
    assert result == build_results(ROOT)
    payload = result["payload"]
    assert payload["source_content_identities"] == EXPECTED_IDENTITIES
    assert payload["source_sha256"] == {
        name: sha256_file(ROOT / name) for name in SOURCE_NAMES
    }
    assert payload["candidate_mechanics_changed"] is False
    assert payload["confirmation_executed"] is False
    assert len(payload["development_case_ids"]) == 24
    assert len(payload["heldout_case_ids_sealed"]) == 14
    assert set(payload["development_case_ids"]).isdisjoint(
        payload["heldout_case_ids_sealed"]
    )
    assert payload["surface_counts"]["union"] == {
        "candidate_pairs": 34,
        "USEFUL": 21,
        "NOT_USEFUL": 13,
        "UNJUDGED": 0,
        "judged_total": 34,
    }
    assert payload["surface_counts"]["new_blinded"]["candidate_pairs"] == 12
    assert payload["surface_counts"]["exact_reuse"]["candidate_pairs"] == 22
    assert payload["surface_counts"]["complete_existing_evidence_escape"] == {
        "candidate_pairs": 1,
        "USEFUL": 0,
        "NOT_USEFUL": 1,
        "UNJUDGED": 0,
        "judged_total": 1,
    }
    assert payload["useful_escape_pairs"]["complete_existing_evidence_escape"] == []
    assert (
        len(payload["joined_pairs"])
        == len({(row["case_id"], row["address"]) for row in payload["joined_pairs"]})
        == 34
    )
    assert payload["source_sha256"][CANDIDATES_NAME] == sha256_file(
        ROOT / CANDIDATES_NAME
    )
