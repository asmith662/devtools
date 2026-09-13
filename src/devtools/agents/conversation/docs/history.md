# History

`History` is an immutable insertion-ordered sequence of
`ConversationMessage` values. It records which durable communications occurred
without selecting model context, invoking providers, storing continuations, or
owning persistence.

Appending returns a new History and retains the supplied message value exactly;
roles, sources, IDs, content, and timestamps are not normalized by History.
