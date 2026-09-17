# Architecture

`devtools` is organized by responsibility. This document is the canonical
overview of current and accepted system architecture: it records domains,
cross-package ownership, dependency direction, and cross-domain composition.
[The taxonomy](architecture/taxonomy.md) defines semantic terms; package-local
documentation defines exact implemented APIs; and
[architecture decisions](architecture/decisions/) preserve rationale and
historical evolution. Accepted architecture is summarized here as well as in
its ADR, while accepted-but-unimplemented semantics never claim a current API.

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
- Model proposal, Tool visibility, and Tool validation are not authorization.
- Cancellation is not rollback, and communication failure does not prove an
  external effect did not occur.

## Accepted ModelInteraction boundary

[ADR-0001](architecture/decisions/ADR-0001-cohesive-model-interaction-boundary.md)
approves a cohesive future ModelInteraction boundary: immutable semantic
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
and repository-relationship graph families. It also preserves Context as
purpose-relative selection and disclosure rather than repository truth.

This architecture does not imply a current `context` implementation. Filesystem
Resources remain access mechanisms, not Repository identity. Retrieval,
ranking, Context compilation, progressive disclosure, storage, and evaluation
remain unimplemented future responsibilities; Runtime remains narrow and model
requests remain non-authoritative.

## Accepted retrieval and ranking semantics

[ADR-0003](architecture/decisions/ADR-0003-information-need-retrieval-evidence-and-ranking.md)
accepts InformationNeed, bounded retrieval planning/applications,
ContextCandidate, provenance-bearing RelevanceEvidence, and ranking semantics.
It preserves retrieval as multi-strategy evidence discovery; ranking as evidence
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
strings. A DisclosureOption is a future purpose-relative information-and-
representation possibility, with origin, form, fidelity, cost, and provenance
kept semantically distinct. Source-preserving material, existing knowledge
projections, and synthesized semantic assertions are distinct origins; new
assertions remain explicit ADR-0002 DerivedKnowledge rather than opaque compiler
text. Composite provenance-preserving representations are permitted.

DisclosurePlan, ContextDisclosure, and ModelRequest remain distinct:

```text
InformationNeed -> DisclosurePlan -> materialization -> ContextDisclosure
    -> model-input assembly -> ModelRequest
```

The Plan is an immutable selected-information decision; the Disclosure is an
immutable realized information artifact under/reference to that plan; the
ModelRequest is a consumer-specific presentation. Materialization cannot silently
re-plan or present inapplicable information as current. Planning and possession
of a disclosure are not disclosure/presentation authority.

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
authority, conflict, coherence, synthesis, materialization, cache, assembly,
and evaluation mechanisms remain unimplemented.

See [documentation_map.md](documentation_map.md) for current package
documentation, [taxonomy.md](architecture/taxonomy.md) for definitions, and
[ADR-0001](architecture/decisions/ADR-0001-cohesive-model-interaction-boundary.md)
for the approved future boundary.
