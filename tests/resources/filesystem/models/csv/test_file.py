# Copyright (c) 2026
"""Tests for immutable structured CSV files."""

from __future__ import annotations

from typing import TYPE_CHECKING

import pytest

from devtools.core.conversion import ConversionError
from devtools.core.paths import ResolvedPath
from devtools.resources.filesystem import CsvDialect, CsvFile, CsvRow

if TYPE_CHECKING:
    from pathlib import Path


def _file(tmp_path: Path) -> CsvFile:
    """Create a representative structured CSV model."""
    headers = ("id", "status")
    return CsvFile(
        ResolvedPath(tmp_path / "reports.csv"),
        "id,status\nreport-1,passed\nreport-2,failed\n",
        headers=headers,
        rows=(
            CsvRow(headers, ("report-1", "passed")),
            CsvRow(headers, ("report-2", "failed")),
        ),
        dialect=CsvDialect(),
    )


def test_file_is_a_sequence_with_columns_and_structured_search(tmp_path: Path) -> None:
    """CSV files provide ordered rows, columns, and non-coercive row search."""
    file = _file(tmp_path)
    expected_rows = 2

    assert len(file) == expected_rows
    assert file[0]["id"] == "report-1"
    assert file[-1]["status"] == "failed"
    assert file[:] == file.rows
    assert tuple(file) == file.rows
    assert file.column("status") == ("passed", "failed")
    assert file.find(lambda row: row["status"] == "failed") == file[1]
    assert file.find(lambda row: row["status"] == "missing") is None
    assert file.find_all(lambda row: row["status"] == "failed") == (file[1],)
    assert file.find_by("id", "report-2") == file[1]

    with pytest.raises(KeyError):
        file.column("missing")

    with pytest.raises(KeyError):
        file.find_by("missing", "value")


def test_file_transformations_preserve_source_provenance_and_original(
    tmp_path: Path,
) -> None:
    """Row changes are immutable structured state rather than source rewrites."""
    file = _file(tmp_path)
    appended = file.appended(CsvRow(file.headers, ("report-3", "passed")))
    extended = appended.extended((CsvRow(file.headers, ("report-4", "failed")),))
    replaced = extended.with_row(0, CsvRow(file.headers, ("report-1", "fixed")))
    removed = replaced.without_row(-1)
    original_rows = 2
    remaining_rows = 3

    assert len(file) == original_rows
    assert file.content == appended.content == removed.content
    assert appended[-1]["id"] == "report-3"
    assert extended[-1]["id"] == "report-4"
    assert replaced[0]["status"] == "fixed"
    assert len(removed) == remaining_rows

    wrong = CsvRow(("other",), ("value",))
    with pytest.raises(ValueError, match="match"):
        file.appended(wrong)

    with pytest.raises(IndexError):
        file.with_row(9, file[0])

    with pytest.raises(IndexError):
        file.without_row(9)


@pytest.mark.parametrize(
    ("headers", "rows", "match"),
    [
        ((), (), "header"),
        (("",), (), "blank"),
        (("id", "id"), (), "unique"),
        (("id",), (CsvRow(("other",), ("value",)),), "match"),
    ],
)
def test_file_rejects_ambiguous_headers_and_incompatible_rows(
    tmp_path: Path,
    headers: tuple[str, ...],
    rows: tuple[CsvRow, ...],
    match: str,
) -> None:
    """Header identity is required for deterministic mapping-style access."""
    with pytest.raises(ValueError, match=match):
        CsvFile(
            ResolvedPath(tmp_path / "invalid.csv"),
            "",
            headers=headers,
            rows=rows,
        )


def test_file_converts_rows_in_order_with_indexed_failures(tmp_path: Path) -> None:
    """Batch row conversion is ordered, fail-fast, and retains row position."""
    file = _file(tmp_path)
    calls: list[str] = []

    assert file.convert_rows(lambda row: row["id"]) == ("report-1", "report-2")

    def fail_on_second(row: CsvRow) -> str:
        identifier = row["id"]
        calls.append(identifier)
        if identifier == "report-2":
            message = "invalid report"
            raise ValueError(message)

        return identifier

    with pytest.raises(ConversionError) as raised:
        file.convert_rows(fail_on_second)

    assert calls == ["report-1", "report-2"]
    assert raised.value.index == 1
    assert raised.value.source_type is CsvRow
    assert isinstance(raised.value.__cause__, ConversionError)
