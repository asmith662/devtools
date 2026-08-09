# Copyright (c) 2026
"""Text filesystem models."""

from __future__ import annotations

from dataclasses import dataclass

from devtools import regex
from devtools.filesystem.models.base import File, FileFormat


@dataclass(frozen=True, slots=True)
class TextFile(File):
    """Represent immutable decoded text file content.

    :ivar content: Decoded source content.
    :ivar encoding: Encoding used to decode source bytes.
    :ivar byte_size: Number of retained source bytes.
    :ivar truncated: Whether source content was truncated.
    """

    content: str
    encoding: str = "utf-8"
    byte_size: int = 0
    truncated: bool = False

    def __post_init__(self) -> None:
        """Validate text-file invariants."""
        self._validate()

    def _validate(self) -> None:
        """Validate the text file.

        :raises ValueError: If the encoding is blank or byte size is negative.
        """
        if not self.encoding.strip():
            msg = "Text file encoding cannot be empty."
            raise ValueError(msg)

        if self.byte_size < 0:
            msg = "Text file byte size cannot be negative."
            raise ValueError(msg)

    @property
    def format(self) -> FileFormat:
        """Return the text file format.

        :returns: Text file format.
        """
        return FileFormat.TEXT

    @property
    def character_count(self) -> int:
        """Return the decoded character count.

        :returns: Number of decoded characters.
        """
        return len(self.content)

    @property
    def lines(self) -> tuple[str, ...]:
        """Return immutable logical lines.

        :returns: Logical lines without newline separators.
        """
        return tuple(self.content.splitlines())

    @property
    def line_count(self) -> int:
        """Return the number of logical lines.

        :returns: Logical line count.
        """
        return len(self.lines)

    def contains(self, value: str) -> bool:
        """Return whether literal text occurs in the content.

        :param value: Literal text to locate.
        :returns: Whether the value occurs.
        """
        return value in self.content

    def search_regex(
        self,
        pattern: regex.RegexPattern,
        *,
        flags: int = 0,
    ) -> regex.RegexMatch | None:
        """Return the first matching pattern.

        :param pattern: Regular-expression pattern.
        :param flags: Standard-library regular-expression flags.
        :returns: First match or ``None``.
        """
        return regex.search_regex(
            self.content,
            pattern,
            flags=flags,
        )

    def find_all_regex(
        self,
        pattern: regex.RegexPattern,
        *,
        flags: int = 0,
    ) -> tuple[regex.RegexMatch, ...]:
        """Return all matching patterns.

        :param pattern: Regular-expression pattern.
        :param flags: Standard-library regular-expression flags.
        :returns: Immutable sequence of matches.
        """
        return regex.find_all_regex(
            self.content,
            pattern,
            flags=flags,
        )
