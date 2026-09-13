# Copyright (c) 2026
"""Binary filesystem models."""

from __future__ import annotations

from dataclasses import dataclass

from devtools.resources.filesystem.models.base import File, FileFormat


@dataclass(frozen=True, slots=True)
class BinaryFile(File):
    """Represent immutable binary file content.

    :ivar content: Exact file bytes retained in memory.
    :ivar truncated: Whether the retained content was truncated by a read limit.
    """

    content: bytes
    truncated: bool = False

    @property
    def format(self) -> FileFormat:
        """Return the binary file format.

        :returns: Binary file format.
        """
        return FileFormat.BINARY

    @property
    def size_bytes(self) -> int:
        """Return the number of retained content bytes.

        :returns: Retained byte count.
        """
        return len(self.content)
