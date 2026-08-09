# Implementation Ledger

## Implemented

- one `devtools` distribution with capability-oriented source domains,
- `devtools.paths.ResolvedPath`, filesystem-path and dot-path parsing, and
  explicit resolution,
- `devtools.system` operating-system family detection,
- `devtools.time` timestamps, durations, parsing, and a monotonic stopwatch,
- `devtools.commands` immutable fluent command specifications, final results,
  awaitable executions, structured streaming events, timeout and cancellation
  cleanup for an immediate child process, and bounded output/event buffering,
- `devtools.identity` UUID-based immutable identities,
- `devtools.regex` immutable match values and regex operations,
- `devtools.filesystem` immutable binary, text, CSV, Markdown, and JSON model
  foundations, including recursively frozen JSON object/list/scalar values,
- `devtools.filesystem.JsonCodec` source decode/parse and serialize/encode
  conversion between JSON representations and immutable JSON models,
- `devtools.filesystem.read()` bounded, codec-backed JSON disk reads with
  suffix inference or an explicit format override,
- `devtools.filesystem.write()` JSON model persistence through sibling
  temporary-file replacement; it writes current structured model state rather
  than stale source provenance,
- package-level Ruff, strict mypy, pytest, and 100% branch-coverage policy.

## Not Implemented

- path containment,
- generic filesystem support beyond JSON and its currently implemented codec,
- process-tree termination, stdin, shell execution, environment overrides,
  output decoding, pipelines, and event broadcast.
