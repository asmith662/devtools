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

Results additionally retain optional usage-only `CodexUsage` turn aggregates.
`capture_codex_usage` inspects retained stdout independently of semantic final
response acceptance. It preserves the five observed Codex 0.162.1 token fields
and raw provider usage JSON without inferring request counts or overlapping totals.
`CodexError` retains recoverable usage for unsuccessful process/output paths.
Unavailable or malformed usage is distinct from reported zero. Optional accounting
errors do not erase an otherwise valid response; a consumer requiring accounting
must independently fail its publication gate. This is not automatic scientific
acceptance, a usage ledger, pricing, or subscription accounting.

```python
from devtools.agents.integrations.codex import CodexAgent
```

See [CLI behavior](cli.md) for executable, sandbox, JSONL, and opt-in live-test
details.
