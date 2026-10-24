# Devtools — Research, Architectural Reconciliation, and Session Transition Charter

**Working status:** Proposed coordination charter; not an accepted ADR, source inspection report, cleanup authorization, or backlog closure.  
**Date:** 2026-10-22  
**Program center:** `devtools` — one canonical repository checkout and ordinary feature branches only.  
**Current conversation's role:** Researcher, independent architectural reviewer, synthesis steward, and eventual successor-session handoff author. Codex remains the authorized local source-inspection/documentation worker, not the decision-maker for architecture-sensitive changes.

## 1. Why we are changing direction

After many substantial Devtools increments, the codebase contains functioning repository intelligence, retrieval, Context planning, model interaction, source editing, execution, validation, evidence and lifecycle capabilities. Nevertheless, end-to-end local coding-agent completion is not yet dependable. Repeated attempts have produced useful evidence and software, but the focus on consecutive narrowly frozen Qwen assignments prevented a systematic review of whether our foundations, model/harness configuration, reusable infrastructure and production integration form a cohesive system.

The previous omnibus Deep Research report raised legitimate questions but was insufficiently precise for architectural decisions. We will research relevant open-source implementations **ourselves**, in this ChatGPT conversation, at verifiable source/documentation boundaries; keep the research cumulative; reconcile Devtools' history and actual source; capture issues as backlog proposals rather than interrupting every investigation for a fix; and prepare a complete transition to a fresh ChatGPT conversation soon.

This is a **finite reconciliation phase**, not indefinite feature suspension, another parallel experimental codebase, or permission to build a generic framework before studying current ownership. Priorities are to recover understanding, strengthen the foundations, identify what is already built but unused, and arrive at a coherent, evidence-based implementation direction.

## 2. North star and boundaries

Devtools is the current practical implementation center for a larger OpenMind/Continuum ambition: governed agents that can acquire, compose, evaluate, revise and retire capabilities, learn from validated experience, and carry substantial work through independently reviewed delivery. Autonomous software engineering is the present vertical slice, **not** the long-term ceiling.

Model neutrality is a requirement: Qwen and future local/remote planners, coders, reviewers and maintenance agents should share governance, repository truth, Tool contracts, validation and observability. We should not automatically preserve a Qwen-specific agent loop when a proven OSS harness could do better, but also should not replace valuable typed, source-bound domain infrastructure merely to adopt another runtime.

**Non-negotiable constraints:**
- Only the one canonical Devtools checkout. No Git worktrees, backup clones, duplicate source directories or shadow repositories. Ordinary feature branches are permitted.
- Preserve original experiment inputs, negative results, model calls, source fingerprints, receipts and scientific/engineering provenance. Never relabel Codex code as Qwen success.
- No automatic protected-main promotion or backlog parent closure; review and existing grants remain authoritative.
- Keep authorization and observation distinct: model Tool requests and map metadata do not confer source-edit or command-execution authority.
- Research/documentation may proceed without a full protected test gate; source behavior changes require their proper validation.
- No automatic Qwen coding experiment or large foundational refactor until its purpose follows the research and reconciliation decisions.
- Avoid repeatedly asking the user to run manual diagnostics or multiline PowerShell sequences. Prefer one bounded Codex assignment to inspect, document, verify, commit and push coherent increments.

## 3. Overall method and decision rules

1. **Document the program and current evidence** before researching alternatives. This charter is the first deliverable.
2. **Research external OSS implementations** in focused increments in this same chat, comparing specific mechanisms against *actual* Devtools owners. Include source paths, revisions, tradeoffs, limitations, and actionable findings; no README-only architecture decisions.
3. **Inventory and reconcile historical experiments** with current maintained source, tests, consumers, docs and protected main. Preserve negative and inconclusive outcomes. Separate "implemented on feature branch" from "integrated into protected main" and "actively consumed by a production workflow."
4. **Audit the framework at multiple levels**: overarching flow, subsystem contracts, package/module ownership, shared utilities, duplicated mechanics, APIs, ergonomics and concrete dead/temporary artifacts.
5. **Create backlog proposals as we discover things** rather than letting each finding interrupt the audit. Classify risk, evidence and prerequisites, then batch/refine/prioritize after related areas are understood.
6. **Promote only decisions, not hunches.** An external framework's attractive feature is a candidate, not an architectural mandate. Review provenance, existing overlapping abstractions, integration cost and model-neutral compatibility.
7. **Complete a successor-chat handoff** containing authoritative repository state, research verdicts, backlog, accepted/rejected decisions, workflow constraints and the next bounded assignment. Close this long conversation after that handoff is checked, rather than letting it become another indefinite implementation chat.

Each increment must label statements:
- **Verified repository fact:** actual source/commit/test or local Codex inspection.
- **Historical receipt:** prior handoff or experiment artifact, not reverified against current source.
- **External documented fact:** linked OSS source and version/revision.
- **Hypothesis / improvement opportunity:** not proven; merits a story, experiment or decision.

## 4. Research tracks (this conversation)

### R1 — Open-source agent harnesses and developer interaction

Study **Qwen Code, Pydantic AI, DeepSeek Harness, Aider, OpenHands, SWE-agent/mini-SWE-agent**, and selected additional credible frameworks if relevant. Prioritize how the runtime actually works:
- model adapters, reasoning channels, chat templates and typed Tool schema generation;
- Tool registry/composition, approval/permission hooks, result correlation and recovery;
- source navigation, editing/patch workflows, shell/process access and safety;
- session/turn/event lifecycle, provenance, tracing, logging, budgets and cancellation;
- context compression, task-local working state, plans and memory;
- agent/harness interoperability: ACP, SDK, MCP, headless APIs and governance seams;
- extensibility (plugin systems, decorators, capability packs), tests, licensing and supply chain.

Deliver one evidence-grounded research file per major subject, then a comparative synthesis. Source-revision pinning is necessary for final decisions; a live `main` link alone is a provisional source.

### R2 — Model/serving correctness and model-neutrality

Audit the **actual installed** Qwen3.8 GGUF identity, quantization, 32K window, thinking disabled, chat template, tool parser, sampling, KV cache, context reserve and llama.cpp startup/versions before deciding what model configuration to test. Research alternative quantizations/models and context feasibility without assuming advertised capacities imply quality on 16GB VRAM. Compare mature Qwen Code harness using the *same weights and server* before declaring Qwen's model incapable.

No presumption that Pydantic AI automatically solves semantic tool mistakes or that an apply-patch schema is inherently safer. Distinguish model-facing ergonomics from the host's established exact-source transaction authority.

### R3 — Experiment/repository adoption and historical cleanup

Enumerate experiments, direct-production modules, feature publications, tested but unused infrastructure, scientific reference implementations and temporary assets. Trace code, tests, actual consumers, source revisions and protected-main incorporation. Classify each item's recommended disposition; do not infer it from a "PASS" receipt alone.

### R4 — Architecture cohesion and developer experience

Inspect end-to-end data/control/evidence flow and each module's actual purpose, identify duplicated parsing/ranking/provenance/validation/logging, shared protocol candidates, inconsistent naming, API friction, ergonomics, well-founded decorators/context managers/typed wrappers, package boundaries, central indexes and discovery. Do not introduce a base class solely because two functions are similar; abstractions should be justified by stable contracts, consumers and clear duplication removal. Likewise, don't defer mature standard infrastructure merely because a second consumer has not appeared.

### R5 — Observability and eventual quality-maintenance agents

Audit what `observability` actually implements today versus logger helpers, model-interaction evidence, ToolRunner receipts, WorkCycle, usages, and experiment traces. Determine whether there is a coherent reusable telemetry/event/tracing substrate and why it is or is not used. Backlog the missing pieces before any generic tracing implementation. Evaluate future specialist maintenance roles (source ownership auditor, duplication/refactor analyst, dependency/update auditor, documentation/index steward, experiment custody/promoter, observability verifier) subject to existing governance.

## 5. End-to-end audit map

Trace real code and real events through:

**Goal → backlog/work item → task authority → repository/snapshot observation → RI/graph/retrieval → Context need/selection/materialization → model request and reasoning → Tool proposal → ToolRunner permissions → source/command execution → validation and repair → independent review → Git publication/promotion → observability → working memory/experience → next work item.**

At each handoff, record:
- authoritative owner and its public entrypoint;
- input/output semantic types, identity/provenance, scope and validity;
- caller(s), observed real consumer(s) and integration maturity;
- error handling, recoverability, state/cancellation and idempotence;
- test/diagnostic/trace coverage;
- reused library versus duplicated implementation;
- developer ergonomics and discoverability;
- missing or ambiguous contract;
- backlog proposals, not immediate patches.

Cross-check from three perspectives: **top-down lifecycle**, **horizontal subsystem boundaries**, and **bottom-up library/module patterns**. A fourth view follows one real successful and one failed engineering task through every event/log/receipt to test whether the architecture's intended seams actually work.

## 6. Experiment and production disposition vocabulary

Apply separately to every relevant feature/experiment:

| Axis | Values or questions |
|---|---|
| Scientific/behavioral result | Supported, negative, limited, inconclusive, not measured; immutable original receipt |
| Implementation | Design/research only, experimental code, maintained library, application-only, superseded candidate |
| Integration | No consumer, tests only, application-used, feature branch, protected main, external/sibling usage |
| Adoption risk | Safe reusable, dependencies incomplete, semantic mismatch, needs destination validation, blocked by governance |
| Artifact custody | Original evidence, needed for reproduction, replicated/verifiable, disposable generated cache, unknown ownership |
| Action | Retain, add consumer, consolidate, promote selectively, refactor, fix, archive, delete only after custody and explicit approval |

**Important:** `Learned Intelligence` is a separate sibling project and its B-0001–B-0053 experiment catalog, `src/learned_intelligence`, and `.tmp` cleanup data must not be silently counted as Devtools experiments or transferred into Devtools production. Record genuine cross-project dependencies without conflating histories.

## 7. Candidate audit hotspots, not asserted current defects

1. **Observability:** reusable event/trace context, correlation, span hierarchy, Usage and ModelInteraction evidence, emitters/exporters, privacy and retention, cost/time and human-debug views. Historical logging may have grown locally instead of through a deliberate common contract. Inspect first.
2. **Model/agent neutrality:** current `models/interaction`, serving/providers, `agents`, `runtime`, application Qwen code and ToolRunner boundaries. Identify Qwen-only assumptions and avoid duplicate model adapters.
3. **Context/RI/retrieval overlap:** candidate selection, BM25, graph map, source index, SourceSearch, progressive disclosure, ContextTools navigation and model-facing Tool naming; actual worker utilization versus API existence.
4. **WorkCycle/review and experiment orchestration:** repeated source/authentication, checks, reporting, commit/branch tracking, lifecycle edges, failure recovery, existing backlog pipelines and experiment managers.
5. **Developer tools and public APIs:** typed tools, validated decorators, data-class factories, parser/CLI ergonomics, test fixtures, no-op boilerplate, canonical command locations, discoverability and consistent output/exception idioms.
6. **Directory hygiene:** root `docs`, `src`, `apps`, `scripts`, `tests`, `experiments`, reports, evaluation artifacts, ignored `.local` and historical `.local/worktrees`; classify each, never create another checkout.
7. **Portable system capabilities:** paths, commands, time, model serving, filesystem, persistence, runtime/execution, typed contracts and code quality rules; find duplicated mechanics and clear package ownership.
8. **Documentation/indexes:** current architecture vs actual code, accepted ADRs, research status, backlog story indices, experiment ledgers, navigational README and stable Codex handoff.
9. **Maintenance-agent backlog:** repeatable audits, code-quality drift, unused functionality, overgrown packages, stale docs and empirically valuable refactoring candidates.

These are leads justified by the project history, **not** code-inspection findings. Every story must specify what still needs verification.

## 8. Backlog story schema and intake policy

Use the repository's **existing authoritative backlog** and ID conventions rather than inventing a parallel system. Each proposed story must contain:

- Title and **type**: `FEATURE`, `ENHANCEMENT`, `BUG`, `MAINTENANCE_REFACTOR`, `INTEGRATION_PROMOTION`, `DOCUMENTATION_INDEX`, `OBSERVABILITY`, `CUSTODY_CLEANUP`, `SECURITY_GOVERNANCE`, or `RESEARCH_DECISION` (map to current categories as needed).
- Problem/impact and current behavior, not just a solution slogan.
- Grounded owner(s), source paths, known consumers, actual evidence references and current Git status.
- Suspected cause versus verified finding; consequences and risks.
- Candidate solution(s), reuse opportunities, constraints and architecture decision prerequisites.
- Acceptance criteria and what would falsify the issue or demonstrate resolution.
- Relative priority, dependencies, scope, likely effort, and whether user architecture approval is required.
- Disposition: proposed / qualified / approved / implemented / validated / integrated / closed, preserving historical statuses.

At first, record **candidates**, not fabricated completed tickets. Deduplicate against the existing backlog, attach to existing parent goals, and update indices. Documentation research continues without implementing each item.

## 9. Cleanup and repository organization rules

- Inventory before changes, including ignored/untracked directories and old worktree remnants; prove current owners, whether files are sole copies and whether process/log/experiment evidence depends on them.
- Never delete an experiment's only raw source, failed trace, original frozen oracle, signed/hashed report or source provenance.
- Classify `ACTIVE`, `BLOCKED`, `COMPLETED`, `REOPENED`, `HISTORICAL`, `CANDIDATE_DELETE` separately from feature acceptance.
- Temporary generated files may be removed **after** reproducing exact path/size/membership, confirming no live process or active Checkout owner, checking `.gitignore` and reuse, and recording authorization and audit evidence. No blanket `rm -rf`, root clean sweep or uncontrolled rewrite.
- Eliminate duplicate folders/worktrees rather than adding new clones; reconcile surviving legitimate work through ordinary branches in the single checkout.
- Documentation and manifests remain discoverable through existing indexes; do not keep duplicate, conflicting authoritative status files.

## 10. Current known checkpoint (historical, source re-verification required)

Last provided `native-map-28` handoff reported:
- `feat/qwen-context-worker` remote HEAD `3c09641dd17b13b83c2fe84e3f1cf4920ca7186f`.
- Protected `main` `5d979920d0728775ed529457c88f5b68b440c64f`, including Commands PR #1.
- Model Qwen3.8-27B UD-IQ4_XS, 32K, q4 K/V, thinking off; native attempt 19 requests, five proposals (four admitted), behavioral/typing failures, no actual map or `check_changes` invocation, later Context-budget refusal. A separate Codex-authored scoped-search implementation was feature-published; 2,663 protected tests passed, 2 skipped, with required 100% production branch coverage.
- Earlier Engineering 25 delivered genuine Qwen-authored correct Localization role code, but the live `check_changes` result was blocked by host-created untracked evaluation artifacts; subsequent supervised exact-source validation/publication did not rewrite the original failure.
- Engineering 26 demonstrated diagnostic-guided size-refusal recovery and exposed a no-final-newline Git patch defect subsequently corrected by Codex.
- Engineering 27 delivered map-to-source progressive Context via Codex; native Qwen made zero edits.
- Additional earlier `run_check(all)`, `check_changes`, SnapshotDelta, RI configuration, map and navigation APIs were published to **a feature branch**; do **not** assume incorporation into protected main, actual worker use, or operational observability without inspecting current source.

These are handoff-derived checkpoints, not today's independent Git verification. The next Codex inspection must list all relevant source/commit statuses and parent ancestry precisely.

## 11. Research cadence and file protocol

1. Charter/strategy captured and committed to canonical docs/maintenance or architecture-reconciliation area.
2. First **source-level** comparative review: Qwen Code, Pydantic AI and DeepSeek Harness, with links to actual mechanisms, evidence classifications and Devtools applicability. Aider and others follow.
3. Continue focused research (tool/edit/Context, serving/quantization/model alternatives, observability) and append to stable research documents. If source revisions cannot be pinned remotely, label citations as moving-branch evidence pending local pinning.
4. Parallel *read-only* Codex inventory of the canonical checkout and backlog indexes after the charter is recorded. The inventory should be thorough, but report status incrementally; it does not fix or delete findings.
5. Review candidate stories together, merge into the existing backlog, and update indexes/architecture diagrams where source facts justify it.
6. As needed, authorize separate coherent infrastructure/production promotions; do not derail the research stream with opportunistic repairs.
7. Finish with successor-chat handoff verified against current Git and accepted research.

Each increment must be persisted as a repository Markdown source or maintained register, with dated revision and source links. Do not depend on terminal scrollback or this chat as the only storage.

## 12. Handoff criteria

Before ending this long ChatGPT conversation, create a coherent successor artifact containing:
1. Long-term vision and current Devtools role.
2. Active source revision, branches and main integration state, explicitly verified.
3. Accepted ADRs and major design boundaries.
4. Subsystem ownership map and end-to-end lifecycle map.
5. Canonical experiment inventory, original outcomes, maintained-library adoption and unresolved production promotions.
6. OSS research completed, external references/revisions, accepted conclusions, rejected claims and open questions.
7. All newly created/deduplicated backlog stories by ID and category, prioritized with dependencies.
8. Observability/trace architecture audit findings and other foundation/DX issues.
9. Experiment/evidence custody, temporary-directory cleanup status and any destructive actions explicitly approved/performed.
10. Current testing/protected validation and remaining source uncertainty.
11. The next clearly bounded Codex engineering/research assignment and relevant stable handoff paths.
12. Non-negotiable single-checkout, governance, model-attribution and process instructions.

The goal of this phase is **recovered system understanding and a cohesive roadmap**, not a particular number of code commits or an artificial end-to-end Qwen success.
