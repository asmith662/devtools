# B-0014 — Investigate retry, repair, and reconciliation semantics

- type: INVESTIGATION
- status: DEFERRED
- decision_maturity: DISCOVERED
- necessity: FUTURE_REQUIRED
- architectural_significance: FOUNDATIONAL
- urgency: DEFERRED
- evidence_basis: RESEARCH
- scope: retry, semantic repair, and reconciliation semantics
- parent: B-0005

## Problem / value

Preserve distinctions:

    transport failure -> possible retry
    failed tests -> semantic repair or new work
    unknown external outcome -> reconcile before repeat

Replanning changes strategy or decomposition and is distinct from repair.
Known success, known failure, and unknown outcome must remain distinct. An
external effect may succeed while communication fails before its response is
observed, so communication failure does not establish that repetition is safe.
Retryability is not equivalent to failure; persistence/checkpointing alone does
not provide exactly-once effects; cancellation does not necessarily roll back.
Partial side effects, nested retries, stale authority during retry/resume, and
workflow branching add pressure, but the component reporting failure should not
automatically own the retry decision.

## Dependencies / risks / validation

- hard_dependencies: B-0012 for effect outcome semantics
- pressure_dependencies: B-0010, B-0013, B-0021, B-0026, B-0028
- operational_dependencies: safely repeatable or uncertain real effect
- consumers: future recovery behavior
- unresolved_semantics: retry, repair, replanning, workflow branching, reconciliation, known/unknown outcome classification, idempotency, partial side effects, nested retries, stale authority, and repair identity
- risk_if_deferred: local recovery remains explicit until needed
- risk_if_implemented_early: generic retry policy with false safety claims
- promotion_trigger: real effect has uncertain outcome or needs safe retry
- validation_level: NONE
- live_validation_trigger: uncertain external effect outcome or safe retry need is observed
- related: B-0005, B-0010, B-0012, B-0013, B-0021, B-0026, B-0028
