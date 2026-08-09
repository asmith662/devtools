# Copyright (c) 2026
"""Codec-backed atomic filesystem writing."""

from __future__ import annotations

import os
from pathlib import Path
from tempfile import NamedTemporaryFile

from devtools.filesystem.errors import (
    FilesystemPermissionError,
)
from devtools.filesystem.models import File
from devtools.filesystem.resolution import resolve_codec


def write(
    file: File,
    *,
    overwrite: bool = True,
) -> None:
    """Persist a file model using its format codec.

    The file model's format determines the codec used for serialization.
    Writes are performed through a sibling temporary file and atomically
    replace the destination on success.

    :param file: File model to persist.
    :param overwrite: Whether an existing destination may be replaced.
    :raises FileExistsError: If the destination exists and overwrite is false.
    :raises FilesystemPermissionError: If filesystem permissions prevent the
        write or replacement.
    """
    target = file.path.value

    try:
        if target.exists() and not overwrite:
            msg = f"Filesystem path already exists: {file.path}."
            raise FileExistsError(msg)
    except PermissionError as error:
        msg = f"Permission denied while inspecting file: {file.path}."
        raise FilesystemPermissionError(msg) from error

    codec = resolve_codec(file.format)
    content = codec.encode(file)

    _atomic_write(
        target,
        content,
    )


def _atomic_write(
    target: Path,
    content: bytes,
) -> None:
    """Atomically write bytes to a filesystem path.

    A temporary file is created in the destination directory so the final
    replacement remains on the same filesystem.

    :param target: Destination path.
    :param content: Bytes to persist.
    :raises FilesystemPermissionError: If the filesystem denies the operation.
    """
    temporary_path: Path | None = None

    try:
        with NamedTemporaryFile(
            mode="wb",
            dir=target.parent,
            prefix=f".{target.name}.",
            suffix=".tmp",
            delete=False,
        ) as temporary:
            temporary.write(content)
            temporary.flush()
            os.fsync(temporary.fileno())
            temporary_path = Path(temporary.name)

        os.replace(
            temporary_path,
            target,
        )

        temporary_path = None
    except PermissionError as error:
        msg = f"Permission denied while writing file: {target}."
        raise FilesystemPermissionError(msg) from error
    finally:
        if temporary_path is not None:
            try:
                temporary_path.unlink(missing_ok=True)
            except PermissionError as error:
                msg = f"Permission denied while cleaning temporary file: {target}."
                raise FilesystemPermissionError(msg) from error
