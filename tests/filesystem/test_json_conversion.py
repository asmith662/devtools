# Copyright (c) 2026
"""Tests for explicit conversion adapters on JSON models."""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass
from typing import TYPE_CHECKING

import pytest

from devtools.conversion import ConversionError
from devtools.filesystem import JsonCodec, JsonListFile, JsonObjectFile, JsonScalarFile
from devtools.paths import ResolvedPath

if TYPE_CHECKING:
    from pathlib import Path

    from devtools.filesystem.models.json.base import JsonMutableValue


@dataclass(frozen=True)
class _Report:
    """Represent a test conversion target."""

    name: JsonMutableValue
    tags: JsonMutableValue


def test_object_conversion_receives_thawed_mutable_data_and_preserves_source(
    tmp_path: Path,
) -> None:
    """Object conversion exposes conventional data without thawing model storage."""
    file = _parse_object(
        tmp_path,
        '{"name":"report","tags":["stable"],"meta":{"active":true}}',
    )

    def build(value: dict[str, JsonMutableValue]) -> _Report:
        tags = value["tags"]
        metadata = value["meta"]
        assert isinstance(tags, list)
        assert isinstance(metadata, dict)
        tags.append("converted")
        return _Report(name=value["name"], tags=tags)

    report = file.convert(build)

    assert report == _Report("report", ["stable", "converted"])
    assert isinstance(file.value, Mapping)
    assert file.value["tags"] == ("stable",)
    assert file.value["meta"] == {"active": True}


def test_object_conversion_normalizes_converter_errors(tmp_path: Path) -> None:
    """Object conversion retains generic conversion failure semantics."""
    file = _parse_object(tmp_path, '{"name":"report"}')

    def fail(_value: dict[str, JsonMutableValue]) -> None:
        message = "invalid"
        raise ValueError(message)

    with pytest.raises(ConversionError) as raised:
        file.convert(fail)

    assert raised.value.index is None
    assert raised.value.source_type is dict
    assert isinstance(raised.value.__cause__, ValueError)


@pytest.mark.parametrize(
    ("source", "expected"),
    [
        ('"text"', "str"),
        ("1", "int"),
        ("1.5", "float"),
        ("true", "bool"),
        ("null", "NoneType"),
    ],
)
def test_scalar_conversion_supports_every_json_scalar(
    tmp_path: Path,
    source: str,
    expected: str,
) -> None:
    """Scalar conversion passes each ordinary JSON scalar unchanged."""
    file = JsonCodec().parse(ResolvedPath(tmp_path / "scalar.json"), source)

    assert isinstance(file, JsonScalarFile)
    assert file.convert(lambda value: type(value).__name__) == expected


def test_list_conversion_thaws_all_json_item_shapes_in_order(tmp_path: Path) -> None:
    """List conversion supports object, array, scalar, and null entries."""
    file = JsonCodec().parse(
        ResolvedPath(tmp_path / "items.json"),
        '[{"id":1},["nested"],"text",null]',
    )

    assert isinstance(file, JsonListFile)
    converted = file.convert_items(type)

    assert converted == (dict, list, str, type(None))
    assert file.value[0] == {"id": 1}
    assert file.value[1] == ("nested",)


def test_list_conversion_is_fail_fast_and_reports_array_index(tmp_path: Path) -> None:
    """List conversion preserves generic indexed failure semantics."""
    file = JsonCodec().parse(ResolvedPath(tmp_path / "items.json"), "[1, 2, 3]")
    calls: list[int] = []
    failing_value = 2

    assert isinstance(file, JsonListFile)

    def fail_on_second(value: object) -> int:
        assert isinstance(value, int)
        calls.append(value)
        if value == failing_value:
            message = "bad value"
            raise ValueError(message)

        return value

    with pytest.raises(ConversionError) as raised:
        file.convert_items(fail_on_second)

    assert calls == [1, 2]
    assert raised.value.index == 1
    assert raised.value.source_type is int
    assert isinstance(raised.value.__cause__, ConversionError)


def _parse_object(tmp_path: Path, source: str) -> JsonObjectFile:
    """Parse a source object into its concrete JSON model."""
    file = JsonCodec().parse(ResolvedPath(tmp_path / "report.json"), source)
    assert isinstance(file, JsonObjectFile)
    return file
