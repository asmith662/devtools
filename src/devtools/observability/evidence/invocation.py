# Copyright (c) 2026
"""Typed invocation measurements, separate from execution and acceptance authority."""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import StrEnum
from math import isfinite
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from devtools.models.interaction.usage import ModelUsage


class Availability(StrEnum):
    """Describe the provenance of an optional measurement."""

    REPORTED = "REPORTED"
    DERIVED = "DERIVED"
    ESTIMATED = "ESTIMATED"
    UNKNOWN = "UNKNOWN"
    NOT_APPLICABLE = "NOT_APPLICABLE"


@dataclass(frozen=True, slots=True)
class Measured[T]:
    """Keep an invocation field's value, availability and provenance together."""

    value: T | None
    availability: Availability
    provenance: str

    def __post_init__(self) -> None:
        """Never substitute zero for absence or lose the source of a number."""
        missing = self.availability in {
            Availability.UNKNOWN,
            Availability.NOT_APPLICABLE,
        }
        if (self.value is None) != missing or not self.provenance.strip():
            message = "Measurement availability/value/provenance mismatch"
            raise ValueError(message)


class ExecutionOrigin(StrEnum):
    """Distinguish a new execution from provenance-preserving branch adoption."""

    EXECUTED = "EXECUTED"
    ADOPTED = "ADOPTED"


@dataclass(frozen=True, slots=True, kw_only=True)
class InvocationMeasurement:
    """One invocation's observations; no costs or hidden request counts inferred.

    Token provenance applies independently to each optional ModelUsage field:
    a supplied count is REPORTED; an absent count is UNKNOWN. Raw provider JSON
    remains separate, and no total is derived from overlapping categories.
    """

    backend: str
    provider: str
    execution_profile: str
    requested_model: str
    reported_model: Measured[str]
    reasoning_effort: str
    task_id: str
    invocation_id: str
    backend_thread_id: Measured[str]
    backend_turn_id: Measured[str]
    disclosed_chars: Measured[int]
    disclosed_bytes: Measured[int]
    disclosure_digest: str
    usage: ModelUsage
    usage_provenance: str
    raw_provider_usage_json: str
    model_turns: Measured[int]
    observed_tool_calls: Measured[int]
    subprocesses: Measured[int]
    wall_seconds: Measured[float]
    model_seconds: Measured[float]
    completed: bool
    validated: bool
    accepted: bool
    failure_class: str | None
    execution_origin: ExecutionOrigin
    response_chars: Measured[int] = field(
        default_factory=lambda: Measured(
            None,
            Availability.UNKNOWN,
            "Response not captured",
        ),
    )
    response_bytes: Measured[int] = field(
        default_factory=lambda: Measured(
            None,
            Availability.UNKNOWN,
            "Response not captured",
        ),
    )

    def __post_init__(self) -> None:
        """Keep identities and durations honest without granting authority."""
        if not self.invocation_id.strip() or not self.usage_provenance.strip():
            message = "Invocation identity and usage provenance required"
            raise ValueError(message)
        for observation in (self.wall_seconds, self.model_seconds):
            if observation.value is not None and (
                not isfinite(observation.value) or observation.value < 0
            ):
                message = "Invocation duration must be finite and nonnegative"
                raise ValueError(message)
        if self.accepted and not (self.completed and self.validated):
            message = "Accepted invocation must be completed and validated"
            raise ValueError(message)

    def token_availability(self, name: str) -> Availability:
        """Report each optional token category without deriving missing counts."""
        return (
            Availability.UNKNOWN
            if getattr(self.usage, name) is None
            else Availability.REPORTED
        )
