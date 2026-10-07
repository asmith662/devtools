# Case 0010 Stage D — joined canonical BM25 parameter sensitivity

## Join integrity

The blind was intentionally lifted only after independent clean Stage C was committed. Frozen checkpoint ancestry, committed input bytes, Stage A/B seals, gold hashes, full content identities, native query identities and R1.5 score/positive-universe/tie replay all pass.

- repository_id: `5cf96d9e-d6a5-44a6-83d3-1e24f6e00009`
- snapshot_id: `3728b26c92d4a3e20e8860b226d843d8dcf35d454b1e6f0951a92f728f90f032`
- corpus_id: `3eb6d9cb1b253e56ae6f6b7a8c898ec5417371b5f305cca2ee6efe6d571d1e70`
- task_identity: `case-0010-line-range-disclosure`

531/531 resources, 10/10 obligations, 5,310/5,310 cells; zero duplicate, missing or unexpected identities. All four arms have the same eleven exact queries. Gold: 39 REQUIRED, 47 HELPFUL_ONLY, 5,224 UNNECESSARY, 0 UNRESOLVED; 40 distinct units, 45 obligation-relative unit judgments, 22 unique REQUIRED resources. All ten obligations apply. Fourteen alternatives and nine complete combinations are validated. Every combination's resource union equals the complete 22-resource REQUIRED universe: global completion therefore equals its last resource's rank. All 40 units are INFERABLE_AT_START; inherent discovery is zero. Task and repository-information gaps are NONE.

## Primary prospective measurements

Ratios use A as denominator; lower is better. Parameters are (k1, b, filename weight). Canonical tokenization, whole-resource frame, independent content/filename scoring and stable corpus tie rules remain identical. No identifier expansion, query rewriting or BM25F.

| Arm | Parameters | Global positive | Own positive union | Own positive cells | REQUIRED resources/cells/unit judgments/distinct units |
|---|---|---:|---:|---:|---|
| A | [1.2, 0.75, 0.25] | 529 | 497 | 3178 | 22/22; 39/39; 45/45; 40/40 |
| B | [2.4, 0.0, 2.0] | 529 | 497 | 3178 | 22/22; 39/39; 45/45; 40/40 |
| C | [2.4, 0.5, 1.0] | 529 | 497 | 3178 | 22/22; 39/39; 45/45; 40/40 |
| D | [2.4, 0.75, 0.25] | 529 | 497 | 3178 | 22/22; 39/39; 45/45; 40/40 |

For B, C and D, A-only REQUIRED, challenger-only REQUIRED and missed-by-both are empty for resources, cells, obligation-relative units and distinct units. Membership is stable, verified by exact sets.

| Arm | Global completion | Ratio | Max-own | Ratio | Change | Prefix occurrences | Unique union | Union/22 | Excess | Union change vs A | REQUIRED | HELPFUL | UNNECESSARY |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| A | 360 | 1.000000 | 192 | 1.000000 | +0.000% | 556 | 257 | 11.681818 | 235 | +0.000% | 39 | 27 | 490 |
| B | 363 | 1.008333 | 196 | 1.020833 | +2.083% | 623 | 243 | 11.045455 | 221 | -5.447% | 39 | 29 | 555 |
| C | 360 | 1.000000 | 183 | 0.953125 | -4.688% | 506 | 232 | 10.545455 | 210 | -9.728% | 39 | 28 | 439 |
| D | 366 | 1.016667 | 178 | 0.927083 | -7.292% | 509 | 243 | 11.045455 | 221 | -5.447% | 39 | 25 | 445 |

### Per-obligation accepted-alternative completion

All members of one alternative are required. Equal-depth alternatives tie by frozen alternative identity; no members are mixed between alternatives. Each cell below reports depth (ratio to A).

| Obligation | A | B | C | D | Best | Notes |
|---|---:|---:|---:|---:|---|---|
| ownership | 42 (1.000000) | 51 (1.214286) | 37 (0.880952) | 34 (0.809524) | D | B worsens; C improves; D improves |
| range | 65 (1.000000) | 42 (0.646154) | 26 (0.400000) | 60 (0.923077) | C | B improves; C improves; D improves |
| identity | 192 (1.000000) | 196 (1.020833) | 183 (0.953125) | 178 (0.927083) | D | B worsens; C improves; D improves |
| frame | 158 (1.000000) | 149 (0.943038) | 149 (0.943038) | 148 (0.936709) | D | B improves; C improves; D improves |
| materialization | 8 (1.000000) | 31 (3.875000) | 13 (1.625000) | 7 (0.875000) | D | B worsens; C worsens; D improves |
| assembly | 1 (1.000000) | 12 (12.000000) | 1 (1.000000) | 1 (1.000000) | A, C, D | B worsens; C ties; D ties |
| package | 32 (1.000000) | 54 (1.687500) | 37 (1.156250) | 31 (0.968750) | D | B worsens; C worsens; D improves |
| tests | 31 (1.000000) | 31 (1.000000) | 30 (0.967742) | 25 (0.806452) | D | B ties; C improves; D improves |
| documentation | 15 (1.000000) | 16 (1.066667) | 14 (0.933333) | 19 (1.266667) | C | B worsens; C improves; D worsens |
| validation | 12 (1.000000) | 41 (3.416667) | 16 (1.333333) | 6 (0.500000) | D | B worsens; C worsens; D improves |

### Exact frozen gates

No required resource/cell/unit loss; global/max-own <=1.05 baseline; >=10% union OR max-own improvement; each own depth <=1.25 baseline; >=half obligations nonworse; median/p95 query scoring <=3x; development worst max-own/union <=1.25. Candidate is later adoption consideration only. BASELINE_ROBUST if all challengers reach-safe and all global/max-own/union ratios within [0.95,1.05] without meaningful improvement; otherwise MIXED / NO SAFE REPLACEMENT. Concrete scorer defect stops.

| Gate | A | B | C | D |
|---|---|---|---|---|
| REQUIRED reach safe | baseline | PASS | PASS | PASS |
| Global ≤1.05× | baseline | PASS | PASS | PASS |
| Max-own ≤1.05× | baseline | PASS | PASS | PASS |
| ≥10% primary improvement | — | FAIL | FAIL | FAIL |
| No obligation >1.25× | — | FAIL | FAIL | FAIL |
| ≥half obligations nonworse | — | FAIL | PASS | PASS |
| Cost ≤3× | baseline | PASS | PASS | PASS |
| Development safety ≤1.25 | baseline | PASS | PASS | PASS |
| Overall prospective rule | BASELINE | FAIL | FAIL | FAIL |

**Outcome: MIXED / NO SAFE REPLACEMENT. Passing candidates: [].**
No pre-frozen prospective precedence chooses a single winner if several candidates pass; all would be retained. A candidate earns a separate production-adoption checkpoint, never automatic adoption.

## Supporting top-K and paired REQUIRED ranks

Global labels are an explicit resource projection: REQUIRED if required by any obligation, otherwise HELPFUL_ONLY if helpful to any, otherwise UNNECESSARY. Own labels are obligation-relative. R+H is REQUIRED plus HELPFUL_ONLY. These descriptive metrics do not override the frozen gates.

| Arm | K | Global R | Global R+H | Global U | Own R | Own R+H | Own U | Own denominator |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| A | 5 | 3 | 4 | 1 | 15 | 27 | 23 | 50 |
| A | 10 | 4 | 6 | 4 | 20 | 36 | 64 | 100 |
| A | 20 | 4 | 8 | 12 | 26 | 48 | 152 | 200 |
| B | 5 | 1 | 2 | 3 | 6 | 13 | 37 | 50 |
| B | 10 | 3 | 4 | 6 | 13 | 26 | 74 | 100 |
| B | 20 | 4 | 8 | 12 | 21 | 41 | 159 | 200 |
| C | 5 | 3 | 4 | 1 | 15 | 26 | 24 | 50 |
| C | 10 | 4 | 5 | 5 | 19 | 37 | 63 | 100 |
| C | 20 | 4 | 8 | 12 | 27 | 50 | 150 | 200 |
| D | 5 | 3 | 4 | 1 | 15 | 28 | 22 | 50 |
| D | 10 | 3 | 5 | 5 | 23 | 41 | 59 | 100 |
| D | 20 | 4 | 8 | 12 | 25 | 49 | 151 | 200 |

Rank delta = challenger minus A; negative improves. All 39 REQUIRED cells are paired.

| Arm | Improved | Unchanged | Worsened | Median delta | Best improvement | Worst regression |
|---|---:|---:|---:|---:|---:|---:|
| B | 9 | 2 | 28 | 4 | -34 | 34 |
| C | 18 | 9 | 12 | 0 | -39 | 11 |
| D | 20 | 11 | 8 | -1 | -14 | 7 |

## R1.5 diagnostic evidence

Representatives are chosen deterministically: largest own-lane REQUIRED gain and regression for each challenger (obligation/address ties), its largest completion-ratio regression bottleneck, plus its global completion bottleneck. Full explanations, source spans, every term and changed unnecessary overtaker are in analysis.json. Mechanics reconstruct captured scores, not a second query execution. DF/IDF and lexical matches do not change between arms. Global-lane diagnostics retain no obligation judgment; their overtaker label counts are unjudged, rather than negative evidence.

### B / largest_required_gain: range

`src/devtools/resources/filesystem/codecs/text.py`: rank 65 → 31, score 10.440633 → 20.005970. Overtakers added 6, removed 40. New overtaker labels: {'REQUIRED': 0, 'HELPFUL_ONLY': 0, 'UNNECESSARY': 6, 'UNRESOLVED': 0}.

| Field/term | TF | DF | IDF | Length / average | Saturation A → challenger | Weighted contribution A → challenger |
|---|---:|---:|---:|---|---|---|
| filename/text | 1 | 2 | 5.360353 | 1 / 1.521657 | 1.163122 → 1.000000 | 1.558687 → 10.720706 |
| content/text | 12 | 168 | 1.149708 | 224 / 569.743879 | 2.086323 → 2.833333 | 2.398661 → 3.257505 |
| content/content | 7 | 171 | 1.132060 | 224 / 569.743879 | 2.012061 → 2.531915 | 2.277774 → 2.866280 |
| content/utf | 1 | 99 | 1.676486 | 224 / 569.743879 | 1.330235 → 1.000000 | 2.230120 → 1.676486 |
| content/8 | 1 | 120 | 1.484994 | 224 / 569.743879 | 1.330235 → 1.000000 | 1.975391 → 1.484994 |

A: content 8.881946; weighted filename 1.558687.

B: content 9.285265; weighted filename 10.720706.

new UNNECESSARY overtaker `docs/architecture/decisions/ADR-0002-repository-intelligence-identity-and-derivation.md`: rank 77 → 5; leading content/range TF 2, DF 18, IDF 3.358873, length 8240/569.743879, saturation 1.545455, weighted contribution 5.190985.

new UNNECESSARY overtaker `docs/architecture/decisions/ADR-0004-context-disclosure-planning-and-assembly.md`: rank 138 → 29; leading content/extraction TF 2, DF 9, IDF 4.025352, length 3908/569.743879, saturation 1.545455, weighted contribution 6.220998.

new UNNECESSARY overtaker `docs/architecture/taxonomy.md`: rank 139 → 19; leading content/resource TF 31, DF 154, IDF 1.236449, length 7251/569.743879, saturation 3.155689, weighted contribution 3.901849.

### B / largest_required_regression: frame

`src/devtools/context/planning/materialization.py`: rank 92 → 126, score 9.386776 → 10.402187. Overtakers added 35, removed 1. New overtaker labels: {'REQUIRED': 0, 'HELPFUL_ONLY': 0, 'UNNECESSARY': 35, 'UNRESOLVED': 0}.

| Field/term | TF | DF | IDF | Length / average | Saturation A → challenger | Weighted contribution A → challenger |
|---|---:|---:|---:|---|---|---|
| content/snapshot | 6 | 151 | 1.256058 | 309 / 569.743879 | 1.944575 → 2.428571 | 2.442499 → 3.050426 |
| content/repository | 6 | 217 | 0.894445 | 309 / 569.743879 | 1.944575 → 2.428571 | 1.739315 → 2.172223 |
| content/identity | 4 | 189 | 1.032254 | 309 / 569.743879 | 1.837884 → 2.125000 | 1.897164 → 2.193541 |
| content/resource | 1 | 154 | 1.236449 | 309 / 569.743879 | 1.230347 → 1.000000 | 1.521261 → 1.236449 |
| content/content | 2 | 171 | 1.132060 | 309 / 569.743879 | 1.578128 → 1.545455 | 1.786536 → 1.749548 |

A: content 9.386776; weighted filename 0.000000.

B: content 10.402187; weighted filename 0.000000.

new UNNECESSARY overtaker `AGENTS.md`: rank 115 → 85; leading content/validation TF 5, DF 49, IDF 2.374671, length 1629/569.743879, saturation 2.297297, weighted contribution 5.455325.

new UNNECESSARY overtaker `docs/backlog/epics/B-0015-framework-acceptance-harness-validation.md`: rank 142 → 72; leading filename/validation TF 1, DF 3, IDF 5.023881, length 6/1.521657, saturation 1.000000, weighted contribution 10.047761.

new UNNECESSARY overtaker `docs/backlog/items/B-0008-investigate-repository-context-discovery.md`: rank 119 → 57; leading filename/repository TF 1, DF 3, IDF 5.023881, length 6/1.521657, saturation 1.000000, weighted contribution 10.047761.

### B / largest_completion_regression: assembly

`src/devtools/context/planning/rendering.py`: rank 1 → 12, score 24.721021 → 25.856730. Overtakers added 11, removed 0. New overtaker labels: {'REQUIRED': 0, 'HELPFUL_ONLY': 1, 'UNNECESSARY': 10, 'UNRESOLVED': 0}.

| Field/term | TF | DF | IDF | Length / average | Saturation A → challenger | Weighted contribution A → challenger |
|---|---:|---:|---:|---|---|---|
| content/disclosure | 10 | 52 | 2.315830 | 221 / 569.743879 | 2.065901 → 2.741935 | 4.784277 → 6.349857 |
| content/render | 1 | 5 | 4.571895 | 221 / 569.743879 | 1.334058 → 1.000000 | 6.099172 → 4.571895 |
| content/plan | 4 | 22 | 3.163128 | 221 / 569.743879 | 1.892838 → 2.125000 | 5.987288 → 6.721647 |
| content/order | 1 | 79 | 1.900886 | 221 / 569.743879 | 1.334058 → 1.000000 | 2.535892 → 1.900886 |
| content/context | 10 | 234 | 0.819188 | 221 / 569.743879 | 2.065901 → 2.741935 | 1.692361 → 2.246160 |
| content/task | 4 | 78 | 1.913545 | 221 / 569.743879 | 1.892838 → 2.125000 | 3.622030 → 4.066283 |

A: content 24.721021; weighted filename 0.000000.

B: content 25.856730; weighted filename 0.000000.

new UNNECESSARY overtaker `docs/architecture.md`: rank 6 → 2; leading content/plan TF 10, DF 22, IDF 3.163128, length 11091/569.743879, saturation 2.741935, weighted contribution 8.673093.

new UNNECESSARY overtaker `docs/architecture/decisions/ADR-0001-cohesive-model-interaction-boundary.md`: rank 24 → 11; leading filename/model TF 1, DF 7, IDF 4.261740, length 6/1.521657, saturation 1.000000, weighted contribution 8.523481.

new UNNECESSARY overtaker `docs/architecture/decisions/ADR-0002-repository-intelligence-identity-and-derivation.md`: rank 40 → 8; leading content/disclosure TF 13, DF 52, IDF 2.315830, length 8240/569.743879, saturation 2.870130, weighted contribution 6.646734.

### B / global_completion_bottleneck: global

`pyproject.toml`: rank 346 → 363, score 18.678060 → 14.174060. Overtakers added 19, removed 2. New overtaker labels: {'REQUIRED': 0, 'HELPFUL_ONLY': 0, 'UNNECESSARY': 0, 'UNRESOLVED': 0}.

| Field/term | TF | DF | IDF | Length / average | Saturation A → challenger | Weighted contribution A → challenger |
|---|---:|---:|---:|---|---|---|
| content/line | 1 | 37 | 2.652303 | 165 / 569.743879 | 1.409675 → 1.000000 | 3.738885 → 2.652303 |
| content/dependency | 1 | 68 | 2.049810 | 165 / 569.743879 | 1.409675 → 1.000000 | 2.889566 → 2.049810 |
| content/run | 1 | 78 | 1.913545 | 165 / 569.743879 | 1.409675 → 1.000000 | 2.697476 → 1.913545 |
| content/8 | 1 | 120 | 1.484994 | 165 / 569.743879 | 1.409675 → 1.000000 | 2.093359 → 1.484994 |
| content/source | 1 | 193 | 1.011366 | 165 / 569.743879 | 1.409675 → 1.000000 | 1.425697 → 1.011366 |
| content/in | 1 | 270 | 0.676371 | 165 / 569.743879 | 1.409675 → 1.000000 | 0.953464 → 0.676371 |

A: content 18.678060; weighted filename 0.000000.

B: content 14.174060; weighted filename 0.000000.

### C / largest_required_gain: range

`src/devtools/resources/filesystem/codecs/text.py`: rank 65 → 26, score 10.440633 → 16.659353. Overtakers added 0, removed 39. New overtaker labels: {'REQUIRED': 0, 'HELPFUL_ONLY': 0, 'UNNECESSARY': 0, 'UNRESOLVED': 0}.

| Field/term | TF | DF | IDF | Length / average | Saturation A → challenger | Weighted contribution A → challenger |
|---|---:|---:|---:|---|---|---|
| filename/text | 1 | 2 | 5.360353 | 1 / 1.521657 | 1.163122 → 1.137651 | 1.558687 → 6.098211 |
| content/text | 12 | 168 | 1.149708 | 224 / 569.743879 | 2.086323 → 2.984247 | 2.398661 → 3.431012 |
| content/content | 7 | 171 | 1.132060 | 224 / 569.743879 | 2.012061 → 2.744531 | 2.277774 → 3.106974 |
| content/utf | 1 | 99 | 1.676486 | 224 / 569.743879 | 1.330235 → 1.272555 | 2.230120 → 2.133420 |
| content/8 | 1 | 120 | 1.484994 | 224 / 569.743879 | 1.330235 → 1.272555 | 1.975391 → 1.889736 |

A: content 8.881946; weighted filename 1.558687.

C: content 10.561142; weighted filename 6.098211.

removed UNNECESSARY overtaker `docs/architecture/localization.md`: rank 58 → 56; leading content/end TF 8, DF 29, IDF 2.892253, length 2749/569.743879, saturation 1.814547, weighted contribution 5.248128.

removed UNNECESSARY overtaker `docs/architecture/retrieval.md`: rank 53 → 47; leading content/resource TF 20, DF 154, IDF 1.236449, length 3059/569.743879, saturation 2.459945, weighted contribution 3.041597.

removed UNNECESSARY overtaker `docs/documentation_map.md`: rank 56 → 54; leading content/boundaries TF 5, DF 50, IDF 2.354670, length 3828/569.743879, saturation 1.191931, weighted contribution 2.806604.

### C / largest_required_regression: identity

`src/devtools/context/repository/observation.py`: rank 105 → 116, score 3.739272 → 4.063713. Overtakers added 13, removed 2. New overtaker labels: {'REQUIRED': 0, 'HELPFUL_ONLY': 1, 'UNNECESSARY': 12, 'UNRESOLVED': 0}.

| Field/term | TF | DF | IDF | Length / average | Saturation A → challenger | Weighted contribution A → challenger |
|---|---:|---:|---:|---|---|---|
| content/order | 2 | 79 | 1.900886 | 525 / 569.743879 | 1.406056 → 1.579280 | 2.672753 → 3.002032 |
| content/identity | 1 | 189 | 1.032254 | 525 / 569.743879 | 1.033194 → 1.028508 | 1.066519 → 1.061682 |

A: content 3.739272; weighted filename 0.000000.

C: content 4.063713; weighted filename 0.000000.

new UNNECESSARY overtaker `src/devtools/agents/conversation/history.py`: rank 111 → 109; leading content/order TF 3, DF 79, IDF 1.900886, length 158/569.743879, saturation 2.250274, weighted contribution 4.277516.

new UNNECESSARY overtaker `src/devtools/context/localization/association/hypothesis.py`: rank 123 → 107; leading content/identity TF 32, DF 189, IDF 1.032254, length 1478/569.743879, saturation 2.996174, weighted contribution 3.092814.

new UNNECESSARY overtaker `src/devtools/context/localization/identity.py`: rank 130 → 61; leading filename/identity TF 1, DF 4, IDF 4.772566, length 1/1.521657, saturation 1.137651, weighted contribution 5.429515.

### C / largest_completion_regression: materialization

`src/devtools/context/python/function/planned_reference.py`: rank 8 → 13, score 19.749828 → 22.400870. Overtakers added 5, removed 0. New overtaker labels: {'REQUIRED': 0, 'HELPFUL_ONLY': 0, 'UNNECESSARY': 5, 'UNRESOLVED': 0}.

| Field/term | TF | DF | IDF | Length / average | Saturation A → challenger | Weighted contribution A → challenger |
|---|---:|---:|---:|---|---|---|
| content/disclosure | 9 | 52 | 2.315830 | 249 / 569.743879 | 2.042641 → 2.853294 | 4.730409 → 6.607745 |
| content/representation | 4 | 82 | 1.863845 | 249 / 569.743879 | 1.874999 → 2.375776 | 3.494709 → 4.428078 |
| content/text | 2 | 168 | 1.149708 | 249 / 569.743879 | 1.633663 → 1.825775 | 1.878235 → 2.099107 |
| content/materialize | 1 | 7 | 4.261740 | 249 / 569.743879 | 1.299212 → 1.247960 | 5.536903 → 5.318482 |
| content/plan | 1 | 22 | 3.163128 | 249 / 569.743879 | 1.299212 → 1.247960 | 4.109573 → 3.947458 |

A: content 19.749828; weighted filename 0.000000.

C: content 22.400870; weighted filename 0.000000.

new UNNECESSARY overtaker `docs/architecture/taxonomy.md`: rank 9 → 9; leading content/disclosure TF 21, DF 52, IDF 2.315830, length 7251/569.743879, saturation 1.905416, weighted contribution 4.412621.

new UNNECESSARY overtaker `docs/backlog/epics/B-0002-coding-context-substrate.md`: rank 10 → 8; leading content/disclosure TF 23, DF 52, IDF 2.315830, length 9795/569.743879, saturation 1.744355, weighted contribution 4.039630.

new UNNECESSARY overtaker `docs/documentation_map.md`: rank 11 → 10; leading content/disclosure TF 9, DF 52, IDF 2.315830, length 3828/569.743879, saturation 1.675558, weighted contribution 3.880309.

### C / global_completion_bottleneck: global

`src/devtools/context/__init__.py`: rank 360 → 360, score 16.425542 → 17.389481. Overtakers added 2, removed 2. New overtaker labels: {'REQUIRED': 0, 'HELPFUL_ONLY': 0, 'UNNECESSARY': 0, 'UNRESOLVED': 0}.

| Field/term | TF | DF | IDF | Length / average | Saturation A → challenger | Weighted contribution A → challenger |
|---|---:|---:|---:|---|---|---|
| content/context | 6 | 234 | 0.819188 | 263 / 569.743879 | 1.965617 → 2.630923 | 1.610209 → 2.155220 |
| content/repository | 4 | 217 | 0.894445 | 263 / 569.743879 | 1.866206 → 2.363601 | 1.669218 → 2.114110 |
| content/python | 2 | 168 | 1.149708 | 263 / 569.743879 | 1.620358 → 1.811433 | 1.862938 → 2.082619 |
| content/from | 5 | 408 | 0.264152 | 263 / 569.743879 | 1.924608 → 2.517052 | 0.508388 → 0.664883 |
| content/planning | 1 | 28 | 2.926739 | 263 / 569.743879 | 1.282462 → 1.234598 | 3.753433 → 3.613346 |
| content/public | 1 | 60 | 2.174000 | 263 / 569.743879 | 1.282462 → 1.234598 | 2.788074 → 2.684016 |

A: content 16.425542; weighted filename 0.000000.

C: content 17.389481; weighted filename 0.000000.

### D / largest_required_gain: identity

`src/devtools/context/repository/resource.py`: rank 192 → 178, score 1.903444 → 2.531936. Overtakers added 0, removed 14. New overtaker labels: {'REQUIRED': 0, 'HELPFUL_ONLY': 0, 'UNNECESSARY': 0, 'UNRESOLVED': 0}.

| Field/term | TF | DF | IDF | Length / average | Saturation A → challenger | Weighted contribution A → challenger |
|---|---:|---:|---:|---|---|---|
| content/identity | 4 | 189 | 1.032254 | 299 / 569.743879 | 1.843968 → 2.452822 | 1.903444 → 2.531936 |

A: content 1.903444; weighted filename 0.000000.

D: content 2.531936; weighted filename 0.000000.

removed UNNECESSARY overtaker `src/devtools/models/serving/llama_cpp.py`: rank 181 → 230; leading content/option TF 1, DF 16, IDF 3.473283, length 1647/569.743879, saturation 0.499751, weighted contribution 1.735776.

removed UNNECESSARY overtaker `src/devtools/observability/evidence/model_interaction.py`: rank 154 → 205; leading content/order TF 1, DF 79, IDF 1.900886, length 960/569.743879, saturation 0.733875, weighted contribution 1.395013.

removed UNNECESSARY overtaker `src/devtools/persistence/sqlite.py`: rank 160 → 197; leading content/order TF 2, DF 79, IDF 1.900886, length 989/569.743879, saturation 1.187864, weighted contribution 2.257994.

### D / largest_required_regression: identity

`src/devtools/context/repository/observation.py`: rank 105 → 112, score 3.739272 → 4.112282. Overtakers added 9, removed 2. New overtaker labels: {'REQUIRED': 0, 'HELPFUL_ONLY': 1, 'UNNECESSARY': 8, 'UNRESOLVED': 0}.

| Field/term | TF | DF | IDF | Length / average | Saturation A → challenger | Weighted contribution A → challenger |
|---|---:|---:|---:|---|---|---|
| content/order | 2 | 79 | 1.900886 | 525 / 569.743879 | 1.406056 → 1.596754 | 2.672753 → 3.035248 |
| content/identity | 1 | 189 | 1.032254 | 525 / 569.743879 | 1.033194 → 1.043380 | 1.066519 → 1.077034 |

A: content 3.739272; weighted filename 0.000000.

D: content 4.112282; weighted filename 0.000000.

new UNNECESSARY overtaker `docs/backlog/items/B-0016-define-framework-live-harness-acceptance.md`: rank 118 → 107; leading content/deterministic TF 2, DF 79, IDF 1.900886, length 127/569.743879, saturation 2.265736, weighted contribution 4.306906.

new UNNECESSARY overtaker `src/devtools/agents/conversation/history.py`: rank 111 → 96; leading content/order TF 3, DF 79, IDF 1.900886, length 158/569.743879, saturation 2.488308, weighted contribution 4.729990.

new UNNECESSARY overtaker `src/devtools/context/localization/routing/derive.py`: rank 107 → 104; leading content/identity TF 9, DF 189, IDF 1.032254, length 719/569.743879, saturation 2.577592, weighted contribution 2.660730.

### D / largest_completion_regression: documentation

`docs/architecture/taxonomy.md`: rank 15 → 19, score 17.799830 → 18.863374. Overtakers added 4, removed 0. New overtaker labels: {'REQUIRED': 0, 'HELPFUL_ONLY': 0, 'UNNECESSARY': 4, 'UNRESOLVED': 0}.

| Field/term | TF | DF | IDF | Length / average | Saturation A → challenger | Weighted contribution A → challenger |
|---|---:|---:|---:|---|---|---|
| content/representation | 25 | 82 | 1.863845 | 7251 / 569.743879 | 1.496432 → 1.752281 | 2.789117 → 3.265981 |
| content/disclosure | 21 | 52 | 2.315830 | 7251 / 569.743879 | 1.410511 → 1.604199 | 3.266503 → 3.715053 |
| content/context | 43 | 234 | 0.819188 | 7251 / 569.743879 | 1.727725 → 2.198226 | 1.415331 → 1.800760 |
| content/documentation | 3 | 29 | 2.892253 | 7251 / 569.743879 | 0.447333 → 0.384787 | 1.293802 → 1.112901 |
| content/materialization | 3 | 39 | 2.600343 | 7251 / 569.743879 | 0.447333 → 0.384787 | 1.163220 → 1.000578 |
| content/architecture | 4 | 46 | 2.437191 | 7251 / 569.743879 | 0.558585 → 0.494398 | 1.361378 → 1.204943 |

A: content 17.799830; weighted filename 0.000000.

D: content 18.863374; weighted filename 0.000000.

new UNNECESSARY overtaker `docs/backlog/overview.md`: rank 20 → 17; leading content/documentation TF 12, DF 29, IDF 2.892253, length 1215/569.743879, saturation 2.481968, weighted contribution 7.178480.

new UNNECESSARY overtaker `src/devtools/context/planning/materialization.py`: rank 16 → 11; leading content/disclosure TF 4, DF 52, IDF 2.315830, length 309/569.743879, saturation 2.438925, weighted contribution 5.648136.

new UNNECESSARY overtaker `src/devtools/context/planning/rendering.py`: rank 17 → 15; leading content/disclosure TF 10, DF 52, IDF 2.315830, length 221/569.743879, saturation 3.009327, weighted contribution 6.969090.

### D / global_completion_bottleneck: global

`src/devtools/context/__init__.py`: rank 360 → 366, score 16.425542 → 19.216789. Overtakers added 6, removed 0. New overtaker labels: {'REQUIRED': 0, 'HELPFUL_ONLY': 0, 'UNNECESSARY': 0, 'UNRESOLVED': 0}.

| Field/term | TF | DF | IDF | Length / average | Saturation A → challenger | Weighted contribution A → challenger |
|---|---:|---:|---:|---|---|---|
| content/context | 6 | 234 | 0.819188 | 263 / 569.743879 | 1.965617 → 2.745293 | 1.610209 → 2.248911 |
| content/repository | 4 | 217 | 0.894445 | 263 / 569.743879 | 1.866206 → 2.504189 | 1.669218 → 2.239859 |
| content/python | 2 | 168 | 1.149708 | 263 / 569.743879 | 1.620358 → 1.981987 | 1.862938 → 2.278706 |
| content/planning | 1 | 28 | 2.926739 | 263 / 569.743879 | 1.282462 → 1.398659 | 3.753433 → 4.093511 |
| content/public | 1 | 60 | 2.174000 | 263 / 569.743879 | 1.282462 → 1.398659 | 2.788074 → 3.040685 |
| content/retrieval | 1 | 94 | 1.728044 | 263 / 569.743879 | 1.282462 → 1.398659 | 2.216151 → 2.416944 |

A: content 16.425542; weighted filename 0.000000.

D: content 19.216789; weighted filename 0.000000.

## Query-term discrimination inputs for R1.7

Profiles are obligation-relative. Matching resources are content/positive filename union; DF/IDF below refer to content, with independent filename profiles retained in JSON. Yields describe gold, not instructions to remove or weight terms. Representative high-footprint terms are selected per lane by descending effective matched count; high-value terms by REQUIRED yield (then count, then term).

| Obligation | Selection | Term | Content DF | IDF | Matched/frame | REQUIRED | HELPFUL | UNNECESSARY | R yield | H yield | U yield |
|---|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| ownership | footprint | context | 234 | 0.819188 | 234/531 (44.068%) | 5 | 4 | 225 | 2.137% | 1.709% | 96.154% |
| ownership | footprint | representation | 82 | 1.863845 | 82/531 (15.443%) | 4 | 4 | 74 | 4.878% | 4.878% | 90.244% |
| ownership | yield | planning | 28 | 2.926739 | 28/531 (5.273%) | 5 | 3 | 20 | 17.857% | 10.714% | 71.429% |
| ownership | yield | disclosure | 52 | 2.315830 | 52/531 (9.793%) | 4 | 3 | 45 | 7.692% | 5.769% | 86.538% |
| range | footprint | content | 171 | 1.132060 | 171/531 (32.203%) | 5 | 7 | 159 | 2.924% | 4.094% | 92.982% |
| range | footprint | text | 168 | 1.149708 | 168/531 (31.638%) | 4 | 7 | 157 | 2.381% | 4.167% | 93.452% |
| range | yield | range | 18 | 3.358873 | 18/531 (3.390%) | 2 | 2 | 14 | 11.111% | 11.111% | 77.778% |
| range | yield | end | 29 | 2.892253 | 29/531 (5.461%) | 2 | 2 | 25 | 6.897% | 6.897% | 86.207% |
| identity | footprint | identity | 189 | 1.032254 | 189/531 (35.593%) | 4 | 7 | 178 | 2.116% | 3.704% | 94.180% |
| identity | footprint | deterministic | 79 | 1.900886 | 79/531 (14.878%) | 0 | 2 | 77 | 0.000% | 2.532% | 97.468% |
| identity | yield | plan | 22 | 3.163128 | 22/531 (4.143%) | 2 | 3 | 17 | 9.091% | 13.636% | 77.273% |
| identity | yield | lineage | 14 | 3.602495 | 14/531 (2.637%) | 1 | 1 | 12 | 7.143% | 7.143% | 85.714% |
| frame | footprint | repository | 217 | 0.894445 | 217/531 (40.866%) | 5 | 4 | 208 | 2.304% | 1.843% | 95.853% |
| frame | footprint | identity | 189 | 1.032254 | 189/531 (35.593%) | 5 | 4 | 180 | 2.646% | 2.116% | 95.238% |
| frame | yield | occurrence | 70 | 2.021031 | 70/531 (13.183%) | 3 | 3 | 64 | 4.286% | 4.286% | 91.429% |
| frame | yield | snapshot | 151 | 1.256058 | 151/531 (28.437%) | 4 | 4 | 143 | 2.649% | 2.649% | 94.702% |
| materialization | footprint | content | 171 | 1.132060 | 171/531 (32.203%) | 2 | 3 | 166 | 1.170% | 1.754% | 97.076% |
| materialization | footprint | text | 168 | 1.149708 | 168/531 (31.638%) | 3 | 4 | 161 | 1.786% | 2.381% | 95.833% |
| materialization | yield | materialize | 7 | 4.261740 | 7/531 (1.318%) | 4 | 0 | 3 | 57.143% | 0.000% | 42.857% |
| materialization | yield | plan | 22 | 3.163128 | 22/531 (4.143%) | 4 | 2 | 16 | 18.182% | 9.091% | 72.727% |
| assembly | footprint | context | 234 | 0.819188 | 234/531 (44.068%) | 1 | 5 | 228 | 0.427% | 2.137% | 97.436% |
| assembly | footprint | model | 143 | 1.310308 | 144/531 (27.119%) | 0 | 6 | 138 | 0.000% | 4.167% | 95.833% |
| assembly | yield | render | 5 | 4.571895 | 5/531 (0.942%) | 1 | 0 | 4 | 20.000% | 0.000% | 80.000% |
| assembly | yield | plan | 22 | 3.163128 | 22/531 (4.143%) | 1 | 3 | 18 | 4.545% | 13.636% | 81.818% |
| package | footprint | context | 234 | 0.819188 | 234/531 (44.068%) | 6 | 3 | 225 | 2.564% | 1.282% | 96.154% |
| package | footprint | package | 89 | 1.782405 | 89/531 (16.761%) | 3 | 1 | 85 | 3.371% | 1.124% | 95.506% |
| package | yield | planning | 28 | 2.926739 | 28/531 (5.273%) | 6 | 0 | 22 | 21.429% | 0.000% | 78.571% |
| package | yield | materialization | 39 | 2.600343 | 40/531 (7.533%) | 5 | 1 | 34 | 12.500% | 2.500% | 85.000% |
| tests | footprint | tests | 204 | 0.956076 | 204/531 (38.418%) | 2 | 5 | 197 | 0.980% | 2.451% | 96.569% |
| tests | footprint | identity | 189 | 1.032254 | 189/531 (35.593%) | 2 | 2 | 185 | 1.058% | 1.058% | 97.884% |
| tests | yield | range | 18 | 3.358873 | 18/531 (3.390%) | 1 | 0 | 17 | 5.556% | 0.000% | 94.444% |
| tests | yield | newline | 24 | 3.077970 | 24/531 (4.520%) | 1 | 0 | 23 | 4.167% | 0.000% | 95.833% |
| documentation | footprint | context | 234 | 0.819188 | 234/531 (44.068%) | 4 | 3 | 227 | 1.709% | 1.282% | 97.009% |
| documentation | footprint | explicit | 161 | 1.192138 | 161/531 (30.320%) | 4 | 3 | 154 | 2.484% | 1.863% | 95.652% |
| documentation | yield | planning | 28 | 2.926739 | 28/531 (5.273%) | 4 | 2 | 22 | 14.286% | 7.143% | 78.571% |
| documentation | yield | documentation | 29 | 2.892253 | 29/531 (5.461%) | 3 | 2 | 24 | 10.345% | 6.897% | 82.759% |
| validation | footprint | pytest | 139 | 1.338579 | 139/531 (26.177%) | 3 | 2 | 134 | 2.158% | 1.439% | 96.403% |
| validation | footprint | ruff | 73 | 1.979358 | 73/531 (13.748%) | 3 | 2 | 68 | 4.110% | 2.740% | 93.151% |
| validation | yield | mypy | 13 | 3.673954 | 13/531 (2.448%) | 2 | 1 | 10 | 15.385% | 7.692% | 76.923% |
| validation | yield | protected | 14 | 3.602495 | 14/531 (2.637%) | 2 | 3 | 9 | 14.286% | 21.429% | 64.286% |

## Captured costs and development comparison

Single treatment-run descriptive observations, not latency benchmarks. Shared index construction is 0.4245589000056498 s; diagnostics are excluded from query timing. No second treatment execution.

| Arm | Median ms | p95 ms | Eleven-query sum s | Median ratio | p95 ratio | Development worst own/union |
|---|---:|---:|---:|---:|---:|---:|
| A | 4.120900 | 17.026400 | 0.057223200 | 1.000000 | 1.000000 | 1/1 (1.000000) |
| B | 3.920200 | 17.073700 | 0.056590000 | 0.951297 | 1.002778 | 194/185 (1.048649) |
| C | 4.206900 | 17.189500 | 0.058910700 | 1.020869 | 1.009579 | 1/1 (1.000000) |
| D | 4.068200 | 16.419300 | 0.057390900 | 0.987212 | 0.964344 | 253/256 (0.988281) |

Development and prospective data remain separate; only the pre-frozen development safety bound enters candidate gating. Case 0008 remains supplementary for incomplete own metrics.

## Interpretation and limits

No development-selected configuration earned a production-adoption checkpoint. The exact outcome is MIXED / NO SAFE REPLACEMENT. BASELINE_ROBUST is inapplicable: C's union ratio 232/257 and D's max-own ratio 178/192 are outside the required 0.95–1.05 band. C's 9.728% union reduction is below 10%, without rounding or discretionary near-pass; satisfying that threshold would require at most 231 resources (0.9 × 257 = 231.3). Useful sensitivity exists, but no challenger passes every frozen gate.

D is the clean k1-only comparison. Higher k1 preserves all REQUIRED reach. It worsens global completion 360→366 (+1.667%), improves max-own 192→178 (−7.292%), and reduces union 257→243 (−5.447%), below the meaningful threshold. Eight obligations improve (ownership, range, identity, frame, materialization, package, tests, validation), assembly ties, and documentation worsens 15→19 (1.266667×), exceeding 1.25×. Development's stable max-own/union improvement replicates directionally, including nine nonworse obligations, but prospective per-obligation safety does not. Thus k1=2.4 does not earn production-candidate status under this protocol.

For REQUIRED repository/resource.py in the identity lane, identity TF=4, DF=189, IDF=1.032254, length=299 versus average 569.743879: saturation rises 1.843968→2.452822, content score 1.903444→2.531936, and rank 192→178. There is no filename contribution. Repetition gains also benefit UNNECESSARY competitors: conversation/history.py's order TF=3, DF=79, IDF=1.900886, length=158 has D saturation 2.488308 and contribution 4.729990, moving 111→96 and newly overtaking REQUIRED observation.py. That target's own score rises 3.739272→4.112282 while its rank worsens 105→112. Exact overtaker-set changes, rather than target score alone, explain ranking movement. The documentation bottleneck has its own paired diagnostic below.

B does not replicate a generally improved own completion: max-own worsens 192→196 (+2.083%), occurrences grow 556→623, and only three obligations are nonworse (range, frame, tests). Global depth worsens modestly 360→363, within the global gate; union falls to 243, below 10% improvement. Materialization 8→31, assembly 1→12, package 32→54, and validation 12→41 violate 1.25×. The development pattern remains mixed and prospective completion benefit weakens; global cost is less severe here than Case 0006's 155→212. Removing length normalization removes long-resource suppression while amplified filename evidence helps and collides: codecs/text.py gets 10.720706 weighted filename score versus 1.558687 at A. In the frame lane, unnecessary B-0015 validation and B-0008 repository filenames contribute 10.047761 each, newly overtaking required materialization.py. Long REQUIRED architecture.md improves package rank 9→3, while long UNNECESSARY ADR-0002 (8,240 tokens) improves range rank 77→5. These are joint configuration effects, not isolated causal attribution to b or filename weight.

C directionally reinforces development burden reduction: union 257→232 (−9.728%), occurrences 556→506, max-own 192→183 (−4.688%), and global depth ties at 360. Six obligations improve, assembly ties, and materialization, package and validation worsen. Materialization 8→13 (1.625×) and validation 12→16 (1.333333×) violate safety. Medium length normalization and filename weight 1 jointly boost text.py: weighted filename contribution 1.558687→6.098211, content 8.881946→10.561142, rank 65→26. Filename collisions also boost unnecessary localization/identity.py (identity lane 130→61), whose filename identity contribution is 5.429515. C is a near-threshold burden improvement, not a passing replacement.

k1: the isolated D comparison supports useful repetition sensitivity, not adoption of 2.4. b: the selected b=0 arm has serious obligation regressions and benefits both long required and irrelevant resources; b=0.5 offers burden improvements with regressions; b=0.75 with higher k1 is mostly stable but fails documentation safety. Filename weights 1 and 2 strengthen both helpful and colliding stems in C/B; 0.25 remains the unchanged production setting. Only D isolates one parameter. No causal optimum for b or filename weight, untested values, or universal production optimum follows from these three joint arms.

Keep development and Case 0010 separate. B weakens the completion-selected pattern and reinforces its known mixed/global-risk character. C reinforces the burden direction, with materially smaller gains than Case 0005's 151→106 and unsafe prospective obligations. D reinforces development's broad directional own/union stability, while its documentation regression weakens any claim of per-obligation robustness. Worst historical own/union ratios are B=194/185, C=1, D=253/256; all satisfy 1.25. No configuration was reselected or optimized using prospective gold.

Retain obligation-specific footprint/yield profiles, high-TF required/competitor changes, filename collisions and full-task term evidence. Examples: frame/repository DF=217, IDF=0.894445, 217/531 matched, 5 REQUIRED, 4 HELPFUL, 208 UNNECESSARY; identity/identity DF=189, IDF=1.032254, 4/7/178; ownership/context DF=234, IDF=0.819188, 5/4/225. More selective cues include ownership/planning (DF=28, 5/3/20), range/range (DF=18, 2/2/14), identity/lineage (DF=14, 1/1/12), and validation/mypy (DF=13, 2/1/10). In the full-task global bottleneck, rare planning/public evidence competes with ubiquitous context/repository/python/from evidence in long query text. Those contributions and repeated identity/order terms are direct inputs for R1.7 to investigate; this checkpoint neither implements weighting nor claims a term is harmful merely from footprint.

All required evidence is positively retrieved; the remaining observed problem is ranking discrimination, not required reach. Even C's smallest union is 232 versus the gold minimum 22, with 439 unnecessary prefix occurrences. R1.5 establishes RANKING_DISCRIMINATION_FAILURE on REQUIRED subjects with at least 20 unnecessary overtakers. REPRESENTATION_FAILURE and VOCABULARY_SEMANTIC_MISMATCH are not established by identical canonical parameter arms with no misses; RELATIONAL_RELEVANCE is not assessed by these lexical captures. CONTEXT_DISCLOSURE_FAILURE is outside this experiment's scope; INFORMATION_NEED_OBLIGATION_FAILURE is not supported (clean task gap NONE), without claiming end-to-end task success. Potential purpose-relative tuning is a future hypothesis suggested by mixed obligation effects, not implementation authorization.


Production parameters remain k1=1.2, b=0.75, filename weight=0.25. No production change, query weighting, BM25F, or R1.7 execution occurred. Confirmation/reserve access: NO. All Stage C attestations retain their historical NO values; this later authorized Stage D intentionally accesses treatment data.

R1 DONE; R1.5 DONE; R1.6 DONE. R1.6b remains not required before BM25F; no concrete scorer pathology was exposed. Next: R1.7 — investigate query-term discrimination and weighting using the completed R1.5 diagnostics and R1.6 parameter evidence, without yet changing production query semantics. After R1.7, R2 — true BM25F / field-aware sparse retrieval remains mandatory. R3–R6 and the preserved Localization continuation follow.
