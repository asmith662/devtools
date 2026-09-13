# Copyright (c) 2026
"""Tests for Markdown structural interpretation."""

from __future__ import annotations

import re
from typing import TYPE_CHECKING

from devtools.core.paths import ResolvedPath
from devtools.resources.filesystem import MarkdownFile

if TYPE_CHECKING:
    from pathlib import Path


def test_atx_headings_ignore_non_headings_and_fenced_code(tmp_path: Path) -> None:
    """Only valid ATX headings outside backtick and tilde fences are recognized."""
    source = """# Document #
##   Architecture   ###
####### too many
#no-space
ordinary # text
```python
## Hidden backtick
```
~~~text
### Hidden tilde
~~~
   ```python
### Hidden indented
   ```
###### Final
"""
    source += "#" + " " + "\n"
    file = MarkdownFile(ResolvedPath(tmp_path / "document.md"), source)

    assert tuple((item.level, item.text, item.line) for item in file.headings) == (
        (1, "Document", 1),
        (2, "Architecture", 2),
        (6, "Final", 15),
        (1, "", 16),
    )
    assert isinstance(file.headings, tuple)
    assert file.headings == file.headings


def test_heading_and_section_properties_are_empty_without_atx_source(
    tmp_path: Path,
) -> None:
    """Ordinary text does not create structural headings or sections."""
    file = MarkdownFile(
        ResolvedPath(tmp_path / "plain.md"),
        "#no-space\n####### too many\n",
    )

    assert file.headings == ()
    assert file.sections == ()


def test_long_fences_require_an_equally_long_matching_closer(tmp_path: Path) -> None:
    """A shorter same-character fence cannot end a longer opening fence."""
    source = """````python
# Still hidden
```
## Also hidden
````
# Visible
"""
    file = MarkdownFile(ResolvedPath(tmp_path / "fences.md"), source)

    assert tuple(heading.text for heading in file.headings) == ("Visible",)


def test_sections_follow_same_or_higher_heading_boundaries(tmp_path: Path) -> None:
    """Parent sections include nested headings and stop at peer/ancestor headings."""
    source = """# Document

## Architecture
Intro

### Runtime
Runtime details

### Storage
Storage details

## Testing
Tests
"""
    file = MarkdownFile(ResolvedPath(tmp_path / "sections.md"), source)
    sections = {section.title: section for section in file.sections}
    document_end_line = 13
    architecture_start_line = 3
    architecture_end_line = 11
    runtime_end_line = 8

    assert sections["Document"].end_line == document_end_line
    assert sections["Architecture"].start_line == architecture_start_line
    assert sections["Architecture"].end_line == architecture_end_line
    assert sections["Architecture"].content == (
        "Intro\n\n### Runtime\nRuntime details\n\n### Storage\nStorage details\n"
    )
    assert sections["Runtime"].end_line == runtime_end_line
    assert sections["Storage"].end_line == architecture_end_line
    assert sections["Testing"].end_line == document_end_line


def test_sections_handle_adjacent_and_nested_level_changes(tmp_path: Path) -> None:
    """Final, empty, and unevenly nested sections have inclusive boundaries."""
    source = """## Parent
#### Deep
### Middle
## Next
"""
    file = MarkdownFile(ResolvedPath(tmp_path / "nested.md"), source)
    parent, deep, middle, next_section = file.sections

    assert (parent.start_line, parent.end_line, parent.content) == (
        1,
        3,
        "#### Deep\n### Middle",
    )
    assert (deep.start_line, deep.end_line) == (2, 2)
    assert (middle.start_line, middle.end_line) == (3, 3)
    assert (next_section.start_line, next_section.end_line, next_section.content) == (
        4,
        4,
        "",
    )


def test_lookup_and_inherited_source_search_are_independent(tmp_path: Path) -> None:
    """Structural lookups coexist with source-text and regex accessors."""
    source = """# Intro
text
## INTRO
details
"""
    file = MarkdownFile(ResolvedPath(tmp_path / "lookup.md"), source)

    first_heading = file.find_heading("intro")
    exact_heading = file.find_heading("INTRO", case_sensitive=True)
    first_section = file.find_section("intro")
    exact_section = file.find_section("INTRO", case_sensitive=True)
    expected_second_heading_line = 3
    expected_match_count = 2

    assert first_heading is not None
    assert exact_heading is not None
    assert first_section is not None
    assert exact_section is not None
    assert first_heading.line == 1
    assert exact_heading.line == expected_second_heading_line
    assert file.find_heading("intro", case_sensitive=True) is None
    assert first_section.start_line == 1
    assert exact_section.start_line == expected_second_heading_line
    assert file.find_section("missing") is None
    assert file.contains("details") is True
    assert file.search_regex(r"# Intro") is not None
    assert len(file.find_all_regex(r"^#+", flags=re.MULTILINE)) == expected_match_count


def test_section_content_is_normalized_logical_source(tmp_path: Path) -> None:
    """Section bodies normalize CRLF and do not retain a final source newline."""
    source = "# Title\r\nBody\r\n"
    file = MarkdownFile(ResolvedPath(tmp_path / "logical.md"), source)

    assert file.sections[0].content == "Body"
