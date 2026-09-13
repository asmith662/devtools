# Copyright (c) 2026
"""Small Codex-specific parsed values."""

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from devtools.agents.conversation import ConversationMessage
    from devtools.models.interaction import ConversationRef


@dataclass(frozen=True, slots=True)
class CodexTurnOutput:
    """Represent the successful final values emitted by Codex JSONL.

    :ivar thread_id: Codex session identifier accepted by ``codex exec resume``.
    :ivar final_message: Final completed Codex agent message.
    """

    thread_id: str
    final_message: str


@dataclass(frozen=True, slots=True)
class CodexConversationResult:
    """Represent one external-agent response and its continuation."""

    message: ConversationMessage
    conversation: ConversationRef
