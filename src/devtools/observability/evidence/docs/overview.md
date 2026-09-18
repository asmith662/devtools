# `devtools.observability.evidence`

This package owns immutable factual Evidence about completed execution
boundaries. `InteractionAttemptTerminalEvidence` records the terminal outcome
of one specialized `InteractionAttempt`; `EvidenceSink` accepts such records;
and `ExecutionInspector` observes execution lifecycle facts, constructs
terminal Evidence, and retains or forwards it for process-local diagnostics.

Execution owns the mutable `InteractionAttempt` lifecycle and its observer
contract. It does not import this package. Observability may depend on
execution lifecycle facts to construct Evidence, preserving the dependency
direction:

```text
execution -> InteractionAttemptObserver -> observability/evidence
```

Evidence is historical observation, not authorization, tracing, telemetry, or
current authority.

`ModelInteractionEvidence` is a separate Evidence form for one completed model
invocation. `ModelInteractionInspector` is optional process-local observation:
models and Runtime work normally when it is absent. The inspector owns capture
policy, evidence construction, capture manifests, collection, and inspection.
It currently receives only successfully completed normalized interaction
observations. Its capture-controlled request/response representation is not
necessarily exact replay material, is not automatically correlated to a
Runtime `InteractionAttempt`, and is not an Evaluation realization or judgment.
Failed provider/model realizations and observer failures require distinct
accounting by a future consumer that claims a complete evaluation population.
Payload manifests distinguish captured, omitted, redacted, and unavailable;
credentials, transport headers, and equivalent sensitive transport state have
no generic capture path.

For collections of Tool schemas or arguments, a `partial` manifest state means
the occurrences have differing retention states. It never claims that a
collection was wholly captured, omitted, redacted, or unavailable.

Structural request settings, normalized usage and termination, serving-profile
provenance, and bounded provider exchange facts remain inspectable. Prompt,
visible content, reasoning, and selected provider identity strings are retained
only under explicit capture policy. This package does not own Trace, Telemetry,
persistence, request policy, or model execution.

When present, disclosed normalized Tool names/descriptions are structural
Evidence. Tool schemas and returned untrusted call arguments are capture
controlled. Evidence never retains executable Tool objects, ToolRunner state,
authorization, or execution outcomes.
