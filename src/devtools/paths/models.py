# Copyright (c) 2026
"""Immutable path value objects."""

from __future__ import annotations

import os
from dataclasses import dataclass
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from pathlib import Path


@dataclass(frozen=True, slots=True)
class ResolvedPath(os.PathLike[str]):
    """Represent an immutable absolute filesystem path.

    The model validates only that its value is absolute. Filesystem
    normalization and resolution are performed by the path-resolution
    operations.

    :ivar value: Absolute filesystem path.
    """

    value: Path

    def __post_init__(self) -> None:
        """Validate model invariants."""
        self._validate()

    def _validate(self) -> None:
        """Validate the resolved path value.

        :raises ValueError: If the path is not absolute.
        """
        if not self.value.is_absolute():
            msg = "ResolvedPath requires an absolute path."
            raise ValueError(msg)

    @property
    def name(self) -> str:
        """Return the final path component.

        :returns: Final path component.
        """
        return self.value.name

    @property
    def stem(self) -> str:
        """Return the final component without its last suffix.

        :returns: Final component stem.
        """
        return self.value.stem

    @property
    def suffix(self) -> str:
        """Return the final path suffix.

        :returns: Final suffix, including the leading period when present.
        """
        return self.value.suffix

    @property
    def suffixes(self) -> tuple[str, ...]:
        """Return all suffixes for the final path component.

        :returns: Immutable sequence of suffixes.
        """
        return tuple(self.value.suffixes)

    @property
    def parent(self) -> Path:
        """Return the parent filesystem path.

        :returns: Parent path.
        """
        return self.value.parent

    @property
    def parts(self) -> tuple[str, ...]:
        """Return the filesystem path components.

        :returns: Immutable sequence of path components.
        """
        return self.value.parts

    def as_posix(self) -> str:
        """Return the path using forward slashes.

        :returns: POSIX-style path representation.
        """
        return self.value.as_posix()

    def as_uri(self) -> str:
        """Return the path as a file URI.

        :returns: File URI representation.
        """
        return self.value.as_uri()

    def __str__(self) -> str:
        """Return the native filesystem representation.

        :returns: Native path string.
        """
        return str(self.value)

    def __fspath__(self) -> str:
        """Return the filesystem path protocol representation.

        :returns: Native filesystem path string.
        """
        return os.fspath(self.value)
