# Copyright (c) 2026
"""Validation for frozen blinded Increment-27 top-five judgments."""

from __future__ import annotations

import json
from pathlib import Path
from typing import cast

import pytest

from experiments.increment_27.lexical_top5_judgments import (
    ALLOWED_LABELS,
    BLINDED_INPUT_SHA256,
    NEW_POPULATION_IDENTITY,
    TOP5_FREEZE_IDENTITY,
    build_frozen_judgments,
    canonical_json_bytes,
    content_identity,
    validate_blinded_input,
    validate_frozen_judgments,
)

_INCREMENT_27 = Path(__file__).parents[3] / "experiments" / "increment_27"
_INPUT = _INCREMENT_27 / "lexical_top5_blinded_judgment_input.json"
_EXPECTED_TARGET_COUNT = 133
_EXPECTED_UNJUDGED_COUNT = 5


def _input() -> dict[str, object]:
    return cast("dict[str, object]", json.loads(_INPUT.read_text(encoding="utf-8")))


def test_frozen_judgments_bind_exactly_one_record_to_each_target() -> None:
    """All and only the committed neutral targets receive one outcome."""
    blinded = validate_blinded_input(_input())
    artifact = build_frozen_judgments(_INPUT)
    validate_frozen_judgments(blinded, artifact)
    payload = cast("dict[str, object]", artifact["payload"])
    blinded_payload = cast("dict[str, object]", blinded["payload"])
    cases = cast("list[dict[str, object]]", blinded_payload["cases"])
    pairs = {
        (case["neutral_case_id"], resource["address"], resource["neutral_resource_id"])
        for case in cases
        for resource in cast("list[dict[str, object]]", case["resources"])
    }
    records = cast("list[dict[str, str]]", payload["judgments"])
    assert len(pairs) == _EXPECTED_TARGET_COUNT
    assert len(records) == _EXPECTED_TARGET_COUNT
    assert {
        (record["case_id"], record["address"], record["resource_id"])
        for record in records
    } == pairs


def test_judgments_preserve_three_states_and_require_rationales() -> None:
    """Uncertain evidence remains distinct and every decision is explained."""
    artifact = build_frozen_judgments(_INPUT)
    payload = cast("dict[str, object]", artifact["payload"])
    records = cast("list[dict[str, str]]", payload["judgments"])
    assert {record["judgment"] for record in records} == ALLOWED_LABELS
    assert all(record["rationale"].strip() for record in records)
    assert (
        sum(record["judgment"] == "UNJUDGED" for record in records)
        == _EXPECTED_UNJUDGED_COUNT
    )


def test_frozen_identity_is_deterministic_and_binds_input_and_freeze() -> None:
    """Repeated serialization yields the same identity and frozen parents."""
    first = build_frozen_judgments(_INPUT)
    second = build_frozen_judgments(_INPUT)
    assert first == second
    payload = cast("dict[str, object]", first["payload"])
    assert first["content_identity"] == content_identity(payload)
    assert payload["top5_freeze_identity"] == TOP5_FREEZE_IDENTITY
    assert payload["new_blinded_population_identity"] == NEW_POPULATION_IDENTITY
    assert payload["blinded_input_sha256"] == BLINDED_INPUT_SHA256
    assert canonical_json_bytes(first) == canonical_json_bytes(second)


def test_blinded_input_rejects_method_rank_score_and_outcome_fields() -> None:
    """Only the declared neutral input fields are accepted for adjudication."""
    mutated = _input()
    payload = cast("dict[str, object]", mutated["payload"])
    cases = cast("list[dict[str, object]]", payload["cases"])
    cases[0]["rank"] = 1
    with pytest.raises(ValueError, match="unexpected or hidden fields"):
        validate_blinded_input(mutated)


def test_judgment_artifact_rejects_retrieval_origin_fields() -> None:
    """Frozen outcomes cannot acquire method, rank, score, or origin metadata."""
    blinded = _input()
    artifact = build_frozen_judgments(_INPUT)
    payload = cast("dict[str, object]", artifact["payload"])
    rows = cast("list[dict[str, str]]", payload["judgments"])
    rows[0]["method"] = "hidden"
    artifact["content_identity"] = content_identity(payload)
    with pytest.raises(ValueError, match="prohibited or unexpected fields"):
        validate_frozen_judgments(blinded, artifact)


def test_heldout_case_cannot_replace_a_frozen_development_case() -> None:
    """The exact neutral development case set excludes confirmation records."""
    mutated = _input()
    payload = cast("dict[str, object]", mutated["payload"])
    cases = cast("list[dict[str, object]]", payload["cases"])
    cases[0]["neutral_case_id"] = "heldout-confirmation-case"
    with pytest.raises(ValueError, match="development cases differ"):
        validate_blinded_input(mutated)


def test_any_change_to_the_frozen_blinded_input_fails_file_binding(
    tmp_path: Path,
) -> None:
    """Judgments cannot be rebuilt against altered need or parent content."""
    payload = _input()
    payload_body = cast("dict[str, object]", payload["payload"])
    cases = cast("list[dict[str, object]]", payload_body["cases"])
    cases[0]["information_need"] = {"purpose": "changed", "lexical_query": "changed"}
    altered = tmp_path / "input.json"
    altered.write_bytes(canonical_json_bytes(payload) + b"\n")
    with pytest.raises(ValueError, match="file hash changed"):
        build_frozen_judgments(altered)


def test_input_population_identity_cannot_be_replaced() -> None:
    """The committed new-pair population identity is required exactly."""
    mutated = _input()
    mutated["content_identity"] = "0" * 64
    with pytest.raises(ValueError, match="population identity changed"):
        validate_blinded_input(mutated)
