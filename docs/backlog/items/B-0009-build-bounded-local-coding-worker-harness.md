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

## First real task evidence (2026-10-17)

The [frozen Markdown task report](../../../experiments/qwen/docs/first_real_task.json)
distinguishes validated host composition from **unaccepted real-task competence**.
The existing acceptance entrypoint now composes native ModelToolDefinition/Call,
ToolInvocation/ToolRunner and repository read Tools with caller-selected RI/Context
disclosure and managed one-file Git patch admission. Historical fixtures and their
exact patch grammar remain intact. No universal worker/Agent API is added.

One local Qwen attempt ran for 32.26 s: five turns, nine proposed native reads,
seven accepted reads, 37,644 input and 403 output tokens. Native normalization and
host execution work, unlike the retained text-only list_files failure. Repeated
source/test acquisition produced no patch; the final batch exceeded the action
cap. Source is unchanged and the independent frozen oracle still fails. No second
attempt or substituted Codex solution occurred. The primary task failure is
reasoning/continuation progress; single-Prompt textual feedback remains a confound.

Harness status stays VALIDATED, but **a real accepted Qwen development change has
not been demonstrated**. Focused tests and protected validation pass, with 100%
production branch coverage. The smallest next decision is to inspect the retained
trace before separately authorizing a changed continuation/prompt attempt. This
evidence authorizes no generic framework or automatic retry.
