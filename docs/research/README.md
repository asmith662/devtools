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
| [Purpose-relative repository Context](purpose-relative-repository-context.md) | Retrieval, decision, disclosure | Reconciled | Truth, surfacing, relevance, ranking, disclosure differ | 0003, 0004 | Lexical and import experiments | Universal Candidate/Selector/score | Increment 20 | Stable need-specific selection value |
| [Retrieval architecture synthesis](retrieval-architecture-synthesis.md) | Retrieval portfolio and research recovery | Reconciled synthesis | Heterogeneous portfolio; direct acquisition; decision and disclosure remain distinct | 0002-0004 | Filename BM25; exact-name lookup; import knowledge | Semantic/learned retrieval, progressive disclosure, shadow comparison | Increments 16, 20, 21 | Held-out decision rule; direct-lookup controls; semantic prerequisites |
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
the Increment 10-21 empirical lineage; it records shadow comparison as a
research-recovery gap rather than an accepted mechanism.

## Research governance

1. Give new research a stable subject-oriented filename.
2. Preserve its substantive body.
3. Add or update its `## Disposition` section.
4. Add it to this README.
5. Link durable accepted decisions to an ADR.
6. Preserve deferred and rejected-for-now findings rather than deleting them.
7. Update the disposition when later ADRs, implementation, experiments, or
   research materially change its status.
