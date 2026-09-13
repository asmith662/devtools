# B-0028 — Investigate persistence and durable-state boundaries

- type: INVESTIGATION
- status: DEFERRED
- decision_maturity: DISCOVERED
- necessity: FUTURE_REQUIRED
- architectural_significance: STRUCTURAL
- urgency: DEFERRED
- evidence_basis: MULTIPLE
- scope: durability mechanics and domain-owned recovery state
- primary_domain: persistence
- supporting_domains: execution, governance, observability, orchestration

## Problem / value

Conversation persistence is implemented and retains historical durable schema
names where compatibility requires them. It does not imply Run recovery,
InteractionAttempt persistence, approval state, checkpointing, or exactly-once
effects.

Determine durable state only when a real process-loss, recovery, resume, or
workflow consumer identifies its owning domain.

- hard_dependencies: none
- pressure_dependencies: B-0011, B-0024, B-0027, B-0034, B-0038
- operational_dependencies: real recovery or durable-state consumer
- promotion_trigger: process loss requires recovery of domain-owned state
- validation_level: NONE
