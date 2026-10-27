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

## Executed five-flow lifecycle evidence (2026-10-23)

Codex27 closeout records source.py and representation.py physical CRLF SHA-256 values; committed blobs have different SHA-256 values that reproduce those hashes exactly after LF-to-CRLF conversion. Other selected files match exactly. Document/test stored versus physical identity rather than silently equating them, normalizing model edits or rewriting historical receipts. Distinct JSON serializers/seals/views have different contracts; repeated syntax alone is not duplication.

See the [source/evidence audit and priority crosswalk](../../research/development-lifecycle-observability-audit.md)
and its [authenticated metadata](../../research/development-lifecycle-observability-evidence-20261023.json).
Status, dependencies, decision maturity and promotion trigger remain unchanged.

## Persistence/Recovery audit evidence

Literal JSON v1 compatibility is independently verified; JSON is conversion only and has strict field/type policy. SQLite text affinity is not semantic string validation: four BLOB columns and a Runtime continuation consumer reproduce a separately captured P2. Durable names remain compatible; no universal serializer or global model validation rewrite. [Full review and independent evidence](../../research/persistence-and-recovery-audit.md). Existing status, decision maturity, dependencies and authority unchanged. `audit:persistence-recovery:206d58e2:20261026`.
