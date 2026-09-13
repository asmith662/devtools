# Copyright (c) 2026
"""Immutable terminal Evidence for interaction-attempt lifecycle facts."""

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

from devtools.core.identity import Identity
from devtools.core.time import Timestamp

if TYPE_CHECKING:
    from devtools.execution.interaction_attempt import (
        InteractionAttemptId,
        InteractionAttemptOutcome,
    )


@dataclass(frozen=True, slots=True)
class EvidenceId:
    """Identify one immutable Evidence record."""

    value: Identity

    @classmethod
    def new(cls) -> EvidenceId:
        """Generate an Evidence identity."""
        return cls(Identity.new())

    @classmethod
    def parse(cls, value: str) -> EvidenceId:
        """Parse UUID text as an Evidence identity."""
        return cls(Identity.parse(value))

    def __str__(self) -> str:
        """Return canonical UUID text."""
        return str(self.value)


@dataclass(frozen=True, slots=True, kw_only=True)
class InteractionAttemptTerminalEvidence:
    """Record one immutable observation of a terminal interaction attempt."""

    id: EvidenceId
    attempt_id: InteractionAttemptId
    occurred_at: Timestamp
    observed_at: Timestamp
    outcome: InteractionAttemptOutcome

    @classmethod
    def new(
        cls,
        *,
        attempt_id: InteractionAttemptId,
        occurred_at: Timestamp,
        outcome: InteractionAttemptOutcome,
    ) -> InteractionAttemptTerminalEvidence:
        """Create a terminal record with a fresh observation identity."""
        return cls(
            id=EvidenceId.new(),
            attempt_id=attempt_id,
            occurred_at=occurred_at,
            observed_at=Timestamp.now(),
            outcome=outcome,
        )
