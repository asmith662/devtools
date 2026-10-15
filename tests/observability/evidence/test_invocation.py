# Copyright (c) 2026
"""Explicit provenance/availability for invocation measurements and adoption."""

from dataclasses import replace

import pytest

from devtools.models.interaction.usage import ModelUsage
from devtools.observability.evidence.invocation import (
    Availability,
    ExecutionOrigin,
    InvocationMeasurement,
    Measured,
)


def measurement() -> InvocationMeasurement:
    """Construct one unknown-usage observation without charging a zero call."""
    return InvocationMeasurement(
        backend="codex",
        provider="openai",
        execution_profile="SEMANTIC_WORKER",
        requested_model="synthetic-model",
        reported_model=Measured(None, Availability.UNKNOWN, "not reported"),
        reasoning_effort="High",
        task_id="synthetic-task",
        invocation_id="original-invocation",
        backend_thread_id=Measured("thread", Availability.REPORTED, "thread.started"),
        backend_turn_id=Measured(None, Availability.UNKNOWN, "not reported"),
        disclosed_chars=Measured(4, Availability.DERIVED, "exact Unicode count"),
        disclosed_bytes=Measured(4, Availability.DERIVED, "exact UTF8 count"),
        disclosure_digest="a" * 64,
        usage=ModelUsage(),
        usage_provenance="retained completion stream",
        raw_provider_usage_json="{}",
        model_turns=Measured(1, Availability.DERIVED, "observed turn.completed"),
        observed_tool_calls=Measured(0, Availability.DERIVED, "completed tool items"),
        subprocesses=Measured(1, Availability.REPORTED, "process receipt"),
        wall_seconds=Measured(2.0, Availability.REPORTED, "exit receipt"),
        model_seconds=Measured(None, Availability.NOT_APPLICABLE, "not exposed"),
        completed=True,
        validated=False,
        accepted=False,
        failure_class="SCIENTIFIC_ARTIFACT_INVALID",
        execution_origin=ExecutionOrigin.EXECUTED,
    )


def test_unknown_and_adopted_measurements_preserve_original_usage() -> None:
    """Adoption changes attribution, never identity, process duration or tokens."""
    original = measurement()
    assert original.token_availability("input_tokens") == Availability.UNKNOWN
    original = replace(original, usage=ModelUsage(input_tokens=10, output_tokens=0))
    adopted = replace(original, execution_origin=ExecutionOrigin.ADOPTED)
    assert adopted.invocation_id == original.invocation_id
    assert adopted.usage == original.usage
    assert adopted.wall_seconds == original.wall_seconds
    assert adopted.token_availability("output_tokens") == Availability.REPORTED
    assert adopted.usage.total_tokens is None


@pytest.mark.parametrize(
    ("value", "status", "source"),
    [
        (None, Availability.REPORTED, "event"),
        (0, Availability.UNKNOWN, "missing"),
        (1, Availability.DERIVED, ""),
    ],
)
def test_availability_must_match_value(
    value: int | None,
    status: Availability,
    source: str,
) -> None:
    """A missing quantity cannot masquerade as reported zero."""
    with pytest.raises(ValueError, match="mismatch"):
        Measured(value, status, source)


@pytest.mark.parametrize("value", [-1.0, float("nan"), float("inf")])
def test_invalid_duration_rejected(value: float) -> None:
    """Duration observations retain physical finite nonnegative values."""
    with pytest.raises(ValueError, match="duration"):
        replace(measurement(), wall_seconds=Measured(value, Availability.REPORTED, "x"))


def test_identity_and_acceptance_require_support() -> None:
    """Acceptance is neither process completion nor an unspecified identity."""
    with pytest.raises(ValueError, match="identity"):
        replace(measurement(), invocation_id="")
    with pytest.raises(ValueError, match="identity"):
        replace(measurement(), usage_provenance="")
    with pytest.raises(ValueError, match="Accepted"):
        replace(measurement(), accepted=True)
    assert replace(measurement(), validated=True, accepted=True).accepted
