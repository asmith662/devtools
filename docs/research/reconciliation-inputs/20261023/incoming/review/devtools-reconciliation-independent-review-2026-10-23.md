# Devtools Reconciliation — Independent Checkpoint Review and Harness Research 01

**Date:** 2026-10-23  
**Disposition:** Preliminary source-grounded review, NOT an accepted architecture decision, implementation authorization, or completed repository audit.  
**Origin:** Independent ChatGPT review of supplied Devtools reconciliation reports and read-only inspection of pinned upstream Qwen Code/Pydantic AI source. No Devtools checkout, model inference, new repository clone, or external agent execution was performed.

## 1. Actual repository checkpoint (owner-supplied evidence)

The local Codex handoff reports feature `feat/qwen-context-worker` published at `3b2b3de845fbc0d8b510449bed9f492a54e39734`; remote protected `main` remains `5d979920d0728775ed529457c88f5b68b440c64f`. These Git identities are **reported**, not independently authenticated against the private repository here. The documentation-only checkpoint preserved original experiment receipts, 13 source-grounding forensics, and existing backlog/ADR authority. Its initial matrix differentiates source-on-main, feature-only code, historical experiments, actual consumers and tested results. The initial custody scan inventoried eight residual `.local/preserved-checkouts` directories with no Git marker, plus five synthetic nested Git fixtures. It did not establish cleanup safety. See uploaded `latest(20261023-130642).md`, `architecture-reconciliation-inventory.md`, `artifact-custody-inventory.md`.

**High-priority conclusions:**

- Main already contains Commands; do not reopen its successful merge. Substantial later Qwen Worker, Context Planning and Repository Intelligence changes remain feature-only and need capability-specific destination review, not wholesale feature-branch promotion.
- The current `observability` foundation is *not empty*: terminal/model Evidence, usage accounting, and bounded Commands events exist. Trace/Tool correlation, failed realization capture, durable evidence, exporter semantics, and actual native-worker adoption are unresolved research areas. An OpenTelemetry dependency or generic event bus would be premature without lifecycle/use-case verification.
- `context_tools.py`, `coding_loop.py`, and `development_task.py` have reported source sizes ~39KB/~72KB/~61KB, larger than the worker's ~32KB individual-resource limitation. Investigate justified modular ownership and developer ergonomics without automatically weakening admission limits or mechanically splitting files.
- One canonical checkout is preserved. Historical preservation directories and nested fixture repositories cannot be automatically labeled redundant clones or deletable caches. Archive/restore evidence must be authenticated before exact-path cleanup; same-SSD archives are not off-volume disaster recovery.

## 2. Original starter package recovered and verified in conversation runtime

The original package is available at `sandbox:/mnt/data/devtools-reconciliation-starter-2026-10-22.zip` **in the ChatGPT sandbox**. Its ZIP SHA-256 is:

`891d670922000782d75fc37bd45784990226fc41c486730f3a7b2d8a0a7c1cfd`

It contains these exact members; member hashes were independently recomputed and agree with its own MANIFEST:

| Member (under `devtools_transition/`) | SHA-256 |
|---|---|
| `01-reconciliation-charter.md` | `dd3835adc1e0a027eed2f76e604b15fdeb71ea32ba8e17f2051aaa54e7b45102` |
| `02-oss-harness-mechanism-review-initial.md` | `6f78e8bc81d80b034eef6ed30e7403886ea4df2e1a5c281f6a235806ad79ae55` |
| `03-audit-backlog-seeds.md` | `1d5142d0e0e25e0f472d2108922b963ee9d02ee48bfb92b106c6a013db4e5ab2` |

**Important distinction:** The user's local Codex process did not receive this ZIP and correctly reported unavailable input. ChatGPT sandbox visibility does not imply local Windows filesystem visibility. Transfer is needed before Codex can authenticate/deduplicate all 18 seeds. Do not claim repository-side import occurred yet.

## 3. Eighteen original story candidates: proposed routing, NOT authoritative deduplication

The original package contains 18 numbered candidates. The following preliminary crosswalk is based solely on their titles and the supplied *initial* backlog inventory, not inspection of canonical story bodies:

| Original candidate(s) | Domain | Existing story/pressure to inspect before intake |
|---|---|---|
| 01 | Selective production integration | Main/feature capability matrix, current B-0006, integration authority |
| 02, 10, 12 | Duplication, Context ownership, lifecycle reuse | Existing B-0029/30/31, B-0044/45 and B-0002; require source call-graph evidence |
| 03, 04 | Reusable observability, trace, usage | B-0023 tracing; B-0011 durable Evidence; distinguish three needs |
| 05 | Qwen inference/protocol/quant/model baseline | Existing model serving and interaction owners; do not create generic model harness based on guess |
| 06 | Multiple coding harnesses | Existing Agent/provider/runtime boundaries and B-0029/31/44/45 |
| 07, 15 | Typed Tool ergonomics, public package facades/decorators | Existing B-0035/36 and package docs; check real duplication before genericization |
| 08 | Alternative model-facing editing | Existing source admission/edit diagnostics, Engineering 19/22/26/28; preserve exact candidate integrity |
| 09 | Operational graph/map Context | B-0002 and established navigation consumers; separate enabled Tool from measured adoption |
| 11 | Durable task-local working state | Existing memory/wiki/procedural skills proposals; separate task state from repository evidence |
| 13 | Custody-aware cleanup | Newly captured proposal `0385a359-399f-40bb-aed4-caf5239c9fc8` |
| 14 | Documentation/index | B-0006; maintain existing docs map, research inventory, backlog as authorities |
| 16 | Specialized maintenance/code-quality agents | Agent architecture backlog, new proposal only if truly unmatched |
| 17 | Cancellation, errors, recovery | Terminal Evidence, ToolRunner, Commands, Checkout; source-backed bug/maintenance qualification |
| 18 | Learned Intelligence repository distinction | Existing reconciliation policy: do not merge separate scientific catalogs |

**Do not approve or create 18 new IDs by arithmetic.** Inspect proposal hashes, exact bodies, existing parent relationships and review history; update advisory reviews or add new intakes only for distinct unmet outcomes.

## 4. Independent upstream source findings — Qwen Code

**Pinned revision:** `a98615bedbe1ef0ab5e343de7471b06bfd79014d`. Primary files:

- [`packages/core/src/core/turn.ts`](https://github.com/QwenLM/qwen-code/blob/a98615bedbe1ef0ab5e343de7471b06bfd79014d/packages/core/src/core/turn.ts)
- [`packages/core/src/core/client.ts`](https://github.com/QwenLM/qwen-code/blob/a98615bedbe1ef0ab5e343de7471b06bfd79014d/packages/core/src/core/client.ts)
- [`packages/core/src/services/tool-exploration-budget.ts`](https://github.com/QwenLM/qwen-code/blob/a98615bedbe1ef0ab5e343de7471b06bfd79014d/packages/core/src/services/tool-exploration-budget.ts)
- [`packages/core/src/services/loopDetectionService.ts`](https://github.com/QwenLM/qwen-code/blob/a98615bedbe1ef0ab5e343de7471b06bfd79014d/packages/core/src/services/loopDetectionService.ts)
- [`packages/core/src/services/microcompaction/microcompact.ts`](https://github.com/QwenLM/qwen-code/blob/a98615bedbe1ef0ab5e343de7471b06bfd79014d/packages/core/src/services/microcompaction/microcompact.ts)

### Direct observations

1. `turn.ts` models `ToolCallRequestInfo` with provider ID, call ID, prompt/response IDs, tool arguments, incomplete-argument indicators and **in-process tool-execution origin**. Origin distinguishes model/client/fixed-policy and explicitly does not trust model argument data for authorization; missing origin defaults to least-privileged model. This is relevant to Devtools model-vs-supervisor provenance and standing delegated authority, but is **not** proof that Qwen Code matches Devtools's Checkout/WorkCycle safeguards.
2. `Turn.run` processes retry events by clearing partial pending Tool calls, clearing metadata and reestablishing a clean stream state. On model fallback it also discards prior partial tool calls and tracks the model transition. It emits separately typed Thought, Content, ToolCallRequest, ChatCompressed and Error events. This separation is a candidate comparison target for Devtools's `ModelInteraction`, terminal/model Evidence and trace correlations.
3. `tool-exploration-budget.ts` classifies read/search/fetch exploration and emits a *non-authorizing reminder* after an allowance; it resets when a non-read operation occurs. It does **not** simply kill the agent after a fixed number of read requests. This is relevant to Engineering 16–28 repeated discovery, but its empirical effectiveness has not been demonstrated here.
4. `loopDetectionService.ts` distinguishes identical Tool-call/content repetition; it contains a threshold for repeated identical calls. The guard behavior and false positives must be assessed in its tests before adoption.
5. `microcompact.ts` has tool-specific old-output elision and distinguishes file-touching Tool results so eviction is not silent. This is a useful design cue but potentially dangerous if copied into Devtools without source observation/version preservation. The exact editor authority is not transferable merely by compaction.

### Research implications, NOT decisions

- Compare normalized Tool/Turn states and model-versus-host provenance with current Devtools without introducing a second permission system.
- Compare a soft, phase-aware exploration reminder to Devtools's capacity/turn bounds; do not prematurely adopt automatic prompt steering without evidence.
- A common trace may need to relate Tool events across model request, Retry, Host validation and WorkCycle, while preserving distinct evidence strengths.
- Inspect provider adapters, scheduler, permission manager, and tests before making a harness adoption recommendation.

## 5. Independent upstream source findings — Pydantic AI

**Pinned revision:** `d97c25c6d749b121494c28684273a3df37955803`. Primary files:

- [`pydantic_ai_slim/pydantic_ai/_agent_graph.py`](https://github.com/pydantic/pydantic-ai/blob/d97c25c6d749b121494c28684273a3df37955803/pydantic_ai_slim/pydantic_ai/_agent_graph.py)
- [`pydantic_ai_slim/pydantic_ai/tool_manager.py`](https://github.com/pydantic/pydantic-ai/blob/d97c25c6d749b121494c28684273a3df37955803/pydantic_ai_slim/pydantic_ai/tool_manager.py)
- [`pydantic_ai_slim/pydantic_ai/_tool_execution.py`](https://github.com/pydantic/pydantic-ai/blob/d97c25c6d749b121494c28684273a3df37955803/pydantic_ai_slim/pydantic_ai/_tool_execution.py)

### Direct observations

1. `ToolManager.validate_tool_call()` explicitly validates arguments **before** execution, enabling model-visible validity status and separate handling for validation versus execution errors. `execute_tool_call()` follows a separate boundary. This is a candidate for simplifying Devtools developer-facing Tool definitions, not authorization to give Pydantic the final source-edit grant.
2. Validation errors and explicit `ModelRetry` can be turned into structured retry feedback with a **per-Tool bounded retry counter** and final `UnexpectedModelBehavior`. Invalid output remains possible: the system detects, accounts for and handles it rather than guaranteeing the model cannot generate errors.
3. `_tool_execution.py` distinguishes function/output Tools and supports ordered strategies (`early`, `graceful`, `exhaustive`), parallel groups and sequential barriers. This demonstrates concrete orchestration ownership not provided merely by typed `@tool` functions. It also makes cancellation/side effects important to compare before reuse.
4. `_agent_graph.py` imports OpenTelemetry tracer and instrumentation helpers and represents an agent-level graph with model requests, Tool calls, usage, output validation and result handling. These should inform an observability gap comparison; a source import alone does not prove complete, durable, reliable cross-process traces or cost accuracy.
5. Agent-specific graph nodes and Tool Manager are **different abstractions** from Devtools's narrower single-invocation Runtime plus domain-specific Qwen loop. Do not assume replacing Runtime with a generic Agent class is necessary without consumer analysis.

### Research implications, NOT decisions

- Investigate typed schema generation, dynamic Toolsets, validation decorators and readable Tool failures, but preserve existing ToolRunner's execute-once and Checkout authority.
- Inspect actual Pydantic AI tests for retry counting, cancellation, deferred/approved tools, validation failure observability and usage accounting before selection.
- Compare explicit Tool validation/execution separation to present Devtools Tool definitions and event capture; avoid a second independent execution owner.

## 6. Provisional priorities after this checkpoint

1. **Transfer/reconcile original ZIP** into current canonical documentation/backlog using its verified manifest; do not create a parallel authority or accept all 18 as new stories.
2. Complete **Qwen Code and Pydantic AI source-and-test mechanism comparison** at the pinned revisions, cross-referencing actual Devtools component owners. Record observed vs inferred vs proposal.
3. Complete **observability/lifecycle correlation audit** end-to-end: objective/agent run -> model request -> Tool -> source edit -> validation -> WorkCycle. Keep evidence, live event, usage measurement and causal trace distinct; do not add an OTel exporter until a concrete consumer exists.
4. Continue **production adoption and preservation/cleanup** review: selective destination diffs and exact archive/member/recovery proofs, not full ancestry merge or recursive deletion.
5. Audit developer ergonomics (large worker modules, repeated helpers, facades, justified base classes/decorators) after the ownership/call graph is grounded.
6. Prepare a **comprehensive successor-chat handoff** only when the finite review has sufficient source-backed findings and pending questions.

### Explicitly not authorized

No Qwen experiments, new clones/worktrees, feature promotions, destructive cleanup, generic Agent/Trace implementation, automatic backlog approval, or broad source refactoring merely because this document exists.

