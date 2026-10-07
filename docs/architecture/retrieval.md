# Retrieval foundation: current state and research boundaries

## Authority and scope

This document owns the detailed current Retrieval / Repository Intelligence
(RI) / Localization reconciliation. [Central architecture](../architecture.md)
owns domain boundaries; the [taxonomy](taxonomy.md) owns terminology;
[roadmap](../roadmap.md) owns sequencing; package contracts and source define
implemented behavior. Research and frozen experiments retain historical detail.
Mandatory roadmap experiments are not accepted production algorithms.

`devtools` has a substantial deterministic RI and retrieval foundation, but
lower-level retrieval representation, fielding, query formulation, semantic
mismatch handling, ranking/discrimination, and candidate selection remain
materially underexplored. Neither BM25 plus graph nor the latest Localization
work exhausts that space. Retrieval is not solved; semantic resolution is not
the only major remaining uncertainty.

## Current production inventory

Supported framework code lives under `src/devtools`; retained probes under
`experiments` are not production dependencies. These are callable capabilities,
not a mandatory pipeline or a default fusion policy.

| Capability | Current behavior and owner |
| --- | --- |
| Whole-resource sparse retrieval | [Lexical BM25](../../src/devtools/context/retrieval/lexical/bm25.py): content-only API and canonical content plus filename-stem API; positive matches over caller-selected observed text resources |
| Filename evidence | [Independent filename index](../../src/devtools/context/retrieval/lexical/filename.py), weighted 0.25 in canonical resource scoring |
| Exact addressed and symbolic acquisition | Snapshot resource lookup, [module lookup](../../src/devtools/context/python/modules/lookup.py), [exact declared-name retrieval](../../src/devtools/context/python/function/retrieval.py), native declaration/class/method selection and bounded import/member resolution; not lexical ranking |
| Exact task-anchor grounding | [Localization grounding](../../src/devtools/context/localization/grounding/resolve.py): explicit resource/module/source-declaration/method locators; preserves unsupported, unresolved and ambiguous results |
| Typed structural candidates | [Direct structural retrieval](../../src/devtools/context/retrieval/structural.py): one supplied Imports, References/direct Calls or immediate-package relation in either direction; unranked resource candidates with native support |
| Candidate/evidence union | [Composition](../../src/devtools/context/retrieval/composition.py): snapshot-bound lexical/direct resource inventory, neutral address order, separate native ranks and supports; no fused ranking |
| Query-conditioned graph ranking | [Typed views](../../src/devtools/context/retrieval/graph/view.py) and [PPR](../../src/devtools/context/retrieval/graph/pagerank.py): resource/declaration views over supplied Imports, References, containment and direct bases; optional navigation adds membership/mirrors |
| Repository-map ranking | [Map contract](../../src/devtools/context/retrieval/repository_map/docs/overview.md): query-independent dependency importance, compact symbol/path BM25, symbol RRF, best-symbol resource projection; no map rendering |
| Resource rank fusion | [Fusion](../../src/devtools/context/retrieval/fusion.py): optional equal-channel lexical/PPR or lexical/map RRF, constant 60; preserves native evidence, snapshot/address deduplication and deterministic ties |
| Task and obligation lexical lanes | [Localization lexical adapter](../../src/devtools/context/localization/lexical.py): caller-authored full-task query plus caller-authored obligation queries, separate native rankings |
| Role evidence and routing | [Role evidence](../../src/devtools/context/localization/roles/docs/overview.md) and [routing](../../src/devtools/context/localization/routing/docs/overview.md): positive hints and lossless preferred/escape ordering of obligation lanes; unchanged full-task lane, no semantic satisfaction |
| Structural witness hypotheses | [Generation](../../src/devtools/context/localization/docs/overview.md#bounded-candidate-witness-generation): OWNER_RESOURCE, MIRRORED_RESOURCE, REFERENCING_RESOURCE and DIRECT_IMPORT_DEPENDENCY_RESOURCE; caller-authored recipes, bounded branching/work/results, exact native provenance |
| Witness association and resolution recording | [Localization contract](../../src/devtools/context/localization/docs/overview.md): unresolved competing/complementary candidates, explicit member decisions, explicit complete-support promotion and caller-supplied frame readiness; no automatic semantic decisions |

**Production dense retrieval = none. Production learned sparse retrieval =
none. Production learned ranking / reranking = none. Production BM25F = none.**
Identifier-aware lexical views and CodeRankEmbed remain experimental. The
[external semantic-resolution adapter](../../experiments/codex_dogfood/semantic_resolution/README.md)
is non-production, review-gated proposal infrastructure, not a retrieval model
or an effectiveness result.

RI owns snapshot-local subjects, occurrences, qualified relations and derivation
provenance. Its bounded Python References include direct syntactic Call tags,
not inferred runtime dispatch. Direct bases do not establish an MRO. Mirrors
are path correspondence, not tests/coverage. Static project/test configuration
facts exist but do not establish runtime registration/binding; configuration
targets contribute role evidence, not current graph edges. Exact grounding of
decorated source declarations is distinct from conservative binding resolution.

Candidate generation, evidence composition, ranking fusion and witness
resolution are separate. Direct relation projection can discover nonlexical
resources. PPR can assign mass to graph-reachable resources absent from its
lexical seeds; map ranking can surface global-importance symbols once symbol
lexical relevance is nonempty. RRF unions and reorders its input rankings; it
does not discover resources outside them. Routing changes order, not membership.
No default graph rank, structural insertion rule or universal Selector follows.

## Canonical lexical representation and scoring

The [canonical analyzer](../../src/devtools/context/retrieval/lexical/analysis.py)
matches ordinary Unicode `\w+` spans and case-folds them. It does **not** split
snake_case, camelCase, PascalCase, acronym boundaries or identifier components.
`CandidateMemberResolution` becomes `candidatememberresolution`;
`acquire_localization_lexical_evidence` remains
`acquire_localization_lexical_evidence`. Punctuation separates spans; underscores
remain word characters. There is no stemming, lemmatization, stop-word removal,
character n-gram representation or language-aware identifier decomposition in
this analyzer. Exact Python NAME-token filtering elsewhere is not the BM25
representation.

One [text document](../../src/devtools/context/repository/document.py) represents
one whole observed resource with retained content identity and exact text.
Content flattens code, imports, declarations, docstrings and comments into the
same term stream. These do not have separate content fields/statistics.
Filename evidence uses `PurePosixPath.stem`, excluding directories and extension.

Canonical resource scoring is:

```text
content BM25 + 0.25 × filename-stem BM25
```

The two independently scored representations have independent term frequencies,
document lengths, document frequencies, average lengths and inverted indexes.
Length normalization and saturation occur within each scoring view before score
addition. **This is NOT BM25F.** It does not pool field-normalized term evidence
into a true field-aware sparse formulation.

The [in-repository scoring code](../../src/devtools/context/retrieval/lexical/scoring.py)
uses explicit defaults `k1=1.2`, `b=0.75`, positive IDF
`ln(1 + (N - df + 0.5)/(df + 0.5))`, and ordinary Okapi term saturation.
Lengths count observed tokens; average length includes the indexed documents.
Distinct normalized query terms contribute once, with no query-frequency boost.
Scores are not globally normalized. Positive matches sort by descending score,
then document-collection order; `maximum_results` is caller-supplied, not a
production fixed five. Filename-only matches can enter the candidate set.
Content indexing is explicit over the selected corpus; filename state is built
by the combined retrieval operation. Native results retain query, index,
statistics, term/field evidence and observed source content. Snapshot-bound
composition validates the entire corpus against the supplied snapshot because
even nonreturned documents influence scores. A Git commit is not snapshot identity.

Unsplit identifiers hide concepts that already exist lexically in source. This
is a first-class possible **REPRESENTATION_FAILURE**, not evidence of genuine
vocabulary/semantic mismatch.

## Retained empirical evidence and its limits

The [breadth synthesis](../research/repository-retrieval-breadth-production-gate.md)
owns Increment 25–36 detail: chiefly 24 historical `devtools` development needs,
eight dense cases, incomplete pooled judgments and sampled graph populations.
Counts below are case/resource pairs or top-five occurrences as stated, not
generalized recall or unbiased prospective production-effectiveness claims.
Published imported-member aggregates are retained in
[B-0002](../backlog/epics/B-0002-coding-context-substrate.md); sealed confirmation
artifacts are not needed to use that already published historical summary.

| Mechanism / record | Retained aggregate | Supported interpretation |
| --- | --- | --- |
| [Increment 27 lexical](../../experiments/increment_27/lexical_top5_development_results.json) | Useful@5: canonical 63; BM25+ 63; identifier 68; path 31; lexical RRF 74 | Identifier gains and losses; useful code-specific signal remains unused canonically. Development RRF is a comparator, not promoted default |
| [Fixed lexical windows](../../experiments/increment_27/window_unit_development_results.json) | Useful@5 64 versus whole-resource 63; window-only candidates had positive whole-resource ranks | Weak gain parks that fixed-window formulation, not all semantic granularities |
| Imported-member structural retrieval, Increment 25 | 31 additions, 17 useful, 5 useful with no positive lexical rank | Bounded deterministic resolution can supply lexical escapes |
| [Direct Imports](../../experiments/increment_27/structural_import_development_results.json) | 109 additions, 38 useful, 11 useful outside all five lexical universes | Direct relations can supply complementary reach |
| [References / Calls](../../experiments/increment_29/references_calls_development_results.json) | 71 additions, 35 useful, 4 useful beyond lexical + Imports | Call-tagged direct evidence complemented prior candidates; non-call marginal value not isolated |
| [Package membership](../../experiments/increment_30/package_containment_development_results.json) | 49 additions, 14 useful | Useful candidates, but no useful novelty over the earlier union on this surface |
| [Graph-1](../../experiments/increment_32/graph_round_one_development_results.json) | 704 novel pairs, 10,550 support paths; prospective sample 2 useful / 128 | Poor sampled marginal yield, not full-population precision |
| [Graph-2](../../experiments/increment_33/graph_round_two_development_results.json) | 987 further pairs, 85,015 novel-support paths; prospective sample 0 useful / 128 | More blind depth increased fan-out without sampled useful yield |
| [CodeRankEmbed](../../experiments/increment_26/README.md) | Dense useful 18/40 versus lexical 16/40 | Eight useful dense-only top-five hits had deeper positive lexical ranks; no demonstrated unique useful reach for this formulation |

Identifier evidence motivates additive **whole identifier + identifier subtokens**.
It does not authorize replacing production tokenization now. Placement remains
open: canonical content representation, separate identifier field, separate
lexical view/channel, or an empirically justified hybrid. Representation answers
**what terms exist**; BM25F asks **where terms occur and how field evidence
contributes**. They may be complementary.

Canonical retrieval is whole-resource. Repository-map relevance has compact
symbol metadata, not function/class body retrieval. Function/method/class and
other semantic granularities have not been comprehensively tested. Fixed windows
did not settle retrieval granularity or Context disclosure granularity.

[Case 0002 PPR](../../experiments/graph_ranking_baseline/README.md),
[typed graph](../../experiments/typed_graph_baseline/README.md) and
[map](../../experiments/repository_map_baseline/README.md) diagnostics found plain
resource BM25 had better complete-required depth than every tested PPR/map
formulation and tested fusion in that case (BM25 full/short: 43/87). This is one
retained-case diagnosis, not a universal algorithm comparison. Deterministic
structure is useful knowledge/navigation, but blind expansion and tested global
diffusion/ranking produced much purpose-irrelevant connectivity and have not
earned default retrieval status. Structure is not useless. Direct,
purpose-bounded relations have complementary evidence; blind/deep expansion
has poor marginal precision; global/diffused ranking has not established
superiority over BM25.

The retained CodeRankEmbed formulation was expensive enough not to productionize
and did not establish unique useful reach. **This does not disprove dense
retrieval as a family.** A later dense comparison should preferably target
verified VOCABULARY_SEMANTIC_MISMATCH after stronger code-aware sparse baselines,
without opening sealed confirmation or turning an outcome into a family veto.

## Query representation and candidate discrimination

Current Localization queries are primarily one caller-authored full-task query
plus caller-authored obligation lexical queries, executed largely as supplied.
Automatic identifier extraction, high-information-term extraction,
obligation-to-query formulation, irrelevant-prose removal, synonym/query
expansion, failed-query reformulation, generated alternative lexical views and
relevance feedback are absent. Independently supplied multiple query lanes are
not automatic query formulation. Real Codex instructions can be long,
multi-obligation prompts: query representation is a separate research problem
from document representation.

| Localization development record | Completion / sufficient-set evidence |
| --- | --- |
| [Case 0004](../../experiments/codex_dogfood/case_0004/analysis.md) | Global complete depth 325; maximum own-obligation completion 193 |
| [Case 0005](../../experiments/codex_dogfood/case_0005/analysis.md) | Minimum sufficient union 22; native prefix union 151; routed prefix union 160; maximum own-native 110, own-routed 88 |
| [Case 0008](../../experiments/codex_dogfood/case_0008/analysis.md) | Global completion 361; own completion 177; routed completion 243 |

Lane maxima are not a merged rank. Important tasks often contain a small
sufficient witness set inside a much larger plausible candidate universe.
Candidate ranking/selection/resolution remains serious. These results do **not**
establish that representation, fielding, query formulation or semantic retrieval
are adequate. Multiple failure classes can coexist.

A legitimate future supervised formulation is: given obligation O and candidate
resource R with heterogeneous retrieval evidence, estimate or rank whether R
provides useful evidence for satisfying O. No model is selected. Possible
features include canonical BM25, filename, identifiers/subtokens, BM25F fields,
symbol/exact matches, Import, Reference, Call, containment/package, mirror, role,
obligation-specific rank and generation provenance; retained PPR/map diagnostics
may be features if useful. These are potential evidence inputs, not a feature
schema or trained system.

**UNJUDGED != NOT_USEFUL.** The
[structural union](../../experiments/increment_34/structural_union_development_results.json)
contains 1,916 pairs / 85 known useful / **1,431 never adjudicated**, plus 20
explicit UNJUDGED outcomes. The
[heterogeneous union](../../experiments/increment_35/heterogeneous_union_development_results.json)
contains 3,922 pairs / 176 known useful / **3,228 never adjudicated**, plus 38
explicit UNJUDGED outcomes. These unknown states are distinct, and neither is a
negative label. No supervised retrieval/ranking experiment may use unjudged
examples as negatives without a scientifically justified labeling/sampling
protocol. Historical useful-pool oracles are not executable rankers.

## Retrieval family status and open design space

This is a hypothesis map, not an implementation shopping list. Unexplored
means no retained effectiveness comparison establishes the family here.

| Family | Current status / limits |
| --- | --- |
| Exact / symbolic | Production path, module, declaration, symbol-name and bounded qualified-name/import/member resolution and exact References; scope and ambiguity remain native RI qualifications |
| Classical sparse | Production BM25 and filename score; experimental BM25+, identifier/subtoken, path and lexical RRF. Boolean/TF-IDF vector-space comparisons, character n-grams, query expansion and relevance feedback remain open. **True BM25F is a mandatory experiment**, not production |
| Structural / relational | Production Imports, References/Calls, containment/direct bases, package membership, mirror and bounded Localization projections. Verified test relations, richer inheritance, package relations and configuration/registration/binding retrieval remain open or require scoped RI prerequisites |
| Graph ranking / expansion | Optional production PPR/map/RRF; weak/negative diagnostic diffusion and sampled deep-expansion evidence; no default improvement earned |
| Dense / semantic | Retained CodeRankEmbed probe; no production model/index. Bi-encoders, exact dense variants and ANN/vector indexes remain open; future effectiveness depends on a justified mismatch protocol |
| Learned sparse | Open/unexplored; no production path |
| Late interaction | Open/unexplored; no production path |
| Reranking / learning-to-rank | Deterministic production rank combination/routing exist; richer purpose-relative deterministic scoring, pointwise, pairwise/listwise learning, RankSVM, LambdaMART/boosted-tree ranking and cross-encoders remain open; supervised execution requires valid labels |
| Fusion | Production native evidence union, fixed content/filename score combination and two resource RRF pairs; experimental lexical/dense rank fusion. Interleaving, other score/rank fusion, evidence-conditioned and learned fusion remain open; complementary signal must precede further comparison |

## Retrieval, Localization, resolution and Context

The [Localization continuity owner](localization.md) records its current status
matrix, Cases 0004–0008, structural-breadth closure and exact reasoning resumption
after the immediate retrieval checkpoints. This retrieval inventory does not
replace that downstream history or imply additional relation breadth is next.

Retrieval/Search acquires or generates candidate evidence. Localization defines
obligation-relative information needs and candidate witness semantics. Semantic
resolution judges whether bounded evidence establishes a task-relative
member/witness claim. These are separate failure surfaces: **semantic resolution
must not compensate for avoidable retrieval representation, fielding or query
defects; stronger retrieval cannot by itself establish semantic witness
sufficiency.** Both research tracks remain necessary.

```text
[PRODUCTION] observed text corpus + snapshot-qualified supplied RI
    explicit query --> resource BM25 ----+--> lexical/direct inventory
    seeds + RI --> direct retrieval ----+
    BM25 + typed RI graph --> PPR ---------> optional BM25/PPR RRF
    query + RI map --> map ranking --------> optional BM25/map RRF
    (native candidate evidence/ranks; no automatic Context selection)

[PRODUCTION] caller task / obligations / explicit queries
    --> Localization lexical adapter --> separate BM25 lanes
    --> optional lossless role routing --> caller witness association
                                                ^
    explicit locators + RI --> exact grounding   |
    --> bounded structural witness generation --+
                                                |
                                                v
                   explicit resolution recording / witness promotion
                   --> caller assessment / frame readiness

[EXPERIMENTAL] bounded external proposal --> human review --> explicit record
[EXPERIMENTAL; EVALUATED] R1 whole identifiers + subtokens (retain separate view)
[EXPERIMENTAL; INSTRUMENTATION] R1.5 exact retrieval/failure diagnostics
[EXPERIMENTAL; DEVELOPMENT COMPLETE, PROSPECTIVE GOLD PENDING] R1.6 BM25 sensitivity
[ROADMAP; NOT EXECUTED] R1.7 query-term discrimination investigation
[MANDATORY ROADMAP; NOT IMPLEMENTED] R2 true BM25F, regardless of R1 outcome

[PRODUCTION, CALLER-DIRECTED] explicit Context choices --> plan
                     --> exact materialization --> rendering / assembly
    (automatic Localization-to-Context handoff is not implemented)
```

The diagram shows available composition, not one automatic executor. Native
results can retain full observed text through their index/snapshot provenance;
retrieval does not itself render model Context. Context owns form/amount,
representation expansion and budgeting. Explicit whole-resource and bounded
Reference/declaration materialization exist; an automatic budgeted planner,
obligation handoff, search controller, elimination and stopping policy do not.

## Governing experiment constraints and unresolved choices

Future protocols must declare their primary [failure class](taxonomy.md#retrieval-and-localization-failure-classes)
before treatment execution. Report representation versus fielding gains
separately. The [two-track roadmap](../roadmap.md#current-sequencing) freezes R1
and unconditional R2, comparison arms, metrics and the reasoning-evaluation pause.
The [R1 experimental view](../../experiments/identifier_sparse/README.md) and
[Case 0009 protocol](../../experiments/codex_dogfood/case_0009/README.md) now
implement and freeze the representation hypothesis. Canonical production
retrieval remains unchanged. [Case 0009 Stage D](../../experiments/codex_dogfood/case_0009/analysis.md)
now evaluates R1 against clean independent gold: **RETAIN AS SEPARATE RETRIEVAL
VIEW**. Both arms reach all 37 REQUIRED cells; global depth improves 342 to 331,
maximum own depth worsens 185 to 231, and union burden falls only 1.9455% (257
to 252). The frozen promotion gates fail; the separate-view criterion passes.
This is one mixed prospective case, not production adoption. **R2 remains
mandatory regardless of this result.** R1.5 now provides reusable experimental
[retrieval diagnostics](../../experiments/retrieval_diagnostics/README.md), with
[all 37 Case 0009 REQUIRED cells](../../experiments/retrieval_diagnostics/case_0009.md)
replayed under both arms. It consumes native lexical/exact/structural/role evidence
and optional gold without making judgments a production dependency. Current
generic evaluation retains its identity-coverage responsibility.

**Future retrieval experiments must diagnose observed failures by class rather
than reporting only aggregate metric movement. BM25F evaluation must use the
diagnostic facility to explain field/parameter effects.** Exact mechanics do not
prove semantic equivalence or relational necessity; Context and obligation
failures require independent evidence outside lexical diagnosis. The roadmap now
orders R1.6 canonical parameter sensitivity, R1.7 query-term investigation,
then mandatory R2 before R3–R6. No parameter or query-weight tuning is included
in R1.5, and Localization's continuation remains unchanged.

R1.6 now has a [precommitted protocol](../../experiments/bm25_sensitivity/PROTOCOL.md),
complete 180-configuration development surfaces over six frozen historical cases,
R1.5 native-score-validated diagnostics, and three deterministically selected
challengers. [Case 0010](../../experiments/codex_dogfood/case_0010/README.md) has
committed Stage A and one-time Stage B capture; independent sterile gold and
effectiveness are pending. Production `k1=1.2`, `b=0.75`, filename weight `0.25`
remain unchanged. The [variant audit](../../experiments/bm25_sensitivity/VARIANTS.md)
does not justify an R1.6b prerequisite before BM25F; open variant hypotheses remain.
R1.7 follows prospective R1.6 completion, then mandatory R2. No field aggregation,
query weighting or semantic-resolution experiment is implemented here.

Open adjudications include the placement of identifier evidence, the smallest
scientifically useful BM25F field schema, semantic retrieval granularity,
query formulation, valid supervised labels, purpose-relative discrimination,
complementary fusion and Context handoff/sufficiency. No choice is settled by
this document. ADR-0002/0003/0004/0005 remain consistent: they separate repository
truth, retrieval evidence/ranking, obligation resolution and disclosure, and
do not assert retrieval completeness or select one algorithm portfolio. Their
implementation/next-increment statements record their adoption checkpoints;
current state and sequencing live in architecture and roadmap. No ADR change
is required.
