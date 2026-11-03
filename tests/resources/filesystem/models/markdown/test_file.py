# Copyright (c) 2026
"""Tests for Markdown structural interpretation."""

from __future__ import annotations

import re
from typing import TYPE_CHECKING

import pytest

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


@pytest.mark.parametrize(
    ("source", "expected"),
    [
        ("# C#", "C#"),
        ("### F##  ", "F##"),
        ("## alpha#beta###", "alpha#beta###"),
        ("# end#\t", "end#"),
        ("# C## ###", "C##"),
        ("# word ### tail#", "word ### tail#"),
        ("# word\t####\t ", "word"),
        ("# Plain ###", "Plain"),
        (r"# x \#", r"x \#"),
        (r"# foo #\##", r"foo #\##"),
        ("# hashes ### #", "hashes ###"),
        ("# ### #", "###"),
        ("# word\u00a0###", "word\u00a0###"),
        ("# trailing # tail", "trailing # tail"),
        ("###### Plain", "Plain"),
        ("# \t", ""),
    ],
)
def test_atx_titles_strip_only_separated_terminal_hashes(
    tmp_path: Path,
    source: str,
    expected: str,
) -> None:
    """Literal suffixes survive while space/tab-delimited closing runs disappear."""
    content = source + "\nBody\n"
    file = MarkdownFile(ResolvedPath(tmp_path / "hash-titles.md"), content)
    (heading,) = file.headings
    (section,) = file.sections

    assert heading.text == expected
    assert file.find_heading(expected, case_sensitive=True) == heading
    assert file.find_section(expected, case_sensitive=True) == section
    assert section.title == expected
    assert section.content == "Body"
    assert file.content == content


@pytest.mark.parametrize("level", [1, 2, 6])
@pytest.mark.parametrize("separator", [" ", "\t", "  "])
@pytest.mark.parametrize("closing_length", [1, 2, 7])
def test_closing_hashes_preserve_empty_atx_titles(
    tmp_path: Path,
    level: int,
    separator: str,
    closing_length: int,
) -> None:
    """Keep the 27 revealed post-hoc empty-title cases as public regressions."""
    source = "#" * level + separator + "#" * closing_length + "\nBody\n"
    file = MarkdownFile(ResolvedPath(tmp_path / "empty-title.md"), source)
    (heading,) = file.headings
    (section,) = file.sections

    assert (heading.level, heading.text, heading.line) == (level, "", 1)
    assert file.find_heading("", case_sensitive=True) == heading
    assert file.find_section("", case_sensitive=True) == section
    assert (section.title, section.start_line, section.end_line) == ("", 1, 2)
    assert section.content == "Body"
    assert file.content == source


def test_hash_titles_preserve_crlf_sections_and_fence_boundaries(
    tmp_path: Path,
) -> None:
    """Hash-bearing and empty titles retain level, lookup and source contracts."""
    source = (
        "# Root#\r\nBody\r\n## Child## ###\r\nData\r\n"
        "```text\r\n# hidden#\r\n```\r\n# ##\r\nEmpty\r\n# NEXT#\r\nDone\r\n"
    )
    file = MarkdownFile(ResolvedPath(tmp_path / "hash-sections.md"), source)

    assert [(h.level, h.text, h.line) for h in file.headings] == [
        (1, "Root#", 1),
        (2, "Child##", 3),
        (1, "", 8),
        (1, "NEXT#", 10),
    ]
    assert [(s.title, s.start_line, s.end_line) for s in file.sections] == [
        ("Root#", 1, 7),
        ("Child##", 3, 7),
        ("", 8, 9),
        ("NEXT#", 10, 11),
    ]
    assert file.find_heading("next#") == file.headings[-1]
    assert file.find_section("next#") == file.sections[-1]
    assert file.sections[-1].content == "Done"
    assert file.find_heading("hidden#") is None
    assert file.find_section("hidden#") is None
    assert file.content == source


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


@pytest.mark.parametrize("marker", ["`", "~"])
@pytest.mark.parametrize("closer", ["text-suffix", "shorter", "other-marker", "longer"])
def test_fence_closer_requires_matching_markers_and_no_text_suffix(
    tmp_path: Path,
    marker: str,
    closer: str,
) -> None:
    """Keep all eight independently accepted fence scenarios as regressions."""
    opening = marker * 4
    other = ("~" if marker == "`" else "`") * 4
    candidates = {
        "text-suffix": opening + "not-a-closer",
        "shorter": marker * 3,
        "other-marker": other,
    }
    if closer == "longer":
        source = opening + "python\n# hidden\n" + marker * 5 + "\n# visible\n"
    else:
        source = (
            opening
            + "python\n"
            + candidates[closer]
            + "\n# hidden\n"
            + opening
            + " \t\n# visible\n"
        )
    file = MarkdownFile(ResolvedPath(tmp_path / "regression.md"), source)
    assert tuple(heading.text for heading in file.headings) == ("visible",)
    assert file.find_section("hidden") is None
