# ExperimentExecutionPipeline: governed execution version 2

Increment 1 provides concrete, non-executing preparation of prospective
experiment-controller plans. The callable `ExperimentExecutionPipeline` and
operator CLI coordinate existing owners; they define no workflow DSL, generic
Run/Step/Attempt runtime, Agent, model routing or scientific execution mechanism.
This production capability lives in `devtools.orchestration.experiments`.
It depends on Core paths/time/identity and Resources commands/filesystem.
Reusable source does not import `experiments` into the pipeline process.

The target-owned adapter runs as a fixed program through the target's Python
interpreter, using normal Python imports in its CWD. It calls the existing
experiment `Controller.from_plan`, `plan_report`, `require_not_superseded`,
worker startup preflight, usage observatory and read-only budget `preview`.
The controller retains plan/source/Stage A authentication, scientific journals,
approval, execution, publication and reconciliation ownership. The preparation path never calls `approve`, `run`, `reserve`, a scientific
adapter command, or a model. Execution consumes existing exact authority and
invokes `Controller.run` in the target process; it never publishes approval.

## Operator commands

Run from the pipeline's installed checkout/environment:

```text
uv run python -B -m devtools.orchestration.experiments prepare experiments/example/plan.json --target C:/AuthenticatedTarget --receipts C:/PreparationReceipts
uv run python -B -m devtools.orchestration.experiments status experiments/example/plan.json --receipts C:/PreparationReceipts
uv run python -B -m devtools.orchestration.experiments history --receipts C:/PreparationReceipts
```

`status` without a plan selects the latest receipt only when target and plan
digest are unambiguous. `history [plan]` lists all matching attempts, newest
first. Separate receipt directories disambiguate targets/revised plans. No
scientific run ID is needed. `--json` exposes full structured results; the
default summary shows identity/purpose, target, readiness, preflight, maximum
fresh calls, models/reasoning, adopted work, forecast, observed usage, budget,
approval requirement and report location. Preparation exits zero only for
`READY_FOR_APPROVAL`, otherwise one. Status/history are read-only.

The plan is relative to `--target` (default CWD), or an absolute path contained
in it. The default interpreter is the target's `.venv/Scripts/python.exe` on
Windows or `.venv/bin/python` elsewhere. `--python` can select another correctly
installed target environment. Both controller and devtools command imports
must originate in the target checkout. A feature environment cannot masquerade
as target code. No PYTHONPATH rewriting or cross-checkout module loading occurs.

Receipt storage must be outside the target. For immediate use without options,
the default is the OS temporary directory's `devtools-experiment-preparations/`.
These files survive process exit, but host temporary-directory cleanup can
remove them. Use an explicit persistent `--receipts` directory for retained
operator history; use the same directory for subsequent status/history commands.
Receipts contain local usage metadata: do not publish them as scientific evidence.

## Authentication and compatibility

The target must satisfy the controller's existing exact-root, clean main,
committed canonical plan, Stage A ancestry, source hashes, preserved forensic
file hashes and configured remote synchronization contracts. This increment
does not waive main-only controller authentication or reinterpret feature HEAD
as an authenticated scientific implementation. Target HEAD, Git directory,
interpreter, exact plan digest and immutable scientific identity are retained.
Authentication runs before and after target checks. Startup is limited to the
existing bound external-CWD `python -B script --help` behavior. No worker root
is created or used, and bytecode writing is disabled in target subprocesses.

Preparation supports prospective never-entered, unapproved plans. Controller
supersession rejection is reused. Any existing scientific run directory requires
separate controller reconciliation and is refused, including approvals,
dead/interrupted/completed runs and orphan or empty state. Preparation does not read or reinterpret their
semantic results or retry scientific operations. This conservative scope is
intentional: preparation receipts are not a second mutable scientific journal.

The frozen source-grounding plan at main `92250292dacfb8289d129063d5523dd87b63162b`
was exercised through its own Python 3.14 environment: exact plan digest
`64d0d087fb2ace87a2c01c931f3c03eda71d0e1d7af1a762afd10bc35f1a5f48`,
scientific run `7fdadd776309a3e25c14a3191e2cdf444473a0a4436492275dc76d8206c028f5`,
`PLAN_VALID`, real worker-startup `PASS`, four maximum fresh calls, and partial
local usage/forecast capture. It ends **BUDGET_UNAVAILABLE**, because that target
has no read-only budget preview seam. It is **not READY_FOR_APPROVAL**. No
binding, approval or scientific journal was changed to accommodate the feature.

The minimal new target seam is `experiments.orchestration.usage_budget.preview`.
It shares `_assess_call` with existing reservation admission, simulating the
whole prospective inventory in memory. It does not reserve, write state, or
require/manufacture an execution grant. Adding it changes controller hashes,
so simply using feature source against an old plan is invalid. Deployment for
that scientific lineage requires separately authorized engineering publication
and binding-only successor planning/review; this increment does neither.

## Usage, economics and budget semantics

The controller authenticates the frozen economics forecast and exact fresh-call
inventory against Stage A. Preparation obtains that forecast rather than
regenerating disclosure/candidates or fitting a new policy. Usage comes from
the target's existing metadata ledger, through `observability.usage.report`.
Missing ledger means `UNAVAILABLE`, with no zero-consumption assertion. Known
local subtotals, unknown categories, conflicting observations, coverage and
unallocated timestamps are retained. Cached input and reasoning output remain
provider categories within input/output; they are never added into a new total.
No account-wide quota, subscription percentage or dollar amount is inferred.

Budget preview reuses configured observed-window/project/experiment/stage/model
constraints, freshness checks, existing outstanding reservations, call/model
ceilings and `governance.usage` checks. Missing numeric configuration is `UNSET`,
not admission success or an invented infinite budget. Missing forecast/inventory,
ledger required by configured limits, or target preview support is unavailable.
Configured limits rejecting combined proposed work produce `BUDGET_REJECTED`.
Unknown required amounts fail existing checks. Preview is an observation, never
a reservation: later authorized execution must revalidate freshness and reserve.

## Receipts, dispositions and recovery

Each invocation exclusively allocates a new `PreparationId` based on Core
`Identity`. `<receipts>/<id>/start.json`, stage receipts and `result.json` use
the versioned `experiment-preparation-v1` envelope with canonical-payload SHA-256.
Terminal results bind stage receipt digests. Files are written once through the
filesystem owner's atomic-write behavior. Status authenticates schema, payload
and referenced-stage integrity. These hashes detect corruption; they are not
signatures, tamper-proof storage, approval or authority. No durable scientific
schema is modified. Pipeline version is `2`; preparation-v1 remains readable.

Receipts retain pipeline/attempt identity, plan digest, target identity,
stage dispositions and wall/elapsed timings, diagnostics, observed validation,
preflight and usage results, forecast and budget evidence references/digests,
final disposition and report path. Evidence snapshots can become stale; they
do not assert that the target is still ready when a status command reads them.

| Disposition | Meaning |
|---|---|
| `READY_FOR_APPROVAL` | Actual target checks, applicable preflight, usage observation and configured budget preview passed; awaiting a separate decision. |
| `PLAN_INVALID_OR_INCOMPATIBLE` | Target/plan authentication, supersession or prospective eligibility refused. |
| `STARTUP_PREFLIGHT_FAILED` | Existing startup preflight refused required worker readiness. |
| `BUDGET_REJECTED` | Existing configured numeric policy refused preparation's forecast. |
| `BUDGET_UNAVAILABLE` | Required budget assessment is unavailable or UNSET. |
| `EVIDENCE_UNAVAILABLE` | Required structured/usage evidence cannot establish readiness. |
| `PREPARATION_FAILED` | Infrastructure or input failure; diagnostics retained. |
| `INTERRUPTED` | Observed cancellation; terminal receipt is written before propagation. |
| `INTERRUPTED_OR_IN_PROGRESS` | Start exists without terminal receipt; crash versus active process is indeterminate. |

Repeating preparation creates an independent observation and repeats only safe
checks. It neither resumes nor creates scientific operations. No stale receipt
is silently repaired, overwritten or promoted to success. A hard process crash
or storage failure can leave only start/stage receipts; inspect them and rerun
preparation if desired. No generic resume protocol or live-PID truth is claimed.

`PLAN_VALID != READY_FOR_APPROVAL != AUTHORIZED != EXECUTED != ACCEPTED`.
Preparation always reports no authority, no scientific dispatch and unassessed
acceptance. It does not verify a pre-existing approval as part of this slice.

## Validation and remaining work

Deterministic production tests cover receipts, failure/cancellation, transport,
unknown evidence, repetition and CLI lookup. A synthetic committed main checkout
with a separate Python environment reaches READY using actual controller and
preflight/budget procedures. Its worker rejects all commands except `--help`.
Tests assert target and usage bytes stay unchanged and reject source mismatch,
supersession and a feature interpreter. Existing budget tests cover shared
reservation semantics and combined-inventory preview refusal.

[B-0048](../../../../../docs/backlog/items/B-0048-experiment-pipeline-authorized-execution.md)
records the validated Increment 2 engineering below and its separate remaining
scientific deployment. Approval and live science require their own authorization.
The roadmap remains
`ExperimentExecutionPipeline -> ExperimentManagerAgent -> ResearchAgent`,
separately `FeatureCloseoutPipeline -> CodingAgent`; none of those future Agents
or the separate closeout pipeline is implemented here.


## Increment 2: externally authorized execution

The concrete lifecycle is prepare, await external exact authority, revalidate,
dispatch through the target controller, observe, reconcile and report. Production
orchestration owns requests, transport and operator receipts; the controller
continues to own scientific scheduling, operation claims, no-retry rules,
publication and verification. No universal workflow runtime or new authority
framework is introduced.

```text
uv run python -B -m devtools.orchestration.experiments execute experiments/example/plan.json --target C:/AuthenticatedTarget --work-root C:/ExternalWorkers --receipts C:/RetainedPipelineReceipts
uv run python -B -m devtools.orchestration.experiments status experiments/example/plan.json --receipts C:/RetainedPipelineReceipts
uv run python -B -m devtools.orchestration.experiments reconcile experiments/example/plan.json --target C:/AuthenticatedTarget --receipts C:/RetainedPipelineReceipts
uv run python -B -m devtools.orchestration.experiments status --active --receipts C:/RetainedPipelineReceipts
```

Execution requires an explicit persistent external receipt directory outside OS
temporary storage, plus an external worker root. The pipeline selects the latest
preparation for the exact target/plan or accepts `--preparation <receipt>`.
Execution requires a fresh version-2 preparation containing the target Python
binary SHA-256 and version. Older preparation-v1 envelopes remain readable for
history, but receipts missing that binding cannot admit execution. The target
rechecks the executable path, bytes and version before admission and reconciliation.
Neither that reference nor the `execute` command grants scientific authority.
The pipeline offers no approval-publication flag. A trusted host must already
have issued and durably published the existing controller approval. Deployment
of that authority mechanism remains distinct from pipeline preparation.

The target adapter authenticates the committed approval with
`Controller.execution_authorization`: exact plan, scientific run, source/controller
binding, immutable approval history, review parent, approval publication and
remote policy. The target must be at the exact approval checkpoint. Preparation
may name that checkpoint or its authenticated review parent, allowing the expected
approval commit without accepting arbitrary target advancement. Missing, changed,
superseded or mismatched authority fails before scientific dispatch. Targets must
contain the execution contract; feature modules are never substituted into them.

Before dispatch the target repeats plan/source authentication, startup admission,
prospective-state and supersession checks, exact approval authentication, current
usage and configured budget preview. Receipt writes establish storage readiness.
The controller then reauthenticates authority under its existing OS writer lease.
`Controller.run(..., require_budget_policy=True)` repeats configured admission
under that lease, and actual controlled-call reservations require configuration
and an observed ledger as well. Preview is never a reservation. The existing
scope/freshness/unknown-value policy is shared by admission and post-run consumption
assessment; no numeric allowances or subscription accounting are invented.

A durable external dispatch request is written before process launch. A target
claim at `.local/experiment-pipeline-dispatch/<scientific-run>.json` is created
under the controller writer lease before invoking `run`. It is a conservative
pipeline intent, not a scientific ENTERED claim or authority. Its presence blocks
another pipeline dispatch, including from a different receipt directory. It is
never automatically cleared, repaired or retried. The controller still enforces
its own immutable run identity and operation journals. The pipeline never calls
scientific resume or silently selects a replacement attempt. A claim without a
run context remains an uncertain launch unless a recorded controller return
proves failure before entry. Confirmed failure with only preparation stages is
reported separately from B/C scientific stage entry.

Managed command handles stream structured controller observations during the
single target process. Existing controller supervision retains per-operation
limits, worker tree ownership and stage ordering. Progress logs retain timestamps,
case/stage/operation, status and durations with operational provenance. They are
not proof of scientific completion. No polling process farm, event bus or model
text interpretation is added. The outer dispatch has no new arbitrary deadline;
controller worker/validation limits remain authoritative. Cancellation terminates
and reaps the immediate managed adapter; surviving controller workers may still
finish under their existing supervision. Interruption is not rollback or proof
of zero model calls.

## Execution receipts and reconciliation

`experiment-execution-v1` extends the existing receipt envelope without changing
preparation-v1 or scientific durable schemas. Each `ExecutionId` directory owns
start, admission request/result, dispatch request/result, controller-return and
terminal result receipts. Admission/dispatch timings and total elapsed duration
are retained. Requests reference preparation identity/digest, exact plan/target,
worker root, scientific run and authenticated approval. The target claim binds the
request digest. Structured operational progress is separate from immutable
receipts and authoritative scientific journals.

`reconcile` and `status --refresh --target ...` only observe. They select the
latest actual dispatch intent rather than treating a later refused duplicate as
the active scientific run. Each reconciliation appends an integrity-checked
receipt with a new report path; original receipts are preserved. Status/history
support plan/latest lookup, and `status --active` selects unresolved execution
where unambiguous. Full identities and evidence remain available with `--json`.

| Execution disposition | Meaning |
|---|---|
| `ADMISSION_REFUSED` | Authority, preparation, bindings, policy or duplicate-state checks refused before this pipeline request launched dispatch. |
| `INTERRUPTED_BEFORE_DISPATCH` | Observation canceled before the consequential request. |
| `DISPATCH_COMPLETION_UNKNOWN` | Request may have reached the controller; no scientific retry is permitted. |
| `FAILED_BEFORE_SCIENTIFIC_ENTRY` | Target recorded controller failure without a scientific run context. |
| `CONTROLLER_FAILED` | Authenticated controller records show failure; existing scientific no-retry semantics remain. |
| `RECONCILIATION_REQUIRED` | Live, interrupted, orphan, altered or incomplete evidence cannot establish terminal closeout. |
| `COMPLETE_WITH_PARTIAL_ACCOUNTING` | Scientific publication verified, but consumption/budget evidence remains partial or unavailable. |
| `COMPLETE` | Controller return, scientific publications and observed-scope accounting/budget checks authenticated. Scientific conclusions still require maintainer review. |

A process exit code never determines scientific success. Closeout uses
`Controller.verify`, journal bindings, all PACKET/B/C/D publication identities and
available controller-return evidence bound to the exact dispatch request, attempt
and scientific run. Missing termination proof remains unknown
even when some publications exist. An incomplete publication or dirty scientific
state cannot become successful closeout. Safe repeated observation never calls
`run` again. Ambiguous cases require explicit operator reconciliation outside this
increment; no speculative automatic repair or stale-claim deletion is provided.

Usage snapshots preserve local rolling observations and the execution-window,
run-attributed report, with ledger/policy/backfill/reservation references. Original
consumption and adopted dependencies are reconciled by the existing observatory.
Input, cached input, output and reasoning categories remain separate; no overlapping
categories are added. Closeout reports forecast upper amounts beside reported
subtotals and unknown counts, plus actual consumption/outstanding-reservation
assessment through the same configured budget policy. Missing measurements,
unsettled reservations, conflicts, unallocated timestamps and unknown categories
prevent complete accounting. These are observed local scopes, not account-wide
usage, billing or inferred acceptance of scientific conclusions.

## Engineering completion and controlled deployment

Increment 2 is validated through isolated authenticated synthetic checkouts,
external synthetic grants and harmless local substitute workers. Test-only frozen
controller copies replace the expensive framework checkpoint floor with the
existing fixture validator contract; the shipped controller retains that floor.
The workers simulate judgments/usage and invoke no provider-backed models.

The protected source-grounding checkout remains at `9225029`, unapproved and
unentered. Its controller lacks this execution/preview contract and its local
numeric policy is unset. Engineering implementation does not deploy it or rebind
its frozen scientific plan. The next controlled task is to establish an
authenticated successor execution checkout and binding-only scientific successor,
configure explicit budget policy and fresh usage evidence, obtain exact human
approval, then execute and evaluate the existing experiment. None of those
scientific deployment actions is performed by this engineering increment.

Remaining limitations are deliberate: no automatic science retry/resume, no
remote/mobile approval UX, no distributed lease, no receipt relocation protocol,
and no account-wide quota service. Filesystem retention and trusted host access
remain operator responsibilities. Broader Agent and separate feature-closeout
roadmaps remain as stated above.
