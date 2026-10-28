# Command observations and procedural candidates

CommandObservation is a bounded factual projection with explicit host origin,
value-free CommandPattern, source, known/unknown entry, outcome, exit/duration
and capture qualification. It is process-local; no store or global collector is
installed. EvidenceSink's specialized InteractionAttempt contract is unchanged.

CommandInspector observes one existing managed handle without changing its
result, original failure or cancellation. Completed result projection also works
when a consumer has only a CommandResult. No raw argv, command text, environment,
stdin, stdout/stderr or exception payload is retained in normalized observations.
Host-supplied labels and source archives still require privacy/retention policy.

summarize_patterns deduplicates stable origins, refuses conflicting input records,
and groups operation/argument roles/capabilities with explicit known/unknown
outcomes. Same-run co-occurrence is unordered. Frequency never grants trust or
automatically creates an executable Tool. CLI item reconciliation belongs to
the Codex external-agent adapter; missing CLI events are not negative evidence.

See [sources, privacy, limits and promotion requirements](../../../../../docs/development/command-capabilities.md).
