# Devtools — External Agent Harness Mechanisms: Initial Source Review

**Research state:** First evidence-gathering increment; not a complete comparative evaluation or accepted architectural decision.  
**Date:** 2026-10-22.  
**Scope:** Qwen Code, Pydantic AI / Pydantic AI Harness, DeepSeek Harness, Aider.  
**Source provenance:** Maintained upstream public source/documentation on moving branches (`main`/`master`) as accessed for this review. **Pin exact Git revisions in the next accepted research increment**; do not fabricate a revision hash. Local Devtools source is not inspected here: comparisons use owner-provided recent handoffs and remain hypotheses pending canonical-checkout audit.

## A. The question these implementations help answer

Does Devtools need a new agent runtime, a simpler model-facing surface over its established ToolRunner/source integrity boundary, richer lifecycle observability, a better model-configuration adapter, or primarily better use of capabilities already implemented? We should not assume that adding another Tool or making Qwen think longer is a substitute for systematic evidence.

## 1. Qwen Code: concrete runtime and interoperability seams

**Verified from maintained architecture source:**
- The project distinguishes **direct CLI/headless execution** from **ACP-hosted execution** (`qwen --acp`). An HTTP/SSE `qwen serve` control plane drives ACP-backed workspace-scoped runtimes. An in-process/child process and an ACP bridge are different integration contracts.
- `packages/core` owns model requests, session/context, Tool execution, permissions, memory and telemetry; `packages/cli` owns presentation/launch; `packages/acp-bridge` owns multiplexed session, filesystem and permission mediation; `packages/sdk-typescript` and `packages/sdk-python` provide clients. The public documentation explicitly describes separate host, runtime and transport layers.
- Tool calls go through an explicit permission policy in the documented direct path. ACP bridge also mediates host permission requests and exposed filesystem seams. **Do not assume ACP alone enforces Devtools' source-specific authorization or WorkCycle governance.**
- Source file `packages/core/src/config/config.ts` imports `ToolRegistry`, `PermissionManager`, `TurnBudget`, `AgentCore`/agent runtime services, model-specific `reasoning-effort`, telemetry settings, memory pressure monitoring, tool-result output thresholds, and optional tool search/deferred schema settings. That is a concrete sign that model/harness configuration and Tool visibility are integrated, not a thin CLI wrapper.
- A public design document describes stable sorting of tool schemas to preserve provider prompt-cache prefix stability; it identifies `ToolRegistry.getFunctionDeclarations()` and `GeminiClient.setTools()`. Treat this document as a design proposal until inspecting final source/tests.

**Source paths / references:**
- [Qwen Code architecture](https://github.com/QwenLM/qwen-code/blob/main/docs/developers/architecture.md)
- [Qwen Code runtime configuration source](https://github.com/QwenLM/qwen-code/blob/main/packages/core/src/config/config.ts)
- [Tool-schema sorting design](https://github.com/QwenLM/qwen-code/blob/main/docs/design/prompt-cache/global-tool-schema-stable-sort.md)
- [Qwen Code parent repository](https://github.com/QwenLM/qwen-code)

**Devtools comparison (requires local verification):**
- Existing Devtools ModelRequest/ModelInteraction/ModelToolCall and ToolRunner boundaries may already cover much of the model-neutral core; do not invent another identical adapter layer.
- Compare Qwen Code's model-specific template/reasoning and Tool lifecycle against `models/interaction`, `model_serving`, `apps/qwen/coding_loop.py` and `apps/qwen/context_tools.py`.
- Investigate Qwen Code **as a distinct governed worker runtime**, with ACP/SDK as potential integration seam, not simply as a substitute "model provider". Its file-system and command operations cannot receive write authority just because its CLI accepts a working directory.
- Inspect actual Tool-call execution equivalence between direct CLI, headless and ACP. An upstream issue (#3247) raised divergence between these paths; this is *historical issue evidence*, not proof the defect persists in current code.
- Potential ergonomics pattern: stable Tool naming/schema visibility and bounded dynamic exposure, but only compare after recording currently advertised Devtools Tool definitions and actual Qwen behavior.

**Key unverified questions:** What exact model-specific reasoning template does Qwen Code use for Qwen3.8? Are its current ACP permission hooks sufficient to interpose Devtools tools without patching a fork? What features depend on unrestricted host filesystem/shell? Can we run a fair same-model comparison against a tiny separately authored fixture with identical task authority, without a second Devtools checkout?

## 2. Pydantic AI: typed Tools, retries, external tools, observability, ergonomics

**Verified from source-level API documentation:**
- `FunctionToolset` groups typed functions and Tool definitions; combined, filtered, renamed, prefixed and dynamic toolsets can change model-visible Tool sets by run or capability. This is an *ergonomics/composition* feature, not direct execution authority.
- Argument validation occurs before Tool execution. Validation failures and a Tool-raised `ModelRetry` can result in `RetryPromptPart` including failed-call correlation and validation details; a Tool can instead raise `ToolFailed` to return an ordinary failed outcome **without** consuming a retry budget. Arbitrary exceptions do not automatically become retries.
- Retry scopes are independent: HTTP transport, provider, durable-step, fallback-model, per-tool, output validation and request hooks. Their budgets can multiply; per-tool counters reset upon success. **Do not equate "typed Tool" with "a model cannot generate invalid or semantically wrong arguments"**.
- `ExternalToolset` supports declaring externally executed Tools with validated arguments and unique call IDs, yielding `DeferredToolRequests` and accepting correlated `DeferredToolResults`. This is especially relevant if Devtools retains sole command/edit authority while another harness owns an agent loop.
- The separate **Pydantic AI Harness** (distinct from Pydantic AI core) describes `Step Persistence`, `Repair Tool Arguments`, tool capability packages and OpenTelemetry-backed instrumentation. Verify current version/compatibility before considering adoption; these are not all core features.
- Instrumentation capability reports OpenTelemetry GenAI spans for agent runs, model requests and Tool executions; it can use any OTLP backend, with Pydantic Logfire as one frontend. This is a particularly concrete reference for our unformalized observability concern.

**Sources:**
- [Pydantic Toolsets](https://github.com/pydantic/pydantic-ai/blob/main/docs/toolsets.md)
- [Advanced Tool execution, retry and failure](https://github.com/pydantic/pydantic-ai/blob/main/docs/tools-advanced.md)
- [Retries and retry-layer multiplication](https://github.com/pydantic/pydantic-ai/blob/main/docs/retries.md)
- [Instrumentation](https://github.com/pydantic/pydantic-ai/blob/main/docs/capabilities/instrumentation.md)
- [Pydantic AI Harness capabilities](https://github.com/pydantic/pydantic-ai/blob/main/docs/capabilities/overview.md)
- [Pydantic AI harness repo](https://github.com/pydantic/pydantic-ai-harness)

**Devtools comparison (requires source audit):**
- Review whether our manually authored ModelToolDefinition schemas/ToolRunner argument parsing duplicate type-to-schema and retry-correlation logic. Typed wrappers or decorators may simplify API definition while preserving unchanged source edit contracts.
- `ExternalToolset` and `DeferredToolResults` suggest a genuine interoperability seam to evaluate if adopting an external harness; it does not grant file/command capability by itself.
- Compare current Devtools `observability/evidence` and `observability/usage`, model interaction evidence, ToolRunner evidence and WorkCycle receipts against a common trace-span hierarchy, correlation, privacy capture controls and export backend. An OpenTelemetry exporter might be suitable after identifying maintained emitters, rather than replacing provenance with trace spans.
- Scope initial ergonomics experiment narrowly: schemas, Tool argument retry messages, and model-facing Tool count. Do not adopt a competing retry budget that obscures our existing task-authority bounds.

**Key unverified questions:** Does Devtools already use Pydantic validation internally? What fraction of Qwen failures were Tool syntax versus wrong semantic edits (recent runs often had valid structured calls but wrong code)? Can Pydantic style be introduced as a decorator/factory on existing tools instead of replacing their domain interfaces? What span relationships are needed for the complete coding lifecycle and postmortem?

## 3. DeepSeek Harness: reversible plugin lifecycles and durable session-event semantics

**Verified from architecture/primer:**
- Cordis composes named services and typed events under a shared plugin context; registrations are reversible effects, and plugin dependencies are declared through `inject`. This is a managed lifecycle, not merely an arbitrary dictionary of functions.
- The system ships profile/bundle composition (`web`, `headless`, `sdk`, `sdk-minimal`, `acp`), allowing different host surfaces over common services. It explicitly separates model/Tool/session/agent-loop services.
- Its documented subsystem owners include `core/session` for an **append-only SessionEvent log**, `core/tools` for scoped registry/guarded execution, `core/system-prompt` for prompt/schema assembly, `core/agent` and `core/agent-loop` for orchestration, and `llm/llm` for message/stream adapter seams.
- The runtime distinguishes durable **session events** (must survive replay) from live `agent/*` lifecycle events and `fs/*`/`tools/*`/`telemetry/*` capability events. The documented turn flow includes `step/start`, frozen request history, assistant streams, `tools/pre-execute` / `tools/execute` / `tools/post-execute`, `tool/result`, `step/end`, and `turn/end`.
- It is still marked developer preview by maintainers; plugin loading and remote dependencies impose trust/custody questions. **We should study patterns as public source, not run an untrusted plugin stack against our private checkout**.

**Sources:**
- [DeepSeek Harness architecture](https://github.com/deepseek-ai/deepseek-harness/blob/master/docs/architecture.md)
- [Cordis primer](https://github.com/deepseek-ai/deepseek-harness/blob/master/docs/cordis-primer.md)
- [Developer preview and safety notice](https://github.com/deepseek-ai/deepseek-harness)

**Devtools relevance:** The strongest candidate idea is a **defined reusable event taxonomy and emitter boundary** so that long-running agent work produces correlated, observable phases without application-specific logging everywhere. Do not import Cordis concepts wholesale: compare with existing `agents`, `runtime`, `observability`, `execution`, `evidence`, `backlog` and WorkCycle lifecycles to avoid duplicate registries and ambiguous authority.

## 4. Aider: repository map plus deliberately model-friendly editing

**Verified from source and docs:**
- Aider's `aider/repomap.py` uses Tree-sitter/grep-ast tags and reference/declaration relationships with importance ranking (including PageRank-related logic). It renders a constrained map into model context, rather than requiring an agent to discover each symbol via Tool calls before seeing any map information.
- The documented map includes relevant classes/functions and definitions and is provided with change requests. It is a different product decision from Devtools' new *opt-in model-invoked `repository_map` Tool*; neither strategy wins without controlled tests.
- `aider/coders/editblock_coder.py` implements search/replace edit blocks and parsing/repair behavior; `editor_editblock_coder.py` separates a focused editor from other reasoning paths. This is a concrete alternative **model-facing editing format**, not an argument for abandoning safe host-side source/version checks.

**Sources:**
- [Aider repository-map implementation](https://github.com/Aider-AI/aider/blob/main/aider/repomap.py)
- [Aider repository-map docs](https://github.com/Aider-AI/aider/blob/main/aider/website/docs/repomap.md)
- [Aider edit block coder](https://github.com/Aider-AI/aider/blob/main/aider/coders/editblock_coder.py)
- [Aider focused editor](https://github.com/Aider-AI/aider/blob/main/aider/coders/editor_editblock_coder.py)

**Devtools relevance:** Contrast "include a compact graph map in the initial Context" vs "offer opt-in `repository_map` and expect a weaker model to choose it." Engineering 28 demonstrates availability without model use, not that graph Context is useless. Compare editor-friendly formats through the *same host admission* before a wholesale patch redesign. Examine whether a separate planning model and focused editing model has a meaningful place in the future model-neutral agent lineup.

## 5. Initial cross-harness mechanism matrix (inference, not an adoption decision)

| Concern | Qwen Code | Pydantic AI | DeepSeek Harness | Aider | Devtools audit question |
|---|---|---|---|---|---|
| Run/tool lifecycle | Core with CLI/ACP hosts | Agent + toolsets/capabilities | Typed step/turn plugin events | Coder loop | Are these already distributed across `models`, `agents`, `runtime`, `apps/qwen`, `tools`? |
| Source editing | Built-in file tools under permissions | User-supplied tools/external tools | Guarded registry surface | Edit blocks/search-replace | Can model-facing edits be simplified without weakening exact admitted source? |
| Context navigation | Prompt/context services + tools | User-defined tools/capabilities | Runtime-context projection | Inline ranked repo map | Is native map Tool avoidance a UX/prompt issue? |
| Memory/continuation | Session/memory/SDK | Step persistence options | Append-only session events | Conversation/repo map | Which Devtools state is actually durable, coherent and rehydratable? |
| Tracing | Telemetry in core | OTel GenAI instrumentation | Session + telemetry events | Command/log outputs | What reusable observability module should own spans/events/evidence? |
| External integration | ACP, SDK, MCP | ExternalToolset/deferred IDs | SDK/ACP plugin profiles | CLI/commands | Where do external agents rejoin our WorkCycle/ToolRunner authority? |

## 6. Preliminary recommendations and next research gaps

**Support for action:**
1. Create a rigorous Devtools subsystem and observability audit before adopting another runtime or duplicate ModelAdapter.
2. Research Qwen Code **runtime implementation, tool scheduler, providers, permission mediation, compaction**, and its actual model-dependent task performance. The architecture document alone is insufficient.
3. Investigate Pydantic AI's external/deferred tool integration and typed Tool retry semantics; compare them to existing ToolRunner semantics and governance. Include Pydantic AI Harness as a distinct newer library.
4. Study DeepSeek's event/turn taxonomy as an observability reference. Do not run it or copy plugins.
5. Compare Aider's initial repo-map disclosure and editing formats with Devtools' opt-in map/search/replace workflow in a proper controlled experiment later.

**Do not decide yet:** Pydantic AI adoption, Qwen Code substitution, new event base class, automatic map injection, bigger Context, alternative quantization, or wholesale edit protocol replacement. All require either local source evidence, bounded comparative runs, or user architecture approval.

**Next sources to inspect in detail (not yet completed):**
- Qwen Code `packages/core/src/core/*`, `tools/coreToolScheduler.ts`, `tools/tool-registry.ts`, permission implementation, prompt compaction and reasoning adapters; Qwen Code ACP bridge tests.
- Pydantic AI `pydantic_ai_slim/pydantic_ai/toolsets.py`, `tools.py`, `agent/abstract.py`, instrumentation internals, `ExternalToolset`, capabilities/step-persistence implementations.
- DeepSeek Harness `packages/core/session`, `core/agent-loop`, `core/tools`, `core/system-prompt`, event map and `llm/llm` source.
- Aider `aider/coders/editblock_coder.py` validation/repair, `aider/repomap.py` ranking, task prompts and Context budgets.
- **Devtools canonical checkout** owners, current tests, the actual `observability` tree, accepted ADRs and past experiment recipients. No claim of inspection until Codex returns exact file/revision evidence.
