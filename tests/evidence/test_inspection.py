# Copyright (c) 2026
"""Tests for the experimental in-memory ExecutionInspector."""

from __future__ import annotations

import asyncio
from datetime import UTC, datetime
from typing import TYPE_CHECKING

import pytest

from devtools.context import Message, MessageId, MessageRole, MessageSource, Session
from devtools.evidence import (
    Attempt,
    AttemptCancelled,
    AttemptFailed,
    AttemptId,
    AttemptStage,
    AttemptState,
    AttemptSucceeded,
    AttemptTerminalEvidence,
    EvidenceId,
)
from devtools.evidence.inspection import ExecutionInspector
from devtools.interactions import ConversationRef, InteractionTurn
from devtools.runtime import Runtime
from devtools.time import Timestamp

if TYPE_CHECKING:
    from collections.abc import Sequence


class _FakeInteraction:
    """Return one configured turn or raise one configured primary outcome."""

    def __init__(
        self,
        source: MessageSource,
        turns: Sequence[InteractionTurn] = (),
        *,
        error: BaseException | None = None,
    ) -> None:
        """Create a deterministic Interaction test double."""
        self.source = source
        self._turns = list(turns)
        self._error = error

    async def send(
        self,
        message: Message,
        *,
        conversation: ConversationRef | None = None,
    ) -> InteractionTurn:
        """Return the next configured result after accepting Runtime arguments."""
        del message, conversation
        if self._error is not None:
            raise self._error
        return self._turns.pop(0)


def _message(
    content: str,
    *,
    role: MessageRole = MessageRole.USER,
    source: str = "caller",
) -> Message:
    """Create one message with a deterministic test source."""
    return Message.new(content, role=role, source=MessageSource(source))


def _attempt(*, id: AttemptId | None = None) -> Attempt:  # noqa: A002
    """Create one running Attempt with optional semantic identity reuse."""
    return Attempt(
        id=id or AttemptId.new(),
        session_id=Session.new().id,
        message_id=MessageId.new(),
        interaction_source=MessageSource("agent"),
        started_at=Timestamp.now(),
        state=AttemptState.RUNNING,
        completed_at=None,
    )


def _evidence(
    *,
    id: EvidenceId | None = None,  # noqa: A002
    attempt_id: AttemptId | None = None,
    outcome: AttemptSucceeded | AttemptFailed | AttemptCancelled | None = None,
) -> AttemptTerminalEvidence:
    """Create one deterministic-shape immutable terminal Evidence value."""
    return AttemptTerminalEvidence(
        id=id or EvidenceId.new(),
        attempt_id=attempt_id or AttemptId.new(),
        occurred_at=Timestamp(datetime(2026, 8, 29, tzinfo=UTC)),
        observed_at=Timestamp(datetime(2026, 8, 29, 0, 0, 1, tzinfo=UTC)),
        outcome=outcome or AttemptSucceeded(),
    )


def _capture_attempts(
    monkeypatch: pytest.MonkeyPatch,
) -> list[Attempt]:
    """Capture Attempts created by Runtime without adding a production seam."""
    attempts: list[Attempt] = []
    original_new = Attempt.new

    def capture_new(**kwargs: object) -> Attempt:
        attempt = original_new(**kwargs)  # type: ignore[arg-type]
        attempts.append(attempt)
        return attempt

    monkeypatch.setattr(Attempt, "new", capture_new)
    return attempts


def test_inspector_retains_exact_live_attempt_and_observes_lifecycle() -> None:
    """Attempt lookups intentionally expose the current retained live object."""
    inspector = ExecutionInspector()
    attempt = _attempt()

    inspector.attempt_started(attempt)
    attempt.succeed()

    assert inspector.get_attempt(attempt.id) is attempt
    assert inspector.get_attempt(attempt.id).state is AttemptState.SUCCEEDED  # type: ignore[union-attr]


def test_inspector_finished_registers_or_replaces_attempt_without_start() -> None:
    """Finished callbacks accept standalone and repeated semantic identities."""
    inspector = ExecutionInspector()
    first = _attempt()
    replacement = _attempt(id=first.id)

    inspector.attempt_finished(first)
    inspector.attempt_finished(replacement)

    assert inspector.get_attempt(first.id) is replacement
    assert inspector.attempt_ids() == (first.id,)


def test_inspector_attempt_ids_are_unique_tuple_values_without_order_contract() -> None:
    """Discovery returns retained semantic IDs without exposing Attempts or order."""
    inspector = ExecutionInspector()
    first = _attempt()
    second = _attempt()

    inspector.attempt_started(first)
    inspector.attempt_finished(_attempt(id=first.id))
    inspector.attempt_started(second)
    identifiers = inspector.attempt_ids()

    assert isinstance(identifiers, tuple)
    assert set(identifiers) == {first.id, second.id}


def test_inspector_accepts_first_evidence_receipt_for_an_identity() -> None:
    """Repeated or conflicting manual receipts retain only the first value."""
    inspector = ExecutionInspector()
    first = _evidence()
    conflicting = _evidence(
        id=first.id,
        attempt_id=first.attempt_id,
        outcome=AttemptFailed(AttemptStage.INTERACTION_INVOCATION),
    )

    inspector.accept(first)
    inspector.accept(first)
    inspector.accept(conflicting)

    assert inspector.get_evidence(first.id) is first
    assert inspector.get_evidence_for_attempt(first.attempt_id) == (first,)


def test_inspector_uses_none_or_empty_tuple_for_missing_identifiers() -> None:
    """Absent entries have deliberately non-exceptional lookup semantics."""
    inspector = ExecutionInspector()
    unknown_attempt = AttemptId.new()
    unknown_evidence = EvidenceId.new()

    assert inspector.attempt_ids() == ()
    assert inspector.get_attempt(unknown_attempt) is None
    assert inspector.get_evidence(unknown_evidence) is None
    assert inspector.get_evidence_for_attempt(unknown_attempt) == ()


def test_inspector_retains_multiple_evidence_values_for_one_attempt() -> None:
    """Evidence-by-Attempt preserves the value model's many-record cardinality."""
    inspector = ExecutionInspector()
    attempt_id = AttemptId.new()
    first = _evidence(attempt_id=attempt_id)
    second = _evidence(
        attempt_id=attempt_id,
        outcome=AttemptCancelled(AttemptStage.INTERACTION_INVOCATION),
    )

    inspector.accept(first)
    inspector.accept(second)
    retained = inspector.get_evidence_for_attempt(attempt_id)

    assert isinstance(retained, tuple)
    assert set(retained) == {first, second}
    expanded = (*retained, first)
    assert len(expanded) == len(retained) + 1
    assert set(inspector.get_evidence_for_attempt(attempt_id)) == {first, second}


def test_inspector_clear_discards_attempt_and_evidence_state() -> None:
    """Manual clearing releases all retained process-local diagnostic state."""
    inspector = ExecutionInspector()
    attempt = _attempt()
    evidence = _evidence(attempt_id=attempt.id)
    inspector.attempt_started(attempt)
    inspector.accept(evidence)

    inspector.clear()

    assert inspector.get_attempt(attempt.id) is None
    assert inspector.get_evidence(evidence.id) is None
    assert inspector.get_evidence_for_attempt(attempt.id) == ()
    assert inspector.attempt_ids() == ()


def test_runtime_both_configuration_publicly_discovers_success() -> None:
    """Existing Runtime seams supply one live Attempt and success Evidence."""

    async def exercise() -> None:
        inspector = ExecutionInspector()
        response = _message("response", role=MessageRole.ASSISTANT, source="agent")
        await Runtime(observer=inspector, evidence_sink=inspector).send(
            session=Session.new(),
            interaction=_FakeInteraction(
                MessageSource("agent"), (InteractionTurn(response),),
            ),
            message=_message("request"),
        )

        attempt_ids = inspector.attempt_ids()
        assert len(attempt_ids) == 1
        attempt = inspector.get_attempt(attempt_ids[0])
        assert attempt is not None
        records = inspector.get_evidence_for_attempt(attempt.id)
        assert len(records) == 1
        assert records[0].attempt_id is attempt.id
        assert isinstance(records[0].outcome, AttemptSucceeded)

    asyncio.run(exercise())


def test_runtime_both_configuration_correlates_failure(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Primary failures retain correlation without replacing their exception."""

    async def exercise() -> None:
        attempts = _capture_attempts(monkeypatch)
        inspector = ExecutionInspector()
        primary = LookupError("agent failed")

        with pytest.raises(LookupError) as raised:
            await Runtime(observer=inspector, evidence_sink=inspector).send(
                session=Session.new(),
                interaction=_FakeInteraction(MessageSource("agent"), error=primary),
                message=_message("request"),
            )

        assert raised.value is primary
        attempt = attempts[0]
        records = inspector.get_evidence_for_attempt(attempt.id)
        assert inspector.get_attempt(attempt.id) is attempt
        assert isinstance(records[0].outcome, AttemptFailed)

    asyncio.run(exercise())


def test_runtime_both_configuration_correlates_cancellation(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Primary cancellation retains correlation and original cancellation identity."""

    async def exercise() -> None:
        attempts = _capture_attempts(monkeypatch)
        inspector = ExecutionInspector()
        primary = asyncio.CancelledError("agent cancelled")

        with pytest.raises(asyncio.CancelledError) as raised:
            await Runtime(observer=inspector, evidence_sink=inspector).send(
                session=Session.new(),
                interaction=_FakeInteraction(MessageSource("agent"), error=primary),
                message=_message("request"),
            )

        assert raised.value is primary
        attempt = attempts[0]
        records = inspector.get_evidence_for_attempt(attempt.id)
        assert inspector.get_attempt(attempt.id) is attempt
        assert isinstance(records[0].outcome, AttemptCancelled)

    asyncio.run(exercise())


def test_runtime_observer_only_retains_orphan_attempt(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Observer-only Runtime retains no terminal Evidence through the inspector."""

    async def exercise() -> None:
        attempts = _capture_attempts(monkeypatch)
        inspector = ExecutionInspector()
        response = _message("response", role=MessageRole.ASSISTANT, source="agent")
        await Runtime(observer=inspector).send(
            session=Session.new(),
            interaction=_FakeInteraction(
                MessageSource("agent"), (InteractionTurn(response),),
            ),
            message=_message("request"),
        )

        attempt = attempts[0]
        assert inspector.get_attempt(attempt.id) is attempt
        assert inspector.attempt_ids() == (attempt.id,)
        assert inspector.get_evidence_for_attempt(attempt.id) == ()

    asyncio.run(exercise())


def test_runtime_sink_only_retains_orphan_evidence(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Sink-only Runtime retains terminal Evidence without live Attempt observation."""

    async def exercise() -> None:
        attempts = _capture_attempts(monkeypatch)
        inspector = ExecutionInspector()
        response = _message("response", role=MessageRole.ASSISTANT, source="agent")
        await Runtime(evidence_sink=inspector).send(
            session=Session.new(),
            interaction=_FakeInteraction(
                MessageSource("agent"), (InteractionTurn(response),),
            ),
            message=_message("request"),
        )

        attempt = attempts[0]
        records = inspector.get_evidence_for_attempt(attempt.id)
        assert inspector.get_attempt(attempt.id) is None
        assert len(records) == 1
        assert records[0].attempt_id is attempt.id

    asyncio.run(exercise())
