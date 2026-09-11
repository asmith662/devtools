# B-0028 — Investigate persistence and durable-state boundaries

- type: INVESTIGATION
- status: DEFERRED
- decision_maturity: DISCOVERED
- necessity: FUTURE_REQUIRED
- architectural_significance: STRUCTURAL
- urgency: DEFERRED
- evidence_basis: MULTIPLE
- scope: durability mechanics and domain-owned durable state semantics
- parent: none

## Problem / value

Investigate persistence mechanics, state ownership, atomicity, consistency,
checkpointing, resume, persisted attempts, session/workflow durability,
authorization/approval state, persistence failure, and reconstruction.

## Evidence / invariants

Persistence supplies durability mechanics; owning domains define state
semantics. Persistence or checkpointing does not by itself create exactly-once
external effects. Existing persistence is not execution persistence by default.

## Dependencies / risks / validation

- hard_dependencies: none
- pressure_dependencies: B-0011, B-0014, B-0021, B-0024, B-0027
- operational_dependencies: a real recovery, resume, or durable-state consumer
- consumers: future recovery, approval, audit, and workflow-like needs
- established_invariants: current Session persistence does not imply execution durability
- unresolved_semantics: owned state, atomicity, consistency, checkpoints, resume, reconstruction, authorization/approval state, and persistence failures
- risk_if_deferred: no durability claim is made before its owner is clear
- risk_if_implemented_early: generic persistence framework or false exactly-once claim
- promotion_trigger: real process loss requires recovery of domain-owned state
- validation_level: NONE
- live_validation_trigger: meaningful live recovery or resume scenario exists
- first_harness_consumer: unknown
- second_harness_trigger: a second domain needs unchanged durability mechanics
- related: B-0011, B-0014, B-0021, B-0024, B-0027
