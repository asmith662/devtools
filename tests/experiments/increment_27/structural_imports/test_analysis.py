# Copyright (c) 2026
# ruff: noqa: D103, PLR2004
"""Frozen development join, reach partition, and three-state accounting."""

from __future__ import annotations

from collections import Counter
from pathlib import Path
from typing import Any, cast

from experiments.increment_27.depth_diagnostic import (
    _digest,
    _read_json,
    canonical_json_bytes,
)
from experiments.increment_27.structural_imports.analysis import (
    RESULT_NAME,
    build_results,
)

ROOT = Path("experiments/increment_27")


def test_frozen_development_result_reproduces_exact_join() -> None:
    saved = cast("dict[str, Any]", _read_json(ROOT / RESULT_NAME))
    assert saved == build_results(ROOT)
    assert (ROOT / RESULT_NAME).read_bytes() == canonical_json_bytes(saved)
    payload = cast("dict[str, Any]", saved["payload"])
    assert saved["content_identity"] == _digest(payload)
    sources = payload["sources"]
    assert len(sources["development_case_ids"]) == 24
    assert not set(sources["development_case_ids"]) & set(
        sources["heldout_case_ids_sealed"],
    )
    assert sources["new_judgment_count"] == 140
    assert sources["exact_reused_count"] == 61
    rows = payload["joined_population"]
    assert len(rows) == 201
    assert len(
        {
            (
                row["information_need"]["purpose"],
                row["information_need"]["lexical_query"],
                row["parent_snapshot_sha"],
                row["address"],
                row["usefulness_semantics"],
            )
            for row in rows
        },
    ) == len(rows)
    assert {row["judgment"] for row in rows} <= {"USEFUL", "NOT_USEFUL", "UNJUDGED"}
    surfaces = payload["surface_counts"]
    assert surfaces["structural_union"]["total_candidates"] == 109
    assert surfaces["outgoing"]["total_candidates"] == 99
    assert surfaces["incoming"]["total_candidates"] == 23
    assert surfaces["canonical_rank_gt_5"]["total_candidates"] == 43
    assert surfaces["no_positive_canonical_rank"]["total_candidates"] == 66
    assert surfaces["absent_all_saved_positive_lexical"]["total_candidates"] == 54
    assert surfaces["same_volume_lexical_control_union"]["total_candidates"] == 101
    for surface in surfaces.values():
        assert surface["total_candidates"] == sum(
            surface[state] for state in ("USEFUL", "NOT_USEFUL", "UNJUDGED")
        )
        assert surface["judged_total"] == surface["USEFUL"] + surface["NOT_USEFUL"]
        if surface["judged_total"]:
            assert surface["useful_rate_among_judged"] == round(
                surface["USEFUL"] / surface["judged_total"], 6,
            )


def test_useful_reach_direction_and_control_counts_are_deduplicated() -> None:
    payload = cast("dict[str, Any]", _read_json(ROOT / RESULT_NAME)["payload"])
    rows = payload["joined_population"]
    reach = payload["lexical_reach_useful_structural"]
    assert {name: value["count"] for name, value in reach.items()} == {
        "canonical_rank_gt_5": 23,
        "no_positive_canonical_other_saved_positive": 4,
        "absent_all_saved_positive_lexical": 11,
    }
    assert (
        sum(value["count"] for value in reach.values())
        == payload["surface_counts"]["structural_union"]["USEFUL"]
    )
    all_absent = reach["absent_all_saved_positive_lexical"]["resources"]
    assert len({(item["case_id"], item["address"]) for item in all_absent}) == 11
    overlap = [
        row for row in rows if row["outgoing_structural"] and row["incoming_structural"]
    ]
    assert len(overlap) == 13
    assert Counter(row["judgment"] for row in overlap) == {
        "USEFUL": 10,
        "NOT_USEFUL": 3,
    }
    comparison = payload["control_comparison"]
    assert comparison["case_contingency"] == {
        "structure_only": 4,
        "lexical_control_only": 3,
        "both": 14,
        "neither": 3,
    }
    assert len(payload["per_case"]) == 24
    assert sum(row["structural_candidates"] for row in payload["per_case"]) == 109
    assert sum(row["useful_structural"] for row in payload["per_case"]) == 38
    assert sum(row["unjudged_structural"] for row in payload["per_case"]) == 20
    assert payload["unjudged"]["absent_all_saved_positive_lexical"] == 12
    assert payload["heldout_executed"] is False
    assert payload["suspended_increment_26_confirmation_executed"] is False
    assert payload["judgments_changed"] is False
