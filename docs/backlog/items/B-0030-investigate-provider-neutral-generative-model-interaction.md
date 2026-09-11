# B-0030 — Investigate provider-neutral generative-model interaction

- type: INVESTIGATION
- status: BACKLOG
- decision_maturity: NEEDS_INVESTIGATION
- necessity: REQUIRED
- architectural_significance: STRUCTURAL
- urgency: SOON
- evidence_basis: MULTIPLE
- scope: model interaction semantics and provider adaptation boundaries
- parent: none

## Problem / value

Determine the minimum provider-neutral model request/response semantics needed
by a bounded worker while retaining provider protocol, wire representation, and
errors at adaptation boundaries. Investigate messages and model context input,
final/streaming output, action-call and reasoning representations, usage,
errors, feature discovery, context limits, model identity/configuration, and
the Qwen/llama.cpp, Codex, and future-provider boundary.

## Evidence / invariants

Existing `Agent` is a narrow final-message contract and Codex is its first
concrete implementation; it does not settle broader generative-model semantics.
Provider-specific protocol, wire representation, and errors must not silently
become generic model semantics. Routing pressure—quality, latency, cost,
capability, policy, health, context size, jurisdiction, and availability—stays
inside this investigation and does not authorize a router.

## Dependencies / risks / validation

- hard_dependencies: none
- pressure_dependencies: B-0008, B-0009, B-0020, B-0027, B-0029
- operational_dependencies: bounded multi-provider or action-capable model path
- consumers: first Qwen coding worker, Codex, and future provider adapters
- established_invariants: serving/provider mechanics and errors remain provider-local; current Agent protocol remains narrow
- unresolved_semantics: request/response, streaming, actions, reasoning, usage, capability discovery, identity/configuration, provider adaptation, and routing
- risk_if_deferred: worker may require a narrowly local adapter first
- risk_if_implemented_early: lowest-common-denominator provider client or model router
- promotion_trigger: bounded Qwen worker needs semantics not representable by current Agent contract, or a second provider needs the same meaning
- validation_level: NONE
- live_validation_trigger: real model interaction returns context/action result and continues meaningfully
- first_harness_consumer: Local coding worker / Qwen
- second_harness_trigger: Codex or another provider uses unchanged core semantics
- related: B-0008, B-0009, B-0020, B-0027, B-0029
