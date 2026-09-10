# B-0004 — Governed Execution Evolution

- type: EPIC
- status: DEFERRED
- decision_maturity: DISCOVERED
- necessity: FUTURE_REQUIRED
- architectural_significance: FOUNDATIONAL
- urgency: DEFERRED
- evidence_basis: MULTIPLE
- scope: future work, execution, attempt, and evidence semantics

## Problem / value

Preserve pressure to evolve beyond Runtime, Attempt, and terminal Evidence only
when real multi-attempt, durable, or causal work requires it.

## Evidence / invariants / dependencies

Existing Attempt/Evidence semantics are evidence, not disposable scaffolding.

- hard_dependencies: none
- pressure_dependencies: B-0005
- operational_dependencies: none
- children: B-0010, B-0011
- unresolved_semantics: work/execution/attempt hierarchy
- risk_if_implemented_early: invented hierarchy becomes infrastructure
- risk_if_deferred: none until current identities are insufficient
- promotion_trigger: user-visible work spans attempts, repairs, or takeover
- validation_level: NONE
- live_validation_trigger: unknown until a consumer exposes identity pressure
