# Copyright (c) 2026
"""Tests for public CSV dialect values."""

from __future__ import annotations

from typing import TYPE_CHECKING

import pytest

from devtools.filesystem import CsvDialect, CsvQuoting

if TYPE_CHECKING:
    from collections.abc import Callable


def test_dialect_retains_immutable_default_and_explicit_policy() -> None:
    """Dialect values expose stable public CSV policy without stdlib integers."""
    dialect = CsvDialect(delimiter=";", quoting=CsvQuoting.ALL)

    assert dialect.delimiter == ";"
    assert dialect.quotechar == '"'
    assert dialect.lineterminator == "\n"
    assert dialect.quoting is CsvQuoting.ALL
    assert dialect == CsvDialect(delimiter=";", quoting=CsvQuoting.ALL)
    assert hash(dialect) == hash(CsvDialect(delimiter=";", quoting=CsvQuoting.ALL))

    with pytest.raises(AttributeError):
        dialect.delimiter = ","  # type: ignore[misc]


@pytest.mark.parametrize(
    ("factory", "match"),
    [
        (lambda: CsvDialect(delimiter="::"), "delimiter"),
        (lambda: CsvDialect(quotechar=""), "quote"),
        (lambda: CsvDialect(escapechar="##"), "escape"),
        (lambda: CsvDialect(lineterminator=""), "terminator"),
    ],
)
def test_dialect_rejects_invalid_csv_control_characters(
    factory: Callable[[], CsvDialect],
    match: str,
) -> None:
    """CSV controls require explicit, non-empty single-character values."""
    with pytest.raises(ValueError, match=match):
        factory()
