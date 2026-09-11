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

Investigation must also distinguish repository inventory/addressability,
resolution of a known resource, discovery for an information need,
disclosure/access eligibility, selection/transformation, context
budgeting/compilation, and final model-facing context. These are semantic
questions, not a commitment to separate packages or APIs.

Further pressure separates candidate information from its eventual disclosure,
ranking, transformation, synthesis, deduplication, truncation, and budgeting.
Resolving a known resource is not the same question as discovering relevant
information. Repository mutation may invalidate prior compiled context. Action
or tool-discovery information also consumes model context, without implying it
shares repository discovery implementation.

Candidate context material includes authoritative source material, excerpts,
deterministic transformations, summaries, syntheses, instructions, tool output,
and retained information. Derived material must not silently acquire the
authority of its source. Source/derivation provenance,
authoritative-versus-derived classification, freshness/staleness, disclosure
eligibility, and trust/confidence remain unresolved. Future investigation may
distinguish resolution, retrieval, context access, compilation, and model
context, but need not make them separate packages. Contextual information must
remain narrow and explicit rather than becoming an arbitrary universal Context
container.

## Dependencies / risks / validation

- hard_dependencies: none
- pressure_dependencies: B-0003
- operational_dependencies: paths, filesystem, regex
- consumers: Local coding worker / Qwen
- established_invariants: Context is currently conversational, not repository state
- unresolved_semantics: coding-specific versus reusable boundary; discovery, access, selection, compilation, provenance, and trust boundaries
- risk_if_deferred: harness-specific discovery is improvised
- risk_if_implemented_early: generic Context, Memory, retrieval, or compiler architecture
- promotion_trigger: one frozen worker story identifies minimum inputs
- validation_level: NONE
- live_validation_trigger: a bounded coding harness consumes selected context
- first_harness_consumer: Local coding worker / Qwen
- second_harness_trigger: Codex needs equivalent discovery semantics
- related: B-0002, B-0009, B-0016
