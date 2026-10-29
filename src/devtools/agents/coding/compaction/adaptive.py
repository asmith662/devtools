# Copyright (c) 2026
"""Conservative host policy for preserving valuable omitted working information."""

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from collections.abc import Callable

    from devtools.agents.coding.projection import ProjectionOutcome
    from devtools.models.interaction import PromptMessage


@dataclass(frozen=True, slots=True)
class AdaptiveCompaction:
    """Explicit pressure, value and reserve; never infer importance from model text.

    ``valuable`` identifies original records whose omission loses useful working
    information. It does not authorize disclosure or replacement. SummarySelection
    remains the separate authority. Reserve includes projected note overhead and
    is a conservative preflight, not a substitute for final request measurement.
    """

    pressure_bytes: int
    reserve_bytes: int
    valuable: Callable[[tuple[PromptMessage, ...]], frozenset[int]]

    def __post_init__(self) -> None:
        """Require explicit finite positive thresholds, without universal defaults."""
        if any(
            type(v) is not int or v <= 0
            for v in (self.pressure_bytes, self.reserve_bytes)
        ):
            msg = "Adaptive thresholds must be positive integers."
            raise ValueError(msg)

    def assess(
        self,
        messages: tuple[PromptMessage, ...],
        projection: ProjectionOutcome,
    ) -> str:
        """Select only affordable omission with explicit host value and headroom."""
        if projection.status == "insufficient":
            return "protected-context-unaffordable"
        if projection.original_bytes < self.pressure_bytes:
            return "no-pressure"
        if projection.resulting_bytes + self.reserve_bytes > projection.hard_bytes:
            return "insufficient-headroom"
        selected = self.valuable(messages)
        if not isinstance(selected, frozenset) or any(
            type(i) is not int or not 0 <= i < len(messages) for i in selected
        ):
            msg = "Adaptive value selection contains invalid original indices."
            raise ValueError(msg)
        omitted = {
            i
            for first, end, _reason in projection.omitted_exchanges
            for i in range(first, end)
        }
        if not selected.intersection(omitted):
            return "deterministic-sufficient"
        return "semantic-requested"
