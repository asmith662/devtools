# Direct structural discrimination capture

This package implements the already-frozen Stage A protocol without changing its
sources or artifacts. Capture order is 0017, 0018, 0019; any failure stops the
cohort and kills that execution identity. It never reads child implementations,
holdouts, gold or confirmation/reserve. No reranking, PPR or RRF is performed.

`python -m experiments.structural_discrimination.stage_b.execute capture`
authenticates the accepted Stage A, publishes all three exact schedules before
claiming an execution, then runs each scientific operation once. The inherited
exclusive journal owns ENTERED/RETURNED/FAILED_NO_RETURN and shared pickle memo
semantics. Convenience journal writes are disabled. Derived progress is printed
at operation boundaries and retained only in `.local`, outside scientific seals.

The capture-only journal codec uses the existing GraphEncoding to emit exactly
the historical native graph bytes, with invocation-local immutable node templates.
It changes serialization cost, not the native scientific result or journal schema.
Deep proof decodes the ordered shared-memo archive and checks every canonical
return with the existing alias/type/order correspondence verifier exactly once.
It also reconstructs the published scientific artifacts and validates evidence
completeness from those returns, without executing BM25 or RI again.

Each completion proof binds Stage A protocol/frame, schedule, journal chain,
native envelope bytes, derived canonical artifacts, producer/verifier source
hashes and execution completion. Its digest is anchored by the accepted treatment
Git commit through integrity.json. Normal `verify --checkpoint COMMIT` hashes
every bound byte, authenticates the journal envelopes and proof and reconstructs
canonical reporting, but does not unpickle or re-establish native correspondence.
Prepublication verification is explicitly distinct from committed authority.
No trust is cached across invocations; no silent deep fallback exists.

Warm timing includes the exact canonical query analysis/BM25 call, ordinary
annotation guards, support projection, annotation construction and explicit local
pair record construction. A small line observer marks the boundary already in
the frozen annotate function; its overhead is included and disclosed. It neither
changes the function nor observes RI or scoring internals. The native annotation
already retains its predecessor; pair timing additionally covers construction of
the explicit diagnostic records, not a second annotation pass. Offline native
frame, lexical fields/index, module universe and Reference preparation, journal
serialization, deep proof, validation, reports, hashes and Git are excluded.
Nine single scientific workload samples are descriptive, not a benchmark rerun.

Primary annotation passes are three per case. Separate validation ablations use
empty Reference input to reconstruct empty annotations with the same A object;
they do not repeat scoring or the primary structural treatment. Evidence and
pair validation may inspect retained native/canonical results but never rederive
References. Full positive and negative RI assessments remain in the native journal
and complete canonical RI graph. Human-readable trace includes all A ranks,
supports, pairs and mechanical counters, with no semantic labels or usefulness
inference. Stage C is constructed only after the complete cohort is published.
