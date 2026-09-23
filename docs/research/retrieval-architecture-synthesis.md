# Retrieval Architecture Synthesis and Research-Recovery Checkpoint

## Purpose

This is durable research synthesis, not an ADR and not implementation
authorization. It reconciles the recovered research corpus, accepted ADRs,
current source, B-0002's empirical lineage, the retained Increment 22 Pass 4
report at `251e290c985d1b93aa97b346ee44dbb949f21932` (2026-09-22), and the
retained Increment 23 independent-validation report. Its purpose is to keep
both positive and negative retrieval/Context findings recoverable and to
interpret the frozen decision-rule evidence. It does not authorize a
Selector, Candidate framework, graph store, vector system, learned ranker,
shadow runtime, or Context redesign.

The governing hierarchy remains: research evidence -> ADR disposition ->
accepted architecture -> implementation -> empirical evaluation. A later layer
can constrain an earlier proposal; it cannot erase the earlier evidence.

## Sources reviewed

Full-body review covered the research index and every indexed canonical body:

- [Architecture adversarial review](architecture-adversarial-review.md),
  [Framework domain boundaries](framework-domain-boundaries.md),
  [Purpose-relative repository Context](purpose-relative-repository-context.md),
  [Repository Context system](repository-context-system-architecture.md),
  [Derived knowledge boundary](repository-derived-knowledge-boundary.md),
  [Repository information boundaries](repository-information-boundaries.md),
  [Repository intelligence review](repository-intelligence-architecture-review.md),
  [Snapshot identity](repository-snapshot-identity.md),
  [Subject identity](repository-subject-identity-and-decomposition.md), and
  [Runtime Evidence governance](runtime-evidence-governance.md).
- [ADR-0001](../architecture/decisions/ADR-0001-cohesive-model-interaction-boundary.md),
  [ADR-0002](../architecture/decisions/ADR-0002-repository-intelligence-identity-and-derivation.md),
  [ADR-0003](../architecture/decisions/ADR-0003-information-need-retrieval-evidence-and-ranking.md),
  and [ADR-0004](../architecture/decisions/ADR-0004-context-disclosure-planning-and-assembly.md).
- [Architecture](../architecture.md), [documentation map](../documentation_map.md),
  [roadmap](../roadmap.md), and the complete [B-0002 epic](../backlog/epics/B-0002-coding-context-substrate.md).

Targeted implementation inspection covered `context.repository`,
`context.retrieval.lexical`, `context.python.function`,
`context.python.modules`, and `context.python.imports`, including the exact
name retrieval/disclosure/materialization path, BM25 and filename-field code,
module interpretation, import resolution, and declaration-grounded relations.
Targeted experiment inspection covered identifier decomposition/address lexical
work, structural expansion, import-relationship comparison/cases, and the
purpose-relative oracle comparison/cases. Increment 22 inspection covered the
frozen design/tests and
[retained Pass 4 report](../../.b0002-purpose-relative-admission-rule.json).
Increment 23 inspection covered its frozen validation design, invalidated v1
projection, corrected v2 blinded package, immutable adjudication, and
[independent-validation report](../../.b0002-purpose-relative-independent-validation.json).
Neither capture nor the rule was rerun or tuned.

## Historical retrieval trajectory

The evidence sequence is cumulative rather than a replacement of old work by
the newest result.

1. The real-repository BM25 baseline established a deterministic, inspectable
   content lexical reference point, not universal retrieval sufficiency.
2. Identifier decomposition improved some identifier-boundary cases but lost a
   multi-resource case; it remains experiment-only.
3. Address experiments separated filename stems from directories/full paths.
   Filename stems improved the paired and robustness sets. The promotion gate
   selected a fixed `0.25` filename-field weight; full-path/directory scoring
   was not promoted.
4. Increment 16 tested raw same-parent/directory distance. It produced no
   fixed-capacity recovery and displaced relevant resources. This falsifies a
   default filesystem-proximity prior, not structural retrieval in general.
5. Function declarations, module interpretation, import declarations, qualified
   resolution, and directed declaration-grounded import relations established
   useful Repository Intelligence. They are facts/qualified results, not
   retrieval relevance.
6. Increment 20 showed that outgoing and incoming relation expansion can surface
   lexical misses, but also exposes explicitly irrelevant controls; blind
   fixed-K insertion degraded results. Relationship truth is therefore not
   admission truth, and direction/provenance must survive.
7. Increment 21 froze twelve purpose-relative needs, including a same-query,
   different-purpose pair. Lexical top-five useful recall was `0.5278`; lexical
   width fifteen had oracle size-five recall `0.7986`; outgoing/bidirectional
   one-hop surfaces reached `0.9167`; incoming did not improve beyond lexical
   width. Blind bidirectional insertion was `0.3889` with five controls. This
   establishes consideration and oracle headroom, not an implementable policy.
8. Increment 22 froze a purpose-profile/direction mapping, two-distinct-support
   threshold, one rank-five reservation, and explicit abstention before one
   held-out run. Across eight held-out cases, directional reservation improved
   Hit@5 from `0.6250` to `0.8750`, mean Recall@5 from `0.4167` to `0.5625`,
   and MRR from `0.3333` to `0.3833`. It admitted five resources, three judged
   relevant and two unjudged; recovered three new relevant resources; and lost
   no previously retrieved relevant resource. It abstained twice by local
   profile and once for no qualifying target. No explicit control reached an
   eligible surface, so negative rejection remains untested. This establishes
   practical held-out evidence for the purpose-bearing admission boundary, not
   production readiness of the rule.
9. Increment 23 independently captured six cases and adjudicated 96 material
   resources through a corrected structural blinded projection. It retained 18
   useful, 68 not-useful, and 10 unjudged judgments. Canonical and directional
   top five each recovered 10/18 known-useful resources: the rule recovered one
   useful relationship target but displaced one useful lexical rank-five
   resource, and its second admission was not useful. Lexical top fifteen
   contained all 18 known-useful resources. One expected negative control was
   independently judged useful; post-unblinding review preserved both labels
   and found the control expectation unsupported for the exact need. The rule
   is not ready for shadow or production promotion.

## Current production state

### Production retrieval

The only general ranked production retrieval is bounded BM25 over whole
observed repository-text documents:

- content lexical BM25, with Unicode `\\w+` observations and casefolding;
- an independently indexed final filename-stem BM25 field at fixed `0.25`;
- separate retained content, filename, and term-contribution evidence; and
- positive-score, document-order-tie-broken results under an explicit bound.

Directories and full paths are not scored. Identifier decomposition is not in
this path. There is no production semantic/vector retrieval, learned ranker,
relationship expansion, graph traversal, model-directed retrieval, shadow
mode, source/test heuristic, or generic ranking/selection mechanism.

There is also a narrow production exact route: exact equality lookup over
caller-supplied direct module-body Python function declaration knowledge. It
returns all matching declarations in supplied order with typed exact-match
evidence, can project supporting distinct resources, and has an all-match
declaration disclosure/materialization/rendering/assembly path. It is not a
repository-wide symbol service, overload resolver, generic direct-resource
retriever, or general Context planner. `RepositorySnapshot.resource_at` is an
exact addressed acquisition primitive, not relevance discovery.

### Current Repository Intelligence substrate

Implemented, bounded deterministic substrate includes logical repository and
snapshot/resource/content identities; recursive address discovery; caller-
selected UTF-8 observation; corpora and whole-resource documents; lexical
observations/statistics/indexes; direct module-body Python function declaration
knowledge and source occurrences; direct import declarations; explicit-root
module interpretations; qualified import-resolution outcomes (`resolved`,
`unresolved-in-universe`, `ambiguous`, `unsupported`); and one directed
source-module-to-uniquely-resolved-target relation per qualifying declaration.

This does **not** establish runtime import behavior, generic symbols, calls,
tests-to-code links, a universal graph, or a general repository snapshot policy.
Relationship facts and their source/declaration provenance can support a future
retriever, but are not themselves a retriever.

## Intended heterogeneous portfolio

ADR-0003 accepts a portfolio, not a mandatory pipeline: exact/identifier,
lexical, symbol/structural, typed relationship/graph, optional semantic,
change/history, and future mechanisms may independently surface typed evidence.
ADR-0002 makes typed graph views a future Repository Intelligence capability;
ADR-0004 makes final disclosure representation-aware. The portfolio's current
dispositions are:

- **Exact/direct resource or fact resolution:** architecturally accepted as a
  distinct path when a resource, region, symbol, or knowledge artifact is
  already addressed. Narrow exact-name lookup is implemented. Revisit broader
  lookup only with a concrete address/subject family and a consumer.
- **Lexical:** production baseline and durable evaluation reference; keep its
  native evidence rather than treating it as relevance truth.
- **Path/address:** filename stem is production lexical evidence; full path,
  directory proximity, and package proximity are constrained/deferred.
- **Symbol/declaration:** narrow direct function-name lookup is production;
  richer subject/declaration/reference lookup is accepted future pressure.
- **Typed relationship views:** accepted Repository Intelligence semantics;
  import relations are implemented knowledge and experiment-only surfacing.
  Future traversal must be typed, directed, bounded, and purpose-derived.
- **Semantic/vector:** durable research support for an optional later family,
  but no ADR selection or local evaluation. It needs an honest representation
  unit, frozen tasks where lexical cues are weak, a model/index version and
  cost basis, comparison with lexical/direct/relationship baselines, and
  held-out evidence before promotion.
- **Model-directed/iterative:** accepted as a future possible planning or
  progressive-acquisition implementation, not Runtime ownership and not a
  current agent loop. Cheap independent applications may be concurrent; later
  waves require evidence/coverage justification.
- **Learned fusion/ranking:** enabled but explicitly unselected. It belongs in
  a particular retrieval or Context-planning policy according to its target,
  not in Repository Intelligence and not in a universal score abstraction.

## Semantic/vector retrieval boundary

Semantic/vector retrieval remains a research-supported optional family, not an
accepted production mechanism. Existing progress establishes better lexical and
relation evaluation discipline, but not that embeddings improve this repository
or what unit should be embedded. An honest experiment must freeze needs that
expose lexical/direct failure, make unit/chunk and model/index versions
explicit, compare against lexical/direct/typed-relation controls under equal
consideration and disclosure cost, and use held-out cases. No vector database,
embedding cache, or reranker follows from the current headroom.

## Exact/direct lookup boundary

Retrieval is not always required. ADR-0003 explicitly distinguishes semantic
discovery from exact addressed acquisition. If a need already identifies a
resource, region, declaration, relationship, or established knowledge artifact,
direct resolution can bypass relevance discovery. This is meaningful because it
has different evidence, cost, and failure semantics; it does **not** authorize a
universal router or imply that a string resembling an identifier is exact.

The recovery finding is that the distinction is preserved more strongly than a
generic "skip retrieval" claim. Increment 22's two controls each resolved one
exactly named function resource and performed no heterogeneous K=5 admission.
That strengthens the direct-versus-discovery distinction without establishing
a safe generic eligibility threshold or universal router. Purpose-policy
abstention is separately accepted as decision semantics, not as evidence that
all skipped retrieval is correct.

## Relationship/graph boundary

Increment 16's raw geometry and Increment 20's declaration-grounded imports
answer different questions. The former rejects raw filesystem proximity as a
default relevance signal. The latter establishes a real qualified relationship
family and shows it can increase surfacing headroom while causing controls.
Neither supports an undirected adjacency score, universal graph, graph store,
or relationship insertion rule.

ADR-0002 resolves the prior research disagreement in favor of multiple typed
relationship/graph views, not one canonical graph. A graph view is a projection
over qualified relationship knowledge; it can be an index, adjacency structure,
or on-demand projection. Its node domain and traversal limits are view-specific.
The derivation dependency graph remains distinct from repository relationships.

## Purpose-relative decision and Context disclosure

The cumulative evidence supports this minimum distinction:

```text
repository proposition
!= surfaced/considered evidence
!= purpose-bearing bounded admission/abstention
!= representation-aware disclosure
```

These are causal/evaluation distinctions, not a requirement for four domains or
types. A benchmark usefulness judgment is not itself a production stage, and
Increment 22's reservation combines its local priority and capacity allocation
rather than proving that ranking must be a separate reusable component.
Increment 21 established that purpose can change judged usefulness while
lexical input/ranking and repository state remain unchanged, that a
heterogeneous universe contains better possible five-resource subsets, and
that blind expansion is inadequate. Increment 22 shows that one precommitted
purpose-bearing rule can realize some of that headroom while abstaining and
preserving judged-relevant lexical results on its held-out set. Neither proves
a scalar score, Selector class, universal Candidate, production policy, or
general no-loss property.

Purpose must therefore be explicitly available to a decision that conditions
on it, but `InformationNeed` already owns that semantic fact. The experiment's
`PurposeProfile` is a temporary three-value projection used by one rule; it is
not a production intent ontology. An operation-specific policy/value can carry
the exact purpose facts it needs without a durable purpose identity, public
enum, universal admission model, or Selection domain.

## Increment 22 evidence interpretation

The retained report uses schema
`devtools-b0002-purpose-relative-admission-rule-v1` and frozen design
fingerprint
`7e215ac2961a4329074e9a25d35d3decc554f394435aa0b73cb2251254160345`.
Its held-out improvement establishes that this particular precommitted rule
realized useful relationship-candidate headroom on this set. It supports the
architectural separation between surfacing and purpose-bearing decision. It
does not establish production readiness, cross-repository generalization, or
that this is the right policy.

All admissions protected lexical ranks one through four and replaced only rank
five. None of the five displaced rank-five resources was judged relevant, so
the practical arm recorded zero relevant displacements and zero previously
retrieved relevant losses. This is materially different from the destructive
fixed-K insertion observed in Increments 16 and 20, but it is conditional on
these cases and judgments; a future case can have a relevant resource at rank
five.

Three of five admitted resources were judged useful. The other two are
explicitly `unjudged`, not known irrelevant. Their contribution cannot be
classified without judgments against the complete InformationNeed and existing
Context, ideally including whether they add information beyond the already
retrieved resources. Conversely, no explicit negative control reached an
eligible directional surface. Zero control admissions therefore says nothing
about whether the two-support threshold rejects a known negative once eligible.

The two local-profile abstentions and one no-qualifying-target abstention are
rule outcomes, not missing observations. They demonstrate that a bounded policy
can decline to spend its reserved slot. They do not prove correctness: one
no-target abstention preserved a miss, and the local cases merely show what the
frozen purpose projection did.

The two `Context disclosure` cases hold query text and lexical ranking fixed.
The local-definition/governance profile abstained, while the
incoming-consumer-or-test profile admitted incoming evidence. This supports the
claim that query text does not fully determine a purpose-relative decision and
that purpose must be available separately. It does not validate either profile
as a production taxonomy, prove the architecture case should always abstain, or
show the implementation admission was useful: that admission was unjudged and
did not improve already-perfect recall.

Both exact-name controls returned one directly resolved resource and performed
no heterogeneous admission. They strengthen the distinction among direct
deterministic resolution, heterogeneous surfacing, purpose-relative admission,
and later Context disclosure. They do not establish a universal eligibility
test or request router.

The historical purpose-compatible oracle mean Recall@5 is `0.8021`, versus
`0.5625` for the practical rule, a descriptive difference of `0.2396` after
rounding. The oracle was measured at another checkpoint/corpus, so this is not a
paired effect or an estimate of attainable improvement on the current set. The
remaining difference cannot be apportioned among lexical or relationship
candidate recall, purpose representation, direction, support multiplicity,
threshold, single-slot/rank-five capacity policy, candidate-specific evidence,
incomplete judgments, or case-set size.

ADR-0004 accepts that Context planning can reason jointly over resources,
regions, symbols/declarations, DerivedKnowledge projections, relationships, and
source-preserving or synthesized representations. It recognizes coverage,
marginal contribution, overlap, complementarity, coherence, authority/
applicability, prior availability, and multi-dimensional cost as potential
constraints/preferences. It does not select algorithms, a representation
taxonomy, a cost function, or a general compiler. Current exact-name disclosure
is a deliberately narrow all-match projection, not proof of general planning.

## Context planning/disclosure boundary

Context is the purpose-relative information made available to a consumer. It
is not a ranked list, repository truth, Conversation, or an automatic model
prompt. Planning determines what and in which representation is useful under
constraints; materialization faithfully realizes that choice; assembly decides
how it is positioned in one ModelRequest. These are accepted semantics, while
all general mechanisms remain deferred.

## Progressive disclosure

Progressive disclosure is a possible response to demonstrated insufficiency: it
creates a later/refined acquisition episode without retroactively claiming that
the original need was satisfied. It preserves initial-versus-eventual quality as
separate evaluation questions. It has no current implementation or selected
orchestration owner.

## Evaluation/observability chain

The intended diagnostic chain is:

```text
fact unavailable/unsupported
-> not surfaced
-> surfaced but not admitted
-> admitted but poorly represented or undisclosed
-> disclosed but unused/misused by model
-> model used evidence but task failed
```

ADR-0002 supports qualified knowledge, availability, coverage, and execution
distinctions; the lexical evaluator supports surfacing metrics; Increment 21
supports consideration-versus-oracle-admission analysis. ADR-0003 explicitly
requires future observability to distinguish retrieval, ranking, selection,
representation/budget/disclosure, and model-utilization failure. ADR-0004
further distinguishes planning, materialization, assembly, and utilization.
The latter four are not yet implemented end-to-end. No generic telemetry or
Evidence system follows.

## Shadow-mode assessment

Shadow mode is a **near-term bounded evaluation direction, not accepted generic
architecture**. B-0002's
near-term sequence explicitly names Phase 1: run `devtools` predictions in
shadow mode without influencing native agent acquisition, then compare before
proactive assistance. No recovered research document, ADR, implementation, or
runtime design owns its contract, retained alternative Context, workload
correlation, or task-outcome comparator. Increment 22 strengthens the need for
such a path because it supplies an auditable hypothetical decision whose
production effect should not be assumed from offline metrics. A future bounded
slice needs a real native baseline, retained non-controlling surfaces and
decisions, disclosure/privacy policy, and a comparison basis. Shadow output
must never silently affect production Context. Nothing here justifies a
heavyweight experimentation platform.

Increment 23 demonstrates that the repaired capture/blinding/freezing/
unblinding/evaluation chain can retain such evidence, but it does not pass the
precommitted readiness gates for executing the current rule in shadow. Ten
material resources remain unjudged, no validated negative control reaches the
eligible relationship surface, one not-useful resource is admitted, and one
useful lexical rank-five resource is displaced. The next step is therefore a
stronger offline candidate/ranking comparison, not operational shadow rollout
of directional-reservation-v1.

## Learned-intelligence assessment

Research permits learned analyzers only when their qualified output and
provenance are explicit; it never makes a prediction unqualified repository
truth. For learned ranking, the stronger prerequisite is not merely features:
it is a defined purpose-relative target, sufficiently diverse held-out needs,
multiple competing evidence mechanisms, trustworthy labels or task outcomes,
and retained decision/disclosure/outcome traces. Current twelve manually judged
needs and oracle results are useful semantic counterexamples, not training data
for a general model. Shadow evidence could later provide non-controlling
comparisons; it does not itself solve labels or causal attribution.

## Architecture evidence matrix

| Capability / proposition | Research support | ADR disposition | Implementation status | Empirical evidence | Current disposition | Revisit / promotion trigger | Important caveat |
|---|---|---|---|---|---|---|---|
| Content BM25 | Strong baseline | Permitted, mechanism unselected | Production | Real-repo baseline | Production | New corpus/task evidence | Score is lexical observation, not truth |
| Filename BM25 | Address-field research | Mechanism unselected | Production at 0.25 | Promotion gate/robustness set | Production | Cross-repo regression evidence | Final stem only; separate statistics |
| Identifier decomposition | Useful but mixed | No acceptance | Experiment only | 13-case gain and a loss | Empirically constrained | Held-out benefit without regressions | Not a proxy for path evidence |
| Full path/directory lexical evidence | Mixed/negative | Deferred | Absent | Filename beat full path; proximity failed | Rejected for now | Need-conditioned held-out gain | Directory is not semantic relation |
| Filesystem proximity | Negative | ADR-0003 constraint | Experiment only | Increment 16 fixed-K losses | Rejected for now | New semantics, not more tuning | Does not falsify typed relations |
| Exact/direct resource lookup | Strong conceptual support | Accepted direct-acquisition boundary | Addressed `resource_at`/materialization support | No broad evaluation | Implemented support only | Concrete addressed consumer | Exact address is not discovery |
| Exact symbol/declaration lookup | Strong | Accepted; narrow implementation | Direct function-name lookup | Deterministic tests, no portfolio comparison | Production, bounded | Another declaration/subject family and consumer | Not repository-wide symbol resolution |
| Import declarations | Strong deterministic substrate | ADR-0002 compatible | Production knowledge | Deterministic tests | Implemented knowledge only | Consumer needing syntax facts | Syntax does not prove target |
| Module interpretation | Strong qualification support | ADR-0002 compatible | Production knowledge | Deterministic tests | Implemented knowledge only | Explicit-root consumer | Not runtime importability |
| Import resolution | Strong qualified-relation support | ADR-0002 compatible | Production knowledge | Increment 20-22 inputs | Implemented knowledge only | Broader language semantics | Unresolved is only in-universe |
| Declaration-grounded import relations | Strong, direction-sensitive | Typed views accepted | Production knowledge | Increment 20-22 | Implemented knowledge only | Stable retrieval value | Not generic dependency/runtime import |
| Outgoing relation expansion | Supported but constrained | No production promotion | Experiment only | Added headroom; one useful Increment-22 admission | Experiment only | Independent fully judged value | Direction/seed provenance matters |
| Incoming relation expansion | Supported but constrained | No production promotion | Experiment only | Increment-22 gains and unjudged admissions | Experiment only | Eligible negative controls and broader tasks | Not universally better |
| Generic graph abstraction | Earlier research proposed it; later criticism/ADR rejected | Rejected | Absent | None | Rejected for now | None absent new architecture decision | Do not confuse with typed views |
| Typed graph/relationship views | Strong | Accepted future capability | One import relation family only | Import experiments | Accepted but mostly unimplemented | Independently useful bounded view | Views need not share nodes/store |
| Semantic/vector retrieval | Research-supported optional family | Deferred/unselected | Absent | No local experiment | Deferred | Honest frozen comparison and representation/cost basis | Embeddings are not presumed better |
| Learned fusion/ranking | Research-supported late option | Enabled, unselected | Absent | No labels/workload | Deferred | Diverse labels/outcomes and alternatives | No universal feature/score meaning |
| Model-directed/iterative retrieval | Research-supported future | Future planning/acquisition | Absent | No local agent experiment | Deferred | Bounded task/outcome evidence | Not narrow Runtime ownership |
| Purpose-relative admission/selection | Strong semantic/evaluation support | Purpose-bearing admission/abstention accepted; representation open | Experiment rule only; exact all-match is narrow | Increment 22 improved one set; Increment 23 had zero net known-useful gain and one useful loss | Architecture accepted; concrete rule not shadow-ready | Stronger bounded candidate/ranking evidence | Rule is not a Selector or safety proof |
| Universal Candidate abstraction | Earlier proposals challenged | No generic Candidate; ADR-0003 has conceptual ContextCandidate | Absent | Increment 20/21 support typed grouping | Rejected for now | Durable cross-stage need beyond identity + observations | Do not conflate ADR concept with generic class |
| Universal CandidateEvidence abstraction | Rejected by later research | No mandatory evidence artifact | Absent | Typed surfaces useful | Rejected for now | Shared semantics not expressible natively | Preserve native provenance |
| Normalized universal relevance score | Rejected | Rejected | Absent | BM25/relation incomparable | Rejected for now | Explicit calibrated policy/model | Numeric output can be policy-local |
| First-class Selector | Challenged | Rejected for now | Absent | Oracle only | Rejected for now | Reuse outside Context planning | Decision is a verb before a domain |
| Standalone Selection domain | Challenged | Rejected for now | Absent | None | Rejected for now | Independent lifecycle/consumers | Context may own admission |
| Context representation choice | Strong | Accepted semantics | Narrow declaration/source representations | No comparative representation experiment | Accepted but unimplemented generally | Bounded representation experiment | Resource top-K is insufficient |
| Progressive disclosure | Strong research support | Accepted future semantics | Absent | No local outcome evaluation | Deferred | Bounded acquisition/outcome evidence | New episode, not a loop inside Context |
| Shadow retrieval/evaluation | B-0002 staged direction | No generic platform accepted | Absent | Increment 23 validates the pipeline but fails its frozen shadow-readiness gates | Not ready for shadow | Stronger candidate/ranking strategy plus complete decision-surface judgments | Must not control production behavior |
| Source/test heuristics | Research challenge and local negative evidence | No default weighting | Absent | Relevant and irrelevant test controls | Rejected for now | Need-specific held-out evidence | Role is not relevance |
| Evaluation / retained evidence | Strong | Accepted future responsibility | Lexical evaluator + experiment JSON schema/code | Increments 10-23 | Partially implemented | Claim-specific evaluation need | No universal metric/store |

## Recovered and missing historical findings

| Earlier synthesis lead | Recovery classification | Evidence and disposition |
|---|---|---|
| No universal retriever; task dependence | Fully preserved | Repository Context research, ADR-0003 portfolio, Increment 21/22 paired needs |
| Exact/direct lookup can bypass discovery | Fully preserved | ADR-0003 and exact-name implementation |
| Lexical deterministic baseline | Fully preserved | Production BM25 and B-0002 lineage |
| Filename/path evidence as separate signals | Fully preserved | Filename design, path experiments, ADR-0003 native evidence |
| Multiple typed relationship views, not one graph/store | Fully preserved | Subject research and ADR-0002 |
| Semantic/vector later family | Fully preserved | Research and ADR-0002/0003 deferrals |
| Learned ranking only after evidence | Fully preserved | Purpose-relative research and ADR-0003 |
| Native evidence rather than universal score | Fully preserved | ADR-0003 and Increment 21/22 surface records |
| Parallel/pipelined retrieval before planning | Fully preserved | ADR-0003 independent concurrent applications/conditional waves |
| Iterative/model-directed retrieval | Fully preserved as deferred | Research, ADR-0002/0003 progressive acquisition |
| Retrieval skipping | Refined | Direct acquisition is separate; purpose-policy abstention is accepted semantics but not a generic gate |
| Context is more than top-K; representations/progressive disclosure matter | Fully preserved | ADR-0004 |
| Coverage, complementarity, authority, coherence, multidimensional cost | Fully preserved as accepted semantics | ADR-0004; mechanisms remain open |
| Surface/choose/disclose/model-use failure separation | Fully preserved as future requirement | ADR-0003/0004; Increment 22 evaluates only early stages |
| Shadow comparison on real workloads | Preserved but deferred by frozen readiness gates | B-0002 plus Increment 23; stronger candidate/ranking evidence and the operational contract remain absent |
| Repository Intelligence is not retrieval; usefulness is not truth | Fully preserved | ADR-0002 through ADR-0004 |

The material most plausibly lost from the recalled **“Summarize strong
findings”** lineage is not the heterogeneous portfolio itself; that is well
preserved. The material gap is the operational research framing for shadow,
non-controlling comparison and retained alternative Context. B-0002 preserves
the staged idea, but it lacks a dedicated canonical research artifact and ADR
disposition. This synthesis restores discoverability without accepting it.

## Rejected and constrained approaches

Do not infer production architecture from early research proposals for a
unified graph, Candidate-plus-score pipeline, generic score fusion, vector DB,
or a selector. Those recommendations were narrowed/superseded by ADR-0002 to
ADR-0004 and later experiments. Explicitly rejected-for-now: universal graph/
store, universal Candidate/CandidateEvidence, universal relevance/confidence
score, generic Selector/Selection domain, default source/test and directory
priors, relation multiplicity bonus, blind relationship insertion, and generic
telemetry/evidence machinery. These remain discoverable as alternatives, not
silently discarded history.

## Deferred capabilities

Open pressure includes broader exact/symbol lookup; useful relationship families
beyond imports; independent purpose-policy validation; semantic comparison;
task-conditioned planning; learned policy;
representation/fidelity/cost measurement; sufficiency and progressive
acquisition; shadow comparison; task outcomes; change/history and test/code
views; and privacy-safe retained decision/disclosure evidence. The key questions
are empirical: when direct acquisition is sufficient; whether the frozen rule
generalizes and rejects eligible negatives; which unjudged admissions are useful;
whether another retrieval family adds unique value beyond lexical width; and
which representation helps the downstream consumer.

## Open questions

No current source establishes the right direct-lookup eligibility test, the
next relationship family, a semantic retrieval unit, a useful representation
cost model, a sufficiency signal, an authority assessment, shadow ownership, or
a learned objective. Increment 23 directly demonstrates that the current
support threshold admits non-useful evidence and that the sole reservation slot
can lose useful lexical rank five. It still does not establish validated
negative-control rejection, complete relevance labels, cross-repository
generalization, or a safe alternative capacity/ranking policy. These are
questions to preserve for bounded evidence, not unfilled interfaces.

## Recommended next investigations

Order is dependency-based:

1. Stop tuning the single rank-five reservation rule. Freeze the same needs and
   compare stronger bounded candidate generation and purpose-relative ranking
   over lexical top-fifteen and typed relationship surfaces. Retain native
   evidence, useful-loss accounting, candidate volume, and unresolved-label
   bounds; do not normalize heterogeneous evidence into one universal score.
2. Establish a bounded non-controlling shadow comparison only after the stronger
   offline strategy has complete decision-surface judgments and passes explicit
   loss, non-useful-admission, and negative-control gates, and when a real native
   acquisition workload, retained hypothetical decision record, comparison
   basis, and disclosure/privacy policy exist. Production Context must remain
   unchanged.
3. If independent evidence remains positive, evaluate a bounded Context
   representation/admission comparison on fixed selected information before
   promoting any selector-shaped API.
4. Then select the next retrieval family by unique held-out failure mode:
   broaden direct declaration/reference lookup if exact needs dominate; add a
   second typed relation only where a documented need remains unserved; or run
   a semantic experiment only with its explicit prerequisites and lexical/direct
   controls.
5. Learned ranking should wait still longer for diverse labels/outcomes and
   shadow/decision/disclosure traces.

## Revisit triggers

Revisit semantic retrieval on lexical/direct/typed-view misses with frozen
needs and representation/cost accounting. Revisit learned ranking only when
there are sufficient diverse held-out examples and a target that is not an
oracle label alone. Revisit a first-class Selector only when multiple consumers
need reusable decisions outside operation-specific policy or
representation-aware Context planning.

## ADR assessment and disposition

ADR-0002, ADR-0003, and ADR-0004 own Repository Intelligence/typed views;
InformationNeed/native evidence/direct acquisition/ranking; and
representation-aware disclosure respectively. ADR-0003 is amended to record
the now-empirical requirement that purpose be available to a bounded admission
decision and that explicit abstention is valid decision semantics. ADR-0004
already permits that decision to remain local to Context planning and needs no
amendment. No new ADR is justified: there is no distinct new domain, lifecycle,
or cross-package owner. Shadow comparison remains a bounded evaluation direction
whose scope, owner, privacy boundary, and production-control contract are open.

## Long-term architecture synthesis

The evidence supports the following **conditional** flow, not a mandatory
runtime pipeline:

```text
Repository and applicable external state
  [implemented bounded observation; broader policy deferred]
    -> Repository Intelligence
       [some declarations/modules/import facts implemented; typed views accepted]
    -> InformationNeed
       [accepted semantic distinction; no production enum/type selected]
    -> exact/direct resolution OR heterogeneous bounded discovery
       [narrow exact + lexical production; other families deferred]
    -> purpose-relative decision under capacity
       [accepted semantics; one experimental rule, no production policy]
    -> Context planning and representation-aware disclosure
       [accepted; only narrow exact-name realization implemented]
    -> model/agent
       [existing interaction boundary; no retrieval loop]
    -> outcome/evaluation
       [partial retrieval evidence; end-to-end chain deferred]
    -> non-controlling shadow comparison / future learning
       [near-term bounded evaluation direction; no generic platform]
```

At every boundary, do not conflate repository truth with surfacing, surfacing
with usefulness, admission with representation, disclosure with model use, or
historical evaluation evidence with production authority. The architecture is
heterogeneous by design but deliberately does not standardize its mechanisms
before their evidence and consumers exist.

## Final disposition

**Disposition B, refined by Increment 23:** retain the underlying
purpose-relative admission architecture, but stop optimizing directional
reservation v1. Independent validation finds zero net known-useful gain, one
not-useful admission, and one useful rank-five loss. It also finds that lexical
top fifteen contains all known-useful material resources while the relationship
surface contributes only one useful resource beyond top five. The concrete rule
is `NOT_READY_FOR_SHADOW` and production promotion is not justified. This does
not falsify purpose-relative retrieval or the heterogeneous portfolio; it shifts
the next bounded work toward stronger candidate generation and ranking.
Production remains content BM25 plus `0.25 *` filename-stem BM25 at `K=5`;
relationship expansion and admission remain experimental, and exact/direct
resolution remains separate.

**Increment 24 refinement:** the frozen offline ranking comparison finds no
local improvement from its purpose-relative deterministic ordering: it recovers
9 known-useful resources versus 10 for lexical/native ranking, and selects
three additional known-not-useful resources. All 18 known-useful material
resources are already in lexical top fifteen. Typed import evidence has no
demonstrated incremental ranking value on this six-case devtools surface; a
learned baseline is not estimable without unacceptable grouped-split variance.
This is not evidence that lexical width is generally sufficient. Increment 25
should test a distinct semantic candidate-generation family, and Increment 26
requires independent-repository evidence before closure.
