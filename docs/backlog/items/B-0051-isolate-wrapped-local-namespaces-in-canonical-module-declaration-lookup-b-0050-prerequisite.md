# B-0051 — Isolate wrapped local namespaces in canonical module declaration lookup (B-0050 prerequisite)

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
- proposal: ../proposals/cdbe84f8-5f1d-47a9-a421-131db4966a1e/proposal.json
- intake_review: ../proposals/cdbe84f8-5f1d-47a9-a421-131db4966a1e/review-0001.json

## Problem / value

Related canonical prerequisite for unresolved B-0049/B-0050 facade repair. Offline exact B-0050 candidate reproduction shows its repaired consumer guard prunes conditional-local imports, but canonical modules/declarations.py independently walks into local bodies and returns ambiguity. Repair ONLY this canonical owner; keep the original facade consumer defect and parent obligations open. Fresh baseline: 17 of 38 public semantic cases and 8 of 12 distinct private holdouts fail; 17 maintained module-selection tests pass.

## Proposed benefit

Restore bounded module/local binding distinctions in the canonical lookup without bypassing refusal in a consumer. Preserve direct target/source provenance and genuine module stores, declarations, imports, aliases, patterns, handlers, star/dynamic conservatism. One supervised model-authored continuation; no reference implementation, automatic installation or closure.

## Uncertainty / unresolved semantics

The complete parent facade repair spans two owners and does not fit native one-file v1 safely. This item is a related prerequisite, not a duplicate independent obligation or completion of the parent. Public tests disclose the prior revealed failure category; private holdouts use separately authored non-import binding/provenance distinctions. Bounded acceptance is not exhaustive Python semantics. Native WorkCycle rejects provider-specific sampling overrides; an approved future episode must disclose unchanged defaults rather than bypass that guard.

## Discovery / parent

{'kind': 'research', 'reference': 'docs/research/code-audit/native-scope-followup-20261101/historical-causal-reproduction.json'}
B-0050

## Evidence

docs/research/live-native64-maintenance-task.md
docs/research/code-audit/native-scope-followup-20261101/behavioral-baseline.json
docs/research/code-audit/native-scope-followup-20261101/public-matrix.json

## Affected resources

src/devtools/context/python/modules/declarations.py
src/devtools/context/python/modules/bindings.py
tests/context/python/modules/test_selection.py

## Possible dependencies

B-0050
B-0049

## Consumers / invariants / risks

unknown; preserve existing behavior and authority boundaries

## Promotion / validation expectations

Backlog inclusion only. Scope, priority, dependencies and acceptance require deliberate review before implementation.

## Prepared live continuation

The [failure analysis and frozen acceptance](../../research/native-scope-followup.md)
document this canonical prerequisite and the still-unresolved parent facade repair.
Human Intake approval does not grant coding, installation or closeout authority.
