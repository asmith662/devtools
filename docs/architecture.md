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
context/        bounded repository observation and future repository intelligence/Context
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

Current `context` implementation includes bounded recursive discovery of regular
file addresses beneath an explicit resolved root. The operation is correlated
to a logical Repository, requires positive maximum counts for both examined
filesystem entries and discovered regular resources, skips symbolic links and
Windows junctions, and returns canonical repository-relative addresses in
lexical order. It uses filesystem metadata without reading file contents.
Discovery does not create resource occurrences, content identities, or a
RepositorySnapshot, and it assigns no language or relevance semantics.
Successful empty discovery applies only to that root and local mechanism; a
required traversal failure or exceeded bound publishes no partial result. These
recursion, link, and bound choices are local implementation semantics, and the
sequential metadata traversal makes no atomic or race-free filesystem claim.
They are not universal Repository architecture.

For the bounded Python-function path, a separate purpose-sensitive projection
can nominate discovered addresses ending in the exact, case-sensitive `.py`
suffix for source observation. It consumes only the completed discovery value,
preserves discovery order and original address values, and performs no
filesystem or content access. This address convention is evidence of candidacy,
not proof of Python contents, successful UTF-8 observation, task relevance, or
declaration knowledge. Repository discovery itself remains language-neutral.

Current `context` implementation includes bounded observation of a finite,
explicitly addressed collection of UTF-8 text resources. It establishes nominal
Repository identity, repository-relative resource occurrences,
address-independent decoded-text content identities, and deterministic
identified snapshot state under versioned local semantics. Caller order is
canonicalized by repository-relative address, and duplicate addresses are
rejected. Resources are read sequentially; success claims completeness only for
the exact requested collection and makes no repository-wide or atomic-filesystem
claim. Its local digest and representation choices do not select universal
snapshot or ContentIdentity architecture.

For the exact Python function-name purpose, a bounded pre-analysis selector can
filter a caller-ordered, nonempty set of eligible observed resources by exact
stdlib-tokenizer `NAME` equality over their retained decoded text. It preserves
eligible order and all matching-token observations while selecting each
resource once. A positive candidate is only a purpose-relative prediction that
the resource may deserve declaration analysis; calls, references, and methods
are expected false positives relative to the later direct-declaration scope.
Candidate zero is bounded to the explicitly eligible resources, and tokenizer
failure publishes no successful candidate result. The selector performs no
filesystem acquisition or AST analysis and establishes no declaration
knowledge.

The first bounded derivation consumes one caller-selected resource occurrence
from that observed state and uses stdlib `ast` with explicit Python 3.12
grammar-feature semantics to establish source-grounded knowledge for direct
module-body synchronous and asynchronous function declarations. Other snapshot
resources are not direct semantic dependencies of that derivation. Its
identified definition also records the ambient parser
implementation and runtime version. Successful analysis publishes separately
referable declaration knowledge plus exhaustive coverage of exactly that scope;
syntax failure publishes neither successful coverage nor declaration knowledge.
Subjects are snapshot-local and distinct from their AST nodes, declared names,
and UTF-8-byte-column source occurrences. This local representation does not
select universal subject, source, derivation, coverage, or failure architecture.
A bounded aggregate can apply that existing derivation independently to a
caller-ordered, nonempty set of distinct selected resource addresses. It retains
each per-resource analysis and flattens their existing knowledge in selection
and source order for downstream retrieval. It is not a synthetic derivation or
aggregate coverage claim; selection or parse failure returns no aggregate.

The first bounded retrieval operation consumes supplied declaration knowledge
and filters it by exact declared-name equality. Its nonempty name query is the
purpose representation, and each match carries purpose-relative exact-match
RelevanceEvidence referencing the original knowledge. Input order is preserved;
zero matches succeed only over the supplied knowledge. The operation performs no
repository access or parsing and introduces no score, ranking, or Context
selection semantics.

A bounded resource-selection projection can consume that retrieval result and
identify the distinct snapshot-relative resource addresses supporting its
matches. It preserves first-match order and every original declaration-level
match as support when several matches occur in one resource. This projection
performs no retrieval, analysis, or source access and makes no claim that an
unselected resource is irrelevant or that a selected resource is useful beyond
the exact-name purpose.

The first bounded Context operation consumes that successful retrieval result,
selects every exact-name match in retrieval order, and realizes a structured
knowledge projection for each selection. Each item retains its retrieval
evidence and exposes only the established declared name, declaration kind,
proposition, and snapshot-local source occurrence. The retrieval result does not
carry resource content, so the structured disclosure itself does not include
source text or reacquire it. A bounded materializer can separately accept the
identified RepositorySnapshot, validate each occurrence's snapshot identity,
resolve its exact observed resource by repository-relative address, and extract
its exact source segment using the established one-based line and UTF-8-byte-column
coordinates. It preserves observed newline
bytes after UTF-8 decoding and performs no filesystem access or parsing.
A bounded renderer then produces deterministic human-readable Context text from
the materialized values, preserving selection order, duplicates, source
metadata, and each unchanged exact source segment. It retains correlation to
the materialized Context and performs no upstream work or model-specific request
construction. Successful retrieval zero becomes a successful zero-item
disclosure, materialization, and rendering. These local Context artifacts are
not a generic DisclosurePlan/compiler, ranking result, or prompt protocol. A
bounded assembly operation can accept an existing caller-owned `ModelRequest`
whose `Prompt` contains the primary task, preserve its role and all other request
semantics, and construct a new `ModelRequest` whose prompt visibly places the
unchanged rendered Context after the unchanged task. It does not mutate
Conversation, invoke ModelInteraction, or retain Context provenance in the
request. General model-input assembly remains unimplemented.

Filesystem Resources remain access mechanisms, not Repository identity. Python
analysis beyond that declaration scope, capability/execution infrastructure,
broader retrieval, ranking, general Context compilation, progressive disclosure,
storage, and evaluation remain unimplemented future responsibilities; Runtime
remains narrow and model requests remain non-authoritative.

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

## Accepted Evaluation responsibility

Evaluation is a distinct semantic responsibility for assessment and controlled
comparison. It correlates layer-owned artifacts and factual Evidence without
owning RepositorySnapshot, DerivedKnowledge, retrieval observations, Context
artifacts, ModelRequest/ModelResponse, Tool execution, Runtime lifecycle, or
generic Trace. Distributed ownership plus explicit correlation is preferred to
one cross-domain experiment object.

At the granularity required by a particular evaluation, the evaluation meaning
must make referenceable the assessment/comparison basis, intended condition or
intervention and relevant fixed factors, realized execution, applied evaluator/
oracle/criterion, heterogeneous observations or outcomes, and any later
comparison or inference. These are semantic distinctions, not mandatory
classes, globally identified artifacts, persistent lifecycles, or a universal
runtime pipeline. A fixture or scoped configuration can be sufficient for a
bounded evaluation. Repeated realizations remain distinguishable when the
claim depends on them, but an execution Attempt does not automatically become
an evaluation realization.

Evaluation outcomes retain their native meanings: correctness judgments,
coverage, sets, categorical results, durations, token or call counts, costs,
human assessments, and other observations do not collapse into a foundational
scalar score. Policy-specific aggregation, Pareto comparison, or cost-
effectiveness analysis may be layered later. Trace/observability can explain
what occurred and its execution order; it does not establish intended
intervention, controlled factors, oracle meaning, or comparison validity.

Historical evaluation evidence remains truth about an assessment performed
under identified conditions. Whether it predicts or transfers to current
conditions is a later evaluation inference, not ADR-0002 DerivedKnowledge
applicability. An evaluator can judge DerivedKnowledge without that judgment
becoming repository intelligence. Evaluator-private answers, tests, labels,
solutions, or treatment assignments must not become model-visible unless
disclosure is deliberate and authorized; host-side oracle use that changes an
adaptive interaction remains intervention/provenance even when the oracle is
not directly disclosed.

No universal `EvaluationCase`, `Treatment`, `EvaluationRun`,
`EvaluationEpisode`, scalar quality model, causal DAG, trajectory ontology,
oracle abstraction, metric system, trace platform, statistics subsystem, or
evaluation store is accepted. RepositorySnapshot also does not identify the
whole evaluated intelligence condition: knowledge/view availability,
derivation or analyzer semantics, coverage, external semantic state, and reuse
state can differ. Experiments retain the actual relevant basis without creating
a universal `RepositoryIntelligenceSnapshot`, `KnowledgeClosure`, or
`IntelligenceClosure`.

Experimental causation is study-relative and is not either ADR-0002 graph
family. Derivation dependencies explain semantic support/applicability, and
repository graph views express repository relationships; neither makes a claim
such as “graph retrieval improved task outcome” repository graph knowledge.
Such a claim remains an evaluation hypothesis or inference supported by the
particular design, correlations, observations, and analysis.

Counterfactual claims remain bounded. A fixed candidate/evidence set can support
a local ranker comparison, a fixed disclosure can support an assembly
comparison, and an exact request can support repeated model realizations. When
an earlier adaptive decision changes, recorded downstream purposes, retrieval,
or model actions are not automatically a valid counterfactual continuation;
the affected continuation may require a rerun. Progressive evaluation can
retain experiment-local decision correlation without a foundational Episode or
Trajectory model.

## Implementation-start and remaining evidence constraints

The focused external-semantic-state investigation has been reconciled within
ADR-0002. Repository derivations may consume an open set of external semantic
inputs, including configuration, language/toolchain semantics, dependency or
resolution state, generated inputs, platform semantics, environment values, and
external resources. If such state can change derivation meaning or results, it
must not remain an invisible ambient dependency: definition, dependency,
assumption/scope, observation, applicability, and provenance semantics account
for it according to its role. A value, reference, constraint, existing identity,
inline observation, or other adequate representation may suffice; semantic
importance does not automatically require independent identity or persistence.

The semantic thing, its state/value, and its observation are distinct.
Observation must not claim stronger identity, consistency, completeness,
equivalence, or other guarantees than its mechanism establishes. Identity,
value equality, semantic equivalence, compatibility, and applicability likewise
remain distinct, and dependency satisfaction uses the domain- and derivation-
appropriate relation rather than universal identity equality. No foundational
universal `WorkspaceSnapshot`, `EnvironmentSnapshot`, external-state ontology,
observation artifact, equivalence framework, or applicability algorithm is
accepted. One RepositorySnapshot can support multiple configuration/toolchain/
platform interpretations. Committed generated files can be snapshot resources,
while other generated material can be derivation-produced or use a future
analysis-resource model without expanding repository-state identity.

Provenance inspection, semantic replay/reconstruction, and operational replay
have different retention requirements. Semantic identity neither requires a
retained executable artifact nor proves that a historical environment can be
recreated. External dependencies and their observations also bound negative or
exhaustive knowledge; coverage cannot exceed the closure actually established
by dependencies, scope, assumptions, and observation semantics. Concrete
external-state representation, observation, equivalence/compatibility,
generated-resource, enforcement, retention, and replay mechanisms remain
implementation design.

The focused evaluation-architecture and causal-attribution investigation has
completed its substantive analysis, and its accepted findings are reconciled
above. The research dossier's producing process did not complete its final
mechanical artifact-integrity verification; the later architectural review and
this reconciliation therefore treat it as research evidence rather than as a
verified decision artifact.

Existing boundaries require future evaluation to distinguish, where meaningful,
repository observation correctness;
repository-intelligence semantic correctness and derivation-family-specific
soundness, precision, or coverage; incremental-maintenance correctness and
dependency-granularity economics; graph, retrieval, RelevanceEvidence, and
ranking contribution; disclosure selection, representation, coherence,
redundancy, complementarity, synthesis fidelity, and semantic-strength
preservation; model-input presentation effects; resource efficiency; and
end-to-end coding-agent outcomes. Layer-local correctness or quality is not
equivalent to task success, and task success alone does not identify which
layer caused success or failure. Controlled comparison and causal or marginal
contribution assessment should remain possible where practical without
requiring a universal score or a score from every component. Metrics, datasets,
benchmarks, formulas, storage, and APIs remain open. Relevant attribution can
include the marginal or unique contribution of retrievers, graph views, ranking
mechanisms, Context representations, synthesis, and finer incremental-
maintenance precision.

Replay, debugging, and evaluation may therefore need sufficient correlation
among relevant RepositorySnapshot, derivation semantics, semantic dependencies,
DerivedKnowledge, retrieval purpose/planning/applications, candidates and
RelevanceEvidence, ranking, DisclosurePlan, ContextDisclosure, model-input
assembly, ModelInteraction Evidence, and downstream outcome/evaluation identity.
This is a correlation and evidence requirement for the purpose being supported,
not a requirement that every concept have standalone identity, persistence, an
independent lifecycle, or universal storage. It creates no universal
`ReplayRecord`, `Episode`, or Trace and does not collapse repository state,
derivation, retrieval, disclosure, model interaction, and evaluation into one
ownership domain.

The implementation-start assessment is **SAFE WITH PRESERVED SEAMS**. A bounded
repository-intelligence slice can enter concrete design without a generic
Evaluation framework, provided it does not foreclose retention or correlation
of the semantic basis its claims require. Depending on the slice, that includes
deterministic fixture/state reference, RepositorySnapshot identity and
observation semantics, consumed external semantic inputs, DerivationDefinition
meaning and compatibility basis, direct dependencies, produced
DerivedKnowledge and result-specific support, relevant qualification and
semantic-result coverage, distinct success/zero/partial/exhaustive/failure
semantics, analyzer/binding provenance, and correlation among requested work,
realization, dependencies, results, diagnostics, and terminal outcome. This is
neither implementation authorization nor a claim that Evaluation infrastructure
exists.

The external adversarial confirmation remains a confirmation/reopen gate, not
an implementation-start gate. It can reopen architecture if it exposes a
material defect. Initial design remains governed by B-0002 promotion and must
preserve local semantic correctness separately from downstream/task utility,
typed resource observations, and the intended factor/fixed-condition seams
needed to assess marginal contribution or interaction effects later.

Remaining choices such as snapshot digest/Merkle construction, observation
mechanics, parser/analyzer technology, graph storage/indexes/algorithms,
cache/persistence backend, concrete dependency representation and per-family
granularity, capability APIs/scheduling, InformationNeed and RelevanceEvidence
representations, retrieval/ranking implementations, DisclosurePlan/
ContextDisclosure models, materializer and synthesis mechanisms, and exact
evaluation metrics/benchmarks are normally implementation-design and empirical-
evidence questions under the accepted constraints, not reasons to continue
general abstract architecture research.

Settled foundational semantics should be reopened only when concrete research
or implementation evidence contradicts an accepted invariant or shows that
required semantics cannot be represented correctly. Representative triggers
include external state that cannot be represented reproducibly, no viable
dependency granularity preserving correct applicability, required graph
composition needing a missing common semantic abstraction, bounded realization
preventing correct dependency discovery, a knowledge family unable to express
its qualification, Context realization unable to preserve semantic strength,
or accepted layer boundaries preventing meaningful causal evaluation.

See [documentation_map.md](documentation_map.md) for current package
documentation, [taxonomy.md](architecture/taxonomy.md) for definitions, and
[ADR-0001](architecture/decisions/ADR-0001-cohesive-model-interaction-boundary.md)
for the approved future boundary.
