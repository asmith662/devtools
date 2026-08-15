# Copyright (c) 2026
"""Immutable filesystem models and filesystem-domain errors."""

from devtools.filesystem.codecs import CsvCodec, JsonCodec, MarkdownCodec, TextCodec
from devtools.filesystem.errors import (
    FileFormatError,
    FilesystemError,
    FilesystemNotFoundError,
    FilesystemPermissionError,
    FileTooLargeError,
    NotAFileError,
    TextDecodingError,
    TextEncodingError,
)
from devtools.filesystem.models import (
    BinaryFile,
    CsvDialect,
    CsvFile,
    CsvQuoting,
    CsvRow,
    File,
    FileFormat,
    JsonFile,
    JsonListFile,
    JsonObjectFile,
    JsonScalar,
    JsonScalarFile,
    JsonValue,
    MarkdownFile,
    MarkdownHeading,
    MarkdownSection,
    TextFile,
)
from devtools.filesystem.reading import DEFAULT_MAX_READ_BYTES, read
from devtools.filesystem.resolution import resolve_file_format
from devtools.filesystem.writing import write

__all__ = [
    "DEFAULT_MAX_READ_BYTES",
    "BinaryFile",
    "CsvCodec",
    "CsvDialect",
    "CsvFile",
    "CsvQuoting",
    "CsvRow",
    "File",
    "FileFormat",
    "FileFormatError",
    "FileTooLargeError",
    "FilesystemError",
    "FilesystemNotFoundError",
    "FilesystemPermissionError",
    "JsonCodec",
    "JsonFile",
    "JsonListFile",
    "JsonObjectFile",
    "JsonScalar",
    "JsonScalarFile",
    "JsonValue",
    "MarkdownCodec",
    "MarkdownFile",
    "MarkdownHeading",
    "MarkdownSection",
    "NotAFileError",
    "TextCodec",
    "TextDecodingError",
    "TextEncodingError",
    "TextFile",
    "read",
    "resolve_file_format",
    "write",
]
