# Increment 34: Structural Union of frozen development evidence

**State:** completed deterministic consolidation. Confirmation remains sealed. The exact next step is Heterogeneous Union.

## Scope and reproduction

Run `uv run python -m experiments.increment_34.analysis` from the repository root. The analysis consumes only frozen development candidate and result artifacts from Increments 27, 29, 30, 31, 32, and 33, plus Increment 27's five positive lexical rankings. It verifies source content identities, rejects confirmation execution flags, preserves the 24 InformationNeeds, queries, snapshots, and canonical lexical top-five seeds, and writes `structural_union_development_results.json` deterministically. The result records every source path, content identity, and SHA-256. Its content identity is `48727589108bcf37d172532c1e1eea8d8640e55642ed99a49716877049244886`; its SHA-256 is `5b3f2957fea3afcd22c09a5b09e5598269ee650a2f488c8dafda4f0f77257774`.

One candidate is one development case, exact InformationNeed/query and usefulness semantics, parent snapshot, and resource address. Family membership is evidence, never candidate multiplicity or a score. The result links each candidate to its fingerprinted native family artifact by family, case, and address. Detailed import declarations, reference occurrences, containment evidence, mirrored paths, and graph path supports stay in those authoritative artifacts. Calls remain a specialization of References, mirrored paths assert only exact observed correspondence, and Graph-1/Graph-2 are traversal-derived candidate surfaces rather than repository relations. No relation is regenerated; no judgment is created.

## Candidate reach and lexical complementarity

| Cumulative surface | Case/resource pairs | Addresses | Cases | Maximum per case | Outside canonical top five | Outside all five positive lexical universes |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| Direct structural union | 225 | 93 | 23 | 17 | 225 | 78 |
| Direct plus Graph-1 | 929 | 234 | 23 | 93 | 929 | 782 |
| Direct plus Graph-1 plus Graph-2 | **1,916** | **340** | **23** | **148** | **1,916** | **1,769** |

The complete surface has 312 distinct addresses represented by these per-case hard lexical escapes, across 22 cases. The direct union has 37 such addresses across 21 cases. Graph-1 adds 704 case/resource pairs beyond the direct union; Graph-2 adds another 987 beyond the direct union and Graph-1. These are additive at candidate identity, not necessarily at address identity across different cases. The six chronological increments add 46, 19, 15, 13, 141, and 106 previously unseen addresses respectively. This is descriptive ordering, not an optimized sequence.

Direct Imports contributes 109 pairs, References/Calls 71, Containment 49, and mirrored paths 34 before deduplication. Exactly 189 direct-union candidates have one family support, 34 have two, and two have three. Pairwise direct overlaps are Imports–References 3, Imports–Containment 20, Imports–mirrored paths 3, References–mirrored paths 14, References–Containment 0, and Containment–mirrored paths 0. Removing one direct family loses 85 Import pairs, 56 Reference/Call pairs, 29 Containment pairs, or 19 mirrored-path pairs. Their lost known-useful counts are 22, 25, 0, and 12. Removing a relation family from graph expansions would change their derivation, so graph rounds are not given a misleading leave-one-family-out interpretation.

| Added family in fixed chronology | New pairs | New addresses | Known-useful new pairs | Known-useful hard lexical escapes | Never adjudicated new pairs |
| --- | ---: | ---: | ---: | ---: | ---: |
| Imports | 109 | 46 | 38 | 11 | 0 |
| References/Calls | 68 | 19 | 33 | 4 | 0 |
| Containment | 29 | 15 | 0 | 0 | 0 |
| Mirrored paths | 19 | 13 | 12 | 0 | 0 |
| Graph-1 | 704 | 141 | 2 | 2 | 574 |
| Graph-2 | 987 | 106 | 0 | 0 | 857 |

## Known usefulness and sampling boundary

Exact development judgments across the six sources have no conflicting labels. The direct union has 83 known `USEFUL`, 122 known `NOT_USEFUL`, and 20 adjudicator-returned `UNJUDGED` pairs. The complete Structural Union has **85 known USEFUL** pairs in 22 cases and 47 distinct addresses; all 85 lie outside canonical top five, and 17 lie outside every saved positive lexical universe. Known-useful family memberships are Imports 38, References/Calls 35, Containment 14, mirrored paths 21, Graph-1 2, and Graph-2 0. Memberships overlap and must not be summed. The complete surface also has 380 known `NOT_USEFUL`, 20 known `UNJUDGED`, and **1,431 never adjudicated** pairs. Never adjudicated means no semantic judgment was returned; it is not `UNJUDGED` and certainly not `NOT_USEFUL`.

Graph-1 has a complete 704-pair novel surface: two exact reused `NOT_USEFUL`, a prospectively sampled 128 with 2 `USEFUL` and 126 `NOT_USEFUL`, and 574 unsampled pairs. Its sample's useful fraction was 1.56%, with a descriptive 95% Wilson interval 0.43%–5.52% for its 702 unresolved frame. Graph-2 has a complete 987-pair novel surface: two exact reused `NOT_USEFUL`, a separate prospectively sampled 128 with 0 `USEFUL` and 128 `NOT_USEFUL`, and 857 unsampled pairs. Its sample's useful fraction was 0%, with a descriptive 95% Wilson interval 0%–2.91% for its 985 unresolved frame. These separate samples have different frozen frames and are not pooled into a universal graph precision estimate. No usefulness is inferred for the 1,431 unsampled pairs.

## Cost and bounded verdict

The direct family surfaces were comparatively bounded: 225 union candidates and at most 17 per case. Graph-1 added 704 novel pairs and retained 10,550 typed paths. Graph-2 added 987 further pairs; its complete three-edge traversal had 294,154 typed paths, 85,015 supporting novel pairs. Import-mediated traversal, including inverse imports, was a major fan-out source. Graph-1's probability sample established sparse useful complementary reach; Graph-2's sample observed none, without proving its whole surface lacks useful resources. Structural evidence as a whole has **17 known-useful hard lexical escapes**, while most of the enlarged graph surface lacks labels and the observed graph samples show low useful fractions. This is a reach and known-usefulness synthesis, not a ranking-performance or precision claim. No pruning, Graph-3, or new adjudication follows here.

## Architecture inventory for the later production gate

**Production RI:** uniquely resolved direct Imports already has production relation ownership. **Strong production-RI candidates:** bounded Reference occurrences with exact spans and direct Call specialization, plus uniquely observed immediate package membership, have been deterministically reconstructed across experiments and can serve uses beyond retrieval. **Weak convention-dependent fact:** exact mirrored source/test path correspondence can be retained as a narrow observed path fact; it does not mean tests, exercises, covers, or validates. **Experiment logic:** candidate projection, graph composition, sampling, usefulness joins, overlap analysis, and ranking comparisons remain retrieval/evaluation work. Repeated reconstruction creates promotion pressure for sound facts, not automatic authority for a universal graph, ranking policy, or production retrieval strategy.

For future Context compilation, Import facts could support dependency summaries and pointers; Reference occurrences could disclose exact supporting spans and uses; Call tags could support bounded caller/callee explanations; Containment could support ownership summaries and parent/child navigation; mirrored paths could provide possible example pointers with weak semantics; and typed paths could explain why a related resource surfaced and enable progressive inspection. All are plausible but **untested as Context compilation**. This increment evaluates file candidate usefulness only, not span selection, summaries, disclosure budgets, or agent task success.

## Evaluation and metrics ownership pressure

Increments 27–34 repeatedly froze case populations, exact candidate and usefulness identities, neutral samples, exact judgment coverage, and outcome artifacts. These are concrete pressure for a reusable **Evaluation** substrate to own assessment identity, coverage, sample provenance, and comparison basis when promotion is authorized. Family candidate derivation, lexical comparison construction, and traversal remain retrieval-specific. A later Learning capability may consume evaluations or train selection models, but the population of development retrieval candidates alone does not make Learning the owner. The existing shared `retrieval_judgment_coverage.py` is a bounded experiment helper, not a mandate for an Evaluation framework now.

The current production lexical retrieval evaluator computes Hit@K, Recall@K, reciprocal rank, and MRR for its bounded retrieval contract. Precision@K and NDCG have not been established here. Metric formulas may later be shared at a lower Evaluation layer if multiple domains actually need the same assessment basis; retrieval still owns which resources, relevance labels, K, ranking, and denominator its measures mean. Learning should not become the default owner of all retrieval metrics. No metrics package or API is introduced in this increment.

## Limits and next step

The 24-case development population is narrow; labels on graph surfaces are sparse and probability sampled; address counts collapse case/snapshot distinctions; the fixed family chronology is descriptive; and path multiplicity is not usefulness evidence. Confirmation remains sealed. The next breadth step is **Heterogeneous Union**, combining the frozen lexical and structural surfaces without inventing new labels.
