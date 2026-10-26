# B-0041 — Investigate execution-local lifecycle control

- type: INVESTIGATION
- status: DEFERRED
- decision_maturity: DISCOVERED
- necessity: FUTURE_REQUIRED
- architectural_significance: STRUCTURAL
- urgency: DEFERRED
- evidence_basis: MULTIPLE
- scope: cancellation, timeout, cleanup, and ownership at execution boundaries
- primary_domain: execution
- supporting_domains: resources, models, tools, observability
- split_from: B-0026

## Problem / value

Determine execution-local cancellation, deadlines, cleanup precedence, and
partial-work outcome semantics across model and Tool activity. Runtime remains
narrow and is not a universal control plane.

- hard_dependencies: none
- pressure_dependencies: B-0031
- operational_dependencies: conflicting live execution lifecycle behavior
- promotion_trigger: local boundaries need shared lifecycle control semantics
- validation_level: NONE

## Core/Resources audit evidence (2026-10-25)

A deterministic public Commands I/O-fault probe returns terminal failure while one sibling reader remains pending. A specific P2 repair is captured without promoting generic lifecycle control. Actual immediate-child cancellation/timeout controls pass and external effects remain; no leaked live child is demonstrated. See the [review and exact bounded scopes](../../research/core-paths-filesystem-and-commands-audit.md). Status, decision maturity and promotion authority remain unchanged.

## Core/Resources repair evidence (2026-10-26)

Bounded child37a647f2 is implemented through normal PR#23: Commands settles owned read/input tasks before terminal completion and preserves original errors. This is not shared lifecycle architecture, descendant control, a spawn-wide deadline, arbitrary repeated-cancellation handling or external-effect rollback. See the [delivered repair](../../development/core-resources-integrity-repair.md). Status, maturity and parent authority remain unchanged.
