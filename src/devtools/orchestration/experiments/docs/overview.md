# ExperimentExecutionPipeline: preparation version 1

Increment 1 implements concrete, non-executing preparation of prospective
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
approval, execution, publication and reconciliation ownership. The pipeline
never calls `approve`, `run`, `reserve`, a scientific adapter command, or a model.

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

The pipeline supports prospective never-entered, unapproved plans. Controller
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
schema is modified. Pipeline version is `1`.

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
owns Increment 2: target deployment/binding compatibility, host-issued exact-plan
authority, dispatch through the existing controller, conservative reconciliation
and terminal closeout, with no duplicate scientific truth. Approval and live
science require their own authorization. The roadmap remains
`ExperimentExecutionPipeline -> ExperimentManagerAgent -> ResearchAgent`,
separately `FeatureCloseoutPipeline -> CodingAgent`; none of those future Agents
or the separate closeout pipeline is implemented here.
