# ADR-0003 — InformationNeed, retrieval evidence, and ranking semantics

- Status: Accepted
- Date: 2026-09-16
- Evidence amendments: 2026-09-22 (Increment 22 purpose-relative admission),
  2026-09-22 (Increment 23 independent blinded validation)
- Scope: semantic architecture for future InformationNeed, retrieval planning,
  bounded retrieval applications, ContextCandidates, RelevanceEvidence, and
  ranking, including bounded purpose-relative admission and abstention. This
  decision authorizes no production retrieval, planner, index, ranker,
  admission policy, Context compiler, graph algorithm, persistence, protocol,
  or test.

## Research reconciliation

The [purpose-relative Context research](../../research/purpose-relative-repository-context.md),
[repository Context-system research](../../research/repository-context-system-architecture.md),
[adversarial review](../../research/architecture-adversarial-review.md), and
[retrieval synthesis](../../research/retrieval-architecture-synthesis.md) support
this boundary. They, plus Increments 16, 20, 21, and 22, preserve:

> repository relationship truth != surfaced retrieval evidence !=
> purpose-relative admission != Context disclosure

InformationNeed is not query text; repository truth is not retrieval evidence;
candidate surfacing is not final selection; and evaluation remains distinct from
the mechanism evaluated. Increment 16 found filesystem/path geometry inadequate
as purpose-relative ranking evidence. Increment 20 found true resolved import
relations could expose lexical misses but direct fixed-K insertion could expose
controls and displace relevant lexical resources. Increment 21 established
purpose-relative oracle headroom and a same-query/different-purpose
counterexample, but no realizable decision policy. Increment 22's frozen,
precommitted directional-reservation rule improved its eight held-out cases
without removing a judged-relevant lexical result and abstained on three cases.
That result is evidence for a purpose-bearing admission operation, not proof
that the concrete rule generalizes or is production-ready: only one held-out
run exists, two admissions remain unjudged, and no explicit negative control
reached an eligible directional surface.

Increment 23 independently adjudicated six new cases and confirmed the semantic
separation while pressuring the concrete rule. Canonical and practical top five
each recovered 10 of 18 known-useful material resources: the rule recovered one
useful relationship target but displaced one useful lexical rank-five resource,
and its other admission was not useful. Ten of 96 material judgments remain
`UNJUDGED`, so final Recall/MRR claims are bounded. Lexical top fifteen contained
all 18 known-useful resources; relationship surfaces exposed only one useful
resource beyond top five. This evidence rejects shadow readiness and production
promotion for the concrete rule without rejecting purpose-relative decision
semantics or heterogeneous retrieval.

Accordingly, the architecture accepts purpose-relative admission and explicit
abstention as possible bounded decision semantics while leaving their concrete
policy and owner-specific representation open. There is still no universal
Candidate, CandidateEvidence, relevance-score normalization, first-class
Selector, standalone Selection domain, production relationship
expansion/scoring, or source/test weighting/suppression.
Source/test classification may be useful evidence for a particular InformationNeed,
but location alone does not establish purpose-relative relevance.

An experiment's expected control label is also not repository truth or
authoritative relevance truth. Increment 23 preserved a blinded `USEFUL`
judgment that conflicted with an expected negative control, then separately
reviewed the now-unblinded resource and found the control expectation
unsupported for the exact InformationNeed. Control expectation, independent
usefulness judgment, and post-unblinding disposition must remain distinguishable
when they disagree; none may silently rewrite the others.

Revisit a reusable admission/selection abstraction only with broader,
independently evaluated evidence showing stable need-specific value that cannot
remain operation-local or within Context planning.

## Context

ADR-0002 establishes Repository identity, snapshots, Derivations,
DerivedKnowledge, applicability, and repository-relationship graph semantics.
Those foundations permit deterministic repository intelligence, but do not say
what a consumer needs to know, how independent discovery mechanisms compose,
or how relevance is interpreted without conflating retrieval with Context
compilation.

Repository discovery must reduce costly model archaeology while preserving that
repository-intelligence results, relevance observations, ranking, and model-
visible Context are different semantic layers. A single universal relevance
score or one mandatory retrieval graph would lose evidence needed for replay,
debugging, comparison, and task-sensitive evolution.

## Decision

### InformationNeed

An **InformationNeed** is the conceptual, purpose-relative distinction for
knowledge desired by a consumer to reduce uncertainty. It is distinct from its
originating Task, a search query, retrieval operation or strategy, model Prompt,
Context, token budget, and satisfaction. A Task or current reasoning state can
give rise to zero, one, or many information purposes over time. Human,
deterministic-workflow, planner, coding-worker/model, evaluation-fixture, and
future-Agent origins are provenance, not different InformationNeed semantics.

This semantic distinction does not require an independently identified,
durable, immutable runtime artifact, standalone lifecycle, persistent need
graph, or persistence outside a planning/acquisition episode. A future
implementation may establish that an explicit identified InformationNeed model
is useful, but its identity and lifecycle must earn that cost through evidence.
This supersedes the stronger assumption that reproducibility, decomposition,
progressive acquisition, or retrieval evaluation require every purpose-relative
information demand to be an independently identified immutable artifact.

An information purpose may conceptually involve a semantic description/question,
typed known anchors, desired information characteristics, constraints on
satisfying information, and causal provenance. Planning/application structures
may eventually carry or reference those facts along with planner-derived query
material, bounds, strategy, and refinement/decomposition provenance; this does
not assign every fact to one model or freeze a Python representation. Anchors
preserve known clues as strongly typed references
when available—such as identifiers, repository entities/symbols, paths/resources,
documents, existing knowledge, or changes—and as plain text only when nothing
stronger is known. Exact anchor taxonomy remains open. An anchor does not select
a retriever: an identifier anchor does not require a SymbolRetriever.

Information-purpose constraints describe acceptable information, for example
current repository state, required tests, governing architecture, or production
rather than generated fixtures. They must not prescribe mechanisms such as
BM25, semantic search, PageRank, or a particular retriever. Mechanism choice
belongs to retrieval planning, and purpose remains distinguishable from
mechanism-specific query material.

Changed uncertainty, acquired information, or prior disclosure can justify a
later purpose, refinement, or decomposition. Causal/provenance relationships
should remain available where needed without requiring mutable evolution of one
need artifact or a persistent tree of child artifacts. Prior disclosure and
Context/model token budgets are not intrinsic purpose semantics: the same
purpose can be approached differently for consumers with different available
information. Satisfaction is a separate assessment against available/disclosed
information; it may be deterministic, model/workflow/human judged, or evaluated
later. No satisfaction representation or assessor is selected.

Semantic discovery is distinct from exact addressed acquisition. When a known
resource, region, symbol, or knowledge artifact is already exactly addressed,
future architecture may resolve it through a bounded direct path rather than
forcing relevance discovery. Exact naming and API remain open.

### Candidates and relevance evidence

A **ContextCandidate** identifies an addressable repository-intelligence
referent that may help satisfy an InformationNeed. The referent can be a
RepositorySubject, ResourceOccurrence, SourceOccurrence, DerivedKnowledge, or
another future addressable referent under ADR-0002 semantics. It does not
prescribe final model-visible representation. Discovering a symbol does not
decide whether later Context
discloses its name, signature, documentation, body, containing class, source
region, summary, or relationship neighborhood.

Candidates may address resource occurrences, source occurrences/regions,
RepositorySubjects, relationships, DerivedKnowledge, and other future
referents. Their equivalence follows the underlying addressed identity rather
than arbitrary retrieval-result UUIDs, so independent discoveries of the same
referent can accumulate evidence. Different granularities remain distinct
candidates: a file, contained symbol, and source region do not automatically
collapse.
Overlap/deduplication is Context selection/compilation work, not retrieval.

**RelevanceEvidence** is the semantic concept for typed, provenance-bearing
retrieval observations relevant to assessing why a ContextCandidate may or may
not help satisfy an information purpose. It is neither universal relevance
truth, a universal normalized score, a ranking decision, nor final
Context-selection utility. Potential observations include exact/identifier or
lexical matches, definition or reference observations, import/call/graph
proximity, test, documentation/governance, semantic-similarity, and
change/history evidence; these examples are not an exhaustive hierarchy.

This semantic distinction does not require every observation to have independent
global identity, a standalone lifecycle or persistence, repository-snapshot
ownership, repository-level applicability, a dedicated cache abstraction, or a
mandatory immutable artifact representation. Evidence can be represented within
or alongside retrieval execution/results when that preserves the required
semantics. A future representation may earn independent identity, persistence,
or reuse through evidence; none is required now.

Retriever-native measurements retain native meaning rather than becoming a
universal relevance score during retrieval: BM25, semantic similarity, graph
distance, exact-match truth, and reference count are not inherently comparable.
Multiple independent retrieval applications may contribute observations for the
same candidate; composition must preserve evidence type, originating mechanism/
application, native measurement semantics, provenance, and relevant qualifiers
rather than averaging them into one truth score. An ephemeral candidate-centered
grouping is permitted; a persistent independently identified aggregate is not
required. An identified ranker later interprets the preserved observations.

Evidence can support or oppose usefulness when the observation semantics justify
that polarity. Absence of supporting evidence is not opposing evidence: a failed
discovery can reflect incomplete retrieval or index knowledge and must not
silently claim irrelevance. Likewise, a low measurement is opposing evidence
only when its own semantics support that conclusion. Measurement certainty or
confidence, evidence strength, task-specific ranking influence, and relevance
truth remain distinct; no universal confidence, polarity, or ranking-policy
representation is selected.

Repository knowledge used by retrieval can be ADR-0002 DerivedKnowledge, while a
purpose-relative traversal, hit, score, or candidate observation is not
automatically repository DerivedKnowledge merely because it is deterministic,
provenance-bearing, or reproducible. Such observations may depend on, cite, or
be supported by DerivedKnowledge without sharing its identity, applicability,
or persistence semantics. This preserves a future evidence type with genuinely
reusable derived semantics without making DerivedKnowledge a universal container
for retrieval data. Recordability and replayability likewise do not require
standalone evidence identity: evidence may be ephemeral or retained within an
execution/evaluation record when useful. Concrete evidence, aggregation,
confidence, polarity, persistence, replay, and caching representations remain
open.

### Retrieval planning and bounded applications

Retrieval planning is distinct from information purpose and execution. It answers:

> Which retrieval capabilities should be applied, with what bounded
> purpose-derived inputs, to investigate this information purpose?

A plan selects **applications** of capabilities, not merely retriever names.
For example, relationship retrieval can start from an established anchor with
selected relationship families and bounded traversal; lexical retrieval can use
purpose-derived terms; exact retrieval can use an identifier anchor. Future
planner-produced query material—terms, anchors, families, query forms, and
scopes—retains provenance through a planning derivation. It is hypothesis/query
material, not established repository knowledge when it proposes an unestablished
entity.

Graph retrieval consumes ADR-0002 typed graph views and shared graph mechanics
as repository intelligence. A purpose-relative traversal selects compatible
relationship families and bounded traversal constraints; its reached candidates,
path, distance, and relationship observations remain RelevanceEvidence rather
than automatically becoming repository DerivedKnowledge.

Planning may later be deterministic, learned, model-assisted, or hybrid. This
ADR freezes none of `Retriever`, `RetrievalPlan`, `RetrievalApplication`, or a
planner implementation shape.

Retrieval is bounded independently of Context/model token budgeting. Candidate
count, graph depth, relationship families, repository scope, resource kinds,
time/compute, and other work bounds may constrain discovery. Retrieval bounds
control discovery work; Context budgets control later disclosure. Repository
intelligence must not become unbounded analysis by default.

Independent retrieval applications may execute concurrently. Ordering is needed
only when an application depends on results established by another. Future
planning/execution may therefore express a bounded application dependency DAG,
without selecting a scheduler, task framework, concurrency primitive, or DAG
representation. Conditional waves are also enabled: cheap/high-confidence
applications may run first, followed by structural/relationship or broader
semantic/history applications only when evidence/coverage justifies them.
Within a wave, independent applications may run concurrently. Wave contents are
not policy; the accepted principle is progressive expected-information-gain
against cost and latency rather than running every mechanism indiscriminately.

Repository discovery is intentionally multi-strategy. Exact/identifier,
lexical, symbol/structural, relationship/graph, optional semantic,
change/history, and future mechanisms may independently contribute evidence
for one candidate. Import, reference, call, test, documentation, governance,
and change-impact views may likewise contribute together. No mechanism, graph,
or pipeline owns repository relevance, and independent evidence must not erase
or overwrite other evidence.

The evidence families remain deliberately heterogeneous. Semantic retrieval may
later consume a pretrained representation model to produce a semantic-similarity
observation; that is distinct from training a ranking or decision model. A
future learned policy may interpret retained native observations, but neither a
pretrained representation nor learned ranking changes Repository Intelligence
truth, supplies a universal score, or is selected by this ADR. The current
devtools-only lexical, import, admission, and offline-ranking experiments are
local evidence, not a general portfolio ordering or a claim that lexical width
is generally sufficient. Independent-repository evaluation is required before
strong retrieval or ranking conclusions; a non-controlling shadow comparison,
if ever justified, follows offline and independent evaluation rather than
becoming a retrieval mechanism itself.

### Purpose-relative admission and abstention

When a bounded decision chooses whether surfaced information may consume scarce
consideration or disclosure capacity, the information purpose must be available
as an explicit input or an explicitly referenced fact. Query text alone is not
sufficient: Increment 22 retained identical `Context disclosure` query text and
lexical ranking while its frozen local/governance purpose abstained and its
implementation-oriented purpose admitted incoming relationship evidence. This
does not require a separate durable `Purpose` object or enum; InformationNeed
already owns the semantic distinction, and an operation-specific projection can
carry only the purpose facts that its policy actually uses.

Admission is a purpose-relative bounded decision over surfaced native evidence;
it is not proof of relevance or usefulness, and it need not assign a normalized
score or total order. An admission policy may explicitly abstain when its
purpose makes the mechanism inapplicable or its evidence does not satisfy the
policy. Abstention is an outcome to retain and evaluate, not missing data or
proof that the unchanged result is correct. Capacity reservation can reduce the
destructive behavior of blind fixed-K insertion, but one zero-loss held-out run
does not establish a general safety property.

These semantics do not require an `Admission`, `Selector`, or `Selection`
domain artifact. A retrieval procedure or Context planner may make a local
decision while preserving the surfaced evidence, purpose basis, capacity
condition, decision, and abstention reason needed for evaluation. The
Increment 22 directional-reservation-v1 policy remains experimental; no
relationship expansion or admission policy is promoted to production by this
decision.

### Ranking and Context boundary

**Ranking** is a distinct semantic stage that interprets an information purpose,
ContextCandidate, accumulated RelevanceEvidence, and identified ranking
semantics/policy to produce comparative relevance or ordering. It does not
destroy, overwrite, or replace evidence. Different deterministic or learned,
task-conditioned rankers must be able to assess the same candidate/evidence
set. Learned ranking is enabled, not selected; fixed weights and task
classification are open.

Ranking remains distinct from Context selection. Retrieval discovers candidates
and evidence; ranking interprets relative value; Context selection chooses a
combination of candidates and representations for disclosure under constraints.
A high-ranked symbol, containing class, and file need not all be disclosed.
Representation, overlap resolution, deduplication, novelty, diversity,
budgeting, and ordering remain Context compilation concerns.

Evidence usefulness can vary by need: exact/symbol observations can be strong
for localization, documentation/relationships for architecture questions, and
tests/change/reference/history for regression investigation. Native evidence
semantics preserve one input surface for both deterministic and future learned
rankers rather than prematurely fixing universal normalization.

### Evaluation, progressive disclosure, and authority

Future evaluation must be able to reproduce and correlate the assessment basis
required by its claim: potentially RepositorySnapshot and relevant external or
intelligence conditions, acquisition/information purpose, planning semantics/
applications, derivations, candidates, evidence, ranking, later selection/
representation/disclosure, and model/task outcome. Repeatable benchmark-style
work can use a stable evaluation-case reference containing Task, purpose,
anchors, constraints, or expected semantics, but neither a universal
`EvaluationCase` nor runtime InformationNeed identity is required. Intended
experimental condition remains distinct from base assessment basis,
configuration, realization, and outcome; a scoped fixture/configuration can
represent these distinctions without a universal `Treatment` entity.

This permits controlled comparisons of rankers over fixed retrieval
observations, retrieval portfolios under fixed ranking, or Context compilers
over fixed ranked candidates, without selecting storage or experiment
infrastructure. Recordable observations can support replay, debugging,
controlled comparison, provenance inspection, and retriever marginal-
contribution analysis without requiring standalone RelevanceEvidence identity
or mandatory persistence. Retrieval observations and evaluator judgments
retain their own semantics rather than becoming repository DerivedKnowledge.

Provenance/observability must eventually distinguish retrieval failure (useful
information never a candidate), ranking failure (candidate ranked too poorly),
selection failure (adequately ranked candidate excluded), representation failure
(right subject, wrong/insufficient detail), budget/disclosure failure, and
model-utilization failure (correct information reaches the model but is not used).
It must also permit absolute and marginal/unique retriever contribution evidence:
candidates/useful candidates produced, uniquely produced value, evidence
contribution, and latency/compute cost. This future evidence may inform
identifiable, replaceable, evaluable, governable adaptive planning; it does not
authorize uncontrolled self-modification.

Initial Context need not achieve perfect recall. A consumer may receive
high-value initial disclosure, expose remaining uncertainty, and justify a
later/refined information purpose or acquisition episode for targeted discovery.
This does not excuse poor
initial retrieval; initial and eventual acquisition quality remain separately
measurable. Orchestration of repeated acquisition stays above deterministic
retrieval and Context compilation; retrieval is not an autonomous Agent.

Repository information and RelevanceEvidence remain data, not execution
authority. Existing model Tool/proposal/materialization/validation/
authorization/execution boundaries remain authoritative. Retrieval planning
does not grant capability or collapse into Tool authorization or execution.

### Increment 23 independent-validation evidence

The retained report uses schema
`devtools-b0002-purpose-relative-independent-validation-v1`. Increment 23
separated judgment-free capture, a corrected v2 structural blinded projection,
immutable usefulness judgments, authorized unblinding, control annotation, and
mechanism evaluation. The invalid v1 package remains preserved because its raw
source projection exposed expected judgments and control semantics. A frozen
blinded judgment contains neither resource address nor control truth; those
facts enter only after its fingerprint is fixed.

Across six cases, 86/96 material resources received definitive judgments and 10
remain `UNJUDGED`. Canonical and directional top five each recover 10/18 known-
useful resources. Their exact known-hit rate is `1.0`; unresolved evidence bounds
macro Recall@5 to `[0.5111, 0.7202]` and MRR to `[0.5389, 0.8889]` for both
arms. Directional reservation makes two admissions with precision `0.5`: one
useful and one not useful. It displaces two rank-five resources, including one
useful resource, producing one useful recovery and one useful loss rather than
a net known-useful gain. Protected ranks one through four record no loss.

Lexical top fifteen contains all 18 known-useful material resources, eight more
than top five. Relationship surfaces contain eight candidates: two useful and
six not useful; only one useful relationship resource is beyond lexical top
five. Qualification passes one useful and two not-useful candidates, so the
two-support threshold is not an adequate relevance discriminator on this set.
No paired oracle result was retained, and none is fabricated.

The concrete rule is `NOT_READY_FOR_SHADOW` under its frozen readiness criteria:
coverage is incomplete, no validated negative control reaches the relationship
surface, one not-useful admission occurs, and one useful rank-five resource is
lost. Production promotion is not justified. The next evidence step is a
stronger bounded candidate/ranking comparison, not threshold tuning of this
sole reservation slot. This does not retract the purpose-relative decision
boundary or select a universal selector.

### Increment 24 offline ranking evidence

The retained Increment 24 report uses schema
`devtools-b0002-purpose-relative-ranking-comparison-v1`. It compares frozen,
judgment-free Increment 23 material surfaces with labels joined only by the
offline evaluator. On six devtools InformationNeeds, all 18 known-useful
resources are present in lexical top fifteen, while canonical top five recovers
10. A predeclared purpose-relative deterministic ordering recovers 9 and
selects three more known-not-useful resources than the lexical/native baseline.
Typed import evidence therefore does not add demonstrated ranking value on this
surface, and no lightweight learned ranking result is estimated: six grouped
needs do not support a non-leaking train/evaluation split.

This is repository-local descriptive evidence, not a selection of a ranking
policy or a change to the accepted ranking boundary. It reinforces that ranking
must be evaluated separately from surfacing, but does not justify production
ranking, shadow execution, universal feature normalization, or a Selector.
Cross-repository evidence remains required before architectural closure.

## Deferred and open pressure

This ADR does not select concrete purpose/InformationNeed representation or
whether explicit need identity proves useful; anchor, addressed-request,
decomposition/refinement or causal-provenance representation; Retriever,
CandidateProducer/EvidenceProducer, planner, plan-identity or
persistence, application-DAG, scheduler, bound, lexical, graph, semantic,
embedding, historical-retrieval, evidence, confidence, polarity, normalization,
deterministic-ranking, learned-ranking, task-classification, wave-policy,
purpose projection, admission policy/representation, candidate/evidence
association, measurement taxonomy, cross-retriever
aggregation, evidence-cache/persistence, evaluation-case or execution-record
identity, evaluation-storage, or metric implementations.

## Status and implementation boundary

This decision settles semantic architecture only. B-0002 retains unimplemented
repository-intelligence, retrieval, Context-selection/compilation, progressive-
disclosure, and evaluation pressure. ADR-0002 remains responsible for identity,
snapshots, derivation, DerivedKnowledge applicability, and graph-semantic
foundations. Nothing here creates a production API, retrieval system, planner,
ranker, admission policy, Context compiler, graph algorithm, persistence model,
Agent loop, Runtime responsibility, or test requirement.
