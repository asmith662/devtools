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
