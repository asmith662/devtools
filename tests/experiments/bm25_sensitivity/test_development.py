# Copyright (c) 2026
# ruff: noqa: PLR2004 -- frozen factorial evidence
"""Validate complete cross-case partitions and deterministic selection replay."""

from __future__ import annotations

import math

from experiments.bm25_sensitivity.protocol import BASELINE, GRID, select
from experiments.bm25_sensitivity.storage import HERE, get
from experiments.bm25_sensitivity.study import pareto, report, surfaces
from experiments.bm25_sensitivity.summary import summarize
from experiments.codex_dogfood.case_0009.artifacts import binary


def test_complete_grid_replay_and_missing_alternatives() -> None:
    """No missing configuration, unsafe reach, synthetic completion or scalar winner."""
    data = get(HERE / "development.json.gz")
    assert [tuple(r["parameters"]) for r in data["rows"]] == list(GRID)
    assert select(data["rows"]) == data["selection"]
    assert pareto(data["rows"]) == data["pareto"]
    assert surfaces(data["rows"]) == data["surfaces"]
    assert report(data).encode() == binary(HERE / "analysis.md")
    for row in data["rows"]:
        assert row["reach_safe"]
        assert [c["case"] for c in row["cases"]] == list(range(4, 10))
        for case in row["cases"]:
            assert len(case["required_cells_reached"]) <= case["required_cells_total"]
            if case["case"] == 8:
                assert not case["selection_eligible"]
                assert case["max_own"] is None
                assert case["prefix_union"] is None
                assert len(case["required_cells_reached"]) == 48
            else:
                assert case["selection_eligible"]
                assert (
                    len(case["required_cells_reached"]) == case["required_cells_total"]
                )
                if tuple(row["parameters"]) == BASELINE:
                    assert all(v == 1 for v in case["normalized"].values())


def test_diagnostic_score_reconstruction_and_parameter_only_effects() -> None:
    """Derived explanations agree with captured scores and retain lexical invariants."""
    data = get(HERE / "diagnostics.json.gz")
    assert {r["case"] for r in data["records"]} == set(range(4, 10))
    for record in data["records"]:
        for side in ("A", "B"):
            explanation = record[side]
            score = sum(t["weighted_contribution"] for t in explanation["terms"])
            assert math.isclose(score, explanation["score"], abs_tol=1e-10)
            if explanation["captured_score"] is not None:
                assert explanation["score_reconstructed"]
                assert math.isclose(score, explanation["captured_score"], abs_tol=1e-10)
        assert record["pair"]["changed_query_terms"] == {"added": [], "removed": []}
        for term in record["pair"]["mechanics"]["term_deltas"]:
            if term["A"] and term["B"]:
                assert term["tf_delta"] == term["df_delta"] == term["idf_delta"] == 0


def test_sensitivity_details_replay_and_baseline_interaction_zero() -> None:
    """Derived cross-case slices/ranges/contrasts retain undefined completions."""
    details = get(HERE / "sensitivity_details.json")
    assert summarize(get(HERE / "development.json.gz")) == details
    for record in details["interactions"]:
        if tuple(record["parameters"]) == BASELINE:
            assert all(
                v in (0, None) for v in record["finite_interaction_contrast"].values()
            )
