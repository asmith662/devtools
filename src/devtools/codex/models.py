# Copyright (c) 2026
"""Small Codex-specific parsed values."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class CodexTurnOutput:
    """Represent the successful final values emitted by Codex JSONL.

    :ivar thread_id: Codex session identifier accepted by ``codex exec resume``.
    :ivar final_message: Final completed Codex agent message.
    """

    thread_id: str
    final_message: str
