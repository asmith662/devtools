# Copyright (c) 2026
# ruff: noqa: ANN401, D103
"""Exact pair-identity and judgment coverage checks for retrieval experiments."""

from __future__ import annotations

from typing import Any

import pytest

from experiments.retrieval_judgment_coverage import (
    judgment_identity,
    validate_frozen_judgment_coverage,
    validate_neutral_target_coverage,
    validated_outcome_mappings,
)

STATES = ("USEFUL", "NOT_USEFUL", "UNJUDGED")


def _record(**overrides: Any) -> dict[str, Any]:
    record = {
        "neutral_case_id": "case-1",
        "neutral_resource_id": "resource-1",
        "information_need": {"purpose": "purpose", "lexical_query": "query"},
        "parent_snapshot_sha": "snapshot",
        "address": "src/module.py",
        "usefulness_semantics": "purpose-relative-three-state-v1",
        "judgment": "USEFUL",
        "rationale": "Contains the behavior needed for the task.",
    }
    record.update(overrides)
    return record


def _validate(
    targets: list[dict[str, Any]],
    decisions: list[dict[str, Any]],
) -> dict[tuple[str, str, str, str, str], Any]:
    return validate_frozen_judgment_coverage(targets, decisions, STATES)


def test_exact_valid_coverage_returns_three_state_outcomes() -> None:
    target = _record()
    useful = _record()
    unknown = _record(
        neutral_resource_id="resource-2",
        address="src/other.py",
        judgment="UNJUDGED",
        rationale="Insufficient exposed evidence to decide.",
    )
    outcomes = _validate([target, unknown], [useful, unknown])
    assert outcomes[judgment_identity(target)]["judgment"] == "USEFUL"
    assert outcomes[judgment_identity(unknown)]["judgment"] == "UNJUDGED"


@pytest.mark.parametrize(
    ("field", "update"),
    [
        (
            "purpose",
            {"information_need": {"purpose": "other", "lexical_query": "query"}},
        ),
        (
            "query",
            {"information_need": {"purpose": "purpose", "lexical_query": "other"}},
        ),
        ("snapshot", {"parent_snapshot_sha": "other"}),
        ("address", {"address": "src/other.py"}),
        ("semantics", {"usefulness_semantics": "other-semantics"}),
    ],
)
def test_each_identity_component_must_match(field: str, update: dict[str, Any]) -> None:
    del field
    with pytest.raises(ValueError, match="exact neutral target"):
        _validate([_record()], [_record(**update)])


def test_duplicate_neutral_targets_are_rejected() -> None:
    with pytest.raises(ValueError, match="targets contain duplicates"):
        validate_neutral_target_coverage([_record(), _record()])


def test_neutral_targets_must_match_expected_unresolved_set() -> None:
    target = _record()
    extra = _record(neutral_resource_id="resource-extra", address="extra.py")
    expected = [("case-1", "resource-1")]
    assert set(validate_neutral_target_coverage([target], expected)) == set(expected)
    with pytest.raises(ValueError, match="expected unresolved pairs"):
        validate_neutral_target_coverage([target, extra], expected)
    with pytest.raises(ValueError, match="expected unresolved pairs"):
        validate_neutral_target_coverage([], expected)


def test_duplicate_frozen_decisions_are_rejected() -> None:
    with pytest.raises(ValueError, match="exact neutral target"):
        _validate([_record()], [_record(), _record()])


def test_missing_and_extra_decisions_are_rejected() -> None:
    with pytest.raises(ValueError, match="coverage is incomplete"):
        _validate([_record()], [])
    extra = _record(neutral_resource_id="resource-extra", address="extra.py")
    with pytest.raises(ValueError, match="exact neutral target"):
        _validate([_record()], [_record(), extra])


def test_invalid_state_and_empty_rationale_are_rejected() -> None:
    with pytest.raises(ValueError, match="exact neutral target"):
        _validate([_record()], [_record(judgment="MAYBE")])
    with pytest.raises(ValueError, match="exact neutral target"):
        _validate([_record()], [_record(rationale="  ")])


def test_reuse_new_overlap_and_duplicate_reuse_are_rejected() -> None:
    identity = judgment_identity(_record())
    with pytest.raises(ValueError, match="overlap"):
        validated_outcome_mappings(
            [_record(judgment="NOT_USEFUL")],
            {identity: _record()},
        )
    with pytest.raises(ValueError, match="duplicate identities"):
        validated_outcome_mappings([_record(), _record()], {})


def test_unjudged_is_a_frozen_outcome_not_missing_coverage() -> None:
    target = _record(judgment="UNJUDGED", rationale="Evidence is insufficient.")
    assert (
        _validate([target], [target])[judgment_identity(target)]["judgment"]
        == "UNJUDGED"
    )
    with pytest.raises(ValueError, match="coverage is incomplete"):
        _validate([target], [])
