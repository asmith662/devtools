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
native cwd, and stdout/stderr pipes. There is no shell, stdin, environment
override, or process-group configuration.

If creation raises `FileNotFoundError`, it becomes `CommandNotFoundError` with
the original error retained as its cause. No started event or result is
produced, and the event stream closes.

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
