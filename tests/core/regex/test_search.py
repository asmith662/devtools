# Copyright (c) 2026
"""Tests for regex search operations."""

from __future__ import annotations

import re

import pytest

from devtools.core.regex import (
    RegexPattern,
    compile_regex,
    find_all_regex,
    iter_regex,
    replace_regex,
    search_regex,
)


def test_regex_pattern_is_available_from_the_package_root() -> None:
    """The public pattern alias accepts source text at the package boundary."""
    pattern: RegexPattern = "abc"

    assert compile_regex(pattern).pattern == "abc"


def test_compile_regex_supports_strings_and_compiled_patterns() -> None:
    """Compilation preserves a supplied pattern and applies flags to strings."""
    compiled = compile_regex("abc", flags=re.IGNORECASE)
    existing = re.compile("abc")

    assert compiled.search("ABC") is not None
    assert compile_regex(existing) is existing

    with pytest.raises(ValueError, match="Flags cannot"):
        compile_regex(existing, flags=re.IGNORECASE)


def test_search_find_iteration_replacement_and_flags() -> None:
    """Regex operations preserve match structure and standard flag behavior."""
    text = "A-1 a-22"
    pattern = r"(?P<letter>a)-(\d+)"

    first = search_regex(text, pattern, flags=re.IGNORECASE)
    matches = find_all_regex(text, pattern, flags=re.IGNORECASE)
    lazy_matches = tuple(iter_regex(text, pattern, flags=re.IGNORECASE))
    expected_match_count = len(("A-1", "a-22"))

    assert first is not None
    assert first.value == "A-1"
    assert first.groups == ("A", "1")
    assert first.named_groups == (("letter", "A"),)
    assert matches == lazy_matches
    assert len(matches) == expected_match_count
    assert search_regex(text, "missing") is None
    assert replace_regex(text, r"\d+", "#", count=1) == "A-# a-22"


def test_regex_operations_preserve_standard_library_edge_semantics() -> None:
    """Zero-width matches, syntax errors, and replacements follow ``re``."""
    matches = tuple(iter_regex("aa", r"(?=a)"))

    assert tuple(match.span for match in matches) == ((0, 0), (1, 1))
    assert replace_regex("a-1 b-2", r"([a-z])-(\d)", r"\2:\1") == "1:a 2:b"

    with pytest.raises(re.error):
        compile_regex("[")
