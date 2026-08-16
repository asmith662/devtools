# Copyright (c) 2026
"""Tests for Session semantic identity values."""

from __future__ import annotations

from dataclasses import FrozenInstanceError

import pytest

from devtools.context import Session, SessionId
from devtools.context.session import Session as SessionFromSubmodule
from devtools.context.session import SessionId as SessionIdFromSubmodule
from devtools.identity import Identity


def test_context_root_and_submodule_expose_the_same_session_types() -> None:
    """Session public imports are canonical type identities."""
    assert Session is SessionFromSubmodule
    assert SessionId is SessionIdFromSubmodule


def test_session_id_is_an_immutable_semantic_identity() -> None:
    """Session identities compose generic Identity with UUID value semantics."""
    parsed = SessionId.parse("12345678-1234-5678-1234-567812345678")
    equivalent = SessionId(Identity.parse(str(parsed)))
    generated = SessionId.new()
    expected_uuid_version = len(("one", "two", "three", "four"))

    assert generated.value.value.version == expected_uuid_version
    assert str(parsed) == "12345678-1234-5678-1234-567812345678"
    assert parsed == equivalent
    assert hash(parsed) == hash(equivalent)

    with pytest.raises(ValueError, match="badly formed"):
        SessionId.parse("not-a-uuid")

    with pytest.raises(FrozenInstanceError):
        parsed.value = Identity.new()  # type: ignore[misc]


def test_session_id_parsing_preserves_identity_version_and_canonical_text() -> None:
    """SessionId keeps the generic Identity parser's UUID-version behavior."""
    non_v4 = "6ba7b810-9dad-11d1-80b4-00c04fd430c8"
    uppercase = "12345678-1234-5678-1234-567812345678".upper()
    expected_uuid_version = len(("one",))

    parsed_non_v4 = SessionId.parse(non_v4)
    parsed_uppercase = SessionId.parse(uppercase)

    assert parsed_non_v4.value.value.version == expected_uuid_version
    assert str(parsed_non_v4) == non_v4
    assert str(parsed_uppercase) == uppercase.lower()
