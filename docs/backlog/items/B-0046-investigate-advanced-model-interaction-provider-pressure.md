# B-0046 — Investigate advanced model-interaction/provider pressure

- type: INVESTIGATION
- status: BACKLOG
- decision_maturity: READY_FOR_IMPLEMENTATION
- necessity: FUTURE_REQUIRED
- architectural_significance: STRUCTURAL
- urgency: SOON
- evidence_basis: MULTIPLE
- scope: advanced model interaction and provider adaptation beyond established core
- primary_domain: models
- supporting_domains: agents, tools, execution, evaluation
- split_from: B-0030

## Problem / value

Preserve pressure for streaming, richer structured responses, model-native
action payloads, reasoning or usage metadata, provider capability discovery,
additional provider adapters, and later routing/model selection only when a
consumer needs them. Codex is an external Agent, not a model-provider consumer.

## Approved cohesive boundary

[ADR-0001](../../architecture/decisions/ADR-0001-cohesive-model-interaction-boundary.md)
freezes the next cohesive implementation boundary. It replaces further
field-by-field request growth with immutable `ModelRequest` and
`ModelSettings`, typed provider request extensions, normalized model-native
Tool definitions/calls, capture-controlled model interaction Evidence, and
serving-profile provenance. The approved phases are request migration,
interaction Evidence/provenance, then model-native Tools. The ADR does not
implement deferred structured output, capabilities, generic generation
configuration, provider registry, Context, Action, governance, Trace, or
Telemetry.

## Implemented Phase 1: cohesive request boundary

Phase 1 now provides immutable `ModelRequest` and `ModelSettings`, typed
`ProviderRequestSettings`, and the empty typed `LlamaCppRequestSettings`
extension seam. `ModelInteraction.send()` accepts exactly one `ModelRequest`;
the previous request keyword API has been removed. `maximum_output_tokens` and
`thinking_enabled` retain their established semantics as portable
`ModelSettings` fields. Runtime and the Qwen experiments mechanically forward
those immutable settings; llama.cpp maps them to `max_tokens` and
`chat_template_kwargs.enable_thinking` respectively. No default policy,
provider options bag, Evidence, serving provenance, or model-native Tool
behavior was introduced.

## Implemented Phase 2: interaction Evidence and serving provenance

Phase 2 now provides `ModelInteractionId`, an optional completed-interaction
observation seam, capture-controlled immutable `ModelInteractionEvidence`, a
typed capture policy and manifest, bounded provider exchange facts,
process-local inspection, and `ServingProfileIdentity`. Structural request and
response facts remain inspectable while prompts, visible text, reasoning, and
selected provider identifiers are explicitly captured, omitted, redacted, or
unavailable. Runtime and models do not depend on observability, and raw
transport payloads, Trace, Telemetry, persistence, and model-native Tool
semantics remain deferred.

For multiple disclosed schemas or returned Tool-call argument values, the
Phase 3 capture manifest uses `PARTIAL` when occurrence retention states differ;
it does not mislabel a collection containing captured payload as wholly omitted
or redacted.

## Implemented Phase 3: model-native Tool boundary

Phase 3 now provides explicit model-agnostic `ToolDescriptor` and
`ToolInvocation` seams, normalized immutable `ModelToolDefinition` and
`ModelToolCall` values, llama.cpp native Tool serialization/parsing, and
capture-controlled Tool schema/argument Evidence. Model Tool calls are only
descriptive requests: no Tool lookup, validation, authorization, Action, or
execution occurs. B-0009's textual proposal grammar remains experiment-local
historical/control evidence.

## Established subset: provider-reported usage

The B-0009 coding-worker acceptance consumer established the smallest reusable
usage boundary: immutable optional `ModelUsage` on `ModelResponse`, with
provider-reported input, output, and total token counts. Missing counts remain
absent; no local estimation occurs and a provider-reported total is never
derived or forced to equal the component counts.

The pinned llama.cpp server source for image build `b10868`, commit
[`304665fe7`](https://github.com/ggml-org/llama.cpp/blob/304665fe7/tools/server/README.md#timings-and-context-usage),
documents `usage.prompt_tokens`, `usage.completion_tokens`, and
`usage.total_tokens` for `/v1/chat/completions`. `LlamaCppInteraction` maps
only those fields. Its timing, cached-token, and reasoning fields remain
provider-specific and unpromoted. The B-0009 report retains per-turn usage and
an exact cumulative field total only when every model turn supplied that field.

This establishes no Context budgeting, tokenizer, prompt provenance, generic
metrics, Telemetry, Trace, pricing, or provider-capability registry.

## Established subset: bounded output request

The measured selection-stress acceptance exposed a separate request-side
pressure: without a completion cap, the pinned llama.cpp route may use the
remaining context window for generation even when the prompt is small. The
minimal reusable response is optional positive-integer `maximum_output_tokens`
in `ModelSettings` on one `ModelInteraction` request. It is a requested per-invocation output
limit, not ModelUsage, context-window capacity, cumulative run budgeting, or
Context budgeting. An adapter must honor a supplied value or reject it.

For llama.cpp's pinned OpenAI-compatible chat route,
`maximum_output_tokens` maps only to request `max_tokens`; absent values leave
the existing request payload unchanged. Provider-reported usage remains factual
post-hoc data and is not clamped, derived, or reconciled to the requested cap.
The B-0009 runner may select a cap as experiment-local policy and records that
choice in its schema `/4` fixture data.

## Established subset: provider-reported termination

The bounded selection-stress acceptance established a separate response-side
diagnostic pressure: a requested output cap can be reached while visible
assistant content remains empty. The smallest reusable response is optional
immutable `ModelTermination` on `ModelResponse`. It preserves only the
provider-reported semantic end of a successful response: normal stop,
output/length limit, or tool-call termination. It is independent of
`maximum_output_tokens` (a request constraint) and `ModelUsage` (post-hoc
provider accounting), and neither is inferred from the other.

For llama.cpp image build `b10868`, commit
[`304665fe7`](https://github.com/ggml-org/llama.cpp/blob/304665fe7/tools/server/server-task.cpp),
`choices[0].finish_reason` maps `stop`, `length`, and `tool_calls` to those
three values. Missing or null values remain absent; malformed or unrecognized
values remain provider-response errors. The B-0009 schema `/4` artifact retains
the optional termination for each model turn without retaining raw provider
payloads.

## Established subset: separately returned reasoning content

A direct bounded Qwen diagnostic established that the pinned llama.cpp route
can return meaningful `message.reasoning_content` while visible
`message.content` remains empty and the provider reports `length` termination.
The minimal reusable response is optional immutable `reasoning_content` on
`ModelResponse`. It preserves only separately returned textual model reasoning
for the same interaction, without substituting, concatenating, or interpreting
it as visible assistant content. Missing and null provider fields remain
absent; a supplied empty string is preserved exactly.

For llama.cpp image build `b10868`, commit
[`304665fe7`](https://github.com/ggml-org/llama.cpp/blob/304665fe7/common/chat.cpp),
`choices[0].message.reasoning_content` maps directly to that field. It remains
independent of `ModelUsage`, `ModelTermination`, and request-side output limits.
The B-0009 schema `/4` artifact retains optional reasoning by model turn for
this narrow diagnostic purpose, without printing, persisting to Conversation,
or retaining raw provider response payloads.

## Established subset: per-request thinking control

A direct bounded diagnostic established that the exact pinned Qwen profile
honors per-request thinking disable: `chat_template_kwargs.enable_thinking`
set to `false` returned visible `OK`, no reasoning content, `stop`, and two
completion tokens, while the unchanged default consumed the 128-token cap in
reasoning. The smallest reusable request semantic is optional
`thinking_enabled: bool | None` in `ModelSettings` for one `ModelInteraction` invocation. `None`
preserves provider defaults; explicit `True` or `False` must be honored or
rejected rather than silently ignored.

For llama.cpp, explicit values map only to
`chat_template_kwargs.enable_thinking`; `None` introduces no such field. This
request fact remains independent of `maximum_output_tokens`,
`reasoning_content`, `ModelUsage`, and `ModelTermination`. It does not create a
reusable thinking policy or default, and the Qwen acceptance runner records its
explicit experiment choice in schema `/4`.

Reasoning budgets, reasoning parsing, generic chat-template kwargs, and raw
provider-response retention remain deferred pressure.

- hard_dependencies: B-0045
- pressure_dependencies: B-0035, B-0036, B-0027
- operational_dependencies: model/provider path needing unavailable semantics
- promotion_trigger: a stable consumer needs meaning not expressible by current ModelInteraction
- validation_level: INTEGRATION
