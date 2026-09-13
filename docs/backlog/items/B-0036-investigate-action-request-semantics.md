# B-0036 — Investigate Action request semantics

- type: INVESTIGATION
- status: DEFERRED
- decision_maturity: DISCOVERED
- necessity: FUTURE_REQUIRED
- architectural_significance: STRUCTURAL
- urgency: DEFERRED
- evidence_basis: MULTIPLE
- scope: interpreted model- or Agent-originated requests for capabilities
- primary_domain: agents
- supporting_domains: tools, models, governance, experiments
- split_from: B-0020

## Problem / value

Determine whether reusable Action request semantics are needed beyond local
Qwen proposal parsing and materialization. An Action is requested work, not a
Tool, capability inventory, or authority.

Promotion requires sufficient evidence that the boundary is stable independent
of experiment-local control flow. An independent consumer is strong evidence,
not a universal numerical rule.

- hard_dependencies: none
- pressure_dependencies: B-0035, B-0012
- operational_dependencies: another stable Action-like consumer
- promotion_trigger: shared semantics cannot remain cleanly local
- validation_level: NONE
