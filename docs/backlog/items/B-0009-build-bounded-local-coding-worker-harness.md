# B-0009 — Build the first bounded local coding-worker harness

- type: STORY
- status: BLOCKED
- decision_maturity: SEMANTICS_PARTIAL
- necessity: REQUIRED
- architectural_significance: HARNESS_LOCAL
- urgency: SOON
- evidence_basis: REAL_USE
- scope: first bounded local Qwen coding-worker harness
- parent: B-0003

## Problem / value

Create the first bounded Qwen coding-worker harness after its minimum
repository-context boundary is known.

## Evidence / invariants

Qwen serving is validated. The harness must create real pressure for framework
acceptance but must not predefine a universal tool loop, execution envelope, or
effect model.

## Future effectiveness evidence

When the harness is evaluated, retain enough evidence to determine whether the
local worker reduces strong-model or Codex effort needed for an accepted result.
Useful future evidence may include first-pass acceptance, supervisor or Codex
correction turns, observable supervisor prompt/completion use, takeover, and
review/correction effort. This preserves an evaluation question; it does not
define a metric, benchmark schema, or token-accounting policy.

## Dependencies / risks / validation

- hard_dependencies: B-0008
- pressure_dependencies: B-0012, B-0016
- operational_dependencies: pinned Qwen serving profile
- blocked_by: sufficient B-0008 resolution
- consumers: Local coding worker / Qwen
- unresolved_semantics: exact tool/effect loop
- risk_if_deferred: no live coding-harness consumer
- risk_if_implemented_early: context/effect semantics become fixed
- promotion_trigger: bounded repository-context requirements are designed
- validation_level: LIVE_SINGLE_HARNESS
- live_validation_trigger: harness can inspect, request an operation, and return evidence
- first_harness_consumer: Local coding worker / Qwen
- second_harness_trigger: Codex uses unchanged core semantics
- related: B-0003, B-0008, B-0016
