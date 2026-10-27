# B-0003 — Local Coding Worker Harness

- type: EPIC
- status: BLOCKED
- decision_maturity: SEMANTICS_PARTIAL
- necessity: REQUIRED
- architectural_significance: HARNESS_LOCAL
- urgency: SOON
- evidence_basis: REAL_USE
- scope: first bounded local coding-worker experiment
- primary_domain: experiments
- supporting_domains: agents, context, tools, models, execution, evaluation

## Problem / value

Eventually exercise a bounded Qwen coding worker that can use selected Context,
request bounded Tool work, make explicitly governed effects where required,
validate outcomes, and produce review evidence. It is experimental composition,
not a generic Agent or orchestration implementation.

Existing Qwen read-only probes provide predecessor evidence for model turns,
read-only Tool use, local Action parsing, bounded projections, and durable
acceptance reporting. They are not a coding/editing worker.

- hard_dependencies: B-0008
- pressure_dependencies: B-0012, B-0016, B-0035, B-0036, B-0043, B-0044
- operational_dependencies: pinned Qwen serving profile
- children: B-0009
- blocked_by: minimum coding-context boundary for the selected story
- promotion_trigger: B-0008 resolves required selected repository information
- validation_level: LIVE_SINGLE_HARNESS

## Qwen operational application audit evidence

Current maintained application does implement bounded model/Context/Tool/edit/check/repair/candidate composition and trusted local Checkout entry, beyond this epic's dated read-only predecessor description. This source-backed audit does not change status/dependencies/maturity or approve a generic Agent. One bounded task-outcome P2 and existing cohesion/Localization/recovery owners remain. [Operational assessment](../../research/qwen-operational-lifecycle-audit.md). audit:qwen-operational:7a657dba:20261027.

## Framework/application direction design — 2026-10-27

PR45/46 delivered a bounded behavior-preserving Qwen application extraction and remain valid delivery evidence. They do not promote portable workflow/source/check mechanisms into the framework or establish Qwen as the primary architectural owner. The maintainer-directed reconciliation now prioritizes framework reuse and an independent non-Qwen consumer. This epic preserves the historical bounded experiment; B-0035/B-0043/B-0044/B-0042 retain separate structural authority. Do not repeat the delivered extraction or treat further application-only sophistication as the framework migration. [Decision package](../../development/framework-application-direction.md). Status, maturity, dependencies, original approvals and promotion triggers remain unchanged. `design:framework-application-direction:e84b724c:20261027`.
