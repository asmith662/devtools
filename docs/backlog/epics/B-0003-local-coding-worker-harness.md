# B-0003 — Local Coding Worker Harness

- type: EPIC
- status: BLOCKED
- decision_maturity: SEMANTICS_PARTIAL
- necessity: REQUIRED
- architectural_significance: HARNESS_LOCAL
- urgency: SOON
- evidence_basis: REAL_USE
- scope: first bounded Qwen coding-worker harness

## Problem / value

Eventually provide a bounded Qwen coding-worker harness that can inspect work,
invoke governed capabilities, make bounded edits/effects, run checks, repair,
escalate, and produce supervisor-review evidence.

## Evidence / consumers / invariants

Qwen serving is operational. Missing work is harness/framework capability, not
model fit. No exact tool loop, execution envelope, or effect semantics are set.

## Dependencies / risks / validation

- hard_dependencies: B-0008
- pressure_dependencies: B-0012, B-0016
- operational_dependencies: pinned Qwen serving profile
- children: B-0009
- unresolved_semantics: tool loop and governed effect boundary
- risk_if_deferred: no real coding consumer pressure-tests framework work
- risk_if_implemented_early: unresolved semantics become fixed
- promotion_trigger: B-0008 resolves minimum context requirements
- validation_level: LIVE_SINGLE_HARNESS
- live_validation_trigger: bounded harness completes an end-to-end task path
- first_harness_consumer: Local coding worker / Qwen
- related: B-0008, B-0009, B-0016
