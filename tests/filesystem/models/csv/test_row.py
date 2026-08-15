# Copyright (c) 2026
"""Tests for immutable header-addressable CSV rows."""

from __future__ import annotations

from typing import cast

import pytest

from devtools.conversion import ConversionError
from devtools.filesystem import CsvRow


def test_row_supports_positional_and_keyed_read_only_access() -> None:
    """Rows preserve positional values and unambiguous header lookup."""
    row = CsvRow(("id", "status"), ("report-17", "failed"))
    expected_length = 2

    assert row[0] == "report-17"
    assert row[-1] == "failed"
    assert row[:] == ("report-17", "failed")
    assert row["status"] == "failed"
    assert len(row) == expected_length
    assert tuple(row) == ("report-17", "failed")
    assert "id" in row
    assert "failed" not in row
    assert row.get("missing") is None
    assert row.get("missing", "default") == "default"
    assert row.keys() == ("id", "status")
    assert row.values() == ("report-17", "failed")
    assert row.items() == (("id", "report-17"), ("status", "failed"))
    assert row.as_dict() == {"id": "report-17", "status": "failed"}

    with pytest.raises(KeyError):
        row["missing"]

    with pytest.raises(AttributeError):
        row.cells = ("changed", "failed")  # type: ignore[misc]


def test_row_rejects_mismatched_header_and_value_widths() -> None:
    """A row must remain aligned with its positional schema."""
    with pytest.raises(ValueError, match="match"):
        CsvRow(("id",), ("one", "two"))

    with pytest.raises(ValueError, match="strings"):
        CsvRow(("id",), cast("tuple[str, ...]", (1,)))


def test_row_conversion_delegates_to_the_explicit_callable() -> None:
    """Row conversion supplies the immutable row rather than an implicit mapping."""
    row = CsvRow(("id", "status"), ("report-17", "failed"))

    assert row.convert(lambda value: value.as_dict()) == {
        "id": "report-17",
        "status": "failed",
    }

    def fail(_value: CsvRow) -> None:
        message = "invalid row"
        raise ValueError(message)

    with pytest.raises(ConversionError) as raised:
        row.convert(fail)

    assert raised.value.index is None
    assert raised.value.source_type is CsvRow
    assert isinstance(raised.value.__cause__, ValueError)
