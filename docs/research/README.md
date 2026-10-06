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

## Current retrieval research checkpoint

[Experimental R1 method](../../experiments/identifier_sparse/README.md) and
[prospective Case 0009](../../experiments/codex_dogfood/case_0009/README.md) now
record the whole-identifier-plus-subtoken treatment and its
[Stage D evaluation](../../experiments/codex_dogfood/case_0009/analysis.md):
**RETAIN AS SEPARATE RETRIEVAL VIEW**, with unchanged REQUIRED positive reach and
mixed ranking gains/regressions. Canonical BM25 is unchanged. Mandatory R2
true BM25F is next regardless of the R1 result.

The [retrieval foundation](../architecture/retrieval.md) owns current production
status and reconciled empirical interpretation. The
[two-track roadmap](../roadmap.md#current-sequencing) mandates **R1 additive
whole identifiers + subtokens, then R2 true BM25F regardless of R1 outcome**.
Representation and fielding must remain separately attributable; A–D arms and
cost/coverage/discrimination metrics are specified there. BM25F is a mandatory
empirical benchmark, not an optional idea or production adoption.

Protocols must declare a primary [failure class](../architecture/taxonomy.md#retrieval-and-localization-failure-classes)
before treatment execution. Query representation, semantic mismatch, semantic
granularity, candidate discrimination and valid labels remain open. Unjudged
is not negative. Direct structural value does not imply blind diffusion value;
the CodeRankEmbed probe did not disprove dense retrieval. Prospective semantic
resolution effectiveness is paused pending R1/R2 progress unless an explicit
concrete reason justifies earlier parallel work. Historical "next" recommendations
below and in retained bodies do not override the current roadmap.

For downstream continuity, the [Localization status/history owner](../architecture/localization.md)
links Cases 0004–0008, the production resolution kernel, experimental external
adapter and future frontier/acquisition/sufficiency chain. The
[roadmap resumption point](../roadmap.md#localization-resumption-after-the-retrieval-checkpoints)
returns to a new prospective claim-level semantic-resolution case after R1/R2
by default. Structural breadth is closed for now; its operators remain available.

## Research inventory

| Research document | Subject | Status | Principal findings | Related ADRs | Implemented evidence | Deferred / rejected for now | Superseded/refined by | Revisit triggers |
|---|---|---|---|---|---|---|---|---|
| [Architecture adversarial review](architecture-adversarial-review.md) | Adversarial architecture challenge | Partially reconciled | Preserve evidence boundaries; resist premature abstractions | 0002-0004 | Lexical evaluation | Universal graph/store; model knowledge promotion | ADRs; Inc. 16/20 | Bounded evidence requiring reusable semantics |
| [Framework domain boundaries](framework-domain-boundaries.md) | Framework ownership | Reconciled | Narrow orthogonal domains | 0001, 0004 | Runtime/Tool/Context separation | Workflow infrastructure | Taxonomy | Cross-domain consumer pressure |
| [Purpose-relative repository Context](purpose-relative-repository-context.md) | Retrieval, decision, disclosure | Reconciled | Truth, surfacing, relevance, ranking, disclosure differ | 0003, 0004 | Lexical and import experiments | Universal Candidate/Selector/score | Increments 20-22 | Stable need-specific value requiring reuse beyond local policy/Context planning |
| [Retrieval architecture synthesis](retrieval-architecture-synthesis.md) | Retrieval portfolio and research recovery | Historical synthesis; current foundation qualified | Heterogeneous portfolio; direct acquisition; admission and disclosure remain distinct | 0002-0004 | Filename BM25; exact lookup; native direct/PPR/map channels now inventoried in current foundation | Universal Selector/default recursive expansion; neural production promotion | [Current retrieval foundation](../architecture/retrieval.md) and roadmap | Mandatory R1/R2 and independent-repository evidence |
| [Structural repository retrieval](structural-repository-retrieval.md) | Typed structural evidence, graph representation, and candidate generation | Reconciled historical research | Native typed relationships; physical graph form remains open; bounded structural complementarity against lexical widening | 0002, 0003 | Qualified native relations, direct retrieval, optional production PPR/map; Increment 25 historical evidence | Universal graph/store/API, default recursive traversal/diffusion and learned ranker | ADR-0002/0003; current retrieval foundation | Relation-specific useful novelty and purpose-relative discrimination |
| [Repository retrieval algorithm landscape](repository-retrieval-algorithm-landscape.md) | Retrieval variables and experimental sequence | Historical prospective recommendation | Measure depth, unit, representation, fields, fusion, and disclosure separately | 0002-0004 | Increments 25-26 development | Generic graph/vector infrastructure and retrieval-local training | Breadth production gate | Independent-repository evidence |
| [Repository retrieval breadth production gate](repository-retrieval-breadth-production-gate.md) | Completed Tier-1 breadth evidence and production dispositions | Accepted development synthesis | Direct structural useful reach, graph fan-out, heterogeneous selection gap, and bounded RI/Context/Evaluation migration | 0002-0004 | Increments 25-36 development | Universal graph, default structural rank, generic experiment platform, confirmation inference | Retrieval landscape's prospective sequence | Independent-repository evidence, production semantic counterexample, or a bounded selection policy |
| [Repository Context Planning and graph-assisted retrieval](repository-context-planning-and-graph-assisted-retrieval.md) | Context Planning, progressive disclosure, repository maps, Aider-style ranking, PPR, heterogeneous evidence fusion and RRF | Partially adopted; later admission refinement | Separate disclosure from retrieval; distinguish graph mechanisms and progressive acquisition | 0003, 0004 | Explicit plans, qualified Reference disclosure, PPR/map and composition | Default resource fusion, recovery guarantee, learned decisions | [Heterogeneous admission and recovery](heterogeneous-context-admission-and-recovery.md); roadmap | Prospective representation/planning outcomes |
| [Repository Context system](repository-context-system-architecture.md) | Repository intelligence and Context | Partially reconciled | Deterministic intelligence precedes model use | 0002-0004 | Corpus and lexical retrieval | Vectors, change impact, progressive disclosure | Later ADRs | Independent bounded evidence |
| [Heterogeneous Context admission and recovery](heterogeneous-context-admission-and-recovery.md) | Option admission, scoped coverage, progressive requests and learning seam | Context ownership retained; lane policy historical | Representation admission, native provenance and bounded assessment remain useful | 0003-0005 | Existing plans/materializers and Cases 0001-0003; policy unimplemented | Question-lane floors/weights as next build; sufficiency probabilities and controller | ADR-0005 | Obligation and representation outcomes |
| [Obligation-driven repository Localization](obligation-driven-repository-localization.md) | Supplied deep research: obligations, role routing, hypothesis resolution and stopping | Retained intact; boundary reconciled | Distinct Localization responsibility; shared anchors; global recall; bounded satisfaction and proof-scoped negatives | 0005 | Caller-authored kernel, lexical lanes, roles/routing, grounding, bounded generation and explicit resolution recording; automatic policy absent | Mandatory TaskModel/evidence hierarchy, numeric confidence, generic sequential/learned planner | ADR-0005, current retrieval foundation and roadmap | Prospectively frozen obligation coverage, false elimination, acquisition/Context cost and discovery frontier |
| [Direct Reference witness generation](direct-reference-witness-generation.md) | Exact inverse Python References as Localization candidates | Investigation complete; bounded operator implemented | Native facts support exact resource projection; explicit branching and visible bounds | 0002, 0003, 0005 | Production referencing-resource adapter; prospective Cases 0007/0008 analyzed | Implicit complementarity, arbitrary first-K truncation, graph expansion | Localization package and current roadmap | New relation-specific evidence, without assuming structural breadth settles retrieval |
| [Evidence-to-witness resolution policy](evidence-to-witness-resolution-policy.md) | Producing explicit candidate-member judgments | Proposed architecture; experimental adapter available | Prose criteria need semantic interpretation; external review-gated direction retained; lexical association separate | 0005 | Explicit resolution kernel; non-production adapter with no resolver; aggregate Cases 0004–0008 | Automatic acceptance, criterion-name rules, universal claims and fifth relation | No automatic policy accepted; current two-track roadmap qualifies timing | Prospective effectiveness after R1/R2 progress by default; concrete exception required |
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
semantic evidence. At that checkpoint, the repository-retrieval landscape
recommended testing retrieval foundations before further evidence-family
escalation; the [roadmap](../roadmap.md) owns the current sequence. The
[breadth production gate](repository-retrieval-breadth-production-gate.md)
now records the completed Increment 25-36 development evidence and current
production, Context, and Evaluation dispositions; the older landscape remains
the prospective research sequence at its original checkpoint.
The [Context Planning and graph-assisted retrieval research](repository-context-planning-and-graph-assisted-retrieval.md)
compares the completed breadth evidence and dogfood with Aider-style repository
maps, query-conditioned graph ranking, and progressive disclosure. ADR-0003 and
ADR-0004 remain the accepted semantic authority; the roadmap owns the next
production and evaluation sequence.

## Research governance

1. Give new research a stable subject-oriented filename.
2. Preserve its substantive body.
3. Add or update its `## Disposition` section.
4. Add it to this README.
5. Link durable accepted decisions to an ADR.
6. Preserve deferred and rejected-for-now findings rather than deleting them.
7. Update the disposition when later ADRs, implementation, experiments, or
   research materially change its status.
