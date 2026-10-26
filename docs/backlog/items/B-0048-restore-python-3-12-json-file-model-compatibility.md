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

## Filesystem audit maintenance evidence — 2026-10-26

On main `26bd8053ab8ad8323dd3273b4b0e986de05388e9`, existing CPython3.12.13 reproduces TypeError `super(type, obj): obj must be an instance or subtype of type` in JsonObjectFile, JsonListFile and CsvFile direct construction, their codecs, public object read and ToolRunner rich-object read (eight failures). Four scalar/Markdown/text/binary controls pass. All twelve corresponding3.14 calls pass. Existing3.12 has no pytest; this is bounded native behavioral evidence, not a complete supported-runtime matrix. Zero-argument super in these three slotted model post-init bodies is the common current failure boundary.

Existing B-0048 and its already recorded list/CSV siblings remain sufficient; no new compatibility proposal or scope closure. A future bounded maintainer-authorized correction should cover all three model families, parsed/read and immutable-transform consumers, independent3.12/3.14 tests and full final committed production validation. The historical object-only accepted worker candidate/review is evidence, not current destination validation or publication authority. No grant or source change is issued here. Existing status/maturity/authorization fields remain unchanged. [Audit](../../research/filesystem-codecs-and-models-audit.md), [exact probes](../../research/code-audit/filesystem-codecs-models-probes.json). `audit:filesystem-codecs-models:26bd8053:20261026`.
