# Documentation Map

## Authority

- [Architecture taxonomy](architecture/taxonomy.md) defines semantic terms and
  non-equivalence.
- [Architecture](architecture.md) defines current cross-package ownership and
  dependency direction.
- [Accepted architecture decisions](architecture/decisions/) freeze approved
  future cross-package decisions; they do not claim an unimplemented API is
  current behavior. [ADR-0001](architecture/decisions/ADR-0001-cohesive-model-interaction-boundary.md)
  defines the approved ModelInteraction redesign. [ADR-0002](architecture/decisions/ADR-0002-repository-intelligence-identity-and-derivation.md)
  defines accepted future repository-intelligence and coding-Context semantics.
  [ADR-0003](architecture/decisions/ADR-0003-information-need-retrieval-evidence-and-ranking.md)
  defines accepted future InformationNeed, retrieval-evidence, and ranking semantics.
- [AGENTS.md](../AGENTS.md) defines repository-operating rules.
- Package-local documentation defines implemented public APIs, behavior, and
  limitations.
- Source and tests define the final implemented behavior where documentation is
  incomplete.
- Backlog and implementation-ledger records are historical or unresolved
  architectural evidence; they do not independently authorize implementation.
- [Roadmap](roadmap.md) records selected current sequencing and links to the
  canonical backlog; it does not supersede the taxonomy or architecture.

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
reusable implementation API.

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
