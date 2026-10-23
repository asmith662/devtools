# Agent harness mechanism review: initial source cursors

## Disposition

Initial source-reference collection, 2026-10-23. Detailed comparative research is
the next assignment, not a completed result here. No external architecture is
adopted, no harness was installed/executed, and no model comparison or scientific
experiment was launched. This is Codex-authored research preparation, **not** an
import of the unavailable `02-oss-harness-mechanism-review-initial.md`.

The [reconciliation charter](../development/reconciliation.md#finite-architecture-and-research-reconciliation-2026-10-23)
governs the finite phase. Existing ADRs and source ownership remain authoritative.
The [Devtools source inventory](architecture-reconciliation-inventory.md) supplies
the local comparison baseline; upstream names do not redefine Devtools taxonomy.

## Collection method and limits

Remote HEADs were queried with `git ls-remote`. Individual files were read through
the primary GitHub contents API at those revisions, preserving blob/SHA-256/size
metadata in [the source cursor record](agent-harness-source-cursors-20261023.json).
No clone, source-tree copy, package install or upstream execution occurred.
The browser could not retrieve the pinned Qwen/Pydantic files, but the GitHub API
succeeded. Only references, identifiers and observations are published, not a
duplicate upstream source tree or long code excerpts. Recheck revisions before
later comparisons and record any movement rather than silently replacing pins.

These cursors establish implementation locations, not maturity rankings,
correctness, comparative performance, licensing approval for reuse, or proof
that a named feature is effective. DeepSeek's own preview warning specifically
precludes treating all four projects as equally mature.

## Ordered research targets

| Order / project | Authenticated revision | Primary implementation cursor / limited observation |
|---|---|---|
| 1. Qwen Code | `a98615bedbe1ef0ab5e343de7471b06bfd79014d` | [`packages/core/src/core/client.ts`](https://github.com/QwenLM/qwen-code/blob/a98615bedbe1ef0ab5e343de7471b06bfd79014d/packages/core/src/core/client.ts#L496) declares LlmClient and compression-observer hooks. Follow their actual call paths before inferring loop, capacity or failure semantics. |
| 2. Pydantic AI | `d97c25c6d749b121494c28684273a3df37955803` | [`pydantic_ai_slim/pydantic_ai/_agent_graph.py`](https://github.com/pydantic/pydantic-ai/blob/d97c25c6d749b121494c28684273a3df37955803/pydantic_ai_slim/pydantic_ai/_agent_graph.py#L667) defines UserPromptNode/ModelRequestNode and references UsageLimits/ModelRetry. Graph nodes are an upstream implementation choice, not authorization to broaden Devtools Runtime. |
| 3. DeepSeek Harness | `687f282e8625c6b8d11ff58211a90524be2e4317` | Its [README](https://github.com/deepseek-ai/deepseek-harness/blob/687f282e8625c6b8d11ff58211a90524be2e4317/README.md) describes plugin composition using Cordis and explicitly marks developer-preview compatibility risk. Implementation/dependency tracing remains future work; README claims are not a code-level comparison. |
| 4. Aider | `5dc9490bb35f9729ef2c95d00a19ccd30c26339c` | [`aider/repomap.py`](https://github.com/Aider-AI/aider/blob/5dc9490bb35f9729ef2c95d00a19ccd30c26339c/aider/repomap.py#L42) defines RepoMap and explicit map/tag methods. Inspect invalidation, ranking/disclosure, token accounting and edit integration separately; no effectiveness claim is inferred from these entry points. |

The official repositories are [Qwen Code](https://github.com/QwenLM/qwen-code),
[Pydantic AI](https://github.com/pydantic/pydantic-ai),
[DeepSeek Harness](https://github.com/deepseek-ai/deepseek-harness) and
[Aider](https://github.com/Aider-AI/aider). Vendor model identity, an Agent harness,
a library and a coding application are not automatically interchangeable units.

## Mechanism worksheet for the next assignment

Study Qwen Code and Pydantic AI first. For each mechanism, record exact revision,
source symbol/path, direct dependencies, relevant tests, supported/unsupported
behavior and one concrete difference from Devtools. Distinguish observation,
interpretation, candidate recommendation and accepted decision.

1. Model/provider boundary, settings and native Tool-call/result correlation.
   Compare with ModelInteraction/ModelRequest/ModelResponse, not a generic Agent
   alias for every provider or model name.
2. Invocation versus multi-turn engineering loop; completion, budgets and stop
   rules. Compare the narrow Runtime with application orchestration separately.
3. Tool execution/admission, cancellation, timeout, validation failure, retries
   and ambiguous external effects. Preserve cancellation != rollback.
4. Context selection, projection, compaction, reacquisition and current source
   grounding. Determine which evidence is exact and which is a summary/estimate.
5. Editing/application atomicity, new files and source-version validity; compare
   guarantees rather than matching function names or patch syntax.
6. Evidence/capture policy, failed invocations, Tool/Command correlation, tracing,
   exporter hooks and privacy. Do not confuse upstream logs with Devtools Evidence.
7. Usage categories, timing boundaries, unknown costs and budget enforcement.
   A source field or advertised integration is not complete measurement coverage.
8. Durable conversation/run state, resume/replay and schema compatibility. Separate
   source persistence, restoration and repeated effects from exactly-once claims.
9. Configuration, developer ergonomics, package boundaries and justified shared
   primitives. Identify existing Devtools owners before recommending abstraction.

Read associated tests and failure paths; do not execute an upstream agent,
provider call or scientific benchmark as part of source inspection. If a bounded
deterministic execution is later proposed, qualify its inputs and authorize it
separately. Do not copy a framework because its package names appear similar.

## Hypotheses, not decisions

- Existing local model/provider/Tool/Runtime primitives may be sufficient while
  application loop orchestration differs. The source comparison must test that
  hypothesis before a reusable Agent lifecycle is proposed.
- Correlation may be the immediate observability pressure rather than a global
  event bus. Inspect failure/cancellation and multiple actual consumers under
  B-0023/B-0011 before choosing any trace/export API.
- External Context mechanisms may clarify engineering tradeoffs, but the failed
  Qwen attempts do not alone establish that a particular compaction, planner,
  serving profile or harness replacement would work.

Record candidate changes through existing backlog intake. Broad related records
include B-0023, B-0027/28/29/30/31, B-0035/36 and B-0044/45. No new B-number,
implementation authorization or promotion follows from this worksheet.

## Finite follow-up deliverable

Produce one bounded Qwen Code/Pydantic AI source-and-test comparison covering
the worksheet, explicit unknowns and source-backed proposals. Then study
DeepSeek Harness/Aider using the same distinctions. Reconcile findings with the
local adoption/custody inventory before selecting any implementation or preparing
the comprehensive fresh-ChatGPT-session handoff. Do not launch another Qwen task
as a substitute for this research.
