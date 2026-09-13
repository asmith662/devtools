# `devtools.agents.integrations.codex`

This package adapts the external Codex agent system. Codex is an Agent
integration, not a `ModelInteraction` provider: its CLI owns planning,
repository interaction, sandbox behavior, and its internal action loop.

`CodexAgent` accepts a user `ConversationMessage` and returns a narrow
`CodexConversationResult` containing the final assistant
`ConversationMessage` and an optional provider-owned `ConversationRef`.
It owns CLI command construction, JSONL interpretation, Codex-specific
errors, working-directory handling, and provider-thread continuation.

It does not own generic conversation history, model prompts/responses, Runtime,
subprocess execution, or an Agent framework. Managed execution is supplied by
`devtools.resources.commands`.

```python
from devtools.agents.integrations.codex import CodexAgent
```

See [CLI behavior](cli.md) for executable, sandbox, JSONL, and opt-in live-test
details.
