# B-0006 — Reconcile authoritative architecture documentation

- type: INVESTIGATION
- status: ACTIVE
- decision_maturity: READY_FOR_DESIGN
- necessity: REQUIRED
- architectural_significance: STRUCTURAL
- urgency: NOW
- evidence_basis: REPOSITORY
- scope: repository-level architecture documentation reconciliation
- parent: B-0001

## Problem / value

Reconcile repository-level architecture documentation with experimental Tools,
model serving, model benchmarks, worker telemetry, and reviewed boundaries.
This is documentation work, not package redesign.

## Evidence / invariants

The current graph describes frozen foundation domains but omits newer
experimental branches. Package-local docs remain authoritative for exact behavior.

## Dependencies / risks / validation

- hard_dependencies: none
- pressure_dependencies: B-0007
- operational_dependencies: none
- consumers: maintainers and future architecture work
- unresolved_semantics: which experimental relationships belong in the graph
- risk_if_deferred: maintainers infer boundaries from stale graphs
- risk_if_implemented_early: speculation presented as implemented fact
- promotion_trigger: reviewed scope for experimental branch documentation
- validation_level: INTEGRATION
- live_validation_trigger: not applicable; this is documentation work
- related: B-0001, B-0007
