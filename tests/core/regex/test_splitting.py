# Copyright (c) 2026
"""Independent permanent regressions for the Qwen-authored splitting API."""

from __future__ import annotations

import re
from typing import TYPE_CHECKING

import pytest

import devtools.core.regex as public
from devtools.core.regex import split_regex
from devtools.core.regex.splitting import split_regex as implementation

if TYPE_CHECKING:
    from devtools.core.regex import RegexPattern


def test_split_is_public_and_implemented_in_its_module() -> None:
    """The maintained package exposes its actual implementation."""
    assert public.split_regex is implementation
    assert "split_regex" in public.__all__


@pytest.mark.parametrize(
    ("text", "pattern", "maximum", "flags"),
    [
        ("a,b,,c", ",", 0, 0),
        ("xbx", "(a)?b", 0, 0),
        ("AaA", "a", 0, re.IGNORECASE),
        ("abc", "", 2, 0),
        ("café 雪", r"\s+", 0, 0),
        ("", ",", 0, 0),
        ("a,b,c", re.compile(","), 1, 0),
        ("abc", ",", -1, 0),
    ],
)
def test_split_preserves_standard_semantics(
    text: str,
    pattern: RegexPattern,
    maximum: int,
    flags: int,
) -> None:
    """Captures, limits, Unicode and empty inputs follow installed re.split."""
    actual = split_regex(text, pattern, maxsplit=maximum, flags=flags)
    assert isinstance(actual, tuple)
    assert actual == tuple(re.split(pattern, text, maxsplit=maximum, flags=flags))


def test_split_preserves_compilation_errors_and_optional_captures() -> None:
    """Compiled-pattern policy is preserved alongside optional capture values."""
    assert split_regex("xbx", "(a)?b") == ("x", None, "x")
    compiled = re.compile(",", re.IGNORECASE)
    assert split_regex("a,b", compiled) == ("a", "b")
    with pytest.raises(ValueError, match="Flags cannot"):
        split_regex("a,b", compiled, flags=re.IGNORECASE)
    with pytest.raises(re.error):
        split_regex("x", "[")
