# Copyright (c) 2026
"""Tests for regex value objects."""

from __future__ import annotations

from dataclasses import FrozenInstanceError
from typing import Any

import pytest

from devtools.regex import RegexMatch


def test_regex_match_exposes_immutable_match_data() -> None:
    """A match exposes offsets and captured groups through immutable values."""
    match = RegexMatch(
        "whole",
        2,
        7,
        ("first", None),
        (("name", "value"),),
    )
    expected_length = 7 - 2

    assert match.span == (2, 7)
    assert match.length == expected_length
    assert match.group(0) == "first"
    assert match.group(1) is None
    assert match.named_group("name") == "value"
    assert match == RegexMatch(
        "whole",
        2,
        7,
        ("first", None),
        (("name", "value"),),
    )
    equivalent = RegexMatch(
        "whole",
        2,
        7,
        ("first", None),
        (("name", "value"),),
    )

    assert len({match, equivalent}) == 1

    with pytest.raises(IndexError):
        match.group(2)

    with pytest.raises(KeyError):
        match.named_group("missing")

    mutable_match: Any = match

    with pytest.raises(FrozenInstanceError):
        mutable_match.start = 0


@pytest.mark.parametrize(
    ("start", "end", "match"),
    [(-1, 0, "cannot be negative"), (2, 1, "cannot precede")],
)
def test_regex_match_rejects_invalid_offsets(
    start: int,
    end: int,
    match: str,
) -> None:
    """Match offsets must form a non-negative ordered span."""
    with pytest.raises(ValueError, match=match):
        RegexMatch("value", start, end)
