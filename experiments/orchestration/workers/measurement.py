# Copyright (c) 2026
# ruff: noqa: ANN401, PLR0913, PLR0917 -- explicit invocation measurement inputs
"""Retain measured invocation facts independently of semantic acceptance."""

from __future__ import annotations

import json
from dataclasses import asdict
from typing import Any

from devtools.agents.integrations.codex.errors import CodexOutputError
from devtools.agents.integrations.codex.usage import CodexUsage, capture_codex_usage
from devtools.models.interaction.usage import ModelUsage
from devtools.observability.evidence.invocation import (
    Availability,
    ExecutionOrigin,
    InvocationMeasurement,
    Measured,
)
from experiments.codex_dogfood.case_0009.artifacts import digest


def capture(
    config: Any,
    case: str,
    invocation: str,
    prompt: bytes,
    result: Any,
    response: bytes | None,
    *,
    validated: bool,
    failure: str | None,
    raw_stdout: bytes | None = None,
) -> dict[str, Any]:
    """Report missing data as unknown, including failures before a usage event."""
    records: tuple[CodexUsage, ...] = ()
    usage_error = None
    try:
        stdout = (
            raw_stdout
            if raw_stdout is not None
            else result.stdout
            if result is not None
            else None
        )
        records = capture_codex_usage(stdout) if stdout is not None else ()
    except CodexOutputError as error:
        usage_error = str(error)
    one = records[0] if len(records) == 1 else None
    counts = one.counts if one is not None else ModelUsage()
    duration = getattr(result, "duration", None)
    wall = duration.total_seconds if duration is not None else None

    def observed(value: Any, provenance: str) -> Measured[Any]:
        return Measured(
            value,
            Availability.REPORTED if value is not None else Availability.UNKNOWN,
            provenance,
        )

    def derived(value: Any, provenance: str) -> Measured[Any]:
        return Measured(
            value,
            Availability.DERIVED if value is not None else Availability.UNKNOWN,
            provenance,
        )

    measurement = InvocationMeasurement(
        backend="Codex",
        provider="OpenAI",
        execution_profile="SEMANTIC_WORKER",
        requested_model=config["model_id"],
        reported_model=observed(None, "No provider model identity event"),
        reasoning_effort=config["reasoning"],
        task_id=case,
        invocation_id=invocation,
        backend_thread_id=observed(
            one.thread_id if one else None,
            "Codex JSONL thread identity",
        ),
        backend_turn_id=observed(
            one.turn_id if one else None,
            "Codex JSONL turn identity",
        ),
        disclosed_chars=derived(len(prompt.decode()), "Exact UTF-8 stdin disclosure"),
        disclosed_bytes=derived(len(prompt), "Exact UTF-8 stdin disclosure"),
        disclosure_digest=digest(prompt),
        usage=counts,
        usage_provenance="Codex turn.completed aggregates; request boundaries unknown",
        raw_provider_usage_json=json.dumps(
            [json.loads(record.raw_json) for record in records],
            sort_keys=True,
        ),
        model_turns=derived(
            len(records) if records else None,
            "Observed completed-turn events; absence unknown",
        ),
        observed_tool_calls=derived(
            0 if validated else None,
            "Validated tool-free transport or unavailable",
        ),
        subprocesses=derived(None, "No aggregate descendant-process count exposed"),
        wall_seconds=derived(wall, "Managed process monotonic duration"),
        model_seconds=observed(None, "No authoritative model-only duration"),
        completed=bool(records),
        validated=validated,
        accepted=False,
        failure_class=failure,
        execution_origin=ExecutionOrigin.EXECUTED,
        response_chars=derived(
            len(response.decode()) if response is not None else None,
            "Canonical semantic response",
        ),
        response_bytes=derived(
            len(response) if response is not None else None,
            "Canonical semantic response",
        ),
    )
    return {
        "schema": "semantic-invocation-measurement-v1",
        "measurement": asdict(measurement),
        "usage_error": usage_error,
    }
