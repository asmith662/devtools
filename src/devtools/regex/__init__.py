# Copyright (c) 2026
"""Regular-expression primitives for developer tooling."""

from devtools.regex.models import RegexMatch
from devtools.regex.search import (
    RegexPattern,
    compile_regex,
    find_all_regex,
    iter_regex,
    replace_regex,
    search_regex,
)

__all__ = [
    "RegexMatch",
    "RegexPattern",
    "compile_regex",
    "find_all_regex",
    "iter_regex",
    "replace_regex",
    "search_regex",
]
