# B-0031 — Investigate generic execution lifecycle promotion

- type: INVESTIGATION
- status: DEFERRED
- decision_maturity: READY_FOR_DESIGN
- necessity: FUTURE_REQUIRED
- architectural_significance: FOUNDATIONAL
- urgency: DEFERRED
- evidence_basis: MULTIPLE
- scope: promotion of generic Run, Step, and Attempt lifecycle semantics
- primary_domain: execution
- supporting_domains: agents, orchestration, observability, persistence
- split_from: B-0004

## Problem / value

The taxonomy resolves `Run -> Step -> Attempt`; current `InteractionAttempt`
is a specialized Runtime lifecycle and is not the generic Attempt. Determine
whether a reusable consumer now requires generic lifecycle implementation.

## Promotion / boundaries

Do not create generic lifecycle values from terminology alone. Promote only
when a bounded Agent or orchestration consumer needs stable logical-work,
retry, or multi-step identity beyond `InteractionAttempt`.

- hard_dependencies: none
- pressure_dependencies: B-0010
- operational_dependencies: reusable multi-step consumer
- promotion_trigger: a consumer cannot remain honest with specialized InteractionAttempt
- validation_level: NONE
