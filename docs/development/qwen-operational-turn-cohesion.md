# Qwen operational turn cohesion

This delivers one behavior-preserving application extraction under existing
proposal `39c6663a-bab7-43ed-8166-82e780a75d05`. It adds no agent capability,
authority, larger limit or framework lifecycle.

## Accepted identities and scope

Authenticated starting local/origin/remote main: `0b8331e645d8d9bf71e0f751aae90ee5e9dc7f82`. Production commit
`cd0a8330282d9b074ccb6d5dbf80a0f8c963c6ff`, tree `a275778ccd548514f020ef5cf2c4f260ab1cfb59`, merged normally through PR #45 to independently
verified source main `abe1ca13fbb5960f937383bb9e257ce05fe14f22`. The [machine receipt](../research/code-audit/qwen-turn-cohesion-20261027.json)
retains baseline path/blobs, physical gate inputs, exact commands, timestamps,
durations, exits, environment, new-version review and accepted ancestry. Later
documentation/Intake integration preserves those executable inputs.

The tracked/index tree began clean; the only untracked files were the thirteen
preserved source-grounding forensic files. Checkout ownership was absent. All
thirteen hashes, 903 retained RI JSONL rows, original historical refs and frozen
experiment inputs remain preserved. No model/service/scientific execution,
worktree, clone, backup source tree, reset, force push or ref deletion was used.

## Existing responsibility and consumer map

| Responsibility | Original owner/actual consumer | Resulting owner |
| --- | --- | --- |
| Immutable task and preflight | tasks.CodingTask; CLI and WorkCycle select trusted tasks, coding_loop preflight/authenticate | Unchanged |
| Model requests, response source and bounded turn sequence | coding_loop._turns; actual run_coding_task and direct maintained tests | turns.loop.run_turns through the same _turns signature |
| Initial host Prompt and measured input projection | Inlined _turns instructions/capacity; continuation.select_messages/present_sources own selection | turns.prompt.initial_history/fit_capacity; canonical continuation unchanged |
| Context acquisition and disclosure | coding_loop.acquire_context; ContextTools -> RI/Context/ToolRunner | Unchanged APIs; loop retains actual ContextTools instance/history |
| Required/helpful evidence and readiness | obligations.NativeObligations project/admit/retain | Unchanged, called at the same request/edit boundaries |
| Authorized read/check dispatch and feedback | Inlined _turns calls ContextTools/CodingCommands, correlates native IDs | turns.tools.dispatch_context_calls; same task/action budget and authoritative Tool/check owners |
| Exact edit admission and Git application | edits admission, development_task.apply_source_patches, _turns coordinator | Existing owners unchanged; turns.loop coordinates once |
| Fixed checks and repair | CodingCommands/change_checks; coding_loop.validate_workspace/_validation_feedback | Same callable facade adapters explicitly supplied to turn implementation |
| Candidate archive, restoration and unknown bytes | run_coding_task finally; Checkout callbacks/adapters outside worker | Unchanged coordinator body |
| Terminal disposition, acceptance and usage | run_coding_task exception/final accounting; actual CLI/WorkCycle/local-closeout consumers | Unchanged coordinator body and serialized fields |
| Review/publication | WorkCycle, Checkout and integration; coding_worker entry point | Unchanged, separate from candidate/Context readiness |

`scripts/qwen/coding_worker.py` and `scripts/backlog/work.py` still call
`coding_loop.run_coding_task`; local integration still calls its existing
`_prepare_workspace`/`validate_workspace`. The private `_turns` adapter remains
because the coordinator and real maintained direct callers/fault schedules use
that seam. This is one delegation adapter, not a second turn implementation.

## Selected extraction and package

`apps/qwen/turns/` contains `loop.py`, `prompt.py`, `tools.py`, an export-only
`__init__.py` and its ownership README. It is application composition, not a
generic Runtime, planner or reusable framework protocol. No framework source
depends on the application.

The loop owns the existing local history/counters and invokes existing admission
and validation mechanisms. The prompt owner builds initial instructions and fits
the same selected input using actual llama.cpp token measurements; it does not
perform generation. The Tool owner consumes one already classified authorized
batch and returns its action count, retaining the actual shared history/stage/
report objects. There is no additional mutable session copy, global registry,
result wrapper or new persistence schema. The concrete acquisition, validation,
feedback and projection callbacks make existing seams explicit without a new
protocol hierarchy or a circular import back into the facade.

Moving the whole turn body alone would have left its new owner oversized.
Prompt/input projection and fixed Tool dispatch are cohesive existing operations;
they were extracted on those boundaries rather than split into line-count chunks.
No simultaneous development_task or ContextTools decomposition was attempted.

## Behavior and compatibility evidence

The original `_turns` signature is identical. Seven original coordinator/helper
function bodies, including all of run_coding_task and its terminal handlers/finally,
match the starting AST. Inlining the extracted bodies reconstructs the original
turn AST, ignoring local type annotations and mapping the explicit aliases/early
batch return and output-ceiling placement back to their original scopes. This
checks statement/refusal/persistence ordering as well as literal instructions;
it is structural evidence alongside independently specified behavioral tests.

Tasks.py, ContextTools, continuation, obligations, edits, commands, checks, CLI,
WorkCycle and local integration source are unchanged. Existing task serialization,
definition hashes, native request/call IDs, frozen inputs, qwen-coding-loop-v2 result
fields, all byte/token/action/call/proposal budgets and authority remain unchanged.
Existing private monkeypatches follow the actual new module owners; their
assertions and fault schedules remain. Public worker/preflight/acquisition/check
imports and the real local-closeout seams remain at coding_loop.

Two new maintained public-worker cases were added and run before production edits.
They independently specify prepared/native success, exact task/result identity,
original-source restoration, retained literal candidate, actual source disclosure
and native call correlation. Existing tests protect validation-feedback repair,
invalid/foreign source response, refused edits and frozen-input drift, CLI status,
and independent local/governed admission.

All 53 existing native-obligation cases remain in the focused/full runs: mandatory
missing/high-relevance refusal, helpful nonblocking, exact current source/coordinate
coverage, partial/foreign/conflicting witnesses, acquisition within existing budgets,
active compaction and stale-source refusal, no model-created scope, valid/invalid
edits, shared checks, actual CLI custody and known-evidence retention.

Terminal controls retain known provider/Tool/Git effects without redispatch,
unknown usage and provider completion, validation cancellation, completion-stage
record failures after candidate checks, final result-write failure after
restoration, unknown installed bytes and failed restoration. Passing candidate
evidence remains distinct from final worker completion; Context readiness does
not grant edit/review/publication authority. No observer, retry or recovery policy
was implemented.

## Self-editability and limitations

Exact before/after raw and normalized UTF-8 sizes are retained in the receipt;
the package README defines ownership and bounds. Starting coding_loop was 73,482 physical bytes, exceeding the
unchanged 32,768 resulting-source bound. It and all extracted Python owners now
fit that bound, including their normal CRLF representation. The existing
development_task remains 60,528 physical/59,089 normalized bytes and ContextTools
39,019 physical/38,106 normalized bytes; both remain oversized.

| Owner | Starting physical / normalized bytes | Final physical / normalized bytes | Final CRLF bytes |
| --- | --- | --- | --- |
| coding_loop.py | 73,482 / 73,482 | 30,617 / 30,617 | 31,380 |
| turns/loop.py | New owner | 30,025 / 30,025 | 30,746 |
| turns/prompt.py | New owner | 11,407 / 11,407 | 11,661 |
| turns/tools.py | New owner | 7,260 / 7,260 | 7,453 |
| turns/__init__.py | New export only | 157 / 157 | 163 |

New physical files and the original coordinator use LF; the comparison explicitly
retains the actual starting physical/normalized sizes and conservative ordinary-CRLF sizes. The coordinator's CRLF margin is
1,388 bytes and the loop's2,022; prompt/Tool owners have more room. Total code size
is not claimed to shrink: explicit interfaces, ownership documentation and imports
trade some text for clearer responsibilities and bounded individual sources.

This is measurable source-admission progress, not proof a model can autonomously
perform this refactor or arbitrary edits. Each old/new region remains at most
4,096 bytes, aggregate old+new at most8,192 and combined patch at most16,384;
Context/action budgets and edit scope still apply. A whole-file replacement of
these larger owners need not fit one proposal even though a small exact edit can
meet the resulting-source limit. No limit was raised.

## Validation and qualifications

Final committed protected gate: **3284 passed, 2 optional live skips,
100% configured production branch coverage**, exit0, recorded 1174.10877 seconds.
The protected selector, exclusions and thresholds are unchanged. Supported Ruff,
formatter, strict mypy, layout and focused operational/obligation/Context/ToolRunner/
Checkout/WorkCycle/closeout tests pass. Exact selectors and per-case focused
outcomes, bounded post-main checks, physical hashes and versions are in the receipt.
JSON/JSONL, local links, Intake chains, original overlay fields, whitespace and
forensic/ref preservation are independently checked.

The original baseline passed198 cases; one new assertion initially expected
`read-tiny`, whereas the actual deterministic fixture emits `tiny-0`. Corrected
characterization passed both modes before production changes. The first strict
mypy run required an explicit heterogeneous `result` annotation after removing
the old earlier declaration with Tool dispatch. The AST harness initially put the
restored output ceiling at the wrong syntactic depth; correcting that comparison
established exact equivalence. These are recorded development/harness issues,
not new product defects or reasons to weaken assertions. No live effectiveness,
universal environment closure, all-application branch coverage or runtime-efficiency
improvement is claimed.

## Canonical disposition and remaining work

The sole existing39c6663a proposal receives append-only implemented-and-merged
ADVISORY evidence for this bounded slice. Its administrative PENDING_REVIEW,
parent ownership and remaining development_task/ContextTools obligations stay
open. Original Qwen17-body frozen review/probes and two earlier maintenance
overlays retain their exact historical meanings; new/current blobs have separate
maintenance evidence rather than inherited full review credit.

The next justified cohesion boundary is the live task/patch/check mechanics in
development_task versus retained experiment/controller composition: first map
actual consumers and compatibility, then separately authorize an owner-local
extraction without moving Checkout custody or increasing limits. ContextTools
needs its own dependency/cohesion decision. The next comprehensive application
review can cover the remaining dashboard/operator surfaces when separately
assigned; it was not started here.

B-0028/B-0034/B-0011/B-0023 task recovery and Evidence remain separate. A+C is
unapproved, and the limited host-frame integration was not broadened. Observation
OptionB remains unimplemented pending per-invocation correlation, secondary
reporter-failure handling, privacy/retention and mandatory-versus-optional evidence
admission. RI93/93 fixtures and606/606 experiment-path dispositions retain their
qualified scope;188 older versions remain a separate assurance program. No next
cohort, live experiment or successor-session dossier was launched.
