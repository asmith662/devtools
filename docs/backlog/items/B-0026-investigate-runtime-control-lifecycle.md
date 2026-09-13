# B-0026 — Runtime control and lifecycle

- type: INVESTIGATION
- status: SUPERSEDED
- decision_maturity: READY_FOR_DESIGN
- necessity: FUTURE_REQUIRED
- architectural_significance: STRUCTURAL
- urgency: DEFERRED
- evidence_basis: MULTIPLE
- scope: historical parent for execution-local and workflow lifecycle control
- primary_domain: execution
- supporting_domains: orchestration, resources, models, tools
- split_children: B-0041, B-0042

## Split record

Execution-local cancellation, cleanup, timeout, and ownership semantics differ
from control across future Runs and workflows. Runtime remains narrow. B-0041
and B-0042 preserve those separate pressures.
