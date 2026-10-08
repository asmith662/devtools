# Case 0011 reviewed gold and reliability conclusion

Reviewed gold is COMPLETE and immutable. It is the architecture-grade Case 0011 evaluation target. Primary gold alone was unsafe for architecture conclusions. Independent review exposed material necessity and witness-structure instability. These are case-local conclusions; no cross-case generality or U1 effectiveness is established.

## Construction and supported necessity semantics

The builder reads only the frozen task/resource frame, primary Stage C, independent Stage C-R, neutral disagreement packet/agreed-cell seal, and sealed reconciliation decisions. Source adjudications remain immutable. Reviewed gold has not existed before this checkpoint. C.5 and Stage D remain unperformed at import time.

REQUIRED means necessary within at least one acceptable witness alternative for that obligation; it does not mean present in every alternative or every valid task solution. The entire required union is not simultaneously necessary.

Full frame: 531 resources × 9 obligations = 4779 cells. Labels: {'HELPFUL_ONLY': 84, 'REQUIRED': 23, 'UNNECESSARY': 4672}. Provenance: {'INHERITED_AGREEMENT': 4713, 'RECONCILED_DISPUTE': 65, 'RECONCILED_EXCEPTION': 1}. Duplicate, missing and unexpected qualified identities: zero. Unresolved reconciliation propositions: zero.

All 140 propositions resolved: ACCEPT_POSITION_1 = 35; ACCEPT_POSITION_2 = 33; REPLACE_WITH_RECONCILED_JUDGMENT = 72; UNRESOLVED = 0. The 4,714-cell seal is verified; 4,713 labels/content/qualified identities inherit unchanged and one explicit validation-script exception becomes HELPFUL_ONLY. Reconciled reviewed-unit bindings are separate from the inherited source claims. Every unit retains its exact statement, obligation scope, source spans/content identity/excerpt digest, necessity rationale, inferability, alternative membership and decision provenance. No new semantic adjudication was performed during import.

## Exact witness structures

Required units: 32; required resource union: 16. Alternative counts: {'bytes': 1, 'ceiling': 3, 'documentation': 1, 'exports': 1, 'frame': 1, 'ownership': 2, 'request': 1, 'tests': 1, 'validation': 1}. Six complete Cartesian-product combinations produce two distinct resource unions and three distinct unit unions. Minimum sufficient resource union = 15; maximum = 16. Task-indispensable resources = 15; task-indispensable units = 30. Minimum/maximum sufficient unit unions = 30/31. ALL members of an alternative are complementary; ANY complete alternative suffices. Incompatible alternatives are never mixed.

| Obligation | Indispensable resources | Indispensable units |
| --- | ---: | ---: |
| bytes | 1 | 2 |
| ceiling | 1 | 1 |
| documentation | 2 | 2 |
| exports | 2 | 2 |
| frame | 5 | 9 |
| ownership | 1 | 2 |
| request | 2 | 3 |
| tests | 2 | 6 |
| validation | 2 | 4 |

Exact resource/unit sets, six combinations, alternative-specific evidence bindings and minimum/maximum unions live in reviewed_statistics.json and reviewed_gold.json. The optional resource in the 16-member union is the model-usage numeric-admission witness; the 15-member witness establishes the ceiling through request-side alternatives. The entire required union is not simultaneously necessary.

Required resource union:

- `docs/architecture.md`
- `docs/development/validation.md`
- `pyproject.toml`
- `src/devtools/context/__init__.py`
- `src/devtools/context/planning/__init__.py`
- `src/devtools/context/planning/docs/overview.md`
- `src/devtools/context/planning/materialization.py`
- `src/devtools/context/planning/plan.py`
- `src/devtools/context/planning/rendering.py`
- `src/devtools/context/planning/resource.py`
- `src/devtools/context/python/function/planned_reference.py`
- `src/devtools/context/python/function/qualified_reference.py`
- `src/devtools/models/interaction/models.py`
- `src/devtools/models/interaction/usage.py`
- `tests/context/planning/test_plan.py`
- `tests/models/interaction/test_models.py`

## Reliability and source changes

Primary versus independent REQUIRED cells: intersection 22, union 40, Jaccard 0.55; primary 38, independent 24, with 16 primary-only and two independent-only required cells. Only 22/38 primary required cells were retained. Aggregate 4,714/4,779 agreement is dominated by unnecessary cells and does not establish necessity reliability.

Primary → reviewed: 32 label changes (16 REQUIRED → HELPFUL_ONLY, one HELPFUL_ONLY → REQUIRED, 11 HELPFUL_ONLY → UNNECESSARY, four UNNECESSARY → HELPFUL_ONLY). Required cells 38 → 23; required resource union 26 → 16; source unit account 42 (including one supplemental operational handoff) → 32 reconciled semantic units. Alternatives 20 → 12; complete combinations 144 → 6; sufficient resource range 23–25 → 15–16; task-indispensable resources 22 → 15. Broad/redundant claims are narrowed into exact supported necessary fragments, corroboration is separated, and the operational handoff is removed from semantic task-gap/witness scope. Unit identities/granularities are distinct, so these counts are not a one-to-one semantic deletion metric.

C-R → reviewed: 35 label changes (31 UNNECESSARY → HELPFUL_ONLY, one HELPFUL_ONLY → REQUIRED, one HELPFUL_ONLY → UNNECESSARY, two REQUIRED → HELPFUL_ONLY). Required cells 24 → 23; required resource union 17 → 16; units 31 → 32; alternatives remain 12 but are reconstructed with reconciled membership/evidence. Complete combinations 8 → 6; sufficient range 15–17 → 15–16; task-indispensable resources remain 15. The alternative numeric-admission witness is retained; redundant validation-script necessity is removed; corroborating resources are retained as helpful. Exact label changes are listed in reviewed_statistics.json, with all source decisions available in the immutable reconciliation.

Necessity judgments, unit granularity, witness sufficiency and exception interpretations remain case-local human judgments over this frozen frame. Independent reconstruction validates their consistency and source support, not a universal truth reference. No treatment result has been joined.

## Task gap and process safeguard

Task gap = NONE, following the explicit reconciled task-gap decision. Repository-information gap is not introduced by operational completion reporting.

`.local/codex-result.md` is an operational, ignored, non-authoritative result handoff used to relay Codex output. It is not repository feature semantics, not part of implementation correctness, not a repository resource, and not eligible as a task obligation, information need, witness, required resource, task gap, or repository-information gap.

## Interpretation limitations

Each exact reconciled statement below constrains implementation, blocks no judgment and requires no inherent discovery. Decision-specific exact evidence remains in reconciliation.json; this publication preserves the accepted wording and impact.

### Fresh-state versus retained-frame checks

Foreign/stale checks apply at planning and materialization against supplied retained snapshots. Existing assembly has no fresh snapshot argument and cannot discover subsequent filesystem changes; preservation must not be read as requiring newly current-state validation during assembly.

This genuine retained-state/current-state boundary constrains the future implementation and stale-test interpretation, but does not block gold necessity judgments.

Disposition: constrains implementation = YES; blocks no judgment = YES; requires no inherent discovery = YES.

### Canonical Context versus outer envelope

The task counts exact rendered Context including headings/separators. Canonical rendering produces context.text, while assembly adds an outer Context length label and begin/end markers. The existing separate Context length supports len(context.text.encode("utf-8")); the task does not explicitly name whether outer Context envelope markers also belong to the ceiling.

The reconciled witness uses the canonical rendered-text boundary. This genuine wording boundary constrains specification of future byte tests/API behavior; it does not make either source account unresolved.

Disposition: constrains implementation = YES; blocks no judgment = YES; requires no inherent discovery = YES.

### Materialized versus rendered public input

The exact task names an already materialized ContextDisclosure as supplied input; the current exported assembler accepts RenderedContextDisclosure. Future implementation must account for canonical rendering and this public-input mismatch; the task does not select a new signature, compatible wrapper or precise compatibility arrangement.

This concrete input-type mismatch constrains the implementation design and public API documentation; it does not block identifying necessary current input/rendering information.

Disposition: constrains implementation = YES; blocks no judgment = YES; requires no inherent discovery = YES.

### Nonuniform numeric exception conventions

The task requires existing validation/error conventions, but reusable request numeric admission raises ValueError for bool/non-int, whereas reusable ModelUsage admission raises TypeError for those types and ValueError for negatives. Thus frozen evidence does not identify a unique new exception policy.

This genuine nonuniform repository convention limits inference of exact exception assertions, while allowing either documented numeric witness. Argument naming and exact message wording are ordinary design choices and are not retained as interpretation limitations.

Disposition: constrains implementation = YES; blocks no judgment = YES; requires no inherent discovery = YES.

### Zero ceiling and canonical nonempty disclosure

The task permits zero only for zero-byte rendered Context. Current valid plans prohibit empty choices, and canonical common rendering always emits nonempty headings, so ordinary valid common disclosures cannot exercise a zero-byte success path.

This mismatch between a generic admission rule and currently reachable representations constrains testing: zero must reject ordinary canonical disclosures; do not weaken plan invariants or fabricate a zero-header representation. It does not block the ceiling rule.

Disposition: constrains implementation = YES; blocks no judgment = YES; requires no inherent discovery = YES.

### Native provenance versus request presentation

Native provenance is retained in MaterializedDisclosureItem/ContextDisclosure and the rendered value's disclosure reference; ModelRequest has no disclosure-provenance field. Preserve the caller's native chain and copy the request without inferring a new request field.

The provenance-preservation wording crosses a native-artifact/presentation boundary. It constrains future implementation without requiring provenance persistence or blocking current necessity judgments.

Disposition: constrains implementation = YES; blocks no judgment = YES; requires no inherent discovery = YES.

## Integrity, replay and publication boundaries

Authoritative reconciliation workspace: `C:\Users\recoveryadmin\AppData\Local\Temp\case_0011_reconciliation_sterile_1ae9b07`. Immutable reconciliation SHA-256: `f3d7c291b9ca17e1e4a7b73400871cc8be3b8bd27b28303dcd822f6ed3094a44`. Archive, decompressed payload, packet, manifest, integrity and agreed-cell seal use exactly their declared digest scopes; no additional serialization requirement is imposed on imported output.

reviewed_gold.json SHA-256: `0d6f54a4ab1eed68b2deb4f4557ef767ff9f2a7771eebde534527c425ae34430`; reviewed_statistics.json SHA-256: `3b04391f5977dd4ce09bfe8255c9302b6cd02036308462592eec5c4baf131596`. The checksum file seals the gold. The deterministic builder refuses overwrites and --check reconstructs exact bytes. Publication/validation notes are outside the imported reconciliation hash set.

The original reconciliation reports ten isolated tests passed. Its temporary authored test suite was removed in the source workspace, as explicitly recorded in the sealed validation object; it is not available to rerun. This import independently verifies all 140 identities/decisions, full frozen source support, inherited-cell seal, cells/units/alternatives, exact products/intersections, limitations/gap, byte-identical replay and overwrite refusal with the repository-authored reviewed suite. No claim is made to have rerun that removed suite.

## Prepared separate Stage C.5

The separate ../stage_c5/ packet has 18 frozen manual InformationNeeds × 32 units = 576 pairs, including all cross-obligation mappings. It projects only pre-acquisition semantics, exact original task/obligations, unit semantics and alternative membership. Three unit statements omit answer-location names while retaining their fact semantics. Opaque neutral unit/alternative IDs bind to reviewed gold via the repository-side projection_audit.json, which is never supplied to the reviewer. Original source-unit identities, decision provenance and chronology are absent from the packet.

The packet manifest binds exact reviewed-gold bytes and exact canonical frozen semantic-needs projection. The repository-side audit additionally binds the original authoring container SHA without exposing query fields. Query values are never selected or inspected. C5_PACKET_REVIEW.md shows the maintainer exactly the future reviewer content; it is not C.5 gold. Strict nested metadata allowlists, answer-location rejection and leakage injection tests pass.

Sterile workspace: `C:\Users\recoveryadmin\AppData\Local\Temp\case_0011_stage_c5_sterile_5ade1674`. Exact files: C5_INSTRUCTIONS.md, manifest.json, packet.json.gz, integrity.json. No checkout, Git, directory children, symlinks, junctions or reparse points. The workspace matches the repository packet byte-for-byte.

| Digest scope | SHA-256 |
| --- | --- |
| archive_sha256 | `da77c2a3e32129eabd3ffe4331ae2a1caef91cffffbd21b728420a953ad7e6f1` |
| canonical_payload_sha256 | `c7b0236c21b1cf6168f6eac123f412dd8e90df8dad7058829b99107d7be2ebe3` |
| manifest_sha256 | `b39d7b9121d07f5a842bbed40f5a876d828d0fa7a82d3900b05f428a622892f1` |
| integrity_sha256 | `d85c45a838586fead1ba25791a5f6d9c5d69db97b249d2a0ba3f3571695bfd66` |
| frozen_needs_sha256 | `8e951bc42ee08db656717ffb494880de26007c087d31f38657b421b8793c54aa` |

Stage C.5 packet = PREPARED; Stage C.5 adjudication = NOT PERFORMED; Stage D = NOT PERFORMED; U1 effectiveness = UNKNOWN. No lexical query values, retrieval results, candidate memberships, ranks, scores, acquisition costs, treatment outcomes or confirmation data were inspected. However, protocol.py was opened to establish frozen InformationNeed identity projection and exposed A/B/C query wiring. This violated the operator treatment-arm access restriction. Publication is stopped before commit/push; this checkpoint cannot claim that treatment-arm identities were not accessed. The prepared future-reviewer packet contains no arm identities, and no C.5 or Stage D adjudication was performed. Only frozen InformationNeed semantics were projected from their permitted authoring container.

Next step: Start a completely fresh treatment-blind Stage C.5 session from the prepared sterile workspace and adjudicate only InformationNeed-to-reviewed-unit semantic coverage. Do not access lexical queries, result resources, ranks, scores, acquisition costs, treatment arms, or Stage D outcomes.
