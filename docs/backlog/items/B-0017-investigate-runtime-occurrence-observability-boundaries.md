# B-0017 — Investigate runtime occurrence and observability boundaries

- type: INVESTIGATION
- status: DEFERRED
- decision_maturity: DISCOVERED
- necessity: FUTURE_REQUIRED
- architectural_significance: STRUCTURAL
- urgency: DEFERRED
- evidence_basis: MULTIPLE
- scope: runtime occurrence evidence and observability boundaries
- parent: none

## Problem / value

Determine the semantics of runtime occurrence needed for framework debugging
and live-harness validation, without assuming semantic outcome, logs,
structured events, traces, metrics, audit evidence, or durable Evidence are
interchangeable.

## Current evidence / invariants

ExecutionInspector is process-local diagnostic state; terminal Evidence is a
minimal immutable outcome record; command events are local command behavior.
Observability should target meaningful semantic boundaries rather than every
method, and instrumentation failure must not silently redefine primary work.

Questions include occurrence identity, time, ordering, correlation, causality,
attempt association, component-local diagnostics, and execution,
authorization, model, and tool occurrences. Observability and audit may consume
or project occurrence facts without being equivalent to them. Semantic domain
results must not automatically become runtime-occurrence records merely because
they need observation.

## Dependencies / risks / validation

- hard_dependencies: none
- pressure_dependencies: B-0010, B-0011, B-0012, B-0016, B-0023, B-0024, B-0025
- operational_dependencies: meaningful live harness or diagnostic consumer
- consumers: future harness validation and framework debugging
- established_invariants: runtime occurrence is not equivalent to semantic outcome or durable Evidence
- unresolved_semantics: occurrence identity/time/ordering, correlation, causality, attempt association, logs, events, traces, metrics, audit evidence, provider/transport/lifecycle boundaries, and observability failure behavior
- risk_if_deferred: live validation cannot establish required causal paths
- risk_if_implemented_early: universal Event, EventBus, telemetry middleware, or global observer
- promotion_trigger: a live acceptance needs proof of a boundary beyond its final result
- validation_level: NONE
- live_validation_trigger: a real harness must prove occurrence, denial, absence of execution, or causal continuation
- first_harness_consumer: Local coding worker / Qwen
- second_harness_trigger: Codex or another harness requires equivalent causal evidence
- related: B-0010, B-0011, B-0012, B-0016, B-0018, B-0023, B-0024, B-0025
