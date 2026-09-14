# B-0046 — Investigate advanced model-interaction/provider pressure

- type: INVESTIGATION
- status: DEFERRED
- decision_maturity: SEMANTICS_PARTIAL
- necessity: FUTURE_REQUIRED
- architectural_significance: STRUCTURAL
- urgency: DEFERRED
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
on one `ModelInteraction` request. It is a requested per-invocation output
limit, not ModelUsage, context-window capacity, cumulative run budgeting, or
Context budgeting. An adapter must honor a supplied value or reject it.

For llama.cpp's pinned OpenAI-compatible chat route,
`maximum_output_tokens` maps only to request `max_tokens`; absent values leave
the existing request payload unchanged. Provider-reported usage remains factual
post-hoc data and is not clamped, derived, or reconciled to the requested cap.
The B-0009 runner may select a cap as experiment-local policy and records that
choice in its existing schema `/3` fixture data.

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
values remain provider-response errors. The B-0009 schema `/3` artifact retains
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
The B-0009 schema `/3` artifact retains optional reasoning by model turn for
this narrow diagnostic purpose, without printing, persisting to Conversation,
or retaining raw provider response payloads.

Thinking controls, reasoning budgets, reasoning parsing, and raw
provider-response retention remain deferred pressure.

- hard_dependencies: B-0045
- pressure_dependencies: B-0035, B-0036, B-0027
- operational_dependencies: model/provider path needing unavailable semantics
- promotion_trigger: a stable consumer needs meaning not expressible by current ModelInteraction
- validation_level: INTEGRATION
