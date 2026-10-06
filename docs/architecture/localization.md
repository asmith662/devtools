# Localization continuity: current state, evidence and resumption

## Authority and navigation

This is the single current Localization continuity/status owner, including its
status matrix and compact empirical history. [Central architecture](../architecture.md)
owns system boundaries; [taxonomy](taxonomy.md) defines semantics; [ADR-0005](decisions/ADR-0005-obligation-driven-repository-localization.md)
preserves the accepted decision; [roadmap](../roadmap.md#current-sequencing)
owns sequencing. The [package overview](../../src/devtools/context/localization/docs/overview.md)
owns detailed implemented contracts, with source/tests defining behavior.
[Retrieval foundation](retrieval.md) owns lower-level retrieval status and evidence.
This document adds no production semantics or implementation authorization.

| Evidence owner | Authority / how to read it |
| --- | --- |
| Taxonomy, central architecture, this continuity view | Current accepted meaning, boundaries and implementation status |
| Roadmap and [B-0002](../backlog/epics/B-0002-coding-context-substrate.md) | Selected sequencing versus unresolved pressure; backlog remains open |
| ADR-0002/0003/0004/0005 | Accepted rationale and semantic constraints; adoption-time implementation/next-step text is historical |
| Package contracts, source and tests | Implemented API, scope, invariants and integrity checks |
| [Research index](../research/README.md) and dispositions | Historical reasoning, active/parked hypotheses; not automatically accepted policy |
| Case analysis summaries linked below | Frozen development evidence; stage-freeze README language is not today's completion status |
| [External decision adapter](../../experiments/codex_dogfood/semantic_resolution/README.md) | Non-production experimental infrastructure, not an automatic resolver or effectiveness evidence |
| [Implementation ledger](../implementation_ledger.md) | Completed milestone history; its old "next" statements do not override current roadmap |

The earlier [B-0008 investigation](../backlog/items/B-0008-investigate-repository-context-discovery.md)
is superseded historical navigation evidence. Earlier Context question/evidence
lane floors and capacity shares remain unimplemented historical research;
ADR-0005 places obligation resolution in Localization, not Context Planning.

## Current pipeline and semantic gap

The following is caller-directed composition, not one automatic execution loop.
Task interpretation can precede repository observation; grounding and generation
are optional ways of forming associated hypotheses, not mandatory gates on
caller-associated lexical candidates.

```text
[PRODUCTION] RI: observed snapshot, native identities, qualified facts/provenance
                       |
               Retrieval / candidate evidence
                       |
caller task interpretation / obligations / explicit queries and locators
       |                                 |
       v                                 v
separate full-task / obligation      exact anchor grounding
BM25 lanes; optional role routing        |
       |                            bounded structural generation
       +--------------------+------------+
                            v
             caller candidate witness association
             (competitors; complementary members; unresolved)
                            |
                 explicit member resolution recording
                            |
                 complete support + explicit promotion
                            |
              WitnessSet / SupportedWitness values
                            |
        caller accepted alternatives / LocalizationAssessment
                            |
             assess_localization_readiness (supplied frame)

[FUTURE] resolution state -> unresolved obligation/evidence frontier
       -> bounded acquisition request -> authorized orchestration
       -> reacquire -> reassociate / resolve -> iterative sufficiency
       -> Context Planning handoff -> autonomous coding-agent evaluation

[RETRIEVAL ROADMAP] R1 -> mandatory R2 -> justified R3-R6 work
       -> stronger native acquisition evidence for the same Localization boundary
```

Repository fact F does **not** automatically imply task-relative criterion C:
owning declaration D does not establish satisfaction of obligation O, and
importing module M does not establish that M is a sufficient witness for O.
Lexical match, role preference and exact grounding are similarly weaker than
witness sufficiency. This is why evidence-to-witness resolution was introduced.
It is a semantic judgment boundary, not another ranker. Better retrieval changes
which evidence reaches it; it does not remove the need to interpret criteria.

### Task, grounding, association and generation

`LocalizationTaskIdentity`, shared anchor and obligation identities use stable
caller-named task-local keys with `TaskProvenance`. Anchor text remains a
task-relative interpretation, not a repository entity. A
`LocalizationObligation` carries a desired-information predicate, anchors,
mandatory/helpful status, optional applicability condition, named
`SatisfactionCriterion` and accepted alternative `WitnessSet` values. Predicates,
criteria and conditions are caller-authored prose, not executable predicates.
All targets in one witness set are complementary; any fully satisfied accepted
alternative can meet that obligation. Automatic decomposition is not implemented.

[Grounding](../../src/devtools/context/localization/docs/overview.md#exact-task-anchor-grounding)
consumes an explicit locator and native RI frame. Exact resources, explicit-root
modules, direct source declarations and directly contained methods are supported.
`RESOLVED`, `AMBIGUOUS`, `UNRESOLVED` and `UNSUPPORTED` preserve native evidence
and bounds. Decorated source declaration identity is selectable independently of
conservative static binding lookup; it does not identify a runtime/import object
after decorators, rebinding or descriptors. Grounding creates task-relative
links to native truth; it neither derives new truth nor accepts a witness.

[Association](../../src/devtools/context/localization/docs/overview.md#candidate-witness-association)
retains `CandidateWitnessHypothesis` and exact snapshot resource members with
explicit reasons. Members complement within a hypothesis; hypotheses compete
within an obligation and may share resources across obligations. Native lexical,
role, routed, owner, mirror, Reference and Import support retains exact lineage.
Ordering is deterministic inspection, not rank, confidence or satisfaction.
The builder validates caller hypotheses; it does not associate every lexical
match automatically or mutate accepted alternatives.

[Generation](../../src/devtools/context/localization/docs/overview.md#bounded-candidate-witness-generation)
uses caller-authored fixed recipes or families with at most one branching member.
Each in-bound exact target creates one child with its fixed complements. OWNER,
MIRROR, REFERENCE and direct Import dependency consume bounded native facts.
Work and distinct-result limits are independent; incomplete work and whole-set
overflow do not admit an arbitrary prefix. Work units are source analyses, not a
universal CPU/byte budget. There is no ranking, Cartesian-product composition,
recursive graph expansion or automatic witness acceptance.

### Resolution, accepted witnesses, assessment and readiness

The [production resolution-recording kernel](../../src/devtools/context/localization/docs/overview.md#explicit-evidence-to-witness-resolution)
retains exact candidate/member, criterion, claim/reason, caller provenance and
attached native evidence in `CandidateMemberResolution`. Dispositions are
`SUPPORTED`, `UNRESOLVED`, `ABSTAINED`, `CONTRADICTED`; support and contradiction
require explicit evidence. The kernel validates lineage and frame, not the
logical truth of prose. A missing record differs from explicit unresolved or
abstained. Neither rank nor relation count produces a decision.

`WitnessResolutionView` aggregates a hypothesis as contradicted if any member is
contradicted, completely supported only if every complementary member is
explicitly supported, otherwise unresolved. Competitors and generated siblings
remain independent. Contradiction does not eliminate or remove candidates.
`promote_supported_hypothesis` explicitly creates existing `WitnessSet` and
`SupportedWitness` values with evidence references. Promotion does not register
an accepted alternative, mutate `LocalizationAssessment` or change readiness.
The caller supplies accepted alternatives and assessments through the existing
APIs; supported candidate presence alone is not obligation satisfaction.

[Assessment](../../src/devtools/context/localization/assessment.py) records open,
resolved, not-applicable, deferred-discovery or abstained dispositions under an
exact repository/snapshot frame. Applicability is assessed separately.
[Readiness](../../src/devtools/context/localization/readiness.py) checks exact frame
coverage, disposition consistency and supported accepted-witness targets.
`READY` covers every applicable mandatory obligation in the supplied frame;
`CONDITIONAL` requires explicitly accepted named deferred discovery;
`BLOCKED` and `INVALID_FRAME` preserve their diagnostics. Helpful gaps do not
block mandatory readiness. None of these checks inspects criterion prose for
entailment, proves the task frame exhaustive or establishes end-to-end sufficiency.

## Capability status matrix

This is the one Localization continuity matrix. IMPLEMENTED means supported
framework behavior; EXPERIMENTAL means retained non-production code; RESEARCH
ONLY means a proposal without executable policy; PARKED means no immediate
expansion/effectiveness step; FUTURE means not implemented. Combined states
distinguish an available contract from its unproven policy or evaluation.

| Capability | Status | Scope / boundary |
| --- | --- | --- |
| RI identities / derivations | IMPLEMENTED, bounded slices | Native repository/snapshot/content/subject/occurrence provenance; not universal language/runtime knowledge |
| Canonical lexical retrieval | IMPLEMENTED | Whole-resource content + independent filename BM25; not BM25F |
| Task interpretation / obligations | IMPLEMENTED, caller-authored | No automatic decomposition or criterion execution |
| Obligation lexical acquisition | IMPLEMENTED | Separate caller queries and unchanged global safety lane |
| Role evidence | IMPLEMENTED | Soft positive multi-label hints, not negative facts |
| Role routing | IMPLEMENTED; PARKED as primary discriminator | Lossless preference/escape ordering; tested effects mixed |
| Exact grounding | IMPLEMENTED | Source identity separate from runtime/binding identity; ambiguity retained |
| Candidate association | IMPLEMENTED | Caller-associated unresolved competitors/complements |
| Branching generation | IMPLEMENTED | One bounded branching member, exact child lineage, independent work/result bounds |
| OWNER_RESOURCE | IMPLEMENTED; retained | Useful required evidence in recent prospective cases |
| MIRRORED_RESOURCE | IMPLEMENTED; retained | Low recent marginal value; correspondence is not coverage |
| REFERENCING_RESOURCE | IMPLEMENTED; retained | Zero marginal REQUIRED-cell gain in Cases 0007/0008; not a universal failure |
| DIRECT_IMPORT_DEPENDENCY_RESOURCE | IMPLEMENTED; retained | Small real Case 0008 marginal gain; one forward module step |
| Additional structural breadth | PARKED / CLOSED FOR NOW | No fifth relation justified by Case 0008; new evidence required |
| Resolution-recording kernel / explicit promotion | IMPLEMENTED | Caller judgments and integrity, not automatic semantic decisions |
| External semantic-resolution recommendation | RESEARCH ONLY | Interpretation policy not accepted production behavior |
| External semantic decision adapter | EXPERIMENTAL | Explicit proposal, human review and materialization; no resolver invocation |
| Prospective semantic-resolution effectiveness | PARKED | Resume after immediate R1/R2 checkpoints by default |
| Automatic semantic resolver | FUTURE | No policy/model selected or effectiveness established |
| Bounded lexical candidate association policy | FUTURE | Caller association exists; automatic/bounded inclusion policy remains open |
| Automatic contradiction / proof-carrying negative evidence | FUTURE | Explicit contradicted record exists; automatic proof policy absent |
| Candidate elimination | FUTURE | Low rank, absent support or graph disconnection is not elimination proof |
| Unresolved frontier | FUTURE / NOT IMPLEMENTED | Readiness diagnostics and generation-local incomplete enumeration are not a reusable frontier |
| Bounded acquisition requests | FUTURE / NOT IMPLEMENTED | Accepted direction; no current Localization request/controller API |
| Autonomous acquisition execution / iterative reacquisition | FUTURE / NOT IMPLEMENTED | Agent/orchestration owns execution and retries |
| Iterative sufficiency loop | FUTURE, unproven | Frame readiness is implemented; complete acquire/resolve/stop semantics are not |
| Localization-to-Context handoff | FUTURE | Explicit Context plans/materializers exist; automatic obligation provenance transfer does not |
| End-to-end autonomous coding-agent evaluation | FUTURE, unproven | Dogfood acquisition/generation evidence is not agent success/cost evidence |
| R1 code-aware sparse representation | EXPERIMENTAL; prospectively evaluated; retain separate view | [Case 0009 Stage D](../../experiments/codex_dogfood/case_0009/analysis.md); REQUIRED reach unchanged, mixed ranking gains/regressions; canonical BM25 unchanged |
| R2 true BM25F | FUTURE; MANDATORY regardless of R1 | Separate representation/fielding attribution, not production replacement |
| R3-R6 retrieval work | FUTURE, governed hypotheses | Query formulation, verified mismatch, discrimination and complementary fusion |

## Prospective Cases 0004-0008 and structural-breadth closure

These are frozen development tasks/configurations, not universal algorithm
claims. Linked Stage D summaries and JSON own their joins, stage commit lineage,
digests and recovery limitations. Do not alter frozen artifacts or turn a
counterfactual into a rerun. Older stage-freeze README statements such as "not
executed" describe their checkpoints; the completed analyses below own outcomes.

| Case / durable record | Observed conclusion / subsequent disposition |
| --- | --- |
| [0004 analysis](../../experiments/codex_dogfood/case_0004/analysis.md), [JSON](../../experiments/codex_dogfood/case_0004/analysis.json) | Obligation queries improved discrimination: global completion 325, max own completion 193; lexical consideration remained broad. Acquisition completeness is not semantic satisfaction |
| [0005 analysis](../../experiments/codex_dogfood/case_0005/analysis.md), [JSON](../../experiments/codex_dogfood/case_0005/analysis.json) | Minimum sufficient union 22 versus native/routed prefix unions 151/160; own maxima 110/88. Routing helped locally and harmed some obligations; association of competing/complementary candidate witnesses became justified |
| [0006 analysis](../../experiments/codex_dogfood/case_0006/analysis.md), [JSON](../../experiments/codex_dogfood/case_0006/analysis.json) | Decorated declaration grounding prospectively blocked generation: actual zero generated candidates. Counterfactual repaired grounding reached only 12/28 required cells and 2/10 obligations with unchanged OWNER/MIRROR recipes. Exact source selection was later corrected without loosening binding semantics; no replay or improved Case 0006 outcome is claimed |
| [0007 analysis](../../experiments/codex_dogfood/case_0007/analysis.md), [JSON](../../experiments/codex_dogfood/case_0007/analysis.json) | Bounded Reference branching received a prospective test after the grounding correction. Zero marginal REQUIRED cells over OWNER/MIRROR; all three channels covered 10/55 required cells, 1/11 complete obligations. The diagnostic suggested testing direct Import dependency on a fresh case, not admitting overflow prefixes or declaring References universally ineffective |
| [0008 analysis](../../experiments/codex_dogfood/case_0008/analysis.md), [JSON](../../experiments/codex_dogfood/case_0008/analysis.json) | OWNER supplied 14/50 required cells; MIRROR and REFERENCE added zero required cells; Import added +1 marginal required cell. All four covered 15/50 cells and completed 2/13 obligations. The 19-resource union was below the minimum sufficient union of 21. No fifth deterministic relation was justified. Frozen stopping decision: MOVE TO EVIDENCE RESOLUTION |

**Structural breadth is CLOSED FOR NOW.** Retain all four bounded channels:
OWNER has demonstrated useful evidence; MIRROR has low recent marginal value;
REFERENCE has zero marginal REQUIRED-cell gain in these two cases; Import has
small but real marginal gain. Stop expanding deterministic relation breadth
absent new evidence. This is neither operator removal nor a universal family
veto, and does not mean adding graph edges will eventually solve recall.

The Case 0008 workload concerned frontier/acquisition architecture, but running
an experiment about that task did not implement the task. Its generation-only
recovery and digest qualifications remain in the analysis. Its historical
resolution stopping choice is now sequenced after the immediate retrieval
foundation work; neither conclusion establishes lexical adequacy.

## External semantic-resolution boundary and resumption

[Resolution research](../research/evidence-to-witness-resolution-policy.md)
explains why prose criteria require interpretation and recommends an external,
review-gated experimental semantic resolver before a proof DSL. Production owns
the recording kernel; the recommendation remains research; the
[decision adapter](../../experiments/codex_dogfood/semantic_resolution/README.md)
is executable experimental infrastructure. It chooses/invokes no model, builds
no automatic candidate association and has no prospective effectiveness result.

The adapter retains explicit member claim, exact criterion, bounded frozen
content, policy/version identity, proposal, exact citations and native support
handles, then named human ACCEPT/REJECT and explicit materialization into
`CandidateMemberResolution`. V1 content is restricted to the member's exact
resource. Its proposal vocabulary permits SUPPORTED/UNRESOLVED/ABSTAINED and
rejects CONTRADICTED, even from a human producer. Review is not automatic trust;
ACCEPT does not itself materialize, promote, update assessment or change
readiness. It ranks/eliminates nothing and authenticates no human reviewer.

**After immediate retrieval-foundation work, at minimum R1 and mandatory R2
BM25F, resume Localization from the prospective semantic-resolution effectiveness
boundary unless retrieval findings materially alter prerequisites.** The roadmap
allows an earlier parallel experiment only with a concrete recorded reason;
neither mandatory retrieval checkpoint is waived.

The existing intended continuation, not an implementation in this audit, is:

```text
freeze NEW prospective claim-level semantic-resolution case
    -> caller-associated candidate batch + explicit member claims
    -> exact obligation criteria + bounded frozen content disclosure
    -> policy/version/definition identity + human-review protocol
    -> external semantic proposal + citations
    -> human ACCEPT/REJECT
    -> explicit CandidateMemberResolution materialization
    -> evaluate support precision / recall / abstention / inspection cost
```

Freeze the protocol and independent blind claim/witness gold before resolver
execution; measure candidate inclusion separately from conditional resolution.
Report raw proposals, human reviews and materialized records distinctly. No
model is selected. Stronger retrieval may change candidate inclusion, batch
size, content burden and association policy. If bounded lexical association is
a prerequisite, record it explicitly rather than inventing a policy from old
gold. Retrieval cannot establish semantic witness sufficiency by itself;
semantic resolution must not compensate for avoidable retrieval defects.

## Downstream future work and evidence confidence

After that empirical boundary, safe contradiction/negative evidence and
elimination remain future proof-scoped work. A proposed elimination must retain
obligation, exact referent, rule, snapshot/frame, adequate coverage and positive
proof; low rank or absent relation is not proof. Current explicit CONTRADICTED
records neither provide an automatic contradiction policy nor eliminate.

The future chain is resolution state -> unresolved obligation/evidence frontier
-> bounded request for missing observation -> authorized acquisition ->
reassociation/resolution -> sufficiency. Existing generation-local incomplete
enumeration, readiness diagnostics and named deferred discovery do not implement
that frontier or request protocol. Localization may describe missing evidence;
Agent/orchestration decides whether/how/when to execute, retry, escalate or stop.
No autonomous execution ownership moves into Localization or narrow Runtime.

Localization determines obligation-relative evidence/witness state; Context
Planning chooses faithful representations, disclosure ordering, current
availability and capacity. Existing explicit plans, materialization, rendering
and assembly do not implement automatic Localization handoff or minimal
sufficient disclosure. Frame readiness is not a demonstrated iterative
sufficiency loop or proof of coding-agent success. Autonomous coding-agent
evaluation remains a separate future end-to-end outcome.

Within tested cases, obligation decomposition often improves discrimination,
canonical lexical reach is broad, routing is mixed, and structural channels
alone are insufficient. Existing breadth evidence also diagnoses poor blind
graph yield and canonical identifier/subtoken weakness. These bounded findings
are firmer than the open hypotheses that stronger sparse retrieval, semantic
resolution or valid-label reranking will reduce candidate burden. Automatic
resolver effectiveness, iterative frontier/reacquisition, learned candidate
policy and end-to-end agent success/cost are unproven. No result implies
"retrieval solved", "structure failed" or "resolution will solve everything".

Retrieval learned sparse/dense/reranking, external semantic model/agent reasoning
and later learned association/acquisition policy are distinct empirical
possibilities. None selects a model or owns RI truth. **UNJUDGED != NOT_USEFUL**;
unknown labels require a scientifically justified labeling/sampling protocol.
Future protocols must state a primary [failure class](taxonomy.md#retrieval-and-localization-failure-classes):
representation, vocabulary/semantic mismatch, relational relevance,
ranking/discrimination, Context disclosure or information-need/obligation failure.
These surfaces can coexist; the retrieval detour preserves the downstream work.
