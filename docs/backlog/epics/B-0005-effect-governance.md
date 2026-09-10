# B-0005 — Effect Governance

- type: EPIC
- status: DEFERRED
- decision_maturity: DISCOVERED
- necessity: FUTURE_REQUIRED
- architectural_significance: FOUNDATIONAL
- urgency: DEFERRED
- evidence_basis: MULTIPLE
- scope: governance of externally meaningful operations

## Problem / value

Preserve future pressure around operations causing effects and their governance.
Tool discovery or admission is not authorization.

## Dependencies / risks / validation

- hard_dependencies: none
- pressure_dependencies: B-0004
- operational_dependencies: a mutating harness capability
- children: B-0012, B-0013, B-0014
- unresolved_semantics: effect identity, outcome, policy, authority
- risk_if_implemented_early: universal Tool, Effect, or Capability model
- risk_if_deferred: bounded harnesses remain explicit/local
- promotion_trigger: a mutation crosses a reusable harness boundary
- validation_level: NONE
- live_validation_trigger: a real harness reaches a governed mutating boundary
