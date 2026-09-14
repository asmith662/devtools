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

Finish reasons and separated reasoning content remain deferred diagnostic
pressure. They are not part of this established output-bound semantic.

- hard_dependencies: B-0045
- pressure_dependencies: B-0035, B-0036, B-0027
- operational_dependencies: model/provider path needing unavailable semantics
- promotion_trigger: a stable consumer needs meaning not expressible by current ModelInteraction
- validation_level: INTEGRATION
