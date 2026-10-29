# Copyright (c) 2026
# ruff: noqa: D103 -- literal source/capacity expectations
"""Navigation reuses the actual scoped index; metadata is never a disclosure."""

from __future__ import annotations

import asyncio
import json
from dataclasses import replace
from typing import TYPE_CHECKING

import pytest

from devtools.agents.coding.navigation import (
    navigation_feedback,
    navigation_request,
    unit_read_request,
)
from devtools.context import RepositoryResourceAddress
from devtools.context.planning.materialization import ContextDisclosure
from devtools.context.planning.source import SourceRangeDisclosureOption
from devtools.tools import ToolInputError, ToolRunner
from devtools.tools.source import (
    ScopedSourceNavigationTool,
    SourceNavigationRequest,
)
from tests.tools.source_fixture import TEXT, source_fixture
from tests.tools.test_source_reads import read_tool

if TYPE_CHECKING:
    from pathlib import Path


def test_real_symbol_outline_search_and_exact_read(tmp_path: Path) -> None:
    scope, index = source_fixture(tmp_path)
    tool = ScopedSourceNavigationTool(scope, index, maximum_results=1)
    selected = asyncio.run(ToolRunner().execute(tool, SourceNavigationRequest()))
    assert len(selected) == 1
    unit = selected[0]
    assert unit.qualified_name == "value"
    assert unit.text == "def value():\r\n    return 7"
    assert unit.start == len("# \u03c0 prefix\r\n")
    assert unit.end == TEXT.index("\r\n# tail")
    result = navigation_feedback(
        selected,
        index,
        offset=0,
        maximum_bytes=4096,
        page_size=1,
    )
    assert result["source_acquired"] is False
    assert result["next_offset"] == 1
    assert "return 7" not in json.dumps(result)
    searched = asyncio.run(
        ToolRunner().execute(
            tool,
            SourceNavigationRequest("value", RepositoryResourceAddress("module.py")),
        ),
    )
    assert searched == selected
    assert (
        asyncio.run(ToolRunner().execute(tool, SourceNavigationRequest(offset=1))) == ()
    )
    request = unit_read_request(
        index,
        {"unit_id": str(unit.id), "snapshot_id": str(index.snapshot.id)},
        purpose="inspect",
        maximum_bytes=4096,
    )
    materialized = asyncio.run(ToolRunner().execute(read_tool(scope), request))
    assert isinstance(materialized, ContextDisclosure)
    assert materialized.items[0].text == "def value():\r\n    return 7"
    assert isinstance(
        materialized.items[0].native_provenance,
        SourceRangeDisclosureOption,
    )
    assert materialized.items[0].native_provenance.span == (unit.start, unit.end)


@pytest.mark.parametrize("mode", ["file", "window", "mixed"])
def test_available_views_and_query_paths(tmp_path: Path, mode: str) -> None:
    scope, index = source_fixture(tmp_path)
    tool = ScopedSourceNavigationTool(scope, index)
    selection = navigation_request({"mode": mode})
    units = asyncio.run(ToolRunner().execute(tool, selection))
    assert units
    assert all(u.resource.address.value == "module.py" for u in units)
    assert len({u.id for u in units}) == len(units)
    result = asyncio.run(ToolRunner().execute(tool, replace(selection, query="value")))
    assert result
    assert (
        asyncio.run(
            ToolRunner().execute(tool, replace(selection, query="zzzzunmatched")),
        )
        == ()
    )


@pytest.mark.parametrize(
    "values",
    [
        {"mode": "foreign"},
        {"query": 1},
        {"query": "x" * 257},
        {"offset": True},
        {"offset": -1},
        {"offset": 10000},
        {"path": "private.py"},
    ],
)
def test_invalid_or_foreign_navigation_refused_before_entry(
    tmp_path: Path,
    values: dict[str, object],
) -> None:
    scope, index = source_fixture(tmp_path)
    tool = ScopedSourceNavigationTool(scope, index)
    with pytest.raises(ToolInputError, match="index or bounds"):
        asyncio.run(ToolRunner().execute(tool, navigation_request(values)))


@pytest.mark.parametrize("fault", ["stale", "foreign", "limit"])
def test_scope_configuration_and_currentness(tmp_path: Path, fault: str) -> None:
    scope, index = source_fixture(tmp_path)
    if fault == "limit":
        with pytest.raises(ValueError, match="positive"):
            ScopedSourceNavigationTool(scope, index, maximum_results=0)
        return
    if fault == "stale":
        (tmp_path / "module.py").write_text("changed", encoding="utf-8")
    else:
        other = tmp_path / "other"
        other.mkdir()
        scope, _ = source_fixture(other, "different")
    with pytest.raises(ToolInputError):
        asyncio.run(
            ToolRunner().execute(
                ScopedSourceNavigationTool(scope, index),
                SourceNavigationRequest(),
            ),
        )


@pytest.mark.parametrize("fault", ["unit", "snapshot"])
def test_unit_binding_refuses_unknown_reference(tmp_path: Path, fault: str) -> None:
    _, index = source_fixture(tmp_path)
    values = {
        "unit_id": str(index.views[1].units[0].id),
        "snapshot_id": str(index.snapshot.id),
    }
    values[fault + "_id"] = "foreign"
    with pytest.raises(ValueError, match="foreign, stale"):
        unit_read_request(index, values, purpose="read", maximum_bytes=100)


def test_bounded_metadata_pages_and_partial_unit_disclosure(tmp_path: Path) -> None:
    scope, index = source_fixture(
        tmp_path,
        "class A:\r\n    def one(self):\r\n        return 1\r\n"
        "    def two(self):\r\n        return 2\r\n",
    )
    units = asyncio.run(
        ToolRunner().execute(
            ScopedSourceNavigationTool(scope, index),
            SourceNavigationRequest(),
        ),
    )
    assert [u.qualified_name for u in units] == ["A", "A.one", "A.two"]
    full = navigation_feedback(units, index, offset=0, maximum_bytes=4096)
    assert full["partial"] is False
    first = navigation_feedback(
        units[:1],
        index,
        offset=0,
        maximum_bytes=4096,
        page_size=1,
    )
    limit = len(json.dumps(first, ensure_ascii=False).encode())
    partial = navigation_feedback(units, index, offset=0, maximum_bytes=limit)
    assert partial == first
    assert units[1].parent_symbol_id == units[0].id
    for budget in (1, 300):
        with pytest.raises(ValueError, match="metadata cannot fit"):
            navigation_feedback(units, index, offset=0, maximum_bytes=budget)
    with pytest.raises(ValueError, match="metadata cannot fit"):
        navigation_feedback((), index, offset=0, maximum_bytes=1)
    assert navigation_feedback((), index, offset=0, maximum_bytes=4096)["units"] == []
    req = unit_read_request(
        index,
        {"unit_id": str(units[1].id), "snapshot_id": str(index.snapshot.id)},
        purpose="partial",
        maximum_bytes=8,
    )
    disclosure = asyncio.run(ToolRunner().execute(read_tool(scope), req))
    assert isinstance(disclosure, ContextDisclosure)
    assert disclosure.items[0].text == "def one("
    assert isinstance(
        disclosure.items[0].native_provenance,
        SourceRangeDisclosureOption,
    )
    assert disclosure.items[0].native_provenance.truncated
