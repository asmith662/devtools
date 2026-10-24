# Copyright (c) 2026
# ruff: noqa: COM812 -- maintained test formatting convention
"""Independent maintained checks for the frozen bounded-read requirements."""

from __future__ import annotations

from io import BytesIO
from operator import index
from typing import TYPE_CHECKING

import pytest

from devtools.core.paths import ResolvedPath
from devtools.resources.filesystem import (
    BinaryFile,
    FileFormat,
    FilesystemPermissionError,
    FileTooLargeError,
    read,
)

if TYPE_CHECKING:
    from pathlib import Path
    from typing import SupportsIndex


class ObservedStream(BytesIO):
    """Record allocation requests while simulating legal short reads."""

    def __init__(self, data: bytes, *, short: bool = False) -> None:
        """Capture only the supplied finite test resource."""
        super().__init__(data)
        self.requests: list[int] = []
        self.consumed = 0
        self.short = short

    def read(self, size: SupportsIndex | None = -1, /) -> bytes:
        """Honor normal read semantics with optional short positive reads."""
        requested = -1 if size is None else index(size)
        self.requests.append(requested)
        short_size = 2
        result = super().read(
            short_size if self.short and requested > short_size else requested
        )
        self.consumed += len(result)
        return result


@pytest.mark.parametrize(
    ("data", "limit", "short", "overflow"),
    [
        (b"x" * 100_000, 5, False, True),
        (b"abcde", 5, False, False),
        (b"abcde", 5, True, False),
        (b"abcdefghi", 5, True, True),
        (b"", 5, False, False),
        (b"arbitrary\x00\xff", None, False, False),
        (b"", 0, False, False),
        (b"x", 0, False, True),
    ],
    ids=(
        "growth",
        "exact",
        "short",
        "short-growth",
        "empty",
        "unlimited",
        "zero",
        "zero-growth",
    ),
)
def test_actual_consumption_is_bounded_and_short_reads_are_complete(  # noqa: PLR0913 -- fixture matrix
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    data: bytes,
    limit: int | None,
    *,
    short: bool,
    overflow: bool,
) -> None:
    """A small stat result cannot admit an unlimited growing byte stream."""
    source = tmp_path / "input.data"
    source.write_bytes(b"" if limit == 0 else b"x")
    stream = ObservedStream(data, short=short)

    def opening(path: Path, mode: str) -> BytesIO:
        assert path == source
        assert mode == "rb"
        return stream

    monkeypatch.setattr(type(source), "open", opening)
    if overflow:
        with pytest.raises(FileTooLargeError):
            read(ResolvedPath(source), file_format=FileFormat.BINARY, max_bytes=limit)
    else:
        result = read(
            ResolvedPath(source), file_format=FileFormat.BINARY, max_bytes=limit
        )
        assert isinstance(result, BinaryFile)
        assert result.content == data
        assert result.size_bytes == len(data)
        assert not result.truncated
    assert stream.closed
    assert stream.requests
    if limit is not None:
        assert all(0 <= request <= limit + 1 for request in stream.requests)
        assert stream.consumed <= limit + 1


def test_read_stream_failure_closes_and_normalizes_permissions(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """A denied read after opening retains cleanup and domain errors."""
    source = tmp_path / "denied.data"
    source.write_bytes(b"x")

    class DeniedStream(BytesIO):
        def read(self, _size: SupportsIndex | None = -1, /) -> bytes:
            """Simulate a permission failure after opening succeeds."""
            raise PermissionError

    stream = DeniedStream(b"x")

    def opening(_path: Path, _mode: str) -> BytesIO:
        return stream

    monkeypatch.setattr(type(source), "open", opening)
    with pytest.raises(FilesystemPermissionError):
        read(ResolvedPath(source), file_format=FileFormat.BINARY, max_bytes=3)
    assert stream.closed
