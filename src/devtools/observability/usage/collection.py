# Copyright (c) 2026
"""Reconcile turn aggregates and response observations without double counting."""

from __future__ import annotations

from dataclasses import dataclass, replace
from itertools import groupby, pairwise

from devtools.models.interaction.usage import ModelUsage
from devtools.observability.evidence.invocation import ExecutionOrigin
from devtools.observability.usage.models import Attribution, Purpose, UsageObservation

TOKEN_FIELDS = (
    "input_tokens",
    "cached_input_tokens",
    "cache_write_tokens",
    "output_tokens",
    "reasoning_tokens",
)


def sum_usage(values: tuple[ModelUsage, ...]) -> ModelUsage:
    """Sum each disjoint observation category; any missing value remains unknown."""
    fields = {}
    for name in TOKEN_FIELDS:
        numbers = [getattr(value, name) for value in values]
        fields[name] = sum(numbers) if all(n is not None for n in numbers) else None
    return ModelUsage(**fields)


def incompatible(left: ModelUsage, right: ModelUsage) -> bool:
    """Unknown values do not contradict known values; unequal reports do."""
    return any(
        getattr(left, k) is not None
        and getattr(right, k) is not None
        and getattr(left, k) != getattr(right, k)
        for k in TOKEN_FIELDS
    )


@dataclass(frozen=True, slots=True)
class ReconciledInvocation:
    """One identity component, with conflicts excluded from numerical totals."""

    identity: str
    observations: tuple[UsageObservation, ...]
    consumption: tuple[UsageObservation, ...]
    attribution: Attribution
    conflict: bool


def reconcile(  # noqa: C901, PLR0912, PLR0915 -- one identity-component reconciliation decision tree
    observations: tuple[UsageObservation, ...],
) -> tuple[ReconciledInvocation, ...]:
    """Match backend identities, original invocations and immutable receipt copies.

    A missing turn ID can match a thread only if that thread has one known turn.
    Ambiguous multi-turn aliases are conflicts, never convenient extra charges.
    Local cumulative snapshots may advance; ordinary completed receipts may not.
    """
    threads: dict[str, set[str]] = {}
    aliases: dict[str, set[str]] = {}
    for row in observations:
        if row.thread_id and row.turn_id:
            threads.setdefault(row.thread_id, set()).add(row.turn_id)
        if row.invocation_id and row.thread_id:
            aliases.setdefault(row.invocation_id, set()).add(row.thread_id)

    def key(row: UsageObservation) -> str:
        thread = row.thread_id
        if thread is None and row.invocation_id in aliases:
            thread = min(aliases[row.invocation_id])
        turn = row.turn_id
        if turn is None and thread in threads and len(threads[thread]) == 1:
            turn = next(iter(threads[thread]))
        identity = (
            f"thread:{thread}/turn:{turn}"
            if thread
            else (
                "invocation:" + row.invocation_id
                if row.invocation_id
                else "response:" + str(row.response_id)
            )
        )
        return row.backend + "/" + row.provider + "/" + identity

    result = []
    for identity, rows in groupby(sorted(observations, key=key), key=key):
        group = tuple(rows)
        conflict = any(
            (
                r.thread_id in threads
                and r.turn_id is None
                and len(threads[r.thread_id]) > 1
            )
            or (r.invocation_id in aliases and len(aliases[r.invocation_id]) > 1)
            for r in group
        )
        responses: dict[str, UsageObservation] = {}
        totals = []
        snapshots = []
        for row in group:
            if row.granularity == "RESPONSE":
                response_key = row.response_id or row.source_digest
                prior = responses.get(response_key)
                conflict |= prior is not None and incompatible(prior.usage, row.usage)
                conflict |= (
                    prior is not None
                    and prior.model != "UNKNOWN"
                    and row.model not in ("UNKNOWN", prior.model)
                )
                responses[response_key] = row
            elif row.source == "LOCAL_CODEX_TURN_SUMMARY":
                snapshots.append(row)
            else:
                totals.append(row)
        snapshots.sort(key=lambda r: str(r.timestamp))
        if snapshots:
            conflict |= any(
                getattr(old.usage, field) is not None
                and getattr(new.usage, field) is not None
                and getattr(old.usage, field) > getattr(new.usage, field)
                for old, new in pairwise(snapshots)
                for field in TOKEN_FIELDS
            )
            totals.append(snapshots[-1])
        if responses:
            observed = tuple(responses.values())
            summed = sum_usage(tuple(r.usage for r in observed))
            conflict |= any(incompatible(summed, r.usage) for r in totals)
        else:
            # Prefer the most complete report; conflicting known reports fail closed.
            totals.sort(
                key=lambda r: (
                    sum(getattr(r.usage, k) is not None for k in TOKEN_FIELDS),
                    r.timestamp is not None,
                    r.execution_origin == ExecutionOrigin.EXECUTED,
                ),
                reverse=True,
            )
            chosen = totals[0]
            conflict |= any(incompatible(chosen.usage, r.usage) for r in totals)
            if chosen.execution_origin == ExecutionOrigin.ADOPTED:
                chosen = replace(chosen, timestamp=chosen.original_timestamp)
            observed = (chosen,)
        attrs = [
            r.attribution
            if r.execution_origin == ExecutionOrigin.EXECUTED
            else r.original_attribution or Attribution()
            for r in group
        ]
        # Attribution refinements are not new consumption. Conflicting named scopes
        # are visible and excluded, rather than assigned to the convenient project.
        dimensions = []
        for name in ("project", "purpose", "experiment", "case", "stage"):
            named = {getattr(a, name) for a in attrs if getattr(a, name) != "UNKNOWN"}
            conflict |= len(named) > 1
            dimensions.append(min(named) if named else "UNKNOWN")
        attr = Attribution(dimensions[0], Purpose(dimensions[1]), *dimensions[2:])
        result.append(ReconciledInvocation(identity, group, observed, attr, conflict))
    return tuple(result)
