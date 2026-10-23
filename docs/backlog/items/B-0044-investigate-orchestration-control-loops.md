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
