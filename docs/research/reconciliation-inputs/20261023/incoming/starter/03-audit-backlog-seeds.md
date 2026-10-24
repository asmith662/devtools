# Devtools — Initial Reconciliation Backlog Candidates

**State:** Intake seed list created from the user's direction, historical handoffs and first external mechanism review. **These are not verified code defects, accepted architecture decisions or assigned canonical backlog IDs.** Deduplicate each against the repository's existing backlog before publishing; replace `CANDIDATE-xx` with authorized IDs, add source evidence, and preserve existing parent work. Date: 2026-10-22.

Every item deliberately describes an **investigation and acceptance boundary**, not an automatic permission to refactor. Source paths are leads unless explicitly supported by a prior handoff; Codex must verify actual revisions/consumers/tests.

| Seed | Type | Suspected gap / value | Initial evidence or trigger | Investigation/acceptance before approval |
|---|---|---|---|---|
| CANDIDATE-01 | INTEGRATION_PROMOTION | Reconcile successful feature-branch capabilities with protected main and actual application consumers | Commands PR #1 merged main; many Context/RI/validation/worker increments feature-published only | Build exact Git lineage and capability matrix; identify complete dependencies, destination behavior/tests and safe bounded integration groups; never bulk merge Qwen/experiment ancestry |
| CANDIDATE-02 | MAINTENANCE_REFACTOR | Inventory repeated domain semantics and utility implementations across apps, tools, Context, agents and runtime | Project grew rapidly across vertical slices | Show actual overlapping code paths and tests; identify one canonical owner, migration/caller compatibility and measurable deletion/ergonomics benefit; avoid speculative base classes |
| CANDIDATE-03 | OBSERVABILITY | Establish a reusable, model-neutral observability/event/tracing contract if the present module is fragmented | User reports mostly-empty observability package; existing evidence and usage, per-run logs and scientific receipts are fragmented | Inventory `observability`, `evidence`, `usage`, model-serving, ToolRunner, WorkCycle, experiments; map correlation/events/spans/OTel/retention/redaction; define smallest coherent production contract and first consumers before implementation |
| CANDIDATE-04 | OBSERVABILITY | Unified end-to-end agent trace and cost/time visibility | 19–28 Qwen experiments repeatedly lacked paid Codex coordination cost, active supervision time, full GPU/RAM/energy | Specify trace scope across task, model request, Tool, source edit, validation, review, publication; what is locally measureable versus unavailable; sensitive data capture control and queryable timeline; tests/OTel compatibility |
| CANDIDATE-05 | RESEARCH_DECISION | Verify Qwen thinking, template/tool protocol, quantization, KV cache and context against official recommendations | Current Qwen3.8-27B UD-IQ4_XS 32K q4 KV thinking-off, mixed quality and Context failures | Source-level model/llama.cpp configuration audit, full raw Tool round-trip, same-model controlled thinking baseline and hardware feasibility; no new RI task during reconnaissance |
| CANDIDATE-06 | FEATURE_ENHANCEMENT | Make specialized coding harnesses usable through common governed boundaries | Qwen Code core/ACP/SDK; Pydantic ExternalToolset; existing Devtools ModelToolDefinition + ToolRunner | Compare actual source and approval/edit authorities; propose agent-runtime interface only for demonstrably missing seam; show no competing Checkout/WorkCycle; controlled same-model harness comparison |
| CANDIDATE-07 | DEVELOPER_EXPERIENCE | Simplify Tool declaration / argument validation / model-facing errors with typed reusable APIs or decorators | Pydantic AI FunctionToolset/ModelRetry/ToolFailed and current custom Tool schemas | Audit current serialization/validation duplications; measure syntax versus semantic errors from native receipts; design transparent decorator/typed wrapper only if decreases boilerplate without changing authority |
| CANDIDATE-08 | ENHANCEMENT | Evaluate simpler model-facing editing without sacrificing exact-source integrity | Engineering19/22/26/28 Qwen edit refusals and one real-Git EOF host bug; Aider editblock | Compare same model/tasks using established `replace_source` and alternative `apply_patch`/search-replace façade; host translates only when semantically exact; retain atomic validation, bytes, version, scope, restoration; do not replace eagerly |
| CANDIDATE-09 | ENHANCEMENT | Make existing graph/map-assisted Context useful rather than merely callable | Engineering28 native `repository_map` available but never invoked; Aider includes compact repo map with change requests | Verify model-facing descriptions, orientation size, Tool overlap, retrieval quality; measure task owner discovery/repeated reads, not forced Tool use; avoid another graph engine |
| CANDIDATE-10 | MAINTENANCE_REFACTOR | Reconcile code/context acquisition duplication and projection costs | RI, lexical/BM25, graph map, source index, Planning, ContextTools navigation, many repeated source reads | Build call graph/ownership; distinguish ranked candidates, native provenance, source authority, disclosure; identify duplication and missing multi-granularity consumers; propose canonical reusable operators only when semantics align |
| CANDIDATE-11 | FEATURE_ENHANCEMENT | Durable task-local working state and verified progress/checkpoints | Qwen misremembered applied edits; 32K Context refills after read/edit/validation; historic memory roadmap | Specify exact source/version/edit ledger versus summarizable plan/facts; atomic checkpoints, freshness and restoration; avoid duplicating model traces, repository store or long-term memory |
| CANDIDATE-12 | MAINTENANCE_REFACTOR | Unify or explicitly separate experiment orchestration, coding task lifecycle, Checkout and WorkCycle | Repeated run preparation, frozen oracles, source authentication, review and publication | Inspect established pipeline owners and backlog/control interfaces; find duplicated state transitions, absent error path and unnecessary revalidation; preserve approvals and immutability |
| CANDIDATE-13 | CUSTODY_CLEANUP | Classify, document and delete verified disposable temporary artifacts and reconcile historical duplicate checkout paths | Existing `.local` evidence, previous `.local/worktrees` concern, generated test/execution scratch | Inventory ignored/untracked/branch assets, ownership and sole original evidence; no active processes; reviewed exact-path deletion with hashes/custody and approval; never delete whole `.local` or frozen receipts blindly |
| CANDIDATE-14 | DOCUMENTATION_INDEX | Make architecture, production APIs, experiments and backlog navigable from one canonical index | Many report/README/hand-off snapshots; accepted ADRs and archived experiments span directions | Find authoritative indices; cross-link known owners and statuses; remove/confine misleading duplicate status docs; provide developer-facing package capability map and examples |
| CANDIDATE-15 | DEVELOPER_EXPERIENCE | Audit package layout, public facades, import cycles, naming, typed factories and justified syntactic sugar | Context planning/retrieval circular-import accommodations, specialized apps and repeated Test fixtures | Inspect imports/API/entrypoints, classify intentional layering vs accidental nesting; propose clearer modules/base/decorators where contracts demonstrably stabilize; protect compatibility |
| CANDIDATE-16 | FEATURE_ENHANCEMENT | Define specialized code-quality/maintenance/research agent roles under existing governance | User wants proactive duplication, unused capability, documentation and infrastructure stewardship | Specify non-mutating detection/reporting roles first, proposal evidence, false-positive control, human-approved fixes, reproducibility and scope; do not create self-modifying general agent prematurely |
| CANDIDATE-17 | BUG_OR_MAINTENANCE | Assess completeness of cancellation, exception and recovery paths across source/Tool/command/model operations | Proven host blockers in Engineering25/26 and source identity strictness; Windows subprocess risks | Audit transition/error matrix with actual logs, owner recovery, temporary effects, subprocess cleanup and repeated validation; distinguish actual bug from intentionally strict guard |
| CANDIDATE-18 | DOCUMENTATION_RESEARCH | Keep sibling Learned Intelligence research/catalog independent of Devtools's experiment status | Prior records mention B-0001–0053 and `src/learned_intelligence`; separate repo from `devtools` | Mark cross-project references, imports and intended integration boundaries; do not count sibling source as Devtools production or clear its `.tmp`/scientific evidence during Devtools cleanup |

## Proposed audit order (no immediate fixes)

1. **First:** recover actual docs, current branch/production adoption and manifest/custody/index surfaces; verify which checklist findings already have tickets.
2. **Next:** source-level external harness research + exact core model/Tool/Context and observability substrate inventory.
3. **Then:** complete end-to-end lifecycle map and redundancy/API-ergonomics audit; refine candidate stories with exact implementation evidence and dependencies.
4. **Then:** inspected experiment promotions and cleanup proposals, selective integrations and explicit architecture decision records.
5. **Before successor handoff:** reconcile status, priority, handoff links and next bounded executable assignment.

## Story acceptance template

```markdown
### [Repository ID]: [short factual title]
Type: ...     Status: PROPOSED / QUALIFIED / APPROVED / ...
Parent goal / capability: ...
Problem and why it matters: ...
Observed behavior and evidence: exact commit/source path/test/log/published reference
Existing owner and downstream consumers: ...
What is known, hypothesized and unverified: ...
Options and integration/compatibility consequences: ...
Risks, governance, custody and model-neutral concerns: ...
Acceptance criteria and anti-goals: ...
Dependencies and architecture/user approval needed: ...
Verification commands (repository-owned, bounded): ...
Documentation/index updates on resolution: ...
```
