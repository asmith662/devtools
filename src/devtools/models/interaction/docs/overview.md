# `devtools.models.interaction`

This package owns one bounded model invocation boundary:

```text
Prompt -> ModelInteraction -> ModelResponse
```

`Prompt` is per-invocation model-facing input and deliberately has no durable
conversation-message identity or local conversation timestamp. `ModelResponse`
contains model output, its source, and optional provider continuation; it is
not automatically retained as a `ConversationMessage` or treated as an Agent
result.

`ModelInteraction` performs provider request/response translation and exposes
provider-local failure and continuation behavior. It does not own conversation
history, goals, tools, authorization, Runtime orchestration, or model-serving
lifecycle. `ConversationRef` and `InteractionSource` are narrow model-provider
values used at this boundary.

The configurable llama.cpp implementation is under `providers/`; it communicates
with an already-running model endpoint. Endpoint lifecycle is separately owned
by `devtools.models.serving`.
