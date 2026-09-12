# Agents

`devtools.agents` defines the smallest provider-neutral asynchronous contract
for one message invocation and its final result. It is an extension interface,
not provider, plugin, session, or runtime infrastructure.

## Public API

```python
from devtools.agents import Agent, AgentTurn, ConversationRef
```

The package directly depends only on `devtools.context.message` for `Message`
and `MessageSource`. Message identity, timestamps, roles, and source values
remain owned by Context.

## Agent Protocol

```python
class Agent(Protocol):
    @property
    def source(self) -> MessageSource: ...

    async def send(
        self,
        message: Message,
        *,
        conversation: ConversationRef | None = None,
    ) -> AgentTurn: ...
```

An Agent accepts one message and returns one final message, optionally carrying
opaque agent-owned continuation state. It is async-only, structural, not
runtime-checkable, and has no generic parameters. Compatible implementations do
not inherit from `Agent`:

```python
agent: Agent = implementation
```

`Agent.source` identifies the producer represented by an implementation. Values
such as `codex`, `qwen`, and `local` are open examples, not a provider registry.
A source is not a model setting, account, runtime identity, or session identity.

The generic protocol is input-role and output-role neutral. An implementation
may impose its own policy; for example, Codex accepts USER input and returns an
ASSISTANT message, but neither rule belongs to this contract.

## ConversationRef

```python
@dataclass(frozen=True, slots=True)
class ConversationRef:
    source: MessageSource
    value: str
```

`source` identifies the agent/source that owns external continuation state.
`value` is opaque provider-owned identity. It is not a SessionId, MessageId,
workspace identity, provider configuration, or model identity.

Valid values are nonblank and have no surrounding whitespace:

```python
value == value.strip()
```

Case and punctuation are preserved. UUID-looking and non-UUID strings are both
valid; the generic package does not parse or normalize provider IDs. Concrete
agents must reject an incoming reference owned by another source.

## AgentTurn

```python
@dataclass(frozen=True, slots=True)
class AgentTurn:
    message: Message
    conversation: ConversationRef | None = None
```

An AgentTurn is the final generic result of one invocation. If it includes a
conversation reference, its source must equal the final message source;
mismatches raise `ValueError`. Source comparison is value-based, not object
identity-based.

Stateless implementations are valid:

```python
AgentTurn(message=response, conversation=None)
```

## Invocation

Fresh invocation needs no generic start/create-thread method:

```python
turn = await agent.send(message)
```

Continuation uses the returned generic reference:

```python
next_turn = await agent.send(next_message, conversation=turn.conversation)
```

The contract does not use provider-specific terms such as `resume`; concrete
adapters own their provider mappings.

## Errors, async, and cancellation

Intrinsic value-model violations raise `ValueError`. There is no generic
`AgentError`: provider, transport, and command failures retain their useful
provider-specific boundaries. `Agent.send()` has no synchronous wrapper,
generic timeout, or cancellation method. Normal async cancellation propagates;
concrete implementations own transport cleanup.

## Concrete implementations

[`devtools.codex`](../../codex/docs/overview.md) is the first concrete Agent
implementation. It validates fresh and continued calls, maps Codex thread state
to `ConversationRef`, and maps final provider output to `Message`. This is
evidence that the protocol is a real composition seam, not a hypothetical
abstraction; `agents` does not depend on Codex.

Stateless adapters may return an `AgentTurn` with no conversation reference.
[`devtools.qwen`](../../qwen/docs/overview.md) is one provider-specific example;
its HTTP and llama.cpp mechanics remain local to that adapter.

## Package boundaries

Agents does not own provider transport, subprocesses, HTTP, configuration,
model selection, routing, retries, timeouts, streaming, events, tools,
metrics, session storage, history, persistence, serialization, orchestration,
parallel execution, discovery, registries, entry points, loaders, or dependency
injection.

The `Agent` Protocol is the current extension seam. Plugin infrastructure is
not implemented and is not currently justified.

## Limitations and constrained future evolution

After multiple compatible consumers demonstrate a need, generic streaming,
metrics, capabilities, or multi-message final results may be justified. Generic
timeouts, Agent errors, provider/model identity objects, and serialization
remain deferred. Registries, plugin discovery, provider configuration, routing,
session persistence, and orchestration stay out of scope until architecture
materially changes.
