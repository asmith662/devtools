# Documentation Map

## Authority

Package-local documentation is authoritative for its package's public API,
behavior, invariants, limitations, and package-specific future work.

Repository-level documentation has separate responsibilities:

- [architecture.md](architecture.md): package relationships, cross-package
  boundaries, dependency direction, and architectural principles.
- [roadmap.md](roadmap.md): completed and future architectural sequencing.
- [implementation_ledger.md](implementation_ledger.md): historical
  implementation milestones and verification state.

The ledger records history; it does not authorize future architecture.

## Package documentation

- [identity overview](../src/devtools/identity/docs/overview.md)
- [agents overview](../src/devtools/agents/docs/overview.md)
- [context overview](../src/devtools/context/docs/overview.md) — Context domain
  ownership and boundaries for Message, History, and Session
- [History](../src/devtools/context/docs/history.md) — exact immutable
  transcript behavior and API
- [Session](../src/devtools/context/docs/session.md) — exact SessionId,
  mutable lifecycle, and continuation-state contract
- [Runtime overview](../src/devtools/runtime/docs/overview.md) -
  configuration-bearing, interaction-stateless Agent/Session coordination and
  optional Attempt observation contract
- [Persistence overview](../src/devtools/persistence/docs/overview.md) - durable
  semantic Session reconstruction boundary
- [Persistence JSON](../src/devtools/persistence/docs/json.md) - strict portable
  JSON Session representation
- [Persistence SQLite](../src/devtools/persistence/docs/sqlite.md) - normalized
  SQLite Session snapshot store
- [Evidence overview](../src/devtools/evidence/docs/overview.md) - live Attempt
  lifecycle/AttemptObserver and immutable terminal Evidence value-model contract
- [system overview](../src/devtools/system/docs/overview.md)
- [paths overview](../src/devtools/paths/docs/overview.md) and
  [resolution](../src/devtools/paths/docs/resolution.md)
- [time overview](../src/devtools/time/docs/overview.md),
  [timestamps](../src/devtools/time/docs/timestamps.md), and
  [timing](../src/devtools/time/docs/timing.md)
- [commands overview](../src/devtools/commands/docs/overview.md),
  [command values](../src/devtools/commands/docs/command.md),
  [execution](../src/devtools/commands/docs/execution.md), and
  [events](../src/devtools/commands/docs/events.md)
- [Codex overview](../src/devtools/codex/docs/overview.md) and
  [CLI behavior](../src/devtools/codex/docs/cli.md)
- [regex overview](../src/devtools/regex/docs/overview.md)
- [conversion overview](../src/devtools/conversion/docs/overview.md)
- [filesystem overview](../src/devtools/filesystem/docs/overview.md),
  [models](../src/devtools/filesystem/docs/models.md),
  [codecs](../src/devtools/filesystem/docs/codecs.md),
  [I/O](../src/devtools/filesystem/docs/io.md),
  [JSON](../src/devtools/filesystem/docs/json.md),
  [Markdown](../src/devtools/filesystem/docs/markdown.md),
  [CSV](../src/devtools/filesystem/docs/csv.md), and
  [filesystem future work](../src/devtools/filesystem/docs/roadmap.md)

## Updating documentation

When implementation changes:

1. Update the affected package-local documentation first.
2. Update [architecture.md](architecture.md) only when cross-package
   architecture changes.
3. Update [roadmap.md](roadmap.md) when milestone status or sequencing changes.
4. Update the [implementation ledger](implementation_ledger.md) when a
   meaningful implementation milestone becomes true.
