# Runtime

## Purpose

`Runtime` is a stateless coordination service that applies one caller-selected
`Agent` interaction to one mutable `Session`. It owns no retained interaction
or provider state; `Session` owns retained `History` and current continuation
references, while an `Agent` owns response and provider behavior.

```text
Message          one contextual utterance
Session          retained mutable interaction state
Agent            asynchronous responder contract
Runtime          one-interaction coordinator
```

Runtime is provider-neutral. [Codex](../../codex/docs/overview.md) is a real
acceptance implementation, not a Runtime dependency.

## Public API

```python
from devtools.runtime import Runtime

runtime = Runtime()
turn = await runtime.send(
    session=session,
    agent=agent,
    message=message,
)
```

`Runtime` is the complete root public API. It has no configuration, identity,
lifecycle, lock, retained Session, retained Agent, continuation, last result,
or other interaction state.

## Coordination algorithm

`Runtime.send()` performs one `Agent.send()` invocation in this order:

1. Acquire `session.turn()`.
2. Record the supplied input `Message` once.
3. Retrieve the current continuation with
   `session.conversation_for(agent.source)`.
4. Invoke `Agent.send()` exactly once.
5. Validate that the returned Message source equals `agent.source`.
6. Record the returned Message.
7. Store the returned continuation when it is non-`None`.
8. Return the original `AgentTurn`.
9. Release `session.turn()`.

The complete operation is held inside `session.turn()`, including the awaited
Agent call. Runtime never directly constructs History or mutates the public
conversation mapping.

## Messages and Agent selection

The caller explicitly supplies the Agent. Runtime does not route, discover,
rank, substitute, or fall back between Agents.

Any valid `Message` may be submitted to any Session. Runtime is role-neutral:
it does not require a USER input or an ASSISTANT output. Input source identifies
the producer of the Message and need not equal the selected Agent source.

Runtime records the supplied Message exactly once after turn acquisition. The
same exact Message may be submitted again; each invocation records another
occurrence without cloning, deduplicating, retry classification, or MessageId
regeneration. Such repetitions are factual repeated submission, not a retry or
replay model.

## Continuations and validation

Runtime retrieves continuations only through Session's source-keyed API and
trusts Session's continuation/source invariant. It also trusts AgentTurn's
continuation/message-source invariant and provider-specific continuation
syntax.

Runtime uniquely knows both the selected Agent and returned AgentTurn, so it
validates:

```python
turn.message.source == agent.source
```

On mismatch, Runtime raises `ValueError` before recording returned state. The
input remains retained, while the returned Message and continuation are not
committed.

On success, Runtime records the returned Message before replacing continuation
state. Continuation state therefore cannot advance beyond the History entry
that produced it. A returned `conversation=None` performs no update and does
not clear an existing Session continuation. Runtime returns the original
`AgentTurn`; it defines no Runtime-specific result model.

## Concurrency

Runtime relies on Session-owned complete-turn coordination:

```text
same Session object       complete Runtime turns serialize
different Session objects Runtime operations may proceed concurrently
```

This scope covers the awaited Agent call. For the same source, if turn A reads
ref A and returns ref B, a turn B queued while A is in flight receives ref B
when it eventually invokes its Agent. This prevents stale continuation use.

Runtime owns no global lock and imposes no generic lock on a shared Agent
instance; concrete Agents own their own concurrency guarantees. Runtime
inherits Session coordination boundaries: they are object-local,
single-event-loop, and in-process. They do not synchronize event loops,
threads, separately reconstructed objects with equal Session IDs, processes,
or distributed workers.

## Failures and cancellation

If `Agent.send()` raises, Runtime retains the already-recorded input, records
no output, leaves the current continuation unchanged, releases Session
coordination, and propagates the original exception unchanged. Runtime does not
distinguish transport, provider, or parsing failure phases and creates no error,
status, or informational Messages.

Cancellation while waiting to acquire `session.turn()` leaves Session unchanged:
input is not recorded and Agent is not called. Cancellation while the Agent is
in flight leaves the retained input, commits no output or continuation update,
releases Session coordination, and propagates cancellation. Agent transport
cleanup belongs to the concrete Agent.

Runtime coordination is forward-only, not transactional. It does not roll back
an earlier Session mutation if a later local operation unexpectedly fails.

## Boundaries

Runtime has no retry, fallback, timeout, deadline, persistence, context
compiler, tracing, attempt, routing, or Agent-selection policy. One Runtime
call invokes one supplied Agent once. Timeout policy belongs to the concrete
Agent or transport.

Runtime inherits Session's current limitation of one current `ConversationRef`
per `MessageSource`. It does not solve independent continuations for multiple
logical participants sharing a source.

## Dependencies

```text
runtime -> agents
runtime -> context.message
runtime -> context.session
```

Runtime has no direct Codex dependency.

## Live Codex acceptance

The opt-in Runtime/Codex acceptance uses an isolated temporary Git repository.
It verifies fresh input/output retention, Session-stored continuation,
automatic Runtime continuation lookup, same-thread resume, an exact four-Message
History, stable SessionId and creation time, and resumed read-only write denial.
This is evidence that Runtime coordinates one real Agent implementation; it is
not a requirement that Runtime depend on Codex.

## Constrained future evolution

Concrete consumers may justify tracing/evidence, an attempt model, turn
deadline policy, Agent routing/selection, or coordination-policy collaborators.
Retry policy, Runtime result/error models, and constructor collaborators remain
speculative. Session persistence, context compilation, provider configuration,
ConversationRef parsing, and Agent transport behavior remain outside Runtime
ownership.
