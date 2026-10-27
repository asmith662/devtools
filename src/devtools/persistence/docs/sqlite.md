# SQLite conversation persistence

The SQLite store saves and loads durable `Conversation` state. It preserves the
established normalized schema and historical table or column names such as
`sessions`, `session_messages`, and `session_id` for compatibility. Those names
are schema identifiers, not active `Session` terminology.

Saving replaces one conversation's persisted history and continuation snapshot
atomically within the store transaction. It does not acquire Conversation turn
coordination, provide cross-process execution locking, or make external effects
exactly once.

Each load holds one explicit SQLite read transaction across the session,
ordered messages and source-keyed references. WAL readers may retain an older
committed snapshot while another connection commits. With rollback journaling,
an active reader can make a writer wait or report SQLite's normal busy error.
Missing records still return `None`; all read transactions and connections are
settled on ordinary return or failure.

Fresh initialization reserves a SQLite write transaction, rechecks the schema
version after obtaining it, and installs the existing tables, indexes and version
together. It executes the owned DDL statements individually; `executescript`
would implicitly commit an existing legacy transaction. Intermediate failure
rolls back to the original empty schema, permitting a later ordinary retry.
An already initialized concurrent caller is validated normally. Unknown nonempty
version-zero databases, including old partial installations, remain refused and
are never automatically deleted, overwritten or migrated.

Stored message content/source and continuation source/value must have the text
storage representation before semantic values are constructed. Unsupported
classes such as BLOB are refused as `PersistenceFormatError`, with a safe
field-specific TypeError cause; bytes are not coerced or guessed. Existing
timestamp, identity, role and reference checks remain in force. Native SQLite
operational failures retain their existing exception contract.

Schema version one and all existing table, column and index definitions remain
compatible. Saving remains current-snapshot replacement, without a revision/CAS
policy or automatic checkpoint. Retained global message rows, Evidence storage,
cross-process agent execution, privacy/retention policy, uncertain post-commit
acknowledgment and hardware power-loss guarantees remain separate obligations.
