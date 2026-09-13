# B-0035 — Investigate Tool-facing capability exposure

- type: INVESTIGATION
- status: DEFERRED
- decision_maturity: DISCOVERED
- necessity: FUTURE_REQUIRED
- architectural_significance: STRUCTURAL
- urgency: DEFERRED
- evidence_basis: MULTIPLE
- scope: exposing reusable Tool semantics at a model or Agent boundary
- primary_domain: tools
- supporting_domains: models, agents, context
- split_from: B-0020

## Problem / value

Determine how a Tool's bounded contract may be described and projected for a
model or Agent without making Tools own model protocol, Action parsing,
authorization, or result reconstruction. Resources remain lower-level than
Tools.

The Qwen probes demonstrate local descriptions, bounded projections, and
action-specific materialization only. They do not establish a reusable schema
or registry.

- hard_dependencies: none
- pressure_dependencies: B-0008
- operational_dependencies: stable model-facing Tool consumer
- promotion_trigger: exposure semantics are stable independently of local experiment code
- validation_level: NONE
