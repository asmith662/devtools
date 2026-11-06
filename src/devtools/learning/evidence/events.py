# Copyright (c) 2026
"""Immutable empirical observations, independent of storage and ML backends."""

from __future__ import annotations

import math
from dataclasses import dataclass
from datetime import datetime, timedelta
from enum import StrEnum
from uuid import UUID

type Scalar = str | int | float | bool | None


def _text(value: str, name: str) -> None:
    if not isinstance(value, str) or not value.strip():
        msg = f"{name} must be a nonempty string"
        raise ValueError(msg)


def _count(value: int, name: str) -> None:
    if type(value) is not int or value < 0:
        msg = f"{name} must be a nonnegative integer"
        raise ValueError(msg)


@dataclass(frozen=True, slots=True)
class Fact:
    """A named safe scalar fact; never an arbitrary runtime object."""

    name: str
    value: Scalar

    def __post_init__(self) -> None:
        """Validate the immutable scientific contract and its correspondence."""
        _text(self.name, "fact name")
        if self.value is not None and type(self.value) not in (str, int, float, bool):
            msg = "fact values must be JSON scalars"
            raise TypeError(msg)
        if isinstance(self.value, float) and (not math.isfinite(self.value)):
            msg = "fact values must be finite"
            raise ValueError(msg)


def _facts(values: tuple[Fact, ...]) -> None:
    if not isinstance(values, tuple) or any(not isinstance(v, Fact) for v in values):
        msg = "facts must be an immutable tuple of Fact"
        raise TypeError(msg)
    if len({v.name for v in values}) != len(values):
        msg = "fact names must be unique"
        raise ValueError(msg)


class Lifecycle(StrEnum):
    """Activity projection; outcome is a separate fact."""

    PENDING = "pending"
    RUNNING = "running"
    STOPPED = "stopped"


class Outcome(StrEnum):
    """Observed termination reason, not a recovery policy."""

    COMPLETED = "completed"
    FAILED = "failed"
    INTERRUPTED = "interrupted"
    CANCELLED = "cancelled"


class FailureCategory(StrEnum):
    """Categories exercised at actual managed boundaries."""

    INPUT = "input"
    COMPATIBILITY = "compatibility"
    CONFIGURATION = "configuration"
    ENVIRONMENT = "environment"
    BACKEND = "backend"
    NUMERICAL = "numerical"
    INVALID_RESULT = "invalid_result"
    RECORDING = "recording"
    PUBLICATION = "publication"
    INTERRUPTION = "interruption"
    OBSERVER = "optional_observer"
    PROCESS = "process_termination"
    TIMEOUT = "timeout"
    RESOURCE = "resource_exhaustion"


class Severity(StrEnum):
    """Retain the declared Severity scientific values and invariants."""

    WARNING = "warning"
    ERROR = "error"


@dataclass(frozen=True, slots=True)
class Admitted:
    """Retain the declared Admitted scientific values and invariants."""

    operation: str
    facts: tuple[Fact, ...] = ()

    def __post_init__(self) -> None:
        """Validate the immutable scientific contract and its correspondence."""
        _text(self.operation, "operation")
        _facts(self.facts)


@dataclass(frozen=True, slots=True)
class Activated:
    """Retain the declared Activated scientific values and invariants."""

    process_id: int
    hostname: str
    python_version: str
    platform: str

    def __post_init__(self) -> None:
        """Validate the immutable scientific contract and its correspondence."""
        _count(self.process_id, "process_id")
        if self.process_id == 0:
            msg = "process_id must be positive"
            raise ValueError(msg)
        for v in (self.hostname, self.python_version, self.platform):
            _text(v, "environment")


@dataclass(frozen=True, slots=True)
class StageStarted:
    """Retain the declared StageStarted scientific values and invariants."""

    stage: str
    description: str
    facts: tuple[Fact, ...] = ()

    def __post_init__(self) -> None:
        """Validate the immutable scientific contract and its correspondence."""
        _text(self.stage, "stage")
        _text(self.description, "description")
        _facts(self.facts)


@dataclass(frozen=True, slots=True)
class StageFinished:
    """Retain the declared StageFinished scientific values and invariants."""

    stage: str
    duration_seconds: float

    def __post_init__(self) -> None:
        """Validate the immutable scientific contract and its correspondence."""
        _text(self.stage, "stage")
        if type(self.duration_seconds) not in (int, float) or (
            not math.isfinite(self.duration_seconds) or self.duration_seconds < 0
        ):
            msg = "stage duration must be finite and nonnegative"
            raise ValueError(msg)


@dataclass(frozen=True, slots=True)
class Progress:
    """Unknown completed/total counts represent indeterminate work."""

    stage: str
    unit: str
    completed: int | None = None
    total: int | None = None

    def __post_init__(self) -> None:
        """Validate the immutable scientific contract and its correspondence."""
        _text(self.stage, "stage")
        _text(self.unit, "unit")
        for v in (self.completed, self.total):
            if v is not None:
                _count(v, "work count")
        if self.total is not None and (
            self.completed is None or self.completed > self.total
        ):
            msg = "known total requires completed <= total"
            raise ValueError(msg)


@dataclass(frozen=True, slots=True)
class ExceptionFact:
    """One bounded exception-chain member, preserving relation and type."""

    type_name: str
    message: str
    relation: str

    def __post_init__(self) -> None:
        """Validate the immutable scientific contract and its correspondence."""
        _text(self.type_name, "exception type")
        if not isinstance(self.message, str):
            msg = "exception message must be text"
            raise TypeError(msg)
        if self.relation not in ("primary", "cause", "context"):
            msg = "invalid exception relation"
            raise ValueError(msg)


@dataclass(frozen=True, slots=True)
class Diagnostic:
    """Facts/classification do not establish a cause or authorize recovery."""

    category: FailureCategory
    severity: Severity
    symptom: str
    stage: str | None = None
    exception_chain: tuple[ExceptionFact, ...] = ()
    traceback_text: str | None = None
    truncated: bool = False
    root_cause: None = None

    def __post_init__(self) -> None:
        """Validate the immutable scientific contract and its correspondence."""
        if not isinstance(self.category, FailureCategory):
            msg = "diagnostic category must use FailureCategory"
            raise TypeError(msg)
        if not isinstance(self.severity, Severity):
            msg = "diagnostic severity must use Severity"
            raise TypeError(msg)
        _text(self.symptom, "symptom")
        if self.stage is not None:
            _text(self.stage, "stage")
        if not isinstance(self.exception_chain, tuple) or any(
            not isinstance(v, ExceptionFact) for v in self.exception_chain
        ):
            msg = "exception chain must be immutable ExceptionFact values"
            raise TypeError(msg)
        if self.traceback_text is not None and (
            not isinstance(self.traceback_text, str)
        ):
            msg = "traceback must be text"
            raise TypeError(msg)
        if type(self.truncated) is not bool or self.root_cause is not None:
            msg = "root cause is unknown; truncated must be boolean"
            raise ValueError(msg)


@dataclass(frozen=True, slots=True)
class Terminal:
    """Outcome and small output facts; neither state serialization nor publication."""

    outcome: Outcome
    facts: tuple[Fact, ...] = ()

    def __post_init__(self) -> None:
        """Validate the immutable scientific contract and its correspondence."""
        if not isinstance(self.outcome, Outcome):
            msg = "outcome must use Outcome"
            raise TypeError(msg)
        _facts(self.facts)


type Payload = (
    Admitted
    | Activated
    | StageStarted
    | StageFinished
    | Progress
    | Diagnostic
    | Terminal
)


@dataclass(frozen=True, slots=True, kw_only=True)
class ExecutionEvent:
    """One producer observation; observed_at is assigned by its recorder."""

    event_id: UUID
    execution_id: UUID
    activation_id: UUID
    producer: str
    sequence: int
    occurred_at: datetime
    elapsed_seconds: float
    payload: Payload
    observed_at: datetime | None = None
    parent_execution_id: UUID | None = None
    schema_version: int = 1

    def __post_init__(self) -> None:
        """Validate the immutable scientific contract and its correspondence."""
        for v in (self.event_id, self.execution_id, self.activation_id):
            if not isinstance(v, UUID):
                msg = "event, execution and activation IDs must be UUIDs"
                raise TypeError(msg)
        if self.execution_id == self.activation_id:
            msg = "execution and activation identities must differ"
            raise ValueError(msg)
        if self.parent_execution_id is not None and (
            not isinstance(self.parent_execution_id, UUID)
            or self.parent_execution_id == self.execution_id
        ):
            msg = "parent must be a different execution"
            raise ValueError(msg)
        if type(self.schema_version) is not int or self.schema_version != 1:
            msg = "unsupported event schema version"
            raise ValueError(msg)
        _text(self.producer, "producer")
        _count(self.sequence, "sequence")
        if self.sequence < 1:
            msg = "sequence starts at one"
            raise ValueError(msg)
        for timestamp in (self.occurred_at, self.observed_at):
            if timestamp is not None and (
                not isinstance(timestamp, datetime)
                or timestamp.utcoffset() != timedelta(0)
            ):
                msg = "timestamps must be timezone-aware UTC"
                raise ValueError(msg)
        if self.occurred_at is None:
            msg = "occurrence time is required"
            raise ValueError(msg)
        if type(self.elapsed_seconds) not in (int, float) or (
            not math.isfinite(self.elapsed_seconds) or self.elapsed_seconds < 0
        ):
            msg = "elapsed duration must be finite and nonnegative"
            raise ValueError(msg)
        if not isinstance(
            self.payload,
            Admitted
            | Activated
            | StageStarted
            | StageFinished
            | Progress
            | Diagnostic
            | Terminal,
        ):
            msg = "payload must be a supported typed observation"
            raise TypeError(msg)

    @property
    def kind(self) -> str:
        """A closed wire discriminator derived from the validated payload."""
        return type(self.payload).__name__


@dataclass(frozen=True, slots=True)
class ActivationHistory:
    """Acknowledged process segment, without inferring liveness from a PID."""

    activation_id: UUID
    started_at: datetime | None
    ended_at: datetime | None
    process_id: int | None
    outcome: Outcome | None


@dataclass(frozen=True, slots=True)
class ExecutionHistory:
    """Read-only persisted history. Missing outcome means unknown, never success."""

    execution_id: UUID
    operation: str
    lifecycle: Lifecycle
    outcome: Outcome | None
    activations: tuple[ActivationHistory, ...]
    events: tuple[ExecutionEvent, ...]

    @property
    def parent_execution_id(self) -> UUID | None:
        """Explicit composition lineage, independent of input dependencies."""
        return self.events[0].parent_execution_id

    @property
    def incomplete(self) -> bool:
        """Apply the explicit incomplete contract within this owner."""
        return self.outcome is None
