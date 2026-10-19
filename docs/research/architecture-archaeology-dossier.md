# Architecture archaeology dossier

Repository state examined: `main` at `7ff69df7196fe2c3bf67fa894c492b45583e5cfd`.

Evidence labels used below:

- **Direct** — stated by an authoritative repository document or directly implemented.
- **Reconstruction** — a relationship inferred by combining multiple repository sources.
- **Historical** — preserved by the ledger, backlog, experiments, or commit sequence; not current architecture.

## A. Executive reconstruction

The accepted architecture separates five successive semantic problems:

1. Observe and identify repository state without equating identity with a checkout path, Git commit, watcher event, or current contents.
2. Establish deterministic, provenance-bearing repository intelligence through identified semantic derivations and explicit dependencies.
3. Express a consumer’s purpose-relative uncertainty as an `InformationNeed`, retrieve possible supporting referents through bounded independent strategies, and preserve native relevance evidence.
4. Interpret that evidence through ranking, then select both information and representation through disclosure planning under coverage, applicability, authority, coherence, redundancy, sufficiency, and multidimensional cost constraints.
5. Materialize selected information into a `ContextDisclosure`, assemble it for a particular consumer as a `ModelRequest`, and invoke a bounded `ModelInteraction` without collapsing selection, presentation, authorization, Tool execution, Agent behavior, Conversation continuity, or Runtime mechanics.

The corrected conceptual flow is:

```text
Repository
    ↓ observation under explicit policy/consistency semantics
RepositorySnapshot
    ├── ResourceOccurrence ──→ ContentIdentity
    ├── SourceOccurrence
    └── analysis may establish RepositorySubject

DerivationDefinition
    + explicit direct semantic dependencies
    ↓ maintenance/realization planning
available repository-intelligence capability
    ↓ chosen implementation realization
DerivationExecution
    ↓ 0..N
DerivedKnowledge
    ├── structural/local facts
    ├── typed semantic relationships / graph views
    ├── diagnostics and projections
    └── possible knowledge dependencies on other DerivedKnowledge

InformationNeed
    ├── optional direct addressed acquisition
    └── optional provenance-bearing decomposition/refinement
            ↓
retrieval planning
    ↓
bounded RetrievalApplications
    ↓
ContextCandidate + RelevanceEvidence
    ↓
ranking
    ↓
DisclosureOptions
    ↓
DisclosurePlan
    ↓ materialization
ContextDisclosure
    ↓ consumer/model-input assembly
ModelRequest
    ↓
ModelInteraction
```

This is not one containment pipeline:

- Repository subjects and source occurrences are parallel referential domains, not necessarily successive objects.
- Repository graph views are DerivedKnowledge, not a mandatory stage or universal graph.
- Retrieval can address subjects, occurrences, knowledge, relationships, and future referents.
- Direct addressed acquisition can bypass relevance discovery when the target is already known.
- Synthesis that introduces new semantic assertions returns to the derivation layer before disclosure.
- Repeated acquisition and progressive disclosure require orchestration above retrieval and compilation; they are not Runtime behavior.

The architecture’s strongest preservation goals are traceability, reproducibility, honest identity, explicit semantic dependency accounting, immutable historical artifacts, absence discipline, separation of factual evidence from authority, and measurability of failures at the layer that caused them. These are stated across the [canonical architecture](C:/Users/recoveryadmin/Workspace/tools/devtools/docs/architecture.md:103), [taxonomy](C:/Users/recoveryadmin/Workspace/tools/devtools/docs/architecture/taxonomy.md:284), and ADRs.

Implementation reality is much smaller. The repository currently implements:

- paths, bounded filesystem I/O, and commands;
- read/list/command Tools and `ToolRunner`;
- `Conversation`, `ConversationMessage`, and persistence;
- one bounded `ModelRequest -> ModelInteraction -> ModelResponse` contract;
- a llama.cpp provider with normalized model-native Tool definitions/calls;
- narrow `Runtime`;
- specialized `InteractionAttempt` and immutable terminal Evidence;
- capture-controlled model-interaction Evidence;
- an external read-only Codex Agent adapter;
- experimental Qwen controller loops and local-model serving/benchmark support.

No production Repository, snapshot, derivation, intelligence, graph, retrieval, ranking, Context compiler, disclosure, or model-input assembly implementation exists. The `context`, `orchestration`, `governance`, and `evaluation` namespaces are intentionally sparse. This status boundary is explicit in [architecture.md](C:/Users/recoveryadmin/Workspace/tools/devtools/docs/architecture.md:103), [ADR-0002](C:/Users/recoveryadmin/Workspace/tools/devtools/docs/architecture/decisions/ADR-0002-repository-intelligence-identity-and-derivation.md:629), [ADR-0003](C:/Users/recoveryadmin/Workspace/tools/devtools/docs/architecture/decisions/ADR-0003-information-need-retrieval-evidence-and-ranking.md:218), and [ADR-0004](C:/Users/recoveryadmin/Workspace/tools/devtools/docs/architecture/decisions/ADR-0004-context-disclosure-planning-and-assembly.md:315).

## B. Evidence base

### Authoritative architecture inspected in full

- [docs/architecture.md](C:/Users/recoveryadmin/Workspace/tools/devtools/docs/architecture.md:1)
- [docs/architecture/taxonomy.md](C:/Users/recoveryadmin/Workspace/tools/devtools/docs/architecture/taxonomy.md:1)
- [docs/documentation_map.md](C:/Users/recoveryadmin/Workspace/tools/devtools/docs/documentation_map.md:1)
- [ADR-0001](C:/Users/recoveryadmin/Workspace/tools/devtools/docs/architecture/decisions/ADR-0001-cohesive-model-interaction-boundary.md:1)
- [ADR-0002](C:/Users/recoveryadmin/Workspace/tools/devtools/docs/architecture/decisions/ADR-0002-repository-intelligence-identity-and-derivation.md:1)
- [ADR-0003](C:/Users/recoveryadmin/Workspace/tools/devtools/docs/architecture/decisions/ADR-0003-information-need-retrieval-evidence-and-ranking.md:1)
- [ADR-0004](C:/Users/recoveryadmin/Workspace/tools/devtools/docs/architecture/decisions/ADR-0004-context-disclosure-planning-and-assembly.md:1)

### Backlog, sequencing, and history

- [B-0002](C:/Users/recoveryadmin/Workspace/tools/devtools/docs/backlog/epics/B-0002-coding-context-substrate.md:1)
- [B-0008](C:/Users/recoveryadmin/Workspace/tools/devtools/docs/backlog/items/B-0008-investigate-repository-context-discovery.md:1)
- [backlog overview](C:/Users/recoveryadmin/Workspace/tools/devtools/docs/backlog/overview.md:1)
- [backlog metadata](C:/Users/recoveryadmin/Workspace/tools/devtools/docs/backlog/metadata.md:1)
- [roadmap](C:/Users/recoveryadmin/Workspace/tools/devtools/docs/roadmap.md:1)
- [implementation ledger](C:/Users/recoveryadmin/Workspace/tools/devtools/docs/implementation_ledger.md:1)
- Related records for Agent, execution, observability, governance, persistence, Tool exposure, Action semantics, orchestration, and evaluation: B-0010, B-0011, B-0012, B-0013, B-0015, B-0016, B-0017, B-0025, B-0027, B-0028, B-0029, B-0030, B-0031, B-0035, B-0036, B-0041, B-0043, B-0044, B-0045, and B-0046.

### Implemented packages and tests

Inspected current package documentation, production source, and targeted tests for:

- [Conversation](C:/Users/recoveryadmin/Workspace/tools/devtools/src/devtools/agents/conversation/conversation.py:61)
- [CodexAgent](C:/Users/recoveryadmin/Workspace/tools/devtools/src/devtools/agents/integrations/codex/agent.py:32)
- [ModelRequest and interaction values](C:/Users/recoveryadmin/Workspace/tools/devtools/src/devtools/models/interaction/models.py:31)
- [ModelInteraction protocol](C:/Users/recoveryadmin/Workspace/tools/devtools/src/devtools/models/interaction/protocols.py:13)
- [llama.cpp provider](C:/Users/recoveryadmin/Workspace/tools/devtools/src/devtools/models/interaction/providers/llama_cpp.py:49)
- [Tool/ToolRunner](C:/Users/recoveryadmin/Workspace/tools/devtools/src/devtools/tools/execution.py:12)
- [repository filesystem Tools](C:/Users/recoveryadmin/Workspace/tools/devtools/src/devtools/tools/filesystem.py:28)
- [Runtime](C:/Users/recoveryadmin/Workspace/tools/devtools/src/devtools/execution/runtime.py:37)
- [InteractionAttempt](C:/Users/recoveryadmin/Workspace/tools/devtools/src/devtools/execution/interaction_attempt.py:83)
- [terminal Evidence](C:/Users/recoveryadmin/Workspace/tools/devtools/src/devtools/observability/evidence/terminal.py:41)
- [model-interaction Evidence](C:/Users/recoveryadmin/Workspace/tools/devtools/src/devtools/observability/evidence/model_interaction.py:143)
- paths, filesystem, commands, persistence, serving, benchmarks, and their tests.

### Experimental evidence

- [Qwen experiment overview](C:/Users/recoveryadmin/Workspace/tools/devtools/experiments/qwen/docs/overview.md:1)
- [two-action read-only controller](C:/Users/recoveryadmin/Workspace/tools/devtools/experiments/qwen/two_action_read_only_experiment.py:112)
- [patch-proposal worker](C:/Users/recoveryadmin/Workspace/tools/devtools/experiments/qwen/patch_proposal_worker.py:311)
- [Tool descriptor composition seam](C:/Users/recoveryadmin/Workspace/tools/devtools/experiments/qwen/model_tool_composition.py:15)
- [local Qwen serving profile](C:/Users/recoveryadmin/Workspace/tools/devtools/docs/experiments/qwen38_llama_cpp.md:1)
- [experimental worker-story result](C:/Users/recoveryadmin/Workspace/tools/devtools/experiments/worker_story/result.py:15)

No live model or Docker action was performed.

## C. Architectural evolution

### C.1 Former Session/Context ownership

Historical milestones originally placed Message, History, and mutable `Session` in `devtools.context`. That Session held identity, creation time, transcript, provider continuations, and a turn lock. Runtime operated on Session and an older Agent/Interaction boundary.

The twelve-domain correction moved durable communication to `agents.conversation`, renamed Session to `Conversation`, kept schema labels only for persistence compatibility, and made `context` the future purpose-relative information-selection domain. Current documentation explicitly says the sparse namespace does not own former Message/History/Session semantics. See [documentation map](C:/Users/recoveryadmin/Workspace/tools/devtools/docs/documentation_map.md:36), [Conversation docs](C:/Users/recoveryadmin/Workspace/tools/devtools/src/devtools/agents/conversation/docs/conversation.md:1), and the historical ledger’s warning at [Agent integration milestone](C:/Users/recoveryadmin/Workspace/tools/devtools/docs/implementation_ledger.md:45).

### C.2 Model versus Agent correction

An intermediate architecture used a generic `Interaction` package containing both Codex and llama.cpp providers. The current taxonomy split this:

- `ModelInteraction` is one bounded inference invocation.
- Codex owns planning, repository interaction, and its internal action loop, so it is an external Agent integration.
- Qwen controllers are experiment-local evidence, not reusable Agent implementations.
- Model identity is configuration, not a provider class or model-named Agent class.

This correction is reflected in [taxonomy: ModelInteraction](C:/Users/recoveryadmin/Workspace/tools/devtools/docs/architecture/taxonomy.md:135), [taxonomy: Agent](C:/Users/recoveryadmin/Workspace/tools/devtools/docs/architecture/taxonomy.md:192), and [Codex](C:/Users/recoveryadmin/Workspace/tools/devtools/docs/architecture/taxonomy.md:664).

### C.3 B-0008: navigation evidence, not Context architecture

B-0008 originally asked for the smallest repository-information boundary for one coding-worker story. Its experiment showed that a controller could start at repository-relative `.`, perform bounded nonrecursive listings, discover a previously unnamed path, and read text through existing Tools.

The correction was that this proved only:

```text
root-origin fact acquisition
+ controller-directed navigation
```

It did not prove inventory, indexing, repository identity, semantic retrieval, ranking, Context selection, budgeting, or compilation. B-0008 is therefore superseded; B-0002 retains the broader pressure. See [B-0008](C:/Users/recoveryadmin/Workspace/tools/devtools/docs/backlog/items/B-0008-investigate-repository-context-discovery.md:15).

### C.4 Evolution of Repository Intelligence

The commit and ledger sequence is:

1. Initial ADR-0002: Repository versus snapshot/content identity, derivation-aware knowledge, separate graph families, and Context separation.
2. Subject refinement: replaced a loose “repository entity” idea with explicit `RepositorySubject` and `SourceOccurrence`; rejected path/range, AST node, name, graph node, containment tree, and universal Chunk as foundational identity.
3. Snapshot refinement: changed “complete included content state” into “logically complete successfully observed state under explicit inclusion and consistency semantics”; separated snapshot, delta, watcher input, and maintenance.
4. Derivation refinement: split the earlier broad Derivation notion into `DerivationDefinition`, `Derivation`, execution, and `0..N` DerivedKnowledge; added role-bearing direct dependencies, coverage discipline, result-specific provenance, and external applicability.
5. Capability refinement, the current Item 4: distinguished semantic definition, currently available capability, implementation binding, admission, execution, and scheduling; required bounded dependency access and finalized dynamic dependency accounting.

The current checkpoint history is recorded in [implementation ledger: architecture decisions](C:/Users/recoveryadmin/Workspace/tools/devtools/docs/implementation_ledger.md:240).

### C.5 Validity became applicability

Earlier ADR language described knowledge as “valid” or “invalidated.” The accepted refinement uses state-relative applicability:

- knowledge remains immutable historical meaning;
- applicability is assessed externally against semantic dependencies and derivation semantics;
- loss of applicability at S2 does not mutate or invalidate what was established at S1;
- invalidation discovery is merely an efficient maintenance operation.

This avoids using a mutable `currently_valid` field and permits one knowledge artifact to apply to multiple snapshots. See [ADR-0002: applicability](C:/Users/recoveryadmin/Workspace/tools/devtools/docs/architecture/decisions/ADR-0002-repository-intelligence-identity-and-derivation.md:289).

### C.6 Context became disclosure architecture

The accepted evolution was:

```text
repository content/navigation
    → Repository Intelligence
    → InformationNeed and retrieval evidence
    → ranking
    → disclosure composition
    → materialization
    → consumer-specific assembly
```

ADR-0004 was subsequently refined to make `DisclosurePlan` distinct from `ContextDisclosure`, make disclosure about information rather than strings, and classify representation origin. New interpretive assertions were routed back through ADR-0002 derivation semantics rather than permitted as opaque compiler prose. See [ADR-0004: disclosure artifacts](C:/Users/recoveryadmin/Workspace/tools/devtools/docs/architecture/decisions/ADR-0004-context-disclosure-planning-and-assembly.md:109) and [representation refinement](C:/Users/recoveryadmin/Workspace/tools/devtools/docs/architecture/decisions/ADR-0004-context-disclosure-planning-and-assembly.md:217).

### C.7 Capability and execution corrections

The architecture repeatedly corrected capability availability away from authority:

```text
available capability
!= model visibility
!= proposal
!= materialized input
!= validation
!= authorization
!= execution
```

ADR-0001 implemented model-native Tool description/call normalization but deliberately stopped before Action interpretation, authorization, lookup, or execution. ADR-0002 then defined repository-intelligence capability admission as an internal deterministic-work boundary, not model Tool authorization.

## D. End-to-end semantic architecture

| Stage | Responsibility, identity, and mutability | Inputs → outputs and evidence | Non-ownership / status |
|---|---|---|---|
| Repository | Nominal identity across changing states; construction unresolved. | Supported resource arrangement → repository scope. | Not path, checkout, contents, or Git commit. **FUTURE**. |
| RepositorySnapshot | Immutable, content-derived, logically complete observed state under declared inclusion/consistency semantics. | Observation policy/mechanism → snapshot, occurrences, provenance. | Not intelligence completeness, watcher log, physical copy, or Git identity. **FUTURE**. |
| ResourceOccurrence / ContentIdentity | Occurrence is snapshot + repository-relative address; content identity is address-independent and reusable. | Included resource observation → contextual occurrence referencing content identity. | No magical persistent file identity. **FUTURE**. |
| RepositorySubject / SourceOccurrence | Subject is snapshot-local semantic/structural referent; source occurrence is a local anchor/span. Both immutable directions once established. | Analyzer output → subjects and/or source anchors. | Location does not identify subject; not every anchor/AST/graph node is a subject. **FUTURE**. |
| DerivationDefinition | Identified reusable semantic computation. | Semantic specification/configuration → compatibility domain. | Not necessarily callable, plugin, class, Tool, or binding. **FUTURE**. |
| Derivation | Identified application of a definition to explicit role-bearing direct semantic dependencies. | Definition + dependencies → semantic computation instance. | Not its execution or result set. **FUTURE**. |
| Capability realization | Current ability to realize compatible definition semantics. Runtime availability can change. | Required derivation + admitted bounded dependencies → selected binding/execution. | Does not own global planning, cache, scheduling, caller needs, retrieval, or Tools. **FUTURE**. |
| DerivationExecution | One realization attempt; mutable execution state followed by immutable Evidence. | Selected binding + dependency access → zero, partial, or exhaustive results, diagnostics, terminal outcome. | Execution success/failure is not repository truth. **CONCEPTUAL FUTURE**, not a mandated class. |
| DerivedKnowledge | Immutable knowledge with reproducible identity, value, direct dependencies, derivation, and provenance. | Successful semantic establishment → `0..N` artifacts. | Not snapshot-owned; applicability external; zero results do not prove absence. **FUTURE**. |
| Relationship/graph views | Typed relationship facts and task-specific projections over suitable node domains. | DerivedKnowledge → concurrent semantic views. | No universal graph, graph store, or graph-node identity. **FUTURE**. |
| InformationNeed | Immutable purpose-relative desired knowledge. Changed uncertainty creates a new need. | Task/consumer uncertainty/anchors/constraints → need. | Not Task, query, strategy, budget, Context, Prompt, or satisfaction state. **FUTURE**. |
| Decomposition/direct acquisition | Optional need refinement or exact addressed resolution. | Need + known referents → child needs or exact bounded acquisition. | Decomposition is not mandatory; children do not replace parent. **FUTURE**. |
| Retrieval planning | Chooses bounded applications of retrieval capabilities and their purpose-derived inputs. | Need, anchors, available capabilities → application DAG/waves. | Not execution, authority, or InformationNeed. **FUTURE**. |
| Retrieval | Discovers candidates and preserves native observations. | Bounded applications + repository intelligence → candidates/evidence. | Does not own arbitrary derivation, ranking truth, final selection, or budgets. **FUTURE**. |
| ContextCandidate | Addressed referent that might help. Equivalence follows addressed identity. | Retriever discovery → candidate. | Not a rendered representation or arbitrary result UUID. **FUTURE**. |
| RelevanceEvidence | Typed, provenance-bearing, purpose-relative support or opposition. Immutable artifact direction. | Native retrieval observations → evidence set. | Score is not universal relevance truth; no-support is not opposition. **FUTURE**. |
| Ranking | Identified interpretation of need, candidate, and accumulated evidence. | Fixed evidence set → comparative relevance/order. | Does not overwrite evidence or perform selection, representation, deduplication, budgeting, or ordering for presentation. **FUTURE**. |
| DisclosureOption | Conceptual information-plus-representation possibility with origin, form, fidelity, cost, provenance, and expected contribution. | Candidate/knowledge/source + representation possibility → selectable option. | Not prompt text and not necessarily one candidate/file/symbol. **FUTURE**. |
| DisclosurePlan | Immutable identified selection decision under purpose, evidence, constraints, and planning semantics. | Ranked candidates/options, available information, budgets, policy → plan. | Not realized content or presentation authority. **FUTURE**. |
| Materialization | Faithfully realizes the plan; checks applicability, resolution, actual cost, and policy. | Plan + applicable source/knowledge → disclosure or observable discrepancy/failure. | Cannot silently re-plan or create new semantic assertions. **FUTURE**. |
| ContextDisclosure | Immutable identified provenance-bearing realized information artifact referencing its plan. | Materialization → represented information. | Not ModelRequest, model knowledge, universal authorization, or Conversation history. **FUTURE**. |
| Model-input assembly | Serializes, orders, positions, and combines disclosure with instructions, conversation, Tools, and model/provider constraints. | Disclosure + model capabilities/presentation policy → ModelRequest. | Does not determine repository relevance or disclosure selection. **FUTURE**. |
| ModelRequest / ModelInteraction | Immutable request without identity; one interaction occurrence has `ModelInteractionId`. | Prompt/settings/continuation/tool definitions → ModelResponse and optional Evidence. | Does not execute Tools, own Agent goals, retrieval, or serving. **IMPLEMENTED**. |

Primary evidence: [ADR-0002](C:/Users/recoveryadmin/Workspace/tools/devtools/docs/architecture/decisions/ADR-0002-repository-intelligence-identity-and-derivation.md:25), [ADR-0003](C:/Users/recoveryadmin/Workspace/tools/devtools/docs/architecture/decisions/ADR-0003-information-need-retrieval-evidence-and-ranking.md:25), [ADR-0004](C:/Users/recoveryadmin/Workspace/tools/devtools/docs/architecture/decisions/ADR-0004-context-disclosure-planning-and-assembly.md:25), and [ADR-0001](C:/Users/recoveryadmin/Workspace/tools/devtools/docs/architecture/decisions/ADR-0001-cohesive-model-interaction-boundary.md:18).

## E. Repository state and identity

### Repository

A Repository is a logical software repository across change. Its nominal identity can persist while path, checkout, branch, dirty state, and contents change. It may be backed by a Git checkout, fixture, generated workspace, archive, or another resource arrangement.

Known exclusions:

```text
RepositoryId != filesystem path
RepositoryId != checkout identity
RepositoryId != Git commit
RepositoryId != current contents
```

`ResolvedPath` remains a location/access value and explicitly does not imply existence, containment, trust, or authorization. See [path docs](C:/Users/recoveryadmin/Workspace/tools/devtools/src/devtools/core/paths/docs/overview.md:35).

### RepositorySnapshot

A snapshot is:

- immutable;
- content-derived;
- logically complete relative to declared inclusion semantics;
- successfully observed under an explicit consistency guarantee;
- reproducible under equivalent snapshot semantics;
- address-sensitive when address is part of state;
- sensitive to identity-relevant resource attributes;
- insensitive to irrelevant ephemeral metadata;
- traversal-order independent when order lacks meaning.

Logical completeness does not require:

- copying every file;
- including every object below a root;
- a full rescan;
- rebuilding all intelligence;
- analysis success;
- a simultaneously observed state stronger than the mechanism can establish.

An observation that cannot satisfy its declared contract must not masquerade as complete. Sequential reads/stats cannot silently claim atomic simultaneous state.

Open mechanisms include Git-tree observation, filesystem snapshots, validation/retry/quiescence approaches, flat or hierarchical digesting, Merkle-compatible structures, and storage layout. No hashing algorithm or canonical serialization is selected. See [ADR-0002: Repository state](C:/Users/recoveryadmin/Workspace/tools/devtools/docs/architecture/decisions/ADR-0002-repository-intelligence-identity-and-derivation.md:27).

### Inclusion and observation policy

The policy must be able to address root interpretation, ignore/include rules, generated/vendor/binary treatment, symlinks, nested repositories, submodules, multiple roots, identity-relevant metadata, and consistency guarantees.

The relationship between policy identity and state identity is deliberately unresolved:

- different policies might observe equivalent state;
- some policy differences might be identity-relevant.

### ContentIdentity and ResourceOccurrence

`ContentIdentity` is deterministic, address-independent, reusable across snapshots and potentially repositories, and independent of irrelevant occurrence metadata.

A resource occurrence is contextual:

```text
(snapshot identity, repository-relative address) → ContentIdentity
```

Consequences:

- edit: new content identity;
- move: new occurrence/address, possibly same content identity;
- copy: multiple occurrences referencing one content identity;
- delete: occurrence absent from later snapshot;
- delete/recreate identical content: no automatic historical-object continuity.

Raw-versus-normalized content semantics and digest construction are unresolved. Parsed or normalized representation identity is separate from foundational content identity.

### SnapshotDelta

`SnapshotDelta` is a difference relationship between two identified snapshots. It may state address added/removed, same address changed/unchanged, or same content at another address.

It is not:

- repository state;
- snapshot identity;
- an ordered mutation log;
- watcher output;
- proof of rename/copy/entity continuity.

### Watchers and Git

Watcher events are only dirty-set hints or triggers. They are not authoritative state or a delta.

Git may provide:

- committed-tree observation;
- enumeration;
- content acceleration;
- change hints;
- provenance;
- historical access.

Git remains optional and cannot define repository or snapshot identity because working-tree states can differ at the same HEAD.

### Historical/replay implications

Evicting snapshot representation, content, indexes, caches, or DerivedKnowledge does not change the historical meaning of their identities. Retention is separate from semantics. Replay is an intended property but indefinite persistence is not required.

## F. Repository semantic identity

### RepositorySubject

A RepositorySubject is a snapshot-local identifiable structural or semantic thing about which repository intelligence can make assertions.

Possible, non-exhaustive examples include:

- modules, classes, functions, methods, nested functions;
- Markdown documents or sections;
- configuration tables or entries;
- workflows, jobs, and steps.

Statements, parameters, expressions, blocks, and behavioral regions are neither universally included nor excluded. Subjecthood is justified when a domain needs independent referential identity for assertions, relationships, queries, or dependencies.

### SourceOccurrence

A SourceOccurrence is a snapshot-local source span or anchor inside a ResourceOccurrence: declaration, reference, call site, import occurrence, literal, or another addressable source location.

It can:

- support provenance;
- be a relationship endpoint;
- declare, define, or reference a subject;
- be a derivation dependency.

It does not automatically become a subject.

### Identity differences

```text
ResourceOccurrence:
    snapshot-local resource at an address

SourceOccurrence:
    snapshot-local anchor within a resource occurrence

RepositorySubject:
    snapshot-local semantic/structural referent

ContentIdentity:
    address-independent content identity
```

A path/range locates; it does not itself identify a semantic subject. Names, qualified names, containment, resolution, and declarations are knowledge about a subject, not foundational subject identity.

### Structural versus semantic decomposition

Three decompositions are explicitly separate:

1. Analyzer structural decomposition may establish subjects such as a module, class, method, section, or workflow step.
2. Repository-semantic decomposition—failure paths, lifecycles, responsibilities, authorization interactions—is DerivedKnowledge by default.
3. Purpose-relative decomposition produces child InformationNeeds or composite disclosure demands; those do not become subjects.

### Cross-snapshot continuity

There is no foundational global entity that survives arbitrary edits. Rename, move, copy, split, merge, evolution, and “same logical entity” are future DerivedKnowledge claims with evidence and possible ambiguity.

### ASTs, graphs, and chunks

- AST nodes are analyzer artifacts unless a justified subject identity is established.
- A graph node is not necessarily a RepositorySubject.
- Containment is typed relationship knowledge, not subject-ID nesting.
- No universal `Chunk` is foundational. Token windows, line slices, syntax regions, graph neighborhoods, and subject combinations are downstream retrieval/disclosure constructions.

See [ADR-0002: subjects](C:/Users/recoveryadmin/Workspace/tools/devtools/docs/architecture/decisions/ADR-0002-repository-intelligence-identity-and-derivation.md:135) and [distinct decomposition](C:/Users/recoveryadmin/Workspace/tools/devtools/docs/architecture/decisions/ADR-0002-repository-intelligence-identity-and-derivation.md:186).

## G. Derivation and DerivedKnowledge

### DerivationDefinition

Identifies reusable semantic computation, such as Python structural analysis under particular grammar semantics, import resolution, call analysis, or continuity analysis.

It is not necessarily:

- a callable;
- class;
- plugin;
- package;
- executable;
- worker;
- Tool;
- implementation digest.

Compatibility concerns semantic behavior. A compatible refactor need not create new semantic identity; a small behavior-changing edit may. Semantic versioning, compatibility declarations, and implementation digests are unresolved mechanisms.

### Derivation

A Derivation applies one definition to explicit direct semantic dependencies. Equal derivation identities must imply equivalent semantics for identical relevant inputs.

Examples:

```text
PythonParse(definition semantics, ContentIdentity X)
ImportResolution(definition semantics, local knowledge, namespace, config)
```

Concrete identity construction is unresolved.

### Dependencies

Dependencies are:

- explicit;
- heterogeneous;
- semantic rather than incidental;
- role-bearing where role affects computation;
- direct rather than flattened transitive closure.

Potential dependencies include:

- ContentIdentity;
- ResourceOccurrence;
- RepositorySubject;
- SourceOccurrence;
- other DerivedKnowledge;
- snapshot-scoped facts;
- grammar/language/toolchain semantics;
- derivation configuration;
- other explicitly identified semantic inputs.

Incidental inputs such as worker count, trace ID, temporary directory, scheduler choice, logging configuration, wall-clock time, or cache location are not automatically semantic dependencies.

A derivation consuming knowledge K2 need not claim K2’s content dependency as its own direct dependency. Transitive applicability follows the dependency structure.

### Dependency versus provenance

Dependency answers what semantic input affects applicability.

Provenance answers how computation occurred and what supports a result.

Shared derivation provenance may describe the overall computation. Result-specific provenance may point to particular SourceOccurrences or supporting knowledge for one assertion. The schemas remain open.

### DerivationExecution

A DerivationExecution is one realization attempt. It is conceptual terminology, not authorization for a repository-specific production `Attempt` class.

Execution must eventually correlate:

- requested semantic work;
- definition;
- actual consumed dependencies;
- produced knowledge;
- partial/exhaustive status where meaningful;
- diagnostics;
- terminal outcome.

These outcomes must remain distinct:

```text
unknown semantics
known but unsupported semantics
supported but unavailable realization
admission denial
execution failure
successful zero-result
successful partial result
successful exhaustive result
```

### DerivedKnowledge

DerivedKnowledge is immutable knowledge established by an identified derivation, with explicit dependencies, value, provenance, and reproducible identity.

Its value may be a fact, relationship, diagnostic, collection, projection, assertion, syntax structure, or another heterogeneous form. It is a semantic concept, not a mandated Python base class or universal key/value record.

One derivation establishes `0..N` separately referable artifacts. Execution, derivation, grouping, and result granularity are distinct.

### Zero, partial, and exhaustive results

- Zero artifacts do not prove absence unless the derivation explicitly establishes exhaustive coverage.
- Positive artifacts do not prove completeness.
- Partial execution can leave independently supported artifacts applicable.
- A parser crash is execution Evidence, not automatically a syntax-error knowledge fact.
- Exhaustive coverage requires an explicit claim/evidence representation.

### Applicability

The accepted rule is:

> DerivedKnowledge is applicable when its explicit semantic dependencies are satisfied under the same relevant derivation semantics.

Applicability is:

- external to immutable knowledge;
- state- and environment-relative;
- not merely snapshot-ID equality;
- not a mutable validity flag;
- distinct from relevance.

Knowledge established while observing S1 may apply to S2 if its actual dependencies still hold. It is neither copied nor rebound to S2. Failure to apply later does not alter historical meaning.

### Determinism, correctness, and confidence

```text
determinism != correctness
determinism != semantic certainty
confidence != completeness
execution success != semantic authority
```

Confidence, ambiguity, alternatives, and uncertainty belong to definition- or result-specific semantics when meaningful; no universal confidence field is mandated.

Primary evidence: [ADR-0002: derivation](C:/Users/recoveryadmin/Workspace/tools/devtools/docs/architecture/decisions/ADR-0002-repository-intelligence-identity-and-derivation.md:205).

## H. Capability realization

The accepted design is semantic-capability-first:

```text
known DerivationDefinition semantics
    ≠ supported semantics
    ≠ currently available realization
    ≠ implementation binding
    ≠ execution outcome
```

A repository-intelligence capability is the currently available semantic ability to realize compatible definition semantics.

### Capability versus binding

Multiple implementations may realize equivalent semantics. Selection may consider platform, language/toolchain support, performance, cost, availability, or incremental state without changing the requested knowledge.

A concrete implementation may combine capability and binding in one object, but this cannot collapse:

- semantic definition identity;
- implementation identity;
- current availability;
- historical derivation meaning.

Registration/discovery exposes runtime availability. It does not create definitions or alter historical knowledge when an implementation is removed or replaced.

### Planning and realization

```text
required semantic derivation
    → maintenance / realization planning
    → available capability
    → implementation realization
    → execution
    → DerivedKnowledge
```

Planning owns required semantic work, prerequisite ordering, cache/reuse decisions, eager/lazy policy, and global scheduling. A capability owns neither caller needs nor the global maintenance problem.

### Bounded dependency access

Foundational execution receives bounded repository-state and dependency access capable of accounting for consumed inputs. Ambient unrestricted `analyze(repo_root)` access to a changing live tree is explicitly rejected as the foundational model.

Efficient in-process access is still allowed; the architecture does not require RPC or Tool calls for every read.

Dynamic dependency discovery is allowed, but the finalized dependency/provenance record must include every semantically relevant input actually consumed. Expected/static dependencies alone cannot govern replay or applicability.

### Deterministic observational boundary

Foundational repository intelligence is:

- deterministic;
- LLM-independent;
- observational with respect to the analyzed repository state.

A capability must not silently:

- mutate the analyzed repository;
- invoke arbitrary model-visible Tools;
- send model requests;
- gain Agent authority;
- expand its own authority.

Cache/index writes, temporary files, persistence, and Evidence outside the analyzed state may eventually occur, but their mechanics and governance are not selected. LLM-assisted or nondeterministic analysis would require explicitly different semantics.

### Admission versus authorization

Repository-intelligence admission constrains internal deterministic work by repository/snapshot, configured realization, resources, time, and memory.

Model Tool authorization governs an untrusted model-originated request.

Common future governance primitives may be shared, but these responsibilities must not merge.

### Scheduling and failure

Independent derivations may run concurrently. Dependency scheduling belongs to maintenance/planning or a future scheduler, not individual capabilities. Concrete registry, binding, selection, admission, scheduler, process/in-process execution, Evidence, and publication models remain unresolved.

This boundary is conceptual and does not mandate a separate class for every responsibility. See [ADR-0002: capability boundary](C:/Users/recoveryadmin/Workspace/tools/devtools/docs/architecture/decisions/ADR-0002-repository-intelligence-identity-and-derivation.md:354).

## I. Incremental maintenance

The architecture distinguishes:

```text
RepositorySnapshot:
    immutable complete logical state

SnapshotDelta:
    difference between two states

IncrementalMaintenance:
    process for establishing applicable intelligence efficiently

applicability:
    semantic assessment

invalidation discovery:
    efficient detection of lost applicability

cache lookup:
    search for already available applicable knowledge

recomputation/rederivation:
    establishment of missing replacement knowledge
```

Immutable snapshots coexist with efficiency because physical representation and knowledge can be shared. Logical immutability does not require physical duplication.

A changed B resource can make B parse knowledge inapplicable, then affect symbol or cross-resource facts depending on it, while unrelated A knowledge remains applicable. A move can preserve content-local knowledge while invalidating address-sensitive knowledge.

Increasingly selective maintenance can follow finer dependency domains:

```text
resource/content
    → subject
    → source occurrence
    → individual fact
    → graph region
```

This is an enabled refinement path, not an implemented engine design.

Possible mechanisms include reverse dependency indexes, dirty sets, red/green build-style evaluation, watcher hints, Merkle structures, persistent caches, and incremental parser state. None defines applicability.

Graph-derived knowledge complicates maintenance because relationship facts can depend on broad namespace or graph state, and some algorithms may not support trivial edge patching. The architecture promises dependency-governed reuse, not cheap incremental updates for every graph algorithm. See [ADR-0002: SnapshotDelta and maintenance](C:/Users/recoveryadmin/Workspace/tools/devtools/docs/architecture/decisions/ADR-0002-repository-intelligence-identity-and-derivation.md:100).

## J. Repository graph architecture

Two graph families are non-equivalent.

### Derivation dependency graph

Answers:

- what knowledge depends on which direct inputs or prior knowledge;
- how applicability propagates;
- how invalidation may be discovered;
- what must be rederived;
- what can be reused.

Example:

```text
content → parse knowledge → symbol knowledge → resolved-reference knowledge
```

This is not repository topology and does not mandate graph storage.

### Repository semantic/relationship views

Represent typed DerivedKnowledge such as:

- `DEFINES`;
- `REFERENCES`;
- `IMPORTS`;
- `CALLS`;
- `INHERITS`;
- `TESTS` / `EXERCISES`;
- `DOCUMENTS`;
- `GOVERNS`;
- continuity/change relationships.

Future pressure also mentions file dependencies, symbol references, call and inheritance views, test/code, documentation/code, governance, historical co-change, and change-impact views.

### View semantics

There is no universal graph. Multiple concurrent task-specific views may contribute independent retrieval evidence.

Node domains vary:

- containment: subject to subject;
- reference: SourceOccurrence to RepositorySubject;
- call: function/method subject to subject;
- control/data flow: derivation-local basic blocks/statements/instructions, without promoting every node to RepositorySubject.

Relationships are DerivedKnowledge values. A separate foundational `RelationshipId` is not required; derivation and knowledge identity provide lineage.

Storage remains database-neutral. No graph database, globally materialized graph, common graph store, or shared physical representation is selected. See [ADR-0002: graph families](C:/Users/recoveryadmin/Workspace/tools/devtools/docs/architecture/decisions/ADR-0002-repository-intelligence-identity-and-derivation.md:458).

## K. InformationNeed and decomposition

An `InformationNeed` is immutable, purpose-relative knowledge required to reduce a consumer’s uncertainty.

It is not:

```text
Task
query
retrieval strategy
retrieval operation
Prompt
Context
token budget
mutable satisfaction state
```

A Task may create zero, one, or many needs over time. Human, workflow, planner, model, fixture, and future-Agent origin are provenance, not different need types.

A need may conceptually carry:

- semantic question/description;
- purpose;
- typed known anchors;
- desired information characteristics;
- constraints on acceptable information;
- provenance.

Typed anchors may refer to identifiers, resources, paths, subjects/symbols, changes, documents, or existing knowledge. Text is used when nothing stronger is known. An anchor does not prescribe a retriever.

Constraints may require current state, relevant tests, governing architecture, or production rather than generated material. They must not specify mechanisms such as BM25, embeddings, PageRank, or a particular retriever.

Needs do not mutate. Changed uncertainty creates a new need with possible provenance relationships such as decomposition, refinement, or arising from earlier disclosure.

Satisfaction is a separate purpose-/consumer-relative assessment against currently available information. It may later be deterministic, human, workflow, model, or evaluation judged.

### Direct acquisition

When a resource, region, subject, or knowledge artifact is already exactly addressed, future architecture may use a bounded direct resolution path instead of pretending it needs relevance discovery.

### Decomposition

Decomposition is optional. Focused needs can go directly to retrieval.

For a broad need:

- child needs preserve parent provenance;
- parent remains meaningful;
- decomposition can be progressive;
- independent children may be acquired concurrently;
- child satisfaction does not prove parent satisfaction;
- omitted parent dimensions remain possible;
- decomposition itself should be identifiable, replayable derivation work.

No persistent NeedGraph is required. See [ADR-0003: InformationNeed](C:/Users/recoveryadmin/Workspace/tools/devtools/docs/architecture/decisions/ADR-0003-information-need-retrieval-evidence-and-ranking.md:27) and [ADR-0004: decomposition](C:/Users/recoveryadmin/Workspace/tools/devtools/docs/architecture/decisions/ADR-0004-context-disclosure-planning-and-assembly.md:199).

## L. Retrieval

### Planning

Retrieval planning asks which capabilities should investigate a need, with which bounded purpose-derived inputs. A plan selects capability applications, not only retriever names.

Planner-derived terms, anchors, relationship families, scopes, and query forms retain provenance. Proposed query material is a hypothesis, not repository fact.

Planning may eventually be deterministic, learned, model-assisted, or hybrid.

### Bounded applications

Discovery bounds can include:

- candidate count;
- graph depth;
- relationship families;
- repository scope;
- resource kinds;
- time;
- compute.

These bounds are independent of later Context/model token budgets.

Applications can form a dependency DAG:

- independent applications execute concurrently;
- dependent applications are staged;
- cheap or high-confidence waves can precede broader graph, semantic, or historical work;
- later waves are conditional on evidence, coverage, expected information gain, cost, and latency.

No scheduler or DAG representation is selected.

### Candidate identity

A ContextCandidate addresses a RepositorySubject, ResourceOccurrence, SourceOccurrence, DerivedKnowledge, relationship, or other future ADR-0002 referent.

Candidate equivalence follows the addressed identity, so independent discoveries accumulate evidence. File, symbol, and region candidates remain distinct even when physically overlapping.

### RelevanceEvidence

RelevanceEvidence preserves:

- evidence type and native semantics;
- candidate and InformationNeed association;
- provenance/dependencies;
- support or opposition;
- epistemic confidence where meaningful;
- ranking influence as a separate later interpretation.

Native measures are intentionally heterogeneous:

```text
exact-match truth
BM25-like lexical measure
semantic similarity
graph distance
reference count
change/history observation
```

They cannot be treated as directly comparable universal scores.

Negative evidence requires actual opposing semantics. Failure to discover a candidate is not evidence of irrelevance unless the retrieval operation has justified exhaustive semantics.

### Strategy portfolio

Accepted possible strategies include:

- exact/identifier;
- lexical;
- symbol/structural;
- repository relationship/graph;
- optional semantic;
- history/change;
- future mechanisms.

Import, call, reference, test, documentation, governance, co-change, and impact views may contribute independently. No graph or retriever owns relevance.

### Derivation boundary

Retrieval consumes repository intelligence. If required knowledge is absent, retrieval cannot silently become an analyzer. Additional acquisition crosses the explicit maintenance/realization boundary so cost, dependencies, concurrency, Evidence, and replay remain visible.

### Failure and contribution decomposition

Future observability/evaluation should distinguish:

- retrieval failure: useful information never became a candidate;
- ranking failure;
- selection failure;
- representation failure;
- budget/disclosure failure;
- model-utilization failure.

It should permit absolute and marginal retriever contribution: candidates, useful candidates, uniquely contributed value, evidence contribution, latency, and compute cost.

See [ADR-0003: candidates/evidence](C:/Users/recoveryadmin/Workspace/tools/devtools/docs/architecture/decisions/ADR-0003-information-need-retrieval-evidence-and-ranking.md:66) and [planning](C:/Users/recoveryadmin/Workspace/tools/devtools/docs/architecture/decisions/ADR-0003-information-need-retrieval-evidence-and-ranking.md:110).

## M. Ranking

Ranking is an identified interpretation of:

```text
InformationNeed
+ ContextCandidate
+ accumulated RelevanceEvidence
+ ranking semantics/policy
```

It produces comparative relevance or ordering without destroying evidence.

Ranking is purpose-sensitive: exact/symbol evidence may dominate localization, architecture relationships may matter more for design questions, and tests/change/history may matter more for regression work.

Raw measurements cannot simply be averaged because their scales and meanings differ. “Exact match,” graph distance, reference count, semantic similarity, and lexical score do not share a universal probability or relevance scale.

The architecture enables deterministic rankers and future learned/task-conditioned rankers over the same preserved evidence. It selects no formula, normalization, weighting, task classifier, learned model, or ranking API.

Ranking is not:

- retrieval;
- repository truth;
- candidate deduplication;
- diversity;
- representation choice;
- final selection;
- disclosure budgeting;
- model presentation order.

Preserving candidate/evidence inputs and identified ranker semantics is what makes replay, comparison, replacement, and controlled evolution possible. See [ADR-0003: ranking](C:/Users/recoveryadmin/Workspace/tools/devtools/docs/architecture/decisions/ADR-0003-information-need-retrieval-evidence-and-ranking.md:154).

## N. Context disclosure

Context compilation is conditional information composition, not top-K retrieval or automatic context-window filling.

### DisclosureOption

A conceptual option couples identified information with a possible representation. Relevant dimensions are semantically distinct:

- origin;
- form;
- fidelity;
- dependencies and provenance;
- applicability;
- expected information contribution;
- estimated multidimensional cost.

One candidate may support identity/name, signature, documentation, source region, complete definition, relationship view, or other representations. An option can span multiple candidates or subjects.

### Coverage and utility

Coverage asks which aspects of a need are represented. It is distinct from relevance.

Disclosure utility is marginal and non-additive:

- a high-ranked option may add little after similar information is selected;
- a lower-ranked option may add missing coverage;
- implementation and test can be complementary;
- interface and implementation can be complementary;
- source and relationship evidence can be complementary.

Redundancy and overlap are representation- and purpose-relative, not determined merely by shared path, subject, or source range.

### Sufficiency

Coverage describes represented aspects. Sufficiency asks whether the currently available information is adequate for this consumer and purpose, potentially considering fidelity, authority, uncertainty, and consumer requirements.

Sufficiency is not mutable state inside the InformationNeed.

### Coherence and reconstruction burden

Coherence means the presented information forms an intelligible unit with enough relationship/purpose structure to avoid unnecessary consumer reconstruction. It does not mean physical source contiguity.

A compact fragment may be coherent; a large contiguous file may impose greater reconstruction burden. No coherence metric or algorithm is selected.

### Prior information and disclosure history

The architecture distinguishes:

```text
previously disclosed
currently available
currently applicable
understood or used by the model
```

These are not equivalent. Truncation, compaction, provider changes, new interactions, or lifecycle transitions can remove availability. Applicable prior information can be reused across snapshots; stale information cannot be omitted merely because it was once disclosed.

No `ModelKnowledgeState` is accepted. Model understanding/utilization is evaluation evidence.

### Budgets

Budget is a ceiling, not a target. Potential dimensions include:

- input tokens;
- latency;
- retrieval compute;
- representation/compilation compute;
- monetary cost;
- other bounded resources.

The architecture separates:

- hard model/consumer capacity;
- policy budget;
- capacity already used by instructions, Tools, conversation, and other input;
- derived remaining capacity.

Hard constraints can include capacity, policy/authorization, applicability, and mandatory governance requirements. Preferences can include coverage, low redundancy, complementarity, coherence, fidelity, authority, token efficiency, latency, and cost. They are not collapsed into one score.

See [ADR-0004: conditional composition](C:/Users/recoveryadmin/Workspace/tools/devtools/docs/architecture/decisions/ADR-0004-context-disclosure-planning-and-assembly.md:27).

## O. Synthesis, authority, and conflict

### Representation origins

ADR-0004 distinguishes:

1. **Source-preserving representation** — selects or transforms identified source without new semantic assertion: signature, docstring, complete definition, region, test body, architecture section.
2. **Knowledge projection** — exposes existing DerivedKnowledge: symbol facts, relationship lists, dependency neighborhoods, structural views.
3. **Synthesized representation** — introduces new semantic assertions or explanations: implementation summary, lifecycle explanation, behavioral synopsis, change-impact narrative.
4. **Composite representation** — combines multiple origins while preserving constituent provenance.

Formatting, omission, extraction, ordering, or serialization do not alone make content synthesized. Interpretive explanation does.

### Reconnection to derivation

New semantic assertions must follow:

```text
supporting information
    → identified derivation
    → provenance-bearing DerivedKnowledge
    → disclosure option/materialization
```

Materialization may project already-derived synthesis but cannot hide new analysis inside ephemeral compiler prose.

### Determinism and certainty

A deterministic synthesis is reproducible but not necessarily correct or certain. Any confidence, alternatives, or authority implications belong to its derivation/result semantics.

### Authority

Authority is claim- and purpose-relative evidence. There is no universal source ordering among implementation, tests, architecture, ADRs, documentation, comments, history, experiments, and generated artifacts.

Source roles can establish different claims:

- current source: executable behavior;
- tests: expected or verified behavior;
- accepted architecture: architectural constraint;
- ADR: decision rationale and evolution;
- ledger: historical checkpoint.

Authority remains distinct from relevance, confidence, coverage, and ranking influence.

### Conflict and absence discipline

Material conflict among relevant applicable sources is itself preservable information. Disclosure planning is not a general truth arbiter and must not silently collapse disagreement into an unqualified statement without an identified capable derivation.

Similarly:

```text
not found != absent
no supporting evidence != opposing evidence
zero result != proof of absence
```

See [ADR-0004: origin, authority, conflict](C:/Users/recoveryadmin/Workspace/tools/devtools/docs/architecture/decisions/ADR-0004-context-disclosure-planning-and-assembly.md:217).

## P. DisclosurePlan → ContextDisclosure → ModelRequest

The accepted distinctions are:

```text
InformationNeed:
    information desired

DisclosurePlan:
    information and representation selected

ContextDisclosure:
    information actually realized

ModelRequest:
    information presented to one model invocation
```

### DisclosurePlan

An immutable identified decision under a purpose, evidence set, constraints, representation choices, and planning semantics. Revision creates a new plan.

### Materialization

Materialization:

- resolves source;
- checks applicability;
- extracts source-preserving material;
- projects existing knowledge;
- realizes already-derived synthesis;
- formats or structures without adding assertions;
- exposes actual realized cost.

If faithful realization is impossible because of dependency change, unavailable knowledge, derivation failure, cost violation, unresolved source, or policy, materialization must report the discrepancy. It cannot silently substitute materially different information.

Planning-time applicability can race with realization-time state. Handling may later re-plan, rederive, or reacquire; atomicity/race mechanics are open.

### ContextDisclosure

An immutable identified provenance-bearing realized artifact referencing its plan. A plan may fail to realize, and future cardinality may permit multiple disclosures from one plan. The same applicable disclosure may be reusable across ModelRequests or assembly policies, but applicability alone does not establish relevance or authorization.

### Model-input assembly

Assembly determines:

- provider serialization;
- prompt structure;
- separators;
- presentation order;
- placement;
- tokenizer/model constraints;
- coexistence with instructions, Tools, and conversation.

Selection determines what to disclose; assembly determines how to present it.

Position effects are treated as empirical, model-specific behavior evidence. The repository does not currently state a universal beginning/middle/end attention rule. A future assembly policy may use identified model capabilities or behavior profiles, but neither abstraction is selected.

Planning and possession do not authorize disclosure or presentation. Consumer policy, governance, provider restrictions, applicability, and interaction limits remain applicable. See [ADR-0004: planning versus assembly](C:/Users/recoveryadmin/Workspace/tools/devtools/docs/architecture/decisions/ADR-0004-context-disclosure-planning-and-assembly.md:176).

## Q. Progressive disclosure

The accepted progressive-acquisition model is:

1. Begin with a focused need or optionally decompose a broad need.
2. Run bounded high-value retrieval applications.
3. Rank evidence.
4. Select a compact sufficient initial disclosure rather than fill capacity.
5. Preserve disclosure history separately from current availability.
6. Let remaining uncertainty produce a new/refined InformationNeed.
7. Perform targeted additional acquisition.
8. Reassess coverage and sufficiency.

Bounded model-originated requests for more information are permitted conceptually, but remain descriptive proposals. They still cross materialization, validation, authorization, Tool, or repository-intelligence admission boundaries as appropriate.

The architecture does not assume that a model understood previous information merely because it was sent. It tracks disclosure/availability/applicability, not model knowledge.

Repeated acquisition remains orchestration above deterministic retrieval and Context compilation. No loop, stopping policy, scheduler, Agent behavior, or progressive-acquisition protocol is selected.

Efficiency motivation is explicit: reduce repeated expensive model archaeology, unnecessary disclosure, token use, repository operations, and model calls while retaining measurable initial versus eventual acquisition quality. See [ADR-0003: progressive disclosure](C:/Users/recoveryadmin/Workspace/tools/devtools/docs/architecture/decisions/ADR-0003-information-need-retrieval-evidence-and-ranking.md:177).

## R. ModelInteraction and Tool boundary

ADR-0001’s implemented flow is:

```text
ToolDescriptor
    → composition projection
ModelToolDefinition
    → ModelRequest
provider-native Tool schema
    → provider output
ModelToolCall
    → future materialization
future Action/request interpretation
    → authorization
ToolRunner
```

### Proposal and request

`ModelToolCall` is normalized provider output containing callable name, serialized arguments, and optional opaque provider call ID. It is an untrusted proposal, not typed Tool input, Action, authority, approval, or execution.

### Materialization and validation

`ToolInvocation.materialize()` can turn serialized arguments into candidate typed Tool input. It does not validate or execute.

`ToolRunner` calls `Tool.validate()` and then executes once. Validation is semantic admission to that Tool’s contract, not authorization.

### Model visibility

`ToolDescriptor` discloses only an intentionally bounded name, description, and JSON Schema. It should not disclose repository roots, host paths, handles, or execution authority.

The experiment composition seam converts `ToolDescriptor` to `ModelToolDefinition`; neither tools nor models depend on the other package.

### Tool execution

`ModelInteraction` never executes Tools. Current `LlamaCppInteraction` serializes definitions and parses calls only. Current Runtime does not accept Tools or dispatch returned calls.

### Evidence

Interaction Evidence can capture normalized Tool names/descriptions structurally and Tool schemas/call arguments under explicit capture policy. It retains no executable Tool object, authorization, or execution outcome.

### Repository-intelligence capability distinction

Repository-intelligence execution is internally admitted, bounded, deterministic, and observational semantic computation. A model Tool request is untrusted proposed work. The former is not merely exposed as a Tool because doing so would conflate maintenance planning, semantic dependencies, capability availability, model visibility, and authorization.

Evidence: [ADR-0001: model-facing Tools](C:/Users/recoveryadmin/Workspace/tools/devtools/docs/architecture/decisions/ADR-0001-cohesive-model-interaction-boundary.md:112), [Tool code](C:/Users/recoveryadmin/Workspace/tools/devtools/src/devtools/tools/protocols.py:9), and [model Tool values](C:/Users/recoveryadmin/Workspace/tools/devtools/src/devtools/models/interaction/tools.py:24).

## S. Agent / Conversation / Runtime

### Agent

The accepted semantic Agent is a goal-directed actor owning the behavioral process for pursuing a goal through one or more Runs using Models, Context, capabilities, and policy.

There is no generic implemented Agent protocol, `BaseAgent`, Run engine, or reusable Agent loop.

Current concrete evidence:

- `CodexAgent` is an external Agent integration.
- Qwen loops are experimental local compositions.
- A raw llama.cpp-backed model is not an Agent.

### Conversation

Implemented `Conversation` owns:

- UUID-backed `ConversationId`;
- creation timestamp;
- immutable ordered `History`;
- source-keyed opaque `ConversationRef` values;
- per-object asynchronous turn serialization.

It is a mutable entity with object-identity equality and fresh local coordination after persistence reconstruction.

Conversation does not own Run lifecycle, retries, cancellation, Tool state, orchestration, or model configuration.

`ConversationMessage` is immutable durable semantic communication with identity, timestamp, text, role, and source. It is not a Prompt or ModelResponse.

### Runtime

Implemented Runtime coordinates exactly one selected `ModelInteraction` with one `Conversation`:

```text
retain input ConversationMessage
    → continuation lookup
    → project to Prompt
    → invoke ModelInteraction
    → validate response source
    → materialize assistant ConversationMessage
    → retain output
    → optionally replace continuation
```

It optionally creates a specialized `InteractionAttempt` only when an observer is configured. Attempt scope begins after input retention and covers continuation lookup through final commit.

Runtime does not own:

- Agent goals or loops;
- generic Run/Step/Attempt;
- routing;
- retries;
- Tool dispatch;
- repository retrieval;
- Context compilation;
- workflows;
- scheduling;
- orchestration;
- Evidence.

Future retrieval/disclosure may participate before a ModelRequest or inside an Agent/Run workflow, but that does not move orchestration into Runtime.

Evidence: [Runtime docs](C:/Users/recoveryadmin/Workspace/tools/devtools/src/devtools/execution/docs/overview.md:1) and [Runtime implementation](C:/Users/recoveryadmin/Workspace/tools/devtools/src/devtools/execution/runtime.py:51).

## T. Current implementation substrate

| Capability | Status | Current reality |
|---|---|---|
| Generic identity wrappers | **IMPLEMENTED** | Immutable UUID values and domain wrappers for Conversation, Message, attempts, interactions, and Evidence. Not suitable as future content/derivation identity merely by reuse. |
| Path parsing/resolution | **IMPLEMENTED** | `ResolvedPath`, explicit base resolution, normalization. Absolute does not mean contained/trusted/authorized. |
| Filesystem models/read/write | **IMPLEMENTED** | Immutable text/JSON/Markdown/CSV models, 16 MiB default bounded reads, decoding, atomic-replacement writes. No indexing, traversal policy, watchers, or repository identity. |
| Commands | **IMPLEMENTED** | Direct argv subprocesses, bounded output/events, timeout/cancellation of immediate child. No shell, retries, process-tree orchestration, or repository semantics. |
| Tool / ToolRunner | **IMPLEMENTED** | Typed validation followed by one async execution. No authorization, registry, retries, persistence, or generic lifecycle. |
| Repository file read Tool | **IMPLEMENTED** | Normalized root containment; structured format inference or bounded text decoding. |
| Repository directory-list Tool | **IMPLEMENTED** | Sorted, bounded, nonrecursive names/kinds with explicit truncation. |
| Command Tool | **IMPLEMENTED** | Adapts an already constructed Command; admits all valid Commands. Not generically model-disclosed. |
| ToolDescriptor / ToolInvocation | **IMPLEMENTED** | Disclosure and candidate materialization seams; no execution authority. |
| Conversation | **IMPLEMENTED** | Durable communication continuity and provider refs. |
| Generic Agent | **ABSENT / DOCUMENTED FUTURE** | Semantic concept only. |
| Codex external Agent | **IMPLEMENTED** | Read-only CLI adapter using managed commands and provider thread continuation. |
| Prompt / ModelRequest / ModelResponse | **IMPLEMENTED** | One text Prompt; immutable request/settings; usage, termination, reasoning, Tool definitions/calls. |
| ModelInteraction | **IMPLEMENTED** | One bounded invocation protocol. |
| llama.cpp interaction | **IMPLEMENTED** | Non-streaming endpoint adapter, typed settings, native Tool schema/call normalization, optional observation. |
| Runtime | **IMPLEMENTED** | One Conversation/ModelInteraction exchange; no Tool loop or context assembly. |
| InteractionAttempt | **IMPLEMENTED, SPECIALIZED** | Mutable four-state lifecycle for Runtime’s one exchange. |
| Terminal attempt Evidence | **IMPLEMENTED** | Immutable process-local historical facts, optional sink. |
| Model-interaction Evidence | **IMPLEMENTED** | Capture policy/manifest, bounded provider facts, serving-profile provenance. No raw dumps, Trace, Telemetry, or persistence. |
| Conversation persistence | **IMPLEMENTED** | JSON/SQLite restore semantic state; historical Session schema labels retained. |
| Model serving | **PARTIAL / EXPERIMENTAL** | vLLM and llama.cpp lifecycle implementations; serving remains separate from interaction. |
| Model benchmarks | **PARTIAL / EXPERIMENTAL** | One streamed vLLM benchmark and JSON artifacts; no statistical or Agent evaluation suite. |
| Qwen navigation and patch worker | **EXPERIMENTAL** | Bounded explicit controller branches, read-only model capabilities, disposable host-side patch application. |
| Repository identity/snapshot | **DOCUMENTED FUTURE** | Accepted semantics, no production type. |
| RepositorySubject/SourceOccurrence | **DOCUMENTED FUTURE** | Accepted semantics, no analyzer or identity model. |
| Derivation/DerivedKnowledge | **DOCUMENTED FUTURE** | Accepted semantics, no production model or engine. |
| Repository-intelligence capability | **DOCUMENTED FUTURE** | Accepted boundary, no registry, binding, dependency provider, admission, scheduler, or execution API. |
| Indexing/search | **ABSENT** | Generic regex and experiment navigation exist, but no repository index, lexical retrieval system, symbol index, embedding store, or graph retrieval. |
| Repository graph views | **DOCUMENTED FUTURE** | No graph implementation or store. |
| InformationNeed/retrieval/ranking | **DOCUMENTED FUTURE** | No production API or algorithm. |
| Context compiler/disclosure | **ABSENT / DOCUMENTED FUTURE** | `context/__init__.py` contains only the domain marker. |
| Model-input assembly | **DOCUMENTED FUTURE** | Runtime only maps one ConversationMessage to one text Prompt. |
| Orchestration/governance/evaluation | **SPARSE / DOCUMENTED FUTURE** | Namespaces exist; no reusable implementations. |

## U. Trust and governance boundaries

The architecture composes several boundaries:

```text
repository material
    = untrusted data
    ≠ instruction
    ≠ policy
    ≠ authority

model output
    = proposal/data
    ≠ authorization
    ≠ execution

available capability
    ≠ permission to invoke

Tool validation
    ≠ authorization

historical Evidence
    ≠ current authority

DisclosurePlan
    ≠ disclosure authority

ContextDisclosure possession
    ≠ permission to include every item in every ModelRequest
```

Repository intelligence capabilities may read declared snapshot/dependency state under internal admission but must remain observational toward the analyzed repository.

Current repository Tools enforce a bounded root but not general authorization. Generic filesystem/path packages explicitly lack containment and sandbox policy. Tool-level containment is therefore consumer-specific.

Current Codex integration forces a read-only sandbox for fresh and resumed turns. Current Qwen patch experiments expose only list/read actions; host code validates and applies one patch inside a disposable fixture. The model never receives write or command authority.

Mutating governance remains deferred: principals, grants, policy, revocation, approval, delegation, authorization freshness, reconciliation, and uncertain effects are unresolved. Approval is explicitly not authority.

## V. Determinism, provenance, and replay

The intended reproducibility chain is:

```text
Repository nominal identity
+ snapshot/observation semantics
+ deterministic snapshot identity
+ occurrence/content identity
+ DerivationDefinition semantics
+ explicit direct semantic dependencies
+ Derivation identity
+ result-specific and shared provenance
+ immutable DerivedKnowledge
+ external applicability assessment
+ InformationNeed and planning provenance
+ native RelevanceEvidence
+ identified ranking semantics
+ DisclosurePlan provenance
+ materialization facts / ContextDisclosure
+ assembly policy
+ ModelInteraction occurrence Evidence
```

This supports future:

- cache reuse;
- selective recomputation;
- replay;
- historical comparison;
- debugging;
- fixed-evidence ranker experiments;
- fixed-ranked-input compiler experiments;
- presentation experiments over one disclosure;
- attribution of failure to retrieval, ranking, selection, representation, materialization, assembly, or model utilization.

Execution Evidence is intentionally separate from knowledge provenance. A successful execution does not establish authority or correctness; a failed execution does not negate independently established knowledge.

Unresolved exact mechanisms include identity serialization/digests, snapshot observation, definition compatibility, dependency/provenance schemas, applicability algorithms, persistence, cache keys, evidence storage, replay infrastructure, and assembly identity.

## W. Evaluation architecture

No finalized metric suite exists. The architecture preserves the following measurement pressures.

### Repository-intelligence and maintenance

- deterministic replay;
- dependency-accounting correctness;
- applicability correctness;
- exhaustive/partial-result honesty;
- incremental correctness;
- reuse and cache effectiveness;
- recomputation avoided;
- derivation work and latency;
- snapshot observation consistency.

These are reconstruction-level categories enabled by ADR-0002; exact metrics are open.

### Retrieval and ranking

- retrieval/context quality;
- whether useful information became a candidate;
- initial versus eventual acquisition quality;
- relevant-context recall pressure, expressed through retrieval failure and the statement that initial Context need not have perfect recall;
- precision where a fixture has ground truth;
- candidate and useful-candidate contribution;
- unique/marginal retriever contribution;
- evidence contribution;
- graph/relationship contribution as one retriever family;
- retrieval latency and compute cost;
- ranker comparison over fixed evidence;
- ranking failure versus retrieval failure.

### Disclosure

- coverage;
- sufficiency;
- redundancy/overlap;
- complementarity;
- coherence;
- reconstruction burden;
- fidelity;
- authority and conflict preservation;
- estimated versus realized cost;
- applicability failures at realization;
- materialization failure;
- assembly failure;
- disclosure utility;
- model utilization after correct information was presented;
- decomposition quality/failure.

### End-to-end efficiency and outcome

ADR-0002 explicitly lists:

- task success;
- model calls;
- input/output/total tokens;
- repository operations and repeated reads;
- iterations;
- elapsed time;
- cost.

The experiments additionally measure:

- required-read coverage;
- acquisition precision;
- context utilization against the fixed 32K experimental profile;
- per-turn provider usage;
- termination/reasoning diagnostics;
- worker-story duration;
- gate success;
- supervisor review;
- repair attempts and correction turns;
- supervisor tokens;
- escalation;
- architecture violations;
- human intervention.

Those experiment metrics are evidence, not the reusable evaluation architecture. See [ADR-0003: evaluation](C:/Users/recoveryadmin/Workspace/tools/devtools/docs/architecture/decisions/ADR-0003-information-need-retrieval-evidence-and-ranking.md:177), [ADR-0002: Context evaluation pressure](C:/Users/recoveryadmin/Workspace/tools/devtools/docs/architecture/decisions/ADR-0002-repository-intelligence-identity-and-derivation.md:534), and [Qwen overview](C:/Users/recoveryadmin/Workspace/tools/devtools/experiments/qwen/docs/overview.md:54).

## X. Efficiency architecture

Accepted efficiency properties are:

- establish reusable deterministic intelligence outside the LLM;
- avoid repeated repository archaeology;
- reuse knowledge across snapshots according to semantic dependencies;
- represent immutable snapshots with physical sharing;
- separate cache lookup from applicability and recomputation;
- allow increasingly fine dependency granularity;
- run independent derivations and retrieval applications concurrently;
- stage dependent or conditional retrieval waves;
- use direct addressed acquisition when relevance discovery is unnecessary;
- combine multiple retrieval strategies instead of overloading one;
- bound discovery work independently of disclosure capacity;
- use marginal information value rather than filling the context window;
- reuse applicable DerivedKnowledge, materialized representations, or disclosures where appropriate;
- progressively acquire information as uncertainty becomes clearer;
- measure calls, tokens, repository operations, latency, and cost.

The local-model ambition is historical/future motivation, not a Context mechanism: reduce expensive-model dependency and eventually allow Qwen-family models to perform primary or sole coding-worker roles. The current fixed Qwen profile, read controllers, and patch worker are experimental evidence only.

No maintenance engine, scheduler, cache, index, retrieval portfolio policy, stopping policy, learned ranker, token estimator, or compiler optimization is implemented.

## Y. Architectural invariants

1. **Identity must not be confused with location.** Repository is not path; subject is not source range; content identity is address-independent.  
   Evidence: [ADR-0002 state](C:/Users/recoveryadmin/Workspace/tools/devtools/docs/architecture/decisions/ADR-0002-repository-intelligence-identity-and-derivation.md:27), [subjects](C:/Users/recoveryadmin/Workspace/tools/devtools/docs/architecture/decisions/ADR-0002-repository-intelligence-identity-and-derivation.md:135).

2. **Repository, snapshot, occurrence, content, subject, source occurrence, derivation, execution, and knowledge identities are separate domains.**  
   Evidence: [ADR-0002 identity taxonomy](C:/Users/recoveryadmin/Workspace/tools/devtools/docs/architecture/decisions/ADR-0002-repository-intelligence-identity-and-derivation.md:566).

3. **A snapshot must not claim stronger completeness or consistency than observation establishes.**  
   Evidence: [ADR-0002 observation](C:/Users/recoveryadmin/Workspace/tools/devtools/docs/architecture/decisions/ADR-0002-repository-intelligence-identity-and-derivation.md:27).

4. **Watcher events and Git metadata do not define repository truth.**  
   Evidence: [ADR-0002 SnapshotDelta](C:/Users/recoveryadmin/Workspace/tools/devtools/docs/architecture/decisions/ADR-0002-repository-intelligence-identity-and-derivation.md:100).

5. **Historical artifacts remain immutable; applicability is externally state-relative.**  
   Evidence: [ADR-0002 applicability](C:/Users/recoveryadmin/Workspace/tools/devtools/docs/architecture/decisions/ADR-0002-repository-intelligence-identity-and-derivation.md:289).

6. **Semantic dependencies must be explicit, direct, and role-aware where the role matters.**  
   Evidence: [ADR-0002 dependencies](C:/Users/recoveryadmin/Workspace/tools/devtools/docs/architecture/decisions/ADR-0002-repository-intelligence-identity-and-derivation.md:274).

7. **Incidental execution inputs do not automatically become semantic dependencies.**  
   Evidence: same section.

8. **Dependency and provenance are related but non-equivalent.**  
   Evidence: [ADR-0002 provenance](C:/Users/recoveryadmin/Workspace/tools/devtools/docs/architecture/decisions/ADR-0002-repository-intelligence-identity-and-derivation.md:302).

9. **Execution does not create repository truth or semantic authority.**  
   Evidence: [ADR-0002 execution](C:/Users/recoveryadmin/Workspace/tools/devtools/docs/architecture/decisions/ADR-0002-repository-intelligence-identity-and-derivation.md:229).

10. **Zero results do not prove absence, and positive results do not prove exhaustive coverage.**  
    Evidence: [ADR-0002 cardinality](C:/Users/recoveryadmin/Workspace/tools/devtools/docs/architecture/decisions/ADR-0002-repository-intelligence-identity-and-derivation.md:263).

11. **Graph edge shape does not unify derivation-dependency and repository-semantic graphs.**  
    Evidence: [ADR-0002 graph families](C:/Users/recoveryadmin/Workspace/tools/devtools/docs/architecture/decisions/ADR-0002-repository-intelligence-identity-and-derivation.md:458).

12. **Repository material is data, not instruction, policy, or execution authority.**  
    Evidence: [ADR-0002 Context boundary](C:/Users/recoveryadmin/Workspace/tools/devtools/docs/architecture/decisions/ADR-0002-repository-intelligence-identity-and-derivation.md:534).

13. **Retriever-native evidence is not universal relevance truth.**  
    Evidence: [ADR-0003 evidence](C:/Users/recoveryadmin/Workspace/tools/devtools/docs/architecture/decisions/ADR-0003-information-need-retrieval-evidence-and-ranking.md:66).

14. **Absence of support is not opposing evidence without justified exhaustive semantics.**  
    Evidence: same ADR section.

15. **Retrieval is not ranking; ranking is not selection; selection is not representation or presentation.**  
    Evidence: [ADR-0003 ranking](C:/Users/recoveryadmin/Workspace/tools/devtools/docs/architecture/decisions/ADR-0003-information-need-retrieval-evidence-and-ranking.md:154), [ADR-0004 assembly](C:/Users/recoveryadmin/Workspace/tools/devtools/docs/architecture/decisions/ADR-0004-context-disclosure-planning-and-assembly.md:176).

16. **A budget is a ceiling, not a fill target.**  
    Evidence: [ADR-0004 constraints](C:/Users/recoveryadmin/Workspace/tools/devtools/docs/architecture/decisions/ADR-0004-context-disclosure-planning-and-assembly.md:109).

17. **New semantic assertions require explicit provenance-bearing derivation.**  
    Evidence: [ADR-0004 synthesis](C:/Users/recoveryadmin/Workspace/tools/devtools/docs/architecture/decisions/ADR-0004-context-disclosure-planning-and-assembly.md:217).

18. **Planning and possession do not confer disclosure authority.**  
    Evidence: same ADR section.

19. **Model proposal, visibility, materialization, Tool validation, approval, and authorization are different boundaries.**  
    Evidence: [ADR-0001 Tools](C:/Users/recoveryadmin/Workspace/tools/devtools/docs/architecture/decisions/ADR-0001-cohesive-model-interaction-boundary.md:112), [taxonomy invariants](C:/Users/recoveryadmin/Workspace/tools/devtools/docs/architecture/taxonomy.md:701).

20. **Model is not Agent; Conversation is not Run; ModelResponse is not AgentResult.**  
    Evidence: [taxonomy](C:/Users/recoveryadmin/Workspace/tools/devtools/docs/architecture/taxonomy.md:105).

21. **Resource is not Tool; Tool is not Action; capability availability is not authority.**  
    Evidence: [taxonomy resources/capabilities](C:/Users/recoveryadmin/Workspace/tools/devtools/docs/architecture/taxonomy.md:533).

22. **Evidence is historical fact, not Trace, Telemetry, audit, or current authority.**  
    Evidence: [taxonomy Evidence](C:/Users/recoveryadmin/Workspace/tools/devtools/docs/architecture/taxonomy.md:589).

23. **Cancellation is not rollback; communication failure does not prove an external effect failed.**  
    Evidence: [taxonomy invariants](C:/Users/recoveryadmin/Workspace/tools/devtools/docs/architecture/taxonomy.md:701).

24. **Accepted semantic separation does not mandate one production class per concept.**  
    Evidence: [ADR-0002 capability](C:/Users/recoveryadmin/Workspace/tools/devtools/docs/architecture/decisions/ADR-0002-repository-intelligence-identity-and-derivation.md:354) and repeated “conceptual, not required class” qualifications throughout the ADRs.

## Z. Responsibility matrix

| Responsibility | Owns | Consumes | Produces | Explicitly does not own | Status |
|---|---|---|---|---|---|
| Repository | Nominal logical identity/scope | Resource arrangement | Scope for observation | Path, Git, snapshot, Context | Future |
| RepositorySnapshot | Immutable observed state | Policy, observation | Occurrences/state identity | Intelligence completeness, history | Future |
| RepositorySubject | Snapshot-local referential subjecthood | Analyzer-established structure | Referents | Names, ranges, continuity | Future |
| SourceOccurrence | Snapshot-local source anchors | ResourceOccurrence | Provenance/relationship anchors | Automatic subjecthood | Future |
| DerivationDefinition | Semantic computation identity | Semantic specification/config | Compatibility domain | Binding/execution | Future |
| Derivation | Definition applied to direct dependencies | Definition, semantic dependencies | Identified semantic application | Attempt/result set | Future |
| DerivedKnowledge | Immutable knowledge/value/dependencies/provenance | Derivation results | Referable knowledge | Mutable validity, universal confidence | Future |
| RI capability | Currently available semantic realization | Admitted work/dependency access | Realization ability/results | Global planning, caller needs, Tool authority | Future |
| Incremental maintenance | Establish applicable knowledge efficiently | Snapshot/delta/dependency state | Reuse/rederivation decisions | Snapshot identity | Future |
| Graph views | Typed semantic relationships/views | DerivedKnowledge | Traversable projections | Universal graph/store/node identity | Future |
| InformationNeed | Desired purpose-relative information | Consumer uncertainty/anchors | Immutable need | Query, strategy, budget, satisfaction | Future |
| Retrieval planning | Capability applications/bounds/waves | Need, anchors, availability | Plan/applications | Execution/authorization | Future |
| Retrieval | Candidate/evidence discovery | Plan, repository intelligence | Candidates/evidence | Arbitrary derivation, ranking, selection | Future |
| RelevanceEvidence | Native observations/provenance/polarity | Retriever observations | Support/opposition facts | Universal relevance score | Future |
| Ranking | Evidence interpretation | Need/candidate/evidence | Comparative ordering | Selection/representation/budget | Future |
| Disclosure planning | Information/representation selection | Ranked candidates, policy, prior availability | DisclosurePlan | Materialization/presentation authority | Future |
| Materialization | Faithful realization | Plan, applicable source/knowledge | ContextDisclosure or discrepancy | Replanning/new hidden assertions | Future |
| ContextDisclosure | Realized represented information | Materialized plan | Reusable disclosure artifact | ModelRequest/model knowledge | Future |
| Model-input assembly | Consumer-specific presentation | Disclosure, Tools, instructions, conversation, model limits | ModelRequest | Relevance/coverage truth | Future |
| Agent | Goal-directed behavior | Models, Context, capabilities, policy | AgentResult/Run behavior | Raw inference identity | Semantic future; Codex concrete |
| Conversation | Durable communication continuity | Messages/provider refs | History/current refs | Run, Tool, orchestration | Implemented |
| Runtime | One Conversation/ModelInteraction exchange | Message, conversation, interaction | Response, retained assistant message, optional attempt facts | Agent loop, retrieval, Tool dispatch, Evidence | Implemented |
| Tool | Typed validation/execution contract | Candidate typed arguments, Resources | Tool result | Visibility, Action, authorization | Implemented |
| Authorization/admission | Permission for work under authority/policy | Proposal, capability, policy, current grants | Permit/deny decision | Tool validation or approval alone | Governance future; RI admission conceptual |
| InteractionAttempt | Mutable specialized lifecycle | Runtime exchange facts | Terminal state/outcome | Generic Step Attempt, Evidence | Implemented |
| Evidence | Immutable factual historical observation | Completed boundary facts | Evidence records | Current authority, Trace, Telemetry | Implemented for two bounded forms |
| Persistence | Storage/restoration mechanics | Domain-owned representations | Reconstructed Conversation | Domain semantics, exactly-once effects | Implemented for Conversation |

## AA. Identity matrix

| Identity domain | Accepted meaning | Known not to be | Construction status |
|---|---|---|---|
| Repository | Nominal identity across changing states | Path, Git repo/commit, contents, checkout | Unresolved |
| RepositorySnapshot | Immutable complete observed state under semantics | Timestamp, HEAD, watcher batch, intelligence set | Deterministic/content-derived required; digest unresolved |
| ContentIdentity | Address-independent content identity | Path, occurrence, parsed/normalized derivative by default | Raw/normalized semantics and digest unresolved |
| ResourceOccurrence | Snapshot + repository-relative address | Persistent file object, ContentIdentity | Exact type/name unresolved |
| SourceOccurrence | Snapshot-local anchor in ResourceOccurrence | Subject, cross-snapshot entity, semantic name | Locator/identity unresolved |
| RepositorySubject | Snapshot-local structural/semantic referent | Path/range, name, qualified name, AST node, universal graph node | SubjectId/kind/fingerprint unresolved |
| DerivationDefinition | Reusable semantic computation | Callable, plugin, package, binding, source digest | Compatibility/versioning unresolved |
| Derivation | Definition applied to role-bearing direct dependencies | Execution attempt, result artifact | Reproducible construction unresolved |
| DerivationExecution / Attempt | Particular realization occurrence | Definition, derivation, repository truth | Future RI integration unresolved; current InteractionAttempt uses UUID |
| DerivedKnowledge | Reproducible knowledge/result lineage | Arbitrary UUID alone, snapshot ownership, mutable validity | Result participation/digest unresolved |
| InformationNeed | Immutable purpose-relative need | Task, query, budget, satisfaction state | Concrete identity/model unresolved; changed uncertainty means new need |
| ContextCandidate | Underlying addressed referent equivalence | Arbitrary retrieval-result UUID, rendered representation | Concrete model unresolved |
| DisclosurePlan | Identified immutable selection decision | Disclosure or ModelRequest | Identity construction/cardinality unresolved |
| ContextDisclosure | Identified immutable realized artifact tied to plan | Plan, ModelRequest, Conversation history, model knowledge | Identity construction/cardinality unresolved |
| ModelRequest | Immutable semantic invocation value | Interaction occurrence identity | Explicitly has no identity |
| ModelInteraction occurrence | One bounded invocation occurrence | Request/response identity | Implemented `ModelInteractionId` UUID |
| Conversation | Durable communicative continuity | Run, Session schema label | Implemented `ConversationId` UUID |
| ConversationMessage | Durable semantic communication | Prompt or ModelResponse | Implemented `MessageId` UUID |
| InteractionAttempt | One Runtime-managed processing try | Generic Attempt | Implemented `InteractionAttemptId` UUID |
| Evidence | One immutable historical record | Attempt identity or current authority | Implemented `EvidenceId` UUID |

## AB. Artifact/state lifecycle

| Category | Concepts |
|---|---|
| Immutable repository artifacts | RepositorySnapshot, ContentIdentity, ResourceOccurrence direction, SourceOccurrence, RepositorySubject identity, DerivationDefinition, Derivation, DerivedKnowledge, SnapshotDelta relation |
| Mutable runtime state | Conversation, specialized InteractionAttempt, future execution/scheduler state |
| Runtime availability | Registered capabilities, implementation bindings, provider/server readiness, caches |
| Historical Evidence | InteractionAttemptTerminalEvidence, ModelInteractionEvidence, future capability-execution Evidence |
| Purpose-relative immutable artifacts | InformationNeed, ContextCandidate, RelevanceEvidence, DisclosurePlan, ContextDisclosure |
| Purpose-relative mutable assessments/state | Satisfaction/sufficiency assessment, currently available information, disclosure history store, applicability assessment/cache |
| Execution state | Admission, selected binding, dependency acquisition, running/terminal attempt, partial publication, diagnostics |
| Derived knowledge | Immutable assertions/facts/relationships with dependencies and provenance |
| Presentation artifacts | ModelRequest and ModelResponse; no durable Conversation identity unless explicitly materialized |
| Durable communication | ConversationMessage and History, distinct from repository/disclosure history |

Critical lifecycle distinctions:

- Snapshot is immutable; observation is an activity.
- DerivedKnowledge is immutable; applicability is a later assessment.
- InformationNeed is immutable; satisfaction is separate.
- Disclosure history records what happened; current availability can change.
- Capability availability is runtime state; definitions and historical knowledge do not change when availability changes.
- Attempts are mutable until terminal; Evidence is immutable after observation.
- A plan is immutable selection; materialization may fail; a disclosure is immutable realization.

## AC. Consolidated unresolved design surface

### FOUNDATIONAL SEMANTICS STILL UNCERTAIN

These are deliberately open semantic details, not evidence that the accepted high-level boundary is absent:

- exact SnapshotPolicy-to-state-identity relationship;
- raw-versus-normalized ContentIdentity semantics;
- identity construction for Repository, snapshots, occurrences, subjects, definitions, derivations, knowledge, plans, and disclosures;
- definition compatibility/versioning semantics;
- dependency-role and semantic-input representation;
- applicability assessment representation;
- exhaustive-coverage and result-grouping semantics;
- partial publication semantics;
- external/environment-dependent derivations;
- semantics/governance for nondeterministic or LLM-assisted analysis;
- concrete authority, conflict, coverage, fidelity, sufficiency, and coherence evidence models;
- disclosure-plan/disclosure cardinality and identity;
- exact ownership/package boundary for new production APIs.

### CONCRETE IMPLEMENTATION DESIGN

- snapshot data model and observation protocol;
- analyzer/parser interfaces;
- RepositorySubject/SourceOccurrence models and locators;
- DerivationDefinition/Derivation/DerivedKnowledge models;
- capability/binding/catalog/registration/discovery interfaces;
- bounded dependency provider and execution context;
- admission and governance integration;
- execution Evidence schema;
- result publication and transactions;
- maintenance planner and scheduler;
- retrieval planner/application API;
- candidate/evidence/ranker models;
- disclosure planner/materializer/assembler;
- availability/disclosure-history store;
- persistence and serialization boundaries;
- evaluation infrastructure.

### MECHANISM / ALGORITHM CHOICE

- cryptographic hash and flat versus Merkle construction;
- filesystem consistency, retry, or quiescence algorithm;
- subject fingerprints and continuity matching;
- dynamic dependency tracking;
- invalidation discovery and rederivation;
- eager versus lazy maintenance;
- parser and incremental parser technology;
- lexical retrieval: grep, BM25, trigram, or other;
- embeddings and semantic retrieval;
- graph algorithms;
- historical/co-change retrieval;
- deterministic or learned ranking;
- retrieval-wave and stopping policy;
- coverage, utility, redundancy, complementarity, and sufficiency algorithms;
- synthesis validation;
- coherence/reconstruction-burden estimation;
- materialization race handling;
- presentation ordering/tokenization policy.

### STORAGE / PERFORMANCE

- snapshot persistence and eviction;
- content-addressed storage;
- cross-repository content reuse;
- cache keys and reuse granularity;
- reverse dependency indexes;
- graph storage;
- evidence and provenance storage;
- index storage;
- vector storage;
- concurrency primitives;
- in-process versus subprocess/native execution;
- materialized representation and disclosure caching.

### EVALUATION

- exact metric definitions;
- gold standards/fixtures;
- relevant-context recall and precision methodology;
- ranking-quality measurement;
- graph/retriever marginal contribution;
- decomposition quality;
- coverage/sufficiency assessment;
- redundancy, coherence, and reconstruction burden;
- incremental/replay correctness;
- cache/reuse effectiveness;
- task-success attribution;
- model-utilization assessment;
- cost/token/latency accounting;
- live-harness acceptance methodology.

### FUTURE EXTENSION

- cross-snapshot subject continuity;
- richer semantic graph families;
- change-impact and governance graphs;
- model-assisted analysis under separate semantics;
- learned planning/ranking;
- Memory integration;
- reusable Agent/Run/orchestration;
- disclosure authorization;
- structured output and model capability profiles;
- multiple provider adapters and routing.

The roadmap explicitly says the four planned foundational repository-intelligence architecture items—subject identity, snapshot/maintenance, derivation/knowledge, and capability realization—are documented and ready to pass through the architecture-review gate before implementation design. B-0002 is `READY_FOR_DESIGN`, not `READY_FOR_IMPLEMENTATION`. See [roadmap review gate](C:/Users/recoveryadmin/Workspace/tools/devtools/docs/roadmap.md:60) and [B-0002](C:/Users/recoveryadmin/Workspace/tools/devtools/docs/backlog/epics/B-0002-coding-context-substrate.md:1).

## AD. Internal tensions and ambiguities

### DOCUMENTATION AMBIGUITY — ContextCandidate breadth

The taxonomy initially calls ContextCandidate an “addressable repository subject,” while ADR-0003 explicitly allows ResourceOccurrence, SourceOccurrence, DerivedKnowledge, relationships, and other referents. ADR-0003 is more precise for the accepted retrieval layer; “subject” in the taxonomy appears linguistically broader than `RepositorySubject`, but this is not explicitly clarified.

### DOCUMENTATION AMBIGUITY — ADR-0001 implementation sentence

ADR-0001’s header, migration sections, architecture overview, source, and tests say all three phases are implemented. Its final Consequences sentence still says the decision “does not claim the described types are implemented today.” That final sentence is stale relative to the rest of the accepted/current evidence.

### HISTORICAL TERMINOLOGY — ledger’s “current implementation”

The historical Agent milestone says its older Agent boundary was superseded by `devtools.interactions.Interaction`, but the current architecture subsequently superseded `interactions` with `models.interaction`, `agents.conversation`, and `agents.integrations.codex`. The ledger labels the whole section historical, so this is preserved history rather than current authority.

### HISTORICAL TERMINOLOGY — Session labels

Test filenames, variables, and persistence schema names such as `sessions`, `session_messages`, and `session_id` survive. Package documentation explicitly says these are compatibility labels, not a current Session API.

### IMPLEMENTATION LAG — Runtime and native model Tools

ADR-0001 Phase 3 and direct ModelInteraction calls support `ModelRequest.tools` and returned `ModelToolCall` values. Current `Runtime.send()` exposes no tools parameter and performs no Tool-call loop. This is consistent with Runtime’s narrow contract but matters to any reviewer assuming the implemented native boundary is end-to-end Agent Tool execution.

### IMPLEMENTATION LAG — accepted repository/context architecture

The accepted semantics are extensive, while `context`, `orchestration`, `governance`, and `evaluation` remain sparse. This is intentional and repeatedly documented, not evidence of hidden implementation.

### DOCUMENTATION AMBIGUITY — Tools “experimental” wording

Central architecture/taxonomy classify Tool semantics as established, while several source docstrings still call the Tool protocol/runner/adapters experimental. The implemented boundary is real; broader Tool exposure, Action, authorization, and lifecycle remain deferred.

### DOCUMENTATION AMBIGUITY — ModelServing status wording

The taxonomy marks ModelServing semantically established. Package documentation calls the implementation experimental/unfrozen and begins by saying the first slice supports vLLM, then describes llama.cpp as a second provider. This is best reconstructed as established responsibility with experimental provider implementations.

### POSSIBLE ARCHITECTURAL TENSION — generic Capability versus RI capability

The taxonomy says generic Capability is provisional and no generic registry is authorized. ADR-0002 accepts a domain-specific repository-intelligence capability and future catalog/discovery pressure. The accepted reading is that domain-specific realization semantics do not authorize a universal Capability registry; the shared word could nevertheless mislead an external reviewer.

### DOCUMENTATION AMBIGUITY — backlog lifecycle

B-0003 remains `BLOCKED` by B-0008 even though B-0008 is superseded and its child B-0009 is validated. Current roadmap authority points instead to B-0002 and the architecture-review gate. This appears to be backlog lifecycle/history lag, not current repository-intelligence semantics.

### IMPLEMENTATION LAG / BACKLOG WORDING — B-0035

B-0035 still speaks of the Tool descriptor/materialization seam as future implementation pressure, while ADR-0001 Phase 3 and source implement `ToolDescriptor`, `ToolInvocation`, `ModelToolDefinition`, and `ModelToolCall`. The unresolved remainder is independent consumers and Action/governance integration.

### OPEN ACCEPTED BOUNDARY — identity and cardinality

Several concepts are called “identified” or immutable, but exact construction and sometimes cardinality are explicitly open. An external reviewer must not infer UUIDs, hashes, one-plan/one-disclosure cardinality, or persisted IDs.

No authoritative contradiction was found that prevents reconstructing the intended semantic ownership. The ambiguities above should be carried into adversarial review rather than silently resolved.

## AE. Readiness for adversarial review

Yes. Repository evidence is sufficiently coherent to submit the accepted architecture to external adversarial review.

That conclusion is based on repository-declared readiness, not an assessment of architectural quality:

- all four planned ADRs are accepted;
- the repository-intelligence refinements are explicitly sequenced and recorded;
- central architecture summarizes accepted current truth without requiring ADR replay;
- B-0002 is `READY_FOR_DESIGN`;
- the roadmap explicitly places archaeology and adversarial review before implementation design;
- implementation/non-implementation boundaries are repeatedly stated;
- unresolved mechanisms are catalogued rather than disguised as decided.

The evidence does not show a repository-declared blocking foundational semantic hole. It does show deliberately unresolved foundational details—identity construction, snapshot-policy relationships, compatibility, coverage, partial publication, authority evidence, and package/API ownership—that the adversarial process should treat as open design surface.

This readiness statement does not imply that implementation is authorized or that the architecture will survive review.

## AF. Source/path index

| Conclusion | Primary repository evidence |
|---|---|
| Documentation authority hierarchy | [documentation_map.md](C:/Users/recoveryadmin/Workspace/tools/devtools/docs/documentation_map.md:3) |
| Domain ownership and accepted status | [architecture.md](C:/Users/recoveryadmin/Workspace/tools/devtools/docs/architecture.md:12) |
| Semantic vocabulary/non-equivalence | [taxonomy.md](C:/Users/recoveryadmin/Workspace/tools/devtools/docs/architecture/taxonomy.md:3) |
| ModelInteraction/Tool boundary | [ADR-0001](C:/Users/recoveryadmin/Workspace/tools/devtools/docs/architecture/decisions/ADR-0001-cohesive-model-interaction-boundary.md:18) |
| Repository/snapshot identity | [ADR-0002](C:/Users/recoveryadmin/Workspace/tools/devtools/docs/architecture/decisions/ADR-0002-repository-intelligence-identity-and-derivation.md:27) |
| SnapshotDelta/incremental maintenance | [ADR-0002](C:/Users/recoveryadmin/Workspace/tools/devtools/docs/architecture/decisions/ADR-0002-repository-intelligence-identity-and-derivation.md:100) |
| Subjects/source occurrences | [ADR-0002](C:/Users/recoveryadmin/Workspace/tools/devtools/docs/architecture/decisions/ADR-0002-repository-intelligence-identity-and-derivation.md:135) |
| Derivation/knowledge semantics | [ADR-0002](C:/Users/recoveryadmin/Workspace/tools/devtools/docs/architecture/decisions/ADR-0002-repository-intelligence-identity-and-derivation.md:205) |
| Capability realization | [ADR-0002](C:/Users/recoveryadmin/Workspace/tools/devtools/docs/architecture/decisions/ADR-0002-repository-intelligence-identity-and-derivation.md:354) |
| Graph families | [ADR-0002](C:/Users/recoveryadmin/Workspace/tools/devtools/docs/architecture/decisions/ADR-0002-repository-intelligence-identity-and-derivation.md:458) |
| InformationNeed | [ADR-0003](C:/Users/recoveryadmin/Workspace/tools/devtools/docs/architecture/decisions/ADR-0003-information-need-retrieval-evidence-and-ranking.md:27) |
| Candidates/relevance evidence | [ADR-0003](C:/Users/recoveryadmin/Workspace/tools/devtools/docs/architecture/decisions/ADR-0003-information-need-retrieval-evidence-and-ranking.md:66) |
| Retrieval planning/concurrency | [ADR-0003](C:/Users/recoveryadmin/Workspace/tools/devtools/docs/architecture/decisions/ADR-0003-information-need-retrieval-evidence-and-ranking.md:110) |
| Ranking | [ADR-0003](C:/Users/recoveryadmin/Workspace/tools/devtools/docs/architecture/decisions/ADR-0003-information-need-retrieval-evidence-and-ranking.md:154) |
| Disclosure planning | [ADR-0004](C:/Users/recoveryadmin/Workspace/tools/devtools/docs/architecture/decisions/ADR-0004-context-disclosure-planning-and-assembly.md:27) |
| Plan/materialization/disclosure | [ADR-0004](C:/Users/recoveryadmin/Workspace/tools/devtools/docs/architecture/decisions/ADR-0004-context-disclosure-planning-and-assembly.md:109) |
| Assembly and presentation | [ADR-0004](C:/Users/recoveryadmin/Workspace/tools/devtools/docs/architecture/decisions/ADR-0004-context-disclosure-planning-and-assembly.md:176) |
| Synthesis/authority/conflict | [ADR-0004](C:/Users/recoveryadmin/Workspace/tools/devtools/docs/architecture/decisions/ADR-0004-context-disclosure-planning-and-assembly.md:217) |
| Unimplemented design pressure | [B-0002](C:/Users/recoveryadmin/Workspace/tools/devtools/docs/backlog/epics/B-0002-coding-context-substrate.md:14) |
| Superseded navigation assumption | [B-0008](C:/Users/recoveryadmin/Workspace/tools/devtools/docs/backlog/items/B-0008-investigate-repository-context-discovery.md:15) |
| Review sequencing/readiness | [roadmap.md](C:/Users/recoveryadmin/Workspace/tools/devtools/docs/roadmap.md:40) |
| Refinement history | [implementation_ledger.md](C:/Users/recoveryadmin/Workspace/tools/devtools/docs/implementation_ledger.md:240) |
| Current Conversation behavior | [conversation.py](C:/Users/recoveryadmin/Workspace/tools/devtools/src/devtools/agents/conversation/conversation.py:61) |
| Current ModelRequest behavior | [models.py](C:/Users/recoveryadmin/Workspace/tools/devtools/src/devtools/models/interaction/models.py:99) |
| Current Runtime behavior | [runtime.py](C:/Users/recoveryadmin/Workspace/tools/devtools/src/devtools/execution/runtime.py:37) |
| Current Tool execution | [execution.py](C:/Users/recoveryadmin/Workspace/tools/devtools/src/devtools/tools/execution.py:12) |
| Current repository read/list Tools | [filesystem.py](C:/Users/recoveryadmin/Workspace/tools/devtools/src/devtools/tools/filesystem.py:28) |
| Current execution Evidence | [inspection.py](C:/Users/recoveryadmin/Workspace/tools/devtools/src/devtools/observability/evidence/inspection.py:16) |
| Current external Codex Agent | [agent.py](C:/Users/recoveryadmin/Workspace/tools/devtools/src/devtools/agents/integrations/codex/agent.py:32) |
| Qwen experiment boundaries | [Qwen overview](C:/Users/recoveryadmin/Workspace/tools/devtools/experiments/qwen/docs/overview.md:1) |

### Read-only verification

Final Git state matches the initial state:

```text
branch: main
HEAD: 7ff69df7196fe2c3bf67fa894c492b45583e5cfd
tracked changes: none
staged changes: none
git diff --check: clean
git diff --cached --check: clean
```

Pre-existing untracked files, left untouched:

```text
.qwen-selection-stress-bounded-live-report.json
.qwen-selection-stress-live-report.json
.qwen-selection-stress-termination-live-report.json
.qwen-selection-stress-thinking-disabled-live-report.json
```

No files were edited, created, deleted, staged, committed, or otherwise modified.
