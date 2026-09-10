# B-0014 — Investigate retry, repair, and reconciliation semantics

- type: INVESTIGATION
- status: DEFERRED
- decision_maturity: DISCOVERED
- necessity: FUTURE_REQUIRED
- architectural_significance: FOUNDATIONAL
- urgency: DEFERRED
- evidence_basis: RESEARCH
- scope: retry, semantic repair, and reconciliation semantics
- parent: B-0005

## Problem / value

Preserve distinctions:

    transport failure -> possible retry
    failed tests -> semantic repair or new work
    unknown external outcome -> reconcile before repeat

## Dependencies / risks / validation

- hard_dependencies: B-0012 for effect outcome semantics
- pressure_dependencies: B-0010, B-0013
- operational_dependencies: safely repeatable or uncertain real effect
- consumers: future recovery behavior
- unresolved_semantics: classification, idempotency, repair identity
- risk_if_deferred: local recovery remains explicit until needed
- risk_if_implemented_early: generic retry policy with false safety claims
- promotion_trigger: real effect has uncertain outcome or needs safe retry
- validation_level: NONE
- live_validation_trigger: uncertain external effect outcome or safe retry need is observed
- related: B-0005, B-0010, B-0012, B-0013
