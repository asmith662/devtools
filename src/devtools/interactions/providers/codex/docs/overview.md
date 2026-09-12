# devtools.interactions.providers.codex

`devtools.interactions.providers.codex` exposes the external Codex agent system through
[`devtools.interactions.Interaction`](../../../protocols.py). It adapts the local Codex
CLI into a final assistant [`Message`](../../../../context/message.py) and an opaque
provider-owned `ConversationRef`.

## Public API

```python
from devtools.interactions.providers.codex import (
    CodexAgent,
    CodexCommandError,
    CodexError,
    CodexOutputError,
)
from devtools.interactions import Interaction
```

`CodexTurnOutput`, JSONL parsing, executable resolution, and command building
are implementation details rather than package-root API.

## Architecture

```text
Message
  -> Interaction
  -> CodexAgent
  -> CommandExecutor
  -> Codex CLI JSONL
  -> Message + ConversationRef
```

The direct production dependencies are:

```text
codex -> interactions
codex -> context.message
codex -> commands
codex -> paths
```

`CodexAgent` is structural: `interaction: Interaction = CodexAgent(...)` is valid without
inheritance from the protocol.

## Construction and turns

```python
interaction = CodexAgent(
    executor,
    working_directory,
    executable="codex",
)
```

`executor` is supplied by the caller. `working_directory` is an explicit
`ResolvedPath`; the Interaction never silently takes process cwd. The Interaction keeps no
mutable per-conversation state. Callers retain each returned `ConversationRef`
and provide it to resume a turn.

The stable Interaction source is `MessageSource("codex")`. It is used for the Interaction,
every returned assistant message, every returned conversation reference, and
incoming conversation-ownership checks.

Only `MessageRole.USER` is accepted as input. ASSISTANT and SYSTEM input raise
`ValueError` before CLI execution. This is a Codex adapter policy, not a
general `Interaction` requirement. A supplied continuation must have the same source;
foreign provider references are rejected rather than reinterpreted.

## Result mapping

The final Codex text becomes:

```python
Message.new(
    final_text,
    role=MessageRole.ASSISTANT,
    source=interaction.source,
)
```

The text is not trimmed. The new message has its own `MessageId` and local
timestamp; it does not carry the provider thread ID. That identity becomes:

```python
ConversationRef(source=interaction.source, value=thread_id)
```

The reference is only opaque Codex continuation identity. It does not carry a
workspace, sandbox, approval policy, model, provider configuration, or a
future session identity.

For a successful resume, the current Codex CLI continues the same provider
thread; the live acceptance test verifies that the first and second reference
values match.

## Errors

```text
CodexError
|- CodexCommandError
`- CodexOutputError
```

`CodexCommandError` represents a completed nonzero CLI exit and exposes only
`exit_code`. `CodexOutputError` represents malformed, incomplete, failed, or
knowingly truncated structured output.

Command-domain failures remain command-domain failures. For example,
`CommandNotFoundError` and `CommandTimeoutError` are not flattened into Codex
errors.

## Boundaries and limitations

This package owns Codex executable adaptation, CLI command construction, JSONL
interpretation, Codex errors, and the concrete Interaction implementation. It does
not own subprocess execution, generic Interaction or Message semantics, session
history, runtime routing, provider discovery, or another provider.

Codex remains externally agentic: its CLI owns its internal planning, repository interaction, sandbox behavior, and action loop. The repository adapter exposes only one bounded Interaction turn.

The adapter has no per-turn timeout setting and no provider concurrency
guarantee. It has no mutable in-memory turn state, so independent calls do not
conflict in the adapter itself; external Codex CLI/session-store concurrency is
not established as a package guarantee.

See [CLI behavior](cli.md) for the current executable, invocation, sandbox,
JSONL, and live-test contract.

## Verified acceptance

The opt-in live test starts a temporary Git repository, sends a fresh user
turn, resumes with the returned conversation reference, verifies the exact
continuity marker and unchanged thread ID, and verifies that a disposable
resumed write target is not created under read-only execution.

Run it separately from deterministic coverage:

```powershell
$env:DEVTOOLS_LIVE_CODEX="1"
uv run pytest --no-cov tests/interactions/providers/codex/test_live.py -v
Remove-Item Env:DEVTOOLS_LIVE_CODEX
```

## Constrained future work

Justified future work includes per-turn timeout configuration, incremental
JSONL parsing, richer provider diagnostics, configurable sandbox policy, and
wider executable discovery. Richer events, model selection, alternate
transports, stdin prompting, provider concurrency guarantees, and metrics are
not current milestone commitments.
