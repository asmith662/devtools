# Case 0011 Stage D

## Join integrity — PASSED

Case/task/RepositoryId/SnapshotId/CorpusId, 531 resource/content identities, nine obligations, 4,779 cells, 32 exact reviewed unit identities/statements, 18 exact needs and 576 pair mappings join without duplicate, missing or unexpected entries. All 28 captured literal queries ran once and retain exact route, terms, ranks, scores, contributions and tie order. No retrieval was rerun.

Frozen chain ancestry and exact selected committed blobs pass. Stage A's C5_PROTOCOL.md placeholder was intentionally superseded at 918e90bc; both protocol versions are pinned at their proper commits. The primary C.5 PUBLICATION.md also gained a historical-status preface at 53e1681; both committed versions are authenticated separately from immutable adjudication data. The original Stage A current-worktree verifier cannot replay the superseded placeholder; Stage D retains scientific checks and authenticates the documented history. No frozen treatment, gold, mapping or A/B trace changed.

```json
{
  "status": "PASSED",
  "case_identity": "case-0011",
  "corpus_id": "1e9d78ac0f6c2ca788c161649450bc70f953ea084b97b5f403344655f78721e4",
  "repository_id": "5cf96d9e-d6a5-44a6-83d3-1e24f6e00009",
  "snapshot_id": "981d67d6678d538776f2e400d79156b6e92fed048ee9af57b5a3a0a6e5f4cd17",
  "task_identity": "case-0011-context-utf8-ceiling",
  "resources": 531,
  "obligations": 9,
  "cells": 4779,
  "required_cells": 23,
  "required_units": 32,
  "needs": 18,
  "mappings": 576,
  "queries": 28,
  "query_execution_count_each": 1,
  "alternatives": 12,
  "task_combinations": 6,
  "duplicate_missing_unexpected": 0,
  "exact_statements_and_content_identities": "PASSED"
}
```

## DID WE IMPROVE?

**Frozen outcome: INFORMATION_NEED_AUTHORING_DEFECT.** Two completely unrequested units (U02/U19) trigger the literal omitted-unit precedence. Partial coverage alone does not imply a MISFORMULATED need. This one need set provides local rank gains but worsens aggregate responsible subset burden and fails full semantic completeness.

| Dimension | Observed result |
| --- | --- |
| Semantic completeness | Strict C: 15/32 units and 0/12 alternatives; secondary collective diagnostic: 18/32 and 0/12. Neither completes any obligation. |
| Required reach | A/B/C all reach 16 resources, 23 owning cells, 32 distinct units (34 obligation/unit pairs), 15 indispensable resources. No reach rescue or loss. |
| Covered-unit depth | C improves 5 and regresses 10 against B; no ties/misses. U26 retains both B owning lanes separately. |
| Unique prefix union | A→B: 370→269 (-101, -27.297%). Same 15-unit B→C: 220→371 (+151, +68.636%). |
| Unnecessary prefix occurrences | A→B: 331→513 (+182, +54.985%); labels use global scope for A and owning obligation scope for B. Same-subset B→C: 337→737 (+400, +118.694%). |
| Execution cost | A/B/C: 1/9/18 queries; 0.021986300 / 0.066727000 / 0.159203800 seconds. C costs +0.092476800 seconds (+138.590%) over B. |
| Raw candidate duplication | A/B/C: 0 / 2,039 / 4,269 duplicate occurrences. C adds 2,230 duplicates to B. |
| Content volume | A→B: 3,104,937→2,656,630 bytes (-448,307, -14.438%). Same-subset B→C: 2,315,351→2,689,816 bytes (+374,465, +16.173%). |

All prefix metrics describe **counterfactual completion-prefix inspection burden**. Actual evidence-inspection cost is **NOT MEASURED**. Positive counts, raw recall and prefix volumes are separate measurements.

### Exact magnitude of each burden change

#### A_vs_B_complete

| Metric | Baseline | Changed | Delta | Percent change | Result |
| --- | --- | --- | --- | --- | --- |
| unique_resources | 370 | 269 | -101 | -27.297297% | IMPROVED |
| occurrences | 370 | 589 | 219 | 59.189189% | WORSENED |
| duplicates | 0 | 320 | 320 | undefined zero baseline | WORSENED |
| utf8_bytes | 3104937 | 2656630 | -448307 | -14.438522% | IMPROVED |
| query_count_used | 1 | 9 | 8 | 800.000000% | WORSENED |
| UNNECESSARY | 331 | 513 | 182 | 54.984894% | WORSENED |

#### B_vs_C_strict_same_units

| Metric | Baseline | Changed | Delta | Percent change | Result |
| --- | --- | --- | --- | --- | --- |
| unique_resources | 220 | 371 | 151 | 68.636364% | WORSENED |
| occurrences | 394 | 809 | 415 | 105.329949% | WORSENED |
| duplicates | 174 | 438 | 264 | 151.724138% | WORSENED |
| utf8_bytes | 2315351 | 2689816 | 374465 | 16.173142% | WORSENED |
| query_count_used | 8 | 10 | 2 | 25.000000% | WORSENED |
| UNNECESSARY | 337 | 737 | 400 | 118.694362% | WORSENED |

#### B_vs_C_granularity_same_units

| Metric | Baseline | Changed | Delta | Percent change | Result |
| --- | --- | --- | --- | --- | --- |
| unique_resources | 250 | 391 | 141 | 56.400000% | WORSENED |
| occurrences | 464 | 920 | 456 | 98.275862% | WORSENED |
| duplicates | 214 | 529 | 315 | 147.196262% | WORSENED |
| utf8_bytes | 2552629 | 2897119 | 344490 | 13.495498% | WORSENED |
| query_count_used | 8 | 11 | 3 | 37.500000% | WORSENED |
| UNNECESSARY | 404 | 831 | 427 | 105.693069% | WORSENED |

## Reviewed references

Task gold: 531 resources × nine obligations = 4,779 cells; REQUIRED 23, HELPFUL_ONLY 84, UNNECESSARY 4,672, UNRESOLVED 0. Thirty-two required units; 16-resource union, 12 acceptable alternatives, six complete task combinations, two distinct resource unions; minimum 15, maximum 16 sufficient resources; 15 indispensable resources and 30 indispensable units. Task gap NONE; repository-information gap NONE. The 16-resource REQUIRED union is not simultaneously necessary.

C.5: 576 pairs = 15 DIRECTLY_COVERS + 55 PARTIALLY_COVERS + 506 DOES_NOT_COVER + 0 AMBIGUOUS. Strict units: 15 COVERED, 15 PARTIAL_ONLY, two UNCOVERED. Needs: ten NECESSARY, eight PARTIAL_ONLY, all other classifications zero. Granularity: 26 atomic, six collectively coverable, zero overcompound/ambiguous. Accepted N09/N10 sets cover U07/U28/U30 only. Diagnostic units: 18 covered, 12 partial, two uncovered. All 12 alternatives remain incomplete under both rules.

## Raw acquisition and required reach

| Arm | Queries | Query seconds | Positive occurrences | Unique positive | Duplicates | R resources | R cells | R units | Indispensable |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| A | 1 | 0.021986300 | 529 | 529 | 0 | 16 | 23 | 32 | 15 |
| B | 9 | 0.066727000 | 2523 | 484 | 2039 | 16 | 23 | 32 | 15 |
| C | 18 | 0.159203800 | 4766 | 497 | 4269 | 16 | 23 | 32 | 15 |

Pair overlaps: `{"A_B": {"A_only": 45, "B_only": 0, "intersection": 484}, "A_C": {"A_only": 32, "C_only": 0, "intersection": 497}, "B_C": {"B_only": 4, "C_only": 17, "intersection": 480}}`. All required entities are common to all arms; A-only/B-only/C-only/missed-all sets are empty for required resources/cells/units/indispensable resources. C's unique raw universe grows by 13 and occurrences by 2,243 over B, without any required-reach gain.

Shared content index: 0.433378300s. Content index reused; native per-query filename index build is included in query timing. R1.5 projection is separately timed in the frozen costs artifact. Single-run timings are descriptive, not latency benchmarks.

## Arm A — valid whole-task completion

Best valid task-alternative depth 370; last indispensable-resource rank 370. Prefix has 370 unique resources, 3,104,937 UTF-8 bytes, excess 355 over the 15-resource minimum, ratio 370/15 = 24.667. All six combinations are evaluated independently; no all-16 requirement was imposed.

| Combination | Sufficient resources | Completion depth | Alternative identities |
| --- | --- | --- | --- |
| 1 | 15 | 370 | reconciled-alternative-07341a89b6d3791b7ae85f2faead66701099a85d1872f5361256ee7de8570a13, reconciled-alternative-4c0191d69223c378c0f0141116d45f84c0186c6ebe51fd375d449c6fe0daaa56, reconciled-alternative-e46154e553697037cffb79112d4341c22697efc3a58b671585f4e80e4150fcc8, reconciled-alternative-56e21da89b0c7d9e2fc4fc86a42143d319bfbe03df70d753c2aabd7b5db12fae, reconciled-alternative-f67b434bae46e7400da6b563a5fb1f3ad1545bd1788ce835a9df8d7522bdd387, reconciled-alternative-5a6352354f06be41de763b0b31993052594b3b3d38965bb777e83948855466e3, reconciled-alternative-d12a52b7a7deae632c88b6982e1f082e27d5ecf77d2c1c5c24a231589040b307, reconciled-alternative-7e3bc3fbffd7dcff9b8c6b74d9ca04f007fc376676349f692339604bef56372f, reconciled-alternative-5fef3b648030e5857c8de5839839181c79f43a8145ede821aa2943dcdb76668d |
| 2 | 15 | 370 | reconciled-alternative-07341a89b6d3791b7ae85f2faead66701099a85d1872f5361256ee7de8570a13, reconciled-alternative-4c0191d69223c378c0f0141116d45f84c0186c6ebe51fd375d449c6fe0daaa56, reconciled-alternative-e46154e553697037cffb79112d4341c22697efc3a58b671585f4e80e4150fcc8, reconciled-alternative-56e21da89b0c7d9e2fc4fc86a42143d319bfbe03df70d753c2aabd7b5db12fae, reconciled-alternative-f67b434bae46e7400da6b563a5fb1f3ad1545bd1788ce835a9df8d7522bdd387, reconciled-alternative-dec8541b9472cd9a0e5df83af182dad98c16f727f28414113ab3fb5fd69f8b1f, reconciled-alternative-d12a52b7a7deae632c88b6982e1f082e27d5ecf77d2c1c5c24a231589040b307, reconciled-alternative-7e3bc3fbffd7dcff9b8c6b74d9ca04f007fc376676349f692339604bef56372f, reconciled-alternative-5fef3b648030e5857c8de5839839181c79f43a8145ede821aa2943dcdb76668d |
| 3 | 16 | 370 | reconciled-alternative-07341a89b6d3791b7ae85f2faead66701099a85d1872f5361256ee7de8570a13, reconciled-alternative-88247b6096c52d866d29704bc512a112275ae0e7a5170bd82ac76bb429e20833, reconciled-alternative-e46154e553697037cffb79112d4341c22697efc3a58b671585f4e80e4150fcc8, reconciled-alternative-56e21da89b0c7d9e2fc4fc86a42143d319bfbe03df70d753c2aabd7b5db12fae, reconciled-alternative-f67b434bae46e7400da6b563a5fb1f3ad1545bd1788ce835a9df8d7522bdd387, reconciled-alternative-5a6352354f06be41de763b0b31993052594b3b3d38965bb777e83948855466e3, reconciled-alternative-d12a52b7a7deae632c88b6982e1f082e27d5ecf77d2c1c5c24a231589040b307, reconciled-alternative-7e3bc3fbffd7dcff9b8c6b74d9ca04f007fc376676349f692339604bef56372f, reconciled-alternative-5fef3b648030e5857c8de5839839181c79f43a8145ede821aa2943dcdb76668d |
| 4 | 16 | 370 | reconciled-alternative-07341a89b6d3791b7ae85f2faead66701099a85d1872f5361256ee7de8570a13, reconciled-alternative-88247b6096c52d866d29704bc512a112275ae0e7a5170bd82ac76bb429e20833, reconciled-alternative-e46154e553697037cffb79112d4341c22697efc3a58b671585f4e80e4150fcc8, reconciled-alternative-56e21da89b0c7d9e2fc4fc86a42143d319bfbe03df70d753c2aabd7b5db12fae, reconciled-alternative-f67b434bae46e7400da6b563a5fb1f3ad1545bd1788ce835a9df8d7522bdd387, reconciled-alternative-dec8541b9472cd9a0e5df83af182dad98c16f727f28414113ab3fb5fd69f8b1f, reconciled-alternative-d12a52b7a7deae632c88b6982e1f082e27d5ecf77d2c1c5c24a231589040b307, reconciled-alternative-7e3bc3fbffd7dcff9b8c6b74d9ca04f007fc376676349f692339604bef56372f, reconciled-alternative-5fef3b648030e5857c8de5839839181c79f43a8145ede821aa2943dcdb76668d |
| 5 | 15 | 370 | reconciled-alternative-07341a89b6d3791b7ae85f2faead66701099a85d1872f5361256ee7de8570a13, reconciled-alternative-f8c7ecb272b20d6e47322f00e52eaf5a199fae721c228e994640ec2aaa691bca, reconciled-alternative-e46154e553697037cffb79112d4341c22697efc3a58b671585f4e80e4150fcc8, reconciled-alternative-56e21da89b0c7d9e2fc4fc86a42143d319bfbe03df70d753c2aabd7b5db12fae, reconciled-alternative-f67b434bae46e7400da6b563a5fb1f3ad1545bd1788ce835a9df8d7522bdd387, reconciled-alternative-5a6352354f06be41de763b0b31993052594b3b3d38965bb777e83948855466e3, reconciled-alternative-d12a52b7a7deae632c88b6982e1f082e27d5ecf77d2c1c5c24a231589040b307, reconciled-alternative-7e3bc3fbffd7dcff9b8c6b74d9ca04f007fc376676349f692339604bef56372f, reconciled-alternative-5fef3b648030e5857c8de5839839181c79f43a8145ede821aa2943dcdb76668d |
| 6 | 15 | 370 | reconciled-alternative-07341a89b6d3791b7ae85f2faead66701099a85d1872f5361256ee7de8570a13, reconciled-alternative-f8c7ecb272b20d6e47322f00e52eaf5a199fae721c228e994640ec2aaa691bca, reconciled-alternative-e46154e553697037cffb79112d4341c22697efc3a58b671585f4e80e4150fcc8, reconciled-alternative-56e21da89b0c7d9e2fc4fc86a42143d319bfbe03df70d753c2aabd7b5db12fae, reconciled-alternative-f67b434bae46e7400da6b563a5fb1f3ad1545bd1788ce835a9df8d7522bdd387, reconciled-alternative-dec8541b9472cd9a0e5df83af182dad98c16f727f28414113ab3fb5fd69f8b1f, reconciled-alternative-d12a52b7a7deae632c88b6982e1f082e27d5ecf77d2c1c5c24a231589040b307, reconciled-alternative-7e3bc3fbffd7dcff9b8c6b74d9ca04f007fc376676349f692339604bef56372f, reconciled-alternative-5fef3b648030e5857c8de5839839181c79f43a8145ede821aa2943dcdb76668d |

## Arm B — obligation-query completion

Each alternative uses all complementary resources; choice is minimum depth, then exact alternative identity. Every alternative, identity and member set is retained in analysis.json.

| Obligation | Depth | Occurrences | Unique | Duplicates | R | H | U | UTF-8 bytes |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| bytes | 10 | 10 | 10 | 0 | 1 | 3 | 6 | 67395 |
| ceiling | 92 | 92 | 92 | 0 | 4 | 5 | 83 | 1205104 |
| documentation | 3 | 3 | 3 | 0 | 2 | 1 | 0 | 124509 |
| exports | 21 | 21 | 21 | 0 | 2 | 2 | 17 | 453708 |
| frame | 158 | 158 | 158 | 0 | 5 | 11 | 142 | 1946220 |
| ownership | 36 | 36 | 36 | 0 | 3 | 7 | 26 | 640244 |
| request | 47 | 47 | 47 | 0 | 2 | 10 | 35 | 830977 |
| tests | 122 | 122 | 122 | 0 | 2 | 10 | 110 | 1573521 |
| validation | 100 | 100 | 100 | 0 | 2 | 4 | 94 | 1226977 |

## Prefix burdens — keep comparison targets separate

| Surface | Occurrences | Unique | Duplicates | R | H | U | UTF-8 bytes |
| --- | --- | --- | --- | --- | --- | --- | --- |
| A valid complete task | 370 | 370 | 0 | 16 | 23 | 331 | 3104937 |
| B valid complete task | 589 | 269 | 320 | 23 | 53 | 513 | 2656630 |
| B same 15 covered units | 394 | 220 | 174 | 18 | 39 | 337 | 2315351 |
| C STRICT_COVERED_SUBSET_DIAGNOSTIC | 809 | 371 | 438 | 21 | 51 | 737 | 2689816 |
| B same 18 diagnostic units | 464 | 250 | 214 | 19 | 41 | 404 | 2552629 |
| C GRANULARITY_AWARE_SUBSET_DIAGNOSTIC | 920 | 391 | 529 | 26 | 63 | 831 | 2897119 |

B has excess 254 over minimum, ratio 269/15 = 17.933. B's summed prefixes are 589 occurrences although its deduplicated union is 269. A→B saves unique resources and bytes but adds occurrences/noise and eight query executions; scope-specific label counts cannot be read as a single scalar winner.

## Arm C — frozen official result

**Semantic completion = INCOMPLETE_INFORMATION_NEED_COVERAGE** for every one of the 12 alternatives and every obligation. Official full completion depth and burden remain null. Covered-subset metrics cannot substitute for full completion.

Strict subset uses ten responsible queries: 809 rows, 371 unique resources, 438 duplicates; 24.733 resources per covered unit. Granularity-aware subset uses 11 responsible queries, including both N09/N10 for each accepted collective unit: 920 rows, 391 unique, 529 duplicates; 21.722 resources per covered unit. The latter is still 12 partial + two uncovered units short.

## B versus C — directly covered units only

| Unit | Owning obligation(s) | B depth | C responsible depth | C−B | Outcome | C route |
| --- | --- | --- | --- | --- | --- | --- |
| U01 | exports | 21 | 22 | 1 | REGRESSION | C.exports.public-boundary |
| U05 | tests | 96 | 273 | 177 | REGRESSION | C.tests.request-preservation |
| U06 | tests | 96 | 162 | 66 | REGRESSION | C.tests.text-boundaries |
| U08 | frame | 88 | 61 | -27 | IMPROVEMENT | C.frame.binding |
| U09 | documentation | 3 | 2 | -1 | IMPROVEMENT | C.documentation.architecture |
| U11 | ceiling | 3 | 19 | 16 | REGRESSION | C.ceiling.validation |
| U13 | request | 47 | 76 | 29 | REGRESSION | C.request.copy |
| U18 | validation | 100 | 104 | 4 | REGRESSION | C.validation.configuration |
| U21 | request | 2 | 17 | 15 | REGRESSION | C.request.copy |
| U22 | frame | 88 | 61 | -27 | IMPROVEMENT | C.frame.binding |
| U23 | tests | 96 | 26 | -70 | IMPROVEMENT | C.tests.frame-rejection |
| U26 | ceiling, tests | 122 | 6 | -116 | IMPROVEMENT | C.tests.request-preservation |
| U27 | bytes | 10 | 64 | 54 | REGRESSION | C.bytes.rendered-boundary |
| U29 | validation | 100 | 104 | 4 | REGRESSION | C.validation.configuration |
| U31 | ceiling | 1 | 10 | 9 | REGRESSION | C.ceiling.validation |

The gains are U08/U22 (88→61, -27 each), U09 (3→2, -1), U23 (96→26, -70), U26 (122→6, -116; its ceiling lane regresses 2→6). Focused frame/rejection, architecture and numeric-validation vocabulary improves those routes. Regressions include U05 96→273 (+177), U06 96→162 (+66), U27 10→64 (+54), U13 47→76 (+29); generic or poorly discriminating terms omit useful owner/type vocabulary or fail to match whole canonical identifiers. Exact per-resource B/C terms, scores and unnecessary overtakers are in the Stage D review/trace.

Granularity-aware same-unit comparison: B→C unique 250→391 (+141), occurrences 464→920 (+456), unnecessary 404→831 (+427), bytes 2,552,629→2,897,119 (+344,490). Adding collective semantic credit still fails both completeness and the secondary quantitative burden gate.

## Partial-only and uncovered units

The following exact statements remain immutable gold. Missing-component summaries are Stage D interpretations grounded in the reviewed mapping rationales; they do not amend those judgments.

| Unit | Obligation | Status | Exact unit statement | Partial frozen needs | Missing component | Any C reaches supports? | Best all-C unit depth (oracle) |
| --- | --- | --- | --- | --- | --- | --- | --- |
| U02 | frame | UNCOVERED | Qualified-reference admission rejects blank purpose, derivation/coverage or analysis-membership mismatch, unsupported target type and unsupported resolution route; its materializer rechecks this admission for directly constructed immutable values. | NONE | No need seeks the complete qualified admission/re-admission contract: purpose, derivation/coverage, analysis membership, target type and route checks. | True | 10 |
| U03 | validation | PARTIAL_ONLY | The protected command is uv run python scripts/validate_development.py; it excludes tests/experiments before collection, retains project pytest configuration and branch coverage with the 100 percent gate, returns pytest's exit code, and does not authorize excluded confirmation validation. | case-0011-context-utf8-ceiling/validation/configuration, case-0011-context-utf8-ceiling/validation/protected-entry | The entry-point question leaves pre-collection exclusion, retained pytest/100% branch gate, exit status and confirmation-authorization boundary unrequested as a complete contract. | True | 1 |
| U04 | documentation | PARTIAL_ONLY | The planning overview describes exact materialization, native provenance, appended copied-request Context and both supported choices, and distinguishes future token budgets/universal costs from current behavior. | case-0011-context-utf8-ceiling/documentation/package | Rendered/copied Context documentation questions do not seek the complete materialization/native-provenance/two-choice contract and current-versus-future budget distinction. | True | 1 |
| U07 | frame | PARTIAL_ONLY | The qualified-reference plan adapter delegates to its validated materializer and renderer and retains both source/target addresses and content identities, the rendered text and native materialized value in the common item. | case-0011-context-utf8-ceiling/frame/binding, case-0011-context-utf8-ceiling/frame/items | Strictly neither frame binding nor item retention alone seeks both validated source/target bindings and renderer/text/native-value handoff; the accepted N09/N10 collective set repairs only the secondary diagnostic. | True | 14 |
| U10 | frame | PARTIAL_ONLY | Common materialization rejects a mismatched repository or snapshot, realizes each selected option in order, verifies its returned identity/representation, and publishes a ContextDisclosure only after all items succeed. | case-0011-context-utf8-ceiling/frame/binding, case-0011-context-utf8-ceiling/frame/items, case-0011-context-utf8-ceiling/tests/frame-rejection | Frame checks/item retention do not seek the complete ordered realization, returned identity/representation validation and all-items-success-before-publication contract. | True | 2 |
| U12 | validation | PARTIAL_ONLY | The protected command runs tests only; the validation guide separately specifies uv Ruff lint/format, mypy and diff whitespace checks, including staged diff checking where applicable. | case-0011-context-utf8-ceiling/validation/configuration, case-0011-context-utf8-ceiling/validation/protected-entry | The validation entry/configuration questions do not seek every separate lint, format, mypy and unstaged/staged diff-check instruction. | True | 1 |
| U14 | frame | PARTIAL_ONLY | Immutable DisclosurePlan carries purpose, repository/snapshot identities and ordered choices, rejecting blank purpose, empty choices, mixed purposes or frames and duplicate choices. | case-0011-context-utf8-ceiling/frame/binding, case-0011-context-utf8-ceiling/frame/items, case-0011-context-utf8-ceiling/tests/frame-rejection | Frame-binding/item-retention questions do not seek all plan-construction rejections: blank purpose, empty/duplicate choices and mixed purposes/frames. | True | 16 |
| U15 | ownership | PARTIAL_ONLY | Common rendering and assembly import ModelRequest and Prompt, use common ContextDisclosure only as a type dependency, and introduce no language-specific adapter or Retrieval dependency. | case-0011-context-utf8-ceiling/ownership/dependencies | Owner/dependency questions do not require the complete exact import/type-only ContextDisclosure contract together with absence of adapter/Retrieval imports. | True | 2 |
| U16 | ceiling | PARTIAL_ONLY | The existing keyword-only common assembly entry point accepts RenderedContextDisclosure, has no limit argument, assembles the entire context.text, and creates the copied request only in its final replace call. | case-0011-context-utf8-ceiling/bytes/rendered-boundary, case-0011-context-utf8-ceiling/ceiling/rejection, case-0011-context-utf8-ceiling/ownership/assembly-owner, case-0011-context-utf8-ceiling/request/copy, case-0011-context-utf8-ceiling/tests/request-preservation | Assembly rejection/ownership questions leave the entire existing keyword-only RenderedContextDisclosure signature, absence of a limit and final replace-only publication point incomplete. | True | 2 |
| U17 | bytes, request | PARTIAL_ONLY | Common assembly embeds unchanged task_text and context.text in separate outer envelopes, reports len(context.text.encode("utf-8")) independently of the task length, and preserves each embedded string and its newline bytes. | case-0011-context-utf8-ceiling/bytes/encoding, case-0011-context-utf8-ceiling/bytes/rendered-boundary, case-0011-context-utf8-ceiling/request/copy, case-0011-context-utf8-ceiling/request/prompt, case-0011-context-utf8-ceiling/tests/text-boundaries | Boundary/task-preservation questions do not require both unchanged outer envelopes, separately reported Context/task byte lengths and all embedded newline bytes as one complete fact. | True | 2 |
| U19 | tests | UNCOVERED | Common planning tests construct a qualified disclosure option through module interpretation and production reference analysis before choosing the retained reference. | NONE | No need seeks qualified test-option construction through module interpretation and production reference analysis before retained-reference choice. | True | 3 |
| U20 | exports | PARTIAL_ONLY | The outer Context public facade explicitly imports the common planning assembler and companion plan/materialization/rendering symbols and lists them in __all__. | case-0011-context-utf8-ceiling/exports/public-boundary | The public planning-package inventory does not require the complete outer Context facade imports and __all__ companion exports. | True | 5 |
| U24 | frame | PARTIAL_ONLY | Qualified target resolution support and any retained declaration analysis must match target resource and repository/snapshot frame, with target declaration membership checked when analysis is retained. | case-0011-context-utf8-ceiling/frame/binding, case-0011-context-utf8-ceiling/tests/frame-rejection | Generic frame binding does not require every target support/declaration-analysis frame and declaration-membership check. | True | 10 |
| U25 | ownership | PARTIAL_ONLY | Common Context Planning owns ordered caller-directed plans and faithful realization before rendering and copied request assembly, independently of Retrieval or automatic selection. | case-0011-context-utf8-ceiling/documentation/architecture, case-0011-context-utf8-ceiling/frame/items, case-0011-context-utf8-ceiling/ownership/assembly-owner, case-0011-context-utf8-ceiling/ownership/dependencies | Assembly ownership does not require the complete ordered planning/faithful-realization/rendering/assembly lifecycle and independence from automatic selection. | True | 2 |
| U28 | frame | PARTIAL_ONLY | Whole-resource realization rejects foreign/stale snapshot frames, missing resources and unequal retained occurrences; its item includes unchanged retained content, resource/content identities and the original occurrence as native provenance. | case-0011-context-utf8-ceiling/frame/binding, case-0011-context-utf8-ceiling/frame/items, case-0011-context-utf8-ceiling/tests/frame-rejection | Neither frame-binding nor item-retention singleton seeks the complete whole-resource validation plus unchanged-content/identity/native-occurrence retention; N09/N10 is collectively sufficient only diagnostically. | True | 18 |
| U30 | frame | PARTIAL_ONLY | Immutable MaterializedDisclosureItem retains option identity, representation, addresses, content identities, exact text and native_provenance; ContextDisclosure requires one item per ordered plan choice with matching identity and representation. | case-0011-context-utf8-ceiling/frame/binding, case-0011-context-utf8-ceiling/frame/items | Neither singleton seeks every immutable item field and ContextDisclosure ordered plan/item agreement; N09/N10 establishes the full fact collectively only in the secondary diagnostic. | True | 2 |
| U32 | tests | PARTIAL_ONLY | The common mixed-plan test uses CRLF and non-ASCII qualified/whole-resource fixtures and checks unchanged retained source, native whole-resource provenance and rendered item order. | case-0011-context-utf8-ceiling/frame/items, case-0011-context-utf8-ceiling/tests/text-boundaries | Focused text/frame/preservation questions do not require the entire mixed-plan CRLF/non-ASCII fixture plus exact-source, native whole-resource provenance and ordered-render assertions. | True | 3 |

Incidental retrieval by unrelated or partial needs does not acquire the complete fact through a semantically responsible route. Every partial mapping rationale and exact need/unit identity is retained in trace.json.

## UNCONSTRAINED_QUERY_ORACLE — secondary only

Best rank of every required resource/unit across all 18 queries is retained. All six valid combinations are projected without mixing incompatible alternatives. The selected per-resource-best-rank projection has maximum best-resource rank 104, seven queries, 183 prefix occurrences, 135 unique resources, 48 duplicates, 144 owning-lane unnecessary occurrences and 1,535,291 UTF-8 bytes. It includes a valid 15-resource sufficient alternative. This is neither a globally optimized prefix union nor an executed/responsible policy, and earns no U1 gate credit. It shows lexical routes exist even for unrequested or incompletely requested facts: semantic omission is the earliest completeness failure, while bad query discrimination separately worsens responsible subset burden.

## Exact hints and query dilution

| Hint | Exact declaration owner | Containing-query owner ranks |
| --- | --- | --- |
| ModelRequest | src/devtools/models/interaction/models.py | A.task: 102, C.ownership.assembly-owner: 56, B.request: 47, C.request.copy: 76 |
| ContextDisclosure | src/devtools/context/planning/materialization.py | A.task: 29, B.frame: 2, C.frame.binding: 2 |
| DisclosurePlan | src/devtools/context/planning/plan.py | A.task: 40, B.frame: 23, C.frame.binding: 16 |

ModelRequest, ContextDisclosure and DisclosurePlan remain lexical-only. Single frozen owner declarations provide deterministic targets for a future U2 experiment; exact lookup was not executed and cannot supply missing task contracts automatically. All containing query texts, declaration/assembly ranks and unnecessary overtakers appear in the trace.

MIXED_INTENT_EVIDENCE_PRESENT is established locally for C.tests.request-preservation: N14 seeks both U05 preservation tests and U26 invalid-numeric tests. The U05 planning test scores 0.732784534 from 'tests' alone at rank 273; the unnecessary Codex CLI document scores 9.522116872, dominated by request/invalid/argument (8.636011463). The same query reaches U26 at rank six. This is contribution-backed competition between distinct concerns, not an inference from DF. QUERY_DILUTION is a contributor; no ablation or rewritten query was run.

U27 also exposes a representation limitation: 'rendered' in RenderedContextDisclosure is analyzed as the whole 'renderedcontextdisclosure'. Its literal query matches the owner only on 'context' (1.692466004), giving rank 64. No identifier-aware treatment was run; its prospective rank effect is unknown. U06 may involve descriptive-vocabulary versus fixture-byte mismatch; that remains POSSIBLE_VOCABULARY_SEMANTIC_MISMATCH. Every query's R1.5 DF/IDF/field fraction, reviewed required/helpful/unnecessary yield and score contributions are in the review/trace.

## Earliest failure attribution

| Unit | Stage | Earliest class | Contributors | What must change |
| --- | --- | --- | --- | --- |
| U01 | None | NO_ACQUISITION_FAILURE |  | No change required for this bounded acquisition. |
| U02 | INFORMATION_NEED_FORMULATION | MISSING_INFORMATION_NEED |  | Author a complete fact-seeking need, then prospectively test its query; collective support does not amend the frozen direct rule. |
| U03 | INFORMATION_NEED_FORMULATION | INCOMPLETE_INFORMATION_NEED |  | Author a complete fact-seeking need, then prospectively test its query; collective support does not amend the frozen direct rule. |
| U04 | INFORMATION_NEED_FORMULATION | INCOMPLETE_INFORMATION_NEED |  | Author a complete fact-seeking need, then prospectively test its query; collective support does not amend the frozen direct rule. |
| U05 | QUERY_FORMULATION | GOOD_NEED_BAD_QUERY | QUERY_DILUTION, RETRIEVAL_RANKING_DISCRIMINATION_FAILURE | Retain distinguishing copied ModelRequest/Context Planning vocabulary in a prospectively frozen literal query. This query matches the actual planning test only on 'tests'; numeric-validation wording instead supplies effective routes to U26 and unrelated argument documentation. No repaired query was tested. |
| U06 | RETRIEVAL_RANKING | RETRIEVAL_RANKING_DISCRIMINATION_FAILURE | POSSIBLE_VOCABULARY_SEMANTIC_MISMATCH | Prospectively improve query discrimination or routing/representation; acquisition is positive but unnecessary candidates overtake it. |
| U07 | INFORMATION_NEED_FORMULATION | INCOMPLETE_INFORMATION_NEED | EXPERIMENTAL_GRANULARITY_LIMITATION | Author a complete fact-seeking need, then prospectively test its query; collective support does not amend the frozen direct rule. |
| U08 | RETRIEVAL_RANKING | RETRIEVAL_RANKING_DISCRIMINATION_FAILURE |  | Prospectively improve query discrimination or routing/representation; acquisition is positive but unnecessary candidates overtake it. |
| U09 | None | NO_ACQUISITION_FAILURE |  | No change required for this bounded acquisition. |
| U10 | INFORMATION_NEED_FORMULATION | INCOMPLETE_INFORMATION_NEED | EXPERIMENTAL_GRANULARITY_LIMITATION | Author a complete fact-seeking need, then prospectively test its query; collective support does not amend the frozen direct rule. |
| U11 | None | NO_ACQUISITION_FAILURE |  | No change required for this bounded acquisition. |
| U12 | INFORMATION_NEED_FORMULATION | INCOMPLETE_INFORMATION_NEED | EXPERIMENTAL_GRANULARITY_LIMITATION | Author a complete fact-seeking need, then prospectively test its query; collective support does not amend the frozen direct rule. |
| U13 | RETRIEVAL_RANKING | RETRIEVAL_RANKING_DISCRIMINATION_FAILURE | EXACT_HINT_NOT_ROUTED | Prospectively improve query discrimination or routing/representation; acquisition is positive but unnecessary candidates overtake it. |
| U14 | INFORMATION_NEED_FORMULATION | INCOMPLETE_INFORMATION_NEED |  | Author a complete fact-seeking need, then prospectively test its query; collective support does not amend the frozen direct rule. |
| U15 | INFORMATION_NEED_FORMULATION | INCOMPLETE_INFORMATION_NEED |  | Author a complete fact-seeking need, then prospectively test its query; collective support does not amend the frozen direct rule. |
| U16 | INFORMATION_NEED_FORMULATION | INCOMPLETE_INFORMATION_NEED |  | Author a complete fact-seeking need, then prospectively test its query; collective support does not amend the frozen direct rule. |
| U17 | INFORMATION_NEED_FORMULATION | INCOMPLETE_INFORMATION_NEED | EXPERIMENTAL_GRANULARITY_LIMITATION | Author a complete fact-seeking need, then prospectively test its query; collective support does not amend the frozen direct rule. |
| U18 | RETRIEVAL_RANKING | RETRIEVAL_RANKING_DISCRIMINATION_FAILURE |  | Prospectively improve query discrimination or routing/representation; acquisition is positive but unnecessary candidates overtake it. |
| U19 | INFORMATION_NEED_FORMULATION | MISSING_INFORMATION_NEED |  | Author a complete fact-seeking need, then prospectively test its query; collective support does not amend the frozen direct rule. |
| U20 | INFORMATION_NEED_FORMULATION | INCOMPLETE_INFORMATION_NEED |  | Author a complete fact-seeking need, then prospectively test its query; collective support does not amend the frozen direct rule. |
| U21 | None | NO_ACQUISITION_FAILURE |  | No change required for this bounded acquisition. |
| U22 | RETRIEVAL_RANKING | RETRIEVAL_RANKING_DISCRIMINATION_FAILURE |  | Prospectively improve query discrimination or routing/representation; acquisition is positive but unnecessary candidates overtake it. |
| U23 | RETRIEVAL_RANKING | RETRIEVAL_RANKING_DISCRIMINATION_FAILURE |  | Prospectively improve query discrimination or routing/representation; acquisition is positive but unnecessary candidates overtake it. |
| U24 | INFORMATION_NEED_FORMULATION | INCOMPLETE_INFORMATION_NEED |  | Author a complete fact-seeking need, then prospectively test its query; collective support does not amend the frozen direct rule. |
| U25 | INFORMATION_NEED_FORMULATION | INCOMPLETE_INFORMATION_NEED |  | Author a complete fact-seeking need, then prospectively test its query; collective support does not amend the frozen direct rule. |
| U26 | None | NO_ACQUISITION_FAILURE |  | No change required for this bounded acquisition. |
| U27 | LEXICAL_REPRESENTATION | REPRESENTATION_FAILURE | RETRIEVAL_RANKING_DISCRIMINATION_FAILURE | Prospectively test whole-identifier plus subtoken evidence or a deterministic owner route. 'rendered' is hidden inside RenderedContextDisclosure in canonical source analysis; the source contributes only 'context' to this query. No alternative representation was executed. |
| U28 | INFORMATION_NEED_FORMULATION | INCOMPLETE_INFORMATION_NEED | EXPERIMENTAL_GRANULARITY_LIMITATION | Author a complete fact-seeking need, then prospectively test its query; collective support does not amend the frozen direct rule. |
| U29 | RETRIEVAL_RANKING | RETRIEVAL_RANKING_DISCRIMINATION_FAILURE |  | Prospectively improve query discrimination or routing/representation; acquisition is positive but unnecessary candidates overtake it. |
| U30 | INFORMATION_NEED_FORMULATION | INCOMPLETE_INFORMATION_NEED | EXPERIMENTAL_GRANULARITY_LIMITATION | Author a complete fact-seeking need, then prospectively test its query; collective support does not amend the frozen direct rule. |
| U31 | None | NO_ACQUISITION_FAILURE |  | No change required for this bounded acquisition. |
| U32 | INFORMATION_NEED_FORMULATION | INCOMPLETE_INFORMATION_NEED |  | Author a complete fact-seeking need, then prospectively test its query; collective support does not amend the frozen direct rule. |

Disjoint earliest-stage totals: `{"GOOD_NEED_BAD_QUERY": 1, "INCOMPLETE_INFORMATION_NEED": 15, "MISSING_INFORMATION_NEED": 2, "NO_ACQUISITION_FAILURE": 6, "REPRESENTATION_FAILURE": 1, "RETRIEVAL_RANKING_DISCRIMINATION_FAILURE": 7}`. Ranking attribution uses R1.5's existing descriptive threshold of 20 unnecessary overtakers; all smaller counts remain visible without a substantial-failure claim. No required resource is absent from all positive sets. Contributors are not added to earliest-stage totals. SEARCH_POLICY_FAILURE = NOT_ASSESSED because U1 executed no sequential frontier/action policy.

## Frozen gates and outcome precedence

| Gate | Result | Evidence |
| --- | --- | --- |
| No loss of B required resource/cell/unit sets | True | Exact set differences empty |
| 100% direct reviewed-unit mapping | False | 15/32; two absent and 15 partial |
| ≥20% union OR noise reduction; other ≤1.05× | False | Official C complete-prefix metrics undefined; cannot pass. Same-subset union 371/220 and noise 737/337 also fail. |
| Every mandatory C union ≤1.25× B depth | False | Every C complete-alternative prefix is null; no obligation can pass a complete-treatment gate. |
| Additional query cost disclosed | True | 18 versus nine; +0.092476800s |

The literal frozen precedence is:

```text
Invalid scientific identity/score/packet/mapping contracts stop as EXPERIMENTAL_CONTRACT_DEFECT. Any unmapped REQUIRED unit or a MISFORMULATED need responsible for a REQUIRED unit yields INFORMATION_NEED_AUTHORING_DEFECT. Otherwise all safety/completeness/burden/obligation gates yield SUPPORTED. Reach-safe positive burden improvement or genuine completion rescue without all gates yields COMPLEMENTARY_BUT_NOT_CLEARLY_BETTER. Otherwise NO_MATERIAL_VALUE.
```

Contract identity/score/packet/mapping checks pass. U02/U19 are completely unrequested, so omitted-unit precedence selects INFORMATION_NEED_AUTHORING_DEFECT before any complementary/no-value interpretation. Granularity does not invalidate the experiment: 26 atomic targets exist and 11 atomic units still lack direct coverage. No collective coverage is promoted into the frozen success rule.

## Case-local limits and exact next step

Tested: one manually authored need set, one devtools task, canonical BM25, no exact routing, mechanism routing, feedback or reformulation. This does not show that all manual or automatic decomposition fails, establish an optimal need count, generalize across repositories, or reject U2/U3/BM25F. Need completeness and query discrimination both require work in this case.

Next step: prepare a separately authorized U2 exact-hint extraction and deterministic-routing experiment with a reviewed complete semantic target. U3 remains future; R1.7 remains retained after upstream evidence; R2 true BM25F remains unconditional and mandatory. No next increment is implemented. No production source, frozen treatment/gold/mapping or confirmation/reserve data changed or was accessed.

## Validation and inspection navigation

Deterministic publication/verification: `uv run python -B -m experiments.codex_dogfood.case_0011.stage_d.analyze build|verify`. R1.5 replay: `uv run python -B -m experiments.codex_dogfood.case_0011.stage_d.analyze verify`. Use `-B` to keep sterile packet directories free of import caches. Focused tests validate bindings, alternative completion, owner responsibility, unions/bytes, partitions, exact arithmetic/precedence, output correspondence, no native retrieval and overwrite refusal. Static/diff checks and exact command outcomes are recorded in validation.md.

[Practical per-query review](STAGE_D_REVIEW.md) prints every input, need, top result, required resource, score evidence, need/unit responsibility and failure. [Machine trace](trace.json) retains complete positive rows and all 576 reviewed mappings; [human trace](TRACE.md) is the separate D layer. Parent ../TRACE.md and ../trace.json remain sealed Stage B artifacts.
