# Architecture Taxonomy

## Authority and scope

This document is the authoritative semantic taxonomy for framework
terminology. It defines what important nouns mean, what they own, what they do
not own, and how currently implemented names relate to the intended
architecture.

Package-local documentation remains authoritative for exact public APIs and
implemented behavior. This taxonomy does not change those APIs.

A concept may be architecturally recognized before its reusable implementation
exists. Taxonomy establishes semantic ownership and vocabulary; it does not
itself authorize new abstractions, packages, type renames, or implementation.
Terms defined here must not be used interchangeably unless this document
explicitly says they are equivalent.

## Status vocabulary

| Status | Meaning |
|---|---|
| **ESTABLISHED** | Existing repository semantics provide strong evidence for the concept. |
| **ESTABLISHED — SPECIALIZED** | An existing stable implementation represents a specialized form of a broader future concept. |
| **EMERGING** | Responsibility is clear enough to name, but reusable implementation is not yet fully established. |
| **PROVISIONAL** | A useful working definition that needs additional evidence before a stronger freeze. |
| **FUTURE** | A known responsibility whose reusable semantics are intentionally unimplemented. |

These labels describe the maturity of a semantic responsibility, not one
implementation lifecycle. A domain can be recognized while sparse, accepted ADR
semantics can precede a production API, and an implemented package mechanism
can remain experimental or unfrozen. Conversely, an accepted ADR is not by
itself implementation completion. Package documentation and source/tests remain
the authority for exact implemented behavior and API maturity.

## Relationship overview

### Conversation and execution

```text
Conversation
└── ConversationTurn
    ├── incoming ConversationMessage
    ├── may trigger Run
    │   └── Step
    │       └── Attempt
    └── outgoing ConversationMessage
```

A ConversationTurn and a Run are not necessarily one-to-one. A Run can exist
without a ConversationTurn, and a Conversation can persist while no Run is
active.

### Model path

```text
Context
  ↓
Prompt
  ↓
ModelInteraction
  ↓
ModelResponse
```

An Agent may interpret a ModelResponse and continue its Run. A ModelResponse
is not automatically user-visible or terminal.

## Conversation domain

### Conversation

**Status: ESTABLISHED.**

A Conversation is durable communicative continuity involving one or more
participants, including Agents, independently of whether execution is active.
It may own an identity, creation time, ordered communicative history, and
current source/provider continuation references.

Conversation does not own Run status, retries, cancellation, Tool state, Step
state, or orchestration. A Conversation can persist while no Agent Run is
active.

The current repository `Conversation` implements this concept. It retains
`History` and source-keyed `ConversationRef` values, and Persistence can
reconstruct that semantic state.

### ConversationMessage

**Status: EMERGING.**

A ConversationMessage is durable semantic communication retained as part of a
Conversation. It records communicative history; it is not necessarily the
same representation sent to a model provider.

The current `ConversationMessage` is the durable communication value. Prompt
and ModelResponse remain distinct model-boundary values rather than durable
conversation records.

### ConversationTurn

**Status: EMERGING.**

A ConversationTurn is one externally meaningful exchange within a
Conversation. It may begin with an incoming ConversationMessage, trigger an
Agent Run, and end with an outgoing ConversationMessage. A Turn is not a Run;
one future Turn may involve substantial internal work.

ConversationTurn is not ModelInteraction or ModelResponse. The repository does
not yet implement a reusable ConversationTurn value.

## Model domain

### Model

**Status: EMERGING.**

A Model is an inference capability that transforms model-facing input into
model output. Depending on its implementation, output may be text, structured
content, model-native action requests, multimodal material, streaming output,
or provider continuation information.

Producing an action request does not itself make a Model an Agent. A Model does
not own goal-directed lifecycle, authorization, Tool execution, completion of
a Run, or orchestration. Model identity is configuration, not a synonym for a
provider implementation. A llama.cpp-served Qwen or DeepSeek deployment is an
illustrative configured model use, not a distinct framework type.

### Prompt

**Status: EMERGING.**

A Prompt is the model-facing input assembled for one ModelInteraction from
information selected as relevant Context. It is not a ConversationMessage, the
Conversation itself, raw repository state, durable Memory, or necessarily one
string.

A future Prompt may use model-oriented messages, structured input,
multimodal components, or provider-specific projections. This taxonomy does
not freeze a representation.

### ModelInteraction

**Status: ESTABLISHED.**

A ModelInteraction is one bounded invocation of a Model using a Prompt and
producing a ModelResponse. It conceptually owns one invocation boundary,
provider/model request and response translation, provider-local invocation
failures, and provider continuation where applicable.

It does not own Agent goals, Runs, Tool execution, authorization, Context
retrieval, orchestration, or ModelServing lifecycle.

The current repository `ModelInteraction` implements this concept for
model-backed adapters. Codex is deliberately separate as an external Agent
integration and is not a ModelInteraction.

### ModelResponse

**Status: EMERGING.**

A ModelResponse is the framework representation of output from one
ModelInteraction. It may eventually contain textual or structured content,
model-native action requests, finish information, usage, or provider metadata.
It must not become a mandatory giant universal result type merely because those
possibilities exist.

ModelResponse is not AgentResult. A ModelResponse can be intermediate material
within a Run.

### ModelServing

**Status: ESTABLISHED.**

ModelServing owns the operational lifecycle needed to make a local or managed
Model endpoint available: artifact acquisition, process/container startup,
hardware/runtime configuration, readiness, shutdown, and endpoint exposure.

This established responsibility does not freeze the current serving-provider
APIs or implementations. The package-local serving slices remain experimental
and unfrozen; their maturity is separate from the recognized lifecycle boundary.

```text
ModelServing       makes an endpoint available
ModelInteraction   communicates with an available endpoint
```

Neither owns the other. `models.serving` implements this distinction;
`LlamaCppServer` and `LlamaCppInteraction` deliberately remain separate.

### ModelBenchmark

**Status: ESTABLISHED.**

A ModelBenchmark measures characteristics of a Model or serving configuration,
such as throughput, latency, context behavior, resource profile, or response
characteristics. It is distinct from future Agent/system evaluation. In
particular, a worker-story or agent-task score is not inherently a
ModelBenchmark.

## Agent and execution domain

### Agent

**Status: EMERGING.**

An Agent is a goal-directed actor that owns the behavioral process for pursuing
a goal through one or more Runs using available Models, Context, capabilities,
and policies. The Agent owns that behavioral process even when lower-level
Runtime/Runner components mechanically execute individual operations.

An Agent need not have Tools, multiple model calls, Memory, a planner, or
unbounded autonomy. A bounded model-backed one-shot actor can be an Agent when
it owns a goal-directed process.

```text
Model   = inference capability
Agent   = goal-directed actor
```

A Model becomes part of an Agent when framework-owned behavior wraps it in a
goal-directed lifecycle; model capability alone is not Agent semantics. This
does not define a `BaseAgent` API.

### AgentResult

**Status: EMERGING.**

An AgentResult is the terminal semantic outcome of one Agent Run. It is not a
ModelResponse: a ModelResponse may request another action or otherwise be an
intermediate result, while AgentResult concerns the completed goal-directed
Run. This taxonomy does not prescribe fields.

### Run

**Status: EMERGING.**

A Run is one bounded effort by an Agent to accomplish a goal. It may include
multiple model interactions, Tools, commands, Context compilation, retrieval,
edits, validation, retries, and multiple Steps.

A Run may eventually be succeeded, failed, cancelled, or suspended, but this
taxonomy intentionally does not freeze lifecycle states. It may be initiated
by a ConversationTurn, orchestration, another Agent, a scheduler, a webhook,
or another future trigger. Run therefore does not belong semantically inside
Conversation.

### Step

**Status: EMERGING.**

A Step is one logical unit of work within a Run. Possible examples are invoking
a model, inspecting a repository resource, executing a command, modifying a
file, retrieving Memory, or validating an outcome. Granularity remains
deliberately unfrozen.

Step represents intended work; Attempt represents a try to perform that work.
This distinction is needed before retries and reconciliation can be described
correctly.

### Attempt

**Status: EMERGING.**

An Attempt is one try to execute one Step. Multiple Attempts may eventually
exist for one Step. Each Attempt has one terminal outcome; a retry, if
introduced, creates another Attempt rather than redefining the original.

Communication failure does not prove an external effect failed, and
cancellation is not rollback. This is the future generic lifecycle concept;
it is not equivalent to the current type named `Attempt`.

### InteractionAttempt

**Status: ESTABLISHED — SPECIALIZED.**

An InteractionAttempt is one Runtime-managed try to process one retained input
ConversationMessage through one selected ModelInteraction source and complete Runtime's
associated validation and Conversation-continuity commit boundaries.

The current implementation is named `InteractionAttempt`. When an observer is
configured, Runtime creates it after input retention and spans:

```text
continuation lookup
→ ModelInteraction invocation
→ result/source validation
→ output retention
→ optional continuation replacement
→ terminalization
```

`InteractionAttempt` is not the future generic Attempt concept.

## Context, resources, and capabilities

### Context

**Status: EMERGING.**

Context is information identified, acquired, selected, transformed, and
assembled as relevant to a specific task, Step, Run, or ModelInteraction. Its
sources may include Conversation, repository resources, filesystem content,
Memory, Tool results, Evidence, documentation, or current Run state.

Context does not own those resources. It means relevance for the current
purpose, not simply all available information.

Repository intelligence is distinct from Context. It establishes deterministic
knowledge about a Repository and its snapshots independently of an LLM;
Context selects, represents, and discloses relevant knowledge or source
material for a purpose. Retrieval provides relevance evidence, ranking is not
repository truth, and final Context selection/compilation remains separate.
Repository-derived material is untrusted data, not policy, instruction, or
execution authority. See [ADR-0002](decisions/ADR-0002-repository-intelligence-identity-and-derivation.md)
for the accepted future repository-intelligence semantics.

### Repository intelligence

**Status: EMERGING.**

Repository intelligence is deterministic knowledge about Repository state,
resources, entities, and typed relationships, useful independently of a Model.
It does not own filesystem access, Context compilation, model prompting,
authorization, Tool execution, Agent loops, or graph storage technology.

`Repository` has nominal identity across changing states. A
`RepositorySnapshot` is an immutable content-derived complete included state
under snapshot semantics; neither a filesystem path nor a Git commit defines
either identity. A resource occurrence is contextual to snapshot plus
repository-relative address and independently refers to content identity.
Entity continuity and move/rename/copy claims across snapshots are derived
knowledge, not foundational identity.

#### RepositorySnapshot, SnapshotDelta, and IncrementalMaintenance

A **RepositorySnapshot** is an immutable, logically complete description of
successfully observed state under explicit snapshot and observation semantics.
Its declared inclusion and consistency contract defines completeness; a valid
snapshot does not imply complete repository intelligence, physical copying, or
full recomputation. Observation cannot claim stronger consistency than its
mechanism establishes, and watcher events are hints rather than repository
truth.

A **SnapshotDelta** is a difference relationship between identified snapshots,
not state, identity, watcher output, or an ordered mutation history. An
**IncrementalMaintenance** process efficiently establishes knowledge applicable
to a state; it does not define that state. Immutable snapshots can share
physical representation and applicable knowledge. The exact snapshot policy,
observation protocol, identity construction, delta model, and maintenance
mechanism remain open.

#### RepositorySubject and SourceOccurrence

A **RepositorySubject** is a snapshot-local identifiable structural or
semantic thing about which repository intelligence can make assertions. It can
be established by analysis; subjecthood and DerivedKnowledge are orthogonal.
For example, a parser can establish a method subject and a later derivation can
produce facts about it. Subject kinds remain open and heterogeneous: code,
documents, configuration, and workflows can establish subjects when independent
referential identity is justified. A **SourceOccurrence** is instead a
snapshot-local source span or anchor within a ResourceOccurrence, such as a
declaration, reference, call, or import. It can support provenance or relate to
a subject without becoming one.

Subject identity is not a source path/range, declared or qualified name, parse
node, or a global entity surviving arbitrary edits. Source addresses locate;
they do not automatically identify the semantic subject. Cross-snapshot
continuity is DerivedKnowledge with evidence, not foundational identity.

Structural analyzer decomposition may establish subjects. Repository-semantic
decomposition is DerivedKnowledge by default, while InformationNeed and
disclosure decomposition are purpose-relative downstream semantics. None of
those latter decompositions automatically creates a RepositorySubject.

#### DerivationDefinition, Derivation, execution, and DerivedKnowledge

A **DerivationDefinition** identifies reusable semantic computation, not
necessarily a callable, plugin, Tool, package, executable, or implementation
binding. A **Derivation** is one semantic application of that definition to
explicit direct semantic dependencies. A future derivation execution is a
particular realization attempt; it is distinct from both Derivation and the
zero-or-more immutable **DerivedKnowledge** artifacts it may establish. Current
`InteractionAttempt` remains a specialized execution lifecycle, not this
unimplemented repository-intelligence concept.

Dependencies are heterogeneous and role-bearing semantic inputs, not a fixed
path/content pair or incidental execution settings. They differ from provenance:
dependencies govern applicability, while shared derivation provenance and
result-specific provenance explain computation and support. Direct dependencies
need not flatten transitive closure. Semantic consumption is not an
instrumentation trace of every operational access. Dependency granularity need
only preserve correct applicability; finer tracking is an optimization whose
reuse benefit must justify bookkeeping, maintenance, and provenance cost.
Definition, derivation, execution, and knowledge identities remain distinct and
their concrete construction is open.

DerivationDefinition compatibility concerns semantic behavior, including
relevant revision and configuration, rather than merely implementation source or
build identity. `DerivedKnowledge` is knowledge with derivation, explicit
dependencies, value, and provenance. Its applicability depends on satisfying
those dependencies under equivalent derivation semantics, not merely on the
snapshot where it was first produced. DerivedKnowledge may depend on other
DerivedKnowledge, enabling targeted invalidation and reuse.

Applicability follows actual semantic dependencies: content, occurrences,
subjects, source occurrences, other knowledge, snapshot facts, and consumed
derivation/language/toolchain semantics are possible inputs. It is not a fixed
path/content dependency convention. One immutable knowledge artifact can apply
to multiple snapshots without rebinding; failure to apply to a later state does
not alter its historical derivation result or provenance. Applicability, invalidation discovery,
rederivation, and cache lookup are separate concerns.

DerivedKnowledge has heterogeneous value shape and may be produced in zero or
more artifacts by one Derivation. Zero artifacts do not prove absence, and
positive artifacts do not prove exhaustive coverage unless derivation semantics
explicitly establish it. Execution failure is Evidence about execution, not
automatically semantic knowledge; partial execution can leave independently
supported knowledge applicable without proving a complete result set. Internal
temporary values, parse nodes, traversal data, and implementation artifacts are
not automatically DerivedKnowledge; result grouping and referential granularity
remain open.

Determinism is distinct from correctness and certainty; confidence is distinct
from completeness and is not a universal knowledge field. Where uncertainty or
alternatives matter, derivation- or knowledge-specific semantics own them.

#### Repository-intelligence capability

A repository-intelligence **capability** is currently available semantic ability
to realize compatible DerivationDefinition semantics. It is distinct from the
definition itself and from a particular implementation binding. Registration or
discovery can expose availability without defining semantics or changing
historical Derivation/DerivedKnowledge meaning. Multiple bindings may realize
compatible semantics; separate production objects are not required solely to
mirror those responsibilities.

Here “repository-intelligence capability” is a qualified conceptual phrase, not
an assertion that it is the generic `Capability` taxonomy concept or a selected
production class. Its availability concerns deterministic derivation
realization, while generic capability availability and authorization retain
their own meanings.

Maintenance/planning determines required semantic work; capabilities realize
admitted bounded work; execution performs selected realization. A capability
does not own global reuse, prerequisites, caller needs, scheduling, retrieval,
Context compilation, Agent behavior, model Tool semantics, or narrow Runtime.
It receives bounded access to repository state and dependencies, may discover
semantic dependencies dynamically, and must expose consumed semantic inputs in
the finalized dependency/provenance record. Foundational capability realization
is deterministic, LLM-independent, and observational with respect to the
analyzed repository. Internal derivation admission differs from model Tool
authorization. Concrete capability, binding, registry, admission, evidence,
scheduler, and package designs remain open.

The derivation dependency graph (applicability/provenance/rederivation) is distinct
from repository semantic relationship views (for example defines, references,
imports, calls, tests, documents, and governs). Typed relationship knowledge is
DerivedKnowledge; composable typed graph views are a first-class
repository-intelligence capability for exposing compatible relational
projections. Shared graph mechanics may support bounded typed traversal or
compatible cross-view composition, but do not determine relationship meaning,
universal node identity, a graph API, or storage. No universal graph, graph
database, or storage model is implied. A graph node is not necessarily a
RepositorySubject: graph views use the node domain their semantics require and
can include local derived nodes. Containment is relationship knowledge rather
than a universal subject-ID tree.
Repository intelligence also has no foundational universal Chunk; downstream
retrieval/disclosure may construct bounded regions, neighborhoods, or subject
sets without defining repository identity. Exact identity representation,
snapshot policy, storage, parser,
retrieval, ranking, and evaluation mechanisms remain unimplemented.

### InformationNeed, retrieval, and ranking

**Status: EMERGING.**

InformationNeed is the conceptual, purpose-relative distinction for information
desired by a consumer to reduce uncertainty. It is not a Task, query, retrieval
operation or strategy, Prompt, Context, token budget, or satisfaction. It does
not by itself require an independently identified, durable, immutable runtime
artifact, standalone lifecycle, persistent need graph, or persistence. A future
implementation may establish that an explicit identified model is useful.
Purpose, typed known anchors, desired characteristics, constraints, and causal
provenance may be carried or referenced by planning/acquisition structures;
constraints describe acceptable information, not retrieval instructions, and
purpose remains distinct from mechanism-specific query material. Changed
uncertainty or acquired information can justify a later purpose. Exact addressed
acquisition remains distinct from relevance discovery.

A ContextCandidate is an addressable repository-intelligence referent that
might help satisfy a need, not its eventual model-visible representation. The
referent can be a RepositorySubject, ResourceOccurrence, SourceOccurrence,
DerivedKnowledge, relationship knowledge, or another future addressable
repository-intelligence referent; this wording does not introduce a universal
referent class or closed candidate taxonomy. Candidate equivalence follows the
underlying addressed identity, enabling independent observations to accumulate;
overlapping file, symbol, and region candidates remain distinct until later
Context selection handles overlap. RelevanceEvidence is typed,
provenance-bearing, purpose-relative retrieval observation for or against
candidate usefulness where its semantics justify that polarity. It is not
universal relevance truth, a normalized score, ranking, or selection utility,
and does not by itself require independent identity, persistence, or
DerivedKnowledge status. Multiple retrievers can contribute native observations
for one candidate; their measurement semantics, confidence/certainty, evidence
strength, and ranking influence remain distinct. Missing support is not negative
evidence merely because a retriever did not discover a candidate.

Retrieval planning selects bounded applications of capabilities using
purpose-derived inputs. It is neither information purpose nor retrieval
execution.
Independent applications may execute concurrently; dependency relationships and
conditional waves can require ordering. Retrieval bounds constrain discovery;
Context budgets constrain disclosure. Multiple exact, lexical, structural,
relationship, semantic, historical, and future mechanisms may contribute
independent evidence; no mechanism or graph owns repository relevance.

Ranking interprets a need, candidate, accumulated evidence, and identified
ranking semantics. It does not overwrite evidence and is distinct from final
Context selection, representation, deduplication, diversity, ordering, and
budgeting. Deterministic and future learned/task-conditioned interpretations
are enabled without selecting formulas, models, or execution technology. See
[ADR-0003](decisions/ADR-0003-information-need-retrieval-evidence-and-ranking.md).

### Context disclosure and assembly

**Status: EMERGING.**

Context compilation conditionally composes information for a consumer; it is
not top-K retrieval or budget filling. Ranking remains an input, while
disclosure planning couples candidate and representation choice and can reason
about coverage, marginal contribution, complementarity, representation-relative
overlap, prior currently available information, applicability, sufficiency,
authority, coherence, and multidimensional cost. A ContextCandidate can support
multiple representations without selecting a fixed `DisclosureOption` type.

A ContextDisclosure is a future identifiable, provenance-bearing account of
purpose-selected represented information. A DisclosurePlan is the distinct
identified decision about what should be made available; a ContextDisclosure is
what was actually realized with reference to that plan. Both are immutable
artifact directions, neither is a ModelRequest, and materialization between
them must not silently make a materially different plan. Repository, disclosure,
and Conversation histories may reference one another but retain separate
identities and lifecycles. Previously disclosed information need not remain
currently available or applicable, and tracking disclosure/availability must
not claim model comprehension or create a ModelKnowledgeState.

Disclosure selects information rather than arbitrary prompt strings. A
DisclosureOption is a conceptual purpose-relative possibility for making
identified information about one or more subjects available through a
representation. Origin, form, fidelity, and cost are separate concerns.
Source-preserving representations select/transform identified source without
new semantic assertions; knowledge projections expose existing DerivedKnowledge;
synthesized representations introduce new semantic assertions and therefore
must remain explicit provenance-bearing derivation work. Determinism does not
by itself establish semantic certainty. Composite representations may preserve
multiple constituent origins.

Disclosure planning determines what information becomes available; model-input
assembly determines how selected information is serialized, ordered, and placed
for a particular model interaction. Presentation effects are empirical
consumer-behavior evidence, not repository relevance or coverage truth. Budget
is a ceiling, not a target, and is distinct from discovery bounds. Optional
Information-purpose decomposition may lead to subordinate purpose/acquisition
work without discarding the broader purpose or requiring persistent child
artifacts; child satisfaction does not prove parent sufficiency. See
[ADR-0004](decisions/ADR-0004-context-disclosure-planning-and-assembly.md).

Coherence is intelligibility of information presented together and the avoided
consumer reconstruction burden, not physical contiguity. Authority is
claim-/purpose-relative evidence, not a universal source ordering, and remains
distinct from relevance, confidence, coverage, and ranking influence. Material
conflicts and absence discipline remain preservable: disclosure planning does
not generally resolve truth, and missing evidence does not prove its opposite.

### Resource

**Status: EMERGING.**

A Resource is a reusable lower-level interface or implementation for accessing
or manipulating an external or local computational resource independently of
Agent semantics. Current filesystem and command infrastructure are examples.

Resource is not Tool. A Tool may adapt a Resource for controlled Agent use;
Context may use a Resource to acquire relevant information; execution may use
a Resource. No one higher-level consumer owns the Resource.

Current filesystem functionality is Resource-family infrastructure: it performs
reusable file I/O and rich file modeling independently of Context or Agent
semantics. Current commands functionality is reusable process infrastructure,
not inherently an Agent execution primitive. Tools may adapt commands; Agents
may use command-backed Tools.

### Tool

**Status: ESTABLISHED.**

A Tool is a typed reusable capability with bounded validation and execution
semantics. Current Tools have local names, descriptions, semantic input
validation, and asynchronous execution through `ToolRunner`.

This established boundary includes implemented narrow Tool behavior, while the
current protocol, runner, and adapters remain experimental and unfrozen
mechanisms. It does not imply a reusable Agent Tool loop, general Tool
authorization, Action framework, or complete Tool ecosystem.

Tool does not itself imply model visibility, permission, authorization,
approval, action parsing, dispatch, or projection of its result into model
Context. Those are separate responsibilities.

### Action

**Status: PROVISIONAL.**

An Action is a model- or Agent-originated request to perform a capability.
Action describes requested work; Tool is one possible implementation mechanism.
Current Qwen experiments provide evidence for proposal/action semantics, but a
shared Action abstraction is not authorized.

### Capability

**Status: PROVISIONAL.**

Capability denotes something a system or Agent could potentially do or access.
Availability does not imply authority to invoke it. No Capability registry is
authorized.

### Authorization

**Status: FUTURE.**

Authorization determines whether a proposed operation is permitted under
current authority and policy. It is distinct from visibility, validation,
permission, and approval. Tool validation is not authorization, and approval
is not automatically authority.

## Evidence and observability

### Evidence

**Status: ESTABLISHED.**

Evidence is immutable factual information supporting what occurred at a
defined system boundary. Current terminal Evidence is specifically evidence
about InteractionAttempt terminal outcomes.

Evidence does not automatically mean trace, telemetry, audit, authorization,
or present authority. Historical Evidence does not create present authority.

### Trace

**Status: FUTURE.**

A Trace is a causal and temporal representation of related activity across
Runs, Steps, Attempts, interactions, or other operations. Trace explains
execution structure; Evidence records factual claims or observations. Trace is
not Evidence.

### Telemetry

**Status: FUTURE.**

Telemetry is operational measurement and signaling about system behavior, such
as metrics, logs, health, performance, or resource observations. Telemetry is
neither Evidence nor Trace.

### Evaluation

**Status: EMERGING.**

Evaluation measures quality, correctness, capability, or behavior of framework
components or complete agentic systems. Future categories may include model
evaluation, Agent task success, trajectory evaluation, Tool selection, workflow
evaluation, and regression acceptance.

Observability explains what happened; Evaluation judges how well or correctly
it happened.

## Memory and persistence

### Persistence

**Status: ESTABLISHED.**

Persistence provides durable storage and restoration of framework state without
redefining that state's semantics. Current implementation primarily persists
Conversation semantic state.

Persistence does not own Conversation, Run, Evidence, or Memory semantics. It
stores representations owned elsewhere.

### Memory

**Status: FUTURE.**

Memory is retained information intended to influence future reasoning or
behavior beyond immediate task Context. Memory is not Conversation history,
Context, or Persistence. Persistence may store Memory; Context may retrieve
from Memory; Conversation may be a Context source.

## Provider and external-agent integration

### Provider

**Status: ESTABLISHED.**

A Provider is an external or local system/protocol implementation through which
a Model or other integration is accessed. Provider is not model identity.
llama.cpp is a current provider/protocol example; future OpenAI, Anthropic, or
other adapters would require their own evidence.

### Codex

**Status: ESTABLISHED.**

Codex is an external agentic system that owns its own goal-directed behavior,
planning, repository interaction, and action loop. It is semantically an
Agent, not a raw Model. The repository reaches it through the bounded
`agents.integrations.codex` integration.

Its placement is not a statement that Codex is a Model provider.

## Orchestration

**Status: FUTURE.**

Orchestration coordinates multiple Runs, Agents, or execution paths into a
larger workflow or control structure. Future concerns may include graphs,
branching, supervisor/worker coordination, scheduling, multi-agent
coordination, retrieval/context flows, and Memory workflows.

Orchestration does not belong inside ModelInteraction or narrow Runtime merely
because those components participate. No orchestration API is authorized.

## Current implementation mapping

| Current repository name | Taxonomy meaning |
|---|---|
| `Conversation` | Durable conversational continuity. |
| `ConversationMessage` | Durable communication retained by Conversation. |
| `Prompt` | Model-facing input for one ModelInteraction. |
| `ModelResponse` | Model-facing output from one ModelInteraction. |
| `ModelInteraction` | Bounded model invocation contract. |
| `InteractionAttempt` | Current specialized execution attempt lifecycle. |
| `AttemptTerminalEvidence` | Evidence about specialized InteractionAttempt terminal outcome. |
| Qwen experiments | Experimental Agent/action-loop evidence, not reusable Agent implementation. |
| Codex adapter | Integration with an external Agent. |

## Semantic invariants

```text
model proposal                 != authority
visibility                     != authorization
Tool validation                != authorization
approval                       != automatically authority
historical Evidence            != current authority
Conversation                   != Run
ConversationTurn               != ModelInteraction
ModelResponse                  != AgentResult
Context                        != Memory
Memory                         != Persistence
Resource                       != Tool
ModelServing                   != ModelInteraction
cancellation                   != rollback
communication failure          != proof an external effect failed
persistence                    != exactly-once external effects
observation                    != permission to disclose payloads
```

## Taxonomy does not authorize implementation

The presence of Agent, Run, Step, Attempt, Action, Capability, Authorization,
Orchestration, Memory, Trace, Telemetry, or Evaluation in this taxonomy does
not authorize generic framework classes, packages, registries, or workflows.
Implementation remains driven by explicit architecture decisions and backlog
promotion based on concrete evidence.
