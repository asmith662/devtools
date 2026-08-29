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
)
```

The terminal submodule exports exactly `AttemptCancelled`, `AttemptFailed`,
`AttemptStage`, `AttemptSucceeded`, `AttemptTerminalEvidence`,
`AttemptTerminalOutcome`, and `EvidenceId`.

## Live Attempt lifecycle

`Attempt` is a mutable live handle for one complete Runtime processing attempt,
not merely one `Agent.send()` call. `AttemptId` identifies that execution
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
event-stream meaning.

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
or `agent_source`; those remain attributes of the referenced Attempt. This is
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
  primary Agent processing; `attempt_started()` can prevent primary processing.
- `CONTINUATION_LOOKUP`: Runtime is obtaining the current continuation before
  Agent invocation.
- `AGENT_INVOCATION`: Runtime has entered Agent invocation. It makes no claim
  whether a provider or another external system received work or made effects.
- `RESULT_VALIDATION`: Agent invocation returned and Runtime is checking its
  own result invariant.
- `OUTPUT_RETENTION`: validation succeeded and Runtime is retaining the output
  Message in Session history.
- `CONTINUATION_REPLACEMENT`: output retention succeeded and Runtime is
  replacing a returned non-None continuation.

There are no stages for terminalization, observer completion, Evidence
construction or delivery, persistence, or telemetry export.

## Temporal and producer semantics

`occurred_at` is the terminal Attempt lifecycle occurrence being evidenced. A
future Runtime producer will normally supply the successfully terminalized
Attempt's `completed_at`; it is not an exact exception, cancellation-arrival,
provider-event, or external-side-effect timestamp.

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

## Runtime boundary

Runtime currently consumes only `Attempt` and `AttemptObserver`. With an
observer configured, it creates an Attempt after turn acquisition and input
retention, calls `attempt_started()` before Agent work, and calls
`attempt_finished()` after successful terminalization. It does **not** currently
construct, emit, deliver, or persist `AttemptTerminalEvidence`.

## Data minimization and exclusions

Terminal Evidence contains semantic identities, timestamps, and typed outcome
and stage values only. It intentionally excludes Message content, prompts,
responses, paths, commands, stdout/stderr, exception text, tracebacks, provider
payloads, credentials, token/cost data, and arbitrary metadata. This is data
minimization, not an encryption or access-control guarantee.

Failure and cancellation do not prove that no external side effect occurred;
in particular, `AGENT_INVOCATION` does not establish provider effect status.
Terminal Evidence is factual input for possible future reconciliation, not a
decision that work is safe to retry, should retry, is replayable, or is
idempotent.

Not implemented: Runtime-to-terminal-Evidence production, `EvidenceSink`,
`EvidenceRecord`, Evidence or Attempt persistence, query APIs, retry/replay
relationships, participant identity, cause taxonomies, metadata bags,
provenance, evaluation/governance Evidence, context-compiler Evidence, and
telemetry or durable-workflow integration. Evidence remains independent of
OpenTelemetry, OpenInference, Dapr, and other execution substrates, though a
future adapter may consume these immutable values.

## Dependencies and freeze status

Evidence depends on `identity`, `time`, and Context semantic values. Runtime
has a one-way dependency on Evidence; Evidence has no Runtime, Persistence,
Agents, or Codex dependency. The Attempt lifecycle/observer and immutable
terminal Evidence value-model concepts are frozen. Future expansion requires a
deliberate architectural reason rather than opportunistic fields or services.
