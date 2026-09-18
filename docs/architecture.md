# Architecture

`devtools` is organized by responsibility. This document is the canonical
overview of current and accepted system architecture: it records domains,
cross-package ownership, dependency direction, and cross-domain composition.
[The taxonomy](architecture/taxonomy.md) defines semantic terms; package-local
documentation defines exact implemented APIs; and
[architecture decisions](architecture/decisions/) preserve rationale and
historical evolution. Accepted architecture is summarized here as well as in
its ADR, while accepted-but-unimplemented semantics never claim a current API.

A first-class semantic distinction does not by itself require a separately
identified, persistent production artifact. Concrete artifacts remain permitted
when independent lifecycle, replay, persistence, reuse, authority, or other
evidence establishes their value.

## Reading architectural and implementation status

An architectural domain can be recognized while its reusable implementation is
sparse; accepted ADR semantics can exist before a production API. Conversely,
implemented package behavior can remain experimental or unfrozen without making
the domain boundary unsettled. ADR acceptance is not implementation completion.
For exact current APIs and their maturity, follow package documentation and
source/tests; use the taxonomy's status labels for semantic vocabulary rather
than as a single implementation-lifecycle scale.

## Domains

```text
core/           foundational values and transformations
resources/      reusable filesystem and process access
models/         model interaction, serving, and benchmarks
agents/         durable conversation and external agent integrations
context/        future repository intelligence and purpose-relative Context
tools/          typed controlled capability boundaries
execution/      narrow Runtime and specialized InteractionAttempt lifecycle
orchestration/  reserved workflow coordination
governance/     reserved authority and policy responsibility
observability/  Evidence and diagnostic observation
persistence/    durable representation storage and restoration
evaluation/     reserved reusable evaluation responsibility
```

Sparse domains are intentional. Their presence does not authorize speculative
APIs.

## Current boundaries

```text
ConversationMessage
    -> Prompt
        -> ModelInteraction
            -> ModelResponse
                -> materialized ConversationMessage
```

`Runtime` coordinates that one-model exchange for one `Conversation`. It owns
neither agent loops nor orchestration. With an execution observer configured,
it creates and terminalizes a specialized `InteractionAttempt`. Execution does
not depend on observability. `ExecutionInspector` in observability observes
attempt facts, constructs immutable terminal Evidence, and optionally forwards
it to an EvidenceSink.

`CodexAgent` is an external Agent integration under `agents.integrations`; it
does not implement `ModelInteraction`. `LlamaCppInteraction` is a configurable
model provider under `models.interaction.providers`. Model serving makes an
endpoint available; model interaction communicates with it.

Resources are not Tools. Resources provide reusable lower-level access;
Tools adapt bounded typed capabilities for controlled invocation. Tool
validation is not authorization.

Persistence stores and restores Conversation representations. It keeps the
established durable JSON and SQLite wire/schema names where compatibility
requires them; storage does not own conversation semantics.

## Dependency direction

```text
core <- resources <- models
core <- resources <- tools
models, tools, resources <- agents
models, agents <- execution
execution <- observability
agents <- persistence
experiments -> devtools
devtools -/> experiments
```

The diagram permits only dependencies justified by a concrete package API.
Notably, core does not depend upward, model interaction does not depend on
Codex, execution does not depend on observability, and Runtime does not own
orchestration.

## Principles

- Model is not Agent; ModelResponse is not AgentResult.
- Conversation is not Run; generic Run, Step, and Attempt remain future work.
- Context is not Memory or Persistence.
- Evidence is not Trace, Telemetry, or present authority.
- Provenance explains origin/support; it does not itself establish authority,
  certainty, correctness, or truth.
- Model proposal, Tool visibility, and Tool validation are not authorization.
- Cancellation is not rollback, and communication failure does not prove an
  external effect did not occur.

## Accepted ModelInteraction boundary

[ADR-0001](architecture/decisions/ADR-0001-cohesive-model-interaction-boundary.md)
approves a cohesive ModelInteraction boundary: immutable semantic
requests and settings, typed provider-only request extensions, normalized
model-native Tool calls, capture-controlled model interaction Evidence, and
serving-profile provenance. Its phased implementation preserves that models
never execute Tools, Tools do not depend on model providers, Runtime remains
narrow, and raw provider exchange data stays outside `ModelResponse`.

All three ADR-0001 phases are implemented; package documentation and source
remain authoritative for exact current APIs.

## Accepted repository-intelligence semantics

[ADR-0002](architecture/decisions/ADR-0002-repository-intelligence-identity-and-derivation.md)
accepts future semantic architecture for Repository identity, content-derived
RepositorySnapshots, derivation-aware DerivedKnowledge, and distinct derivation
and repository-relationship graph families. RepositorySubject is the
snapshot-local identifiable repository thing about which intelligence may make
assertions; SourceOccurrence is a snapshot-local source anchor within a
ResourceOccurrence and is not automatically a subject. Subjecthood and
DerivedKnowledge are orthogonal: analysis may establish a subject, while
Derivations establish knowledge about subjects, source occurrences, resources,
and other dependencies. Subject identity is not a path/range, name, qualified
name, AST node, or cross-snapshot continuity claim.

Typed containment, declaration, reference, call, import, inheritance, and
other relationships remain DerivedKnowledge. Composable typed graph views are a
first-class repository-intelligence capability for reusable relational
navigation, multi-hop reasoning, retrieval, change impact, and Context
efficiency. Graph views choose suitable node domains: they may reuse subjects
and source occurrences, or use local derived nodes without making every graph
node a RepositorySubject. Shared graph/query mechanics may compose compatible
typed views, but do not define relationship semantics or create universal node
identity. There is no universal repository hierarchy, semantic graph, graph
store, graph database, or foundational Chunk. This also preserves Context as
purpose-relative selection and disclosure rather than repository truth.

Relationship labels are illustrative, not universally unqualified Booleans;
their knowledge-family semantics determine qualification. Repository-relative
conflict/divergence knowledge can itself be DerivedKnowledge when a derivation
defines semantic comparability and incompatibility under compatible
assumptions/scope. Source/resource roles and governance or temporal status can
likewise be derived knowledge useful to downstream authority assessment. No
universal conflict engine, mandatory source-role field/taxonomy, or source
precedence is accepted; purpose-relative trust remains an ADR-0004 concern.

A RepositorySnapshot is an immutable, logically complete successfully observed
state under explicit snapshot/observation semantics. Completeness is relative
to declared inclusion and consistency guarantees, not physical copying, a full
rescan, or repository-intelligence completeness. Observation must not claim a
stronger simultaneous-state guarantee than its mechanism establishes; watcher
events are only future triggers/hints. Snapshot identity is deterministic and
content-derived, but digest construction, policy-to-state-identity treatment,
and observation mechanisms remain open. ContentIdentity is address-independent
and reusable; ResourceOccurrences remain snapshot-local.

SnapshotDelta is a difference relationship between states, and
IncrementalMaintenance is the process of efficiently establishing applicable
knowledge. Neither defines repository state or identity. Immutable logical
snapshots and reuse are complementary: applicable DerivedKnowledge can serve
multiple snapshots without copying or rebinding, while missing/inapplicable
knowledge is rederived as required. Applicability follows actual semantic
dependencies, which may include content, occurrences, subjects, source anchors,
other knowledge, snapshot facts, or derivation semanticsâ€”not a fixed
path/content pair or local-versus-relational category. Applicability,
invalidation discovery, rederivation, and cache lookup remain separate.

Repository intelligence distinguishes an identified **DerivationDefinition**
(reusable semantic computation), a **Derivation** (that definition applied to
explicit direct semantic dependencies), a particular execution/Attempt that may
realize it, and the zero-or-more immutable **DerivedKnowledge** artifacts it
may establish. Definitions are not necessarily executable bindings; executions
and their Evidence are not repository truth. Dependencies are role-bearing
semantic inputs rather than incidental execution settings, and direct
dependencies need not flatten transitive closure. Dependencies differ from
provenance: shared derivation provenance and result-specific support may both
matter.

These are distinct semantic roles, not a requirement for four heavyweight
subsystems or one production class per role. DerivedKnowledge does not include
every temporary/intermediate computation value, and dependency/provenance
records need not capture every implementation access or duplicate shared support
per result. Granularity must preserve correct applicability; finer tracking is
an optimization justified by reuse gained versus bookkeeping, maintenance, and
provenance cost.

DerivedKnowledge is repository-relative semantic intelligence established by an
identified Derivation; it is not a universal container for every semantic
assertion or provenance-bearing item in the system. Its meaning can include
explicit assumptions, approximation, uncertainty, scope, and completeness.
Deterministic computation does not imply semantic certainty. Representational
transformation of already available information is distinct from epistemic
derivation that establishes a materially new assertion, and not every epistemic
derivation belongs to repository intelligence. These are semantic distinctions,
not requirements for new production classes or artifacts.

DerivedKnowledge does not mean hard or infallible fact. The identified
DerivationDefinition/result vocabulary determines whether a result means
definite, possible, necessary, conservative, ambiguous, unresolved, bounded,
exhaustive, partial, or another explicitly qualified relationship,
classification, semantic property, or result.
Conceptual `MAY_CALL`, `MUST_CALL`, and `CANNOT_CALL` results would therefore be
different propositions, not confidence levels on one generic `CALLS` fact; no
universal predicates or qualifier encoding are selected. Nor is there a
foundational Claim/Assertion/Proposition layer spanning repository intelligence,
retrieval evidence, Context synthesis, and authority judgments.

DerivedKnowledge is not snapshot-owned and has heterogeneous value shape.
Applicability is an external assessment, not mutable knowledge state. Zero
results do not prove absence, positive results do not prove exhaustive coverage,
and failed or partial execution does not automatically negate independently
established knowledge. Definition, derivation, execution, and knowledge
identities remain distinct; concrete models, compatibility/versioning,
provenance, execution integration, and coverage mechanisms remain open.

Semantic-result coverage describes which result space a derivation/result set
accounted for under its scope, assumptions, and semantics; it is not ADR-0004
purpose-relative disclosure coverage. Execution success is not completeness,
partial analysis is not failure, unsupported territory is not negative
knowledge, and absent knowledge normally means unknown/not established. Absence
has negative force only when derivation semantics and sufficient coverage
justify it. Assertion/result, dependencies, assumptions/scope, provenance,
coverage, applicability, and execution Evidence remain distinct without
requiring one production object per distinction.

Repository-intelligence capability is semantic-capability-first: it is the
currently available ability to realize compatible DerivationDefinition
semantics, distinct from that definition and from a particular implementation
binding. Registration/discovery exposes available realizations; it does not
create semantic definitions or alter historical knowledge. Maintenance planning
determines required semantic work, capabilities realize admitted bounded work,
and execution performs the chosen realization. This does not assign cache/reuse,
prerequisite planning, global scheduling, or caller information needs to an
individual capability.

Capabilities receive bounded repository-state and dependency access capable of
accounting for semantically consumed inputs. Dynamic discovery is permitted,
but finalized dependencies must make consumed semantic state explicit for replay
and applicability. “Consumed” denotes semantic support rather than an
instrumentation trace of every operational access. Foundational repository
intelligence is deterministic,
LLM-independent, and observational with respect to the analyzed repository;
it is not Tool, Agent, retrieval, Context compiler, or generic Runtime
semantics. Internal admission for bounded deterministic work differs from
ADR-0001 model Tool authorization. Concrete bindings, registries, selection,
admission, evidence, scheduling, and package APIs remain open.

This deterministic foundational preference concerns realization behavior, not
semantic certainty. A future explicitly accepted learned/probabilistic analyzer
could establish only the qualified prediction, classification, heuristic, or
approximation its DerivationDefinition defines; it could not silently strengthen
that output into an unqualified fact. No such analyzer or infrastructure is
selected.

Analyzer-established structural decomposition may establish subjects. Further
repository-semantic decomposition (for example a failure path or responsibility)
is DerivedKnowledge by default. Purpose-relative information-purpose
decomposition and purpose-relative composite disclosure are downstream concerns
under ADR-0003/ADR-0004; neither makes resulting demands or disclosure units
into RepositorySubjects.

This architecture does not imply a current `context` implementation. Filesystem
Resources remain access mechanisms, not Repository identity. Retrieval,
ranking, Context compilation, progressive disclosure, storage, and evaluation
remain unimplemented future responsibilities; Runtime remains narrow and model
requests remain non-authoritative.

These concepts describe reusable semantic relationships, not a mandatory
runtime pipeline. ResourceOccurrence, SourceOccurrence, and RepositorySubject
are distinct referential domains; graph views are first-class reusable typed
projections over relationship knowledge rather than a mandatory stage; and
directly addressed information can be
acquired without relevance discovery. Retrieval strategies may independently
query different intelligence views. Repository-relative derivation can establish
new DerivedKnowledge, while purpose-relative Context synthesis can establish
provenance-bearing information without automatically becoming repository
intelligence. Progressive disclosure can justify another information purpose/
acquisition episode. A request need not traverse every concept or view.

## Accepted retrieval and ranking semantics

[ADR-0003](architecture/decisions/ADR-0003-information-need-retrieval-evidence-and-ranking.md)
accepts InformationNeed as purpose-relative desired-information semantics,
bounded retrieval planning/applications,
ContextCandidate, provenance-bearing RelevanceEvidence, and ranking semantics.
ContextCandidate addresses a repository-intelligence referent—such as a
RepositorySubject, ResourceOccurrence, SourceOccurrence, DerivedKnowledge, or
relationship knowledge—not RepositorySubject alone; representation remains a
later disclosure concern.
RelevanceEvidence preserves typed, provenance-bearing purpose-relative
retrieval observations and retriever-native measurements without requiring a
standalone artifact or repository DerivedKnowledge status. It preserves
retrieval as multi-strategy evidence discovery; ranking as evidence
interpretation; and Context selection/compilation as a later, distinct concern.
It also preserves concurrent dependency-aware retrieval, staged expansion,
progressive disclosure, and future evaluation pressure without assigning them
to Runtime, Tool execution, authorization, or an Agent loop.

## Accepted Context and disclosure semantics

[ADR-0004](architecture/decisions/ADR-0004-context-disclosure-planning-and-assembly.md)
accepts the post-ranking Context layer. Context compilation is conditional
information composition, not top-K retrieval or automatic budget filling.
Disclosure planning couples candidate and representation choice and reasons
about coverage, marginal contribution, complementarity, representation-relative
overlap, prior currently available information, applicability, sufficiency,
authority, and multidimensional cost. It selects information rather than prompt
strings. A DisclosureOption is a future purpose-relative possibility for
exposing information through a selected representation or transformation, with
origin, form, fidelity, cost, and provenance kept semantically distinct.
Source-preserving material, existing knowledge projections, and synthesized
semantic assertions are distinct origins. A new
repository-relative assertion can be ADR-0002 DerivedKnowledge; a purpose-
relative Context synthesis remains explicit and provenance-bearing without
automatic promotion to repository intelligence. Composite provenance-preserving
representations are permitted.

DisclosurePlan, ContextDisclosure, and ModelRequest remain distinct:

```text
InformationNeed -> DisclosurePlan -> materialization -> ContextDisclosure
    -> model-input assembly -> ModelRequest
```

The Plan is an immutable selected-information decision; the Disclosure is an
immutable realized information artifact under/reference to that plan; the
ModelRequest is a consumer-specific presentation. Materialization faithfully
realizes the selected representation and may perform an explicitly planned
semantic transformation or lossy synthesis. It cannot silently re-plan, invent
a materially different synthesis, or present inapplicable information as
current. Assembly arranges already-realized disclosure and must not introduce
new semantic assertions through formatting, placement, or budget handling.
Planning and possession of a disclosure are not disclosure/presentation
authority.

Every disclosure stage preserves semantic strength: representation selection,
projection, synthesis, compression, materialization, disclosure realization,
and assembly must not turn a possible result into a definite one, a partial set
into an exhaustive set, an approximation into an exact assertion, or a
preserved disagreement into one truth unless an identified semantically capable
process establishes the stronger conclusion. Source semantics, support,
assumptions/scope, conflict state, and semantic-result coverage bound what may
be represented.

This architecture distinguishes repository history, disclosure history, and
Conversation history. Current Conversation ownership remains
`agents.conversation`; the sparse `context` namespace does not own a current
compiler or former Session semantics. Model-input assembly is a separate future
concern: it determines how a selected disclosure is realized for a model, while
disclosure planning determines what information should be available. Context
budgets are ceilings rather than targets, and repeated acquisition remains above
deterministic retrieval/compilation rather than inside Runtime.

Coherence concerns intelligible meaningful units and consumer reconstruction
burden, not source contiguity. Authority is claim-/purpose-relative evidence,
not a universal source hierarchy; relevant applicable conflicts remain
preservable rather than being silently arbitrated. Concrete coverage, fidelity,
authority, uncertainty, completeness, conflict, coherence, semantic-
transformation/synthesis validation, materialization, cache, assembly, and
evaluation mechanisms remain unimplemented.

See [documentation_map.md](documentation_map.md) for current package
documentation, [taxonomy.md](architecture/taxonomy.md) for definitions, and
[ADR-0001](architecture/decisions/ADR-0001-cohesive-model-interaction-boundary.md)
for the approved future boundary.
