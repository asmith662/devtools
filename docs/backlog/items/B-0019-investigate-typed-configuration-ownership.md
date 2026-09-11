# B-0019 — Investigate typed configuration ownership

- type: INVESTIGATION
- status: DEFERRED
- decision_maturity: DISCOVERED
- necessity: FUTURE_REQUIRED
- architectural_significance: STRUCTURAL
- urgency: DEFERRED
- evidence_basis: REPOSITORY
- scope: future shared configuration ownership across framework consumers
- parent: none

## Problem / value

Determine when repeated framework pressure warrants typed shared configuration
rather than existing local package or provider configuration.

## Current evidence / invariants

Existing serving, runtime, and provider configuration is deliberately local.
Intended configuration is distinct from runtime execution state,
session/conversation state, workflow state, memory, and Evidence/audit state.
Configuration semantics are distinct from sources such as CLI, environment,
files, defaults, or programmatic construction.

Applicable policy for a concrete occurrence is distinct from configured
governance population. Future pressure includes provider/model and harness
configuration, context budgets, action/tool exposure, and execution behavior;
configuration source is not configuration semantics.

Runtime/session state, Conversation, caches, retrieved information, Audit, plan
history, and durable learned information must not automatically be collapsed
into "Memory." A Memory investigation is warranted only when a real consumer
requires durable retained-information semantics.

## Dependencies / risks / validation

- hard_dependencies: none
- pressure_dependencies: B-0003, B-0008, B-0012, B-0029, B-0030
- operational_dependencies: multiple consumers with materially shared configuration ownership
- consumers: future model/provider, harness, context-budget, capability exposure, execution-policy, and runtime behavior work
- established_invariants: local configuration remains owned by its current package/provider
- unresolved_semantics: common ownership boundary, typed values, source precedence, construction lifecycle, governance configuration versus occurrence applicability, and operational telemetry separation
- risk_if_deferred: consumers may duplicate incompatible configuration semantics
- risk_if_implemented_early: global configuration object, untyped bag, loader, environment framework, dependency injection container, or service locator
- promotion_trigger: multiple framework consumers require the same configuration semantic with conflicting local ownership
- validation_level: NONE
- live_validation_trigger: unknown until shared configuration affects a meaningful harness path
- first_harness_consumer: unknown
- second_harness_trigger: a second consumer requires unchanged configuration semantics
- related: B-0003, B-0008, B-0012, B-0029, B-0030
