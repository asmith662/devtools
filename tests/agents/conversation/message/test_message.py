# Copyright (c) 2026
# ruff: noqa: E501
"""Tests for context message value objects."""

from __future__ import annotations

from dataclasses import FrozenInstanceError
from datetime import UTC, datetime

import pytest

from devtools.agents.conversation import (
    ConversationMessage,
    ConversationMessageRole,
    MessageId,
)
from devtools.agents.conversation.message import (
    ConversationMessage as MessageFromSubmodule,
)
from devtools.agents.conversation.message import (
    ConversationMessageRole as MessageRoleFromSubmodule,
)
from devtools.agents.conversation.message import (
    MessageId as MessageIdFromSubmodule,
)
from devtools.core.identity import Identity
from devtools.core.time import Timestamp
from devtools.models.interaction import InteractionSource


def _message() -> ConversationMessage:
    """Create a deterministic message for value-semantics tests."""
    return ConversationMessage(
        id=MessageId.parse("12345678-1234-5678-1234-567812345678"),
        created_at=Timestamp(datetime(2026, 8, 9, 12, 30, tzinfo=UTC)),
        content="Please inspect the repository.",
        role=ConversationMessageRole.USER,
        source=InteractionSource("operator"),
    )


def test_context_root_reexports_the_canonical_message_types() -> None:
    """Context root exposes each currently implemented message type."""
    assert ConversationMessage is MessageFromSubmodule
    assert MessageId is MessageIdFromSubmodule
    assert ConversationMessageRole is MessageRoleFromSubmodule


def test_message_id_is_a_public_immutable_semantic_identity() -> None:
    """ConversationMessage identities compose generic identities with UUID value semantics."""
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
    """ConversationMessage identity parsing retains the generic Identity version policy."""
    value = "6ba7b810-9dad-11d1-80b4-00c04fd430c8"
    expected_uuid_version = len(("one",))
    message_id = MessageId.parse(value)

    assert message_id.value.value.version == expected_uuid_version
    assert str(message_id) == value


def test_message_role_values_are_stable_strings() -> None:
    """ConversationMessage roles preserve their public string representations."""
    assert ConversationMessageRole.USER.value == "user"
    assert ConversationMessageRole.ASSISTANT.value == "assistant"
    assert ConversationMessageRole.SYSTEM.value == "system"
    assert str(ConversationMessageRole.USER) == "user"


def test_message_source_is_immutable_and_uses_exact_nonblank_identifiers() -> None:
    """Sources retain their identifiers without provider normalization."""
    source = InteractionSource("codex")
    equivalent = InteractionSource("codex")

    assert str(source) == "codex"
    assert source == equivalent
    assert hash(source) == hash(equivalent)

    with pytest.raises(ValueError, match="cannot be blank"):
        InteractionSource("")

    with pytest.raises(ValueError, match="cannot be blank"):
        InteractionSource("   ")

    with pytest.raises(FrozenInstanceError):
        source.value = "qwen"  # type: ignore[misc]


def test_message_source_preserves_case() -> None:
    """Source labels remain opaque and do not undergo case normalization."""
    source = InteractionSource("Codex")

    assert source.value == "Codex"
    assert str(source) == "Codex"


@pytest.mark.parametrize("value", [" codex", "codex "])
def test_message_source_rejects_each_surrounding_whitespace_boundary(
    value: str,
) -> None:
    """Successful source values must equal their stripped representation."""
    with pytest.raises(ValueError, match="surrounding whitespace"):
        InteractionSource(value)


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
    """ConversationMessage content accepts text without trimming or interpretation."""
    message = ConversationMessage(
        id=MessageId.parse("12345678-1234-5678-1234-567812345678"),
        created_at=Timestamp(datetime(2026, 8, 9, 12, 30, tzinfo=UTC)),
        content=content,
        role=ConversationMessageRole.SYSTEM,
        source=InteractionSource("runtime"),
    )

    assert message.content == content
    assert str(message) == content


def test_message_supports_deterministic_immutable_value_semantics() -> None:
    """Explicit construction preserves supplied fields and remains hashable."""
    message = _message()
    equivalent = _message()

    assert message.role is ConversationMessageRole.USER
    assert message.source == InteractionSource("operator")
    assert message == equivalent
    assert hash(message) == hash(equivalent)

    with pytest.raises(FrozenInstanceError):
        message.content = "Changed."  # type: ignore[misc]


def test_message_new_generates_identity_and_timestamp_without_mutating_inputs() -> None:
    """The convenience factory creates fresh message state from supplied values."""
    source = InteractionSource("codex")
    first = ConversationMessage.new(
        "First response.",
        role=ConversationMessageRole.ASSISTANT,
        source=source,
    )
    second = ConversationMessage.new(
        "Second response.",
        role=ConversationMessageRole.ASSISTANT,
        source=source,
    )

    assert first.id != second.id
    assert isinstance(first.created_at, Timestamp)
    assert first.created_at.value.tzinfo is UTC
    assert first.content == "First response."
    assert first.role is ConversationMessageRole.ASSISTANT
    assert first.source is source
