# Bounded local coding worker

Host tasks may opt into `path_edits=True`: flat `replace_source(path, old_text,
new_text)` resolves nonempty exact old text against the union of current disclosed
source spans for an authorized path. The existing transaction engine still
requires a unique source occurrence and enforces version, scope, overlap and byte
limits atomically. Empty old text is admitted only for observed authorized absence.
Legacy reference calls retain their original strict region semantics; they are
never redirected to a different observation. Default task hashes and three-edit
budgets remain compatible. Native tasks may prospectively select
`maximum_proposals` up to six (default three), without expanding calls/time/actions.

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
Native assistant/call/result associations remain complete. No LLM summary or
new Memory store is involved. Investigation continuations reserve at most 4K
output; initial implementation and edit/repair continuations target the frozen
ceiling, with a 4K minimum fallback and the unchanged 2K safety allowance.
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

Explicit `new_paths` admit existing-parent Python implementation files only.
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
provided at least 4,096 tokens remain after the unchanged 2,048-token safety
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
