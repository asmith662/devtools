# Copyright (c) 2026
# ruff: noqa: E501
"""Tests for process-local Evidence inspection."""

from __future__ import annotations

from datetime import UTC, datetime

from devtools.agents.conversation import ConversationId, MessageId
from devtools.core.time import Timestamp
from devtools.execution import (
    InteractionAttempt,
    InteractionAttemptFailed,
    InteractionAttemptId,
    InteractionAttemptStage,
    InteractionAttemptState,
    InteractionAttemptSucceeded,
)
from devtools.models.interaction import InteractionSource
from devtools.observability.evidence import (
    EvidenceId,
    ExecutionInspector,
    InteractionAttemptTerminalEvidence,
)


class _Sink:
    """Retain forwarded immutable Evidence values."""

    def __init__(self) -> None:
        """Create empty receipt storage."""
        self.values: list[InteractionAttemptTerminalEvidence] = []

    def accept(self, evidence: InteractionAttemptTerminalEvidence) -> None:
        """Record one delivered Evidence value."""
        self.values.append(evidence)


def _attempt() -> InteractionAttempt:
    """Create one deterministic terminal interaction-attempt fact."""
    return InteractionAttempt(
        id=InteractionAttemptId.parse("00000000-0000-4000-8000-000000000001"),
        conversation_id=ConversationId.parse("00000000-0000-4000-8000-000000000002"),
        message_id=MessageId.parse("00000000-0000-4000-8000-000000000003"),
        interaction_source=InteractionSource("model"),
        started_at=Timestamp(datetime(2026, 1, 1, tzinfo=UTC)),
        state=InteractionAttemptState.SUCCEEDED,
        completed_at=Timestamp(datetime(2026, 1, 1, 0, 0, 1, tzinfo=UTC)),
    )


def test_inspector_constructs_and_correlates_evidence_from_execution_facts() -> None:
    """Observability owns immutable Evidence construction after terminal lifecycle facts."""
    inspector = ExecutionInspector()
    attempt = _attempt()
    inspector.attempt_started(attempt)
    inspector.attempt_finished(
        attempt,
        InteractionAttemptSucceeded(),
    )

    assert inspector.attempt_ids() == (attempt.id,)
    records = inspector.get_evidence_for_attempt(attempt.id)
    assert len(records) == 1
    assert records[0].attempt_id == attempt.id
    assert inspector.get_evidence(records[0].id) is records[0]


def test_inspector_retains_first_evidence_identity_and_can_clear() -> None:
    """Inspection is process-local correlation, not execution lifecycle ownership."""
    inspector = ExecutionInspector()
    attempt = _attempt()
    evidence = InteractionAttemptTerminalEvidence.new(
        attempt_id=attempt.id,
        occurred_at=attempt.completed_at or attempt.started_at,
        outcome=InteractionAttemptFailed(
            InteractionAttemptStage.INTERACTION_INVOCATION,
        ),
    )
    conflicting = InteractionAttemptTerminalEvidence(
        id=evidence.id,
        attempt_id=attempt.id,
        occurred_at=evidence.occurred_at,
        observed_at=evidence.observed_at,
        outcome=evidence.outcome,
    )
    inspector.accept(evidence)
    inspector.accept(conflicting)
    assert inspector.get_evidence(evidence.id) is evidence
    inspector.clear()
    assert inspector.attempt_ids() == ()
    assert inspector.get_evidence(EvidenceId.new()) is None
    assert inspector.get_evidence_for_attempt(attempt.id) == ()


def test_inspector_forwards_completed_attempt_evidence_and_ignores_live_attempt() -> (
    None
):
    """Only a terminal execution fact produces Evidence and reaches a configured sink."""
    sink = _Sink()
    inspector = ExecutionInspector(sink)
    attempt = _attempt()
    live = InteractionAttempt(
        id=InteractionAttemptId.new(),
        conversation_id=attempt.conversation_id,
        message_id=attempt.message_id,
        interaction_source=attempt.interaction_source,
        started_at=attempt.started_at,
        state=InteractionAttemptState.RUNNING,
        completed_at=None,
    )
    inspector.attempt_finished(live, InteractionAttemptSucceeded())
    assert sink.values == []
    inspector.attempt_finished(attempt, InteractionAttemptSucceeded())
    assert len(sink.values) == 1
