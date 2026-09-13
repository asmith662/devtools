# B-0017 — Record settled execution and observability ownership

- type: INVESTIGATION
- status: SUPERSEDED
- decision_maturity: READY_FOR_DESIGN
- necessity: FUTURE_REQUIRED
- architectural_significance: STRUCTURAL
- urgency: DEFERRED
- evidence_basis: MULTIPLE
- scope: resolved execution/Evidence seam and redirection of future causal occurrence pressure
- primary_domain: observability
- supporting_domains: execution
- semantic_decision: RESOLVED

## Resolved semantic decision

Execution owns InteractionAttempt lifecycle. Observability owns immutable
Evidence and may observe execution facts; execution does not depend on
observability. This settles the ownership part of the former investigation.

Future causal occurrence, ordering, correlation, and Trace pressure is owned
by B-0023. No Event bus, Trace implementation, or telemetry middleware is
authorized by this record.

- related: B-0023, B-0011, B-0024
- validation_level: NONE
