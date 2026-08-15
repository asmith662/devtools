# Copyright (c) 2026
"""Tests for immutable Markdown section values."""

from __future__ import annotations

import pytest

from devtools.filesystem import MarkdownHeading, MarkdownSection


def test_section_exposes_boundaries_and_normalized_string_forms() -> None:
    """Sections expose inclusive source ranges and heading-derived metadata."""
    heading = MarkdownHeading(2, "Architecture", 4)
    section = MarkdownSection(heading, "Intro\n\nDetails", 4, 7)
    empty = MarkdownSection(heading, "", 4, 4)
    expected_level = 2
    expected_line_count = 4

    assert section.level == expected_level
    assert section.title == "Architecture"
    assert section.line_count == expected_line_count
    assert section.contains_line(4) is True
    assert section.contains_line(7) is True
    assert section.contains_line(8) is False
    assert str(section) == "## Architecture\nIntro\n\nDetails"
    assert str(empty) == "## Architecture"
    assert section == MarkdownSection(heading, "Intro\n\nDetails", 4, 7)
    assert hash(section) == hash(MarkdownSection(heading, "Intro\n\nDetails", 4, 7))

    with pytest.raises(AttributeError):
        section.content = "Changed"  # type: ignore[misc]


@pytest.mark.parametrize(
    ("start_line", "end_line", "heading_line", "match"),
    [
        (0, 1, 1, "positive"),
        (3, 2, 3, "cannot precede"),
        (2, 3, 1, "must match"),
    ],
)
def test_section_rejects_invalid_boundaries(
    start_line: int,
    end_line: int,
    heading_line: int,
    match: str,
) -> None:
    """Section boundaries must be positive, ordered, and heading-aligned."""
    heading = MarkdownHeading(1, "Title", heading_line)

    with pytest.raises(ValueError, match=match):
        MarkdownSection(heading, "", start_line, end_line)
