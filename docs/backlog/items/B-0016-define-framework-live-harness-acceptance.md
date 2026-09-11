# B-0016 — Define framework live-harness acceptance methodology

- type: INVESTIGATION
- status: BACKLOG
- decision_maturity: NEEDS_INVESTIGATION
- necessity: REQUIRED
- architectural_significance: STRUCTURAL
- urgency: SOON
- evidence_basis: MULTIPLE
- scope: progressive real-harness framework validation methodology
- parent: B-0015

## Problem / value

Define how structural framework primitives graduate from deterministic tests to
meaningful real-harness validation without creating a generic live-test runner.

## Validation pressures

Observability: real model conversation, tool request, tool execution, result,
continuation, and completion should yield an accurate causal observation.

Authority: test framework denial when a model requests forbidden operation, not
whether the model voluntarily obeys.

Cancellation: interrupt a real model/tool path, clean owned resources, preserve
cancellation identity/outcome, and capture observation.

Multi-harness: after Qwen validates a primitive, Codex or another harness uses
equivalent semantics without changing the core contract.

Final semantic results may not prove the required runtime path occurred. Future
acceptance may need causal occurrence evidence, for example model interaction
to proposal/materialization to authorization denial and absence of execution,
or context retrieval/compilation to tool execution, returned result, and model
continuation. These are examples, not an event schema.

## Dependencies / risks / validation

- hard_dependencies: none
- pressure_dependencies: B-0003, B-0011, B-0012
- operational_dependencies: meaningful specialized harness path
- consumers: future structural framework primitives
- unresolved_semantics: occurrence evidence, causal boundaries, evidence sufficiency, nondeterminism, provider/framework failures, and CI boundaries
- risk_if_deferred: framework semantics may be accepted from mocks alone
- risk_if_implemented_early: generic test framework before scenarios stabilize
- promotion_trigger: primitive has unit/integration coverage and a live path
- validation_level: INTEGRATION
- live_validation_trigger: a primitive has unit/integration coverage and a live path
- first_harness_consumer: Local coding worker / Qwen
- second_harness_trigger: Codex or another harness uses unchanged semantics
- related: B-0015, B-0009, B-0012, B-0013
