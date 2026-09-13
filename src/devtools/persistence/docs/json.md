# JSON conversation persistence

The JSON helpers encode and decode the durable `Conversation` representation:
identity, creation time, ordered `ConversationMessage` values, and keyed
`ConversationRef` continuation values. They do not open files; callers compose
them with `devtools.resources.filesystem` when file I/O is needed.

JSON field names remain compatible with the established durable format where
possible. They are storage details and do not define the runtime conversation
API.
