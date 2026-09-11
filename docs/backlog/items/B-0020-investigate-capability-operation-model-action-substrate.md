# B-0020 — Investigate capability, operation, and model-action substrate

- type: INVESTIGATION
- status: DEFERRED
- decision_maturity: DISCOVERED
- necessity: FUTURE_REQUIRED
- architectural_significance: STRUCTURAL
- urgency: DEFERRED
- evidence_basis: MULTIPLE
- scope: model-facing capabilities, operation contracts, bindings, and proposals
- parent: none

## Problem / value

Determine whether the existing experimental `Tool`/`ToolRunner` seams and
their command/filesystem bridges provide an appropriate substrate for
model-facing actions, and what additional semantics are genuinely required.
The repository currently has no `OperationDescriptor`, `Binding`, or `Registry`
public primitive; this record must not assume those names or types.

## Evidence / invariants

Investigate semantic capability, executable operation, declarative contract,
runtime implementation or binding, canonical contract, provider-specific schema
projection, accessible and model-visible sets, contextual action discovery,
proposal normalization/materialization, contract evolution, multiple eligible
implementations, and eligibility versus selection. Model proposals remain
untrusted until framework-governed; routing or binding selection must not
manufacture authority. Generalization requires repeated consumers with shared
semantics, not merely one tool bridge.

## Dependencies / risks / validation

- hard_dependencies: none
- pressure_dependencies: B-0008, B-0009, B-0012, B-0030
- operational_dependencies: a bounded model-facing action consumer
- consumers: future Qwen/Codex harness action paths
- established_invariants: existing Tools are experimental local contracts; Tool admission is not authorization
- unresolved_semantics: capability/operation/contract/binding distinctions, schema projection, visible/accessed sets, proposal materialization, eligibility, and selection
- risk_if_deferred: first harness may need a narrow local bridge
- risk_if_implemented_early: generic Capability, Tool, registry, binding, or router framework
- promotion_trigger: two consumers need a common governed model-facing action boundary
- validation_level: NONE
- live_validation_trigger: a bounded harness proposes an action through a reusable boundary
- first_harness_consumer: Local coding worker / Qwen
- second_harness_trigger: Codex requires unchanged core action semantics
- related: B-0008, B-0009, B-0012, B-0030
