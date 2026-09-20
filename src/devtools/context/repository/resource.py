# Copyright (c) 2026
"""Repository resource addresses, content identity, and occurrences."""

from __future__ import annotations

import string
from dataclasses import dataclass
from pathlib import PurePosixPath, PureWindowsPath

_SHA256_HEX_LENGTH = 64


@dataclass(frozen=True, slots=True)
class RepositoryResourceAddress:
    """Represent one canonical POSIX-style path relative to a repository root."""

    value: str

    def __post_init__(self) -> None:
        """Reject empty, absolute, noncanonical, or traversing addresses."""
        if not self.value:
            msg = "Repository resource address cannot be empty."
            raise ValueError(msg)
        if "\\" in self.value:
            msg = "Repository resource address must use forward slashes."
            raise ValueError(msg)

        posix_path = PurePosixPath(self.value)
        windows_path = PureWindowsPath(self.value)
        if posix_path.is_absolute() or windows_path.drive:
            msg = "Repository resource address must be relative."
            raise ValueError(msg)

        parts = self.value.split("/")
        if any(part in {"", ".", ".."} for part in parts):
            msg = "Repository resource address must be canonical without traversal."
            raise ValueError(msg)

    @property
    def parts(self) -> tuple[str, ...]:
        """Return canonical repository-relative path components."""
        return tuple(self.value.split("/"))

    def __str__(self) -> str:
        """Return the canonical repository-relative address."""
        return self.value


@dataclass(frozen=True, slots=True)
class ContentIdentity:
    """Identify decoded UTF-8 text independently of its repository address."""

    value: str

    def __post_init__(self) -> None:
        """Validate the local SHA-256 hexadecimal representation."""
        _validate_sha256(self.value, label="Content identity")

    def __str__(self) -> str:
        """Return the local hexadecimal identity representation."""
        return self.value


@dataclass(frozen=True, slots=True)
class RepositoryResourceOccurrence:
    """Retain one addressed text occurrence and its independent content identity."""

    address: RepositoryResourceAddress
    content_identity: ContentIdentity
    content: str
    encoding: str
    byte_size: int


def _validate_sha256(value: str, *, label: str) -> None:
    """Validate one lowercase SHA-256 hexadecimal representation."""
    if len(value) != _SHA256_HEX_LENGTH or any(
        character not in string.hexdigits for character in value
    ):
        msg = f"{label} must be a 64-character hexadecimal SHA-256 value."
        raise ValueError(msg)
    if value != value.lower():
        msg = f"{label} must use lowercase hexadecimal."
        raise ValueError(msg)
