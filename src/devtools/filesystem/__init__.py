# Copyright (c) 2026
"""Immutable filesystem models and filesystem-domain errors."""

from devtools.filesystem.codecs import JsonCodec
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
    CsvFile,
    File,
    FileFormat,
    JsonFile,
    JsonListFile,
    JsonObjectFile,
    JsonScalar,
    JsonScalarFile,
    JsonValue,
    MarkdownFile,
    TextFile,
)

__all__ = [
    "BinaryFile",
    "CsvFile",
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
    "MarkdownFile",
    "NotAFileError",
    "TextDecodingError",
    "TextEncodingError",
    "TextFile",
]
