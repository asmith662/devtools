# Copyright (c) 2026
"""Deterministic partial-coverage reports of observed consumption, not quota."""

from __future__ import annotations

from typing import TYPE_CHECKING, NotRequired, TypedDict

from devtools.observability.evidence.invocation import ExecutionOrigin
from devtools.observability.usage.collection import TOKEN_FIELDS, reconcile

if TYPE_CHECKING:
    from devtools.observability.usage.models import UsageObservation
    from devtools.observability.usage.windows import UsageWindow


class UsageGroup(TypedDict):
    """One named report dimension with five separate provider categories."""

    dimension: str
    value: str
    fresh_invocations: int
    adopted_dependencies: int
    tokens: dict[str, int]
    unknown: dict[str, int]
    observed_input_percent: NotRequired[float | None]
    observed_fresh_call_percent: NotRequired[float | None]


class UsageReport(TypedDict):
    """Versioned machine report, explicitly partial and non-authoritative."""

    schema: str
    coverage: str
    window: dict[str, str]
    fresh_invocations: int
    adopted_dependencies: int
    accepted: int
    rejected: int
    failed: int
    outcome_unknown: int
    missing_usage_invocations: int
    tokens: dict[str, int]
    unknown_category_observations: dict[str, int]
    conflicting_invocations_excluded: int
    unallocated_timestamp_observations: int
    sources: list[str]
    groups: list[UsageGroup]
    notes: list[str]


def report(  # noqa: C901, PLR0912 -- one pass over disjoint reconciled components
    observations: tuple[UsageObservation, ...],
    window: UsageWindow,
    *,
    experiment: str | None = None,
) -> UsageReport:
    """Report known sums plus per-category unknown counts and distinct fresh turns.

    Responses are timestamped independently when available. A turn aggregate
    alone is allocated to its reported timestamp; this limitation is explicit.
    No personal history becomes an account-wide total or subscription estimate.
    """
    components = reconcile(observations)
    groups: dict[str, UsageGroup] = {}
    tokens = dict.fromkeys(TOKEN_FIELDS, 0)
    unknown = dict.fromkeys(TOKEN_FIELDS, 0)
    fresh = adopted = accepted = rejected = failed = conflicts = missing = (
        unallocated
    ) = 0
    sources: set[str] = set()
    for component in components:
        attr = component.attribution
        consumed = tuple(
            r
            for r in component.consumption
            if window.contains(r.timestamp)
            and (experiment is None or attr.experiment == experiment)
        )
        uses = tuple(
            r
            for r in component.observations
            if r.execution_origin == ExecutionOrigin.ADOPTED
            and window.contains(r.timestamp)
            and (experiment is None or r.attribution.experiment == experiment)
        )
        unallocated += sum(r.timestamp is None for r in component.consumption)
        adopted += bool(uses)
        for dependency in {r.attribution.experiment for r in uses}:
            name = "experiment:" + dependency
            group = groups.setdefault(
                name,
                {
                    "dimension": "experiment",
                    "value": dependency,
                    "fresh_invocations": 0,
                    "adopted_dependencies": 0,
                    "tokens": dict.fromkeys(TOKEN_FIELDS, 0),
                    "unknown": dict.fromkeys(TOKEN_FIELDS, 0),
                },
            )
            group["adopted_dependencies"] += 1
        sources.update(r.source for r in component.observations)
        if not consumed:
            continue
        if component.conflict:
            conflicts += 1
            continue
        fresh += 1
        known_accepted = any(r.accepted is True for r in component.observations)
        known_failure = any(r.failure_class is not None for r in component.observations)
        accepted += known_accepted
        failed += not known_accepted and known_failure
        rejected += (
            not known_accepted
            and not known_failure
            and any(
                r.completed is True and (r.validated is False or r.accepted is False)
                for r in component.observations
            )
        )
        missing += any(
            getattr(r.usage, k) is None for r in consumed for k in TOKEN_FIELDS
        )
        dimensions = {
            "model": next(
                (r.model for r in component.observations if r.model != "UNKNOWN"),
                "UNKNOWN",
            ),
            "reasoning": next(
                (
                    r.reasoning_effort
                    for r in component.observations
                    if r.reasoning_effort != "UNKNOWN"
                ),
                "UNKNOWN",
            ),
            "purpose": attr.purpose,
            "project": attr.project,
            "experiment": attr.experiment,
        }
        # A long agentic turn may legitimately change model or effort. Its fresh
        # invocation is still one turn; mixed attribution must remain visible.
        for dimension, field in (("model", "model"), ("reasoning", "reasoning_effort")):
            labels = {
                getattr(r, field).casefold()
                for r in component.observations
                if getattr(r, field) != "UNKNOWN"
            }
            if len(labels) > 1:
                dimensions[dimension] = "MIXED"
        for dimension, label in dimensions.items():
            name = dimension + ":" + label
            group = groups.setdefault(
                name,
                {
                    "dimension": dimension,
                    "value": label,
                    "fresh_invocations": 0,
                    "adopted_dependencies": 0,
                    "tokens": dict.fromkeys(TOKEN_FIELDS, 0),
                    "unknown": dict.fromkeys(TOKEN_FIELDS, 0),
                },
            )
            group["fresh_invocations"] += 1
        for row in consumed:
            for k in TOKEN_FIELDS:
                value = getattr(row.usage, k)
                if value is None:
                    unknown[k] += 1
                else:
                    tokens[k] += value
                for dimension, label in dimensions.items():
                    group = groups[dimension + ":" + label]
                    counts = group["unknown" if value is None else "tokens"]
                    counts[k] += 1 if value is None else value
    for group in groups.values():
        if group["dimension"] == "experiment":
            amounts = group["tokens"]
            group["observed_input_percent"] = (
                100 * amounts["input_tokens"] / tokens["input_tokens"]
                if tokens["input_tokens"]
                else None
            )
            group["observed_fresh_call_percent"] = (
                100 * group["fresh_invocations"] / fresh if fresh else None
            )
    return {
        "schema": "observed-usage-report-v1",
        "coverage": "PARTIAL / OBSERVED_LOCAL_AND_DEVTOOLS / NOT_ACCOUNT_WIDE",
        "window": {
            "start": str(window.start),
            "end": str(window.end),
            "timezone": window.timezone,
            "interval": "[start,end)",
        },
        "fresh_invocations": fresh,
        "adopted_dependencies": adopted,
        "accepted": accepted,
        "rejected": rejected,
        "failed": failed,
        "outcome_unknown": fresh - accepted - rejected - failed,
        "missing_usage_invocations": missing,
        "tokens": tokens,
        "unknown_category_observations": unknown,
        "conflicting_invocations_excluded": conflicts,
        "unallocated_timestamp_observations": unallocated,
        "sources": sorted(sources),
        "groups": [groups[k] for k in sorted(groups)],
        "notes": [
            "Token categories overlap; no summed total",
            "Unknown is not zero",
            "Aggregate-only consumption is allocated to its observed timestamp",
            "No subscription-quota or dollar inference",
        ],
    }
