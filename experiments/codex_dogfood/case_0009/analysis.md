# Case 0009 Stage D: joined R1 effectiveness

**R1 = prospectively evaluated against clean independent Stage C gold.**
**R2 TRUE BM25F / FIELD-AWARE SPARSE RETRIEVAL REMAINS MANDATORY REGARDLESS OF R1 OUTCOME.**

Canonical production BM25 is unchanged. One prospective task cannot establish universal dominance or solve code-aware representation. The primary questions below precede the architectural recommendation.

## Integrity and procedural provenance

Ordered ancestry and exact committed bytes were verified for Stage A `eb4060ff`, Stage B `44638db3`, packet repair `c2d6f322`, and clean Stage C `092f9a76`. The join has 531 treatment and gold resources, 9 obligations and exactly 10 frozen query lanes; duplicate/missing/unexpected identities = 0. Repository, snapshot, corpus, task, resource/content and query identities agree. Native frozen input content equals the packet. All eight clean gold hashes and repaired packet digests match committed Git bytes. Captured query terms, complete positive universes, all field TF/DF/length/average statistics, field sums and score arithmetic were mechanically verified without executing new ranked treatments or collecting costs.

The initial Stage C stopped before decompression over ambiguous digest scopes. Repair changed digest scopes, not packet semantics. A later broad pytest run crossed the blind boundary and invalidated its provisional gold. That quarantined attempt is never used here. Fresh Stage C ran in a sterile external workspace; clean outputs were imported byte-for-byte and committed. The supplied procedural history records material differences from invalid provisional gold; no comparison or access to that invalid gold was made during this analysis. Only Stage D now intentionally lifts the blind. The ten original Stage C NO attestations remain frozen historical assertions, not a claim that Stage D is blind.

Frame: `{"case_identity": "case-0009", "corpus_id": "ed3a4bbb514968e62cae6e906cf738edd491f4202827fc574b0e4c384abed57f", "repository_id": "5cf96d9e-d6a5-44a6-83d3-1e24f6e00009", "snapshot_id": "901d98cacf86c9750162cf8f483c973d6100aa73316f4e33bf70451dbe5101a8", "task_identity": "case-0009-explicit-assessment-bridge"}`.

Gold: 4,779 cells (37 REQUIRED, 78 HELPFUL_ONLY, 4,664 UNNECESSARY, 0 UNRESOLVED); 9 applicable obligations; 40 distinct required units, 42 obligation-relative unit judgments, 23 unique required resources and 10 alternatives. Minimum/maximum sufficient resource union = 22/23. All 40 units are INFERABLE_AT_START; inherent discovery = 0. Task gap and repository-information gap = NONE.

Arm A is exact canonical whole-resource content BM25 + 0.25 filename-stem BM25. Arm B changes only lexical analysis of content, filename stems and queries to whole identifiers plus unique subtokens. Both use k1=1.2, b=0.75, identical corpus/query text, independent field arithmetic and native corpus tie order. No structural retrieval, fusion, reranking, stemming, synonyms, semantic expansion, reformulation or BM25F. Primary intended class = REPRESENTATION_FAILURE; secondary = RANKING_DISCRIMINATION_FAILURE.

## Primary questions before recommendation

| Question | Joined answer |
|---|---|
| 1. Any A-positive REQUIRED resource lost by B? | NO, either globally or in own lanes. |
| 2. Any REQUIRED zero-A-positive resource rescued? | NO; both reach all 23 resources and 37 own cells. |
| 3. Better global completion? | YES: 342 to 331 (-11). |
| 4. Better own-obligation completion? | Three improve, five worsen, one ties; maximum worsens 185 to 231. |
| 5. Lower prefix burden? | YES but small: union 257 to 252 (1.9455%); occurrences 454 to 423. |
| 6. Better REQUIRED ranks without harming others? | NO: 13 improve, 9 tie, 15 worsen. |
| 7. Identifier-attributable gains? | Source component exposure in explicit_package_bases and test names; query-side LocalizationAssessment; shared-term TF expansion. No positive-reach rescue. |
| 8. Expansion regressions? | Captured TF/DF/length changes and new overtakers explain score/rank partitions; isolated rank-causal field allocation is unknown. |
| 9. Net gain/loss? | Required reach gains 0, losses 0, net 0; mixed ranking changes and one top-20 entry versus two exits. |
| 10. Frozen rule satisfied? | Promotion NO (two gates fail); separate-view condition YES (one required top-20 entry and three improved completions). |

## Primary paired metrics

| Metric | Arm A | Arm B | B minus A |
|---|---:|---:|---:|
| REQUIRED unique resources reached / 23 | 23 | 23 | +0 |
| REQUIRED own cells reached / 37 | 37 | 37 | +0 |
| REQUIRED unit judgments reached / 42 | 42 | 42 | +0 |
| Distinct REQUIRED units reached / 40 | 40 | 40 | +0 |
| Global sufficient completion depth | 342 | 331 | -11 |
| Maximum own-obligation completion | 185 | 231 | +46 |
| Completion-prefix unique union | 257 | 252 | -5 |
| Completion-prefix occurrences | 454 | 423 | -31 |
| Own top-5 REQUIRED (nine lanes) | 15 | 15 | +0 |
| Own top-10 REQUIRED (nine lanes) | 24 | 23 | -1 |
| Own top-20 REQUIRED (nine lanes) | 28 | 27 | -1 |

Both arms positively retrieve the same 23 REQUIRED resources, all 37 REQUIRED own cells, all 42 obligation-relative unit judgments and all 40 distinct units. Both global and any-lane required-resource partitions are identical. A-only = B-only = neither = 0 in all required reach partitions. B required gains = 0, required losses = 0, net positive-reach change = 0. There are no verified positive-reach representation recoveries. The complete lists are in analysis.json; positive reach is not completion prefix size.

Required resources reached by both:

- `AGENTS.md`
- `docs/architecture.md`
- `docs/architecture/decisions/ADR-0005-obligation-driven-repository-localization.md`
- `docs/architecture/localization.md`
- `docs/development/validation.md`
- `docs/documentation_map.md`
- `pyproject.toml`
- `scripts/validate_development.py`
- `src/devtools/context/localization/__init__.py`
- `src/devtools/context/localization/assessment.py`
- `src/devtools/context/localization/association/hypothesis.py`
- `src/devtools/context/localization/docs/overview.md`
- `src/devtools/context/localization/obligation.py`
- `src/devtools/context/localization/readiness.py`
- `src/devtools/context/localization/resolution/__init__.py`
- `src/devtools/context/localization/resolution/contract.py`
- `src/devtools/context/localization/resolution/promotion.py`
- `src/devtools/context/localization/resolution/view.py`
- `src/devtools/context/localization/task.py`
- `src/devtools/context/repository/resource.py`
- `src/devtools/context/repository/snapshot.py`
- `tests/context/localization/resolution/test_resolution.py`
- `tests/context/localization/test_kernel.py`

## Complete positive universes and own completion

| Lane/obligation | A positives | B positives | A completion | B completion | Delta | Winner |
|---|---:|---:|---:|---:|---:|---|
| global | 529 | 529 | 342 | 331 | -11 | B |
| alternatives | 118 | 134 | 10 | 12 | 2 | A |
| applicability | 146 | 178 | 2 | 3 | 1 | A |
| bridge | 181 | 242 | 16 | 23 | 7 | A |
| documentation | 156 | 193 | 10 | 9 | -1 | B |
| frame | 314 | 347 | 185 | 231 | 46 | A |
| package | 245 | 259 | 178 | 99 | -79 | B |
| readiness | 180 | 256 | 34 | 35 | 1 | A |
| tests | 314 | 350 | 12 | 4 | -8 | B |
| validation | 151 | 192 | 7 | 7 | 0 | Tie |

Own positive-resource unions: A 472, B 478; own positive cells: A 1805, B 2151. Across global and own lanes, unique positive resources: A 529, B 529. The two global positive sets are equal. A/B global completeness is evaluated over each valid combination, not all 23 possible resources by assumption.

| Arm | Combination | Unique required resources | Global completion |
|---|---|---:|---:|
| A | alternatives:1, applicability:1, bridge:1, documentation:1, frame:1, package:1, readiness:1, tests:1, validation:1 | 23 | 342 |
| A | alternatives:2, applicability:1, bridge:1, documentation:1, frame:1, package:1, readiness:1, tests:1, validation:1 | 22 | 342 |
| B | alternatives:1, applicability:1, bridge:1, documentation:1, frame:1, package:1, readiness:1, tests:1, validation:1 | 23 | 331 |
| B | alternatives:2, applicability:1, bridge:1, documentation:1, frame:1, package:1, readiness:1, tests:1, validation:1 | 22 | 331 |

Both global combinations have the same depth within each arm, with pyproject.toml the global bottleneck at A342/B331. For the alternatives obligation, both arms choose the documentation alternative; incompatible alternatives are never mixed. B improves documentation, package and tests completion, ties validation, and worsens alternatives, applicability, bridge, frame and readiness. Maximum own depth worsens 185 to 231 (+46).

## Completion-prefix burden and top-K

| Prefix metric | Arm A | Arm B |
|---|---:|---:|
| occurrences | 454 | 423 |
| union_count | 257 | 252 |
| excess | 235 | 230 |
| multiple | 11.681818181818182 | 11.454545454545455 |
| REQUIRED cells in own prefixes | 36 | 36 |
| HELPFUL_ONLY cells in own prefixes | 46 | 45 |
| UNNECESSARY cells in own prefixes | 372 | 342 |
| UNRESOLVED cells in own prefixes | 0 | 0 |

The exact unique-union reduction is (257 - 252) / 257 = 5/257 = **1.9455252918%**, below the frozen 20% threshold. The 22-resource lower bound leaves A 235 excess candidates (11.681818x gold), B 230 excess candidates (11.454545x gold). Prefixes include 36 of the 37 REQUIRED cells: the unchosen alternative's source-only member is not needed by the selected sufficient combination. Own occurrences fall by 31; unnecessary own-prefix cells fall by 30. Severe discrimination weakness remains.

Own top-K sums nine obligation-relative prefixes (45/90/180 candidate cells). Global top-K uses union relevance: REQUIRED precedence, then HELPFUL in any obligation, then UNNECESSARY; it is not an obligation-relative judgment or the historical Increment 27 metric.

| Scope | K | A REQUIRED | B REQUIRED | A useful (R+H) | B useful | A UNNECESSARY | B UNNECESSARY |
|---|---:|---:|---:|---:|---:|---:|---:|
| own_topk | 5 | 15 | 15 | 36 | 35 | 9 | 10 |
| own_topk | 10 | 24 | 23 | 54 | 56 | 36 | 34 |
| own_topk | 20 | 28 | 27 | 77 | 77 | 103 | 103 |
| global_topk | 5 | 3 | 3 | 5 | 5 | 0 | 0 |
| global_topk | 10 | 5 | 6 | 8 | 9 | 2 | 1 |
| global_topk | 20 | 9 | 9 | 12 | 12 | 8 | 8 |

## All paired REQUIRED own-cell ranks

Counts: 13 improved, 9 unchanged, 15 worsened. Median delta = 0; mean delta = -0.567568 (supporting only; does not cancel regressions). Delta = B - A.

| Obligation | Resource | A | B | Delta | Status | Field mechanism |
|---|---|---:|---:|---:|---|---|
| alternatives | `docs/architecture/decisions/ADR-0005-obligation-driven-repository-localization.md` | 10 | 12 | +2 | WORSENED | STATISTICS_ONLY |
| alternatives | `src/devtools/context/localization/docs/overview.md` | 2 | 1 | -1 | IMPROVED | CONTENT_IDENTIFIER_GAIN |
| alternatives | `src/devtools/context/localization/obligation.py` | 6 | 9 | +3 | WORSENED | CONTENT_IDENTIFIER_GAIN |
| alternatives | `src/devtools/context/localization/readiness.py` | 24 | 24 | +0 | UNCHANGED | CONTENT_IDENTIFIER_GAIN |
| alternatives | `src/devtools/context/localization/resolution/promotion.py` | 4 | 3 | -1 | IMPROVED | CONTENT_IDENTIFIER_GAIN |
| alternatives | `src/devtools/context/localization/resolution/view.py` | 5 | 6 | +1 | WORSENED | CONTENT_IDENTIFIER_GAIN |
| applicability | `src/devtools/context/localization/assessment.py` | 1 | 1 | +0 | UNCHANGED | CONTENT_IDENTIFIER_GAIN |
| applicability | `src/devtools/context/localization/readiness.py` | 2 | 3 | +1 | WORSENED | CONTENT_IDENTIFIER_GAIN |
| bridge | `src/devtools/context/localization/assessment.py` | 16 | 23 | +7 | WORSENED | CONTENT_IDENTIFIER_GAIN |
| bridge | `src/devtools/context/localization/resolution/contract.py` | 5 | 6 | +1 | WORSENED | CONTENT_IDENTIFIER_GAIN |
| bridge | `src/devtools/context/localization/resolution/promotion.py` | 1 | 1 | +0 | UNCHANGED | CONTENT_IDENTIFIER_GAIN |
| bridge | `src/devtools/context/localization/resolution/view.py` | 3 | 3 | +0 | UNCHANGED | CONTENT_IDENTIFIER_GAIN |
| documentation | `docs/architecture.md` | 9 | 7 | -2 | IMPROVED | CONTENT_IDENTIFIER_GAIN |
| documentation | `docs/architecture/localization.md` | 2 | 1 | -1 | IMPROVED | CONTENT_IDENTIFIER_GAIN |
| documentation | `docs/documentation_map.md` | 5 | 5 | +0 | UNCHANGED | MIXED |
| documentation | `src/devtools/context/localization/docs/overview.md` | 10 | 9 | -1 | IMPROVED | CONTENT_IDENTIFIER_GAIN |
| frame | `src/devtools/context/localization/assessment.py` | 10 | 16 | +6 | WORSENED | CONTENT_IDENTIFIER_GAIN |
| frame | `src/devtools/context/localization/association/hypothesis.py` | 12 | 14 | +2 | WORSENED | CONTENT_IDENTIFIER_GAIN |
| frame | `src/devtools/context/localization/readiness.py` | 6 | 5 | -1 | IMPROVED | CONTENT_IDENTIFIER_GAIN |
| frame | `src/devtools/context/localization/resolution/contract.py` | 9 | 8 | -1 | IMPROVED | CONTENT_IDENTIFIER_GAIN |
| frame | `src/devtools/context/localization/task.py` | 20 | 22 | +2 | WORSENED | CONTENT_IDENTIFIER_GAIN |
| frame | `src/devtools/context/repository/resource.py` | 185 | 231 | +46 | WORSENED | CONTENT_IDENTIFIER_GAIN |
| frame | `src/devtools/context/repository/snapshot.py` | 80 | 92 | +12 | WORSENED | CONTENT_IDENTIFIER_GAIN |
| package | `AGENTS.md` | 28 | 27 | -1 | IMPROVED | STATISTICS_ONLY |
| package | `docs/architecture/decisions/ADR-0005-obligation-driven-repository-localization.md` | 3 | 3 | +0 | UNCHANGED | CONTENT_IDENTIFIER_GAIN |
| package | `pyproject.toml` | 178 | 99 | -79 | IMPROVED | CONTENT_IDENTIFIER_GAIN |
| package | `src/devtools/context/localization/__init__.py` | 37 | 42 | +5 | WORSENED | CONTENT_IDENTIFIER_GAIN |
| package | `src/devtools/context/localization/resolution/__init__.py` | 44 | 55 | +11 | WORSENED | CONTENT_IDENTIFIER_GAIN |
| readiness | `src/devtools/context/localization/assessment.py` | 7 | 5 | -2 | IMPROVED | MIXED |
| readiness | `src/devtools/context/localization/readiness.py` | 1 | 1 | +0 | UNCHANGED | CONTENT_IDENTIFIER_GAIN |
| readiness | `src/devtools/context/localization/resolution/promotion.py` | 33 | 11 | -22 | IMPROVED | CONTENT_IDENTIFIER_GAIN |
| readiness | `src/devtools/context/localization/resolution/view.py` | 34 | 35 | +1 | WORSENED | CONTENT_IDENTIFIER_GAIN |
| tests | `tests/context/localization/resolution/test_resolution.py` | 3 | 1 | -2 | IMPROVED | MIXED |
| tests | `tests/context/localization/test_kernel.py` | 12 | 4 | -8 | IMPROVED | CONTENT_IDENTIFIER_GAIN |
| validation | `docs/development/validation.md` | 1 | 1 | +0 | UNCHANGED | CONTENT_IDENTIFIER_GAIN |
| validation | `pyproject.toml` | 5 | 6 | +1 | WORSENED | CONTENT_IDENTIFIER_GAIN |
| validation | `scripts/validate_development.py` | 7 | 7 | +0 | UNCHANGED | FILENAME_IDENTIFIER_GAIN |

## Representation, field and query attribution

No B-only REQUIRED resource/cell exists, so **VERIFIED_IDENTIFIER_REPRESENTATION_RECOVERY = 0**. Paired rank wins are IDENTIFIER_AWARE_RANKING_GAIN, not rescues. Whole-form plus components changes TF, DF and document length even when both arms already match. Field classes below identify local added-match/TF mechanisms; they do not independently prove that field alone caused a rank movement. The only query with added identifier terms is the global task and readiness lane: `LocalizationAssessment` retains `localizationassessment` and adds `localization`, `assessment`. Other own queries are ordinary separated words and have no query-side additions.

For every REQUIRED cell and global REQUIRED resource, analysis.json records exact A/B terms and ranks, required units, field contribution evidence, source identifier/text samples with line/character offsets, occurrence counts, query identifier spans, and sequential TF/DF/length score decomposition. These records distinguish document-only matches, query-only matches and both-side compound exposure. Each field's total delta equals added matches plus shared-term statistic deltas. Source samples are capped at three occurrences per term; full occurrence counts are verified.

Meaningful own-cell gains and their exact lexical evidence:

- **alternatives** `src/devtools/context/localization/docs/overview.md` 2->1: CONTENT_IDENTIFIER_GAIN; content: `PREFERRED_ROLE_SUPPORTED` -> `supported` (TF 12->18, line 127); content: `CandidateWitnessHypothesis` -> `witness` (TF 21->43, line 253).
- **alternatives** `src/devtools/context/localization/resolution/promotion.py` 4->3: CONTENT_IDENTIFIER_GAIN; content: `SupportedWitness` -> `supported` (TF 1->7, line 12); content: `SupportedWitness` -> `witness` (TF 4->17, line 12).
- **documentation** `docs/architecture.md` 9->7: CONTENT_IDENTIFIER_GAIN; content: `documentation_map` -> `documentation` (TF 7->9, line 1302); content: `WitnessSet` -> `witness` (TF 10->12, line 929).
- **documentation** `docs/architecture/localization.md` 2->1: CONTENT_IDENTIFIER_GAIN; content: `LocalizationAssessment` -> `assessment` (TF 4->6, line 59); content: `LocalizationAssessment` -> `localization` (TF 21->26, line 59); content: `LocalizationObligation` -> `obligation` (TF 19->20, line 85); content: `semantic_resolution` -> `resolution` (TF 23->29, line 22); content: `WitnessSet` -> `witness` (TF 15->22, line 57).
- **documentation** `src/devtools/context/localization/docs/overview.md` 10->9: CONTENT_IDENTIFIER_GAIN; content: `LocalizationAssessment` -> `assessment` (TF 7->10, line 273); content: `LocalizationLexicalAcquisitionRequest` -> `localization` (TF 14->23, line 76); content: `ObligationRolePreference` -> `obligation` (TF 45->49, line 110); content: `CandidateMemberResolution` -> `resolution` (TF 20->23, line 327); content: `CandidateWitnessHypothesis` -> `witness` (TF 21->43, line 253).
- **frame** `src/devtools/context/localization/readiness.py` 6->5: CONTENT_IDENTIFIER_GAIN; content: `LocalizationEvidenceReference` -> `evidence` (TF 5->15, line 22); content: `INVALID_FRAME` -> `frame` (TF 6->25, line 39); content: `IdentityCoverage` -> `identity` (TF 15->40, line 15); content: `LocalizationObligationIdentity` -> `obligation` (TF 43->75, line 25); content: `RepositoryId` -> `repository` (TF 4->35, line 29).
- **frame** `src/devtools/context/localization/resolution/contract.py` 9->8: CONTENT_IDENTIFIER_GAIN; content: `LocalizationEvidenceReference` -> `evidence` (TF 6->8, line 12); content: `LocalizationObligationIdentity` -> `identity` (TF 8->12, line 19); content: `LocalizationObligationIdentity` -> `obligation` (TF 9->11, line 19); content: `TaskProvenance` -> `provenance` (TF 1->3, line 21); content: `RepositoryId` -> `repository` (TF 4->12, line 24).
- **package** `AGENTS.md` 28->27: STATISTICS_ONLY; no local matching-term/TF expansion; captured DF and length statistics change.
- **package** `pyproject.toml` 178->99: CONTENT_IDENTIFIER_GAIN; content: `explicit_package_bases` -> `package` (DOCUMENT_SIDE, line 77).
- **readiness** `src/devtools/context/localization/assessment.py` 7->5: MIXED; content: `LocalizationAssessment` -> `assessment` (QUERY_AND_MIXED_DOCUMENT_OCCURRENCES, line 81); content: `LocalizationObligationIdentity` -> `localization` (QUERY_AND_MIXED_DOCUMENT_OCCURRENCES, line 13); content: `supported_witnesses` -> `witnesses` (DOCUMENT_SIDE, line 90); content: `SupportedWitness` -> `supported` (TF 2->7, line 51); filename: `assessment` -> `assessment` (QUERY_SIDE, line 1).
- **readiness** `src/devtools/context/localization/resolution/promotion.py` 33->11: CONTENT_IDENTIFIER_GAIN; content: `assessment` -> `assessment` (QUERY_SIDE, line 10); content: `LocalizationEvidenceReference` -> `localization` (QUERY_AND_MIXED_DOCUMENT_OCCURRENCES, line 11); content: `supported_witnesses` -> `witnesses` (DOCUMENT_SIDE, line 51); content: `SupportedWitness` -> `supported` (TF 1->7, line 12).
- **tests** `tests/context/localization/resolution/test_resolution.py` 3->1: MIXED; content: `LocalizationAssessment` -> `assessment` (TF 1->8, line 14); content: `_frame` -> `frame` (TF 42->52, line 54); content: `test_lexical_only_promotion_and_existing_readiness_flow` -> `promotion` (TF 5->6, line 325); content: `assess_localization_readiness` -> `readiness` (TF 1->6, line 21); content: `CandidateHypothesisResolution` -> `resolution` (TF 8->36, line 38).
- **tests** `tests/context/localization/test_kernel.py` 12->4: CONTENT_IDENTIFIER_GAIN; content: `INVALID_FRAME` -> `frame` (DOCUMENT_SIDE, line 329); content: `test_unconditional_resolution_does_not_claim_applicability_evidence` -> `resolution` (DOCUMENT_SIDE, line 363); content: `LocalizationAssessment` -> `assessment` (TF 21->39, line 19); content: `HandoffReadiness` -> `readiness` (TF 24->55, line 16); content: `stale_evidence` -> `stale` (TF 2->5, line 541).

The readiness promotion resource improves 33->11, entering top-20; its required unit is `promotion-no-mutation`. Query-side `LocalizationAssessment` expansion is material: B matches `localization`/`assessment` that A's whole query term did not supply to this resource. It is an identifier-aware ranking gain, not a zero-score rescue. It does not complete readiness earlier because `resolution/view.py` moves 34->35. Required top-20 exits are bridge assessment.py (16->23) and frame task.py (20->22), so own top-20 REQUIRED net change is -1 despite the one entry.

## Regression attribution

Known: the frozen statistics show additional identifier matches, changed term frequencies and document frequencies, and changed relative document lengths. Added query terms have nonnegative additive scores; there is no query-score dilution normalization in this BM25 implementation. Rank moves are exactly partitioned into new overtakers minus removed overtakers. The following score decomposition is sequential TF -> DF/IDF -> length/average; interaction attribution is path-dependent, not a new ranked ablation.

| Regressed cell | Rank delta | Score delta | Added matches | TF effect | DF effect | Length effect | New/removed overtakers | Newly ahead labels |
|---|---:|---:|---:|---:|---:|---:|---|---|
| alternatives: `docs/architecture/decisions/ADR-0005-obligation-driven-repository-localization.md` | +2 | 0.941370 | 0.000000 | 0.000000 | -0.886662 | 1.828032 | 3/1 | {'HELPFUL_ONLY': 1, 'UNNECESSARY': 2} |
| alternatives: `src/devtools/context/localization/obligation.py` | +3 | -0.466048 | 0.000000 | 0.670565 | -1.324723 | 0.188111 | 3/0 | {'HELPFUL_ONLY': 2, 'UNNECESSARY': 1} |
| alternatives: `src/devtools/context/localization/resolution/view.py` | +1 | 2.500785 | 0.000000 | 3.704842 | -1.359940 | 0.155883 | 1/0 | {'HELPFUL_ONLY': 1} |
| applicability: `src/devtools/context/localization/readiness.py` | +1 | 2.932949 | 1.675544 | 2.918347 | -1.386766 | -0.274176 | 1/0 | {'HELPFUL_ONLY': 1} |
| bridge: `src/devtools/context/localization/assessment.py` | +7 | 0.414244 | 0.000000 | 1.628456 | -1.511410 | 0.297198 | 7/0 | {'HELPFUL_ONLY': 1, 'UNNECESSARY': 6} |
| bridge: `src/devtools/context/localization/resolution/contract.py` | +1 | 2.448691 | 0.000000 | 4.307392 | -2.162112 | 0.303410 | 2/1 | {'HELPFUL_ONLY': 2} |
| frame: `src/devtools/context/localization/assessment.py` | +6 | -0.890246 | 0.000000 | 1.101836 | -2.198962 | 0.206880 | 6/0 | {'HELPFUL_ONLY': 1, 'REQUIRED': 1, 'UNNECESSARY': 4} |
| frame: `src/devtools/context/localization/association/hypothesis.py` | +2 | 0.883610 | 0.000000 | 2.530347 | -1.606449 | -0.040289 | 3/1 | {'UNNECESSARY': 3} |
| frame: `src/devtools/context/localization/task.py` | +2 | 0.442885 | 0.000000 | 1.132033 | -0.957997 | 0.268849 | 4/2 | {'UNNECESSARY': 4} |
| frame: `src/devtools/context/repository/resource.py` | +46 | -0.122931 | 0.000000 | 0.178656 | -0.315239 | 0.013652 | 51/5 | {'UNNECESSARY': 51} |
| frame: `src/devtools/context/repository/snapshot.py` | +12 | -0.123561 | 0.000000 | 0.261461 | -0.586316 | 0.201294 | 16/4 | {'HELPFUL_ONLY': 1, 'UNNECESSARY': 15} |
| package: `src/devtools/context/localization/__init__.py` | +5 | 0.401526 | 0.000000 | 1.413295 | -0.844631 | -0.167138 | 6/1 | {'UNNECESSARY': 6} |
| package: `src/devtools/context/localization/resolution/__init__.py` | +11 | -0.046493 | 0.000000 | 0.249276 | -0.250837 | -0.044932 | 12/1 | {'HELPFUL_ONLY': 1, 'UNNECESSARY': 11} |
| readiness: `src/devtools/context/localization/resolution/view.py` | +1 | 4.207508 | 3.935640 | 0.647576 | -0.443701 | 0.067993 | 8/7 | {'UNNECESSARY': 8} |
| validation: `pyproject.toml` | +1 | 0.277680 | 0.000000 | 0.497482 | -0.432146 | 0.212344 | 1/0 | {'HELPFUL_ONLY': 1} |

Known local arithmetic effects and overtaker identities are recorded exactly. New own positive cells total 346: 345 UNNECESSARY, 1 HELPFUL_ONLY and 0 REQUIRED; per-lane counts are in positive_universe_partitions. Likely: common component exposure increases competition from weakly relevant/unnecessary resources, consistent with expanded positive cells and the overtaker label counts. Unknown: unique causal allocation of final rank changes among interacting TF, DF, length, content and filename changes without separately frozen ablation arms. No such arms were executed. Native tie ordering is preserved; no analyzer-contract defect was demonstrated. Whole-form preservation guarantees lexical reach, not ranking preservation.

## Whole forms, complementarity and remaining failures

All canonical positive REQUIRED field terms are retained in B (lost terms = 0). 9 required lane/resource/field observations retain the compound whole query term `localizationassessment`. No REQUIRED observed row depends exclusively on that compound whole form as its only canonical matching term. Both arms have other canonical evidence for those rows; there is no isolated whole-form-only REQUIRED reach case. Captured whole-term statistics/ranks still change with corpus length normalization and competition.

A union B reaches the same 23 REQUIRED resources, 37 own cells and 40 units as either arm alone: no added REQUIRED positive reach. Complementarity here is ranking: readiness's required top-20 entry and three improved obligation completions coexist with five worsened completions and 15 worsened required-cell ranks. The frozen separate-view rule explicitly permits that top-20 entry plus improved completion; no fusion is implemented.

Remaining positive-reach misses = 0, so no residual zero-score miss can be assigned to REPRESENTATION_FAILURE or VOCABULARY_SEMANTIC_MISMATCH. Required evidence outside shallow prefixes/top-20 and the 252-resource union demonstrate RANKING_DISCRIMINATION_FAILURE. Query/field representation effects are observed, but not all semantic insufficiency is representation failure. RELATIONAL_RELEVANCE may motivate future hypotheses but is not established as the cause of a positive miss here. CONTEXT_DISCLOSURE_FAILURE is unmeasured (no downstream Context output). INFORMATION_NEED_OBLIGATION_FAILURE is not established: task gap NONE and nine applicable obligations cover the task. No semantic-resolution effectiveness or execution claim follows.

## Costs and exact frozen decision

| Captured cost | Arm A | Arm B | B/A | Frozen <=3x |
|---|---:|---:|---:|---|
| index_build_seconds | 1.5785610000020824 | 3.3875384000129998 | 2.145966105 | not a separate frozen gate |
| median_query_seconds | 0.026403399999253452 | 0.021373400028096512 | 0.809494233 | PASS |
| index_plus_query_seconds | 1.9206255999743007 | 3.6348013999522664 | 1.892509087 | PASS |
| content_vocabulary_size | 10054 | 10338 | 1.028247464 | not a separate frozen gate |
| content_posting_count | 86320 | 97054 | 1.124351251 | not a separate frozen gate |
| serialized_index_bytes | 22291111 | 4244482 | 0.190411416 | PASS |
| traced_peak_bytes | 259903337 | 19333169 | 0.074385998 | PASS |

All four frozen gates (median query, index+queries, serialized index, traced peak) pass <=3x. Single traced execution, not a latency benchmark. Native A serializes richer provenance/span objects than B and allocation includes projection; lower B index bytes/peak are not evidence that lexical expansion saves memory. Filename indexes rebuild per query in both arms. No RSS conclusion.

| Promotion condition | Result |
|---|---|
| valid_complete_gold_and_join | PASS |
| no_A_positive_required_cells_lost | PASS |
| no_worse_every_own_and_global_completion | FAIL |
| twenty_percent_burden_or_verified_required_rescue | FAIL |
| all_frozen_cost_limits | PASS |

Promotion fails both no-worse-completion and 20%-burden-or-rescue gates. Separate-view criteria pass: one verified identifier-attributable required top-20 entry, three improved own completions, and failed promotion. Primary outcome: **RETAIN AS SEPARATE RETRIEVAL VIEW**. No production consideration checkpoint is earned by this exact prospective case, no concrete representation defect is demonstrated, and the PARK condition is not selected. Canonical production retrieval remains unchanged.

## Historical context after the primary metric freeze

Primary Case 0009 metrics were computed and written before contextual historical comparison. Retained Increment 27 aggregates: canonical useful@5=63; identifier=68; lexical RRF=74. Increment 27 also preserved whole forms plus subtokens but used different scoring infrastructure. Case 0009 remains **mixed** relative to that evidence: it prospectively reinforces specific unused identifier signal and paired ranking gains, while weakening any replacement inference through regressions, unchanged REQUIRED positive reach and only 1.9455% burden reduction. Case 0009 own useful@5 falls 36->35; it is a different nine-obligation aggregation and cannot be pooled numerically with Increment 27. Historical RRF is a comparator, not a default or a new Case 0009 fusion result.

## R2 design inputs and limits

R1 asks which lexical terms should be exposed; R2 asks how evidence from distinct code/document fields should contribute. R2 must prospectively retain separate canonical and identifier-aware representations so fielding and representation effects can be attributed independently. Include whole+subtoken terms in an R2 comparison arm, preserve whole identifiers, and explicitly distinguish filename/name evidence from body/content. Filename expansion demonstrably supplies `resolution` from `test_resolution`; content expansion and query-side `LocalizationAssessment` provide different ranking effects. Expanded common components also grow positive candidate competition. These observations inform hypotheses and field schemas, not Case 0009 post-hoc BM25F weight tuning. No R2 weights, BM25F implementation or semantic-resolution experiment is introduced here.

## Validation and access

15 focused Stage D tests passed, checking joins, golden metric totals, gain/loss partitions, alternative ALL/ANY completion, source/term attribution, score decomposition, costs and frozen decision precedence. CLI verify rebuilds analysis.json and analysis.md exactly from frozen inputs. Scoped Ruff and formatter checks apply only to new Stage D Python; frozen Stage C remains byte-identical. Diff checks pass. Confirmation/reserve and quarantined invalid gold were not accessed. Stage B treatments were not reexecuted.

Next step:

> R2 — design, implement, freeze and prospectively evaluate true BM25F / field-aware sparse retrieval. R2 occurs regardless of R1 outcome.

STOP. Do not implement R2 in this task.
