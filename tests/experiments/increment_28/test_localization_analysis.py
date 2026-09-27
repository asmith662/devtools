# Copyright (c) 2026
# ruff: noqa: E501, PLR2004
"""Post-checkpoint localization join preserves exact frozen judgments."""

from __future__ import annotations

import json

from experiments.increment_27.structural_imports.analysis import _verify_and_join
from experiments.increment_28.import_use import ROOT27
from experiments.increment_28.localization.analysis import RESULT_NAME, build_results
from experiments.increment_28.localization.evidence import ROOT28


def test_localization_join_reuses_every_existing_outgoing_state() -> None:
    """The post-outcome artifact changes neither pairs nor three-state labels."""
    result = json.loads((ROOT28 / RESULT_NAME).read_text(encoding="utf-8"))
    assert result == build_results()
    joined, _sources = _verify_and_join(ROOT27)
    existing = {
        (row["case_id"], row["address"]): row["judgment"]
        for row in joined if row["outgoing_structural"]
    }
    pairs = result["payload"]["pairs"]
    assert len(existing) == len(pairs) == 99
    assert {(row["case_id"], row["address"]) for row in pairs} == set(existing)
    assert all(row["judgment"] == existing[row["case_id"], row["address"]] for row in pairs)
    assert result["payload"]["new_candidates"] == result["payload"]["new_judgments"] == 0
    assert result["payload"]["judgments_changed"] is False
    assert result["payload"]["heldout_executed"] is False
    assert result["payload"]["suspended_increment_26_confirmation_executed"] is False


def test_primary_control_retains_unknowns_and_coarse_cell_sizes() -> None:
    """Inside, outside-only, and unknown surfaces remain distinct."""
    payload = build_results()["payload"]
    groups = payload["groups"]
    assert sum(row["pairs"] for row in groups.values()) == 99
    assert payload["single_support"]["all"]["pairs"] == 29
    assert payload["hard_lexical_escapes"]["all"]["pairs"] == 52
    assert payload["paired_case_control"]["case_count"] == 11
    for stratum in payload["exact_coarse_matched_strata"]:
        assert stratum["inside"]["pairs"] > 0
        assert stratum["outside_only"]["pairs"] > 0
    assert len(payload["development_case_ids"]) == 24
