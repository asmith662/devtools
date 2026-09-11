# B-0010 — Investigate logical work, execution, and attempt semantics

- type: INVESTIGATION
- status: DEFERRED
- decision_maturity: DISCOVERED
- necessity: FUTURE_REQUIRED
- architectural_significance: FOUNDATIONAL
- urgency: DEFERRED
- evidence_basis: MULTIPLE
- scope: logical-work, execution, and attempt identity semantics
- parent: B-0004

## Problem / value

Determine whether and when work, execution, and attempt identities must be
distinct beyond existing Runtime Attempt and terminal Evidence.

## Evidence / invariants

Runtime to Attempt to terminal Evidence is established. Unknown: whether Attempt
already represents execution, retry/repair identity, supervisor takeover, and
whether child model/tool activity becomes nested execution.

Independent pressure confirms that one logical requested piece of work need not
be one concrete attempt. Retries, repairs, supervisor corrections, worker
re-execution, stronger-model takeover, cancellation/resumption, and durable
evidence may expose that distinction; none establishes a Work-to-Execution-to-
Attempt hierarchy.

Future investigation must distinguish framework-owned work/attempt identity
from provider or external execution identity and from correlation identity.
Those identities may coincide for a simple operation but need not under retry,
repair, re-execution, supervisor-requested correction, Codex takeover, or
cancellation/resumption.

## Dependencies / risks / validation

- hard_dependencies: none
- pressure_dependencies: B-0011, B-0014, B-0025, B-0026, B-0028
- operational_dependencies: multi-attempt consumer
- consumers: future repair/takeover/durable execution work
- established_invariants: Runtime -> Attempt -> terminal Evidence is existing evidence, not disposable design
- unresolved_semantics: logical Work identity, repair/retry identity, framework/provider/correlation identities, takeover, cancellation/resumption, and child execution nesting
- risk_if_deferred: none until current identities are insufficient
- risk_if_implemented_early: invented hierarchy becomes infrastructure
- promotion_trigger: user-visible work spans attempts, repairs, or takeover
- validation_level: NONE
- live_validation_trigger: real work spans attempts or supervisor transitions
- related: B-0004, B-0011, B-0014, B-0025, B-0026, B-0028
