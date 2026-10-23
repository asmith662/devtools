# Initial architecture and production-adoption inventory

## Disposition

Initial source-backed audit, 2026-10-23. This is dated evidence and a research
starting point, not a replacement architecture, API index, backlog or deployment
certificate. The [finite phase charter](../development/reconciliation.md#finite-architecture-and-research-reconciliation-2026-10-23)
owns the immediate scope. Taxonomy, the documentation map, accepted ADRs, current
source/tests and canonical backlog retain their existing authority.

The requested starter ZIP was not found in accessible canonical-checkout paths.
No attachment path was supplied. Permission-restricted and excluded cache regions
limit that search. Its manifest and three document bodies were not available;
their SHA-256 values were **not verified**. The supplied 18 candidate stories
therefore cannot be reconstructed or claimed deduplicated. This report and the
charter are Codex-authored from the user's explicit direction and actual source.

## Authenticated baseline and method

- Feature/local/remote: `feat/qwen-context-worker` at
  `3c09641dd17b13b83c2fe84e3f1cf4920ca7186f`.
- Protected remote main: `5d979920d0728775ed529457c88f5b68b440c64f`.
  These identities were queried remotely; no branch switch or main write occurred.
- Tracked/index state initially clean; 13 original forensic files untracked and
  fingerprinted. One registered canonical checkout; no active Checkout owner.
- Git tree/blob comparison, current exports/source/docs, permanent test bodies,
  experiment manifests and delivery reports were inspected. No production tests,
  scientific experiment or inference were run to create this inventory.
- [Dated machine evidence](../development/reconciliation-inventory-20261023.json)
  records source blob comparisons, component counts, directory/custody metadata,
  original forensic identities and explicit inspection limitations. Git blob IDs
  establish byte equality at the pinned revisions, not behavioral equivalence for
  different blobs. Prefix counts overlap and include `__init__.py`; test-tree
  counts include excluded `tests/experiments`, not protected-test collection size.
- The ordinary Git helper refused a tree listing above its 1 MiB output bound.
  The audit used the existing CommandExecutor with a specific 16 MiB metadata
  allowance and checked truncation. No execution helper or limit was changed.

## Documentation and backlog authority

| Responsibility | Existing canonical address and rule |
|---|---|
| Terminology/current architecture | [Taxonomy](../architecture/taxonomy.md), [architecture](../architecture.md), [documentation map](../documentation_map.md); do not infer implementation from acceptance |
| Decisions | `docs/architecture/decisions/ADR-0001` through `ADR-0005`; accepted status belongs to each ADR, no parallel decision index |
| Sequencing | [Roadmap](../roadmap.md); historical research recommendations are not current execution selection |
| Research | [Research inventory](README.md); preserve substantive bodies and include a Disposition section |
| Experimental outcomes | [Experiment lifecycle](../../experiments/README.md), collection `SUMMARY.md`/`manifest.json`, case protocol/result/Stage D; no blanket PASS means adoption |
| Historical implementation | [Ledger](../implementation_ledger.md); historical evidence, not an API/roadmap authority |
| Maintenance | Existing `docs/development/reconciliation.md` and [validation profile](../development/validation.md); no separate maintenance authority found or created |
| Backlog | [Overview](../backlog/overview.md), [metadata](../backlog/metadata.md), existing `epics/` and `items/` B-numbers |
| Discovery intake | Existing `scripts/backlog/intake.py`; UUID proposals plus append-only advisory reviews; no B-number/approval/promotion in this audit |
| Package/component navigation | Documentation map plus package-local `docs/overview.md`, exports and tests; this dated matrix is not a second component registry |
| Local handoff | Ignored `codex-handoff/latest.md` and `.local/codex-result.md`; durable findings remain in the documents linked here |
| Artifact custody | Existing reconciliation and experiment recovery policy; [current custody inventory](../development/artifact-custody-inventory.md) adds observations, not deletion authority |

## Production-adoption matrix

All rows below have maintained source on the published feature baseline. Main
means source integration at the authenticated destination, not a running service
or proof of live model adoption. `same` means all Python blobs under the indicated
prefix match main; `delta` means present but differing/new files require the
specific capability to be reviewed. Historical tests below are evidence locations,
not fresh passing results from this audit. Counts are in the machine evidence.

| Capability / current source owner | Historical evidence / feature publication | Protected-main source | Actual maintained consumer / independent evidence | Remaining work |
|---|---|---|---|---|
| Core paths, `src/devtools/core/paths/` | Maintained foundation, feature HEAD | same: 4 files | Commands, filesystem, models, WorkCycle; `tests/core/paths/` | API/consumer audit, no new path resolver |
| Core time, `src/devtools/core/time/` | Maintained foundation | same: 7 files | Runtime, events, usage, custody timestamps; `tests/core/time/` | Pending duration-contract proposal remains unresolved |
| Core identity, `src/devtools/core/identity/models.py` | UUID constructor invariant delivered in continuation09 | delta: constructor validation absent on main | Domain identity wrappers; `tests/core/identity/test_uuid_invariant.py` | Selective destination review; do not equate main file presence with invariant adoption |
| Filesystem model/codec/read/write owners | Earlier JSON work, binary and bounded-read publications in engineering08/continuation09 | delta: 6 differing files, binary codec feature-only | Commands/Tools, package exports, `tests/resources/filesystem/` | Separate JSON/binary/bounded-I/O compatibility and adoption review; B-0048 approval is not adoption |
| Commands stdin/environment/exit-code/output validation/decoded output | Original five-capability provenance in commands integration/new-module22 reports; reviewed main-derived branch | same: all 9 source files, merged PR #1 | CommandExecutor, CommandTool, Codex integration, scripts; real stdin/environment/exit/output permanent tests | Already source-adopted. Reconcile pending intake states; retain Windows/child-process limits |
| Local model serving, `src/devtools/models/serving/` | llama.cpp/vLLM/Hugging Face and profile identity source | same: 6 files | `scripts/qwen/llama_cpp_service.py`, model benchmarks; `tests/models/` | Serving process availability/profile is operational, not Agent semantics or inference success |
| ModelInteraction protocol/values | ADR-0001; `models/interaction/` exports | present, 4 files differ | Provider adapter and Runtime; tests under `tests/models/interaction/` | Native message/settings/provider conformance differs from main; review actual hunks |
| llama.cpp/native message templates | Feature provider and Prompt changes | delta in prompt/provider/settings | Native Qwen request/token measurement; provider regressions | Destination compatibility and capture policy must travel together |
| Conversation/history | Maintained `agents/conversation/` | same: 4 files | Runtime and conversation persistence; conversation tests | Conversation is not Run or mutable task execution state |
| External Codex Agent integration | `agents/integrations/codex/` | same: 7 files | Agent CLI/session adapter, usage ingestion; agent integration tests | Do not reclassify the external Agent as a raw model/provider |
| Narrow Runtime/InteractionAttempt | ADR-0001, execution package | same: 4 files | Acceptance scripts `two_read_acceptance`, `two_action_read_only_acceptance`, `patch_proposal_worker_acceptance`; execution tests | Native coding loop calls interaction directly; no generic orchestration promotion inferred |
| Tool protocol/ToolRunner/CommandTool | `src/devtools/tools/` | same: 7 files | ContextTools/CodingCommands, fixed checks; Tool tests | Minimal validate/execute substrate; generic tracing is not provided by its name |
| Terminal/model Evidence | ADR-0001, `observability/evidence/` | base present; structured-history capture differs in 1 file | Inspectors and independent evidence tests; usage consumes invocation measurements | Failure observation, durable collection and layer correlation still qualified gaps |
| Observed usage, forecasts and pure usage constraints | `observability/usage/`, `governance/` | same: 8 usage and 2 governance files | `scripts/usage.py`, metadata-only Codex adapter, orchestration measurement; usage tests | Partial observed usage is not billing/account-wide cost; unknown remains unknown |
| Persistence | `src/devtools/persistence/` | same: 5 files | Conversation/model representations and tests | Do not make persistence own lifecycle/evidence semantics; durable compatibility audit remains |
| Repository/resource/snapshot/corpus | ADR-0002, `context/repository/` | base present; discovery/export changes | Python RI, source indexing, ContextTools; repository tests | Snapshot identity is not Git/index identity or physical deletion |
| RepositorySnapshotDelta | New-module22 Codex delivery | `repository/changes.py` feature-only | Only declaration and `tests/context/repository/test_changes.py` found by literal call search | No maintained operational consumer or incremental RI maintenance established |
| Python functions/classes/imports/modules/references | Native RI packages and typed evidence | most blobs same; qualified-reference/request assembly differ | Source units, structural retrievers, Localization; RI tests | Static supported scope only; no runtime importability/complete dynamic graph |
| Python project configuration | Configuration-obstructions21, dependency-groups24 | delta in settings/models/declarations | Role inputs and independent obstruction/dependency-group tests | Qualified unsupported/absence/version behavior needs selective integration |
| Lexical retrieval and composition | R1/R2/graph experiments retain original outcomes | lexical and composition blobs same | Source search and Localization lexical lanes; lexical tests | Experimental rank improvements/failures are not automatic policy adoption |
| Selectable file/symbol/window/mixed source search | Earlier maintained source-search delivery | 3 source package blobs same; search.py differs | ContextTools and source/Planning tests | Physical/logical-line proposal pair still needs semantic disposition |
| Caller-scoped source search | Codex fallback28, `a951957c75ba187b8ac8bb29ad2520750ebb3783` | new scope behavior not adopted | `tests/context/retrieval/source/test_scope.py`; original corpus evidence retained | Native search_source has no scoped argument yet; tests are not model adoption |
| Typed graph and repository-map ranking | Graph/map development experiments, existing Retrieval owners | same: 4 graph and 5 map files | Optional application navigation, graph/map tests | Incremental maintenance and comparative effectiveness remain separate |
| Context Planning/materialization/render/assembly | ADR-0004, existing plan/source/whole-resource APIs | base present; rendering/export deltas | Qwen prepared/source acquisition paths and Planning tests | No autonomous planner or universal sufficiency mechanism |
| Caller-selected map metadata and exact source | Codex26/27 Planning adapters; `0bdc8507601dcf65a742ab3ce5cca4bb8e6f590a` source adapter | `planning/repository_map.py` feature-only | `apps/qwen/navigation.py`, exact-range Planning regressions | Selective main adoption; metadata never edit authority |
| Localization roles/routing/grounding/resolution | ADR-0005 and retained case results | base present; 2 role files differ | Consumer APIs/tests; dependency-group role source delivered25 | Caller judgments/readiness are not automatic relevance or review approval |
| Evaluation frame | `src/devtools/evaluation/` | same: 2 files | Retained experimental consumers | Not a complete general evaluation platform |
| CodingCommands shared validation | Codex all-checks/check_changes publications | native `commands.py`/`change_checks.py` absent | Native model surface, source-bound reports, real Git/ToolRunner tests | is_current is freshness, not correctness or publication authority |
| Native Qwen observed editing/navigation | Feature worker 15 Python files vs main 8 | current extended surface not adopted | Native loop, deterministic tests and genuine receipts through 28 | Latest run19 calls, 4 admitted proposals, failed behavior/repair Context; no model map/check_changes use |
| Checkout/WorkCycle/intake/publication | Existing ordinary-branch integration lifecycle | `scripts/backlog/` 14 Python files feature-only | Native worker/local closeout; authored Git-fixture tests | Preserve authority/recovery boundaries; do not merge feature ancestry wholesale |
| Operator dashboard | Maintained app and historical browser/build evidence | feature-only Python application | Existing local UI/API/tests | Dependency findings from earlier audit are historical; current risk needs separate requalification |
| Test/documentation trees | Latest feature protected result 2663 passed/2 skipped, 100% recorded28 | test tree differs; main has its own destination evidence | Layout/validation owners and package tests | No full production gate rerun in this documentation-only audit |
| Historical experiments | Collection summaries/manifests and case records | All671 experimental Python blobs match | Experiments consume framework APIs; protected profile excludes tests/experiments | CLOSED may mean negative; INCOMPLETE/BLOCKED remain; preserve packets and scientific catalogs |

### What the comparison does and does not establish

The approved Commands integration is complete in the actual destination. Native
worker/Planning/configuration improvements are not thereby promoted. Identical
base graph, map, paths, time and usage source must not be described as missing
from main. Conversely, a same-named module or an older main worker does not
establish adoption of later behavior. Different blobs need hunk/contract review.
The matrix is an initial inventory, not a dependency-complete integration plan.
Learned Intelligence's other repository and scientific catalogs were not read,
merged, relabeled or used as a Devtools capability catalog.

## Initial observability gap map

| Boundary / source inspected | Existing factual capability | Observed limitation / research question |
|---|---|---|
| `observability/evidence/inspection.py`, `terminal.py` | Process-local attempts, terminal outcomes, optional EvidenceSink, attempt/evidence IDs | No durable store supplied by the inspector; map to B-0011, not an automatic storage project |
| `evidence/model_interaction.py`, model observation protocol | Explicit capture/omit/redact/unavailable states, immutable completed model Evidence, Tool schema/argument capture controls | Successful normalized responses only; failed realization/observer failure and Runtime-attempt association are not automatically accounted for |
| `evidence/invocation.py` | Measured values, independent usage categories, availability/provenance, EXECUTED versus ADOPTED | It is a typed record, not an automatic collector, causal trace, price table or invocation ledger service |
| `observability/usage/` and `scripts/usage.py` | Metadata-only ingestion, identity reconciliation, partial reports, UTC/calendar windows, empirical forecasts | No account-wide billing completeness; source provenance and missing data remain explicit |
| `resources/commands/events.py`, events documentation | Frozen started/stdout/stderr/exited values; bounded single-consumer event stream and drop counts | Best-effort stream may drop terminal events; no generic span ID/causal export implied. Command events are not automatically durable Tool evidence |
| `tools/execution.py` | Calls validate then execute exactly once, returns original failures/results | No observation/export interface in this class; Tool invocation correlation is application-specific |
| `apps/qwen/coding_loop.py`, `commands.py`, `change_checks.py` | Raw requests/responses, provider call IDs, timing, validation evidence, source/plan/Git hashes | Useful maintained app receipts, not a general framework Trace/Telemetry representation |
| `scripts/backlog/checkout.py`, integration modules | Exclusive ownership, recovery receipts, exact candidate/review/publication identities | No automatically shared cross-layer span hierarchy; execution authority remains separate from historical facts |
| `experiments/orchestration/`, worker measurement and journals | Stage/run-local receipts, lifecycle histories and InvocationMeasurement composition | Retained experiment timeline semantics are not a reusable generic execution lifecycle or evidence of new scientific authority |
| Maintained source and pyproject search | No shared logging/structured-event bus, OTel exporter or trace/span implementation discovered in scanned Python owners; no OTel dependency declared in pyproject | Bounded negative search, not a claim about third-party packages or every historical artifact. Need concrete shared-consumer requirements before promotion |

`Runtime` lives in `devtools.execution`, not a `devtools.runtime` package. The
model-neutral invocation protocol is `ModelInteraction`; provider launch belongs
to `models.serving`. Conversation and external `CodexAgent` are under `agents`.
There is no generic Agent planner/Run/Step framework to assume from these names.
Source import/constructor searches found inspector use in tests, usage record
construction in the usage adapter/orchestration worker, and Runtime calls in
three acceptance scripts. They do not establish automatic inspector adoption by
the native Qwen loop. Deep consumer/correlation coverage remains to be audited.

## Reuse and overlap candidates

1. Command events, terminal Evidence, model Evidence and app JSON receipts have
   different owners/guarantees. Their coexistence is not proof of duplication;
   investigate correlation and loss/capture semantics under B-0023.
2. Runtime and the coding loop are not interchangeable: one invocation versus
   application orchestration. Compare upstream harness loops before designing a
   reusable Agent lifecycle under B-0029/B-0031/B-0044.
3. `CommandTool` delegates managed Commands; CodingCommands adds fixed task
   scope/plans/evidence. Reuse execution, do not replace both with arbitrary shell
   pipelines merely because names overlap.
4. Multiple bounded `_save`/hash/serialization helpers are candidates for an
   ergonomics audit, not evidence that one universal state/persistence API is
   appropriate. Preserve domain schemas and current durable contracts.
5. The current worker's `context_tools.py` 39,019, `coding_loop.py` 71,938 and
   `development_task.py` 60,528 raw bytes exceed its 32,768-byte individual-source
   candidate/closeout limit. This is concrete task-feasibility pressure, not
   permission to weaken limits or split modules mechanically.

## Backlog crosswalk

The original supplied 18-item list is **unavailable**. The following is a separate
audit-derived mapping, not a reconstruction or complete deduplication of it.

| Audit pressure | Existing record / disposition | This checkpoint |
|---|---|---|
| Architecture/index/current-status reconciliation | B-0001/B-0006, existing ACTIVE documentation work | Update B-0006 evidence; retain IDs/status |
| Generic tracing/export/correlation | B-0023, DEFERRED; B-0011 durable Evidence, DEFERRED | Add source-backed gaps, no new duplicate Trace framework story |
| Model/Agent/provider/runtime boundaries | B-0029/B-0030/B-0031/B-0044/B-0045 | Retain existing boundary investigations; source comparison first |
| Tool/capability/authorization abstraction | B-0035/B-0036, governance siblings | Existing concerns, no new registry proposal |
| Persistence and representation | B-0027/B-0028 | Existing concerns; no generic store introduced |
| Framework acceptance and autonomous reliability | B-0015/B-0016/B-0009 | Existing test/actual-use distinctions retained |
| RI/Context/graph/localization | B-0002 and existing ADR-0002/3/4/5 | Inventory delivered subsets; do not close epic or reinterpret experiment outcomes |
| Environment, stdin, successful exits | Existing proposals `2c443f76-ad59-43c4-bb4c-c956ae7f5c28`, `796ac652-dbd7-488b-98bb-444f695bfa92`, `d9416198-66c7-40b9-b566-e2a8806a81b5` | Append ADVISORY main-delivery evidence; all remain PENDING_REVIEW |
| Physical source-span concerns | Existing `416658bd-8ab9-43c4-bbb3-98a18a88cd4d` and `5aa7a431-fd3c-4d46-a3a2-cb4e59e9c28e` | Potential duplicate pair; compare original contracts/invalid-oracle history before disposition, no merge |
| Memory/wiki/procedural skills/CodeGraph | Existing proposals `ae6b9374-f74d-4cd4-b079-a9f843ce3420`, `255498b8-4b09-4153-a819-56af0fa5bb36`, `14f19339-9213-443d-ac8c-b1018ae1f5bc`, `ae03cda7-955e-40c6-a131-9e2ba209c9a6` | Already discoverable; no implementation/promotion based on external popularity |
| Worker source granularity/admission | [Pending proposal](../backlog/proposals/39c6663a-bab7-43ed-8166-82e780a75d05/proposal.json), parent B-0003 | New bounded investigation with advisory duplicate check; no source refactor |
| Ignored evidence custody/cleanup/recovery | [Pending proposal](../backlog/proposals/0385a359-399f-40bb-aed4-caf5239c9fc8/proposal.json), parent unassigned | New operational investigation; dependencies are possible relations, no deletion authority |

The initial queue had 14 proposals: 13 pending and one approved. Intake readers
validated existing hash chains without errors. Two new captures are pending;
three existing proposal reviews are advisory only. No B-number, parent status,
approval, promotion or execution grant changes. Automated duplicate search found
no match for the new captures; that incomplete lexical aid is not semantic proof.

## Checkpoint validation

The existing root-layout check passed. The existing layout and backlog-intake
tests passed 36 cases in 1.56 seconds using the focused no-cov profile. The bounded
documentation check validated 41 newly introduced local links/anchors and 9 JSON
documents, canonical backlog table/body preservation, unchanged existing proposal
dispositions and all intake hash chains. Original forensic fingerprints match
their earlier preservation record. Historical reconciliation/research substantive
bodies and all production source/tests/apps/scripts/experiments remain unchanged.

These are documentation/administration checks, not new scientific outcomes or a
fresh protected-production gate. The previously recorded 2663-test/100% feature
gate is historical supporting evidence only; it was not rerun for this checkpoint.
The dated metadata record retains the check commands/results and exact changed
documentation/intake paths. Git whitespace validation passed.

## Remaining audit scope

- Obtain/verify the actual starter ZIP and reconcile its exact18 items.
- Complete [pinned Qwen Code/Pydantic AI mechanism research](agent-harness-mechanism-review.md),
  then DeepSeek Harness/Aider, including dependencies and failure-path tests.
- Extend this presence/delta matrix to capability-level source/test/dependency
  contracts on the actual destination; no full feature-ancestry merge.
- Audit inspector adoption, failed invocation accounting, task/Tool/Command
  correlation, privacy, cancellation and exporter needs with concrete consumers.
- Reconcile stale current-looking research/index statements (for example R2
  described as next in an earlier research checkpoint versus completed later
  roadmap results). Preserve historical bodies and accepted semantics.
- Complete custody/recovery and developer-ergonomics review before selecting
  improvements; prepare the comprehensive fresh-session handoff only after those
  findings are sufficiently reconciled. This initial checkpoint is not that final
  architecture audit or a new Qwen benchmark.

## Subsequent original-input and mechanism checkpoint (2026-10-23)

The missing-input/crosswalk and next-research statements above describe this
initial audit at `3c09641d`, not current unavailability. The [verified transfer and
exact18 reconciliation](reconciliation-input-reconciliation.md) now preserve the
original assistant drafts and independent review with their full provenance.
The [Qwen Code/Pydantic AI source-and-test comparison](agent-harness-mechanism-review.md#source-and-test-comparison-2026-10-23)
deepens actual owner/correlation/failure-path findings against `3b2b3de8` source,
unchanged from the initial production inventory. No main/feature source adoption,
prior experimental result or cleanup disposition changes. The full architecture
audit remains unfinished; DeepSeek/Aider and deeper real-trajectory joins follow.

## Four-project follow-up (2026-10-23)

The [DeepSeek Harness/Aider audit](agent-harness-mechanism-review.md#deepseek-harness-and-aider-source-and-test-audit-2026-10-23)
now completes the selected external mechanism comparisons. It distinguishes
in-memory commit, backend durability, live instrumentation and immutable Evidence,
and compares Aider's host edit/map mechanics with existing source-bound owners.
The [five-flow local audit plan](development-lifecycle-audit-plan.md) selects
actual original receipts and correlation fields. Source/test trees, adoption
matrix and historical experiments are unchanged; no new production integration
or cleanup is inferred. Complete those local joins and exact destination/custody
checks before declaring reconciliation complete.

## Executed lifecycle follow-up (2026-10-23)

The [five-flow observability audit](development-lifecycle-observability-audit.md)
now examines actual original requests, provider/Tool IDs, source/candidate/check
identities, review subjects, commits and recovery seals. Existing typed Evidence
and usage are not universally installed consumers; native application receipts
provide separate strong links. Historical navigation refusal and Git-versus-
physical newline identity are explicitly qualified. This adds no production
adoption or cleanup result to the matrix above. The next bounded phase is actual
destination capability dependencies, feature/experiment ownership and custody
eligibility before successor handoff.

## Final production reconciliation checkpoint (2026-10-23)

The [complete production/experiment/cohesion reconciliation](production-adoption-and-architecture-reconciliation.md)
extends this initial presence/delta inventory at feature
`8d70ba9fc4f0d9bb45c1f8528e212ecf9c601e6b` against authenticated remote main
`5d979920d0728775ed529457c88f5b68b440c64f`. The earlier missing-input and
"next research" paragraphs above retain their historical checkpoint meaning.
Original18 intake, four-project source/test research and five-flow lifecycle
audit are now complete bounded evidence, not pending external research.

The [companion source/custody manifest](production-adoption-and-architecture-evidence-20261023.json)
covers all 250 framework Python files in 48 overlapping semantic slices and
513 selected source/test file identities.218 framework blobs match main;
28 differ and four are new. Commands' nine source files match main. Preserve
main-only `tests/resources/commands/test_composition.py` and
`docs/development/commands-integration.md` in future main-derived integrations.

All 35 collections retain24 CLOSED/nine INCOMPLETE/two BLOCKED statuses; the new
report records each outcome, maintained relationship or explicit UNKNOWN link,
consumer/main state and remaining obligation. CLOSED is not positive science.
Case 0015 R2 and Case 0016 GRAPH-3 are COMPLETE/HARMFUL under their frozen rules;
do not revive older future-tense roadmap statements. Later Qwen evaluations are
application receipts, not new top-level collections.

Eight bounded integration groups separate G1-G5 destination-review candidates
from G6's missing consumer and G7/G8 authority/reliability/privacy blockers.
Static dependency closure is an upper bound including public initializers and
deferred imports, never a copy list. No destination validation was executed.
SnapshotDelta, optional Evidence inspector composition and a complete native
Localization witness consumer remain unintegrated. Internal primitive consumers
are explicitly distinguished from an autonomous agent adopting the whole API.

The report qualifies actual large-module responsibilities, two-consumer Tool
definition/receipt ergonomics and exact-path custody rather than refactoring.
The bounded [protected-validation reuse investigation](../backlog/proposals/d58697fd-bb03-4e98-bdac-fa29444fc6ff/proposal.json)
is PENDING_REVIEW under B-0047; it claims no historical validation bypass.
The next checkpoint is comprehensive successor-session handoff. No new research
program, inference, implementation, cleanup or protected adoption starts here.

## Deeper code-review checkpoint (2026-10-23)

This initial inventory is not a complete implementation review. The maintainer's
[comprehensive audit](comprehensive-code-audit.md) now records all reachable ref
trees and intermediate/deleted path/blob versions. The [RI domain report](repository-intelligence-code-audit.md)
inspects current substantive algorithms and real native consumers; its
[ledger](code-audit/README.md) explicitly leaves unreviewed historical versions,
fixtures and experiment controllers visible. Production adoption, test coverage,
API exposure and model use remain separate claims. The final successor-session
dossier is postponed.
