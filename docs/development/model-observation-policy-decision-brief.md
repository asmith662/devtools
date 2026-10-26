# Model response and observation failure: decision brief

Status: **recommendation only, not approved or implemented**. Existing
[ADR-0001](../architecture/decisions/ADR-0001-cohesive-model-interaction-boundary.md),
B-0011 and B-0046 retain authority. The five bounded ModelInteraction/Serving P2
repairs leave this behavior unchanged. Original evidence is in the
[audit](../research/model-interaction-and-serving-audit.md) and its exact probes.

## Current ownership and sequence

`LlamaCppInteraction.send` records a start wall instant and occurrence identity,
invokes the provider, normalizes a ModelResponse, and only then constructs a
completed ModelInteractionObservation and invokes an optional observer. The
response has already succeeded at the provider boundary when observation can
fail. A backwards wall instant violates Observation's ordered-interval invariant
before callback entry. A callback can fail after seeing response, usage and
provider identity. Both currently propagate and hide the return value. No retry
or successful Evidence is fabricated.

Runtime retains the admitted input but does not append the assistant response
after this exception; its attempt records invocation failure. It independently
contains terminal attempt-observer errors. These are separate seams. Native
Qwen constructs an unobserved adapter by default, archives its own results and
checks source correspondence before Tool admission. Application records are
not automatic normalized framework Evidence ingestion.

An exception is not proof of model nonentry, zero usage or absent external
effect. Returned-but-unobserved and response-unavailable are different facts.
ModelInteraction response semantics, optional capture outcome and downstream
worker acceptance must remain distinct.

## Option A: explicit post-response exception

Retain error propagation, but define a narrow post-response failure containing
the normalized response and separate observation-failure classification, with
carefully controlled access to occurrence/provider information. No successful
Evidence record is manufactured. The caller may recover the known response and
account for actual returned usage while explicitly recording failed capture.

This preserves a failure-first caller control flow, but changes public exception
shape and requires Runtime/Qwen/application migration. Existing generic retry
handlers could still duplicate a completed request unless explicitly taught
this outcome. Carrying response/prompt-related data on errors also creates
privacy, logging and persistence compatibility obligations. An outcome wrapper
replacing ModelResponse would contradict the current ADR return contract and
would require a separate accepted architectural change; it is not implied by
this option.

## Option B: preserve primary response, report optional capture failure separately

Contain optional completion-observation failure at an explicitly chosen existing
owner/composition boundary, return the already normalized response and make
capture failure independently visible. Unavailable/failed capture remains
unavailable/failed, not successful Evidence. Mandatory evidence requirements can
still refuse downstream acceptance/publication while preserving the known
provider result, rather than pretending the model failed or replaying it.

This keeps `send -> ModelResponse` and better separates result from capture, but
changes today's exception behavior and demands a concrete failure consumer.
Simply catching and discarding observer exceptions would lose important facts
and is not this option. Runtime could retain known assistant output while the
host separately evaluates capture sufficiency. Qwen's unobserved default need
not change; opt-in observed workers need an explicit capture-failure projection.
Usage must preserve observed counts and unknowns, not refund on callback failure.
No automatic retry follows either failure projection.

## Clock representation is a related, separate compatibility decision

Canonical Stopwatch can measure monotonic elapsed time, but cannot by itself
make backwards wall instants satisfy an ordered wall interval or prevent a
callback exception. Options include keeping both observed wall instants with
an explicit clock-adjustment/elapsed claim, or refusing capture while retaining
the known primary response through the selected policy. Neither authorizes
clamping timestamps or representing invented wall order as historical fact.
Observation and Evidence validation/serialization consumers must be inspected
before changing their interval/duration representation. Occurrence identity is
not an InteractionAttempt identity or a retry authorization.

## Recommendation and decision required

Prefer **Option B in principle**, because optional capture should not erase a
known provider result. Approval must first identify the exact existing producer,
failure representation and real durable/operator consumer; specify mandatory
capture admission separately; review privacy/schema compatibility; and preserve
unknown usage and side-effect reconciliation. If that narrow consumer contract
cannot yet be made concrete, Option A is a defensible explicit interim outcome,
with equally explicit non-retry semantics. Neither option is approved here.

Acceptance for a future authorized implementation must independently cover
success, pre-entry refusal, possible-entry transport failure, malformed response,
backwards clock, callback failure, partial capture, known/unknown usage, Runtime
history/attempt correspondence and opt-in Qwen feedback. It must demonstrate
one provider invocation, no Tool dispatch from a failed/unadmitted frame, no
automatic retry/refund, no fabricated Evidence and explicit failed-capture
visibility. It must not introduce a new EventBus, general Agent lifecycle,
persistence store or retry supervisor.
