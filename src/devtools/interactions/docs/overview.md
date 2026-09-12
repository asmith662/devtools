# Interactions

`devtools.interactions` defines the smallest provider-neutral asynchronous
contract for one bounded exchange and its final result:

```text
Message + optional opaque ConversationRef
-> final Message + optional opaque ConversationRef
```

`Interaction` defines that contract. Concrete adapters under
`devtools.interactions.providers` own provider transport, request/response
adaptation, provider configuration, failures, and optional continuation
mapping. Neither layer implies planning, tool use, repository access,
authority, or an action loop.

`ConversationRef` is opaque source-owned provider continuation state. It is
not framework history, a Session, model identity, or provider configuration.

## Boundaries

Model identity is configuration.
`devtools.interactions.providers.LlamaCppInteraction` accepts an endpoint,
served model name, and `MessageSource`; compatible Qwen, Llama, DeepSeek,
Gemma, and Mistral deployments therefore use the same interaction type.

An agent is a system that owns agentic behavior such as planning, action
selection, looping, or execution. A harness is framework-owned bounded
composition around interactions. Codex can be reached through `Interaction`
while remaining an externally agentic system; the Qwen read experiment remains
a Qwen-specific acceptance harness in the repository-level `experiments/`
area.

Serving lifecycle stays separate in `devtools.model_serving`: it owns endpoint,
readiness, and container lifecycle, not model invocation.
