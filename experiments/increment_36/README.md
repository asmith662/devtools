# Increment 36: final simple retrieval fusion baseline

**State:** completed one development-only executable combination baseline. The next step is Breadth Synthesis / Production Gate. Confirmation remains sealed.

## Ordering gate and algorithm decision

Frozen canonical BM25, BM25+, identifier-aware BM25, path-only BM25, and the already saved lexical RRF have legitimate rank orders. Pinned Increment-26 CodeRankEmbed has a legitimate top-five resource rank in eight frozen development cases. Increment-35 Structural Union has family membership, direction, native occurrences, typed paths, and round provenance, **but no frozen relevance rank**. Serialization order, address order, path count, and support multiplicity are not structural rankings. No established repository rule combines ranked and unranked binary structural evidence without a new allocation or weighting choice. Structural evidence therefore cannot legitimately enter RRF in this baseline.

The one authorized fallback is **standard Reciprocal Rank Fusion of two ranked modalities**: the frozen Increment-27 lexical RRF ranking as one source and the frozen dense ranking as the other source where available. The repository had already fixed the conventional `k=60` RRF formula, `sum(1/(60 + positive_rank))`. Using the saved lexical RRF as one source avoids counting its canonical, identifier, and path ingredients again; BM25+ is not given an extra correlated vote. No constant, K, weight, source order, or tie rule was tuned against development outcomes. A missing dense list contributes nothing, so the 16 cases without dense results retain exactly the saved lexical RRF order. The tie rule is fused score descending, then frozen lexical RRF rank where present, then address ascending. Only frozen Increment-35 candidates may be selected. The budget is exactly five resources per case.

This is an executable **ranked-input fusion**, not fusion of the complete lexical, structural, and dense surface. It does not claim a structural or graph retrieval contribution. An alternative that admits unranked structural candidates needs a separately justified selection rule and belongs after breadth synthesis.

## Pre-outcome freeze and reproducibility

Run `uv run python -m experiments.increment_36.mechanics` to reconstruct `simple_rank_fusion_freeze.json`. Mechanics reads only frozen outcome-free Increment-27 lexical rankings and canonical case basis plus Increment-26 dense candidate evidence. It verifies the Increment-35 result's SHA-256 as bytes **without decoding its outcome-bearing rows**. The freeze records source hashes/identities, 24 InformationNeeds and parent snapshots, source coverage, the exact algorithm and tie handling, all **2,157** ranked case/resource pairs, their source ranks and RRF scores, and every final K=5 selection. It was written, hashed, and reproduced before the development result opened Increment 35. Freeze content identity: `55c692e49ab7998bae2c865738ad37cbd3f94a811b431dcb58580253e044f744`; SHA-256: `b76d50e630eac938204feed1f218dac35f626ae73a06394c00a513a7b7d99ea2`.

Only after that checkpoint did `uv run python -m experiments.increment_36.analysis` verify the freeze hash, open the frozen Increment-35 inventory, check every ranked and selected candidate against it, and join existing exact development outcomes. The result records the two source artifact identities and hashes, all selected pairs, case results, comparisons, and oracle accounting. Result content identity: `4069ac00507e691283ec705ff1281220c52a5aba18a7dc0e2a6db04948ced148`; SHA-256: `923fdd82a4a1f8a2fbc59b55d1553cc532ecb3ffd58882fb7d92c2c35d0b0c43`. Rebuilding both artifacts is byte-deterministic. No judgment was created or changed.

## K=5 development result

| Frozen executable strategy | Selected pairs | USEFUL | NOT_USEFUL | Returned UNJUDGED | Never adjudicated | Cases with ≥1 useful | Cases with ≥2 useful |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| Canonical BM25 top five | 120 | 63 | 52 | 5 | 0 | 19 | 18 |
| Saved lexical RRF top five | 120 | **74** | 41 | 5 | 0 | 20 | **19** |
| Lexical RRF + available dense RRF | 120 | **73** | 40 | 7 | 0 | 20 | 18 |

Against canonical top five, fusion retains 76 candidate pairs and replaces 44. The replacements add 25 known-useful candidates and displace 15 known-useful canonical candidates, for **+10** net known-useful selections. Ten cases improve, 12 tie, and two worsen on known-useful count. Fusion increases cases with at least one known-useful resource from 19 to 20; it does not increase cases with at least two. Against the already established lexical RRF top five, fusion retains 96 pairs and yields **one fewer** known-useful resource. The 16 cases without dense evidence keep exactly the lexical RRF top five; all eight dense-covered cases change selection.

The non-executable Increment-35 known-useful heterogeneous oracle at K=5 is **99**, versus 63 for canonical. Fusion captures 10 of that 36-resource known-label headroom, or 27.8%; saved lexical RRF captures 11. The oracle counts only known USEFUL labels, leaves unknownness intact, and is neither an executable strategy nor a performance estimate. All 120 selected pairs in this particular frozen baseline happen to have existing labels: 73 USEFUL, 40 NOT_USEFUL, seven adjudicator-returned UNJUDGED. No never-adjudicated candidate was relabeled.

Dense is available in eight cases. There, canonical selects 16 known-useful resources and fusion selects 18, while saved lexical RRF selects 19. In the 16 cases without dense, canonical selects 47 and fusion/lexical RRF select 55. Fusion selects 37 resources that have dense support, including one dense-only resource. That dense-only selection is NOT_USEFUL. No structural-only resource enters top five; one selected resource has Graph-2 provenance but was selected through ranked dense evidence and is NOT_USEFUL. Neither observation is a graph score or structural selection effect.

Outcome-free fusion construction, including reading and hash-checking the frozen rank inputs and building all 24 complete rankings, took about **0.053 seconds** in one local measurement. Candidate generation and embedding inference were not rerun.

## Breadth verdict and production-gate notes

The one established ranked-input combination improves known-useful K=5 yield over canonical BM25 but **does not improve on saved lexical RRF**. The observed dense addition yields one fewer known-useful selection than lexical RRF on the same 24 development cases. It adds no direct evidence about whether the complete structural complement can be selected well, because that surface has no scientifically legitimate frozen rank. The experiment therefore establishes neither a production fusion policy nor a structural ranking architecture. No second fusion method, weight sweep, pruning, or Graph-3 follows in this sprint.

For the production gate, keep deterministic repository facts distinct from retrieval selection: Imports already has production RI ownership; bounded Reference/Call occurrences and immediate package membership remain strong fact-promotion candidates; mirrored path correspondence remains a weak convention fact. Lexical ranked evidence is executable; dense evidence exists for only eight frozen cases; structural candidate reach is substantial but its K=5 selection remains unresolved. Graph traversal and this RRF experiment are retrieval logic, not repository facts. Candidate projection, frozen protocol writing, and one-off sampled judgment machinery should be reviewed for consolidation rather than promoted wholesale.

Weak file-level retrieval performance does not make occurrence-backed RI useless. Future Context compilation must choose which declarations, spans, import/reference/call occurrences, structural chains, summaries, and progressive-disclosure pointers to reveal after relevant resources are identified. This experiment measures only file-resource selection, not disclosure or agent task success.

Across the breadth sprint, population and candidate identity, exact judgment coverage, sampling frame, protocol freeze, metric basis, strategy comparison, and reproducible result semantics recur. These are evidence for a future distinct Evaluation substrate; retrieval owns the meaning of relevance and ranking, Context owns disclosure, and Learning may consume evaluations without owning all evaluation. Synthesis should decide the ownership boundary. This increment creates no reusable Evaluation, Fusion, or Learning framework.

## Limits and next step

These are 24 development cases, with dense candidates frozen for only eight. Unknown labels outside the selected top five remain unknown. Known-useful counts do not show confirmation generalization, optimal fusion, calibrated structural ranking, or production readiness. **Stop executable breadth work here; next is Breadth Synthesis / Production Gate.** Confirmation remains sealed.
