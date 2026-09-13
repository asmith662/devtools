# Copyright (c) 2026
"""Process-local diagnostic collection of interaction-attempt Evidence."""

from devtools.execution.interaction_attempt import (
    InteractionAttempt,
    InteractionAttemptId,
    InteractionAttemptOutcome,
)
from devtools.observability.evidence.protocols import EvidenceSink
from devtools.observability.evidence.terminal import (
    EvidenceId,
    InteractionAttemptTerminalEvidence,
)


class ExecutionInspector:
    """Observe attempts and construct process-local terminal Evidence."""

    __slots__ = ("_attempts_by_id", "_evidence_by_id", "_sink")

    def __init__(self, sink: EvidenceSink | None = None) -> None:
        """Create an inspector with an optional narrow Evidence sink."""
        self._attempts_by_id: dict[InteractionAttemptId, InteractionAttempt] = {}
        self._evidence_by_id: dict[EvidenceId, InteractionAttemptTerminalEvidence] = {}
        self._sink = sink

    def attempt_started(self, attempt: InteractionAttempt) -> None:
        """Retain a live attempt reference."""
        self._attempts_by_id[attempt.id] = attempt

    def attempt_finished(
        self,
        attempt: InteractionAttempt,
        outcome: InteractionAttemptOutcome,
    ) -> None:
        """Construct and retain Evidence after successful terminalization."""
        self._attempts_by_id[attempt.id] = attempt
        if attempt.completed_at is None:
            return
        evidence = InteractionAttemptTerminalEvidence.new(
            attempt_id=attempt.id,
            occurred_at=attempt.completed_at,
            outcome=outcome,
        )
        self.accept(evidence)
        if self._sink is not None:
            self._sink.accept(evidence)

    def accept(self, evidence: InteractionAttemptTerminalEvidence) -> None:
        """Retain one terminal Evidence value."""
        self._evidence_by_id.setdefault(evidence.id, evidence)

    def attempt_ids(self) -> tuple[InteractionAttemptId, ...]:
        """Return retained attempt identities."""
        return tuple(self._attempts_by_id)

    def get_attempt(
        self,
        attempt_id: InteractionAttemptId,
    ) -> InteractionAttempt | None:
        """Return one retained live attempt."""
        return self._attempts_by_id.get(attempt_id)

    def get_evidence(
        self,
        evidence_id: EvidenceId,
    ) -> InteractionAttemptTerminalEvidence | None:
        """Return retained Evidence by identity."""
        return self._evidence_by_id.get(evidence_id)

    def get_evidence_for_attempt(
        self,
        attempt_id: InteractionAttemptId,
    ) -> tuple[InteractionAttemptTerminalEvidence, ...]:
        """Return retained Evidence correlated to one interaction attempt."""
        return tuple(
            evidence
            for evidence in self._evidence_by_id.values()
            if evidence.attempt_id == attempt_id
        )

    def clear(self) -> None:
        """Discard process-local diagnostic references."""
        self._attempts_by_id.clear()
        self._evidence_by_id.clear()
