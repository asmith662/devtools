# B-0004 — Governed Execution Evolution

- type: EPIC
- status: SUPERSEDED
- decision_maturity: READY_FOR_DESIGN
- necessity: FUTURE_REQUIRED
- architectural_significance: FOUNDATIONAL
- urgency: DEFERRED
- evidence_basis: MULTIPLE
- scope: historical parent for separated execution lifecycle and durable observation pressure
- primary_domain: execution
- supporting_domains: observability, persistence, governance
- split_children: B-0031

## Split record

The former epic incorrectly grouped generic execution lifecycle, specialized
InteractionAttempt, terminal Evidence, and durability. Execution now owns the
specialized lifecycle; observability owns Evidence; Persistence owns storage
mechanics.

Future generic lifecycle promotion is B-0031. Durable evidence and recovery
remain separately represented by B-0011 and B-0028. This record preserves
lineage and does not authorize implementation.
