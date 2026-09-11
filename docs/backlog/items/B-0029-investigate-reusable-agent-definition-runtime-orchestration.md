# B-0029 — Investigate reusable agent definition and runtime orchestration

- type: INVESTIGATION
- status: DEFERRED
- decision_maturity: DISCOVERED
- necessity: FUTURE_REQUIRED
- architectural_significance: STRUCTURAL
- urgency: DEFERRED
- evidence_basis: MULTIPLE
- scope: agent behavior, active runtime, orchestration, and supervision boundaries
- parent: none

## Problem / value

Investigate whether and how to distinguish agent definition/behavior, agent
identity, active agent runtime, orchestration, model interaction, context
acquisition, action handling, loop progression, supervision, escalation,
cancellation/control, and runtime occurrence.

## Evidence / invariants

Agent behavior is not automatically authorization identity; tool execution
infrastructure is not automatically Agent Runtime; and conversation/session
state is not automatically Agent Runtime. Keep definition and active runtime in
one investigation until concrete pressure warrants separation. The first Qwen
worker validates generic boundaries but does not define them.

## Dependencies / risks / validation

- hard_dependencies: none
- pressure_dependencies: B-0008, B-0009, B-0020, B-0025, B-0026, B-0030
- operational_dependencies: a bounded worker path with active orchestration
- consumers: future Qwen/Codex and supervision harnesses
- established_invariants: current Agent protocol is a narrow single-message extension seam; Runtime coordinates one interaction
- unresolved_semantics: definition/runtime distinction, identity, orchestration, loop progression, supervision, escalation, control, and occurrence association
- risk_if_deferred: first worker can use a deliberately bounded local harness
- risk_if_implemented_early: universal AgentRuntime or orchestration framework
- promotion_trigger: multiple harnesses need shared active orchestration semantics
- validation_level: NONE
- live_validation_trigger: bounded worker requires repeated model/context/action progression
- first_harness_consumer: Local coding worker / Qwen
- second_harness_trigger: Codex uses unchanged orchestration semantics
- related: B-0008, B-0009, B-0020, B-0025, B-0026, B-0030
