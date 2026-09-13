# B-0012 — Investigate governed effect semantics

- type: INVESTIGATION
- status: DEFERRED
- decision_maturity: DISCOVERED
- necessity: FUTURE_REQUIRED
- architectural_significance: FOUNDATIONAL
- urgency: DEFERRED
- evidence_basis: MULTIPLE
- scope: governance boundary for externally meaningful operations
- primary_domain: governance
- supporting_domains: tools, agents, execution, observability
- parent: B-0005

## Problem / value

Determine authority and outcome boundaries for reusable externally meaningful
operations. Model proposal, model-visible capability, Tool validation, and
Tool eligibility are not authorization. A generic Action type is not required
to investigate governance semantics.

- hard_dependencies: none
- pressure_dependencies: B-0035
- operational_dependencies: real mutating harness capability
- promotion_trigger: mutation crosses a reusable boundary
- validation_level: NONE
