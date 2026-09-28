# Increment 33: structural expansion round two (Graph-2)

**State: completed development breadth baseline using one prospectively frozen probability sample.** Candidate mechanics, sampling, blinded decisions, and the development result are frozen. Confirmation remains sealed.

## Question and protocol

Graph-2 asks whether **one** additional structural edge from every frozen novel Graph-1 candidate exposes useful repository resources beyond the complete direct evidence union and Graph-1. A full path is ordinarily three structural edges from a canonical lexical top-five seed. The frontier is all 704 frozen Graph-1 case/resource candidates, independent of judgments, path multiplicity, relation type, lexical rank, or apparent quality. The third edge is derived from parent-snapshot relation facts for arbitrary frontier resources. Saved candidate lists are not used as adjacency lists. The 24 development cases, queries, InformationNeeds, source artifacts, and parent snapshots are bound by `graph_round_two_freeze.json` before outcome access.

The third edge uses exactly the four existing bounded relation families: uniquely resolved declaration-grounded direct Imports in both directions; bounded References in both directions with direct Call retained as a specialization on one occurrence; immediate package membership in both directions; and exact mirrored source/test path correspondence in both directions. Mirroring asserts a path match only. No edge claims runtime import execution, test coverage, or validation. Nothing recursively expands a Graph-2 result. No pruning, score, weighting, ranking, relation registry, or graph framework is present.

Candidate identity is one exact InformationNeed/query, case, parent snapshot, and resource identity under established usefulness semantics. The complete prior exclusion surface per case is all five saved positive lexical universes, four direct structural candidate families, and every frozen novel Graph-1 candidate. Third-edge landings are classified as original seed, other direct evidence, Graph-1, or new Graph-2. Only new Graph-2 landings enter the judgment population. Reversal and rediscovery are measured before exclusion.

## Compact exact support representation

The candidate artifact retains the SHA-256 and content identity of the immutable Graph-1 candidate/path artifact. For each novel third edge, it stores one record keyed by the canonical digest of its source, target, relation family, direction, and **full native support**. A Graph-2 candidate stores its address and the exact IDs of all third-edge records reaching it. Each record's source identifies one frozen Graph-1 candidate; **every** frozen path for that source is crossed with that third edge. This exactly reconstructs each three-edge typed path and all first, second, and third native supports. The digest is an index into retained information, not a replacement for provenance. Exact duplicate third-edge supports collapse; distinct native supports and distinct Graph-1 prefixes remain distinct. The experiment stores no multiplicity score.

This representation reconstructs **85,015** paths supporting novel candidates from a **5,688,965-byte** candidate artifact. It avoids serializing those paths as repeated full objects. The candidate population, typed supports, diagnostics, and lexical comparator were frozen before any usefulness source was opened.

## Frozen outcome-free reach

| Measure | Result |
| --- | ---: |
| Development cases / cases with novel reach | 24 / 22 |
| Graph-1 frontier case/resource pairs / pairs with incident relations | 704 / 704 |
| Raw third-edge supports / exact distinct third edges | 11,208 / 11,208 |
| Projected case/resource pairs before exclusion | 2,084 |
| Original-seed returns / other direct-union overlaps / Graph-1 overlaps | 0 / 598 / 499 |
| New Graph-2 case/resource pairs | **987** |
| Distinct addresses in new pairs | 232 |
| Addresses absent from every earlier development direct/Graph-1 surface | 82 |
| Complete three-edge typed paths / paths to novel pairs | 294,154 / 85,015 |
| Immediate edge-2 reversal paths / direct-frontier return paths | 93,248 / 132,594 |
| Maximum novel candidates per case / original seed | 87 / 70 |
| Maximum distinct neighbors from one Graph-1 frontier resource | 44 |

The 232-address count deduplicates addresses among novel case pairs. Of these, 82 addresses are absent from all earlier development evidence; the other 150 were seen in earlier surfaces for a different case. This global address diagnostic does not replace case/snapshot candidate identity.

| Third-edge relation and direction | Raw supports | Typed paths before novelty exclusion |
| --- | ---: | ---: |
| Import forward / inverse | 4,316 / 3,996 | 120,350 / 120,811 |
| Reference forward / inverse | 812 / 469 | 16,023 / 5,115 |
| Package child→package / package→child | 677 / 585 | 10,078 / 16,979 |
| Mirror source→test / test→source | 133 / 220 | 1,642 / 3,156 |

Leading novel three-edge combinations, counted as typed support paths only, were `import:outgoing → import:forward → import:forward` 35,116; `import:outgoing → import:inverse → import:forward` 11,167; `import:outgoing → import:forward → import:inverse` 5,271; `reference:reverse → import:forward → import:inverse` 5,041; and `import:outgoing → import:inverse → immediate_package:child_to_package` 4,777. Their frequency is not a usefulness signal.

The volume-matched frozen canonical lexical comparator requested 987 rank-six-or-deeper resources and supplied 811; seven cases exhausted. It did not alter Graph-2 candidates.

## Judgment boundary and prospective sample

Only after the candidate artifact froze, exact older **development** judgment reuse covered 2/987 pairs: 0 `USEFUL`, 2 `NOT_USEFUL`, 0 `UNJUDGED`. Neither Graph-1 sampled judgments nor its usefulness-bearing result was opened. The remaining **985** exact candidate identities formed a complete neutral unresolved input, with resource content and InformationNeed but no structural origin, path, direction, multiplicity, rank, score, or prior evidence membership.

Exhaustive adjudication of 985 pairs is disproportionate to the breadth question. Before any new outcome, `graph_round_two_sampling_freeze.json` selected a simple random sample **without replacement** of **128** neutral target identities using `random.Random(330128).sample` on lexicographically sorted `(neutral_case_id, neutral_resource_id)` pairs. It records all 128 selected and 857 unselected identities, the source input identity and SHA-256, and the sampled neutral input identity. The 857 unselected targets have **no** new judgment; they are not adjudicator-returned `UNJUDGED`.

The six pre-adjudication Increment-33 artifacts and the frozen Graph-1 input were verified against their recorded SHA-256 and content identities before review. Each of the 128 sampled targets was judged solely from its frozen neutral InformationNeed, address, and resource content. Each received one of the established three states and a nonblank purpose-relative rationale. The shared judgment-coverage helper verified exact sampled identity coverage, no extra or duplicate target, valid state and rationale, and no overlap with exact reuse. The sampled judgment artifact was written, fingerprinted, and revalidated **before** the development result read candidate provenance. Neither Graph-1 sampled judgments nor its usefulness-bearing result was opened; confirmation remains sealed.

| Outcome population | USEFUL | NOT_USEFUL | UNJUDGED | Total |
| --- | ---: | ---: | ---: | ---: |
| Exact older development reuse | 0 | 2 | 0 | 2 |
| New blinded probability sample | **0** | **128** | **0** | **128** |
| Unsampled, unadjudicated | — | — | — | **857** |

The observed sampled useful fraction is **0/128 = 0%**. A descriptive **95% Wilson score interval**, using the binomial approximation **without finite-population correction**, is **0%–2.91%** for the useful proportion of the 985 frozen unresolved pairs. Sampling was without replacement; this interval is an approximate diagnostic, not a census or a claim about other repositories. The two exact reused `NOT_USEFUL` pairs are outside that sample. No exact total useful count for the 987-pair candidate surface is claimed.

| Frozen artifact | Content identity | SHA-256 |
| --- | --- | --- |
| `graph_round_two_freeze.json` | `d4014605c9d836cbc1885bf0255db9d69bb86919b1aa45bb91a924c025eb8978` | `9e7b3769daa2b0a975a8163f998fcbf9c04808cc88f82b64b464d364e0c1772b` |
| `graph_round_two_candidates.json` | `e2323fb7a9b6a575d0e033e36bab0a2e1695989d9cc2bef6dac223f3edba8858` | `f1b13d1c9b1142fcdd8ba48d2ddf700de684da5570bd28d13fc93aac156b3ace` |
| `graph_round_two_judgment_freeze.json` | `0da845aaa0bc8b86e62bfa04842db30f88c42a8796fef9ea9574531d2e40532d` | `c5309f3c589534be0e87cea5d7750566dcdbe5cc9b92f15d09b1c7b0cf012088` |
| `graph_round_two_blinded_judgment_input.json` | `1a7e028014e15188e0753c839b190b9a8ef9dea9b242d806a591bcc150020779` | `c85d502f109f5075f56a26ee466484d2c49d20b71e51dcd60b18652f3fb691b6` |
| `graph_round_two_sampling_freeze.json` | `716b76e07384f18406febab3b0e6e89c09e1896025bcb1372622ba10e9229e9b` | `230cd6a5b5bba79ecaec31f36d127ee575cedcdfa8d03ef488c04ccd4e4761f6` |
| `graph_round_two_sampled_blinded_judgment_input.json` | `cb2a8977c285df008daf52228cc4e6a0eb5c137c460973d2222b0a5fac66cc86` | `3d66623275ccaf5f8807974b4c805885b9427d44cf0a1f74a00c2a83383f12b7` |
| `graph_round_two_sampled_frozen_judgments.json` | `457e10b91aae0a1b8356f68442e1f656dc1dc9885b37fad8ee8936b412ed754a` | `9d42baf327c549288389355a96e498dea700f4042fff96224a31ae6e77deedd3` |
| `graph_round_two_development_results.json` | `3f033e872efe17a8e4f279b48a112419a9dffc90693751fff07f77ee0d9d5583` | `3e829e22e221ab9a9de2de0f5e481eafbea3df74d66576a84b8f638eda89bc02` |

## Architecture and next step

**Breadth verdict:** Graph-2 composition established substantial independent development reach: 987 case/resource pairs outside every earlier direct and Graph-1 surface, including 82 addresses absent from all earlier development surfaces. No useful candidate was observed among the 128 prospectively sampled unresolved pairs. Thus this baseline **did not establish useful complementary Graph-2 reach**; it does not prove that the full surface has no useful resources. No sampled useful path exists for post-join path-family description. The natural traversal also produced 294,154 complete typed paths, 85,015 paths to novel pairs, 598 direct and 499 Graph-1 overlap pairs, and substantial reversal traffic. These are descriptive cost/noise findings, not ranking evidence. No Graph-2 pruning, weighting, or another sample follows from this result.

Production Repository Intelligence facts remain distinct from candidate projection, typed traversal/composition, observed usefulness, ranking/selection, and Context disclosure. Direct Imports already has production relation ownership. Repeated reconstruction increases production-design pressure for sound bounded References/Calls and immediate package membership; mirrored correspondence remains a weaker narrow fact. Retrieval performance alone does not justify a production graph abstraction. No relation promotion occurs here.

Three-edge provenance could plausibly support future Context compilation through occurrence-backed explanations, short structural summaries, dependency pointers, and progressive disclosure of related resources. This experiment tests file candidate usefulness only. It does not test relevant spans, declaration selection, summaries, synthesized Context, disclosure budgets, or agent task performance. Low sampled file-level usefulness does not settle those Context questions.

Graph-2 is the final planned depth baseline in this Tier-1 breadth sprint. Graph-3, exhaustive graph labeling, pruning, relation weighting, and other depth refinements are parked. **Next breadth step: Structural Union**, using the accumulated frozen structural surfaces with exact candidate identity and typed support retained. No next frontier is selected from partial outcome labels.
