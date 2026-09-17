# Documentation Map

## Authority and ownership

- [Central architecture](architecture.md) is the canonical current and accepted
  system-architecture overview: domains, boundaries, dependency direction,
  cross-domain composition, and whether architecture is implemented/current or
  accepted but not implemented. It must be understandable without replaying all
  ADRs.
- [Architecture taxonomy](architecture/taxonomy.md) defines semantic vocabulary
  and non-equivalence. It does not replace the architecture overview.
- [Accepted architecture decisions](architecture/decisions/) preserve decision
  rationale, alternatives, consequences, and historical evolution. They explain
  why architecture was chosen; they are not the sole current-state specification.
  ADR-0001 defines ModelInteraction/Tool semantics; ADR-0002 repository identity,
  subjects/source occurrences, derivation, and graph semantics; ADR-0003
  InformationNeed/retrieval/ranking; and
  [ADR-0004](architecture/decisions/ADR-0004-context-disclosure-planning-and-assembly.md)
  Context/disclosure planning, materialization, representation-origin, and
  model-input assembly semantics.
- [AGENTS.md](../AGENTS.md) defines repository-operating rules.
- Package-local documentation defines detailed implemented public APIs, package
  design, lifecycle/operational behavior, and usage. Central architecture
  summarizes system-level ownership and links outward; it does not duplicate
  every package contract.
- Source and tests define the final implemented behavior where documentation is
  incomplete.
- Backlog records unresolved/future pressure; [roadmap](roadmap.md) records
  sequencing; the implementation ledger records implementation/history; and
  experiments are evidence. None is canonical current architecture or
  independently authorizes implementation. Historical terminology remains
  historical unless a clarification is needed to prevent a current-state error.

## Package documentation

- Core: [identity](../src/devtools/core/identity/docs/overview.md),
  [paths](../src/devtools/core/paths/docs/overview.md),
  [time](../src/devtools/core/time/docs/overview.md),
  [regex](../src/devtools/core/regex/docs/overview.md), and
  [conversion](../src/devtools/core/conversion/docs/overview.md).
- Resources: [commands](../src/devtools/resources/commands/docs/overview.md)
  and [filesystem](../src/devtools/resources/filesystem/docs/overview.md).
- Models: [interaction](../src/devtools/models/interaction/docs/overview.md),
  [serving](../src/devtools/models/serving/docs/overview.md), and
  [benchmarks](../src/devtools/models/benchmarks/docs/overview.md).
- Agents: [conversation](../src/devtools/agents/conversation/docs/overview.md)
  and [Codex integration](../src/devtools/agents/integrations/codex/docs/overview.md).
- Execution: [Runtime](../src/devtools/execution/docs/overview.md).
- Observability: [Evidence](../src/devtools/observability/evidence/docs/overview.md).
- Persistence: [overview](../src/devtools/persistence/docs/overview.md),
  [JSON](../src/devtools/persistence/docs/json.md), and
  [SQLite](../src/devtools/persistence/docs/sqlite.md).
- Tools: [overview](../src/devtools/tools/docs/overview.md).

The `context`, `orchestration`, `governance`, and `evaluation` domains are
recognized sparse namespaces. They intentionally do not yet document a
reusable implementation API. In particular, current durable conversation
semantics live in `agents.conversation`; the sparse `context` namespace does
not own former Message/History/Session semantics or a Context compiler.

## Experiments and scripts

`experiments/` is non-installable composition and may depend on `devtools`;
reusable source must not import it. [Qwen experiment documentation](../experiments/qwen/docs/overview.md)
describes the bounded read-only experiments. Operational entry points remain
under `scripts/`.

## Backlog navigation

[Backlog overview](backlog/overview.md) is the canonical record index, grouped
by stable ID, lifecycle status, and primary domain. [Backlog metadata](backlog/metadata.md)
defines ownership, split-lineage, dependency, and promotion terminology.

## Update workflow

For an implemented behavior change, update package documentation first, then
this map and architecture documentation when navigation or cross-package
ownership changes. Update an accepted ADR when an approved cross-package
decision changes. Preserve historical records as history rather than rewriting
them to conceal a former architecture.
