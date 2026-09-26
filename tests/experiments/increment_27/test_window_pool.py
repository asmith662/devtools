# Copyright (c) 2026
# ruff: noqa: COM812, PLR2004
"""Check the frozen retrieval-unit pool, exact reuse, and neutral boundary."""

from __future__ import annotations

from pathlib import Path
from typing import Any, cast

from experiments.increment_25.development import _task_card
from experiments.increment_27.depth_diagnostic import (
    _read_json,
    canonical_json_bytes,
    prior_judgment_matches,
)
from experiments.increment_27.window_pool import STATES, candidate_surface
from experiments.increment_27.window_unit import _digest

ROOT = Path(__file__).resolve().parents[3] / "experiments" / "increment_27"


def test_pool_identity_partition_and_exact_reuse() -> None:
    """Every pooled resource is either exact reuse or a new neutral target."""
    pairs, freeze, ranking = candidate_surface(ROOT)
    pool = cast("dict[str, Any]", _read_json(ROOT / "window_unit_pool.json"))
    assert pool["content_identity"] == _digest(
        {key: value for key, value in pool.items() if key != "content_identity"}
    )
    assert pool["window_freeze_identity"] == freeze["content_identity"]
    assert pool["window_rankings_identity"] == ranking["content_identity"]
    assert pool["pairs"] == pairs
    assert pool["counts"] == {"pooled": 150, "reused": 138, "new": 12}
    keys = {(row["case_id"], row["address"]) for row in pairs}
    reused = {(row["case_id"], row["address"]) for row in pool["reused"]}
    new = {(row["case_id"], row["address"]) for row in pool["new_pairs"]}
    assert len(keys) == len(pairs)
    assert len(reused) == len(pool["reused"])
    assert len(new) == len(pool["new_pairs"])
    assert reused.isdisjoint(new)
    assert keys == reused | new
    assert {row["judgment"] for row in pool["reused"]} <= STATES
    assert all("judgment" not in row for row in pool["new_pairs"])
    heldout = set(cast("dict[str, Any]", freeze["payload"])["heldout_case_ids_sealed"])
    assert not {case_id for case_id, _address in keys} & heldout
    assert pool["heldout_executed"] is False
    assert pool["comparison_performed"] is False
    assert (ROOT / "window_unit_pool.json").read_bytes() == canonical_json_bytes(pool)
    assert (
        ROOT / "window_resource_rankings.json"
    ).read_bytes() == canonical_json_bytes(ranking)
    assert (
        sum(
            row["window_top5_rank"] is not None and row["whole_top5_rank"] is None
            for row in pairs
        )
        == 30
    )
    assert all(
        row["whole_positive_rank"] is not None
        for row in pairs
        if row["window_top5_rank"] is not None
    )


def test_blinded_input_has_exact_new_pairs_and_no_origin() -> None:
    """Neutral input contains only purpose, query, snapshot, address, and content."""
    pool = cast("dict[str, Any]", _read_json(ROOT / "window_unit_pool.json"))
    blind = cast(
        "dict[str, Any]", _read_json(ROOT / "window_unit_blinded_judgment_input.json")
    )
    assert blind["content_identity"] == _digest(
        {key: value for key, value in blind.items() if key != "content_identity"}
    )
    assert blind["pool_identity"] == pool["content_identity"]
    expected = {
        (
            row["information_need"]["purpose"],
            row["information_need"]["lexical_query"],
            row["parent_snapshot_sha"],
            row["address"],
        )
        for row in pool["new_pairs"]
    }
    actual = set()
    for case in blind["cases"]:
        assert set(case) == {
            "neutral_case_id",
            "information_need",
            "parent_snapshot_sha",
            "resources",
        }
        assert set(case["information_need"]) == {"purpose", "lexical_query"}
        assert [row["neutral_resource_id"] for row in case["resources"]] == sorted(
            row["neutral_resource_id"] for row in case["resources"]
        )
        for resource in case["resources"]:
            assert set(resource) == {"neutral_resource_id", "address", "content"}
            actual.add(
                (
                    case["information_need"]["purpose"],
                    case["information_need"]["lexical_query"],
                    case["parent_snapshot_sha"],
                    resource["address"],
                )
            )
    assert len(actual) == 12
    assert actual == expected
    assert [case["neutral_case_id"] for case in blind["cases"]] == sorted(
        case["neutral_case_id"] for case in blind["cases"]
    )
    assert (
        ROOT / "window_unit_blinded_judgment_input.json"
    ).read_bytes() == canonical_json_bytes(blind)


def test_prior_reuse_requires_exact_identity() -> None:
    """A changed purpose, snapshot, address, or semantics blocks reuse."""
    pool = cast("dict[str, Any]", _read_json(ROOT / "window_unit_pool.json"))
    row = pool["reused"][0]
    population = cast(
        "dict[str, Any]",
        _read_json(ROOT.parent / "increment_25" / "task_population_freeze.json"),
    )
    card = next(
        _task_card(candidate)
        for candidate in population["payload"]["task_cards"]
        if candidate["case_id"] == row["case_id"]
    )
    need = row["information_need"]
    base = {
        "card": card,
        "prior_information_need": need,
        "prior_parent_snapshot": row["parent_snapshot_sha"],
        "prior_address": row["address"],
        "resource_address": row["address"],
        "prior_usefulness_semantics": row["judgment_semantics"],
    }
    assert prior_judgment_matches(**base)
    assert not prior_judgment_matches(
        **{**base, "prior_information_need": {**need, "purpose": "changed"}}
    )
    assert not prior_judgment_matches(**{**base, "prior_parent_snapshot": "changed"})
    assert not prior_judgment_matches(**{**base, "prior_address": "changed"})
    assert not prior_judgment_matches(
        **{**base, "prior_usefulness_semantics": "changed"}
    )
