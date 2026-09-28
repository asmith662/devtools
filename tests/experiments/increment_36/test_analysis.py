# Copyright (c) 2026
# ruff: noqa: COM812, D103, PLR2004
"""Post-freeze fusion result and preserved unknownness tests."""

from __future__ import annotations

from typing import Any, cast

import pytest

from experiments.increment_27.depth_diagnostic import _read_json
from experiments.increment_36 import analysis
from experiments.increment_36.analysis import RESULT_NAME, build_result
from experiments.increment_36.mechanics import ROOT


@pytest.fixture(scope="module")
def result() -> dict[str, Any]:
    return build_result()


def test_freeze_is_required_before_outcome_join(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setattr(analysis, "FROZEN_SHA256", "invalid")
    with pytest.raises(ValueError, match="Pre-outcome fusion freeze differs"):
        analysis.build_result()


def test_exact_k5_outcomes_and_unknownness(result: dict[str, Any]) -> None:
    p = result["payload"]
    assert {
        name: row["selected_candidate_pairs"]
        for name, row in p["strategy_summaries"].items()
    } == {"canonical": 120, "lexical_rrf": 120, "fusion": 120}
    assert p["strategy_summaries"]["canonical"]["states"] == {
        "USEFUL": 63,
        "NOT_USEFUL": 52,
        "UNJUDGED": 5,
        "NEVER_ADJUDICATED": 0,
    }
    assert p["strategy_summaries"]["lexical_rrf"]["states"] == {
        "USEFUL": 74,
        "NOT_USEFUL": 41,
        "UNJUDGED": 5,
        "NEVER_ADJUDICATED": 0,
    }
    assert p["strategy_summaries"]["fusion"]["states"] == {
        "USEFUL": 73,
        "NOT_USEFUL": 40,
        "UNJUDGED": 7,
        "NEVER_ADJUDICATED": 0,
    }
    assert (
        p["strategy_summaries"]["fusion"]["cases_with_at_least_one_known_useful"] == 20
    )
    assert (
        p["strategy_summaries"]["fusion"]["cases_with_at_least_two_known_useful"] == 18
    )
    assert not p["new_judgments_created"]
    assert not p["confirmation_executed"]


def test_canonical_rrf_and_oracle_comparisons(result: dict[str, Any]) -> None:
    p = result["payload"]
    assert p["canonical_comparison"] == {
        "candidate_overlap": 76,
        "replacements": 44,
        "useful_additions": 25,
        "useful_displacements": 15,
        "net_known_useful_change": 10,
    }
    assert p["lexical_rrf_comparison"] == {
        "candidate_overlap": 96,
        "net_known_useful_change": -1,
    }
    assert p["known_useful_oracle"]["total_at_k5"] == 99
    assert p["known_useful_oracle"]["available_headroom"] == 36
    assert p["known_useful_oracle"]["fusion_increment_over_canonical"] == 10
    assert p["case_change_counts"] == {"improved": 10, "unchanged": 12, "worsened": 2}
    assert len(p["per_case"]) == 24
    assert sum(row["delta_known_useful"] for row in p["per_case"]) == 10


def test_dense_coverage_and_structural_order_boundary(result: dict[str, Any]) -> None:
    p = result["payload"]
    assert p["dense_coverage"]["available"]["case_count"] == 8
    assert p["dense_coverage"]["unavailable"]["case_count"] == 16
    assert p["dense_coverage"]["available"]["fusion"]["states"]["USEFUL"] == 18
    assert p["dense_coverage"]["unavailable"]["fusion"]["states"]["USEFUL"] == 55
    assert p["dense_supported_selected"] == 37
    assert p["structural_only_selected"] == 0
    assert p["graph_supported_selected"] == 1
    assert not p["structural_rank_available"]
    assert not p["graph_rank_available"]


def test_deterministic_result_and_frozen_candidate_membership(
    result: dict[str, Any],
) -> None:
    assert result == _read_json(ROOT / RESULT_NAME) == build_result()
    p = result["payload"]
    union = cast(
        "dict[str, Any]",
        _read_json(
            ROOT.parent / "increment_35/heterogeneous_union_development_results.json"
        ),
    )
    addresses = {
        (row["case_id"], row["parent_snapshot_sha"], row["address"])
        for row in union["payload"]["candidates"]
    }
    assert all(
        (row["case_id"], row["parent_snapshot_sha"], row["address"]) in addresses
        for row in p["selected_pairs"]["fusion"]
    )
