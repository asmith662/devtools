# Copyright (c) 2026
"""Independent exact-byte and shared-policy binary I/O acceptance."""

from __future__ import annotations

from typing import TYPE_CHECKING

import pytest

from devtools.core.paths import ResolvedPath
from devtools.resources.filesystem import (
    BinaryCodec,
    BinaryFile,
    FileFormat,
    FileFormatError,
    FilesystemPermissionError,
    FileTooLargeError,
    read,
    write,
)
from devtools.resources.filesystem.codecs import BinaryCodec as ExportedBinaryCodec
from devtools.resources.filesystem.resolution import resolve_codec, resolve_file_format

if TYPE_CHECKING:
    from pathlib import Path


@pytest.mark.parametrize("content", [b"", b"\x00\xff\xfe\r\n", bytes(range(256)) * 8])
def test_exact_binary_round_trip_with_explicit_format(
    tmp_path: Path,
    content: bytes,
) -> None:
    """The codec and generic operations preserve arbitrary bytes and model identity."""
    path = ResolvedPath(tmp_path / "payload.unknown")
    codec = BinaryCodec()
    assert ExportedBinaryCodec is BinaryCodec
    assert isinstance(resolve_codec(FileFormat.BINARY), BinaryCodec)
    model = codec.decode(path, content)
    assert type(model) is BinaryFile
    assert model.path == path
    assert model.content == content
    assert model.size_bytes == len(content)
    assert not model.truncated
    assert codec.encode(model) == content
    write(model)
    assert path.value.read_bytes() == content
    result = read(path, file_format=FileFormat.BINARY, max_bytes=len(content))
    assert isinstance(result, BinaryFile)
    assert result.content == content
    assert not result.truncated
    unlimited = read(path, file_format=FileFormat.BINARY, max_bytes=None)
    assert isinstance(unlimited, BinaryFile)
    assert unlimited.content == content
    if content:
        with pytest.raises(FileTooLargeError):
            read(path, file_format=FileFormat.BINARY, max_bytes=len(content) - 1)
    with pytest.raises(FileExistsError):
        write(BinaryFile(path, b"changed"), overwrite=False)
    assert path.value.read_bytes() == content


@pytest.mark.parametrize("suffix", [".bin", ".unknown"])
def test_binary_format_is_never_inferred(tmp_path: Path, suffix: str) -> None:
    """Unknown files do not silently bypass textual suffix policy."""
    path = ResolvedPath(tmp_path / ("data" + suffix))
    path.value.write_bytes(b"data")
    with pytest.raises(FileFormatError):
        resolve_file_format(path)
    with pytest.raises(FileFormatError):
        read(path)


def test_binary_permission_failure_uses_shared_atomic_cleanup(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Failed replacement preserves the existing target and removes its temporary."""
    path = ResolvedPath(tmp_path / "protected.bin")
    path.value.write_bytes(b"old")

    def denied(*_args: object) -> None:
        raise PermissionError

    monkeypatch.setattr("devtools.resources.filesystem.writing.os.replace", denied)
    with pytest.raises(FilesystemPermissionError):
        write(BinaryFile(path, b"new"))
    assert path.value.read_bytes() == b"old"
    assert not list(tmp_path.glob(".protected.bin.*.tmp"))
