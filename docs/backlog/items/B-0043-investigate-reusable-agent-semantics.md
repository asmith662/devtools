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

## Active-projection delivered evidence — 2026-10-28

Implementation `75692067b3c7dc8b21a3be2eb5d794f650b11d87` is verified on accepted main checkpoint
`bf91842a6ba8c360bc694bfe45221154368cf1a2` after the unchanged committed protected gate and independent
source/input checks. [Contract and measured validation](../../development/active-context-projection.md),
[exact receipt](../../research/code-audit/active-context-projection-20261028.json).
This delivers only opt-in deterministic active projection and native-boundary
reuse. Original first-request inventory, structured summaries, adaptive/live
assessment, Evidence durability, broader A+C and recovery remain separate.
No status, maturity, dependency, grant, approval or parent closure is inferred.

## Authorized semantic-compaction increment — 2026-10-28

The explicit Implementation 2 assignment authorizes the bounded
[structured working-state extension](../../development/semantic-context-compaction.md)
to the existing neutral active-projection lifecycle. Host-selected outbound
disclosure and replacement, a separately bounded optional ModelInteraction,
cited fallible notes, exact recent/check evidence and deterministic fallback
reuse existing Context/Prompt/source/custody contracts. Guarded scripted repair
demonstrates an independent consumer; no real summary effectiveness is claimed.
This planning entry is not delivery evidence or a new approval/grant. Adaptive
policy, live assessment, initial inventory, broad A+C, observation Option B,
Evidence durability and autonomous recovery remain separate. Status, maturity,
dependencies and broader parent obligations remain unchanged.

## Semantic-compaction delivered evidence — 2026-10-28

Implementation `dfe62a3ed2ff353ee62e186fdaf31f4d04695bc1` is verified on accepted main checkpoint
`37a4797099c3ff3be4c57b573a5d5d0e593b20d5` after the unchanged committed protected gate and exact
source/input/ancestry checks. [Contract and measured limits](../../development/semantic-context-compaction.md),
[receipt](../../research/code-audit/semantic-context-compaction-20261028.json).
This delivers only optional bounded semantic working-state notes, independent
repair consumption and safe deterministic fallback. Adaptive policy, real summary
fidelity, first-request inventory, Evidence durability, restart, broader A+C and
observation Option B remain separate. No status, maturity, dependency, grant,
approval or parent closure is inferred. `integration:semantic-context-compaction:dfe62a3e:20261028`.
## Adaptive Context assessment checkpoint — 2026-10-29

The authorized [adaptive compaction increment](../../development/adaptive-context-compaction.md)
uses the existing neutral coding host and semantic operation. Host-valued omitted
records, explicit pressure/reserve, auxiliary ceilings, cache validity and failure
suppression are now implemented locally in `7cf1eb79`. The
[real comparison](../../../experiments/context_compaction/REPORT.md) did not adopt
either generated summary; one fallback candidate passed independent checks.
This is a bounded mechanism and qualified assessment, not validated universal
strategy selection or completion of reusable-agent architecture. Qwen legacy
adapter migration, recovery/Evidence, Option B and broader A+C remain separate.
No status, grant, approval or parent closure is inferred before delivery evidence.

## Adaptive Context delivered evidence — 2026-10-29 UTC

Implementation `7cf1eb79dc638dece63ae80971d3de342758f71b` is verified on accepted main
`f558d4b9acd83e565604aa158f8917f56e6591fb` after the unchanged committed protected gate and exact physical-input,
source-blob and ancestry checks. [Contract](../../development/adaptive-context-compaction.md)
and [receipt](../../research/code-audit/adaptive-context-compaction-20261029.json)
record the bounded opt-in policy and the real comparison's format refusals,
deterministic fallback and unestablished semantic benefit. No universal threshold,
legacy Qwen adapter migration, durable recovery, Evidence store, observation
Option B, broader A+C, grant or parent closure is implied. Existing statuses,
dependencies and outstanding historical obligations remain unchanged.
`integration:adaptive-context:7cf1eb79:20261029`.

## Local agent reliability checkpoint — 2026-10-29

The authorized [bounded correction](../../development/local-agent-reliability.md)
and [retained verification](../../../experiments/local_agent_reliability/REPORT.md)
address known source-range argument feedback and structured summary admission.
The live JSON setting still yielded a fence; explicit envelope handling was
subsequently verified without rerunning the model. Source usability worked,
but a frozen focused expectation was incorrect and repair quality is confounded.
This is bounded evidence under existing owners, not a new grant, proposal,
parent closure or approval of broader autonomy/Context/Evidence work. Accepted
publication will be recorded separately after final protected validation.

## Delivered reliability evidence — 2026-10-29

Ordinary direct-main publication was independently verified at `f4ddecff8dea2c00f5ef86f461f890a866e6352b`,
including protected implementation `9593d8f541a3cf58478f77052accb80b5a99e681` and matching physical
validation inputs. The [delivery receipt](../../research/code-audit/local-agent-reliability-20261029.json)
records typed source-range refusals, bounded source metadata, explicit auxiliary
JSON settings and optional single-fence normalization. This is append-only
evidence under this existing owner; no new grant or parent closure is implied.

The [one frozen live verification](../../../experiments/local_agent_reliability/REPORT.md)
had usable source reads but no live summary adoption or accepted candidate.
Its focused oracle defect is preserved and repair conclusions remain qualified.
Post-hoc offline normalization and scripted non-Qwen consumption are separately
identified. Context fidelity, truthful repair feedback, Evidence/recovery and
broader reusable-agent obligations remain open.

## Supervised maintenance checkpoint — 2026-10-29

The authorized [oracle-integrity increment](../../development/oracle-integrity-preflight.md)
provides finite independently cross-checked expectations and required preflight
controls. The [one frozen B-0035 attempt](../../../experiments/local_maintenance_feedback/REPORT.md)
made eight real requests and two source-grounded proposals. Both were refused
at the unchanged 32,768-byte resulting-source ceiling: the existing owner was
32,648 bytes, and proposals were 32,990/33,568 bytes. No source change, candidate
validation, effective repair or model-authored integration occurred. The original
inventory obligation stays open; no Codex substitute was supplied.

Existing cohesion/self-editability pressure now has direct operational evidence
in the reusable host. Recommend a separately authorized coherent extraction,
not higher limits or another compaction policy. B-0035/B-0043, existing cohesion,
Evidence/recovery and historical RI obligations remain open. This checkpoint
creates no proposal, grant, approval, status change or parent closure. Delivery
of the preflight implementation will be recorded after accepted-main validation.

## Delivered supervisor-feedback evidence - 2026-10-29

Ordinary direct-main publication was independently verified at
`3712af8db1e0757fd429b4ac99473eb84366d913`, including protected implementation
`9aae92ca8ac176c3a15940028b7a64a671da1ba1` with matching executable blobs and physical validation
inputs. The [delivery receipt](../../research/code-audit/supervisor-feedback-20261029.json)
records the reusable finite oracle-preflight comparison, atomic-repair
characterization and the independently graded real maintenance attempt.

This delivers supervisor reliability support, not the B-0035 inventory change.
The local model's two oversized proposals were refused; no model-authored
candidate was accepted or substituted by Codex. No worker validation or effective
repair occurred. Existing B-0035/B-0043, cohesion, Evidence/recovery and historical
RI obligations remain open. This append-only advisory creates no grant,
approval, proposal, status transition or parent closure.


## Coding-host cohesion and edit feasibility - 2026-10-29

The explicitly authorized [host extraction](../../development/coding-host-cohesion.md)
moves pure source-batch geometry into the existing Agents editing owner while
retaining host readiness/currentness, native decoding, effects and custody.
The first-request inventory obligation remains unimplemented by the supervisor.
A separate preflighted local attempt will determine maintenance outcome.

The 32,768 resulting-source setting is host policy, separate from Prompt bytes,
edit-region and aggregate limits. Whole-file materialization can reject a small
legitimate edit in a larger file. A future coordinated finite materialization/
growth profile deserves review under this existing owner; it must preserve
SourceScope/custody bounds and exact witnessed edits. No limit is raised and no
general large-file editing contract, new proposal, grant or parent closure follows.

## Post-extraction maintenance observation - 2026-10-29

The separately frozen [Maintenance-cohesion-0001](../../../experiments/local_maintenance_cohesion/REPORT.md)
ran after the committed extraction passed 3,836 protected tests, two optional
skips and 100% configured coverage. Ten acting requests acquired five distinct
source spans and repeated three after active omission. No proposal, edit, worker
check, repair, semantic summary or model-authored integration occurred. The
unchanged archive still fails the pre-frozen inventory obligations. B-0035 and
the broader coding/Context work remain open.

The extraction fixes one ownership pressure and restores practical host edit
headroom without raising limits. The next observed constraint is task-relevant
source selection/retention under bounded continuation, not a demonstrated new
edit-size rejection. Use existing symbol/window retrieval, exact ranges and
projection to investigate it in separately authorized work. This advisory adds
no proposal, grant, approval, status transition or parent closure; ordinary
publication evidence follows only after accepted-main verification.

## Delivered cohesion and maintenance evidence - 2026-10-29

Ordinary direct-main publication was independently verified at
`195035b99f97081e63fffade3313d4a481839a2f`, containing protected executable commit
`11945801c1f42e2adfc1614f672fc96d3ae400eb`. All 1,185 recorded physical validation inputs
and the accepted source/test blobs match the committed gate. The
[delivery receipt](../../research/code-audit/coding-host-cohesion-20261029.json)
records GitHub requirements, ordinary fast-forward publication, 3,836 passed/two
optional skips, 100% configured coverage, preservation and independent grading.

Delivered: cohesive pure batch-admission ownership and host edit headroom under
unchanged limits. Not delivered: B-0035 inventory behavior. The one real model
attempt stopped after ten requests without a proposal; its archive is unchanged.
No model-authored implementation, supervisor replacement, grant, approval,
proposal/status transition or parent closure is implied. General large-file
editing policy, Context working-set pressure and existing broader obligations
remain open. No next increment is begun.

## Authorized source-navigation increment - 2026-10-29

The [bounded implementation](../../development/source-navigation-continuity.md)
connects existing scoped file/symbol/window search to exact native unit acquisition.
It reuses current projection rather than adding unbounded pinning. Frozen trace
reconstruction finds that all broad reads cannot fit; scripted precise selections
retain three exact methods and permit an independent fixture edit/check. This is
not B-0035 inventory delivery or evidence of autonomous source-selection success.
The [new protocol](../../../experiments/local_maintenance_navigation/protocol.md)
separately preflights a single maintenance opportunity. Broader obligations stay
open; no proposal, grant, approval, status transition or parent closure is created.

## Source-navigation maintenance outcome - 2026-10-29

[Maintenance-navigation-0001](../../../experiments/local_maintenance_navigation/REPORT.md)
exhausted ten requests paging metadata, with no source read, edit or validation.
Its unchanged archive fails the same three focused/five withheld obligations.
No model-authored inventory implementation, new grant, status transition or
parent closure is implied. B-0035 and broader task-directed navigation remain
open. The separate grading owner was released only after explicit human consent
through default-No recovery; missing grading exit receipts remain unknown.

## Verified publication - 2026-10-29

Ordinary non-force publication was independently verified at
`75d511694bf2971645c7fca3f3fb2134514f19b0`, containing protected implementation
`e3be8f8e7890ede763ba5770c7ac08621c57d294`. All 1,189 physical gate inputs and
accepted source/test blobs still match. The explicit human-authorized default-No
recovery released the grading owner without redispatch or authority transfer.
The failed evaluation remains unchanged: ten metadata pages, zero source reads,
proposals, edits or worker checks. Missing grading-wrapper exit receipts remain
unknown. No model-authored code, B-0035 closure or next increment is implied.

## Authorized task-directed navigation increment - 2026-10-29

The [bounded host integration](../../development/task-directed-navigation.md)
reuses existing file/symbol search for initial task candidates and makes global
outline browsing explicit under a finite host allowance. This is incomplete
metadata and does not implement B-0035's complete inventory. A separately
preflighted [maintenance protocol](../../../experiments/local_maintenance_task_navigation/protocol.md)
will record actual model use if protected validation permits entry. No grant,
proposal/status transition, parent closure or model success is implied.

## Task-directed navigation evidence - 2026-10-29

The [shared entry](../../development/task-directed-navigation.md) passed protected
validation; [Maintenance-task-navigation-0001](../../../experiments/local_maintenance_task_navigation/REPORT.md)
selected relevant source immediately but exhausted ten requests rereading broad
regions, without any edit or worker check. Independent focused/withheld grading
rejected the unchanged archive. Complete authorized inventory is still missing;
no model-authored work, grant, approval, status transition or parent closure is
implied. Method-sized working-set selection remains concrete unresolved pressure.

## Verified publication - 2026-10-29

Ordinary non-force publication was independently verified at
`faa7bd3d04fdfaaecd9499d01faaaa3e1afb7231`. Its source/test blobs and all 1191 physical
protected inputs match committed executable tree `4d5ad371dd4d43cb677ad2c7d9ac40549a3fd573`.
Checkout is released, tracked state is clean, and prior forensic files, experiments
and refs are preserved. The live attempt remains a failed B-0035 result with no
model-authored implementation; no status transition or additional authority follows.

## Investigation-to-implementation evidence - 2026-10-29

The [source-status projection](../../development/investigation-transition.md)
adds bounded opt-in active-source and historical-disclosure facts, reusing existing
Context bindings. The unchanged protected gate passed 3,899 tests, two optional
skips and 100% configured production line/branch coverage. The separately frozen
[read-only diagnostic](../../../experiments/coding_transition/REPORT.md) used four
real Qwen calls: task-directed search followed by three reads, with no expressed
implementation decision or blocker. A repeated additional range had been evicted;
all core host methods stayed exact. No B-0035 code, candidate, worker check, grant,
status transition or parent closure follows. Before another full attempt, test a
bounded decision checkpoint and continuously required source selection, accounting
for annotation overhead; this records pressure, not new execution authority.

## Verified publication - 2026-10-29 local / 2026-10-30 UTC

Ordinary non-force main publication was independently verified at
`6fbd7d1a87307c9b585c9bce558259d7440d7182`, containing protected executable commit
`c2bc06f4f604c6ccb87279f6315bfa87b59ce6fa`. All 1188 physical protected inputs and
source/test blobs match. Diagnostic JSON blobs preserve exact measured bytes
under scoped data-only attributes; executable input bytes did not change.
Checkout released normally, tracked state was clean, and original experiments,
forensic files, RI ledgers and historical refs were preserved. The read-only
four-call diagnostic remains a failed transition with no candidate or B-0035
completion. Documentation-only receipt closeout adds no execution authority.

## Decision checkpoint - 2026-10-30

The [paired assessment](../../../experiments/decision_checkpoint/REPORT.md)
compared identical source/task messages with and without source Tools. B-0035
produced a relevant Tool query versus partial prose with a real undisclosed-callee
question and unsupported assumptions. Both smaller edit-contract controls reached
correct core decisions, including with Tools available. Recommend completing the
small initialization/message-construction source closure through existing Context
selection before another full trial; no new phase framework, model success, grant,
status transition or B-0035 delivery follows. Production inputs remain unchanged.

## Supervisor-prepared B-0035 checkpoint — 2026-10-30

The [new source-backed delegation](../../../experiments/supervised_b0035/REPORT.md)
closed the initialization/navigation source gap using existing Context materialization.
One real response-only Qwen request timed out at 150 seconds; server logs record
generation and cancellation, but no answer or supported hypothesis was received.
No coding phase, candidate, worker check or model-authored production change followed.
B-0035 remains open. Reconcile concise decision-output/time bounds before a separately
authorized follow-up; no new framework, grant, status transition or parent closure
is implied. Prior evidence and unknown historical receipts remain unchanged.
