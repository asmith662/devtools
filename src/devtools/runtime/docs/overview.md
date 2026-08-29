# Runtime

## Purpose

`Runtime` is a configuration-bearing but interaction-stateless coordination
service that applies one caller-selected `Agent` interaction to one mutable
`Session`. Its only retained configuration is an optional fixed
`AttemptObserver`; it owns no retained interaction or provider state. `Session`
owns retained `History` and current continuation references, while an `Agent`
owns response and provider behavior.

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
# Or: runtime = Runtime(observer=observer)
turn = await runtime.send(
    session=session,
    agent=agent,
    message=message,
)
```

`Runtime` is the complete root public API. `runtime.observer` is readable,
fixed configuration with type `AttemptObserver | None`; no replacement API
exists. Runtime has no identity, lifecycle, lock, retained Session, retained
Agent, continuation, last result, current Attempt, or other interaction state.

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

## Optional Attempt observation

`Runtime()` and `Runtime(observer=None)` create no Attempt at all: no
AttemptId, Attempt timestamp, lifecycle bookkeeping, callback, or hidden null
observer exists for that invocation. The unobserved processing path retains the
ordinary Runtime contract.

With an observer, Runtime creates an Attempt only after Session turn acquisition
and successful input retention. It then calls `attempt_started()` before
continuation lookup or Agent invocation. This is an admission boundary: waiting
cancellation, input-retention failure, or Attempt construction/start observation
failure results in no Agent call; the first two create no Attempt/callback.

After successful start observation, the Attempt spans continuation lookup,
Agent invocation, returned-source validation, output retention, and
continuation replacement. Success is established only after those primary
Runtime commits complete.

Runtime attempts at most one terminal lifecycle method (`succeed()`, `fail()`,
or `cancel()`) and calls `attempt_finished()` at most once only after successful
terminalization. Both callbacks receive the same live mutable Attempt; an
observer needing callback-time values must copy them.

The precedence is primary Runtime outcome, then Attempt accounting, then
observer notification. Secondary ordinary `Exception` and
`asyncio.CancelledError` do not replace an established primary failure,
cancellation, or committed success; committed success still returns the exact
`AgentTurn`. There is no wrapper, aggregation, logging, or secondary-error
collection.

Runtime does not broadly catch `BaseException`. A non-cancellation
`BaseException` from lifecycle or observer code is intentionally unsuppressed
and may supersede an active ordinary exception or cancellation during cleanup.
It propagates after committed success as well. If terminalization fails, it is
not retried and no finished callback occurs; Attempt remains RUNNING when its
timestamp acquisition fails.

Callbacks are synchronous and run under `Session.turn()`. Same-Session observed
turns serialize from started through finished, while different Sessions remain
independently concurrent. Runtime supplies no observer-global lock; observers
own their concurrency safety, must keep work bounded, and cannot synchronously
reenter Runtime for the same Session because Session turn coordination is
non-reentrant. Runtime does not roll back observer side effects, and callback
success is not a durability guarantee.

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

An admitted Attempt records the primary Runtime outcome: SUCCEEDED means all
primary Runtime work completed, FAILED means ordinary non-cancellation failure,
and CANCELLED means cancellation. FAILED/CANCELLED do not prove a provider,
filesystem, network, or external side effect did not occur; neither makes retry
or replay safe or idempotent.

## Boundaries

Runtime has no retry, replay, fallback, timeout, deadline, persistence, context
compiler, concrete Evidence record, routing, or Agent-selection policy. One
Runtime call invokes one supplied Agent once. Timeout policy belongs to the
concrete Agent or transport.

Runtime inherits Session's current limitation of one current `ConversationRef`
per `MessageSource`. It does not solve independent continuations for multiple
logical participants sharing a source.

## Dependencies

```text
runtime -> agents
runtime -> context.message
runtime -> context.session
runtime -> evidence
```

Evidence does not depend on Runtime. Runtime has no direct Codex or Persistence
dependency.

## Live Codex acceptance

Opt-in Runtime/Codex acceptance uses an isolated temporary Git repository. The
no-observer path verifies automatic two-turn continuation, same-thread resume,
an exact four-Message History, stable SessionId/time, and read-only write denial.
The observed path verifies a real successful Attempt with exact attribution, the
same live object across callbacks, two-message History, and write denial. This
is acceptance evidence, not a Runtime dependency on Codex.

## Constrained future evolution

Concrete factual Evidence, Attempt persistence, retry policy, turn deadlines,
and routing require separate designs. Session persistence, context compilation,
provider configuration, ConversationRef parsing, and Agent transport behavior
remain outside Runtime ownership.
