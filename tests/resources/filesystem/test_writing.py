# Copyright (c) 2026
"""Tests for codec-backed atomic filesystem writing."""

from __future__ import annotations

import json
import os
from importlib import import_module
from pathlib import Path
from typing import Never

import pytest

from devtools.core.paths import ResolvedPath
from devtools.resources.filesystem import (
    BinaryFile,
    CsvCodec,
    FileFormatError,
    FilesystemPermissionError,
    JsonCodec,
    JsonObjectFile,
    MarkdownCodec,
    TextCodec,
    write,
)

_SYMLINK_PRIVILEGE_NOT_HELD = 1314


def test_write_persists_a_new_json_file_and_fsyncs_before_replacement(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Writing uses a sibling temporary file, fsync, then atomic replacement."""
    target = tmp_path / "result.json"
    file = JsonCodec().parse(ResolvedPath(target), '{"name":"Ada"}')
    fsync_calls: list[int] = []
    replace_calls: list[tuple[Path, Path]] = []
    order: list[str] = []
    original_fsync = os.fsync
    original_replace = os.replace

    def record_fsync(file_descriptor: int) -> None:
        order.append("fsync")
        fsync_calls.append(file_descriptor)
        original_fsync(file_descriptor)

    def record_replace(source: Path, destination: Path) -> None:
        order.append("replace")
        replace_calls.append((source, destination))
        original_replace(source, destination)

    monkeypatch.setattr("devtools.resources.filesystem.writing.os.fsync", record_fsync)
    monkeypatch.setattr(
        "devtools.resources.filesystem.writing.os.replace",
        record_replace,
    )

    write(file)

    assert json.loads(target.read_text(encoding="utf-8")) == {"name": "Ada"}
    assert fsync_calls
    assert replace_calls[0][0].parent == target.parent
    assert replace_calls[0][1] == target
    assert order == ["fsync", "replace"]


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


def test_write_persists_text_using_the_model_format_not_the_suffix(
    tmp_path: Path,
) -> None:
    """A text model writes text even when its destination has a JSON suffix."""
    target = tmp_path / "notes.json"
    file = TextCodec().decode(
        ResolvedPath(target),
        "cafÃ©\r\n".encode(),
    )

    write(file)

    assert target.read_bytes() == "cafÃ©\r\n".encode()


def test_write_text_overwrites_or_preserves_existing_destinations(
    tmp_path: Path,
) -> None:
    """Text models use the shared overwrite policy and atomic writer path."""
    target = tmp_path / "notes.txt"
    target.write_bytes(b"old")
    file = TextCodec().decode(ResolvedPath(target), b"new\n")

    with pytest.raises(FileExistsError, match="already exists"):
        write(file, overwrite=False)

    assert target.read_bytes() == b"old"

    write(file)

    assert target.read_bytes() == b"new\n"


def test_write_persists_markdown_using_the_model_format_not_the_suffix(
    tmp_path: Path,
) -> None:
    """A Markdown model uses MarkdownCodec even with a misleading text suffix."""
    target = tmp_path / "document.txt"
    content = "# Title\r\n"
    file = MarkdownCodec().decode(ResolvedPath(target), content.encode())

    write(file)

    assert target.read_bytes() == content.encode()


def test_write_markdown_honors_the_shared_overwrite_policy(tmp_path: Path) -> None:
    """Markdown writes preserve existing data when overwrite is disabled."""
    target = tmp_path / "document.md"
    target.write_bytes(b"# Old\n")
    file = MarkdownCodec().decode(ResolvedPath(target), b"# New\n")

    with pytest.raises(FileExistsError, match="already exists"):
        write(file, overwrite=False)

    assert target.read_bytes() == b"# Old\n"


def test_write_persists_current_csv_state_not_stale_source_provenance(
    tmp_path: Path,
) -> None:
    """CSV writes serialize current rows through CsvCodec despite path suffix."""
    target = tmp_path / "reports.txt"
    original = CsvCodec().parse(
        ResolvedPath(target),
        "id,status\nreport-1,failed\n",
    )
    updated = original.appended(original[0])

    write(updated)

    reparsed = CsvCodec().decode(ResolvedPath(target), target.read_bytes())
    assert updated.content == original.content
    assert reparsed.headers == updated.headers
    assert reparsed.rows == updated.rows


def test_write_csv_honors_the_shared_overwrite_policy(tmp_path: Path) -> None:
    """CSV persistence preserves an existing target when overwrite is disabled."""
    target = tmp_path / "reports.csv"
    target.write_bytes(b"id\nold\n")
    file = CsvCodec().parse(ResolvedPath(target), "id\nnew\n")

    with pytest.raises(FileExistsError, match="already exists"):
        write(file, overwrite=False)

    assert target.read_bytes() == b"id\nold\n"


def test_write_rejects_a_binary_model_codec_mismatch(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """A broken resolver cannot route binary bytes through a text codec."""
    file = BinaryFile(ResolvedPath(tmp_path / "value.bin"), b"data")
    monkeypatch.setattr(
        "devtools.resources.filesystem.writing.resolve_codec",
        lambda _file_format: TextCodec(),
    )

    with pytest.raises(FileFormatError, match="No codec"):
        write(file)


def test_write_rejects_a_defensive_model_codec_mismatch(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """A broken resolver cannot route a JSON model through the text codec."""
    target = tmp_path / "value.json"
    file = JsonCodec().parse(ResolvedPath(target), "{}")

    writing_module = import_module("devtools.resources.filesystem.writing")
    monkeypatch.setattr(
        writing_module,
        "resolve_codec",
        lambda _file_format: TextCodec(),
    )

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

    monkeypatch.setattr(
        "devtools.resources.filesystem.writing.os.replace",
        deny_replace,
    )

    with pytest.raises(FilesystemPermissionError, match="writing"):
        write(file)

    assert temporary_paths[0].parent == target.parent
    assert not temporary_paths[0].exists()
    assert target.read_bytes() == original_content


def test_write_cleans_a_temporary_file_when_preparation_fsync_fails(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """A temporary path is cleaned when preparation fails before replacement."""
    target = tmp_path / "preparation.json"
    original_content = b'{"status":"old"}'
    target.write_bytes(original_content)
    file = JsonCodec().parse(ResolvedPath(target), '{"status":"new"}')
    replace_calls: list[tuple[Path, Path]] = []

    def deny_fsync(_file_descriptor: int) -> None:
        raise PermissionError

    def record_replace(source: Path, destination: Path) -> None:
        replace_calls.append((source, destination))

    monkeypatch.setattr("devtools.resources.filesystem.writing.os.fsync", deny_fsync)
    monkeypatch.setattr(
        "devtools.resources.filesystem.writing.os.replace",
        record_replace,
    )

    with pytest.raises(FilesystemPermissionError, match="writing"):
        write(file)

    assert target.read_bytes() == original_content
    assert replace_calls == []
    assert tuple(tmp_path.glob(f".{target.name}.*.tmp")) == ()


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

    monkeypatch.setattr(
        "devtools.resources.filesystem.writing.os.replace",
        deny_replace,
    )
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

    def deny_lstat(_path: Path) -> Never:
        raise PermissionError

    monkeypatch.setattr(Path, "lstat", deny_lstat)

    with pytest.raises(FilesystemPermissionError, match="inspecting"):
        write(file)

    monkeypatch.undo()

    def deny_temporary_file(**_kwargs: object) -> Never:
        raise PermissionError

    monkeypatch.setattr(
        "devtools.resources.filesystem.writing.NamedTemporaryFile",
        deny_temporary_file,
    )

    with pytest.raises(FilesystemPermissionError, match="writing"):
        write(file)


@pytest.mark.parametrize("binary", [False, True])
@pytest.mark.parametrize("directory", [False, True])
@pytest.mark.parametrize("live", [False, True])
def test_no_overwrite_preserves_real_link_entry(
    tmp_path: Path,
    *,
    binary: bool,
    directory: bool,
    live: bool,
) -> None:
    """Entry existence is independent of whether its referent currently exists."""
    target = tmp_path / "referent"
    if live:
        if directory:
            target.mkdir()
            (target / "member").write_bytes(b"original")
        else:
            target.write_bytes(b"original")
    folder = tmp_path / "nested"
    folder.mkdir()
    link = folder / "entry"
    try:
        link.symlink_to(target, target_is_directory=directory)
    except OSError as error:
        if os.name == "nt" and error.winerror == _SYMLINK_PRIVILEGE_NOT_HELD:
            pytest.skip("Windows symlink privilege unavailable")
        raise
    before = link.lstat()
    original_link = os.readlink(link)  # noqa: PTH115 -- preserve exact native target spelling
    file = (
        BinaryFile(ResolvedPath(link), b"new")
        if binary
        else TextCodec().decode(ResolvedPath(link), b"new")
    )
    with pytest.raises(FileExistsError, match="already exists"):
        write(file, overwrite=False)
    assert link.is_symlink()
    assert os.readlink(link) == original_link  # noqa: PTH115 -- exact link identity
    assert link.lstat().st_ino == before.st_ino
    assert target.exists() is live
    if live:
        assert (target / "member" if directory else target).read_bytes() == b"original"
    assert tuple(folder.iterdir()) == (link,)


@pytest.mark.parametrize("binary", [False, True])
def test_no_overwrite_absent_and_directory_controls(
    tmp_path: Path,
    *,
    binary: bool,
) -> None:
    """Absent entries write normally; an existing directory stays intact."""
    path = tmp_path / "absent"
    file = (
        BinaryFile(ResolvedPath(path), b"literal")
        if binary
        else TextCodec().decode(ResolvedPath(path), b"literal")
    )
    write(file, overwrite=False)
    assert path.read_bytes() == b"literal"
    folder = tmp_path / "directory"
    folder.mkdir()
    existing = BinaryFile(ResolvedPath(folder), b"literal")
    with pytest.raises(FileExistsError):
        write(existing, overwrite=False)
    assert folder.is_dir()
    assert tuple(folder.iterdir()) == ()


def test_unclassifiable_destination_refuses_before_preparing_a_write(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """An inspection error is not evidence of absence or permission to replace."""
    path = tmp_path / "unknown"
    error = OSError("literal inspection failure")

    def fail_inspection(_path: Path) -> Never:
        raise error

    def unexpected_prepare(**_kwargs: object) -> Never:
        pytest.fail("Writer entered preparation after unclassified destination")

    monkeypatch.setattr(Path, "lstat", fail_inspection)
    monkeypatch.setattr(
        "devtools.resources.filesystem.writing.NamedTemporaryFile",
        unexpected_prepare,
    )
    with pytest.raises(OSError, match="literal inspection failure") as raised:
        write(BinaryFile(ResolvedPath(path), b"new"), overwrite=False)
    assert raised.value is error


@pytest.mark.parametrize("live", [False, True])
def test_permitted_overwrite_replaces_link_without_writing_its_referent(
    tmp_path: Path,
    *,
    live: bool,
) -> None:
    """The explicit overwrite policy still replaces a file-link directory entry."""
    target = tmp_path / "target"
    if live:
        target.write_bytes(b"original")
    link = tmp_path / "link"
    try:
        link.symlink_to(target)
    except OSError as error:
        if os.name == "nt" and error.winerror == _SYMLINK_PRIVILEGE_NOT_HELD:
            pytest.skip("Windows symlink privilege unavailable")
        raise
    write(BinaryFile(ResolvedPath(link), b"replacement"), overwrite=True)
    assert not link.is_symlink()
    assert link.read_bytes() == b"replacement"
    assert target.exists() is live
    if live:
        assert target.read_bytes() == b"original"
