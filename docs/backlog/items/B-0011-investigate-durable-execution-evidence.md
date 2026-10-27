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

## Evidence/usage/operator audit — 2026-10-25

The frozen12-body Evidence/usage audit identifies actual process-local terminal/model inspectors, a separate mutable usage snapshot and repository usage CLI, and app-local Qwen/WorkCycle records read directly by dashboard. Native Qwen does not automatically emit normalized InvocationMeasurement or store inspector Evidence. A bounded existing-record adapter for a real operator consumer is preferable to a second store, but source/task/occurrence identity joins, conflict/unknown semantics, capture/privacy and retention need an explicit decision. Two collection P2 defects have distinct pending proposals; no durable consumer implementation or status promotion is authorized.

See the [source, probes and consumer assessment](../../research/evidence-usage-and-operator-audit.md). Deferred status, decision maturity, dependencies and promotion trigger remain unchanged; no implementation, approval or closure.

## Core Identity/Time consumer evidence — 2026-10-26

A controlled backward UTC clock step in the maintained llama.cpp send/observation path yields ValueError after one deterministic transport-double completion; the forward-clock observed and backward-clock unobserved controls return the response. ModelInteractionObservation requires ordered wall instants, and captured duration subtracts those instants. This is a concrete case of the already documented ADR-0001 observation-versus-model outcome limitation, not a Timestamp invariant failure, live model result or new retry permission. Carry clock-step/monotonic elapsed and response/observer failure separation into the model/Evidence consumer decision; no clock framework, persistence schema or automatic suppression is approved. [Exact probes and review](../../research/core-identity-and-time-audit.md). Status and promotion trigger remain unchanged. `audit:core-identity-time:32c91a17:20261026`.

## ModelInteraction/Serving evidence — 2026-10-26

ModelInteraction/Serving audit on `a7a49cc18f3b40a5bf4e3897ca30d9a5cddc30d1`: all30 selected bodies/export/marker surfaces (7,119 lines) fully reviewed,321 focused plus113 real-consumer deterministic tests pass.44 independent cases reproduce five bounded P2 families (UTF8 normalization, vLLM response framing/shape, readiness writer cleanup, registry-port/tag admission, strict Tool JSON). See [report](../../research/model-interaction-and-serving-audit.md) and [exact evidence](../../research/code-audit/model-interaction-serving-assurance.json). No source/test change, live inference or new protected gate. Completed-success observation remains optional and can fail after response/usage normalization; backward wall time refuses before callback. Native Qwen default adapter has no observer, Inspector is not automatic native ingestion. Preserve existing missing-consumer, privacy and failure-correlation obligations; no new clock/observer duplicate or policy approval. Existing status, decision maturity, dependencies, approvals and authority remain unchanged. `audit:model-interaction-serving:a7a49cc1:20261026`.

## ModelInteraction/Serving repair evidence — 2026-10-26

Observer/capture-result and clock decision remains explicitly unapproved; normalized native Evidence ingestion/correlation is not delivered by these P2 corrections. [Delivered repair](../../development/model-serving-contract-repair.md), production `5125ab6a847ee1844913c006d801b01f5fea7cc4`, normal PR32, verified main `a602dae60b3a7c71bdd1c1231613143c309292c1`. No state/maturity/approval/parent closure or new authority. `repair:model-serving-contracts:5125ab6a:20261026`.

## Agents/Conversation/Runtime audit — 2026-10-26

Existing ExecutionInspector retains local terminal facts before optional sink; sink failure is contained and not automatically durable/operator-visible. ModelInteractionInspector has no capture-failure contract. Option B requires explicit provider-local failure reporting and real host/policy consumer, not ModelResponse metadata or a new store. Known response/usage must survive capture failure without fabricating Evidence/refunding unknown consumption. [Exact source/probe/consumer evidence](../../research/agents-conversation-and-runtime-audit.md). No status, maturity, approval, dependency or parent closure changes. `audit:agents-conversation-runtime:87f5b9d2:20261026`.

## Codex contract repair evidence

Both bounded Codex defects delivered. Optional capture policy remains unapproved: per-invocation correlation, secondary-report failure, privacy/retention and mandatory evidence admission remain explicit decisions. [Delivered correction](../../development/codex-input-and-metadata-repair.md), normal PR35 and verified main `4189fffd79eaaa64debfc7b601bb729de92002de`. No state, approval, grant or parent closure. `repair:codex-input-metadata:c39c1f0f:20261026`.

## Persistence/Recovery audit evidence

Conversation storage has no Evidence/attempt/usage schema or automatic Runtime persistence. Model Inspector callback/local retention is not durability; ExecutionInspector sink accept does not specify flush/commit. OptionB can preserve primary response independently of storage, but durable correlated failure capture needs a real owner/consumer and approved privacy/retention contract. [Full review and independent evidence](../../research/persistence-and-recovery-audit.md). Existing status, decision maturity, dependencies and authority unchanged. `audit:persistence-recovery:206d58e2:20261026`.

## SQLite repair delivery evidence

Conversation store correctness is improved; no EvidenceSink durability, normalized capture ingestion or automatic Runtime checkpoint is added. Four OptionB approval conditions remain unchanged. [Verified implementation and limitations](../../development/persistence-sqlite-contract-repair.md), normal PR38, main `c6ca6a2f64d729a8192cde1109e68b4a1830c7d2`. Existing state, maturity, dependencies and parent scope unchanged. `repair:persistence-sqlite:233b170e:20261026`.
