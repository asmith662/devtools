# Copyright (c) 2026
# ruff: noqa: D103 -- literal independent range and effect assertions
"""Literal source requests retain coordinates and fail before disclosure."""

from __future__ import annotations

import asyncio
from dataclasses import replace
from typing import TYPE_CHECKING

import pytest

from devtools.context import RepositoryResourceAddress
from devtools.context.planning.materialization import ContextDisclosure
from devtools.context.planning.source import SourceRangeDisclosureOption
from devtools.tools import Tool, ToolInputError, ToolRunner
from devtools.tools.source import (
    ScopedSourceTool,
    SourceReadRefusal,
    SourceReadRequest,
    SourceScope,
    source_read_bounds,
)
from tests.tools.source_fixture import source_fixture

if TYPE_CHECKING:
    from pathlib import Path


def test_663_character_source_and_exact_corrected_interval(tmp_path: Path) -> None:
    scope, index = source_fixture(tmp_path, "#" + "x" * 662)
    request = SourceReadRequest("inspect", index.views[0].units[0], 439, 878, 4096)
    tool = read_tool(scope)
    rejected = asyncio.run(ToolRunner().execute(tool, request))
    assert isinstance(rejected, SourceReadRefusal)
    assert rejected.request is request
    assert source_read_bounds(request)["valid_range"] == [0, 663]
    accepted = asyncio.run(ToolRunner().execute(tool, replace(request, end=663)))
    assert isinstance(accepted, ContextDisclosure)
    assert accepted.items[0].text == "x" * 224
    assert isinstance(accepted.items[0].native_provenance, SourceRangeDisclosureOption)
    assert accepted.items[0].native_provenance.span == (439, 663)


@pytest.mark.parametrize(
    ("start", "end"),
    [(0, 0), (663, 663), (-1, 4), (4, 3), (0, 664)],
)
def test_invalid_literal_intervals_are_not_clamped(
    tmp_path: Path,
    start: int,
    end: int,
) -> None:
    scope, index = source_fixture(tmp_path, "#" + "x" * 662)
    request = SourceReadRequest("inspect", index.views[0].units[0], start, end, 4096)
    result = asyncio.run(ToolRunner().execute(read_tool(scope), request))
    assert isinstance(result, SourceReadRefusal)
    assert result.request.start == start
    assert result.request.end == end


@pytest.mark.parametrize(
    ("text", "limit", "expected"),
    [("", 4, ""), ("# π\r\n", 4, "# π"), ("# π\r\n", 3, "# ")],
)
def test_optional_end_utf8_and_crlf_are_truthful(
    tmp_path: Path,
    text: str,
    limit: int,
    expected: str,
) -> None:
    root = tmp_path / "source space π"
    root.mkdir()
    scope, index = source_fixture(root, text)
    request = SourceReadRequest("inspect", index.views[0].units[0], 0, None, limit)
    result = asyncio.run(ToolRunner().execute(read_tool(scope), request))
    assert isinstance(result, ContextDisclosure)
    assert result.items[0].text == expected
    option = result.items[0].native_provenance
    assert isinstance(option, SourceRangeDisclosureOption)
    assert option.span == (0, len(expected))
    assert option.truncated == (len(expected) < len(text))
    assert source_read_bounds(request)["source_length"] == len(text)
    assert source_read_bounds(request)["maximum_bytes"] == limit


@pytest.mark.parametrize("fault", ["stale", "foreign", "budget"])
def test_invalid_range_does_not_hide_scope_or_currentness_error(
    tmp_path: Path,
    fault: str,
) -> None:
    scope, index = source_fixture(tmp_path)
    unit = index.views[0].units[0]
    if fault == "stale":
        (tmp_path / "module.py").write_text("changed")
    if fault == "foreign":
        unit = replace(
            unit,
            resource=replace(
                unit.resource,
                address=RepositoryResourceAddress("private.py"),
            ),
        )
    request = SourceReadRequest(
        "inspect",
        unit,
        0,
        9999,
        4097 if fault == "budget" else 4096,
    )
    with pytest.raises(ToolInputError):
        asyncio.run(ToolRunner().execute(read_tool(scope), request))


@pytest.mark.parametrize(
    ("purpose", "limit"),
    [("", 1), ("inspect", 0), ("inspect", True)],
)
def test_host_configuration_error_is_not_model_refusal(
    tmp_path: Path,
    purpose: str,
    limit: int,
) -> None:
    _, index = source_fixture(tmp_path)
    with pytest.raises(ValueError, match="purpose"):
        SourceReadRequest(purpose, index.views[0].units[0], 0, None, limit)


def read_tool(
    scope: SourceScope,
) -> Tool[SourceReadRequest, ContextDisclosure | SourceReadRefusal]:
    return ScopedSourceTool(scope)
