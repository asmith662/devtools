# Copyright (c) 2026
# ruff: noqa: PLR2004
"""Post-freeze retrieval-unit development accounting from saved evidence."""

from __future__ import annotations

import copy
from pathlib import Path
from typing import Any, cast

import pytest

from experiments.increment_27.depth_diagnostic import (
    _read_json,
    canonical_json_bytes,
    sha256_file,
)
from experiments.increment_27.window_results import (
    JUDGMENT_IDENTITY,
    JUDGMENT_SHA256,
    POOL_SHA256,
    RANKINGS_SHA256,
    build_results,
    join_frozen_labels,
    load_verified_sources,
)
from experiments.increment_27.window_unit import _digest

ROOT = Path(__file__).resolve().parents[3] / "experiments" / "increment_27"
RESULT = ROOT / "window_unit_development_results.json"


def test_exact_source_binding_and_deterministic_result() -> None:
    """No saved ranking or frozen label can change silently after the join."""
    first = build_results(ROOT)
    second = build_results(ROOT)
    persisted = cast("dict[str, Any]", _read_json(RESULT))
    assert first == second == persisted
    assert RESULT.read_bytes() == canonical_json_bytes(first)
    assert first["content_identity"] == _digest(first["payload"])
    payload = first["payload"]
    assert (
        payload["pool_sha256"]
        == sha256_file(ROOT / "window_unit_pool.json")
        == POOL_SHA256
    )
    assert (
        payload["window_rankings_sha256"]
        == sha256_file(ROOT / "window_resource_rankings.json")
        == RANKINGS_SHA256
    )
    assert (
        payload["frozen_judgment_sha256"]
        == sha256_file(ROOT / "window_unit_frozen_judgments.json")
        == JUDGMENT_SHA256
    )
    assert payload["frozen_judgment_identity"] == JUDGMENT_IDENTITY
    assert payload["heldout_executed"] is False


def test_complete_three_state_arm_and_union_accounting() -> None:
    """The 150-pair union partitions each equal-capacity resource surface."""
    payload = build_results(ROOT)["payload"]
    assert payload["union"] == {
        "total": 150,
        "USEFUL": 75,
        "NOT_USEFUL": 68,
        "UNJUDGED": 7,
    }
    assert payload["surfaces"] == {
        "whole": {"total": 120, "USEFUL": 63, "NOT_USEFUL": 52, "UNJUDGED": 5},
        "window": {"total": 120, "USEFUL": 64, "NOT_USEFUL": 50, "UNJUDGED": 6},
        "overlap": {"total": 90, "USEFUL": 52, "NOT_USEFUL": 34, "UNJUDGED": 4},
        "whole_only": {"total": 30, "USEFUL": 11, "NOT_USEFUL": 18, "UNJUDGED": 1},
        "window_only": {"total": 30, "USEFUL": 12, "NOT_USEFUL": 16, "UNJUDGED": 2},
    }
    for label in ("USEFUL", "NOT_USEFUL", "UNJUDGED"):
        assert (
            payload["surfaces"]["whole"][label]
            == payload["surfaces"]["overlap"][label]
            + payload["surfaces"]["whole_only"][label]
        )
        assert (
            payload["surfaces"]["window"][label]
            == payload["surfaces"]["overlap"][label]
            + payload["surfaces"]["window_only"][label]
        )
        assert (
            payload["union"][label]
            == payload["surfaces"]["overlap"][label]
            + payload["surfaces"]["whole_only"][label]
            + payload["surfaces"]["window_only"][label]
        )


def test_per_case_coverage_and_lexical_reachability() -> None:
    """The small shallow gain is reordering, without new positive reachability."""
    payload = build_results(ROOT)["payload"]
    cases = payload["per_case"]
    assert len(cases) == len({row["case_id"] for row in cases}) == 24
    assert sum(row["surfaces"]["whole"]["USEFUL"] for row in cases) == 63
    assert sum(row["surfaces"]["window"]["USEFUL"] for row in cases) == 64
    assert sum(row["case_useful_coverage"]["whole"] for row in cases) == 19
    assert sum(row["case_useful_coverage"]["window"] for row in cases) == 20
    assert [
        row["case_id"]
        for row in cases
        if row["case_useful_coverage"]["window"]
        and not row["case_useful_coverage"]["whole"]
    ] == ["i25-739c82bd3398"]
    assert not [
        row
        for row in cases
        if row["case_useful_coverage"]["whole"]
        and not row["case_useful_coverage"]["window"]
    ]
    reachability = payload["reachability"]
    assert reachability["window_only_no_positive_whole_rank"] == 0
    assert reachability["useful_window_only_no_positive_whole_rank"] == 0
    assert len(reachability["useful_window_only_whole_positive_ranks"]) == 12
    assert all(
        6 <= rank <= 23 for rank in reachability["all_window_only_whole_positive_ranks"]
    )


def test_exact_150_pair_join_rejects_missing_reused_label() -> None:
    """The join rejects an incomplete or altered source label set."""
    sources = load_verified_sources(ROOT)
    rows = join_frozen_labels(sources)
    assert len(rows) == len({(row["case_id"], row["address"]) for row in rows}) == 150
    assert sum(row["judgment_provenance"] == "REUSED" for row in rows) == 138
    assert sum(row["judgment_provenance"] == "NEW" for row in rows) == 12
    modified = copy.deepcopy(sources)
    modified["pool"]["reused"].pop()
    with pytest.raises(ValueError, match="exact 150-pair pool"):
        join_frozen_labels(modified)
