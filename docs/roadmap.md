# Roadmap

## Purpose

This document records deliberately selected current sequencing. It is not an
API reference, a replacement for the canonical backlog, or authorization to
implement a future domain. The [architecture taxonomy](architecture/taxonomy.md)
defines terms; [architecture](architecture.md) defines current ownership; the
[backlog](backlog/overview.md) preserves unresolved pressure.

## Established architecture

The twelve-domain framework architecture is established:

```text
core/ resources/ models/ agents/ context/ tools/
execution/ orchestration/ governance/ observability/ persistence/ evaluation/
```

Current implemented seams include the core and resource substrates,
`Prompt -> ModelInteraction -> ModelResponse`, durable `Conversation` and
`ConversationMessage` state, narrow execution `Runtime` with specialized
`InteractionAttempt`, terminal Evidence in observability, Conversation
persistence, Tools, model serving and benchmarks, and the external Codex Agent
integration. Sparse domains are intentionally not implementation commitments.

Historical pre-migration milestones, including former Session, Interaction,
and Evidence ownership terminology, remain in the
[implementation ledger](implementation_ledger.md) as history only.

## Current sequencing

### Now — documentation integrity and backlog rebase

- [B-0001](backlog/epics/B-0001-architecture-documentation-integrity.md) and
  [B-0006](backlog/items/B-0006-reconcile-authoritative-architecture-documentation.md)
  keep current documentation, roadmap sequencing, and backlog pressure aligned
  with the established architecture.

### Next candidate — repository intelligence and coding-Context design

- [ADR-0002](architecture/decisions/ADR-0002-repository-intelligence-identity-and-derivation.md)
  establishes semantic architecture for Repository identity, snapshots,
  Derivations, DerivedKnowledge, and Context boundaries. [ADR-0003](architecture/decisions/ADR-0003-information-need-retrieval-evidence-and-ranking.md)
  establishes InformationNeed, retrieval evidence/planning, and ranking
  semantics. [ADR-0004](architecture/decisions/ADR-0004-context-disclosure-planning-and-assembly.md)
  establishes Context/disclosure planning, materialization, provenance-bearing
  disclosure artifacts, representation origins, and model-input assembly
  semantics.
  [B-0002](backlog/epics/B-0002-coding-context-substrate.md)
  retains the unimplemented design pressure. These decisions are not authorization
  for a Context compiler, disclosure model, index, parser, graph store, retrieval system, Memory,
  Agent loop, or orchestration system. [B-0008](backlog/items/B-0008-investigate-repository-context-discovery.md)
  remains superseded historical navigation evidence.

### Later — promotion only when evidence is sufficient

The canonical backlog contains deferred pressure for generic execution
lifecycle promotion, model-facing Tool and Action boundaries, Agent semantics,
orchestration, governance, durable observability, and advanced model
interaction. Each remains subject to its own dependencies and promotion
conditions. The Qwen probes are experimental evidence, not reusable framework
promotion.

## Validation cadence

Use deterministic validation for implemented changes. Add task-specific live
acceptance only when a meaningful specialized path exists; live evidence tests
framework enforcement and causal boundaries, not voluntary model obedience.

See [documentation_map.md](documentation_map.md) for authority and navigation.
