# B-0029 — Reusable Agent definition and runtime orchestration

- type: INVESTIGATION
- status: SUPERSEDED
- decision_maturity: READY_FOR_DESIGN
- necessity: FUTURE_REQUIRED
- architectural_significance: STRUCTURAL
- urgency: DEFERRED
- evidence_basis: MULTIPLE
- scope: historical parent for Agent, lifecycle, and orchestration concerns
- primary_domain: agents
- supporting_domains: execution, orchestration, context, tools, models
- split_children: B-0043, B-0044

## Split record

Agent semantics, generic lifecycle promotion, and orchestration are distinct
approved domains. Current Codex integration is an external Agent; Qwen loops
are experiment-local control evidence. Neither establishes a BaseAgent,
generic Run implementation, or orchestration framework.

B-0043 owns future Agent semantics, B-0031 owns generic lifecycle promotion,
and B-0044 owns orchestration pressure.
