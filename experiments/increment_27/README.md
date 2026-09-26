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

### Frozen top-five development analysis

The frozen 58 reused and 133 new judgments were joined to the saved five-method
top-five pool only after source hashes, content identities, the exact 191-pair
union, and the 24-development/14-held-out boundary were checked. The
deterministic `lexical_top5_development_results.json` retains each pair's
three-state judgment, provenance, and native method ranks, plus source bindings
and aggregate, pairwise, agreement, case, fusion, and depth diagnostics. No
ranking or judgment was recomputed. Its content identity is
`ecbe17480a250cd8ab2e14f67ebdc81e6ac8ca5f8ca979f98109ad2941feb2df`.

The 191-pair union contains 104 USEFUL, 81 NOT_USEFUL, and 6 UNJUDGED
resources across case/resource pairs. Twenty of 24 cases have at least one
USEFUL union resource. Per-method top-five exposure is:

| Method | Occurrences | USEFUL | NOT_USEFUL | UNJUDGED | Cases with USEFUL | Useful among binary judgments |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| Canonical BM25 | 120 | 63 | 52 | 5 | 19 | 63/115 |
| BM25+ | 120 | 63 | 52 | 5 | 19 | 63/115 |
| Identifier-aware BM25 | 120 | 68 | 46 | 6 | 20 | 68/114 |
| Path-only BM25 | 48 | 31 | 16 | 1 | 10 | 31/47 |
| RRF | 120 | 74 | 41 | 5 | 20 | 74/115 |

These fractions describe judged binary outcomes within each frozen candidate
surface. They do not measure exhaustive corpus recall or task success.
Twenty-six useful pairs occur in exactly one method's top five; 18 in two,
12 in three, 39 in four, and 9 in all five. Nine of ten all-five pairs are
USEFUL, but the useful fraction is not monotonic across agreement levels.
Agreement is evidence to inspect, not a universal relevance score.

BM25+ changes top-five membership by two pairs on each side of canonical, but
exposes no additional USEFUL pair; both methods expose the same 63 useful
pairs. Identifier-aware BM25 exposes 16 useful pairs absent from canonical top
five, including six unique to identifier top five across all methods. Path-only
BM25 exposes 21 useful pairs absent from canonical top five, including 14
unique to path top five; its 28 method-exclusive pairs also contain 14
NOT_USEFUL outcomes. Thus path evidence is not merely weak overlap. It has
48 top-five occurrences in 12 cases, with useful results in ten of them.

RRF exposes 74 useful top-five pairs: 21 absent from canonical top five, 17
absent from identifier top five, and 11 absent from both. Six useful RRF
top-five pairs are outside *all three* input top-five surfaces. Each of those
six is present deeper in at least one positive input ranking. RRF changes
ordering and capacity exposure; it does not generate a resource outside its
input rankings.

The full union's 20-case useful coverage exceeds canonical's 19 cases by one:
`i25-739c82bd3398` has useful identifier and RRF candidates but no useful
canonical top-five candidate. Identifier alone and RRF alone each cover all
20 union-covered cases on this development sample, but expose only 68 and 74
of the union's 104 useful pairs respectively. Four cases have no USEFUL pair
in any tested top-five surface. These observed one-method subsets are not
production selections.

All 41 useful union pairs absent from canonical top five nevertheless have a
positive canonical rank: 35 at ranks 6–50 and six beyond rank 50; the range is
6–97. This distinguishes shallow ranking/capacity loss from lexical
unreachability for this *judged union*. The earlier Phase-0 depth result used
only 49 prior-known useful pairs and therefore has a different judgment
denominator. Its broader K curve and this fully judged top-five union both
show strong depth effects. Neither exhaustively labels the repository.

Increment 25's confirmed five useful structural additions with no positive
lexical rank remain valid evidence for that typed imported-member family;
this lexical-only top-five result does not invalidate them. Increment 26's
eight useful semantic-only top-five development resources were all reachable
deeper lexically, consistent with the ranking-depth pattern observed here.
Its confirmation remains suspended. No structural or semantic score was
combined with these lexical scores.

On this development sample, the tested cheap mechanisms provide useful
top-five *resource* complementarity, while only identifier and RRF add
case-level coverage over canonical. BM25+ is largely redundant here. The
remaining observed whole-resource lexical problem is chiefly early ordering
and five-resource capacity within the judged union; broad candidate-generation
failure outside that union remains unresolved. The next bounded scientific
step was a preregistered **retrieval-unit ablation** over the same development
population, comparing whole-resource retrieval with deterministic fixed-window
lexical units projected back to resource candidates.
It should preserve the retrieval-unit/disclosure-unit distinction and freeze
its configuration before any new outcomes. More BM25 formula tuning, the
971-pair deep adjudication, production promotion, and sealed confirmation are
not justified by this development analysis alone.

## Retrieval-unit ablation: frozen candidate checkpoint

This experiment isolates the **content scoring unit**. It asks whether bounded
source windows improve shallow useful-resource exposure over whole resources
by reducing length and topic dilution. The control is the saved canonical
whole-resource ranking, checked against the separately saved Phase-2 canonical
scores and order. Both arms use the same 24 development InformationNeeds,
frozen lexical queries, parent-snapshot corpora, canonical Unicode word-span
casefold analysis, BM25 arithmetic (`k1=1.2`, `b=0.75`), resource-level
filename-stem BM25 and `0.25` filename coefficient, positive results, and
five-resource capacity. Window content scores use windows as the BM25 document
universe; the strongest positive window score per resource is added to the
unchanged filename score. Corpus order breaks resource ties and the earliest
window breaks exact within-resource content-score ties.

The representation contract was written to `window_unit_freeze.json` before
new retrieval or usefulness reuse. A window holds at most 256 canonical
lexical content tokens, advances 224 tokens, and overlaps its predecessor by
32. The last nonempty partial window is retained. A short resource gets one
window; resources with no lexical token get zero content windows and can still
match through the filename field. Every source character is covered by the
retained window spans when the resource has lexical tokens. Window identity
binds parent snapshot, resource address, ordinal, and half-open token and
character spans. The winning window's span, source text, hash, native score,
and per-term contributions are retained as **retrieval evidence**; the
candidate remains the parent-snapshot resource address. A window is neither
Repository Intelligence nor a Context disclosure unit.

This single setting was selected before outcome joins. In a mechanical count
of current `src/` and `tests/` Python files, median canonical lexical length
was 251 tokens, and 165 of 333 files exceeded 256 tokens. A 256-token cap
therefore leaves many small files intact while splitting longer ones; 32-token
overlap limits boundary loss at modest duplication cost. Byte or line windows
would make lexical lengths incomparable; declaration units would introduce
parsing and a different hypothesis. Nonoverlapping windows would make
boundary placement unusually influential. These observations motivate one
falsifiable control, not an outcome-tuned window-size sweep.

The development execution produced 13,908 content windows across 24
historical corpora. The complete positive resource set matched the canonical
set case by case (1,942 positive resource occurrences in each arm), as
expected with unchanged query terms and lexical tokenization. At equal
top-five resource capacity, the arms share 90 pairs, with 30 whole-resource
only and 30 window-only pairs. All 30 window-only top-five resources have a
deeper positive whole-resource rank. This is **candidate-surface mechanics
only**; usefulness of newly exposed resources has not been judged. The unit
change reorders lexically reachable resources rather than making unmatched
lexical resources positive.

The equal-capacity union is 150 neutral case/resource pairs. Exact
InformationNeed, parent-snapshot, resource-address, and usefulness-semantics
identity permits 138 previously frozen judgments to be reused. The other 12
pairs are in `window_unit_blinded_judgment_input.json`, containing only neutral
case/resource identities, frozen purpose and query, parent snapshot, address,
and exact parent-snapshot source content. It contains no origin, rank, score,
window, overlap, or prior outcome fields. At this candidate checkpoint the 12
pairs had **no judgment**. Arm usefulness was compared only after their blind
judgments were completed and frozen, as recorded below.

Artifacts and identities:

- `window_unit_freeze.json`: contract identity
  `bfb805bcc124b5eef9cf27cb44905287cfef41a108fd903864024ad781eb8a62`.
- `window_resource_rankings.json`: complete positive development ranking identity
  `9d813083ef7370dd8f895ba8e7bc61c61078962497a6cbecec5d42198cbd6520`.
- `window_unit_pool.json`: candidate union and exact reuse identity
  `50b7523ddcf890c8c1df832908929d0d208ec347bf18164b8f4ad9f9f1832132`.
- `window_unit_blinded_judgment_input.json`: new neutral input identity
  `ae238e965b8278ed788f24ff93c21354bb167bfd7d0de2c9381d125fb20ce28c`.

The 14 Increment-27 held-out cases have no window rankings or judgment pool.
The suspended Increment-26 confirmation and Phase-1 971-pair deep adjudication
remain untouched. This ablation does not test declarations, AST units,
semantic chunks, structural retrieval, learned ranking, Context disclosure,
or production chunk storage.

### Blinded judgments and completed development result

The 12 new neutral pairs were adjudicated from the committed blind input only:
3 USEFUL, 8 NOT_USEFUL, and 1 UNJUDGED. The UNJUDGED pair has a truncated
InformationNeed of only “ed evidence”; its usefulness cannot be decided from
the exposed purpose. Each new label has a content-grounded rationale. The
frozen artifact `window_unit_frozen_judgments.json` binds the exact input file
hash, neutral 12-pair population, retrieval-unit freeze, and three-state
semantics. Its content identity is
`ec4bdbb83c2c9bea2b87e513ee87b5a5a8ead769d4d161364c5c599ba254c01d`.
No retrieval origin was joined until this artifact passed validation.

The subsequent deterministic result artifact joined those 12 labels with 138
exactly reused judgments, without rerunning retrieval or changing labels.
The 150-pair union contains 75 USEFUL, 68 NOT_USEFUL, and 7 UNJUDGED pairs.
At equal top-five **resource** capacity:

| Surface | Candidates | USEFUL | NOT_USEFUL | UNJUDGED |
| --- | ---: | ---: | ---: | ---: |
| Whole resource | 120 | 63 | 52 | 5 |
| Fixed window | 120 | 64 | 50 | 6 |
| Both | 90 | 52 | 34 | 4 |
| Whole resource only | 30 | 11 | 18 | 1 |
| Window only | 30 | 12 | 16 | 2 |

Windowing changed top-five usefulness by **one net useful resource**. Its
useful count was higher in seven cases, lower in six, and equal in eleven.
Whole-resource scoring found at least one useful top-five resource in 19 of
24 cases; windowing did so in 20. It recovered one case with no useful
whole-resource top-five candidate and lost no such covered case.

Every window-only top-five resource, including all 12 useful ones, already
had a positive whole-resource lexical rank. The useful additions' canonical
ranks were 6–22. Thus this is a **small useful incremental ranking
improvement** in this development sample, not a new positive lexical
candidate-coverage capability. The unit change promoted deeper canonical
candidates into shallow capacity. Its 30 changed candidate identities should
not be mistaken for 30 new useful resources or broad task gains.

The result is descriptive for 24 historical devtools cases, one fixed window
setting, one query view, and five-resource capacity. UNJUDGED remains distinct
from NOT_USEFUL. It does not establish statistical generalization, production
benefit, independent-repository behavior, or Context disclosure quality.
The held-out Increment-27 population and suspended Increment-26 confirmation
remain sealed. No window-size or overlap tuning follows from this result.
The **lexical-window retrieval-unit branch is complete and closed**.

`window_unit_development_results.json` retains all per-case and per-surface
three-state counts, source bindings, and the canonical reachability of window
additions. Its content identity is
`32b46ea33c7f0a3110342a87e6e535cd3507cd83a681855543e58b31cdee5999`.

## Direct module-import structural candidate and judgment-cost gate

This next development-only slice consumes the existing directed,
declaration-grounded `PythonResolvedModuleImportRelation`. The frozen primary
seeds are exactly the saved first five positive canonical lexical resources for
each of the 24 previously executed development InformationNeeds. An outgoing
path projects the uniquely resolved target module to its resource; an incoming
path uses a reverse lookup of an independently established directed relation
and projects its importer resource. Each candidate path contains exactly one
resolved relation. The arms remain separate, exclude seed resources, and retain
every declaration/resolution/relation support after resource deduplication.
There is no general graph traversal or new Repository Intelligence.

The outcome-blind protocol was persisted to `structural_import_freeze.json`
before derivation (content identity
`b1e73fcf79f1bbf0e75a83b71822550352ce208107efc61ad5dab5001edc7dda`).
The complete candidate mechanics were then persisted as exact canonical UTF-8
JSON inside `structural_import_candidates.json.gz` (content identity
`f9a78024a0be52af56dc5d676794f4dba2f52ca90a6c0454644d113bb34f09a0`).
The original 42,265,900 JSON bytes have SHA-256
`f42215df4ab75455f8a6fc5993993d81093f411b0835f449afe9ece16d6551b5`.
Deterministic `gzip.compress` with `compresslevel=9` and `mtime=0` stores those
exact bytes in 4,574,038 bytes (compressed SHA-256
`bfc399e1ecf8315c6ec9e12bf5f900b8766e697def5eb8e5f07b21bb699afb68`).
Decompression, raw-byte identity, and candidate content identity are checked
when the artifact is read.
It retains source-level import-resolution qualifications, seed interpretation
status, all candidate paths and support, per-direction branching, saved lexical
reachability, and same-volume lexical controls. It contains no usefulness
judgments. Only after this artifact was frozen did the exact-label reuse audit
write `structural_import_judgment_cost.json` (content identity
`ae7ea932dea5278e980cfe0a567132be5b437cc8e07457307905bfb11fada71a`).

Across 120 saved seed slots, 79 were eligible module interpretations and 41
were non-Python resources. The derivation examined 40,412 direct import alias
occurrences across the 24 parent-snapshot corpora, with 24,963 uniquely
resolved module relations and 15,449 unresolved-in-universe outcomes. These
are corpus-wide work counts, not retrieval candidates. The outgoing arm had
511 one-relation paths from seeds and 99 unique non-seed resource additions;
the incoming arm had 165 paths and 23 additions. The arms overlap on 13
case/resource pairs, making a 109-pair structural union. No case produced more
than eight outgoing or four incoming additions. Path multiplicity is material:
outgoing retained 499 non-seed supports and incoming retained 153, with all
supports preserved on their deduplicated candidates.

All additions are outside the canonical top five because the seed resources
are excluded. Outgoing has 36 candidates with deeper positive canonical ranks
and 63 with no positive canonical rank. Incoming has 16 and seven respectively.
The structural union has 66 distinct candidates without a positive canonical
rank. Of those, 54 also lack a positive rank in **every** saved lexical
universe (canonical, BM25+, identifier, path, and RRF). These are
candidate-mechanics categories, not usefulness outcomes. Each direction's
same-volume control adds the next `m` canonical positive resources: 99 outgoing
control occurrences and 23 incoming, with no lexical-exhaustion case.

Exact reuse of the already frozen Increment-25/26/27 judgments covers 14 of
the 109 structural union pairs; **95 pairs require new blinded judgments**
before usefulness can be compared. The outgoing count is 10 reused / 89 new
of 99; incoming is 10 reused / 13 new of 23. The canonical-zero union is two
reused / 64 new of 66. All 54 candidates absent from every saved positive
lexical universe lack a prior judgment and require first-time adjudication.
The same-volume lexical controls contain 52 reused / 49 new distinct pairs in
their 101-pair union. Existing
`UNJUDGED` remains a third state; no new labels were assigned. The cost
artifact lists counts by case and direction without comparing label outcomes.

The pre-adjudication checkpoint freezes one exact population in
`structural_import_judgment_freeze.json` (content identity
`30396777d0f0e719a5c717a47697f83fa9f0ea7cd6a18c3d650da7d33d64439e`,
file SHA-256
`a28d079344f85ecd0a79dbc50fdca2a336f1f80f4ee72cd9798dc6486b4416ee`).
Its hidden evidence retains origin membership, all structural supports, five
saved lexical ranks, exact three-state judgment reuse, and source hashes. Of
the 95 new structural pairs and 49 new control pairs, four overlap, leaving
**140 distinct new judgments**. The separate human input,
`comparison_blinded_judgment_input.json` (content identity
`90213a1d9dc7370559313a425a593208ba5c71e523a78fd71753beab8d905fe3`,
file SHA-256
`1114ff4d1b45edfac8178744e29640763ff1cc2c8cd5804e80dc67351694a26f`),
contains only opaque case/resource identities, frozen InformationNeed text,
parent snapshot identity, resource address, and exact parent-snapshot content.
It contains no origin metadata or usefulness outcome.

The 109 structural candidates and 54 absent from every saved positive lexical
universe establish **candidate novelty only**. Whether any new candidate is
useful, or contributes useful resources beyond same-volume canonical lexical
widening, remains unknown. The 14 Increment-27 held-out confirmation cases and
suspended Increment-26 confirmation remain sealed and unexecuted in this step.
The next bounded step is blinded adjudication of exactly the frozen 140 pairs;
no usefulness comparison is permitted before those labels are frozen.

## Blinded comparison judgments

The neutral input contained 140 new targets across 23 nonempty development
case records. The remaining development case, `i25-c0fabcb195e2`, had zero
new targets after exact judgment reuse and pair deduplication; no empty case
record was added. Every neutral target received one purpose-relative judgment
and a concise usefulness rationale: 41 `USEFUL`, 68 `NOT_USEFUL`, and 31
`UNJUDGED`. The three states remain distinct.

The frozen `comparison_frozen_judgments.json` has content identity
`4e7394f0c2cfa8079f5e0b8b06506834046c3035856f6ab8db8c92b21efadea2`
and file SHA-256
`08cf1c7e05e1299fbb76eaa956657cb625852765fa446009c3cc06c47a9f6383`.
It binds to the exact neutral input identity and byte hash. Judgments were
completed and frozen before any retrieval-origin join. Method-level results
remain unknown, and held-out confirmation remains sealed.

## Direct-import development comparison

After the 140 neutral judgments were frozen, the development-only join matched
them and 61 exact prior judgments to the persisted structural candidates and
same-volume deeper canonical lexical controls. No label was changed, and no
retrieval was rerun. The joined union contains 201 distinct case/resource
pairs. `USEFUL`, `NOT_USEFUL`, and `UNJUDGED` remain separate; the rate below
uses only the first two states as its denominator.

| Surface | Candidates | USEFUL | NOT_USEFUL | UNJUDGED | Useful / judged |
| --- | ---: | ---: | ---: | ---: | ---: |
| Structural union | 109 | 38 | 51 | 20 | 42.7% |
| Outgoing additions | 99 | 31 | 49 | 19 | 38.8% |
| Incoming additions | 23 | 17 | 5 | 1 | 77.3% |
| Structural, canonical rank > 5 | 43 | 23 | 15 | 5 | 60.5% |
| Structural, no positive canonical rank | 66 | 15 | 36 | 15 | 29.4% |
| Structural, absent from all five saved positive lexical universes | 54 | 11 | 31 | 12 | 26.2% |
| Same-volume lexical-control union | 101 | 38 | 50 | 13 | 43.2% |

The outgoing and incoming arms overlap on 13 pairs, including ten useful
pairs, so their counts must not be added to obtain the structural union. The
separate controls match each arm's candidate volume; deduplication leaves 109
structural pairs and 101 distinct control pairs. Structural and control unions
each contain 38 useful resources. Eighteen cases have a useful structural
addition and seventeen have a useful control addition. Four cases have useful
structure but no useful control, three have useful control but no useful
structure, fourteen have both, and three have neither. These descriptive
counts do not establish general statistical superiority.

Among the 38 useful structural pairs, 23 have a deeper positive canonical
rank, four have no positive canonical rank but appear in another saved
positive lexical method, and **eleven are absent from all five saved positive
lexical universes**. Those eleven span nine development cases (ten outgoing,
one incoming). Direct import structure therefore demonstrated useful
candidate reach beyond the five saved lexical retrieval universes on
Increment-27 development. It also recovered useful resources already
lexically reachable at greater depth. Candidate novelty alone would not have
established either usefulness result.

The 31 newly blinded `UNJUDGED` targets remain unresolved. Across the joined
surfaces, 20 structural and 13 control pairs are `UNJUDGED`; 12 of the 54
structural pairs absent from all five lexical universes are `UNJUDGED`. Their
usefulness is unknown. This limits rate comparisons, though it does not erase
the eleven observed useful cases of lexical-universe escape. The evidence
supports retaining directed import relationships as experimental candidate
evidence and testing combination later; it does not specify a ranking or
Context-disclosure policy or justify production promotion.

`structural_import_development_results.json` binds the candidate, lexical,
population, neutral input, and judgment evidence and retains the exact joined
pairs, useful addresses, per-case counts, reach partitions, and unknown-state
accounting. Its content identity is
`c1f70f19210e06e04d52ffff31ab9f0e58be950b73e5f4d8721765dc276600eb`;
its file SHA-256 is
`21d1bd3a3935c1a400d266bdd19538f59d90b11a541f4af331a6210fc7dbafcf`.
The Increment-27 held-out population and suspended Increment-26 confirmation
remain sealed. A subsequent scientific decision may test a bounded combination
of lexical and import evidence before any authorized confirmation.
