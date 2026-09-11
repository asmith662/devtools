# B-0021 — Investigate approval and human-governance workflow

- type: INVESTIGATION
- status: DEFERRED
- decision_maturity: DISCOVERED
- necessity: FUTURE_REQUIRED
- architectural_significance: STRUCTURAL
- urgency: DEFERRED
- evidence_basis: RESEARCH
- scope: obtaining, waiting for, and revalidating human approval
- parent: none

## Problem / value

Separate approval semantics from the workflow that could obtain it. Investigate
approval request identity, approver eligibility, delivery/notification, waiting,
denial, expiration, reuse, persistence, multiple approvers, separation of
duties, suspension, resumption, and revalidation before continued execution.

## Evidence / invariants

Future pressure is: authorization determines approval is required; future
orchestration may obtain it; execution revalidates before continuing. Approval
evidence is not the workflow that obtains approval. No workflow, notification,
persistence, or UI architecture is selected here.

## Dependencies / risks / validation

- hard_dependencies: none
- pressure_dependencies: B-0013, B-0014, B-0026, B-0028
- operational_dependencies: a real governed action requiring human approval
- consumers: future governed mutation and supervision paths
- established_invariants: approval is not underlying authority
- unresolved_semantics: approval request, approver, delivery, waiting, expiration, reuse, separation of duties, suspension, resumption, and revalidation
- risk_if_deferred: approval remains explicitly local when first needed
- risk_if_implemented_early: workflow, notification, or approval subsystem without a real consumer
- promotion_trigger: a governed operation must wait for and resume after human approval
- validation_level: NONE
- live_validation_trigger: real harness operation requires approval before effect
- first_harness_consumer: unknown
- second_harness_trigger: another harness needs unchanged approval semantics
- related: B-0013, B-0014, B-0026, B-0028
