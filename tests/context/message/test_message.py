# Copyright (c) 2026
"""Tests for context message value objects."""

from __future__ import annotations

from dataclasses import FrozenInstanceError
from datetime import UTC, datetime

import pytest

from devtools.context import Message, MessageId, MessageRole, MessageSource
from devtools.context.message import (
    Message as MessageFromSubmodule,
)
from devtools.context.message import (
    MessageId as MessageIdFromSubmodule,
)
from devtools.context.message import (
    MessageRole as MessageRoleFromSubmodule,
)
from devtools.context.message import (
    MessageSource as MessageSourceFromSubmodule,
)
from devtools.identity import Identity
from devtools.time import Timestamp


def _message() -> Message:
    """Create a deterministic message for value-semantics tests."""
    return Message(
        id=MessageId.parse("12345678-1234-5678-1234-567812345678"),
        created_at=Timestamp(datetime(2026, 8, 9, 12, 30, tzinfo=UTC)),
        content="Please inspect the repository.",
        role=MessageRole.USER,
        source=MessageSource("operator"),
    )


def test_context_root_reexports_the_canonical_message_types() -> None:
    """Context root exposes each currently implemented message type."""
    assert Message is MessageFromSubmodule
    assert MessageId is MessageIdFromSubmodule
    assert MessageRole is MessageRoleFromSubmodule
    assert MessageSource is MessageSourceFromSubmodule


def test_message_id_is_a_public_immutable_semantic_identity() -> None:
    """Message identities compose generic identities with UUID value semantics."""
    parsed = MessageId.parse("12345678-1234-5678-1234-567812345678")
    equivalent = MessageId(Identity.parse(str(parsed)))
    generated = MessageId.new()
    expected_uuid_version = len(("one", "two", "three", "four"))

    assert isinstance(generated, MessageId)
    assert generated.value.value.version == expected_uuid_version
    assert str(parsed) == "12345678-1234-5678-1234-567812345678"
    assert parsed == equivalent
    assert hash(parsed) == hash(equivalent)

    with pytest.raises(ValueError, match="badly formed"):
        MessageId.parse("not-a-uuid")

    with pytest.raises(FrozenInstanceError):
        parsed.value = Identity.new()  # type: ignore[misc]


def test_message_id_parse_preserves_non_v4_identity_versions() -> None:
    """Message identity parsing retains the generic Identity version policy."""
    value = "6ba7b810-9dad-11d1-80b4-00c04fd430c8"
    expected_uuid_version = len(("one",))
    message_id = MessageId.parse(value)

    assert message_id.value.value.version == expected_uuid_version
    assert str(message_id) == value


def test_message_role_values_are_stable_strings() -> None:
    """Message roles preserve their public string representations."""
    assert MessageRole.USER.value == "user"
    assert MessageRole.ASSISTANT.value == "assistant"
    assert MessageRole.SYSTEM.value == "system"
    assert str(MessageRole.USER) == "user"


def test_message_source_is_immutable_and_uses_exact_nonblank_identifiers() -> None:
    """Sources retain their identifiers without provider normalization."""
    source = MessageSource("codex")
    equivalent = MessageSource("codex")

    assert str(source) == "codex"
    assert source == equivalent
    assert hash(source) == hash(equivalent)

    with pytest.raises(ValueError, match="cannot be blank"):
        MessageSource("")

    with pytest.raises(ValueError, match="cannot be blank"):
        MessageSource("   ")

    with pytest.raises(FrozenInstanceError):
        source.value = "qwen"  # type: ignore[misc]


def test_message_source_preserves_case() -> None:
    """Source labels remain opaque and do not undergo case normalization."""
    source = MessageSource("Codex")

    assert source.value == "Codex"
    assert str(source) == "Codex"


@pytest.mark.parametrize("value", [" codex", "codex "])
def test_message_source_rejects_each_surrounding_whitespace_boundary(
    value: str,
) -> None:
    """Successful source values must equal their stripped representation."""
    with pytest.raises(ValueError, match="surrounding whitespace"):
        MessageSource(value)


@pytest.mark.parametrize(
    "content",
    [
        "",
        "   ",
        "first line\nsecond line",
        "café — こんにちは",
        '# Heading\n{"status": "ok"}',
    ],
)
def test_message_preserves_uninterpreted_content_exactly(content: str) -> None:
    """Message content accepts text without trimming or interpretation."""
    message = Message(
        id=MessageId.parse("12345678-1234-5678-1234-567812345678"),
        created_at=Timestamp(datetime(2026, 8, 9, 12, 30, tzinfo=UTC)),
        content=content,
        role=MessageRole.SYSTEM,
        source=MessageSource("runtime"),
    )

    assert message.content == content
    assert str(message) == content


def test_message_supports_deterministic_immutable_value_semantics() -> None:
    """Explicit construction preserves supplied fields and remains hashable."""
    message = _message()
    equivalent = _message()

    assert message.role is MessageRole.USER
    assert message.source == MessageSource("operator")
    assert message == equivalent
    assert hash(message) == hash(equivalent)

    with pytest.raises(FrozenInstanceError):
        message.content = "Changed."  # type: ignore[misc]


def test_message_new_generates_identity_and_timestamp_without_mutating_inputs() -> None:
    """The convenience factory creates fresh message state from supplied values."""
    source = MessageSource("codex")
    first = Message.new(
        "First response.",
        role=MessageRole.ASSISTANT,
        source=source,
    )
    second = Message.new(
        "Second response.",
        role=MessageRole.ASSISTANT,
        source=source,
    )

    assert first.id != second.id
    assert isinstance(first.created_at, Timestamp)
    assert first.created_at.value.tzinfo is UTC
    assert first.content == "First response."
    assert first.role is MessageRole.ASSISTANT
    assert first.source is source
