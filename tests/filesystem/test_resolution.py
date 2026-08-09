# Copyright (c) 2026
"""Tests for filesystem format and codec resolution."""

from __future__ import annotations

from typing import TYPE_CHECKING

import pytest

from devtools.filesystem import (
    FileFormat,
    FileFormatError,
    JsonCodec,
    resolve_file_format,
)
from devtools.filesystem.resolution import resolve_codec
from devtools.paths import ResolvedPath

if TYPE_CHECKING:
    from pathlib import Path


def test_resolve_file_format_is_case_insensitive_for_json(tmp_path: Path) -> None:
    """JSON suffixes resolve regardless of case."""
    path = ResolvedPath(tmp_path / "report.JsOn")

    assert resolve_file_format(path) is FileFormat.JSON


def test_resolution_rejects_unsupported_formats(tmp_path: Path) -> None:
    """Only formats with real codecs resolve during this milestone."""
    with pytest.raises(FileFormatError, match="Unsupported file format"):
        resolve_file_format(ResolvedPath(tmp_path / "report.txt"))

    with pytest.raises(FileFormatError, match="No codec"):
        resolve_codec(FileFormat.TEXT)


def test_resolve_codec_returns_a_json_codec() -> None:
    """The implemented JSON format resolves to its representation codec."""
    assert isinstance(resolve_codec(FileFormat.JSON), JsonCodec)
