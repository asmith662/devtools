# Filesystem models

See the package [overview](overview.md) for boundaries and supported formats.

## Hierarchy

```text
File
├── BinaryFile
└── TextFile
    ├── JsonFile
    │   ├── JsonObjectFile
    │   ├── JsonListFile
    │   └── JsonScalarFile
    ├── MarkdownFile
    └── CsvFile
```

Inheritance expresses shared source representation, not interchangeable
serialization semantics. Structured models retain their own operations and
their codecs are selected explicitly by format.

## `File`

`File` is the minimal frozen, slotted base. It associates a `ResolvedPath`
with an abstract `FileFormat`. It does not promise text, structured values,
serialization, or universal hashability.

Models are immutable and value-oriented, but hashability is not universal:
recursively immutable JSON mappings use `MappingProxyType`, which is not
hashable. Equality remains predictable; callers must not assume every file
model can be used as a dictionary key.

## Binary and text

`BinaryFile` stores immutable `bytes`, a `truncated` flag, and `size_bytes` for
the retained byte count. It is currently model-only; there is no BinaryCodec or
generic binary I/O.

`TextFile` stores `content`, `encoding`, `byte_size`, and `truncated`. It
provides `character_count`, literal `contains()`, and regex wrappers
`search_regex()` / `find_all_regex()`. It deliberately has no `__iter__()`.
Logical lines are exactly `tuple(content.splitlines())`: separators are
removed, and a final newline does not retain a terminal empty line.

## Provenance

JSON and CSV `.content` is original decoded source provenance. Their structured
state can diverge through immutable transformations; codecs persist that state
rather than stale source. Markdown headings/sections are derived from
authoritative `.content`; TextFile has no secondary state.

See [json.md](json.md), [markdown.md](markdown.md), and [csv.md](csv.md) for
format-specific models.
