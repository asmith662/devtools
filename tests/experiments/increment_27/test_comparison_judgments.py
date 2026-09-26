# Copyright (c) 2026
# ruff: noqa: D103, PLR2004
"""Frozen neutral judgment coverage and source binding."""

from __future__ import annotations

import hashlib
from pathlib import Path
from typing import Any, cast

import pytest

from experiments.increment_27.comparison_judgments import (
    INPUT_IDENTITY,
    INPUT_NAME,
    INPUT_SHA256,
    OUTPUT_NAME,
    SEMANTICS,
    build_judgments,
)
from experiments.increment_27.depth_diagnostic import (
    _digest,
    _read_json,
    canonical_json_bytes,
)

ROOT = Path("experiments/increment_27")


def test_frozen_judgments_cover_exactly_the_neutral_input() -> None:
    source = cast("dict[str, Any]", _read_json(ROOT / INPUT_NAME))
    saved = cast("dict[str, Any]", _read_json(ROOT / OUTPUT_NAME))
    assert hashlib.sha256((ROOT / INPUT_NAME).read_bytes()).hexdigest() == INPUT_SHA256
    assert source["content_identity"] == INPUT_IDENTITY == _digest(source["payload"])
    assert saved == build_judgments(ROOT)
    assert (ROOT / OUTPUT_NAME).read_bytes() == canonical_json_bytes(saved)
    assert saved["content_identity"] == _digest(saved["payload"])
    payload = saved["payload"]
    assert payload["blinded_input_content_identity"] == INPUT_IDENTITY
    assert payload["blinded_input_sha256"] == INPUT_SHA256
    assert payload["usefulness_semantics"] == SEMANTICS
    assert payload["target_count"] == 140
    assert sum(payload["state_counts"].values()) == 140
    assert set(payload["state_counts"]) == {"USEFUL", "NOT_USEFUL", "UNJUDGED"}
    assert set(payload) == {
        "schema",
        "blinded_input_content_identity",
        "blinded_input_sha256",
        "usefulness_semantics",
        "three_states",
        "target_count",
        "state_counts",
        "records",
    }
    expected = {
        (
            case["neutral_case_id"],
            case["information_need"]["purpose"],
            case["information_need"]["lexical_query"],
            case["parent_snapshot_sha"],
            resource["neutral_resource_id"],
            resource["address"],
        )
        for case in source["payload"]["cases"]
        for resource in case["resources"]
    }
    actual = {
        (
            row["neutral_case_id"],
            row["information_need"]["purpose"],
            row["information_need"]["lexical_query"],
            row["parent_snapshot_sha"],
            row["neutral_resource_id"],
            row["address"],
        )
        for row in payload["records"]
    }
    assert len(expected) == len(actual) == len(payload["records"]) == 140
    assert actual == expected
    assert all(
        set(row)
        == {
            "neutral_case_id",
            "information_need",
            "parent_snapshot_sha",
            "neutral_resource_id",
            "address",
            "usefulness_semantics",
            "judgment",
            "rationale",
        }
        and row["usefulness_semantics"] == SEMANTICS
        and row["judgment"] in payload["three_states"]
        and bool(row["rationale"].strip())
        for row in payload["records"]
    )


def test_changed_neutral_input_is_rejected_before_judgment(tmp_path: Path) -> None:
    raw = (ROOT / INPUT_NAME).read_bytes()
    (tmp_path / INPUT_NAME).write_bytes(raw + b" ")
    with pytest.raises(ValueError, match="byte identity"):
        build_judgments(tmp_path)
