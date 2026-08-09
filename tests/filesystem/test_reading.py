# Copyright (c) 2026
"""Tests for bounded codec-backed filesystem reading."""

from __future__ import annotations

from pathlib import Path

import pytest

from devtools.filesystem import (
    DEFAULT_MAX_READ_BYTES,
    FileFormat,
    FileFormatError,
    FilesystemNotFoundError,
    FilesystemPermissionError,
    FileTooLargeError,
    JsonListFile,
    JsonObjectFile,
    JsonScalarFile,
    NotAFileError,
    read,
)
from devtools.paths import ResolvedPath


@pytest.mark.parametrize(
    ("name", "content", "model_type"),
    [
        ("object.json", b'{"name":"Ada","id":2}', JsonObjectFile),
        ("array.JSON", b'[{"id":1}]', JsonListFile),
        ("scalar.json", b"true", JsonScalarFile),
    ],
)
def test_read_returns_the_concrete_json_root_model(
    tmp_path: Path,
    name: str,
    content: bytes,
    model_type: type[JsonObjectFile | JsonListFile | JsonScalarFile],
) -> None:
    """Suffix resolution and decoding preserve the rich JSON root type."""
    source = tmp_path / name
    source.write_bytes(content)

    file = read(ResolvedPath(source))

    assert isinstance(file, model_type)
    assert file.byte_size == len(content)


def test_read_allows_an_explicit_format_override_and_retains_json_behavior(
    tmp_path: Path,
) -> None:
    """Explicit format selection bypasses suffix inference without losing models."""
    source = tmp_path / "configuration.data"
    source.write_text('{"name":"Ada","enabled":true}', encoding="utf-8")

    file = read(ResolvedPath(source), file_format=FileFormat.JSON)

    assert isinstance(file, JsonObjectFile)
    assert file.search_regex("Ada") is not None
    assert file.find(lambda key, _value: key == "enabled") == ("enabled", True)


def test_read_rejects_missing_paths_and_directories(tmp_path: Path) -> None:
    """Generic reading accepts existing regular files only."""
    with pytest.raises(FilesystemNotFoundError, match="does not exist"):
        read(ResolvedPath(tmp_path / "missing.json"))

    with pytest.raises(NotAFileError, match="not a regular file"):
        read(ResolvedPath(tmp_path))


def test_read_enforces_configured_size_limits(tmp_path: Path) -> None:
    """Bounded reads reject oversized files but accept an exact boundary."""
    source = tmp_path / "value.json"
    source.write_bytes(b"{}")

    assert isinstance(read(ResolvedPath(source), max_bytes=2), JsonObjectFile)

    with pytest.raises(FileTooLargeError, match="exceeds"):
        read(ResolvedPath(source), max_bytes=1)

    with pytest.raises(ValueError, match="cannot be negative"):
        read(ResolvedPath(source), max_bytes=-1)


def test_read_supports_an_explicitly_unbounded_limit(tmp_path: Path) -> None:
    """A ``None`` limit opts into an unbounded complete read."""
    source = tmp_path / "large.json"
    source.write_bytes(b'"' + (b"a" * (DEFAULT_MAX_READ_BYTES + 1)) + b'"')

    file = read(ResolvedPath(source), max_bytes=None)

    assert isinstance(file, JsonScalarFile)
    assert file.character_count == DEFAULT_MAX_READ_BYTES + 3


def test_read_rechecks_size_after_the_content_is_loaded(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """A file that grows after stat is rejected rather than returned oversized."""
    source = tmp_path / "racing.json"
    source.write_bytes(b"{}")
    grown_content = b'{"name":"longer"}'

    def read_grown_content(_path: Path) -> bytes:
        return grown_content

    monkeypatch.setattr(Path, "read_bytes", read_grown_content)

    with pytest.raises(FileTooLargeError, match="exceeds"):
        read(ResolvedPath(source), max_bytes=2)


def test_read_normalizes_permission_failures(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Inspection and content-read permission failures use domain errors."""
    source = tmp_path / "value.json"
    source.write_bytes(b"{}")

    def deny_exists(_path: Path) -> bool:
        raise PermissionError

    monkeypatch.setattr(Path, "exists", deny_exists)

    with pytest.raises(FilesystemPermissionError, match="inspecting"):
        read(ResolvedPath(source))

    monkeypatch.undo()

    def deny_read(_path: Path) -> bytes:
        raise PermissionError

    monkeypatch.setattr(Path, "read_bytes", deny_read)

    with pytest.raises(FilesystemPermissionError, match="reading"):
        read(ResolvedPath(source))


def test_read_reports_unsupported_inferred_suffixes(tmp_path: Path) -> None:
    """An unsupported suffix fails after a complete bounded file read."""
    source = tmp_path / "value.unknown"
    source.write_bytes(b"{}")

    with pytest.raises(FileFormatError, match="Unsupported file format"):
        read(ResolvedPath(source))
