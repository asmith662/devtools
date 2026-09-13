# Copyright (c) 2026
"""Filesystem format and codec resolution."""

from __future__ import annotations

from typing import TYPE_CHECKING

from devtools.resources.filesystem.codecs import (
    CsvCodec,
    JsonCodec,
    MarkdownCodec,
    TextCodec,
)
from devtools.resources.filesystem.errors import FileFormatError
from devtools.resources.filesystem.models import FileFormat

if TYPE_CHECKING:
    from devtools.core.paths import ResolvedPath

_SUFFIX_FORMATS = {
    ".csv": FileFormat.CSV,
    ".json": FileFormat.JSON,
    ".md": FileFormat.MARKDOWN,
    ".markdown": FileFormat.MARKDOWN,
    ".txt": FileFormat.TEXT,
}
_CODEC_TYPES: dict[
    FileFormat,
    type[CsvCodec | JsonCodec | MarkdownCodec | TextCodec],
] = {
    FileFormat.CSV: CsvCodec,
    FileFormat.JSON: JsonCodec,
    FileFormat.MARKDOWN: MarkdownCodec,
    FileFormat.TEXT: TextCodec,
}


def resolve_file_format(path: ResolvedPath) -> FileFormat:
    """Resolve a file format from a path.

    Resolution is based on the final filename suffix. Only formats with an
    implemented codec are currently recognized.

    :param path: Resolved filesystem path.
    :returns: Resolved file format.
    :raises FileFormatError: If the path suffix has no supported format.
    """
    suffix = path.suffix.lower()

    try:
        return _SUFFIX_FORMATS[suffix]
    except KeyError as error:
        msg = f"Unsupported file format for path: {path}."
        raise FileFormatError(msg) from error


def resolve_codec(
    file_format: FileFormat,
) -> CsvCodec | JsonCodec | MarkdownCodec | TextCodec:
    """Resolve the codec for a file format.

    :param file_format: File format requiring representation conversion.
    :returns: Codec supporting the supplied format.
    :raises FileFormatError: If no codec is implemented for the format.
    """
    try:
        codec_type = _CODEC_TYPES[file_format]
    except KeyError as error:
        msg = f"No codec is implemented for file format: {file_format.value!r}."
        raise FileFormatError(msg) from error

    return codec_type()
