# Bounded local coding worker

## Framework-owned native model/Tool composition

Both `ContextTools.dispatch` and `CodingCommands.dispatch` now delegate selected
native calls through `devtools.agents.model_tools`, using the existing typed
ToolInvocation and ToolRunner. The application retains trusted task operation
selection, JSON tuple materialization, source admission/currentness, fixed
commands, journals, budgets and result decoration. The previous descriptor
normalizer remains a direct compatibility facade. This capability is also
exercised by a non-Qwen host denied application imports and file access; it is
not a promotion of the complete Qwen coding loop. See the
[shared contract](../../src/devtools/agents/docs/model_tools.md).

## Operational application ownership

The public `coding_loop` entry point retains task preparation, validation adapters,
candidate archiving, source restoration and terminal accounting. Its
[turn implementation](turns/README.md) separates bounded turn sequencing,
Prompt/input projection and authorized read/check dispatch. Existing task hashes,
records, budgets, native obligations and public callers retain their contracts.
This extraction adds no model capability or authority and raises no edit limit.

## Opt-in obligation-driven Context

The native worker can consume a trusted, task-bound `--obligation-frame` using
existing Localization grounding, association, caller resolution, promotion and
readiness. Exact current witness ranges must be present in active Context before
mandatory requirements permit an edit. Helpful gaps remain visible without
blocking; relevance and model claims do not establish support. Existing source
admission, checks, limits, terminal outcomes and publication authority remain
separate. Unframed task formats/digests and behavior are unchanged. See the
[frame contract, CLI and limitations](obligations/README.md). This bounded consumer
does not approve A+C, automatic semantic resolution or restart/replay.

## Command receipt custody

CodingCommands reserves a journal name before command entry using atomic directory
creation in its evidence folder. Existing receipts and reservations are never
reused, including across fresh adapters. Bundles and change reports use the same
allocator. Reservations survive interruption and are not stale locks to delete.
Single commands retain intent before execution and replace only their own intent
with the completed result. Missing completion means unknown outcome, not permission
to redispatch. A storage failure before intent prevents execution; failed result
persistence after entry is reported without retry. This is not a power-loss or
exactly-once external-effect guarantee.

## Maintained worker acceptance integrity

The terminal `accepted` flag means the worker completed successfully with its
required candidate checks and final integrity conditions satisfied. It is the
CLI/closeout success signal, not a standalone test verdict. Fatal worker errors
and timeouts clear it even after shared checks established a valid candidate.
Per-turn validation, `change_check` and its installed-currentness observation,
candidate archives, completed effects, counters and error/disposition remain
factual evidence; they are not rewritten as failed tests. Currentness recorded
before restoration does not claim the restored working tree is that candidate.
Failure while archiving/restoring or writing the final result propagates without
returning success or retrying. Missing acknowledgment can remain ambiguous;
neither an archived candidate nor a partial record licenses replay. Independent
review/publication and Checkout finalization retain their separate contracts.

Prepared and native coding validation use the same journaled fixed-check bundle.
The worker binds its immutable validation plan before baseline checks, preserves
complete host diagnostics, checks input/source correspondence between checks and
reauthenticates before final acceptance. Changed tests, read inputs, runners or
configuration refuse acceptance; unexpected bytes remain for reconciliation.
Known admitted source restoration is separate from immutable-input integrity.
This is not an OS sandbox, task-completeness proof or publication authority.
Both modes consume one proposal allowance per attempted edit response, including
refusals. Multiple components in one admitted native batch remain one proposal.
The independently bounded model-call limit still applies; prepared prompt and
receipt counters distinguish attempted, refused and admitted proposals.
The application retains the returned response and usage, then authenticates its
source against the interaction selected before invocation. A foreign label stops
before Tool/edit admission with RESPONSE_VALIDATION_FAILED and no redispatch.
Runtime's equivalent private check remains within its own narrow boundary; the
coding application does not require a Conversation or a new execution framework.

## Map-to-source27: Codex capability, native investigation exhausted Context

Caller-selected map orientation can now expand a represented symbol to its exact
RI declaration range through existing Planning/source machinery. This is Codex
software. The one Qwen attempt made14 requests,256,729 input/1,142 output tokens
in194.803 worker seconds,25 investigation dispatches and no edits. Request15
was host-refused at28,478 input tokens:2242 safe generation tokens versus the
4096 investigation minimum. Baseline restoration succeeded, without host Git
contamination. No native check_changes, behavioral repair or live EOF application
occurred; deterministic EOF regressions pass separately. No worker/Context/serving
change or task retry was made. Separate host checks/currentness, real progressive
Context composition and WorkCycle publication qualify the delivered source.
See [contract, demonstration and immutable outcome](evaluation/map-source-27/README.md).

## Map disclosure26: useful Codex delivery, native EOF application failure

One clean, qualified Qwen session attempted compact repository-map Context.
15 requests used280,669 input/3,690 output tokens in346.564 worker seconds.
Response14's9,578-byte component was specifically refused; response15 reduced
it to an admitted1,148-byte new-file header. The host diff boundary added an
unproposed final LF, correctly tripping exact-byte verification and requiring
stopped-owner recovery. Original nonacceptance is unchanged. No native
check_changes, behavioral acceptance/repair or Context exhaustion occurred.
The concrete EOF generator defect now has a narrow standard-marker correction
and real Git regressions; there was no model retry. Codex separately delivered
the frozen map-disclosure feature with independent tests, real host shared-check
PASS/current-installed/stale-restored evidence and protected WorkCycle closeout.
No Qwen source is credited for the delivered implementation. See
[qualification, provenance and final validation](evaluation/map-disclosure-26/README.md).

## Role integration25: Qwen source, host-blocked native completion

Qwen authored the complete dependency-group Localization correction, passing
behavior/quality on its first proposal. Fourteen requests used 261,714 input/
2,303 output tokens in 302.035 worker seconds. Native check_changes was genuinely
called but correctly blocked by host-owned untracked apps evaluation artifacts.
The original nonaccepted receipt is unchanged. Separate supervised ToolRunner
checks pass on identical Qwen bytes; host freshness is current while installed,
stale after restoration. Existing WorkCycle publishes those bytes at `5ebe8eb674f836581fc8162859c9b5f2b3242d49`
with independent regressions and protected validation. No Codex semantic patch
or fallback is credited to Qwen. No behavioral repair occurred.

One Codex projection correction shares identical search-hit provenance, restoring
Engineering 24's blocked request from 31,867 to 28,400 tokens with 2,320 safe output.
Raw source/feedback/native correlations remain;32K serving is unchanged. This is
measured continuation capacity, not proof of general repair reliability.
See [exact task, source, admission and validation evidence](evaluation/role-groups-25/README.md).


## Static dependency groups24: Codex delivery after Context-blocked Qwen attempt

The bounded raw-string RI capability is feature-published at `7e1b10033c8793440994ef6069c9c0482dea74f8` with Codex
authorship. One genuine Qwen attempt made ten requests, 173,464 input/3,117 output
tokens and one admitted four-component transaction in 244.057 worker seconds.
It used the wrong TOML parent, failed behavior and quality, then searched for
oracle expectations. Request 11 was blocked at 31,867 prompt tokens after
compaction; no behavioral repair, native check_changes or host freshness success
is claimed. No edits were refused, so new component diagnostics were not tested
by inference. The worker/serving profile is unchanged. Codex separately delivered
the frozen contract after authenticated restoration, with 151 focused RI cases,
100% scoped branch coverage and exact-source protected WorkCycle validation.
See [full evidence](evaluation/dependency-groups-24/README.md). B-0002/B-0009
remain at their existing broader status; protected-main adoption is separate.


[New module22](evaluation/new-module-22/README.md) fixes authorized absent-slot
feedback and demonstrates real module creation, but the Qwen attempt failed public
integration after six proposals. The available check_changes/is_current Tools were
not invoked by Qwen. Its exact partial source remains evidence-only; Codex delivered
the snapshot-comparison capability separately at `3c624129ee2d6324ed161a2e9e3b2733622e7b08`. Deterministic native
creation/feedback/ToolRunner/restoration passes; this is not model success.


[Configuration obstructions21](evaluation/configuration-obstructions-21/README.md)
feature-publishes the RI correction with explicit Codex authorship and the unchanged
original oracle. No Qwen continuation ran: existing replay could not authenticate
the required prefix without extension. Engineering20 remains eight genuine Qwen
responses, ten successful investigations and zero edits; the supervisor stopped
before request9 with Context available. This was not a behavioral failure, and
Engineering14's first edit on response9 disproves a general eight-response cutoff.
Qwen did not use check_changes. A narrow Codex prerequisite now lets
an opt-in worker continue after accepted edits until model-invoked checks and
host freshness, but its live Qwen use remains unproven. Older outcomes stay intact.

**Delivered directly by Codex:** shared `check_changes` and `is_current` are
feature-published at `4d401c828b5fef4e2d4db949c2f80549ea445fe0`, composing the previously delivered `run_check(all)`.
See [the shared Tool contract](#source-bound-change-checks) and
[delivery evidence](evaluation/change-check-codex/README.md). This is Codex-authored
software, not a new Qwen success. All historical outcomes below remain unchanged.

[Source-supplied19](evaluation/source-supplied-19/README.md) began implementation
on response two but **did not deliver** the bundle. Authentic initial Context
fit at 9,151 input tokens; six requests produced four atomically refused proposals
(oversized regions, then a no-op), with no source mutation or Context failure.
The presentation elicited proposals, not accepted software. Stop repeating minor
Qwen variants of this contract: deliver the bundle in a separately attributed
Codex implementation increment, then compose full check_changes. Existing exact
admission stays unchanged. Earlier entries below retain their historical status.

[Fixed check-bundle18](evaluation/check-bundle-18/README.md) is **not delivered**.
The smaller `run_check(check="all")` assignment used nine requests and all 16
successful read actions, but made zero edits. Pending request ten compacted to
27,561 input tokens, leaving 3,159 safe output tokens below the 4,096 minimum.
No worker or source implementation changed and no retry followed. The immediate
obligation remains this fixed bundle; full `check_changes` and its original
contract remain unfinished. Before another attempt, use an implementation-oriented
assignment with authenticated essential owner/helper source, rather than another
localization exercise or generic Context optimization. Entries below are history.

[Change-check17](evaluation/change-check-17/README.md) remains **not delivered**.
Narrower approved-owner scope avoided the prior closeout detour, but Qwen made
11 requests/20 read actions and zero edits before Context refusal. The action
allowance was exhausted, so source could not be omitted for future reacquisition;
31,675 input tokens plus safety exceeded capacity. The original oracle is unchanged.
No maintained code, projection or serving configuration changed. Next assess a
smaller useful fixed-check bundle in existing run_check, not generic Context work
or a claim that partial functionality completes check_changes. Older entries below
retain their historical status.

[Shared change-check16](evaluation/change-check-16/README.md) **was not delivered**.
The one Qwen attempt made 15 requests and 20 read actions with no edit, then failed
Context admission: 28,489 input tokens left 2,231 safe output below the 4,096 minimum.
The exact frozen contract and failure remain evidence. Codex only enabled explicit
maintained application task paths/local imports so Qwen could target the existing
owner; this is not a check_changes implementation. No retry, semantic substitute
or speculative worker optimization occurred. The next obligation remains this
same composed Tool; prior accepted Commands features remain published.
Earlier entries below retain their historical status.

[Output policy development15](evaluation/output-policy-15/README.md) completes
the previously exposed integer/bool validation defect with the unchanged worker.
The independently reconciled contract uses TypeError for wrong types and
ValueError for invalid integer bounds. Qwen's first transaction passes: 6 requests,
one admitted proposal, no repair/refusal; exact source plus 60 independent regressions
are feature-published at `c93e5bf0f508`. 176 focused cases and the protected gate
pass. This is development continuation, not fresh confirmation or repair evidence.
Next evaluate a practical shared change-check bundle over existing Git/validation
operations; no new harness optimization is justified by this result.
Earlier entries below retain their historical then-current status.

[Engineering 14](evaluation/engineering-14/README.md) demonstrates fresh useful
development with the unchanged worker: a complete command/result capability,
real-child/Tool validation and one corrected behavioral defect, 10 requests and
two admitted transactions. Exact Qwen source and independent permanent tests
are feature-published at `73e5ee07ee49`. No worker/Context/edit/serving change
or implementation intervention was required; general reliability remains open.

[Environment development 13](evaluation/environment-13/README.md) completes the
original exposed Commands environment contract through the unchanged worker:
14 calls, five admitted proposals, no refusals, full independent behavior/quality
acceptance. Exact Qwen source plus independent regressions is reviewed and
feature-published at `b81891ceeafa`. The existing 32K profile and editing/Context
contracts are unchanged. Pi's bounded diagnostic timed out with incomplete code
and adapter/output limitations; no general harness ranking follows. Prior failed
receipts remain immutable; earlier checkpoint descriptions below retain their
historical scope. Protected-main adoption and general engineering reliability
remain open.

Host tasks may opt into `path_edits=True`: flat `replace_source(path, old_text,
new_text)` resolves nonempty exact old text against the union of current disclosed
source spans for an authorized path. The existing transaction engine still
requires a unique source occurrence and enforces version, scope, overlap and byte
limits atomically. Empty old text is admitted only for observed authorized absence.
Legacy reference calls retain their original strict region semantics; they are
never redirected to a different observation. Default task hashes and three-edit
budgets remain compatible. Native tasks may prospectively select
`maximum_proposals` up to six (default three), without expanding calls/time/actions.
Use `--observed-edits` with a host task definition selecting `path_edits`, or
`run_local_task(..., coordinated_edits=True, observed_edits=True)`. Historical
definitions continue to use the reference contract by default.

In path mode, source is rendered in separate exact code blocks with path, span,
version, character length and text hash; metadata is explicitly outside the code.
Projection/token accounting uses that actual rendered Prompt. Original structured
Tool observations, native call/result IDs and unprojected Prompts remain archived.
This is a presentation/admission option within existing owners, not another
reader, patch engine or memory store. The
[stdin development continuation](evaluation/stdin-11/README.md) retains the original
qualified contract and does not relabel Engineering 10 or claim fresh confirmation.

Pre-edit source embedded in component receipts now uses the same stale-version
and duplicate-text projection as reads and refreshed observations. Complete raw
receipts remain archived; current source, handles, feedback and native correlation
are preserved. [Qualified engineering 10](evaluation/qualified-10/README.md)
records why this correction was needed and two genuine unsuccessful tasks.
It demonstrates live feedback continuation, not successful behavioral repair or
general substantial-task acceptance.

Exact tokenizer measurement precedes capacity refusal. The worker first removes
redundant attestation envelopes and repeated refusal bodies with explicit links
to original archived Tool call IDs/hashes. When necessary, older read-only source
excerpts are explicitly marked for reacquisition; current editable observation
text, versions, handles and recent refusal/validation feedback remain intact.
In compact mode, completed applied arguments and older refused arguments
superseded by an applied transaction are explicit archival projections, retaining
original hashes and correlated host receipts. These projection objects are not
examples of new Tool arguments. Pending/unknown/latest refused arguments stay
exact. Current contained excerpts may reference a strictly larger same-path,
same-version observation only after exact coordinate/character verification.
Original handles survive; no source is invented or approximate matching admitted.
Text-free stale/duplicate observation envelopes retain their identity/reference
fields, backed by the archived whole-message hash. Full raw evidence is unchanged.
See [environment development evidence](evaluation/environment-12/README.md) for
the live recovery and failed coding disposition. No unlimited-session guarantee.

Native assistant/call/result associations remain complete. No LLM summary or
new Memory store is involved. Investigation continuations reserve at most 4K
output; initial implementation and edit/repair continuations target the frozen
ceiling. Initial implementation retains a 4K fallback; short investigation and
already-started bounded repair may use at least 2K measured remaining output
with the unchanged 2K safety
allowance. Superseded diagnostic bodies compact to prior check statuses and
archival provenance; the latest exact failures and current source stay available.
On-demand task ceilings are 24 model requests and 1,800 cumulative seconds,
independent of the unchanged 32K per-request server capacity. Defaults and
historical receipts are unchanged. Actual `freeze.tool` now records the flat
observed schema when selected; historical `request.tools` remain authoritative.
An older excerpt is omitted only while both read actions and subsequent model
calls remain available. Exhaustion preserves source and refuses capacity instead.
Each new native turn archives `unprojected-prompt.json` using the same `Prompt`
contract as `request.prompt`, including exact original Tool-content strings.
It is evidence outside the active input, not a second conversation representation.

The coding environment also supports task-opted-in `git_inspect` (scoped status,
diff and history) and `run_check` (fixed regression/oracle/Ruff/format/strict mypy)
through ToolRunner and managed Commands. No model-selected argv or shell is
accepted. Full check logs are archived; model results are bounded and source-bound.
`command_tools`, `tool_actions` (default eight, host ceiling 32) and
`mechanical_format` enter the task digest. Formatting is opt-in, AST-equivalent,
and journaled before writing; behavior/typing failures use the same repair loop.

## Fixed all-check bundle

Use the existing `CodingCommands` instance bound to an absolute canonical root,
host evidence directory and host-owned CodingTask with prepared validation runners:

```python
report = await ToolRunner().execute(commands, ("run_check", {"check": "all"}))
```

Native `ModelToolCall("run_check", '{"check":"all"}', call_id)` dispatches through
the same ToolRunner. The five individual selectors remain unchanged. The `all`
selection is also available to direct trusted callers of module-level `run_check`.
Native command availability still requires `task.command_tools`; a read result
or a passing report grants no authority.

Tests and independent oracle are required. Ruff/format follow `quality_checks`;
strict mypy follows `command_tools`. Each of the five entries has its own status,
elapsed seconds, bounded stdout/stderr (3,000 characters each), truncation flag
and full evidence reference. Ordinary nonzero checks are FAIL and do not prevent
independent checks. Missing/mismatched plans, unavailable commands, timeouts,
incomplete managed output or observed identity drift make the bundle BLOCKED.
Unstarted checks remain NOT_RUN; disabled checks are NOT_APPLICABLE. PASS requires
all applicable checks to pass together on unchanged observed inputs.

`source_sha256`/`source_after_sha256` include authorized absent new slots as null.
`task_definition_sha256`, `plan_sha256`/`plan_after_sha256` and cumulative
`source_unchanged`/`plan_unchanged` bind the report to source, immutable read/test
inputs, fixed runners, interpreter/root and standard applicable configuration.
The existing runner rendering is shared by preparation and admission; even a
nonempty substituted runner is refused. Nested Ruff configuration and pytest
conftest files along declared paths are included. Identity is sampled around
each check and at completion; observed drift stays invalid even if later restored.
The caller's existing Checkout owner supplies mutation serialization.

One `coding-command-NN.json` journal retains full captured outputs and plan
identities under existing managed output/time limits. Rows correlate by check
name and reference that journal. Progress is saved before execution, so failure
cannot turn unexecuted checks into passes. Cancellation records INTERRUPTED and
propagates; an evidence-write failure is attached to cancellation rather than
masking it. The operation does not edit source, format it in place or mutate Git.
Check programs may create normal caches/fixtures; observed source mutation blocks
the report and is not automatically rolled back by this read/validation Tool.

This checks only the host-declared resources and fixed plan. It performs no Git
change discovery, generalized test selection, historical freshness query or
review-readiness certification. It cannot detect unobserved mutation/restoration
inside a check. Reports apply to their recorded state, not arbitrary future edits.
WorkCycle alone retains independent review, protected validation and explicitly
authorized publication. The delivered `check_changes` reuses this bundle; it does
not reimplement checks.

## Native completion with shared checks

Trusted callers may pass `check_changes_before_completion=True` to the existing
run_local_task, or use `--observed-edits --check-changes-before-completion` on the
coding_worker CLI. This requires task command_tools and quality_checks. It does
not change Task identities/defaults, grant authority or add another runner.

The legacy default still terminates after independently passing edit validation.
The opt-in mode continues in the same bounded native conversation until Qwen
invokes check_changes on an installed edited candidate. At the end of that Tool
batch, the host calls is_current through ToolRunner and accepts only current,
complete passing evidence. A later failed Tool in that batch prevents acceptance.
Plain model completion without the check remains unsuccessful. Budget limits and
atomic admission remain unchanged. Evidence records model Tool calls separately
from host freshness verification; pristine report payloads receive no host_limits
presentation mutation. Once source is restored, do not claim that report remains
current. WorkCycle must install/revalidate/review the exact candidate independently.
This pathway passes deterministic worker tests; Engineering20 never reached it.

## Source-bound change checks

```python
report = await ToolRunner().execute(commands, ("check_changes", {}))
freshness = await ToolRunner().execute(commands, ("is_current", {"report": report}))
```

The same operations are exposed through native `ModelToolCall` dispatch when
`task.command_tools` authorizes CodingCommands. Empty change-check arguments cannot
supply alternate scope, tests, commands or effects. The host prepares the canonical
CodingTask and runners and retains existing Checkout mutation ownership.

`changed` distinguishes staged/unstaged status, authorized new-file presence and
content hashes. `source_sha256` includes absent new slots as null. Scoped literal
Git observations retain HEAD/branch, exact index entries and NUL-delimited status.
HEAD must match the task baseline. Unsupported deletion, unmerged index entries,
changed test/read/configuration resources, other tracked changes and unapproved
new source/test files block readiness. Unrelated untracked artifacts are excluded;
this never certifies whole-repository cleanliness.

`candidate_sha256`, `checked_candidate_sha256`, `after_candidate_sha256`,
`task_definition_sha256` and `plan_sha256` bind the observed/checking/postcheck state.
Full before/after data is in the journal. The plan includes frozen tests/read inputs,
applicable configuration, actual and canonical generated runners, interpreter
identity and fixed implementation hashes. Changes to check-execution code require
a freshly loaded host-bound Tool/session; the old bound plan fails closed.
The bundle authenticates source/plan
and scoped Git state at check boundaries; any observed drift blocks the result.

One nested ToolRunner `run_check(all)` is the only check-execution path. Full
pre-review validation requires all five checks. Independent PASS/FAIL and blocked
outcomes retain timings, bounded diagnostics and underlying evidence references.
The outer projection marks unexecuted integrity-stopped checks BLOCKED and records
`bundle_status=NOT_RUN`; the unchanged raw bundle is also archived. No changes
returns NO_CHANGES/false readiness with explicitly nonexecuted checks. Missing or
incomplete plans, unavailable commands and incomplete logs cannot pass. Cancellation
propagates while preserving already completed outcomes and interruption evidence.

`change-check-NN.json` retains full original bundle outputs and observed states.
The bounded returned report carries its `receipt_sha256` and the full bundle
receipt/hash. `is_current` confines evidence lookup to that host directory,
authenticates the complete report payload and underlying log, and reobserves
source/new absence, HEAD/index, task, runner and input/configuration identities.
It never reads arbitrary paths from a caller report and never reruns the checks.
The historical synchronous `commands.is_current(report)` remains a boolean helper
using the same managed observations through a single compatibility thread; native
and ToolRunner freshness operations are async and return structured results.

Freshness and correctness are separate: a complete FAIL can remain current, but
`ready_for_review` remains false. PASS readiness requires a complete unchanged
five-check plan, not style checks alone. It only means eligible for independent
review under the frozen plan; it proves neither complete obligation coverage nor
publication authority. Changed source or index needs renewed checks. Incomplete
evidence cannot establish current validation. Existing Checkout serialization and
WorkCycle final source reauthentication remain required; unobserved external
change-and-restore between observation boundaries cannot be detected.

Explicit `new_paths` admit existing-parent Python implementation files only.
Repair feedback uses a null source version for an authorized slot that remains
absent; this is not an empty source observation. Created files have their actual
snapshot versions. The worker reauthenticates current Context before feedback,
so required-resource loss and unexpected new-path occupation remain failures.
`inspect_new_source` verifies actual absence and returns its task-bound version;
an atomic proposal uses that version and empty old text. Unknown files, aliases,
collisions and unobserved absence refuse. Existing resources keep exact source
observation requirements. Historical task digests/defaults remain unchanged.

An explicitly scoped local operation may now contain up to five implementation
files (at most four existing plus authorized new paths), within the unchanged
32-resource corpus and transaction byte limits. `disclose_edit_paths=False`
withholds the exact editable subset from the initial native prompt for genuine
diagnosis tasks. The model receives a sorted read corpus with plausible
alternatives; admission still enforces the exact frozen paths. The default
retains prior hints and definition digests. This is task-local investigation,
not authority to edit every visible resource.

For observed, thinking-off requests with an output ceiling above 4,096, measured
32K capacity may reduce the requested generation allowance to available space,
provided at least 4,096 tokens remain for an initial implementation, or 2,048
for a measured investigation/started repair, after the unchanged 2,048-token safety
margin. Evidence records the task ceiling and effective request limit. Source
observations are retained; reasoning-mode allowances are not reduced. A full
input or insufficient remaining generation capacity still refuses dispatch.
Wrong-region edit refusals name the exact observation handle/path/span; the
host never substitutes another anchor or partially applies the transaction.

Native tasks may explicitly reserve up to 12,288 output tokens and 600 seconds
per call for reasoning evaluation; defaults remain 4,096/300 and 900 task seconds,
with an explicit on-demand task ceiling of 1,800 seconds.
`--thinking enabled --reasoning-effort medium` selects the
actual supported template control. The 32K input/output allocation is respected
by the existing working-set budget. Returned assistant reasoning can be retained
in native continuation; unavailable internal reasoning is never invented.

Local accepted candidates enter the existing integration owner via
`WorkCycle.integration.closeout_local` or the same CLI with `--closeout`, an
existing `--report-directory`, task definition and exact `--expected-head`.
Initial closeout authenticates bytes and scope, installs temporarily, runs the
shared checks and returns a review subject. `--review-json` binds Codex's
`ACCEPT_RECOMMENDED` rationale to that exact subject. Explicit `--commit` and
`--push` effects permit only an ordinary `feat/` branch; no model Tool can invoke
them. Duplicate publication verifies the exact commit/ref. Backlog progression
and protected target promotion retain the existing governed lifecycle.

Closeout admits `--additions-json` with a `files` array of independently authored
`{path,text,author,reference}` test records. Qwen candidate source cannot be
overridden through this entry. Use `--protected-validation` once on the final
installed tree; the exact subject-bound passing result is reusable for subsequent
review/commit. Feature push can bind `--expected-remote` when reviewed framework
commits are not yet published; divergent or moved refs refuse. Commit intent,
parent/tree and trailer reconcile interrupted publication without duplicate commits.
The same integration owner serves Codex and other trusted supervisors; no model
Tool has access to these effects.

Optional `--sampling-profile qwen-instruct` and `qwen-thinking` select the
manufacturer's explicit request settings for the corresponding thinking mode.
`baseline` remains the default and retains the actual server's metadata-derived
settings. A named preset is not evidence of better acceptance; measured results
and any differences are recorded separately. No weights, cache or resident
service are changed by this request option.

Git may rematerialize logically identical baseline resources with different
LF/CRLF bytes. The direct runner authenticates the frozen Git/content binding,
journals all baseline input resources under the existing owner, materializes
their exact frozen bytes for evaluation, and restores their original checkout
bytes afterward. Any difference beyond LF/CRLF equivalence refuses. Read/test
materialization is host-owned and grants no model edit authority over tests.

For the actual llama.cpp provider, active input is now measured with its same
native message/schema/template serialization via `/apply-template` and
`/tokenize` before inference. Input plus requested output plus 2,048 safety tokens
must fit 32,768. A 131,072-byte transport ceiling bounds selection independently;
it is not a larger model window. Non-provider scripted interactions retain the
conservative byte projection. The measured cohort documents why the old 36K-byte
cap refused a 14,923-token pending repair which fit the actual model window.

Maintained repository-local application composition now lives here. The existing
worker, native proposal admission, LF/CRLF handling, task configuration and
host-owned validation were relocated without changing their contracts. Framework
Context/RI, ModelInteraction, Tools, managed commands and filesystem primitives
remain in `src/devtools`. Legacy fixture helpers remain because the existing
patch-proposal CLI and deterministic acceptance still consume them; they are not
a generic Agent API.

`scripts/qwen/coding_worker.py` is the trusted local evaluation entrypoint. Its
invocation supplies bounded development authority without backlog promotion,
standing grants or interactive confirmation. It does not authorize production
publication. Historical Markdown and source
segment task definitions pin their original Git baselines; they are reproducible
evaluation definitions, not unresolved current defects. Complete evidence and
outcomes remain in `experiments/qwen/` and `.local/qwen-coding-worker/`.

The first task was accepted and its exact Markdown correction integrated; the
second task failed and received a separately attributed Codex production repair.
B-0048 is a separate accepted candidate, not integrated source. WorkCycle/delegation/integration now uses the canonical checkout and ordinary
branches under exclusive recoverable ownership. The worker applies only the
admitted source file in place, captures the candidate, and restores original
bytes; it never copies the repository or src tree. Validation binds imports to
the exact selected source. Historical task definitions require selecting their
actual baseline branch rather than substituting old bytes under a current HEAD. Old grants
are historical and cannot be reused at this new coordinator path.

## Native Context investigation

### Opt-in repository-map navigation

For existing on-demand tasks, host-selected `CodingTask.map_navigation=True`
adds the native
`repository_map(query, start)` Tool and `expand_source(unit, to="source")` mode.
Defaults and historical task-definition hashes remain unchanged. Orientation
uses the current task's admitted SourceSearchIndex declarations and existing
static reference analysis to construct the canonical typed core/map. Existing
map importance/BM25/RRF ranking supplies six-symbol pages. This is bounded scoped
orientation, not whole-repository coverage or a new automatic planner.

Each returned handle selects a server-held `choose_repository_map_disclosure`
option and native symbol. Its metadata is not a source observation. Exact
expansion uses `choose_repository_map_source_disclosure` against that same
snapshot/index, materializes the RI declaration range, and passes that exact
span through ordinary source observation/reference ownership. Declarations over
4,096 UTF-8 bytes are refused without partial exact-source claims; ordinary
bounded inspection remains available. Unicode, original line endings, decorators
outside the RI range and final-newline absence follow the Planning contract.

Every dispatch reauthenticates task source. An admitted edit discards the map
frame; old handles fail closed and fresh orientation can create a current frame.
Foreign/unknown handles cannot select source. No extra read/edit scope, source
store, parser, ranker, execution or publication authority is introduced.
Preparation time, orientation bytes, selected paths/native declarations, source
spans and disclosure identities remain in correlated raw Tool evidence. Existing
lookup/parent expansion and path inspection remain available and unchanged.

The integration is Codex-authored. Deterministic navigation tests use scripted
assistants and must not be counted as Qwen Tool-use or coding evidence.

`CodingTask.context_mode="on-demand"` selects investigation in the **same**
`run_coding_task` loop. Default `"prepared"` retains caller-selected disclosures.
Mode/read scope enter the exact task digest; original prepared definitions retain
their historical digests. The initial request contains the objective, boundaries
and admitted paths, rather than complete implementation/test files.

| Native operation | Arguments | Existing owner reused |
| --- | --- | --- |
| `search_source` | `query, mode` | file/symbol/window/mixed source index and ranking |
| `lookup_symbol` | `name` | exact qualified Python source-unit names; all matches retained |
| `read_source` | `path, version, start, end` | observed source + authenticated Context materialization; half-open character offsets |
| `expand_source` | `unit, to` | existing parent-symbol identity and class/file expansion |
| `source_relationships` | `path, version` | bounded static Python declaration references/direct calls |

Descriptors use the existing model/Tool composition; `ToolRunner` validates and
executes reads. No Tool provides shell, Git, writes, approval or publication.
`propose_edit` still admits one bounded contiguous replacement in the single
authorized file, with the established LF/CRLF safeguards. Predetermined tests
and the independent oracle decide acceptance. Failed valid edits remain current
for up to two corrections; no Codex replacement is supplied.

Read scope is source, tests and optional `read_paths` (exact Python paths), frozen
in `baseline_hashes` and `context`. At most 32 resources are admitted: this is not
unrestricted repository access or automatic obligation sufficiency. Explicit-
address discovery never enumerates `.local` or unrelated directories. Observation
is bounded at 131,072 bytes/resource. Drift, stale versions/units, aliases,
unauthorized paths and malformed calls refuse. Safe request-schema, unknown-unit,
stale-version and missing-parent mistakes return correlated actionable feedback
and consume their action without terminating sibling reads. Authority/alias/drift
failures remain terminal. Only an exact host-admitted edit
can refresh the snapshot. Results retain repository/snapshot/revision, source
versions/spans where applicable, explicit truncation and static-analysis limits.
For range reads, `span` describes the exact returned text; `parent` retains the
original whole-file unit identity/span/line metadata without rebinding that
identity to a smaller excerpt.
`revision` names the pinned assignment base; `snapshot`/`version` identify current
observed source, including a temporary host-admitted edit before any Git commit.

`Prompt.messages` carries user/assistant/tool roles, visible assistant content,
native calls and correlated results. llama.cpp serializes native chat messages;
opaque `ConversationRef` remains unsupported by this stateless adapter.
`PromptMessage` is invocation input, not a durable `ConversationMessage` or Memory.
The installed Qwen template advertises native Tools and call/result support;
no template, service or 32K profile change was made.

On-demand host ceilings are **24 total model requests**, three proposals and 32
read/check actions. Defaults remain three calls, eight actions, 4,096 output
tokens/call, 300 seconds/call and 900 seconds overall; the exact task may explicitly
reserve longer bounded work. Existing grants retain their actual limits.
Investigation consumes the same call/action budgets. After the action budget
only proposal Tools remain. Malformed native JSON, output-limit responses and
ambiguous provider outcomes terminate without automatic retry.
A version mismatch on an admitted, unchanged
read is returned as a correlated REFUSED Tool result, consuming the same action
budget. Qwen may obtain the actual version and make a new request; the host never
accepts CURRENT or silently retries. Drift and unauthorized paths remain terminal;
safe Context request shape/unit/range errors return correlated correction feedback.

### Source-grounded working set

The application projects its archived native exchanges into a bounded active
working set. Current editable source observations (including tails), the objective
and latest validation/refusal are retained. Older read-only excerpts may be
explicitly omitted for reacquisition only when the remaining budgets permit it.
Repeated identical text is referenced by its original Tool call; stale text is
explicitly marked and removed after a host-admitted edit. Redundant parent
metadata is projected away with the original Tool-message SHA-256 and call ID.
Exact raw requests, responses and Tool observations remain immutable in evidence.
This is task-local Context selection, not a Memory repository or inferred summary.

Complete assistant/call/result groups remain correlated. Lower-value complete
exchanges may be omitted explicitly; if current source and validation cannot
fit, selection refuses instead of silently dropping code. A prefix has no
priority over a later symbol. Scripted/non-tokenized interactions retain the
36,000-byte conservative fallback. Real llama.cpp requests measure actual
messages, Tool schemas and generation prefix through the installed template and
tokenizer; token-guided compaction precedes refusal under the unchanged 32,768
Context and 2,048 safety tokens. `capacity.json` records each measurement and
effective generation allowance. Cohort 01 full CSV histories were about 35.5K
bytes: the old 24K eviction, rather than the model window, discarded source.

Reads disclose at most 4,096 UTF-8 source bytes, exact half-open Unicode character
coordinates, current version, parent source identity, source length, valid range,
truncation and continuation start. An authorized out-of-bounds read returns a
correlated REFUSED result with bounds and consumes its action. Wrong versions
still refuse; unauthorized paths, drift and malformed calls remain terminal.
The returned span is identified by resource path/version and exact coordinates;
the parent source unit is never rebound to the smaller span.

Native edits additionally require old text within the union of actually observed
current source spans. Existing exact/unique LF/CRLF-safe admission remains intact.
No approximate edit is applied. Nonunique or unobserved text returns no-effect
feedback within the same three-proposal bound. After admission, old source
observations are invalidated. Previously observed portions outside the exact edit
are refreshed only after exact-text verification against the current source;
their original read/version/span and admitted edit remain referenced. Unseen or
changed text is never inferred. The exact admitted replacement becomes a
correlated current observation available for repair.

Host task definitions may freeze `quality_checks: true`. Acceptance then requires
the existing tests, independent oracle, scoped Ruff and formatter checks. Complete
logs remain archived; bounded Ruff diagnostics and formatter diff join existing
native validation feedback for repair. Legacy false/default configurations keep
their original definition digests and do not retroactively change prior outcomes.

Repair feedback identifies each check as behavior, regression, lint, formatting
or typing, records the evaluated source version, and repeats the frozen public
requirements alongside already-passing checks. A lint suggestion cannot override
the task's API or exception contract. All required checks must pass on the same
candidate. Complete logs remain separate from this bounded projection.
When the test runner has captured structured primary failures, repeated pytest
tracebacks are replaced by those facts and the outcome tail; nonduplicate stderr
and explicit truncation remain. A source-preserving working-set refusal is
reported as `CONTEXT_BUDGET_FAILED`, rather than attributing it to the last Tool.

Before freezing a new task, review public behavior and exception compatibility,
legitimate alternative implementations, independent acceptance, existing tests,
Ruff, formatting and typing together. `--preflight-only` runs baseline checks and
strict scoped mypy without inference; its successful disposition still requires
this engineering review and is not a proof that arbitrary specifications are
satisfiable. It adds no execution approval gate. Cohort definitions can include
fixed managed typing checks in their independent oracle.

`--thinking enabled` explicitly selects the existing model template's reasoning
option for a measured local evaluation. The default remains disabled. No model,
chat template, serving process or context-window change is implied. See
`evaluation/native-cohort-03/` for the frozen development comparison.

## Execution and inspection

### Coordinated source edits and installed API contracts

For simpler native editing, select `--observed-edits` (or
`observed_edits=True, coordinated_edits=True` on `run_local_task`). Source
observations return short task-local `edit_ref` handles. The flat native Tool is
`replace_source(reference, old_text, new_text)`: the host resolves paths, exact
versions and required installed-API observations. Empty old text selects the
whole observed span, or an explicitly authorized absent new file. Nonempty old
text must still match exactly. Multiple calls in one assistant response form
one atomic transaction through the existing admission/application path.
No approximate matching, suffix repair or partial mutation is permitted.

Atomic refusals retain the existing `PatchProposalError` and public Tool error
classification. Additive `details` identify the original **one-based** component,
authorized path, native proposal call ID and stable reason code. Region and
aggregate measurements are UTF-8 bytes (including adapted newline measurements
when relevant); overlap diagnostics name both original component indices. A
combined source/patch bound can instead identify all contributing components.
`observed_match_count` counts overlapping occurrences only in the union of current
disclosed spans for that path. It is not a whole-file or cross-owner search result.
Unobserved source identities and unauthorized path information are not disclosed.
Path/reference resolution precedes transaction admission; the first blocking
failure in that existing order is reported. Raw requests remain unchanged and
every retained native call receives its correlated all-or-nothing refusal.
Host-integrity failures (including unexpected new-slot occupation) remain terminal;
no failure is converted into permission to repair or apply an approximate edit.
See the [Codex diagnostics delivery](evaluation/edit-diagnostics-codex/README.md)
for the deterministic native repair proof and its limits.

`inspect_source(path, start)` resolves the current authorized source version
and returns at most 4,096 UTF-8 bytes, source length, continuation coordinates
and an observation handle. It reuses Context disclosure and grants no edit
authority. Historical versioned reads, single-edit and nested transactions
remain compatible. Safe unknown-unit/empty-version mistakes produce correlated
bounded feedback; authorization and source-drift refusals remain enforced.
See [editing comparison 06](evaluation/editing-06/README.md) for measured results.
The simpler interface is opt-in; historical receipts are unchanged.

In this mode, `inspect_source` is the sole disclosed range-reading operation;
version-heavy `read_source` and redundant `inspect_new_source` remain available
in historical mode. Truncation reflects remaining source, not just a capped
request. Continue at the returned character offset; each payload is at most
4,096 UTF-8 bytes. Empty existing files and authorized absent files are distinct.
`ContextRequestError` is an application-local request refusal, not a new framework
failure protocol. Recovery checks source integrity before returning feedback;
source drift or unauthorized access is not reinterpreted as a harmless typo.
See [investigation comparison 07](evaluation/investigation-07/README.md).

Trusted local tasks may explicitly declare `additional_edit_paths` (at most
three existing implementation files under `src/devtools/`) and `api_targets`.
All edit and read resources remain frozen by baseline revision/content hashes;
tests and oracles remain host-owned and immutable. Select `--coordinated-edits`
on the same CLI, or `coordinated_edits=True` on `run_local_task`. Historical
single-edit definitions/digests and the default legacy invocation remain valid.

The native `propose_edits(plan, api_evidence, edits)` operation carries a brief
compatibility/implementation plan and up to sixteen exact observed anchors. Each
component names its authorized path, exact current source version, old text and
replacement. Empty replacements support anchored deletion. All components refer
to one pre-edit state; stale, unobserved, ambiguous, overlapping and unauthorized
anchors refuse before mutation. Existing exact LF/CRLF admission is reused.
Each region remains bounded by 4,096 UTF-8 bytes, with 8,192 combined old/new
bytes and a 16,384-byte combined patch cap: multiple regions do not enlarge the
legacy aggregate text budget. The Checkout owner journals every file expectation
before one native Git apply/check operation. Per-edit provenance, combined diff,
all candidate source hashes and interrupted/restored state remain in the existing
`qwen-coding-loop-v2` evidence. No parallel editing engine was introduced.

`inspect_api(target)` uses ToolRunner to observe a fixed host-allowlisted installed
stdlib object's actual signature/docstring, package/runtime version, truncation
and observation digest. It permits no model-selected imports, object traversal,
API execution or arbitrary Python. Initial supported targets are JSON loads and
decoder contracts, regex Pattern finditer/search/fullmatch, bytes.decode and
str.encode. JSON loads observations also disclose the actual delegated decoder
signature; this exposes unsupported keyword assumptions without supplying a
completed implementation. The task selects permitted and required targets.
Transactions cite genuine observation IDs covering those targets; the host
authenticates observations, not the semantic correctness of the model's plan.

Source and API observations remain correlated and deduplicated in bounded active
Context. Current tested source versions across the edit scope and passed/failing
behavior/quality obligations accompany repair feedback. Validation and cleanup
cover all authorized files; unknown bytes require reconciliation. The existing
one-file governed assignment-v1 refuses multi-file preparation; local capability
does not silently expand production execution or integration authority. The
dashboard displays either proposal shape through the same read-only raw evidence.

A read/API batch exceeding a positive remaining allowance is refused as a whole,
with one correlated result per call and no Tool dispatch. The model may select a
smaller batch within its original call/time/action limits. Requested, dispatched
and returned actions remain distinguishable; eight actual dispatch attempts are
still the maximum, including version refusals. Requests after total exhaustion
remain terminal. This permits bounded recovery without refunding actions or
silently increasing the task budget.

The existing CLI also accepts a trusted host task definition:

```powershell
uv run python scripts/qwen/coding_worker.py --task-definition .local/backlog/preparation/WORK/task.json --report-directory .local/qwen-coding-worker/NEW-RUN
```

Trusted invocation is local evaluation authority, including for an explicitly
selected historical baseline; model-authored task JSON is never authority.
Paths/config are checked before source or service effects. The CLI selects or
creates an ordinary `feat/qwen-local-<task-hash-prefix>` branch at the exact task
base, uses the existing exclusive Checkout owner, restores source and returns to
the original branch. `--branch` can name another ordinary feature branch at that
same base. Dirty/index/collision checks remain enforced. Reusing a report directory
refuses before dispatch. There is no confirmation prompt or `--yes` switch.
Delegated WorkCycle execution uses its existing exact-task review, reservation,
source owner and per-call guard without redundant consent. Reads must fit the
standing source/test scope; publication remains separate. Never reuse an old
path-bound grant or redispatch an existing work slot.

Existing `qwen-coding-loop-v2` captures remain the evidence contract. Each turn
retains request/response JSON and hashes, native IDs, `tools.json` call/results,
versioned selections, diffs, full validation logs, bounded feedback, UTC timing,
usage and termination. Selection never erases archives. Repairs count proposals,
not investigation requests. The existing dashboard consumes these same records
behind raw-data disclosure controls. Optional framework observation honors
independent prompt/call-argument capture policies for native input history.
Text-only Context assemblers explicitly refuse structured input rather than
discarding history. No second transcript or authority store was introduced.

[Evaluation and authority status](EVALUATION.md) separates scripted acceptance,
live read-only conformance and still-unmeasured live coding efficacy.

## Explicit maintained application task scope

CodingTask may bind exact Python paths in src/devtools/ or apps/, with tests/
remaining read-only acceptance. Canonical addresses, pinned revisions/hashes,
explicit read/edit/new slots, existing byte/budget bounds and Checkout ownership
remain mandatory. Model output cannot expand those lists. Application validation
runners add the canonical checkout root and verify the actual imported module
path; integration uses the same local import rule. Framework source must not
import apps. Historical task definitions/receipts and grants remain unchanged.


### Public task semantics and preparation artifacts

Host task objectives must state essential normative facts (such as top-level
TOML ownership and permitted roles), rather than expect retrieval of unavailable
external specifications or private oracles. Independent diagnostics should name
expected versus observed behavior without revealing a reference implementation.

Keep frozen local task/oracle/evaluation preparation in ignored `.local/` until
post-run publication. Untracked artifacts under `apps/`, `src/` or `tests/` can
correctly block check_changes as outside the authorized edit scope. Qualification
must verify initial Git scope as well as native Tool registration. Do not weaken
the guard or claim a blocked native report is a pass. A later supervisor-only
check is separately attributed; WorkCycle must reauthenticate final source.

Capacity projection factors search-match repository/snapshot/revision fields
only when all exactly match the result envelope. Omitted fields inherit that
envelope or its existing correlated reference; explicit mismatches remain.
Paths, units, versions, spans, ranking, exact source and latest diagnostics stay
intact. Raw native results are archived and projected history grants no new
observation or edit authority. Current source and reports remain bound to their
exact task/Checkout state, not arbitrary future branch commits.

Generated exact-source patches preserve an absent final line terminator using
Git's standard no-final-newline marker. The patch store does not thereby grant
normalization authority; proposed and installed bytes must still match exactly.
