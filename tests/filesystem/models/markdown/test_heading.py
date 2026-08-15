# Copyright (c) 2026
"""Tests for immutable Markdown heading values."""

from __future__ import annotations

import pytest

from devtools.filesystem import MarkdownHeading


@pytest.mark.parametrize("level", range(1, 7))
def test_heading_exposes_level_depth_marker_and_normalized_text(level: int) -> None:
    """Every valid ATX level has predictable immutable value semantics."""
    heading = MarkdownHeading(level, "Title", 3)

    assert heading.level == level
    assert heading.depth == level
    assert heading.marker == "#" * level
    assert str(heading) == f"{'#' * level} Title"
    assert heading == MarkdownHeading(level, "Title", 3)
    assert hash(heading) == hash(MarkdownHeading(level, "Title", 3))

    with pytest.raises(AttributeError):
        heading.text = "Changed"  # type: ignore[misc]


@pytest.mark.parametrize(
    ("level", "line", "match"),
    [
        (0, 1, "between"),
        (7, 1, "between"),
        (1, 0, "positive"),
    ],
)
def test_heading_rejects_invalid_source_coordinates(
    level: int,
    line: int,
    match: str,
) -> None:
    """Headings require a valid ATX level and one-based source line."""
    with pytest.raises(ValueError, match=match):
        MarkdownHeading(level, "Title", line)
