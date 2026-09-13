# Copyright (c) 2026
"""Tests for bounded worker acceptance telemetry values."""

from __future__ import annotations

from dataclasses import FrozenInstanceError

import pytest

from devtools.core.time import Duration, Timestamp
from experiments.worker_story.result import WorkerStoryResult


def _result(**changes: object) -> WorkerStoryResult:
    values: dict[str, object] = {
        "story_name": "add pinned profile",
        "difficulty": 2,
        "started_at": Timestamp.now(),
        "duration": Duration.minutes(3),
        "gates_passed": True,
        "review_outcome": "accepted",
        "local_repair_attempts": 0,
        "supervisor_correction_turns": 0,
        "supervisor_prompt_tokens": None,
        "supervisor_completion_tokens": None,
        "escalated": False,
        "escalation_reason": None,
        "architecture_violation_count": 0,
        "human_intervention": False,
    }
    values.update(changes)
    return WorkerStoryResult(**values)  # type: ignore[arg-type]


def test_worker_story_result_is_immutable_and_allows_unknown_usage() -> None:
    """Supervisor usage is optional because some supervisors do not expose it."""
    result = _result()

    assert hash(result) == hash(result)
    with pytest.raises(FrozenInstanceError):
        result.story_name = "other"  # type: ignore[misc]


@pytest.mark.parametrize("difficulty", [1, 2, 3, 4, 5])
def test_worker_story_result_accepts_bounded_difficulty(difficulty: int) -> None:
    """The initial experimental difficulty scale is deliberately closed."""
    assert _result(difficulty=difficulty).difficulty == difficulty


@pytest.mark.parametrize(
    ("field", "value"),
    [
        ("difficulty", True),
        ("difficulty", False),
        ("local_repair_attempts", True),
        ("local_repair_attempts", False),
        ("supervisor_correction_turns", True),
        ("supervisor_correction_turns", False),
        ("architecture_violation_count", True),
        ("architecture_violation_count", False),
        ("supervisor_prompt_tokens", True),
        ("supervisor_prompt_tokens", False),
        ("supervisor_completion_tokens", True),
        ("supervisor_completion_tokens", False),
    ],
)
def test_worker_story_result_rejects_boolean_integer_values(
    field: str,
    value: object,
) -> None:
    """Boolean values cannot stand in for bounded difficulty or count values."""
    with pytest.raises((TypeError, ValueError)):
        _result(**{field: value})


@pytest.mark.parametrize(
    ("field", "value"),
    [
        ("supervisor_prompt_tokens", 0),
        ("supervisor_prompt_tokens", 123),
        ("supervisor_completion_tokens", 0),
        ("supervisor_completion_tokens", 123),
    ],
)
def test_worker_story_result_accepts_optional_supervisor_token_counts(
    field: str,
    value: int,
) -> None:
    """Known supervisor usage may be zero or a positive integer."""
    assert getattr(_result(**{field: value}), field) == value


@pytest.mark.parametrize(
    ("changes", "match"),
    [
        ({"difficulty": 0}, "difficulty"),
        ({"difficulty": 6}, "difficulty"),
        ({"story_name": " "}, "Story name"),
        ({"review_outcome": "pending"}, "outcome"),
        ({"local_repair_attempts": -1}, "repair"),
        ({"supervisor_correction_turns": -1}, "correction"),
        ({"supervisor_prompt_tokens": -1}, "prompt"),
        ({"supervisor_completion_tokens": -1}, "completion"),
        ({"architecture_violation_count": -1}, "violation"),
        ({"escalation_reason": " "}, "Escalation reason"),
    ],
)
def test_worker_story_result_rejects_invalid_bounded_measurements(
    changes: dict[str, object],
    match: str,
) -> None:
    """Impossible counts and unbounded categorical values fail at the value edge."""
    with pytest.raises(ValueError, match=match):
        _result(**changes)
