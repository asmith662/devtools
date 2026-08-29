# Copyright (c) 2026
"""Structural protocols for factual execution observation."""

from __future__ import annotations

from typing import TYPE_CHECKING, Protocol

if TYPE_CHECKING:
    from devtools.evidence.attempt import Attempt


class AttemptObserver(Protocol):
    """Observe one live Attempt lifecycle synchronously."""

    def attempt_started(self, attempt: Attempt) -> None:
        """Observe a newly created running attempt."""

    def attempt_finished(self, attempt: Attempt) -> None:
        """Observe an attempt after successful terminalization."""
