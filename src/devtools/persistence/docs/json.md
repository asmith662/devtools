# Persistence JSON

## API

```python
encode_session_json(session: Session) -> str
decode_session_json(text: str) -> Session
```

These functions serialize Session semantics as text only. They do not open,
read, write, or atomically replace files; compose them with `devtools.filesystem`
when file I/O is needed.

## Schema version 1

```json
{
  "schema_version": 1,
  "session": {
    "id": "...",
    "created_at": "..."
  },
  "history": [
    {
      "id": "...",
      "created_at": "...",
      "content": "...",
      "role": "user",
      "source": "user"
    }
  ],
  "conversations": [
    {
      "source": "codex",
      "value": "opaque-value"
    }
  ]
}
```

`schema_version` is required, must be an exact integer rather than `true` or
`false`, and currently must equal `1`. Unsupported versions raise
`PersistenceVersionError`; no migration or guessing occurs.

The decoder requires exact field sets at the root and every nested object.
Unknown fields, missing fields, wrong types, duplicate object keys, and
`NaN`/Infinity constants raise `PersistenceFormatError`.

## Values and ordering

Timestamps use `Timestamp.isoformat()` and `Timestamp.from_isoformat()`.
Roles use `user`, `assistant`, or `system`; sources preserve exact strings and
their existing Context validation. Conversations preserve generic opaque source
and value strings without provider parsing.

History array order is authoritative. The same Message may occur repeatedly;
each occurrence is encoded completely. Reuse of one MessageId with different
creation time, content, role, or source raises `PersistenceConflictError`.
Duplicate conversation sources are rejected. Conversations are sorted by source
only for stable output; their order has no decoded Session meaning.

Encoding uses Unicode-preserving, sorted, two-space-indented JSON with a final
newline. This is a stable output convenience for diffs and fixtures, not part
of the semantic model: decoding relies on fields and values, not whitespace or
object-key order. Message text is retained exactly, including Unicode,
whitespace, multiline content, and JSON-like text.
