# B-0049 — Prevent one-facade import fallback from overriding competing pattern or handler bindings

- type: STORY
- status: BACKLOG
- decision_maturity: DISCOVERED
- primary_domain: context
- supporting_domains: unknown
- evidence_basis: REPOSITORY
- hard_dependencies: unknown
- pressure_dependencies: unknown
- operational_dependencies: unknown
- validation_level: NONE
- execution_authorization: NONE
- proposal: ../proposals/ff4c4110-9c3b-480d-8f0f-77cf4610b700/proposal.json
- intake_review: ../proposals/ff4c4110-9c3b-480d-8f0f-77cf4610b700/review-0003.json

## Problem / value

P1 maintained RI false-positive References. With actual observed target.py defining f, facade.py importing f then binding f through MatchAs, MatchStar, MatchMapping.rest or ExceptHandler.name, corrected direct module lookup refuses unique declaration truth, but resolve_python_imported_member returns RESOLVED. references.declarations.resolution._resolve overrides the direct refusal with ONE_FACADE and emits a direct-call Reference to target.f. Real ContextTools source_relationships dispatch also exposes the incorrect target for capture and handler cases. Six independently authored source fixtures include valid plain import and refusing ordinary-assignment controls. No source fixture executed, model invoked or edit-authority bypass established.

## Proposed benefit

Bounded owner: one-facade imported-member resolution and its Reference fallback, separate from the delivered direct lookup/module-local/base correction. Fail closed on genuine competing bindings and preserve qualified support/reasons. Reuse the maintained non-Name binding extraction only with correct facade scope/traversal; never blindly scan nested local scopes. Acceptance: real retained-source independent regressions for simple/star/mapping-rest captures and exception aliases after facade import; unrelated/local names, unchanged sync/async facade and ordinary assignments remain correct; before/after/lifetime differences remain conservative rather than interpreted at runtime. No fallback may upgrade an authenticated competing-binding refusal into a positive Reference. Cover complete resolver-to-Reference-to-ContextTools ToolRunner composition with literal target/refusal expectations, stale/foreign inputs and stable provenance. Preserve syntactic declaration selection and edit authority. Run focused regressions, Ruff/format, strict mypy and final-tree protected 100% branch coverage before normal PR promotion.

## Uncertainty / unresolved semantics

Observed at main457def and actual maintained APIs; synthetic tiny source repositories establish production code-path correctness failure, not observed historical corruption or autonomous engineering harm. No source fix in this audit: separate bounded repair requires permanent regressions/full gate. Pattern capture and exception alias lifetimes differ; do not erase those distinctions or build a general scope evaluator. Target-module rebinding and other unsupported forms require explicit inspection during the bounded repair, not an assertion that they are already fixed. Original proposal16b27e74 remains implemented and merged for its three-owner scope; this is a distinct facade/fallback responsibility not included in that patch.

## Discovery / parent

{'kind': 'research', 'reference': 'docs/research/ri-configuration-role-closure-audit.md'}
B-0002

## Evidence

docs/research/ri-configuration-role-closure-audit.md
docs/research/code-audit/ri-config-role-probes.json

## Affected resources

src/devtools/context/python/imports/members.py
src/devtools/context/python/references/declarations/resolution.py
src/devtools/context/python/modules/bindings.py
tests/context/python/imports/test_members.py
tests/context/python/references/declarations/test_analysis.py
apps/qwen/context_tools.py
tests/apps/qwen/test_context_tools.py

## Possible dependencies

16b27e74-f553-40a8-b342-c3458a7b7a01
B-0008

## Consumers / invariants / risks

unknown; preserve existing behavior and authority boundaries

## Promotion / validation expectations

Backlog inclusion only. Scope, priority, dependencies and acceptance require deliberate review before implementation.

