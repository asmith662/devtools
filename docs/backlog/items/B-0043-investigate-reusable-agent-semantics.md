# B-0043 — Investigate reusable Agent semantics

- type: INVESTIGATION
- status: DEFERRED
- decision_maturity: DISCOVERED
- necessity: FUTURE_REQUIRED
- architectural_significance: STRUCTURAL
- urgency: DEFERRED
- evidence_basis: MULTIPLE
- scope: reusable goal-directed Agent behavior beyond current integrations and experiments
- primary_domain: agents
- supporting_domains: models, context, tools, execution, governance
- split_from: B-0029

## Problem / value

Determine what reusable Agent behavior is justified beyond the external Codex
integration and bounded Qwen experiments. A Model is not an Agent, and no
BaseAgent API is authorized merely because the domain exists.

- hard_dependencies: none
- pressure_dependencies: B-0008, B-0036, B-0031
- operational_dependencies: stable bounded Agent consumer
- promotion_trigger: shared Agent semantics are stable beyond local composition
- validation_level: NONE

## Recorded follow-up direction after source grounding

The bounded source-grounding recovery assignment records these future decisions;
it does not implement them or promote a generic Agent API. Complete or explicitly
stop the current scientific experiment before starting an autonomous-agent slice.

- ExperimentController remains deterministic frozen-plan execution.
- ExperimentManagerAgent is the first later autonomous vertical slice: diagnosis,
  proposal, stopping and escalation. It does not grant execution authority.
- ResearchAgent follows, composing external research and evidence synthesis around
  bounded experiment management. No inheritance hierarchy is selected.

Execution profiles remain distinct: SEMANTIC_WORKER receives frozen host disclosure
without tools/network/user rules; CODING_WORKER has an explicit repository workspace
and curated execution policy; REVIEW_WORKER is primarily read-only with bounded
validation and no default commit/push. Do not copy the historical personal allowlist.

Future `closeout_feature` begins as one deterministic repository-owned capability:
authenticate declared scope; apply scoped format/safe fixes; run statics, targeted
tests and required protected/full gates; verify diff/docs/handoff; emit a tree-bound
validation receipt. Commit requires supplied publication authority; push requires
an exact remote/ref grant. It is not a workflow DSL or automatic authority grant.

The future usage benchmark crosses runtime-supported model and reasoning effort,
SEMANTIC_NO_TOOLS/CODING_AGENT/REVIEW_AGENT, MINIMAL/SHORT/MEDIUM/LONG tasks, and
explicit repetitions. Measure tokens, uncached input, reasoning and wall time per
accepted task, acceptance, retry/failure burden and matched-workload Codex tokens
avoided by local workers. Preserve unavailable fields; do not equate API prices,
subscription units and raw token counts. Pilot cheaply before an expensive matrix.
No matrix, Qwen agent, Worker/ModelBackend/AgentBackend hierarchy, distributed ledger
or general AgentRuntime is authorized by this record alone.
