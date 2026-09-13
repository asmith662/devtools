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

- hard_dependencies: none
- pressure_dependencies: B-0008, B-0013, B-0023, B-0024
- operational_dependencies: sensitive diagnostic or evidence payload
- promotion_trigger: real harness must retain or export data whose disclosure matters
- validation_level: NONE
