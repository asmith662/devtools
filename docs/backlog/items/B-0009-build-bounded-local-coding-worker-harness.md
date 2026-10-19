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

### Current real-task integration checkpoint

The [concrete coding worker](../../../experiments/qwen/docs/overview.md#retrieved-context-markdown-coding-worker)
now consumes multi-resolution Context, isolated native proposals and focused
test-feedback repair, capped at three calls. Scripted responses validate initial
acceptance, a corrected second edit, refusal, exhaustion and cleanup against the
unchanged eight-scenario oracle. The first real Markdown run is now accepted:
two Qwen calls, one repair, 8,178 input / 525 output tokens, 34.76 seconds.
The exact captured edit is integrated with eight permanent regressions and
[verified provenance](../../../experiments/qwen/docs/first_accepted_coding_task.json).
No new inference occurred during closeout. General reliability and reusable
Agent promotion remain unestablished; the next checkpoint is a different real task.
The existing loop now accepts host-owned one-file task configuration through
`run_coding_task(..., task=...)` and CLI `--task`. Original Markdown compatibility
and second-task Context/validation/repair/refusal are deterministically tested.
The [second task preparation](../../../experiments/qwen/docs/second_task_preparation.json)
freezes an existing Python source-materialization defect, independent checks and
all bounds. The live [second-task result](../../../experiments/qwen/docs/second_task_result.json)
remains REPAIR_BUDGET_EXHAUSTED: three calls, two repairs, 19,587 input / 1,848
output tokens, 105.74 seconds. Codex corrected the production materializer and
added primary-exception feedback capture after this failure. Neither correction
constitutes Qwen task acceptance or reusable Agent-framework promotion.
Task-local native structured continuation and five read-only Context operations
are now connected to that same coding loop on `feat/qwen-context-worker`.
Scripted search/read/edit/failure/repair passes the unchanged oracle and genuine
local native search/read completed (3 requests, 4 reads, 12,152 input / 645 output
tokens, 40.037 seconds). No new coding authority exists at the canonical checkout,
so this is not another accepted Qwen task or demonstrated coding improvement.
See the [maintained contract and evaluation](../../../apps/qwen/README.md).
General continuation, atomic task-local state, long-term memory and 32K/64K
benchmarking remain planned.

The existing WorkCycle now provides a [separately governed integration lifecycle](../integration.md)
for accepted candidates: destination-based installation, validation, exact-tree
supervisory review, feature publication, authorized target promotion, verification
and canonical backlog progress. Coding authority still grants no integration
permission. B-0048 remains an accepted object-only candidate pending a genuine
integration grant; sibling compatibility obligations remain open. No new Qwen
run or protected merge is part of this engineering increment.

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

A second deterministic repository-selection stress fixture now retains the
same small one-line label-matching change while adding plausible source, test,
and documentation alternatives. It uses seven bounded list/read actions and
records fixture-local required, plausible-unnecessary, and clearly-irrelevant
file-read facts alongside ModelUsage, projections, and duration. It is the
first measured selection-stress reference; no successful live result exists
for it yet, and scripted success does not establish Context pressure.

- hard_dependencies: B-0008
- pressure_dependencies: B-0012, B-0016, B-0035, B-0036, B-0043, B-0044
- operational_dependencies: pinned Qwen serving profile
- blocked_by: none
- promotion_trigger: deterministic worker composition plus live task evidence
- validation_level: LIVE_SINGLE_HARNESS


## Canonical consolidation checkpoint

The standalone worker is at `apps/qwen`. The first accepted Markdown correction
is adopted; Task 02 remains failed with a separate Codex repair. Single-checkout
WorkCycle/integration is implemented on `feat/qwen-context-worker`; main adoption
and dashboard dependency review remain separate. No model task ran during cleanup.
The later native Context increment adds measured read-only conformance, not a new
coding result. General reliability, durable continuation and Memory remain open.
