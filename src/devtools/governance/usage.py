# Copyright (c) 2026
"""Narrow numeric usage constraints; passing never grants execution authority."""

from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum


class BudgetScope(StrEnum):
    """Name the explicitly observed population covered by a numeric constraint."""

    OBSERVED_WINDOW = "OBSERVED_WINDOW"
    PROJECT = "PROJECT"
    EXPERIMENT = "EXPERIMENT"
    STAGE = "STAGE"


@dataclass(frozen=True, slots=True)
class UsageAmount:
    """Separate fresh calls and non-overlapping-with-it token dimensions."""

    fresh_calls: int | None
    input_tokens: int | None
    output_tokens: int | None

    def __post_init__(self) -> None:
        """Unknown is allowed; negative allowances or measurements are not."""
        if any(
            v is not None and (type(v) is not int or v < 0)
            for v in (self.fresh_calls, self.input_tokens, self.output_tokens)
        ):
            message = "Usage budget quantities must be nonnegative or UNKNOWN"
            raise ValueError(message)


@dataclass(frozen=True, slots=True)
class UsageBudget:
    """UNSET dimensions impose no numeric limit; no universal default is chosen."""

    scope: BudgetScope
    identity: str
    limits: UsageAmount
    model: str | None = None

    def check(
        self,
        consumed: UsageAmount,
        reserved: UsageAmount,
        proposed: UsageAmount,
    ) -> BudgetDecision:
        """Compare reported/forecast bounds before launch, including reservations."""
        blocked = []
        for name in ("fresh_calls", "input_tokens", "output_tokens"):
            limit = getattr(self.limits, name)
            if limit is None:
                continue
            values = [getattr(v, name) for v in (consumed, reserved, proposed)]
            if any(v is None for v in values):
                blocked.append(name + ":UNKNOWN")
            elif sum(values) > limit:
                blocked.append(name + ":EXCEEDED")
        return BudgetDecision(not blocked, tuple(blocked))


@dataclass(frozen=True, slots=True)
class BudgetDecision:
    """Constraint result only: even PASS does not authorize a model or science."""

    allowed: bool
    reasons: tuple[str, ...]

    @property
    def status(self) -> str:
        """Expose the mandatory no-launch failure category."""
        return "BUDGET_CHECK_PASS" if self.allowed else "BUDGET_BLOCKED"
