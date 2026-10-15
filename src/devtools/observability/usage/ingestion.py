# Copyright (c) 2026

"""Metadata-only projections from existing measurements and local Codex usage."""

from __future__ import annotations

from dataclasses import replace
from typing import TYPE_CHECKING, Any

from devtools.agents.integrations.codex.sessions import read_session_usage
from devtools.models.interaction.usage import ModelUsage
from devtools.observability.evidence.invocation import (
    Availability,
    ExecutionOrigin,
    InvocationMeasurement,
    Measured,
)
from devtools.observability.usage.models import (
    UNATTRIBUTED,
    Attribution,
    UsageObservation,
)

if TYPE_CHECKING:
    from pathlib import Path

    from devtools.core.time import Timestamp

_MEASURED = (
    "reported_model",
    "backend_thread_id",
    "backend_turn_id",
    "disclosed_chars",
    "disclosed_bytes",
    "model_turns",
    "observed_tool_calls",
    "subprocesses",
    "wall_seconds",
    "model_seconds",
    "response_chars",
    "response_bytes",
)


def measurement(capture: dict[str, Any]) -> InvocationMeasurement:
    """Restore the existing closed normalized measurement representation."""
    fields = dict(capture["measurement"])
    fields["usage"] = ModelUsage(**fields["usage"])
    for name in _MEASURED:
        if name in fields:
            field = fields[name]
            fields[name] = Measured(
                field["value"],
                Availability(field["availability"]),
                field["provenance"],
            )
    fields["execution_origin"] = ExecutionOrigin(fields["execution_origin"])
    return InvocationMeasurement(**fields)


def from_capture(  # noqa: PLR0913 -- explicit observation provenance
    capture: dict[str, Any],
    *,
    timestamp: Timestamp | None,
    source: str,
    source_digest: str,
    attribution: Attribution = UNATTRIBUTED,
    original_timestamp: Timestamp | None = None,
) -> UsageObservation:
    """Reuse InvocationMeasurement; retain no payload or free-text error message."""
    measured = measurement(capture)
    projected = UsageObservation.from_invocation(
        measured,
        timestamp=timestamp,
        source=source,
        source_digest=source_digest,
        attribution=attribution,
        original_timestamp=original_timestamp,
    )
    # A process-level accepted=False precedes scientific adjudication; it is not
    # evidence of scientific rejection. Domain acceptance is explicitly named.
    return replace(
        projected,
        accepted=measured.accepted if "acceptance_domain" in capture else None,
        failure_class="RECORDED_INVOCATION_FAILURE" if measured.failure_class else None,
    )


def from_session(path: Path) -> tuple[UsageObservation, ...]:
    """Retain disjoint response records plus the latest authoritative turn sum."""
    rows = read_session_usage(path)
    observations = []
    last = {}
    for row in rows:
        observed = UsageObservation(
            timestamp=row.timestamp,
            backend="Codex",
            provider="OpenAI",
            model=row.requested_model,
            reasoning_effort=row.reasoning_effort,
            execution_profile="UNKNOWN",
            invocation_id=None,
            thread_id=row.thread_id,
            turn_id=row.turn_id,
            response_id=row.response_id,
            usage=row.usage,
            source="LOCAL_CODEX_RESPONSE",
            source_digest=row.metadata_digest,
            attribution=Attribution(project=row.project),
            granularity="RESPONSE",
            completed=row.completed,
        )
        observations.append(observed)
        last[row.thread_id, row.turn_id] = replace(
            observed,
            granularity="TURN",
            response_id=None,
            usage=row.turn_usage,
            source="LOCAL_CODEX_TURN_SUMMARY",
            source_digest=row.metadata_digest + ":turn",
        )
    return (*observations, *last.values())
