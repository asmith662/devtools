# B-0048 — Experiment pipeline authorized execution and terminal closeout

- type: STORY
- status: BACKLOG
- decision_maturity: SEMANTICS_PARTIAL
- necessity: FUTURE_REQUIRED
- architectural_significance: SUPPORTING
- urgency: SOON
- evidence_basis: REPOSITORY
- scope: ExperimentExecutionPipeline Increment 2, beyond non-executing preparation
- primary_domain: orchestration
- supporting_domains: governance, observability, experiments
- hard_dependencies: none
- pressure_dependencies: B-0038, B-0034, B-0042
- operational_dependencies: authenticated target with read-only budget preview; explicit scientific maintainer authority
- promotion_trigger: separately authorized execution/closeout increment with a supported target
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
