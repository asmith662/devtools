# B-0009 — Build the first bounded local coding-worker harness

- type: STORY
- status: ACTIVE
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

This is deterministic framework-composition evidence, not evidence that Qwen
can independently perform the worker task. The live single-harness validation
remains the outstanding completion criterion.

The first live attempt safely failed before mutation when Qwen submitted an
ungrounded patch without using a repository Tool. The experiment now retains
that raw response and requires fixture-specific evidence acquisition: accepted
reads of the relevant implementation and focused test before a final patch is
admissible. One controller-authored correction requests inspection without
revealing repository locations; a repeated ungrounded final response fails.
This is local worker-contract evidence, not a reusable Context, Agent, Action,
or governance promotion. A second live attempt remains pending.

- hard_dependencies: B-0008
- pressure_dependencies: B-0012, B-0016, B-0035, B-0036, B-0043, B-0044
- operational_dependencies: pinned Qwen serving profile
- blocked_by: none; bounded live Qwen coding-worker acceptance remains pending
- promotion_trigger: deterministic worker composition plus live task evidence
- validation_level: LIVE_SINGLE_HARNESS
