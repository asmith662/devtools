# devtools.codex

`devtools.codex` is the first concrete implementation of
[`devtools.agents.Agent`](../../agents/protocols.py). It adapts the local Codex
CLI into a final assistant [`Message`](../../message/models.py) and an opaque
provider-owned `ConversationRef`.

## Public API

```python
from devtools.codex import (
    CodexAgent,
    CodexCommandError,
    CodexError,
    CodexOutputError,
)
```

`CodexTurnOutput`, JSONL parsing, executable resolution, and command building
are implementation details rather than package-root API.

## Architecture

```text
Message
  -> Agent
  -> CodexAgent
  -> CommandExecutor
  -> Codex CLI JSONL
  -> Message + ConversationRef
```

The direct production dependencies are:

```text
codex -> agents
codex -> message
codex -> commands
codex -> paths
```

`CodexAgent` is structural: `agent: Agent = CodexAgent(...)` is valid without
inheritance from the protocol.

## Construction and turns

```python
agent = CodexAgent(
    executor,
    working_directory,
    executable="codex",
)
```

`executor` is supplied by the caller. `working_directory` is an explicit
`ResolvedPath`; the agent never silently takes process cwd. The agent keeps no
mutable per-conversation state. Callers retain each returned `ConversationRef`
and provide it to resume a turn.

The stable agent source is `MessageSource("codex")`. It is used for the agent,
every returned assistant message, every returned conversation reference, and
incoming conversation-ownership checks.

Only `MessageRole.USER` is accepted as input. ASSISTANT and SYSTEM input raise
`ValueError` before CLI execution. This is a Codex adapter policy, not a
general `Agent` requirement. A supplied continuation must have the same source;
foreign provider references are rejected rather than reinterpreted.

## Result mapping

The final Codex text becomes:

```python
Message.new(
    final_text,
    role=MessageRole.ASSISTANT,
    source=agent.source,
)
```

The text is not trimmed. The new message has its own `MessageId` and local
timestamp; it does not carry the provider thread ID. That identity becomes:

```python
ConversationRef(source=agent.source, value=thread_id)
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
interpretation, Codex errors, and the concrete Agent implementation. It does
not own subprocess execution, generic Agent or Message semantics, session
history, runtime routing, provider discovery, or another provider.

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
uv run pytest --no-cov tests/codex/test_live.py -v
Remove-Item Env:DEVTOOLS_LIVE_CODEX
```

## Constrained future work

Justified future work includes per-turn timeout configuration, incremental
JSONL parsing, richer provider diagnostics, configurable sandbox policy, and
wider executable discovery. Richer events, model selection, alternate
transports, stdin prompting, provider concurrency guarantees, and metrics are
not current milestone commitments.
