# Increment 27: retrieval foundations, Phases 0–2

Increment 27 tests whether repository retrieval misses come from ranking
depth, lexical representation, path evidence, or complementary inexpensive
retrieval methods. The work is experiment-local and has not changed production
retrieval. It began with one narrow baseline question: for resources already
judged useful, where does the unchanged canonical combined lexical retriever
rank them?

The depth diagnostic runs only the 24 previously executed Increment-25/26
cases. It materializes each historical parent snapshot with the Increment-25
Git snapshot machinery and uses the existing `content BM25 + 0.25 *
filename-stem BM25` retrieval operation without changing query text, scoring,
positive-result filtering, tie ordering, or corpus construction. Complete
positive rankings are retained.

The 14 formerly unused eligible Increment-25 cards are frozen as the held-out
Increment-27 confirmation population. Their parent snapshots and query text
are recorded, but no retrieval is executed and no outcome is included. The
suspended Increment-26 confirmation population remains separately preserved.

Existing usefulness labels are reused before expanding the blinded judgment
pool. A label is attached only when InformationNeed identity (purpose and
frozen query), parent snapshot, resource address, and the established
purpose-relative three-state usefulness semantics match exactly. `UNJUDGED`
remains distinct from `NOT_USEFUL`; no new judgments are generated here.

The K checkpoints (1, 3, 5, 10, 20, 50) report how many already-known useful
judged resources occur within each positive-ranking depth. These are
judged-pool depth diagnostics, not exhaustive repository Recall@K: the pool is
incomplete and cannot establish that unjudged resources are irrelevant or that
all useful repository resources were retrieved.

Artifacts:

- `experiment_freeze.json`: population, snapshots, frozen queries, reuse
  identity, retrieval configuration, checkpoints, and sealing boundary.
- `canonical_positive_lexical_rankings.json`: every positive canonical lexical
  result for each of the 24 development cases.
- `existing_judgment_depth_diagnostics.json`: exact prior labels with ranks,
  explicit positive-result absence, and per-case depth counts.
- `development_depth_summary.json`: aggregate known-useful rank and
  first-useful-case distributions.

Phase 0 tests no retrieval-unit change, identifier splitting, fielded
retrieval, alternative BM25 variant, fusion, structural retrieval, dense
retrieval, learned ranking, or Context disclosure hypothesis. It does not
change the retrieval configuration.

## Phase 0 result

The completed depth diagnostic reused the 120 exact-identity prior judgments
across the 24 development cases: 49 USEFUL, 69 NOT_USEFUL, and 2 UNJUDGED.
Among the known USEFUL pairs, canonical lexical ranking reached 16 by rank 5,
35 by rank 10, 41 by rank 20, and 42 by rank 50; two were ranked beyond 50 and
five had no positive lexical rank. These remain judged-pool diagnostics, not
exhaustive repository recall.

The five zero-overlap lexical misses and the already-demonstrated
Increment-25 structural imported-member recovery are recorded as prior
evidence. No targeted full-path experiment was run during Phase 0.
The two resources ranked beyond 50 remain described by the prior diagnostic
as lexically reachable, with limited query-term overlap and stronger
competing resources as the primary observed explanation.

## Phase 1: pooled lexical judgment population

For each of the same 24 development InformationNeeds, Phase 1 pools resources
at positive canonical lexical ranks 1 through 50, or all positive results
where fewer than 50 exist. This freezes 1,065 distinct case/resource pairs.
The rankings were read from the saved Phase-0 artifact; no retrieval was
executed in this phase.

At the Phase-1 freeze, ninety-four pairs had exact reusable Increment-25/26
judgments: 42 USEFUL, 50 NOT_USEFUL, and 2 UNJUDGED. Those pairs are not sent
for adjudication.
The remaining 971 pairs are new blinded targets, with no usefulness outcomes
assigned. Missing prior labels remain missing and are never treated as
NOT_USEFUL. No Phase-1 usefulness judgment has been performed. The later
Phase-2 lexical comparison is documented separately below.

Adjudication of these 971 pairs is **suspended**. At roughly one to two minutes
per pair, labeling this single-retriever, deep top-50 pool would cost about
16–32 hours before testing whether other inexpensive lexical mechanisms expose
different candidates. The freeze and blinded input remain preserved and may
provide depth judgments later if needed. This change does not revise any
Phase-1 identity or label.

The blind input contains opaque case/resource identities, frozen purpose and
query, parent snapshot identity, resource address, and exact content read from
that parent commit. It omits rank, score, retrieval origin, overlap, changed
paths, post-change content, and judgments of other resources. The 14
Increment-27 confirmation cases remain sealed and have no Phase-1 pool or
outcomes. The suspended Increment-26 confirmation population is untouched.

Eight development cases exhausted their positive lexical rankings before
rank 50. Their pool sizes are 42, 43, 37, 33, 46, 20, 38, and 6; the freeze
records the case-by-case mapping and exact positive-result counts.

Phase-1 artifacts and identities:

- `phase1_population_freeze.json` — content identity
  `44ea9b89baec2e68e11ee3ba476317e7ef65f9c396b965b1bcc38e727cd07642`.
- `phase1_pooled_pairs.json` — pooled-population identity
  `a9d56ba5ce3ddcf5a21411daa0a0d0ea14d3487e33c2cc20408e3bbe2181310d`.
- `phase1_reused_judgments.json` — reuse-map identity
  `0475e11f86a385f5b91c0f5778444cd9c23f63d0d6551e9e6ca2ec3203e47783`.
- `phase1_blinded_judgment_input.json` — new population identity
  `b7ccacfe76990cfab5ad0f17b70886ca5d9c4d8fc8e4c88f03b2d8ddb00f55e2`.

These are development-only population artifacts. Confirmation remains sealed.

## Phase 2: small lexical comparison

The accepted [retrieval landscape research](../../docs/research/repository-retrieval-algorithm-landscape.md)
motivates a narrow comparison of five resource-ranking methods on the **same
24 development cases and parent-snapshot corpora**:

| Method | Change and hypothesis |
| --- | --- |
| Canonical | Reuse the unchanged Phase-0 content BM25 + 0.25 filename-stem BM25 positive ranking. |
| BM25+ | Use `bm25s 0.3.11` BM25+ (`k1=1.2`, `b=0.75`, `delta=0.5`) with the same two fields and coefficient. Test one distinct formula's low-frequency/length behavior. |
| Identifier | Use `bm25s` Lucene BM25 (`k1=1.2`, `b=0.75`) on exact words plus deterministic snake/camel/acronym/digit subtokens in query, content, and filename stem. Test code naming morphology without dropping exact identifiers. |
| Path | Use `bm25s` Lucene BM25 on a separate complete relative-path field with baseline Unicode word spans. Test whether path/module evidence independently reaches resources. |
| RRF | Sum `1/(60+rank)` from positive canonical, identifier, and path rankings. Test cheap candidate complementarity without making native scores commensurate. |

The `bm25s` adapters use pretokenized fields, `float64`, the NumPy backend,
no stemming or stopwords, and all positive ranks. BM25+ assigns background
scores even to nonmatching documents, so a resource is positive only when a
query term actually appears in a contributing field and its combined score is
positive. Corpus order breaks ties. Canonical scores remain those produced by
the existing production operation; they are not recomputed by `bm25s`. The
canonical result is rechecked exactly against the saved Phase-0 order and
score so that its native content and weighted filename components can also be
retained.

This is a fixed hypothesis comparison, not a parameter sweep. The method
specification in `lexical_comparison_freeze.json` is written before new
rankings. `lexical_comparison_rankings.json` is generated without loading
judgments. Only after that complete ranking artifact is persisted does
`lexical_comparison_analysis.json` join the 120 previously frozen labels and
size top-5, top-10, and top-20 prospective neutral pools. Missing labels stay
missing; the reported known-useful depths are incomplete-judgment diagnostics,
not exhaustive Recall@K. No usefulness labels are created or changed.

This slice does not test retrieval-unit ablation, char n-grams, BM25F,
query rewriting, structural/graph evidence, dense or learned retrieval,
Context disclosure, or sealed confirmation. The top-5 union was frozen for
blinded adjudication and is adjudicated below; the larger top-10 and top-20
pool estimates remain prospective and do not imply that those larger pools
should be adjudicated.

### Development mechanics and existing-label diagnostics

The first complete 24-case comparison produced 1,942 positive canonical
resources, 1,942 BM25+ resources, 2,149 identifier resources, 149 path
resources, and 2,152 RRF resources across cases. BM25+ has the same positive
membership as canonical because it uses the same fields and tokens, but its
ordering differs in 18 of the 24 cases. Identifier and path ordering differ
from canonical in 23 and 24 cases, respectively. These are ranking mechanics,
not usefulness outcomes.

For the 49 already-known USEFUL case/resource pairs, positive-rank exposure is:

| Method | K=1 | K=3 | K=5 | K=10 | K=20 | K=50 | No positive rank |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| Canonical | 2 | 9 | 16 | 35 | 41 | 42 | 5 |
| BM25+ | 2 | 9 | 16 | 35 | 41 | 42 | 5 |
| Identifier | 3 | 10 | 19 | 30 | 43 | 44 | 5 |
| Path | 1 | 5 | 8 | 12 | 24 | 24 | 25 |
| RRF | 3 | 13 | 22 | 35 | 44 | 44 | 4 |

These are observations on incomplete existing judgments. They do not measure
exhaustive Recall@K or justify selecting a winner. Each method's diagnostic
artifact also retains NOT_USEFUL and UNJUDGED exposure, first known-useful
rank per case, and top-K overlap with canonical.

Prospective unions of equally shallow method rankings are:

| Depth per method | Unique pairs | Already judged | New judgments | Estimated new work at 1–2 min/pair |
| ---: | ---: | ---: | ---: | ---: |
| 5 | 191 | 58 | 133 | 2.2–4.4 hours |
| 10 | 332 | 90 | 242 | 4.0–8.1 hours |
| 20 | 573 | 98 | 475 | 7.9–15.8 hours |

The top-5 union covered multiple mechanism-specific candidates for roughly
one-seventh of Phase-1's 971 new labels. This calculation motivated the frozen
top-5 pool described below; it did not select a retrieval method. At the time
of that calculation no new pair had been judged. The later adjudication is
recorded below, and confirmation remains sealed.

### Phase 1 disposition and frozen top-five population

The canonical-BM25 top-50 Phase-1 population remains scientifically valid as a
frozen deep lexical pool. Its four artifacts and identities above are
preserved byte-for-byte, but adjudication is suspended. The top-five union
across the completed lexical comparison is being evaluated first because it
provides a more diverse comparison surface per new human judgment: 191 pooled
pairs require 133 new judgments, compared with 971 in the suspended Phase-1
pool. Deeper adjudication may be resumed later if the shallow results leave
the retrieval-depth question unresolved.

The new pool uses persisted top-five rankings from exactly these frozen
methods: canonical BM25, BM25+, identifier-aware BM25, path-only BM25, and
RRF. The pair union is 191. Candidate-surface membership counts are: 51 pairs
occur in one method, 33 in two, 27 in three, 70 in four, and 10 in all five.
Each of canonical BM25, BM25+, identifier-aware BM25, and RRF contributes
120 top-five occurrences; path-only BM25 contributes 48 because some saved
rankings have fewer than five positive results. Method-exclusive counts are
0, 1, 14, 28, and 8 respectively in that method order. Pairwise overlap is
recorded in the pooled-pairs artifact. These are candidate-surface counts,
not usefulness results.

Fifty-eight pairs reuse exact prior judgments (28 USEFUL, 29 NOT_USEFUL, and
1 UNJUDGED), each linked to its source artifact hash and source judgment
identity. The other 133 pairs were new neutral blinded targets. At the time
the population was frozen they had no usefulness outcomes. The blinded input
contains all 24 neutral case identities and only the 133 new resources; it
omits method membership, rank, score, retrieval-family evidence, and prior
labels. New resource order is based on opaque neutral identities rather than
ranking.

Top-five freeze and population identities:

- `lexical_top5_judgment_freeze.json` — overall freeze content identity
  `ace8c18e42bc88f1304030c399f29daea66baf26772558ed867244e9dd20ce44`.
- Complete pooled population identity:
  `5095a7dbdd054bdba51c41d9a171ef718151caa05360557e8b702aae46b53390`.
- Reused judgment mapping identity:
  `d7bc881400a2fc475c098f153c94829f23e39257c7bc3a8a857cfacb44cce1b9`.
- New blinded population identity:
  `f2dabd43c8de35b9bc3f9ae4ef5d8d0149849bee6270d9f9744a6f533fc19555`.

The 14 Increment-27 confirmation cases remain sealed. The suspended
Increment-26 confirmation population remains untouched. The pool-construction
pass did not adjudicate targets, calculate new metrics, or execute retrieval.

### Frozen top-five development judgments

All 133 new targets in the frozen top-five blinded population have now been
adjudicated from that neutral input and frozen. The aggregate labels are 76
USEFUL, 52 NOT_USEFUL, and 5 UNJUDGED. The five UNJUDGED outcomes preserve
cases where the exposed task description did not support a defensible binary
decision. Existing reused judgments remain separately frozen.

The judgment artifact is `lexical_top5_frozen_judgments.json`, with content
identity
`4ad2219a71f161c1ed3a7576300e707f0154b5bc8b1732015618b7f44e3e0960`.
Retrieval origins remain unjoined. No method-level usefulness comparison has
yet occurred, and the 14 Increment-27 confirmation cases remain sealed. This
judgment checkpoint does not promote any retrieval method or change production
retrieval.
