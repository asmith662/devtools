# `devtools.regex`

## Purpose

`devtools.regex` is a small reusable layer over Python's `re` module. It
provides stable explicit operation names, interoperable string and compiled
patterns, and immutable match values without hiding standard-library regex
semantics.

## Public API

```python
from devtools.regex import (
    RegexMatch,
    RegexPattern,
    compile_regex,
    find_all_regex,
    iter_regex,
    replace_regex,
    search_regex,
)
```

| Group       | API                                |
|-------------|------------------------------------|
| Types       | `RegexPattern`, `RegexMatch`       |
| Compilation | `compile_regex()`                  |
| Search      | `search_regex()`                   |
| Iteration   | `iter_regex()`, `find_all_regex()` |
| Replacement | `replace_regex()`                  |

## Pattern handling

`RegexPattern` is `str | Pattern[str]`. String patterns are compiled when an
operation uses them. Existing `Pattern[str]` values can be reused directly:

```python
compiled = compile_regex(r"item-(\d+)")
same_pattern = compile_regex(compiled)
assert same_pattern is compiled
```

Additional flags apply only to string patterns. Passing nonzero `flags` with
an already compiled pattern raises `ValueError`, because its flags are already
part of that pattern.

## `RegexMatch`

`RegexMatch` is a frozen, slotted, value-based match representation:

```python
RegexMatch(
    value="item-17",
    start=0,
    end=7,
    groups=("17",),
    named_groups=(("number", "17"),),
)
```

`value` is the complete matched text. `start` is inclusive, `end` is
exclusive, `span` returns `(start, end)`, and `length` returns `end - start`.
Offsets must satisfy `start >= 0` and `end >= start`. Capture storage is
immutable; equality and hashing are value-based.

### Capture indexing differs from `re.Match`

This is intentional and important: `RegexMatch.group()` indexes the stored
capture tuple, not the complete match.

```python
match.value       # complete match, for example "item-17"
match.group(0)    # first captured group, for example "17"
match.group(1)    # second captured group
```

This differs from `re.Match.group(0)`, which returns the complete match.
Optional unmatched captures are `None`. Unknown numeric capture indexes raise
`IndexError`. Named captures are available through `named_group(name)` and an
unknown name raises `KeyError`.

## Search APIs

The search operations differ only in result shape:

| Operation | Result |
|---|---|
| `search_regex()` | First match or `None` |
| `iter_regex()` | Lazy generator of matches |
| `find_all_regex()` | Eager immutable tuple of matches |

All use standard-library non-overlapping, source-order matching semantics.
`iter_regex()` is based on `Pattern.finditer()` and performs work as callers
consume it. `find_all_regex()` materializes `tuple(iter_regex(...))`; no
matches produce `()`.

Offsets always refer to the supplied source text, but `RegexMatch` retains
only the matched text and captures, not the full source. Zero-width matching
follows Python `re` semantics.

## Replacement

```python
replace_regex(text, pattern, replacement, *, count=0, flags=0)
```

Replacement is currently a string and delegates to `Pattern.sub()`. A
`count` of zero means unlimited replacements. Standard Python replacement
backreferences are available, and invalid replacement expressions retain the
standard-library error behavior. Callable replacements are not part of this
API.

## Error semantics

The package intentionally exposes Python regex and protocol errors rather
than defining a parallel regex-specific hierarchy:

| Condition | Error |
|---|---|
| Invalid regex syntax | Standard-library regex error |
| Compiled pattern with extra flags | `ValueError` |
| Invalid `RegexMatch` offsets | `ValueError` |
| Unknown capture index | `IndexError` |
| Unknown named capture | `KeyError` |
| Invalid replacement expression | Standard-library regex error behavior |

## Dependencies and consumers

`devtools.regex` depends only on Python standard-library regex and typing
facilities. It has no dependency on another `devtools` package.

Its primary production consumer is `devtools.filesystem.models.TextFile`,
which provides `search_regex()` and `find_all_regex()` as file-oriented
wrappers. JSON, CSV, and Markdown text-derived models inherit that behavior:

```text
devtools.regex
    generic regex mechanics
        ↑
TextFile
    file-oriented wrappers
        ↑
JSON / CSV / Markdown text-derived models
```

The dependency direction is `filesystem -> regex`, never the reverse.

## Boundaries

This package owns regex compilation, search, iteration, replacement, and
immutable match representation. It does not own fuzzy search, literal file
search, document querying, predicate systems, filesystem traversal, search
indexing, or language-specific parsing.

## Limitations

- Callable replacements are not supported.
- There is no overlapping-match API or line/column metadata.
- There is no custom regex compilation cache.
- `RegexMatch` does not retain its complete source text.
- `RegexMatch.group(0)` differs from `re.Match.group(0)` as described above.

## Future evolution

Callable replacements, line/column metadata, or overlapping-match support
should be added only if concrete consumers require them. A custom cache, a
precompiled-regex value object, and split or escape wrappers are not currently
justified because Python's `re` module already provides suitable mechanisms.
