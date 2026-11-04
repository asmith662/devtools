# B-0033 — Investigate semantic repair and replanning

- type: INVESTIGATION
- status: ACTIVE
- decision_maturity: DISCOVERED
- necessity: FUTURE_REQUIRED
- architectural_significance: STRUCTURAL
- urgency: DEFERRED
- evidence_basis: RESEARCH
- scope: goal-directed repair and changed strategy after known outcome
- primary_domain: agents
- supporting_domains: orchestration, evaluation
- split_from: B-0014

## Problem / value

Determine when an Agent changes strategy, decomposes new work, or repairs a
known failed result. This is not transport retry and does not authorize an
Agent framework or orchestration engine.

- hard_dependencies: none
- pressure_dependencies: B-0043, B-0044
- operational_dependencies: bounded Agent consumer with known failed work
- promotion_trigger: one consumer needs explicit repair distinct from retry
- validation_level: INTEGRATION

## B-0053 continuation requirement (2026-11-03)

Implementation readiness was explicitly activated through Intake's existing-item
owner following the operator's bounded implementation request and policy decision.
The known failed consumer satisfies the promotion trigger. The broader
investigation remains open; see the [first bounded contract](../../development/coding-continuation.md).

B-0053 supplies a live failed-attempt case: its native Qwen execution remains
BLOCKED after frozen private acceptance rejected the candidate, while a separate
authorized Codex repair completed the engineering obligation. A future bounded
repair-continuation or delegation capability should continue the same engineering
obligation after a failed attempt instead of creating a replacement backlog task.
It must preserve task identity, source custody, independent acceptance, finite
execution budgets, model provenance and diagnostic confidentiality. This is
follow-up evidence for the existing investigation, not implementation authority
or a promotion of this deferred item.

## First bounded implementation (2026-11-03)

The operator subsequently authorized implementation and activated the two-total-
attempt standing amendment. Intake recorded readiness from DEFERRED to ACTIVE
without creating a replacement obligation. WorkCycle.native now addresses
immutable coding children and issues fresh policy-derived grants after known
terminal public-validation failure. The 17 focused deterministic regressions
passed, including an alternate scripted coding model; this is simulated evidence,
not another live Qwen episode.

B-0051 is the first prospective live opportunity: its unresolved episode ended
in public-validation failure with acknowledged effects, restored source and
released Checkout custody. Current inputs, branch and historical authority still
require admission checks. No continuation has been prepared or dispatched here.

This delivers one conservative slice. Independent private-acceptance rejection
requires future supervised diagnostic disclosure that protects oracle
implementation. Broader strategy repair, replanning and delegation remain open.
