# Copyright (c) 2026
"""Immutable header-based CSV filesystem models."""

from __future__ import annotations

from dataclasses import dataclass, field, replace
from enum import StrEnum
from typing import TYPE_CHECKING, overload

from devtools.conversion import convert, convert_all
from devtools.filesystem.models.base import FileFormat
from devtools.filesystem.models.text import TextFile

if TYPE_CHECKING:
    from collections.abc import Callable, Iterable, Iterator

    from devtools.conversion import Converter


class CsvQuoting(StrEnum):
    """Represent supported CSV quoting policies."""

    MINIMAL = "minimal"
    ALL = "all"
    NONNUMERIC = "nonnumeric"
    NONE = "none"


@dataclass(frozen=True, slots=True)
class CsvDialect:
    """Represent immutable CSV parsing and serialization policy.

    :ivar delimiter: Single-character field delimiter.
    :ivar quotechar: Single-character quote marker.
    :ivar escapechar: Optional single-character escape marker.
    :ivar doublequote: Whether doubled quote markers escape quotes.
    :ivar skipinitialspace: Whether parsing skips spaces after delimiters.
    :ivar lineterminator: Serialized record terminator.
    :ivar quoting: Public quoting policy.
    """

    delimiter: str = ","
    quotechar: str = '"'
    escapechar: str | None = None
    doublequote: bool = True
    skipinitialspace: bool = False
    lineterminator: str = "\n"
    quoting: CsvQuoting = CsvQuoting.MINIMAL

    def __post_init__(self) -> None:
        """Validate CSV dialect invariants."""
        if len(self.delimiter) != 1:
            msg = "CSV delimiter must be exactly one character."
            raise ValueError(msg)

        if len(self.quotechar) != 1:
            msg = "CSV quote character must be exactly one character."
            raise ValueError(msg)

        if self.escapechar is not None and len(self.escapechar) != 1:
            msg = "CSV escape character must be exactly one character."
            raise ValueError(msg)

        if not self.lineterminator:
            msg = "CSV line terminator cannot be empty."
            raise ValueError(msg)


@dataclass(frozen=True, slots=True)
class CsvRow:
    """Represent one immutable header-addressable CSV row.

    :ivar headers: Column names in positional order.
    :ivar cells: Cell values in positional order.
    """

    headers: tuple[str, ...]
    cells: tuple[str, ...]

    def __post_init__(self) -> None:
        """Freeze storage and validate row dimensions."""
        object.__setattr__(self, "headers", tuple(self.headers))
        object.__setattr__(self, "cells", tuple(self.cells))

        if len(self.headers) != len(self.cells):
            msg = "CSV row values must match the number of headers."
            raise ValueError(msg)

        if any(not isinstance(value, str) for value in self.cells):
            msg = "CSV row values must be strings."
            raise ValueError(msg)

    @overload
    def __getitem__(self, key: int) -> str: ...

    @overload
    def __getitem__(self, key: slice) -> tuple[str, ...]: ...

    @overload
    def __getitem__(self, key: str) -> str: ...

    def __getitem__(self, key: int | slice | str) -> str | tuple[str, ...]:
        """Return a cell by position, slice, or header name.

        :param key: Integer position, slice, or header name.
        :returns: Cell value or immutable cell slice.
        :raises KeyError: If a header name is unknown.
        """
        if isinstance(key, str):
            try:
                index = self.headers.index(key)
            except ValueError as error:
                raise KeyError(key) from error

            return self.cells[index]

        return self.cells[key]

    def __iter__(self) -> Iterator[str]:
        """Iterate over row values in positional order."""
        return iter(self.cells)

    def __len__(self) -> int:
        """Return the number of cells in the row."""
        return len(self.cells)

    def __contains__(self, key: object) -> bool:
        """Return whether a header name is present in the row."""
        return isinstance(key, str) and key in self.headers

    def get(self, key: str, default: str | None = None) -> str | None:
        """Return a named value or an explicit default.

        :param key: Header name.
        :param default: Value returned when the header is absent.
        :returns: Named cell or default.
        """
        try:
            return self[key]
        except KeyError:
            return default

    def keys(self) -> tuple[str, ...]:
        """Return column names in positional order."""
        return self.headers

    def values(self) -> tuple[str, ...]:
        """Return cell values in positional order."""
        return self.cells

    def items(self) -> tuple[tuple[str, str], ...]:
        """Return immutable header/value pairs in positional order."""
        return tuple(zip(self.headers, self.cells, strict=True))

    def as_dict(self) -> dict[str, str]:
        """Return an ordinary mapping copy of the row."""
        return dict(self.items())

    def convert[TargetT](self, converter: Converter[CsvRow, TargetT]) -> TargetT:
        """Convert this row through an explicit callable.

        :param converter: Callable receiving this immutable row.
        :returns: Converter result.
        :raises ConversionError: If the converter raises an ordinary exception.
        """
        return convert(self, converter)


@dataclass(frozen=True, slots=True)
class CsvFile(TextFile):
    """Represent immutable header-based CSV source and structured rows.

    ``content`` is original decoded source provenance. ``headers`` and ``rows``
    are the current structured state; ``CsvCodec`` serializes that state after
    immutable transformations.

    :ivar headers: Unique, non-blank CSV headers.
    :ivar rows: Immutable rows sharing the file headers.
    :ivar dialect: CSV parsing and serialization policy.
    """

    headers: tuple[str, ...] = field(kw_only=True)
    rows: tuple[CsvRow, ...] = field(kw_only=True)
    dialect: CsvDialect = field(default_factory=CsvDialect, kw_only=True)

    def __post_init__(self) -> None:
        """Validate text metadata and freeze structured CSV state."""
        super().__post_init__()
        object.__setattr__(self, "headers", tuple(self.headers))
        object.__setattr__(self, "rows", tuple(self.rows))

        if not self.headers:
            msg = "CSV files require a header row."
            raise ValueError(msg)

        if any(not header.strip() for header in self.headers):
            msg = "CSV headers cannot be blank."
            raise ValueError(msg)

        if len(set(self.headers)) != len(self.headers):
            msg = "CSV headers must be unique."
            raise ValueError(msg)

        for row in self.rows:
            if row.headers != self.headers:
                msg = "CSV row headers must match the file headers."
                raise ValueError(msg)

    @property
    def format(self) -> FileFormat:
        """Return the CSV file format."""
        return FileFormat.CSV

    @overload
    def __getitem__(self, index: int) -> CsvRow: ...

    @overload
    def __getitem__(self, index: slice) -> tuple[CsvRow, ...]: ...

    def __getitem__(self, index: int | slice) -> CsvRow | tuple[CsvRow, ...]:
        """Return a row or immutable row slice."""
        return self.rows[index]

    def __iter__(self) -> Iterator[CsvRow]:
        """Iterate over structured rows."""
        return iter(self.rows)

    def __len__(self) -> int:
        """Return the number of data rows."""
        return len(self.rows)

    def column(self, name: str) -> tuple[str, ...]:
        """Return values for a named column in row order.

        :param name: Header name.
        :returns: Immutable values in data-row order.
        :raises KeyError: If the header is unknown.
        """
        if name not in self.headers:
            raise KeyError(name)

        return tuple(row[name] for row in self.rows)

    def find(self, predicate: Callable[[CsvRow], bool]) -> CsvRow | None:
        """Return the first row satisfying a predicate.

        :param predicate: Predicate receiving one structured row.
        :returns: First matching row or ``None``.
        """
        for row in self.rows:
            if predicate(row):
                return row

        return None

    def find_all(self, predicate: Callable[[CsvRow], bool]) -> tuple[CsvRow, ...]:
        """Return all rows satisfying a predicate."""
        return tuple(row for row in self.rows if predicate(row))

    def find_by(self, column: str, value: str) -> CsvRow | None:
        """Return the first row with a matching named cell."""
        if column not in self.headers:
            raise KeyError(column)

        return self.find(lambda row: row[column] == value)

    def convert_rows[TargetT](
        self,
        converter: Converter[CsvRow, TargetT],
    ) -> tuple[TargetT, ...]:
        """Convert structured rows through an explicit callable.

        :param converter: Callable receiving each immutable row.
        :returns: Immutable converted results in row order.
        :raises ConversionError: If a row conversion fails.
        """
        return convert_all(self.rows, converter)

    def appended(self, row: CsvRow) -> CsvFile:
        """Return a copy with an appended compatible row."""
        self._validate_row_headers(row)
        return replace(self, rows=(*self.rows, row))

    def extended(self, rows: Iterable[CsvRow]) -> CsvFile:
        """Return a copy with additional compatible rows."""
        additions = tuple(rows)

        for row in additions:
            self._validate_row_headers(row)

        return replace(self, rows=(*self.rows, *additions))

    def with_row(self, index: int, row: CsvRow) -> CsvFile:
        """Return a copy with one compatible row replaced."""
        self._validate_row_headers(row)
        updated = list(self.rows)
        updated[index] = row
        return replace(self, rows=tuple(updated))

    def without_row(self, index: int) -> CsvFile:
        """Return a copy without one row."""
        updated = list(self.rows)
        del updated[index]
        return replace(self, rows=tuple(updated))

    def _validate_row_headers(self, row: CsvRow) -> None:
        """Validate that a row belongs to this file schema."""
        if row.headers != self.headers:
            msg = "CSV row headers must match the file headers."
            raise ValueError(msg)
