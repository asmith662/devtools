# Qwen coding worker and operational lifecycle audit

Baseline: **`7a657dba031c43a30d33086808899498ee616052`**, tree
`3df5930a1ac79817d771eb97b8a4d9ec28523457`. Local main, origin/main and a fresh
remote-main observation agreed before the ordinary audit branch was created.
Tracked/index state was clean; the thirteen known untracked forensic files were
authenticated and preserved. SQLite audit/repairs PRs #37–39 were already
integrated. Their committed 3,218-pass/two-live-skip/100% protected gate remains
dated evidence, not a newly executed gate.

This is a documentation/Intake audit, not a worker implementation, model run,
new autonomy architecture or reclassification of historical experiments. The
maintainer selected Qwen ahead of the previously recommended dashboard review;
that dashboard review remains outstanding. No observation policy is approved.

## Scope, depth and authority

The [frozen cohort](code-audit/qwen-operational-cohort.json) records all **230
tracked paths** in apps/qwen, tests/apps/qwen, scripts/qwen and tests/scripts/qwen
at the baseline. Sixteen operational source/test paths were selected before
body inspection: coding_loop, development_task, context_tools, continuation,
edits, commands, change_checks, navigation, api_contracts, model_tool_composition,
the coding_worker CLI, conftest and four main test modules. Their **9,641 lines**
received complete body/assertion/helper review. The required CodingTask owner
tasks.py received a separately identified full dependency review. Remaining
files have their exact versions and actual lesser depth retained; executing
their tests does not confer full body review.

Full development_task inspection includes retained Markdown/prepared/structured
experimental runners. They are not the coding_worker CLI's operational loop;
their weaker historical capture/restoration paths must not inherit native-loop
assurance. We did not execute their frozen scientific treatments. Immediate
WorkCycle/delegation/local-closeout, model/provider, Resource and Tool dependencies
were traced at selected interfaces; prior matching audits remain their evidence,
not a new full subsystem review. See [assurance and function ranges](code-audit/qwen-operational-assurance.json).

Authority remains the [taxonomy](../architecture/taxonomy.md), current source,
accepted [ADR-0001](../architecture/decisions/ADR-0001-cohesive-model-interaction-boundary.md),
RI/Context/Localization decisions, [architecture](../architecture.md), and
canonical backlog. The [comprehensive audit](comprehensive-code-audit.md) requires
exact-version review, independent outcomes and actual consumer evidence. README's
governed evolving-intelligence direction is broader than today's bounded coding
worker. Neither accepted architecture nor experimental success means that the
whole long-term system is implemented.

## Actual operational flow

| Stage and real owner | Admission, effect and retained result | Failure/recovery boundary |
| --- | --- | --- |
| coding_worker.main → select_task/task_from_dict → CodingTask | Trusted host objective, exact Git revision/content hashes, Python source/test/read corpus, new slots, fixed oracle and limits. Default named tasks are historical reproducible defects; host task JSON supplies other bounded engineering tasks. | A model cannot select its own task, commands, scope or grants. Current API requires existing tests and an initially failing assertion oracle; this is not a generic issue-to-requirements planner. |
| run_local_task → WorkCycle baseline helper → Checkout | Select/create ordinary feat branch at the exact task base; reject dirty/colliding content; bind existing/new paths; materialize only authenticated LF/CRLF equivalents. Checkout holds custody and owner.expect journals intended source before writes. | No backlog promotion or standing grant is needed for trusted local evaluation. Checkout grants serialization, not task/publication authority. Owner failure/recovery is separate from worker result. No actual canonical source mutation was probed. |
| local_interaction | Query existing service/profile readiness, require expected=observed fingerprint; construct unobserved LlamaCppInteraction with fixed endpoint/model/source and explicit sampling options. | It does not start servers or download models. Readiness is a point observation, not proof the server cannot change later. Model serving owns lifecycle; interaction owns requests. No service query/inference was executed here. |
| run_coding_task preparation | Refuse existing output directory; authenticate Git and physical frozen inputs; write fixed test/oracle runners; run baseline checks; freeze task/tools/settings. | Preflight does not prove oracle satisfiability or semantic completeness. Host test/oracle code executes candidate imports and is not an OS sandbox. |
| _turns request and Context | Prepared mode reacquires selected disclosures; native mode holds PromptMessage history, scoped ContextTools snapshot/index, optional map frame, observations and edit references. Project active input; for real llama clients measure actual tokenizer/template input before dispatch. Save request/stage intent first. | Fixed per-call and total time, call/action/proposal ceilings; 32K context/2K safety in this adapter. If current source/latest feedback cannot fit, refuse. No universal provider-capacity abstraction or unlimited context claim. |
| ModelInteraction.send → response admission | Archive normalized response/usage/native IDs; compare source to selected interaction; reject output-limit, invalid/mixed calls, missing/duplicate same-response IDs and source drift before action. | No automatic repeat after provider exception or unknown completion. Unknown usage stays null. Optional provider-observer failure can still hide a completed response under the unchanged policy. |
| ContextTools/CodingCommands → ToolRunner | Host-bound paths, schema/argument checks and freshness precede fixed read/search/map/API/Git/check execution. Context request mistakes can return correlated refusal feedback; source/authority errors terminate. Attempt count precedes dispatch. | ToolRunner validates/executes; it does not create authority. Calls in a read/check batch execute sequentially; earlier actions are not rolled back if a later action fails. REFUSED is not proof that an executor never entered. |
| observed/transaction admission → apply_source_patches | One proposal may contain up to 16 components across up to five task-authorized files. Authenticate current disclosed anchors/absence/API evidence, uniqueness, overlap and byte limits before mutation. Journal expected sources; one managed Git apply without --reject; verify installed text. | All-or-nothing admission is implemented. Check/apply are distinct Git operations, not a universal filesystem transaction; Checkout supplies source custody. Unknown installed bytes are preserved for reconciliation. |
| validate_workspace → CodingCommands bundle | Same fixed check owner serves host and model. Before/between/after checks authenticate declared source, immutable tests/read inputs, runners and configuration. Tests+oracle always required; quality and typing follow host task flags. Full logs and bounded categorized feedback are separate. | Passing focused checks means the declared criteria passed on that candidate, not that every requirement, semantic review or full protected suite passed. Broader d586 input/toolchain closure remains open. |
| repair/continuation | Failed admitted edits remain current during the same bounded task; verified unchanged source regions and replacements refresh observations. Next prompt carries exact current source, diagnostics, passed requirements and remaining limits. Refused proposals count; multiple components count as one proposal. | No automatic decomposition/subtask scheduler or host-generated repair patch. Model decides next investigation/edit. A text-only stop without the required edit/check does not become acceptance. |
| shared-check completion (opt-in) | After an edit passes, continue until model invokes check_changes; host calls is_current through ToolRunner before acceptance/restoration. Actual offline control reaches PASS/current. | Default completion stops after host checks. check_changes can legitimately block unrelated untracked apps/src/tests preparation; host artifacts must stay ignored until publication. Currentness is not review or publication authority. |
| finalization and handoff | Archive candidate source(s); restore only original/admitted known source; preserve unknown changes. Record restoration, original-input integrity, counters, nullable usage, disposition and result.json. | This is a candidate handoff, not a resumable checkpoint or Checkout-release certificate. A final write failure can leave no result after a known effect/restoration; no automatic retry follows. |
| separate WorkCycle integration | Governed WorkCycle validates task-specific authorization/expiry/delegation and claims dispatch once before calling the same loop. Local closeout separately authenticates result/candidate, installs, checks, binds independent review, validates protected inputs and explicitly commits/publishes. | Governed assignment-v1 does not silently inherit the local multi-file/native options. Worker acceptance, REVIEW_CANDIDATE, review, protected validation and remote acceptance remain different claims. No grant/review/publication effect was fabricated in probes. |

## Framework adoption and historical evidence

| Capability | Retained experimental evidence | Current operational adoption and actual consumer | Remaining limitation |
| --- | --- | --- | --- |
| Model requests/native calls | Prepared Markdown and native coding cohorts; Engineering14 useful implementation plus one behavioral repair | _turns constructs ModelRequest/Prompt/ModelSettings and calls ModelInteraction; descriptor projection follows ADR-0001 | Default operational client is llama.cpp/Qwen; no current multi-provider worker qualification. A model-neutral protocol is not measured portable effectiveness. |
| Lexical/source Context | Native read-only and source-grounded cohorts | acquire_context and ContextTools use canonical discovery, observation, corpus, file/symbol/window/mixed SourceSearchIndex and Planning/materialization | Host preselects at most 32 Python resources. Not whole-repository automatic task discovery, dependency closure or sufficiency. |
| Exact source/occurrence provenance | Source-grounding, edit diagnostics and EOF correction | Real repository/snapshot/resource identities, versioned units, exact half-open spans and disclosure identities reach native results and anchor admission | Edit handles Rn are local provenance references, not replacement RI identity or authority. Aliases/drift refuse; no atomic immutability against external filesystem actors. |
| Structural relationships/map | Native-map28 has deterministic map qualification; its genuine Qwen run did not invoke map or shared checks | Optional RepositoryMapNavigation uses canonical typed-core/map/ranking/Planning; independent real worker map→exact-source→edit control succeeds here | Only admitted declarations/resolved outgoing References are supplied; not every graph relation family. Live utility/selection improvement remains unestablished. |
| Obligation-driven Localization | Host-authored research treatments and accepted APIs | No operational acquire-localization/candidate-resolution/readiness consumer in this cohort | Existing 15bae0a6 owns explicit trusted task-obligation/witness composition. Rank is not obligation coverage. A+C remains unapproved. |
| Edits and fixed checks | Editing06, Environment13, Engineering14/15; later Codex bundle/check_changes delivery | Observed/path/nested interfaces share exact admission and managed Git; CodingCommands uses Resources and ToolRunner | Exact 4096-region/8192 aggregate/16384 patch/32768 resulting-source bounds. Available checks do not guarantee the model invokes them. |
| Native history/continuation | Continuation09 archived capacity replay and a separately authorized development continuation | Existing PromptMessage roles/call IDs, source-preserving projection, tokenizer measurement and archives | This is task-local Context projection, not Conversation/Memory or automatic restart. Historical supervisor continuation required separately bounded authority/evidence; not an operational resume API. |
| Runtime/Conversation | Separate narrow Runtime and historical experimental controllers | Native coding loop deliberately calls ModelInteraction directly; no Runtime/Conversation persistence in this path | Moving the entire loop into Runtime would violate its narrow owner and would not solve task recovery. |
| Evidence/usage/Persistence | Prior audits establish independent inspectors, usage collection and Conversation stores | Native worker writes application JSON and nullable usage totals; dashboard reads application records directly | No automatic InvocationMeasurement/normalized Evidence ingestion, EvidenceSink or SQLite task checkpoint. A JSON directory is not a safe replay protocol. |
| Review/integration | Environment13/Engineering14 and separate Codex closeouts | CLI closeout and governed WorkCycle compose existing independent validation/review/publication owners | Accepted candidate is not automatic approved/main delivery; source-restored flags do not prove Checkout finalization or remote publication. |

Historical [Engineering14](../../apps/qwen/evaluation/engineering-14/README.md)
records ten real requests, two transactions and one actual behavioral repair
without implementation intervention. It supports bounded capability, not merely
model-call conformance. [Editing06](../../apps/qwen/evaluation/editing-06/README.md)
records small Devtools/Pi comparisons, unequal action surfaces, an invalid oracle,
replacement confirmation and explicit limitations; it is not a controlled Codex
cost/superiority result. [Continuation09](../../apps/qwen/evaluation/continuation-09/README.md)
separates tokenizer replay, evaluator error and supervised development continuation.
[Native-map28](../../apps/qwen/evaluation/native-map-28/README.md) separates
available map Tools, offline qualification and a genuine unsuccessful Qwen run
that never selected them. These summaries were inspected and pinned; their full
raw ignored archives/scientific cells were not reaudited or replayed. No new live
effectiveness, feature authorship, candidate integration or comparative result
is claimed. Earlier Duration/B-0048 candidates are not the later independently
delivered production repairs.

## Confirmed P2: inconsistent terminal worker acceptance

New canonical proposal **`835a203f-8fd4-4bc2-ace8-8772137eaf2f`**. Owner:
coding_loop._turns shared-check completion and run_coding_task exception/final
accounting; consumer: coding_worker.main's `return 0 if result['accepted'] else 1`.

Independent temporary Git task: value() initially returns 0, tests preserve its
integer API, host oracle requires 1. A deterministic model reads source, proposes
an annotated return-1 replacement, passes actual tests/oracle/Ruff/format/mypy,
invokes check_changes, and receives host currentness. After `_turns` sets
accepted=True, inject one OSError at completion-stage persistence. The outer
exception handler changes disposition/error but never clears accepted.

Actual result: **accepted=True, CONTEXT_TOOL_EXECUTION_FAILED**, retained OSError,
three model entries, one real Git application, original bytes restored, passing
candidate/check evidence retained. Feeding that actual result to the maintained
CLI return path yields **exit 0**. The unaffected shared-check control returns
accepted=True/ACCEPTED. The defect repeated across two qualified probe executions;
one final sixteen-case set is the counted population.

This is a task-outcome/accounting defect. It does not establish that the candidate
is incorrect, that validation failed, or that protected publication was bypassed.
Local closeout initially admits by accepted/task/oracle identity but independently
rechecks source, validation and review before publication. Current governed
assignment-v1 does not enable this native shared-completion option. No actual
disk failure or production model task occurred; a controlled fault schedules a
reachable owned write boundary.

Recommended bounded correction: reconcile fatal task exceptions with final
accepted/disposition/CLI status, preserving known response/check/candidate facts,
uncertainty and source custody. Test real run_coding_task plus CLI, normal shared
completion, before/after edit/capture failure and cancellation. Do not solve this
by retrying, discarding a known provider result, changing ModelResponse, or
implementing optional-observation Option B. A separately approved qualified
success policy would need an explicit contract; current unqualified success
should not contradict its own terminal failure. No repair is implemented here.

Duplicate checking covered all 67 prior payloads and relevant histories. Delivered
41a497a8/660900a1/751451cb concern immutable validation inputs, budgets and source
correspondence, not this new post-acceptance failure. Those repairs remain intact.

## Independent schedules, limits and test quality

The [probe artifact](code-audit/qwen-operational-probes.json) retains authored
source, literal expectations, outcomes, command evidence and qualification:
**16 cases: one desired-contract violation; 15 agreeing controls or qualified
limits**. Tiny task setup reuses the maintained independently authored fixture;
model actions, fault schedules and expectations are independent. No Devtools tree
was copied. No model, Docker/server, private log or frozen controller ran.

- Prepared bounded completion, native failed-oracle feedback followed by repair,
  and shared-check completion work through the real public loop and actual checks.
- Unobserved anchors and foreign response source refuse before effects. Map
  orientation is metadata; a whole-file anchor extending beyond the selected
  declaration's final newline correctly refuses. Exact in-range source accepts.
- Cancellation during model entry remains completion-unknown, with null usage
  and no retry. Cancellation during post-edit validation propagates HOST_CANCELLED
  and restores known source. Neither proves external rollback.
- An unexpected source change is archived and preserved with
  CLEANUP_RECONCILIATION_REQUIRED; it is not overwritten with the baseline.
- A fault after actual Git application leaves an admitted candidate and restores
  recognized source without repeating the edit. A final result-write failure
  propagates after restoration, with candidate evidence but no result.json.
- A fixed Git command actually exits 0, then its result wrapper raises. The worker
  records a REFUSED event and terminates without retry; the command's intent lacks
  completed evidence. This confirms that REFUSED alone does not prove nonentry,
  not that a destructive command or an OS process leaked.
- Reusing an existing report directory refuses before an additional invocation.
  There is no CLI resume/task-state rehydration protocol. Host-created fresh
  directories are new work, not evidence-authorized replay of old effects.

Two initial harness failures are excluded: missing canonical import path and a
Windows temporary path alias correctly refused before model entry. The initial
map expectation incorrectly included an undisclosed newline; it became an explicit
negative control with a separate positive. No harness error is counted as a bug.

The maintained **471 tests passed** in 474.60 pytest seconds (476.437891 managed
seconds), exit 0: all tests/apps/qwen, coding_worker CLI and delegation tests.
This includes real oracle/managed-Git paths plus intentionally synthetic
acceptance, private-helper and historical captured-input fixtures. Test execution
does not establish model reasoning. Some tests stub validation or profile
readiness, so they prove sequencing/contract behavior only. Legacy fixtures assert
internally composed round trips; new literal probes provide independent outcomes.
Selected test bodies were reviewed fully; other executed test files retain
EXECUTED_ONLY or targeted depth and exact remaining versions.

## Prioritized architecture gaps and realistic decisions

| Priority / capability | Concrete evidence and consequence | Existing owner / bounded recommendation |
| --- | --- | --- |
| 1: trustworthy terminal outcome | New post-acceptance write fault leaves accepted=True/failed disposition and CLI success | 835a203f; bounded worker accounting repair before using accepted as a complete run-success signal. No model/observer redesign. |
| 1: task-relevant Context and completion coverage | Host must preselect <=32 Python files; search/map results do not establish mandatory obligations; no Localization native consumer | 15bae0a6, B-0002/B-0035; decide one explicit host obligation frame and actual native readiness consumer. Preserve lexical escape and unresolved witnesses. Not another graph/embedding layer or automatic planner; A+C still needs approval. |
| 1: coherent application ownership/edit feasibility | One _turns body combines protocol, budgets, projection, effects, validation and journals; helpers share a module with historical task runners. coding_loop73594 and development_task60528 physical bytes exceed32768; even an8192-byte all-deletion first proposal cannot reach the result bound. context_tools39019 also has substantial pressure | Existing39c6663a; identify current compatibility and responsibility seams, extract only existing behavior into cohesive application owners with unchanged admission/validation, rather than increasing bounds or inventing a generic executor. File size is a demonstrated maintenance constraint, not sufficient authority to refactor. |
| 2: recoverable task-local working state | In-memory history/observations/budgets vanish at process exit; records are sufficient for inspection but no authenticated load/resume protocol exists. Missing completion after an effect cannot license redispatch | B-0028/B-0034/B-0011; define a bounded stopped-task reconciliation and continuation decision over existing records, code/task/input identities, remaining budgets and Checkout custody. Do not add a backend, replay Tool effects or reuse Conversation persistence as if it stored this state. |
| 2: useful evidence/operator consumption | Native journals/usage are not normalized framework Evidence; successful callbacks do not prove durability; optional observer can hide a known response | B-0011/B-0023/B-0046 and existing decision brief; choose a real consumer and narrow correlation/capture policy before ingestion. Reuse existing records first, without a second store or EventBus. |
| 2: measured operational effectiveness | Some useful autonomous tasks succeed, but later tasks exhaust Context, fail integration or do not invoke available capabilities; historical oracles and supervision differ | B-0009/88246171; after bounded contract/ownership decisions, a separately authorized fixed fresh engineering task can evaluate complete obligations and failure recovery. Do not retune/replay sealed cases, assume Codex savings or start an open-ended research program. |
| 3: documentation/adoption clarity | Current README/architecture contain dated three-proposal, source-only and old candidate-unintegrated statements beside newer authoritative overlays. Default named tasks intentionally reference old baselines | B-0006/B-0009; consolidate current operator guidance with explicit historical links in later authorized documentation maintenance. Preserve scientific records and grant/path history. This audit supplies the present answer without rewriting them. |

The useful boundaries are already present: ModelInteraction owns model semantics;
Resources own I/O/process mechanics; ToolRunner owns typed execution; Context/RI
own grounded observations; Checkout owns source serialization/recovery; WorkCycle
owns assignment authority and integration. Adopting narrow Runtime merely to move
the loop would not improve these responsibilities. The application needs clearer
composition and actual consumers, not universal Agent/Run classes. Repeated full
snapshot/index/reference rebuilding is real reuse/performance pressure under
existing RI proposals, not a new cache/source authority authorized by this audit.

## Observation preference and host implications

Option B remains preferred in principle and **unapproved**. The default CLI
adapter has no observer; opt-in observed adapters can still lose a normalized
response through callback/backward-wall-clock failure. _turns' MODEL_REQUEST
classification cannot recover that response from today's exception. The host
has a task/turn/request hash and a natural place to retain a separate capture
failure, but source/turn alone is insufficient correlation for shared concurrent
adapters. ModelInteraction occurrence and app turn identity are not automatically
joined. Required decisions remain:

1. Per-invocation correlation at ModelInteraction/provider observation and the
   application composition boundary, without adding metadata to ModelResponse.
2. Handling failure of secondary reporting through existing Inspector/report
   ownership; no recursive reporter or silent loss.
3. Privacy-safe payload and retention via capture policy and explicit app records.
4. Mandatory-versus-optional evidence admission at trusted Qwen/WorkCycle host
   acceptance before actions, independently of known provider success.

No callback suppression, timestamp clamping, retry/refund, automatic SQLite save
or new Evidence store follows. The new task-journal P2 is not an approval to
silently implement this separate model-observation policy.

## Canonical disposition, validation and finite remainder

One new P2, three separate append-only advisories on existing39c6663a/15bae0a6/
88246171, and evidence overlays on existing parent records are the only backlog
effects. Administrative states, B-numbers, dependencies, grants and approvals are
unchanged. No already delivered RI/worker/Checkout/validation/Evidence/Core/model/
Persistence repair is rescheduled. [Checkpoint](code-audit/qwen-operational-checkpoint.json)
records exact source/test and physical-input preservation, JSON/JSONL, local
links/layout, canonical Intake chains, whitespace, forensic and ref checks.
There are no production/test/configuration changes, no new protected-gate claim
and no live execution. Normal GitHub publication/merge eligibility is checked;
actual final commit/main/PR identity belongs in the completion record.

The remaining **213 Qwen-root paths** include unselected tests/helpers, legacy
worker/read-only controllers, acceptance scripts/service adapters and retained
evaluation artifacts. The ledger distinguishes their prior audit reuse/targeted
inspection, execution-only and inventory-only status; it does not declare all
Qwen or Serving complete. Remaining Tools/Core/Resources/configuration surfaces,
dashboard HTTP/frontend security and disclosure, developer/scientific tooling and
cross-domain reconciliation stay explicit under the comprehensive inventory.

Next bounded assignment: separately authorize the new terminal-outcome P2 with
permanent actual-loop/CLI fault regressions and full committed production gate;
then decide the existing minimal task-obligation consumer/ownership scope rather
than another minor Qwen experiment. Dashboard/tooling review remains the next
unaudited application flow, not begun here. RI fixtures93/93 and experimental
paths606/606 retain their defined completion; **188 historical exact versions**
remain a separate seven-family program with no new credit. A+C and observation
Option B remain unapproved. No successor-session dossier was prepared.

`audit:qwen-operational:7a657dba:20261027`.

## Delivered terminal-outcome maintenance overlay

The existing P2 is delivered through normal PR #41, production `5e16b832429789ea9dd63989476a163b376f20db`, verified main `9ea992f347c18b5206b50e1cd6c7ad89b2f564a8`. Original frozen17-body findings/probes remain historical; changed source/test/package-document versions have separate delta overlays. [Correction and remaining decisions](../development/qwen-terminal-outcome-repair.md); [exact committed validation](code-audit/qwen-terminal-repair-20261027.json). No Localization/A+C, application extraction, restart/Evidence protocol or observation policy was implemented. `repair:qwen-terminal-outcome:5e16b832:20261027`.

## Delivered native obligation consumer overlay

The specifically authorized first opt-in host-frame consumer is delivered by PR #43, production `b7790180629e840d63d1d5b6815eb12a5d39a5a4`, verified main `7f4f0871d0689ec2ae565bdcad741d032845af9d`. [Contract and exact validation](../development/qwen-native-obligation-context.md); [machine receipt](code-audit/qwen-obligation-integration-20261027.json). Currentness-qualified actual active source disclosures, explicit caller decisions and existing Localization readiness now gate native source-changing proposals. The original17-body audit/probes and earlier maintenance stay historical; new/changed versions have separate overlays. Broader15bae0a6/A+C, automatic resolution, task-only evidence, restart/normalized Evidence, OptionB and39c6663a remain separate. `integration:native-obligation-context:b7790180:20261027`.


## Delivered operational turn cohesion overlay

Production `cd0a8330282d9b074ccb6d5dbf80a0f8c963c6ff`, PR #45, verified main `abe1ca13fbb5960f937383bb9e257ce05fe14f22` extracts application turn/prompt/fixed Tool dispatch ownership while retaining task lifecycle and terminal custody in coding_loop. [Contract and validation](../development/qwen-operational-turn-cohesion.md); [exact changed versions](code-audit/qwen-turn-cohesion-20261027.json). Original frozen17-body review and prior overlays retain their version/depth. Development_task/context_tools, recovery/Evidence, A+C and OptionB remain separate. `integration:qwen-turn-cohesion:cd0a8330:20261027`.

## Delivered framework migration 1 - 2026-10-27

The current explicit maintainer assignment authorized only the native model/Tool composition increment. Production `31627dcae17fa1e429fbc4c1f3d31941ef5803a7`, PR #48, accepted main `6a331e65ebb5f5c467a32eb694ca7a95056865a1` delivers a real Agents-owned operation used by both Qwen dispatchers and a non-Qwen host denied application imports and file reads. Existing ToolRunner, native model values, source/check Resources and host authority remain owners. [Contract, independent effects, validation and limits](../development/native-model-tool-composition.md). Later source/check/coding-Agent migrations remain proposals requiring approval; this is not a whole-Agent promotion, parent closure or automatic status/maturity change. Original design/audit evidence and prior overlays retain their dates/blobs. `integration:native-model-tools:31627dca:20261027`.
