# Evidence overview

## Purpose

`devtools.evidence` owns factual execution evidence. Its frozen scope contains
two deliberately different forms of evidence:

- `Attempt`, a mutable live lifecycle handle for one application-level Runtime
  processing attempt; and
- `AttemptTerminalEvidence`, an immutable historical value describing one
  terminal outcome of an Attempt.

The package is not a Runtime coordinator, persistence store, telemetry system,
or retry policy engine.

## Public API

```python
from devtools.evidence import (
    Attempt,
    AttemptCancelled,
    AttemptFailed,
    AttemptId,
    AttemptObserver,
    AttemptStage,
    AttemptState,
    AttemptSucceeded,
    AttemptTerminalEvidence,
    AttemptTerminalOutcome,
    EvidenceId,
    EvidenceSink,
)
```

The terminal submodule exports exactly `AttemptCancelled`, `AttemptFailed`,
`AttemptStage`, `AttemptSucceeded`, `AttemptTerminalEvidence`,
`AttemptTerminalOutcome`, and `EvidenceId`.

## Live Attempt lifecycle

`Attempt` is a mutable live handle for one complete Runtime processing attempt,
not merely one `Interaction.send()` call. `AttemptId` identifies that execution
occurrence. An Attempt records its `AttemptId`, `SessionId`, input `MessageId`,
`MessageSource` attribution, `started_at`, lifecycle `state`, and optional
`completed_at`.

```text
RUNNING
|- SUCCEEDED
|- FAILED
`- CANCELLED
```

`succeed()`, `fail()`, and `cancel()` make the one allowed terminal transition
and capture the completion timestamp before mutation. A timestamp failure leaves
the Attempt RUNNING. Attempt uses Python object-identity equality and is
unhashable: two reconstructed live objects with the same `AttemptId` remain
different mutable objects.

`AttemptObserver` is a structural synchronous protocol for this live lifecycle.
It has `attempt_started(attempt)` and `attempt_finished(attempt)` callbacks.
It has no default implementation, registry, persistence, delivery, or
event-stream meaning. It remains distinct from `EvidenceSink`, which receives
immutable historical values rather than the live Attempt.

## Immutable terminal Evidence

`AttemptTerminalEvidence` is an immutable historical factual value. It does not
embed the mutable `Attempt`; it refers to its subject through `AttemptId`.
Its exact fields are:

- `id: EvidenceId`
- `attempt_id: AttemptId`
- `occurred_at: Timestamp`
- `observed_at: Timestamp`
- `outcome: AttemptTerminalOutcome`

The dataclass is frozen, slotted, and keyword-only. It supports direct
reconstruction from those five fields, structural equality, and hashing. This
is intentionally different from live Attempt identity semantics.

`EvidenceId` identifies one immutable Evidence record; `AttemptId` identifies
one execution occurrence. They are distinct semantic identities. The in-memory
value model neither globally enforces one terminal record per Attempt nor
detects differing values built with the same `EvidenceId`. Future producers may
choose stricter cardinality, and future persistence may own immutable-identity
conflict detection.

Terminal Evidence intentionally stores no duplicate `SessionId`, `MessageId`,
or `interaction_source`; those remain attributes of the referenced Attempt. This is
the current value-model boundary, not a commitment to a future storage layout.

## Terminal outcomes and stages

`AttemptTerminalOutcome` is the closed union:

```python
AttemptSucceeded | AttemptFailed | AttemptCancelled
```

`AttemptSucceeded` is an intentionally empty immutable typed value. A success
completed the required Runtime path, so it has no interruption location and no
invented final-success stage.

`AttemptFailed(stage)` and `AttemptCancelled(stage)` each require an
`AttemptStage`. The stage says **where** normal Runtime processing stopped or
was interrupted, never **why**. It is not a failure cause, provider diagnosis,
exception classification, side-effect claim, or retryability signal.

The exact stable stages are:

- `ADMISSION`: the Attempt exists at the observer admission boundary before
  primary Interaction processing; `attempt_started()` can prevent primary processing.
- `CONTINUATION_LOOKUP`: Runtime is obtaining the current continuation before
  Interaction invocation.
- `INTERACTION_INVOCATION`: Runtime has entered Interaction invocation. It makes no claim
  whether a provider or another external system received work or made effects.
- `RESULT_VALIDATION`: Interaction invocation returned and Runtime is checking its
  own result invariant.
- `OUTPUT_RETENTION`: validation succeeded and Runtime is retaining the output
  Message in Session history.
- `CONTINUATION_REPLACEMENT`: output retention succeeded and Runtime is
  replacing a returned non-None continuation.

There are no stages for terminalization, observer completion, Evidence
construction or delivery, persistence, or telemetry export.

## Temporal and producer semantics

`occurred_at` is the terminal Attempt lifecycle occurrence being evidenced.
Runtime supplies the exact successfully terminalized Attempt's `completed_at`;
it is not an exact exception, cancellation-arrival, provider-event, or
external-side-effect timestamp.

`observed_at` is when this immutable record was constructed. `.new()` creates
a fresh `EvidenceId` and captures `observed_at` with `Timestamp.now()`, while
requiring the caller to supply `occurred_at`, `attempt_id`, and `outcome`.

No `observed_at >= occurred_at` validation exists. These wall-clock timestamps
are descriptive values, not causal clocks; sequence and causal-clock concepts
remain deferred.

The value model does not inspect a live Attempt. The authoritative producer
must ensure outcome/state consistency and only construct normal terminal
Evidence after Attempt terminalization succeeds. If terminalization fails and
the Attempt remains RUNNING, normal `AttemptTerminalEvidence` must not be
fabricated. Accounting-failure Evidence is not implemented.

## Runtime production and EvidenceSink

`EvidenceSink` is the frozen synchronous structural protocol:

```python
def accept(self, evidence: AttemptTerminalEvidence) -> None: ...
```

Runtime holds a sink as fixed configuration and offers it only immutable
`AttemptTerminalEvidence`, never Attempt, Session, Message, InteractionTurn,
exceptions, tracebacks, provider payloads, or context dictionaries. A normal
return means the configured consumer accepted responsibility according to its
own contract. It does **not** generically guarantee persistence, durability,
fsync, replication, recoverability, queryability, or eventual export. Concrete
sinks may provide stronger guarantees; the protocol is not a mutable store,
telemetry abstraction, or generic EvidenceRecord API.

Runtime creates an Attempt iff an observer or sink is configured. Attempt
creation remains after `Session.turn()` acquisition and successful input
retention, so lock-wait cancellation and input-retention failure produce no
Attempt, terminal Evidence, callback, or sink delivery. Observer-only Runtime
does not allocate discarded Evidence; bare Runtime creates neither Attempt nor
terminal Evidence.

Runtime is the canonical producer because it owns the Attempt, Runtime-owned
commit boundaries, stage, and terminal disposition. After successful
terminalization it constructs Evidence only when a sink exists, then invokes
`attempt_finished()` when configured, then offers the same immutable object to
the sink. It constructs at most one normal record per Attempt and attempts sink
acceptance at most once; there is no retry or replacement EvidenceId.

The stages are set immediately before their named operations. `ADMISSION`
exists only for observer start admission; `CONTINUATION_REPLACEMENT` exists
only for a returned non-None continuation. They are not mandatory stages.

Ordinary `Exception` and `asyncio.CancelledError` from Evidence construction,
finished notification, or sink acceptance are secondary once the primary
outcome is established. Construction failure still permits finished notification
but leaves no record for the sink; finished failure still permits sink
acceptance. Primary success, failure, or cancellation remains authoritative.
Non-cancellation `BaseException` is unsuppressed: construction stops before
finished/sink, finished stops before sink, and sink propagates immediately.

Normal terminal Evidence requires successful Attempt terminalization. If it
fails and Attempt remains RUNNING, Runtime creates no normal Evidence and calls
neither finished nor sink. All terminalization, construction, callbacks, and
synchronous sink acceptance occur while `Session.turn()` remains held. This
preserves same-Session acceptance order but provides no global cross-Session
order; shared-sink concurrency is sink-owned. A slow synchronous sink can delay
a later same-Session turn and block the event-loop thread, so acceptance is
expected to be bounded synchronous work.

## Experimental execution inspection

**Experimental — retained, submodule-only, process-local, and not frozen.**
`ExecutionInspector` is a non-durable diagnostic consumer for developers
inspecting current-process Runtime executions. It consumes the existing
structural `AttemptObserver` and `EvidenceSink` seams; Runtime has no special
knowledge of it.

Import it explicitly rather than from the Evidence root API:

```python
from devtools.evidence.inspection import ExecutionInspector
```

Its demonstrated configuration is:

```python
inspector = ExecutionInspector()

runtime = Runtime(
    observer=inspector,
    evidence_sink=inspector,
)
```

The inspector retains current-process Attempt diagnostics and terminal Evidence
only. It is not persistent execution history, an audit journal, a durable
Evidence store, a canonical store, a conflict detector, or an integrity
authority.

For discovery, `attempt_ids()` returns a point-in-time tuple of currently
retained `AttemptId` values. It has **no ordering guarantee**: tuple positions
do not indicate execution, chronological, callback, Session, latest, or oldest
order. Callers can inspect a selected execution with `get_attempt(attempt_id)`;
the returned Attempt is the currently retained live object and should be treated
as observational diagnostic state. Its existing `message_id`, `session_id`,
`interaction_source`, and timestamps can help identify an execution.

`get_evidence(evidence_id)` retrieves a currently retained terminal Evidence
record, and `get_evidence_for_attempt(attempt_id)` retrieves currently retained
terminal Evidence records associated with an Attempt. `clear()` discards all
currently retained diagnostic state. There is no automatic retention bound; use
`clear()` or release the inspector when diagnostics are no longer needed. No
cross-thread safety guarantee is provided.

This experimental API and behavior may change as additional diagnostic use
cases are exercised. It remains outside the frozen Evidence root API and does
not change the canonical Evidence architecture.

## Data minimization and exclusions

Terminal Evidence contains semantic identities, timestamps, and typed outcome
and stage values only. It intentionally excludes Message content, prompts,
responses, paths, commands, stdout/stderr, exception text, tracebacks, provider
payloads, credentials, token/cost data, and arbitrary metadata. This is data
minimization, not an encryption or access-control guarantee.

Failure and cancellation do not prove that no external side effect occurred;
in particular, `INTERACTION_INVOCATION` does not establish provider effect status.
Terminal Evidence is factual input for possible future reconciliation, not a
decision that work is safe to retry, should retry, is replayable, or is
idempotent.

Not implemented: `EvidenceRecord` or a generalized hierarchy, Evidence or
Attempt persistence, query APIs, mandatory durability/governance policy,
secondary-error reporting, async sinks, retry/replay and idempotent delivery,
participant identity, cause taxonomies, metadata bags, provenance,
evaluation/governance Evidence, context-compiler Evidence, telemetry adapters,
and durable-workflow integration. `devtools.persistence` does not persist
Attempts or terminal Evidence. Evidence remains independent of OpenTelemetry,
OpenInference, Dapr, and other execution substrates, though future adapters may
consume these immutable values.

## Dependencies and freeze status

Evidence depends on `identity`, `time`, and Context semantic values. Runtime
has a one-way dependency on Evidence; Evidence has no Runtime, Persistence,
Agents, or Codex dependency. The Attempt lifecycle/observer, immutable terminal
Evidence value model, and Runtime-to-terminal-Evidence producer/delivery
boundary are frozen. Future expansion requires a deliberate architectural
reason rather than opportunistic fields, services, or delivery guarantees.
