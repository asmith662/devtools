# B-0047 — Protected development validation profile

- id: B-0047
- type: INVESTIGATION
- status: BACKLOG
- decision_maturity: NEEDS_INVESTIGATION
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
and 100% production branch coverage. This is demonstrated operational evidence,
not a supported general profile or permission to run sealed audit tests.

## Scope and invariants

Investigate a documented supported profile declaring eligible development tests,
excluding sealed/retained outcomes and preserving meaningful coverage gates.
Host-owned comprehensive validation stays separate. Selection must precede
collection; filtering after a sealed test executes is insufficient. Confirmation
contents are unnecessary to establish isolation. Preserve repository artifacts
and other workers' files. This pressure authorizes no universal harness,
sandbox framework, registry, runner or production RI/Retrieval changes.

- consumers: protected development agents and host validators
- hard_dependencies: none
- pressure_dependencies: B-0015, B-0002
- operational_dependencies: host-owned separation of development and sealed material
- risk_if_deferred: default discovery can invalidate prospective isolation
- risk_if_implemented_early: local experiment policy becomes framework semantics
- unresolved_semantics: supported selection/exclusion mechanism, artifact boundaries, coverage accounting and host/developer responsibilities
- promotion_trigger: repeated protected work requires an explicit profile whose isolation can be validated without reading sealed material
- validation_level: NONE
- live_validation_trigger: none; deterministic development isolation
