# Roadmap

## Purpose

This document records deliberately selected current sequencing. It is not an
API reference, a replacement for the canonical backlog, or authorization to
implement a future domain. The [architecture taxonomy](architecture/taxonomy.md)
defines terms; [architecture](architecture.md) defines current ownership; the
[backlog](backlog/overview.md) preserves unresolved pressure.

## Established architecture

The twelve-domain framework architecture is established:

```text
core/ resources/ models/ agents/ context/ tools/
execution/ orchestration/ governance/ observability/ persistence/ evaluation/
```

Current implemented seams include the core and resource substrates,
`Prompt -> ModelInteraction -> ModelResponse`, durable `Conversation` and
`ConversationMessage` state, narrow execution `Runtime` with specialized
`InteractionAttempt`, terminal Evidence in observability, Conversation
persistence, Tools, model serving and benchmarks, and the external Codex Agent
integration. Sparse domains are intentionally not implementation commitments.

Historical pre-migration milestones, including former Session, Interaction,
and Evidence ownership terminology, remain in the
[implementation ledger](implementation_ledger.md) as history only.

## Current sequencing

### Current — advisory Codex retrieval dogfooding

The Tier-1 breadth sprint through Increment 36 is complete. The
[breadth evidence and production gate](research/repository-retrieval-breadth-production-gate.md)
records its empirical limits and dispositions; the prospective Increment 27
sequence and earlier retrieval checkpoint below remain historical. Direct
Imports and bounded References/direct Calls supplied useful complementary
resource reach. Unranked Graph-1/Graph-2 traversal caused large fan-out, and
structural selection at K=5 is unresolved. Canonical lexical retrieval remains
the default ranked baseline. Direct structural retrieval and snapshot-bound
resource evidence composition are production candidate inventory surfaces.
Query-conditioned PPR and optional rank-level RRF are also production retrieval
evidence; no default graph fusion, dense model, or Context disclosure policy is
promoted.

The bounded declaration Reference increment now extends production Repository
Intelligence to same-module functions/classes, directly imported declarations,
module-qualified declarations, and statically class-qualified direct methods.
The frozen Case 0002 structural replay increased forward graph edges from 279
to 360 and connected four of seven formerly isolated required resources. The
unchanged Personalized PageRank (PPR) replay still placed the last required
resource at rank 87 for the full prompt (formerly 84), because documentation
and configuration required resources remain structurally isolated. The
subsequent richer Retrieval graph comparison projected
Imports, References, containment, direct bases, package membership, and
mirrored-path correspondence with explicit edge-family and direction choices.
On the retained development case, typed
declaration topology was restored, but complete required-resource depth
worsened. Prospective evaluation of resource aggregation or a global structural prior
requires an independently frozen task. The separate repository-map checkpoint
below implements that channel and retains Case 0002 only as diagnostic replay. This is a
Retrieval decision, not a change to Context admission. The single retained
case is diagnostic evidence, not an unbiased ranking evaluation.

The production Selection architecture investigation is complete. No universal
resource-Selection stage is mandatory between Retrieval and Context. Resource
assessment and sufficiency are distinct possible decisions, with no
variable-cardinality admission rule, budgeted file set, or Selector API
selected. A retrieval candidate or advisory orientation does not imply
disclosure or sufficiency. Codex dogfood keeps normal search, open, edit, and
validation access.

Proceed in dependency order: (1) bounded source-grounded Python function
Reference/direct Call Repository Intelligence; (2) qualified immediate package
membership; (3) a narrow cross-domain Evaluation assessment/coverage kernel;
(4) direct retrieval candidate generation consuming production typed facts;
(5) compose lexical and structural native evidence in one snapshot-bound
resource inventory; (6) investigate Selection architecture; (7) dogfood
advisory retrieval on real Codex tasks; (8) adjudicate misses and waste;
(9) consider a budgeted resource rule only with evidence; (10) implement one
fine-grained Context disclosure slice from an explicitly supplied fact.
Items 1-8 and 10 are complete; item 9 remains evidence-dependent. The first
six items established bounded Reference/direct Call RI, qualified immediate
package membership RI, the domain-neutral expected-versus-observed identity
coverage kernel, and direct
structural candidate projection over production RI, followed by native evidence
composition. The inventory is not a selected file set. Assessment identity and
outcome semantics remain consumer-owned. Preserve frozen experiments for
reproduction; new consumers should use production RI rather than duplicate
its derivation or experiment-only union logic. Confirmation remains sealed; no
shadow or independent-repository claim follows from development results.

The first fine-grained Context increment is an explicit qualified Python
Reference/direct Call disclosure. A caller supplies a purpose, one established
fact from its analysis, and the matching snapshot. Context validates both
source dependencies, discloses the exact Reference Name and target function
declaration with relationship provenance and pointers, and can assemble the
result beside a task. This does not solve general Selection or sufficiency.
Later/refined InformationNeeds and progressive disclosure remain possible
future behavior, not a demonstrated recovery guarantee.

The current Context checkpoint establishes a caller-directed, snapshot-bound
DisclosurePlan with multiple ordered concrete choices and a distinct realized
ContextDisclosure. The existing qualified Reference path participates without
losing its native checks; an explicitly chosen whole observed resource is a
second faithful representation. This is a production planning boundary, not
automatic ranking, budget allocation, sufficiency, or a recovery controller.
The [Context Planning and graph-assisted retrieval research](research/repository-context-planning-and-graph-assisted-retrieval.md)
provides comparative motivation; ADR-0003 and ADR-0004 govern accepted meaning.

[Codex dogfood Case 0001](../experiments/codex_dogfood/case_0001/README.md)
completes the first advisory run and blind required-resource adjudication for
steps 7-8. Both complete lexical inventories found all seven required
resources, but full-prompt BM25 needed 35 candidates to cover them and the
short InformationNeed needed 132. Direct structural evidence rescued none.
This single case identifies candidate ordering and handoff volume as measured
pressure; it does not select a production Selection rule or establish a general
query-formulation result.

[Codex dogfood Case 0002](../experiments/codex_dogfood/case_0002/README.md)
completes a second prospectively frozen implementation task: the roadmap's
explicit lexical-only path for future cases without justified structural
seeds. Blind adjudication required ten resources in a 302-resource frame;
both complete lexical inventories found all ten. Full-prompt BM25 needed 43
candidates for complete coverage and the short InformationNeed needed 87.
Direct structural evidence again rescued none. The edit-capable Codex host
was interrupted and continued in a second ephemeral session; both traces and
the resulting observation limits are retained. These two repository-local
cases continue steps 7-8 and show measured handoff pressure, but do not
select a production rule for step 9. Further dogfood needs an independently
justified task; no Case 0003 is created by this Context checkpoint.

### Completed — graph-assisted repository ranking baseline

Immediately after the Context Planning foundation, the project implemented a
bounded repository-map-inspired **query-conditioned structural ranking**
baseline over production Repository Intelligence using personalized PageRank.
The production graph view uses forward Imports and References/direct Calls,
equal fact weights, lexical-rank personalization, weighted PPR, and optional
equal-channel RRF. It preserves native evidence and leaves disclosure to
Context Planning. This is not Graph-3: historical Graph-1/Graph-2 evaluated
unranked breadth. The [development replay](../experiments/graph_ranking_baseline/README.md)
on one frozen production-RI case found worse required-resource depth for PPR
and fusion than BM25. Seven of ten required resources were graph-isolated.
The graph channel remains optional; no automatic Context handoff follows.
Confirmation remains sealed.

### Current structural RI sequence — richer repository facts before graph replay

1. Promote exact observed mirrored source/test path correspondence as a narrow
   Python Repository Intelligence fact. This increment is complete. The fact
   establishes a path convention, not a semantic test relationship. Historical
   candidate usefulness and deterministic repository truth are separate claims.
2. Establish declaration ownership/containment with exact resource and source
   support. This increment is complete as a validated navigation view over
   intrinsic function declaration ownership; it adds no duplicate RI fact.
3. Establish bounded class and method declarations. This increment is complete
   for direct module-body classes and direct synchronous/async methods, with
   occurrence-resource and direct lexical-parent semantics kept distinct.
4. Establish bounded direct inheritance/base relationships with qualified
   resolution and uncertainty. This increment is complete: every retained
   base expression receives a snapshot-bound assessment; positive direct
   repository class targets require an unambiguous supported binding.
5. Extend Reference/direct Call structure under bounded, source-grounded
   resolution. Complete: supported functions, classes, and direct methods now
   have one canonical production Reference derivation.
6. Construct and prospectively evaluate a richer typed Retrieval graph over
   that RI. Complete: the [fixed development replay](../experiments/typed_graph_baseline/README.md)
   restores declaration topology, but typed PPR and equal-channel fusion do
   not beat BM25 complete required depth on retained Case 0002. Confirmation
   is sealed. Graph ranking remains optional evidence.
7. Completed in Case 0003: freeze a new independent development task/frame before comparing a
   repository-map-style structural prior and alternative typed-node resource
   aggregation. The retained Case 0002 result diagnoses missing
   documentation/configuration relationships and resource-biased aggregation;
   it must not be reused to tune those choices. Keep Selection and Context
   disclosure decisions separate from Retrieval ranking.

### Controlled advisory Codex dogfooding

The authorized Case 0003 implementation establishes bounded
[Python configuration RI](../src/devtools/context/python/project_configuration/docs/overview.md)
for the six selectors actually declared by this project. This adds static
observed relationships and explicit assessments, without changing ranking,
graph projection or Context policy. Future relation admission requires its own
explicit Retrieval decision and prospective evidence. Entrypoint machinery is
not justified by this project, and B-0019 runtime configuration remains deferred.
The [Case 0003 record](../experiments/codex_dogfood/case_0003/README.md) now owns
the completed independent blind adjudication and cross-case findings. Nineteen
resources were required in a 472-resource pre-task frame. Full/short BM25 complete
depths were 348/180, typed Personalized PageRank (PPR) 314/278, and BM25/map
Reciprocal Rank Fusion (RRF) 372/279. Repository map found five required resources
and omitted fourteen in both arms. No required lexical miss was rescued. The
broader frame and task differ from earlier cases; no pooled ranking or exploration
savings claim is made. Ranking parameters and Context policy remain unchanged.

[B-0047](backlog/items/B-0047-protected-development-validation-profile.md)
records current pressure for supported development validation isolation before
collection. This increment uses explicit safe test directories and focused
coverage overrides. Host validation passed 1,299 tests with two live skips and
100% production branch coverage using `tests --ignore=tests/experiments` plus
explicit capture and Case 0003 protocol files. All retained experiment tests
were excluded before recursive collection. No general harness is promoted here.

For each bounded real task, freeze the snapshot, eligible lexical index/corpus,
verbatim prompt, separately authored short InformationNeed, BM25 settings,
qualified seed origins when justified, and already-derived RI fact inputs before
retrieval. The research capture in `experiments/codex_dogfood` runs both lexical
arms over the same index/settings and complete positive-match work bound. With
qualified seeds, it composes each arm with one direct structural result under
the short purpose. With zero seeds, it checks the entire lexical corpus against
the frozen snapshot and retains both native BM25 results in lexical-only
inventories; it makes no structural request. The inventories retain native
lexical rank, score and contributions, and query text. Seeded inventories also
retain structural seeds, directions and facts. The initial orientation lists
all surfaced resource addresses by neutral address order with provenance. It
is an advisory work aid, not a selected or sufficient file set; Codex remains
free to search, open, edit, and validate outside it.

Record Codex searches, opened/read resources, modified resources, validation
resources, task and validation outcomes, and bytes/tokens only where reliably
observed. State the observation source and completeness limits. The current
production Codex adapter is read-only and returns final text/thread identity,
not exhaustive tool activity, so it is not an edit-capable telemetry source.
Use an authorized normal Codex run with separately captured interaction history;
do not infer an unobserved search/read from its final answer. Never treat opened
or modified resources as synonymous with required resources.

After task completion, pool prospectively expected resources if available,
surfaced resources, searched/opened resources, modified resources, validation
resources, and plausible misses for blinded adjudication. Label whether each
resource was required for understanding, implementation, API/contract review,
tests, configuration, or validation; helpful only; unnecessary; or unresolved.
Record acceptable alternatives. Do not feed labels back into retrieval. Compare
initial and eventual required-resource coverage, misses, unused surfaced
resources, additional searches and opens, reliable file/byte/token reads, task
success, and validation success separately. Compare full-prompt and short-query
coverage and waste rather than assuming either wins. A later controlled
retrieval-assisted versus unaided Codex comparison may measure exploration
reduction under matched conditions. Any production resource-admission or
budget policy remains a separate, conditional decision informed by these
observations; no universal Selection stage is assumed. Confirmation stays
sealed.

### Ongoing — documentation integrity and backlog rebase

- [B-0001](backlog/epics/B-0001-architecture-documentation-integrity.md) and
  [B-0006](backlog/items/B-0006-reconcile-authoritative-architecture-documentation.md)
  keep current documentation, roadmap sequencing, and backlog pressure aligned
  with the established architecture.

### Historical starting point — bounded Repository Intelligence and retrieval evidence

- [ADR-0002](architecture/decisions/ADR-0002-repository-intelligence-identity-and-derivation.md)
  establishes semantic architecture for Repository identity, snapshots,
  RepositorySubjects/SourceOccurrences, Derivations, DerivedKnowledge, graph
  semantics, snapshot observation/delta/incremental-maintenance, minimum
  derivation/knowledge semantics, repository DerivedKnowledge jurisdiction,
  qualified epistemic semantics, semantic-result coverage/absence,
  repository conflict/source-role knowledge, epistemic-derivation/
  representational-transformation distinction, capability-realization boundary,
  and Context boundaries.
  [ADR-0003](architecture/decisions/ADR-0003-information-need-retrieval-evidence-and-ranking.md)
  establishes InformationNeed, retrieval evidence/planning, and ranking
  semantics. [ADR-0004](architecture/decisions/ADR-0004-context-disclosure-planning-and-assembly.md)
  establishes Context/disclosure planning, materialization, provenance-bearing
  disclosure artifacts, representation origins, purpose-relative synthesis,
  explicitly planned semantic transformation and semantic-strength preservation
  during materialization/assembly, and model-input assembly semantics.
  [B-0002](backlog/epics/B-0002-coding-context-substrate.md)
  retains the unimplemented design pressure. These decisions are not authorization
  for a general Context compiler, disclosure model, parser, graph store, retrieval
  system, Memory, Agent loop, or orchestration system; the current bounded lexical
  index, bounded filename-field BM25 baseline, deterministic fixture evaluation, and small real-repository
  benchmark do not settle those broader responsibilities.
  [B-0008](backlog/items/B-0008-investigate-repository-context-discovery.md)
  remains superseded historical navigation evidence.

- The selected starting hypothesis began with direct module-body Python function
  declaration knowledge. The bounded implementation tests the proposition in
  which direct module-body `ast.FunctionDef` and `ast.AsyncFunctionDef` source
  occurrences in an identified RepositorySnapshot syntactically declare
  distinct snapshot-local function RepositorySubjects. Subsequent bounded
  production slices establish direct module-body import-declaration syntax and
  explicit-root Python module interpretation for selected observed `.py`
  resources. The first slices did not implement import resolution, repository
  dependency relationships, graphs, retrieval integration, or runtime import
  semantics.
  A subsequent bounded resolver now resolves eligible import module portions only
  within an explicit module-interpretation universe. A bounded relation
  derivation now retains directed declaration-grounded source-to-target module
  relations only for qualified resolved outcomes; it does not establish runtime
  imports or retrieval relevance, and is not integrated into production
  retrieval. The resolver and relation derivation remain distinct from runtime
  import semantics.
  These are design targets, not fixed production representations or a universal
  declaration ontology. [B-0002](backlog/epics/B-0002-coding-context-substrate.md)
  preserves the exact scope, design pressure, and deliberate deferrals.

- Increment 23 completes the independent blinded validation of Increment 22's
  rule. Its repaired pipeline freezes 96 judgments and preserves disagreement
  among control expectation, blinded usefulness, and post-unblinding review.
  The rule has zero net known-useful gain, one not-useful admission, and one
  useful rank-five loss; it is `NOT_READY_FOR_SHADOW` and not production-ready.
  Lexical top fifteen contains all known-useful material resources, so this
  checkpoint points toward measuring candidate coverage and ranking depth
  separately, not further tuning of the single reservation slot. Production
  retrieval/disclosure remains unchanged; no generic experiment platform,
  Selector, or production Context influence is authorized.

### Architecture review gate — crossed with preserved seams

The broad repository-intelligence architecture investigation has occurred. The
work included architecture reconstruction/archaeology, rationale steelmanning,
external adversarial/Deep Research review, finding-by-finding reconciliation
across multiple focused passes, and a preservation audit. Repository identity,
subjects/source occurrences, snapshots/maintenance, derivation/knowledge,
capability realization, graph views, retrieval/ranking, Context disclosure,
synthesis, authority/conflict boundaries, and semantic-strength preservation
are considered sufficiently settled at the foundational semantic level. The
focused external-semantic-state/dependency-identity/applicability/replay Deep
Research investigation has also completed and its accepted findings have been
reconciled into ADR-0002 without selecting concrete mechanisms.

The focused integrated-evaluation/causal-attribution investigation has now
completed its substantive analysis and its accepted findings have been
reconciled into the canonical architecture. Evaluation is a distinct semantic
responsibility, but no universal Evaluation framework, Episode, score, causal
graph, trajectory, store, or lifecycle is accepted. The producing research
process did not complete its dossier's final mechanical artifact-integrity
verification; subsequent review and reconciliation treated the dossier as
research evidence rather than an accepted or mechanically verified decision.

The implementation-start assessment is **SAFE WITH PRESERVED SEAMS**. The core
semantic architecture is sufficiently settled, and B-0002's bounded-slice
promotion trigger is now met at the design level by the selected starting
hypothesis. This sequencing decision does not itself authorize production
implementation. Initial design must retain the semantic basis and correlation
needed for later local-correctness, downstream-utility, resource, and marginal-
contribution evaluation without first building generic Evaluation
infrastructure.

The recovered [research evidence](research/README.md) has been reconciled into
canonical research records and linked ADR dispositions. It preserves historical
alternatives and deferrals; it neither authorizes implementation nor converts
research recommendations into roadmap commitments.

Later external adversarial/Deep Research confirmation remains a confirmation/
reopen gate, not an implementation-start gate. It can reopen foundational
architecture if it discovers a material contradiction or missing semantic
capability. This roadmap state does not authorize implementation, mark B-0002
complete, claim Evaluation infrastructure exists, or settle implementation-
shaped choices.

### Later — promotion only when evidence is sufficient

The canonical backlog contains deferred pressure for generic execution
lifecycle promotion, model-facing Tool and Action boundaries, Agent semantics,
orchestration, governance, durable observability, and advanced model
interaction. Each remains subject to its own dependencies and promotion
conditions. The Qwen probes are experimental evidence, not reusable framework
promotion.

## Validation cadence

Use deterministic validation for implemented changes. Add task-specific live
acceptance only when a meaningful specialized path exists; live evidence tests
framework enforcement and causal boundaries, not voluntary model obedience.

See [documentation_map.md](documentation_map.md) for authority and navigation.

## Historical retrieval evidence checkpoint

Increment 24's offline comparison over Increment 23's retained six-case surface
does not promote a ranker: its frozen purpose-relative deterministic arm recovers
9 known-useful resources versus 10 for lexical/native ranking. The reconciled
[structural-retrieval research](research/structural-repository-retrieval.md)
changed the Increment 25 question from how relationship evidence should occupy
K=5 to which evidence families expose complementary useful resources. The
[repository-retrieval landscape](research/repository-retrieval-algorithm-landscape.md)
now directs the next experiment toward foundational retrieval variables.

- **Increment 25 (complete):** the frozen `devtools` confirmation compared
  one-hop outgoing imported-member function-binding expansion from lexical
  top-five seeds with candidate-volume-matched lexical widening. Structural
  expansion fired in 12/16 cases and produced 31 additions: 17 useful and 14
  not useful. Of the useful additions, seven overlapped matched lexical
  widening, ten were structural-only, and five had no positive lexical rank.
  Matched lexical widening produced 15 useful and 16 not-useful additions,
  including eight useful lexical-only resources. This repository-local result
  retains the imported-member family as validated structural evidence without
  authorizing production retrieval, common graph infrastructure, or ranking
  changes.
- **Increment 26 (development complete):** the frozen CodeRankEmbed comparison
  found eight useful semantic-only top-five resources. All eight had a deeper
  positive lexical rank, so this is top-K/ranking complementarity, not evidence
  of useful lexical-unreachable resources. Preserve its valid development
  evidence and sealed confirmation population. Confirmation is suspended
  pending a decision-worthy future comparison; it is neither completed nor
  rejected. No trained ranker or vector database follows from this result.
- **Increment 27 — Repository Retrieval Foundations: unit, representation,
  fielding, fusion, and ranking-depth falsification:** test the ceiling and
  failure modes of inexpensive code-aware retrieval. Measure Recall@K over
  depth; exact symbol/path/error resolution or routing where applicable;
  resource, declaration/AST-aware, and useful fixed-window retrieval units;
  exact identifiers plus
  subtokens, code-aware lexical text, and path/module/symbol/content fields;
  deterministic query-clue extraction while preserving the InformationNeed;
  a small BM25 sensitivity check; character n-gram auxiliary retrieval; cheap
  union/interleaving/Reciprocal Rank Fusion; already validated structural
  evidence; and compact repository/symbol-map disclosure where appropriate.
  Keep retrieval unit distinct from disclosure unit. This is a bounded
  falsification program, not a generic retrieval framework.
- **Later, conditional evidence:** test additional typed relations, lightweight
  learned ranking only after a high-recall pool exists, and persistent-index
  neural retrieval with a competitive model only if cheaper baselines leave a
  decision-worthy gap. Any broader evidence-family comparison depends on the
  foundations results; no later increment is selected yet. Falsify surviving
  claims on independently selected repositories before broader generalization
  or production promotion. Consider non-controlling shadow comparison only
  under separate governance and later supporting evidence.

Evaluate stages separately: poor broad Recall@K points to candidate generation;
good broad recall but poor small-K ordering points to ranking; good ordering
but poor useful information per disclosure budget points to representation and
Context disclosure. Cheap follow-up inspection/search can also change the
value of one-shot ranking. These are diagnostic guides for experiments, not
fixed architecture or a universal score.

The broader portfolio remains heterogeneous: typed structural/relational views,
semantic/pretrained-representation evidence, and later learned decision models
are separate hypotheses with native evidence semantics. Repository Intelligence
owns qualified typed facts; whether future structural navigation uses independent
views, a unified typed substrate, or relation/index projections remains an
operational question. Shadow execution, if later justified, follows offline and
independent validation and remains non-controlling until separately promoted.


## Repository-map checkpoint and next evidence gate

The separate repository-map increment is implemented: global dependency
importance, compact declaration/path BM25, symbol RRF and maximum-symbol
resource projection, with optional lexical-resource RRF and retained provenance.
The [package contract](../src/devtools/context/retrieval/repository_map/docs/overview.md)
and [diagnostic record](../experiments/repository_map_baseline/README.md) distinguish
it from query-conditioned PPR. Case 0002 remains diagnostic: improved
implementation ranks do not overcome absent governance/configuration symbols,
and fusion worsens complete coverage depth. No default fusion is selected.

That prospective gate is complete in
[Case 0003](../experiments/codex_dogfood/case_0003/README.md), whose independently
justified production task establishes Python-project configuration RI. It
confirms complementary implementation-resource ordering, not a universal map
ranker or default fusion. Full-prompt PPR modestly improves complete depth in
this case; the short need improves lexical depth here after hurting Cases 0001
and 0002. Configuration facts were deliberately not added to Retrieval during
this comparison.

The exact next recommended architectural increment is an explicit bounded
Retrieval projection of configuration declarations and qualified target facts,
with selector families, direction, prefix fan-out, duplicate handling and
resource/symbol eligibility fixed before a new natural-task comparison. Do not
turn all 1,026 prefix facts into equally persuasive relevance votes. Keep the
lexical channel available for governance/docs and declaration-free facades;
current evidence does not justify a universal admission or default RRF policy.
B-0047 is an operational prerequisite for further autonomous evaluation work:
retain a supported protected development-validation invocation. Broader RI or
compact Context-map disclosure remain separate decisions. No next increment
is begun by this checkpoint.
