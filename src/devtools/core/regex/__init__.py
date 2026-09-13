# Copyright (c) 2026
"""Regular-expression primitives for developer tooling."""

from devtools.core.regex.models import RegexMatch
from devtools.core.regex.search import (
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
