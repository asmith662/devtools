# Copyright (c) 2026
"""Tests for the structural Interaction protocol."""

from __future__ import annotations

import asyncio
from dataclasses import dataclass
from datetime import UTC, datetime

from devtools.context.message import Message, MessageId, MessageRole, MessageSource
from devtools.interactions import ConversationRef, Interaction, InteractionTurn
from devtools.time import Timestamp


@dataclass(frozen=True, slots=True)
class FakeInteraction:
    """Minimal structural Interaction implementation used for protocol coverage."""

    source: MessageSource

    async def send(
        self,
        message: Message,
        *,
        conversation: ConversationRef | None = None,
    ) -> InteractionTurn:
        """Return a same-source final response and preserve continuation state."""
        response = Message(
            id=MessageId.parse("12345678-1234-5678-1234-567812345678"),
            created_at=Timestamp(datetime(2026, 8, 10, 13, 0, tzinfo=UTC)),
            content=f"Reply to: {message.content}",
            role=MessageRole.ASSISTANT,
            source=self.source,
        )
        return InteractionTurn(message=response, conversation=conversation)


def test_interaction_protocol_is_structural_and_supports_async_continued_calls() -> (
    None
):
    """A compatible implementation can be used solely through Interaction typing."""
    source = MessageSource("fake")
    interaction: Interaction = FakeInteraction(source)
    prompt = Message(
        id=MessageId.parse("87654321-4321-8765-4321-876543218765"),
        created_at=Timestamp(datetime(2026, 8, 10, 12, 45, tzinfo=UTC)),
        content="Remember ALPHA-4821.",
        role=MessageRole.USER,
        source=MessageSource("user"),
    )
    conversation = ConversationRef(source, "opaque-thread")

    async def send_twice() -> tuple[InteractionTurn, InteractionTurn]:
        """Exercise fresh and continued generic invocation shapes."""
        first = await interaction.send(prompt)
        second = await interaction.send(prompt, conversation=conversation)
        return first, second

    first, second = asyncio.run(send_twice())

    assert first.conversation is None
    assert first.message.source == source
    assert second.conversation is conversation
    assert second.message.source == source
