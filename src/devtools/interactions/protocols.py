# Copyright (c) 2026
"""Structural protocols for asynchronous interactions."""

from __future__ import annotations

from typing import TYPE_CHECKING, Protocol

if TYPE_CHECKING:
    from devtools.context.message import Message, MessageSource

    from .models import ConversationRef, InteractionTurn


class Interaction(Protocol):
    """Describe one asynchronous source-owned message interaction.

    Implementations own provider-specific transport, configuration, failures,
    and conversation-resumption behavior. When a conversation is supplied,
    implementations must reject one owned by a different source.
    """

    @property
    def source(self) -> MessageSource:
        """Return the source represented by this interaction."""

    async def send(
        self,
        message: Message,
        *,
        conversation: ConversationRef | None = None,
    ) -> InteractionTurn:
        """Send one message and return the final interaction turn."""
