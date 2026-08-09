# Copyright (c) 2026
"""Tests for identity value objects."""

from __future__ import annotations

from uuid import UUID

import pytest

from devtools.identity.models import Identity


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
