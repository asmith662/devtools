# Maintenance-navigation-0001

## Verdict

One real Qwen3.8-27B attempt failed B-0035 without proposing an edit. The worker
spent all ten requests paging global symbol metadata at offsets 0 through 72.
No query/path/mode selection, source read, edit proposal, validation, repair or
semantic summary occurred. `accepted=False`, terminal `model_limit`; candidate
archive equals all eight frozen source files. No model-authored code is accepted.

This is not improved source efficiency: zero source acquisition means no exact
implementation investigation. The interface is operational, but this one model
trajectory did not use it productively. No second attempt or supervisory patch
was substituted.

## Authority and frozen inputs

Framework baseline: `eb053c735c7edbdfb8058170adfc3786fcf28fa3`.
Protected implementation: `e3be8f8e7890ede763ba5770c7ac08621c57d294`.
Freeze source: `f90f2744c4288518c37a3465c26e5dbdfceee73c`; execution commit:
`a3fd27cb10dce79abd05c176a9375bed2bf733b2`.
Freeze digest: `fe0d91966f94c7359305389d20b48aafc3cf0c7156d11b726b70e49ab9b318cb`.
Snapshot: `6300d3faeac903096664845691cc350cb547522b130547bbc33f65a6f82e26f8`.

[Freeze](freeze.json), [protocol](protocol.md), [preflight](preflight.json) and
[objective](objective.md) were retained before inference. The genuine backlog
obligation remains first-request authorized inventory. It was not manually
implemented during navigation work. Independent oracle controls passed ten
reference/negative cases and established the same three focused/five withheld
baseline failures. Source-size feasibility was checked under unchanged limits.
The reference and withheld files were outside the 17-resource read scope.

The installed Qwen3.8-27B UD-IQ4_XS artifact, image/profile, alias and 32K service
capacity were authenticated by the controller. Exact settings and artifact hash
are in the freeze. No download, provider substitution, paid call or service
mutation occurred. Qwen is the selected interaction, not an Agents dependency.

Ten acting calls maximum, four proposals, three admitted candidates/two natural
repairs, twenty acquisition actions, 150-second calls, 1,080-second process and
1,200-second outer window. Input cap 28,160 provider tokens; output 4,096 tokens;
complete-request and resulting-source bounds 32,768 bytes. Disclosure 8,192,
edit-region 4,096, aggregate 8,192 bytes/two operations. Deterministic projection
24,576/20,000; no auxiliary model configured. No limits or oracle changed.

## Actual interaction

| Request | Outline offset | Sent bytes | Input tokens | Output tokens | Inference seconds |
|---|---:|---:|---:|---:|---:|
| 1 | 0 | 5,224 | 1,268 | 14 | 7.893 |
| 2 | 8 | 9,873 | 3,582 | 26 | 3.700 |
| 3 | 16 | 14,619 | 6,060 | 27 | 3.832 |
| 4 | 24 | 19,220 | 8,536 | 27 | 4.052 |
| 5 | 32 | 23,740 | 10,927 | 27 | 3.985 |
| 6 | 40 | 18,944 | 8,612 | 27 | 16.758 |
| 7 | 48 | 19,194 | 8,916 | 27 | 9.636 |
| 8 | 56 | 19,337 | 9,027 | 27 | 13.290 |
| 9 | 64 | 19,460 | 9,123 | 27 | 11.840 |
| 10 | 72 | 19,302 | 8,908 | 27 | 11.495 |

All requests received normalized native `find_source` calls with distinct IDs.
The shared navigation Tool returned eight current metadata units per call:
80 units total, 72 presented in subsequent model requests. The final page was
retained but never consumed. It contained `RepositoryCodingHost.build_request`
at `[11495,12239)` and `prepare` at `[12247,16586)`; earlier pages included
focused-test symbols, custody, edits, process and projection metadata.
These were metadata coordinates, never disclosed source or edit witnesses.

The model did not choose task-directed search, path narrowing, file/window mode,
`read_source_unit`, generic reads or the available inspect-and-validate procedure.
There is no evidence that it understood the target implementation. The tenth
metadata result cannot be credited as model-consumed Context.

Projection began omitting old metadata at request six. Complete retained input
grew to 47,268 bytes; the final active request was 19,302. Peak sent input was
23,740 bytes. All native Prompt correlations and objective text verified.
No source witness was acquired, retained, evicted or falsely credited in this run.
No repeated source reads occurred because there were no source reads at all.

Known provider totals: 74,959 input and
256 output tokens. Cached/reasoning usage is
unknown for every request, not zero. Inference elapsed 86.481080
seconds; coding process 87.411954 seconds. Auxiliary calls: zero.

## Independent assessment and custody

[Verification](verification.json) rechecks the frozen snapshot against current
authorized source, each returned unit's literal identity/name/span/size, all
native Prompt boundaries, exact request accounting and unchanged candidate hashes.
[Candidate archive](evidence/candidate.json) preserves exact bytes as UTF-8 with
hashes. SourceCustody restored known source; the model-run Checkout released.
All ten acquisition acknowledgments are known. No edit, command check or unknown
worker effect is inferred. Command observations retain only actually observed
host Git/service operations; navigation is a Tool operation, not a subprocess.

The independent focused XML has one pass/three failures; held-out XML has one
pass/five failures, exactly the preflight failure sets. The unchanged candidate
does not satisfy inventory behavior. These grading tests are supervisor-triggered,
not feedback consumed by the acting model.

There was a separate supervisory closeout error: retained artifacts were copied
into the untracked experiment directory while the grading Checkout was active.
Its guard correctly refused release. The grading process exited; source remained
exactly baseline. Only the newly generated artifacts were moved to ignored storage,
preserving their bytes and restoring the original thirteen-file untracked set.
The stopped-owner receipt and recovery outcome are retained separately. Both test
XMLs survive, but the grading wrapper did not write its per-process exit receipts;
those exit codes remain unavailable. No grading or model call is replayed to fill
that gap. Recovery/publication status is recorded in the delivery receipt.

## Interpretation and next bounded improvement

The shared capability offers exact named navigation, demonstrated by independent
deterministic editing/check tests. The real worker instead followed exhaustive
global outline pagination. Its ten-call limit ended before it read implementation.
The interface's default outline and repeated next-offset affordance made that
unproductive path available. This is observed model/tool interaction friction,
not a serving error, range refusal, source-capacity rejection or bad oracle.
We cannot infer the model's private reasoning or a causal policy effect from one
unpaired run.

The highest-leverage next improvement is task-directed navigation entry and
stopping: use existing query/path/mode selection and compact authorized file
metadata to avoid consuming the investigation budget on a global symbol scan.
Evaluate that bounded behavior separately; do not add a planner/index, raise
limits or claim that the present omission of broad reads establishes progress.
B-0035 and B-0043 remain open. No next increment is authorized by this report.

## Validation and preservation

The production implementation passed 3,866 protected tests, two optional skips,
100% configured line/branch coverage, supported Ruff/format, strict mypy and layout.
Its 1,189 physical validation inputs stayed unchanged. Focused compatibility:
2,380 passed; thirty new navigation/negative controls passed. See the
[framework contract and receipt](../../docs/development/source-navigation-continuity.md).
The old experiments, thirteen forensic records, 903 RI rows, historical refs and
188 outstanding RI-version obligations are not rewritten. No live effectiveness
claim or historical success-rate change follows from this case.

## Authorized recovery and reconciliation

The maintainer explicitly answered `+yes` to the exact scoped recovery request.
The existing interactive default-No `work-recover` procedure received `y` and
returned `CHECKOUT_RECOVERED`, exit 0, `dispatch_authorized=false`. The owner
was released after its original source/index/untracked state was authenticated.
Generated artifacts were copied from preserved ignored storage with byte hashes
verified. No model, grading command or prior effect was replayed.
[Recovery receipt](recovery.json) retains the owner identity, authorization and
verification; the missing grading-wrapper exit receipts remain unknown.

## Verified publication - 2026-10-29

Ordinary non-force publication was independently verified at
`75d511694bf2971645c7fca3f3fb2134514f19b0`, containing protected implementation
`e3be8f8e7890ede763ba5770c7ac08621c57d294`. All 1,189 physical gate inputs and
accepted source/test blobs still match. The explicit human-authorized default-No
recovery released the grading owner without redispatch or authority transfer.
The failed evaluation remains unchanged: ten metadata pages, zero source reads,
proposals, edits or worker checks. Missing grading-wrapper exit receipts remain
unknown. No model-authored code, B-0035 closure or next increment is implied.
