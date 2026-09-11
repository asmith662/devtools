# B-0022 — Investigate delegation and acting authority

- type: INVESTIGATION
- status: DEFERRED
- decision_maturity: DISCOVERED
- necessity: FUTURE_REQUIRED
- architectural_significance: STRUCTURAL
- urgency: DEFERRED
- evidence_basis: RESEARCH
- scope: delegated authority and accountability across supervisor/worker paths
- parent: none

## Problem / value

Investigate acting on behalf of another actor, authority ownership and
provenance, attenuation, nested delegation, task scope, freshness/revocation,
accountability, and the relation among agent, authorization, and execution
identity. The motivating shape may be human → Codex → Qwen → governed action,
without selecting identities or delegation types.

## Evidence / invariants

Delegation must not manufacture authority the delegating actor did not possess.
Agent identity must not automatically be authorization identity.

## Dependencies / risks / validation

- hard_dependencies: none
- pressure_dependencies: B-0013, B-0016, B-0029
- operational_dependencies: a real multi-actor governed operation
- consumers: future supervision and multi-harness work
- established_invariants: approval and authority remain distinct
- unresolved_semantics: acting identity, ownership, provenance, attenuation, nesting, scope, revocation, freshness, and accountability
- risk_if_deferred: early supervision can remain explicit and local
- risk_if_implemented_early: Principal or Delegation framework without actual delegation
- promotion_trigger: a worker must act under another actor's constrained authority
- validation_level: NONE
- live_validation_trigger: second actor delegates a governed action to a harness
- first_harness_consumer: unknown
- second_harness_trigger: materially different harness needs the same delegation semantics
- related: B-0013, B-0016, B-0029
