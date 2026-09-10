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
