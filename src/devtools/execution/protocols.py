# Copyright (c) 2026
"""Execution-lifecycle observation contracts."""

from typing import Protocol

from devtools.execution.interaction_attempt import (
    InteractionAttempt,
    InteractionAttemptOutcome,
)


class InteractionAttemptObserver(Protocol):
    """Observe one Runtime-managed interaction-attempt lifecycle."""

    def attempt_started(self, attempt: InteractionAttempt) -> None:
        """Observe a newly created running attempt."""

    def attempt_finished(
        self,
        attempt: InteractionAttempt,
        outcome: InteractionAttemptOutcome,
    ) -> None:
        """Observe a successfully terminalized attempt and terminal facts."""
