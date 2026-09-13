# B-0009 — Build the first bounded local coding-worker harness

- type: STORY
- status: BLOCKED
- decision_maturity: SEMANTICS_PARTIAL
- necessity: REQUIRED
- architectural_significance: HARNESS_LOCAL
- urgency: SOON
- evidence_basis: REAL_USE
- scope: experimental Qwen coding-worker vertical slice
- primary_domain: experiments
- supporting_domains: agents, context, tools, models, execution, evaluation
- parent: B-0003

## Problem / value

Build one bounded experimental coding worker after B-0008 defines the required
Context. It may exercise ModelInteraction, selected Context, bounded Tool use,
execution, and task-specific acceptance without promoting a generic Agent,
Action, authorization, or orchestration framework.

Qwen read-only experiments are predecessor evidence only; no coding/editing
worker exists.

- hard_dependencies: B-0008
- pressure_dependencies: B-0012, B-0016, B-0035, B-0036, B-0043, B-0044
- operational_dependencies: pinned Qwen serving profile
- blocked_by: minimum Context requirements for the selected story
- promotion_trigger: bounded coding context is designed
- validation_level: LIVE_SINGLE_HARNESS
