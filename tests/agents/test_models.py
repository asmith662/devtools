# Copyright (c) 2026
"""Tests for agent value objects."""

from __future__ import annotations

from dataclasses import FrozenInstanceError
from datetime import UTC, datetime

import pytest

from devtools.agents import AgentTurn, ConversationRef
from devtools.context.message import Message, MessageId, MessageRole, MessageSource
from devtools.time import Timestamp


def _message(source: MessageSource) -> Message:
    """Create a deterministic agent response message."""
    return Message(
        id=MessageId.parse("12345678-1234-5678-1234-567812345678"),
        created_at=Timestamp(datetime(2026, 8, 10, 12, 30, tzinfo=UTC)),
        content="A final response.",
        role=MessageRole.ASSISTANT,
        source=source,
    )


def test_conversation_ref_is_a_public_immutable_opaque_value() -> None:
    """Conversation references preserve arbitrary source-owned identifiers."""
    source = MessageSource("Codex")
    reference = ConversationRef(source=source, value="opaque-token:ALPHA/42")
    equivalent = ConversationRef(
        source=MessageSource("Codex"),
        value="opaque-token:ALPHA/42",
    )

    assert reference.source is source
    assert reference.value == "opaque-token:ALPHA/42"
    assert reference == equivalent
    assert hash(reference) == hash(equivalent)

    with pytest.raises(FrozenInstanceError):
        reference.value = "other"  # type: ignore[misc]


@pytest.mark.parametrize(
    "value",
    [
        "019f2b90-1234-5678-90ab-cdef12345678",
        "conversation_token.v1/ALPHA:42",
    ],
)
def test_conversation_ref_accepts_uuid_and_non_uuid_opaque_values(value: str) -> None:
    """References do not parse or constrain provider-specific identifiers."""
    reference = ConversationRef(MessageSource("qwen"), value)

    assert reference.value == value


@pytest.mark.parametrize("value", ["", "   "])
def test_conversation_ref_rejects_blank_values(value: str) -> None:
    """A continuation identifier must contain non-whitespace text."""
    with pytest.raises(ValueError, match="cannot be blank"):
        ConversationRef(MessageSource("codex"), value)


@pytest.mark.parametrize("value", [" codex-thread", "codex-thread "])
def test_conversation_ref_rejects_each_surrounding_whitespace_boundary(
    value: str,
) -> None:
    """Successful reference values equal their stripped representation."""
    with pytest.raises(ValueError, match="surrounding whitespace"):
        ConversationRef(MessageSource("codex"), value)


def test_agent_turn_supports_stateless_and_matching_continued_value_semantics() -> None:
    """Turns preserve final messages and optional same-source continuation state."""
    source = MessageSource("codex")
    message = _message(source)
    stateless = AgentTurn(message)
    reference = ConversationRef(source, "thread-42")
    continued = AgentTurn(message=message, conversation=reference)
    equivalent = AgentTurn(message=message, conversation=reference)

    assert stateless.message is message
    assert stateless.conversation is None
    assert continued.message is message
    assert continued.conversation is reference
    assert continued == equivalent
    assert hash(continued) == hash(equivalent)

    with pytest.raises(FrozenInstanceError):
        continued.conversation = None  # type: ignore[misc]


def test_agent_turn_accepts_equal_distinct_source_values() -> None:
    """Ownership compares source values rather than object identity."""
    message = _message(MessageSource("codex"))
    conversation = ConversationRef(MessageSource("codex"), "thread-42")

    turn = AgentTurn(message=message, conversation=conversation)

    assert turn.conversation is conversation


def test_agent_turn_rejects_a_conversation_owned_by_another_source() -> None:
    """Continuation state and final message must share one producer source."""
    message = _message(MessageSource("codex"))
    reference = ConversationRef(MessageSource("qwen"), "thread-42")

    with pytest.raises(ValueError, match="must match"):
        AgentTurn(message=message, conversation=reference)
