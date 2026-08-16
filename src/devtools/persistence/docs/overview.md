# Persistence

## Purpose

`devtools.persistence` durably represents and reconstructs the semantic state
of a `Session` while `devtools.context` remains storage-agnostic. It provides
strict portable JSON text serialization and a normalized SQLite current-snapshot
store.

```python
from devtools.persistence import (
    SqliteSessionStore,
    decode_session_json,
    encode_session_json,
)
```

The public root also exports `PersistenceError`, `PersistenceFormatError`,
`PersistenceVersionError`, and `PersistenceConflictError`.

## Semantic snapshot and reconstruction

Persistence stores Session ID, creation time, ordered History occurrences, and
current `ConversationRef` values. Each Message occurrence retains Message ID,
creation time, content, role, and source.

It does not store Session turn-lock state or event-loop binding, Runtime,
Agents, Codex configuration or process state, working-directory/sandbox/model
configuration, credentials, or provider state beyond opaque ConversationRefs.

Decoding or loading creates a new Session with equal semantic state and fresh
object-local `Session.turn()` coordination. Persistence preserves value
semantics, not Python object identity across the reconstruction boundary.

JSON and SQLite use the same private semantic capture/restoration seam so they
reconstruct the same Session model. That seam is implementation detail, not a
public record API.

## Formats and boundaries

JSON is portable strict text serialization; it performs no file I/O.
`devtools.filesystem` remains responsible for any file read/write composition.
SQLite is a normalized, queryable current-snapshot representation; its public
store operations are only `save()` and `load()`.

Persistence depends on generic Context, Agent continuation, Time, and path
contracts. It does not depend on Runtime, Codex, or Filesystem in production.
Runtime can immediately use a loaded Session, but Persistence does not invoke
Agents or coordinate Runtime turns.

The opt-in SQLite acceptance reconstructs a Session after a real Codex turn,
then proves Runtime resumes the same thread from the restored continuation in
an isolated temporary Git repository.

## Errors

`PersistenceFormatError` identifies malformed persisted representations;
`PersistenceVersionError` identifies unsupported JSON or SQLite versions; and
`PersistenceConflictError` identifies conflicting immutable Message or Session
identity state. Operational SQLite errors remain SQLite errors. Diagnostics do
not include Message content, ConversationRef values, or full payloads.

## Coordination, security, and limits

Persistence does not acquire `Session.turn()`. A caller saving a Session that
may overlap Runtime mutation must coordinate the snapshot itself:

```python
async with session.turn():
    store.save(session)
```

Persistence does not provide Session thread safety, cross-process coordination,
retry/backoff, encryption, access control, credential protection, retention
limits, deletion, garbage collection, migrations, async wrappers, or generic
storage backends. JSON and SQLite store Message content and ConversationRef
values as plaintext under normal filesystem permissions.

Current saves rewrite one Session's occurrence and conversation snapshot; JSON
repeats Message bodies for repeated History occurrences. Both are intentional
first-milestone tradeoffs. The normalized identity model leaves room for future
Evidence to reference SessionId and MessageId without placing Evidence in
Session persistence.
