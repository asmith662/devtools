# Copyright (c) 2026
"""Tests for codec-backed atomic filesystem writing."""

from __future__ import annotations

import json
import os
from pathlib import Path
from typing import Never

import pytest

from devtools.filesystem import (
    BinaryFile,
    FileFormatError,
    FilesystemPermissionError,
    JsonCodec,
    JsonObjectFile,
    write,
)
from devtools.paths import ResolvedPath


def test_write_persists_a_new_json_file_and_fsyncs_before_replacement(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Writing uses a sibling temporary file, fsync, then atomic replacement."""
    target = tmp_path / "result.json"
    file = JsonCodec().parse(ResolvedPath(target), '{"name":"Ada"}')
    fsync_calls: list[int] = []
    replace_calls: list[tuple[Path, Path]] = []
    original_fsync = os.fsync
    original_replace = os.replace

    def record_fsync(file_descriptor: int) -> None:
        fsync_calls.append(file_descriptor)
        original_fsync(file_descriptor)

    def record_replace(source: Path, destination: Path) -> None:
        replace_calls.append((source, destination))
        original_replace(source, destination)

    monkeypatch.setattr("devtools.filesystem.writing.os.fsync", record_fsync)
    monkeypatch.setattr("devtools.filesystem.writing.os.replace", record_replace)

    write(file)

    assert json.loads(target.read_text(encoding="utf-8")) == {"name": "Ada"}
    assert fsync_calls
    assert replace_calls[0][0].parent == target.parent
    assert replace_calls[0][1] == target


def test_write_persists_current_json_value_not_stale_source_provenance(
    tmp_path: Path,
) -> None:
    """Structured transformations control persistence even when content is stale."""
    target = tmp_path / "settings.txt"
    original = JsonCodec().parse(ResolvedPath(target), '{"status":"old"}')
    assert isinstance(original, JsonObjectFile)
    updated = original.with_item("status", "new")

    write(updated)

    assert updated.content == original.content
    assert json.loads(target.read_text(encoding="utf-8")) == {"status": "new"}


def test_write_rejects_existing_targets_when_overwrite_is_disabled(
    tmp_path: Path,
) -> None:
    """The conventional builtin error preserves an untouched destination."""
    target = tmp_path / "existing.json"
    target.write_text('{"status":"old"}', encoding="utf-8")
    file = JsonCodec().parse(ResolvedPath(target), '{"status":"new"}')

    with pytest.raises(FileExistsError, match="already exists"):
        write(file, overwrite=False)

    assert target.read_text(encoding="utf-8") == '{"status":"old"}'


def test_write_overwrites_an_existing_target_by_default(tmp_path: Path) -> None:
    """Existing destinations are atomically replaced when overwrite is enabled."""
    target = tmp_path / "existing.json"
    target.write_text('{"status":"old"}', encoding="utf-8")
    file = JsonCodec().parse(ResolvedPath(target), '{"status":"new"}')

    write(file)

    assert json.loads(target.read_text(encoding="utf-8")) == {"status": "new"}


def test_write_rejects_models_without_an_implemented_codec(tmp_path: Path) -> None:
    """Generic writing exposes only the currently implemented JSON codec."""
    file = BinaryFile(ResolvedPath(tmp_path / "value.bin"), b"data")

    with pytest.raises(FileFormatError, match="No codec"):
        write(file)


def test_write_normalizes_permission_failures_and_cleans_temporary_files(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Denied replacement leaves the old target and removes the sibling temporary."""
    target = tmp_path / "protected.json"
    original_content = b'{"status":"old"}'
    target.write_bytes(original_content)
    file = JsonCodec().parse(ResolvedPath(target), '{"status":"new"}')
    temporary_paths: list[Path] = []

    def deny_replace(source: Path, _destination: Path) -> None:
        temporary_paths.append(source)
        raise PermissionError

    monkeypatch.setattr("devtools.filesystem.writing.os.replace", deny_replace)

    with pytest.raises(FilesystemPermissionError, match="writing"):
        write(file)

    assert temporary_paths[0].parent == target.parent
    assert not temporary_paths[0].exists()
    assert target.read_bytes() == original_content


def test_write_normalizes_temporary_cleanup_permission_failures(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """A denied cleanup is reported as a filesystem-domain permission error."""
    target = tmp_path / "cleanup.json"
    file = JsonCodec().parse(ResolvedPath(target), "{}")
    temporary_paths: list[Path] = []

    def deny_replace(source: Path, _destination: Path) -> None:
        temporary_paths.append(source)
        raise PermissionError

    def deny_unlink(_path: Path, *, missing_ok: bool = False) -> None:
        del missing_ok
        raise PermissionError

    monkeypatch.setattr("devtools.filesystem.writing.os.replace", deny_replace)
    monkeypatch.setattr(Path, "unlink", deny_unlink)

    with pytest.raises(FilesystemPermissionError, match="cleaning"):
        write(file)

    monkeypatch.undo()
    temporary_paths[0].unlink()


def test_write_normalizes_inspection_and_temporary_creation_permission_errors(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Permission errors at both write setup stages use the domain error."""
    target = tmp_path / "value.json"
    file = JsonCodec().parse(ResolvedPath(target), "{}")

    def deny_exists(_path: Path) -> bool:
        raise PermissionError

    monkeypatch.setattr(Path, "exists", deny_exists)

    with pytest.raises(FilesystemPermissionError, match="inspecting"):
        write(file)

    monkeypatch.undo()

    def deny_temporary_file(**_kwargs: object) -> Never:
        raise PermissionError

    monkeypatch.setattr(
        "devtools.filesystem.writing.NamedTemporaryFile",
        deny_temporary_file,
    )

    with pytest.raises(FilesystemPermissionError, match="writing"):
        write(file)
