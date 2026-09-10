# B-0008 — Investigate repository-context discovery for coding harnesses

- type: INVESTIGATION
- status: BACKLOG
- decision_maturity: NEEDS_INVESTIGATION
- necessity: REQUIRED
- architectural_significance: STRUCTURAL
- urgency: SOON
- evidence_basis: MULTIPLE
- scope: coding-harness repository discovery and selected context
- parent: B-0002

## Problem / value

Determine the smallest repository-discovery and context-selection boundary
required by coding harnesses.

## Current evidence / consumers

The first consumer is the Local coding worker / Qwen. Existing paths,
filesystem, regex, and Markdown structures are inputs, not a repository-context
implementation.

Questions include inventory, file discovery, source retrieval, text search,
Python symbols/imports, Markdown sections, snapshot identity, selected-context
provenance, budgeting, truncation, trust/staleness, and request semantics.

## Dependencies / risks / validation

- hard_dependencies: none
- pressure_dependencies: B-0003
- operational_dependencies: paths, filesystem, regex
- consumers: Local coding worker / Qwen
- established_invariants: Context is currently conversational, not repository state
- unresolved_semantics: coding-specific versus reusable boundary
- risk_if_deferred: harness-specific discovery is improvised
- risk_if_implemented_early: generic Context or Memory architecture
- promotion_trigger: one frozen worker story identifies minimum inputs
- validation_level: NONE
- live_validation_trigger: a bounded coding harness consumes selected context
- first_harness_consumer: Local coding worker / Qwen
- second_harness_trigger: Codex needs equivalent discovery semantics
- related: B-0002, B-0009, B-0016
