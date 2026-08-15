# Copyright (c) 2026
"""Structural protocols for asynchronous agents."""

from __future__ import annotations

from typing import TYPE_CHECKING, Protocol

if TYPE_CHECKING:
    from devtools.message import Message, MessageSource

    from .models import AgentTurn, ConversationRef


class Agent(Protocol):
    """Describe an asynchronous agent that exchanges final messages.

    Implementations own provider-specific transport, configuration, failures,
    and conversation-resumption behavior. When a conversation is supplied,
    implementations must reject one owned by a different source.
    """

    @property
    def source(self) -> MessageSource:
        """Return the source represented by this agent."""

    async def send(
        self,
        message: Message,
        *,
        conversation: ConversationRef | None = None,
    ) -> AgentTurn:
        """Send one message and return the final agent turn."""
