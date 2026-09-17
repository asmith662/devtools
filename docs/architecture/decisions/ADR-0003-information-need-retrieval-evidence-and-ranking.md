# ADR-0003 — InformationNeed, retrieval evidence, and ranking semantics

- Status: Accepted
- Date: 2026-09-16
- Scope: semantic architecture for future InformationNeed, retrieval planning,
  bounded retrieval applications, ContextCandidates, RelevanceEvidence, and
  ranking. This decision authorizes no production retrieval, planner, index,
  ranker, Context compiler, graph algorithm, persistence, protocol, or test.

## Context

ADR-0002 establishes Repository identity, snapshots, Derivations,
DerivedKnowledge, validity, and repository-relationship graph semantics.
Those foundations permit deterministic repository intelligence, but do not say
what a consumer needs to know, how independent discovery mechanisms compose,
or how relevance is interpreted without conflating retrieval with Context
compilation.

Repository discovery must reduce costly model archaeology while preserving that
repository facts, relevance observations, ranking, and model-visible Context
are different semantic layers. A single universal relevance score or one
mandatory retrieval graph would lose evidence needed for replay, debugging,
comparison, and task-sensitive evolution.

## Decision

### InformationNeed

An **InformationNeed** is an immutable, purpose-relative description of
knowledge required by a consumer to reduce uncertainty. It is distinct from its
originating Task, a search query, retrieval operation or strategy, model Prompt,
Context, token budget, and mutable satisfaction state. A Task may yield zero,
one, or many InformationNeeds over time. Human, deterministic workflow,
planner, coding-worker/model, evaluation-fixture, and future-Agent origins are
provenance, not different InformationNeed semantics.

An InformationNeed may conceptually express a semantic description/question,
purpose, typed known anchors, desired information characteristics, constraints
on satisfying information, and provenance. This does not freeze a Python model
or exhaustive enum. Anchors preserve known clues as strongly typed references
when available—such as identifiers, repository entities/symbols, paths/resources,
documents, existing knowledge, or changes—and as plain text only when nothing
stronger is known. Exact anchor taxonomy remains open. An anchor does not select
a retriever: an identifier anchor does not require a SymbolRetriever.

InformationNeed constraints describe acceptable information, for example current
repository state, required tests, governing architecture, or production rather
than generated fixtures. They must not prescribe mechanisms such as BM25,
semantic search, PageRank, or a particular retriever. Mechanism choice belongs
to retrieval planning.

Needs never mutate. Changed uncertainty creates another need, with future
causal relationships such as decomposition, refinement after learning, or
arising from prior disclosure. A persistent NeedGraph is not required. Prior
disclosure and Context/model token budgets are not intrinsic to a need: the
same need can be satisfied differently for consumers with different prior
disclosure. Satisfaction is a separate assessment against available/disclosed
information; it may be deterministic, model/workflow/human judged, or evaluated
later. No satisfaction enum is selected.

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

**RelevanceEvidence** is typed, provenance-bearing, purpose-relative evidence
explaining why a ContextCandidate may or may not help satisfy an InformationNeed.
It must not be reduced during retrieval to `candidate + universal score`.
Potential observations include exact/identifier or lexical matches, definition
or reference observations, import/call/graph proximity, test,
documentation/governance, semantic-similarity, and change/history evidence;
these examples are not an exhaustive hierarchy.

Retriever-native measurements retain native meaning rather than becoming a
universal relevance score during retrieval: BM25, semantic similarity, graph
distance, exact-match truth, and reference count are not inherently comparable.
Retrieval preserves observations; an identified ranker later interprets them.
Evidence can support or oppose usefulness. Absence of supporting evidence is
not opposing evidence: a failed discovery can reflect incomplete retrieval or
index knowledge and must not silently claim irrelevance unless the operation's
semantics justify it. Epistemic confidence that an observation is correct is
separate from its task-specific ranking influence.

RelevanceEvidence obeys ADR-0002 provenance, dependency, and reproducibility
principles and may ultimately be a purpose-relative form of DerivedKnowledge.
This does not require literal Python inheritance. Reproducibility enables replay,
caching, debugging, comparison, evaluation, and controlled evolution; concrete
evidence, confidence, and polarity representations remain open.

### Retrieval planning and bounded applications

Retrieval planning is distinct from InformationNeed and execution. It answers:

> Which retrieval capabilities should be applied, with what bounded
> purpose-derived inputs, to investigate this InformationNeed?

A plan selects **applications** of capabilities, not merely retriever names.
For example, relationship retrieval can start from an established anchor with
selected relationship families and bounded traversal; lexical retrieval can use
purpose-derived terms; exact retrieval can use an identifier anchor. Future
planner-produced query material—terms, anchors, families, query forms, and
scopes—retains provenance through a planning derivation. It is hypothesis/query
material, not repository fact when it proposes an unestablished entity.

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

### Ranking and Context boundary

**Ranking** is a distinct semantic stage that interprets an InformationNeed,
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

Future evaluation must be able to reproduce and correlate RepositorySnapshot,
InformationNeed, planning semantics/applications, derivations, candidates,
evidence, ranking, later selection/representation/disclosure, and model/task
outcome. This permits controlled comparisons of rankers over fixed evidence,
retrieval portfolios under fixed ranking, or Context compilers over fixed ranked
candidates, without selecting storage or experiment infrastructure.

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
high-value initial disclosure, expose remaining uncertainty, and create/refine
another InformationNeed for targeted discovery. This does not excuse poor
initial retrieval; initial and eventual acquisition quality remain separately
measurable. Orchestration of repeated acquisition stays above deterministic
retrieval and Context compilation; retrieval is not an autonomous Agent.

Repository information and RelevanceEvidence remain data, not execution
authority. Existing model Tool/proposal/materialization/validation/
authorization/execution boundaries remain authoritative. Retrieval planning
does not grant capability or collapse into Tool authorization or execution.

## Deferred and open pressure

This ADR does not select concrete InformationNeed, anchor, addressed-request,
Retriever, CandidateProducer/EvidenceProducer, planner, plan-identity or
persistence, application-DAG, scheduler, bound, lexical, graph, semantic,
embedding, historical-retrieval, evidence, confidence, polarity, normalization,
deterministic-ranking, learned-ranking, task-classification, wave-policy,
evidence-cache/persistence, evaluation-storage, or metric implementations.

## Status and implementation boundary

This decision settles semantic architecture only. B-0002 retains unimplemented
repository-intelligence, retrieval, Context-selection/compilation, progressive-
disclosure, and evaluation pressure. ADR-0002 remains responsible for identity,
snapshots, derivation, DerivedKnowledge validity, and graph-semantic foundations.
Nothing here creates a production API, retrieval system, planner, ranker,
Context compiler, graph algorithm, persistence model, Agent loop, Runtime
responsibility, or test requirement.
