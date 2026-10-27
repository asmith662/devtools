# Copyright (c) 2026
# ruff: noqa: D103 -- literal scope/materialization tests
"""Actual bounded source admission and live correspondence, no application."""

from __future__ import annotations

import asyncio
from dataclasses import replace
from pathlib import Path

import pytest

from devtools.context import Repository, RepositoryResourceAddress
from devtools.context.planning.source import SourceRangeDisclosureOption
from devtools.context.repository.snapshot import RepositorySnapshotId
from devtools.core.paths import resolve_path
from devtools.tools import ToolRunner, source
from devtools.tools.errors import ToolInputError
from devtools.tools.source import ScopedSourceTool
from tests.tools.source_fixture import TEXT, source_fixture


@pytest.mark.parametrize("kind", [0, 1, 2])
def test_actual_file_symbol_window_materialization(tmp_path: Path, kind: int) -> None:
    scope, index = source_fixture(tmp_path)
    unit = index.views[kind].units[-1]
    option = SourceRangeDisclosureOption("inspect", unit, unit.start, unit.end, 4096)
    result = asyncio.run(ToolRunner().execute(ScopedSourceTool(scope), option))
    assert result.items[0].text == TEXT[unit.start : unit.end]
    assert result.items[0].content_identities == (unit.resource.content_identity,)
    assert result.items[0].native_provenance is option
    assert option.span == (unit.start, unit.end)


@pytest.mark.parametrize("fault", ["repository", "snapshot", "resource", "budget"])
def test_foreign_source_or_disclosure_refused(tmp_path: Path, fault: str) -> None:
    scope, index = source_fixture(tmp_path)
    unit = index.views[0].units[0]
    if fault == "repository":
        unit = replace(unit, repository_id=Repository.new().id)
    elif fault == "snapshot":
        unit = replace(unit, snapshot_id=RepositorySnapshotId("f" * 64))
    elif fault == "resource":
        unit = replace(
            unit,
            resource=replace(
                unit.resource,
                address=RepositoryResourceAddress("foreign.py"),
            ),
        )
    option = SourceRangeDisclosureOption(
        "inspect",
        unit,
        0,
        unit.end,
        4097 if fault == "budget" else 4096,
    )
    with pytest.raises(ToolInputError, match="scope"):
        asyncio.run(ToolRunner().execute(ScopedSourceTool(scope), option))


def test_stale_source_and_unrelated_file(tmp_path: Path) -> None:
    scope, index = source_fixture(tmp_path)
    (tmp_path / "unrelated.txt").write_text("irrelevant", encoding="utf-8")
    scope.check_current()
    (tmp_path / "module.py").write_text("changed", encoding="utf-8")
    option = SourceRangeDisclosureOption(
        "inspect",
        index.views[0].units[0],
        0,
        len(TEXT),
        4096,
    )
    with pytest.raises(ToolInputError, match="current"):
        asyncio.run(ToolRunner().execute(ScopedSourceTool(scope), option))


@pytest.mark.parametrize("alias", ["is_symlink", "is_junction"])
def test_alias_admission_is_conservative(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    alias: str,
) -> None:
    scope, _ = source_fixture(tmp_path)
    monkeypatch.setattr(Path, alias, lambda _self: True)
    with pytest.raises(ToolInputError, match="aliases"):
        scope.check_current()


def test_invalid_disclosure_bound(tmp_path: Path) -> None:
    scope, _ = source_fixture(tmp_path)
    with pytest.raises(ValueError, match="positive"):
        ScopedSourceTool(scope, maximum_bytes=0)


def test_changed_root_identity_refused(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    scope, _ = source_fixture(tmp_path)
    monkeypatch.setattr(
        source,
        "resolve_path",
        lambda _path: resolve_path(tmp_path.parent),
    )
    with pytest.raises(ToolInputError, match="root aliases"):
        scope.check_current()
