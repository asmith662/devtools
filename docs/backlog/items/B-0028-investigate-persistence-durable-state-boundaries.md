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

## Recovered-input / pinned mechanism evidence (2026-10-23)

Original candidate11 and [interrupted-history research](../../research/agent-harness-mechanism-review.md#pydantic-ai-execution-order-cancellation-and-state)
distinguish task-local verified state from Conversation and Memory. Pydantic core
retains completed returns on cancellation; durable workflow integration is a
separate backend. Qwen transcript reconstruction is not exactly-once effects.
Devtools already has raw receipts, source hashes, Checkout recovery and WorkCycle
Git reconciliation. Qualify the missing recovery consumer/owning domain before
any checkpoint store. The existing Memory proposal receives advisory evidence;
no backend, schema or lifecycle ownership changes.

## DeepSeek Harness / Aider evidence (2026-10-23)

The pinned DeepSeek handle interface separates accepted append from crash-survival
flush. JSONL live routing buffers, retains failed batches and rejects explicit
drains; close can release ownership while reporting failure. SessionStore.flush
reports listener participation, not a per-writer durability certificate. Memory-
only creation and persistence-required resume are different supported paths.
These are backend/lifecycle research inputs; Devtools snapshot persistence and
Checkout are not missing implementations of that upstream Session interface.

See the [pinned source-and-test comparison](../../research/agent-harness-mechanism-review.md#deepseek-harness-and-aider-source-and-test-audit-2026-10-23)
and [five-flow audit plan](../../research/development-lifecycle-audit-plan.md).
Status, dependencies, decision maturity and promotion trigger remain unchanged.

## Executed five-flow lifecycle evidence (2026-10-23)

Conversation JSON/SQLite state, source observations, check journals, native checkpoints and Checkout owner seals have separate owners. Completed protected evidence can be reused by closeout subject/passed condition; full plan/config/toolchain closure is not separately named by that subject. Qualify changed-input negative cases before stronger exact-tree reuse claims. No invalid historical gate or bypass is established by this source audit.

See the [source/evidence audit and priority crosswalk](../../research/development-lifecycle-observability-audit.md)
and its [authenticated metadata](../../research/development-lifecycle-observability-evidence-20261023.json).
Status, dependencies, decision maturity and promotion trigger remain unchanged.

## Production reconciliation evidence (2026-10-23)

Protected-gate reuse/input-closure now has a distinct bounded pending investigation d58697fd-bb03-4e98-bdac-fa29444fc6ff under B-0047, related to this durable-state boundary. Conversation persistence, native working-state/source checks, Checkout recovery and publication evidence retain separate ownership. No generic store, exactly-once guarantee or historical validation bypass inferred.

See the [complete audit and prioritized roadmap](../../research/production-adoption-and-architecture-reconciliation.md)
and [source/custody identities](../../research/production-adoption-and-architecture-evidence-20261023.json).
Existing status, parent, dependencies, decision maturity and promotion trigger
remain unchanged; advisory research does not authorize implementation.

## Persistence/Recovery audit evidence

All 11 Persistence paths now fully reviewed. Three exact P2 proposals own read coherence, initial schema atomicity and persisted text admission; no source correction in this checkpoint. Save replacement rollback/process restart controls pass; stale saves intentionally replace current state and unreferenced global message rows remain. Explicit checkpoint/custody/retention/consumer decisions remain broader than these repairs. [Full review and independent evidence](../../research/persistence-and-recovery-audit.md). Existing status, decision maturity, dependencies and authority unchanged. `audit:persistence-recovery:206d58e2:20261026`.
