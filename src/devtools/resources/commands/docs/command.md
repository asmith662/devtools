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
    stdin: bytes | None = None,
    environment: Mapping[str, str] | None = None,
)
```

`Command` is a frozen, slotted value object. Blank executables are invalid.
Construction and fluent replacements reject non-string executables and require
a tuple containing only strings for arguments (`TypeError`). Blank string
executables still raise `ValueError`. Empty, Unicode and shell-looking argument
strings remain literal values; validation never strips or splits arguments.
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
with_stdin(bytes)     replace immutable binary input
without_stdin()       restore inherited stdin
with_environment(...) replace environment overrides
without_environment() restore inherited environment
```

`stdin=None` preserves inherited input. Immutable `bytes`, including `b""`,
select a child pipe and exact payload followed by EOF. Other types raise
`TypeError` at construction and fluent replacement. Input participates in value
equality/hash and is preserved by every other fluent method. Payload storage is
in-memory; there is no separate input-size policy.

`environment` accepts a string-to-string Mapping or None. Construction and fluent
replacement snapshot the mapping and expose a read-only view. Equivalent override
mappings have order-independent equality/hash; all fluent operations preserve the
other command dimensions. Non-mappings/non-string entries raise TypeError; empty
names, equals signs in names, and NUL in names or values raise ValueError.

None and an empty mapping inherit the current parent at process launch. Nonempty
overrides replace only their keys, retaining other parent values. Empty strings
and Unicode values are supported. The executor never mutates os.environ; concurrent
commands receive independent overlays. The original immutable Mapping is a command
value, not a captured full parent-environment snapshot.

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
