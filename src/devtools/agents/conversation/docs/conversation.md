# Conversation

`Conversation` is the mutable owner of durable conversation identity, creation
time, immutable ordered `History`, source-keyed `ConversationRef` values, and
object-local complete-turn coordination. It stores continuity but does not
invoke models, own a Run, execute Tools, or configure providers.

`Conversation.new()` creates a new durable identity. `add()` retains a supplied
`ConversationMessage`; `conversation_for()` and `set_conversation()` manage
opaque provider continuation by source. `turn()` serializes complete Runtime
turns for this in-memory object; it is not persistence, cross-process locking,
or rollback.

Persistence may reconstruct the same durable state with fresh local
coordination. Existing durable storage names such as `sessions` and
`session_messages` remain historical wire-schema compatibility details, not
runtime terminology.
