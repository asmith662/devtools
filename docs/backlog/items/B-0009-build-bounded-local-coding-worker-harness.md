# B-0009 — Build the first bounded local coding-worker harness

- type: STORY
- status: VALIDATED
- decision_maturity: READY_FOR_IMPLEMENTATION
- necessity: REQUIRED
- architectural_significance: HARNESS_LOCAL
- urgency: SOON
- evidence_basis: REAL_USE
- scope: experimental Qwen coding-worker vertical slice
- primary_domain: experiments
- supporting_domains: agents, context, tools, models, execution, evaluation
- parent: B-0003

## Problem / value

Build one bounded experimental coding worker after B-0008 establishes the
minimum repository fact-acquisition boundary. It may exercise
ModelInteraction, experiment-local relevance choice, bounded Tool use,
execution, and task-specific acceptance without promoting a generic Context,
Agent, Action, authorization, or orchestration framework.

The deterministic fixture now proves a bounded patch-proposal worker can start
without source or test paths, acquire both through existing bounded list/read
Tools, return one permitted diff, and have host-side experimental code apply
and validate it only inside a disposable fixture. It uses no model-directed
mutation, reusable Context, Agent, Action, authorization, orchestration, or
evaluation implementation.

The final bounded live single-harness acceptance succeeded: Qwen inspected the
fixture, read both required artifacts, returned the permitted semantic patch,
and the host applied it only inside the disposable fixture before behavioral
validation passed. The durable live report remains temporary evidence rather
than reusable framework state.

Earlier live attempts safely exposed and corrected fixture-local grounding and
EOF-diff-admission issues before the final success. The worker retains raw
responses separately from the canonical patch it applies. It now also records
optional provider-reported ModelUsage per turn and complete cumulative reported
totals in the acceptance artifact when every turn supplies a count. This is
measurement evidence only, not a reusable Context, Agent, Action, governance,
or orchestration promotion.

- hard_dependencies: B-0008
- pressure_dependencies: B-0012, B-0016, B-0035, B-0036, B-0043, B-0044
- operational_dependencies: pinned Qwen serving profile
- blocked_by: none
- promotion_trigger: deterministic worker composition plus live task evidence
- validation_level: LIVE_SINGLE_HARNESS
