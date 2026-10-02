# B-0047 — Protected development validation profile

- id: B-0047
- type: INVESTIGATION
- status: VALIDATED
- decision_maturity: READY_FOR_IMPLEMENTATION
- necessity: REQUIRED
- architectural_significance: SUPPORTING
- urgency: SOON
- evidence_basis: REAL_USE
- primary_domain: evaluation
- supporting_domains: context
- scope: explicit supported deterministic development validation isolation

## Problem and evidence

Prospectively frozen dogfood work needs development checks that cannot collect
sealed confirmation or retained outcome tests. Case 0003 development uses
explicit production-neighbor directories and a new-package coverage override.
The ordinary project has `testpaths = ["tests"]` and production-wide 100%
coverage; that default does not express this protected boundary. Local
cache/temp restrictions also need writable operational destinations, distinct
from semantic test selection.

The Case 0003 host subsequently validated a stronger bounded invocation:
`uv run pytest tests --ignore=tests/experiments tests/experiments/test_codex_dogfood_capture.py tests/experiments/codex_dogfood/test_case_0003.py`.
It excludes the retained experiment tree before recursive collection and admits
only the two explicit dogfood files. All 1,299 tests passed with two live skips
and 100% production branch coverage. The supported general profile now uses
the same pre-collection `tests/experiments/` boundary and runs the remaining
ordinary test tree through `uv run python scripts/validate_development.py`.

## Implemented contract

The operational entry point is `scripts/validate_development.py`. It invokes
pytest over `tests/` with `tests/experiments/` ignored before recursive
collection. This stable directory boundary excludes retained replay and
outcome-dependent material without inspecting outcomes or maintaining a list
of sensitive test node IDs. It leaves project pytest options, including the
100% production branch-coverage requirement, intact and returns pytest's
failure code. The profile contract and separate static quality gates are
documented in `docs/development/validation.md` and linked from `AGENTS.md`.

## Scope and invariants

The profile declares the ordinary test tree while excluding the experiment tree
before collection and preserving production coverage gates. Host-owned
confirmation validation stays separate. Confirmation contents are unnecessary
to establish isolation. This capability is a repository-local command, not a
universal harness, sandbox framework, registry, runner, or Evaluation redesign.

- consumers: protected development agents and host validators
- hard_dependencies: none
- pressure_dependencies: B-0015, B-0002
- operational_dependencies: host-owned separation of development and sealed material
- risk_if_deferred: default discovery can invalidate prospective isolation
- risk_if_implemented_early: local experiment policy becomes framework semantics
- established_invariants: exclusion occurs before collection; the whole experiment-test subtree is excluded by repository role; configured production coverage remains enabled; confirmation outcomes are not read to select tests
- unresolved_semantics: none for the bounded protected development profile; confirmation validation remains separately governed
- promotion_trigger: satisfied by repeated protected work and a validated repository-local command
- validation_level: INTEGRATION
- live_validation_trigger: none; deterministic development isolation
