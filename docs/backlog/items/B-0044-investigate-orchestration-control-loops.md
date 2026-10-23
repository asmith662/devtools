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

## Recovered-input / pinned mechanism evidence (2026-10-23)

Original candidates06/12 and [Qwen continuation research](../../research/agent-harness-mechanism-review.md#qwen-code-exploration-compaction-and-source-residency)
show soft exploration reminders, separate repetition/cap guards and retry-aware
bookkeeping, versus the native app's frozen hard ceilings. Pydantic has explicit
end strategies/sequential barriers; this is not the narrow Runtime contract.
Selected tests establish intended policies, not efficacy on Devtools tasks.
No new phase controller, graph runtime or automatic retry is selected. Current
application orchestration and WorkCycle authority remain separate.

## DeepSeek Harness / Aider evidence (2026-10-23)

DeepSeek's default AgentLoop is distinct from its Agent interface and scoped
services; it owns turn/step admission, bounded Tool scheduling and teardown.
Aider's reflection, host edit mechanics and optional architect/editor composition
are application policies with different authority. Neither justifies broadening
Devtools narrow Runtime. Audit actual native-worker and WorkCycle trajectories
before shared hooks or future maintenance-agent lifecycle abstractions; no
generic phase controller, DI container or runtime adoption is authorized.

See the [pinned source-and-test comparison](../../research/agent-harness-mechanism-review.md#deepseek-harness-and-aider-source-and-test-audit-2026-10-23)
and [five-flow audit plan](../../research/development-lifecycle-audit-plan.md).
Status, dependencies, decision maturity and promotion trigger remain unchanged.
