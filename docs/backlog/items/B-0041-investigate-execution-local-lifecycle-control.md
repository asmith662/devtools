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

## ModelInteraction/Serving evidence — 2026-10-26

ModelInteraction/Serving audit on `a7a49cc18f3b40a5bf4e3897ca30d9a5cddc30d1`: all30 selected bodies/export/marker surfaces (7,119 lines) fully reviewed,321 focused plus113 real-consumer deterministic tests pass.44 independent cases reproduce five bounded P2 families (UTF8 normalization, vLLM response framing/shape, readiness writer cleanup, registry-port/tag admission, strict Tool JSON). See [report](../../research/model-interaction-and-serving-audit.md) and [exact evidence](../../research/code-audit/model-interaction-serving-assurance.json). No source/test change, live inference or new protected gate. New serving readiness-stream cleanup has a separate pending P2 UUID; it is not the already delivered managed Command collector repair. Known-CID cleanup works, lost Docker acknowledgment and HF thread cancellation remain external-effect ambiguity; no whole-start deadline or descendant cleanup guarantee added. Existing status, decision maturity, dependencies, approvals and authority remain unchanged. `audit:model-interaction-serving:a7a49cc1:20261026`.
