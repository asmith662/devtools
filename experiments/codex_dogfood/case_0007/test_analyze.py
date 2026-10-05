# Copyright (c) 2026
"""Focused integrity checks for the frozen Case 0007 Stage D analysis."""

from __future__ import annotations

import importlib.util
from pathlib import Path

import pytest

MODULE_PATH = Path(__file__).with_name("analyze.py")
SPEC = importlib.util.spec_from_file_location("case_0007_analyze", MODULE_PATH)
assert SPEC is not None and SPEC.loader is not None
ANALYSIS = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(ANALYSIS)


def test_joined_gold_and_structural_counts() -> None:
    result, _ = ANALYSIS.compute()

    assert result["join_integrity"]["judgment_cells_observed"] == 5_731
    assert result["gold"]["required_cells"] == 55
    assert result["gold"]["required_unit_judgments"] == 56
    assert result["sufficient_combinations"]["combination_count"] == 432
    assert result["structural_surfaces"]["ALL"]["candidate_resources"] == 19
    assert result["reference_marginal"]["new_required_cells"] == 0
    assert result["overflow"]["counterfactual_required_cells"] == 0


def test_writer_refuses_to_overwrite_frozen_analysis() -> None:
    with pytest.raises(FileExistsError):
        ANALYSIS.write()
