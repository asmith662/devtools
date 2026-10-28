# Framework-first migration 3 delivery

The reusable bounded coding Agent is delivered in production `22c44a88fa20da8d580b1470441030c80835b7d0`,
tree `ee61df0307f934d14c1e20bbc4faccd0a4524c6d`, normal PR #52, independently verified source main `a23c081cefb7524471a26a8f539356fa2545a38e`.
Starting main was `172f49b2d01e4821cc619b02d520cac99ff0f23a`, tree
`8f4980bca7a131e2df8a4babf485370cc146ef5b`; local, origin and independent remote
observations agreed. One canonical checkout and ordinary branch were used.
This assignment explicitly authorized migration 3, not migration 4 or a universal
agent architecture. [Public contract](bounded-coding-agent.md) and
[exact machine evidence](../research/code-audit/bounded-coding-agent-20261027.json).

## Ownership and actual reuse

| Responsibility | Delivered owner | Reused foundations / remaining host authority |
| --- | --- | --- |
| Bounded coding sequence | `agents.coding.process.run_coding_agent` | One ModelInteraction, native Prompt/response, explicit host phase seam; finite calls/proposals/actions, repair and stop, source and native ID admission, terminal reconciliation |
| Neutral objective and candidate facts | `agents.coding.models`, `repository.CodingObjective` | Existing SourceScope, RepositoryResourceAddress, FixedCheckPlan, Duration and ModelUsage; no Qwen task/profile/default provider |
| Source acquisition and feedback | `RepositoryCodingHost` | RI observations/discovery/corpus/SourceSearchIndex, Context range plans/materialization, ScopedSourceTool, native model/Tool composition and ToolRunner |
| Exact edit admission | `agents.coding.edits.replace_exact_text` plus repository host | Promoted literal anchor/line-ending/size mechanics; actual disclosed current spans, whole-batch overlap/path/byte checks; language/API/new-file/Git policy stays with host |
| Effects and fixed validation | Explicit host callback and `FixedCheckTool` | Existing Resource writes or host-selected managed Git, ToolRunner and CommandExecutor; no second executor, arbitrary model command or implicit retry |
| Candidate custody | `SourceCustody` with host archival/restoration | Canonical ContentIdentity and bounded Resource reads; known-source recheck/restoration verification; unknown bytes refuse cleanup; no Checkout authority or transaction |
| Qwen compatibility | `apps.qwen.turns.loop._LegacyHost` and thin `run_turns` facade | Legacy prompts/capacity, task/readiness/oracle/journal policy, existing scope and native operations; no separate model send or repair loop |

The coding process receives one host composition per invocation. `CodingHost` is
one coding-specific typed seam with two real consumers, not a BaseAgent, workflow
engine or configurable execution DSL. New modules contain no app/script/experiment
imports and no provider-specific branching. Models and Tools remain independent;
their composition stays in Agents. Runtime/Conversation and Codex external-Agent
semantics are unchanged.

## Qwen adoption and compatibility

Prepared and native `run_coding_task` actually enter the same framework process as
the independent host. Boundary instrumentation proves one entry and expected
model/proposal counts, real candidate archives and known-source restoration.
A forced shared-entry fault produces the original failure; there is no app-loop
fallback. Both Qwen literal edit admission and outer source restoration delegate
to promoted mechanics. Existing task hashes, native names and IDs, v2 field names,
fixed command/oracle selection, source caps, action/refusal order, journals,
readiness, CLI accepted/disposition semantics, Checkout and WorkCycle/local-closeout
authority remain compatible. Public entry signatures and task hash owner are
unchanged. No limits were increased.

The application adapter still owns legacy request/capacity presentation,
application-specific refusal/feedback records, Python/API/new-file policy and
governed closeout. It contains no independent model/repair sequence. This is
substantive independent framework behavior, not the Qwen loop copied into src.
Application cohesion remains open; production file sizes and exact changed blobs
are retained in the receipt rather than claiming the oversized app owners solved.

## Independent full engineering task

Thirty-six literal schedules run under guards refusing application, script and
experiment imports and checkout file reads outside framework/dependencies and the
independently authored test support. Explicit attempted Qwen import/file access is
refused before contents are read. The host requires no CodingTask, Qwen profile,
prompt, journal format or historical controller. It supplies configuration and
effects; `run_coding_agent` is the sole coding/repair loop in both compositions.

The representative repair observes an authored temporary Git repository, acquires
exact Unicode source under native call `read-1`, applies an admitted incorrect
`edit-2`, receives a real fixed Python check exit1 and current-source/version
feedback, then applies `repair-3`. The same immutable argv returns exit0 with
literal `checked:7\n`. Three model calls, two applications and two checks occur.
The archive contains the exact return7 candidate and the working source is restored
to return6. The test independently asserts actual disclosed text/span, source and
snapshot identities, native feedback IDs, changed-source correspondence, exact
command and outcomes. Usage remains `None` for all three calls.

Controls cover missing/partial Context, required-readiness refusal, unauthorized
paths/operations, stale source, bad anchors, duplicate/overlapping/oversized edits,
budget exhaustion, foreign model source, invalid native IDs, partial Tool batches,
failed checks, cancellation, lost file/Git/check acknowledgment, feedback and
completion failure, failed restoration and unknown installed bytes. Known earlier
effects remain retained and ambiguous effects are not retried. A primary effect
failure remains distinct from secondary completion failure. No harness/setup
failure is reported as a product defect.

## Outcome, recovery and authority limits

Candidate validation is a factual check result, not worker completion. A fatal
feedback/archive/restoration failure prevents unconditional accepted success while
retaining the known candidate/check evidence. Native Tool dispatch is charged
before entry and never refunded on an exception. An unacknowledged dispatch does
not prove absence of an effect; known returned checks remain available. Unknown
installed bytes are archived/retained for reconciliation rather than overwritten.
Existing terminal/cancellation/CLI and closeout regressions protect these facts.

The default neutral profile supports existing UTF-8 text. New-file/language/API
admission remains an explicit host specialization; Qwen preserves its established
policy through the same generic process. Resource writes are individually atomic,
not a cross-file transaction. SourceScope and custody checks do not promise an
atomic filesystem snapshot, cross-process exclusion or universal validation-input
closure. Hosts retain source serialization, Checkout, bounded cleanup and effect
authority. Fixed checks and Context readiness do not certify independent review,
protected validation, destination acceptance or publication.

Continuation and effect notes are transient, not durable restart/checkpoint or
exactly-once recovery. Existing Evidence/usage/Conversation persistence is not
silently extended. Observation Option B remains unapproved: per-invocation
correlation, safe secondary-report failure, privacy/retention and mandatory versus
optional evidence admission still need explicit decisions. No A+C expansion,
provider, retrieval engine, Evidence store, automatic replay or migration 4 was
implemented.

## Validation and evidence

- Original actual Qwen/edit/obligation/WorkCycle/local-closeout characterization:
  208 passed, exit0, 344.000769s managed elapsed, baseline main above.
- Migrated workflow diagnostic:299 passed, exit0, 402.691309s managed
  elapsed. Its explicit nongating coverage diagnostic did not
  change the protected profile or threshold.
- Final focused framework, guarded/direct independent hosts, actual Qwen
  delegation, Model/Tool, source/check, Codex, CLI, obligation and Checkout tests:
  304 passed, exit0, 185.031375s managed elapsed.
- Final committed protected command `uv run python scripts/validate_development.py`:
  **3498 passed, 2 optional live skips,100% configured production
  branch coverage**, exit0, 1433.341071s managed elapsed on the production commit
  and exact physical inputs in the receipt. No threshold, exclusion or test
  selection change. Protected framework coverage is not full app coverage or
  proof of live autonomous effectiveness.
- Supported Ruff, formatter, strict mypy563 source files, layout, links,
  JSON/JSONL/Intake and whitespace checks passed. Post-source-main bounded checks
  passed with matching accepted blobs and physical executable inputs.

Python3.14.3, SQLite3.50.4, Windows11, Git2.53.0.windows.2, uv0.12.2,
Ruff0.16.2, mypy2.3.0 and pytest9.1.1 were observed. No new supported-runtime matrix,
live inference, model/server startup, API expenditure or scientific replay was
performed. The receipt captures commands, tool versions, UTC timestamps, exits,
timings, per-file blobs, raw physical hashes, test cases and actual independent
host effects. It explicitly preserves failed harness attempts and their corrections.

## Canonical disposition and remaining work

One append-only delivered ADVISORY uses existing39c6663a/B-0035/B-0043 ownership.
Administrative PENDING_REVIEW, story status/maturity, parent scopes and existing
approvals/grants remain unchanged. Changed-version Qwen maintenance overlays
preserve original frozen fields/findings and earlier overlays without transferring
old review credit to new blobs. No duplicate proposal or B-number was created.

All13 original forensic files,903 RI ledger rows, original experiments and authored
historical refs are preserved. The188 historical RI-version obligations remain a
separate assurance program. Broader validation-input closure and B-0011/B-0023/
B-0034/B-0028 recovery/Evidence obligations remain open; A+C remains unapproved.

The next justified decision is the already-planned evidence/host convergence:
select one real producer-consumer join, define task/invocation/source correlation,
unknown/capture and privacy/retention semantics, then reuse existing Observability/
usage and host admission. Decide the four Option B conditions separately before
changing ModelInteraction. Do not assume a new store, automatic restart or generic
orchestrator is necessary. No migration4, dashboard audit or successor dossier was
started during this delivery.
