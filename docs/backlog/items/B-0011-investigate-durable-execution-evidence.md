# B-0011 — Investigate durable execution Evidence

- type: INVESTIGATION
- status: DEFERRED
- decision_maturity: DISCOVERED
- necessity: FUTURE_REQUIRED
- architectural_significance: STRUCTURAL
- urgency: DEFERRED
- evidence_basis: REPOSITORY
- scope: durable evidence beyond in-process session persistence
- parent: B-0004

## Problem / value

Determine whether Attempt/Evidence must survive process loss, recovery, or audit.

## Evidence / invariants

Session persistence is semantic Session reconstruction, not execution
persistence. ExecutionInspector is process-local diagnostic state.

## Dependencies / risks / validation

- hard_dependencies: B-0010
- pressure_dependencies: B-0016
- operational_dependencies: durable recovery/audit consumer
- consumers: future recovery and audit needs
- unresolved_semantics: storage, delivery, retention, and replay boundaries
- risk_if_deferred: evidence is unavailable beyond process lifetime when required
- risk_if_implemented_early: generic event store without stable identity semantics
- promotion_trigger: real recovery, resume, or audit need
- validation_level: NONE
- live_validation_trigger: recovery, resume, or external audit is meaningful
- related: B-0004, B-0010, B-0016
