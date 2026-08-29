# Copyright (c) 2026
"""Tests for Evidence structural protocols."""

from __future__ import annotations

from devtools import evidence
from devtools.context import MessageId, MessageSource, SessionId
from devtools.evidence import Attempt, AttemptId, AttemptObserver, AttemptState
from devtools.evidence.protocols import AttemptObserver as AttemptObserverFromSubmodule
from devtools.time import Timestamp


class FakeObserver:
    """Minimal structural AttemptObserver implementation."""

    def __init__(self) -> None:
        """Initialize observed lifecycle storage."""
        self.started: list[Attempt] = []
        self.finished: list[Attempt] = []

    def attempt_started(self, attempt: Attempt) -> None:
        """Record a started attempt."""
        self.started.append(attempt)

    def attempt_finished(self, attempt: Attempt) -> None:
        """Record a finished attempt."""
        self.finished.append(attempt)


def test_attempt_observer_is_a_structural_root_public_protocol() -> None:
    """A plain compatible object satisfies the public observation contract."""
    fake = FakeObserver()
    observer: AttemptObserver = fake
    attempt = Attempt(
        id=AttemptId.new(),
        session_id=SessionId.new(),
        message_id=MessageId.new(),
        agent_source=MessageSource("agent"),
        started_at=Timestamp.now(),
        state=AttemptState.RUNNING,
        completed_at=None,
    )

    observer.attempt_started(attempt)
    attempt.succeed()
    observer.attempt_finished(attempt)

    assert AttemptObserver is AttemptObserverFromSubmodule
    assert evidence.__all__ == [
        "Attempt",
        "AttemptCancelled",
        "AttemptFailed",
        "AttemptId",
        "AttemptObserver",
        "AttemptStage",
        "AttemptState",
        "AttemptSucceeded",
        "AttemptTerminalEvidence",
        "AttemptTerminalOutcome",
        "EvidenceId",
    ]
    assert fake.started == [attempt]
    assert fake.finished == [attempt]
