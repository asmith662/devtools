# B-0013 — Investigate authority, grants, authorization, and approval

- type: INVESTIGATION
- status: DEFERRED
- decision_maturity: DISCOVERED
- necessity: FUTURE_REQUIRED
- architectural_significance: FOUNDATIONAL
- urgency: DEFERRED
- evidence_basis: RESEARCH
- scope: authority possession, policy, authorization, and approval conditions
- primary_domain: governance
- supporting_domains: observability, persistence, orchestration
- parent: B-0005

## Problem / value

Determine principals, grants, restrictions, authorization, approval conditions,
delegation, revocation, and freshness only when a governed mutation needs them.
Approval is not authority; historical authorization evidence is not current
authority.

- hard_dependencies: B-0012
- pressure_dependencies: B-0024
- operational_dependencies: discoverable but forbidden governed capability
- promotion_trigger: real harness needs capability exposure plus execution denial
- validation_level: NONE
