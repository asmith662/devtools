# Copyright (c) 2026
"""Immutable terminal observations for application processing attempts."""

from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum
from typing import TYPE_CHECKING

from devtools.identity import Identity
from devtools.time import Timestamp

if TYPE_CHECKING:
    from devtools.evidence.attempt import AttemptId


__all__ = [
    "AttemptCancelled",
    "AttemptFailed",
    "AttemptStage",
    "AttemptSucceeded",
    "AttemptTerminalEvidence",
    "AttemptTerminalOutcome",
    "EvidenceId",
]


@dataclass(frozen=True, slots=True)
class EvidenceId:
    """Represent an immutable semantic identity for one Evidence record."""

    value: Identity

    @classmethod
    def new(cls) -> EvidenceId:
        """Generate a new Evidence identity."""
        return cls(Identity.new())

    @classmethod
    def parse(cls, value: str) -> EvidenceId:
        """Parse an Evidence identity from UUID text."""
        return cls(Identity.parse(value))

    def __str__(self) -> str:
        """Return the canonical Evidence identity representation."""
        return str(self.value)


class AttemptStage(StrEnum):
    """Identify the Runtime boundary where processing stopped or was interrupted."""

    ADMISSION = "admission"
    CONTINUATION_LOOKUP = "continuation_lookup"
    AGENT_INVOCATION = "agent_invocation"
    RESULT_VALIDATION = "result_validation"
    OUTPUT_RETENTION = "output_retention"
    CONTINUATION_REPLACEMENT = "continuation_replacement"


@dataclass(frozen=True, slots=True)
class AttemptSucceeded:
    """Represent a successfully completed Attempt outcome."""


@dataclass(frozen=True, slots=True)
class AttemptFailed:
    """Represent an Attempt failure at one Runtime processing boundary."""

    stage: AttemptStage


@dataclass(frozen=True, slots=True)
class AttemptCancelled:
    """Represent an Attempt cancellation at one Runtime processing boundary."""

    stage: AttemptStage


type AttemptTerminalOutcome = AttemptSucceeded | AttemptFailed | AttemptCancelled


@dataclass(frozen=True, slots=True, kw_only=True)
class AttemptTerminalEvidence:
    """Represent one immutable terminal observation for an Attempt."""

    id: EvidenceId
    attempt_id: AttemptId
    occurred_at: Timestamp
    observed_at: Timestamp
    outcome: AttemptTerminalOutcome

    @classmethod
    def new(
        cls,
        *,
        attempt_id: AttemptId,
        occurred_at: Timestamp,
        outcome: AttemptTerminalOutcome,
    ) -> AttemptTerminalEvidence:
        """Create a terminal record with fresh identity and observation time."""
        return cls(
            id=EvidenceId.new(),
            attempt_id=attempt_id,
            occurred_at=occurred_at,
            observed_at=Timestamp.now(),
            outcome=outcome,
        )
