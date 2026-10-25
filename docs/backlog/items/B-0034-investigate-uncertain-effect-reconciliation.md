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

## Validation/publication audit evidence — 2026-10-25

An independently authored tiny Git/bare-remote probe lost acknowledgment after a real push. Retrying the maintained publish helper observed the exact intended commit and issued no second push; advancing the remote caused refusal and preserved the new ref. This is a verified operation-specific reconciliation subset, not exactly-once arbitrary external effects or GitHub PR equivalence. Intents precede effects and completion records follow them; missing completion remains uncertain. Existing scripted lifecycle tests cover commit/push resume and interrupted installation. Generic policy, deferred status and authority remain unchanged.

See the [source, independent probes and limitations](../../research/validation-review-publication-audit.md). This append-only evidence does not approve, dispatch or close the story.

## Evidence/usage/operator audit — 2026-10-25

Independent temporary subprocess exits after a recorded filesystem effect and before normal completion; usage writer lease remains and retry refuses. Runtime/Tool cancellation has no rollback or zero-usage implication. Prior closeout helper also durably appended review advisories before a reporting failure, then duplicated them by checking reference instead of canonical decision_reference. Immutable duplicates were preserved. This is caller retry reconciliation, not proof Intake.review promises idempotency; legitimate repeated reviews must not be globally content-deduplicated. Current audit checks exact existing capture/review identity before retry; no new general reconciliation engine or authority is approved.

See the [source, probes and consumer assessment](../../research/evidence-usage-and-operator-audit.md). Deferred status, decision maturity, dependencies and promotion trigger remain unchanged; no implementation, approval or closure.
