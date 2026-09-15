# B-0027 — Investigate serialization and representation boundaries

- type: INVESTIGATION
- status: DEFERRED
- decision_maturity: DISCOVERED
- necessity: FUTURE_REQUIRED
- architectural_significance: STRUCTURAL
- urgency: DEFERRED
- evidence_basis: MULTIPLE
- scope: translation among runtime, provider wire, and durable representations
- primary_domain: persistence
- supporting_domains: models, agents, observability

## Problem / value

Current evidence distinguishes ConversationMessage, Prompt, ModelResponse,
provider wire forms, Conversation persistence forms, and Evidence forms. A
runtime value is not automatically a provider wire or durable schema.

Investigate only when a semantic value must reliably cross distinct boundaries;
do not introduce a universal serializer or schema framework.

[ADR-0001](../../architecture/decisions/ADR-0001-cohesive-model-interaction-boundary.md)
establishes the ModelInteraction application of this distinction: semantic
request/response values, typed provider exchange, and capture-controlled
Evidence are separate representations. It does not authorize a universal
serializer, durable schema, or raw-payload persistence.

- hard_dependencies: none
- pressure_dependencies: none
- operational_dependencies: boundary needing stable compatible representation
- promotion_trigger: one semantic value must reliably cross two representation boundaries
- validation_level: NONE
