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
