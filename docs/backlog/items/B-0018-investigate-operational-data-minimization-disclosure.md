# B-0018 — Investigate operational-data minimization and disclosure

- type: INVESTIGATION
- status: DEFERRED
- decision_maturity: DISCOVERED
- necessity: FUTURE_REQUIRED
- architectural_significance: STRUCTURAL
- urgency: DEFERRED
- evidence_basis: MULTIPLE
- scope: collection, disclosure, retention, and export of operational payloads
- primary_domain: governance
- supporting_domains: observability, context, persistence, models, tools

## Problem / value

Determine minimization and disclosure boundaries for repository data, prompts,
model responses, Tool inputs/results, paths, exceptions, governance facts, and
durable records. Prefer minimizing collection before downstream redaction.

An occurrence may be reportable without authority to disclose its payload.
Current terminal Evidence minimizes payload but does not resolve this pressure.

[ADR-0001](../../architecture/decisions/ADR-0001-cohesive-model-interaction-boundary.md)
establishes the ModelInteraction capture rule: capture policy and a manifest
must distinguish unavailable, omitted, and redacted provider facts, while
credentials and equivalent sensitive transport state are never generically
captured. Retention, export, and broader disclosure policy remain deferred.

- hard_dependencies: none
- pressure_dependencies: B-0008, B-0013, B-0023, B-0024
- operational_dependencies: sensitive diagnostic or evidence payload
- promotion_trigger: real harness must retain or export data whose disclosure matters
- validation_level: NONE

## DeepSeek Harness / Aider evidence (2026-10-23)

DeepSeek's generic telemetry redaction is pass-through without mounted rules;
the inspected OTel provider instead gates capture to canonical explicit feedback
prefixes and can disable transport. These are separate privacy/delivery controls,
not complete content sanitization. Devtools model Evidence has existing category
capture/omission manifests. The local flow audit must inspect actual capture,
lost-record and egress boundaries before any exporter or shared trace consumer.
No upstream privacy efficacy or full plugin supply-chain claim was measured.

See the [pinned source-and-test comparison](../../research/agent-harness-mechanism-review.md#deepseek-harness-and-aider-source-and-test-audit-2026-10-23)
and [five-flow audit plan](../../research/development-lifecycle-audit-plan.md).
Status, dependencies, decision maturity and promotion trigger remain unchanged.
