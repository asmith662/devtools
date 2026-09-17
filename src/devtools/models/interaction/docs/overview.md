# `devtools.models.interaction`

This package owns one bounded model invocation boundary:

```text
ModelRequest -> ModelInteraction -> ModelResponse
```

`ModelRequest` is an immutable semantic invocation value containing a `Prompt`,
immutable portable `ModelSettings`, an optional provider continuation, and an
optional typed provider request extension. `Prompt` is per-invocation
model-facing input and deliberately has no durable conversation-message
identity or local conversation timestamp. `ModelResponse`
contains model output, its source, optional provider continuation, optional
provider-reported `ModelUsage`, and optional provider-reported
`ModelTermination`, plus optional separately returned textual reasoning. Usage
retains only reported input, output, and total token counts; absent counts are
not estimated. Termination retains only a normal stop, an output-limit end, or a
tool-call end when the provider reports one. Reasoning remains distinct from
visible response content and is never substituted or concatenated into it.
None of these provider facts is automatically retained as a
`ConversationMessage` or treated as an Agent result.

`ModelInteraction` performs provider request/response translation and exposes
provider-local failure and continuation behavior. It does not own conversation
history, goals, tools, authorization, Runtime orchestration, or model-serving
lifecycle. `ConversationRef` and `InteractionSource` are narrow model-provider
values used at this boundary.

`ModelSettings.maximum_output_tokens` is an optional positive,
provider-neutral completion-token limit for that single invocation. Its absence
requests no cap. This request constraint is distinct from provider-reported
`ModelUsage`, model context-window capacity, and any future Context or run
budget. An adapter must honor a supplied limit or reject it explicitly.

`ModelSettings.thinking_enabled` is optional: `None` preserves provider
defaults, while `True` or `False` explicitly requests thinking on or off. An
adapter must honor an explicit value or reject it; it must not silently ignore
the request.

`ProviderRequestSettings` is an immutable typed extension seam for one
provider's per-request settings. Portable core does not import provider types;
an adapter rejects another provider's extension instead of silently ignoring
it. `LlamaCppRequestSettings` currently has no extra field because the two
established llama.cpp controls are portable settings. It reserves a typed
provider-owned seam rather than an untyped options dictionary.

All three phases of [ADR-0001](../../../../../docs/architecture/decisions/ADR-0001-cohesive-model-interaction-boundary.md)
are implemented. A provider may emit a completed `ModelInteractionObservation`
to an optional `ModelInteractionObserver`; that transient seam does not change
`send()` or `ModelResponse`, and it does not import observability.
Observability may use it to construct immutable Evidence, while an interaction
remains usable without an observer.

`ModelRequest.tools` contains an ordered immutable tuple of normalized
`ModelToolDefinition` values. `ModelResponse.tool_calls` contains normalized
`ModelToolCall` requests returned by a provider. Neither references executable
Tools, ToolRunner, authorization, or conversation history. A call is descriptive
model output, not execution. The composition seam that converts a tools-owned
`ToolDescriptor` into this normalized model value is outside both packages.
Structured output and capabilities remain unimplemented.

The configurable llama.cpp implementation is under `providers/`; it communicates
with an already-running model endpoint. Endpoint lifecycle is separately owned
by `devtools.models.serving`.
