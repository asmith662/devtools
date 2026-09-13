# B-0046 — Investigate advanced model-interaction/provider pressure

- type: INVESTIGATION
- status: DEFERRED
- decision_maturity: DISCOVERED
- necessity: FUTURE_REQUIRED
- architectural_significance: STRUCTURAL
- urgency: DEFERRED
- evidence_basis: MULTIPLE
- scope: advanced model interaction and provider adaptation beyond established core
- primary_domain: models
- supporting_domains: agents, tools, execution, evaluation
- split_from: B-0030

## Problem / value

Preserve pressure for streaming, richer structured responses, model-native
action payloads, reasoning or usage metadata, provider capability discovery,
additional provider adapters, and later routing/model selection only when a
consumer needs them. Codex is an external Agent, not a model-provider consumer.

- hard_dependencies: B-0045
- pressure_dependencies: B-0035, B-0036, B-0027
- operational_dependencies: model/provider path needing unavailable semantics
- promotion_trigger: a stable consumer needs meaning not expressible by current ModelInteraction
- validation_level: NONE
