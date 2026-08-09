# Copyright (c) 2026
"""Tests for immutable JSON file models."""

from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING

import pytest

from devtools.filesystem import JsonListFile, JsonObjectFile, JsonScalarFile
from devtools.filesystem.models.json import freeze_json
from devtools.paths import ResolvedPath

if TYPE_CHECKING:
    from pathlib import Path

    from devtools.filesystem.models.json.base import (
        JsonCompatible,
        JsonScalar,
        JsonValue,
    )


def test_json_object_behaves_as_a_mapping_and_preserves_source_search(
    tmp_path: Path,
) -> None:
    """JSON objects expose mapping traversal, structured lookup, and source regex."""
    value = _object_value({"name": "Ada", "items": [1, 2], "active": True})
    file = JsonObjectFile(ResolvedPath(tmp_path), '{"name": "Ada"}', value=value)
    expected_member_count = len(("name", "items", "active"))

    assert file["name"] == "Ada"
    assert file.get("missing") is None
    assert tuple(file) == ("name", "items", "active")
    assert len(file) == expected_member_count
    assert "name" in file
    assert tuple(file.keys()) == ("name", "items", "active")
    assert next(iter(file.values())) == "Ada"
    assert next(iter(file.items())) == ("name", "Ada")
    assert file.find(lambda key, _value: key == "items") == ("items", (1, 2))
    assert file.find(lambda _key, _value: False) is None
    assert file.find_all(lambda _key, item: isinstance(item, bool)) == (
        ("active", True),
    )
    assert file.search_regex("Ada") is not None
    assert file.find_all_regex("name")


def test_json_object_transformations_freeze_insertions_and_preserve_original(
    tmp_path: Path,
) -> None:
    """Object transformations return new values without exposing mutability."""
    original = JsonObjectFile(
        ResolvedPath(tmp_path),
        "{}",
        value=_object_value({"stable": 1}),
    )
    updated = original.with_item("nested", {"values": [1]})
    merged = updated.with_items({"more": [2], "stable": 3})
    removed = merged.without("stable")
    expected_replacement = len(("one", "two", "three"))

    assert original == JsonObjectFile(
        ResolvedPath(tmp_path),
        "{}",
        value=_object_value({"stable": 1}),
    )
    assert isinstance(updated["nested"], Mapping)
    assert updated["nested"]["values"] == (1,)
    assert merged["more"] == (2,)
    assert merged["stable"] == expected_replacement
    assert "stable" not in removed

    with pytest.raises(KeyError):
        original.without("missing")


def test_json_list_behaves_as_a_sequence_and_preserves_source_search(
    tmp_path: Path,
) -> None:
    """JSON arrays retain natural sequence behavior and structured traversal."""
    file = JsonListFile(
        ResolvedPath(tmp_path),
        "[1, 2, 3]",
        value=_list_value(({"id": 1}, 2, {"id": 3})),
    )
    matching_number = len(("one", "two"))
    target_identifier = len(("one", "two", "three"))
    expected_item_count = len(("one", "two", "three"))

    assert file[0] == {"id": 1}
    assert file[-1] == {"id": 3}
    assert file[1:] == (2, {"id": 3})
    assert tuple(file) == ({"id": 1}, 2, {"id": 3})
    assert matching_number in file
    assert len(file) == expected_item_count
    assert file.find(lambda item: item == matching_number) == matching_number
    assert file.find(lambda _item: False) is None
    assert file.find_all(lambda item: isinstance(item, Mapping)) == (
        {"id": 1},
        {"id": 3},
    )
    assert file.find_by("id", target_identifier) == {"id": target_identifier}
    assert file.find_by("id", matching_number) is None
    assert file.search_regex("2") is not None


def test_json_list_transformations_are_immutable_and_freeze_insertions(
    tmp_path: Path,
) -> None:
    """Array transformations return tuples and preserve original contents."""
    original = JsonListFile(
        ResolvedPath(tmp_path),
        "[1]",
        value=_list_value((1,)),
    )
    nested_value: JsonCompatible = {"nested": [2]}
    appended = original.appended(nested_value)
    extended = appended.extended(([3], 4))
    replaced = extended.with_item(-1, {"value": 5})
    removed = replaced.without_index(0)

    assert tuple(original) == (1,)
    assert appended[1] == {"nested": (2,)}
    assert extended[2] == (3,)
    assert replaced[-1] == {"value": 5}
    assert tuple(removed) == ({"nested": (2,)}, (3,), {"value": 5})

    with pytest.raises(IndexError):
        original.with_item(3, "missing")

    with pytest.raises(IndexError):
        original.without_index(3)


@pytest.mark.parametrize("value", ["text", 1, 1.5, True, None])
def test_json_scalar_files_represent_every_legal_scalar_root(
    tmp_path: Path,
    value: JsonScalar,
) -> None:
    """Scalar JSON roots remain simple non-iterable values with source search."""
    file = JsonScalarFile(ResolvedPath(tmp_path), str(value), value=value)

    assert file.value == value
    assert file.search_regex(str(value)) is not None


def test_json_models_reject_wrong_root_value_shapes(tmp_path: Path) -> None:
    """Concrete JSON models require object, array, or scalar values respectively."""
    path = ResolvedPath(tmp_path)

    with pytest.raises(TypeError, match="object"):
        JsonObjectFile(path, "[]", value=_list_value(()))  # type: ignore[arg-type]

    with pytest.raises(TypeError, match="array"):
        JsonListFile(path, "{}", value=_object_value({}))  # type: ignore[arg-type]


def _object_value(value: Mapping[str, JsonCompatible]) -> Mapping[str, JsonValue]:
    """Freeze a test object with a mapping-aware static type."""
    frozen = freeze_json(value)
    assert isinstance(frozen, Mapping)
    return frozen


def _list_value(value: tuple[JsonCompatible, ...]) -> tuple[JsonValue, ...]:
    """Freeze a test array with a tuple-aware static type."""
    frozen = freeze_json(value)
    assert isinstance(frozen, tuple)
    return frozen
