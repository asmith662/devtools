# Command values, policy, and results

See the [package overview](overview.md), [execution lifecycle](execution.md),
and [events/output semantics](events.md).

## `Command`

```python
Command(
    executable: str,
    arguments: tuple[str, ...] = (),
    working_directory: ResolvedPath | None = None,
    timeout: Duration | None = None,
)
```

`Command` is a frozen, slotted value object. Blank executables are invalid.
The executable and arguments remain separate; no shell parsing, interpolation,
or quoting occurs. `argv` returns the complete tuple passed to process launch.

All fluent methods return new values:

```text
args(...)             append arguments
with_args(...)        replace arguments
without_args()        clear arguments
with_executable(...)  replace and validate executable
cwd(...)              set ResolvedPath working directory
without_cwd()         clear working directory
with_timeout(...)     set Duration timeout
without_timeout()     clear timeout
```

## `CommandOutputPolicy`

```python
CommandOutputPolicy(
    max_stdout_bytes=1_048_576,
    max_stderr_bytes=1_048_576,
    max_pending_events=1_024,
)
```

Stdout and stderr retention limits are independent. A zero byte limit is valid:
nonempty output remains streamable but no bytes are retained in the final
result, and the matching truncation flag is true. Negative byte limits are
invalid. Pending-event capacity must be positive.

## `CommandResult`

```python
CommandResult(
    command,
    exit_code,
    stdout,
    stderr,
    duration,
    stdout_truncated=False,
    stderr_truncated=False,
    events_dropped=0,
)
```

Results are frozen value objects. Stdout/stderr remain bytes and contain only
the retained leading prefix allowed by the policy; they are not necessarily the
complete process output. Truncation flags report omitted retained bytes, and
`events_dropped` reports bounded-queue loss.

Exit code zero means `succeeded`; every nonzero exit code means `failed` but is
still a completed result. Timeout, cancellation, process-creation failure, and
other execution exceptions produce no `CommandResult`.
