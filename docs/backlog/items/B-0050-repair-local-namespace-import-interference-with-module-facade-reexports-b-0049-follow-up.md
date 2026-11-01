# B-0050 — Repair local-namespace import interference with module facade reexports (B-0049 follow-up)

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
- proposal: ../proposals/f3f3068e-cb95-4718-9def-ba432b1f3ea4/proposal.json
- intake_review: ../proposals/f3f3068e-cb95-4718-9def-ba432b1f3ea4/review-0001.json

## Problem / value

Linked bounded continuation of B-0049 review-0003, not an independent duplicate obligation. Current src/devtools/context/python/imports/members.py still refuses a valid module facade reexport when an unrelated function, async function or class imports the same name in its own namespace. Fresh public and independently authored private baseline checks reproduce the defect. B-0049 original dispatch remains consumed; its broader competing-binding and Reference pressure remains open.

## Proposed benefit

One-file behavioral repair: unrelated local namespaces must not invalidate module reexports; preserve module conditional/try/star imports, aliases, genuine competing declarations and non-Name binding guards conservatively. Measure one real governed 64K native coder episode and, only for a lawful candidate, independent review and a read-only integration plan. Candidate archival/restoration only; no automatic install, merge, publication or closure.

## Uncertainty / unresolved semantics

A linked child is required because Intake terminal approvals require a new related proposal and WorkCycle has one assignment per canonical item. This does not resolve or duplicate the broader B-0049 obligation. Scripted tests establish mechanics, not Qwen competence. 2048-token generation performance is not established by prior 128-token neutral probes. Private acceptance is bounded, independently authored, and not exhaustive.

## Discovery / parent

{'kind': 'research', 'reference': 'docs/research/live-native-maintenance-task.md; docs/research/code-audit/live-native64-20261101/preflight.json'}
B-0049

## Evidence

docs/backlog/proposals/ff4c4110-9c3b-480d-8f0f-77cf4610b700/review-0003.json
docs/research/code-audit/live-native64-20261101/preflight.json
docs/research/live-native-maintenance-task.md

## Affected resources

src/devtools/context/python/imports/members.py
src/devtools/context/python/modules/bindings.py
tests/context/python/imports/test_members.py

## Possible dependencies

B-0049
ff4c4110-9c3b-480d-8f0f-77cf4610b700

## Consumers / invariants / risks

unknown; preserve existing behavior and authority boundaries

## Promotion / validation expectations

Backlog inclusion only. Scope, priority, dependencies and acceptance require deliberate review before implementation.

