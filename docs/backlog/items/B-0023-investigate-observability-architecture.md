# B-0023 — Investigate observability architecture

- type: INVESTIGATION
- status: DEFERRED
- decision_maturity: DISCOVERED
- necessity: FUTURE_REQUIRED
- architectural_significance: STRUCTURAL
- urgency: DEFERRED
- evidence_basis: MULTIPLE
- scope: future Trace and Telemetry projections at meaningful boundaries
- primary_domain: observability
- supporting_domains: execution, models, tools, governance, evaluation

## Problem / value

The authorized candidate-discrimination increment promotes a narrow historical
usage projection over existing ModelUsage/InvocationMeasurement: metadata-only
Codex import, identity reconciliation, window reporting and empirical forecasts.
Its [package contract](../../../src/devtools/observability/usage/docs/overview.md)
does not resolve this broader investigation or introduce Event/Trace/Telemetry.

Current terminal Evidence is immutable factual observation about
InteractionAttempt outcomes. Trace and Telemetry are distinct future concerns:
causal/temporal structure and operational measurement respectively.

Determine shared semantics only when multiple consumers need correlated
observations. Do not introduce Event infrastructure, OpenTelemetry, metrics,
or a global observer merely from this record.

[ADR-0001](../../architecture/decisions/ADR-0001-cohesive-model-interaction-boundary.md)
approves a narrow shared instance of that boundary: capture-policy-controlled
`ModelInteractionEvidence` is Evidence, not Trace or Telemetry. Observability
owns capture, manifests, construction, collection, and inspection; model and
execution operation remains independent of observability. Generic Trace and
Telemetry remain deferred.

Current model-interaction observation covers successfully completed and
normalized responses. Equivalent provider/model failure Evidence is absent; an
observer callback can fail after a response exists; Runtime
`InteractionAttemptId` and `ModelInteractionId` have no automatic association;
and capture-controlled Evidence is not necessarily exact request/response or
replay material. Future consumers must preserve model/provider outcome,
observation failure, and outer orchestration outcome as distinct, correlate
layer-local identities without redefining them, and state capture/replay
strength honestly. These are implementation/conformance pressures, not grounds
for a global observer, generic Event system, or broadened Runtime.

Provider/model alias, requested settings, serving profile, exact revision,
effective defaults, quantization/runtime, and measurement boundaries likewise
carry only the identity or provenance strength actually observed. Unknown
hosted-provider revisions remain unknown; latency measures with different
boundaries are not interchangeable.

- hard_dependencies: none
- pressure_dependencies: B-0011
- operational_dependencies: consumer needing causal or operational evidence beyond terminal result
- promotion_trigger: multiple consumers need equivalent observations at shared boundaries
- validation_level: NONE

## Source-backed reconciliation observations (2026-10-23)

The [initial gap map](../../research/architecture-reconciliation-inventory.md#initial-observability-gap-map)
inspected inspectors, invocation/usage records, narrow Runtime, ToolRunner,
Command events and application/WorkCycle receipts. Existing implementations
already cover substantial Evidence and usage responsibilities. ToolRunner itself
does not provide invocation observation; best-effort Command events are not a
durable causal trace. No shared OTel/exporter implementation was found in the
scanned maintained owners, and pyproject declares no OTel dependency.

Failure accounting, capture/privacy, temporal/correlation boundaries and actual
shared consumers require investigation before a new type, exporter or event bus.
The next external review starts with pinned Qwen Code/Pydantic AI sources, then
DeepSeek Harness/Aider. Status/dependencies/promotion trigger remain unchanged;
these observations neither authorize tracing implementation nor conflate
Evidence, Trace and Telemetry.

## Recovered-input / pinned mechanism evidence (2026-10-23)

The [pinned harness comparison and local join/loss map](../../research/agent-harness-mechanism-review.md#devtools-end-to-end-correlation-map)
inspect model IDs, Runtime attempts, provider Tool IDs, app receipts, source/
validation hashes and WorkCycle review/commit refs. Upstream Qwen uses lifecycle
spans and explicit execution origins; Pydantic instrumentation includes validation
failure spans, run/conversation/call correlation and privacy paths. These show a
concrete comparison target, not durable authority or complete accounting.
Devtools still lacks automatic task→model occurrence→Tool→review joins in the
native application path. Capture/observer failures, dropped Command events and
unknown usage remain separate. Original candidates03/04 are related, not new
Trace/EventBus implementation grants. Deferred status/trigger remain.

## DeepSeek Harness / Aider evidence (2026-10-23)

DeepSeek separates Session log commits, live Agent notifications and capability
policy hooks; its OTel backend exports feedback-authorized Session records, not
automatically a joined development span tree. Aider prefers reported usage but
falls back to estimates and does not supply Devtools publication authority.
Existing Model/terminal Evidence, InvocationMeasurement, Command events and
application receipts are distinct local owners. The five-flow audit below must
qualify direct joins, missing failures, dropped events and capture/export policy
before choosing instrumentation. No new logger, event bus or exporter is selected.

See the [pinned source-and-test comparison](../../research/agent-harness-mechanism-review.md#deepseek-harness-and-aider-source-and-test-audit-2026-10-23)
and [five-flow audit plan](../../research/development-lifecycle-audit-plan.md).
Status, dependencies, decision maturity and promotion trigger remain unchanged.

## Executed five-flow lifecycle evidence (2026-10-23)

The five-flow audit authenticates request/response/call/check/review links but finds absent native Model/Runtime inspector composition, weak host freshness input/time links and no separate post-push ref/time in closeout. Recommend existing-record consumers/adapters first; a shared tracing interface or OTel spans remains a design alternative. Distinguish immutable records, lossy live events, correlation and durable/export consumers.

See the [source/evidence audit and priority crosswalk](../../research/development-lifecycle-observability-audit.md)
and its [authenticated metadata](../../research/development-lifecycle-observability-evidence-20261023.json).
Status, dependencies, decision maturity and promotion trigger remain unchanged.

## Production reconciliation evidence (2026-10-23)

Adoption audit confirms optional model/terminal inspectors are not composed into the native worker; usage CLI/controller consumers and application receipts do exist. Prioritize existing-record joins/consumers, failed realization accounting, report identity/time and separately observed remote ref after push. Immutable Evidence, live lossy events, usage and durability remain distinct; no OpenTelemetry/EventBus dependency or tracing base selected.

See the [complete audit and prioritized roadmap](../../research/production-adoption-and-architecture-reconciliation.md)
and [source/custody identities](../../research/production-adoption-and-architecture-evidence-20261023.json).
Existing status, parent, dependencies, decision maturity and promotion trigger
remain unchanged; advisory research does not authorize implementation.
