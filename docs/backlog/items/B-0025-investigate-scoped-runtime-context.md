# B-0025 — Investigate scoped runtime context

- type: INVESTIGATION
- status: DEFERRED
- decision_maturity: DISCOVERED
- necessity: FUTURE_REQUIRED
- architectural_significance: STRUCTURAL
- urgency: DEFERRED
- evidence_basis: RESEARCH
- scope: narrow propagation of live execution facts
- parent: none

## Problem / value

Investigate correlation, causal linkage, deadline, cancellation, occurrence and
attempt identity, session association, agent-runtime association, and workflow
association for live execution.

## Evidence / invariants

A subsystem should receive the smallest typed contextual projection needed for
its responsibility, not arbitrary higher-level runtime objects or a universal
mutable bag. This rejects `dict[str, Any}` universal context, global mutable
runtime state, and automatic propagation of Agent, Session, Workflow, or
Authorization objects. It does not choose arguments, immutable values, context
variables, envelopes, or another propagation mechanism.

## Dependencies / risks / validation

- hard_dependencies: none
- pressure_dependencies: B-0010, B-0017, B-0026, B-0029
- operational_dependencies: cross-boundary live execution facts
- consumers: future active orchestration and runtime control
- established_invariants: current Runtime is interaction-stateless and Session-owned state remains local
- unresolved_semantics: required facts, scopes, propagation, correlation, causal linkage, deadlines, cancellation, and lifecycle association
- risk_if_deferred: explicit narrow arguments remain available
- risk_if_implemented_early: universal mutable Context or global runtime state
- promotion_trigger: multiple boundaries need the same live facts with unsafe broad-object passing
- validation_level: NONE
- live_validation_trigger: bounded harness needs correlated cancellation or deadline facts across components
- first_harness_consumer: Local coding worker / Qwen
- second_harness_trigger: Codex requires unchanged scoped facts
- related: B-0010, B-0017, B-0026, B-0029
