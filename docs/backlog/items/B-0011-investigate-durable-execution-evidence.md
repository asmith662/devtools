# B-0011 — Investigate durable execution Evidence

- type: INVESTIGATION
- status: DEFERRED
- decision_maturity: DISCOVERED
- necessity: FUTURE_REQUIRED
- architectural_significance: STRUCTURAL
- urgency: DEFERRED
- evidence_basis: REPOSITORY
- scope: durable evidence and recovery beyond process-local terminal Evidence
- primary_domain: observability
- supporting_domains: persistence, execution, governance
- parent: B-0004

## Problem / value

Current terminal Evidence is immutable, in-process observability about an
InteractionAttempt. `ExecutionInspector` is process-local. Determine whether a
real recovery, resume, or audit consumer requires durable Evidence without
making Persistence own Evidence semantics or reintroducing execution ownership
of Evidence.

- hard_dependencies: none
- pressure_dependencies: B-0027, B-0031
- operational_dependencies: durable recovery or audit consumer
- promotion_trigger: recovery, resume, or external audit requires durable evidence
- validation_level: NONE

## Custody and consumer evidence (2026-10-23)

The [initial custody inventory](../../development/artifact-custody-inventory.md)
records existing durable app/experiment receipts, usage storage, archives and
permission-limited preservation regions. Their existence does not mean the
process-local terminal Evidence inspector has a framework durable-store adapter;
conversely, that missing adapter does not mean all execution evidence is volatile.

Recoverability and exact original receipt identities are concrete audit concerns.
Qualify the actual recovery/consumer and schema/authority boundaries first. The
separate pending custody proposal is operational review, not authorization for
a generic Evidence store or cache deletion. Existing deferred disposition and
promotion trigger are retained.
