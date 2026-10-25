# Copyright (c) 2026
"""Reconcile turn aggregates and response observations without double counting."""

from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass, replace
from itertools import groupby, pairwise
from typing import cast

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
        for k in (*TOKEN_FIELDS, "total_tokens")
    )


@dataclass(frozen=True, slots=True)
class ReconciledInvocation:
    """One identity component, with conflicts excluded from numerical totals."""

    identity: str
    observations: tuple[UsageObservation, ...]
    consumption: tuple[UsageObservation, ...]
    attribution: Attribution
    conflict: bool


def _merge_copies(
    rows: tuple[UsageObservation, ...],
) -> tuple[UsageObservation, bool]:
    """Project compatible facts about one measurement, retaining original rows.

    Selection of representative metadata is deterministic, never an authority
    rule for conflicting counts. A derived usage value identifies all contributing
    metadata, rather than pretending one original source reported the union.
    """
    chosen = min(
        rows,
        key=lambda r: (
            -sum(getattr(r.usage, k) is not None for k in TOKEN_FIELDS),
            r.timestamp is None,
            r.execution_origin != ExecutionOrigin.EXECUTED,
            json.dumps(r.to_dict(), sort_keys=True),
        ),
    )
    fields = {}
    conflict = False
    # A supplied provider total is preserved, never inferred or added to categories.
    for field in (*TOKEN_FIELDS, "total_tokens"):
        known = {getattr(r.usage, field) for r in rows} - {None}
        conflict |= len(known) > 1
        fields[field] = next(iter(known)) if len(known) == 1 else None
    usage = ModelUsage(**fields)
    if all(r.usage == usage for r in rows):
        return chosen, conflict
    sources = sorted({json.dumps(r.to_dict(), sort_keys=True) for r in rows})
    return replace(
        chosen,
        usage=usage,
        source="RECONCILED_USAGE",
        source_digest=hashlib.sha256(json.dumps(sources).encode()).hexdigest(),
    ), conflict


def reconcile(  # noqa: C901, PLR0912, PLR0915 -- one identity-component reconciliation decision tree
    observations: tuple[UsageObservation, ...],
) -> tuple[ReconciledInvocation, ...]:
    """Match backend identities, original invocations and immutable receipt copies.

    A missing turn ID can match a thread only if that thread has one known turn.
    Ambiguous multi-turn aliases are conflicts, never convenient extra charges.
    Local cumulative snapshots may advance; ordinary completed receipts may not.
    """
    threads: dict[tuple[str, str, str], set[str]] = {}
    aliases: dict[tuple[str, str, str], set[str]] = {}
    for row in observations:
        if row.thread_id and row.turn_id:
            threads.setdefault((row.backend, row.provider, row.thread_id), set()).add(
                row.turn_id,
            )
        if row.invocation_id and row.thread_id:
            aliases.setdefault(
                (row.backend, row.provider, row.invocation_id),
                set(),
            ).add(row.thread_id)

    def key(row: UsageObservation) -> str:
        thread = row.thread_id
        alias = aliases.get((row.backend, row.provider, row.invocation_id or ""), set())
        if thread is None and alias:
            thread = min(alias)
        turn = row.turn_id
        turns = threads.get((row.backend, row.provider, thread or ""), set())
        if turn is None and len(turns) == 1:
            turn = next(iter(turns))
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
                r.turn_id is None
                and len(threads.get((r.backend, r.provider, r.thread_id or ""), set()))
                > 1
            )
            or len(aliases.get((r.backend, r.provider, r.invocation_id or ""), set()))
            > 1
            for r in group
        )
        responses: dict[str, list[UsageObservation]] = {}
        totals = []
        snapshots = []
        for row in group:
            if row.granularity == "RESPONSE":
                response_key = row.response_id or row.source_digest
                responses.setdefault(response_key, []).append(row)
            elif row.source == "LOCAL_CODEX_TURN_SUMMARY":
                snapshots.append(row)
            else:
                totals.append(row)
        snapshots.sort(key=lambda r: str(r.timestamp))
        if snapshots:
            epochs = []
            for _, copies in groupby(snapshots, key=lambda r: r.timestamp):
                merged, bad = _merge_copies(tuple(copies))
                conflict |= bad
                epochs.append(merged)
            # Explicit cumulative updates may advance. Unknown intermediate
            # fields do not hide a decrease between known observations.
            for field in (*TOKEN_FIELDS, "total_tokens"):
                numbers = [
                    getattr(r.usage, field)
                    for r in epochs
                    if getattr(r.usage, field) is not None
                ]
                conflict |= any(old > new for old, new in pairwise(numbers))
            # Missing time establishes no ordering authority for different counts.
            conflict |= any(
                incompatible(unknown.usage, known.usage)
                for unknown in epochs
                if unknown.timestamp is None
                for known in epochs
            )
            totals.append(epochs[-1])
        total, total_conflict = (
            _merge_copies(tuple(totals)) if totals else (None, False)
        )
        conflict |= total_conflict
        if responses:
            combined = []
            for response_key in sorted(responses):
                response_copies = tuple(responses[response_key])
                merged, bad = _merge_copies(response_copies)
                conflict |= (
                    bad
                    or len({r.model for r in response_copies if r.model != "UNKNOWN"})
                    > 1
                )
                combined.append(merged)
            observed = tuple(combined)
            summed = sum_usage(tuple(r.usage for r in observed))
            conflict |= total is not None and incompatible(summed, total.usage)
        else:
            # A nonempty component without RESPONSE necessarily contains TURN.
            chosen = cast("UsageObservation", total)
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
