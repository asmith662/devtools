# Increment 30: immediate explicit-root package/module containment

**State: completed development breadth baseline.** This Tier-1 experiment tests whether a single observed package-membership edge exposes useful parent-snapshot resources beyond saved lexical, import, and bounded References/Calls evidence. It does not rank or admit candidates into a fixed Context budget.

## Narrow hypothesis and semantics

Existing direct module-body function declarations already identify their own defining resource. Following a resource to its functions and back reaches that same resource; projecting a called function to its defining resource is Increment-29 Calls evidence. Neither is counted here as independent containment reach.

For one frozen parent snapshot and one caller-supplied explicit Python module root, the experiment reuses production `PythonModuleInterpretation` facts. A child interpretation named `P.C` has one immediate package relationship only when exactly one observed `PACKAGE` interpretation named `P` exists under the same root and snapshot. The package interpretation is the observed `__init__.py` resource under production interpretation semantics. Missing or ambiguous parents establish no relation. The retained support identifies both exact resources, both module interpretations and content identities, the explicit root, dotted names, snapshot, seed, and candidate direction.

The candidate projections use one edge only: child seed → immediate package initializer, and package initializer seed → each immediate child module. All saved canonical positive top-five seeds are excluded from additions. Case/snapshot/resource candidate duplicates are merged while every support remains. There is no recursion, package-to-sibling walk, inferred root, namespace-package claim, import/dependency/relevance claim, ranking, or K admission. No production code changed.

## Frozen population and candidate reach

The population is the established 24 development InformationNeeds and historical parent snapshots. The saved canonical first-five positive resources are the only seeds. The 14 Increment-27 held-out cases and suspended 16-case Increment-26 confirmation population were not executed. Candidate mechanics were persisted before any usefulness outcomes were loaded.

| Measure | Frozen result |
| --- | ---: |
| Development cases / cases with qualifying relations / cases with additions | 24 / 24 / 23 |
| Resources examined / interpreted, summed over case analyses | 6,289 / 5,432 |
| Qualified immediate relations, summed over case analyses | 5,031 |
| Missing observed immediate package / ambiguous immediate parent | 140 / 0 |
| Interpretation exclusions: non-Python / root-level initializer | 833 / 24 |
| Candidate pairs / distinct candidate addresses / retained supports | 49 / 26 / 73 |
| Child-to-package / package-to-child pairs | 49 / 0 |
| Maximum case / seed candidate fan-out | 4 / 1 |
| Canonical rank 6+ / no positive canonical rank | 28 / 21 |
| Absent from canonical / BM25+ / identifier / path-only / RRF positive universes | 21 / 21 / 15 / 30 / 15 |
| Absent from all five saved positive lexical universes | 15 |
| Absent from direct-import candidates | 29 |
| Absent from Increment-29 References/Calls candidates | 49 |
| Absent from all saved lexical universes **and** Imports **and** References/Calls | 12 |

All 49 candidate occurrences are observed package initializer resources. The zero package-to-child additions reflects these frozen seeds and the seed-exclusion rule; it does not establish that the reverse relation is impossible elsewhere. Counts of interpreted resources and relations include repeated analysis where cases share a parent snapshot. The case and seed fan-out distributions, relation supports, and exclusion states are in the frozen candidate artifact. The historical snapshot construction completed without a parse phase; module interpretation is address based. No execution-time benchmark was frozen, and no fan-out problem is apparent at this scale.

## Judgment boundary and artifact bindings

Exact development judgment reuse covered 29 pairs: 14 USEFUL, 15 NOT_USEFUL, and 0 UNJUDGED. The other 20 pairs span 16 cases. All 20 are child-to-package candidates; 12 are absent from the combined saved lexical/import/References-Calls surface.

The neutral input contains exactly those 20 targets with opaque identities, frozen InformationNeed purpose/query, parent snapshot, resource address, and parent-snapshot resource content. Its fields contain no containment direction, relation provenance, lexical ranks/scores, retrieval origins, or usefulness outcomes. All 20 were adjudicated from that input before candidate origins were joined: **0 USEFUL, 20 NOT_USEFUL, 0 UNJUDGED**. The hidden judgment freeze retains exact mappings and prior-source bindings. `USEFUL`, `NOT_USEFUL`, and `UNJUDGED` remain distinct.

| Artifact | Content identity | File SHA-256 |
| --- | --- | --- |
| `package_containment_freeze.json` | `c2a9fa9e7fc89da68975752ff229d1b35e2da2865ff14e7aa46304dba4395b0b` | `9be06e2dda17caafcc648ccdb05a2c1d8305126b5295f74685feb105c5dd36ae` |
| `package_containment_candidates.json` | `019c3a6e0a718b0f025a332bdef7d9c7b6f5d40baa453fc9544100572b6ac612` | `39c5624c312e259b002408e9707cb17237f2641d6922b3b20a8559f67efa29ad` |
| `package_containment_judgment_freeze.json` | `21141340498b57be402d09598b58d77e427f2de3de245dd19714734f1d6f398d` | `c3f61fac9c42d2e37ea718fa161a3ad8c9e179a0f7ba6b4c7b54b615b8fb10a5` |
| `package_containment_blinded_judgment_input.json` | `58efd8c4c506a770eb7afed00df3214e4a239be25bd2d84210cd035e53b605f7` | `7ea5664fd8ed90216b9f60e5afb16453e3cc0e6caf94452ce927c24caf8ba244` |
| `package_containment_frozen_judgments.json` | `6e51723f95df07c528f11fa8e78d731ae6fc550e1b9c572155c69ab2a80da1a8` | `408a65bbc4bc30d8284af287b047b737346a1751503d7a17cce5bdd7df1d043e` |
| `package_containment_development_results.json` | `cd071c0206a0dcfabbb95bbc6815443c30adfc6f04fbc65971f4330015bb83b3` | `1ff29c08c138b3ef990eb5b5e2cd1e173e2193c599ac5015ba62263284efd456` |

## Completed development result

| Surface | Candidate pairs | USEFUL | NOT_USEFUL | UNJUDGED |
| --- | ---: | ---: | ---: | ---: |
| Complete containment surface | 49 | 14 | 35 | 0 |
| Child-to-package | 49 | 14 | 35 | 0 |
| Package-to-child | 0 | 0 | 0 | 0 |
| Outside canonical top five | 49 | 14 | 35 | 0 |
| Absent from all five saved positive lexical universes | 15 | 1 | 14 | 0 |
| Absent from direct-import candidates | 29 | 0 | 29 | 0 |
| Absent from References/Calls candidates | 49 | 14 | 35 | 0 |
| Absent from the complete saved lexical/import/References-Calls union | 12 | 0 | 12 | 0 |

The single USEFUL candidate absent from all five saved positive lexical universes was `src/devtools/core/time/models/__init__.py` for `i25-9009cc143957`; it was already in the import candidate surface. All 12 candidates absent from the complete previous evidence union were judged NOT_USEFUL. The 14 useful containment additions were already available through import candidates. The new blinded population supplied no useful pairs.

**Breadth verdict:** immediate explicit-root package/module containment generated distinct candidates but did **not** demonstrate useful reach beyond the complete saved lexical/import/References-Calls evidence union on this development population. Candidate fan-out was small (maximum four per case and one per seed), so no obvious fan-out problem appeared. This is a result for the observed child-module → immediate-package-initializer direction only. The frozen top-five seeds produced no package→child candidate additions; no conclusion about that direction follows.

## Production RI implication and next step

The relation is deterministic repository-structure evidence and remains a plausible later production Repository Intelligence design candidate. Its retrieval result does not invalidate the repository fact, and the experiment implementation is not production-ready. The relation implies neither runtime importability, import dependency, nor task relevance. These 24 development cases, saved seeds, and resource-level judgments do not establish behavior on other repositories, package→child retrieval, or fixed-budget ranking. The 29 reused judgments came from earlier candidate populations, so their usefulness distribution should not be read as an unbiased sample of all package initializers.

**Next breadth family:** Inheritance. Stop containment after this baseline; richer containment and declaration semantics remain parked. Confirmation remains sealed.
