# B-0034 — Investigate uncertain-effect reconciliation

- type: INVESTIGATION
- status: DEFERRED
- decision_maturity: DISCOVERED
- necessity: FUTURE_REQUIRED
- architectural_significance: FOUNDATIONAL
- urgency: DEFERRED
- evidence_basis: RESEARCH
- scope: reconciliation before repeating an externally meaningful operation
- primary_domain: governance
- supporting_domains: execution, observability, persistence
- split_from: B-0014

## Problem / value

Communication failure does not prove an effect failed. Determine how a future
governed operation distinguishes known success, known failure, and uncertain
outcome before repetition. Cancellation is not rollback.

- hard_dependencies: B-0012
- pressure_dependencies: B-0024
- operational_dependencies: uncertain outcome of a real governed effect
- promotion_trigger: repetition could duplicate an externally meaningful effect
- validation_level: NONE

## Recovered-input / pinned mechanism evidence (2026-10-23)

The [source/test comparison](../../research/agent-harness-mechanism-review.md#pydantic-ai-execution-order-cancellation-and-state)
shows completed parallel results retained in interrupted history even when ordered
result events were not emitted. This narrows some redispatch ambiguity, but an
effect without retained result or an abandoned worker thread is not rolled back.
Devtools Checkout source restoration and WorkCycle commit/ref reconciliation are
operation-specific, not universal effect reversal. Original candidate17 is
research evidence here, not a blanket cancellation bug or retry authorization.
