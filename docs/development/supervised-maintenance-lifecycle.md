# B-0043: supervised maintenance lifecycle reconciliation

## Decision, scope and evidence strength

The next increment is **one model-neutral supervised maintenance assignment to
an independently reviewed candidate and read-only integration plan**, composed
under the existing repository WorkCycle/Checkout owners. It is a supported
operator workflow, not another B-0035 evaluation. B-0035 stays closed. This
document establishes the next implementation scope; it neither implements that
workflow nor issues a coding, serving, integration or publication grant.

First consumer: an operator asks Devtools to implement one already-reviewed
backlog obligation in one existing Python source file, supplying a frozen baseline,
behavioral requirements and immutable checks. A supervisor approves its information
obligations and source/check scope. A configured worker attempts implementation;
an independent reviewer assesses the exact candidate and its evidence. The output
is either an explicitly blocked/failed result or an authenticated integration plan
with remaining parent obligations. No daemon selects a task or closes its parent.
The Python limitation belongs to this first repository administration profile:
the current integration oracle imports a Python module. It must not narrow the
generic coding host or pretend that the current integration validator supports
arbitrary resource types.

## Actual implemented owners

| Lifecycle boundary | Existing source and behavior | Connection/limit |
| --- | --- | --- |
| Task intake | [Intake](../../scripts/backlog/intake.py) captures proposals, reviews and separately authorized promotion under a single writer | Durable repository administration, not autonomous task discovery/approval |
| Obligation decomposition | [Localization](../../src/devtools/context/localization/docs/overview.md), ADR-0005 and caller-authored task interpretations/obligations | Explicit kernel exists; no general automatic decomposition or proof that the frame is complete |
| Repository localization | RI, lexical global/obligation lanes, role evidence and scoped source search | Candidate provenance exists; rank does not satisfy an obligation |
| Context preparation | [Planning/materialization](../../src/devtools/context/planning/docs/overview.md), source Tools, native inventory/navigation, projection and optional compaction | Exact source, active witnesses and retained history are distinct; source readiness can be supplied to the neutral host |
| Worker implementation | [Shared process](../../src/devtools/agents/coding/process.py) and [repository host](../../src/devtools/agents/coding/repository.py) | Actual neutral source/edit/check/repair; no supported durable neutral WorkCycle assignment/receipt bridge |
| Existing application | [Legacy host](../../apps/qwen/turns/loop.py) delegates the shared process; [NativeObligations](../../apps/qwen/obligations/native.py) composes production Localization | This is real application reuse, but separate presentation, task and receipt policy; it is not RepositoryCodingHost adoption |
| Delegation and authority | [WorkCycle](../../scripts/backlog/work.py), [Delegations](../../scripts/backlog/delegation.py), [Checkout](../../scripts/backlog/checkout.py) | Exact assignment, approval, budget reservations, exclusive source ownership and no redispatch; current contracts intentionally remain Qwen/application-specific |
| Validation | FixedCheck/Commands, oracle preflight and [fixed integration validator](../../scripts/backlog/integration/validation.py) | Real command results and fresh protected validation; no universal transitive/toolchain/HEAD input closure |
| Independent review | Existing WorkCycle supervision and [candidate authentication](../../scripts/backlog/integration/lifecycle.py) | Exact subject bindings exist; legacy candidate reader requires `backlog-qwen-*` and literal Codex reviewer |
| Integration | Existing plan/install/validate/review/publish/promote/verify phases and [local entry](../../scripts/backlog/integration/local.py) | Controlled one-checkout lifecycle; local entry still expects apps.qwen CodingTask/result and Qwen/Codex author labels |
| Backlog closeout | Existing separate completion review and administrative writer | Parent versus slice and remaining obligations remain explicit; worker acceptance grants no closure rights |
| Execution/Resources | [Runtime](../../src/devtools/execution/docs/overview.md), managed Commands, filesystem, time and paths | Runtime remains one Conversation/ModelInteraction collaborator, not the owner of this workflow |
| Observations and durable records | [Evidence](../../src/devtools/observability/evidence/docs/overview.md), command observations, InvocationMeasurement and existing operational receipts | Typed facts/capture qualifications exist. Native coding history/result is transient; model inspector is completed-success-only, not a complete failed-attempt ledger or restart service |

Source inspection covered WorkCycle prepare/validate/authorize/execute/closeout,
Delegations authority/authorize/model/guard, integration candidate/plan/local-entry
admission and fixed validation, plus the linked public contracts. It is not a new
whole-repository assurance audit.

## What has actually been demonstrated

- **Production and integrated:** native Model/Tool composition; the shared process
  used by the Qwen application and maintained neutral consumers; scoped source;
  exact edit admission; fixed checks; custody; B-0035 inventory/refresh; deterministic
  and optional semantic/adaptive Context management. The protocol extraction changes
  ownership only. Generic task intake, authorization, review and integration exist
  as repository-owned administration with narrower legacy contracts.
- **Implemented but disconnected:** neutral RepositoryCodingHost/CodingResult to
  durable WorkCycle candidate/review/integration entry; neutral obligation-backed
  work preparation; configurable actor provenance on that new path. A callable
  `readiness` hook is not automatic obligation derivation or a complete workflow.
- **Maintained deterministic evidence:** actual read/edit/check/failure/repair and
  restoration under scripted neutral responses; governed Git lifecycle, expiry,
  refusals and interruption controls in tiny authored repositories. These prove
  the stated mechanics, not autonomous engineering success or live remote behavior.
- **Authentic model evidence:** Qwen authored the complete-inventory representation
  and naturally repaired E501. Conditional Stage B did not produce accepted
  integration. gpt-oss passed native compatibility, recovered argument refusals and,
  with ownership guidance, proposed an immediate but incomplete integration edit.
  Its later repair opportunity was interrupted by the framework. Codex completed
  production integration separately. There was no new inference for this refactor.
- **Missing:** a supported neutral task-to-reviewed-candidate consumer; automatic
  reliable planning/decomposition and worker selection; general durable native
  restart; generic supervisor/reviewer role execution. None follows from existing
  classes or benchmark outputs. No BaseAgent/AgentRuntime is selected.
- **Authority constraints, not bugs to bypass:** legacy Qwen grants bind exact
  model/profile/native schema and thinking policy; native results are not accepted
  by legacy candidate readers. Unknown source/effect/dispatch outcomes require
  reconciliation. Missing explicit approval, divergent source/destination or
  insufficient Context must stop. This reconciliation establishes no new provider
  defect, need for a generic Run type, or prerequisite universal Evidence store.

## Dependency and implementation boundary

Use repository tooling under `scripts/backlog` for the prospective handoff. Keep
reusable coding in Agents, sufficiency in Localization, materialization in Context,
execution in Resources/Tools and fact construction in Observability. No framework
source imports application or administrative modules. Runtime is unchanged.

The next native path needs a narrowly versioned operational assignment/result/review
entry at the existing WorkCycle/integration owners. This is additive: existing
Qwen task hashes, one-slot dispatches, policies, reviews and immutable receipts
remain exactly meaningful. Do not copy the WorkCycle state machine or fabricate
legacy-shaped Qwen records. Only the prospective native input is generalized;
standing delegated-policy migration and automatic publication are deferred.

Pressure owners are B-0039 (authority), B-0040/B-0044 (coordination), B-0011
(durable Evidence), B-0034 (uncertainty), B-0041 (local lifecycle), B-0036 (requests)
and existing B-0043 dependencies. These are not blanket implementation prerequisites:
explicit host authorization and stop-on-uncertainty suffice for this bounded slice.
B-0031 generic lifecycle promotion is not needed merely to name these phases.
The broader d58697fd input-assurance investigation remains open; its repaired
stale-validation reuse bug must not be rescheduled. Fresh validation and declared
input qualification remain mandatory without claiming complete environment closure.

The older ExperimentManagerAgent/ResearchAgent sequence remains dated direction.
The current maintainer-prioritized engineering consumer comes first; no experiment
supervisor, scheduler, learned planner, model registry or new retrieval work is
authorized. Supervisor, coder and reviewer are actor roles. A ModelInteraction can
back a coder; Codex remains an external Agent or trusted supervisor/reviewer, not
a fake ModelInteraction. Future actors consume the same task/candidate subjects
and authority boundaries rather than model-specific orchestration architectures.

The planned native candidate entry must feed existing plan and downstream scope
readers for the supported one-file profile, not produce an orphan JSON export.
Tests must show that a fresh separate integration grant can admit that plan in a
tiny authored repository; normal operator execution stops at the plan. Broader
task/policy migration remains a separate decision.

## Ready-to-run next Codex implementation prompt

The complete prompt below is prospective implementation scope, not execution
authority for a real maintenance worker in this assignment.

<!-- BEGIN NEXT PROMPT -->
# Devtools — Supervised Native Maintenance Handoff

Repository: the single canonical devtools checkout. Read AGENTS.md first.
Implement one supported, model-neutral supervisor-to-coder-to-review handoff under
the existing WorkCycle/Checkout/integration owners. Stop at an authenticated
read-only integration plan; do not build a general planner or launch a model campaign.

Authenticate current main, the latest coding-host decomposition receipt, B-0035
closure, B-0043 and docs/development/supervised-maintenance-lifecycle.md. Preserve
historical source/receipts, thirteen forensic files, 903 RI rows, refs and 188
historical obligations. No clones, worktrees, resets, service switches or downloads.

The concrete operator story is: prepare one already-reviewed canonical backlog
obligation as a bounded repair of one existing Python implementation file;
approve its exact source/check/worker authority; obtain a candidate and real check
evidence; independently review it; prepare an integration plan or record a blocker.
The operator supplies the item and source-repair obligation. Do not auto-select,
promote or approve a pending proposal. Refuse closed items and unsupported scopes;
B-0035 must not reenter the campaign.
The first profile is Python because the existing integration oracle imports a
module; keep the reusable coding host resource/model independent.

Inspect scripts/backlog/{intake,work,delegation,checkout}.py and integration/
{lifecycle,local,validation,authority}.py; devtools.agents.coding and model_tools;
Context localization/planning/source Tools; oracle preflight and observation
contracts; apps/qwen task/legacy-host consumers only for compatibility boundaries.
Current WorkCycle uses CodingTask, backlog-qwen-* records and exact-profile guards;
Integration.candidate requires those records and a literal Codex review. These are
intentional old contracts. Do not pass a neutral CodingResult through them by
renaming fields, broadening an old grant or claiming Qwen authorship.

Deliver the narrow prospective native assignment/result/review entry through the
same repository WorkCycle and integration owners. Explicit versioned new input
records and reader branches are authorized for this slice; old durable schemas,
hashes, policies and callers remain compatible and immutable. Reuse the existing
writer, hashes, Checkout, phase/effect mechanisms and integration plan formation.
Do not create another coordinator, registry, generic Run/Agent hierarchy or loop.
If a wider schema/authority migration is necessary, stop with the exact blocker.

A trusted supervisor supplies behavioral obligations, public fixed diagnostics,
an independently preflighted withheld acceptance, authorized read/edit addresses,
baseline/source identities and caller-authored Localization interpretation and
witness criteria. Use current RI/Localization and Context plans to prepare source;
record unresolved mandatory obligations explicitly. Retrieval rank is not a witness;
metadata, recommendations and hidden oracles grant no edit authority. Never feed
the reference solution or withheld implementation to the coding worker.

Inject a selected ModelInteraction and finite ModelSettings/profile as host
configuration. Invoke run_coding_agent with RepositoryCodingHost, scoped Tools,
existing edit admission, projection and managed checks. Claim canonical Checkout
ownership before effects and connect custody expectations/restoration to that
owner. Keep exactly one mutable host/source owner. Start with at most eight
model requests, six acquisition attempts, three proposals, two natural repairs,
the existing 32,768-byte request/resulting-source limits and a finite 20-minute
process ceiling; per-call output/time bounds must be compatible with the selected
profile. Permit genuine blockers. No arbitrary shell or model-controlled Git.

Preparation creates no execution authority. Require fresh explicit host approval
of the exact packet, canonical root, scope, worker/profile, tools, budgets and
expiry before claiming dispatch. Recheck at dispatch and each invocation. No old
Qwen standing grant authorizes this path. Record intent before entry, distinguish
claimed dispatch from actual model/Tool entry, and refuse automatic redispatch
after uncertainty. Planning/coding/review actors have separate authority; a model
response cannot approve itself or grant installation/publication.

Persist bounded task-linked operational facts through the existing administrative
record owner: original obligations/source/disclosures, actual requests and responses
under explicit capture policy, known Tool/check effects, usage/termination, exact
candidate bytes/diff, custody and unknown fields. Use core time/paths/identity and
managed filesystem/Commands. Do not deepcopy arbitrary exceptions or import an
experimental recorder into production. Reuse observation/measurement values where
applicable; receipt persistence is not a universal Evidence database or restart.

Independent review binds the exact task, candidate, check results and source tree
with explicit actor provenance/current host approval. Passing focused checks alone
cannot accept. The new native candidate input must feed the existing read-only
integration-plan owner while preserving original provenance and exact bindings.
The plan must be usable by the existing downstream scope/authority readers for
this supported profile. Prove separate authorized installation in a tiny fixture;
do not create an orphan plan export or grant installation in the operator path.
Install, protected validation, publication and canonical parent closeout remain
separately authorized existing phases; no coding/review receipt confers those rights.
Leave parent obligations explicit. Failed, exhausted, stale, unknown or no-edit
episodes produce truthful terminal evidence and no accepted plan. Preserve unknown
source for the documented default-No recovery rather than clearing ownership.

Ship a supported administrative entry/preview and a real maintained consumer test:
operator packet → explicit approval → current obligation-backed Context → native
source read → admitted edit → actual failed check → newly selected repair → passing
checks → archived/restored candidate → independent review → integration plan.
Use scripted neutral responses and tiny authored repositories; do not label them
live competence. Test a second InteractionSource without separate orchestration,
all source/currentness/refusal/capacity/budget/timeout boundaries, tampered task or
candidate/review, wrong/expired authority, uncertain dispatch/effects, serialization
failure, failed acceptance and unchanged legacy Qwen/delegation/integration flows.
Test that no source, check, review or parent-close authority is invented.

No live inference, paid fallback, model download or service mutation is authorized
by this implementation prompt. A later real operator task requires its own exact
worker authority and available authenticated profile; do not substitute a scripted
run for a real worker result or restart the B-0035 campaign.

Run focused native-host/Localization/Context/Tools/custody/WorkCycle/integration and
Qwen compatibility tests, strict mypy, supported Ruff/formatting, layout, Intake,
JSON/JSONL, links, preservation and whitespace checks. Run the unchanged full
protected gate on the committed final executable tree with configured 100%
production line/branch coverage and physical-input verification. Stage artifacts
outside an active Checkout until release. Ordinary direct-main development and
non-force publication of this feature's implementation are authorized subject to
actual protections; that authority does not publish any delegated worker candidate.
Verify local/remote main, clean tracked/index state, exact tested blobs and custody.

Document supported scope, prospective schemas, compatibility, real versus scripted
results and remaining B-0043 work. Do not close B-0043 from one bounded slice.
Save the complete handoff to .local/codex-result.md. Stop after this vertical
workflow; do not add automatic planning, a third stage, durable model resume,
worker routing, a supervisor daemon or a new model evaluation.
<!-- END NEXT PROMPT -->
