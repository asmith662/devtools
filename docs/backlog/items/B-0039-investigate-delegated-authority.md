# B-0039 — Investigate delegated authority

- type: INVESTIGATION
- status: DEFERRED
- decision_maturity: DISCOVERED
- necessity: FUTURE_REQUIRED
- architectural_significance: STRUCTURAL
- urgency: DEFERRED
- evidence_basis: RESEARCH
- scope: authority delegated to an actor under constraints
- primary_domain: governance
- supporting_domains: agents, observability, persistence
- split_from: B-0022

## Problem / value

Determine authority provenance, attenuation, scope, revocation, freshness, and
accountability for delegated authority. Agent identity is not authorization
identity, and delegation cannot manufacture authority.

- hard_dependencies: B-0013
- pressure_dependencies: B-0024
- operational_dependencies: real multi-actor governed operation
- promotion_trigger: a worker acts under another actor's constrained authority
- validation_level: NONE
