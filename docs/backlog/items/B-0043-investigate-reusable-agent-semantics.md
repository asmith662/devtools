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

## Recovered-input / pinned mechanism evidence (2026-10-23)

Original candidate16 proposes future report-only maintenance specializations.
The [exact crosswalk](../../research/reconciliation-input-reconciliation.md#original-candidate-crosswalk)
relates these to the already recorded ResearchAgent/ExperimentManager direction.
Detection contracts, false-positive control, permissions, actual consumers and
reproducible evidence remain unqualified. Do not create a BaseAgent, self-modifying
maintenance service or new hierarchy from role labels. This is research pressure,
not a distinct verified defect or implementation authorization.

## Agents/Conversation/Runtime audit — 2026-10-26

CodexAgent is external-agent adaptation, not ModelInteraction; no maintained native caller found beyond tests, while parser/usage helpers have retained experimental/usage consumers. New pending P2 literal-prompt transport owner in report. Runtime sends current message/continuation rather than full history; native Qwen owns its separate bounded Tool loop. No BaseAgent/Run/registry promotion follows. [Exact source/probe/consumer evidence](../../research/agents-conversation-and-runtime-audit.md). No status, maturity, approval, dependency or parent closure changes. `audit:agents-conversation-runtime:87f5b9d2:20261026`.

## Codex contract repair evidence

Codex literal input P2 delivered for fresh/resumed stdin transport. No extra invocation or retry. This does not provide a native autonomous Codex loop, change Runtime, or close broader Agent semantics. [Delivered correction](../../development/codex-input-and-metadata-repair.md), normal PR35 and verified main `4189fffd79eaaa64debfc7b601bb729de92002de`. No state, approval, grant or parent closure. `repair:codex-input-metadata:c39c1f0f:20261026`.

## Framework/application direction design — 2026-10-27

The maintainer has reaffirmed reusable model-independent engineering infrastructure as the priority; Qwen is one consumer. A bounded portable coding Agent is a concrete target after reuse of existing model, Tool, Context and check substrates. Runtime is a usable Conversation collaborator, not the owner of all goal-directed code. The proposed first native Tool-composition seam and later agents.coding boundary need explicit contract approval. This design does not introduce BaseAgent, generic Run/Step/Attempt or a workflow engine, and does not approve an autonomous experiment. [Decision package](../../development/framework-application-direction.md). Status, maturity, dependencies, original approvals and promotion triggers remain unchanged. `design:framework-application-direction:e84b724c:20261027`.

## Delivered framework migration 1 - 2026-10-27

The current explicit maintainer assignment authorized only the native model/Tool composition increment. Production `31627dcae17fa1e429fbc4c1f3d31941ef5803a7`, PR #48, accepted main `6a331e65ebb5f5c467a32eb694ca7a95056865a1` delivers a real Agents-owned operation used by both Qwen dispatchers and a non-Qwen host denied application imports and file reads. Existing ToolRunner, native model values, source/check Resources and host authority remain owners. [Contract, independent effects, validation and limits](../../development/native-model-tool-composition.md). Later source/check/coding-Agent migrations remain proposals requiring approval; this is not a whole-Agent promotion, parent closure or automatic status/maturity change. Original design/audit evidence and prior overlays retain their dates/blobs. `integration:native-model-tools:31627dca:20261027`.

## Delivered framework migration 2 - 2026-10-27

The current explicit maintainer assignment authorized only scoped source and fixed validation promotion. Production `59ae70b07f7e2332db887bc61748fe5fd3373fae`, PR #50, accepted main `9078406b76635a81fdaf6e5b45fda2c8db6a3f4f` delivers neutral Tools over existing RI/Context/Commands, actual Qwen source/check adoption, public legacy task-policy closeout adaptation and guarded non-Qwen native execution. [Contract, effects, validation and limits](../../development/framework-source-checks.md). Legacy task/oracle/journal/edit/custody/terminal/governance remain local and unchanged. Broader coding-Agent migration requires explicit neutral task/edit/outcome/custody approval; no status/maturity change, parent closure, A+C, Option B, restart or new execution authority. Original design/audit evidence and prior overlays retain their dates/blobs. `integration:framework-source-checks:59ae70b0:20261027`.

## Delivered framework migration 3 - 2026-10-27

Explicit maintainer authorization delivered production `22c44a88fa20da8d580b1470441030c80835b7d0`, normal PR #52, independently verified source main `a23c081cefb7524471a26a8f539356fa2545a38e`: one Agents-owned bounded coding process, promoted exact edit/known-source custody mechanics, actual prepared/native Qwen delegation and guarded non-Qwen source/edit/check/repair completion. [Contract, effects, validation and limits](../../development/bounded-coding-agent-delivery.md). Existing model/Tool/source/check foundations are reused. Legacy task/hash/journal/readiness/oracle/capacity/authority remain app policy. Broader B-0035/B-0043/39c responsibilities stay open, without status/maturity changes, grants, approvals or parent closures. Runtime, Option B,A+C,restart,Evidence and migration4 remain separate. Original frozen versions/findings and prior overlays retain their identities. `integration:bounded-coding-agent:22c44a88:20261027`.


## Real local-model coding dogfood — 2026-10-28

One explicitly authorized fresh real Qwen3.8 IQ4_XS task completed through the shared coding process with three exact reads, one edit and successful frozen focused/held-out grading. Experimental checkpoint `bfd9aa35a0e0b181a12c203ed022d8bf6203b3bd` is accepted on main; [source/effect/usage evidence, setup diagnosis and limits](../../research/local-coding-agent-dogfood.md). The command procedure was host-triggered, not model-selected; no live repair or autonomous discovery was demonstrated. No production fix, new provider/loop/store, status/maturity/dependency change, approval, grant or parent closure. A+C, Option B, recovery and 188 historical RI obligations remain separate. `experiment:local-coding-dogfood:bfd9aa35:20261028`.

## Local coding discovery Case 0002 — 2026-10-28

One frozen real-model case selected a shared owner from 18 resources/11 permitted runtime modules, used canonical retrieval, read 8 resources and passed 7 focused plus 10 held-out tests after one edit. [Exact discovery/Context trace, scopes and limits](../../research/local-coding-agent-case-0002.md). Search and the initial owner read were requested together; no causal internal-reasoning or live-repair claim. No production defect, new API/loop/provider/store, status/maturity/dependency/approval/grant change or parent closure. Case 0001, A+C, Option B, recovery and 188 historical RI obligations remain separate. Single next recommendation is bounded full inventory in initial Context to save a listing-only request, requiring separate approval. `experiment:local-coding-case0002:9ad37cff:20261028`.


## Real framework maintenance Case 0003 — 2026-10-28

One explicitly authorized real Qwen3.8 maintenance attempt pursued the existing bounded first-request inventory follow-up. Five real requests located the neutral coding host; complete-input preparation then refused 36,640 bytes against the unchanged 32,768-byte cap. No edit proposal, validation/repair turn or production candidate occurred; canonical source was restored and no Codex patch or second attempt substituted. [Frozen evidence, independent verdict and exact limits](../../research/local-coding-maintenance-case-0003.md). This records Context-capacity/usability pressure, not a budget-guard defect or delivered implementation. B-0035 remains open; budget-aware active Context projection is the single next recommendation requiring separate authorization. Both prior cases, historical evidence, 188 RI obligations, A+C, Option B and recovery remain separate. No status/maturity/dependency, approval, grant or parent-closure change. `experiment:real-maintenance-case0003:e85de1a1:20261028`.


## Context-compaction research reconciliation — 2026-10-28

The [hybrid Context decision package](../../research/agent-context-compaction.md)
distinguishes retained execution facts, active native Prompt projection, derived
summaries and current exact-source witnesses. Reuse the existing CodingHost
preparation seam and Context representations rather than another Agent loop or
Memory framework. Research direction is approved; concrete owner/API extensions,
summary budgets/privacy/fallback and rollout require subsequent authorization.
The proposed deterministic first increment is not implemented. Status, maturity,
dependencies, grants, parent obligations, observer Option B and durable recovery
remain unchanged; no scientific result or historical review credit is rewritten.

## Authorized active-projection increment — 2026-10-28

The explicit subsequent assignment implements a narrow opt-in
[Agents coding-input projection](../../development/active-context-projection.md)
through the existing host preparation seam. No second coding loop, Runtime
expansion, persistent memory, Tool executor or provider dependency is added.
Guarded independent repair and Qwen native-boundary delegation exercise actual
consumers. Historical facts, active Prompt, exact source authority and candidate
completion remain distinct. Model-assisted summaries, adaptive assessment,
Evidence durability, restart and observation Option B remain separate decisions.
Status, maturity, dependencies, grants and parent obligations remain unchanged.
