# Copyright (c) 2026
"""Markdown section models."""

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from devtools.resources.filesystem.models.markdown.heading import MarkdownHeading


@dataclass(frozen=True, slots=True)
class MarkdownSection:
    r"""Represent a Markdown section rooted at an ATX heading.

    A section begins at its heading line and extends until the next heading of
    the same or higher level, or the end of the document.

    ``content`` is normalized logical source: it is reconstructed from logical
    lines with ``\n`` separators and does not retain a final source newline.

    :ivar heading: Heading that owns the section.
    :ivar content: Section body without the heading line itself.
    :ivar start_line: One-based source line containing the heading.
    :ivar end_line: One-based inclusive final source line in the section.
    """

    heading: MarkdownHeading
    content: str
    start_line: int
    end_line: int

    def __post_init__(self) -> None:
        """Validate Markdown section invariants."""
        self._validate()

    def _validate(self) -> None:
        """Validate the section.

        :raises ValueError: If source line boundaries are invalid.
        """
        if self.start_line < 1:
            msg = "Markdown section start line must be positive."
            raise ValueError(msg)

        if self.end_line < self.start_line:
            msg = "Markdown section end line cannot precede its start line."
            raise ValueError(msg)

        if self.start_line != self.heading.line:
            msg = "Markdown section start line must match its heading line."
            raise ValueError(msg)

    @property
    def level(self) -> int:
        """Return the owning heading level.

        :returns: Markdown heading level.
        """
        return self.heading.level

    @property
    def title(self) -> str:
        """Return the section heading text.

        :returns: Heading text.
        """
        return self.heading.text

    @property
    def line_count(self) -> int:
        """Return the number of source lines occupied by the section.

        The heading line is included in the count.

        :returns: Inclusive section line count.
        """
        return self.end_line - self.start_line + 1

    def contains_line(self, line: int) -> bool:
        """Return whether a source line belongs to the section.

        :param line: One-based source line number.
        :returns: Whether the line lies within the section boundaries.
        """
        return self.start_line <= line <= self.end_line

    def __str__(self) -> str:
        """Return the normalized section source.

        :returns: Heading followed by the section body.
        """
        if not self.content:
            return str(self.heading)

        return f"{self.heading}\n{self.content}"
