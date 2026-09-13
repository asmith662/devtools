# Copyright (c) 2026
"""Tests for Conversation semantic identity values."""

from __future__ import annotations

from dataclasses import FrozenInstanceError

import pytest

from devtools.agents.conversation import Conversation, ConversationId
from devtools.agents.conversation.conversation import (
    Conversation as SessionFromSubmodule,
)
from devtools.agents.conversation.conversation import (
    ConversationId as SessionIdFromSubmodule,
)
from devtools.core.identity import Identity


def test_context_root_and_submodule_expose_the_same_session_types() -> None:
    """Conversation public imports are canonical type identities."""
    assert Conversation is SessionFromSubmodule
    assert ConversationId is SessionIdFromSubmodule


def test_session_id_is_an_immutable_semantic_identity() -> None:
    """Conversation identities compose generic Identity with UUID value semantics."""
    parsed = ConversationId.parse("12345678-1234-5678-1234-567812345678")
    equivalent = ConversationId(Identity.parse(str(parsed)))
    generated = ConversationId.new()
    expected_uuid_version = len(("one", "two", "three", "four"))

    assert generated.value.value.version == expected_uuid_version
    assert str(parsed) == "12345678-1234-5678-1234-567812345678"
    assert parsed == equivalent
    assert hash(parsed) == hash(equivalent)

    with pytest.raises(ValueError, match="badly formed"):
        ConversationId.parse("not-a-uuid")

    with pytest.raises(FrozenInstanceError):
        parsed.value = Identity.new()  # type: ignore[misc]


def test_session_id_parsing_preserves_identity_version_and_canonical_text() -> None:
    """ConversationId keeps the generic Identity parser's UUID-version behavior."""
    non_v4 = "6ba7b810-9dad-11d1-80b4-00c04fd430c8"
    uppercase = "12345678-1234-5678-1234-567812345678".upper()
    expected_uuid_version = len(("one",))

    parsed_non_v4 = ConversationId.parse(non_v4)
    parsed_uppercase = ConversationId.parse(uppercase)

    assert parsed_non_v4.value.value.version == expected_uuid_version
    assert str(parsed_non_v4) == non_v4
    assert str(parsed_uppercase) == uppercase.lower()
