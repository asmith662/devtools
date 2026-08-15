# Copyright (c) 2026
"""Tests for the header-based CSV representation codec."""

from __future__ import annotations

from typing import TYPE_CHECKING

import pytest

from devtools.filesystem import (
    CsvCodec,
    CsvDialect,
    CsvFile,
    CsvQuoting,
    CsvRow,
    FileFormatError,
    TextDecodingError,
    TextEncodingError,
)
from devtools.paths import ResolvedPath

if TYPE_CHECKING:
    from pathlib import Path


def test_decode_preserves_metadata_and_parses_quoted_csv(tmp_path: Path) -> None:
    """Decoded CSV retains exact source provenance and structured string cells."""
    source = 'id,description\n1,"contains, delimiter"\n2,"line one\nline two"\n'
    encoded = source.encode()

    file = CsvCodec().decode(ResolvedPath(tmp_path / "data.csv"), encoded)

    assert file.content == source
    assert file.encoding == "utf-8"
    assert file.byte_size == len(encoded)
    assert file.headers == ("id", "description")
    assert file[0]["description"] == "contains, delimiter"
    assert file[1]["description"] == "line one\nline two"


def test_decode_supports_alternate_encodings_and_normalizes_errors(
    tmp_path: Path,
) -> None:
    """Byte decoding follows the established codec encoding-error contract."""
    codec = CsvCodec()
    path = ResolvedPath(tmp_path / "data.csv")
    source = "city\nMÃ¼nchen\n"

    file = codec.decode(path, source.encode("utf-16"), encoding="utf-16")

    assert file.encoding == "utf-16"
    assert file[0]["city"] == "MÃ¼nchen"

    with pytest.raises(TextDecodingError, match="utf-8"):
        codec.decode(path, b"\xff")

    with pytest.raises(TextDecodingError, match="unknown-codec"):
        codec.decode(path, b"city\n", encoding="unknown-codec")


@pytest.mark.parametrize(
    ("source", "match"),
    [
        ("", "header row"),
        ("\n", "header row"),
        ("id,id\n1,2\n", "unique"),
        (",name\n1,Ada\n", "blank"),
        ("id,name\n1\n", "values"),
        ('"unterminated', "Invalid CSV"),
        ('id,name\n1,"unterminated', "Invalid CSV"),
    ],
)
def test_parse_rejects_invalid_header_based_source(
    tmp_path: Path,
    source: str,
    match: str,
) -> None:
    """Headerless, ambiguous, ragged, and malformed CSV cannot form a model."""
    with pytest.raises(FileFormatError, match=match):
        CsvCodec().parse(ResolvedPath(tmp_path / "invalid.csv"), source)


def test_parse_derives_source_size_and_supports_header_only_and_dialects(
    tmp_path: Path,
) -> None:
    """Parsing derives metadata and retains explicit delimiter/quoting policy."""
    codec = CsvCodec()
    source = "id;name\n1;Ada\n"
    dialect = CsvDialect(delimiter=";", quoting=CsvQuoting.ALL)

    file = codec.parse(ResolvedPath(tmp_path / "data.csv"), source, dialect=dialect)
    header_only = codec.parse(ResolvedPath(tmp_path / "headers.csv"), "id,name\n")

    assert file.byte_size == len(source.encode())
    assert file.dialect == dialect
    assert file[0]["name"] == "Ada"
    assert len(header_only) == 0

    empty_cell = codec.parse(ResolvedPath(tmp_path / "empty.csv"), 'id\n""\n')
    assert empty_cell[0]["id"] == ""

    with pytest.raises(TextEncodingError, match="ascii"):
        codec.parse(ResolvedPath(tmp_path / "encoding.csv"), "Ã©", encoding="ascii")


@pytest.mark.parametrize(
    "quoting",
    [
        CsvQuoting.MINIMAL,
        CsvQuoting.ALL,
        CsvQuoting.NONNUMERIC,
    ],
)
def test_serialize_uses_current_state_and_explicit_dialect(
    tmp_path: Path,
    quoting: CsvQuoting,
) -> None:
    """Serialization delegates deterministic quoting and line endings to csv.writer."""
    dialect = CsvDialect(quoting=quoting, lineterminator="\r\n")
    file = CsvCodec().parse(
        ResolvedPath(tmp_path / "data.csv"),
        '"id","name"\n"1","Ada"\n',
        dialect=dialect,
    )
    updated = file.appended(file[0])

    serialized = CsvCodec().serialize(updated)
    expected_records = 3
    reparsed = CsvCodec().parse(
        ResolvedPath(tmp_path / "again.csv"),
        serialized,
        dialect=dialect,
    )

    assert serialized.endswith("\r\n")
    assert serialized.count("\r\n") == expected_records
    assert reparsed.rows == updated.rows


def test_serialize_wraps_invalid_quote_none_combinations(tmp_path: Path) -> None:
    """csv.writer failures are surfaced as coherent file-format errors."""
    dialect = CsvDialect(quoting=CsvQuoting.NONE)
    file = CsvFile(
        ResolvedPath(tmp_path / "data.csv"),
        "id\ncontains,delimiter\n",
        headers=("id",),
        rows=(
            CsvRow(("id",), ("contains,delimiter",)),
        ),
        dialect=dialect,
    )

    with pytest.raises(FileFormatError, match="cannot be serialized"):
        CsvCodec().serialize(file)


def test_encode_uses_model_encoding_override_and_normalizes_errors(
    tmp_path: Path,
) -> None:
    """CSV encoding follows file metadata unless an explicit override is supplied."""
    codec = CsvCodec()
    file = codec.parse(
        ResolvedPath(tmp_path / "data.csv"),
        "city\nMÃ¼nchen\n",
        encoding="utf-16",
    )

    assert codec.encode(file) == codec.serialize(file).encode("utf-16")
    assert codec.encode(file, encoding="utf-8") == codec.serialize(file).encode()

    with pytest.raises(TextEncodingError, match="ascii"):
        codec.encode(file, encoding="ascii")

    with pytest.raises(TextEncodingError, match="unknown-codec"):
        codec.encode(file, encoding="unknown-codec")
