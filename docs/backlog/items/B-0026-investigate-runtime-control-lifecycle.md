# B-0026 — Investigate runtime control and lifecycle

- type: INVESTIGATION
- status: DEFERRED
- decision_maturity: DISCOVERED
- necessity: FUTURE_REQUIRED
- architectural_significance: STRUCTURAL
- urgency: DEFERRED
- evidence_basis: MULTIPLE
- scope: cancellation, deadlines, ownership, cleanup, and interruption across execution
- parent: none

## Problem / value

Investigate cancellation and propagation, deadlines, attempt timeout, shutdown,
cleanup, resource ownership, interruption, partial work, and lifecycle
boundaries across model, tool, and execution activity.

## Evidence / invariants

Deadline and attempt timeout may be different semantics. Cancellation does not
automatically imply rollback, and remains distinct from failure. Existing
Runtime, CommandExecutor, and serving ownership/cleanup behaviors are evidence
to reconcile, not a mandate for a replacement control system.

## Dependencies / risks / validation

- hard_dependencies: none
- pressure_dependencies: B-0010, B-0014, B-0025, B-0029
- operational_dependencies: a live multi-boundary operation requiring control
- consumers: future harness orchestration and governed effects
- established_invariants: provider and command cleanup remain locally owned today
- unresolved_semantics: cancellation propagation, deadline versus timeout, ownership, cleanup precedence, shutdown, partial work, and lifecycle boundaries
- risk_if_deferred: existing local lifecycle semantics remain explicit
- risk_if_implemented_early: global control plane or cancellation architecture without shared consumer evidence
- promotion_trigger: live operation spans components whose cancellation/cleanup semantics conflict
- validation_level: NONE
- live_validation_trigger: cancellation interrupts model or tool work while preserving cleanup and outcome evidence
- first_harness_consumer: Local coding worker / Qwen
- second_harness_trigger: Codex requires unchanged control semantics
- related: B-0010, B-0014, B-0025, B-0029
