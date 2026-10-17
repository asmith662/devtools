# B-0048 — Experiment pipeline authorized execution and terminal closeout

- type: STORY
- status: VALIDATED
- decision_maturity: READY_FOR_IMPLEMENTATION
- necessity: FUTURE_REQUIRED
- architectural_significance: SUPPORTING
- urgency: SOON
- evidence_basis: REPOSITORY
- scope: ExperimentExecutionPipeline Increment 2 engineering; scientific deployment remains separate
- primary_domain: orchestration
- supporting_domains: governance, observability, experiments
- hard_dependencies: none
- pressure_dependencies: B-0038, B-0034, B-0042
- operational_dependencies: authenticated target with governed execution contract; configured budget and fresh usage; exact scientific maintainer authority
- promotion_trigger: satisfied for bounded synthetic engineering; live deployment requires separate authority
- validation_level: INTEGRATION

## Implemented boundary and remaining pressure

[Increment 1](../../../src/devtools/orchestration/experiments/docs/overview.md)
implements production preparation, versioned integrity-checked receipts,
status/history, target-controller authentication/startup composition, partial
usage baseline and shared read-only budget assessment. A synthetic separately
installed target reaches READY_FOR_APPROVAL without scientific entry. No generic
workflow runtime, authority API or Agent is promoted by that evidence.

The frozen source-grounding target at `9225029` authenticates its exact plan and
passes real startup preflight, but lacks `usage_budget.preview`. It ends
BUDGET_UNAVAILABLE. The engineering addition changes the controller identity;
using feature code against that plan must continue to fail authentication.
Deploying the seam for this lineage requires separately authorized publication
and binding-only successor planning/review. It must preserve the dead prior run,
scientific inputs, four-fresh-call bound and exact-run approval boundary.

## Increment 2 responsibility

Revalidate target/plan and usage/budget evidence, receive explicit host-issued
exact-plan authority, dispatch only through the existing controller, and project
authoritative scientific journal/result status into operator receipts. Add
terminal closeout and explicit conservative reconciliation for interrupted or
ambiguous outcomes. Never retry dead scientific calls or duplicate mutable
scientific truth. Preparation snapshots are not grants or reservations.

## Validated engineering outcome and remaining deployment

Increment 2 implements exact external approval consumption, fresh target and
interpreter binding checks, current budget admission, dispatch through
`Controller.run`, structured progress, conservative dispatch-intent retention,
read-only reconciliation and publication/usage closeout. Versioned execution
receipts extend preparation history without changing scientific journals.
Controller approval and per-operation reservations remain authoritative.

Isolated committed synthetic checkouts exercise the real managed target-process
path, actual external controller approvals, harmless workers and PACKET/B/C/D
publications. They cover missing/mismatched authority, changed bindings,
supersession, unavailable/refused budget, failure before scientific stages,
confirmed synthetic entry, cancellation/unknown completion, duplicate refusal,
incomplete publications and partial/missing accounting. No provider-backed model
or frozen source-grounding scientific call is used. Production static and
protected development gates remain required for the engineering checkpoint.

Scientific deployment is **not complete**. Following the successor construction
recorded below, configure explicit budget policy and fresh usage evidence,
obtain exact human approval, then execute
and evaluate the existing experiment under separate authorization. Preserve the
permanently dead prior run and the four-fresh-call bound. The frozen `9225029`
target lacks the preview/execution contracts and has no approval; this increment
does not modify it. No automatic retry, receipt relocation protocol, remote/mobile
approval UX, distributed execution or scientific interpretation is implemented.

Controlled deployment preparation has since established the
[binding-only successor and pinned execution checkout](../../../experiments/source_grounding/plans/PIPELINE_DEPLOYMENT_REVIEW.md)
at `35d464425ef13029b0ee6151e5aea232d8489068`. Actual pipeline authentication and
help-only worker startup pass; fresh partial local usage and the unchanged
four-call forecast are evidenced. Preparation remains BUDGET_UNAVAILABLE because
numeric policy is unset; exact approval remains absent. The separate target uses
its own synchronized main and local publication repository, preserving protected
main and the completed feature branch. At that initial checkpoint, remaining
decisions included numeric policy, publication/backup destination and exact human
scientific authority, followed by a separately authorized execution/evaluation.
No scientific call, approval, retry or acceptance follows from this preparation.

The subsequent approved-budget operational review found a concrete deployment
blocker: `usage_budget` skips a nonmatching experiment rule but treats nonempty
configuration as numeric admission. Isolated unrelated-run and wrong-policy
probes therefore return PASS. The approved exact-run candidate was retained but
not installed, preserving fail-closed deployment. A separately authorized
canonical scope correction and any required authenticated rebinding must precede
execution readiness; no new implementation increment was performed. Local
publication is accepted, and an isolated full Git/non-Git recovery rehearsal
passes, but its same-SSD package establishes no independent durability. Fresh
preparation remains BUDGET_UNAVAILABLE, with no approval or scientific entry.
The linked deployment review records exact evidence and remaining conditions.

The subsequently authorized canonical correction is implemented and validated:
every fresh call needs applicable numeric policy, all matching rules apply, and
preview/reservation/consumption share applicability. Scope selection uses existing
usage reconciliation so adopted work is not charged to its successor and relevant
conflicting attribution is retained. All 258 controller regressions and protected
development validation pass. The changed controller hash requires one binding-only
successor after the engineering checkpoint. The maintainer now explicitly accepts
the verified same-SSD recovery package's limitations; no new backup infrastructure
or independent-storage requirement is introduced. Candidate-08 now binds the
stabilized correction; the exact-run approved policy
is installed after isolated real reservation probes. Fresh preparation reaches
READY_FOR_APPROVAL with no authority. The existing recovery facility and restored
repository verify an incremental Git/policy update, without new infrastructure.
Scientific authority remains separate and absent; exact identities, freshness
limits and the next protected grant are recorded in the deployment review.

The consumer is a human operator now and a future ExperimentManagerAgent.
Remain concrete until repeated consumers justify more general semantics.
The roadmap is `ExperimentExecutionPipeline -> ExperimentManagerAgent -> ResearchAgent`;
the independent track is `FeatureCloseoutPipeline -> CodingAgent`. Future Agents
and the separate feature pipeline are not authorized by this backlog record.

## Invariants, risks and validation

Maintain `PLAN_VALID != READY_FOR_APPROVAL != AUTHORIZED != EXECUTED != ACCEPTED`.
Preserve target/source authentication, Model/Agent separation and controller
scientific ownership. Do not expose grant construction as an ungoverned model
capability. A communication failure cannot establish that an external effect
failed; persistence cannot supply exactly-once effects by itself.

Use deterministic isolated repositories and harmless workers for engineering
tests, including authority refusal, stale evidence and ambiguous publication.
Protected production validation and supported-source static gates remain
required. Live science needs separate explicit authorization; no sealed,
confirmation/reserve or historical semantic-judgment access follows from this item.
