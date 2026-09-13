# B-0003 — Local Coding Worker Harness

- type: EPIC
- status: BLOCKED
- decision_maturity: SEMANTICS_PARTIAL
- necessity: REQUIRED
- architectural_significance: HARNESS_LOCAL
- urgency: SOON
- evidence_basis: REAL_USE
- scope: first bounded local coding-worker experiment
- primary_domain: experiments
- supporting_domains: agents, context, tools, models, execution, evaluation

## Problem / value

Eventually exercise a bounded Qwen coding worker that can use selected Context,
request bounded Tool work, make explicitly governed effects where required,
validate outcomes, and produce review evidence. It is experimental composition,
not a generic Agent or orchestration implementation.

Existing Qwen read-only probes provide predecessor evidence for model turns,
read-only Tool use, local Action parsing, bounded projections, and durable
acceptance reporting. They are not a coding/editing worker.

- hard_dependencies: B-0008
- pressure_dependencies: B-0012, B-0016, B-0035, B-0036, B-0043, B-0044
- operational_dependencies: pinned Qwen serving profile
- children: B-0009
- blocked_by: minimum coding-context boundary for the selected story
- promotion_trigger: B-0008 resolves required selected repository information
- validation_level: LIVE_SINGLE_HARNESS
