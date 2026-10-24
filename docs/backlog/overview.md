# Architecture Backlog

Delivered P1 follow-through: [module-binding repair](../development/ri-module-binding-repair.md), PR#5. Proposal16b27e74 receives implemented-and-merged acceptance evidence via append-only ADVISORY; no coding/adoption work remains for this scope. Intake has no delivered/closed proposal enum; no approval, B-number, grant or parent closure was invented.

Integrated RI assurance evidence: [current report](../research/ri-assurance-and-cohesion-audit.md). One distinct new pending [module-pattern/exception binding bug](proposals/16b27e74-f553-40a8-b342-c3458a7b7a01/proposal.json), independently reproduced with real observations, and eight append-only advisories. Delivered-main fixes remain delivered; no implementation repeated, status changed, B-number assigned, approval/grant created or parent closed. Missing Localization and measured reuse retain existing proposal homes.

Production adoption evidence: [PR #2 / main f1adf2c9](../research/feature-branch-integration-20261024.md#protected-main-adoption-completed--2026-10-24) delivers the whole-feature integration and both RI corrections. Seven existing proposals receive append-only main-adoption/remaining-scope advisories; proposal approvals, statuses and B-numbers remain unchanged.

Current integration evidence: [whole-feature main-derived candidate](../research/feature-branch-integration-20261024.md). Six existing proposals receive advisory evidence; [pipeline branch reconciliation](proposals/2fbb85c3-ff31-4312-9df8-51a03ad45bec/proposal.json) is a distinct pending investigation. No canonical status, B-number, grant or approval changes.

## Purpose and authority

The backlog records known work, architectural pressure, investigations, and
unresolved responsibilities discovered through research, audits, or real use.
It answers: **what needs deliberate future attention?**

Backlog presence does not authorize design or implementation. Package-local
documentation remains authoritative for implemented package behavior;
[architecture](../architecture.md) owns current cross-package architecture;
[roadmap](../roadmap.md) records deliberately selected near-term sequencing;
and the implementation ledger records historical fact. Accepted decisions live
under [architecture decisions](../architecture/decisions/); unresolved pressure
remains in this backlog. An ADR does not by itself mark implementation work
complete.

## Proposal intake

The [initial reconciliation crosswalk](../research/architecture-reconciliation-inventory.md#backlog-crosswalk)
maps audit discoveries onto existing records and pending proposals. It does not
replace this canonical index, assign B-numbers or change dispositions. The
original18 list was unavailable at that checkpoint. The [recovered exact-seed
crosswalk](../research/reconciliation-input-reconciliation.md#original-candidate-crosswalk)
now maps all18 to actual canonical records and one new pending edit-ergonomics
investigation. Four existing pending proposals gained advisory research evidence.
Prior IDs/parents/states and canonical B-number rows are unchanged; the queue has
17 proposals (16 pending,1 approved). The pinned harness comparison does not
authorize implementation, model experiments or automatic approval.

[Governed proposal intake](metadata.md#governed-proposal-intake-repository-administration)
captures discoveries without changing active work. Pending proposals and advisory
review history live under `proposals/`; only a host-authorized backlog decision
can publish a normal canonical B-number item. Backlog inclusion still grants no
implementation or execution authority. The real Python 3.12 compatibility
proposal was promoted as B-0048; its accepted object-only candidate still needs
separate integration authority. The
[work-cycle bridge](metadata.md#governed-backlog-to-qwen-cycle) consumes a published
approved item only under separate implementation authority; a single designated
coordinator owns canonical mutations, while isolated workers return reviewable
candidates or escalation evidence without protected publication.

The [integration lifecycle](integration.md) now connects accepted candidates to
validated feature publication, explicitly authorized destination promotion and
verified canonical work progress. No parent is closed merely because a slice
passed. Standing coding and integration grants remain separate authorities.

## Structure

    docs/backlog/
    ├── overview.md
    ├── metadata.md
    ├── epics/
    └── items/

Each canonical record has an opaque stable identifier such as B-0008. The
identifier encodes no type, subsystem, urgency, priority, or status.

## Development cadence

    research / audit / real-use evidence
        -> discover architectural pressure
        -> create or update backlog item
        -> record evidence, consumers, dependencies, invariants, uncertainty,
           risks, and promotion trigger
        -> identify the smallest meaningful slice
        -> implement deterministic semantics
        -> unit validation
        -> integration validation
        -> live harness validation when meaningful
        -> observe real model/system behavior
        -> refine only when evidence requires it
        -> update authoritative documentation, backlog, and implementation ledger

The repository should not build a large abstract foundation and defer its first
real model interaction until the end. A foundational or structural primitive
should be exercised through a specialized live harness as soon as a meaningful
end-to-end path exists. Unit coverage remains necessary, not sufficient.

Validation levels are progressive evidence, not universal gates:

    NONE -> UNIT -> INTEGRATION -> LIVE_SINGLE_HARNESS -> LIVE_MULTI_HARNESS

Live validation tests framework enforcement, not voluntary model compliance. A
forbidden operation is validated when the framework prevents the effect even if
the model requests it.

## Current epics

| ID | Record | Status |
| --- | --- | --- |
| [B-0001](epics/B-0001-architecture-documentation-integrity.md) | Architecture & Documentation Integrity | ACTIVE |
| [B-0002](epics/B-0002-coding-context-substrate.md) | Coding Context Substrate | BACKLOG |
| [B-0003](epics/B-0003-local-coding-worker-harness.md) | Local Coding Worker Harness | BLOCKED |
| [B-0004](epics/B-0004-governed-execution-evolution.md) | Governed Execution Evolution | DEFERRED |
| [B-0005](epics/B-0005-effect-governance.md) | Effect Governance | DEFERRED |
| [B-0015](epics/B-0015-framework-acceptance-harness-validation.md) | Framework Acceptance & Harness Validation | BACKLOG |

## Canonical record index

Every canonical record is indexed below by stable ID, current lifecycle status,
and primary architectural domain. Supporting domains and dependency semantics
are recorded in the linked file.

The table supports ID, status, and primary-domain navigation. Each record's
`hard_dependencies`, `pressure_dependencies`, and `operational_dependencies`
provide dependency navigation without duplicating a second dependency graph.

| ID | Record | Status | Primary domain |
| --- | --- | --- | --- |
| [B-0001](epics/B-0001-architecture-documentation-integrity.md) | Architecture & Documentation Integrity | ACTIVE | documentation |
| [B-0002](epics/B-0002-coding-context-substrate.md) | Coding Context Substrate | BACKLOG | context |
| [B-0003](epics/B-0003-local-coding-worker-harness.md) | Local Coding Worker Harness | BLOCKED | experiments |
| [B-0004](epics/B-0004-governed-execution-evolution.md) | Governed Execution Evolution | SUPERSEDED | execution |
| [B-0005](epics/B-0005-effect-governance.md) | Effect Governance | DEFERRED | governance |
| [B-0006](items/B-0006-reconcile-authoritative-architecture-documentation.md) | Reconcile authoritative architecture documentation | ACTIVE | documentation |
| [B-0007](items/B-0007-correct-model-serving-documentation-drift.md) | Correct model-serving documentation drift | IMPLEMENTED | models |
| [B-0008](items/B-0008-investigate-repository-context-discovery.md) | Investigate repository-context discovery | SUPERSEDED | context |
| [B-0009](items/B-0009-build-bounded-local-coding-worker-harness.md) | Build bounded local coding-worker harness | VALIDATED | experiments |
| [B-0010](items/B-0010-investigate-work-execution-attempt-semantics.md) | Record resolved Run/Step/Attempt semantics | DEFERRED | execution |
| [B-0011](items/B-0011-investigate-durable-execution-evidence.md) | Investigate durable execution Evidence | DEFERRED | observability |
| [B-0012](items/B-0012-investigate-governed-effect-semantics.md) | Investigate governed effect semantics | DEFERRED | governance |
| [B-0013](items/B-0013-investigate-authority-grants-approval.md) | Investigate authority, grants, authorization, and approval | DEFERRED | governance |
| [B-0014](items/B-0014-investigate-retry-repair-reconciliation.md) | Retry, repair, and reconciliation | SUPERSEDED | execution |
| [B-0015](epics/B-0015-framework-acceptance-harness-validation.md) | Framework Acceptance & Harness Validation | BACKLOG | evaluation |
| [B-0016](items/B-0016-define-framework-live-harness-acceptance.md) | Define framework live-harness acceptance methodology | BACKLOG | evaluation |
| [B-0017](items/B-0017-investigate-runtime-occurrence-observability-boundaries.md) | Runtime occurrence and observability boundaries | SUPERSEDED | observability |
| [B-0018](items/B-0018-investigate-operational-data-minimization-disclosure.md) | Investigate operational-data minimization and disclosure | DEFERRED | governance |
| [B-0019](items/B-0019-investigate-typed-configuration-ownership.md) | Investigate typed configuration ownership | DEFERRED | models |
| [B-0020](items/B-0020-investigate-capability-operation-model-action-substrate.md) | Capability, operation, and model-action substrate | SUPERSEDED | tools |
| [B-0021](items/B-0021-investigate-approval-human-governance-workflow.md) | Approval and human-governance workflow | SUPERSEDED | governance |
| [B-0022](items/B-0022-investigate-delegation-acting-authority.md) | Delegation and acting authority | SUPERSEDED | governance |
| [B-0023](items/B-0023-investigate-observability-architecture.md) | Investigate observability architecture | DEFERRED | observability |
| [B-0024](items/B-0024-investigate-audit-durable-accountability.md) | Investigate audit and durable accountability | DEFERRED | governance |
| [B-0025](items/B-0025-investigate-scoped-runtime-context.md) | Investigate scoped execution-fact propagation | DEFERRED | execution |
| [B-0026](items/B-0026-investigate-runtime-control-lifecycle.md) | Runtime control and lifecycle | SUPERSEDED | execution |
| [B-0027](items/B-0027-investigate-serialization-representation-boundaries.md) | Investigate serialization and representation boundaries | DEFERRED | persistence |
| [B-0028](items/B-0028-investigate-persistence-durable-state-boundaries.md) | Investigate persistence and durable-state boundaries | DEFERRED | persistence |
| [B-0029](items/B-0029-investigate-reusable-agent-definition-runtime-orchestration.md) | Reusable Agent definition and runtime orchestration | SUPERSEDED | agents |
| [B-0030](items/B-0030-investigate-provider-neutral-generative-model-interaction.md) | Provider-neutral generative-model interaction | SUPERSEDED | models |
| [B-0031](items/B-0031-investigate-generic-execution-lifecycle-promotion.md) | Investigate generic execution lifecycle promotion | DEFERRED | execution |
| [B-0032](items/B-0032-investigate-execution-retry-mechanics.md) | Investigate execution retry mechanics | DEFERRED | execution |
| [B-0033](items/B-0033-investigate-semantic-repair-replanning.md) | Investigate semantic repair and replanning | DEFERRED | agents |
| [B-0034](items/B-0034-investigate-uncertain-effect-reconciliation.md) | Investigate uncertain-effect reconciliation | DEFERRED | governance |
| [B-0035](items/B-0035-investigate-tool-facing-capability-exposure.md) | Investigate Tool-facing capability exposure | DEFERRED | tools |
| [B-0036](items/B-0036-investigate-action-request-semantics.md) | Investigate Action request semantics | DEFERRED | agents |
| [B-0037](items/B-0037-investigate-approval-semantics.md) | Investigate approval semantics | DEFERRED | governance |
| [B-0038](items/B-0038-investigate-approval-workflow-orchestration.md) | Investigate approval workflow orchestration | DEFERRED | orchestration |
| [B-0039](items/B-0039-investigate-delegated-authority.md) | Investigate delegated authority | DEFERRED | governance |
| [B-0040](items/B-0040-investigate-delegated-agent-coordination.md) | Investigate delegated Agent coordination | DEFERRED | orchestration |
| [B-0041](items/B-0041-investigate-execution-local-lifecycle-control.md) | Investigate execution-local lifecycle control | DEFERRED | execution |
| [B-0042](items/B-0042-investigate-workflow-lifecycle-control.md) | Investigate workflow lifecycle control | DEFERRED | orchestration |
| [B-0043](items/B-0043-investigate-reusable-agent-semantics.md) | Investigate reusable Agent semantics | DEFERRED | agents |
| [B-0044](items/B-0044-investigate-orchestration-control-loops.md) | Investigate orchestration control loops | DEFERRED | orchestration |
| [B-0045](items/B-0045-establish-minimal-model-interaction-core.md) | Establish minimal ModelInteraction core | IMPLEMENTED | models |
| [B-0046](items/B-0046-investigate-advanced-model-interaction-provider-pressure.md) | Investigate advanced model-interaction/provider pressure | BACKLOG | models |
| [B-0047](items/B-0047-protected-development-validation-profile.md) | Protected development validation profile | VALIDATED | evaluation |
| [B-0048](items/B-0048-restore-python-3-12-json-file-model-compatibility.md) | Restore Python 3.12 JSON file-model compatibility | BACKLOG | resources |

See [metadata.md](metadata.md) for record semantics and promotion discipline.

## Four-project research evidence (2026-10-23)

The [DeepSeek Harness/Aider follow-up](../research/agent-harness-mechanism-review.md#deepseek-harness-and-aider-source-and-test-audit-2026-10-23)
adds source/test evidence to B-0011/B-0018/B-0023/B-0028/B-0034/B-0035/B-0044
and ADVISORY reviews to the existing edit, module, CodeGraph and Memory proposals.
No proposal was created or approved and no B-number/status/parent changed. The
[next five-flow local lifecycle audit](../research/development-lifecycle-audit-plan.md)
selects existing receipts; it authorizes no implementation or replay.

## Executed lifecycle audit evidence (2026-10-23)

The [five-flow source/evidence audit](../research/development-lifecycle-observability-audit.md)
adds advisory evidence to B-0011/B-0018/B-0023/B-0027/B-0028/B-0034/B-0035/B-0044/B-0046
and four existing proposals. No new proposal/B-number, status, parent, grant or
approval changed. Existing records own correlation, durable Evidence, privacy,
working-state and uncertain-effect pressure; no implementation follows automatically.

## Completed production reconciliation checkpoint (2026-10-23)

The [production/experiment/cohesion/custody report](../research/production-adoption-and-architecture-reconciliation.md)
adds advisory evidence to B-0006/B-0011/B-0023/B-0028/B-0035/B-0047 and four existing
pending proposals. One distinct [protected-validation reuse/input-closure investigation](proposals/d58697fd-bb03-4e98-bdac-fa29444fc6ff/proposal.json)
is captured PENDING_REVIEW under B-0047. It asserts no historical bypass and
changes no profile/status, B-number, parent, approval or execution authority.
The next checkpoint is comprehensive successor-session handoff, not automatic
implementation, cleanup or protected-main adoption.

## Deep RI/Context code-audit intake (2026-10-23)

The [source/consumer/case report](../research/repository-intelligence-code-audit.md)
adds four concrete PENDING_REVIEW records, without B-number assignment or approval:

- [15bae0a6](proposals/15bae0a6-b95d-417c-98fa-d75a8aff29d4/proposal.json): connect trusted explicit Localization obligations/witness decisions to native Context.
- [1d0ed8bb](proposals/1d0ed8bb-e38e-44ea-8af3-530c2516981a/proposal.json): consume existing SnapshotDelta at authorized native refresh.
- [cea1b3e7](proposals/cea1b3e7-bfa6-492a-b850-343a0c543878/proposal.json): expose qualified direct-base evidence through existing native navigation.
- [aedea41e](proposals/aedea41e-804b-4fe0-ad53-8758e074885d/proposal.json): qualify exact-frame analysis/lexical reuse across current real consumers.

Fresh physical-line reproduction evidence is appended to the two original
pending source-span bug proposals416658bd/5aa7a431; operator dedup remains open.
Existing CodeGraph and module/cohesion proposals receive advisory evidence and
bounded acceptance detail. No original payload/status, parent, B-number, grant
or frozen scientific result changes. The [coverage program](../research/comprehensive-code-audit.md)
postpones the final successor-session dossier and schedules subsequent domains.

### RI follow-up dispositions

The [implementation/fixture follow-up](../research/ri-deep-audit-followup.md)
records the explicitly assigned source-index repair at
`a0a6c22403f7df2679aa574226e420521a8accf5`; both existing bug proposal IDs and
pending states remain. Four integration/reuse records above receive additional
ADVISORY acceptance qualifications, not approvals.

Three distinct source-backed records are newly PENDING_REVIEW:

- [2e70de9a](proposals/2e70de9a-d09c-409d-a7a2-0f32f67c4768/proposal.json): authenticate canonical neutral-ID/address binding in historical unblinding adapters. Synthetic counterexample; no claim original science was corrupted.
- [a88167f9](proposals/a88167f9-2688-478c-9659-202d05e61e1e/proposal.json): disambiguate synthetic RI fixture identities and qualify real observed-input integration.
- [befd10cd](proposals/befd10cd-f382-4f40-aade-5c4119db4c44/proposal.json): correct address-only lost-resource reporting through a qualified derived view if still consumed; retain frozen reports.

No B-number assignment, parent closure, dispatch, grant or historical judgment
change follows. Exact remaining historical source/test review is in the audit
overlay; a passing protected gate does not close that review.

### Scientific-integrity and retrieval-policy follow-up

The [policy/integrity audit](../research/ri-policies-and-scientific-integrity-audit.md)
records the separate versioned unblinding verifier and96 authenticated original
bindings; no historical corruption is demonstrated. Existing integrity proposal
2e70de9a and the two repaired source-span proposals retain pending states with
operator reconciliation recommendations. Nine existing records receive ADVISORY
scope/evidence additions; exact review hashes are in the report's Intake ledger.

One distinct new proposal is pending, without B-number or implementation grant:
[06c3809b](proposals/06c3809b-f80c-461d-9585-2d4a973f8252/proposal.json),
explicit caller-authored task locators to existing native grounding/source
acquisition. It stops at authenticated source acquisition; full semantic
witness/readiness decisions remain the separate15bae0a6 obligation. No new
parser, Context compiler, automatic selector or edit authority is proposed.

### Increment implementation audit intake

The [64-path increment audit](../research/ri-increments-25-36-audit.md) records
one new pending BUG, [dabfa1f7](proposals/dabfa1f7-b4ae-4ed0-82c9-179f47e31630/proposal.json):
preserve complete words in future versioned task-card normalization. Original
cards/judgments remain frozen. Seven existing records receive ADVISORY evidence
on binding guards, historical coordinate copies, source-span reconciliation,
Localization use, fixture scope and measured reuse/cohesion. Exact identities
are in [Intake receipts](../research/code-audit/ri-increments-intake.json).
No proposal is approved or assigned a B-number. The existing B-0002/R1 promotion
boundary remains sufficient for experimental lexical mechanisms; no development
winner becomes a default native strategy through this audit.

### Dogfood lifecycle audit intake

The [94-path dogfood audit](../research/ri-dogfood-lifecycle-audit.md) records
one new pending BUG,
[edfb9e28](proposals/edfb9e28-34fb-497f-8ff1-d3a4c7320eb0/proposal.json):
whole-pipeline missing witness support in an explicitly versioned future U2
analysis adapter. The original closed-case implementation and outcomes remain
frozen; all original selected witnesses were complete. Eight existing records
receive ADVISORY evidence on input/report closure, exact-hint and Localization
consumers, measured reuse, controller/fixture responsibilities and implemented
source-span reconciliation. Original source associations agree in all three
cases; subset-validator limits are not proof of corrupted publication.
[Exact receipts](../research/code-audit/ri-dogfood-intake.json) preserve pending
states, hash chains and operator recommendations. No approval, B-number,
implementation grant, parent closure or scientific rerun is authorized.

### U1, R1.7 and R2 audit intake

The [101-path audit](../research/ri-u1-r17-r2-audit.md) adds distinct pending BUG
[5fa23957](proposals/5fa23957-703a-4de9-9619-316f8f7740ed/proposal.json):
Graph3 metric-subset validation must not claim whole-report/input authentication.
Original expected-output/byte verification still protects the retained publication;
the synthetic accepted mutations do not demonstrate historical corruption.
This responsibility is separate from canonical neutral-ID/address binding.

Ten append-only ADVISORY records qualify existing trusted obligation/need and
exact-hint consumers, versioned U2 incomplete-witness handling, binding-verifier
adoption, Increment25 authoring, measured reuse, fixture/cohesion boundaries and
already implemented source-span reconciliation. U1's unrequested obligations
must not be confused with R1.7/R2 scoring harm. Those adverse scoring policies
remain intentionally unpromoted. [Exact receipts](../research/code-audit/ri-u1-r17-r2-intake.json)
preserve states and hash chains; no approval, B-number, grant or closure follows.

### R1 diagnostics, sensitivity and obligation-coverage intake

The [42-path audit](../research/ri-lexical-sensitivity-audit.md) adds pending BUG
[0182a013](proposals/0182a013-c116-4864-aa10-88ccc0c2a709/proposal.json): bounded
captures must authenticate the actual ranking prefix before diagnosing omitted
higher-ranked resources. A two-document independent probe demonstrates the
weakness; complete original captures do not demonstrate historical verdict impact.
The frozen owner is unchanged and a future versioned verifier is required.

Five append-only ADVISORY records materially qualify existing Localization
consumer15bae0a6, custody0385a359, fixturea88167f9, measured-reuseaedea41e and
cohesion39c6663a proposals. The [decision preparation](../research/task-obligation-coverage-decision.md)
recommends a trusted reviewed task-clause/obligation contract plus explicit
revisions, pending maintainer decision. Readiness remains scoped to supplied
obligations. The Case0009 instruction custody gap must be resolved with original
hash-matching bytes or retained unsupported replay, never reconstructed text.

[Exact Intake receipts](../research/code-audit/ri-lexical-intake.json) distinguish
the new proposal from advisory scope updates. R1's mixed separate-view result
and the unsafe sensitivity replacements remain intentional non-adoption; known
Graph3/U2/binding/normalization bugs keep their separate pending scopes. Previously
delivered physical-line repairs await operator reconciliation, not rediscovery.
No approval, B-number, implementation grant, dispatch or automatic closure follows.

## RI acquisition and shared-verification audit intake

The [78-path source/evidence audit](../research/ri-acquisition-structural-verification-audit.md)
adds four distinct **PENDING_REVIEW** bug proposals:

- [f85c4e7f](proposals/f85c4e7f-b5a4-4187-b80d-8a85aa200369/proposal.json): experiment-local physical-line/UTF-8 source-span correctness, distinct from the delivered production repair.
- [4742b0a2](proposals/4742b0a2-5e42-483d-95c5-09eac6efb0af/proposal.json): ambiguous entered operation must not be declared unentered from zero successful-return count.
- [9c7dff72](proposals/9c7dff72-ea91-4db3-a9a7-fb25971ec00a/proposal.json): Case4 required-resource partition includes413 non-required resources; preserve original report and supply versioned correction/erratum.
- [d183d412](proposals/d183d412-73c8-490c-8f02-a4dc8f3bb17d/proposal.json): marginal obligation/unit gains must not require a globally new resource; retained Case8 marginal totals remain qualified as agreeing.

[Eight advisory updates](../research/code-audit/ri-acquisition-intake.json) distinguish
reviewed-roster limits, delegable independent review and a future agent-proposal
milestone in15bae0a6 from implementation approval. Exact-locator, measured reuse,
application cohesion, fixture, binding-verifier, Graph3 report-assurance and custody
records retain their distinct scopes. The Case9 pinned instruction remains missing;
no reconstruction is authorized. Source-span fixes already delivered in a0a6c224
and supported binding-verifier subsets warrant operator reconciliation through
the existing process, not automatic approval/closure or rediscovery as uninvestigated.
The pending0182a013 diagnostic-ranking defect and other known bugs are unchanged.

These are intake and append-only evidence, not approved B-number stories,
implementation grants, dispatches or parent completion. Frozen science is unchanged.
