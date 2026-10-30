# Coding transition diagnostic

[Report](REPORT.md) records one frozen read-only local Qwen diagnostic using the
shared coding agent, exact host-selected source and opt-in active-source status.
It failed to establish an implementation transition and produced no candidate.

- [Protocol](protocol.md), [objective](objective.md), [freeze](freeze.json).
- [Independent review](review.json), [retained evidence](evidence/).
- [Original ten-call trace](analysis/trace-table.json) and
  [source/payload measurements](analysis/original-trace.json).
- [Source/terminal preflight](analysis/preflight.json), [integrity manifest](manifest.json).

`host.py preview` is explicitly deterministic preflight. `freeze` and `run` are
historical entry points, not permission to repeat inference. No predecessor is
modified; a new experiment needs separate identity and authorization.
