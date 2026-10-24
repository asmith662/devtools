# Recovered reconciliation input: provenance and canonical disposition

## Status and authority

Codex research/documentation checkpoint, 2026-10-23, against feature
`3b2b3de845fbc0d8b510449bed9f492a54e39734`. This completes the missing-input
intake from the first checkpoint, not the entire finite architecture audit.
The original three assistant-authored drafts and independent ChatGPT review are
attributed research inputs, not ADRs, grants, approved stories or current API truth.
Canonical governance remains [the existing finite charter](../development/reconciliation.md#finite-architecture-and-research-reconciliation-2026-10-23),
taxonomy, accepted ADRs and existing backlog. No new governing index is created.

## Archive verification and custody

The locally supplied ZIP SHA-256 was recomputed:
`60762f4dc70d23e9907a0b1eddfbe5ab4405f37f44e07047695f337920ecf386`.
All six entries were inspected before writing: five declared payloads plus
TRANSFER-MANIFEST.json; no extra entry, duplicate path, absolute/drive/parent path,
backslash traversal, symlink or excessive-size member was admitted. All five
payload lengths and SHA-256 values match TRANSFER-MANIFEST; all three original
Markdown lengths/hashes also independently match the original MANIFEST.
TRANSFER-MANIFEST has no self-entry: its observed hash below is anchored by the
verified enclosing ZIP, not a claimed self-authentication.

| Imported original bytes | SHA-256 / verification |
|---|---|
| [Original charter](reconciliation-inputs/20261023/incoming/starter/01-reconciliation-charter.md) | `dd3835adc1e0a027eed2f76e604b15fdeb71ea32ba8e17f2051aaa54e7b45102`, 21,433 bytes, both manifests match |
| [Original harness notes](reconciliation-inputs/20261023/incoming/starter/02-oss-harness-mechanism-review-initial.md) | `6f78e8bc81d80b034eef6ed30e7403886ea4df2e1a5c281f6a235806ad79ae55`, 16,693 bytes, both manifests match |
| [Original18 seeds](reconciliation-inputs/20261023/incoming/starter/03-audit-backlog-seeds.md) | `1d5142d0e0e25e0f472d2108922b963ee9d02ee48bfb92b106c6a013db4e5ab2`, 10,159 bytes, both manifests match |
| [Original MANIFEST](reconciliation-inputs/20261023/incoming/starter/MANIFEST.json) | `eca7aaedf56b8eb2fe90870760b7176337c84ed4b796b23f1dc43c171859a2d8`, 696 bytes, transfer matches |
| [Independent review](reconciliation-inputs/20261023/incoming/review/devtools-reconciliation-independent-review-2026-10-23.md) | `c0755691d63bf5da0c47273134698e4e01f99e2a72f0d168b3ec0631c4ef7007`, 14,314 bytes, transfer matches |
| [TRANSFER-MANIFEST](reconciliation-inputs/20261023/TRANSFER-MANIFEST.json) | observed `1af915626a0de619f2f2609ff96cf34302facbbf1e3bde9e8fa579a6db0a931a`, 1,988 bytes |

Original container SHA `891d670922000782d75fc37bd45784990226fc41c486730f3a7b2d8a0a7c1cfd`
is **reported by the supplied manifest/review**, not recomputed locally: that
original ZIP container was not supplied. This does not weaken the locally verified
member hashes. ChatGPT sandbox access is not local filesystem access. Original
substantive contents and physical bytes are preserved; scoped `.gitattributes`
prevents text normalization and preserves original Markdown hard-break spaces.
The supplied independent review also retains its original final blank line under
a file-specific whitespace attribute; its sealed bytes are not cleaned up.
Historical original links, provisional language and any errors remain original.

The supplied transfer ZIP was moved unchanged from the root into ignored custody
`.local/harness-research-20261023/devtools-reconciliation-research-transfer-2026-10-23.zip`;
its SHA-256 was rechecked after the move. No archive or historical evidence was
deleted. Durable members and [verification/crosswalk metadata](reconciliation-inputs-20261023.json)
remain navigable without publishing the redundant ZIP or a second source tree.
The first checkpoint's NOT_VERIFIED_NO_INPUT claim remains accurate for its time.

## Charter reconciliation

The original charter adds explicit long-horizon OpenMind/Continuum motivation,
model neutrality, eventual specialist maintenance roles, and top-down/horizontal/
bottom-up plus successful/failed-trajectory audits. These are useful research
directions, not accepted reusable Agent/Memory/Trace architecture. It also asks
for finite exit/handoff criteria, exact adoption axes, staged cleanup custody and
proposal-before-fix discipline, already represented in the canonical charter.

Retain these substantive distinctions by reference and the canonical follow-up
appendix; do not create another governance document or overwrite current source
findings. Its category/status template maps to existing intake kinds and metadata,
not new enums/B-numbers. Its tentative parallel review, harness comparisons,
model configuration experiments and destructive-cleanup language are **not current
execution authority**. This assignment is source-and-test research only.

The independent review correctly qualified private Git identities as owner-
reported; this local checkpoint independently authenticates them. Its preliminary
18 routing is now replaced by the inspected crosswalk below, while its exact
original bytes remain unchanged. The starter's mostly-empty observability premise
is contradicted by maintained Evidence/usage/events. Its ExternalToolset validation
claim requires the pinned-source correction in the [mechanism comparison](agent-harness-mechanism-review.md#pydantic-ai-typed-tools-retries-and-permission-handoff).
Moving-main links and source-path leads in the drafts are not stronger evidence
than the new revision/blob/test references. Pydantic AI core and separate Harness
remain distinct; upstream test assertions were inspected, not executed here.

## Original candidate crosswalk

Exact original descriptions, triggers and acceptance wording are retained in the
linked source and JSON crosswalk, not reconstructed from titles. The following
maps every original ID to actual canonical records. Existing statuses/parents,
superseded lineage and append-only review chains are retained. A mapping to a
broad owner is not proof that every subquestion is solved.

| Original ID / exact suspected gap or value | Classification / canonical owner | Source-backed disposition |
|---|---|---|
| CANDIDATE-01 — Reconcile successful feature-branch capabilities with protected main and actual application consumers | RELATED_NEEDS_EVIDENCE; [B-0006](../backlog/items/B-0006-reconcile-authoritative-architecture-documentation.md) ACTIVE, [B-0001](../backlog/epics/B-0001-architecture-documentation-integrity.md) ACTIVE | Commands subset superseded by verified main integration; remaining feature capability adoption needs destination-specific dependencies and tests. The initial matrix is not completion of all promotion work. |
| CANDIDATE-02 — Inventory repeated domain semantics and utility implementations across apps, tools, Context, agents and runtime | RELATED_NEEDS_EVIDENCE; [39c6663a-bab7-43ed-8166-82e780a75d05](../backlog/proposals/39c6663a-bab7-43ed-8166-82e780a75d05/proposal.json) PENDING_REVIEW, [B-0035](../backlog/items/B-0035-investigate-tool-facing-capability-exposure.md) DEFERRED, [B-0044](../backlog/items/B-0044-investigate-orchestration-control-loops.md) DEFERRED | Large-module facts are qualified; duplicated domain semantics are still a hypothesis. Use existing module-size investigation and owner audit, not automatic utility extraction. |
| CANDIDATE-03 — Establish a reusable, model-neutral observability/event/tracing contract if the present module is fragmented | RELATED_NEEDS_EVIDENCE; [B-0023](../backlog/items/B-0023-investigate-observability-architecture.md) DEFERRED, [B-0011](../backlog/items/B-0011-investigate-durable-execution-evidence.md) DEFERRED | Starter report of mostly-empty observability is contradicted by existing Evidence/usage source. Amend research premise, preserve deferred canonical boundaries. |
| CANDIDATE-04 — Unified end-to-end agent trace and cost/time visibility | RELATED_NEEDS_EVIDENCE; [B-0023](../backlog/items/B-0023-investigate-observability-architecture.md) DEFERRED, [B-0024](../backlog/items/B-0024-investigate-audit-durable-accountability.md) DEFERRED, [B-0018](../backlog/items/B-0018-investigate-operational-data-minimization-disclosure.md) DEFERRED | Concrete cross-layer join/loss map adds evidence; paid supervisor time/hardware energy/account-wide costs remain unknown. No global Trace design selected. |
| CANDIDATE-05 — Verify Qwen thinking, template/tool protocol, quantization, KV cache and context against official recommendations | INSUFFICIENT_REQUIRES_INVESTIGATION; [B-0046](../backlog/items/B-0046-investigate-advanced-model-interaction-provider-pressure.md) BACKLOG, [B-0016](../backlog/items/B-0016-define-framework-live-harness-acceptance.md) BACKLOG | Serving/protocol/thinking controls exist, but official recommendation audit and matched model configuration experiments are not performed here. Historical failures do not isolate quantization/model reasoning cause. No new inference authority. |
| CANDIDATE-06 — Make specialized coding harnesses usable through common governed boundaries | RELATED_NEEDS_EVIDENCE; [B-0043](../backlog/items/B-0043-investigate-reusable-agent-semantics.md) DEFERRED, [B-0044](../backlog/items/B-0044-investigate-orchestration-control-loops.md) DEFERRED, [B-0035](../backlog/items/B-0035-investigate-tool-facing-capability-exposure.md) DEFERRED | Existing external Codex Agent and native Tool seams remain. Pinned origins/deferred calls identify integration questions, not an accepted generic Agent runtime. B-0029 is SUPERSEDED lineage. |
| CANDIDATE-07 — Simplify Tool declaration / argument validation / model-facing errors with typed reusable APIs or decorators | RELATED_NEEDS_EVIDENCE; [B-0035](../backlog/items/B-0035-investigate-tool-facing-capability-exposure.md) DEFERRED, [B-0036](../backlog/items/B-0036-investigate-action-request-semantics.md) DEFERRED | Schema preparation/validation-before-execution already partly exists; typed ergonomic comparison now grounded. ExternalToolset any_schema is not application schema validation. |
| CANDIDATE-08 — Evaluate simpler model-facing editing without sacrificing exact-source integrity | DISTINCT_PENDING_PROPOSAL; [88246171-d102-4b62-93d7-03c1e19f8a7b](../backlog/proposals/88246171-d102-4b62-93d7-03c1e19f8a7b/proposal.json) PENDING_REVIEW, [B-0033](../backlog/items/B-0033-investigate-semantic-repair-replanning.md) DEFERRED, [B-0035](../backlog/items/B-0035-investigate-tool-facing-capability-exposure.md) DEFERRED | New pending investigation distinguishes size/anchor/model/host failures and preserves exact authority. No adapter, patch rewrite or comparative run authorized. |
| CANDIDATE-09 — Make existing graph/map-assisted Context useful rather than merely callable | RELATED_NEEDS_EVIDENCE; [B-0002](../backlog/epics/B-0002-coding-context-substrate.md) BACKLOG, [ae03cda7-955e-40c6-a131-9e2ba209c9a6](../backlog/proposals/ae03cda7-955e-40c6-a131-9e2ba209c9a6/proposal.json) PENDING_REVIEW | Map/Planning/native opt-in navigation are implemented; model availability without invocation is not useful-adoption evidence. Existing CodeGraph proposal retains usability/effectiveness question. |
| CANDIDATE-10 — Reconcile code/context acquisition duplication and projection costs | RELATED_NEEDS_EVIDENCE; [B-0002](../backlog/epics/B-0002-coding-context-substrate.md) BACKLOG, [B-0008](../backlog/items/B-0008-investigate-repository-context-discovery.md) SUPERSEDED, [B-0035](../backlog/items/B-0035-investigate-tool-facing-capability-exposure.md) DEFERRED | ADR-0002/3/4/5 and source distinguish RI, retrieval, Localization, disclosure and source authority. No canonical duplication is proven merely by multiple representations. |
| CANDIDATE-11 — Durable task-local working state and verified progress/checkpoints | RELATED_NEEDS_EVIDENCE; [B-0028](../backlog/items/B-0028-investigate-persistence-durable-state-boundaries.md) DEFERRED, [B-0011](../backlog/items/B-0011-investigate-durable-execution-evidence.md) DEFERRED, [ae6b9374-f74d-4cd4-b079-a9f843ce3420](../backlog/proposals/ae6b9374-f74d-4cd4-b079-a9f843ce3420/proposal.json) PENDING_REVIEW | Working state/freshness is narrower than long-term Memory. Existing proposal receives advisory separation of task state, transcript and source authority; durable recovery needs domain-owned contract. |
| CANDIDATE-12 — Unify or explicitly separate experiment orchestration, coding task lifecycle, Checkout and WorkCycle | RELATED_NEEDS_EVIDENCE; [B-0044](../backlog/items/B-0044-investigate-orchestration-control-loops.md) DEFERRED, [B-0031](../backlog/items/B-0031-investigate-generic-execution-lifecycle-promotion.md) DEFERRED, [B-0032](../backlog/items/B-0032-investigate-execution-retry-mechanics.md) DEFERRED, [B-0034](../backlog/items/B-0034-investigate-uncertain-effect-reconciliation.md) DEFERRED | Existing source-specific Checkout/WorkCycle and deterministic experiment controllers are distinct. Shared run mechanics/failed transition audit pending; do not unify by name. |
| CANDIDATE-13 — Classify, document and delete verified disposable temporary artifacts and reconcile historical duplicate checkout paths | ALREADY_CAPTURED; [0385a359-399f-40bb-aed4-caf5239c9fc8](../backlog/proposals/0385a359-399f-40bb-aed4-caf5239c9fc8/proposal.json) PENDING_REVIEW | Existing pending proposal already covers exact-path custody/recovery qualification. ADVISORY update relates exact seed. No deletion/ACL change. |
| CANDIDATE-14 — Make architecture, production APIs, experiments and backlog navigable from one canonical index | ALREADY_CAPTURED; [B-0006](../backlog/items/B-0006-reconcile-authoritative-architecture-documentation.md) ACTIVE, [B-0001](../backlog/epics/B-0001-architecture-documentation-integrity.md) ACTIVE | Canonical doc map, research README, roadmap and existing active documentation reconciliation own this. Imported draft is not another authority/index. Detailed audit remains unfinished. |
| CANDIDATE-15 — Audit package layout, public facades, import cycles, naming, typed factories and justified syntactic sugar | RELATED_NEEDS_EVIDENCE; [39c6663a-bab7-43ed-8166-82e780a75d05](../backlog/proposals/39c6663a-bab7-43ed-8166-82e780a75d05/proposal.json) PENDING_REVIEW, [B-0035](../backlog/items/B-0035-investigate-tool-facing-capability-exposure.md) DEFERRED, [B-0019](../backlog/items/B-0019-investigate-typed-configuration-ownership.md) DEFERRED | Module-size investigation captures concrete pressure; import cycles/naming/factory duplication need measured examples before reusable abstraction. No package redesign authorized. |
| CANDIDATE-16 — Define specialized code-quality/maintenance/research agent roles under existing governance | INSUFFICIENT_REQUIRES_INVESTIGATION; [B-0043](../backlog/items/B-0043-investigate-reusable-agent-semantics.md) DEFERRED, [B-0044](../backlog/items/B-0044-investigate-orchestration-control-loops.md) DEFERRED, [B-0006](../backlog/items/B-0006-reconcile-authoritative-architecture-documentation.md) ACTIVE | B-0043 already records ResearchAgent/ExperimentManager and worker profiles. Separate report-only maintenance roles lack evaluated detection contracts/consumers; retain as role-specialization hypothesis rather than a generic Agent class or another broad ticket. |
| CANDIDATE-17 — Assess completeness of cancellation, exception and recovery paths across source/Tool/command/model operations | RELATED_NEEDS_EVIDENCE; [B-0032](../backlog/items/B-0032-investigate-execution-retry-mechanics.md) DEFERRED, [B-0033](../backlog/items/B-0033-investigate-semantic-repair-replanning.md) DEFERRED, [B-0034](../backlog/items/B-0034-investigate-uncertain-effect-reconciliation.md) DEFERRED, [B-0041](../backlog/items/B-0041-investigate-execution-local-lifecycle-control.md) DEFERRED, [B-0011](../backlog/items/B-0011-investigate-durable-execution-evidence.md) DEFERRED | Cancellation, semantic repair and uncertain effects have separate canonical children of superseded B-0014. New source/test observations support transition audit, not an asserted global cancellation defect. |
| CANDIDATE-18 — Keep sibling Learned Intelligence research/catalog independent of Devtools's experiment status | ALREADY_CAPTURED; [B-0006](../backlog/items/B-0006-reconcile-authoritative-architecture-documentation.md) ACTIVE | Existing charter explicitly separates Learned Intelligence repository/catalogs. Policy requirement is captured; no sibling source inspected, moved or counted. No cross-project ticket invented. |

Summary: 3 already captured adequately (13/14/18); 12 related with additional
evidence/scope qualification (01/02/03/04/06/07/09/10/11/12/15/17); 2 requiring
further investigation without an isolated verified defect (05/16); 1 distinct
pending proposal (08). No whole candidate is falsely marked superseded: only the
Commands subset of01 is verified source-adopted on main. No18 new-story creation,
new B-number, approval, parent completion or execution grant occurred.

## Intake changes and research evidence

New `88246171-d102-4b62-93d7-03c1e19f8a7b` remains PENDING_REVIEW, parent B-0003.
It investigates edit-interface ergonomics under strict existing admission, not
another editor or authorization mechanism. Four existing pending proposals got
ADVISORY evidence: module sizes `39c6663a-bab7-43ed-8166-82e780a75d05`, custody
`0385a359-399f-40bb-aed4-caf5239c9fc8`, Memory
`ae6b9374-f74d-4cd4-b079-a9f843ce3420`, and CodeGraph
`ae03cda7-955e-40c6-a131-9e2ba209c9a6`. Original payloads and prior reviews are
unchanged. Review duplicate candidates are incomplete lexical/resource aids,
not automatic merging. Canonical items gain attributed evidence appendices while
their metadata remains unchanged. Existing 16 proposal states are preserved;
the queue becomes17 (16 pending,1 approved) with valid chains.

The [current source/test comparison](agent-harness-mechanism-review.md) and
[initial adoption inventory](architecture-reconciliation-inventory.md) are the
supporting audit owners. No external code was installed, executed or adopted.
No production/tests, scientific receipts, historical outcomes or source authority
changed. Next external research is bounded DeepSeek Harness/Aider source and
tests, followed by deeper local lifecycle joins/adoption/custody; not launched here.

## Documentation checkpoint validation

The existing layout command passed. Focused existing layout/intake tests passed
36 cases in 1.67 seconds (`uv run pytest --no-cov
tests/scripts/test_validate_layout.py tests/scripts/backlog/test_intake.py -q`).
The bounded integrity review checked63 introduced local links/anchors,53 pinned
upstream path/line references and10 JSON documents; original member hashes and
all18 exact seed descriptions agree with the supplied manifests/source table.
Original canonical metadata and proposal dispositions/chains are preserved.
All13 forensic fingerprints match the prior custody record. Git whitespace
validation passes, including the scoped immutable-input hard-break attributes.

The32-file publication inventory and validation facts are retained in the
verification/crosswalk metadata. No `src`, `apps`, `tests`, `scripts` or
`experiments` tracked bytes changed. The full protected gate was not run for
this documentation-only checkpoint; neither were upstream tests, model inference
or scientific experiments. Source/test inspection is distinct from test execution.
