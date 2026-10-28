# Copyright (c) 2026
"""Coding-specific budgets, progress and terminal facts; never a generic Run."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import TYPE_CHECKING, Literal

if TYPE_CHECKING:
    from devtools.core.time import Duration
    from devtools.models.interaction import ModelUsage

type CodingDisposition = Literal[
    "validated",
    "stopped",
    "model_limit",
    "proposal_limit",
    "failed",
    "cancelled",
    "reconciliation_required",
]


class CodingLimitError(ValueError):
    """A host-fixed coding budget refuses further dispatch."""


@dataclass(frozen=True, slots=True)
class CodingLimits:
    """Finite host ceilings, without provider capacity or application defaults."""

    model_calls: int
    proposals: int
    tool_actions: int
    call_timeout: Duration
    wall_timeout: Duration
    completion_check: bool = False

    def __post_init__(self) -> None:
        """Refuse invalid ceilings before any model or effect entry."""
        if (
            min(self.model_calls, self.proposals) < 1
            or self.tool_actions < 0
            or min(self.call_timeout.total_seconds, self.wall_timeout.total_seconds)
            <= 0
        ):
            msg = (
                "Coding limits require positive calls/proposals/time "
                "and nonnegative actions."
            )
            raise ValueError(msg)


@dataclass(slots=True)
class CodingEffect:
    """A dispatch attempt and its acknowledgment, not proof of rollback or entry."""

    kind: Literal["tool", "edit", "check"]
    native_call_ids: tuple[str | None, ...]
    acknowledged: bool = False
    check_name: str | None = None


@dataclass(slots=True)
class CodingProgress:
    """One invocation's coding counters and known facts, shared with its host."""

    limits: CodingLimits
    number: int = 0
    model_calls: int = 0
    proposals: int = 0
    actions: int = 0
    phase: str = "preparation"
    candidate_validated: bool = False
    effects: list[CodingEffect] = field(default_factory=list)
    usage: list[ModelUsage | None] = field(default_factory=list)

    def claim_action(self, call_id: str | None) -> CodingEffect:
        """Charge before dispatch; failure never silently refunds an attempt."""
        if self.actions >= self.limits.tool_actions:
            msg = "Context action budget exhausted"
            raise CodingLimitError(msg)
        self.actions += 1
        effect = CodingEffect("tool", (call_id,))
        self.effects.append(effect)
        return effect


@dataclass(frozen=True, slots=True)
class CodingCompletion:
    """Host custody facts; absence makes no assertion about restoration."""

    restored: bool | None = None
    reconciliation_required: bool = False
    error: BaseException | None = None


@dataclass(frozen=True, slots=True)
class CodingResult:
    """Candidate evidence is independent of terminal coding execution success."""

    disposition: CodingDisposition
    candidate_validated: bool
    completed: bool
    progress: CodingProgress
    error: BaseException | None = None
    completion_error: BaseException | None = None
    custody: CodingCompletion = CodingCompletion()
    failure_phase: str | None = None

    @property
    def accepted(self) -> bool:
        """Refuse unconditional success after fatal completion/custody failure."""
        return (
            self.disposition == "validated"
            and self.candidate_validated
            and self.completed
            and not self.custody.reconciliation_required
            and self.custody.restored is not False
        )
