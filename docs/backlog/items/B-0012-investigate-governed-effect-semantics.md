# B-0012 — Investigate governed effect semantics

- type: INVESTIGATION
- status: DEFERRED
- decision_maturity: DISCOVERED
- necessity: FUTURE_REQUIRED
- architectural_significance: FOUNDATIONAL
- urgency: DEFERRED
- evidence_basis: MULTIPLE
- scope: governance boundary for externally meaningful operations
- parent: B-0005

## Problem / value

Determine the boundary for reusable operations that cause effects.

## Established invariants / uncertainty

Tool admission or discoverability is not authorization. Commands and existing
Tools remain independent local contracts. Do not create universal Tool, Effect,
Capability, or Operation nouns yet.

## Dependencies / risks / validation

- hard_dependencies: none
- pressure_dependencies: B-0013, B-0014
- operational_dependencies: real mutating harness capability
- consumers: future Qwen/Codex harnesses and mutation bridges
- established_invariants: tool admission or discoverability is not authorization
- unresolved_semantics: operation boundary, effect outcome, idempotency, and reconciliation contract
- risk_if_deferred: bounded harnesses use explicit local effects first
- risk_if_implemented_early: lowest-common-denominator operation framework
- promotion_trigger: mutation crosses reusable harness boundary
- validation_level: NONE
- live_validation_trigger: a real harness exposes a mutating operation across a reusable boundary
- related: B-0005, B-0013, B-0014
