# Codex CLI behavior

`devtools.agents.integrations.codex` is a narrow adapter over the local Codex CLI, not a general
Codex CLI manual. This contract was verified against `codex-cli 0.147.0`.
The argv prompt examples and live procedure below describe that historical
milestone. The maintained prompt transport was subsequently repaired; the
current contract immediately below supersedes those examples.

## Current maintained transport and optional command observations

The delivered [literal-input repair](../../../../../../docs/development/codex-input-and-metadata-repair.md)
uses UTF-8 stdin and the documented `-` prompt operand after `--`, for fresh and
resumed calls. Current source/tests are authoritative. No shell interpolation or
CLI option interpretation of prompt content occurs. This increment does not
change those arguments, continuation, usage or result semantics.

Installed CLI0.162.1 version/help inspection confirms `exec --json` JSONL output;
no new live inference was run. `codex.commands.CodexCommandObserver` optionally
projects available authored/authorized command_execution items into bounded,
privacy-selected command observations. The default CodexAgent still returns
its established final message/usage result and exposes no complete command feed.
CLI reported completion is distinct from local process-entry evidence. Missing
events imply neither zero commands nor known failure. See
[command observation contracts](../../../../../../docs/development/command-capabilities.md).

## Historical 0.147.0 milestone

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

`ConversationMessage.content` is one direct argv value. No shell participates, so spaces,
quotes, multiline content, and empty text remain one prompt argument. Stdin is
not part of this milestone. Unicode is expected under Python argv semantics but
is not a dedicated Codex contract test.

## JSONL contract

The internal parser receives retained `stdout: bytes` and produces the
thread ID, final agent text, and separately captured optional usage.

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

## Usage accounting

Usage-only parsing is independently callable for process failures and rejected
artifacts. Observed 0.162.1 `turn.completed.usage` fields are `input_tokens`,
`cached_input_tokens`, `cache_write_input_tokens`, `output_tokens`, and
`reasoning_output_tokens`. The normalized `ModelUsage` retains optional cache
read/write and reasoning counts without deriving a total. The raw usage object
is preserved separately. Missing values remain unknown, not zero.

A turn aggregate is not an underlying model request. Duplicate completion without
a new turn, or repeated explicit turn identities, rejects usage capture rather
than charging twice. A usage error is returned separately from a successful final
message; callers with mandatory accounting must reject publication separately.
Unsuccessful command/output errors retain available usage, while truncated streams
are explicitly incomplete. No new live model validation accompanies these parser
tests; the older invocation/sandbox compatibility scope above remains unchanged.

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
