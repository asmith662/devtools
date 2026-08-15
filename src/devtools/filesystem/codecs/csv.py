# Copyright (c) 2026
"""CSV representation codec."""

from __future__ import annotations

import csv
from io import StringIO
from typing import TYPE_CHECKING, Literal

from devtools.filesystem.errors import (
    FileFormatError,
    TextDecodingError,
    TextEncodingError,
)
from devtools.filesystem.models import CsvDialect, CsvFile, CsvQuoting, CsvRow

if TYPE_CHECKING:
    from devtools.paths import ResolvedPath

_DEFAULT_DIALECT = CsvDialect()
_QUOTE_MINIMAL: Literal[0] = 0
_QUOTE_ALL: Literal[1] = 1
_QUOTE_NONNUMERIC: Literal[2] = 2
_QUOTE_NONE: Literal[3] = 3


class CsvCodec:
    """Convert CSV source representations and immutable CSV file models."""

    def decode(
        self,
        path: ResolvedPath,
        content: bytes,
        *,
        encoding: str = "utf-8",
        dialect: CsvDialect = _DEFAULT_DIALECT,
    ) -> CsvFile:
        """Decode and parse CSV bytes without accessing the filesystem."""
        try:
            source = content.decode(encoding)
        except (LookupError, UnicodeDecodeError) as error:
            msg = f"Unable to decode CSV file using {encoding!r}: {path}."
            raise TextDecodingError(msg) from error

        return self.parse(
            path,
            source,
            encoding=encoding,
            byte_size=len(content),
            dialect=dialect,
        )

    def parse(
        self,
        path: ResolvedPath,
        content: str,
        *,
        encoding: str = "utf-8",
        byte_size: int | None = None,
        dialect: CsvDialect = _DEFAULT_DIALECT,
    ) -> CsvFile:
        """Parse header-based CSV source into an immutable file model."""
        source_size = byte_size

        if source_size is None:
            try:
                source_size = len(content.encode(encoding))
            except (LookupError, UnicodeEncodeError) as error:
                msg = f"Unable to encode CSV source using {encoding!r}."
                raise TextEncodingError(msg) from error

        try:
            reader = csv.reader(
                StringIO(content, newline=""),
                delimiter=dialect.delimiter,
                quotechar=dialect.quotechar,
                escapechar=dialect.escapechar,
                doublequote=dialect.doublequote,
                skipinitialspace=dialect.skipinitialspace,
                lineterminator=dialect.lineterminator,
                quoting=_to_csv_quoting(dialect.quoting),
                strict=True,
            )
            headers = tuple(next(reader))
        except StopIteration as error:
            msg = "CSV files require a header row."
            raise FileFormatError(msg) from error
        except (csv.Error, ValueError) as error:
            msg = f"Invalid CSV source: {error}."
            raise FileFormatError(msg) from error

        _validate_headers(headers)
        rows: list[CsvRow] = []

        try:
            rows.extend(CsvRow(headers, tuple(values)) for values in reader)
        except (csv.Error, ValueError) as error:
            msg = f"Invalid CSV row: {error}."
            raise FileFormatError(msg) from error

        return CsvFile(
            path,
            content,
            encoding=encoding,
            byte_size=source_size,
            headers=headers,
            rows=tuple(rows),
            dialect=dialect,
        )

    def serialize(self, file: CsvFile) -> str:
        """Serialize current structured CSV state using its dialect."""
        output = StringIO(newline="")

        try:
            writer = csv.writer(
                output,
                delimiter=file.dialect.delimiter,
                quotechar=file.dialect.quotechar,
                escapechar=file.dialect.escapechar,
                doublequote=file.dialect.doublequote,
                skipinitialspace=file.dialect.skipinitialspace,
                lineterminator=file.dialect.lineterminator,
                quoting=_to_csv_quoting(file.dialect.quoting),
            )
            writer.writerow(file.headers)
            writer.writerows(row.values() for row in file.rows)
        except csv.Error as error:
            msg = f"CSV model cannot be serialized: {error}."
            raise FileFormatError(msg) from error

        return output.getvalue()

    def encode(
        self,
        file: CsvFile,
        *,
        encoding: str | None = None,
    ) -> bytes:
        """Serialize and encode a CSV model without writing to disk."""
        target_encoding = file.encoding if encoding is None else encoding
        serialized = self.serialize(file)

        try:
            return serialized.encode(target_encoding)
        except (LookupError, UnicodeEncodeError) as error:
            msg = f"Unable to encode CSV using {target_encoding!r}."
            raise TextEncodingError(msg) from error


def _to_csv_quoting(quoting: CsvQuoting) -> Literal[0, 1, 2, 3]:
    """Map a public quoting value to the standard-library integer constant."""
    mapping: dict[CsvQuoting, Literal[0, 1, 2, 3]] = {
        CsvQuoting.MINIMAL: _QUOTE_MINIMAL,
        CsvQuoting.ALL: _QUOTE_ALL,
        CsvQuoting.NONNUMERIC: _QUOTE_NONNUMERIC,
        CsvQuoting.NONE: _QUOTE_NONE,
    }
    return mapping[quoting]


def _validate_headers(headers: tuple[str, ...]) -> None:
    """Reject header identities that are ambiguous for keyed row access."""
    if not headers:
        msg = "CSV files require a header row."
        raise FileFormatError(msg)

    if any(not header.strip() for header in headers):
        msg = "CSV headers cannot be blank."
        raise FileFormatError(msg)

    if len(set(headers)) != len(headers):
        msg = "CSV headers must be unique."
        raise FileFormatError(msg)
