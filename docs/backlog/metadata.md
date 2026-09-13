# Backlog Metadata

## Required identity and lifecycle fields

Each record has id, type, title, status, and decision_maturity. Unknown values
must be written as explicit uncertainty, not guessed.

| Field | Controlled values |
| --- | --- |
| type | EPIC, STORY, INVESTIGATION |
| status | BACKLOG, BLOCKED, DEFERRED, ACTIVE, IMPLEMENTED, VALIDATED, SUPERSEDED, CLOSED |
| decision_maturity | DISCOVERED, NEEDS_INVESTIGATION, SEMANTICS_PARTIAL, READY_FOR_DESIGN, READY_FOR_IMPLEMENTATION |
| necessity | REQUIRED, OPTIONAL, EXPLORATORY, FUTURE_REQUIRED |
| architectural_significance | FOUNDATIONAL, STRUCTURAL, SUPPORTING, HARNESS_LOCAL, PROVIDER_LOCAL |
| urgency | NOW, SOON, DEFERRED |
| validation_level | NONE, UNIT, INTEGRATION, LIVE_SINGLE_HARNESS, LIVE_MULTI_HARNESS |

Status describes lifecycle selection; decision_maturity describes how well the
semantics are understood. They are intentionally independent.

## Architectural ownership

Each canonical record also identifies one `primary_domain` and, when needed,
`supporting_domains`.

- **Primary domain** owns the architectural pressure and is accountable for
  its eventual semantic boundary.
- **Supporting domains** participate in the concern without taking ownership
  of that boundary.
- Use `supporting_domains: none` when no secondary domain participates.
- `experiments` is permitted as a primary domain only for non-reusable
  composition whose semantics have not been promoted into `src/devtools/`.

Allowed reusable domains are `core`, `resources`, `models`, `agents`,
`context`, `tools`, `execution`, `orchestration`, `governance`,
`observability`, `persistence`, and `evaluation`.

`documentation` is a narrow non-reusable administrative owner for records
about the repository's authoritative documentation itself. It is not a
thirteenth framework domain. `experiments` is the corresponding non-reusable
owner for unpromoted composition.

Cross-domain participation never removes the need for a primary owner. The
field describes architectural ownership, not current Python package location.

## Split lineage and semantic decisions

When a record is decomposed, the original record remains canonical historical
lineage. It uses `status: SUPERSEDED`, names `split_children`, and explains the
scope that was separated. Each surviving child uses `split_from: B-XXXX`.

`semantic_decision: RESOLVED` records that an investigation's terminology or
ownership question is answered by authoritative architecture. It does not
authorize implementation. A resolved decision can therefore remain
`status: DEFERRED` while its reusable implementation lacks a consumer.

## Evidence, scope, dependencies, and risk

Records preserve these independent dimensions when meaningful. Unknown values
are written explicitly as `unknown`, rather than inferred merely to complete a
template:

    evidence_basis
    scope
    consumers
    hard_dependencies
    pressure_dependencies
    operational_dependencies
    blocked_by
    risk_if_deferred
    risk_if_implemented_early
    established_invariants
    unresolved_semantics
    promotion_trigger
    validation_level
    live_validation_trigger
    first_harness_consumer
    second_harness_trigger

Evidence basis may name RESEARCH, REPOSITORY, REAL_USE, or MULTIPLE; it is
descriptive rather than a score.

## Promotion discipline

Promotion requires sufficient evidence that a semantic boundary is stable
independently of an experimental or local implementation. Useful evidence may
include independent consumers, heterogeneous repeated use, multiple
architectural pressures converging on the same boundary, demonstrated reuse
without experiment-specific assumptions, or requirements that cannot remain
cleanly local. No universal consumer count automatically authorizes promotion.

Dependency meanings are distinct:

- **Hard prerequisite:** the dependent work cannot responsibly proceed first.
- **Pressure dependency:** concepts are related, but the relationship is not
  frozen.
- **Operational prerequisite:** needed for an implementation or experiment,
  not conceptually foundational.

## Record body

Every epic or item records problem/value, evidence, consumers, invariants,
prerequisites/dependencies, unresolved semantics, risks, promotion trigger,
validation expectations, and related records. Investigations must not invent
final acceptance criteria before their semantics are known.
