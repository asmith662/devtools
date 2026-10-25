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

## DeepSeek Harness / Aider evidence (2026-10-23)

DeepSeek Session.append commits frozen in-memory events before contained
observers; writer buffering and explicit durability barriers remain separate.
Original event history survives model-surface replacement, but persisted history
does not authenticate effects or publication. The selected real local flow receipts
provide concrete Evidence consumers and missing joins to audit, not authority to
implement a Session/Event/Trace layer or change durable schemas.

See the [pinned source-and-test comparison](../../research/agent-harness-mechanism-review.md#deepseek-harness-and-aider-source-and-test-audit-2026-10-23)
and [five-flow audit plan](../../research/development-lifecycle-audit-plan.md).
Status, dependencies, decision maturity and promotion trigger remain unchanged.

## Executed five-flow lifecycle evidence (2026-10-23)

All21 selected inputs and297 historical files are fingerprinted; both closeout result/review subjects and protected log hashes are checked. Strong byte links coexist with mutable checkpoint files and missing occurrence links. Two27 physical CRLF hashes differ from LF Git blobs. Investigate explicit representation, capture and input-closure contracts rather than treating file checksums or a PASS as durable authority.

See the [source/evidence audit and priority crosswalk](../../research/development-lifecycle-observability-audit.md)
and its [authenticated metadata](../../research/development-lifecycle-observability-evidence-20261023.json).
Status, dependencies, decision maturity and promotion trigger remain unchanged.

## Production reconciliation evidence (2026-10-23)

Use the completed source/experiment adoption and fresh archive-member custody map alongside the five-flow audit. Original historical records remain authoritative; closeout revision is not candidate identity, current qwen documentation differs from its frozen archive version, and same-SSD packet checks are not off-volume protection. The pending reuse investigation d58697fd-bb03-4e98-bdac-fa29444fc6ff qualifies protected input closure without asserting invalid historical evidence.

See the [complete audit and prioritized roadmap](../../research/production-adoption-and-architecture-reconciliation.md)
and [source/custody identities](../../research/production-adoption-and-architecture-evidence-20261023.json).
Existing status, parent, dependencies, decision maturity and promotion trigger
remain unchanged; advisory research does not authorize implementation.

## Validation/publication audit evidence — 2026-10-25

The validation/publication audit authenticates real repository-local progress, intents and result/commit/ref receipts, plus filesystem temp-file fsync/atomic replace without parent-directory fsync. Those durable app records are not automatically the framework ExecutionInspector terminal Evidence store. Worker usage remains in app receipts; selected dashboard projection reads those records directly. Missing/unknown usage is not zero. The next frozen Evidence/usage cohort will inspect normalized ingestion, conflicts, deduplication and durable/operator consumers. No new store, serializer, approval or decision-maturity change is implied.

See the [source, independent probes and limitations](../../research/validation-review-publication-audit.md). This append-only evidence does not approve, dispatch or close the story.
