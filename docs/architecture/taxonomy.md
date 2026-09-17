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

`Derivation` identifies knowledge-producing semantics, including relevant
implementation revision and configuration. `DerivedKnowledge` is knowledge
with derivation, explicit dependencies, value, and provenance. Its validity
depends on satisfying those dependencies under equivalent derivation semantics,
not merely on the snapshot where it was first produced. DerivedKnowledge may
depend on other DerivedKnowledge, enabling targeted invalidation and reuse.

The derivation dependency graph (validity/provenance/recomputation) is distinct
from repository semantic relationship views (for example defines, references,
imports, calls, tests, documents, and governs). Typed relationships are
DerivedKnowledge values; no universal graph, graph database, or storage model
is implied. Exact identity representation, snapshot policy, storage, parser,
retrieval, ranking, and evaluation mechanisms remain unimplemented.

### InformationNeed, retrieval, and ranking

**Status: EMERGING.**

An InformationNeed is immutable, purpose-relative knowledge required by a
consumer to reduce uncertainty. It is not a Task, query, retrieval operation or
strategy, Prompt, Context, token budget, or mutable satisfaction state. It may
retain purpose, description, typed known anchors, desired characteristics,
constraints, and provenance. Constraints describe acceptable information, not
retrieval instructions; origin and prior disclosure are provenance/consumer
facts rather than intrinsic need semantics. Changed uncertainty creates a new
need. Exact addressed acquisition remains distinct from relevance discovery.

A ContextCandidate is an addressable repository subject that might help satisfy
a need, not its eventual model-visible representation. Candidate equivalence
follows the underlying subject, enabling independent observations to accumulate;
overlapping file, symbol, and region candidates remain distinct until later
Context selection handles overlap. RelevanceEvidence is typed,
provenance-bearing, purpose-relative evidence for or against candidate
usefulness. Its native observation semantics, confidence, and ranking influence
are distinct. Missing support is not negative evidence merely because a
retriever did not discover a candidate.

Retrieval planning selects bounded applications of capabilities using
purpose-derived inputs. It is neither InformationNeed nor retrieval execution.
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
purpose-selected represented information. It is distinct from Repository state,
Conversation history, and a model request. Repository, disclosure, and
Conversation histories may reference one another but retain separate identities
and lifecycles. Previously disclosed information need not remain currently
available or applicable, and tracking disclosure/availability must not claim
model comprehension or create a ModelKnowledgeState.

Disclosure planning determines what information becomes available; model-input
assembly determines how selected information is serialized, ordered, and placed
for a particular model interaction. Presentation effects are empirical
consumer-behavior evidence, not repository relevance or coverage truth. Budget
is a ceiling, not a target, and is distinct from discovery bounds. Optional
InformationNeed decomposition may derive child needs without discarding their
parent; child satisfaction does not prove parent satisfaction. See
[ADR-0004](decisions/ADR-0004-context-disclosure-planning-and-assembly.md).

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
