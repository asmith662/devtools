# B-0045 — Establish minimal ModelInteraction core

- type: STORY
- status: IMPLEMENTED
- decision_maturity: READY_FOR_IMPLEMENTATION
- necessity: REQUIRED
- architectural_significance: STRUCTURAL
- urgency: NOW
- evidence_basis: REPOSITORY
- scope: established minimal provider-neutral model invocation boundary
- primary_domain: models
- supporting_domains: agents, execution
- split_from: B-0030

## Resolved scope

The implemented model interaction core consists of `Prompt`,
`ModelInteraction`, `ModelResponse`, `ConversationRef`, `InteractionSource`,
and configurable `LlamaCppInteraction`. It separates model invocation from
ModelServing and from the external Codex Agent integration.

Provider wire translation and provider-local failures remain at the adapter
boundary. This record does not claim streaming, structured action payloads,
usage, routing, or multiple providers.

- related: B-0030, B-0046
- validation_level: INTEGRATION
