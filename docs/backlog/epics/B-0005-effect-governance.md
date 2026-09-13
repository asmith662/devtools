# B-0005 — Effect Governance

- type: EPIC
- status: DEFERRED
- decision_maturity: DISCOVERED
- necessity: FUTURE_REQUIRED
- architectural_significance: FOUNDATIONAL
- urgency: DEFERRED
- evidence_basis: MULTIPLE
- scope: authority for externally meaningful operations
- primary_domain: governance
- supporting_domains: execution, tools, agents, orchestration, observability, persistence

## Problem / value

Preserve pressure for authority, policy, approval, delegation, and safe
handling of externally meaningful effects. Model proposal, capability exposure,
and Tool validation do not create authorization.

Read-only Qwen experiments do not prove mutation governance. Bounded local
effects remain explicit until a reusable mutating boundary needs governance.

- hard_dependencies: none
- pressure_dependencies: B-0031
- operational_dependencies: mutating harness capability
- children: B-0012, B-0013, B-0034, B-0037, B-0039
- promotion_trigger: a mutation crosses a reusable boundary
- validation_level: NONE
