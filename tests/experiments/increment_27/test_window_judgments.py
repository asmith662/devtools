# Copyright (c) 2026
"""Exact frozen blind judgment checkpoint for the window-unit ablation."""

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
from experiments.increment_27.window_judgments import (
    BLINDED_IDENTITY,
    BLINDED_SHA256,
    EXPECTED_COUNT,
    FREEZE_IDENTITY,
    LABELS,
    build_frozen_judgments,
    validate_blinded_input,
    validate_frozen_judgments,
)
from experiments.increment_27.window_unit import _digest

ROOT = Path(__file__).resolve().parents[3] / "experiments" / "increment_27"
BLIND = ROOT / "window_unit_blinded_judgment_input.json"
FROZEN = ROOT / "window_unit_frozen_judgments.json"


def test_exact_twelve_pair_frozen_binding_and_three_states() -> None:
    """All and only the twelve neutral pairs receive a purpose-relative state."""
    blind = validate_blinded_input(BLIND)
    artifact = cast("dict[str, Any]", _read_json(FROZEN))
    validate_frozen_judgments(blind, artifact)
    rows = artifact["payload"]["judgments"]
    expected = {
        (case["neutral_case_id"], resource["neutral_resource_id"], resource["address"])
        for case in blind["cases"]
        for resource in case["resources"]
    }
    actual = {(row["case_id"], row["resource_id"], row["address"]) for row in rows}
    assert len(rows) == len(actual) == len(expected) == EXPECTED_COUNT
    assert actual == expected
    assert {row["judgment"] for row in rows} == LABELS
    assert {
        label: sum(row["judgment"] == label for row in rows) for label in LABELS
    } == {"USEFUL": 3, "NOT_USEFUL": 8, "UNJUDGED": 1}
    assert all(row["rationale"].strip() for row in rows)


def test_deterministic_serialization_and_source_identities() -> None:
    """The persisted artifact reproduces from the exact committed blind input."""
    first = build_frozen_judgments(BLIND)
    second = build_frozen_judgments(BLIND)
    persisted = cast("dict[str, Any]", _read_json(FROZEN))
    assert first == second == persisted
    assert FROZEN.read_bytes() == canonical_json_bytes(first)
    assert sha256_file(BLIND) == BLINDED_SHA256
    assert first["content_identity"] == _digest(first["payload"])
    assert first["payload"]["window_freeze_identity"] == FREEZE_IDENTITY
    assert first["payload"]["blinded_input_identity"] == BLINDED_IDENTITY
    assert first["payload"]["blinded_input_sha256"] == BLINDED_SHA256


def test_origin_fields_and_duplicate_or_missing_targets_are_rejected() -> None:
    """The frozen outcome cannot carry origin metadata or lose a neutral pair."""
    blind = validate_blinded_input(BLIND)
    original = cast("dict[str, Any]", _read_json(FROZEN))
    for field in ("method", "rank", "score", "window_identity", "origin"):
        modified = copy.deepcopy(original)
        modified["payload"]["judgments"][0][field] = "hidden"
        modified["content_identity"] = _digest(modified["payload"])
        with pytest.raises(ValueError, match="origin field"):
            validate_frozen_judgments(blind, modified)
    missing = copy.deepcopy(original)
    missing["payload"]["judgments"].pop()
    missing["content_identity"] = _digest(missing["payload"])
    with pytest.raises(ValueError, match="count changed"):
        validate_frozen_judgments(blind, missing)
    duplicate = copy.deepcopy(original)
    duplicate["payload"]["judgments"][1] = duplicate["payload"]["judgments"][0]
    duplicate["content_identity"] = _digest(duplicate["payload"])
    with pytest.raises(ValueError, match="once"):
        validate_frozen_judgments(blind, duplicate)


def test_changed_blinded_input_cannot_be_adjudicated(tmp_path: Path) -> None:
    """A changed purpose or an added origin field breaks the committed file hash."""
    blind = cast("dict[str, Any]", _read_json(BLIND))
    blind["cases"][0]["information_need"]["purpose"] = "changed"
    altered = tmp_path / "blind.json"
    altered.write_bytes(canonical_json_bytes(blind))
    with pytest.raises(ValueError, match="hash changed"):
        validate_blinded_input(altered)
