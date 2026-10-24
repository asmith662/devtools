# Development lifecycle and observability audit

## Disposition and executive findings

Source-and-historical-evidence audit, 2026-10-23, against
`fa6e90afee6c76846afac5dbe1b8a84b187da8cf` on `feat/qwen-context-worker`.
Remote feature matched that commit at entry; remote main remained
`5d979920d0728775ed529457c88f5b68b440c64f`. The
[reconciliation charter](../development/reconciliation.md) governs this research;
taxonomy, accepted ADRs and package contracts retain semantic authority. This
report implements no instrumentation, execution authority or production feature.

The [five-flow plan](development-lifecycle-audit-plan.md) has now been executed
as an audit, without replay. Its 21 original inputs all match recorded SHA-256
and byte lengths. Additional original requests, normalized/raw responses, stages,
Tool receipts, protected logs and Git objects were inspected. The
[audit metadata](development-lifecycle-observability-evidence-20261023.json)
catalogues 297 existing files, 56 historical request stages, two closeouts and
current local owner identities. It contains metadata/derived observations, not
copied source bodies, model arguments, prompts, logs or sensitive raw receipts.

Findings, in priority order:

1. **Strong existing integrity islands:** native request/response hashes and
   provider Tool IDs, exact source admission, source/plan/Git-bound checks,
   candidate/review-subject binding and Checkout seals work together. All recorded
   request/response digest links checked here match; returned Tool IDs remain in
   the next retained native request wherever one exists. Existing records are
   useful; a new generic event bus is not the prerequisite.
2. **Incomplete occurrence accounting:** completed normalized model Evidence is
   optional and not installed by the ordinary Qwen entry point. Provider failures
   before normalization and observer failures afterward have different effects
   but no common complete realization record. Native application receipts are
   not automatically ModelInteraction/Runtime Evidence or InvocationMeasurement.
3. **Weak publication/recovery observation edges:** closeout binds result,
   candidate and review, but lacks a post-push observed ref/time field; standalone
   host freshness results lack the checked report digest/time. Recovery26 records
   the assertion that the process was stopped without a linked process-stop
   observation. These are evidence gaps, not proof the operations were unsafe.
4. **Two research precision corrections:** Map-source27 turn06's genuine
   `expand_source` call was **REFUSED**, not a successful source disclosure.
   Two Codex27 recorded file hashes describe CRLF worktree bytes while committed
   Git blobs contain LF. Both facts are demonstrable; neither original receipt
   is rewritten or relabelled.
5. **Recommendation A first:** improve joins, failure population and consumers
   over current domain records. Specify contracts under B-0023/B-0011 before
   deciding whether a narrow operational observation interface or OTel spans add
   value. No library, logger, decorator, base class or trace schema is selected.

## Method, evidence keys and clocks

`E001` etc below resolve to **exact original path, full physical SHA-256 and byte
length** in `evidence[]` in the audit metadata. Each stage references its request,
response, Tool receipt and raw provider sidecar when present. Fields omitted from
the public derivative remain in original custody. Source versions, task/oracle,
candidate and plan identities are preserved in the corresponding flow/closeout
objects. IDs are audit-local labels, not new execution identities.

Association strengths:

- **D â€” direct authenticated reference:** an original digest, native call ID,
  review subject or Git object link matches independently inspected bytes.
- **R â€” deterministic derivation:** rehashing, byte comparison or a verified
  schema calculation; no execution/replay is needed.
- **C â€” chronological/contextual association:** co-location, filenames, wall-clock
  order or a producer's assertion without an authenticated causal reference.
- **U â€” unknown/not captured/not applicable:** named explicitly, never a fabricated
  event or automatic failure/success.

Persisted `Timestamp` strings are UTC wall-clock observations, not causal clocks.
Stage `started_monotonic`/elapsed/model/check seconds use process-local performance
counters and cannot be joined across processes. Git author/committer dates retain
their `-04:00` offset; provider `created` is an independent epoch value, not a
trusted host dispatch timestamp. Stage times bracket model, Tool and validation
work rather than timestamping each internal action. `closeout.at` is record
construction time, not commit/push completion. Overwritten stage/closeout/progress
files are latest checkpoints, not an append-only event stream. Checksums establish
retained-byte consistency; they are not signatures, wall-clock attestation or
proof of external effects.

## Existing observability owners and real consumers

| Responsibility | Maintained producer â†’ consumer / evidence | Actual guarantee and limit |
| --- | --- | --- |
| Terminal Evidence | `execution/runtime.py` â†’ InteractionAttemptObserver â†’ `observability/evidence/inspection.py` â†’ optional EvidenceSink; `tests/execution/test_runtime.py` | Optional specialized attempt with Conversation/Message/source, terminal stage/outcome/time. Inspector retains process-local records and synchronously calls sink. Runtime contains finish-observer/terminalization failures to preserve primary result/error. No inspector means no attempt. This path is not invoked by the audited native loop. |
| Model Evidence | `models/interaction/providers/llama_cpp.py:send` â†’ optional ModelInteractionObserver â†’ `evidence/model_interaction.py`; provider/Evidence tests | Fresh ModelInteractionId and completed normalized observation, capture manifest, provider exchange and reported usage. Completion callback occurs after response normalization and before return; it may itself raise. Inspector is process-local and defaults payload categories to OMIT. No common failed invocation callback or automatic Runtime-attempt join. |
| Invocation/usage | `evidence/invocation.py`, `usage/{ingestion,collection,storage,report}.py`; `experiments/orchestration/workers/measurement.py`, `scripts/usage.py` | Existing real external-Codex measurement consumer and usage-ledger CLI. Availability/provenance and EXECUTED/ADOPTED prevent convenient zero/double-counting. Usage storage has a local writer lease and metadata snapshot, not a general Evidence writer. Native Qwen's usage dictionaries do not instantiate this projection automatically. |
| Live Command events | `resources/commands/execution.py` â†’ `handle.py:events` caller; Commands tests | Started/stdout/stderr/exited immutable values, bounded single consumer and drop count. No privileged terminal event, shared invocation ID or durable sink. Timeout/cancellation kills/reaps the immediate child and closes stream; it does not undo external effects or guarantee descendant cleanup. |
| Tool boundary | `tools/execution.py`, `tools/command.py` â†’ supplied Tool/CommandExecutor; `tests/tools/test_execution.py` | Validate then execute once; original typed result/errors/cancellation propagate. No retry, durable call journal, common invocation occurrence/span or permission engine. Caller/application owns exposure, IDs and authorization. |
| Native model/Tool receipts | `apps/qwen/coding_loop.py`, ContextTools and CodingCommands â†’ request/response/stage/tools JSON and next Prompt messages | Actual raw provider captures exist in these selected runs through their wrapper, alongside normalized responses. Source/version/absence references and provider Tool IDs correlate local activity. This is bounded application evidence, not universal provider capture or a taxonomy-wide Run/Step implementation. |
| Candidate validation | `commands.py`, `change_checks.py` â†’ fixed managed checks â†’ full evidence journal and bounded model report | Reused all-checks, source/plan/Git before/after, authenticated receipt hashes, independent statuses, interrupted/incomplete journals. Freshness and pass/fail are separate. Reports confer review eligibility only. |
| Source ownership/recovery | `scripts/backlog/checkout.py` â†’ owner/sealed history; `test_checkout.py` | One canonical source owner, recorded PID/root/branch/base/allowed fingerprints; refuses unknown bytes and explicit stopped-owner recovery is required. Finish/restoration is not rollback of arbitrary subprocess or Git/server effects. |
| Review/publication | `integration/local.py`, `integration/{validation,git}.py`, `work.py` â†’ exact review, protected logs, intent/commit/publication receipts | Trusted feature authority stays separate from model acceptance; protected promotion excluded. Commit-intent reconciliation checks actual parent/tree/trailer; publication queries the exact ref and rejects divergent state. Latest receipts are not a complete immutable transition log. |
| Durable Conversation | `persistence/{json,sqlite,_snapshot}.py` â†’ `agents.conversation`; persistence docs/tests | Stores Conversation identity/history/opaque continuation references. It does not store native worker source observations, ownership lease, Evidence ledger or arbitrary working-state effects. Reload is not resume/exactly-once execution authority. |

The scanned maintained application/entry-point sources do not instantiate
ModelInteractionInspector or ExecutionInspector for these native runs. The
ordinary `scripts/qwen/coding_worker.py:local_interaction` constructs the provider
without an observer; `coding_loop` calls the selected interaction directly.
Raw provider sidecars in these historical runs came from run-specific capture
composition. Exported optional types therefore cannot be treated as universal
adoption. Source hashes and Git blobs for inspected owners/tests are in metadata.

## Cross-component join and authority matrix

| Edge | Existing keys / inspected consumer | Strength and missing contract |
| --- | --- | --- |
| Objective â†’ CodingTask â†’ native result | definition/oracle hashes, baseline/source/check scope; `tasks.py`, loop result | D for exact serialized task hash references; human objective-to-selected-contract interpretation remains qualified. No B-number is required for every local trusted task. |
| Request â†’ normalized response â†’ native Tool | stage file hashes; normalized provider_call_id; raw sidecar call IDs; next Prompt tool_call_id | D/R for 56 checked stage pairs and retained next-result links; request hash is not an occurrence ID. Identical input can recur. A provider exception can leave only DISPATCH_ATTEMPTED. |
| Provider occurrence â†’ Runtime/Model Evidence | ModelInteractionId versus InteractionAttemptId/EvidenceId | U in these native paths: Runtime/inspectors not composed. They must not be inferred from task/turn IDs or invented retrospectively. |
| Tool â†’ exact observation â†’ edit | observation_call_id, unit/parent/span/content version, edit_ref, proposal call IDs, common pre-transaction source hashes | D where disclosed/admitted. Map metadata, failed expansion and a call receipt alone confer no edit authority. Source stale/refusal path is distinct from application failure. |
| Edit â†’ candidate â†’ independent validation | source before/after, proposed/captured candidate hashes, per-check outcomes | D/R for admitted captures and validation records; failed installation26 stops before candidate validation. Passing existing regressions did not satisfy failed independent oracle22. |
| Shared checks â†’ report â†’ currentness | source/plan/Git state, receipt/bundle hash and stored report | D/R for report/journal/bundle27 equality. Saved host `is_current` booleans omit input-report reference and time; association with that report is C, not an independently sealed invocation record. No fresh check was executed here. |
| Accepted result â†’ review â†’ commit | result SHA, files hash list, review_subject and commit trailers/tree | D/R for both inspected closeouts. Git LF/physical CRLF distinction affects two27 file hashes; normalized byte relation is recorded, not silently substituted for exact equality. |
| Commit â†’ remote publication | expected remote, committed hash, FEATURE_PUBLISHED; `integration/git.py:publish` | Local object/trailer D; receipt's successful push assertion supported by source policy, but historical post-push ref/time not independently recorded in closeout. Current feature ancestry is supporting evidence, not historical remote timestamp proof. |
| Source mismatch â†’ stopped owner â†’ restoration | actual/admitted byte hashes, recovery assertion, sealed owner-history operation/PID/base/final HEAD | D/R for byte mismatch and final seal. Stop confirmation lacks a linked process-state/time receipt here (C/U). Restoration proves scoped source return, not side-effect reversal. |

## Lost, interrupted and uncertain outcomes

| Boundary / source and deterministic test evidence | Currently observable, correlated and retained? | Recovery / uncertainty |
| --- | --- | --- |
| Provider transport/framing/normalization failure: `llama_cpp.py`, provider error tests | Native request/stage saved before send; complete model Evidence only after normalization. Response/usage may be absent. Runtime observer tests record provider-stage failure only when that path is composed. | No retry after unknown native completion. Missing normalized response does not prove no inference or zero usage. |
| Response succeeds then completion observer raises: provider send control flow; Runtime finish-failure tests cover a different boundary | Provider callback can convert a completed normalization into raised send; generic completion inspector has no failure counterpart. Dedicated provider post-success observer-failure assertion was not found in inspected tests. | Preserve provider versus observer outcome separately; do not attribute every send exception to model failure. Proposed test/consumer work, not a current measured historical incident. |
| Invalid/refused Tool input: ToolRunner tests;22 turns04/06/08/10 | Validation error or explicit refusal remains correlated to native call; no source mutation admitted. Earlier valid siblings do not apply in an invalid atomic transaction. | Model must correct arguments; current component diagnostics postdate22. Historical generic refusal must not be embellished retroactively. |
| Partial Tool batches: `coding_loop.py`; batch-preservation and later-failure worker tests | Completed prior results can remain even if a later Tool raises; native IDs preserve what returned. Loop/source cleanup does not erase other completed effects. | Cancellation is not transaction rollback for arbitrary Tools. A missing later result is not proof it never started. |
| Command timeout/cancel/missing executable: executor/handle tests | Exceptions and finally-closing events, immediate child kill/reap; no universal terminal CommandResult on exceptional path. Event payloads lack common execution ID/time. | Known process cleanup scope only. No process-group/network/file side-effect rollback inferred. |
| Event loss: `handle.py`; `test_execution` max_pending_events=1 assertion | Test observes four dropped events and no CommandExited while result/output remain available. Drop count is not identities of lost events. | Consume final result/exception too; do not use event absence as effect absence or durable terminal truth. |
| Validation cancellation/evidence-write failure: `commands.py`, `change_checks.py`; cancellation/tamper tests | Journals preserve interrupted current check and NOT_RUN siblings when writes succeed. Cancellation propagates; failed evidence write adds a note or propagates and can leave incomplete state. Final after-state acquisition can also fail. | Fail closed. No complete-success interpretation of absent/interrupted journals. Existing tests are deterministic infrastructure evidence, not live model behavior. |
| Stale/tampered reports: check tests and27 saved host receipts | Report hash/provenance, underlying bundle and current source/Git/plan are rechecked. A current failed report stays FAIL; restoration makes old candidate evidence stale. | No automatic validation rerun in is_current; WorkCycle reauthenticates independently. |
| Unknown source bytes:26; Checkout unknown-effects tests | Owner survives source mismatch; actual bytes and original failed result retained; separate recovery seal. | Explicit host reconciliation only, no deletion of lease/blind redispatch. Stop observation remains incompletely correlated. |
| Ambiguous commit/push: local closeout test lost commit response; integration Git source | COMMIT_INTENT tree/parent/trailer reconciles an already-created commit. Remote exact-ref query separates absence from communication failure. Receipt after publish records disposition, not observed remote ref/time. | Query/reconcile, do not blindly recommit/retry external effects. Current source uses compare-and-swap publication; this audit neither executes it nor grants force/promotion authority. |
| Missing usage/cost: ModelUsage/InvocationMeasurement/usage tests; native stages | Reported categories present per completed response; cache/reasoning values may remain null. Overlapping totals not summed as new categories. Ledger reconciliation handles adopted/duplicate/conflicting observations separately. | Failed/missing response usage, active supervisor time, GPU energy and account billing remain unknown; no zero substitution or cost estimate here. |

## Reuse, fragmentation and options

Source/edit/check authority is cohesive inside the application and source
ownership is cohesive inside Checkout/WorkCycle. Observation is fragmented across
native dictionaries, typed optional Evidence, bounded Command streams and
administrative receipts. This is not necessarily duplicate ownership: the facts,
capture policies and failure populations differ. RepositoryId/snapshot/content/
declaration identities describe knowledge/source applicability; task/turn/call/
review/commit identities describe execution or administrative facts. Equal-looking
hashes do not make them interchangeable.

Concrete serialization repetition exists: `development_task._save` writes sorted
JSON with a newline; `WorkCycle._save` adds a canonical `_digest` seal; integration
progress uses its own checkpoint JSON; check reports use file hashes and a
bounded `_view`. Usage storage has a separate versioned metadata schema/writer.
Those have different durable/current contracts. A shared serializer or base class
cannot be justified merely by repeated `json.dumps`. Likewise native `print`
progress and protected-validation progress are operational channels, not duplicate
Evidence logs. Inspect compatibility before consolidating.

| Option | Reuse / new responsibility | Tradeoffs and present recommendation |
| --- | --- | --- |
| **A. Existing records with explicit adapters/joins** | Reuse Model/terminal Evidence when actually observed, InvocationMeasurement availability, native Tool/source/check receipts and WorkCycle review/commit records. A consumer would identify direct/derived/unknown edges and distinguish realization from observer outcomes. | Least authority/dependency change; immediately useful for native-worker debugging and independent closeout audit. Cannot invent past IDs or express all Tool outcomes as model Evidence. Requires capture policy and schema compatibility decisions before a production writer. **Recommended first bounded design/implementation candidate after backlog selection.** |
| **B. Narrow operational tracing interface** | Common optional occurrence/parent/cause metadata and emission contract over existing domains, not a replacement executor or durable truth. | Could reduce repeated correlation glue in at least native-loop and WorkCycle consumers; needs decisions on task/turn versus invocation identity, async context, observer failure, cancellation, privacy, drop behavior and public compatibility. New cross-domain ownership requires architectural review under B-0023; not yet selected. |
| **C. OTel operational spans** | Reuse established span/export concepts for operational timing, retain Devtools Evidence/source/review records as authoritative facts. | Existing ecosystem/export tools avoid inventing a tracer, but add dependency, deployment, sampling/context propagation and egress obligations. Spans can drop and exporter success does not prove durable evidence or authorization. No current exporter or measured multi-consumer requirement justifies installation now. Evaluate after A defines joins/privacy/failure semantics. |

Minimum missing contract is an **observed occurrence with explicit boundary,
outcome availability and authenticated links**, not a universal success enum or
one UUID for every domain. Model-normalization success, observer failure, Tool
refusal, check failure/currentness and publication are distinct outcomes. Any
future adapter must preserve primary exceptions, record secondary observation
failure separately, never cause a side-effect retry, and keep unknown usage.

Developer-experience opportunities have realistic call sites: model send/capture
in the native entry point, Tool dispatch in ContextTools/CodingCommands, fixed
check journaling, and WorkCycle validation/publication transitions. A transparent
observation helper might reduce repeated begin/end/error/finally bookkeeping
there. A typed Tool-definition helper might reduce descriptor/argument drift in
ContextTools and CodingCommands. No decorator is recommended until ordering,
sync/async cancellation, identity, return/exception preservation and domain
authorization remain equivalent. Large module size alone proves neither need.

## Priority gap and backlog crosswalk

Priority is audit recommendation, not scheduling/grant/status change. Maintenance
agent suitability means a possible later bounded assignment after authorization.

| Priority / observed deficiency | Evidence / owner and consequence | Existing intake / suggested bounded work | Architecture decision? Maintenance-agent suitability / confidence |
| --- | --- | --- | --- |
| P1: incomplete provider/observer realization accounting | Provider send and native pre-dispatch stage; failed or post-response observation can lose response/usage or be misclassified | B-0023/B-0011/B-0046: qualify success, transport/normalization failure and observer failure projections across native loop and external-worker measurement | New reusable outcome semantics need review; adapter/test work can stay bounded. Suitable with fixed negative cases; high source confidence, no historical observer-failure incident claimed. |
| P1: no durable cross-boundary consumer | Selected flows join hashes manually; Runtime/Model IDs not on native path; ToolRunner no occurrence record | B-0023/B-0011: read-only existing-record adapter/consumer before a tracing interface; preserve source/review authority | Consumer can be local first; common cross-domain identity needs decision. Report-only agent suitable; high confidence. |
| P1: exact-tree reuse/evidence boundary not fully explicit | Closeout subject binds result/base/files; prior protected result reuse condition checks subject/passed, not a separately recorded complete plan/config/toolchain digest | B-0011/B-0028/B-0023: qualify exact-tree/input closure and replay-safe gate reuse, with changed runner/config/dependency negative tests | No demonstrated bypass or invalid historic gate asserted; baseline/task/Checkout protections also apply. Bounded maintenance investigation first; medium risk confidence. |
| P2: stored Git versus physical byte identity ambiguity | Codex27 source.py and representation.py physical CRLF hash versus LF Git blob | B-0027/B-0011 and pending module/maintenance investigation: document/test separate stored/worktree identities in closeout | Existing ownership; no automatic newline rewriting. Suitable bounded maintenance; high, exact transformed hash equality verified. |
| P2: freshness invocation lacks recorded input/time | Host-current-installed/restored27 contain no report digest or timestamps | B-0023/B-0011: bind host authentication receipt to supplied report/candidate and occurrence | No new authority; compatible metadata design still needed. Suitable maintenance task; high gap confidence, historical association only C. |
| P2: recovery stop confirmation weakly linked |26 recovery note and owner PID/seal without linked stop observation | B-0034/B-0028: investigate explicit stopped-owner observation and decision receipt | Do not alter takeover rules or invent proof. Report-only audit suitable; high bounded evidence gap, not proof stop was skipped. |
| P2: remote completion weakly recorded | Both closeouts FEATURE_PUBLISHED without post-push ref/time field | B-0023/B-0034: retain observed destination/ref/time and ambiguous outcome distinctly | Existing Git owner; no new Git authority. Suitable metadata/test maintenance; high source/schema confidence. |
| P2: capture policy not propagated across raw app receipts | Evidence defaults OMIT while selected run wrappers retain raw requests/arguments/output; no universal capture manifest for these folders | B-0018/B-0011: document actual per-artifact capture/custody and redaction/export boundary | Cross-domain policy propagation needs decision. Report-only classification suitable; no sensitive-data leak alleged. |
| P2: lossy live Command stream lacks reusable join metadata | Command handle/result and event-drop tests; no per-event invocation/time | B-0023: define operational correlation consumer and loss semantics before span fields | Metadata semantics need design; no new event bus. Medium priority, high inspected behavior confidence. |
| P3: research summaries can overstate Tool use | Fifth selected flow's expand_source was REFUSED; exact original preserved | Existing documentation/maintenance proposal `39c6663a-bab7-43ed-8166-82e780a75d05`, B-0006: add receipt-grounded status qualification to future report reviews | No architecture decision. Report-only maintenance agent suitable; high confidence, correction below. |

Existing editing proposal `88246171-d102-4b62-93d7-03c1e19f8a7b` receives advisory
evidence separating refused arguments, accepted transactions, application mismatch
and failed behavior. Existing custody proposal `0385a359-399f-40bb-aed4-caf5239c9fc8`
retains original receipt/log preservation requirements; Memory proposal
`ae6b9374-f74d-4cd4-b079-a9f843ce3420` must not equate Conversation storage with
native working-state durability. No distinct new proposal is necessary; canonical
items already own the pressures. All reviews are ADVISORY; no IDs, approvals,
parents, statuses, grants or B-numbers change.

## Remaining uncertainty and next audit

Historical records are locally retained assertions plus checked byte/Git links,
not signed independent attestations. The five flows do not establish complete
population accounting, power-loss durability, full platform/descendant cleanup,
collector delivery, billing, or model reliability. No process-stop proof, missing
response, usage or original event was regenerated. The two recorded protected
log sets were authenticated, not rerun; current production source/tests did not
change. Exact raw payloads stay in their existing custody locations.

Next perform selective protected-main capability-adoption and actual
experiment/feature ownership reconciliation against the real destination tree,
then exact-path artifact-custody/cleanup eligibility review and the comprehensive
successor-session handoff. No merge, deletion, further model trial or observability
implementation follows from this report. The timelines below preserve model,
host and supervisory stages separately.

## Timeline 1 — Environment13 Qwen implementation and publication

Task definition `0d666866d8de9168ad359dd0bf35beb1bbe484b09e984a7e17ad6061f31629ea`; oracle `45eb26612a58f60f33449729bcd8b2b832cf374b8c28321684e20da3581c3309`. Result `E002` (`.local/qwen-coding-worker/environment-13/devtools-environment/result.json`; SHA-256 `c1630cc4df16533c96e9bc84400d008dc81fe8e10c6b7f09828ca53d78c3de7f`).

All rows: native loop produces the request/stage and consumes the provider response; ContextTools/edit admission consumes native calls, then the next model request consumes correlated results/feedback. D identifies checked file/call links; R identifies byte-derived source/check facts. Individual call IDs, source before/after hashes, check timestamps/outcomes and every referenced digest remain in the metadata flow rows.

| UTC stage interval | Exact evidence references | Model → host transition / observed outcome | Strength, omissions and authority |
| --- | --- | --- | --- |
| 2026-10-21T16:56:08.626478+00:00 → 2026-10-21T16:56:29.200371+00:00 | `E022`, `E023`, `E024`, `E025`, `E003` | Turn1: inspect_source. CONTEXT_RETURNED | D/R for recorded links; C for wall-clock order. No edit authority from metadata/call alone. No per-call wall timestamp inferred. |
| 2026-10-21T16:56:29.274895+00:00 → 2026-10-21T16:56:38.050870+00:00 | `E026`, `E027`, `E028`, `E030`, `E029` | Turn2: inspect_source. CONTEXT_RETURNED | D/R for recorded links; C for wall-clock order. No edit authority from metadata/call alone. No per-call wall timestamp inferred. |
| 2026-10-21T16:56:38.098165+00:00 → 2026-10-21T16:56:45.047638+00:00 | `E031`, `E032`, `E033`, `E035`, `E034` | Turn3: inspect_source. CONTEXT_RETURNED | D/R for recorded links; C for wall-clock order. No edit authority from metadata/call alone. No per-call wall timestamp inferred. |
| 2026-10-21T16:56:45.129561+00:00 → 2026-10-21T16:56:55.873128+00:00 | `E036`, `E037`, `E038`, `E040`, `E039` | Turn4: search_source, inspect_source. CONTEXT_RETURNED | D/R for recorded links; C for wall-clock order. No edit authority from metadata/call alone. No per-call wall timestamp inferred. |
| 2026-10-21T16:56:55.940633+00:00 → 2026-10-21T16:57:01.284575+00:00 | `E041`, `E042`, `E043`, `E045`, `E044` | Turn5: search_source. CONTEXT_RETURNED | D/R for recorded links; C for wall-clock order. No edit authority from metadata/call alone. No per-call wall timestamp inferred. |
| 2026-10-21T16:57:01.361310+00:00 → 2026-10-21T16:58:19.406136+00:00 | `E046`, `E047`, `E048`, `E050`, `E049` | Turn6: inspect_source. CONTEXT_RETURNED | D/R for recorded links; C for wall-clock order. No edit authority from metadata/call alone. No per-call wall timestamp inferred. |
| 2026-10-21T16:58:19.554515+00:00 → 2026-10-21T16:58:54.717234+00:00 | `E051`, `E052`, `E053`, `E055`, `E054` | Turn7: replace_source. TESTS_FAILED / TESTS_FAILED; checks format:1, oracle:1, ruff:1, tests:0, typing:0 | D/R for recorded links; C for wall-clock order. Admitted proposal; validation/publication remain separate. No per-call wall timestamp inferred. |
| 2026-10-21T16:58:54.862281+00:00 → 2026-10-21T16:59:25.064755+00:00 | `E056`, `E057`, `E058`, `E060`, `E059` | Turn8: inspect_source. CONTEXT_RETURNED | D/R for recorded links; C for wall-clock order. No edit authority from metadata/call alone. No per-call wall timestamp inferred. |
| 2026-10-21T16:59:25.162834+00:00 → 2026-10-21T16:59:56.599964+00:00 | `E061`, `E062`, `E063`, `E065`, `E064` | Turn9: inspect_source. CONTEXT_RETURNED | D/R for recorded links; C for wall-clock order. No edit authority from metadata/call alone. No per-call wall timestamp inferred. |
| 2026-10-21T16:59:56.682296+00:00 → 2026-10-21T17:00:10.669112+00:00 | `E066`, `E067`, `E068`, `E070`, `E069` | Turn10: replace_source. TESTS_FAILED / TESTS_FAILED; checks format:0, oracle:1, ruff:1, tests:0, typing:0 | D/R for recorded links; C for wall-clock order. Admitted proposal; validation/publication remain separate. No per-call wall timestamp inferred. |
| 2026-10-21T17:00:11.042773+00:00 → 2026-10-21T17:00:39.867585+00:00 | `E071`, `E072`, `E073`, `E075`, `E074` | Turn11: inspect_source. CONTEXT_RETURNED | D/R for recorded links; C for wall-clock order. No edit authority from metadata/call alone. No per-call wall timestamp inferred. |
| 2026-10-21T17:00:40.036543+00:00 → 2026-10-21T17:01:18.695857+00:00 | `E076`, `E077`, `E078`, `E080`, `E079` | Turn12: replace_source. TESTS_FAILED / TESTS_FAILED; checks format:0, oracle:1, ruff:0, tests:0, typing:0 | D/R for recorded links; C for wall-clock order. Admitted proposal; validation/publication remain separate. No per-call wall timestamp inferred. |
| 2026-10-21T17:01:19.230998+00:00 → 2026-10-21T17:02:20.071327+00:00 | `E081`, `E082`, `E083`, `E085`, `E084` | Turn13: replace_source. TESTS_FAILED / TESTS_FAILED; checks format:0, oracle:1, ruff:1, tests:0, typing:0 | D/R for recorded links; C for wall-clock order. Admitted proposal; validation/publication remain separate. No per-call wall timestamp inferred. |
| 2026-10-21T17:02:20.598153+00:00 → 2026-10-21T17:03:33.256451+00:00 | `E086`, `E087`, `E088`, `E090`, `E089` | Turn14: replace_source. ACCEPTED / ACCEPTED; checks format:0, oracle:0, ruff:0, tests:0, typing:0 | D/R for recorded links; C for wall-clock order. Admitted proposal; validation/publication remain separate. No per-call wall timestamp inferred. |

Turns07/10/12/13 fail independent behavior (oracle exit1) while existing tests and typing pass; quality outcomes vary. Turn14 passes all five checks. This is model-authored completion with real feedback corrections, not four successful child-overlay algorithm repairs. The installed candidate is captured/restored at 17:03:33.277424Z; no native check_changes/is_current belongs to this older workflow. Both are NOT_APPLICABLE here, not missing successful calls.

Supervisor continuation: protected checks run 2026-10-21T17:05:38.177789+00:00 → 2026-10-21T17:15:36.396773+00:00; originals `E269`, `E270`, `E271`, `E272`, `E273`, `E274`, `E275`, `E276`, `E277`, `E278`, `E279`, `E280`. Their retained hashes and progress/closeout equality authenticate recorded outcomes, not a new execution. Review/closeout `E004` (`.local/qwen-coding-worker/environment-13/devtools-environment/closeout.json`; SHA-256 `3d142c5e27e7ab1afa87bd499781d114e9854c8f6e5503b5557076aac00f0105`) binds exact result/files and review subject `c6530e887c215396060ca2d15ee0ee6087896b34993184823c8358d61393e601` (D/R). The three recorded file hashes equal committed bytes. Commit `b81891ceeafa88d21741ef9b69155180a260e75f` has matching result/review trailers, parent and tree; committer date 2026-10-21T13:16:44-04:00. FEATURE_PUBLISHED is recorded; no separate historical post-push ref/time field exists. No mainline grant is inferred.

## Timeline 2 — New-module22 refusals and incomplete implementation

Task definition `0ee51c4604c795d96e75b927273dfa6f38a572a65e7d8469edbb4775f9b2c7ab`; oracle `e60d40dfa5faf6143703cc8d103db8107a0abdd42475abd341b14d0aa17a9e93`. Result `E007` (`.local/qwen-coding-worker/new-module-22/live/result.json`; SHA-256 `4be17b486c18cfde74c4d15936ed53678f2e51883464a8540116e4fee80185bc`).

All rows: native loop produces the request/stage and consumes the provider response; ContextTools/edit admission consumes native calls, then the next model request consumes correlated results/feedback. D identifies checked file/call links; R identifies byte-derived source/check facts. Individual call IDs, source before/after hashes, check timestamps/outcomes and every referenced digest remain in the metadata flow rows.

| UTC stage interval | Exact evidence references | Model → host transition / observed outcome | Strength, omissions and authority |
| --- | --- | --- | --- |
| 2026-10-22T14:04:04.739977+00:00 → 2026-10-22T14:04:40.565106+00:00 | `E091`, `E092`, `E093`, `E095`, `E094` | Turn1: inspect_source. CONTEXT_RETURNED | D/R for recorded links; C for wall-clock order. No edit authority from metadata/call alone. No per-call wall timestamp inferred. |
| 2026-10-22T14:04:40.733594+00:00 → 2026-10-22T14:04:52.383607+00:00 | `E096`, `E097`, `E098`, `E100`, `E099` | Turn2: inspect_source, git_inspect. CONTEXT_RETURNED / PASS | D/R for recorded links; C for wall-clock order. No edit authority from metadata/call alone. No per-call wall timestamp inferred. |
| 2026-10-22T14:04:52.482607+00:00 → 2026-10-22T14:04:57.300230+00:00 | `E101`, `E102`, `E103`, `E105`, `E104` | Turn3: inspect_source. CONTEXT_RETURNED | D/R for recorded links; C for wall-clock order. No edit authority from metadata/call alone. No per-call wall timestamp inferred. |
| 2026-10-22T14:04:57.399457+00:00 → 2026-10-22T14:05:53.788580+00:00 | `E106`, `E107`, `E108`, `E110`, `E109` | Turn4: replace_source. PROPOSAL_REFUSED / TRANSACTION_REFUSED | D/R for recorded links; C for wall-clock order. Whole proposal refused; no sibling mutation admitted. No per-call wall timestamp inferred. |
| 2026-10-22T14:05:53.874423+00:00 → 2026-10-22T14:05:57.941002+00:00 | `E111`, `E112`, `E113`, `E115`, `E114` | Turn5: inspect_source. CONTEXT_RETURNED / ABSENT | D/R for recorded links; C for wall-clock order. No edit authority from metadata/call alone. No per-call wall timestamp inferred. |
| 2026-10-22T14:05:58.032174+00:00 → 2026-10-22T14:06:58.182212+00:00 | `E008`, `E116`, `E117`, `E119`, `E118` | Turn6: replace_source. PROPOSAL_REFUSED / TRANSACTION_REFUSED | D/R for recorded links; C for wall-clock order. Whole proposal refused; no sibling mutation admitted. No per-call wall timestamp inferred. |
| 2026-10-22T14:06:58.286994+00:00 → 2026-10-22T14:07:02.984542+00:00 | `E120`, `E121`, `E122`, `E124`, `E123` | Turn7: search_source. CONTEXT_RETURNED | D/R for recorded links; C for wall-clock order. No edit authority from metadata/call alone. No per-call wall timestamp inferred. |
| 2026-10-22T14:07:03.065655+00:00 → 2026-10-22T14:08:06.345315+00:00 | `E125`, `E126`, `E127`, `E129`, `E128` | Turn8: replace_source. PROPOSAL_REFUSED / TRANSACTION_REFUSED | D/R for recorded links; C for wall-clock order. Whole proposal refused; no sibling mutation admitted. No per-call wall timestamp inferred. |
| 2026-10-22T14:08:06.434062+00:00 → 2026-10-22T14:08:44.868239+00:00 | `E130`, `E131`, `E132`, `E134`, `E133` | Turn9: replace_source. TESTS_FAILED / TESTS_FAILED; checks format:0, oracle:1, ruff:1, tests:0, typing:0 | D/R for recorded links; C for wall-clock order. Admitted proposal; validation/publication remain separate. No per-call wall timestamp inferred. |
| 2026-10-22T14:08:45.187273+00:00 → 2026-10-22T14:09:52.456346+00:00 | `E135`, `E136`, `E137`, `E139`, `E138` | Turn10: replace_source. PROPOSAL_REFUSED / TRANSACTION_REFUSED | D/R for recorded links; C for wall-clock order. Whole proposal refused; no sibling mutation admitted. No per-call wall timestamp inferred. |
| 2026-10-22T14:09:52.874348+00:00 → 2026-10-22T14:10:19.923989+00:00 | `E140`, `E141`, `E142`, `E144`, `E143` | Turn11: inspect_source. CONTEXT_RETURNED | D/R for recorded links; C for wall-clock order. No edit authority from metadata/call alone. No per-call wall timestamp inferred. |
| 2026-10-22T14:10:20.121304+00:00 → 2026-10-22T14:10:45.602433+00:00 | `E145`, `E146`, `E147`, `E149`, `E148` | Turn12: inspect_source. CONTEXT_RETURNED | D/R for recorded links; C for wall-clock order. No edit authority from metadata/call alone. No per-call wall timestamp inferred. |
| 2026-10-22T14:10:45.820664+00:00 → 2026-10-22T14:11:37.752357+00:00 | `E150`, `E151`, `E152`, `E154`, `E153` | Turn13: replace_source. TESTS_FAILED / TESTS_FAILED; checks format:0, oracle:1, ruff:1, tests:0, typing:0 | D/R for recorded links; C for wall-clock order. Admitted proposal; validation/publication remain separate. No per-call wall timestamp inferred. |

Turns04/06/08/10 refuse entire transactions; turn06 returns seven correlated TRANSACTION_REFUSED results. Two proposals (09/13) install partial source, then fail the independent oracle; both existing tests/type/format pass while Ruff fails. The original result finishes 2026-10-22T14:11:37.775479Z with REPAIR_BUDGET_EXHAUSTED, accepted=false and source_restored=true. No model check_changes, host freshness, accepted-model review or Qwen publication follows. Later Codex SnapshotDelta delivery is excluded from this failed model timeline. Result/stages directly record restoration; this audit does not infer arbitrary Tool side-effect rollback.

## Timeline 3 — Map-source27 Codex WorkCycle acceptance and publication

This is a separate Codex-authored implementation, not the original failed Qwen session. Accepted candidate result `E294` (`.local/qwen-coding-worker/map-source-27/codex-delivery/result.json`; SHA-256 `09a5ef2a90f8cf0630f70ed785b85dcc303f0cb911609c3d7476201ca1a28daf`) binds task `1b225286fff53e1fb380829efec6020a3fa3e0b9e3feabcd26a1f01f677c0616`, oracle in the original task/result, and four source hashes.

| Applicable stage / clock | Exact original evidence | Identity / producing → consuming owner | Outcome, association and omissions |
| --- | --- | --- | --- |
| Fixed checks before accepted result at 2026-10-22T19:42:31.449675Z | `E011`, `E296`, `E297` | CodingCommands/check_changes → run_check(all); plan `f035c230928e1266a623207c2cc9094fe9d7fcea8f6ea19ea7412bd03b85eca2`, candidate `f3a8a289aeb939a5c1005910dd478abfb541eb1945f3a2a1c50d13c5a18b18ab` | All five PASS. Stored report and bundle hashes match, journal before=after (D/R). Full scoped Git/source/input state preserved; no model invocation claimed. |
| Installed/restored host freshness; no timestamp in either receipt | `E012`, `E013` | Host → is_current | true while installed, false after restoration is recorded. Old status remains PASS, readiness becomes false. Exact report input association is C: saved results lack input digest/call ID/time. |
| 2026-10-22T19:46:17.320278+00:00 → 2026-10-22T19:59:23.408960+00:00 | `E295`, `E282`, `E283`, `E284`, `E285`, `E286`, `E287`, `E288`, `E289`, `E290`, `E291`, `E292`, `E293` | Checkout local-closeout → validate_tree → protected profile | All retained log hashes match and progress equals closeout embedded object (D/R). Existing passing evidence was reused by later publication. No gate rerun here. |
| Restoration 2026-10-22T19:59:25.097341Z; later review/closeout at 2026-10-22T20:00:34.516843+00:00 | `E021`, `E010` | Checkout → supervisor review → closeout | History seal matches; review subject `9d27ac7f9f3305f05fe138209b07f51415034f7f6a464249a92d9e69c09e81bf` binds result/base/files. The selected history is validation/restoration, not the final publishing Checkout occurrence. |
| Committer 2026-10-22T16:00:56-04:00 | `E010`, local Git commit `0bdc8507601dcf65a742ab3ce5cca4bb8e6f590a` | Reviewed exact source/test inventory → Git | Matching parent/tree/trailers (D/R). Three files match physical hashes exactly; two match only after explicit Git LF→CRLF conversion. No semantic difference beyond that conversion found by hash relation. |
| Remote publication after commit; no separate completion timestamp | `E010` FEATURE_PUBLISHED | integration.publish → expected remote/ref | Receipt assertion plus inspected exact-ref policy; no independently retained post-push ref observation (C/U). Current reachable history supports adoption, not the historical timestamp. |

The two converted paths are `src/devtools/context/planning/source.py` and `src/devtools/context/retrieval/source/representation.py`. Metadata retains both committed and recorded physical SHA-256 values; current `core.autocrlf=true` and `git ls-files --eol` support the interpretation, but the exact transformed-hash equality is the stronger R evidence. Do not state every committed blob equals the recorded physical bytes. Full validation input-closure/reuse semantics still need targeted qualification; no historical gate was invalidated or rerun by this audit.

## Timeline 4 — Map-disclosure26 mismatch and separate stopped-owner recovery

Task definition `c5b9d451b27f04ed39b97df80dbac3dd002e83400deb3461270f632e310665a1`; oracle `52322a41fae0fb606d3f1a1c2f8cf8a3d61044081a5041c56571120cece2b277`. Result `E017` (`.local/qwen-coding-worker/map-disclosure-26/live/result.json`; SHA-256 `50aca50e491c797bf8ff63fe7bf66dd57eac32e659cf47ec572e700e5feb43a1`).

All rows: native loop produces the request/stage and consumes the provider response; ContextTools/edit admission consumes native calls, then the next model request consumes correlated results/feedback. D identifies checked file/call links; R identifies byte-derived source/check facts. Individual call IDs, source before/after hashes, check timestamps/outcomes and every referenced digest remain in the metadata flow rows.

| UTC stage interval | Exact evidence references | Model → host transition / observed outcome | Strength, omissions and authority |
| --- | --- | --- | --- |
| 2026-10-22T18:39:29.096507+00:00 → 2026-10-22T18:39:40.725750+00:00 | `E155`, `E156`, `E157`, `E158` | Turn1: inspect_source. CONTEXT_RETURNED / ABSENT | D/R for recorded links; C for wall-clock order. No edit authority from metadata/call alone. No per-call wall timestamp inferred. |
| 2026-10-22T18:39:40.773808+00:00 → 2026-10-22T18:39:48.317413+00:00 | `E159`, `E160`, `E161`, `E162` | Turn2: inspect_source. CONTEXT_RETURNED | D/R for recorded links; C for wall-clock order. No edit authority from metadata/call alone. No per-call wall timestamp inferred. |
| 2026-10-22T18:39:48.380925+00:00 → 2026-10-22T18:39:56.176329+00:00 | `E163`, `E164`, `E165`, `E166` | Turn3: inspect_source. CONTEXT_RETURNED | D/R for recorded links; C for wall-clock order. No edit authority from metadata/call alone. No per-call wall timestamp inferred. |
| 2026-10-22T18:39:56.240136+00:00 → 2026-10-22T18:40:04.582239+00:00 | `E167`, `E168`, `E169`, `E170` | Turn4: inspect_source. CONTEXT_RETURNED | D/R for recorded links; C for wall-clock order. No edit authority from metadata/call alone. No per-call wall timestamp inferred. |
| 2026-10-22T18:40:04.655440+00:00 → 2026-10-22T18:40:13.043364+00:00 | `E171`, `E172`, `E173`, `E174` | Turn5: lookup_symbol. CONTEXT_RETURNED / RETURNED | D/R for recorded links; C for wall-clock order. No edit authority from metadata/call alone. No per-call wall timestamp inferred. |
| 2026-10-22T18:40:13.112681+00:00 → 2026-10-22T18:40:24.290923+00:00 | `E175`, `E176`, `E177`, `E178` | Turn6: expand_source. CONTEXT_RETURNED / SOURCE_PARENT_NOT_FOUND | D/R for recorded links; C for wall-clock order. No edit authority from metadata/call alone. No per-call wall timestamp inferred. |
| 2026-10-22T18:40:24.373291+00:00 → 2026-10-22T18:40:30.871243+00:00 | `E179`, `E180`, `E181`, `E182` | Turn7: inspect_source. CONTEXT_RETURNED | D/R for recorded links; C for wall-clock order. No edit authority from metadata/call alone. No per-call wall timestamp inferred. |
| 2026-10-22T18:40:30.975693+00:00 → 2026-10-22T18:40:39.734203+00:00 | `E183`, `E184`, `E185`, `E186` | Turn8: inspect_source. CONTEXT_RETURNED | D/R for recorded links; C for wall-clock order. No edit authority from metadata/call alone. No per-call wall timestamp inferred. |
| 2026-10-22T18:40:39.835135+00:00 → 2026-10-22T18:40:46.318990+00:00 | `E187`, `E188`, `E189`, `E190` | Turn9: inspect_source. CONTEXT_RETURNED | D/R for recorded links; C for wall-clock order. No edit authority from metadata/call alone. No per-call wall timestamp inferred. |
| 2026-10-22T18:40:46.420597+00:00 → 2026-10-22T18:40:51.409689+00:00 | `E191`, `E192`, `E193`, `E194` | Turn10: inspect_source. CONTEXT_RETURNED | D/R for recorded links; C for wall-clock order. No edit authority from metadata/call alone. No per-call wall timestamp inferred. |
| 2026-10-22T18:40:51.556067+00:00 → 2026-10-22T18:41:30.193616+00:00 | `E195`, `E196`, `E197`, `E198` | Turn11: search_source. CONTEXT_RETURNED | D/R for recorded links; C for wall-clock order. No edit authority from metadata/call alone. No per-call wall timestamp inferred. |
| 2026-10-22T18:41:30.349700+00:00 → 2026-10-22T18:42:00.464742+00:00 | `E199`, `E200`, `E201`, `E202` | Turn12: inspect_source. CONTEXT_RETURNED | D/R for recorded links; C for wall-clock order. No edit authority from metadata/call alone. No per-call wall timestamp inferred. |
| 2026-10-22T18:42:00.774877+00:00 → 2026-10-22T18:42:31.530804+00:00 | `E203`, `E204`, `E205`, `E206` | Turn13: search_source. CONTEXT_RETURNED | D/R for recorded links; C for wall-clock order. No edit authority from metadata/call alone. No per-call wall timestamp inferred. |
| 2026-10-22T18:42:31.893892+00:00 → 2026-10-22T18:44:35.577480+00:00 | `E207`, `E208`, `E209`, `E210` | Turn14: replace_source. PROPOSAL_REFUSED / TRANSACTION_REFUSED | D/R for recorded links; C for wall-clock order. Whole proposal refused; no sibling mutation admitted. No per-call wall timestamp inferred. |
| 2026-10-22T18:44:36.435790+00:00 → 2026-10-22T18:45:12.806893+00:00 | `E211`, `E212`, `E213` | Turn15: replace_source. CLEANUP_RECONCILIATION_REQUIRED | D/R for recorded links; C for wall-clock order. Admitted proposal; validation/publication remain separate. No per-call wall timestamp inferred. |

Turn14 rejects an oversized replacement; turn15 is source-admitted, but application adds an unproposed LF. Original result `E017` ends 18:45:12.793629Z with CLEANUP_RECONCILIATION_REQUIRED and source_restored=false. Stage finishes 13ms later at 18:45:12.806893Z: these are nested checkpoint wall observations, not a strict causal event clock. No independent candidate validation, native check_changes, host freshness or Qwen publication occurred.

Separate recovery: `E018` names original result digest and exact admitted/actual hashes; `E019` authenticates actual installed bytes. Comparing the turn15 proposed new_text with retained failed bytes proves exactly one terminal LF was added (R), without applying/replaying the edit. `E020` seals the original operation/PID/base/admitted fingerprints and return HEAD at 18:47:00.837632Z. The recovery note states stopped-process confirmation, but provides no linked timestamped stop observation/approval occurrence. That edge remains C/U. This authenticates scoped recovery evidence, not a successful model outcome or undo of external effects.

## Timeline 5 — Map-source27 turn06 genuine but refused expansion

Task definition `1b225286fff53e1fb380829efec6020a3fa3e0b9e3feabcd26a1f01f677c0616`; oracle `0e4decc8e180a146703ed3600619e2a88aa5237dd720b7fae3cd5d7c10bb9e01`. Result `E268` (`.local/qwen-coding-worker/map-source-27/live/result.json`; SHA-256 `b6d81c21dbfaa811a89aca1836c49fcaf337c2643ab82761d1d988b0f2a827db`).

All rows: native loop produces the request/stage and consumes the provider response; ContextTools/edit admission consumes native calls, then the next model request consumes correlated results/feedback. D identifies checked file/call links; R identifies byte-derived source/check facts. Individual call IDs, source before/after hashes, check timestamps/outcomes and every referenced digest remain in the metadata flow rows.

| UTC stage interval | Exact evidence references | Model → host transition / observed outcome | Strength, omissions and authority |
| --- | --- | --- | --- |
| 2026-10-22T19:32:43.496472+00:00 → 2026-10-22T19:32:47.290319+00:00 | `E230`, `E231`, `E232`, `E233` | Turn5: lookup_symbol. CONTEXT_RETURNED / RETURNED | D/R for recorded links; C for wall-clock order. No edit authority from metadata/call alone. No per-call wall timestamp inferred. |
| 2026-10-22T19:32:47.405575+00:00 → 2026-10-22T19:32:52.484671+00:00 | `E015`, `E234`, `E235`, `E014` | Turn6: expand_source. CONTEXT_RETURNED / SOURCE_PARENT_NOT_FOUND | D/R for recorded links; C for wall-clock order. No edit authority from metadata/call alone. No per-call wall timestamp inferred. |
| 2026-10-22T19:32:52.569320+00:00 → 2026-10-22T19:32:55.471917+00:00 | `E236`, `E237`, `E238`, `E239` | Turn7: inspect_source. CONTEXT_RETURNED | D/R for recorded links; C for wall-clock order. No edit authority from metadata/call alone. No per-call wall timestamp inferred. |

**Correction to the prospective plan:** turn06 requested `expand_source(unit=30fbba64aca016ff6c16485e58f318697447223c71c1db2e2dffd9fc0058db29, to=symbol)` with native provider call ID `EP2mwrJneAOLRWqsf94BcUavLG1venIp`. `E014` is REFUSED / SOURCE_PARENT_NOT_FOUND (“Source unit has no parent symbol”). It returns schema/diagnostic/limits, not source text, a source version or new editable observation. `E015` and its request/response hashes authenticate the call; turn07 contains the matching Tool result ID. The plan’s expectation that this result held source occurrence/provenance was incorrect.

The selected flow is preserved as a real refused navigation operation, not replaced by a manufactured success. Adjacent genuine inspections and Environment13 `E003` demonstrate successful existing source observation separately: the latter ties edit_ref R1, path/content version/span and observation_call_id to native `inspect_source` call `5dT8JtsooVYsXQt5Qv62VHIfIB4u6N8g`. Those are different calls; their authority is not transferred to failed expansion. The original27 session later ends CONTEXT_BUDGET_FAILED, zero proposals; validation/review/publication of model source are NOT_REACHED. The Codex timeline above remains independent.

## Audit verification

Publication checks passed: layout, 36 existing layout/intake tests (1.38s,
`--no-cov`), introduced documentation links/anchors, JSON and canonical intake
chains/dispositions. No new proposal, B-number or approval was created. The
evidence metadata records this bounded validation separately from historical
protected results.

Original21 hashes/lengths, all catalogued file identities, stage request/response references, raw/normalized provider call IDs where sidecars exist, retained next-request Tool IDs, both review-subject calculations, commit parent/tree/trailers, protected logs/progress, report/bundle hashes and Checkout seals were checked without replay. Current source/test state and original forensic files are preserved. Documentation/layout/link/intake validation is recorded at publication; no protected production gate or historical task is rerun for this report.
