# B-0002 — Coding Context Substrate

- type: EPIC
- status: BACKLOG
- decision_maturity: NEEDS_INVESTIGATION
- necessity: REQUIRED
- architectural_significance: STRUCTURAL
- urgency: SOON
- evidence_basis: MULTIPLE
- scope: coding-oriented repository discovery and context selection

## Problem / value

Investigate repository discovery and context selection for coding harnesses
without declaring it universal agent memory.

## Evidence / consumers / invariants

Paths, bounded filesystem reads, regex, and Markdown structure exist; inventory,
symbols, imports, selection provenance, and budgeting do not. The first consumer
is the local coding worker; this is not presumed foundational to every agent.

## Dependencies / risks / validation

- hard_dependencies: none
- pressure_dependencies: B-0003
- operational_dependencies: paths, filesystem, regex
- children: B-0008
- unresolved_semantics: scope and reusable versus coding-specific boundary
- risk_if_deferred: discovery becomes harness-specific improvisation
- risk_if_implemented_early: generic Context or Memory architecture
- promotion_trigger: B-0008 identifies a bounded first use case
- validation_level: NONE
- live_validation_trigger: a meaningful coding-harness context path exists
- related: B-0008, B-0009
