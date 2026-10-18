# B-0048 — Restore Python 3.12 JSON file-model compatibility

- type: STORY
- status: BACKLOG
- decision_maturity: DISCOVERED
- primary_domain: resources
- supporting_domains: unknown
- evidence_basis: REPOSITORY
- hard_dependencies: unknown
- pressure_dependencies: unknown
- operational_dependencies: unknown
- validation_level: NONE
- execution_authorization: NONE
- proposal: ../proposals/f47f3925-6988-4d84-81f4-c5b97a571484/proposal.json
- intake_review: ../proposals/f47f3925-6988-4d84-81f4-c5b97a571484/review-0002.json

## Problem / value

The declared Python >=3.12 distribution fails a JsonObjectFile constructor on installed CPython 3.12.13. Current development verification uses Python 3.14; compatibility remains unresolved.

## Proposed benefit

Restore trustworthy declared-version compatibility and prevent local worker/environment confusion.

## Uncertainty / unresolved semantics

The affected model family, minimal correction, and supported interpreter test matrix require investigation. This proposal provides no implementation or execution authority.

## Discovery / parent

{'kind': 'agent', 'reference': 'git:224644cc4276fd58074329be01be44b7012553b7:docs/implementation_ledger.md (Python 3.12 compatibility observation)'}
B-0009

## Evidence

docs/backlog/proposals/python312-reproduction.json
docs/implementation_ledger.md (unchanged-main JsonObjectFile reproduction and prior 54 Python 3.12 test failures)

## Affected resources

src/devtools/resources/filesystem/models/json/object.py
pyproject.toml

## Possible dependencies

B-0009: pressure only; the current worker remains validated on Python 3.14.

## Consumers / invariants / risks

unknown; preserve existing behavior and authority boundaries

## Promotion / validation expectations

Backlog inclusion only. Scope, priority, dependencies and acceptance require deliberate review before implementation.

