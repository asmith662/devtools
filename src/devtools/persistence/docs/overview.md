# `devtools.persistence`

Persistence durably stores and restores representations owned by other domains.
Its current supported state is `Conversation`: its identity and creation time,
ordered `History` of `ConversationMessage` values, and source-keyed opaque
`ConversationRef` values.

Persistence does not own conversation behavior, Runtime, model invocation,
attempt lifecycle, Evidence, Memory, or authorization. Loading constructs a
new `Conversation` with equal durable state and fresh object-local turn
coordination.

The existing JSON and SQLite wire formats retain historical schema labels such
as `sessions`, `session_messages`, and `session_id` for durable compatibility.
Those labels do not reintroduce the removed runtime `Session` API.
