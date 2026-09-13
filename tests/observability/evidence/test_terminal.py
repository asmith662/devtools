# Copyright (c) 2026
"""Tests for immutable terminal interaction-attempt Evidence."""

from __future__ import annotations

from datetime import UTC, datetime

from devtools.core.time import Timestamp
from devtools.execution import InteractionAttemptId, InteractionAttemptSucceeded
from devtools.observability.evidence import (
    EvidenceId,
    InteractionAttemptTerminalEvidence,
)


def test_terminal_evidence_has_independent_identity_and_observation_time() -> None:
    """Evidence records a fact about execution without owning execution itself."""
    evidence = InteractionAttemptTerminalEvidence.new(
        attempt_id=InteractionAttemptId.parse("00000000-0000-4000-8000-000000000001"),
        occurred_at=Timestamp(datetime(2026, 1, 1, tzinfo=UTC)),
        outcome=InteractionAttemptSucceeded(),
    )
    assert isinstance(evidence.id, EvidenceId)
    assert evidence.observed_at.value >= evidence.occurred_at.value
    assert EvidenceId.parse(str(evidence.id)) == evidence.id
