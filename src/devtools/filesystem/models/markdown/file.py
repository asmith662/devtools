# Copyright (c) 2026
"""Markdown file models."""

from __future__ import annotations

import re
from dataclasses import dataclass
from typing import ClassVar

from devtools.filesystem.models.base import FileFormat
from devtools.filesystem.models.markdown.heading import MarkdownHeading
from devtools.filesystem.models.markdown.section import MarkdownSection
from devtools.filesystem.models.text import TextFile


@dataclass(frozen=True, slots=True)
class MarkdownFile(TextFile):
    """Represent immutable Markdown source with structural access.

    The model currently recognizes ATX headings only. Headings inside fenced
    code blocks are ignored.

    :ivar content: Original decoded Markdown source.
    """

    _ATX_HEADING_PATTERN: ClassVar[re.Pattern[str]] = re.compile(
        r"^(?P<marker>#{1,6})[ \t]+(?P<text>.*?)[ \t]*#*[ \t]*$",
    )
    _FENCE_PATTERN: ClassVar[re.Pattern[str]] = re.compile(
        r"^[ \t]{0,3}(?P<fence>`{3,}|~{3,})",
    )

    @property
    def format(self) -> FileFormat:
        """Return the Markdown file format.

        :returns: Markdown file format.
        """
        return FileFormat.MARKDOWN

    @property
    def headings(self) -> tuple[MarkdownHeading, ...]:
        """Return all recognized ATX headings.

        Headings inside fenced code blocks are ignored.

        :returns: Immutable sequence of headings in source order.
        """
        return tuple(self._parse_headings())

    @property
    def sections(self) -> tuple[MarkdownSection, ...]:
        """Return all heading-rooted Markdown sections.

        A section extends from its heading through the line before the next
        heading of the same or higher level. Nested lower-level headings remain
        part of the parent section.

        :returns: Immutable sequence of sections in source order.
        """
        headings = self.headings

        return tuple(
            self._build_section(index, headings)
            for index in range(len(headings))
        )

    def find_heading(
        self,
        text: str,
        *,
        case_sensitive: bool = False,
    ) -> MarkdownHeading | None:
        """Find the first heading with matching text.

        :param text: Heading text to locate.
        :param case_sensitive: Whether matching should preserve case.
        :returns: First matching heading or ``None``.
        """
        target = text if case_sensitive else text.casefold()

        for heading in self.headings:
            candidate = (
                heading.text
                if case_sensitive
                else heading.text.casefold()
            )

            if candidate == target:
                return heading

        return None

    def find_section(
        self,
        title: str,
        *,
        case_sensitive: bool = False,
    ) -> MarkdownSection | None:
        """Find the first section with matching heading text.

        :param title: Section heading text to locate.
        :param case_sensitive: Whether matching should preserve case.
        :returns: First matching section or ``None``.
        """
        target = title if case_sensitive else title.casefold()

        for section in self.sections:
            candidate = (
                section.title
                if case_sensitive
                else section.title.casefold()
            )

            if candidate == target:
                return section

        return None

    def _parse_headings(self) -> list[MarkdownHeading]:
        """Parse recognized headings from source content.

        :returns: Headings in source order.
        """
        headings: list[MarkdownHeading] = []
        active_fence: str | None = None

        for line_number, line in enumerate(
            self.content.splitlines(),
            start=1,
        ):
            fence_match = self._FENCE_PATTERN.match(line)

            if fence_match is not None:
                fence = fence_match.group("fence")

                if active_fence is None:
                    active_fence = fence
                    continue

                if fence[0] == active_fence[0] and len(fence) >= len(active_fence):
                    active_fence = None
                    continue

            if active_fence is not None:
                continue

            heading_match = self._ATX_HEADING_PATTERN.match(line)

            if heading_match is None:
                continue

            marker = heading_match.group("marker")
            text = heading_match.group("text").strip()

            headings.append(
                MarkdownHeading(
                    level=len(marker),
                    text=text,
                    line=line_number,
                ),
            )

        return headings

    def _build_section(
        self,
        index: int,
        headings: tuple[MarkdownHeading, ...],
    ) -> MarkdownSection:
        """Build one section from parsed heading boundaries.

        :param index: Index of the section heading.
        :param headings: Parsed headings in source order.
        :returns: Constructed Markdown section.
        """
        heading = headings[index]
        lines = self.content.splitlines()

        end_line = len(lines)

        for candidate in headings[index + 1 :]:
            if candidate.level <= heading.level:
                end_line = candidate.line - 1
                break

        content_lines = lines[heading.line:end_line]
        content = "\n".join(content_lines)

        return MarkdownSection(
            heading=heading,
            content=content,
            start_line=heading.line,
            end_line=end_line,
        )
