# B-0015 — Framework Acceptance & Harness Validation

- type: EPIC
- status: BACKLOG
- decision_maturity: NEEDS_INVESTIGATION
- necessity: REQUIRED
- architectural_significance: STRUCTURAL
- urgency: SOON
- evidence_basis: MULTIPLE
- scope: cross-cutting framework acceptance methodology

## Problem / value

Ensure shared framework semantics graduate from deterministic tests to real
specialized-harness validation when a meaningful end-to-end path exists.

## Invariants / dependencies / validation

Unit coverage is necessary but insufficient for agent-facing semantics. Live
tests validate framework enforcement against a model request, not voluntary
model obedience.

- hard_dependencies: none
- pressure_dependencies: B-0003, B-0005
- operational_dependencies: a meaningful first harness path
- children: B-0016
- unresolved_semantics: live evidence sufficiency and nondeterminism handling
- risk_if_implemented_early: generic live-test framework
- risk_if_deferred: semantics are accepted from mocks alone
- promotion_trigger: structural primitive has deterministic coverage and a live path
- validation_level: INTEGRATION
- live_validation_trigger: a structural primitive has a meaningful live path
