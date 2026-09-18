# ADR-0001 — Cohesive ModelInteraction boundary

- Status: Accepted
- Date: 2026-09-15
- Scope: reusable model-interaction boundary. Phases 1, 2, and 3 have
  implemented, deterministically validated slices; current conformance limits
  for failed interaction observation and cross-layer correlation are recorded
  below.

## Context

The Qwen/llama.cpp experiments established, incrementally, that a model
interaction needs more than a growing list of request keywords and
experiment-local diagnostics. Provider-reported usage, output limits,
termination, separately returned reasoning, thinking control, and native Tool
protocols have distinct semantics. They must be represented without turning a
normalized response into a provider transport dump, granting a model authority,
or making a provider-specific option a portable fiction.

## Decision

### Semantic request and response

`ModelInteraction` will expose one request boundary:

```text
async send(request: ModelRequest) -> ModelResponse
```

`ModelRequest` is immutable and has no identity. It contains a `Prompt`,
immutable portable `ModelSettings`, an optional continuation/conversation
reference, optional typed provider request settings, model-facing Tool
definitions, optional Tool-choice semantics, and a future response-format
slot. `ModelResponse` remains normalized model output: visible content,
separately returned reasoning content, continuation, `ModelUsage`,
`ModelTermination`, and future normalized `ModelToolCall` values. Neither
value owns a provider wire payload, serving configuration, timing/cache data,
capture policy, or arbitrary metadata.

`ModelSettings` contains portable, per-invocation semantics. Phase 1 migrates
the established `maximum_output_tokens` and `thinking_enabled` settings.
`None` means the framework did not request a value, so provider/model defaults
remain applicable. Later settings (for example temperature, top-p, top-k,
seed, and stop sequences) need their own evidence before implementation. An
adapter must honor an explicitly supplied portable setting or reject it; it
must never silently ignore it.

`ModelInteraction` returns `ModelResponse`, not a `ModelInteractionResult`.
Observation is orthogonal and must not change the semantic return type.

### Typed provider extensions

Portable interaction core defines a typed `ProviderRequestSettings` extension
seam. A provider package may define an immutable subtype, such as
`LlamaCppRequestSettings`, for its own per-request semantics. `ModelRequest`
may carry one such value. Core does not import provider types; an adapter
rejects a value for another provider before issuing a request. No generic
options dictionary, arbitrary JSON, `**kwargs`, or provider-options bag is
permitted.

This separates portable request semantics from provider-specific request
semantics, adapter-construction configuration, serving configuration, and
higher-level caller policy. It does not freeze a broad llama.cpp option
inventory.

### Interaction occurrence and Evidence

One invocation occurrence has a `ModelInteractionId`; an immutable request or
response does not. Existing `EvidenceId` identifies historical Evidence.
Provider response IDs and provider-native Tool-call IDs are opaque captured
provider facts, not framework identities.

`ModelInteractionEvidence` is an Evidence form, not a parallel generic record
abstraction. It records immutable historical truth about one observed model
interaction. Models own semantic request/response translation. Provider
adapters construct provider-boundary facts and perform field-aware redaction.
Observability owns capture policy, capture manifests, Evidence construction,
collection, and inspection. A model interaction can run with or without
Runtime and with or without observation; Runtime is never required to create
this Evidence. Future Trace references interaction/Evidence identities;
Evaluation consumes Evidence without owning or mutating it; Telemetry may
later aggregate operational measures but does not own historical truth.

Capture policy makes capture explicit. Structural facts retained when available
include occurrence and Evidence identity, provider/source, start/completion/
duration, policy/manifest, usage, termination, failure stage/category,
serving-profile provenance, and presence or omission of requested settings.
Payload capture is controlled for prompts, visible/reasoning text, disclosed
Tool schemas, model Tool-call arguments, provider-specific setting values,
effective provider request/response, provider IDs, timings/cache diagnostics,
and bounded error details. The manifest distinguishes unavailable, omitted,
and redacted data. Credentials, authorization headers, secrets, environment
variables, and equivalent sensitive transport state are never generically
captured. `ProviderExchange` exists only inside capture-controlled interaction
Evidence; it holds typed selected provider request/response facts, response
identity/model identity, and provider diagnostics. It is not a metadata map or
an unconditional raw transport dump. When a payload class has multiple
occurrences with different retention states, its collection manifest uses
`PARTIAL` rather than falsely claiming whole capture, omission, redaction, or
unavailability.

The present implementation emits `ModelInteractionObservation` only after a
provider result has been successfully received and normalized. Provider,
transport, or normalization failures therefore do not currently produce
equivalent `ModelInteractionEvidence`, and an observer callback failure can
surface after the provider response exists. Runtime `InteractionAttemptId` and
`ModelInteractionId` are not automatically correlated. These are conformance
and implementation pressure: model/provider outcome, evidence-observation
outcome, and outer orchestration outcome remain distinct. Evaluation must not
treat the current completed-Evidence population as all assigned model
realizations, overload either identity as an evaluation realization, or assume
capture-controlled Evidence is exact replay material.

### Serving provenance

`ServingProfileIdentity` is a future immutable reproducibility/provenance
snapshot distinct from `ServingConfiguration`. It identifies behaviorally
relevant facts known for a serving environment: provider, model repository and
revision, artifact filename/hash and quantization, pinned server build/image,
served alias, context capacity, and configured template/reasoning defaults.
Ports, container IDs, readiness state, and startup timeouts are operational
facts, not model identity. The current Qwen profile fingerprint is a precursor
that must be assessed rather than assumed complete. Captured interaction
Evidence carries the serving-profile fingerprint/provenance when available.
A configured profile or provider model alias carries evidence only at the
strength established by its source; it does not prove an unobservable hosted
provider revision or unchanged provider defaults. Timing and resource
measurements likewise retain their measurement boundary rather than becoming
interchangeable generic cost facts.

### Model-facing Tools

Tools remain independent of model interaction. A Tool may later expose a
model-agnostic `ToolDescriptor` containing only an intentionally bounded name,
description, and input JSON Schema, plus a `ToolInvocation` materialization
surface for converting untrusted serialized arguments into typed candidate
Tool input. The schema vocabulary is JSON Schema, but this ADR deliberately
does not freeze its internal immutable representation or introduce Pydantic or
a general schema framework.

An application, Agent, or experiment composition seam projects
`ToolDescriptor` to `ModelToolDefinition`; it is the only layer that depends
on both Tool and model concepts. The descriptor is disclosure, not a mirror of
every executable input or host capability. For example, a repository-read Tool
may disclose a repository-relative `path`, never its root, host paths,
filesystem handles, or execution authority. Existing Tool validation remains
authoritative for execution-side admission. `CommandTool` is not generically
disclosed as arbitrary command execution.

`ModelToolCall` is normalized provider output: a requested callable name,
serialized arguments, and optional opaque provider call ID. It is not an
Action, authorization, typed Tool input, execution, approval, or governance
decision. The required flow is:

```text
ToolDescriptor -> ModelToolDefinition -> ModelRequest -> provider-native Tool
definition -> provider response -> ModelToolCall -> materialization ->
future Action/request interpretation -> authorization -> ToolRunner
```

`ModelInteraction` never executes a Tool. The model may request a capability;
it does not receive authority to execute it.

### Dependency direction

The future boundary preserves these directions:

```text
models.interaction core <- provider adapters, execution, observability,
                           agents/application composition, experiments
tools                   <- agents/application composition, experiments
models.interaction + tools <- composition seam
models.serving          <- experiments / operational composition
observability           <- evaluation
```

Forbidden dependencies are `models.interaction -> tools`,
`models.interaction -> ToolRunner`, `tools -> models.interaction`,
`execution -> observability`, and `models.serving -> caller request policy`.
Providers may depend on portable interaction types. Models and execution do
not import observability merely to operate.

### Deferred concepts

`ModelResponseFormat` and `ModelCapabilities` are recognized future boundary
concepts but are not implementation requirements now. There is no current
reusable structured-output consumer or runtime capability-negotiation need.
Adapters continue to honor explicit settings or reject them. This decision
does not authorize a capability registry, endpoint probing, automatic request
adaptation, routing, generic generation configuration, generic Action or
authorization, automatic Tool execution, Context work, Agent promotion,
orchestration, Trace/Telemetry backends, or provider registry.

## Migration plan

### Phase 1 — Request boundary

Introduce immutable `ModelRequest`, `ModelSettings`, and typed provider request
extensions. Atomically migrate established output and thinking controls,
`ModelInteraction` implementations/fakes, Runtime mechanically, and direct
experiment callers; remove the old duplicated keyword request API. Prove
validation and provider serialization deterministically. This phase is
implemented and validated deterministically; no live model was required.

### Phase 2 — Interaction Evidence and serving provenance

Introduce `ModelInteractionId`, capture policy/manifest, `ProviderExchange`,
`ModelInteractionEvidence`, and `ServingProfileIdentity`; migrate reusable
B-0009 model-interaction diagnostics. Prove capture, omission, redaction, and
provenance deterministically. A separately authorized tiny live diagnostic may
follow.

This phase is implemented and deterministically validated. It provides a
portable completed-interaction observation seam, immutable interaction
identity, explicit capture policy and manifest states, bounded
`ProviderExchange`, `ModelInteractionEvidence`, process-local inspection, and
`ServingProfileIdentity`. It does not retain raw transport payloads, implement
Trace or Telemetry, or require Runtime or a model interaction to import
observability.

### Phase 3 — Model-native Tool boundary

Introduce model-agnostic Tool descriptor/invocation surfaces,
`ModelToolDefinition`, `ModelToolCall`, and llama.cpp native Tool translation/
parsing, with a strict no-execution invariant. Retain B-0009's textual grammar
as historical/control evidence initially. Prove deterministically before one
separately authorized bounded native-Tool conformance run.

This phase is implemented and deterministically validated. `ToolDescriptor`
and `ToolInvocation` remain model-agnostic tools-side disclosure and candidate
input materialization seams. `ModelToolDefinition` and `ModelToolCall` are
immutable normalized invocation input/output. llama.cpp translates only those
values at its provider boundary. The experiment composition seam
`normalize_tool_descriptor` performs the explicit descriptor-to-definition
ownership and representation transition. No returned call is looked up, validated,
authorized, or executed; `Tool.validate()` remains execution admission.

## Consequences

Future provider behavior has a defined home: portable request semantics in
`ModelSettings`, typed provider-only semantics in provider extensions,
normalized output in `ModelResponse`, and capture-controlled wire diagnostics
in interaction Evidence. The decision freezes responsibility and dependency
direction. All three scoped phases are implemented and deterministically
validated; this does not claim that broader reusable Agent Tool orchestration,
Tool authorization, Action semantics, or a complete Tool ecosystem exists.
