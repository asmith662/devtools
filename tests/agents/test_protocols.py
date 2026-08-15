# Copyright (c) 2026
"""Tests for the structural agent protocol."""

from __future__ import annotations

import asyncio
from dataclasses import dataclass
from datetime import UTC, datetime

from devtools.agents import Agent, AgentTurn, ConversationRef
from devtools.message import Message, MessageId, MessageRole, MessageSource
from devtools.time import Timestamp


@dataclass(frozen=True, slots=True)
class FakeAgent:
    """Minimal structural Agent implementation used for protocol coverage."""

    source: MessageSource

    async def send(
        self,
        message: Message,
        *,
        conversation: ConversationRef | None = None,
    ) -> AgentTurn:
        """Return a same-source final response and preserve continuation state."""
        response = Message(
            id=MessageId.parse("12345678-1234-5678-1234-567812345678"),
            created_at=Timestamp(datetime(2026, 8, 10, 13, 0, tzinfo=UTC)),
            content=f"Reply to: {message.content}",
            role=MessageRole.ASSISTANT,
            source=self.source,
        )
        return AgentTurn(message=response, conversation=conversation)


def test_agent_protocol_is_structural_and_supports_async_continued_calls() -> None:
    """A compatible implementation can be used solely through Agent typing."""
    source = MessageSource("fake")
    agent: Agent = FakeAgent(source)
    prompt = Message(
        id=MessageId.parse("87654321-4321-8765-4321-876543218765"),
        created_at=Timestamp(datetime(2026, 8, 10, 12, 45, tzinfo=UTC)),
        content="Remember ALPHA-4821.",
        role=MessageRole.USER,
        source=MessageSource("user"),
    )
    conversation = ConversationRef(source, "opaque-thread")

    async def send_twice() -> tuple[AgentTurn, AgentTurn]:
        """Exercise fresh and continued generic invocation shapes."""
        first = await agent.send(prompt)
        second = await agent.send(prompt, conversation=conversation)
        return first, second

    first, second = asyncio.run(send_twice())

    assert first.conversation is None
    assert first.message.source == source
    assert second.conversation is conversation
    assert second.message.source == source
