# Copyright (c) 2026
"""Tests for filesystem format and codec resolution."""

from __future__ import annotations

from typing import TYPE_CHECKING

import pytest

from devtools.core.paths import ResolvedPath
from devtools.resources.filesystem import (
    CsvCodec,
    FileFormat,
    FileFormatError,
    JsonCodec,
    MarkdownCodec,
    TextCodec,
    resolve_file_format,
)
from devtools.resources.filesystem.resolution import resolve_codec

if TYPE_CHECKING:
    from pathlib import Path


@pytest.mark.parametrize(
    ("filename", "file_format"),
    [
        ("report.JsOn", FileFormat.JSON),
        ("report.CsV", FileFormat.CSV),
        ("report.MD", FileFormat.MARKDOWN),
        ("report.MarkDown", FileFormat.MARKDOWN),
        ("report.TxT", FileFormat.TEXT),
    ],
)
def test_resolve_file_format_is_case_insensitive_for_supported_codecs(
    tmp_path: Path,
    filename: str,
    file_format: FileFormat,
) -> None:
    """JSON, text, and Markdown suffixes resolve regardless of case."""
    path = ResolvedPath(tmp_path / filename)

    assert resolve_file_format(path) is file_format


def test_resolution_rejects_unsupported_formats(tmp_path: Path) -> None:
    """Only formats with real codecs resolve during this milestone."""
    with pytest.raises(FileFormatError, match="Unsupported file format"):
        resolve_file_format(ResolvedPath(tmp_path / "report.unsupported"))

    with pytest.raises(FileFormatError, match="No codec"):
        resolve_codec(FileFormat.BINARY)


def test_resolve_codec_returns_implemented_codecs() -> None:
    """Each supported format resolves to its concrete representation codec."""
    assert isinstance(resolve_codec(FileFormat.JSON), JsonCodec)
    assert isinstance(resolve_codec(FileFormat.CSV), CsvCodec)
    assert isinstance(resolve_codec(FileFormat.MARKDOWN), MarkdownCodec)
    assert isinstance(resolve_codec(FileFormat.TEXT), TextCodec)
