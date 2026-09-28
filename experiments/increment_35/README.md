# Increment 35: Heterogeneous Union of frozen development evidence

**State:** completed candidate-ceiling and known-coverage analysis. No retrieval, adjudication, fusion, ranking, selection, or confirmation was run. The next step is one simple established non-learned Fusion test.

## Sources, dense gate, and reproduction

Run `uv run python -m experiments.increment_35.analysis` from the repository root. The deterministic `heterogeneous_union_development_results.json` records every source path, native identity, and SHA-256, plus exact candidate rows, modality membership, known outcomes, per-case headroom, and overlap. Its content identity is `db4a83f891e1549970889276f7f2878d8f5e417020d5b67f378a5f267e1a8337`; its file SHA-256 is `6d00ecc14e6845e3dd1289f9ab52a3b4a1681c3b2c187a37eed3ff2760e6da4f`. Rebuilding reproduces it exactly. Source files are frozen Increment-27 five-method lexical rankings, canonical case basis and development judgments; Increment-34 Structural Union; and Increment-26 dense freeze, candidate evidence, judgments, and development result. No confirmation artifact is opened.

**Dense evidence gate: A — usable frozen development surface.** Increment 26 used pinned `nomic-ai/CodeRankEmbed` revision `3c4b60807d71f79b43f3c4363786d9493691f8b1` to rank resources by maximum similarity from bounded raw-source chunks. Its candidate mechanics were frozen before outcomes, and an independent eight-case CPU replay produced byte-identical candidate evidence. The complete **40 top-five semantic candidate occurrences across eight development cases** have exact existing development labels through the 69-pair neutral semantic/lexical judgment pool. The 40 candidate identities, eight InformationNeeds, parent snapshots, queries, and corpus identities match the current 24-case basis. The other **16 cases have no frozen dense candidate surface**; this analysis does not generate or imply one. Increment-26 confirmation remains sealed.

Candidate identity is the exact case, InformationNeed purpose/query, parent snapshot, resource address, and established usefulness semantics. The five positive lexical universes are canonical BM25, BM25+, identifier-aware BM25, path-only BM25, and rank-only RRF. Lexical rank is retained per method; native scores remain in the fingerprinted ranking artifact. Structural family names link to Increment 34, whose native paths remain in earlier artifacts. Dense rank and native within-model similarity are retained without cross-modality score normalization. A candidate with multiple supports is counted once.

## Candidate volume and known outcomes

Medians include all 24 cases, so dense has median zero; among its eight covered cases its median is five.

| Surface | Pairs | Addresses | Cases | Median/case | Max/case | USEFUL | NOT_USEFUL | UNJUDGED | Never adjudicated |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| Canonical BM25 top five | 120 | 72 | 24 | 5 | 5 | 63 | 52 | 5 | 0 |
| Five-method lexical union | 2,152 | 321 | 24 | 91.5 | 163 | 159 | 170 | 26 | 1,797 |
| Structural Union | 1,916 | 340 | 23 | 85 | 148 | 85 | 380 | 20 | 1,431 |
| Lexical ∪ structural | 3,921 | 460 | 24 | 169 | 232 | 176 | 479 | 38 | 3,228 |
| Eight-case dense surface | 40 | 36 | 8 | 0 | 5 | 18 | 20 | 2 | 0 |
| **Lexical ∪ structural ∪ dense** | **3,922** | **460** | **24** | **169** | **232** | **176** | **480** | **38** | **3,228** |

The lexical candidate universe is highly overlapping: canonical and BM25+ each contain the same 1,942 positive pairs; identifier has 2,149, path-only 149, and RRF 2,152. Exactly 210 lexical-union pairs have two method supports, 1,796 have four, and 146 have five. Pairwise method overlaps are in the result artifact. A positive rank is retrieval evidence, not an adjudicated usefulness label.

| Exclusive modality region | Pairs | Known USEFUL | Known NOT_USEFUL | Returned UNJUDGED | Never adjudicated |
| --- | ---: | ---: | ---: | ---: | ---: |
| Lexical only | 1,979 | 78 | 88 | 16 | 1,797 |
| Structural only | 1,765 | 17 | 305 | 12 | 1,431 |
| Dense only | 1 | 0 | 1 | 0 | 0 |
| Lexical + structural | 138 | 63 | 67 | 8 | 0 |
| Lexical + dense | 26 | 13 | 11 | 2 | 0 |
| Structural + dense | 4 | 0 | 4 | 0 | 0 |
| All three | 9 | 5 | 4 | 0 | 0 |

All exact development labels agree across sources. The complete union contains **176 known-useful case/resource pairs**, 88 distinct useful addresses, across 22 cases. The 3,228 never-adjudicated pairs remain outcome-less, separate from 38 adjudicator-returned `UNJUDGED` pairs. Graph-1 and Graph-2 partial sampling remains exactly as Increment 34 recorded; no unlabeled graph pair is treated as negative.

## Complementarity and known-useful oracle

Structural evidence supplies **17 known-useful pairs outside the complete lexical union**, confirming Increment 34's hard lexical escapes by an independent modality join. They occur in 11 cases and represent 14 distinct addresses. One case gains its first known-useful candidate beyond the complete lexical union. Their family supports are Imports 11, References/Calls 4, Containment 1, and Graph-1 2; these memberships overlap if a pair has multiple supports.

Dense has five pairs outside the complete lexical union, 27 outside Structural Union, and **one** outside lexical ∪ structural. That sole additional pair is known `NOT_USEFUL`. Thus dense adds no known-useful candidate beyond the complete prior union on its eight-case frozen surface. This does not negate its earlier equal-capacity top-five result: eight useful semantic-only top-five pairs were already reachable at deeper positive lexical ranks. Dense has no candidate evidence for the other 16 cases.

A **non-executable known-label oracle** could retain `min(5, known useful candidates)` per case. It yields **99 known-useful resources** across the 24 five-slot surfaces, versus **63** actually known useful in canonical top five. Lexical-only and structural-only known-label ceilings are 95 and 74. Five cases have zero additional known-useful K=5 headroom over canonical, nine have +1, five have +2, three have +3, and two have +4. The result artifact preserves every case's canonical, lexical, structural, heterogeneous, and K=5 counts. This oracle is a lower bound under incomplete labeling, not an executable ranking, expected precision, or achievable policy claim.

## Fusion readiness and architectural implications

**READY for one bounded development-only simple fusion test over existing evidence**, with the eight-case dense scope and outcome gaps stated in advance. Available inputs are each lexical method's rank and native score; Increment-34 structural family membership, direct/Graph-1/Graph-2 origin, and links to native relation/path provenance; and Increment-26 dense rank, similarity, model identity, and winning chunk in its source artifact. Structural families do not carry a calibrated relevance rank; graph path counts are descriptive, not scores. The next experiment must freeze an established allocation/combination rule before inspecting outcomes and must not claim full 24-case dense coverage or complete usefulness labels. This increment defines no rule and performs no fusion.

Heterogeneous overlap changes no production-RI conclusion: Imports already has production ownership; bounded Reference/Call occurrences and immediate package membership remain strong candidates for later RI promotion; mirrored correspondence remains weak and convention-dependent; graph traversal remains derived retrieval logic. Retrieval complementarity does not establish semantic correctness or justify a universal graph.

Heterogeneous retrieval asks **which resources may matter**. Future Context compilation must decide **which facts or spans to disclose and at what fidelity**. Existing lexical matching windows, declaration/reference/call occurrences, import facts, containment, typed paths, exact resource identity, and provenance could support concise explanations and progressive disclosure. This union tests none of those Context outcomes.

The repeated case populations, judgment identities, sampled coverage, reproducible artifacts, and cross-strategy comparisons add evidence for a distinct future Evaluation substrate. Retrieval owns candidate and ranking semantics; Context owns disclosure; Learning may consume evaluations, but does not own all assessment. Existing Hit@K, Recall@K, reciprocal rank, and MRR calculations are retrieval-specific today. If multiple domains need shared metric protocols, a lower Evaluation layer could own assessment mechanics while retrieval supplies its relevance observations, K, ranking, and denominators. Precision@K and NDCG are not implemented or validated here. No reusable framework, metrics package, or Learning package is introduced.

## Limits and next step

This is a 24-case development ceiling, with dense observed on only eight cases and most deep lexical/graph candidates unadjudicated. Regions with known labels are not a probability sample of the full heterogeneous surface. A large candidate ceiling creates a selection problem; it is not retrieval precision. The next step is **one simple established non-learned Fusion baseline**, followed by breadth synthesis and the production gate. Confirmation stays sealed.
