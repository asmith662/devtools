# Command events and bounded output

See the [package overview](overview.md), [command values](command.md), and
[execution lifecycle](execution.md).

## Event values

```text
CommandStarted(command)
CommandStdout(data: bytes)
CommandStderr(data: bytes)
CommandExited(exit_code: int, duration: Duration)
```

These are frozen value objects. `CommandEvent` is their union type alias, not a
runtime base class.

For a successful execution without queue loss, the lifecycle is:

```text
CommandStarted
    ↓
stdout/stderr observations
    ↓
CommandExited
```

Ordering within stdout and within stderr is preserved. Interleaving between the
two streams is not guaranteed.

## `events()`

`execution.events()` is a single-consumer async stream. The claim occurs when
iteration begins; a second consumer attempt raises `RuntimeError`. Streams
close on normal completion, missing executable, timeout, cancellation, and
unexpected stream-read failure.

## Bounded queue and drop policy

The pending queue is bounded by `CommandOutputPolicy.max_pending_events`.
Producers never block when full: any newly emitted event is dropped, and
`events_dropped` records the total. No event type is privileged, so
`CommandExited` may be dropped under pressure. Event delivery is best effort.

## Event bytes versus result bytes

Process streams are read in bounded chunks and fully drained during normal
completion. Result retention independently stores only the leading stdout and
stderr prefixes allowed by the output policy. Bytes beyond a limit are omitted
from `CommandResult` and set the corresponding truncation flag.

An output event may therefore contain bytes that are absent from final retained
result output. Queue buffering and result retention are separate bounds.
