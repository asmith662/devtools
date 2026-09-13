# B-0010 — Record resolved Run, Step, and Attempt semantics

- type: INVESTIGATION
- status: DEFERRED
- decision_maturity: READY_FOR_DESIGN
- necessity: FUTURE_REQUIRED
- architectural_significance: FOUNDATIONAL
- urgency: DEFERRED
- evidence_basis: MULTIPLE
- scope: resolved lifecycle terminology and deferred generic implementation pressure
- primary_domain: execution
- supporting_domains: agents, orchestration, observability, persistence
- parent: B-0004
- semantic_decision: RESOLVED

## Resolved semantic decision

The authoritative taxonomy defines `Run -> Step -> Attempt`. `Attempt` is one
try to execute a Step; `InteractionAttempt` remains the current specialized
Runtime lifecycle and is not generic Attempt.

No generic Run, Step, or Attempt implementation is authorized. Future work
must use this decision rather than reopen terminology and should proceed only
through B-0031 when a reusable consumer requires it.

- related: B-0031, B-0043, B-0044
- validation_level: NONE
