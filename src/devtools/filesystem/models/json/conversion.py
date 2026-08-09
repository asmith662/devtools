# Copyright (c) 2026
"""Recursive conversion between parsed and immutable JSON values."""

from __future__ import annotations

from collections.abc import Mapping
from types import MappingProxyType
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from devtools.filesystem.models.json.base import JsonCompatible, JsonValue


def freeze_json(value: JsonCompatible) -> JsonValue:
    """Recursively convert a JSON-compatible value into immutable storage.

    :param value: Parsed JSON-compatible value.
    :returns: Immutable JSON value.
    """
    if isinstance(value, Mapping):
        return MappingProxyType(
            {key: freeze_json(item) for key, item in value.items()},
        )

    if isinstance(value, list | tuple):
        return tuple(freeze_json(item) for item in value)

    return value


def thaw_json(value: JsonValue) -> JsonCompatible:
    """Recursively convert an immutable JSON value into serializable storage.

    :param value: Immutable JSON value.
    :returns: Standard mutable JSON-compatible value.
    """
    if isinstance(value, Mapping):
        return {key: thaw_json(item) for key, item in value.items()}

    if isinstance(value, tuple):
        return [thaw_json(item) for item in value]

    return value
