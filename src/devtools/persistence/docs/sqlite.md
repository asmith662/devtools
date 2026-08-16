# Persistence SQLite

## Store API and initialization

```python
store = SqliteSessionStore(database=resolved_path)
store.save(session)
loaded = store.load(session.id)  # Session | None
```

`database` is a `ResolvedPath`; construction is side-effect-free and does not
create parent directories. Each operation opens and closes one SQLite
connection, enables foreign keys, and uses normal SQLite operational-error and
file-locking behavior. There is no retained connection, custom retry/backoff,
WAL configuration, async API, or `:memory:` mode.

SQLite physical schema version uses `PRAGMA user_version = 1`, independently of
the JSON schema version. A version-0 database with no user tables is initialized
lazily. Consequently, `load()` on a brand-new database path creates the empty
Persistence schema and returns `None` for the missing Session. A version-0
database with any user table is rejected. Version-1 databases must contain the
Persistence tables and their required columns; extra columns are tolerated.
Unsupported versions are rejected without mutation.

## Normalized current snapshot

```text
sessions          Session ID and creation time
messages          globally keyed immutable Message values
session_messages  zero-based ordered History occurrences
conversations     current Session/source-keyed opaque continuation values
```

`session_messages.position` is authoritative and must load as `0..N-1`.
Every occurrence must resolve to a Message row; missing referenced rows and
invalid reconstructed semantic values fail with `PersistenceFormatError` rather
than yielding a partial Session. The same MessageId may occur multiple times in
one Session or across Sessions, while one global Message row represents its
immutable value.

## Save, conflict, and load semantics

`save()` atomically replaces one Session's current occurrence and conversation
associations. A shorter reconstructed Session therefore removes stale persisted
occurrences and refs. A returned/current ref for a source replaces the older
ref; different sources coexist.

An existing SessionId with a different creation time, or an existing MessageId
with different immutable Message fields, raises `PersistenceConflictError`.
The failed save rolls back all candidate Session, Message, occurrence, and
conversation changes. Equal existing Message rows are reused. Orphan Message
rows are retained; no delete or garbage-collection policy exists.

`load()` returns a new Session or `None`. It reconstructs through the shared
semantic restoration path and therefore receives fresh local `Session.turn()`
coordination. It does not restore lock state.

## Boundaries and queryability

The normalized schema supports future querying by Session creation time,
MessageId, source, and ordered History, but this milestone exposes no query or
delete API. SQLite persists plaintext Message content and ConversationRef values
under normal local filesystem permissions; it provides no encryption, access
control, or credential protection.

Persistence does not acquire `Session.turn()`. When Runtime could mutate a
Session concurrently, callers must hold `session.turn()` while capturing a
coordinated synchronous snapshot. Persistence remains provider-neutral:
ConversationRef values are opaque, and Codex is acceptance evidence rather
than a production dependency.
