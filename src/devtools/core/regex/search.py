# Copyright (c) 2026
"""Regular-expression search operations."""

from __future__ import annotations

import re
from re import Pattern
from typing import TYPE_CHECKING

from devtools.core.regex.models import RegexMatch

if TYPE_CHECKING:
    from collections.abc import Iterator

type RegexPattern = str | Pattern[str]


def compile_regex(
    pattern: RegexPattern,
    *,
    flags: int = 0,
) -> Pattern[str]:
    """Compile a regular-expression pattern.

    A previously compiled pattern is returned unchanged when no additional
    flags are supplied.

    :param pattern: String or compiled regular-expression pattern.
    :param flags: Standard-library regular-expression flags.
    :returns: Compiled regular-expression pattern.
    :raises ValueError: If flags are supplied with an already compiled pattern.
    """
    if isinstance(pattern, Pattern):
        if flags:
            msg = "Flags cannot be supplied with an already compiled regex."
            raise ValueError(msg)

        return pattern

    return re.compile(pattern, flags)


def search_regex(
    text: str,
    pattern: RegexPattern,
    *,
    flags: int = 0,
) -> RegexMatch | None:
    """Return the first matching regular-expression result.

    :param text: Text to search.
    :param pattern: Regular-expression pattern.
    :param flags: Standard-library regular-expression flags.
    :returns: First match or ``None``.
    """
    match = compile_regex(pattern, flags=flags).search(text)

    if match is None:
        return None

    return _to_regex_match(match)


def find_all_regex(
    text: str,
    pattern: RegexPattern,
    *,
    flags: int = 0,
) -> tuple[RegexMatch, ...]:
    """Return all non-overlapping regular-expression matches.

    :param text: Text to search.
    :param pattern: Regular-expression pattern.
    :param flags: Standard-library regular-expression flags.
    :returns: Immutable sequence of matches.
    """
    return tuple(iter_regex(text, pattern, flags=flags))


def iter_regex(
    text: str,
    pattern: RegexPattern,
    *,
    flags: int = 0,
) -> Iterator[RegexMatch]:
    """Iterate lazily over non-overlapping matches.

    :param text: Text to search.
    :param pattern: Regular-expression pattern.
    :param flags: Standard-library regular-expression flags.
    :yields: Regular-expression matches.
    """
    compiled = compile_regex(pattern, flags=flags)

    for match in compiled.finditer(text):
        yield _to_regex_match(match)


def replace_regex(
    text: str,
    pattern: RegexPattern,
    replacement: str,
    *,
    count: int = 0,
    flags: int = 0,
) -> str:
    """Replace regular-expression matches.

    :param text: Source text.
    :param pattern: Regular-expression pattern.
    :param replacement: Replacement expression.
    :param count: Maximum replacements; zero means unlimited.
    :param flags: Standard-library regular-expression flags.
    :returns: Updated text.
    """
    return compile_regex(pattern, flags=flags).sub(
        replacement,
        text,
        count=count,
    )


def _to_regex_match(match: re.Match[str]) -> RegexMatch:
    """Convert a standard-library match.

    :param match: Standard-library regex match.
    :returns: Immutable regex match.
    """
    return RegexMatch(
        value=match.group(0),
        start=match.start(),
        end=match.end(),
        groups=match.groups(),
        named_groups=tuple(match.groupdict().items()),
    )
