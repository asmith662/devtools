# Copyright (c) 2026
"""Filesystem format and codec resolution."""

from __future__ import annotations

from devtools.filesystem.codecs import JsonCodec
from devtools.filesystem.errors import FileFormatError
from devtools.filesystem.models import FileFormat
from devtools.paths import ResolvedPath


def resolve_file_format(path: ResolvedPath) -> FileFormat:
    """Resolve a file format from a path.

    Resolution is based on the final filename suffix. Only formats with an
    implemented codec are currently recognized.

    :param path: Resolved filesystem path.
    :returns: Resolved file format.
    :raises FileFormatError: If the path suffix has no supported format.
    """
    suffix = path.suffix.lower()

    if suffix == ".json":
        return FileFormat.JSON

    msg = f"Unsupported file format for path: {path}."
    raise FileFormatError(msg)


def resolve_codec(
    file_format: FileFormat,
) -> JsonCodec:
    """Resolve the codec for a file format.

    :param file_format: File format requiring representation conversion.
    :returns: Codec supporting the supplied format.
    :raises FileFormatError: If no codec is implemented for the format.
    """
    if file_format is FileFormat.JSON:
        return JsonCodec()

    msg = f"No codec is implemented for file format: {file_format.value!r}."
    raise FileFormatError(msg)