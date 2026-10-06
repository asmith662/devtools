# Repository retrieval breadth: evidence and production gate

## Status and scope

Current-state qualification: the [retrieval foundation](../architecture/retrieval.md)
owns today's implemented inventory and retrieval-maturity interpretation;
[roadmap](../roadmap.md#current-sequencing) mandates R1 and unconditional R2 true
BM25F. The completed breadth sprint below did not adequately explore lexical
representation, fielding, query formulation, semantic mismatch or discrimination.
Its production-gate and "next" statements are historical checkpoints, not
current sequencing. Detailed frozen evidence is retained unchanged.

This is the completed, development-only Tier-1 breadth synthesis through
Increment 36. The production dispositions are recorded concisely in
[architecture](../architecture.md); [roadmap](../roadmap.md) owns their order and
[B-0002](../backlog/epics/B-0002-coding-context-substrate.md) retains unfinished
Context and Repository Intelligence work. This document owns the empirical map
and the reasons for the gate. It creates no production API or retrieval policy.

## Disposition

Accepted as the development evidence synthesis for the completed breadth
sprint. Current ownership and production status remain governed by
[`architecture.md`](../architecture.md), while [`roadmap.md`](../roadmap.md)
sequences the selected implementation work. Claims about other repositories,
structural selection, or Context effectiveness remain open.

The primary population is 24 historical `devtools` development InformationNeeds
at their parent snapshots. Dense evidence exists for only eight of those cases.
Graph-1 and Graph-2 judged probability samples, not their full candidate
surfaces. A returned `UNJUDGED` outcome differs from a never-adjudicated pair.
All Increment-27 and suspended Increment-26 confirmation populations remain
sealed. The [Increment-34 structural union](../../experiments/increment_34/README.md),
[Increment-35 heterogeneous union](../../experiments/increment_35/README.md), and
[Increment-36 fusion](../../experiments/increment_36/README.md) bind their source
artifacts and preserve those limits. Inheritance and Configuration/Registration
were inspections, with no new frozen candidate or usefulness surface in this
repository; their dispositions below are architectural, not measured baselines.

## Final evidence map

"New" below is relative to the stated earlier surface, not a universal
property of a resource. Counts are case/resource pairs unless identified as
addresses. Known usefulness is limited to frozen development judgments.

| Evidence family | Candidate reach and known-useful novelty | Fan-out, labels, and disposition | RI and possible Context value |
| --- | --- | --- | --- |
| Canonical BM25 | 1,942 positive pairs; K=5 has 63 USEFUL / 52 NOT_USEFUL / 5 UNJUDGED | Inexpensive executable production foundation; strong control, not complete Context | Lexical match is retrieval evidence; saved windows may locate source for later disclosure |
| BM25+ | Same 1,942 positive pairs and same K=5 usefulness counts as canonical on this surface | Keep as evaluated formula control; no independent promotion case | No new RI fact; preserves alternative lexical behavior |
| Identifier-aware BM25 | 2,149 positive pairs; K=5 has 68 USEFUL | Experimental lexical evidence, useful for code naming; labels deeper in its universe are incomplete | Exact/subtoken match can point to source names |
| Path-only BM25 | 149 positive pairs; only 48 positive K=5 occurrences, 31 USEFUL | Sparse standalone signal; retain as a field in comparisons, not sole retriever | Path clues can aid navigation, not repository semantic truth |
| Lexical RRF | 2,152 positive pairs; K=5 has 74 USEFUL versus canonical 63 | Strongest executable development K=5 control; promotion of default policy awaits independent validation | Rank fusion creates no RI fact; preserves separate native ranks |
| Dense / CodeRankEmbed | 40 top-five pairs in eight cases; one pair beyond lexical union structural is NOT_USEFUL; eight useful dense-only top-five pairs had deeper positive lexical ranks | Limited eight-case, pinned-model evidence; optional experimental comparator, no vector infrastructure | Winning chunks could inform representation, untested as Context |
| Direct Imports | 109 additions; 38 known USEFUL, including 11 absent from all five lexical universes | 99 outgoing / 23 incoming, 13 overlapping; bounded direct structural evidence, no fixed-K policy | Existing qualified production import facts can support dependency explanations and pointers |
| References / direct Calls | 71 additions, 35 USEFUL; 11 pairs beyond lexical and Imports include 4 USEFUL | 198 supports; maximum 12 additions per case/seed; all 71 call-tagged, so non-call value is unisolated | Bounded occurrence-to-function knowledge merits clean production design; spans and targets support fine disclosure |
| Immediate package containment | 49 additions, 14 USEFUL; 12 beyond earlier lexical/import/reference union are all NOT_USEFUL | Maximum four per case; observed direction is child to package initializer | Exact immediate membership remains a sound, separately useful typed RI design candidate |
| Mirrored test paths | 34 additions, 21 USEFUL; sole candidate beyond earlier complete union is NOT_USEFUL | Maximum four per case; exact path convention only | Possible weak navigation cue; neither TESTS nor EXERCISES nor coverage knowledge |
| Inheritance | No executable candidate baseline; inspected cross-resource cheap paths overlap Imports | Retrieval-degenerate under current facts; richer resolution absent | Direct class/base syntax may later aid contract disclosure; design separately |
| Configuration / Registration | No frozen candidate baseline or qualified relation in this sprint | Do not invent binding semantics for retrieval breadth | Schema-specific registration facts could matter greatly for Context; investigate when a concrete consumer exists |
| Graph-1 | 704 novel pairs beyond direct union; 2 USEFUL in a prospective 128-pair sample | 10,550 novel support paths; 574 unsampled pairs; sample useful fraction 2/128, not full-surface precision | Typed paths are derived consumer evidence, potentially useful for explanation/navigation |
| Graph-2 | 987 further novel pairs; 0 USEFUL in a separate prospective 128-pair sample | 85,015 paths to novel pairs, 294,154 complete paths; 857 unsampled; depth/fan-out parked | No new RI relation; longer paths need provenance and severe cost bounds |
| Structural Union | 1,916 pairs, 85 known USEFUL, 17 useful outside all lexical universes | 1,431 never adjudicated; 225 direct pairs versus 1,691 graph-round additions | Family membership and native supports stay distinct; union is not a graph truth object |
| Heterogeneous Union | 3,922 pairs, 176 known USEFUL; dense adds one NOT_USEFUL pair over lexical union structural | 3,228 never adjudicated; non-executable known-label K=5 ceiling 99 versus canonical 63 | Candidate ceiling is evaluation evidence, not an executable selection rule |
| Simple ranked-input fusion | Lexical RRF + available dense selects 73 USEFUL at K=5; saved lexical RRF selects 74 | No structural rank existed, so no structural-only candidate entered by structural evidence; keep as negative control | Combination is ranking logic, not RI or Context disclosure |

The lexical counts and fixed-window limitation come from
[Increment 27](../../experiments/increment_27/README.md): window K=5 has 64
USEFUL versus whole-resource 63, and every window-only candidate has a positive
whole-resource lexical rank. [Increment 28](../../experiments/increment_28/README.md)
found task-localized imported-binding use associated with usefulness, but its
incremental value conditional on coarse supports is unproven. It creates no
candidates and is not an additional reach row. [Increment 31](../../experiments/increment_31/README.md)
documents the limited mirrored-path meaning. The fixed chronology and reused
labels are descriptive, not a randomized family comparison.

## Decisions from the evidence

1. **Preserve a strong lexical foundation.** Canonical BM25 remains the
   production baseline. Lexical RRF is the stronger development K=5 comparator,
   but a development advantage is not a production default or confirmation.
   BM25+, identifier, and path evidence remain available as bounded controls.
2. **Keep direct structural candidate evidence.** Imports and bounded
   References/direct Calls established useful lexical escapes. A relation's
   repository meaning and its purpose-relative candidate projection are
   separate; neither proves resource usefulness.
3. **Stop automatic graph depth.** Graph-1 sampled useful complementary reach
   sparsely; Graph-2's sample observed none while fan-out grew sharply. The
   unsampled populations cannot be relabeled by inference. Neither result
   justifies a universal graph, default recursive expansion, path-count score,
   or graph database.
4. **Treat the heterogeneous ceiling as a selection problem.** The union has
   176 known-useful pairs, but a five-slot known-label oracle's 99 is a lower
   bound under incomplete labels, not an executable policy. Saved lexical RRF
   selects 74; simple lexical+dense RRF selects 73. The latter never tested how
   unranked structural candidates should enter five slots.
5. **Keep dense as a limited comparator.** Eight cases do not establish general
   embedding failure or warrant another model sweep. No dense useful reach
   beyond lexical union structural appeared on that frozen surface.

## Production Repository Intelligence gate

| Knowledge | Disposition | Semantic reason |
| --- | --- | --- |
| Repository/resource/content/snapshot identities and observation | **Retain existing production ownership** | Identified observed state precedes any retrieval or evaluation claim; Git commit is not snapshot identity |
| RepositorySubject, SourceOccurrence, derivation and coverage distinctions | **Retain and strengthen through bounded implementations** | Existing function declarations embody these semantics; no universal subject or knowledge container is needed |
| Explicit-root Python module interpretation; direct function declarations; direct import declarations | **Retain existing production ownership** | Deterministic qualified facts independent of task usefulness |
| Imported-member resolution and uniquely resolved directed module Imports | **Retain existing production ownership** | Bounded resolution and native provenance are already implemented; no runtime-import claim |
| Qualified function Reference occurrence with direct Call specialization | **Design and implement next, in Python RI** | Repeated experiment derivation, useful direct reach, and span/target value beyond file retrieval justify a narrow durable proposition |
| Immediate observed package/module membership | **Design next after the reference slice** | Exact same-root, same-snapshot, unique-parent proposition is sound despite weak incremental file reach |
| Module/declaration ownership | **Use existing declaration support and module interpretation; expose a typed projection only when a consumer needs it** | A declaration already has an exact containing resource; a resource-to-itself traversal is not novel reach |
| Direct class declarations and syntactic direct-base facts | **Design later, separately** | Meaningful RI/Context facts, but class identity and qualified base semantics are not implemented; no MRO/dispatch inference follows |
| Mirrored code/test paths | **Experiment-only as a convention cue** | Path equality does not establish tests, exercises, execution, or coverage |
| Verified code/test or configuration/registration binding | **Defer until a scoped semantic source and consumer exist** | Do not convert import, path, runtime execution, or configuration spelling into a stronger fact |
| Typed structural paths and traversal | **Consumer-side bounded projection, not canonical RI fact** | RI owns each native relation; retrieval/Context selects compatible path schemas and work limits |

The first RI increment should establish a source-grounded read occurrence tied,
under explicit conservative binding and one-facade limits, to an existing direct
module-body `PythonFunctionSubject`. A direct call is the same qualified
reference when its occurrence occupies `ast.Call.func`; retain the exact span,
supporting import and resolution, snapshot, derivation, uncertainty, and bounded
coverage. This does **not** establish runtime invocation, dispatch, methods,
`obj.foo()`, arbitrary aliases, non-call usefulness, or a function-to-function
CALLS edge. Identifying an enclosing caller function would require a separate
proposition. Port the semantics cleanly; do not move Increment 29 code wholesale.

For containment, package-to-immediate-child and child-to-unique-parent are
two directions over one qualified membership fact. They are not arbitrary
hierarchy traversal. Declaration support already records resource ownership.
Class declarations and direct-base syntax should be considered for later
fine-grained Context, without treating retrieval degeneracy as a negative RI
result. Actual test execution/coverage belongs to execution/observability
evidence until a separately derived repository-relative relation is justified.

## Retrieval, graph views, and the open selection question

ADR-0002's typed graph *views* remain a sound semantic option over native RI;
no materialized universal graph, graph library, or database is justified.
Relation-specific lookup/index mechanics may belong beside authoritative facts
when a measured consumer requires them. A purpose-relative path expansion,
frontier, exclusion rule, candidate and fan-out belong to retrieval or a
specific Context navigation application, not repository truth. Distinct path
schemas and directions must remain visible. Graph-2's 294,154 complete paths
make unbounded traversal an unacceptable default.

Candidate acquisition may maintain a broad, provenance-preserving consideration
surface. RelevanceEvidence retains native lexical ranks, import/reference
supports and qualifications; it is not a common score. Ranking or admission
interprets that evidence for an InformationNeed under scarce resource capacity;
Context planning separately chooses information and representation under a
disclosure budget. No first-class universal Candidate/Selector or fusion API is
required. The specific parked question is: **how should heterogeneous,
unranked structural evidence influence resource selection under a fixed
budget without allowing fan-out or path multiplicity to masquerade as
relevance?** Established aggregation, task-conditioned rules, or learned
ranking remain alternatives, not decisions.

## Retrieval to Context compilation

Resource retrieval answers which files may matter. The next Context problem is
which facts, declarations, spans, relationships, and explanations inside or
across them are sufficient for the InformationNeed. A concrete bounded flow is:

```text
resource candidate + native retrieval evidence
    -> exact snapshot-bound occurrences/subjects and supporting relationships
    -> source-preserving excerpt or knowledge projection, with provenance
    -> purpose-relative disclosure choice under availability and cost limits
    -> faithful materialization -> ContextDisclosure
    -> model-input assembly -> ModelRequest
    -> later, separately requested or justified expansion if needed
```

Existing production declaration spans, exact function source materialization,
import occurrences, module identity and resource metadata can seed this flow.
Saved lexical windows and experimental import-use, reference/call,
containment, mirror, and typed-path evidence show possible localization and
navigation inputs; they have **not** been evaluated as disclosure units or
agent-task improvements. An occurrence span can support direct source
disclosure; a declaration identity can support signature/body selection; an
import/reference can support a qualified relationship explanation; a typed
path can be a pointer to further inspection. A mirror path is only a weak
pointer. A summary that adds semantic assertions needs the explicit synthesis
and provenance discipline of ADR-0004.

Progressive disclosure may initially provide an exact pertinent span or fact,
a concise account of related resources, and stable pointers to undisclosed
material. Additional detail is acquired or disclosed only under a later
purpose/sufficiency decision. Previously disclosed material is not assumed
currently available. A budget is a ceiling, not a requirement to show full
files. This is an architecture direction, not authorization for a generic
compiler, universal information unit, or prompt protocol.

## Evaluation, population, metrics, and Learning

The accepted Evaluation responsibility now has a concrete promotion target:
a **small, cross-domain assessment kernel** for an identified comparison basis,
exact target/decision coverage, outcome missingness, sample-frame/selection
provenance, and reproducible correlation to producing artifacts. The already
extracted [judgment coverage helper](../../experiments/retrieval_judgment_coverage.py)
is evidence of stable safeguards, not a production implementation to copy
unchanged. Evaluation should consume retrieval, Context, Model and execution
observations without owning their lifecycles. The first kernel must not invent
a universal `Population`, `EvaluationCase`, `Metric`, episode, store, or
experiment engine.

The top-level `src/devtools/evaluation/` domain already exists but has no such
production kernel today. This gate affirms Evaluation as its owner and makes
the kernel a later bounded implementation increment, not a blanket migration
of experiment code.

"Population" here names an evaluation cohort or candidate/judgment frame,
not inherently a training dataset. Increment 25 task sampling, Increment 27
lexical pooling, later case/resource candidate sets, and Graph-1/2 probability
sampling have different units and inclusion rules. Evaluation can own the
assessment basis and sample/coverage semantics; retrieval defines candidate
identity and relevance meaning; Learning may consume a governed dataset
derived from those observations. Never-adjudicated, returned `UNJUDGED`,
`NOT_USEFUL`, and `USEFUL` remain distinct.

The production lexical evaluator already computes Hit@K, Recall@K,
reciprocal rank and MRR for its binary designated-resource fixture. That does
not make judged-pool counts exhaustive recall. Retrieval owns relevant-item,
universe, K, ordering, and denominator definitions; Evaluation owns comparison
validity and may later share truly common metric arithmetic. Learning owns
training-specific loss/validation use, not all retrieval metrics. Precision@K
and NDCG are not established implementations here; no generic metric protocol
is selected.

Cross-domain Learned Intelligence is a credible **future** first-class
capability for model construction, training, model artifact/version management,
and reusable inference realization. Its package name and API remain open.
Context or retrieval may use an identified learned capability without owning
training. Learning may use Evaluation and domain-produced features without
owning RepositorySubjects or evaluation truth. The separate model-training
project has no detailed architecture captured here; the clean convergence
seam is native RI/retrieval observations -> governed Evaluation basis ->
Learning construction -> supplied capability consumed by retrieval/Context.
Existing `resources.commands` owns direct process execution and narrow
`execution.Runtime` owns one model interaction; neither should be duplicated
inside future Evaluation or Learning.

## Migration, implementation sequence, and confirmation

Retain frozen Increment 25-36 protocols, candidate artifacts, judgments,
samples and results as scientific history. As production facts become
available, stop re-deriving the same AST import/reference/containment facts in
new consumers; validate parity against frozen fixtures rather than rewriting
historical identities. Experiment candidate projections, neutral blinding,
source-specific frozen loaders, sampled outcome joins, window rankings,
structural unions and fusion baselines remain research code unless a new
production consumer establishes a narrow contract. The small judgment
coverage helper may inform Evaluation; it is not an excuse to migrate all
`population.py` modules. Obsolete runners may later be marked historical or
retired only after reproduction paths and retained artifacts are accounted for.

| Breadth code or artifact | Disposition |
| --- | --- |
| Frozen case definitions, queries, judgments, samples, hashes, results, and blinded inputs | Retain immutable research evidence and reproduction paths; neutral blinding is research protocol, not runtime Context |
| Snapshot/corpus loaders and repeated `population.py` assembly | Keep experiment-local until exact shared input semantics are demonstrated; do not create a universal Population |
| Exact judgment identity, three-state coverage, sampling-frame and artifact correlation checks | Design a small Evaluation-owned kernel after the RI prerequisites; preserve retrieval-owned usefulness semantics |
| Import/reference/call/package AST and resolution derivations | Replace future duplicate derivation with qualified production Python RI as each typed fact is implemented and parity-tested |
| Direct candidate projections and lexical controls | Retrieval-owned strategy candidates after a real consumer is chosen; retain frozen experiment implementations as baselines |
| Lexical windows and structural source spans | Possible Context localization/disclosure inputs; no disclosure policy is yet empirically validated |
| Candidate-level features and outcome joins for future models | Retain as experimental observations; Learning may consume governed datasets later, without owning RI or Evaluation |

The dependency-led sequence is:

1. **Bounded Python Reference/direct Call RI.** Establish qualified
   occurrence-to-function knowledge, uncertainty/coverage, and snapshot-bound
   support; no retrieval behavior change.
2. **Immediate package membership RI.** Derive only unique observed parent
   membership under an explicit root; retain missing/ambiguous outcomes.
3. **Small Evaluation kernel.** Extract exact assessment identity, neutral
   coverage, sampled-frame and missingness semantics from repeated experiments
   without taking ownership of retrieval labels or execution.
4. **Retrieval consolidation.** Consume production typed facts for direct
   candidate generation; retain canonical BM25 and saved lexical RRF as
   evaluated controls; keep structural evidence unranked until a selection
   rule is justified.
5. **First fine-grained Context slice.** From an explicit selected resource,
   disclose a source-grounded declaration plus a qualified related occurrence
   or pointer, with faithful provenance and an optional follow-up expansion.
6. **Post-breadth selection work and later Learning convergence.** Freeze a
   bounded structural admission question before any independent confirmation;
   train nothing merely because heterogeneous features exist.

**Exactly next production increment:** item 1. It removes repeated
experiment-local reference/call derivation, establishes a useful RI and Context
substrate, and gives later retrieval a qualified source of truth. It excludes
general Python name resolution, dynamic dispatch, generic REFERENCES/CALLS
infrastructure, graph storage, ranking, Context compilation, and new
judgments.

Choose **confirmation after a specific selection architecture exists**. The
current simple fusion has no structural admission; confirming it now would not
answer the central structural selection question. Production RI work can
continue while confirmation stays sealed. Confirmation must be bound to a
prospectively selected executable policy and its applicable population; it
must not be used to tune that policy.

## ADR reconciliation and disposition

The breadth evidence **confirms** ADR-0002's separate subjects, occurrences,
qualified typed RI and semantic-versus-physical graph distinction; it adds
implementation pressure for a narrow reference fact, not a new graph
foundation. It **confirms and sharpens** ADR-0003's candidate/evidence versus
ranking/admission distinction: the heterogeneous reach ceiling and small-K
selection gap are now measured, while a structural rank remains unresolved.
It **supports without testing** ADR-0004's resource-to-information and
progressive-disclosure direction. No accepted ADR invariant is contradicted,
so no ADR amendment is required for this gate. Revisit these dispositions only
on a concrete semantic counterexample, independent-repository falsification,
or a consumer that cannot preserve qualification and provenance.
