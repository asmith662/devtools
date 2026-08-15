# Copyright (c) 2026
"""Markdown heading models."""

from __future__ import annotations

from dataclasses import dataclass
from typing import ClassVar


@dataclass(frozen=True, slots=True)
class MarkdownHeading:
    """Represent one ATX Markdown heading.

    :ivar level: Heading level from 1 through 6.
    :ivar text: Heading text without leading hash markers.
    :ivar line: One-based source line containing the heading.
    """

    level: int
    text: str
    line: int

    MAX_LEVEL: ClassVar[int] = 6

    def __post_init__(self) -> None:
        """Validate Markdown heading invariants."""
        self._validate()

    def _validate(self) -> None:
        """Validate the heading.

        :raises ValueError: If the heading level or line number is invalid.
        """
        if not 1 <= self.level <= self.MAX_LEVEL:
            msg = "Markdown heading level must be between 1 and 6."
            raise ValueError(msg)

        if self.line < 1:
            msg = "Markdown heading line must be positive."
            raise ValueError(msg)

    @property
    def depth(self) -> int:
        """Return the heading nesting depth.

        :returns: Heading depth equivalent to its Markdown level.
        """
        return self.level

    @property
    def marker(self) -> str:
        """Return the ATX heading marker.

        :returns: Hash-marker representation for the heading level.
        """
        return "#" * self.level

    def __str__(self) -> str:
        """Return the normalized ATX heading representation.

        :returns: Markdown heading text.
        """
        return f"{self.marker} {self.text}"
