# B-0014 — Retry, repair, and reconciliation

- type: INVESTIGATION
- status: SUPERSEDED
- decision_maturity: READY_FOR_DESIGN
- necessity: FUTURE_REQUIRED
- architectural_significance: FOUNDATIONAL
- urgency: DEFERRED
- evidence_basis: RESEARCH
- scope: historical parent for separated retry, repair, and reconciliation pressure
- primary_domain: execution
- supporting_domains: agents, orchestration, governance, observability, persistence
- split_children: B-0032, B-0033, B-0034

## Split record

Retry of an execution attempt, semantic repair/replanning, and reconciliation
of an uncertain external effect are distinct concerns. Their surviving pressure
is preserved by B-0032, B-0033, and B-0034 respectively.
