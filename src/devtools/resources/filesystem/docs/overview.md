# `devtools.resources.filesystem`

## Purpose

`devtools.resources.filesystem` provides immutable file models, representation codecs,
static format resolution, bounded generic reads, and atomic-replacement writes.
It supports text, JSON, Markdown, and CSV I/O; binary is currently model-only.

## Public API

The root package exports generic I/O (`read`, `write`, `resolve_file_format`,
and `DEFAULT_MAX_READ_BYTES`), codecs, `File`/`FileFormat`, concrete file
models, structured JSON/Markdown/CSV models, and filesystem errors. Internal
codec resolution remains private. JSON `freeze_json()` and `thaw_json()` remain
at the representation-model boundary rather than the root package.

| Format   | Model | Codec | Generic read/write |
|----------|------:|------:|-------------------:|
| Binary   |   Yes |    No |                 No |
| Text     |   Yes |   Yes |                Yes |
| JSON     |   Yes |   Yes |                Yes |
| CSV      |   Yes |   Yes |                Yes |
| Markdown |   Yes |   Yes |                Yes |

## Architecture

```text
ResolvedPath
    ↓
read()
    ↓
format resolution
    ↓
codec
    ↓
rich immutable File model
    ↓
format-native access / search / transformation
    ↓
write()
    ↓
codec
    ↓
atomic replacement
```

The detailed model, codec, and I/O contracts are documented in
[models.md](models.md), [codecs.md](codecs.md), and [io.md](io.md). Format
details are in [json.md](json.md), [markdown.md](markdown.md), and
[csv.md](csv.md).

## Source provenance and current state

JSON and CSV distinguish original decoded source from current structured state.
Their `.content` is source provenance; JSON `.value` and CSV `.headers`/`.rows`
are current state. Immutable transformations retain original `.content`, while
their codecs serialize current structured state. Markdown structure is derived
from authoritative `.content`; plain text has no secondary structured state.

## Dependencies

Filesystem consumes `ResolvedPath` from `devtools.core.paths`, generic regex
mechanics from `devtools.core.regex`, and callable conversion from
`devtools.core.conversion`. It does not depend on `devtools.core.system`.

## Boundaries

This package owns file models, codecs, format resolution, bounded reads,
atomic writes, and format-native access/search/transformation. It does not own
path parsing, directory traversal, repository indexing, sessions, context
compilation, watching, synchronization, authorization, or sandbox policy.

## Errors

```text
FilesystemError
├── FilesystemNotFoundError
├── NotAFileError
├── FileTooLargeError
├── FilesystemPermissionError
├── TextDecodingError
├── TextEncodingError
└── FileFormatError
```

`FileExistsError` intentionally remains the built-in failure for
`write(..., overwrite=False)`.

## Limitations

Generic I/O does not provide containment, symlink-escape prevention,
authorization, race-free limits, locking, ownership policy, secure deletion,
or parent-directory durability after power loss. See [io.md](io.md) for the
exact read and write limits.

## Future evolution

Concrete deferred work is recorded in [roadmap.md](roadmap.md). It does not
authorize dynamic codec registries, plugin discovery, repository indexing, or
filesystem security policy.
