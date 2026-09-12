# Codex CLI behavior

`devtools.interactions.providers.codex` is a narrow adapter over the local Codex CLI, not a general
Codex CLI manual. This contract was verified against `codex-cli 0.147.0`.
Later CLI versions require compatibility verification before relying on the
same details.

## Executable resolution

The default constructor value is `executable="codex"`.

On Windows, only for that default name, the adapter uses
`shutil.which("codex.cmd")`. This is a Codex-specific npm-launcher adaptation:
direct `CommandExecutor` process creation cannot use PowerShell's `codex.ps1`
shim as an interactive PowerShell shell can. If `codex.cmd` cannot be found,
the adapter keeps `"codex"`; normal command execution can then raise
`CommandNotFoundError`.

On non-Windows systems, the default remains `codex`. Any caller-supplied
executable other than the default is preserved exactly. This is not generic
shell or executable discovery. The local `sys.platform == "win32"` check is
launcher mechanics, not a general operating-system domain dependency.

## Invocation and workspace

Fresh turns use direct argv equivalent to:

```text
<resolved executable> exec --sandbox read-only --cd <working-directory> --json <prompt>
```

Resumed turns use direct argv equivalent to:

```text
<resolved executable> exec resume -c sandbox_mode="read-only" --json <thread-id> <prompt>
```

The `sandbox_mode="read-only"` expression is one argv value passed after
`-c`; it is not shell quoting.

Every command also uses `Command.cwd(working_directory)`. That sets the
subprocess cwd. Fresh `--cd` additionally sets the Codex workspace. The
installed `exec resume` interface exposes neither `--cd` nor `--sandbox`, so a
resumed turn relies on process cwd and the supported configuration override.
The configured `CodexAgent.working_directory` governs every subprocess it
launches; threads are not treated as permanently bound to their original fresh
workspace.

## Sandbox and approval

Fresh turns explicitly request `--sandbox read-only`. Resumed turns explicitly
request `-c sandbox_mode="read-only"`. The live acceptance test verified a
read-only fresh provider context, a read-only resumed provider context, and
that a disposable resumed write attempt did not create its target.

Provider records also observed `approval=never`, but the adapter does not set
approval policy. Read-only sandboxing is the adapter contract; approval behavior
is not.

## Prompt transport

`Message.content` is one direct argv value. No shell participates, so spaces,
quotes, multiline content, and empty text remain one prompt argument. Stdin is
not part of this milestone. Unicode is expected under Python argv semantics but
is not a dedicated Codex contract test.

## JSONL contract

The internal parser receives retained `stdout: bytes` and produces only the
thread ID and final agent text needed by `CodexAgent`.

It consumes these current event shapes:

```text
thread.started.thread_id
item.completed.item.type == "agent_message"
item.completed.item.text
turn.completed
turn.failed
```

Unrelated events are ignored. Plain `error` events do not independently fail a
turn because observed reconnect errors can be recoverable and followed by a
valid completion. This does not mean every provider error is harmless.

Success requires a valid nonblank thread ID, at least one completed agent
message, and `turn.completed`, with no `turn.failed`. The last completed agent
message wins. Parsing is presence-based rather than a full event-order state
machine.

Invalid UTF-8, malformed JSON, non-object events, malformed required
structures, invalid or missing thread IDs, missing final messages, missing
completion, `turn.failed`, and retained stdout truncation raise
`CodexOutputError`. UTF-8 and JSON decoder failures remain chained causes where
they originate the failure.

## Retained output and stderr

JSONL is parsed from retained `CommandResult.stdout`. The executor's retention
is finite; `stdout_truncated` fails closed with `CodexOutputError`. Callers that
expect unusually large transcripts can provide `CommandExecutor` with a larger
`CommandOutputPolicy`.

Successful-turn stderr is ignored. It is not assumed empty and is not converted
into an error message.

## Live acceptance procedure

The live test is provider-dependent and separate from the normal 100% coverage
gate. It uses a temporary Git repository and the default `CodexAgent`
constructor:

```powershell
$env:DEVTOOLS_LIVE_CODEX="1"
uv run pytest --no-cov tests/interactions/providers/codex/test_live.py -v
Remove-Item Env:DEVTOOLS_LIVE_CODEX
```

The test verifies the fresh `stored` response, a returned continuation, exact
marker recovery after resume, unchanged thread identity, and resumed write
denial without touching the project worktree.
