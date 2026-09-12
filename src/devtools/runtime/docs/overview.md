# Runtime

## Purpose

`Runtime` is a configuration-bearing but interaction-stateless coordination
service that applies one caller-selected `Interaction` interaction to one mutable
`Session`. Its only retained configuration is an optional fixed
`AttemptObserver` and optional fixed `EvidenceSink`; it owns no retained
interaction or provider state. `Session` owns retained `History` and current
continuation references, while an `Interaction` owns response and provider behavior.

```text
Message          one contextual utterance
Session          retained mutable interaction state
Interaction      asynchronous responder contract
Runtime          one-interaction coordinator
```

Runtime is provider-neutral. [Codex](../../interactions/providers/codex/docs/overview.md) is a real
acceptance implementation, not a Runtime dependency.

## Public API

```python
from devtools.runtime import Runtime

runtime = Runtime()
# Or: runtime = Runtime(observer=observer, evidence_sink=evidence_sink)
turn = await runtime.send(
    session=session,
    interaction=interaction,
    message=message,
)
```

`Runtime` is the complete root public API. `runtime.observer` and
`runtime.evidence_sink` are readable fixed configuration with types
`AttemptObserver | None` and `EvidenceSink | None`; no replacement or per-send
override API exists. Runtime has no identity, lifecycle, lock, retained Session,
retained Interaction, continuation, last result, current Attempt, current Evidence,
or other interaction state.

## Coordination algorithm

`Runtime.send()` performs one `Interaction.send()` invocation in this order:

1. Acquire `session.turn()`.
2. Record the supplied input `Message` once.
3. Retrieve the current continuation with
   `session.conversation_for(interaction.source)`.
4. Invoke `Interaction.send()` exactly once.
5. Validate that the returned Message source equals `interaction.source`.
6. Record the returned Message.
7. Store the returned continuation when it is non-`None`.
8. Return the original `InteractionTurn`.
9. Release `session.turn()`.

The complete operation is held inside `session.turn()`, including the awaited
Interaction call. Runtime never directly constructs History or mutates the public
conversation mapping.

## Optional Attempt observation and terminal Evidence

Runtime creates an Attempt iff either configured capability requires it:

| Observer | Evidence sink | Attempt | Terminal Evidence |
|---|---|---|---|
| absent | absent | no | no |
| configured | absent | yes | no discarded record |
| absent | configured | yes | produced and offered |
| configured | configured | yes | produced and offered |

Attempt creation remains after Session turn acquisition and successful input
retention. Waiting cancellation and input-retention failure therefore create no
Attempt, terminal Evidence, callback, or sink delivery. `attempt_started()` is
the conditional `ADMISSION` boundary before primary processing. An Attempt
spans continuation lookup, Interaction invocation, returned-source validation, output
retention, and replacement of a returned non-None continuation.

Runtime owns terminal Evidence stage attribution. It sets the frozen stages
immediately before their named operations: `ADMISSION` before start observation
when an observer exists, `CONTINUATION_LOOKUP` before lookup,
`INTERACTION_INVOCATION` before `Interaction.send()`, `RESULT_VALIDATION` before Runtime
validation, `OUTPUT_RETENTION` before output retention, and
`CONTINUATION_REPLACEMENT` before replacement. Stages record where processing
stopped or was interrupted, not why; admission and replacement are conditional,
not mandatory state-machine steps.

After all successful Runtime-owned commits, Runtime calls `Attempt.succeed()`.
After primary ordinary failure or cancellation it calls `fail()` or `cancel()`
with the current stage represented in immutable terminal Evidence. Normal
Evidence requires successful terminalization. If terminalization fails and
Attempt remains RUNNING, Runtime creates no normal Evidence and calls neither
finished nor sink.

When a sink is configured, Runtime constructs at most one
`AttemptTerminalEvidence` after terminalization, using exact
`Attempt.completed_at` as `occurred_at`; `.new()` owns its EvidenceId and
`observed_at`. Observer-only Runtime does not allocate a discarded record.
Then, in operational order, Runtime invokes `attempt_finished(live Attempt)`
and offers the same immutable record once to `EvidenceSink.accept()`. Runtime
does not retry construction or acceptance, and does not create replacement
Evidence after delivery failure.

Ordinary `Exception` and `asyncio.CancelledError` from construction, finished,
or sink acceptance are secondary after primary outcome establishment. They do
not replace committed success, primary failure, or original cancellation.
Construction failure still permits finished notification but cannot reach the
sink; finished failure still permits sink acceptance. A non-cancellation
`BaseException` remains unsuppressed: construction stops before finished/sink,
finished stops before sink, and sink propagates immediately. Suppressed
secondary errors have no separate reporting channel in this milestone.

All terminalization, construction, callbacks, and synchronous sink acceptance
run inside `Session.turn()`. Same-Session acceptance therefore follows turn
order; Runtime introduces no global lock between Sessions, and shared-sink
concurrency is sink-owned. A slow sink can delay a next same-Session turn and
block the event-loop thread, so bounded synchronous sink work is assumed.

`EvidenceSink.accept()` means only that the configured consumer accepted its
immutable record under its own contract. It does not generically mean
persistence, durability, fsync, replication, recoverability, queryability, or
remote export. A policy requiring durable Evidence as a condition of operation
success requires separate future architecture.

## Messages and Interaction selection

The caller explicitly supplies the Interaction. Runtime does not route, discover,
rank, substitute, or fall back between Interactions.

Any valid `Message` may be submitted to any Session. Runtime is role-neutral:
it does not require a USER input or an ASSISTANT output. Input source identifies
the producer of the Message and need not equal the selected Interaction source.

Runtime records the supplied Message exactly once after turn acquisition. The
same exact Message may be submitted again; each invocation records another
occurrence without cloning, deduplicating, retry classification, or MessageId
regeneration. Such repetitions are factual repeated submission, not a retry or
replay model.

## Continuations and validation

Runtime retrieves continuations only through Session's source-keyed API and
trusts Session's continuation/source invariant. It also trusts InteractionTurn's
continuation/message-source invariant and provider-specific continuation
syntax.

Runtime uniquely knows both the selected Interaction and returned InteractionTurn, so it
validates:

```python
turn.message.source == interaction.source
```

On mismatch, Runtime raises `ValueError` before recording returned state. The
input remains retained, while the returned Message and continuation are not
committed.

On success, Runtime records the returned Message before replacing continuation
state. Continuation state therefore cannot advance beyond the History entry
that produced it. A returned `conversation=None` performs no update and does
not clear an existing Session continuation. Runtime returns the original
`InteractionTurn`; it defines no Runtime-specific result model.

## Concurrency

Runtime relies on Session-owned complete-turn coordination:

```text
same Session object       complete Runtime turns serialize
different Session objects Runtime operations may proceed concurrently
```

This scope covers the awaited Interaction call. For the same source, if turn A reads
ref A and returns ref B, a turn B queued while A is in flight receives ref B
when it eventually invokes its Interaction. This prevents stale continuation use.

Runtime owns no global lock and imposes no generic lock on a shared Interaction
instance; concrete Interactions own their own concurrency guarantees. Runtime
inherits Session coordination boundaries: they are object-local,
single-event-loop, and in-process. They do not synchronize event loops,
threads, separately reconstructed objects with equal Session IDs, processes,
or distributed workers.

## Failures and cancellation

If `Interaction.send()` raises, Runtime retains the already-recorded input, records
no output, leaves the current continuation unchanged, releases Session
coordination, and propagates the original exception unchanged. Runtime does not
distinguish transport, provider, or parsing failure phases and creates no error,
status, or informational Messages.

Cancellation while waiting to acquire `session.turn()` leaves Session unchanged:
input is not recorded and Interaction is not called. Cancellation while the Interaction is
in flight leaves the retained input, commits no output or continuation update,
releases Session coordination, and propagates cancellation. Interaction transport
cleanup belongs to the concrete Interaction.

Runtime coordination is forward-only, not transactional. It does not roll back
an earlier Session mutation if a later local operation unexpectedly fails.

An admitted Attempt records the primary Runtime outcome: SUCCEEDED means all
primary Runtime work completed, FAILED means ordinary non-cancellation failure,
and CANCELLED means cancellation. FAILED/CANCELLED do not prove a provider,
filesystem, network, or external side effect did not occur; neither makes retry
or replay safe or idempotent.

## Boundaries

Runtime has no retry, replay, fallback, timeout, deadline, persistence, context
compiler, routing, or Interaction-selection policy. One Runtime call invokes one
supplied Interaction once. It does not persist Attempts or Evidence, export telemetry,
or integrate Dapr/durable workflows. Failure/cancellation stages make no
provider-side-effect, retry-safety, idempotency, or replayability claim.
Timeout policy belongs to the concrete Interaction or transport.

Runtime inherits Session's current limitation of one current `ConversationRef`
per `MessageSource`. It does not solve independent continuations for multiple
logical participants sharing a source.

## Dependencies

```text
runtime -> interactions
runtime -> context.message
runtime -> context.session
runtime -> evidence
```

Evidence does not depend on Runtime. Runtime has no direct Codex, Persistence,
telemetry, or workflow dependency.

## Live Codex acceptance

Opt-in Runtime/Codex acceptance uses an isolated temporary Git repository. The
no-observer path verifies automatic two-turn continuation, same-thread resume,
an exact four-Message History, stable SessionId/time, and read-only write denial.
The observed path verifies a real successful Attempt with exact attribution, the
same live object across callbacks, two-message History, and write denial. This
is acceptance evidence, not a Runtime dependency on Codex.

## Constrained future evolution

`EvidenceRecord`, durable Evidence sinks/persistence, Attempt persistence,
mandatory durability policy, async sinks, secondary-error reporting, retry,
replay, idempotent delivery, provenance, telemetry adapters, and durable
workflow infrastructure require separate designs. Session persistence, context
compilation, provider configuration, ConversationRef parsing, and Interaction
transport behavior remain outside Runtime ownership.
