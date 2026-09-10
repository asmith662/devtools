# Architecture Backlog

## Purpose and authority

The backlog records known work, architectural pressure, investigations, and
unresolved responsibilities discovered through research, audits, or real use.
It answers: **what needs deliberate future attention?**

Backlog presence does not authorize design or implementation. Package-local
documentation remains authoritative for implemented package behavior;
[architecture](../architecture.md) owns current cross-package architecture;
[roadmap](../roadmap.md) records deliberately selected near-term sequencing;
and the implementation ledger records historical fact. The repository currently
has no separate ADR process. If one is later adopted, accepted decisions belong
there, not in unresolved backlog records.

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

See [metadata.md](metadata.md) for record semantics.
