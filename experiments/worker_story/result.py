# Copyright (c) 2026
"""Experimental worker-story evaluation result."""

from dataclasses import dataclass
from typing import Literal

from devtools.core.time import Duration, Timestamp

SupervisorReviewOutcome = Literal[
    "accepted",
    "correction_requested",
    "rejected",
    "escalated",
]
_OUTCOMES = frozenset(("accepted", "correction_requested", "rejected", "escalated"))


@dataclass(frozen=True, slots=True)
class WorkerStoryResult:
    """Record acceptance data for one completed experimental worker story."""

    story_name: str
    difficulty: int
    started_at: Timestamp
    duration: Duration
    gates_passed: bool
    review_outcome: SupervisorReviewOutcome
    local_repair_attempts: int
    supervisor_correction_turns: int
    supervisor_prompt_tokens: int | None
    supervisor_completion_tokens: int | None
    escalated: bool
    escalation_reason: str | None
    architecture_violation_count: int
    human_intervention: bool

    def __post_init__(self) -> None:  # noqa: C901
        """Validate bounded worker-story evaluation data."""
        if not self.story_name.strip():
            msg = "Story name cannot be empty."
            raise ValueError(msg)
        if (
            isinstance(self.difficulty, bool)
            or not isinstance(self.difficulty, int)
            or self.difficulty not in {1, 2, 3, 4, 5}
        ):
            msg = "Story difficulty must be an integer from 1 through 5."
            raise ValueError(msg)
        if self.review_outcome not in _OUTCOMES:
            msg = "Supervisor review outcome is invalid."
            raise ValueError(msg)
        for value, label in (
            (self.local_repair_attempts, "Local repair attempts"),
            (self.supervisor_correction_turns, "Supervisor correction turns"),
            (self.architecture_violation_count, "Architecture violation count"),
        ):
            if isinstance(value, bool) or not isinstance(value, int):
                msg = f"{label} must be an integer."
                raise TypeError(msg)
            if value < 0:
                msg = f"{label} cannot be negative."
                raise ValueError(msg)
        for optional_value, label in (
            (self.supervisor_prompt_tokens, "Supervisor prompt tokens"),
            (self.supervisor_completion_tokens, "Supervisor completion tokens"),
        ):
            if optional_value is not None and (
                isinstance(optional_value, bool) or not isinstance(optional_value, int)
            ):
                msg = f"{label} must be an integer."
                raise TypeError(msg)
            if optional_value is not None and optional_value < 0:
                msg = f"{label} cannot be negative."
                raise ValueError(msg)
        if self.escalation_reason is not None and not self.escalation_reason.strip():
            msg = "Escalation reason cannot be blank when supplied."
            raise ValueError(msg)
