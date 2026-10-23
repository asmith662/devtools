# B-0032 — Investigate execution retry mechanics

- type: INVESTIGATION
- status: DEFERRED
- decision_maturity: DISCOVERED
- necessity: FUTURE_REQUIRED
- architectural_significance: STRUCTURAL
- urgency: DEFERRED
- evidence_basis: RESEARCH
- scope: retry of one execution attempt
- primary_domain: execution
- supporting_domains: governance, observability
- split_from: B-0014

## Problem / value

Determine retry eligibility, attempt identity, timeout/cancellation handling,
and outcome classification for safely repeatable execution. Retry is not
semantic repair and is not reconciliation of an uncertain external effect.

- hard_dependencies: none
- pressure_dependencies: B-0031, B-0034, B-0041
- operational_dependencies: real safely repeatable operation
- promotion_trigger: a reusable execution boundary needs a retry decision
- validation_level: NONE

## Recovered-input / pinned mechanism evidence (2026-10-23)

The [Pydantic timeout/retry comparison](../../research/agent-harness-mechanism-review.md#pydantic-ai-execution-order-cancellation-and-state)
distinguishes typed validation repair from ordinary failed results and cancellation.
An upstream synchronous Tool timeout abandons a still-running thread and can
request a retry. This is evidence to qualify repeatability before retrying effects,
not a reusable automatic retry policy for Devtools. Current task ceilings still
charge refused proposals/actions. B-0033/B-0034 remain separate owners.
