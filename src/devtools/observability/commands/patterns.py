# Copyright (c) 2026
"""Deterministic diagnostic candidates; repetition never grants execution trust."""

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from devtools.observability.commands.models import (
        CommandObservation,
        CommandOrigin,
        CommandPattern,
    )


@dataclass(frozen=True, slots=True)
class PatternCandidate:
    """Summarize unique observations and unordered same-run co-occurrence only."""

    pattern: CommandPattern
    frequency: int
    distinct_tasks: int
    distinct_agents: int
    succeeded: int
    failed: int
    cancelled: int
    unknown: int
    conflicting: int
    co_occurring_operations: tuple[str, ...]
    co_occurrence_truncated: bool = False


def summarize_patterns(
    observations: tuple[CommandObservation, ...],
    *,
    maximum_observations: int = 4096,
    maximum_related_operations: int = 32,
) -> tuple[PatternCandidate, ...]:
    """Deduplicate stable origin keys; refuse contradictory independent records.

    CLI-specific partial/conflicting-event reconciliation precedes this function.
    Co-occurrence is not execution ordering, effectiveness, safety or a recipe.
    The caller controls retention; there is no store or automatic promotion.
    """
    if (
        min(maximum_observations, maximum_related_operations) < 1
        or len(observations) > maximum_observations
    ):
        msg = "Command analysis observation bound exceeded."
        raise ValueError(msg)
    unique: dict[CommandOrigin, CommandObservation] = {}
    for item in observations:
        if item.origin in unique and unique[item.origin] != item:
            msg = "Conflicting command observations share an origin."
            raise ValueError(msg)
        unique[item.origin] = item
    groups: dict[CommandPattern, list[CommandObservation]] = {}
    for item in unique.values():
        groups.setdefault(item.pattern, []).append(item)
    result = []
    for pattern, items in groups.items():
        runs = {(x.origin.agent, x.origin.task, x.origin.run) for x in items}
        co_occurring = {
            x.pattern.family + ":" + x.pattern.operation
            for x in unique.values()
            if (x.origin.agent, x.origin.task, x.origin.run) in runs
            and x.pattern != pattern
        }
        result.append(
            PatternCandidate(
                pattern,
                len(items),
                len({x.origin.task for x in items}),
                len({x.origin.agent for x in items}),
                sum(x.outcome == "succeeded" for x in items),
                sum(x.outcome == "failed" for x in items),
                sum(x.outcome == "cancelled" for x in items),
                sum(x.outcome == "unknown" for x in items),
                sum(x.outcome == "conflict" for x in items),
                tuple(sorted(co_occurring)[:maximum_related_operations]),
                len(co_occurring) > maximum_related_operations,
            ),
        )
    return tuple(
        sorted(
            result,
            key=lambda x: (
                x.pattern.family,
                x.pattern.operation,
                x.pattern.argument_roles,
                x.pattern.capabilities,
                x.pattern.equivalent_tool or "",
            ),
        ),
    )
