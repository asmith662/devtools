# Copyright (c) 2026
# ruff: noqa: D103, PLR2004
"""Sampled Graph-1 result preserves complete reach and partial outcomes."""

from __future__ import annotations

from experiments.increment_30.mechanics import _verified_json
from experiments.increment_32.analysis import RESULT_NAME, build_results
from experiments.increment_32.mechanics import CANDIDATES_NAME, ROOT


def test_development_result_keeps_four_population_counts_distinct() -> None:
    result = _verified_json(ROOT / RESULT_NAME)
    assert result == build_results(ROOT)
    payload = result["payload"]
    counts = payload["population_counts"]
    assert counts["complete_novel_candidate_pairs"] == 704
    assert counts["exact_reused"] == 2
    assert counts["new_sampled_adjudicated"] == 128
    assert counts["unsampled_unadjudicated"] == 574
    assert counts["sampled_states"] == {"USEFUL": 2, "NOT_USEFUL": 126, "UNJUDGED": 0}
    assert counts["reused_states"] == {"USEFUL": 0, "NOT_USEFUL": 2, "UNJUDGED": 0}
    assert payload["unsampled_semantic_judgments_assigned"] is False
    assert payload["complete_outcome_coverage_claimed"] is False
    assert len(payload["sampled_pairs"]) == 128
    assert len(payload["reused_pairs"]) == 2
    assert len(payload["sampled_useful_pairs"]) == 2
    assert all(row["judgment"] == "USEFUL" for row in payload["sampled_useful_pairs"])
    interval = payload["sampled_useful_proportion"]
    assert interval["sampled_fraction"] == 2 / 128
    assert interval["lower"] < 2 / 128 < interval["upper"]
    assert interval["finite_population_correction"] is False
    mechanics = _verified_json(ROOT / CANDIDATES_NAME)
    assert payload["outcome_free_reach_and_cost"] == mechanics["summary"]
    assert (
        payload["breadth_verdict"] == "sampled useful complementary reach established"
    )
