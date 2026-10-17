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
cap. Source is unchanged and the independent frozen oracle still fails. No Codex
solution was substituted. The trace showed complete prior file contents in later
prompts, but no structured multi-message continuation or explicit already-read
instruction; the model repeated calls anyway.

A later, distinct complete-context condition supplied the full source and tests in
one initial Context disclosure with zero Tools and one request. It used the same
source/test/oracle hashes; the baseline oracle failed before inference. The pinned
model returned `output_limit` at 1,500 output tokens after 69.26 seconds, with no
unified diff. Patch application and post-patch validation were not reached. Source
remains unchanged. This condition changed Context availability, Tool access and
request count, so it does not isolate continuation alone. The [separate measured
report](../../../experiments/qwen/docs/first_real_task_upfront.json) records the
prompt identity, usage and validation disposition.

A separately authorized output-budget comparison reused attempt-02's exact
prompt bytes, source/test/oracle hashes, model profile, Context configuration,
disabled thinking, one request and zero Tools, changing only the output cap from
1,500 to 4,096 tokens. Qwen stopped normally after 6.65 s with 3,801 input and
139 output tokens, but its response failed the existing exact unified-diff
admission contract. No patch was applied and neither the focused Markdown tests
nor the independent oracle ran after inference. The source remains at its
frozen hash. See the [attempt-03 report](../../../experiments/qwen/docs/first_real_task_output_budget_comparison.json).

Harness status stays VALIDATED, but **a real accepted Qwen development change has
not been demonstrated**. The attempts fail at distinct boundaries: repeated
acquisition in attempt-01, output truncation in attempt-02, and patch-format
admission in attempt-03. Focused deterministic tests, Ruff, formatting and strict
mypy pass for the host harness. No automatic retry or generic framework is
authorized by this evidence.

The attempt-03 response was patch-like but malformed at the file-header boundary
(`---`, `---`, bare `a/<path>` and `b/<path>` lines, then `---`/`+++`); the
existing parser correctly refused it. The response ended inside a source
fragment, so this was not a valid patch incorrectly rejected. The next bounded
condition uses one native `propose_edit(path, old_text, new_text)` proposal and
the host-generated diff/application/oracle path. Its deterministic checks have
passed: exact path and unique nonempty source-region checks, bounded replacement,
duplicate/multiple-call refusal, host-generated diff application, and scripted
oracle-rejection/restoration. The complete-context freeze and one-operation request
are experiment-local; no executable filesystem Tool is exposed. The request will
be frozen against the committed harness before any inference. After that freeze,
the live condition still requires explicit terminal opt-in. No Qwen request has
yet been sent for this condition.
