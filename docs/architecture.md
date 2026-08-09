# Architecture

`devtools` is one Python project and distribution. Its source is organized by
cohesive capability domains under `src/devtools/`.

The current domains are `devtools.system`, `devtools.paths`, `devtools.time`,
`devtools.commands`, `devtools.identity`, `devtools.regex`, and
`devtools.filesystem`. A domain may grow internal modules when cohesion
justifies them; capabilities are not made separately distributable preemptively.

`devtools.paths` owns AI-neutral path primitives for ordinary Python callers.
`ResolvedPath` proves that its stored `pathlib.Path` is absolute; parsing and
explicit resolution are separate operations. Containment remains future work.

`devtools.time` owns timestamps, durations, parsing, and monotonic elapsed-time
measurement. `devtools.commands` keeps immutable command specifications apart
from execution. `CommandExecution` is awaitable and exposes a single-consumer,
best-effort event stream. Commands clean up an immediate child process on
timeout or cancellation. Output retention and pending event buffering are
explicitly bounded by `CommandOutputPolicy`; results report truncated output and
dropped events.

`devtools.regex` provides immutable match values and explicit regex operations.
`devtools.filesystem` provides immutable file models and `JsonCodec`. JSON
models use recursively frozen mappings and tuples, preserve source-text regex
search, and provide structured traversal and transformations. A model's
`content` is source provenance; its `value` is current structured state and is
what `JsonCodec` serializes. Generic filesystem reading and writing remain
separate future work.
