# B-0044 — Investigate orchestration control loops

- type: INVESTIGATION
- status: DEFERRED
- decision_maturity: DISCOVERED
- necessity: FUTURE_REQUIRED
- architectural_significance: STRUCTURAL
- urgency: DEFERRED
- evidence_basis: MULTIPLE
- scope: coordination across Runs, Agents, branches, and workflows
- primary_domain: orchestration
- supporting_domains: agents, execution, context, tools, governance
- split_from: B-0029

## Problem / value

Determine when local control loops require reusable orchestration. Qwen
read-only loops demonstrate bounded experiment-local sequencing only; they do
not establish graphs, supervisors, schedulers, or a workflow runtime.

- hard_dependencies: none
- pressure_dependencies: B-0043, B-0031
- operational_dependencies: multiple consumers sharing loop semantics
- promotion_trigger: coordination boundary is stable independent of one experiment
- validation_level: NONE
