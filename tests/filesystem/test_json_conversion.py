# Copyright (c) 2026
"""Tests for recursive immutable JSON conversion."""

from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, cast

import pytest

from devtools.filesystem.models.json import freeze_json, thaw_json

if TYPE_CHECKING:
    from devtools.filesystem.models.json.base import JsonCompatible, JsonScalar


@pytest.mark.parametrize("value", ["text", 1, 1.5, True, None])
def test_freeze_and_thaw_preserve_json_scalars(value: JsonScalar) -> None:
    """JSON scalar values pass through conversion unchanged."""
    assert thaw_json(freeze_json(value)) == value


def test_freeze_and_thaw_recursively_convert_nested_json_structures() -> None:
    """Objects become mappings, arrays become tuples, and thawing round-trips."""
    source: dict[str, JsonCompatible] = {"items": [1, {"nested": [True, None]}]}
    frozen = freeze_json(source)

    assert isinstance(frozen, Mapping)
    assert isinstance(frozen["items"], tuple)
    nested = frozen["items"][1]
    assert isinstance(nested, Mapping)
    assert isinstance(nested["nested"], tuple)
    assert thaw_json(frozen) == source

    with pytest.raises(TypeError):
        cast("dict[str, object]", frozen)["new"] = "value"

    with pytest.raises(AttributeError):
        frozen["items"].append("value")  # type: ignore[attr-defined]
