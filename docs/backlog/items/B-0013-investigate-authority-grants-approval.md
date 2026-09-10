# B-0013 — Investigate authority, grants, authorization, and approval

- type: INVESTIGATION
- status: DEFERRED
- decision_maturity: DISCOVERED
- necessity: FUTURE_REQUIRED
- architectural_significance: FOUNDATIONAL
- urgency: DEFERRED
- evidence_basis: RESEARCH
- scope: authority, grant, authorization, and approval semantics
- parent: B-0005

## Problem / value

Determine principals, grants, scopes, delegation, revocation, approval
conditions, escalation, and enforcement points only when a governed mutation
needs them.

## Established invariant / validation expectation

Approval is not authorization. A meaningful future live validation is:

    harness requests forbidden operation
    -> framework denies it
    -> effect does not occur
    -> denial is observable

## Dependencies / risks / validation

- hard_dependencies: B-0012 when mutating effects are governed
- pressure_dependencies: B-0014
- operational_dependencies: discoverable but forbidden harness capability
- consumers: future governed mutation harnesses
- unresolved_semantics: principals, grants, scopes, revocation, delegation
- risk_if_deferred: none before reusable governed mutation
- risk_if_implemented_early: policy engine without enforcement boundary
- promotion_trigger: real harness needs exposure plus denial
- validation_level: NONE
- live_validation_trigger: forbidden operation reaches real harness boundary
- first_harness_consumer: Local coding worker / Qwen
- second_harness_trigger: second harness exercises same denial
- related: B-0005, B-0012, B-0014, B-0016
