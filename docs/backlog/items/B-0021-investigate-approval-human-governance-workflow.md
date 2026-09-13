# B-0021 — Approval and human-governance workflow

- type: INVESTIGATION
- status: SUPERSEDED
- decision_maturity: READY_FOR_DESIGN
- necessity: FUTURE_REQUIRED
- architectural_significance: STRUCTURAL
- urgency: DEFERRED
- evidence_basis: RESEARCH
- scope: historical parent for approval conditions and approval workflow
- primary_domain: governance
- supporting_domains: orchestration, persistence, execution
- split_children: B-0037, B-0038

## Split record

Approval semantics are governance conditions; requesting, waiting, suspension,
and resumption are orchestration. Durable state is a supporting Persistence
concern only when a consumer requires it. B-0037 and B-0038 preserve the
separate pressure.
