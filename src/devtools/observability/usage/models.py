# Copyright (c) 2026
"""Metadata-only observations of already normalized invocation usage."""

from __future__ import annotations

from dataclasses import asdict, dataclass
from enum import StrEnum
from typing import TYPE_CHECKING, Any

from devtools.core.time import Timestamp
from devtools.models.interaction.usage import ModelUsage
from devtools.observability.evidence.invocation import ExecutionOrigin

if TYPE_CHECKING:
    from devtools.observability.evidence.invocation import InvocationMeasurement


class Purpose(StrEnum):
    """Attribute observed work without guessing from prompt contents."""

    SCIENCE = "SCIENCE"
    EXPERIMENT_ENGINEERING = "EXPERIMENT_ENGINEERING"
    CODING = "CODING"
    REVIEW = "REVIEW"
    BENCHMARK = "BENCHMARK"
    RESEARCH = "RESEARCH"
    UNKNOWN = "UNKNOWN"


@dataclass(frozen=True, slots=True)
class Attribution:
    """Caller-supplied dimensions, independent of consumption identity."""

    project: str = "UNKNOWN"
    purpose: Purpose = Purpose.UNKNOWN
    experiment: str = "UNKNOWN"
    case: str = "UNKNOWN"
    stage: str = "UNKNOWN"


UNATTRIBUTED = Attribution()


@dataclass(frozen=True, slots=True, kw_only=True)
class UsageObservation:
    """One usage representation or adopted reference, never payload content.

    RESPONSE records are timestamped provider response observations. TURN records
    are whole-turn aggregates. They must be reconciled, never added together.
    ADOPTED timestamps describe use; original_timestamp describes consumption.
    None means UNKNOWN, including outcome and time. No total is manufactured.
    """

    timestamp: Timestamp | None
    backend: str
    provider: str
    model: str
    reasoning_effort: str
    execution_profile: str
    invocation_id: str | None
    thread_id: str | None
    turn_id: str | None
    response_id: str | None
    usage: ModelUsage
    source: str
    source_digest: str
    attribution: Attribution = Attribution()
    granularity: str = "TURN"
    execution_origin: ExecutionOrigin = ExecutionOrigin.EXECUTED
    original_timestamp: Timestamp | None = None
    completed: bool | None = None
    validated: bool | None = None
    accepted: bool | None = None
    failure_class: str | None = None
    original_attribution: Attribution | None = None
    reported_model: str | None = None

    def __post_init__(self) -> None:
        """Require auditable identity and supported measurement granularity."""
        if not self.source_digest or not (
            self.invocation_id or self.thread_id or self.response_id
        ):
            message = "Usage requires source provenance and an observed identity"
            raise ValueError(message)
        if self.granularity not in {"TURN", "RESPONSE"}:
            message = "Unsupported usage granularity"
            raise ValueError(message)

    @classmethod
    def from_invocation(  # noqa: PLR0913 -- explicit observation provenance
        cls,
        value: InvocationMeasurement,
        *,
        timestamp: Timestamp | None,
        source: str,
        source_digest: str,
        attribution: Attribution = UNATTRIBUTED,
        original_timestamp: Timestamp | None = None,
    ) -> UsageObservation:
        """Project the existing typed measurement without retaining its payload."""
        return cls(
            timestamp=timestamp,
            backend=value.backend,
            provider=value.provider,
            model=value.requested_model,
            reasoning_effort=value.reasoning_effort,
            execution_profile=value.execution_profile,
            invocation_id=value.invocation_id,
            thread_id=value.backend_thread_id.value,
            turn_id=value.backend_turn_id.value,
            response_id=None,
            usage=value.usage,
            source=source,
            source_digest=source_digest,
            attribution=attribution,
            execution_origin=value.execution_origin,
            original_timestamp=original_timestamp,
            completed=value.completed,
            validated=value.validated,
            accepted=value.accepted,
            failure_class=value.failure_class,
            reported_model=value.reported_model.value,
        )

    def to_dict(self) -> dict[str, object]:
        """Serialize the version-one operational representation, with UTC times."""
        value = asdict(self)
        value["timestamp"] = str(self.timestamp) if self.timestamp else None
        value["original_timestamp"] = (
            str(self.original_timestamp) if self.original_timestamp else None
        )
        return value

    @classmethod
    def from_dict(cls, value: dict[str, object]) -> UsageObservation:
        """Restore only named usage metadata; reject arbitrary payload fields."""
        fields = set(cls.__dataclass_fields__)
        if set(value) != fields:
            message = "Usage observation fields differ"
            raise ValueError(message)
        copied: dict[str, Any] = dict(value)
        for name in ("timestamp", "original_timestamp"):
            copied[name] = (
                Timestamp.from_isoformat(str(value[name])) if value[name] else None
            )
        usage = value["usage"]
        attr = value["attribution"]
        if not isinstance(usage, dict) or not isinstance(attr, dict):
            message = "Typed usage and attribution required"
            raise TypeError(message)
        copied["usage"] = ModelUsage(**usage)
        attr = {**attr, "purpose": Purpose(attr["purpose"])}
        copied["attribution"] = Attribution(**attr)
        if isinstance(value["original_attribution"], dict):
            original = value["original_attribution"]
            copied["original_attribution"] = Attribution(
                **{**original, "purpose": Purpose(original["purpose"])},
            )
        copied["execution_origin"] = ExecutionOrigin(str(value["execution_origin"]))
        return cls(**copied)
