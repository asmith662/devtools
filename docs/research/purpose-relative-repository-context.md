# Purpose-Relative Repository Context: Retrieval, Selection, and Disclosure

## Disposition

Status: Reconciled

Canonical research subject: Purpose-relative repository Context, retrieval, selection, and disclosure.

Related ADRs: ADR-0003; ADR-0004.

Implemented evidence: lexical retrieval, manually judged evaluation, exact source materialization, and directed import relation knowledge.

Accepted: repository truth, candidate surfacing, purpose-relative relevance, ranking, and disclosure are distinct.

Deferred: reusable purpose-relative selection and concrete disclosure planning.

Rejected for now: universal Candidate/CandidateEvidence, universal relevance score, first-class Selector, standalone Selection domain, undirected graph, and source/test weighting.

Superseded or refined findings: Increment 20 supplies relation-candidate and fixed-K evidence refining this non-promotion boundary.

Open questions: whether a bounded need-sensitive decision requires reusable semantics outside existing Context planning.

Revisit triggers: independently evaluated selection evidence demonstrating stable need-specific value that cannot remain local.

Reconciliation basis: ADR-0003; ADR-0004; Increment 16; Increment 20.

## Executive conclusion and strongest challenges

**Executive conclusion — A.** The evidence does **not** justify introducing a first-class `Selector`, a universal `Candidate`, a universal `CandidateEvidence`, a common relevance score, or a new standalone Selection domain before Increment 21.

The minimum strong architecture is smaller:

```text
Repository Intelligence
    purpose-independent repository facts
                │
                ▼
Retrieval
    mechanism-specific observations/results
    about resources surfaced for a request
                │
                ▼
Context planning
    purpose-relative decision over surfaced resources,
    representations, policy, and budget
                │
                ▼
Context disclosure
    actual information exposed to the consumer
```

There are **four semantic events** here—truth establishment, surfacing, decision, and disclosure—but only **three production boundaries** are presently justified: **Repository Intelligence, Retrieval, and Context**. Purpose-relative resource selection is a real semantic distinction, but the current evidence supports treating it as an operation inside Context planning, or occasionally inside a retrieval procedure, rather than promoting it to an independent architectural domain.

The decisive observation from Increment 20 is not “we need a selector.” It is narrower:

> **A mechanism can surface a resource for a perfectly valid reason without establishing that the resource should be disclosed for the current purpose.**

That invariant must be represented somewhere. It does **not** imply a `Selector` class.

This conclusion is consistent with recent repository-context research. CodeNib explicitly treats repository views as heterogeneous artifacts with different output contracts and warns against collapsing ranked candidates, source locations, and prompt state into one abstraction; it then treats prompt context as a bounded delivery result. citeturn15view0 At the other architectural extreme, SWE-agent obtains context incrementally through an interactive agent-computer interface rather than through a universal candidate-selection object model, while Agentless uses a procedural hierarchy of localization stages. citeturn15view6turn15view7 The successful systems therefore do **not** establish that “selection” must be its own reusable semantic entity.

The recommended minimum invariant is:

```text
repository proposition
    !=
retrieval/surfacing observation
    !=
purpose-relative decision
    !=
disclosed Context item
```

The middle two distinctions must be **observable and evaluable**, but need not correspond one-for-one to public abstractions.

### Strongest challenges to the current framing — B

Several assumptions in the provisional four-stage architecture should be rejected or substantially weakened.

First, **“candidate generation” is probably too grand a name for the semantic requirement**. A lexical search result is already a perfectly adequate representation of “this resource was surfaced lexically.” A relationship-expansion result can similarly mean “this target was reached from seed S through exact relation R in direction D.” Neither needs to become a `Candidate` before a later operation can group both results by resource identity.

Second, **candidatehood is not Repository Knowledge**. It is an execution-relative state: resource `R` happened to enter the consideration universe for information need `N` through retrieval execution `E`. Changing the query, seed width, expansion policy, or purpose can make `R` cease to be a candidate without changing anything about the repository. It therefore has the wrong truth conditions for Repository Intelligence.

Third, **“relevance assessment” should not automatically become a production subsystem**. Relevance is useful as an evaluation relation between an information need and a resource. Production systems need a *decision procedure*, but that procedure may use direct rules, a ranking model, an LLM, incremental agent search, or Context planning. Converting the benchmark concept of relevance into a service called `RelevanceEvaluator` or `Selector` would prematurely turn an evaluation construct into a domain model.

Fourth, **selection is not fundamentally ranking**. Classical information retrieval already contains methods such as Maximal Marginal Relevance whose purpose is to choose results based partly on what has already been selected, explicitly addressing novelty and redundancy rather than simply assigning independent relevance scores. citeturn17search18 Repository tasks strengthen that objection: several files can be individually relevant yet redundant, while another lower-ranked file can supply the missing half of a multi-file explanation or edit.

Fifth, **budget cannot be cleanly attached to “resource relevance.”** A file has no intrinsic token cost until a representation is chosen. A 2,000-line module might be useful if disclosed as one declaration, a symbol outline, a derived import relation, or a 30-line implementation slice, but unaffordable as raw source. RepoNav provides a concrete contemporary example: it leaves retrieval scores unchanged but restructures retrieved material into compact file-centered navigation cues, demonstrating that presentation granularity can alter effective use without changing the underlying retrieval. citeturn15view5

Sixth, **the separate Selection layer may partly be an artifact of top-K benchmarking**. `K=5` forces an artificial moment at which resources appear to have to be selected. Actual Context has token costs, alternative representations, policy constraints, dynamic inspection, and possibly multiple rounds. ContextBench finds significant gaps between context that agents retrieve and context that is ultimately utilized, which is direct evidence that “retrieved resource” and “effective final context” are different objects. citeturn18view2

The result is deliberately asymmetric:

> **Candidate generation and selection should remain conceptually distinguishable for causal evaluation, but they should not yet become two independent architectural domains.**

That is the smallest architecture preserving the lesson of Increment 20 without turning an experimental decomposition into a type hierarchy.

## Semantic decomposition, information need, and candidatehood

**Recommended semantic decomposition — C.** The strongest minimum decomposition is:

```text
               Repository state
                      │
                      ▼
        ┌───────────────────────────┐
        │ Repository Intelligence   │
        │                           │
        │ Resource facts            │
        │ module interpretations    │
        │ declarations              │
        │ resolved import relations │
        └─────────────┬─────────────┘
                      │ purpose-independent facts
                      │
            ┌─────────┴──────────┐
            │                    │
            ▼                    ▼
   Lexical retrieval      Relation-based surfacing
   query → lexical hits   seeds + exact relations
            │                    │
            └─────────┬──────────┘
                      │
        mechanism-specific results
                      │
                      ▼
      ephemeral consideration view
       group by ResourceIdentity
       WITHOUT score normalization
                      │
                      ▼
        ┌───────────────────────────┐
        │ Context planning          │
        │                           │
        │ purpose                   │
        │ admissibility/priority    │
        │ complementarity          │
        │ representation choice     │
        │ disclosure policy         │
        │ token/cost budget         │
        └─────────────┬─────────────┘
                      │
                disclosure plan
                      │
                      ▼
             Context disclosure
```

The “ephemeral consideration view” is intentionally **not a new domain** and need not even be a public type. It can be a temporary mapping:

```python
ResourceIdentity -> tuple[MechanismSpecificResult, ...]
```

Its semantic function is simply deduplication without evidence destruction.

This architecture also permits a mechanism to combine generation and local selection. For example, a future graph retriever could traverse many repository relations internally and expose only a bounded subset. That is legitimate provided its trace makes clear enough of the considered universe and decision procedure to evaluate its recall and filtering behavior. CodeNib similarly permits physical retrieval plans containing reranking or graph expansion, while keeping the operator and candidate-fusion semantics explicit rather than pretending every operation is the same kind of score. citeturn18view0

The protected invariant is therefore not:

> Candidate generation must always run in subsystem X and selection must always run in subsystem Y.

It is:

> **An experiment must be able to distinguish failure to surface a useful resource from failure to choose or use a resource that was surfaced.**

Without that distinction, causal diagnosis becomes impossible.

### Information-need semantics — D

An explicit semantic distinction between **information need** and **retrieval query** is justified.

This is not a novel requirement. TREC has long distinguished the statement of an information need—the “topic”—from the query representation actually submitted to a retrieval system. citeturn14view0 Agent Retrieval Bench makes essentially the repository-agent version of the same distinction: its relevance criterion is based on what the agent needs next rather than merely on direct semantic similarity between query and file, and task families such as `code2test`, `trace2code`, and `edit2ripple` produce materially different notions of useful retrieval. citeturn15view3

The minimum semantic representation is **not** an intent ontology such as:

```text
LOCATE
UNDERSTAND
MODIFY
DEBUG
TEST
REFACTOR
...
```

Nor does it require an LLM classifier.

The minimum is simply to preserve two different things:

```text
Information need:
    the purpose-bearing request/task

Retrieval query:
    the mechanism input derived from or associated with that request
```

For example:

```text
Need A:
    "Where is import resolution implemented?"

Need B:
    "What do I need to understand or modify to change
     import resolution safely?"

Lexical query for both:
    "import resolution"
```

The distinction is semantically sufficient even if the information need is represented only by the original task text plus a benchmark/run identifier. If the caller already knows a structured operation—for example, “locate a definition” versus “prepare an edit”—that existing structure can be preserved, but `devtools` should not invent a universal `Purpose` enumeration merely to support retrieval.

The architectural relationship should instead be:

```text
InformationNeed N
        │
        ├── lexical-query derivation ──> q₁
        ├── future semantic query ─────> q₂
        └── Context planning purpose
```

This protects a crucial fact: **the same query string can be associated with different relevance judgments because it is not the query string that supplies the complete relevance criterion.**

A first-class production `InformationNeed` object is not yet mandatory. The semantic distinction **is** mandatory. Increment 21 can establish it first in the evaluation model and only promote a production type if a production API actually needs to pass it across boundaries.

### Candidate semantics — E

A first-class universal `Candidate` is **not justified**.

The smallest honest definition of candidatehood is:

> A repository resource is a candidate when it belongs to the consideration universe of a particular retrieval/context-planning execution.

That means candidatehood has:

- no repository-level truth value;
- no independent content identity;
- no confidence intrinsic to it;
- no necessary score;
- no cross-query applicability;
- no obvious durable identity beyond “resource R was considered in execution E.”

The resource already has identity. Candidatehood adds operational membership, not a new subject.

Therefore, this:

```python
Candidate(
    id=...,
    resource=...,
    evidence=...,
    confidence=...,
    score=...,
    applicability=...,
)
```

would currently create more semantic questions than it resolves.

By contrast, **support should be retained**—but in mechanism-specific forms.

A lexical hit legitimately carries things such as:

```text
resource
content score/contribution
filename score/contribution
combined lexical score
rank
query
retrieval configuration
```

A relationship-derived surfacing result legitimately carries:

```text
target resource
seed resource
seed provenance/rank
exact repository relation
relation direction
declaration provenance
expansion operation/configuration
```

Neither needs to implement:

```python
CandidateEvidence
```

They share only the weak fact that a later decision may consume them.

Suppose the same target is found through three paths:

```text
bm25 result ------------------------------┐
                                         │
seed A --outgoing import relation R1 ----> resource.py
                                         │
seed B --incoming import relation R2 -----┘
```

The appropriate representation at the combination point is conceptually:

```text
resource.py:
    lexical_result(...)
    outgoing_expansion(seed=A, relation=R1)
    incoming_expansion(seed=B, relation=R2)
```

not:

```text
Candidate(
    resource=resource.py,
    score=12.47,
    confidence=.83,
    evidence=[...]
)
```

The former preserves causal semantics; the latter demands an unsupported theory for converting unlike observations into a scalar.

**Relationship multiplicity** should likewise remain support multiplicity, not relevance magnitude. Three declarations can be three genuine repository facts while being highly dependent evidence from the perspective of retrieval. A resource imported repeatedly is not thereby three times as useful for the task. Aider's repository map illustrates the fact that practical systems can deliberately use occurrence frequency while damping it—the implementation square-roots reference counts before adding graph-edge weight—rather than assuming raw multiplicity is linearly meaningful. citeturn16view1 That is an engineered ranking choice, not a semantic law.

Direction is equally important. `source → imported target` and `importer → source` answer different navigation questions. Increment 20's materially different incoming/outgoing behavior reinforces that direction must remain present in the relationship proposition and, when used for surfacing, in the surfacing provenance. It should not be flattened into generic “adjacency.”

## Selection, evidence composition, budget, and Context

**Selection semantics — F.** Selection deserves a precise *verb*, but not yet a new architectural *noun*.

For this architecture:

> **Selection is a purpose-relative decision to admit, prioritize, or choose among already available alternatives.**

Selection may therefore return:

- a set;
- an ordered set;
- admission/rejection decisions;
- a sequence of incremental choices;
- a representation-specific plan.

A total order is merely one possible implementation.

It helps to distinguish three concepts without prematurely making all three production objects:

```text
Relevance:
    Does resource R meaningfully bear on information need N?

Usefulness:
    Does supplying some representation of R materially improve
    accomplishing N, given the other available Context?

Selection:
    Is R or one of its representations chosen by this policy
    under the present constraints?
```

The difference between relevance and usefulness becomes especially clear once context interactions are admitted. Conceptually:

```text
Relevance:   Rel(N, R)

Usefulness:  U(R | N, already_supplied_context,
               representation, consumer/model)

Selection:   Choose(..., policy, constraints)
```

RLCoder provides a concrete example of a system optimizing something closer to **generation-conditioned usefulness** than classical relevance: it evaluates retrieved material according to how the additional context affects target-code perplexity, and also learns when retrieval should stop and which candidates should be retained. citeturn15view11 Repoformer similarly finds that unconditional retrieval can be unhelpful or harmful and learns when retrieval should be omitted. citeturn15view10 These results do not imply that `devtools` needs such models; they demonstrate why “relevant,” “useful to this consumer,” and “selected” are not interchangeable propositions.

For Increment 21, **relevance can remain an evaluation concept**, usefulness can remain an analysis concept, and selection can remain an execution decision. There is no reason yet for three new production interfaces.

### Heterogeneous evidence composition — G

BM25 evidence and an exact resolved-import relationship should **not** be normalized merely because a later component wants one number.

Consider:

```text
BM25 = 8.3
```

versus:

```text
seed resource S contains direct declaration D
whose qualified resolution uniquely identifies target T
```

The first is an information-retrieval score whose magnitude depends on a corpus, analyzer, query, term statistics, field design, and scoring formula. The second is a proposition established through repository interpretation and resolution.

No meaningful unit conversion follows from their existence.

The default should therefore be:

```text
retain independently
        ↓
let a decision procedure consume the typed observations
```

rather than:

```text
normalize everything
        ↓
weighted universal score
```

A future learned ranker can legitimately consume:

```text
content BM25
filename BM25
lexical rank
outgoing relation present
incoming relation present
number of distinct seeds
number of declarations
...
```

as model features. That does **not** semantically turn those fields into measurements of one latent quantity. The learned model supplies the task-specific mapping.

Similarly, a deterministic policy can say:

```text
admit an outgoing-related target when condition X holds
unless condition Y holds
```

without inventing a relationship “bonus.”

CodeNib is informative here. Its query planner supports lexical, semantic, hybrid, and structural routes; reciprocal-rank fusion belongs only to one hybrid route, while graph expansion is modeled separately. Its experimental graph fusion is explicitly described so graph candidate generation is not mistaken for dense rescoring. citeturn18view0 That is a stronger semantic posture than a universal `final_score = lexical + graph_bonus + ...`.

Universal weighted fusion has several characteristic failure modes:

| Failure | Why it matters here |
|---|---|
| Scale arbitrariness | `8.3` BM25 has no natural exchange rate with one import relation. |
| Query dependence | Score distributions change across queries, so a fixed bonus can dominate one need and vanish on another. |
| Corpus dependence | BM25 magnitude depends on corpus statistics; relationship truth does not. |
| Multiplicity leakage | Repeated declarations or seeds can accidentally become repeated “votes.” |
| Provenance loss | A combined scalar hides whether a resource was lexical, relational, or both. |
| Direction loss | A generic graph bonus easily collapses incoming and outgoing semantics. |
| Calibration illusion | A numeric result can look probabilistic or comparable without ever being calibrated to relevance or utility. |
| Future incompatibility | New mechanisms become pressure to invent another arbitrary coefficient. |

Score fusion is therefore not forbidden. It is simply an **algorithm owned by a particular retrieval/decision policy**, whose calibration and evaluation must be explicit. It should never become the ontology of evidence.

### Negative evidence

An explicit benchmark judgment that a resource is irrelevant to need `N` is **not negative Repository Knowledge**.

It says:

```text
judge J, under benchmark protocol P:
    resource R is not judged relevant for need N
```

not:

```text
repository R proves that resource X is useless
```

TREC's treatment of relevance reinforces the distinction: relevance judgments are associated with information needs, can be graded, and are inherently judgment-dependent; pooled evaluation can even operationally treat unjudged documents as nonrelevant, which is an evaluation convention rather than an ontological fact about those documents. citeturn14view1

Production decision policies may nevertheless consume **negative signals**. Examples include:

```text
a task-specific classifier predicts low utility
a disclosure policy prohibits this representation
an explicit caller constraint excludes generated code
the consumer already possesses equivalent content
```

Those are legitimate decision inputs. They need not become `NegativeEvidence` in Repository Intelligence.

Most importantly:

> **Absence of positive support is not negative relevance evidence.**

“No resolved import path from the selected lexical seed reaches R” does not mean “R is irrelevant.” Increment 20 itself is evidence against such a closed-world inference.

Counterfactual controls should remain primarily an evaluation instrument. Agent Retrieval Bench is particularly cautionary: thresholds calibrated on counterfactual wrong-repository controls did not improve selective retrieval on its natural no-gold cases. citeturn18view3 A control that is useful for falsification is not automatically a production negative feature.

### Multi-resource selection, redundancy, and marginal value

Top-K individual ranking is not expressive enough to represent all of the eventual Context problem.

Suppose:

```text
A: implementation of resolution
B: another file repeating the same high-level implementation facts
C: declaration/type contract needed to understand the boundary
D: test demonstrating the edge case being changed
```

An independent relevance rank could reasonably produce:

```text
A > B > C > D
```

yet under a three-resource budget:

```text
{A, C, D}
```

may be much better Context than:

```text
{A, B, C}
```

because the utility of `B` changes after `A` is present.

This is an old distinction in information retrieval: MMR was introduced specifically to balance query relevance with information novelty and reduce redundancy in selected results. citeturn17search18 The significance for `devtools` is not “implement MMR.” It is that **set utility cannot in general be reduced to independent resource scores**.

ContextBench directly measures redundancy and finds substantial context usage loss in coding agents, while also reporting a recall/precision tradeoff from aggressive context acquisition. citeturn18view1turn18view2 RepoNav likewise reports that reaching the correct file does not settle the finer-grained target-selection problem; reorganizing evidence within files changes downstream localization behavior without changing the raw retriever. citeturn15view4turn15view5

The minimum architectural consequence is modest:

> Do not define the contract of selection as `Candidate -> float`.

That would unnecessarily make future complementarity, redundancy, representation choice, and set coverage awkward.

### Budget and Context boundary — H

There are actually **two different kinds of budget** that should not be conflated.

```text
Retrieval / consideration budget
    query latency
    number of seeds
    expansion width
    reranker calls
    search depth
    maximum surfaced results

Context / disclosure budget
    token capacity
    representation cost
    model/context limits
    disclosure policy
    task-required coverage
```

`K=5` belongs to the first category when it bounds retrieval evaluation. It is not the semantic definition of Context capacity.

The **final Context decision must be budget-aware**, because selecting a resource before choosing its representation can be meaningless. A resource may be:

```text
selected subject:
    src/devtools/imports.py

possible disclosures:
    whole resource              5,900 tokens
    symbol outline                320 tokens
    target declaration             75 tokens
    implementation slice          640 tokens
    derived import relation         30 tokens
```

A resource-level selection that ignores these alternatives cannot determine the economically best Context.

Practical systems already make such tradeoffs in different ways. Aider has long exposed a token budget for its repository map and uses graph/ranking heuristics to prioritize which files and identifiers fit within that representation. citeturn16view2turn16view1 CodeNib separately studies retrieval plans and context-delivery policies, and records budget and provenance in its agent execution. citeturn15view1turn18view0 These systems collapse boundaries differently, which is evidence against treating any one implementation split as universal.

The recommended semantic split is therefore:

```text
purpose-relative assessment / priority
                │
                ▼
Context planning:
    choose subjects + representations jointly
    under disclosure policy and budget
                │
                ▼
disclosure
```

Assessment *can* be performed without a token budget. Final allocation cannot.

This leads to a crucial architectural answer:

> **Selection and Context disclosure are distinct, but selection does not currently deserve its own domain outside Context.**

A resource can be worth considering or even preferred while the actual Context contains only one declaration from it. A repository fact can be disclosed instead of source. Policy can suppress an otherwise useful resource. The Context plan can change when token budget changes without altering retrieval relevance.

### Required distinction matrix

The required pairs resolve as follows:

| Concepts | Determination | Why |
|---|---|---|
| Repository truth ↔ retrieval relevance | **Distinct** | Repository truth is state-relative; relevance depends on an information need. |
| Retrieval relevance ↔ usefulness | **Distinct** | A relevant resource may be redundant, badly represented, too costly, or unhelpful to a particular consumer. |
| Candidate generation ↔ selection | **Distinct semantics; may share implementation** | One determines the consideration universe; the other chooses among it. Separating their evaluation protects causal diagnosis. |
| Ranking ↔ selection | **Distinct** | Ranking is an ordering; selection may be set-based, conditional, diversified, iterative, or constrained. |
| Selection ↔ Context disclosure | **Distinct** | The selected subject need not be disclosed wholesale—or at all—and representation/policy intervene. |
| Candidate identity ↔ candidate support | **Not enough evidence for candidate identity** | Support must survive; a separate candidate identity presently adds nothing beyond resource identity plus execution membership. |
| Resource identity ↔ candidate identity | **Distinct in principle** | Resource identity is durable repository semantics; candidatehood is execution-relative. The latter need not be instantiated. |
| Positive support ↔ relevance judgment | **Distinct** | “This mechanism surfaced R because X” does not establish “R is relevant to N.” |
| Negative benchmark judgment ↔ negative repository knowledge | **Distinct** | Benchmark irrelevance is need/protocol-relative, not a proposition intrinsic to repository state. |
| Relationship truth ↔ relationship-derived candidate support | **Distinct** | The relation is repository knowledge; using it from seed S during retrieval is execution evidence. |
| Lexical score ↔ relationship support | **Distinct** | They have different truth conditions and no natural common numeric unit. |
| Selection evidence ↔ selection identity | **Distinct; identity not presently justified** | Trace inputs explain a decision; they need not define a reusable semantic entity. |
| Selection ↔ budgeting | **Distinct but coupled** | Budget is a constraint on decision/allocation, not itself relevance. Final Context selection should consume it. |
| Candidate recall ↔ final Context quality | **Distinct** | A perfect consideration universe can still be selected, represented, or disclosed badly. |
| Resource relevance ↔ multi-resource completeness | **Distinct** | Per-resource labels cannot by themselves express complementarity, acceptable alternatives, or required combinations. |

This matrix is intentionally dominated by “distinct.” That does **not** imply fifteen classes. The central architectural discipline is to keep propositions distinct without automatically reifying each proposition as a type.

## Identity, provenance, applicability, and replay

**Identity, provenance, applicability, and replay — I.** The framework should be strict about the distinction between **semantic identity** and **execution trace**.

The following should have durable semantic identity where they already naturally possess it:

| Thing | Identity position |
|---|---|
| Repository | Existing repository identity. |
| Repository resource occurrence | Existing exact repository-relative/resource-content semantics. |
| Module interpretation | Existing Repository Intelligence semantics. |
| Import declaration | Existing declaration identity/provenance. |
| Resolved module-import relation | Existing derivation-grounded relation semantics. |
| Information need | May need a benchmark/execution identifier, but no cross-run semantic identity scheme is yet required. |

The following should ordinarily be treated as **execution observations or decisions**, not new Repository Knowledge:

| Thing | Recommended status |
|---|---|
| Lexical retrieval result | Reproducible retrieval observation. |
| Relationship expansion result | Retrieval/surfacing observation referencing repository facts. |
| Considered-resource membership | Ephemeral execution state. |
| Purpose-relative relevance label | Evaluation judgment. |
| Selection/admission result | Execution decision. |
| Context plan | Execution plan under specific policy and budget. |
| Actual disclosure | Execution record. |

A future system may choose to persist all of these. Persistence does not turn them into semantic knowledge.

### What exact replay requires

For deterministic replay and causal investigation, the trace should retain enough to reconstruct each transition:

```text
information need / original request
derived mechanism query or queries

repository identity and relevant observed state

retrieval mechanism identity/version/configuration
index/profile identity where applicable
complete returned results at the tested width

for lexical results:
    content evidence
    filename evidence
    total lexical score
    rank

for relation expansion:
    seed identity
    seed rank/provenance
    exact relationship identity/proposition
    direction
    declaration provenance
    expansion configuration

decision procedure:
    implementation/version
    exact inputs
    configuration
    output/admissions/order
    explicit reasons if that procedure naturally emits them

Context planning:
    disclosure policy
    available representations
    representation costs
    budget
    selected plan

actual disclosure:
    representation identities/content identities
    ordering
    resulting cost
```

For a learned or externally served model, exact reproducibility may additionally require model/provider version, prompt/template version, decoding parameters, and—where available—randomness controls. These are replay metadata, not candidate identity.

CodeNib reaches a similar data-systems conclusion from a different design: it associates views with commits/profiles and records provider/tool provenance and usage in traces, while explicitly giving heterogeneous views separate validity/update semantics. citeturn15view0turn15view1 The transferable lesson is the separation of **what an artifact means** from **what must be logged to reproduce its production**.

### Applicability and invalidation

Selection decisions should be assumed **ephemeral by default**.

There is no strong reason to say:

```text
SelectionDecision X is true of repository snapshot Y
```

in the same sense that an import relation is true of repository state.

Instead:

```text
decision =
    f(
        information need,
        retrieval observations,
        policy/version,
        constraints,
        budget,
        available representations
    )
```

Change any material input and the old decision is no longer authoritative.

This does not require a universal `WorkspaceSnapshot`. Dependencies can remain as narrow as the operation permits.

There is one subtlety for lexical retrieval: an exact BM25 ranking can depend on collection-wide statistics such as document frequency and average document length. Consequently, exact replay may depend on the state/profile of the lexical index even when none of the ultimately selected files changed. That is a property of the retrieval operation, not justification for making every subsequent fact depend on an undifferentiated workspace snapshot.

Relation-derived surfacing can be more narrowly dependent:

```text
seed set
+
relevant exact import relations
+
expansion operation/configuration
```

A Context plan additionally depends on budget, policy, and representation availability.

Caching is still legitimate:

```text
cache key = digest(exact material inputs)
```

but such caching is an execution optimization. It should not be mistaken for reusable repository knowledge.

### What belongs in identity versus logs

A useful rule is:

> **If changing a field creates a different proposition or subject, it may belong to semantic identity. If changing it merely changes how an execution arrived at a result, it belongs in provenance/trace.**

Thus, selector version, BM25 score, candidate rank, token budget, and exclusion rationale generally do **not** belong in resource or relationship identity.

This directly argues against a heavily identified `Candidate` or `SelectionDecision` hierarchy.

## Evaluation, benchmark governance, and learned intelligence

**Evaluation model — J.** The current evaluation should expand along **causal stage boundaries**, not by replacing everything with downstream agent success.

A strong evaluation stack is:

| Question | Primary measures |
|---|---|
| Did candidate/surfacing mechanisms expose the necessary resources? | Candidate recall, oracle recall, positive-case hit rate, expansion count/cost, mechanism-specific recall delta. |
| Did purpose-relative decision-making choose well from what was available? | Precision/recall/F1 over the considered universe; Hit/MRR/NDCG only where ordering or graded relevance is actually part of the question; set coverage; false-admission rate; oracle-gap closure. |
| Did Context planning disclose useful information efficiently? | Gold-context/resource/line coverage, context precision, token efficiency, redundancy, representation cost, required-facet coverage, usage/drop where measurable. |
| Did the eventual agent accomplish the task? | Test-passing patch, task completion, edit correctness, answer quality, cost/latency. |

The four layers should be reported together but not substituted for one another.

ContextBench demonstrates why: it adds human-annotated gold Context and process metrics specifically because final issue-resolution success does not reveal how context was acquired; it measures recall, precision, and efficiency and finds substantial differences between context exploration and utilization. citeturn15view2turn18view2 RepoMirage reaches a compatible conclusion through perturbation: agents can explore broader context and still fail to turn that exploration into useful repository structure, making end-to-end success an insufficient diagnostic for context reasoning. citeturn15view12

Agent Retrieval Bench is similarly useful because it isolates upstream file retrieval and finds different winners for MRR, Recall@20, and token-budgeted context yield. citeturn18view3 This is particularly strong evidence against searching for one universal retrieval metric.

### Which metric answers which question

`Hit@K` is appropriate when the question is simply whether at least one relevant resource is available near the head.

`Recall@K` is more informative for multi-resource needs, but still treats all judged relevant resources as independent and equally necessary.

`MRR` is fundamentally a first-relevant-result measure. It is useful for locate-one-target tasks and much less informative for “understand these interacting components.”

Precision matters once expansion or selection can flood Context with distractors.

NDCG becomes justified when assessors can reliably provide **graded** relevance and when ordering matters. TREC's modern evaluations commonly support graded judgments precisely for this reason. citeturn14view1turn14view2 It should not be adopted merely because it is a standard IR metric.

MAP is useful for ranking over several relevant resources, but again assumes a ranking interpretation rather than a Context-set interpretation.

Token efficiency belongs to Context-level evaluation, not pure resource relevance.

Task completion belongs downstream.

No single metric should be declared “the selection metric.”

### Multi-resource completeness requires more than binary qrels

Binary per-resource relevance can remain the default wherever it answers the experiment.

It becomes inadequate when the benchmark wants to distinguish:

```text
either A or B is enough

from

A and B together are necessary

from

A gives the implementation,
B gives the contract,
C gives the regression behavior
```

The smallest extension is **benchmark-local coverage requirements**, not a universal ontology.

For example:

```text
Need:
    change import resolution safely

Coverage requirements:
    implementation:
        acceptable resources = {A}

    external contract:
        acceptable resources = {B, B2}

    behavioral/regression evidence:
        acceptable resources = {C, C2}
```

Then completeness can mean satisfying all required groups.

This representation permits acceptable alternatives without claiming that a task has one ontologically correct Context set. It can remain entirely in the benchmark/evaluation package.

### Benchmark judgment governance

The current explicit manual judgments remain sound as **case-local judgments**, provided their scope is kept honest.

TREC provides a useful caution: relevance is inherently judgment-dependent, and even established test collections distinguish information needs from queries and may rely on partial judgments selected through pooling. citeturn14view0turn14view1 The right lesson for `devtools` is not to build a richer universal relevance ontology. It is to record enough benchmark context to know what was judged.

For new purpose-sensitive cases:

```text
judgment should bind to:
    repository state
    explicit information need
    resource identity
    judgment value
    benchmark protocol/version
```

Binary labels remain preferable when assessors can make a clear relevant/not-relevant distinction.

Use graded relevance only when the experimental question truly depends on degree.

For important new purpose-paired cases, use at least independent second review or adjudication. Preserve disagreement as benchmark metadata rather than converting it into a global “confidence.”

Explicit controls should be recorded as **negative judgments for that information need**, not as repository facts.

To reduce benchmark leakage, mechanism development and threshold tuning should be separated from final cases, preferably with repository-disjoint held-out cases when enough data exists. CodeNib, for example, reports tuning graph-fusion weight on repository-disjoint tuning repositories before held-out evaluation. citeturn18view0 More importantly for Increment 21, the current seven real-repository cases should not be repeatedly modified until a purpose rule wins on them and then reported as evidence of generality.

### Deterministic versus learned boundary — K

Nothing in the recommended architecture depends on eventual selector technology.

A deterministic rule can consume:

```text
need
lexical results
directed relation supports
```

and return admissions.

A gradient-boosted ranker can consume the same material as features.

A cross-encoder can inspect need/resource pairs.

An LLM can jointly inspect a resource set.

An agent can make incremental decisions through tools.

A model can learn retrieval abstention, as Repoformer does. citeturn15view10 A task-specific system can learn generation-conditioned usefulness, as RLCoder does. citeturn15view11 A multi-path retrieval system can rerank after candidate generation, as CodeRAG does. citeturn15view9 None requires changing the fundamental truth conditions of Repository Intelligence.

The enduring architecture should therefore specify **inputs, outputs, and provenance**, not the model class:

```text
Input:
    purpose-bearing need
    available mechanism-specific retrieval observations
    repository knowledge as explicitly requested
    planning constraints

Decision implementation:
    arbitrary:
        deterministic
        statistical
        learned
        model-mediated
        interactive

Output:
    traceable decision / Context plan
```

The framework should not standardize feature vectors now. Doing so would simply relocate the premature universal-evidence abstraction.

## External evidence and adversarial falsification

**External evidence — L.** Current systems support a surprisingly conservative conclusion: effective repository/context systems repeatedly separate some stages and collapse others, depending on the operation. There is no convergence on a universal `Candidate → score → top-K` architecture.

| System / evidence | What it actually distinguishes or collapses | Transferable architectural lesson |
|---|---|---|
| **TREC evaluation methodology** | Distinguishes information need/topic from query and keeps relevance judgments in the evaluation collection. citeturn14view0turn14view1 | Query is not purpose; benchmark relevance is not corpus truth. |
| **SWE-agent** | Repository context is acquired through interactive search/navigation actions exposed by an agent-computer interface. citeturn15view6 | Candidate generation and selection can be operationally interleaved; a first-class selector is not required for capable behavior. |
| **Agentless** | Uses a procedural hierarchy: file localization → class/function localization → fine-grained localization, followed by repair/filter/rerank. citeturn15view7 | Stages can be task-specific procedures rather than universal domain abstractions. |
| **RepoGraph** | Builds repository definition/reference structure and uses keyword-centered subgraph retrieval integrated into procedural or agent systems. citeturn15view8 | Repository structure can provide a retrieval route; graph truth does not by itself establish task relevance. |
| **Repoformer** | Learns whether retrieval should occur because retrieved material can be unhelpful or harmful. citeturn15view10 | “More retrieval” is not monotonically better; abstention is a decision, not repository knowledge. |
| **RLCoder** | Learns retrieval from a generation-usefulness signal and includes stopping/candidate-retention behavior. citeturn15view11 | Usefulness may be consumer/model-conditioned and is not identical to semantic relevance. |
| **CodeRAG** | Separates query construction, multi-path retrieval, and preference-aligned reranking for repository-level completion. citeturn15view9 | Multi-stage retrieval is empirically viable, but its stages are task-specific—not proof of universal candidate abstractions. |
| **Aider repo map** | Uses reference/definition structure, heuristic weighting, PageRank, and a token budget to build repository Context. citeturn16view1turn16view2 | Pragmatic systems can collapse ranking, graph signals, budgeting, and Context construction; that can be useful without being a semantic template. |
| **CodeNib** | Maintains heterogeneous views with distinct contracts, performs planned retrieval/reranking/graph expansion, and separately studies bounded Context-delivery policies. citeturn15view0turn18view0 | Closest external support for preserving heterogeneous evidence and operation-specific semantics rather than universalizing outputs. |
| **RepoNav** | Leaves underlying retrieval scores intact but reorganizes retrieved evidence into file-centered structural Context. citeturn15view5 | Retrieval success and Context representation are independent axes. |
| **ContextBench** | Separately measures retrieved Context and downstream task success, and observes recall/precision, redundancy, and utilization gaps. citeturn15view2turn18view1turn18view2 | Candidate recall, selection quality, final Context, and task success must be independently inspectable. |
| **Agent Retrieval Bench** | Compares several retrieval families on different task types and metrics; no family dominates every measure. citeturn18view3 | Purpose and evaluation objective materially alter which retrieval mechanism looks best. |
| **RepoMirage** | Uses repository perturbations to isolate context-reasoning failures from final task success. citeturn15view12 | Downstream success cannot substitute for causal process evaluation. |

The most important negative result from this survey is the **absence** of evidence for a universal semantic relevance layer. Current systems implement ranking, reranking, navigation, graph expansion, context maps, interactive search, and learned retrieval policies, but the successful representation of one mechanism is not generally promoted into an ontology covering all the others.

### Adversarial questions

| Challenge | Assessment |
|---|---|
| **A. Why not simply increase lexical K and let Context decide?** | This is a legitimate architecture, and in fact it is close to the recommendation. Increasing K merely expands the consideration universe; Context then performs purpose-relative planning. The objections are operational and empirical, not semantic: larger retrieval can add noise/cost, and aggressive recall expansion can reduce precision. ContextBench observes precisely this tradeoff, while Repoformer demonstrates that unconditional retrieval can hurt generation. citeturn18view1turn15view10 Therefore “larger K + Context” should be an experimental baseline, not rejected a priori. |
| **B. Why not add relation-derived candidates directly to Context and eliminate a selector?** | **Yes—provided “add to Context” means add to Context planning's consideration inputs, not blindly disclose.** This is currently preferable to a standalone selector. Exact relation provenance must remain visible so Context can decide whether it matters for the purpose. |
| **C. Why not use an LLM to rank every candidate?** | It is a future decision implementation, not an architecture. It adds latency/cost and potentially nondeterminism; pointwise ranking also does not inherently solve complementarity, redundancy, representation choice, or disclosure policy. ContextBench's comparison of sophisticated scaffolds with simple search is additional warning against assuming more model mediation is inherently better. citeturn18view1 |
| **D. Why not train one learning-to-rank model over all evidence?** | Possible later, but it requires a defined target and enough representative labels. The present labels are tiny, case-local, and mostly binary; Agent Retrieval Bench finds different retrieval families winning different tasks and objectives, which argues against assuming one task-independent objective now. citeturn18view3 A learned model can eventually consume heterogeneous features without changing the architecture. |
| **E. Why not normalize every retrieval mechanism into a common score?** | Because there is no demonstrated shared unit. Score calibration can be implemented by a particular fusion/model once an objective exists, but normalizing evidence merely to satisfy an interface creates false commensurability. CodeNib's explicit separation of graph expansion from dense scoring is a useful counterexample to mandatory normalization. citeturn18view0 |
| **F. Why not define one generic `Candidate[T]` abstraction now?** | Because the only universal semantics would be “T was considered.” Resource identity already identifies T; all interesting fields are mechanism-specific. A generic type would either be nearly empty or pressure scores, evidence, confidence, and applicability into a false common model. |
| **G. Why not make Context responsible for everything after Repository Intelligence?** | This is almost viable, but Retrieval still deserves a boundary because lexical search and future repository searches have their own request/result semantics, indexes, replay requirements, performance metrics, and reusable operations. The minimum is therefore RI → Retrieval → Context, with selection internal to Context rather than a fourth domain. |
| **H. Why not treat retrieval relevance itself as DerivedKnowledge?** | Because relevance changes with the information need while repository state can remain identical. That violates the intended truth conditions of Repository Intelligence. |
| **I. Why not model relevance as a repository relationship?** | Because one endpoint would effectively be a task/information need, not another repository entity, and the relation would be judgment- and purpose-relative. It is an evaluation/task relation, not repository structure. |
| **J. Why isn't existing manually judged relevance sufficient?** | It is sufficient for the questions it currently answers: resource retrieval for explicit needs. It is not sufficient for marginal usefulness, acceptable alternative contexts, multi-resource completeness, representation granularity, token efficiency, or downstream utilization. |
| **K. Why isn't top-K ranking sufficient?** | Because selection may be set-valued and contextual. Redundancy and marginal contribution make the value of a resource depend on what is already selected; MMR is the classic IR counterexample. citeturn17search18 Context budgets also apply to representations whose costs differ. |
| **L. Why shouldn't relationship multiplicity imply stronger relevance?** | Because repeated relations need not be independent evidence. Repeated imports can reflect syntax/style rather than task importance. Keep multiplicity available as a feature; require empirical evidence before assigning monotonic weight. |
| **M. Why shouldn't tests be penalized for implementation-focused needs?** | Because “implementation-focused” is not a reliable proxy for irrelevance. Change-safety needs can make tests central; Agent Retrieval Bench even treats `code2test` and `edit2ripple` as explicit retrieval tasks. citeturn15view3 Your own structural experiment already found source/test location insufficient to determine relevance. |
| **N. Why shouldn't directory/package location contribute automatically?** | Because your path-proximity experiments did not establish it, and raw filesystem structure is not the same proposition as semantic relation. Location can be retained as data or tested later as a need-conditioned feature; it should not receive an unconditional relevance bonus. |
| **O. Why should a selection decision be reusable at all?** | It generally should not. Default to ephemeral execution evidence. Cache exact deterministic executions by dependencies if useful; do not give the decision repository-knowledge semantics. |
| **P. Could the proposed selection layer be a benchmark artifact?** | **Yes, as a standalone class/domain.** `K=5` creates pressure to imagine a clean selection stage that real Context planning may not possess. The deeper distinction is nevertheless real: surfaced true relationships can be irrelevant to a purpose, and retrieved Context can go unused downstream. citeturn18view2 The answer is to preserve the decision boundary in traces and evaluation while declining to create a Selection domain prematurely. |

The strongest falsification of the current four-stage framing is therefore not that selection is meaningless. It is that **selection may be an internal concern of Context planning rather than a reusable entity in its own right**.

## Increment 21, failure modes, and deliberate non-decisions

**Failure modes — M.** The recommended minimalist architecture has real risks.

The first is **pushing too much intelligence into Context**. If Context becomes an unrestricted place where arbitrary retrieval, ranking, graph traversal, model inference, and policy logic accumulate, “no Selector domain” simply becomes a euphemism for a monolith. The guardrail is not another class hierarchy; it is that Retrieval operations must retain their own request/result semantics, while Context planning may consume but not silently reinterpret repository facts.

The second is **under-modeling information need**. Merely retaining user text does not magically make a deterministic policy purpose-aware. The recommendation is only that purpose *semantics* can initially remain in the request rather than a taxonomy. If Increment 21 demonstrates that two needs with identical retrieval queries require reliably different decisions, then some explicit request-level distinction is proven necessary. If downstream callers already possess such structured information, it should be preserved rather than re-inferred.

The third is **accidentally rebuilding Candidate through aggregation code**. An experimental dictionary keyed by resource can gradually acquire fields such as `score`, `confidence`, `status`, `reason`, `selected`, and `cost` until it is effectively a universal Candidate without an explicit semantic decision. Prevent that by keeping mechanism results immutable and treating grouping as a view.

The fourth is **letting Context planning mutate evidence**. A decision procedure may derive features from retrieval observations, but the original lexical and relationship evidence should remain recoverable. Otherwise a combined score becomes impossible to audit.

The fifth is **confusing oracle headroom with a practical selection solution**. Showing that lexical-plus-relational consideration contains a better size-five subset does not prove a real selector can identify it. It establishes only that candidate generation has made improvement possible.

The sixth is **benchmark overfitting**. Seven real-repository cases are enough to reveal semantic counterexamples but nowhere near enough to justify a universal weighting function, learned ranker, or repository heuristic.

The seventh is **mistaking manual qrels for unique gold Context**. ContextBench explicitly notes that real tasks can admit multiple valid patches and evaluates robustness of its gold context under alternative solutions. citeturn18view2 `devtools` should similarly allow acceptable alternative resources or requirement groups when the task warrants them.

The eighth is **premature optimization around a resource abstraction**. RepoNav's results are an important warning: even after the correct file has been reached, structure and presentation affect target identification. citeturn15view4turn15view5 Resource-level selection can therefore become a bottleneck abstraction if treated as equivalent to final Context construction.

### Explicit non-recommendations — N

Before Increment 21, the evidence does **not** justify introducing:

| Tempting abstraction/mechanism | Recommendation now |
|---|---|
| `Candidate[T]` | **Do not introduce.** |
| Candidate semantic identity | **Do not introduce.** Use resource identity plus execution membership. |
| `CandidateEvidence` superclass | **Do not introduce.** Preserve mechanism-specific result types. |
| First-class `Selector` domain/service | **Do not introduce.** Test decision semantics inside the experiment/Context planning. |
| Universal `RelevanceScore` | **Reject.** |
| Weighted `lexical + relation + structural + …` formula | **Do not promote.** A particular experiment may test one later, but it has no foundational semantics. |
| Universal confidence score | **Reject.** |
| Undirected repository graph abstraction | **Reject.** Preserve exact directed relation semantics. |
| Generic graph database/infrastructure | **Not justified.** |
| Embedding/vector database | **Not justified by the present question.** |
| Cross-encoder reranker | **Not yet justified.** |
| LLM reranker | **Not yet justified.** |
| Classical/gradient-boosted learning-to-rank | **Not yet justified.** |
| Source/test penalty | **Reject absent need-specific evidence.** |
| Directory/package proximity bonus | **Reject absent new evidence.** |
| Relationship-multiplicity bonus | **Reject as default.** Retain multiplicity as observable data only. |
| Generic negative-evidence ontology | **Reject.** |
| Universal task/intent ontology | **Reject.** |
| Whole-workspace applicability for every decision | **Reject.** Track concrete dependencies. |
| Production notion of reusable relevance knowledge | **Reject.** |
| K as a foundational budget | **Reject.** K remains an experimental/retrieval width. |

This is intentionally more conservative than several current research systems. For example, RepoGraph uses a repository graph and subgraph retrieval successfully in its evaluated systems, and CodeRAG uses multi-path retrieval plus reranking. citeturn15view8turn15view9 Those results establish that such mechanisms can work in particular systems; they do not establish that `devtools` needs their abstractions before it has established the semantics of the decision being made.

### Increment 21 implications — O

Increment 21 should be **an architectural falsification experiment, not a selection implementation**.

The exact question should be:

> **For the same surfaced repository universe, can two different purpose-bearing information needs require different resource decisions, and does preserving lexical and directed relationship support separately provide usable decision information beyond simply increasing lexical width?**

A second, subordinate question is:

> **Does the union of lexical and relationship-derived surfacing contain genuine oracle headroom under equal final resource capacity, or are the apparent gains merely the result of considering more resources?**

These questions test whether purpose-relative decision-making is a real architectural requirement and whether relation-derived support is worth exposing downstream. They do **not** assume that a selector is the answer.

#### Production code

**No new production `Selector`, `Candidate`, `Evidence`, relevance model, or score-fusion API is justified for Increment 21.**

Prefer benchmark/experiment-local code.

The only production change worth considering would be one required to expose information that already has clear semantics but is currently lost—for example, exact relation-expansion provenance. Even then the new output should be specific to that retrieval operation, not generalized into a candidate framework.

If the existing retrieval API cannot distinguish the purpose-bearing request from the lexical query, make that distinction in the evaluation fixture first. Promotion into a production `InformationNeed` type should require evidence that a real production boundary must carry it.

#### Smallest required experimental values and operations

The experiment needs only:

```text
NeedCase:
    information_need
    lexical_query
    judgments
```

plus existing lexical results and a narrow relationship-expansion record such as:

```text
ImportExpansionResult:
    target_resource
    seed_resource
    seed_rank
    relationship
    direction
```

and an ephemeral operation:

```text
group_by_resource(
    lexical_results,
    expansion_results,
) -> mapping[ResourceIdentity, tuple[typed_result, ...]]
```

No common base class is required.

A benchmark-local assessment result may record:

```text
resource
judgment / admission
reason-code if the tested rule has one
```

but it should not become production `SelectionDecision` until reuse demands it.

#### Controlled fixtures

Fixtures should be constructed to falsify simplistic semantics, not merely demonstrate a happy path.

At minimum, include these conditions:

| Fixture | What it tests |
|---|---|
| Same repository, same lexical query, **paired purposes** | Demonstrates whether information need must be represented independently from query. |
| Lexically obvious relevant implementation | Ensures relation machinery does not degrade easy lexical behavior. |
| Lexical miss exposed by outgoing relation | Tests genuine relational headroom. |
| Lexical miss exposed by incoming relation | Tests direction independently. |
| True relation to explicit irrelevant control | Reproduces the central “truth ≠ relevance” invariant. |
| Several repeated relations to an irrelevant target, one relation to a relevant target | Falsifies automatic multiplicity-as-relevance. |
| Relevant test for a change-safety need | Falsifies unconditional test penalty. |
| Irrelevant nearby/source-path resource | Falsifies package/path priors. |
| Two redundant relevant resources plus one complementary resource | Demonstrates ranking-versus-set-selection distinction. |
| Resource useful only as a small declaration/derived fact | Establishes resource-selection-versus-disclosure distinction. |

The purpose-pair fixture is particularly important:

```text
query:
    "import resolution"

need A:
    "Locate the implementation of import resolution."

need B:
    "Identify the repository Context needed to change
     import resolution safely."
```

A relation-derived test, caller, contract, or integration resource may legitimately be irrelevant to A but relevant to B, while the implementation is relevant to both. If assessors cannot consistently make such distinctions, that is evidence **against** introducing richer purpose semantics now.

#### Real-repository cases

Reuse the seven Increment 20 cases rather than immediately building a broad benchmark, but change the experimental design.

Cases where outgoing/incoming expansion exposed `resource.py`, the filesystem resource implementation, or `bm25.py` are particularly useful because they already establish that the relation mechanism can surface lexical misses. The next question is not whether those misses exist; it is whether a purpose-sensitive decision can distinguish them from the genuine but irrelevant relationship controls.

Create paired information needs only where they are naturally defensible. Do not mechanically double every case.

A good initial target is roughly a dozen explicitly judged needs, including the existing seven and a small number of paired-purpose variants. That is enough to test semantic counterexamples; it is **not** enough to fit or claim a universal ranking policy.

Freeze the new cases before testing decision heuristics against them.

#### Experimental arms

The smallest informative comparison is:

```text
A. canonical lexical top-5
B. larger lexical consideration universe, Context oracle/select at 5
C. lexical + outgoing relation consideration universe, oracle/select at 5
D. lexical + incoming relation consideration universe, oracle/select at 5
E. lexical + both directed relation mechanisms, oracle/select at 5
```

The use of an **oracle** at this stage is deliberate. It answers the architectural question:

> Does this consideration universe contain a better possible size-five result?

before asking:

> Can we build a general selector that finds it?

That separates generation headroom from selection capability.

Report, for each arm:

```text
candidate/consideration recall
candidate count
oracle Recall@5
oracle precision@5 where meaningful
number and type of controls exposed
support paths for recovered relevant resources
support paths for admitted irrelevant resources
```

Then, and only then, add **one deliberately simple deterministic decision baseline** if there is enough headroom to make selection meaningful.

That baseline should not be a weighted formula. A better test is a transparent admission policy with exact rules chosen before the held-out real cases. Its purpose is not to become production; it is to discover whether typed relationship support can be used without fusion.

#### Evidence that must be retained

For every surfaced resource:

```text
information need
lexical query

resource identity/address

if lexical:
    content score
    filename score
    combined score
    original rank

if relationship-derived:
    exact seed
    seed's lexical rank
    exact relation/declaration provenance
    direction
    target
    every distinct support path

benchmark judgment for this need
explicit control status, where applicable
```

For every experimental decision:

```text
consideration universe
decision policy/version
admitted/excluded resources
ordering if one is produced
capacity condition
```

Do **not** replace the support paths with a support count.

#### Success criteria

Increment 21 should count as architectural evidence for a purpose-relative decision step if all of the following are observed:

1. **Purpose sensitivity:** at least some paired needs sharing the same lexical query and repository state have defensibly different resource judgments.

2. **Generation headroom:** the heterogeneous consideration universe achieves better candidate recall than the canonical lexical baseline on at least some held-out cases.

3. **Selection headroom:** under equal final capacity, an oracle subset of the heterogeneous universe can outperform lexical top-5. This proves that the expanded universe contains useful choices rather than merely more noise.

4. **Blind-expansion failure remains visible:** simply inserting all relation-derived resources or using relation multiplicity as priority does not reproduce the oracle gain. This maintains the Increment 20 distinction between relationship truth and relevance.

5. **Typed evidence matters:** incoming/outgoing direction, seed identity, or exact support path explains at least one materially different outcome that would be lost by collapsing all relation support to a boolean or generic graph score.

These results would justify **purpose-relative planning semantics**. They would still *not* automatically justify a first-class Selector.

A standalone production selector would need additional evidence: a stable contract used by more than one caller/mechanism, with decision behavior that remains meaningful independently of Context representation and budgeting.

A universal Candidate would need an even stronger showing: several mechanisms must require a durable cross-stage object whose semantics cannot be represented as resource identity plus typed retrieval observations. Nothing in the current evidence reaches that threshold.

#### Failure criteria

The experiment should count against further architecture if:

- relation expansion supplies no additional judged-relevant resources beyond a slightly larger lexical K;
- heterogeneous candidate recall rises but oracle fixed-capacity quality does not;
- apparent improvement disappears on held-out cases;
- paired purposes do not result in stable judgment differences;
- direction/multiplicity/provenance provide no useful discriminatory information;
- gains arise only because the expanded arm gets a larger final budget;
- any apparently good deterministic rule merely memorizes the current seven cases.

Under those outcomes, production should remain lexical and the proposed selection architecture should be deferred.

#### Explicitly out of scope for Increment 21

Keep all of the following out:

```text
embeddings
vector databases
cross-encoders
LLM reranking
learning-to-rank
gradient boosting
universal score normalization
graph databases
generic graph traversal infrastructure
Candidate[T]
CandidateEvidence
Selector interface
confidence calibration
source/test penalties
directory/package scoring
dynamic module-root inference
new workspace snapshot abstractions
token-optimal Context compilation
automatic intent classification
task ontologies
production usefulness prediction
```

Increment 21 should settle a semantic boundary, not demonstrate maximum retrieval capability.

### Open questions — P

Several questions should deliberately remain unresolved.

**Whether `InformationNeed` becomes a production type.** The distinction from query is justified; the need for a new public value type is not yet established. An existing Context request or task object may already be the appropriate carrier.

**Whether selection eventually deserves its own boundary.** Promote it only if several independent consumers require reusable purpose-relative resource decisions *before* Context representation and budgeting. Otherwise keep it within Context planning.

**Whether usefulness should ever be first-class.** Generation-conditioned systems such as RLCoder demonstrate that usefulness can be operationalized for a specific consumer. citeturn15view11 That does not establish a framework-wide usefulness proposition.

**Whether heterogeneous mechanisms should ever be calibrated to a common probability or utility.** A sufficiently large task-specific dataset may justify calibration or learning-to-rank. The current evidence does not.

**Whether relation multiplicity has predictive value.** Preserve the raw multiplicity and provenance so this can later be tested. Do not assign it semantics now.

**Whether candidate-set complementarity needs an explicit coverage model.** Increment 21 should use benchmark-local coverage obligations only where necessary. A production subtopic/facet ontology would be premature.

**Whether Context planning should be one-shot or interactive.** SWE-agent-style incremental navigation and RepoNav-style continuation both demonstrate that useful Context acquisition can remain interactive rather than resolve into one static selected set. citeturn15view6turn15view5 The proposed architecture permits both.

**Whether learned intelligence belongs in Retrieval or Context.** There is no need to decide this globally. A retrieval-specific reranker can live with Retrieval; a model that reasons jointly about purpose, representations, redundancy, and token cost naturally belongs to Context planning. Both can consume the same repository facts without changing their semantics.

**Whether relevance should become graded.** Keep binary judgments until a concrete evaluation question requires reliable degree distinctions. Graded qrels are well established in IR, but their availability does not make them mandatory. citeturn14view1turn14view2

**Whether relationship expansion deserves promotion to production retrieval.** Increment 20 says no. Increment 21 should test whether relationship-derived surfacing creates *selectable headroom* once purpose is represented. Until that is shown, the correct production retriever remains the established lexical mechanism.

The resulting pre-Increment-21 architectural position can be stated compactly:

```text
Repository Intelligence
    owns purpose-independent truth.

Retrieval
    owns mechanism-specific attempts to surface useful repository material.
    Its results retain their native semantics.

Candidatehood
    is ephemeral membership in a consideration universe,
    not knowledge and not yet a first-class entity.

Relevance
    is purpose-relative and currently primarily an evaluation judgment.

Selection
    is a real decision concept,
    but not yet a justified standalone architectural domain.

Context planning
    owns the eventual purpose-, representation-, policy-, redundancy-,
    and budget-aware decision about what can usefully be disclosed.

Context disclosure
    is the actual bounded information supplied to the consumer.
```

The strongest recommendation is therefore **not to implement the missing Selection layer**. It is to make Increment 21 determine whether such a layer exists outside the benchmark at all. The framework already has the crucial semantic ingredients: durable repository truth, typed lexical evidence, exact directed relationship knowledge, explicit judgments, and Context as the disclosure boundary. The next increment should preserve those distinctions and test the one missing proposition—**whether purpose-sensitive decisions over heterogeneous surfacing genuinely require a reusable abstraction**—before naming that abstraction into existence.
