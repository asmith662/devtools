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

## DeepSeek Harness / Aider evidence (2026-10-23)

DeepSeek records synthetic not-started versus outcome-unknown Tool results from
turn/step/call evidence and drains started calls on cancellation. It does not
blindly retry an uncertain side effect. Aider's retained successful edit blocks
after later failures further illustrate cancellation/failure versus rollback.
Engineering26 is selected as a real stopped-owner byte-mismatch recovery flow;
its original failed receipt remains unchanged. No replay or new recovery grant
is created by this evidence.

See the [pinned source-and-test comparison](../../research/agent-harness-mechanism-review.md#deepseek-harness-and-aider-source-and-test-audit-2026-10-23)
and [five-flow audit plan](../../research/development-lifecycle-audit-plan.md).
Status, dependencies, decision maturity and promotion trigger remain unchanged.

## Executed five-flow lifecycle evidence (2026-10-23)

Recovery26 preserves original CLEANUP_RECONCILIATION_REQUIRED, exact one-LF byte mismatch and later sealed return to baseline. Process-stop confirmation is asserted without a linked process-state/time record. Commit-intent tests reconcile an already-created commit; historical publication receipts lack a separate post-push ref/time. No event absence proves no effect, and no restoration proves arbitrary external rollback. Preserve current explicit default-No recovery.

See the [source/evidence audit and priority crosswalk](../../research/development-lifecycle-observability-audit.md)
and its [authenticated metadata](../../research/development-lifecycle-observability-evidence-20261023.json).
Status, dependencies, decision maturity and promotion trigger remain unchanged.
