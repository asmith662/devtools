# Copyright (c) 2026
"""Experimental process-local diagnostics for Runtime execution observation."""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from devtools.evidence.attempt import Attempt, AttemptId
    from devtools.evidence.terminal import AttemptTerminalEvidence, EvidenceId


__all__ = ["ExecutionInspector"]


class ExecutionInspector:
    """Correlate live Attempts and terminal Evidence in process-local memory.

    This experimental diagnostic consumer is neither durable storage nor
    canonical execution history.
    """

    __slots__ = ("_attempts_by_id", "_evidence_by_id")

    def __init__(self) -> None:
        """Create an empty process-local execution inspector."""
        self._attempts_by_id: dict[AttemptId, Attempt] = {}
        self._evidence_by_id: dict[EvidenceId, AttemptTerminalEvidence] = {}

    def attempt_started(self, attempt: Attempt) -> None:
        """Retain the current live Attempt reference by its semantic identity."""
        self._attempts_by_id[attempt.id] = attempt

    def attempt_finished(self, attempt: Attempt) -> None:
        """Refresh the current live Attempt reference by its semantic identity."""
        self._attempts_by_id[attempt.id] = attempt

    def accept(self, evidence: AttemptTerminalEvidence) -> None:
        """Retain the first accepted immutable terminal Evidence for its identity."""
        self._evidence_by_id.setdefault(evidence.id, evidence)

    def attempt_ids(self) -> tuple[AttemptId, ...]:
        """Return currently retained Attempt identities without an order guarantee."""
        return tuple(self._attempts_by_id)

    def get_attempt(self, attempt_id: AttemptId) -> Attempt | None:
        """Return the retained live Attempt reference, if currently known."""
        return self._attempts_by_id.get(attempt_id)

    def get_evidence(
        self,
        evidence_id: EvidenceId,
    ) -> AttemptTerminalEvidence | None:
        """Return retained immutable terminal Evidence by semantic identity."""
        return self._evidence_by_id.get(evidence_id)

    def get_evidence_for_attempt(
        self,
        attempt_id: AttemptId,
    ) -> tuple[AttemptTerminalEvidence, ...]:
        """Return a fresh immutable collection of Evidence for one Attempt."""
        return tuple(
            evidence
            for evidence in self._evidence_by_id.values()
            if evidence.attempt_id == attempt_id
        )

    def clear(self) -> None:
        """Discard every process-local Attempt and Evidence reference."""
        self._attempts_by_id.clear()
        self._evidence_by_id.clear()
