# Copyright (c) 2026
"""Tests for identity value objects."""

from __future__ import annotations

from dataclasses import FrozenInstanceError
from uuid import UUID

import pytest

from devtools.identity import Identity


def test_identity_preserves_uuid_value_and_canonical_string() -> None:
    """Identities use UUID value semantics and canonical string output."""
    value = UUID("12345678-1234-5678-1234-567812345678")
    identity = Identity(value)

    assert identity.value is value
    assert str(identity) == "12345678-1234-5678-1234-567812345678"
    assert Identity.parse(str(identity)) == identity


def test_identity_new_generates_uuid4_and_parse_rejects_invalid_text() -> None:
    """New identities are UUID4 values and malformed input remains invalid."""
    identity = Identity.new()
    expected_uuid_version = len(("one", "two", "three", "four"))

    assert identity.value.version == expected_uuid_version

    with pytest.raises(ValueError, match="badly formed"):
        Identity.parse("not-a-uuid")


def test_identity_is_immutable_and_has_uuid_value_equality_and_hashing() -> None:
    """Identities are frozen UUID value objects suitable for dictionary keys."""
    value = UUID("12345678-1234-5678-1234-567812345678")
    identity = Identity(value)
    equivalent = Identity(value)

    assert identity == equivalent
    assert hash(identity) == hash(equivalent)

    with pytest.raises(FrozenInstanceError):
        identity.value = UUID("87654321-4321-8765-4321-876543218765")  # type: ignore[misc]


def test_identity_parse_normalizes_text_and_preserves_non_v4_versions() -> None:
    """Parsing accepts standard UUID text without restricting UUID versions."""
    uppercase = "A0B1C2D3-E4F5-4678-9ABC-DEF012345678"
    non_v4 = "6ba7b810-9dad-11d1-80b4-00c04fd430c8"
    expected_version = len(("one",))

    assert str(Identity.parse(uppercase)) == "a0b1c2d3-e4f5-4678-9abc-def012345678"
    assert Identity.parse(non_v4).value.version == expected_version
