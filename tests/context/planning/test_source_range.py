# Copyright (c) 2026
# ruff: noqa: D103 -- exact independently specified range boundaries
"""Context range representation, distinct from live filesystem authority."""

from __future__ import annotations

from dataclasses import replace
from typing import TYPE_CHECKING

import pytest

from devtools.context import Repository
from devtools.context.planning.source import (
    SourceRangeDisclosureOption,
    materialize_source_range,
)
from tests.tools.source_fixture import source_fixture

if TYPE_CHECKING:
    from pathlib import Path


def test_literal_utf8_partial_disclosure_and_budget_identity(tmp_path: Path) -> None:
    scope, index = source_fixture(tmp_path, "A\u03c0\u03c0Z\r\n")
    unit = index.views[0].units[0]
    option = SourceRangeDisclosureOption("inspect", unit, 1, 4, 3)
    result = materialize_source_range(scope.snapshot, option)
    assert result.items[0].text == "\u03c0"
    assert option.span == (1, 2)
    assert option.truncated is True
    assert result.plan.snapshot_id == scope.snapshot.id
    other = replace(option, maximum_bytes=5)
    assert other.text == "\u03c0\u03c0Z"
    assert other.truncated is False
    assert option.identity != other.identity


@pytest.mark.parametrize(
    ("start", "end", "budget"),
    [
        (0, 0, 4),
        (-1, 2, 4),
        (0, 999, 4),
        (2, 1, 4),
        (0, 1, 0),
        (True, 2, 4),
        (0, False, 4),
        (0, 1, True),
    ],
)
def test_invalid_ranges_and_bounds(
    tmp_path: Path,
    start: int,
    end: int,
    budget: int,
) -> None:
    _, index = source_fixture(tmp_path)
    with pytest.raises(ValueError, match="invalid"):
        SourceRangeDisclosureOption(
            "inspect",
            index.views[0].units[0],
            start,
            end,
            budget,
        )


def test_empty_file_and_foreign_snapshot(tmp_path: Path) -> None:
    scope, index = source_fixture(tmp_path, "")
    option = SourceRangeDisclosureOption("empty", index.views[0].units[0], 0, 0, 4)
    assert materialize_source_range(scope.snapshot, option).items[0].text == ""
    assert option.truncated is False
    with pytest.raises(ValueError, match=r"snapshot|repository"):
        materialize_source_range(
            replace(scope.snapshot, repository_id=Repository.new().id),
            option,
        )
