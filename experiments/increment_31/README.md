# Increment 31: exact mirrored code/test paths

**State: completed development breadth baseline.** This development-only Tier-1 experiment asks whether an exact observed source/test path correspondence supplies useful repository resources beyond the saved lexical, Imports, References/Calls, and immediate Containment evidence. It does not rank or admit candidates into a fixed Context budget.

## Frozen relation and population

In one historical parent `RepositorySnapshot`, both resources must be observed at exactly `src/devtools/<relative-directory>/<stem>.py` and `tests/<relative-directory>/test_<stem>.py`. Paths are canonical repository resource addresses. Initializer resources are excluded. The fact asserted is **exact path correspondence**. It does not assert execution, coverage, test ownership, or that the test exercises the source module. The relation and candidate projection remain experiment-local.

The 24 frozen development InformationNeeds use their saved positive canonical top-five resource seeds. A source seed can nominate only its mirrored test; a test seed can nominate only its mirrored source. All seed resources are excluded. Candidates are deduplicated by InformationNeed, parent snapshot, and resource address while retaining every support and its direction. Source/test matching uses observed parent-snapshot resource addresses only. Historical changed paths are neither read by the matching/projection functions nor used to select judgments. No confirmation population was executed.

## Frozen candidate reach and cost

| Measure | Result |
| --- | ---: |
| Development cases / cases with additions | 24 / 19 |
| Source / test Python resources examined, summed across snapshots | 2,855 / 2,601 |
| Exact mirrored pairs observed, summed across snapshots | 1,152 |
| Unmatched eligible source / named test resources | 880 / 655 |
| Excluded initializer resources | 1,616 |
| Candidate pairs / distinct candidate addresses / retained supports | 34 / 27 / 34 |
| Source→test / test→source candidate pairs | 18 / 16 |
| Maximum case / seed fan-out | 4 / 1 |
| Outside canonical top five | 34 |
| Absent from all five saved positive lexical universes | 1 |
| Absent from Imports / References-Calls / Containment candidates | 31 / 20 / 34 |
| Absent from complete previous evidence union | 1 |
| Exact reusable judgments / new blinded targets | 22 / 12 |

The individual saved lexical absence counts are: canonical BM25 1, BM25+ 1, identifier-aware BM25 1, path-only BM25 20, and RRF 1. These are candidate-reach measurements. The mechanics run took roughly 160 seconds on the local Windows workspace, including historical parent materialization and corpus validation; this is an execution observation, not a comparative benchmark.

Of the 22 exactly reused judgments, 16 are USEFUL and six NOT_USEFUL; none is UNJUDGED. The 12 new pairs occurred in eight development cases. Adjudication used only the verified neutral input, which contains frozen InformationNeed purpose/query, parent snapshot, opaque identities, resource address, and parent-snapshot content. It excludes origin, direction, path support, method membership, ranks, scores, changed paths, and judgments. All 12 decisions were frozen and validated before joining candidate origins.

| Artifact | Content identity | File SHA-256 |
| --- | --- | --- |
| `mirrored_test_paths_freeze.json` | `e05fd19e2ccba9c62a08e68d73cdf833614813b86812ed2119b2c441849a1a53` | `0ad914122b0d45343746b3897968d110c06abf6a73e5f95c6874eefb5e26b709` |
| `mirrored_test_paths_candidates.json` | `7c4e6d924ab5a12477746629a74470dba82281a55e22b950b2126980701113d7` | `73c1358f459f963f58861f1be292e09e81cd51a37a86fa1db474d8e0c71c4b1b` |
| `mirrored_test_paths_judgment_freeze.json` | `4125ed95d7750565e8ff001250e5fbcbf62f32baa5512325d03ceab297164ce6` | `37f49d6bc209088269cc1b8550eda4e00e7d7992aa524dd95b7197e33f853463` |
| `mirrored_test_paths_blinded_judgment_input.json` | `64fb7e675d6d7d0b28e72af7ef5adb1a7bc20bfc384cf21dc5a781c1a5eb85d8` | `968a8d32cfe852252a4a2fdeb2906059f4200e700829ddb02dd5ce9f39d296e3` |
| `mirrored_test_paths_frozen_judgments.json` | `1e603bdaa614b58474f7796e7c80ad732fa806a9bb9ae0ec95475c243aff0799` | `bd432eae57c5ddbfce5d221d6df2e4103c67be4538e88dd8810985bbbd76b190` |
| `mirrored_test_paths_development_results.json` | `f1def496ea7745070d6078d5768f57ad7d529270abbe717d36861e8b5b3feed7` | `ed1f7c9de463ef08d576adbd082fc134a60132b2a8c9a6bd73dd521d59ee67a1` |

## Completed blinded development result

| Surface | Pairs | USEFUL | NOT_USEFUL | UNJUDGED |
| --- | ---: | ---: | ---: | ---: |
| Complete mirrored-path surface | 34 | 21 | 13 | 0 |
| Exact reused judgments | 22 | 16 | 6 | 0 |
| New blinded judgments | 12 | 5 | 7 | 0 |
| Source-to-test projection | 18 | 13 | 5 | 0 |
| Test-to-source projection | 16 | 8 | 8 | 0 |
| Outside canonical top five | 34 | 21 | 13 | 0 |
| Absent from all five saved positive lexical universes | 1 | 0 | 1 | 0 |
| Absent from Imports candidates | 31 | 20 | 11 | 0 |
| Absent from References/Calls candidates | 20 | 12 | 8 | 0 |
| Absent from Containment candidates | 34 | 21 | 13 | 0 |
| Absent from complete prior evidence union | 1 | 0 | 1 | 0 |

**Breadth verdict:** the exact mirrored-path rule exposed one candidate outside the complete saved lexical/import/References-Calls/Containment union, but that candidate was NOT_USEFUL. It found 21 useful candidates overall, all already reachable through at least one saved positive lexical method. This baseline therefore established candidate reach but did **not** demonstrate useful complementary reach beyond the accumulated evidence surface. The result does not justify tuning or adding another Tests variant during this breadth pass. Directional counts describe this workload only and do not establish a preferred projection.

## Interpretation and next boundary

The path convention is an observed, narrow repository cue, not a production `TESTS`, `EXERCISES`, `COVERS`, or `VALIDATES` relation. Retrieval usefulness does not strengthen its semantics. A stronger verified code/test relation might later help Context compilation select behavioral examples, assertion spans, or pointers for progressive disclosure; that remains **plausible but untested**.

Increment 31 again uses the same development-case binding, exact pair identity and prior-judgment reuse, three-state usefulness semantics, neutral input, target validation, artifact identities, frozen judgment validation, and outcome join found in Increments 29 and 30. Path matching, direction, provenance, and prior-surface comparison remain family-specific. The repeated core is now sufficiently stable to **reconsider a small experiment-local extraction** before Configuration/Registration; no refactor was made here.

This result is limited to 24 historical development InformationNeeds, exact path matches in this repository, and a resource-candidate surface without fixed-budget ranking or downstream Context measurement. Prior judgments were gathered for other frozen candidate populations. No held-out confirmation was executed.

**Next step:** one bounded inspection/design prompt for the smallest justified experiment/evaluation extraction, followed immediately by Configuration/Registration. Richer Tests semantics remain parked.
