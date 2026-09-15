# Architecture Backlog

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
| [B-0008](items/B-0008-investigate-repository-context-discovery.md) | Investigate repository-context discovery | BACKLOG | context |
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

See [metadata.md](metadata.md) for record semantics and promotion discipline.
