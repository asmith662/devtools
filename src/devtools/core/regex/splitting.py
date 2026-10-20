# Copyright (c) 2026
"""Regular-expression splitting operations."""

from __future__ import annotations

from typing import TYPE_CHECKING

from devtools.core.regex.search import RegexPattern, compile_regex

if TYPE_CHECKING:
    from re import Pattern

type SplitPiece = str | None


def split_regex(
    text: str,
    pattern: RegexPattern,
    *,
    maxsplit: int = 0,
    flags: int = 0,
) -> tuple[SplitPiece, ...]:
    """Split text by regular-expression matches.

    Mirrors :func:`re.split`, preserving captured groups and unmatched
    optional captures, while accepting the package's string or compiled
    pattern representation.

    :param text: Text to split.
    :param pattern: Regular-expression pattern.
    :param maxsplit: Maximum splits; zero means unlimited.
    :param flags: Standard-library regular-expression flags.
    :returns: Immutable tuple of split pieces; captured groups and unmatched
        optional captures are included, with ``None`` for missing groups.
    :raises ValueError: If flags are supplied with an already compiled pattern.
    :raises re.error: If the pattern cannot be compiled.
    """
    compiled: Pattern[str] = compile_regex(pattern, flags=flags)
    pieces: list[SplitPiece] = compiled.split(text, maxsplit=maxsplit)

    return tuple(pieces)
