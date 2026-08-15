# `devtools.commands`

## Purpose

`devtools.commands` provides asynchronous direct-process execution primitives:
immutable command specifications, bounded output capture, live event
observation, timeout handling, and immediate-child cleanup.

## Public API

```python
from devtools.commands import (
    Command,
    CommandError,
    CommandEvent,
    CommandExecution,
    CommandExecutor,
    CommandExited,
    CommandNotFoundError,
    CommandOutputPolicy,
    CommandResult,
    CommandStarted,
    CommandStderr,
    CommandStdout,
    CommandTimeoutError,
)
```

| Group              | API                                                                                 |
|--------------------|-------------------------------------------------------------------------------------|
| Specification      | `Command`                                                                           |
| Execution          | `CommandExecutor`, `CommandExecution`                                               |
| Events             | `CommandEvent`, `CommandStarted`, `CommandStdout`, `CommandStderr`, `CommandExited` |
| Results and policy | `CommandResult`, `CommandOutputPolicy`                                              |
| Errors             | `CommandError`, `CommandNotFoundError`, `CommandTimeoutError`                       |

`CommandEvent` is a type alias for the concrete event values, not a runtime
event superclass.

## Architecture

```text
Command
   ↓
CommandExecutor.start()
   ↓
CommandExecution
   ├── events()
   └── await
        ↓
   CommandResult
```

`execute()` is the convenience start-and-await path. See [command values](command.md),
[execution lifecycle](execution.md), and [events/output](events.md).

## Dependencies and boundaries

The dependency direction is `commands -> paths` and `commands -> time`.
Commands has no higher-level runtime or session dependency.

It does not own orchestration, sessions, retries, scheduling, shell-language
parsing, repository behavior, or runtime composition.

## Errors

```text
CommandError
├── CommandNotFoundError
└── CommandTimeoutError
```

A nonzero process exit is a normal `CommandResult`, not an exception.

## Limitations and future evolution

Execution manages only the immediate child process. Output/event observation is
bounded and best effort. Shell mode, stdin, environment overrides, process
groups, pipelines, retries, and text decoding are absent.

Potential future work is limited to demonstrated needs: descendant cleanup,
stdin, environment overrides, text decoding, and alternative bounded-output
strategies such as disk spooling. Retry and shell/pipeline policy belong at a
higher layer.
