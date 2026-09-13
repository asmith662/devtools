# SQLite conversation persistence

The SQLite store saves and loads durable `Conversation` state. It preserves the
established normalized schema and historical table or column names such as
`sessions`, `session_messages`, and `session_id` for compatibility. Those names
are schema identifiers, not active `Session` terminology.

Saving replaces one conversation's persisted history and continuation snapshot
atomically within the store transaction. It does not acquire Conversation turn
coordination, provide cross-process execution locking, or make external effects
exactly once.
