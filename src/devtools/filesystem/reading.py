# Copyright (c) 2026
"""Codec-backed filesystem reading."""

from __future__ import annotations

from devtools.filesystem.errors import (
    FileTooLargeError,
    FilesystemNotFoundError,
    FilesystemPermissionError,
    NotAFileError,
)
from devtools.filesystem.models import File, FileFormat
from devtools.filesystem.resolution import (
    resolve_codec,
    resolve_file_format,
)
from devtools.paths import ResolvedPath

DEFAULT_MAX_READ_BYTES = 16 * 1024 * 1024


def read(
    path: ResolvedPath,
    *,
    file_format: FileFormat | None = None,
    max_bytes: int | None = DEFAULT_MAX_READ_BYTES,
) -> File:
    """Read a filesystem file into its rich file model.

    When ``file_format`` is omitted, the format is inferred from the path.
    An explicit format overrides suffix-based inference.

    The file is size-checked before its contents are loaded into memory.

    :param path: Resolved path to the file.
    :param file_format: Explicit file format override.
    :param max_bytes: Maximum permitted file size, or ``None`` for no limit.
    :returns: Decoded file model.
    :raises FilesystemNotFoundError: If the target does not exist.
    :raises NotAFileError: If the target is not a regular file.
    :raises FileTooLargeError: If the file exceeds ``max_bytes``.
    :raises FilesystemPermissionError: If filesystem access is denied.
    """
    source = path.value

    try:
        if not source.exists():
            msg = f"Filesystem path does not exist: {path}."
            raise FilesystemNotFoundError(msg)

        if not source.is_file():
            msg = f"Filesystem path is not a regular file: {path}."
            raise NotAFileError(msg)

        size_bytes = source.stat().st_size
    except PermissionError as error:
        msg = f"Permission denied while inspecting file: {path}."
        raise FilesystemPermissionError(msg) from error

    _validate_read_size(
        path,
        size_bytes=size_bytes,
        max_bytes=max_bytes,
    )

    try:
        content = source.read_bytes()
    except PermissionError as error:
        msg = f"Permission denied while reading file: {path}."
        raise FilesystemPermissionError(msg) from error

    _validate_read_size(
        path,
        size_bytes=len(content),
        max_bytes=max_bytes,
    )

    resolved_format = (
        resolve_file_format(path)
        if file_format is None
        else file_format
    )
    codec = resolve_codec(resolved_format)

    return codec.decode(
        path,
        content,
    )


def _validate_read_size(
    path: ResolvedPath,
    *,
    size_bytes: int,
    max_bytes: int | None,
) -> None:
    """Validate a file against the configured read limit.

    :param path: File being validated.
    :param size_bytes: File size reported by the filesystem.
    :param max_bytes: Maximum permitted byte count.
    :raises ValueError: If ``max_bytes`` is negative.
    :raises FileTooLargeError: If the file exceeds the configured limit.
    """
    if max_bytes is None:
        return

    if max_bytes < 0:
        msg = "Maximum read size cannot be negative."
        raise ValueError(msg)

    if size_bytes > max_bytes:
        msg = (
            f"File size {size_bytes} exceeds maximum read size "
            f"{max_bytes}: {path}."
        )
        raise FileTooLargeError(msg)
