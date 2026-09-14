# `devtools.models.interaction`

This package owns one bounded model invocation boundary:

```text
Prompt -> ModelInteraction -> ModelResponse
```

`Prompt` is per-invocation model-facing input and deliberately has no durable
conversation-message identity or local conversation timestamp. `ModelResponse`
contains model output, its source, optional provider continuation, and optional
provider-reported `ModelUsage`. Usage retains only reported input, output, and
total token counts; absent counts are not estimated. It is not automatically
retained as a `ConversationMessage` or treated as an Agent result.

`ModelInteraction` performs provider request/response translation and exposes
provider-local failure and continuation behavior. It does not own conversation
history, goals, tools, authorization, Runtime orchestration, or model-serving
lifecycle. `ConversationRef` and `InteractionSource` are narrow model-provider
values used at this boundary.

One request may optionally specify `maximum_output_tokens`: a positive,
provider-neutral completion-token limit for that single invocation. Its absence
requests no cap. This request constraint is distinct from provider-reported
`ModelUsage`, model context-window capacity, and any future Context or run
budget. An adapter must honor a supplied limit or reject it explicitly.

The configurable llama.cpp implementation is under `providers/`; it communicates
with an already-running model endpoint. Endpoint lifecycle is separately owned
by `devtools.models.serving`.
