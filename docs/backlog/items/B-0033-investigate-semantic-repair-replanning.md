# B-0033 — Investigate semantic repair and replanning

- type: INVESTIGATION
- status: DEFERRED
- decision_maturity: DISCOVERED
- necessity: FUTURE_REQUIRED
- architectural_significance: STRUCTURAL
- urgency: DEFERRED
- evidence_basis: RESEARCH
- scope: goal-directed repair and changed strategy after known outcome
- primary_domain: agents
- supporting_domains: orchestration, evaluation
- split_from: B-0014

## Problem / value

Determine when an Agent changes strategy, decomposes new work, or repairs a
known failed result. This is not transport retry and does not authorize an
Agent framework or orchestration engine.

- hard_dependencies: none
- pressure_dependencies: B-0043, B-0044
- operational_dependencies: bounded Agent consumer with known failed work
- promotion_trigger: one consumer needs explicit repair distinct from retry
- validation_level: NONE
