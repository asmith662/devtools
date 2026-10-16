# Controlled pipeline deployment candidate: unapproved, budget unavailable

The binding-only successor is **PLAN_VALID** against a separate authenticated
execution checkout. Actual worker startup passes. Preparation ends
**BUDGET_UNAVAILABLE**, because local numeric policy remains unset. Approval is
**NONE**; execution is unauthorized; scientific ENTERED is **0**. This is a
deployment decision packet, not an execution grant or scientific result.

## Scientific identity and publication boundaries

| Identity | Exact value |
| --- | --- |
| Validated pipeline implementation | `2aad8a1c8ccc3cd19a0476d7da13f1d95a833d42` |
| New execution binding / Stage A checkpoint | `784688570669916d5ad0d7e56f2e26a225f51132` |
| Pinned execution target, including the committed plan | `35d464425ef13029b0ee6151e5aea232d8489068` |
| Successor plan | [candidate-discrimination-pipeline-run-plan.json](candidate-discrimination-pipeline-run-plan.json) |
| Successor plan SHA-256 | `de5f0ef1e62823b4be9b7af89c28936aae0224fb1cb4d5720abf8a34b41877a9` |
| New prospective scientific run | `ff37802e430190c9c683df87b03252de1bca09f2389fa8ad3eaf7ace7480c966` |
| Controller implementation-map SHA-256 | `d60eceb33db21fe645427434d59b9b039bcb4661031445926b5fcb3ed274640e` |
| New integrity SHA-256 | `67894fbf0535144b2e7cc794d8c26eb15a084a3ccf199699e0c5559665759a7d` |
| Unchanged protocol SHA-256 | `6962c790c4d6767b7560ede8bbc70c7922312902fe273483c81b351a2b74750f` |

The [original plan](candidate-discrimination-startup-run-plan.json), SHA-256
`64d0d087fb2ace87a2c01c931f3c03eda71d0e1d7af1a762afd10bc35f1a5f48`,
retains prospective run `7fdadd776309a3e25c14a3191e2cdf444473a0a4436492275dc76d8206c028f5`
and its original protected main at `92250292dacfb8289d129063d5523dd87b63162b`.
The dead `b34e9e…` run and its disposition remain immutable historical evidence.
No approval transfers between these identities.

The source commit, binding commit and plan-containing target commit have distinct
roles. The target is pinned to the third commit, not to the implementation commit
or a moving branch. A subsequent documentation-only commit on
`experiment/source-grounding-successor` records this review without advancing the
execution target. Its completed pipeline feature ancestor remains untouched.

## Byte-level scientific equivalence

The [binding record](../bindings/execution-07.json) enumerates exact preserved
artifact hashes and the complete implementation-map delta. The
[new integrity](../bindings/execution-07-integrity.json) retains the original
scientific artifact hash map. The entire candidate-06 protocol remains unchanged
in its original location; no scientific files are regenerated or copied into a
new experimental design. This preserves Stage D's existing candidate-06 lookup.

Cases 0022/0023/0024, BROAD direct-structural universes, selections and identities,
census/sample design, inclusion/weighting, labels, prompts, blinded gold,
estimators, analysis and claim boundaries remain unchanged. The question remains
whether purpose-relative source grounding distinguishes useful sources and
source-to-target pursuits from unnecessary ones within that frozen surface.
Adopted seals, opaque closure bytes, prospective compatibility receipts and
original usage provenance are unchanged. No treatment judgments were inspected.

Plan differences are restricted to name/attempt, Stage A checkpoint and execution
integrity reference, implementation/controller maps, the disclosed implementation
input, and `--stage-a` checkpoint arguments. Publication policy, scientific
protocol, economics, closed inventory, models/reasoning, retry policy and all
other disclosed inputs are unchanged. The bounded builder adds no executor.

| Scientific work | Fresh calls | Adopted dependencies |
| --- | ---: | ---: |
| Sol / High treatment, 0022 and 0023 | 0 | 2 |
| Sol / High treatment, 0024 | 1 | 0 |
| Astra / High blinded gold, one per case | 3 | 0 |
| Total maximum | **4** | **2** |

Adopted work contributes no new consumption. A fifth fresh call is rejected even
when synthetic numeric allowances are enlarged. Scientific retry remains
`NEVER_SCIENTIFIC`; adopted work must never be re-invoked.

## Authenticated target and controller ownership

Target: `C:/Users/recoveryadmin/Workspace/tools/devtools-source-grounding-successor`.
It has its own `.git`, clean tracked/index state, exact-byte checkout, Python
3.14.0 environment and independently synchronized `main`. Its `origin` is the
dedicated local publication repository:
`C:/Users/recoveryadmin/Workspace/tools/devtools/.local/deployments/source-grounding-successor/publication.git`.
Target HEAD, origin/main and actual remote main all equal the pinned target above.
The publication repository has no upstream remote and cannot implicitly forward
scientific publications to protected GitHub main.

`RunPlan` and `Repository.authenticate` require publication on synchronized
`main`; those checks remain intact. The authoring branch is published separately
to GitHub. Target `main` is a branch in a different repository, not the protected
main checkout. Scientific publication still uses `push: true`, with the same
authenticated actual-remote agreement. **Its destination is local**, so the
maintainer must review that destination and backup plan before granting authority.
It is not an off-host publication deployment. Changing publication policy would
require an explicitly reviewed binding change; do not change it silently.

The target-owned process imports its own controller and installed framework.
`Controller.from_plan` authenticates committed canonical plan, source map, Stage A,
inputs, adopted compatibility and worker startup. Supersession checks pass; the
new scientific run directory, approval and dispatch claim are absent. Pipeline
preparation never invokes `approve`, `run`, reservation or scientific stages.
The native execution adapter and budget-preview contract are present and bound.
Controller approval, scheduling, journals, publications and acceptance boundaries
remain their existing owners' responsibility.

An initial engineering clone nested under protected main was refused with
`Worker root may not be inside a checkout`. Its immutable refusal receipt remains
under the parent deployment-receipt directory, attempt
`50078ac2-5d1f-490b-8a08-36595591426f`. It is not the deployment target. Moving the
candidate outside all checkouts fixed the environment contract without code or
scientific changes. Git's CRLF defaults were also corrected for exact source bytes;
fresh target cloning uses `-c core.autocrlf=false`.

To reproduce in **new, empty deployment locations**, clone the published successor
branch as a source repository, initialize a separate bare publication repository,
and publish the exact target commit into its main. Do not reuse or overwrite the
existing target, publication repository, receipts or forensic files:

```text
git clone --branch experiment/source-grounding-successor https://github.com/asmith662/devtools.git <new-source>
git init --bare --initial-branch=main <new-publication.git>
git -C <new-source> push <new-publication.git> 35d464425ef13029b0ee6151e5aea232d8489068:refs/heads/main
git clone -c core.autocrlf=false --branch main <new-publication.git> <new-target-outside-all-checkouts>
git -C <new-target-outside-all-checkouts> rev-parse HEAD origin/main
```

Both revisions must equal the pinned target, regardless of the authoring branch's
later documentation tip. The new bare repository has no upstream. In the new
target run `uv sync --frozen --python 3.14.0`, binding replay and plan replay as
documented in [bindings](../bindings/README.md), then metadata ingest and fresh
pipeline preparation using a distinct external receipt root. Committed scientific
inputs and opaque adopted closures are already present. Existing forensic files
remain in their original checkouts; if restoring copies, authenticate each against
the plan's `preserved_evidence` map. A new checkout has its own target identity
and requires fresh preparation; no prior receipt or approval is transferred.

## Readiness and private evidence

The [machine decision packet](pipeline-deployment-readiness.json) references the
immutable `experiment-preparation-v1` result and hashed stage receipts. Its
snapshot is historical evidence, not current authority. Receipt root:

```text
C:/Users/recoveryadmin/Workspace/tools/devtools/.local/deployment-receipts/source-grounding-successor/candidate
```

Successful authentication / blocked preparation attempt:
`497c2ffc-1a92-4a2a-8d8f-af1dbc9754b8/result.json`.
Raw file SHA-256:
`df7896fe1c08aeece32589f443c9c9e96ed51e1fc9450999a74b147d6033af60`.
Validation took 51.45 seconds, usage 1.76 seconds, budget preview 6.04 seconds.
Actual worker startup used the target interpreter and exact bound script
`discrimination/entry.py` with `--help`, from an empty external directory, exit 0.
Entrypoint SHA-256:
`72ccaa47b4e9bd16b80751a6ab743dd7c64f1f8254de92327ec0321c1d7e0c71`.
The existing target-selected launcher also reports `codex-cli 0.162.1` using
`--no-daemon --version` only; no model request was made.

`admission-refusal.json` separately records canonical controller refusal:
`Execution NOT_AUTHORIZED: approval absent`. Budget preview is `UNSET`, creates no
reservation, and leaves policy/reservation/ledger/backfill hashes unchanged.
Status, by-plan lookup, latest lookup and history authenticate receipt payload
and referenced-stage hashes without manually copying a scientific run ID.

Metadata-only usage refresh completed at `2026-10-16T17:21:21.212205+00:00`.
Coverage is partial local/Devtools observation, not subscription quota. Private
totals, attribution groups and unknown category counts remain in ignored target
usage files and external receipts; only provenance hashes/coverage are published.
Missing observations are not zero consumption. Cached input is a subset of input;
reasoning output is a subset of output. Preserve cache-write observations separately
and never add overlapping categories to input/output budgets.

## Economics and required policy decision

The unchanged low-confidence forecast is **28,539–1,756,679 input tokens** and
**0–191,923 output tokens**, across exactly four fresh calls. These empirical
envelopes are not tokenizer bounds, capacity guarantees, prices or account quota.
The frozen economics file is byte-identical; no new numeric policy was written.

The existing configuration is target `.local/usage/policy.json`. It accepts
`limits` entries containing `scope`, `identity`, optional `model`, and `limits`
with `fresh_calls`, `input_tokens`, `output_tokens`. Dimensions may be `null`
(unconstrained); that is a conscious policy choice. Supported scopes are
`EXPERIMENT`, `PROJECT`, `STAGE`, `OBSERVED_WINDOW`. Experiment identity is the
exact successor run, project identity is `devtools`, stage is B/C; an observed
window applies to all local observations. The window is rolling seven days.
`max_observation_age_seconds` defaults to 300 when numeric policy is configured.
Missing ledger, stale evidence, unknown constrained categories, conflicting
observations or unknown/mixed model attribution can prevent admission.

Concrete options for separate maintainer review:

| Option | Consequence |
| --- | --- |
| Leave numeric policy unset | Preparation remains BUDGET_UNAVAILABLE; pipeline dispatch refuses. |
| Exact successor experiment envelope | A possible reviewed allowance is 4 fresh calls, 1,756,679 input and 191,923 output tokens, using the upper forecast. This is a proposal only; it does not establish account headroom or guarantee actual consumption. |
| Project or observed-window envelope | Maintainer supplies limits covering selected observed consumption, pending reservations and the proposed four-call forecast. Unknown constrained totals can block it; local observations cannot establish account-wide headroom. |
| Stage/model constraints in addition | Use the frozen per-call forecast inventory for applicable B/C and Sol/Astra limits. They add constraints; they never expand the plan's four-call inventory. |

Configured preview simulates the whole inventory without reservation. Authorized
controller dispatch separately performs fresh admission and per-call reservation
under existing writer protection. A crash retains reservations/intent pending
reconciliation, with no automatic scientific retry. Budget PASS never grants
scientific authority. An exact host-issued grant is separately required.

## Verification and timeout assessment

60 existing design/startup, budget and preparation/execution pipeline tests pass;
four new successor byte-equivalence, adoption, fifth-call and canonical-replay
tests pass; 12 existing isolated synthetic authority tests pass. The actual
binding replay and plan replay reproduce exact bytes. Ruff, formatter and strict
mypy pass for the new bounded binding code. Git diff/whitespace checks pass.
The new tests run with `uv run python -m pytest --no-cov -q experiments/source_grounding/bindings`
to include the repository root for non-installable experiment namespace imports.

No supported production or controller code changed from `2aad8a1`. That validated
checkpoint's protected gate (1,662 passed, two skipped, 100% production branch
coverage) is reused for this binding/documentation publication. Confirmation,
sealed evaluations and live-model validation were not run. FINAL protected and
scientific verification remain mandatory at future terminal publication.

The prior 30-second CLI verification deadline belongs to a synthetic test harness.
Its unchanged rerun passed. Existing read-only profiling took 21.86 seconds,
including 17.57 seconds in file reads; 81 Git calls took 2.40 seconds. File-system
latency is real, but no production timeout defect was established. The production
pipeline read-only boundary is 300 seconds; actual candidate authentication took
51.45 seconds. Scientific dispatch has no outer pipeline deadline; frozen worker
21,600-second and validation 3,600-second limits, ten-second grace, and the separate
30-second help-only startup limit remain unchanged. No timeout was raised. A future
observation timeout requires read-only reconciliation, never scientific re-dispatch.

## Subsequent controlled procedure — not performed here

Run from the pinned target with its own interpreter. Set these operator aliases:

```powershell
$plan = 'experiments/source_grounding/plans/candidate-discrimination-pipeline-run-plan.json'
$receipts = 'C:/Users/recoveryadmin/Workspace/tools/devtools/.local/deployment-receipts/source-grounding-successor/candidate'
$workers = 'C:/ExperimentWorkers/source-grounding-successor'
.\.venv\Scripts\python.exe -B scripts/usage.py ingest
.\.venv\Scripts\python.exe -B -m devtools.orchestration.experiments prepare $plan --target . --receipts $receipts
.\.venv\Scripts\python.exe -B -m devtools.orchestration.experiments status $plan --receipts $receipts
.\.venv\Scripts\python.exe -B -m devtools.orchestration.experiments history $plan --receipts $receipts
```

First review the exact pinned target, local publication/backup destination,
scientific equivalence and budget options. Only a separately authorized human
policy decision may configure applicable numeric limits. Refresh metadata and
require justified READY_FOR_APPROVAL. Then obtain separate exact scientific
authority from a trusted host. The existing host API is
`Controller.approve(ApprovalRequest(controller.run_id, principal, decision_reference))`
on an authenticated `Controller.from_plan`; the principal and decision reference
must come from actual human authority. Publish approval only, with no source
changes; its review parent must be the pinned target. Neither the pipeline nor
this document supplies that grant. Verify it with the existing read-only command.

Only in a later explicitly authorized execution assignment:

```powershell
.\.venv\Scripts\python.exe -B -m experiments.orchestration verify-approval $plan
.\.venv\Scripts\python.exe -B scripts/usage.py ingest
.\.venv\Scripts\python.exe -B -m devtools.orchestration.experiments execute $plan --target . --receipts $receipts --work-root $workers
.\.venv\Scripts\python.exe -B -m devtools.orchestration.experiments status $plan --target . --receipts $receipts --refresh
```

The future approval commit legitimately advances target/remote main; scientific
source and plan remain bound. Fresh pipeline admission must authenticate that
exact approval checkpoint. If interrupted or uncertain, use `reconcile`/status
refresh; do not issue another execute command. Terminal controller publication,
qualified usage closeout, scientific evaluation and accepted conclusions remain
separate outcomes. No such action was performed for this deployment preparation.
