# Command execution lifecycle

See the [package overview](overview.md), [command values](command.md), and
[event semantics](events.md).

## Starting and awaiting

```python
executor = CommandExecutor(output_policy=...)
execution = executor.start(command)
result = await execution

# Convenience equivalent
result = await executor.execute(command)
```

`execute()` calls `start()` and awaits the returned handle. `start()` requires
an active asyncio event loop because it immediately creates the underlying
task.

`CommandExecution` owns one task and launches one subprocess. Repeated
successful awaits share that task and return the same `CommandResult` instance.
`is_running` and `is_complete` reflect task state. There is no async context
manager.

## Process creation

Execution uses `asyncio.create_subprocess_exec()` with direct argv, optional
native cwd, and stdout/stderr pipes. Explicit binary stdin is piped while both
output streams drain, then closed to deliver EOF. Empty bytes also create a pipe;
None preserves inherited stdin. Early input closure/child exit remains an ordinary
result. Timeout and cancellation cover blocked input and reap the immediate child.
Per-command environment overrides are merged with the current parent at launch,
without mutating os.environ. None/empty overrides use inherited environment;
nonempty mappings overlay only their keys. Immutable specification validation and
fluent behavior are described in [Command values](command.md). There is no shell
or process-group configuration. The exact Qwen implementation and independent
regressions are reviewed and feature-published; see
[environment development 13](../../../../../apps/qwen/evaluation/environment-13/README.md).
These Commands capabilities were adopted on protected main by the reviewed
Commands integration at `2f9218625ab4` (merge `5d979920d072`).

The exact Qwen-authored stdin implementation was independently qualified after
correcting missing standard attributes in old test doubles, then reviewed and
feature-published through WorkCycle. The live continuation still failed at
Context capacity; see [stdin development evidence](../../../../../apps/qwen/evaluation/stdin-11/README.md).
Its later protected-main integration does not establish uninterrupted autonomous
success for that historical continuation.

If creation raises `FileNotFoundError`, it becomes `CommandNotFoundError` with
the original error retained as its cause. No started event or result is
produced, and the event stream closes.

## Explicit successful statuses

The executor and live handle retain raw process status and result identity.
`CommandResult` applies the originating Command's `success_exit_codes` to its
`succeeded`/`failed` views; CommandTool/ToolRunner forward the same result.
`CommandExited.exit_code` remains the actual status, including a selected nonzero
or excluded zero. This interpretation does not change execution exceptions,
timeouts, cancellation or cleanup. See [command values](command.md).

## Timeout

`Duration.total_seconds` configures an asyncio timeout around post-creation
output collection. Process creation time is not included.

On timeout, the running immediate child is killed and awaited/reaped,
`CommandTimeoutError` is raised with the timeout failure as its cause, and the
event stream closes. No `CommandExited` or final result is fabricated. Events
already observed may remain available, but partial retained output is not
exposed through a result.

## Cancellation

Before child creation completes, cancellation closes the stream and propagates.
After creation, a running immediate child is killed and awaited/reaped;
cancellation then propagates unchanged and no exit event is fabricated. An
already-exited child is awaited without another kill.

Awaiters directly await the same task. Cancelling one awaiter can therefore
cancel the shared command execution for all awaiters.

Only the immediate child is managed. Descendants and process groups are not
terminated.

Output and stdin collection tasks are owned by this execution. Each collecting
boundary cancels and joins its unfinished children before returning, including
when a sibling read/write fails, timeout expires or the caller cancels. Cleanup
collects sibling exceptions without replacing the originating failure. Normal
completion still drains streams and produces one result; failure produces no
successful result or exit event. This is task cleanup, not durable evidence,
external-effect rollback, retry authority or descendant-process management.


## Explicit decoded output views

`CommandResult.stdout_text(*, encoding="utf-8", errors="strict")` and
`stderr_text(...)` return native `bytes.decode` views of the retained channels.
They leave the original bytes, truncation flags, command, duration, exit code and
event-drop metadata unchanged. Alternate codecs/error policies follow Python's
native contract, including `UnicodeDecodeError` and `LookupError`; arguments are
keyword-only. These Qwen-authored methods and independent permanent regressions
were feature-published in `9b667e597f9d` and adopted by the Commands integration
at `2f9218625ab4`.
