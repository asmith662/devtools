# Runtime Evidence Governance: Attempts, Records, Delivery, and Replay

## Disposition

Status: Partially reconciled

Canonical research subject: Runtime Evidence governance, occurrence records, delivery, and replay.

Related ADRs: ADR-0001.

Implemented evidence: narrow InteractionAttempt lifecycle and immutable terminal Evidence.

Accepted: live execution objects differ from historical Evidence; Evidence is not authority, trace, telemetry, or workflow truth.

Deferred: complete failure observation, generalized correlation, durable Evidence storage, replay material, retry/reconciliation, and schema evolution.

Rejected for now: generic event envelopes, causal taxonomy, provenance graph, workflow history engine, and generic Trace/Telemetry infrastructure.

Superseded or refined findings: current taxonomy supplies the established Evidence boundary.

Open questions: durable delivery, independent record persistence, and side-effect certainty.

Revisit triggers: a concrete consumer requiring durable records, ordered delivery, replay, or reconciliation.

Reconciliation basis: ADR-0001; taxonomy; observability and execution documentation.

## Problem formulation and executive conclusion

The architectural problem is not, fundamentally, “how should a failed `Attempt` carry better diagnostics?” It is:

> **How should a runtime preserve durable, typed, falsifiable statements about what happened during an execution without turning those statements into control state, telemetry, policy conclusions, or an prematurely general event system?**

That distinction matters. The future consumers you describe—retry/replay, provenance, persistence, evaluation, context compilation, governance, and self-improvement—need historical facts with different semantics from the live state used to coordinate an execution. They will also eventually need to distinguish an **execution occurrence** from the **records describing that occurrence**, and both from later **assessments or decisions derived from those records**.

This separation appears repeatedly in adjacent systems. W3C PROV distinguishes activities, entities, agents, and relationships among them rather than collapsing provenance into the mutable object being observed. OpenLineage similarly gives a run its own identity while emitting multiple distinct observations about that run. CloudEvents explicitly defines an event as a data record expressing an occurrence and notes that one occurrence can produce more than one event. OpenTelemetry distinguishes a live `Span`, which can be modified during an operation, from immutable events attached to it. citeturn14search0turn19view1turn19view0turn14search1

**Established finding.** These systems differ substantially, but there is strong cross-domain precedent for separating **the thing that happens** from **immutable records concerning what happened**. There is equally strong precedent for keeping execution identity separate from event/record identity. citeturn14search0turn19view0turn19view1

**Architectural inference.** Your foundational concept is best understood as an **execution journal of immutable observation records**. It is *not* yet event sourcing, because Session state is not being reconstructed from Evidence. It is *not* merely distributed tracing, because sampling or exporter loss must eventually be unacceptable for some governance/recovery uses. It is *not* an audit log in the narrow security sense, because it may represent operational provenance and reproducibility facts. And it is not yet a general provenance graph.

The clean conceptual separation is:

```text
                     LIVE EXECUTION PLANE
                     ====================

 Message ──> Session ──> Runtime ──> Agent
                        │
                        │ owns execution boundaries
                        ▼
                    Attempt
            mutable live lifecycle handle
              RUNNING -> terminal


                    HISTORICAL FACT PLANE
                    =====================

             Runtime / boundary owner
                        │
                        │ observes facts
                        ▼
              immutable Evidence records
                        │
                        ▼
                 Evidence recorder
                        │
             ┌──────────┴──────────┐
             ▼                     ▼
          memory now          journal later


                    DERIVED-KNOWLEDGE PLANE
                    =======================

   retry decisions / evaluations / governance / context usefulness
                         │
                         └── reference EvidenceIds,
                             AttemptIds, artifact identities
```

The key rule is that the bottom plane does **not rewrite the middle plane**. An evaluation saying “this context selection was poor,” or a retry policy saying “this operation is safe to retry,” is a conclusion based on evidence—not a mutation of the facts that produced that conclusion.

### Executive conclusion

**Final architectural verdict: implement the next slice, but with material modifications. Do not implement `AttemptOutcomeEvidence` exactly as proposed, and do not replace the overall architecture.**

The broad direction is sound:

- retain `Attempt` as a small mutable **live execution handle**;
- introduce separately identified immutable factual records;
- have Runtime create facts about boundaries that Runtime itself observes;
- keep storage outside Runtime;
- keep Evidence strongly typed;
- keep delivery failures secondary to already-established application outcomes.

But four parts of the proposed next model should change **before freezing it**.

| Proposed decision | Verdict | Why |
|---|---|---|
| Mutable `Attempt` plus immutable Evidence | **Keep** | These have legitimately different semantics. |
| `EvidenceId` separate from `AttemptId` | **Keep** | One attempt will eventually have many records; event identity and subject identity are different concepts. |
| `AttemptOutcomeEvidence` with success/failure/cancellation | **Modify** | A terminal attempt record is a good first fact, but cancellation and failure need boundary/stage information. |
| `AGENT / VALIDATION / SESSION / OBSERVATION` as failure *categories* | **Replace conceptually** | These describe **where normal progress stopped**, not why the underlying failure happened. |
| Only `observed_at` | **Modify** | Preserve occurrence time separately from observation/record time. |
| No terminal Evidence if Attempt terminalization fails | **Keep for the normal terminal record, but add accounting for the gap** | Do not fabricate a terminal fact inconsistent with the live Attempt; also do not silently erase an invariant/accounting failure. |
| `AttemptObserver` + `EvidenceSink` | **Keep conceptually** | Live lifecycle hooks and historical fact delivery are different seams. |
| Synchronous sink initially | **Accept with a strict bounded/nonblocking contract** | Fine for the first vertical slice; do not imply synchronous durable I/O under the Session lock. |
| Flat causal failure taxonomy | **Do not build** | Runtime generally does not know root cause; provider/tool-specific layers may. |
| Append-only evidence persistence | **Adopt eventually** | Historical fact mutation is semantically dangerous; retention/deletion policy remains a separate concern. |

The most consequential correction is this:

> **`AGENT`, `VALIDATION`, `SESSION`, and `OBSERVATION` are not failure causes. They are execution boundaries or stages.**

That is not merely naming pedantry. `SESSION` currently combines a continuation lookup *before* Agent execution with output retention or continuation replacement *after* Agent execution. Those cases have radically different retry implications. A failure before calling `Agent.send()` establishes that that invocation could not have produced provider/tool effects; a failure after the Agent has returned establishes no such thing. Durable workflow systems emphasize precisely this distinction: an activity can execute or partially execute before the orchestrator records completion, and retry safety therefore depends on idempotency or explicit execution records rather than a generic “failed” status. citeturn15search1turn15search4turn15search8turn18search0

My recommended first immutable fact is therefore closer to **`AttemptTerminatedEvidence`** or **`AttemptOutcomeEvidence` with corrected semantics**:

```text
AttemptTerminalEvidence
├── id: EvidenceId
├── attempt_id: AttemptId
├── occurred_at: Timestamp
├── observed_at: Timestamp
└── outcome:
    ├── Succeeded
    ├── Failed
    │   └── stage: AttemptStage
    └── Cancelled
        └── stage: AttemptStage
```

with a stage model based on actual Runtime boundaries, not guessed causes:

```text
ADMISSION
CONTINUATION_LOOKUP
AGENT_INVOCATION
RESULT_VALIDATION
OUTPUT_RETENTION
CONTINUATION_REPLACEMENT
```

The exact names can be adjusted to your vocabulary, but the semantics should be frozen before the names.

Crucially, **do not add a generic causal `reason` field yet**. A Runtime-level `AGENT_INVOCATION` record says where control failed. It does not tell you whether the provider timed out, a tool failed, a socket broke after a remote commit, model parsing failed inside an Agent, or application code raised. Those are lower-level observations owned by whichever layer can actually know them.

## Findings from provenance, tracing, journals, workflows, lineage, and evaluation systems

The adjacent systems are useful chiefly because their differences reveal which semantics belong in your core and which should not be imported.

| System or field | Useful lesson | What not to copy |
|---|---|---|
| **W3C PROV** | Separate activities, entities, agents, usage, generation, derivation, and responsibility. This gives a strong conceptual basis for treating an Attempt as an activity-like occurrence, Messages/artifacts as entity-like things, and future provenance relations as explicit edges. citeturn14search0 | Do not introduce RDF, ontologies, bundles, or a generic provenance graph before you have consumers requiring those relations. |
| **CloudEvents** | An event is a record expressing an occurrence; a single occurrence may yield multiple events. Event identity is distinct from subject/context identity. CloudEvents also separates event context from domain data. citeturn19view0 | A generic interoperable event envelope and arbitrary payload are broader than your current domain requires. |
| **OpenTelemetry tracing** | A span represents a live operation and is mutable until ended; events are immutable; identity/context survive separately. Links exist where simple parent/child structure is insufficient. citeturn14search1 | OTel's status, arbitrary attributes, sampling, exporter semantics, and observability focus are not strong enough to be the authoritative governance journal. |
| **OpenTelemetry logs** | Event time and observation time are genuinely different concepts: `Timestamp` means when the event occurred, while `ObservedTimestamp` means when the collection system observed it. citeturn14search2 | Do not import a generic log body, severity, or attributes dictionary into Evidence. |
| **Temporal** | Durable execution depends on an append-only event history; replay works because previously recorded facts are authoritative. Activities may execute multiple times, so side-effecting work must be made idempotent or otherwise controlled. citeturn15search4turn15search10turn15search1 | Do not turn your current Runtime into a deterministic workflow engine merely to make Evidence durable. |
| **Event sourcing / journals** | Append-only event streams commonly give each event its own ID and maintain stream ordering/revision; state may be reconstructed by replay. citeturn17search2turn17search3turn17search9 | Calling something an “event” does not mean you should event-source Session or Runtime state. |
| **OpenLineage** | A Run has its own stable identity and emits multiple distinct state observations over time; input/output lineage is built from those observations. citeturn19view1 | Its extensible “facet” mechanism is intentionally broad; an equivalent arbitrary extension facility would undermine your narrow typed domain. |
| **in-toto** | A typed statement explicitly binds a claim to a subject and identifies the schema/predicate type. This is a strong model for later evaluation or artifact attestations. citeturn19view2turn16search1 | “Attestation” imports stronger notions of claim authority/authentication than your Evidence records currently guarantee. |
| **SLSA provenance** | Reproducibility/provenance benefits from distinguishing declared inputs from resolved immutable dependencies and from recording run-specific execution details. citeturn16search2 | Supply-chain provenance contains build-specific semantics that should not enter generic Runtime Evidence. |
| **MLflow** | Evaluation/training systems associate results with run identity, datasets, digests, sources, metrics, and artifacts; those are naturally downstream records around an execution rather than a single generic outcome. citeturn16search3turn16search5 | Metrics, tags, arbitrary metadata, and experiment-management concerns should not define your Evidence core. |

### The most important pattern: occurrence identity is not record identity

CloudEvents' conceptual terminology is unusually relevant here: an **occurrence** is a statement-of-fact-worthy thing happening in a system, while an **event** is a record expressing an occurrence and its context; one occurrence may produce multiple events. citeturn19view0

OpenLineage makes almost the same distinction operationally: a Run identifies an execution occurrence, while multiple `RunEvent`s are distinct observations of different run-state transitions. citeturn19view1

**Project recommendation.** That maps almost exactly to:

```text
AttemptId  = identity of the execution occurrence
EvidenceId = identity of one immutable statement about it
```

Therefore the cardinality should be assumed from day one to be:

```text
Session
   1
   │
   └─── * Attempt

Attempt
   1
   │
   └─── * EvidenceRecord
```

Even when the first implementation happens to produce exactly one Evidence record per terminal Attempt, **do not encode 1:1 cardinality into the model or database**.

### The second important pattern: live operational objects and historical records are different

OpenTelemetry is particularly instructive. A Span represents an operation and can acquire attributes, events, status, and end time while it is active; after it ends those aspects are no longer mutable. Its attached Events are independently immutable. citeturn14search1

That is not proof that your `Attempt` should imitate a Span. It does show that there is nothing architecturally suspicious about a mutable lifecycle object coexisting with immutable occurrence records.

**Architectural inference.** The right distinction is not “mutable bad, immutable good.” It is:

- mutable state is appropriate for **what is currently happening**;
- immutable records are appropriate for **what has already been observed to have happened**.

Your `Attempt` is therefore defensible provided it stays small and is not later treated as the durable historical record.

### The third important pattern: durable execution needs more than “failed”

Temporal's Event History is not merely debugging telemetry. The service records lifecycle events so executions can recover after crashes, and replay compares execution commands with previously recorded history. Temporal also explicitly warns that Activities may execute more than once and should be idempotent. citeturn15search4turn15search10turn15search1

Likewise, AWS's discussion of idempotent APIs identifies the classic ambiguity: after a request times out, the caller may not know whether the remote operation executed, so a retry may duplicate an external effect. gRPC goes so far as to document that `DEADLINE_EXCEEDED` can be returned even where a state-changing operation ultimately completed successfully. citeturn18search0turn18search2

This is the strongest evidence against treating:

```text
FAILED
CANCELLED
```

as replay semantics.

They are **control outcomes**, not claims about the external world.

### The fourth important pattern: provenance relationships should be explicit but late

W3C PROV's core relations—use, generation, communication/informing, derivation, association with agents—demonstrate that provenance becomes useful through specific semantic relations, rather than through one generic parent pointer. citeturn14search0

That suggests a future progression like:

```text
Attempt A used Artifact X
Attempt A generated Message Y
Evaluation E assessed Evidence Z
ContextCompilation C used FileSnapshot F
Attempt B was retry-of logical Operation O
```

But it does **not** justify building a generic graph today.

A `parent_evidence_id`, `related_to`, or arbitrary edge-property dictionary is deceptively cheap at first and expensive semantically: every consumer then has to infer what the edge means. Strong provenance models instead give important relations explicit names. citeturn14search0

### The fifth important pattern: evidence transport is not evidence semantics

OpenTelemetry's failure-handling specification deliberately prioritizes preserving application behavior over preserving telemetry, directing SDKs not to propagate exporter failures into application operation and encouraging separate self-diagnostics for telemetry-pipeline problems. citeturn19view3

That strongly supports your instinct that an Evidence delivery failure **after successful committed Runtime work must not transform that work into an apparent Runtime failure**.

But there is a boundary to the analogy: governance-grade Evidence may eventually be more important than ordinary observability telemetry. At that point durability has to become an explicit contract rather than an accidental property of a sink. The core record model should allow that transition without making durability mandatory today.

## Critique of `Attempt`, terminal Evidence, failure semantics, and time

### `Attempt` should remain—but its role should be narrowed conceptually

I would **not remove `Attempt` now**.

It performs a legitimate job that an immutable record does poorly: it is the live object representing the lifecycle of one Runtime execution while that execution is underway. It gives your observer admission and completion hooks a shared identity and gives Runtime a finite state machine it can terminalize.

Its strengths are substantial:

- stable semantic `AttemptId`;
- immutable attribution;
- very small lifecycle state;
- one-way state transitions;
- no provider payload, diagnostic dictionary, retry machinery, or policy;
- a clear distinction between object identity and semantic `AttemptId`;
- no claim that failure implies absence of remote effects.

Those choices are compatible with the better adjacent models.

There are, however, three semantic rough edges worth documenting before further freezing.

**Attempt existence is currently conditional on an observer.** That makes Attempt simultaneously an execution concept and an instrumentation artifact. Once immutable Evidence can be configured independently, Runtime must at least create an Attempt whenever either `AttemptObserver` **or** Evidence recording is enabled. Otherwise an Evidence record has no Attempt identity to reference.

I would **not yet require Runtime to allocate an Attempt on every turn when neither facility is enabled**. There is no durable consumer of the invisible identity. The narrow change is enough:

```text
create Attempt when:
    observer configured
    OR
    evidence recorder configured
```

A future durable-execution layer may justify making execution identity unconditional.

**The Attempt begins after input retention.** According to the frozen sequence, an input-retention failure happens before the Attempt exists. Therefore `Attempt` does not literally represent every failure that can occur after Runtime accepts the turn; it represents the processing occurrence beginning after successful input retention. That is acceptable, but it should be stated as a semantic boundary rather than leaving “one complete application-level Runtime processing attempt” ambiguous.

I would not move that boundary yet. Moving Attempt creation earlier changes observer admission behavior and makes a previously Session-only failure part of Attempt semantics without demonstrated need.

**`message_id` needs a frozen semantic interpretation.** In the current shape it should be documented explicitly as the input/request Message identifier to which this Attempt is attributed. Do not later overload it to mean “the message relevant to this execution.” Output identity should be its own future fact/reference if a consumer needs it.

### `AttemptOutcomeEvidence` is close to the right first fact, but its payload is not ready to freeze

A terminal outcome is a sensible first immutable fact because Runtime already has all the information necessary to produce it and because the record does not require provider inspection.

The variants:

```text
Succeeded
Failed
Cancelled
```

are fundamentally reasonable.

They represent distinct terminal dispositions. Cancellation deserves first-class representation rather than being treated as generic failure; mature RPC and workflow systems likewise distinguish cancellation from failure/error states. citeturn18search2turn15search4

What should change is the information attached to the non-success variants.

The proposed:

```text
AttemptFailed(category=SESSION)
```

answers neither of the two questions a future consumer actually asks:

1. **Where in Runtime did normal execution cease?**
2. **Why did the underlying operation fail?**

Those are different dimensions.

### Observation location and causal reason must not be conflated

Consider three examples.

```text
continuation lookup raises
```

Runtime knows:

```text
normal progress stopped during CONTINUATION_LOOKUP
Agent.send was never entered
```

It might or might not know the deeper reason. Perhaps Session state is corrupt; perhaps custom code raised unexpectedly. That cause is not needed to describe the observed Runtime boundary.

Now consider:

```text
Agent.send raises
```

Runtime knows:

```text
normal progress stopped during AGENT_INVOCATION
```

It does **not** generically know:

```text
network failed
provider rejected request
tool had side effect then raised
model failed
Agent implementation had a bug
```

Finally:

```text
Agent returns
output retention raises
```

Runtime knows the Agent invocation completed and that normal progress subsequently stopped during `OUTPUT_RETENTION`. Calling this merely `SESSION` loses the fact most relevant to replay: Agent execution has already occurred.

**Recommendation:** replace `AttemptFailureCategory` with something explicitly locational, such as:

```text
AttemptStage
```

or:

```text
AttemptFailureStage
```

I slightly prefer `AttemptStage`, because cancellation also needs it.

A minimal set reflecting your current Runtime boundaries is:

| Stage | Meaning |
|---|---|
| `ADMISSION` | The `attempt_started()` admission callback prevented Agent processing from beginning. |
| `CONTINUATION_LOOKUP` | Runtime failed obtaining the continuation before invoking Agent. |
| `AGENT_INVOCATION` | Normal progress ceased while `Agent.send()` was executing. |
| `RESULT_VALIDATION` | Agent returned, but Runtime rejected its result under a Runtime-owned invariant. |
| `OUTPUT_RETENTION` | Agent returned and validation passed, but retaining the output failed. |
| `CONTINUATION_REPLACEMENT` | Output retention occurred, but continuation replacement failed. |

This is more verbose than four coarse categories, but the distinctions correspond to *real control boundaries already present in Runtime*, not speculative taxonomy.

`ADMISSION` is preferable to `OBSERVATION`. A failure in `attempt_finished()` is also an observation failure, but it occurs after the Attempt outcome is established and must not turn the Attempt into `FAILED`. Calling the start-hook category `OBSERVATION` therefore conflates two operationally different cases.

Similarly, `SESSION` should disappear from the terminal taxonomy because it spans both pre-Agent and post-Agent phases.

### Do not add a causal hierarchy now

A hierarchical model such as:

```text
AGENT
  PROVIDER
    NETWORK
      TIMEOUT
    RATE_LIMIT
  TOOL
    ...
```

would be premature and, more importantly, would assign causal authority to the wrong layer.

The generic Runtime does not inspect provider/network/tool/model sub-causes. That is a good architectural boundary. Lower layers can later emit their own typed facts.

OpenTelemetry's semantic conventions follow a comparable separation between an operation's structural context and typed error information; mature network APIs similarly expose an `UNKNOWN` condition when sufficient causal detail is unavailable rather than manufacturing precision. citeturn18search2

So the initial model should contain **location without claimed root cause**.

Later, an Agent or provider integration might emit, for example:

```text
ProviderCallFailed
├── provider_call_id
├── attempt_id
├── provider
├── reason: ProviderFailureReason
└── ...
```

That should not cause Runtime to mutate:

```text
AttemptFailed(stage=AGENT_INVOCATION)
```

The two records express compatible facts at different abstraction levels.

### Cancellation needs a stage too

The proposed empty `AttemptCancelled` throws away useful information.

Cancellation while:

```text
CONTINUATION_LOOKUP
```

is different from cancellation during:

```text
AGENT_INVOCATION
```

and different again from cancellation while performing post-Agent Session mutation.

The correct minimal union is therefore conceptually:

```text
AttemptTerminalOutcome

Succeeded

Failed
└── stage: AttemptStage

Cancelled
└── stage: AttemptStage
```

This gives cancellation exactly the same epistemic discipline as failure: **where cancellation interrupted the attempt, without claiming what external effects did or did not occur**.

### Side-effect certainty should not be stuffed into the first fact

It is tempting to add:

```text
external_effects:
    NONE
    POSSIBLE
    KNOWN
    UNKNOWN
```

That would be useful to retries, but the Runtime often cannot truthfully populate it.

If `CONTINUATION_LOOKUP` fails, Runtime does know that this Attempt did not enter `Agent.send()`. But it cannot generally assert there were no *other* side effects from a Session implementation.

Once `Agent.send()` has been entered, a raised exception or cancellation says very little about remote effects. Distributed systems explicitly have ambiguous completion states: a timeout can occur even when a state-changing remote operation succeeded, and durable execution frameworks therefore rely on idempotency/reconciliation rather than equating error with non-execution. citeturn18search0turn18search2turn15search8

**Recommendation:** do not add generic `external_effects` to the first terminal record.

Instead, preserve the boundary facts now. When actual retry/replay behavior is introduced, add effect facts at the component capable of observing them, such as:

```text
ToolInvocationStarted
ToolInvocationCompleted
ProviderRequestAccepted
ExternalOperationReceiptObserved
```

or explicit idempotency identities.

The absence of such evidence must mean **unknown**, not “no effect.”

### Outcome must never imply retryability

A future consumer must not be allowed to implement:

```text
if attempt.outcome == FAILED:
    retry()
```

as a semantically supported rule.

The correct model is:

```text
facts
    │
    ▼
retry/reconciliation policy
    │
    ├── operation semantics
    ├── idempotency capability
    ├── execution stage
    ├── effect evidence
    ├── prior attempts
    └── current external state
    │
    ▼
decision
```

A retry decision is derived governance state, not Evidence.

### The temporal model needs both occurrence and observation time

`observed_at` is a meaningful concept, but it should not be the only timestamp on terminal Evidence.

OpenTelemetry's log data model explicitly distinguishes:

- source/event `Timestamp`: when the event occurred;
- `ObservedTimestamp`: when the collection system observed it. citeturn14search2

For your terminal record there is an obvious event time:

```text
Attempt.completed_at
```

That is when the live Attempt reached terminal state.

The Evidence object is constructed afterward, at:

```text
observed_at
```

These may be separated by only microseconds today, but they answer different questions and may diverge much more once buffering, recovery, imports, or remote observations exist.

Therefore:

```text
AttemptTerminalEvidence
├── occurred_at      # the terminal lifecycle occurrence
└── observed_at      # when Runtime formed this evidence record
```

is stronger than only `observed_at`.

I would retain **`observed_at`**, rather than rename it to `ingested_at`. Runtime is the observing component; ingestion belongs to a later storage pipeline. A database may additionally assign a persistence timestamp, but that should be storage metadata, not necessarily a field in every domain record.

### Do not introduce causal clocks or domain sequence numbers yet

Today:

- one Session object serializes turns;
- one Runtime execution creates one terminal fact;
- all relevant local boundaries happen on one event loop.

There is no present need for Lamport clocks, vector clocks, distributed timestamps, or a causal DAG.

When an Evidence journal exists, a storage-local monotonic:

```text
journal_sequence
```

is useful for deterministic scans/checkpointing. Event stores commonly distinguish immutable event identity from sequential stream/global positions. citeturn17search9turn17search3

That storage sequence is not the same thing as semantic causal order.

If one Attempt later emits several evidence records whose ordering must survive independent transport, then a source-issued per-Attempt ordinal may become justified. Do not add it before then.

### Terminalization failure is a special accounting failure, not a normal outcome

Your proposed rule:

> no terminal Evidence unless Attempt terminalization succeeded

is correct **for the normal terminal Evidence record**.

If the live Attempt still says `RUNNING`, publishing:

```text
AttemptSucceeded
```

would create contradictory authoritative representations.

But the rule is incomplete if terminalization failure can actually occur. It would leave no record explaining why an execution that had reached a result has a permanently running Attempt.

The strongest design is:

1. make lifecycle terminalization an extremely small, internally controlled, effectively infallible transition;
2. test its invariant rigorously;
3. if it nevertheless raises, treat this as an **internal accounting/invariant failure**, not as an ordinary `AGENT`, `SESSION`, or `VALIDATION` outcome;
4. report it via independent Runtime self-diagnostics;
5. only promote it to a formal Evidence type if it becomes an operational condition consumers actually need to query.

Do **not** try to record `EvidenceRecordingFailed` through the same Evidence recorder that just failed. OpenTelemetry's guidance to separate telemetry self-diagnostics from application telemetry is directly relevant to avoiding that recursion. citeturn19view3

So Attempt-lifecycle failure *can* conceptually be evidence, but it should **not be part of the first domain slice** unless your current implementation really has a nontrivial way for terminalization to fail.

## Identity, creation, delivery, persistence, and schema evolution

### `EvidenceId` is the right identity model

An independently generated semantic `EvidenceId` per factual record is a strong decision.

It gives you:

- unambiguous record identity;
- deduplication;
- foreign-key/reference targets;
- future causal/provenance references;
- a way to distinguish retransmission of the same fact from creation of a new fact;
- storage identity independent of the Attempt being described.

CloudEvents likewise gives an event its own identity and treats source-plus-ID as the uniqueness boundary for distinct events; OpenLineage gives the Run identity independently of its successive observations. citeturn15search6turn19view1

For your single local library, a semantic `EvidenceId` can be globally unique by project convention; there is no need to introduce CloudEvents' `source + id` composite identity unless records begin crossing independently administered producers.

The distinction should be frozen as:

```text
AttemptId
    answers:
    "which execution occurrence?"

EvidenceId
    answers:
    "which historical record?"
```

A future retry system probably needs a *third* identity:

```text
OperationId
    answers:
    "which logical operation are these executions attempting?"
```

That future cardinality is likely:

```text
OperationId
    │
    ├── AttemptId A
    │       ├── EvidenceId 1
    │       └── EvidenceId 2
    │
    └── AttemptId B
            ├── EvidenceId 3
            └── EvidenceId 4
```

Do not add `OperationId` until retry/replay becomes a real consumer.

### Evidence should be an immutable identified record, not a mutable entity

The most precise characterization is:

> An Evidence item is an **immutable, append-only, independently identified observation record**.

“Entity” is too suggestive of mutable CRUD lifecycle.

“Value object” is not quite right either, because two otherwise identical observations with different `EvidenceId`s can legitimately represent distinct record occurrences.

“Event” is technically appropriate—CloudEvents explicitly describes events as records of occurrences—but may accidentally suggest that your architecture is now event sourced. citeturn19view0

I would therefore keep the public domain word **Evidence**, while describing persisted collections as an **Evidence journal** and individual objects as **Evidence records**.

### Typed closed payloads are preferable to arbitrary `kind + payload`

For the Python domain, your instinct is correct.

Prefer:

```text
AttemptTerminalEvidence(
    outcome = Failed(stage=RESULT_VALIDATION)
)
```

over:

```text
Evidence(
    kind="attempt_failed",
    payload={
        "category": "validation",
        ...
    }
)
```

The latter pushes invariant checking into every reader and allows semantically meaningless combinations to enter the journal.

The strongest pattern from in-toto is not “use a JSON dictionary”; it is the separation of a stable statement/subject structure from an explicitly identified **typed predicate schema**. Its test-result predicate, for example, defines a concrete result vocabulary rather than making every consumer interpret arbitrary keys. citeturn19view2turn16search1

For your Python model, a closed tagged union is probably preferable to a deep inheritance hierarchy:

```text
AttemptTerminalOutcome =
    AttemptSucceeded
  | AttemptFailed
  | AttemptCancelled
```

There is no need for open subclass registration.

At the serialization/storage boundary, a discriminator is still useful:

```text
kind = "attempt_terminal"
schema_version = 1
```

That does **not** require exposing `kind + dict` as the domain model.

### Do not build a giant common Evidence envelope

It is reasonable for all Evidence records eventually to share:

```text
EvidenceId
```

and perhaps:

```text
observed_at
```

but resist deciding today that every record must also have:

```text
session_id
attempt_id
actor
trace_id
parent_id
correlation_id
tenant
source
schema
metadata
tags
...
```

CloudEvents needs a general envelope because it solves cross-platform transport interoperability. Your domain has a much narrower purpose. citeturn19view0

Let the second and third Evidence types demonstrate which fields are truly universal before freezing a broad base class.

### Runtime is the correct producer of Runtime-boundary Evidence

Evidence should be created by the component with first-hand semantic knowledge.

Runtime knows:

- when Agent invocation is entered;
- whether Agent returned normally;
- whether Runtime validation rejected the result;
- which Session operation it was performing;
- whether observer admission blocked execution;
- when it successfully terminalized the Attempt.

Therefore Runtime should construct the terminal Attempt Evidence.

The sink must **not** infer the stage from exception types. That would reverse the dependency: storage infrastructure would begin interpreting Runtime semantics.

Likewise, Runtime should not infer provider-specific facts. Provider/tool/Agent layers should later produce records they uniquely know.

This is analogous to provenance systems attributing activity and responsibility at the component that knows the relationship, rather than asking the persistence backend to reconstruct semantics after the fact. citeturn14search0

### `AttemptObserver` and Evidence delivery are properly separate—but `AttemptObserver` is really a lifecycle hook

The proposed separation is sound:

```text
AttemptObserver
    live mutable lifecycle interaction

Evidence recorder/sink
    immutable fact delivery
```

The caveat is that `AttemptObserver` is not observational in the ordinary telemetry sense because `attempt_started()` is an **admission gate**: its failure prevents Agent execution.

That is a legitimate semantic hook; its name is merely softer than its actual authority.

Because that API is frozen, I would not rename it solely for aesthetic reasons. Document the admission semantics explicitly.

The Evidence receiver, by contrast, should never become an admission hook merely because it is synchronous. Recording a terminal fact happens after the primary operation's outcome is established.

### A synchronous Evidence seam is reasonable only under a narrow contract

A synchronous protocol is the smallest implementation:

```text
record(evidence) -> None
```

That is acceptable today if its contract says effectively:

> `record()` is expected to perform bounded local work and must not imply durable remote delivery.

The concern is not synchronization itself. The concern is that Runtime currently holds `Session.turn()` throughout the turn. A future synchronous sink that performs network or slow durable I/O would therefore extend Session serialization for an observability/storage concern.

OpenTelemetry similarly treats span completion as an application hot-path concern and separates recording from exporter processing; its broader error-handling rules also seek to prevent telemetry infrastructure from destabilizing application execution. citeturn14search1turn19view3

So:

```text
Now:
Runtime -> synchronous recorder -> in-memory/test/bounded local handling
```

is fine.

But do not freeze a requirement that:

```text
Runtime -> synchronous remote database/network backend
```

is the durability model.

### Evidence-recording failure should remain secondary

Your stated policy is correct:

> Evidence recording failure must not turn a successfully committed Runtime operation into an apparent application failure.

Otherwise the caller may reasonably retry the application operation and duplicate effects merely because accounting failed. Distributed-system guidance around ambiguous outcomes and idempotency shows why this is dangerous. citeturn18search0turn18search7

But a suppressed Evidence failure must not be *silent*.

The recorder layer should eventually expose independent self-diagnostics such as:

```text
record failures
dropped record count
queue depth
last durable sequence
last exporter error
```

OpenTelemetry expressly recommends this kind of separate self-diagnostic reporting when telemetry machinery suppresses its own errors. citeturn19view3

There is an unavoidable logical limitation:

```text
Evidence sink is unavailable
        │
        ▼
"record EvidenceSinkUnavailable to same sink"
        │
        ▼
still unavailable
```

Therefore **evidence loss is not reliably represented by another ordinary Evidence record in the same channel**.

### Delivery guarantees should evolve explicitly

There are at least three possible contracts:

```text
BEST EFFORT
Runtime outcome does not wait for durable evidence.

JOURNALED
Runtime does not return until the terminal Evidence
has reached a local durable journal.

ADMISSION-JOURNALED
selected execution facts are durably recorded before
potentially side-effecting work is allowed to begin.
```

Only the first is justified now.

The other two become valuable when Evidence itself participates in crash recovery or governance. Durable workflow systems make their execution histories integral to progress precisely because recovery depends on those histories. citeturn15search4turn15search10

Do not add a configurable durability enum yet. There is no implementation behind it and no consumer specifying which guarantee it needs.

Also recognize a hard limit: because current Session mutation is in-memory/nontransactional and Agent may cause arbitrary external effects, there is no general transaction capable of atomically committing:

```text
Session mutation
+
external provider/tool side effect
+
Evidence persistence
```

No Evidence interface can manufacture exactly-once semantics across those boundaries. Systems that tolerate retries use idempotency, durable checkpoints, reconciliation, or explicitly controlled side-effect boundaries instead. citeturn15search8turn18search0turn18search1

### Evidence should eventually persist independently of Session snapshots

Session snapshots and Evidence answer different questions.

```text
Session snapshot:
"What semantic conversation state exists now?"

Evidence journal:
"What execution observations occurred over time?"
```

Putting the journal inside Session serialization would couple a current-state representation to a growing historical record, increase snapshot size, and make retention/evolution of Evidence unnecessarily dependent on Session persistence.

Use semantic foreign identities:

```text
SessionId
AttemptId
MessageId
EvidenceId
```

to connect the two domains without embedding one in the other.

### A minimal normalized SQLite shape

When persistence is actually built, I would start with three narrow relations rather than a generic JSON event table:

| Relation | Minimal purpose |
|---|---|
| `attempt_subject` | Immutable attribution needed to understand an `AttemptId` after Python objects disappear. |
| `evidence_record` | Common journal identity, type/version, timestamps, and ordering metadata. |
| `attempt_terminal_evidence` | Typed columns for the first Evidence payload. |

Conceptually:

```text
attempt_subject
────────────────────────────────────────────
attempt_id            PRIMARY KEY
session_id
input_message_id
agent_source
started_at


evidence_record
────────────────────────────────────────────
journal_sequence      UNIQUE / storage order
evidence_id            PRIMARY KEY
attempt_id             FOREIGN KEY
kind
schema_version
occurred_at
observed_at


attempt_terminal_evidence
────────────────────────────────────────────
evidence_id            PRIMARY/FOREIGN KEY
disposition            SUCCEEDED|FAILED|CANCELLED
stage                   nullable iff SUCCEEDED
```

Two aspects are intentional.

First, **do not persist the live mutable Attempt by repeatedly updating `state`** if the goal is an immutable journal. Persist an immutable Attempt subject/header and derive terminal state from its terminal record.

Second, do not use:

```text
payload_json TEXT
```

as an excuse to bypass the typed schema. A JSON serialization can exist for interchange, but normalized SQLite can enforce the invariants of the initial known fact.

The `attempt_subject` row solves a subtle problem in the proposed design: if Evidence stores only `attempt_id`, but `Attempt` itself is never persisted, an Evidence record recovered after restart cannot tell you which Session, Message, or Agent source that Attempt referred to.

You have three long-term choices:

```text
A. duplicate attribution in every Evidence record
B. persist an immutable Attempt subject once
C. make an Attempt-start record part of the journal
```

**B is the smallest normalized persistence design.**

Do not implement it in the current no-persistence slice; simply avoid designing terminal Evidence under an assumption that its referenced Attempt will always remain a live Python object.

### Append-only should be a semantic guarantee, not a promise of eternal storage

Evidence should be append-only from the application model's perspective:

```text
insert record
never mutate its historical assertion
```

Append-only event journals are a standard event-sourcing pattern. citeturn17search2turn17search3

But “append-only” must not mean “legally or operationally impossible to delete.” Evidence can contain sensitive information, and retention policies may require deletion or redaction.

The useful rule is:

> **No ordinary application UPDATE changes what an Evidence record claims. Administrative retention, physical deletion, or migration is a separate storage-governance operation.**

A tombstone is not always enough for privacy; event-store documentation illustrates that logically deleted/tombstoned data may remain physically present until later compaction/scavenging. citeturn17search6

Cryptographic hash chains, signatures, transparency logs, and tamper-evident ledgers are therefore **not implied by immutability**. Add them only if you later require adversarial audit integrity.

### Schema evolution belongs at the record boundary

Every persisted record type should eventually have a schema version.

A practical discipline is:

```text
same semantic meaning + additive compatible field
    -> compatible schema evolution

incompatible interpretation
    -> new schema version or new record kind

new independent fact
    -> new Evidence type
```

in-toto similarly identifies predicate schemas explicitly, and one of its runtime-trace specifications requires a type-version change for backward-incompatible changes. citeturn19view2turn16search8

Do not rewrite old records merely to make them resemble new records. Readers can adapt old versions into current in-memory models where that is semantics-preserving.

And an old reader should not silently guess the meaning of a future incompatible Evidence type. Failing explicitly is preferable to constructing a false historical interpretation.

## Retry, replay, provenance, context compilation, evaluation, governance, and security

### Retry/replay reveals which future facts actually matter

The minimum long-term retry model is not “Attempt has better error codes.”

It eventually needs to distinguish at least:

```text
logical operation
    │
    ├── requested inputs / identity
    ├── operation semantics
    ├── execution attempts
    │      ├── where each attempt progressed
    │      ├── outputs observed
    │      └── effect/idempotency evidence
    │
    └── reconciliation/retry decisions
```

Durable systems make similar distinctions between a logical activity/workflow and individual executions or retries. Temporal explicitly notes that an Activity may execute more than once, and AWS durable-execution guidance distinguishes execution semantics for retryable idempotent work from operations with non-idempotent external effects. citeturn15search1turn15search20turn18search1

The likely future identities are therefore:

```text
OperationId     logical intended operation
AttemptId       one physical/application-level execution
EvidenceId      one immutable record
```

The first retry slice should introduce `OperationId` only when Runtime or a higher-level coordinator actually supports retries. Adding it now would be speculation.

### Facts required for genuinely safer replay

When replay becomes real, consumers are likely to need:

| Fact | Why it matters |
|---|---|
| Logical operation identity | Groups physical Attempts intended to accomplish the same thing. |
| Stable input identity or digest | Determines whether the retried operation is actually the same request. |
| Agent/runtime/code version identity where relevant | Replaying changed code can alter behavior. Durable replay systems explicitly constrain code changes because saved history must remain interpretable. citeturn18search17turn15search10 |
| Attempt stage/boundaries | Distinguishes work that never entered Agent from work that did. |
| Output/result identity | Determines whether a result was produced/committed. |
| Idempotency key or effect identity | Lets external systems deduplicate re-execution. Idempotency tokens are a standard mechanism for making repeated mutating calls safe. citeturn18search0turn18search7 |
| External receipt/reconciliation evidence | Resolves cases where the caller did not observe completion. |
| Checkpoint/commit facts | Prevents replaying already-durable progress. |

None of that justifies adding provider request IDs, model parameters, token counts, or tool details to the generic terminal record now.

### The precise meaning of “effects unknown”

A safe future interpretation of the recommended stages would be:

| Terminal location | What Runtime can establish |
|---|---|
| `ADMISSION` | This Runtime did not enter `Agent.send()`. |
| `CONTINUATION_LOOKUP` | This Runtime did not enter `Agent.send()`. |
| `AGENT_INVOCATION` failure/cancellation | Agent execution was entered; external effect state is **not established by Runtime**. |
| `RESULT_VALIDATION` | Agent returned; whatever Agent/provider/tool activity occurred has already happened. Its exact effect state is not established by Runtime. |
| `OUTPUT_RETENTION` | Same, plus Runtime reached post-validation Session mutation. |
| `CONTINUATION_REPLACEMENT` | Agent returned and output was retained; continuation update subsequently failed. |

This alone is far more useful for future recovery than `SESSION`.

Notice that these are facts about **control progression**, not a replay policy.

### Provider-specific facts should stay provider-specific

Generic Evidence should not grow fields such as:

```text
http_status
provider_request_id
finish_reason
prompt_tokens
completion_tokens
rate_limit_bucket
tool_call_json
vendor_error_type
```

merely because they may one day be diagnostically useful.

Those belong in:

- provider-specific Evidence record types;
- provider tracing/observability;
- usage/accounting domains;
- separately governed raw artifacts.

A generic Runtime record can reference such facts later by `EvidenceId` without owning their schema.

The same principle applies to exception payloads. Runtime may factually know that `Agent.send()` raised; preserving the exception message, traceback, provider body, and local variables is a separate security-sensitive diagnostic capability.

### Provenance should grow from typed relationships, not a generic graph

W3C PROV provides the right conceptual vocabulary: activities use entities, generate entities, may be informed by other activities, and are associated with responsible agents. citeturn14search0

For this project, the future mapping could be:

```text
Attempt                    ~ activity occurrence
Message / source snapshot  ~ entity
Agent definition/source    ~ responsible agent-like identity
Context compilation        ~ activity
Evaluation                 ~ activity producing an assessment entity
```

But this should remain a **conceptual mapping**, not an imported ontology.

When a real consumer arrives, introduce the narrowest relation necessary:

```text
ContextCompilation used FileSnapshot
AgentAttempt used CompiledContext
AgentAttempt generated Message
Evaluation assessed Attempt/Evidence
```

A generic:

```text
EvidenceRelation(source, target, relation: str, metadata: dict)
```

would be exactly the kind of premature graph abstraction your constraints rightly seek to avoid.

### Context compilation should produce immutable artifacts and provenance facts, not inflate Attempt Evidence

The future context compiler has much richer provenance needs than an Attempt terminal record:

```text
repository identity
commit / filesystem snapshot identity
files considered
regions retrieved
retrieval method/version
ranking result
selected regions
compaction/transformation
final compiled context
```

SLSA provenance's distinction between parameters and resolved immutable dependencies, and MLflow's use of dataset source plus digest, both support the broader pattern of identifying the actual resolved input material rather than merely recording a mutable location/name. citeturn16search2turn16search5

A future compiler should therefore likely produce something conceptually like:

```text
CompiledContextArtifact
├── id
├── digest
└── ...

ContextCompilationEvidence
├── compilation_id
├── selected source refs
├── source snapshot identities/digests
└── output artifact ref
```

Then:

```text
AttemptUsedContext
├── attempt_id
└── compiled_context_id
```

can connect it to execution.

Do not put file lists, rankings, source excerpts, and relevance scores into `AttemptOutcomeEvidence`.

### Evaluation should remain a separate derived domain

An evaluation such as:

```text
"output passed unit tests"
"answer grounded in cited context"
"context region X was useful"
"agent version B outperformed A"
```

is not the same epistemic category as:

```text
"Attempt A terminated at time T"
```

The in-toto test-result model is instructive because it treats a test invocation/result as a specifically typed statement about a subject, while MLflow separately tracks evaluations, datasets, metrics, and artifacts around runs. citeturn16search1turn16search3

Recommended direction:

```text
factual execution Evidence
          │
          ▼
EvaluationRun
          │
          ├── inputs: EvidenceIds / ArtifactIds / AttemptIds
          ├── evaluator identity/version
          └── results
```

Whether evaluation results themselves later qualify as “Evidence” is mostly nomenclature. If you choose to put them in the Evidence domain, they should remain explicitly typed observations with source/evaluator identity—not mutable truth fields attached to an Attempt.

### Governance should consume evidence, not live inside it

Likewise:

```text
retry allowed
agent should be promoted
context source should be suppressed
policy violation occurred
```

are conclusions whose validity can change when policy or evaluation methodology changes.

Historical Evidence should instead preserve the facts used to reach them.

This gives you a very important future property:

```text
same historical evidence
       +
new governance policy
       =
re-evaluable decision
```

without rewriting the past.

That is exactly why provenance is useful for later trust and quality assessment: W3C PROV frames provenance as information about entities, activities, and responsible agents that can subsequently support assessments, rather than itself being the assessment. citeturn14search0

### Security and privacy argue strongly for your narrow core

The proposed refusal to add arbitrary provider payloads, exceptions, prompts, commands, or metadata is architecturally valuable, not just aesthetically clean.

OpenTelemetry's current security guidance explicitly recommends data minimization and avoiding unnecessary sensitive attributes. OWASP's logging guidance calls out access tokens, credentials, sensitive personal data, session identifiers, secrets, and even file paths as data that should often be omitted, masked, sanitized, hashed, or specially protected. citeturn17search0turn17search1

Core Evidence should therefore default to things like:

```text
semantic IDs
typed enumerations
timestamps
versioned artifact references
content digests where appropriate
explicit low-sensitivity provenance links
```

rather than:

```text
raw prompt
raw model response
shell command
stdout/stderr
exception traceback
environment variables
full filesystem path
HTTP headers
provider response body
credentials
tool arguments
```

Those richer artifacts may sometimes be necessary for debugging or research, but they should have a separate storage/security policy.

CloudEvents likewise warns against putting sensitive information into event context attributes because intermediaries may introspect or log them. citeturn19view0

There is another subtle risk: **Evidence makes data more linkable**. A harmless-looking stable SessionId, MessageId, repository path, provider request ID, and user identifier can become much more sensitive once joined into a long-lived execution history.

So future Evidence persistence needs:

- explicit access control;
- retention limits;
- encryption appropriate to its sensitivity;
- data minimization at collection time;
- tenant/security-boundary awareness where relevant;
- separate policy for raw artifacts;
- an ability to delete sensitive retained data despite application-level append-only semantics. citeturn17search0turn17search1

### What explicitly should not be Evidence

At least initially, the following should remain outside the core Evidence domain:

| Information | Why |
|---|---|
| Arbitrary logger messages | Unstructured narrative is not a stable factual schema. |
| Arbitrary metadata dictionaries | They destroy semantic control and make every consumer defensive. |
| Retry recommendations | Policy conclusion, not historical fact. |
| “Safe to replay” | Derived conclusion requiring operation semantics/effect evidence. |
| Agent quality score | Evaluation result, not Runtime execution fact. |
| Current policy decision | Mutable governance state. |
| Raw exception/traceback | Diagnostic artifact with privacy/security/versioning concerns. |
| Provider request/response payload | Provider-specific and potentially highly sensitive. |
| Token/cost accounting | Separate usage/accounting domain unless a concrete Evidence consumer proves otherwise. |
| Prompt/output bodies | Already belong to Message/artifact domains; references are preferable. |
| Arbitrary source files/context contents | Use immutable artifact references/digests and a dedicated context provenance model. |
| Mutable “latest explanation” or root-cause field | Root-cause analysis is revisable; historical facts should not mutate when hypotheses change. |

## Recommended target model and alternatives considered

### Recommended target architecture

The target model I would freeze toward is a **two-plane execution-journal architecture**.

```text
┌──────────────────────────────────────────────────────────────┐
│                         Runtime                              │
│                                                              │
│  acquire Session.turn                                        │
│      │                                                       │
│  retain input                                                │
│      │                                                       │
│  create Attempt if observer OR evidence recording enabled    │
│      │                                                       │
│  observer admission ─────────────── stage: ADMISSION          │
│      │                                                       │
│  continuation lookup ────────────── stage: CONTINUATION       │
│      │                                                       │
│  Agent.send ─────────────────────── stage: AGENT_INVOCATION   │
│      │                                                       │
│  validate ───────────────────────── stage: RESULT_VALIDATION  │
│      │                                                       │
│  retain output ──────────────────── stage: OUTPUT_RETENTION   │
│      │                                                       │
│  replace continuation ───────────── stage: CONT_REPLACEMENT   │
│      │                                                       │
│  terminalize Attempt                                         │
│      │                                                       │
│      ├──── mutable lifecycle ───────> Attempt                 │
│      │                                RUNNING -> terminal     │
│      │                                                       │
│      └──── immutable observation ──> AttemptTerminalEvidence  │
└──────────────────────────────────────────────┬───────────────┘
                                               │
                                               ▼
                                     Evidence recorder
                                               │
                           secondary failures only
                                               │
                      ┌────────────────────────┴───────────┐
                      ▼                                    ▼
               in-memory/tests                    journal later
```

The core type-level concepts should be:

```text
Attempt
    live execution handle
    mutable only for lifecycle
    not historical source of truth

EvidenceId
    semantic identity of one immutable record

AttemptTerminalEvidence
    one immutable terminal observation

AttemptTerminalOutcome
    Succeeded
    Failed(stage)
    Cancelled(stage)

AttemptStage
    Runtime-owned execution boundary vocabulary

EvidenceRecorder / EvidenceSink
    delivery seam only
    no persistence semantics implied
```

Whether you retain the exact name `AttemptOutcomeEvidence` or choose `AttemptTerminalEvidence` is less important than its semantics. I slightly prefer **`AttemptTerminalEvidence`** because it emphasizes that this is the factual terminal observation rather than an open-ended diagnostic description of “outcome.”

### Why `Succeeded / Failed / Cancelled` remains appropriate

There is no strong evidence for replacing these top-level variants with a more elaborate universal status code set.

They answer a narrow Runtime question:

```text
Did this Attempt reach normal success,
terminate due to failure,
or terminate due to cancellation?
```

That is sufficiently stable.

Do not add:

```text
TIMED_OUT
REJECTED
ABORTED
PARTIAL
UNKNOWN
```

until the Runtime itself has those lifecycle states.

Timeout, for example, may currently appear as an Agent failure/cancellation depending on the Agent implementation. Promoting provider-specific timing behavior into generic Attempt lifecycle would violate your existing boundary.

### Alternative: eliminate `Attempt` and use events only

A pure event model might emit:

```text
AttemptStarted
AttemptSucceeded
AttemptFailed
AttemptCancelled
```

and derive all state from the event sequence.

Advantages:

- one historical representation;
- natural persistence/reconstruction;
- no mutable Attempt object;
- easy audit trail.

Costs:

- your observer admission API currently wants a live object;
- Runtime would need event-state reconstruction even for in-process lifecycle behavior;
- the whole design starts moving toward event sourcing;
- crash/durability semantics immediately become central;
- the currently simple `Attempt` FSM becomes distributed across journal interpretation.

This is the right design for some workflow engines, but Temporal obtains the benefits only because its Event History is durable and authoritative for execution recovery. citeturn15search4turn15search10

**Verdict: reject for now.** It removes a useful small object in exchange for infrastructure you do not currently need.

### Alternative: make `Attempt` itself the immutable final record

Another design would keep a mutable builder during execution, then “freeze” it and persist the whole final Attempt:

```text
Attempt
├── id
├── attribution
├── timestamps
├── final outcome
├── diagnostics
└── ...
```

OpenTelemetry Span lifecycle has some superficial similarity: a Span is live and mutable until `End`, after which it stops changing. citeturn14search1

This would simplify identity—one Attempt, one record—but it becomes progressively worse once:

```text
Attempt has many observations
provider facts arrive independently
evaluations reference specific facts
context provenance is appended later
accounting records arrive asynchronously
```

You then either mutate the supposedly historical Attempt or create a giant final envelope.

**Verdict: reject.** Your existing small Attempt is healthier.

### Alternative: generic `Event(kind, payload)` from day one

Advantages:

- trivial extensibility;
- easy JSON;
- storage has one table;
- plugin-like consumers can invent new kinds freely.

Costs:

- schemas move out of Python's type system;
- invariants become convention;
- unknown metadata becomes permanent;
- every consumer handles malformed combinations;
- privacy review becomes much harder;
- the “Evidence” domain quietly becomes a logging/event-bus substrate.

CloudEvents intentionally takes a general-envelope approach because interoperability across unrelated systems is its objective. citeturn19view0

That is not your objective.

**Verdict: reject internally.** A CloudEvents adapter might be useful later at an interoperability boundary.

### Alternative: W3C PROV-style generic provenance graph now

Advantages:

- academically and semantically mature;
- naturally supports arbitrary provenance;
- would serve future context compilation and governance.

Costs:

- enormous increase in abstraction;
- generic Entity/Activity/Agent vocabulary overlaps your domain terminology;
- relationship/query complexity arrives before consumers;
- graph identity and ontology/versioning concerns distract from the one fact you can currently observe reliably.

W3C PROV itself deliberately distinguishes a small core from extended provenance structures. citeturn14search0

**Verdict: use as a conceptual north star, not an implementation dependency.**

### Alternative: OpenTelemetry as the Evidence system

There is an attractive mapping:

```text
Attempt       ~= Span
AttemptId     ~= SpanId
session       ~= trace/grouping context
failures      ~= Span events/status
Evidence      ~= events/log records
```

Advantages:

- mature ecosystem;
- standard tracing identities and links;
- existing exporters/backends;
- strong operational tooling.

But OTel's core objective is observability, and its own error-handling contract explicitly accepts losing telemetry rather than changing application behavior. citeturn19view3

Governance/replay Evidence may eventually require non-sampled, reconstructable, domain-specific durability.

**Verdict: provide an exporter/bridge later, not semantic ownership.**

### Alternative: immediately build a durable Temporal-like execution history

This would provide the strongest future replay foundation:

```text
AttemptScheduled
AttemptStarted
AgentInvocationStarted
AgentInvocationCompleted
SessionCommit...
```

with deterministic replay.

But durable workflow history only works because workflow engines control execution, checkpointing, retry, deterministic replay, and side-effect boundaries as a coherent system. Temporal's history is foundational to its execution semantics, not a passive observability feature. citeturn15search4turn15search10

Your Runtime explicitly does **not** own retry, routing, transactional Session persistence, distributed coordination, or provider side effects.

**Verdict: stop far short of this today.** Preserve enough identity and fact semantics that you could grow in this direction without pretending you already have durable execution.

## Implementation sequence, frozen-boundary changes, unresolved questions, and final verdict

The architecture favors small freezeable slices. That discipline is particularly important here because “Evidence” can easily become a dumping ground for every future concern.

### Recommended next slice

The next independently auditable slice should contain **only terminal Runtime Evidence and its delivery seam**.

Its semantic scope should be:

```text
EvidenceId
AttemptTerminalEvidence
AttemptTerminalOutcome
AttemptStage
EvidenceRecorder/EvidenceSink
Runtime construction/delivery
```

with these invariants:

```text
Evidence is immutable.

EvidenceId has semantic value identity.

AttemptId identifies the subject execution;
EvidenceId identifies the record.

Succeeded carries no stage.

Failed carries the exact Runtime stage at which normal
processing ceased.

Cancelled carries the exact Runtime stage at which
processing was interrupted.

No stage claims root cause.

occurred_at is the Attempt terminal time.

observed_at is when Runtime constructs the record.

A normal terminal Evidence record exists only after
Attempt terminalization succeeds.

Recorder failure cannot replace an established Runtime
success/failure/cancellation.

Recorder failure has independent self-diagnostic handling,
not recursive Evidence delivery.

Runtime creates Attempt when either live observation or
Evidence recording is configured.
```

That is still a very small slice.

### Runtime boundary mapping should be exhaustive

The most important tests are not serialization tests; they are control-boundary tests.

The audit should prove at least:

| Runtime path | Expected terminal evidence |
|---|---|
| Observer admission raises | `Failed(ADMISSION)` |
| Continuation lookup raises | `Failed(CONTINUATION_LOOKUP)` |
| Agent raises | `Failed(AGENT_INVOCATION)` |
| Agent invocation cancelled | `Cancelled(AGENT_INVOCATION)` |
| Agent returns invalid source | `Failed(RESULT_VALIDATION)` |
| Output retention raises | `Failed(OUTPUT_RETENTION)` |
| Continuation replacement raises | `Failed(CONTINUATION_REPLACEMENT)` |
| Entire turn succeeds | `Succeeded` |
| `attempt_finished()` fails after successful Attempt | Attempt outcome unchanged; evidence still represents established outcome |
| Evidence recorder fails after successful Attempt | Runtime result unchanged; self-diagnostic path exercised |
| Attempt terminalization fails | no normal terminal Evidence; invariant/accounting failure surfaced separately |

This boundary table is more valuable than an elaborate causal exception taxonomy because it encodes semantics Runtime can actually guarantee.

### What to build after that

The following slices should remain independent and freezeable.

**Evidence self-diagnostics and delivery discipline.** Define exactly how suppressed recorder errors are reported and provide a trivial deterministic in-memory recorder for tests. Keep the record path bounded. Do not add background queues merely for abstraction.

**Persistence.** Introduce the immutable Attempt attribution/header plus append-only Evidence journal and first type-specific payload table. Add `schema_version`, storage-local journal sequence, deterministic serialization, uniqueness constraints, and duplicate-ID conflict checks.

At this point, an insertion retry using the same `EvidenceId` should be idempotent: the same ID and same content can be treated as the same record, while the same ID with different content is corruption. Event-store systems use stable event IDs precisely to support idempotent appends/deduplication. citeturn17search3turn17search13

**Durability policy only when required.** Decide whether terminal Evidence must be durable before Runtime returns. This decision cannot be derived from architecture taste; it depends on whether recovery/governance consumers require lossless records.

**Retry identity and effect evidence.** When retry/replay is actually introduced, add logical operation identity, idempotency semantics, input/version fingerprints, and facts from effecting components. Do not make `AttemptId` serve simultaneously as both logical operation and physical execution identity.

**Artifact/provenance primitives.** When the context compiler or reproducibility work begins, introduce immutable artifact/source-snapshot identities and only the explicit provenance relationships needed by those consumers.

**Evaluation/governance.** Add assessment/evaluation records that reference historical identities rather than extending core Attempt outcomes.

### What not to build yet

Do **not** build:

- a generic `Evidence(kind, metadata: dict)` container;
- a universal event envelope;
- an Evidence plugin registry;
- a provenance graph database;
- generic arbitrary causal edges;
- parent/child Evidence trees without a use case;
- `OperationId` before actual retries exist;
- provider/tool failure taxonomy in Runtime;
- exception serialization;
- prompt/output duplication inside Evidence;
- token/cost telemetry as generic Evidence;
- cryptographic event chaining;
- digital signatures or attestations;
- distributed sequence/consensus;
- Lamport/vector clocks;
- Kafka/event-bus infrastructure;
- asynchronous sink abstractions before blocking delivery becomes a real problem;
- a generic storage backend interface before the second storage implementation justifies one;
- deterministic replay of Runtime;
- event sourcing of Session;
- automatic retries;
- compensation/Saga infrastructure;
- context-compiler Evidence types before the compiler's first real provenance consumer;
- mutable “root cause,” “usefulness,” or “safe to retry” conclusions.

The adjacent systems show that every one of those concepts can eventually be useful. They do **not** show that importing them early is beneficial.

### Specific changes to the already-frozen `Attempt`

I do **not** recommend a breaking structural change to `Attempt`.

Keep:

```text
AttemptId
SessionId
MessageId
agent_source
started_at
state
completed_at
RUNNING -> SUCCEEDED|FAILED|CANCELLED
```

Keep diagnostics, provider payload, output MessageId, retry relationship, and arbitrary metadata out of it.

Make only semantic/documentation clarifications:

**`Attempt` is the live execution handle, not the historical evidence record.**

**Its `message_id` denotes the input Message to which the Attempt is attributed.**

**Its lifecycle begins after successful input retention under the current Runtime integration.** Therefore an input-retention failure is outside Attempt semantics.

**Its terminal state says nothing about absence of external effects.**

Those clarifications are enough to stop downstream consumers from assigning it stronger semantics than it possesses.

If you have flexibility despite the “frozen” label, the one field name I would have preferred from first principles is `input_message_id` rather than `message_id`; however, I do not think that improvement justifies breaking a frozen public API if documentation can make the semantics exact.

### Specific changes to Runtime integration

Runtime does need a small change once Evidence recording exists.

The construction condition should become:

```text
Attempt required when observer is configured
OR Evidence recording is configured.
```

It should not remain “Attempt exists only if observer exists,” because that would make the new Evidence seam accidentally dependent on the old observation seam.

Runtime should explicitly track its current semantic processing stage around existing control boundaries. This is not telemetry state or retry behavior; it is simply how Runtime constructs a truthful terminal record.

Terminal processing should conceptually be ordered as:

```text
primary Runtime path establishes outcome
        │
        ▼
Attempt terminalization
        │
        ├── fails:
        │      no normal terminal Evidence
        │      report invariant/accounting failure
        │
        └── succeeds:
               construct immutable terminal Evidence
                       │
                       ├── live finish observer
                       │
                       └── Evidence recorder
```

The observer-finish callback and recorder must each be handled so one secondary channel does not prevent the other from being attempted.

There is no reason to couple Evidence construction to exception introspection beyond determining cancellation versus ordinary failure and knowing which Runtime boundary was active.

### A compact decision register for the required architectural questions

| Issue | Decision |
|---|---|
| Mutable Attempt vs immutable Evidence | **Sound separation.** |
| Should Attempt exist? | **Yes, as live lifecycle handle; no, not as historical source of truth.** |
| Is terminal outcome the right first immutable fact? | **Yes, after semantic corrections.** |
| Independent `EvidenceId`? | **Yes.** |
| Evidence entity/event/value object? | **Immutable identified observation record; event-like, append-only, not mutable entity.** |
| Typed payload vs generic kind/payload | **Closed typed domain union; discriminator/version only at serialization boundary.** |
| Success/failure/cancellation variants | **Yes.** |
| `AGENT/VALIDATION/SESSION/OBSERVATION` | **Not as causes.** |
| Hierarchical failure taxonomy | **No, not now.** |
| Observation location vs reason | **Currently conflated; separate them.** |
| Separate dimensions? | **Yes; implement location now, cause later where an authoritative producer exists.** |
| Who constructs terminal Evidence? | **Runtime.** |
| `observed_at` | **Keep, but add occurrence time.** |
| Event/observation/ingestion/sequence | **Occurrence + observation now; storage sequence later; ingestion metadata only if needed.** |
| No terminal Evidence unless Attempt terminalized | **Correct for normal terminal evidence; independently surface terminalization failure.** |
| Attempt lifecycle failure as Evidence | **Conceptually possible, but treat as invariant/self-diagnostic until a consumer justifies a type.** |
| Observer + sink | **Clean separation.** |
| Synchronous sink | **Yes initially, bounded/nonblocking contract.** |
| Delivery guarantee | **Best-effort now; explicit journaled guarantees later if consumers require them.** |
| Represent evidence loss | **Independent channel health/self-diagnostics; never rely on failed channel to report itself.** |
| Persist separately from Session | **Yes.** |
| SQLite model | **Attempt subject/header + Evidence header + type-specific table.** |
| Append-only | **Yes at semantic API level, with separate retention/privacy administration.** |
| Immutability | **Frozen objects; no ordinary record UPDATE; same ID/different body is corruption.** |
| Schema evolution | **Per-kind versioning, explicit incompatible versions, no semantic rewriting of old history.** |
| Minimum replay facts | **Logical operation, stable inputs/version, attempts, execution boundaries, outputs/checkpoints, idempotency/effect evidence.** |
| Failed vs external side effects unknown | **Attempt state cannot distinguish them; stage plus lower-level effect evidence must.** |
| Provider-specific information | **Keep outside generic Runtime Evidence.** |
| Provenance relationships | **Typed references later; no generic graph now.** |
| Context compiler/evaluation coupling | **Separate domains referencing stable Evidence/artifact identities.** |
| Security/privacy | **Data minimization by default; raw prompts, outputs, paths, commands, exceptions and provider data need separate policy.** |
| What is not Evidence? | **Policy, mutable conclusions, arbitrary logs/metadata, retry recommendations, raw telemetry by default.** |
| Useful external concepts/naming | **Execution journal, occurrence/event distinction, run identity, provenance Activity/Entity concepts, dual timestamps.** |
| Existing well-understood model? | **Closest to an execution/provenance journal, not pure event sourcing or tracing.** |
| Smallest next implementation | **One immutable terminal Attempt record with stage-correct semantics and a narrow recorder seam.** |

### Genuine open questions

Several decisions **cannot be responsibly frozen from current consumer evidence**.

**Whether Evidence must eventually be durable before Runtime returns.** Governance, forensic audit, or crash-recovery requirements may say yes; ordinary development observability may say no.

**Whether Attempt identity should eventually exist for every Runtime turn even with no observer/recorder.** This becomes compelling if execution identity is part of reproducibility or cross-process correlation, but it is unnecessary overhead conceptually today.

**Whether retry requires `OperationId`, an idempotency-key abstraction, or both.** These serve related but different purposes; the actual retry API should determine their semantics.

**What provider/tool facts are necessary for effect reconciliation.** That depends on which Agents/tools first need safe retry.

**Whether context compilation records every candidate considered or only selected inputs.** Full retrieval provenance may be needed for evaluation but can be very large and security-sensitive.

**Whether compiled context itself is a Message, an Artifact, or a separate immutable domain object.** The compiler design should answer this.

**Whether Evidence requires cryptographic integrity or producer authentication.** Ordinary reproducibility and debugging do not justify signed attestations; adversarial governance might.

**Whether records require per-Attempt sequence numbers.** One terminal record does not. Multiple independently emitted facts may.

**How long Evidence is retained.** Privacy, audit, evaluation, and cost requirements may conflict.

**Whether evaluation observations belong in the same `devtools.evidence` package or a separate evaluation domain.** Identity/reference design can support either; there is no need to settle package topology now.

**Whether `AttemptObserver` should ever be renamed to reflect its admission authority.** Architecturally the current behavior is clear enough; an API rename is a compatibility decision rather than a missing semantic primitive.

### Final verdict

**Implement with modifications. Do not stop and redesign the architecture, but do not freeze the proposed next slice as written.**

The central architectural direction is stronger than the main alternatives: keep the mutable `Attempt` as a deliberately tiny live execution handle and introduce separately identified immutable records that form an execution Evidence journal over time.

The proposed design goes wrong primarily in **semantic compression**, not in overall structure.

The failure taxonomy compresses execution phase into purported cause:

```text
AGENT / VALIDATION / SESSION / OBSERVATION
```

and `SESSION` in particular destroys distinctions that future replay safety will care about.

The timestamp model compresses occurrence time and observation time.

The no-terminal-Evidence rule correctly avoids contradictory state but lacks a separate accounting path for an impossible/invariant failure.

And Evidence referencing only `AttemptId` is fine in memory today, but future persistence must preserve immutable Attempt attribution somewhere independently of live Python objects.

The smallest defensible next model is therefore:

```text
Attempt
    live, mutable lifecycle handle

AttemptTerminalEvidence
    id: EvidenceId
    attempt_id: AttemptId
    occurred_at: Timestamp
    observed_at: Timestamp
    outcome:
        Succeeded
        Failed(stage: AttemptStage)
        Cancelled(stage: AttemptStage)

AttemptStage
    ADMISSION
    CONTINUATION_LOOKUP
    AGENT_INVOCATION
    RESULT_VALIDATION
    OUTPUT_RETENTION
    CONTINUATION_REPLACEMENT
```

with these architectural laws:

```text
Attempt state is control state, not diagnostic truth.

Evidence records are immutable historical assertions.

EvidenceId identifies a record;
AttemptId identifies the execution it concerns.

Runtime records only facts whose boundary semantics Runtime knows.

Execution stage is not root cause.

Failure/cancellation never implies that external effects did not occur.

Retryability is a derived policy decision, never an Attempt outcome.

Evidence recording failure never rewrites an established application outcome.

A failed Evidence channel cannot reliably testify to its own failure.

Persisted Evidence is append-only in semantic meaning.

Session state and Evidence history remain independently persisted.

Provenance grows through explicit typed relationships only when consumers require them.

Evaluation, governance, and self-improvement consume Evidence;
they do not mutate it.
```

That is small enough to audit and freeze, but it establishes the right fault lines for durable execution later. It borrows the strongest ideas from provenance standards, tracing, event journals, lineage systems, and workflow engines while deliberately refusing their infrastructure and extensibility mechanisms until your own consumers actually require them. citeturn14search0turn14search1turn19view0turn15search4turn19view1
