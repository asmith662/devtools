# B-0006 — Reconcile authoritative architecture documentation

- type: INVESTIGATION
- status: ACTIVE
- decision_maturity: READY_FOR_DESIGN
- necessity: REQUIRED
- architectural_significance: STRUCTURAL
- urgency: NOW
- evidence_basis: REPOSITORY
- scope: current architecture documentation reconciliation
- primary_domain: documentation
- supporting_domains: none
- parent: B-0001

## Problem / value

Keep current architecture documentation synchronized with implemented
twelve-domain ownership and current package APIs. The prior roadmap described
obsolete `interactions`, Conversation predecessors, Runtime/Evidence ownership,
and former source paths; current guidance must not do so.

- hard_dependencies: none
- pressure_dependencies: none
- operational_dependencies: none
- promotion_trigger: current documentation materially drifts from implementation or architecture
- validation_level: INTEGRATION

## Initial reconciliation audit (2026-10-23)

The [dated source/adoption inventory](../../research/architecture-reconciliation-inventory.md)
authenticates feature/main separately, identifies current-looking historical
sequencing and distinguishes maintained APIs, actual consumers, destination blobs
and original experimental outcomes. The research index now qualifies its earlier
R1/R2 checkpoint without rewriting that substantive body. Commands source already
matches remote main, while current WorkCycle/native Context changes do not.

This is an initial documentation checkpoint, not closure of B-0006 or approval
of any architectural change. The starter ZIP/18-story crosswalk remains unavailable;
complete lifecycle/harness/custody comparison and successor-session handoff follow
the [finite phase charter](../../development/reconciliation.md#finite-architecture-and-research-reconciliation-2026-10-23).

## Recovered-input / pinned mechanism evidence (2026-10-23)

Original transfer inputs are authenticated and all18 candidates mapped in the
[canonical crosswalk](../../research/reconciliation-input-reconciliation.md).
This resolves the prior missing-input obligation, not B-0006 or the finite audit.
Exact original drafts remain attributed research; current source findings and
canonical authority are not overwritten. Existing status and parent remain.

## Production reconciliation evidence (2026-10-23)

The completed production reconciliation enumerates48 source-backed capability slices, all35 experimental collections and eight selective destination review groups.32 framework Python blobs differ/new relative to main; Commands source already matches main and destination-only tests/docs must be preserved. Canonical architecture/backlog authority remains separate from dated inventories; comprehensive successor handoff is the next checkpoint.

See the [complete audit and prioritized roadmap](../../research/production-adoption-and-architecture-reconciliation.md)
and [source/custody identities](../../research/production-adoption-and-architecture-evidence-20261023.json).
Existing status, parent, dependencies, decision maturity and promotion trigger
remain unchanged; advisory research does not authorize implementation.

## Core/Resources audit evidence (2026-10-25)

Core/Resources full-body review finds current filesystem package documentation still describes feature-only binary/bounded-read publication even though those owners are integrated. Reading implementation docstring also retains imprecise pre-bounded growth wording. New report supplies exact current-owner evidence; no source semantics or historical records were rewritten. See the [review and exact bounded scopes](../../research/core-paths-filesystem-and-commands-audit.md). Status, decision maturity and promotion authority remain unchanged.

## Core/Resources repair evidence (2026-10-26)

The bounded Core/Resources repair updates current path/I/O/Commands contracts and stale package I/O/roadmap adoption wording. Original scientific/engineering history is unchanged. Other documentation reconciliation, including older dated notes and remaining wording, remains separate. See the [delivered repair](../../development/core-resources-integrity-repair.md). Status, maturity and parent authority remain unchanged.

## Core Identity/Time evidence — 2026-10-26

Current Identity overview correctly describes runtime UUID checking in Construction but incorrectly denies it in Limitations, and says no typed IDs exist despite maintained ConversationId/MessageId/InteractionAttemptId/ModelInteractionId/EvidenceId wrappers. This is stale documentation under existing B-0006, not missing primitive semantics or authority to redesign IDs. Preserve any later migration as separate work. [Full review](../../research/core-identity-and-time-audit.md). Status/maturity unchanged. `audit:core-identity-time:32c91a17:20261026`.

## ModelInteraction/Serving evidence — 2026-10-26

ModelInteraction/Serving audit on `a7a49cc18f3b40a5bf4e3897ca30d9a5cddc30d1`: all30 selected bodies/export/marker surfaces (7,119 lines) fully reviewed,321 focused plus113 real-consumer deterministic tests pass.44 independent cases reproduce five bounded P2 families (UTF8 normalization, vLLM response framing/shape, readiness writer cleanup, registry-port/tag admission, strict Tool JSON). See [report](../../research/model-interaction-and-serving-audit.md) and [exact evidence](../../research/code-audit/model-interaction-serving-assurance.json). No source/test change, live inference or new protected gate. Serving overview Status still says only vLLM although later sections/current code expose llama.cpp; Qwen composition docstring says experiment despite maintained apps owner. These are stale wording under B0006, not an unimplemented Serving capability or reopening B0007. Current audit overlay supplies accurate owner/consumer scope; no source/docstring rewrite. Existing status, decision maturity, dependencies, approvals and authority remain unchanged. `audit:model-interaction-serving:a7a49cc1:20261026`.

## ModelInteraction/Serving repair evidence — 2026-10-26

Current Serving Status and corrected package contracts now describe both concrete adapters and bounded readiness/cleanup. Other stale identity/application wording and broader reconciliation remain separate. [Delivered repair](../../development/model-serving-contract-repair.md), production `5125ab6a847ee1844913c006d801b01f5fea7cc4`, normal PR32, verified main `a602dae60b3a7c71bdd1c1231613143c309292c1`. No state/maturity/approval/parent closure or new authority. `repair:model-serving-contracts:5125ab6a:20261026`.
