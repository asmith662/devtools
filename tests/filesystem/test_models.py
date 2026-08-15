# Copyright (c) 2026
"""Tests for base filesystem models."""

from __future__ import annotations

from typing import TYPE_CHECKING

import pytest

from devtools.filesystem import (
    BinaryFile,
    CsvFile,
    CsvRow,
    FileFormat,
    JsonFile,
    MarkdownFile,
    TextFile,
)
from devtools.paths import ResolvedPath

if TYPE_CHECKING:
    from pathlib import Path


def test_file_models_expose_their_format_and_value_semantics(tmp_path: Path) -> None:
    """Concrete file models retain their path and format identity."""
    path = ResolvedPath(tmp_path / "example.txt")
    binary = BinaryFile(path, b"abc")
    expected_size = len(b"abc")

    assert binary.format is FileFormat.BINARY
    assert binary.size_bytes == expected_size
    assert binary == BinaryFile(path, b"abc")
    assert TextFile(path, "text").format is FileFormat.TEXT
    assert CsvFile(
        path,
        "a,b",
        headers=("a", "b"),
        rows=(CsvRow(("a", "b"), ("1", "2")),),
    ).format is FileFormat.CSV
    assert MarkdownFile(path, "# Title").format is FileFormat.MARKDOWN
    assert JsonFile(path, "{}").format is FileFormat.JSON


@pytest.mark.parametrize(
    ("encoding", "byte_size", "match"),
    [("", 0, "encoding"), ("utf-8", -1, "byte size")],
)
def test_text_file_rejects_invalid_metadata(
    tmp_path: Path,
    encoding: str,
    byte_size: int,
    match: str,
) -> None:
    """Text metadata requires a non-blank encoding and non-negative byte size."""
    with pytest.raises(ValueError, match=match):
        TextFile(ResolvedPath(tmp_path), "text", encoding, byte_size)


def test_text_file_exposes_explicit_line_literal_and_regex_operations(
    tmp_path: Path,
) -> None:
    """Text files provide deterministic source-text access without iteration."""
    text = TextFile(ResolvedPath(tmp_path), "alpha\nbeta\n")
    expected_line_count = len(("alpha", "beta"))

    assert text.lines == ("alpha", "beta")
    assert text.line_count == expected_line_count
    assert text.character_count == len("alpha\nbeta\n")
    assert text.contains("pha") is True
    assert text.contains("missing") is False
    assert text.search_regex(r"b.ta") is not None
    assert tuple(match.value for match in text.find_all_regex(r"[a-z]+")) == (
        "alpha",
        "beta",
    )
