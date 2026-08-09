# Copyright (c) 2026
"""Exceptions for the :mod:`devtools.filesystem` domain."""


class FilesystemError(Exception):
    """Base exception for filesystem-domain failures."""


class FilesystemNotFoundError(FilesystemError):
    """Raised when a requested filesystem path does not exist."""


class NotAFileError(FilesystemError):
    """Raised when an operation requires a regular file."""


class FileTooLargeError(FilesystemError):
    """Raised when a file exceeds an allowed read size."""


class FilesystemPermissionError(FilesystemError):
    """Raised when a filesystem operation is denied by permissions."""


class TextDecodingError(FilesystemError):
    """Raised when file bytes cannot be decoded using the requested encoding."""


class TextEncodingError(FilesystemError):
    """Raised when text cannot be encoded using the requested encoding."""


class FileFormatError(FilesystemError):
    """Raised when file content does not conform to its expected format."""
