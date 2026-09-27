# Copyright (c) 2026
# ruff: noqa: E501, PLR2004
"""Post-checkpoint exact-label join and descriptive result checks."""

from __future__ import annotations

import json

from experiments.increment_27.structural_imports.analysis import _verify_and_join
from experiments.increment_28.analysis import (
    PRE_OUTCOME_COMMIT,
    RESULT_NAME,
    build_results,
)
from experiments.increment_28.import_use import ROOT27


def test_post_checkpoint_join_preserves_exact_frozen_states() -> None:
    """Every outgoing state is reused from the validated frozen population."""
    saved = json.loads((ROOT27.parent / "increment_28" / RESULT_NAME).read_text(encoding="utf-8"))
    assert saved == build_results()
    joined, _sources = _verify_and_join(ROOT27)
    existing = {
        (row["case_id"], row["address"]): row["judgment"]
        for row in joined if row["outgoing_structural"]
    }
    pairs = saved["payload"]["pairs"]
    assert len(pairs) == len(existing) == 99
    assert {(row["case_id"], row["address"]) for row in pairs} == set(existing)
    assert all(row["judgment"] == existing[row["case_id"], row["address"]] for row in pairs)
    assert saved["payload"]["new_judgments"] == 0
    assert saved["payload"]["judgments_changed"] is False
    assert saved["payload"]["heldout_executed"] is False
    assert saved["payload"]["pre_outcome_commit"] == PRE_OUTCOME_COMMIT
    assert saved["payload"]["hard_lexical_escapes"]["all"]["pairs"] == 52
    assert sum(group["pairs"] for group in saved["payload"]["categories"].values()) == 99
