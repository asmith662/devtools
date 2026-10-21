# Copyright (c) 2026
# ruff: noqa: COM812 -- maintained test formatting convention
"""Independent regressions for Qwen's UUID-backed Identity constructor."""

from dataclasses import FrozenInstanceError
from typing import cast
from uuid import UUID

import pytest

from devtools.core.identity import Identity


class SpecializedIdentity(Identity):
    """A semantic identity specialization inherits the invariant."""


@pytest.mark.parametrize("value", [None, "not-a-uuid", 1, True, b"uuid", object()])
@pytest.mark.parametrize("identity_type", [Identity, SpecializedIdentity])
def test_invalid_direct_identity_values(
    value: object, identity_type: type[Identity]
) -> None:
    """Annotations do not substitute for runtime UUID enforcement."""
    with pytest.raises(TypeError, match="UUID"):
        identity_type(cast("UUID", value))


@pytest.mark.parametrize("identity_type", [Identity, SpecializedIdentity])
def test_valid_uuid_and_factories_preserve_semantic_identity(
    identity_type: type[Identity],
) -> None:
    """Factories, immutability, equality and hashing retain their contracts."""
    value = UUID("12345678-1234-5678-1234-567812345678")
    identity = identity_type(value)
    assert identity.value is value
    assert identity_type.parse(str(value)) == identity
    assert hash(identity_type(value)) == hash(identity)
    assert isinstance(identity_type.new(), identity_type)
    attribute = "value"
    with pytest.raises(FrozenInstanceError):
        setattr(identity, attribute, value)
    with pytest.raises(ValueError, match="badly formed"):
        identity_type.parse("invalid")
