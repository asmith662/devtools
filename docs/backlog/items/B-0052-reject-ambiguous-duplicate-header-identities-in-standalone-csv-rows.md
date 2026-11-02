# B-0052 — Reject ambiguous duplicate header identities in standalone CSV rows

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
- proposal: ../proposals/1caa2686-428f-4fdf-b052-f0b8382b44dc/proposal.json
- intake_review: ../proposals/1caa2686-428f-4fdf-b052-f0b8382b44dc/review-0001.json

## Problem / value

Current exported CsvRow admits exact duplicate header names: CsvRow(("id","id"),("first","last"))["id"] returns "first" while as_dict()["id"] returns "last". This inconsistency loses one cell in keyed mapping access. CsvFile and CsvCodec already reject duplicate headers, but public standalone construction bypasses those checks. Repair only standalone exact-name uniqueness admission in the existing model owner.

## Proposed benefit

Make positional, keyed and mapping views agree for every admitted standalone row. Reject exact duplicate names with ValueError after immutable input capture. Preserve exact case/spacing/Unicode spelling, cell order, existing width/type validation, conversion and codec/file behavior. A real one-file model repair with frozen public regressions and independent holdouts; no automatic installation.

## Uncertainty / unresolved semantics

No production data loss observed beyond authored in-memory API calls. Empty standalone rows and unique blank names are outside this repair and retain current behavior. No new normalization, CSV dialect, codec change, transaction, schema migration or broader header type policy. This is a newly reproduced model-owner defect, distinct from delivered NONNUMERIC proposal 67f7d086-86d9-400f-bfaf-d9bc4df9aea1. No earlier dispatch exists.

## Discovery / parent

{'kind': 'agent', 'reference': '.local/e2e-native/frozen.json; current main 0227cdfc23fe73b457f13f15f77a27b1f6bc11e1; independent actual public API reproduction'}
None

## Evidence

src/devtools/resources/filesystem/docs/csv.md
tests/resources/filesystem/models/csv/test_row.py
docs/development/filesystem-contract-repair.md

## Affected resources

src/devtools/resources/filesystem/models/csv.py
tests/resources/filesystem/models/csv/test_row.py
tests/resources/filesystem/models/csv/test_file.py
tests/resources/filesystem/codecs/test_csv.py

## Possible dependencies

Existing CSV model contracts; human Intake approval, exact native coding authority, independent acceptance/review and separate integration authority.

## Consumers / invariants / risks

unknown; preserve existing behavior and authority boundaries

## Promotion / validation expectations

Backlog inclusion only. Scope, priority, dependencies and acceptance require deliberate review before implementation.

