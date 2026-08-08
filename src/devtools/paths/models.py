# Copyright (c) 2026
"""Path value objects."""

from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True, slots=True)
class ResolvedPath(os.PathLike[str]):
    """Represent an absolute resolved filesystem path.

    :ivar path: Absolute filesystem path.
    """

    path: Path

    def __post_init__(self) -> None:
        """Validate path invariants.

        :raises ValueError: If the path is not absolute.
        """
        if not self.path.is_absolute():
            msg = "ResolvedPath requires an absolute path."
            raise ValueError(msg)

    @property
    def name(self) -> str:
        """Return the final path component.

        :returns: Final component of the path.
        """
        return self.path.name

    @property
    def stem(self) -> str:
        """Return the final component without its last suffix.

        :returns: Stem of the final component.
        """
        return self.path.stem

    @property
    def suffix(self) -> str:
        """Return the final path suffix.

        :returns: Final suffix.
        """
        return self.path.suffix

    @property
    def suffixes(self) -> tuple[str, ...]:
        """Return all suffixes.

        :returns: Immutable sequence of suffixes.
        """
        return tuple(self.path.suffixes)

    @property
    def parts(self) -> tuple[str, ...]:
        """Return the path components.

        :returns: Immutable sequence of path components.
        """
        return self.path.parts

    def as_posix(self) -> str:
        """Return the path using forward slashes.

        :returns: POSIX-style path representation.
        """
        return self.path.as_posix()

    def __str__(self) -> str:
        """Return the native string representation.

        :returns: Native filesystem string.
        """
        return str(self.path)

    def __fspath__(self) -> str:
        """Return the filesystem path representation.

        :returns: Native filesystem path string.
        """
        return os.fspath(self.path)