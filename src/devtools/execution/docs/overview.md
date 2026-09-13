# `devtools.execution`

Execution owns narrow mechanics for one selected `ModelInteraction` operating
with one `Conversation`. `Runtime.send()` retains the input
`ConversationMessage`, projects it to `Prompt`, invokes the selected
`ModelInteraction`, validates the returned `ModelResponse`, materializes a new
assistant `ConversationMessage`, retains it, and replaces continuation only
when the response supplies one.

```text
ConversationMessage -> Prompt -> ModelInteraction -> ModelResponse
    -> ConversationMessage
```

Runtime is not an Agent loop, router, workflow engine, scheduler, Tool
dispatcher, or Evidence owner. It optionally exposes its specialized
`InteractionAttempt` lifecycle to an `InteractionAttemptObserver`; no attempt
is allocated when no observer is configured. `InteractionAttempt` is not the
future generic Step Attempt.

Execution does not import observability. Observability observers may construct
historical Evidence from lifecycle facts without changing Runtime ownership.
