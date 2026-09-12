# Copyright (c) 2026
"""Strict portable JSON Session persistence tests."""

from __future__ import annotations

import asyncio
import json
from datetime import UTC, datetime

import pytest

from devtools.context import (
    History,
    Message,
    MessageId,
    MessageRole,
    MessageSource,
    Session,
    SessionId,
)
from devtools.interactions import ConversationRef
from devtools.persistence import (
    PersistenceConflictError,
    PersistenceFormatError,
    PersistenceVersionError,
    decode_session_json,
    encode_session_json,
)
from devtools.time import Timestamp


def _timestamp() -> Timestamp:
    """Return a deterministic UTC timestamp."""
    return Timestamp(datetime(2026, 1, 2, 3, 4, 5, 678901, tzinfo=UTC))


def _message(
    number: int,
    *,
    content: str = "content",
    role: MessageRole = MessageRole.USER,
    source: str = "user",
) -> Message:
    """Build one deterministic Message."""
    return Message(
        id=MessageId.parse(f"00000000-0000-4000-8000-{number:012d}"),
        created_at=_timestamp(),
        content=content,
        role=role,
        source=MessageSource(source),
    )


def _session() -> Session:
    """Build a populated deterministic Session with duplicate occurrence."""
    first = _message(1, content="  whitespace\n雪\n", source="caller")
    second = _message(2, role=MessageRole.ASSISTANT, source="agent")
    third = _message(3, content="", role=MessageRole.SYSTEM, source="system")
    return Session(
        id=SessionId.parse("10000000-0000-4000-8000-000000000001"),
        created_at=_timestamp(),
        history=History(messages=(first, second, first, third)),
        conversations=(
            ConversationRef(MessageSource("zeta"), "thread-z"),
            ConversationRef(MessageSource("agent"), "thread-a"),
        ),
    )


def _value() -> dict[str, object]:
    """Return a mutable decoded valid persistence value."""
    value = json.loads(encode_session_json(_session()))
    assert isinstance(value, dict)
    return value


def test_json_round_trip_preserves_semantic_session_state_and_fresh_turn() -> None:
    """JSON restores ordered Message values and current conversations."""
    original = _session()
    text = encode_session_json(original)
    restored = decode_session_json(text)

    assert restored is not original
    assert restored.id == original.id
    assert restored.created_at == original.created_at
    assert restored.history == original.history
    assert restored.history.messages[0] is restored.history.messages[2]
    assert restored.conversations == original.conversations
    assert text == encode_session_json(original)
    value = json.loads(text)
    assert value["conversations"][0]["source"] == "agent"
    assert "雪" in text

    async def acquire() -> None:
        async with restored.turn():
            pass

    asyncio.run(acquire())


def test_json_empty_session_round_trip() -> None:
    """An empty Session has a portable strict JSON representation."""
    original = Session(
        id=SessionId.parse("10000000-0000-4000-8000-000000000002"),
        created_at=_timestamp(),
    )

    restored = decode_session_json(encode_session_json(original))

    assert restored.id == original.id
    assert restored.created_at == original.created_at
    assert restored.history == History()
    assert dict(restored.conversations) == {}


@pytest.mark.parametrize(
    ("mutate", "error"),
    [
        (lambda value: value.update({"schema_version": 2}), PersistenceVersionError),
        (lambda value: value.update({"schema_version": True}), PersistenceFormatError),
        (lambda value: value.update({"unexpected": None}), PersistenceFormatError),
        (lambda value: value.pop("history"), PersistenceFormatError),
        (lambda value: value.update({"history": {}}), PersistenceFormatError),
        (
            lambda value: value["session"].update({"extra": None}),
            PersistenceFormatError,
        ),
        (lambda value: value["session"].pop("id"), PersistenceFormatError),
        (lambda value: value["session"].update({"id": 1}), PersistenceFormatError),
        (
            lambda value: value["history"][0].update({"role": "unknown"}),
            PersistenceFormatError,
        ),
        (
            lambda value: value["history"][0].update({"source": " "}),
            PersistenceFormatError,
        ),
        (
            lambda value: value["history"][0].update({"id": "not-a-uuid"}),
            PersistenceFormatError,
        ),
        (
            lambda value: value["history"][0].update({"created_at": "invalid"}),
            PersistenceFormatError,
        ),
        (lambda value: value["history"][0].pop("content"), PersistenceFormatError),
        (
            lambda value: value["conversations"][0].update({"value": " "}),
            PersistenceFormatError,
        ),
    ],
)
def test_json_rejects_invalid_schema_values(
    mutate: object,
    error: type[Exception],
) -> None:
    """Version, shape, and Context-value failures are format failures."""
    value = _value()
    assert callable(mutate)
    mutate(value)

    with pytest.raises(error):
        decode_session_json(json.dumps(value))


@pytest.mark.parametrize(
    "text",
    [
        "{",
        "[]",
        '{"schema_version": 1, "schema_version": 1}',
        '{"schema_version": NaN}',
    ],
)
def test_json_rejects_invalid_json_syntax_keys_and_constants(text: str) -> None:
    """Strict parsing does not collapse malformed or non-standard values."""
    with pytest.raises(PersistenceFormatError):
        decode_session_json(text)


def test_json_rejects_duplicate_conversation_source() -> None:
    """Current continuation sources must remain unambiguous."""
    value = _value()
    conversations = value["conversations"]
    assert isinstance(conversations, list)
    conversations.append({"source": "agent", "value": "other"})

    with pytest.raises(PersistenceFormatError):
        decode_session_json(json.dumps(value))


def test_json_rejects_conflicting_repeated_message_id() -> None:
    """One immutable MessageId cannot describe conflicting Message values."""
    value = _value()
    history = value["history"]
    assert isinstance(history, list)
    duplicate = history[2]
    assert isinstance(duplicate, dict)
    duplicate["content"] = "different"

    with pytest.raises(PersistenceConflictError):
        decode_session_json(json.dumps(value))
