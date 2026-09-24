# Research Evidence

This directory preserves durable architectural investigations, alternatives,
criticisms, recommendations, and unresolved questions. Research is evidence and
historical reasoning; it does not automatically define current architecture,
authorize implementation, replace an ADR, or override current source and tests.

ADRs disposition durable architectural decisions. The architecture taxonomy and
`docs/architecture.md` describe accepted current semantics. Implementation and
tests demonstrate realized behavior. Experiments and evaluations provide bounded
empirical evidence. Deferred and rejected-for-now findings remain discoverable
because later evidence may justify reconsideration.

| Research document | Subject | Status | Principal findings | Related ADRs | Implemented evidence | Deferred / rejected for now | Superseded/refined by | Revisit triggers |
|---|---|---|---|---|---|---|---|---|
| [Architecture adversarial review](architecture-adversarial-review.md) | Adversarial architecture challenge | Partially reconciled | Preserve evidence boundaries; resist premature abstractions | 0002-0004 | Lexical evaluation | Universal graph/store; model knowledge promotion | ADRs; Inc. 16/20 | Bounded evidence requiring reusable semantics |
| [Framework domain boundaries](framework-domain-boundaries.md) | Framework ownership | Reconciled | Narrow orthogonal domains | 0001, 0004 | Runtime/Tool/Context separation | Workflow infrastructure | Taxonomy | Cross-domain consumer pressure |
| [Purpose-relative repository Context](purpose-relative-repository-context.md) | Retrieval, decision, disclosure | Reconciled | Truth, surfacing, relevance, ranking, disclosure differ | 0003, 0004 | Lexical and import experiments | Universal Candidate/Selector/score | Increments 20-22 | Stable need-specific value requiring reuse beyond local policy/Context planning |
| [Retrieval architecture synthesis](retrieval-architecture-synthesis.md) | Retrieval portfolio and research recovery | Reconciled synthesis | Heterogeneous portfolio; direct acquisition; purpose-bearing admission and disclosure remain distinct | 0002-0004 | Filename BM25; exact-name lookup; import knowledge; Increments 23-26 offline evaluation | General Selector, production relationship expansion, further neural retrieval | Increments 16, 20, 21, 22, 23, 24; [retrieval landscape](repository-retrieval-algorithm-landscape.md) | Foundational retrieval and independent-repository evidence |
| [Structural repository retrieval](structural-repository-retrieval.md) | Typed structural evidence, graph representation, and candidate generation | Reconciled research evidence | Native typed relationships; physical graph form remains open; test bounded structural complementarity against lexical widening | 0002, 0003 | Qualified import relations and Increment 25 | Universal graph/store/API, recursive traversal, PageRank, learned ranker, production expansion | ADR-0002/0003 reconciliation; [retrieval landscape](repository-retrieval-algorithm-landscape.md) | Concrete consumers and measured structural complementarity across repositories |
| [Repository retrieval algorithm landscape](repository-retrieval-algorithm-landscape.md) | Retrieval variables and experimental sequence | Current research recommendation | Measure depth, unit, representation, fields, fusion, and disclosure separately | 0002-0004 | Increments 25-26 development | Generic graph/vector infrastructure and retrieval-local training | — | Foundational ablations and independent-repository evidence |
| [Repository Context system](repository-context-system-architecture.md) | Repository intelligence and Context | Partially reconciled | Deterministic intelligence precedes model use | 0002-0004 | Corpus and lexical retrieval | Vectors, change impact, progressive disclosure | Later ADRs | Independent bounded evidence |
| [Derived knowledge boundary](repository-derived-knowledge-boundary.md) | Qualification and applicability | Reconciled | Provenance/coverage differ from knowledge | 0002, 0004 | Bounded derivations | Universal claim/confidence | ADR-0002 | Shared consumer need |
| [Repository information boundaries](repository-information-boundaries.md) | Derivation versus representation | Reconciled | Context synthesis is not automatic knowledge | 0002, 0004 | Materialization/rendering | Automatic model knowledge promotion | ADR-0004 | Reusable semantic assertion |
| [Repository intelligence review](repository-intelligence-architecture-review.md) | Comparative architecture | Partially reconciled | Layered intelligence/retrieval/disclosure | 0002-0004 | Snapshot and lexical slices | Universal graph, mandatory mechanism | ADRs/experiments | Useful bounded slice |
| [Snapshot identity](repository-snapshot-identity.md) | State and reuse | Partially reconciled | Content-derived state differs from delta/Git | 0002 | Snapshot/content identity | Policy, delta, maintenance | ADR-0002 | Observation/maintenance consumer |
| [Subject identity](repository-subject-identity-and-decomposition.md) | Subjects and source anchors | Reconciled | Subjects, source occurrences, and continuity differ | 0002 | Function declarations | AST identity, monolithic graph | ADR-0002 | Another subject family |
| [Runtime Evidence governance](runtime-evidence-governance.md) | Attempts and historical Evidence | Partially reconciled | Evidence is not live control state | 0001 | InteractionAttempt/Evidence | Generic event/trace/workflow machinery | Taxonomy | Durable/replay consumer |

## Research lineage

Snapshot identity and subject decomposition informed repository-intelligence and
DerivedKnowledge boundaries, then ADR-0002. Repository/Context architecture,
adversarial criticism, and the purpose-relative investigation informed ADR-0003
and ADR-0004. Framework-boundary and Runtime-Evidence research separately
informed the narrow Runtime, Tool, Context, and Evidence taxonomy.
The retrieval-architecture synthesis reconciles this corpus with B-0002 and
the Increment 10-24 empirical lineage. Increment 23 validates the bounded
capture/blinding/evaluation chain but finds directional-reservation-v1 not ready
for shadow: it has zero net known-useful gain, one not-useful admission, and one
useful loss. Increment 24 then finds no local improvement from its predeclared
purpose-relative deterministic ranking over the same devtools surface. At that
checkpoint the pressure was distinct candidate-generation evidence and
independent-repository validation, not a generic shadow platform or production
decision policy.
The structural-retrieval investigation then reframed the question from how
relationship evidence should occupy K=5 to whether bounded typed structure can
surface useful resources that candidate-volume-matched lexical widening does
not. Increment 25 and Increment 26 development supplied bounded structural and
semantic evidence. The repository-retrieval landscape now recommends testing
retrieval foundations before further evidence-family escalation; the
[roadmap](../roadmap.md) owns the current sequence.

## Research governance

1. Give new research a stable subject-oriented filename.
2. Preserve its substantive body.
3. Add or update its `## Disposition` section.
4. Add it to this README.
5. Link durable accepted decisions to an ADR.
6. Preserve deferred and rejected-for-now findings rather than deleting them.
7. Update the disposition when later ADRs, implementation, experiments, or
   research materially change its status.
