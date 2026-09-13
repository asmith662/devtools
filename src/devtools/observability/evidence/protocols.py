# Copyright (c) 2026
"""Evidence delivery contract."""

from typing import Protocol

from devtools.observability.evidence.terminal import InteractionAttemptTerminalEvidence


class EvidenceSink(Protocol):
    """Accept immutable terminal Evidence synchronously."""

    def accept(self, evidence: InteractionAttemptTerminalEvidence) -> None:
        """Accept responsibility for one Evidence record."""
