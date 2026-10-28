# Agent harness mechanism review: Qwen Code, Pydantic AI, DeepSeek Harness and Aider

## Disposition

Initial source-reference collection followed by the bounded source-and-test
comparison below, 2026-10-23. The initial worksheet is retained as research lineage. No external architecture is
adopted, no harness was installed/executed, and no model comparison or scientific
experiment was launched. This is Codex-authored research preparation, **not** an
import of the originally unavailable `02-oss-harness-mechanism-review-initial.md`.
The [recovered inputs and exact18 crosswalk](reconciliation-input-reconciliation.md)
now preserve that draft and the independent review separately. Later pinned
implementation findings below qualify the earlier notes; no draft becomes an ADR.

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

## Initial mechanism worksheet (retained lineage)

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

## Initial follow-up deliverable (addressed below)

Produce one bounded Qwen Code/Pydantic AI source-and-test comparison covering
the worksheet, explicit unknowns and source-backed proposals. Then study
DeepSeek Harness/Aider using the same distinctions. Reconcile findings with the
local adoption/custody inventory before selecting any implementation or preparing
the comprehensive fresh-ChatGPT-session handoff. Do not launch another Qwen task
as a substitute for this research.


## Source-and-test comparison (2026-10-23)

### Method, evidence strength and limits

Devtools baseline is `3b2b3de845fbc0d8b510449bed9f492a54e39734`.
Upstream pins remain Qwen Code `a98615bedbe1ef0ab5e343de7471b06bfd79014d`
and Pydantic AI `d97c25c6d749b121494c28684273a3df37955803`.
Individual files and recursive **path metadata** were fetched from primary GitHub
endpoints; each inspected file's Git blob was recomputed against its pinned tree.
[Source/test metadata](agent-harness-mechanism-evidence-20261023.json) records
revision, blob, SHA-256, byte count, source/test role and reproducible links.
No clone, upstream source directory, install, agent execution or upstream test run
was made. Temporary individual-file inspection captures remain ignored local evidence;
durable research contains observations/references, not copied source trees.
Browser pinned-file fetches cache-missed; the read-only GitHub API/raw endpoints
succeeded. Retrieval of a file is not a claim that every line/path was audited.

Here **observed** means inspected implementation and selected test assertions.
Tests show intended deterministic contracts, not an independently reproduced
upstream PASS. **Gap** means a difference from actual Devtools owners, not a
mandate to adopt the external mechanism. **Candidate** remains backlog research.
No task performance, model reliability, token savings, hosted cost completeness,
security certification or production availability comparison was performed.
The separate Pydantic AI Harness is not the subject of this core-library review.

### Qwen Code: interaction, provenance and continuation

| Mechanism / inspected source | Observed behavior and test evidence | Actual Devtools comparison / qualified gap |
|---|---|---|
| [Turn request/result correlation](https://github.com/QwenLM/qwen-code/blob/a98615bedbe1ef0ab5e343de7471b06bfd79014d/packages/core/src/core/turn.ts#L191) | Request carries `callId`, separate optional provider-call ID, `prompt_id`, response ID and incomplete/truncation indicators. Response preserves local call ID and execution status; synthetic not-started/duplicate responses are explicit. [Tests](https://github.com/QwenLM/qwen-code/blob/a98615bedbe1ef0ab5e343de7471b06bfd79014d/packages/core/src/core/turn.test.ts#L715) assert provider IDs separate from generated/suffixed IDs. | `ModelToolCall` preserves provider ID and exact JSON; native coding loop requires distinct nonempty IDs per batch and pairs Tool messages. Shared ToolRunner itself has no provider or invocation identity. Do not substitute upstream IDs for source/content/Evidence IDs. Cross-batch effect idempotency is not established by Devtools' per-batch guard. |
| [Host execution provenance](https://github.com/QwenLM/qwen-code/blob/a98615bedbe1ef0ab5e343de7471b06bfd79014d/packages/core/src/core/turn.ts#L143) | `model`, `client`, `fixed_policy` origin is set in process, never parsed from model arguments; absent origin is treated as model. Fixed policy is a restricted media-policy path, not blanket administrative trust. [Gate/tests](https://github.com/QwenLM/qwen-code/blob/a98615bedbe1ef0ab5e343de7471b06bfd79014d/packages/core/src/omni/policy/model-access.test.ts#L345) cover default denial, forged fixed-policy use on ordinary tools and operator-only arguments. | Devtools keeps CodingTask/Checkout/WorkCycle authority host-owned and marks host freshness verification separately. `InvocationMeasurement.execution_origin` concerns EXECUTED versus ADOPTED accounting, a **different meaning** from Qwen's origin. Do not reuse the enum by name or infer a standing grant from client initiation. |
| [Retry/fallback stream handling](https://github.com/QwenLM/qwen-code/blob/a98615bedbe1ef0ab5e343de7471b06bfd79014d/packages/core/src/core/turn.ts#L780) | Retry clears pending calls, citations and finish state; fallback additionally clears response correlation. Thought, visible content, error, retry and fallback are distinct events. [Turn tests](https://github.com/QwenLM/qwen-code/blob/a98615bedbe1ef0ab5e343de7471b06bfd79014d/packages/core/src/core/turn.test.ts#L446) check response-ID reset; tests at338/357 check thought output and936 retry event forwarding. `LlmChat` owns transport/history logic below Turn. | Devtools llama.cpp normalizes final content/reasoning/termination separately; its current HTTP operation is nonstreaming. Native loop deliberately does not redispatch after provider failure or unknown completion. Streaming/retry would add semantics under B-0046/B-0032, not repair an exact edit automatically. |
| [Client continuation bounds](https://github.com/QwenLM/qwen-code/blob/a98615bedbe1ef0ab5e343de7471b06bfd79014d/packages/core/src/core/client.ts#L4544) | Client caps recursive turn allowance at100 and stops at zero; separate session/token/hook/loop conditions exist. This multi-turn client is not merely the provider adapter. [Client tests](https://github.com/QwenLM/qwen-code/blob/a98615bedbe1ef0ab5e343de7471b06bfd79014d/packages/core/src/core/client.test.ts#L4459) cover session limits across routes. This is selected-path inspection, not all managed/CLI/ACP execution modes. | Devtools Runtime coordinates one invocation; `apps/qwen/coding_loop.py` owns the bounded engineering conversation, independent call/action/proposal/time ceilings and accepted completion. Compare that application owner to the client, not Runtime alone. No reason to broaden Runtime follows. |

### Qwen Code: exploration, compaction and source residency

The [exploration budget](https://github.com/QwenLM/qwen-code/blob/a98615bedbe1ef0ab5e343de7471b06bfd79014d/packages/core/src/services/tool-exploration-budget.ts#L67)
counts registered read/search/fetch operations, including explicit discovery
exceptions for LSP/ToolSearch. A non-read/unknown kind resets the phase. At a
finite positive allowance it emits **one reminder**, then permits legitimate
continued investigation. Commit/rollback avoids charging replayed calls twice;
reset commits its zero floor. The [unit tests17–85](https://github.com/QwenLM/qwen-code/blob/a98615bedbe1ef0ab5e343de7471b06bfd79014d/packages/core/src/services/tool-exploration-budget.test.ts#L17)
assert continued reads, reset, rollback and disabled allowances. [Client tests8642–9142](https://github.com/QwenLM/qwen-code/blob/a98615bedbe1ef0ab5e343de7471b06bfd79014d/packages/core/src/core/client.test.ts#L8642)
check actual reminder delivery, retry/fallback accounting, provider duplicates,
bridged reads and concurrent side-query isolation.

The reminder is not authorization and does not ensure implementation starts.
This is importantly different from Devtools Engineering20's discontinued fixed
eight-response stop. Devtools still has prospective hard resource ceilings and
history-based instructions; neither needs replacing by an upstream policy without
measured task evidence. Unknown/non-read resetting also means the counter is an
operational heuristic, not a semantic proof of progress.

[LoopDetectionService](https://github.com/QwenLM/qwen-code/blob/a98615bedbe1ef0ab5e343de7471b06bfd79014d/packages/core/src/services/loopDetectionService.ts#L751)
adds independent repetition guards: identical calls, content/thought repetition,
read/action stagnation, stateful result-aware comparisons and turn caps. Its
built-in cap is adaptive for diverse calls, with a hard backstop; an explicitly
configured cap is hard. Warn/stop/off and session disable are distinct paths.
[Tests1484–1737](https://github.com/QwenLM/qwen-code/blob/a98615bedbe1ef0ab5e343de7471b06bfd79014d/packages/core/src/services/loopDetectionService.test.ts#L1484)
exercise productive diverse calls, repetition, explicit caps and rollback;
[tests2351 onward](https://github.com/QwenLM/qwen-code/blob/a98615bedbe1ef0ab5e343de7471b06bfd79014d/packages/core/src/services/loopDetectionService.test.ts#L2351)
exercise changed-result progress and warn behavior. These tests do not establish
false-positive rates on Devtools engineering tasks. Hard authorization/time
bounds must remain host-owned even if soft progress feedback is later studied.

There are **two different Context mechanisms**:

1. [Microcompaction](https://github.com/QwenLM/qwen-code/blob/a98615bedbe1ef0ab5e343de7471b06bfd79014d/packages/core/src/services/microcompaction/microcompact.ts#L793)
   deterministically elides eligible old Tool bodies/media under idle/size/force
   rules. It preserves Tool response structure/IDs and protected recent results,
   excludes error responses from old-output clearing, and reports evicted file
   paths/unresolved references and memory-body versions. Size accounting uses
   characters/estimates, not Devtools' exact llama.cpp templated-token admission.
   [Tests1984–2028](https://github.com/QwenLM/qwen-code/blob/a98615bedbe1ef0ab5e343de7471b06bfd79014d/packages/core/src/services/microcompaction/microcompact.test.ts#L1984)
   assert the response ID survives, a placeholder replaces content and only the
   evicted path is reported. Tests1160/1538 cover error preservation;2031 onward
   reject a kept read placeholder as proof that full source remains resident.
2. [ChatCompressionService](https://github.com/QwenLM/qwen-code/blob/a98615bedbe1ef0ab5e343de7471b06bfd79014d/packages/core/src/services/chatCompressionService.ts#L600)
   invokes a summarization side-query and reconstructs history from a state
   snapshot/acknowledgment and selected restored content. API/empty/truncated
   summary failures are distinguished; checks avoid orphaned Tool calls.
   [Compression tests](https://github.com/QwenLM/qwen-code/blob/a98615bedbe1ef0ab5e343de7471b06bfd79014d/packages/core/src/services/chatCompressionService.test.ts)
   cover summary failure/capacity paths; this is not exact authoritative source.

The [client invalidates read-cache fast paths after eviction](https://github.com/QwenLM/qwen-code/blob/a98615bedbe1ef0ab5e343de7471b06bfd79014d/packages/core/src/core/client.ts#L6134),
falling back to wider invalidation when path recovery fails.
[Tests4653 onward](https://github.com/QwenLM/qwen-code/blob/a98615bedbe1ef0ab5e343de7471b06bfd79014d/packages/core/src/core/client.test.ts#L4653)
assert surgical disarming and cleanup-failure behavior.
Devtools `apps/qwen/continuation.py` instead projects authenticated historical
disclosure deterministically, retains raw requests/results and preserves current
source observation/version admission. Its active-prompt residency and host edit
authority are distinct. An upstream cache eviction must not revoke/create exact
edit authority implicitly; an LLM summary cannot become source evidence. Future
ergonomics work must make omitted/reacquirable material visible, not copy these
strategies indiscriminately. No compaction change is implemented here.

### Qwen Code: validation, permission, persistence and tracing

The [scheduler](https://github.com/QwenLM/qwen-code/blob/a98615bedbe1ef0ab5e343de7471b06bfd79014d/packages/core/src/core/coreToolScheduler.ts#L3487)
rejects incomplete/truncated Edit calls before execution. PreToolUse hooks can
replace input, after which native build/schema/business checks and permission
checks apply to the replacement. [Declarative Tool build](https://github.com/QwenLM/qwen-code/blob/a98615bedbe1ef0ab5e343de7471b06bfd79014d/packages/core/src/tools/tools.ts#L511)
uses SchemaValidator then invocation construction. Repeated validation errors are
tracked by Tool/error pair; feedback distinguishes output truncation from malformed
arguments. [Scheduler tests8589–8761](https://github.com/QwenLM/qwen-code/blob/a98615bedbe1ef0ab5e343de7471b06bfd79014d/packages/core/src/core/coreToolScheduler.test.ts#L8589)
cover those distinctions. [Tests4992–5066](https://github.com/QwenLM/qwen-code/blob/a98615bedbe1ef0ab5e343de7471b06bfd79014d/packages/core/src/core/coreToolScheduler.test.ts#L4992)
verify replacement executes once, invalid replacement does not fall back to the
original, and permission is checked against rewritten input.

[Permission flow](https://github.com/QwenLM/qwen-code/blob/a98615bedbe1ef0ab5e343de7471b06bfd79014d/packages/core/src/core/permissionFlow.ts#L64)
combines Tool defaults and PermissionManager rules with explicit interaction and
approval-mode handling. Deny is separate from ask; plan/auto-edit policies have
their own checks. Origin gates and later abort rechecks prevent some bypasses.
This is **not equivalent** to Devtools' frozen task path/version/absence and
atomic all-component admission. Upstream model-access defaults/locked arguments,
hook rewrites and permission modes must not become another authority layer in
Devtools. `ToolRunner` validates once, then executes; application Tools implement
scope and source semantics. B-0035 can study definition ergonomics while keeping
that execution boundary unchanged.

[SessionService](https://github.com/QwenLM/qwen-code/blob/a98615bedbe1ef0ab5e343de7471b06bfd79014d/packages/core/src/services/sessionService.ts#L3151)
validates transcript ownership/chain and provides corruption-aware reading and
history reconstruction. Fork paths rebuild UUID/parent chains and stage transcript
and backup writes. [Corruption tests](https://github.com/QwenLM/qwen-code/blob/a98615bedbe1ef0ab5e343de7471b06bfd79014d/packages/core/src/services/sessionService.corruption.test.ts#L121)
exercise malformed/recovered creation records, bounded reads, foreign/corrupt
inputs and reconstruction gaps. This selected legacy SessionService review is
not a complete audit of managed-host session authority or ACP recovery. Loading
history does not establish exactly-once Tool effects. Devtools Conversation
persistence, frozen replay evidence, Checkout restoration and WorkCycle ambiguous
commit/ref reconciliation are different domain contracts; no shared session
store or automatic redispatch follows from transcript support.

The scheduler opens Tool lifecycle/execution/approval/hook spans, with local and
provider call IDs. [Tests1006](https://github.com/QwenLM/qwen-code/blob/a98615bedbe1ef0ab5e343de7471b06bfd79014d/packages/core/src/core/coreToolScheduler.test.ts#L1006)
keep the execution observer unsettled while an abort-ignoring Tool still runs;
tests10825/11207 onward distinguish timeout, returned/thrown errors and cancellation.
[Telemetry helpers](https://github.com/QwenLM/qwen-code/blob/a98615bedbe1ef0ab5e343de7471b06bfd79014d/packages/core/src/telemetry/tracer.ts#L135)
preserve explicitly set error status, use generic thrown-error status text and
catch status/end exporter faults so they do not mask caller behavior. Manual
stream spans require explicit lifetime management. The helper also documents a
synthetic-root sampling caveat: some parent-based ratio configurations effectively
sample all children. [Tracer tests](https://github.com/QwenLM/qwen-code/blob/a98615bedbe1ef0ab5e343de7471b06bfd79014d/packages/core/src/telemetry/tracer.test.ts)
and [context tests](https://github.com/QwenLM/qwen-code/blob/a98615bedbe1ef0ab5e343de7471b06bfd79014d/packages/core/src/telemetry/trace-context.test.ts)
are implementation evidence, not proof of durable export, complete cost coverage
or inclusion of Devtools-style review/publication. SDK/exporter deployment and
all privacy paths remain outside this bounded review.

### Pydantic AI: typed Tools, retries and permission handoff

| Mechanism / source and associated tests | Observed behavior | Devtools comparison and limit |
|---|---|---|
| [FunctionToolset](https://github.com/pydantic/pydantic-ai/blob/d97c25c6d749b121494c28684273a3df37955803/pydantic_ai_slim/pydantic_ai/toolsets/function.py#L614) / [signature tests](https://github.com/pydantic/pydantic-ai/blob/d97c25c6d749b121494c28684273a3df37955803/tests/test_function_signature.py) | Typed functions/decorators generate schema and runtime validator; custom `args_validator` follows schema conversion. Preparation can omit/rename a definition; per-Tool settings include retry/timeout/approval/sequential behavior. Duplicate names are rejected. | Devtools has structural `Tool`, descriptor/invocation seams and explicit schemas/admission in ContextTools/CodingCommands. `ModelToolDefinition` validates a JSON object, not every semantic schema invariant. Candidate: study transparent typed definition helpers under B-0035, not replace ToolRunner/authorization. Implicit conversion/coercion could conflict with exact bool/int/path/byte contracts and needs explicit tests. |
| [ToolManager validation](https://github.com/pydantic/pydantic-ai/blob/d97c25c6d749b121494c28684273a3df37955803/pydantic_ai_slim/pydantic_ai/tool_manager.py#L919) | `ValidatedToolCall` carries admitted arguments or correlated validation error/deferral before `execute_tool_call`. Validation/model retries become retried Tool returns tied to call ID. Deferred validation can be valid without execution. | Devtools already validates before execution and preserves provider-call/result correlation. Generic manager validation is not source observation, current version, exact absence, Checkout ownership or permission to edit. |
| [Retry accounting](https://github.com/pydantic/pydantic-ai/blob/d97c25c6d749b121494c28684273a3df37955803/pydantic_ai_slim/pydantic_ai/tool_manager.py#L513) / [failed-result tests](https://github.com/pydantic/pydantic-ai/blob/d97c25c6d749b121494c28684273a3df37955803/tests/test_tools.py#L1769) | Per-exposed-Tool retries carry between steps, success clears carry-over, exhaustion raises UnexpectedModelBehavior. Validation/ModelRetry charges repair; ToolFailed yields a failed result without that retry charge. First unavailable-tool refusal has a separate free-refusal path. Raw nested mode avoids double charging. | Devtools charges refused edit proposals/actions to frozen host ceilings; no free-refusal or per-Tool unlimited continuation should be imported. Distinguish semantic model repair, transport retry, ordinary test failure and uncertain effect under B-0032/33/34. Typed validation cannot ensure correct code. |
| [Approval/deferred handling](https://github.com/pydantic/pydantic-ai/blob/d97c25c6d749b121494c28684273a3df37955803/pydantic_ai_slim/pydantic_ai/_tool_execution.py#L669) / [unapproved validation tests](https://github.com/pydantic/pydantic-ai/blob/d97c25c6d749b121494c28684273a3df37955803/tests/test_tools.py#L2929) | Invalid typed arguments can produce retry before approval. Approved calls with override arguments are revalidated; denied returns remain denied. Deferred requests/results are correlated by ID. Duplicate IDs in one batch fail before any Tool executes; [test11515](https://github.com/pydantic/pydantic-ai/blob/d97c25c6d749b121494c28684273a3df37955803/tests/test_agent.py#L11515) asserts no effects. | Approval values are host-supplied library inputs, not authenticated repository grants. Devtools must retain Checkout/WorkCycle authority, no model-supplied approved flag. Native distinct batch IDs already exist; cross-process replay/effect reconciliation is separate. |

**Correction to the recovered starter:**
[ExternalToolset](https://github.com/pydantic/pydantic-ai/blob/d97c25c6d749b121494c28684273a3df37955803/pydantic_ai_slim/pydantic_ai/toolsets/external.py#L12)
uses `core_schema.any_schema()` for arguments, sets kind external, and direct
execution raises NotImplementedError. Advertising a JSON schema is therefore not
proof that this path validates its arguments against that schema. The ToolManager
also refuses direct external execution. [Test2918](https://github.com/pydantic/pydantic-ai/blob/d97c25c6d749b121494c28684273a3df37955803/tests/test_tools.py#L2918)
rejects treating an external call as locally approved execution. A future
interoperability seam would have to validate the real arguments at Devtools'
existing Tool boundary and authenticate result/authority provenance. No external
harness integration is implemented or chosen here.

### Pydantic AI: execution order, cancellation and state

[Tool processors](https://github.com/pydantic/pydantic-ai/blob/d97c25c6d749b121494c28684273a3df37955803/pydantic_ai_slim/pydantic_ai/_tool_execution.py#L320)
implement explicit end strategies:

- `early`: output Tools sequentially, first successful output wins; function
  Tools run only if all output Tools fail.
- `graceful` (default): model emission order; parallel function segments complete
  before the next output Tool; later output side effects are skipped after success.
- `exhaustive`: all eligible work executes; output winner follows emission order.
  A `sequential=True` Tool still forms a barrier that runs alone.

Function retries suppress a final result under graceful/exhaustive except where
streamed output is already committed. [Sequential tests10658](https://github.com/pydantic/pydantic-ai/blob/d97c25c6d749b121494c28684273a3df37955803/tests/test_agent.py#L10658)
assert shared-state order around a barrier. End strategies and result-event order
are explicit orchestration semantics; Devtools' native Tool batch is sequential,
and all source edit components admit atomically against a common baseline.
Parallel external execution is not equivalent to atomic source mutation and is
not a missing requirement merely because the upstream can parallelize.

On cancellation or sibling exception, [execution cleanup](https://github.com/pydantic/pydantic-ai/blob/d97c25c6d749b121494c28684273a3df37955803/pydantic_ai_slim/pydantic_ai/_tool_execution.py#L886)
cancels/drains pending tasks and retains already completed results in interrupted
history. Ordered result events may not have emitted those results. [Tests134–176](https://github.com/pydantic/pydantic-ai/blob/d97c25c6d749b121494c28684273a3df37955803/tests/test_run_cancellation.py#L134)
assert both facts separately. First-party RunCancelled is distinct from external
async cancellation; nested self-cancel can become a failed Tool return while
shared cancellation remains explicit. Tests493/609 cover resumable interrupted
Tool history. This prevents some duplicate redispatch, **not exactly-once external
effects**. A completed effect with no retained return remains ambiguous.

[Timeout tests3414–3477](https://github.com/pydantic/pydantic-ai/blob/d97c25c6d749b121494c28684273a3df37955803/tests/test_tools.py#L3414)
turn timeouts into model-facing retry feedback. The synchronous test explicitly
abandons a worker thread that runs to completion afterward. Automatic retries of
such effects would be unsafe without operation-specific repeatability and
reconciliation. Devtools Command cleanup and Checkout restoration do not undo
arbitrary outside effects either; B-0034 remains meaningful.

[Graph state](https://github.com/pydantic/pydantic-ai/blob/d97c25c6d749b121494c28684273a3df37955803/pydantic_ai_slim/pydantic_ai/_agent_graph.py#L806)
retains messages, retries, usage, deferred results and request parameters. Resume
rejects overriding an already recorded Tool result and uses skipped result
markers to avoid repeating recorded work. In-memory history/run state is not a
durable transaction log. The separate [Temporal FunctionToolset adapter](https://github.com/pydantic/pydantic-ai/blob/d97c25c6d749b121494c28684273a3df37955803/pydantic_ai_slim/pydantic_ai/durable_exec/temporal/_function_toolset.py#L34)
reconstructs prepared definitions and executes named activities through an external
workflow backend. Its durability/retry guarantees were **not** fully audited or
executed. No claim that core Agent.run alone persists every step is supported.
Devtools persistence/Checkout/WorkCycle already own different portions of state;
task-local working state belongs in B-0028 and the existing Memory proposal with
an explicit distinction from Conversation and retained source.

### Pydantic AI: instrumentation, usage and developer ergonomics

[Instrumentation capability](https://github.com/pydantic/pydantic-ai/blob/d97c25c6d749b121494c28684273a3df37955803/pydantic_ai_slim/pydantic_ai/capabilities/instrumentation.py#L256)
wraps run, model request, validation failure and Tool execution. Agent spans carry
run/conversation IDs; Tool spans carry call IDs and failure stage/retry information.
`include_content`/binary/parameter settings govern capture; model instrumentation
and telemetry serialization are separate from execution semantics. Validation
failures have spans even when no Tool executes. Run usage attribution separates
nested spend to avoid summing the same usage twice. [Instrumentation tests1184](https://github.com/pydantic/pydantic-ai/blob/d97c25c6d749b121494c28684273a3df37955803/tests/models/test_instrumented.py#L1184)
inspect retry feedback on spans; [redaction tests689–938](https://github.com/pydantic/pydantic-ai/blob/d97c25c6d749b121494c28684273a3df37955803/tests/test_instrumentation_content_redaction.py#L689)
cover successful/history/Tool retry/failure/provider/fallback/serialization paths
and reject another span's capture-policy attribution. These are real privacy
contracts to compare, not a claim all exporter deployments are safe or durable.

[UsageLimits](https://github.com/pydantic/pydantic-ai/blob/d97c25c6d749b121494c28684273a3df37955803/pydantic_ai_slim/pydantic_ai/usage.py#L505)
separates requests, tokens, successful Tool calls, per-request input and cost.
Token pre-count is opt-in; without it some limits are enforced after a response.
Unknown/unpriceable cost yields warning rather than invented price. [Tests1014/1102](https://github.com/pydantic/pydantic-ai/blob/d97c25c6d749b121494c28684273a3df37955803/tests/test_usage_limits.py#L1014)
check failed-call accounting and projected parallel-call bounds;1188 onward
distinguish per-request and cumulative input. Devtools prospective task ceilings
charge different units including refused proposals; provider ModelUsage and
InvocationMeasurement's availability/provenance are observations, not identical
enforcement or billing. Active Codex supervision and GPU energy remain unmeasured.

The ergonomic opportunity is **explicit reusable definition/validation feedback**,
not replacing an exact-source validator with Pydantic or adopting a graph runtime.
Function/Toolset composition, schema generation and clearly separated retry/
failed/denied results are useful reference mechanisms. Any local helper must
reduce demonstrated duplicated semantics, preserve model-neutral descriptors,
strict type/path/version behavior and exact budgets, and delegate execution to
the existing ToolRunner/Commands. B-0035 and the pending module-size investigation
retain that pressure. Syntax validation does not prove behavioral correctness.

### Editing and authority comparison

Neither inspected scheduler nor typed FunctionToolset supplies Devtools' complete
observed-source edit contract: authorized path/current content, exact prior
disclosure, unique match/absence, common pre-transaction anchors, UTF-8 byte bounds,
all-or-nothing admission, exact Git-applied bytes and Checkout restoration.
Current `apps/qwen/edits.py` already returns component/path/reason diagnostics.
Engineering19/22/28 include distinct size, anchor, integration and Context outcomes;
Engineering26's host EOF defect was independently corrected. Do not flatten these
into a generic claim that the edit Tool is bad or the model cannot reason.

[Pending ergonomics investigation](../backlog/proposals/88246171-d102-4b62-93d7-03c1e19f8a7b/proposal.json)
captures original CANDIDATE-08 with those concrete distinctions. Aider was the
next research area at this second checkpoint; the later
[Aider editing audit](#aider-host-editing-mechanics-and-lifecycle) now supplies
source/test findings. No live comparison, adapter, argument rewriting or
admission relaxation follows from either source review.

## Devtools end-to-end correlation map

The following is an inspected **join/loss map**, not a new trace schema.
Local source identities are pinned in the evidence metadata. Narrow Runtime is
not automatically in the native coding-loop path.

| Transition / emission point | Actual keys and retained facts | Loss/error paths, consumers and unresolved gap |
|---|---|---|
| Objective → task (`apps/qwen/tasks.py`, `development_task.py`) | CodingTask name, baseline revision, definition SHA-256, frozen oracle/runner/read/source hashes and resource limits; preflight/task receipts | Not every direct local task has a B-number or governed assignment. Objective prose is not authority; a universal run UUID is not present by implication. |
| Task → model (`coding_loop.py` `_turns`) | Folder/turn number, request/response/stage SHA-256, exact input/output observations, profile/capacity and model seconds; immutable raw native evidence | Stage is saved before provider send; provider exception/timeout can leave no normalized response/usage. No automatic retry after unknown completion. User-visible disposition and factual consumed usage remain separate. |
| Provider → model Evidence (`llama_cpp.py:send`) | Fresh ModelInteractionId, source/provider, timestamps; optional completed observer records provider response ID/model and capture manifest | Observer is called only after successful normalization and may itself raise after a model response exists. Failures before completion lack equivalent model Evidence. IDs are not returned as task-level joins in ModelResponse; native loop doesn't automatically install the inspector. |
| Runtime → terminal Evidence (`runtime.py`, `interaction_attempt.py`, `inspection.py`) | InteractionAttemptId linked to ConversationId/MessageId/source; EvidenceId and stage/outcome/time; process-local inspector and optional sink | Runtime preserves primary provider/cancel errors and suppresses secondary finish-observer failures. It cannot infer ModelInteractionId association. Native application invokes interaction directly; this observer is not its entire execution ledger. |
| Model → Tool (`coding_loop.py`, `context_tools.py`, `commands.py`) | Provider call ID, call name/arguments, correlated native Tool message; attempted/returned/refused Tool events with elapsed time and per-turn tools.json | ToolRunner only calls validate→execute; no shared ToolInvocation occurrence ID/span or global collector. A later Tool failure can leave earlier results retained; this does not roll back executed effects. Context refusal is feedback, unexpected host error propagates. |
| Tool → exact source (`context_tools.py`, `edits.py`) | Resource/content versions, source spans, observation call IDs, local edit references/exact-absence hashes; proposal/admission/component diagnostics; candidate fingerprints | Metadata/visibility is not edit authority. Source changes invalidate prior versions; absent new-file handling and exact EOF bytes have regressions. Rejection is atomic; validation occurs only after admitted installation. |
| Candidate → checks (`commands.py`, `change_checks.py`) | Candidate/task/source/plan/Git-before/after digests; separate check outcomes/times; full bundle and change-report evidence plus receipt SHA-256 | is_current authenticates stored payload/evidence and reobserves source/Git/plan. Current failed report remains failure. Cancellation attempts incomplete journal and propagates; evidence-write failure can remain incomplete. No publication authority. |
| Passing report → native acceptance (`coding_loop.py`) | Actual model check_changes call and host is_current result marked host-invoked; current passing candidate required in opt-in path | Restoring/replacing source invalidates candidate report. Model Tool use, host authentication and independent acceptance remain separately attributable. No blanket acceptance from a Tool returning successfully. |
| Checkout → recovery (`scripts/backlog/checkout.py`) | Owner operation/PID/entry branch+HEAD/scope, admitted fingerprints, original untracked hashes; sealed history receipt | Interrupted/unknown ownership requires inspection/default-No recovery, not deleting lease or blind redispatch. Restoration is source recovery, not undo of every external effect. |
| WorkCycle → review/publication (`integration/local.py`, `work.py`) | Frozen assignment/result/oracle/candidate hashes; exact review subject, validation input digests, implementation attribution; commit/ref/remote receipt | Review recommendation is not grant. Ambiguous commit/push reconciles actual Git identity, not blind retry. Local task closeout and B-number WorkCycle differ; no forced universal key. These facts are not automatically exported as model/Tool span children. |
| Commands live events (`resources/commands/events.py`, `execution.py`) | Started Command, stdout/stderr bytes, exit code/duration; bounded single-consumer stream and dropped count | Events lack a framework invocation/trace ID and may drop terminal events. Not a durable evidence log or proof an absent event means no effect. Caller-held stream identity is local correlation. |
| Usage (`observability/evidence/invocation.py`, `usage/`) | Typed measured availability/provenance, invocation/session observation identities, usage categories, executed/adopted distinction and reconciliation | Not automatically all native calls, account billing, supervisor active time or GPU energy. Raw receipts, measurements, spans and prices have different boundaries. Missing values stay unknown. |

Existing local tests corroborate these boundaries: `tests/tools/test_execution.py`
(admission, ordinary error, cancellation, independent calls),
`tests/execution/test_runtime.py` (provider/observer failures and cancellation),
`tests/models/interaction/providers/test_llama_cpp.py` (native IDs/reasoning/usage,
transport and malformed responses), `tests/observability/evidence/`,
`tests/apps/qwen/test_change_checks.py` (tampering, current failed reports,
drift and incomplete journals), and `tests/scripts/backlog/test_local_closeout.py`
(exact candidate/review/publication and attribution). They were inspected as
evidence locations; only documentation/layout/intake tests were run here.

### Findings and disposition

1. **Observed gap, B-0023/B-0011:** typed Evidence/usage/Command events already
   exist, but a joined lifecycle consumer does not automatically connect task,
   model occurrence, Tool call, validation and publication. Specify join strength,
   missing/failed realization, capture policy, observer failure and drop behavior
   before selecting spans/exporters. Neither an OTel span nor a SHA checksum
   authenticates publication authority or guaranteed replay.
2. **Observed difference, B-0035:** upstream definition helpers can reduce schema
   boilerplate, but coercion, replacement hooks and unvalidated external arguments
   change semantics. A small transparent wrapper is a candidate only after local
   duplication/compatibility measurement; no adoption decision.
3. **Research question, B-0044/B-0033:** soft exploration feedback and result-aware
   repetition differ from a fixed no-edit stop. They merit reading as policy
   references, not another Devtools phase controller or success prediction.
4. **Observed limit, B-0028/B-0034:** transcript resume/interrupted history reduces
   some repeat execution but cannot resolve unknown effects. External backends,
   idempotent operations and exact source restoration have distinct guarantees.
5. **Unmeasured, B-0046/B-0016:** same-model performance across harnesses, thinking/
   template/quantization choices, memory/latency and actual usage completeness.
   No serving or scientific run was authorized by this research checkpoint.

The [original18 reconciliation](reconciliation-input-reconciliation.md) routes
these findings through existing canonical items, append-only advisory reviews and
one distinct pending edit-ergonomics proposal. No prior proposal state/parent,
canonical B-number, ADR or grant changes.

## Second-checkpoint next research (historical)

Inspect pinned DeepSeek Harness and Aider implementation **and tests**, especially
session-event versus operational-event ownership, plugin trust/reversal, Tool
guard/cancellation paths, repository-map initial disclosure and edit-block failure
semantics. Do not launch it automatically. Then deepen Devtools' real successful/
failed receipt joins, dependency-complete destination adoption and custody/recovery
qualification. This review narrows questions; it neither completes the finite
audit nor authorizes a new Agent/Trace/EventBus/ModelAdapter.

## DeepSeek Harness and Aider source-and-test audit (2026-10-23)

This third checkpoint extends, rather than replaces, the earlier Qwen
Code/Pydantic AI findings. Devtools baseline is
`177098f4edd3dd7ea1b6bd889e1a1b1d5074a5fd`; remote main remains
`5d979920d0728775ed529457c88f5b68b440c64f`. Both upstream revisions in the initial
table remain pinned. Individual source/test files were authenticated against
the pinned Git tree with recomputed Git blob and SHA-256 hashes. The
[evidence metadata](agent-harness-mechanism-evidence-20261023.json) adds this
checkpoint without changing earlier records. Fetching a file is not exhaustive
inspection: the findings below identify the relevant functions/assertions.
No upstream package, test suite or agent was installed or executed. No inference,
production source/test change, architectural adoption or comparative effectiveness
measurement occurred. Claims are about these revisions, not current releases.

### DeepSeek: event domains and the actual durability boundary

The [architecture's event distinction](https://github.com/deepseek-ai/deepseek-harness/blob/687f282e8625c6b8d11ff58211a90524be2e4317/docs/architecture.md#L67)
is supported by separate producers/consumers, but its description of Session
events as durable facts needs the persistence preconditions below.

| Mechanism and pinned evidence | Observed behavior and failure boundary | Devtools comparison, opportunity and disposition |
| --- | --- | --- |
| Session append: `Session.append`/`commit`, [source](https://github.com/deepseek-ai/deepseek-harness/blob/687f282e8625c6b8d11ff58211a90524be2e4317/packages/core/session/src/index.ts#L798); [observer assertions](https://github.com/deepseek-ai/deepseek-harness/blob/687f282e8625c6b8d11ff58211a90524be2e4317/packages/core/session/tests/session.spec.ts#L1551) | Snapshot/JSON validation, surface validation, sequence assignment and frozen log insertion happen synchronously. Internal validation can reject before insertion. Public `session/event` observers run after insertion; synchronous/async failures are warned and contained per listener. Append neither awaits storage nor becomes rolled back when an observer fails. | Immutable Evidence and application JSON receipts already have owners in Devtools. A Session log is not a replacement for Evidence/Conversation/Run. B-0011/B-0023 should specify commit, notification and storage guarantees separately. High confidence in inspected boundary; no crash experiment. |
| Awaited `SessionStore.flush`, [source](https://github.com/deepseek-ai/deepseek-harness/blob/687f282e8625c6b8d11ff58211a90524be2e4317/packages/core/session/src/index.ts#L1319) | Requires the exact live session entry; invokes all collected flush listeners, awaits all settlements, then throws the first registered failure. Boolean means listener participation, not a per-writer durability certificate. Telemetry may register a listener too; a persistence listener can have no routed writer. In-memory SessionStore alone persists nothing. | Devtools checks authenticate actual evidence/source identities rather than an unqualified flush flag. B-0028/B-0011: any future durable owner needs explicit writer/backend participation and error semantics, not simply an EventBus callback count. |
| Handle contract, [interface](https://github.com/deepseek-ai/deepseek-harness/blob/687f282e8625c6b8d11ff58211a90524be2e4317/packages/session/session-persistence/src/handle.ts#L15); [JSONL live writer](https://github.com/deepseek-ai/deepseek-harness/blob/687f282e8625c6b8d11ff58211a90524be2e4317/packages/session/session-persistence-jsonl/src/storage.ts#L267) | General handle append accepts an ordered visible prefix and may buffer; flush is the crash-survival barrier promised by that interface. JSONL live routing batches copies for up to 200ms, retains failed batches, warns on background drain failure and pauses timer retries. Explicit drain/flush rejects. Public append and live routing are different entry paths. | Devtools snapshot persistence is not a generic append-only session journal. Existing filesystem atomic writes do not by themselves define a multi-record journal. B-0028/B-0034 cover backend consistency and reconciliation; do not equate enqueue with durable success. |
| JSONL concrete persistence, [persist implementation](https://github.com/deepseek-ai/deepseek-harness/blob/687f282e8625c6b8d11ff58211a90524be2e4317/packages/session/session-persistence-jsonl/src/index.ts#L1262); [lazy/flush/closing tests](https://github.com/deepseek-ai/deepseek-harness/blob/687f282e8625c6b8d11ff58211a90524be2e4317/packages/session/session-persistence-jsonl/tests/jsonl.spec.ts#L1411) | Create is visible in-process without a disk artifact. First append materializes; empty flush writes the header. Concrete writes sync the artifact; failed append attempts truncate/sync the previous length, reporting append plus rollback failure when both fail. A torn tail is read as its committed prefix and repaired on the write path. No generic filesystem/power-loss guarantee was independently measured. | Reuse Devtools' existing file/identity boundaries before considering a journal. Backend protocol promises, concrete sync calls and tested process interruption are three different evidence levels. |
| Writer ownership/close, [lease](https://github.com/deepseek-ai/deepseek-harness/blob/687f282e8625c6b8d11ff58211a90524be2e4317/packages/session/session-persistence-jsonl/src/lease.ts#L1), [close](https://github.com/deepseek-ai/deepseek-harness/blob/687f282e8625c6b8d11ff58211a90524be2e4317/packages/session/session-persistence-jsonl/src/storage.ts#L223), [tests](https://github.com/deepseek-ai/deepseek-harness/blob/687f282e8625c6b8d11ff58211a90524be2e4317/packages/session/session-persistence-jsonl/tests/lease.spec.ts) | One in-process writer plus native POSIX lock/Windows semaphore; no age-based takeover. Close drains late routed events, waits for mutations, releases ownership even if draining fails, and reports failures. Root plugin disposal is concurrent, so it is not a universal producer-before-writer shutdown order. Browser native-lock stub has a different single-process premise. | Checkout's exclusive source owner and default-No recovery are a different resource contract, already implemented. B-0034/B-0028 should audit wedged versus dead owners and unknown bytes; do not adopt upstream lock machinery or treat releasing ownership as rollback. |
| Checkpoint policy, [source](https://github.com/deepseek-ai/deepseek-harness/blob/687f282e8625c6b8d11ff58211a90524be2e4317/packages/session/session-checkpoint-policy/src/index.ts), [failure/cancel assertions](https://github.com/deepseek-ai/deepseek-harness/blob/687f282e8625c6b8d11ff58211a90524be2e4317/packages/session/session-checkpoint-policy/tests/session-checkpoint-policy.spec.ts#L96) | Optional composition flushes before adapter streaming, top-level Tool body and pre-step; nested Tools reuse the outer checkpoint. Rejection prevents body/adapter dispatch. Cancellation is checked again after a Tool checkpoint. Turn boundary records do not themselves automatically flush; memory-only creation is possible, while resume requires configured persistence. | Devtools ToolRunner is intentionally validate-then-execute, not a session durability service. B-0044/B-0028 must establish a real application need before adding lifecycle hooks; keep Runtime narrow. |

**Storage unavailable:** background persistence failure leaves the already
committed in-memory record intact and warns; an awaited failing writer barrier
rejects. Checkpoint-policy tests prove refusal before dispatch when its barrier
rejects. Without that policy, or without a writer, no universal durability-before-
effect guarantee follows. Close may fail after relinquishing ownership. There is
no exactly-once external effect guarantee.

### DeepSeek: composition, dispatch, history and instrumentation

| Mechanism and source/test evidence | Verified mechanism / limitations | Actual Devtools owner, useful question and backlog |
| --- | --- | --- |
| Cordis providers/consumers: [Service](https://github.com/deepseek-ai/deepseek-harness/blob/687f282e8625c6b8d11ff58211a90524be2e4317/vendor/cordis/src/service.ts), [Fiber effects](https://github.com/deepseek-ai/deepseek-harness/blob/687f282e8625c6b8d11ff58211a90524be2e4317/vendor/cordis/src/fiber.ts#L418), [harness lifecycle tests](https://github.com/deepseek-ai/deepseek-harness/blob/687f282e8625c6b8d11ff58211a90524be2e4317/packages/extensions/tool-cordis/tests/cordis-lifecycle.spec.ts) | Named service registration plus declared injection gates plugin activation. Effects register cleanup with the owning fiber, including partial setup/reentrant teardown; yielded cleanup order is reversed. Some unload failures are logged/contained, not universally propagated. Harness tests cover rollback, single-shot disposal, pending/loading registration and teardown observer containment; no separate vendored Cordis unit suite was identified in the inspected tree. | Existing explicit Python composition/Tool protocols and Checkout lifetimes need no DI container by analogy. Pending module investigation `39c6663a-bab7-43ed-8166-82e780a75d05` should measure repeated setup/cleanup responsibilities in native worker and experiment consumers before any helper. |
| Agent factory/loop: [driver](https://github.com/deepseek-ai/deepseek-harness/blob/687f282e8625c6b8d11ff58211a90524be2e4317/packages/core/agent-loop/src/agent.ts#L306), [construction/teardown](https://github.com/deepseek-ai/deepseek-harness/blob/687f282e8625c6b8d11ff58211a90524be2e4317/packages/core/agent-loop/src/index.ts#L541), [resume tests](https://github.com/deepseek-ai/deepseek-harness/blob/687f282e8625c6b8d11ff58211a90524be2e4317/packages/core/agent-loop/tests/resume.spec.ts#L479) | Agent interface/registry is separate from default AgentLoop driver. Steps record model work and Tool outcomes; turn admission/inbox/continuation are loop-owned. Teardown cancels/drains the machine before releasing scoped resources/writer. Failed construction unwinds staged publication; rollback can suppress secondary close failure while normal disposal reports it. | ModelInteraction and narrow Runtime are not this loop. `apps/qwen/coding_loop.py` owns current task-local orchestration; B-0043/B-0044 retain promotion boundaries. A shared base Agent or lifecycle controller is not established by this comparison. |
| Tool definitions: [defineTool](https://github.com/deepseek-ai/deepseek-harness/blob/687f282e8625c6b8d11ff58211a90524be2e4317/packages/core/tools/src/schema.ts#L554), [schema tests](https://github.com/deepseek-ai/deepseek-harness/blob/687f282e8625c6b8d11ff58211a90524be2e4317/packages/core/tools/tests/schema.spec.ts), [registry](https://github.com/deepseek-ai/deepseek-harness/blob/687f282e8625c6b8d11ff58211a90524be2e4317/packages/core/tools/src/index.ts#L1377) | Typed schema DSL infers arguments and wraps validation before the user body. Raw registered Tools still own input validation; registry enforces canonical JSON output schema/rendering. Scoped visibility, pre-policy, monotonic denial guards, around-dispatch and post-policy are distinct stages. `ask` without an approval channel/agent denies; allowed-once is not a standing grant. | `Tool`, ToolRunner, CommandTool and application-specific native argument validation already exist. B-0035 plus pending ergonomics review: measure duplicate descriptor/schema/argument definitions in ContextTools and CodingCommands before proposing a transparent helper. Do not add a competing authorization layer or infer input enforcement from schema visibility alone. |
| Ordered/concurrent dispatch: [scheduler](https://github.com/deepseek-ai/deepseek-harness/blob/687f282e8625c6b8d11ff58211a90524be2e4317/packages/core/agent-loop/src/tool-calls.ts#L60), [ordering assertions](https://github.com/deepseek-ai/deepseek-harness/blob/687f282e8625c6b8d11ff58211a90524be2e4317/packages/core/agent-loop/tests/tool-calls.spec.ts#L230), [uncooperative cancellation assertion](https://github.com/deepseek-ai/deepseek-harness/blob/687f282e8625c6b8d11ff58211a90524be2e4317/packages/core/tools/tests/tools.spec.ts#L1653) | Exclusive barriers and bounded parallel-safe calls; results/post-policy/context commit in model order despite out-of-order completion. Abort stops replenishment and drains started bodies; unstarted calls receive synthetic errors. An uncooperative body can delay completion. Timeout/abort is not undo of effects. | Devtools native batch correlation and later-call failure preservation have existing tests; ToolRunner itself does not schedule a parallel pool. B-0032/B-0034/B-0044: ordering/effect ambiguity before concurrency abstraction. |
| Interrupted history: [recovery](https://github.com/deepseek-ai/deepseek-harness/blob/687f282e8625c6b8d11ff58211a90524be2e4317/packages/core/session/src/repair.ts), [assertions](https://github.com/deepseek-ai/deepseek-harness/blob/687f282e8625c6b8d11ff58211a90524be2e4317/packages/core/session/tests/repair.spec.ts#L54) | Matching turn/step/call ID differentiates requested-but-not-started from started-without-result. Recovery appends explicitly synthetic unknown/not-started errors then closes step/turn, preserving historical events. Fork guidance acknowledges a parent may act after the cut. Resume writes closers through its writer before publishing. No blind retry or claim that an unknown Tool effect failed. | Native raw receipts and Checkout restoration/recovery already preserve failed outcomes. They do not implement general durable session replay. B-0034/B-0028 and pending Memory investigation: restore representation is not permission to repeat effects. |
| Live versus recorded model stream: [attempt](https://github.com/deepseek-ai/deepseek-harness/blob/687f282e8625c6b8d11ff58211a90524be2e4317/packages/core/agent-loop/src/assistant-stream.ts#L40), [scope dispatch](https://github.com/deepseek-ai/deepseek-harness/blob/687f282e8625c6b8d11ff58211a90524be2e4317/packages/core/agent/src/dispatch.ts#L49), [cancel tests](https://github.com/deepseek-ai/deepseek-harness/blob/687f282e8625c6b8d11ff58211a90524be2e4317/packages/core/agent-loop/tests/cancel.spec.ts) | Live frames carry attemptId/revision/index; terminal frame cites the committed Session sequence or explicit abandonment. Stream chunks and latest adapter usage also feed assistant message/attempt records. Request header/context records preserve routed model/configuration; Tool results cite call sequences/IDs. Agent notifications contain observer failures; awaited serial/waterfall hooks intentionally can affect control. | Model Evidence has ModelInteractionId/provider-call IDs/capture manifest; Runtime terminal Evidence has a separate InteractionAttemptId. Native receipts do not automatically join these identities. B-0023/B-0011 need a consumer join/loss contract, not a new catch-all Trace identity. |
| Compaction: [surface fold](https://github.com/deepseek-ai/deepseek-harness/blob/687f282e8625c6b8d11ff58211a90524be2e4317/packages/core/session/src/surface.ts#L329), [backend](https://github.com/deepseek-ai/deepseek-harness/blob/687f282e8625c6b8d11ff58211a90524be2e4317/packages/compaction/compaction-basic/src/index.ts#L144), [stale/failure assertions](https://github.com/deepseek-ai/deepseek-harness/blob/687f282e8625c6b8d11ff58211a90524be2e4317/packages/compaction/compaction-basic/tests/compaction-basic.spec.ts#L1189) | Appended replacement events shadow validated surface ranges with source-sequence citations; original log remains. Boundaries preserve Tool pairing. Stale surfaces/nonshrinking summaries reject; auxiliary summarization failures are recorded. Overflow retries require actual surface generation progress, not a claimed successful compaction. Optional model-free pruning is separate. | Devtools application projection retains raw native requests/results and authentic source/edit observations. It is not this summarizing surface journal. Existing Context ownership and B-0002/B-0044 suffice; no new compiler/history system follows. |
| Telemetry/export/privacy: [coordinator](https://github.com/deepseek-ai/deepseek-harness/blob/687f282e8625c6b8d11ff58211a90524be2e4317/packages/session/session-telemetry/src/coordinator.ts#L198), [OTel backend](https://github.com/deepseek-ai/deepseek-harness/blob/687f282e8625c6b8d11ff58211a90524be2e4317/packages/session/session-telemetry-otel/src/index.ts#L144), [egress tests](https://github.com/deepseek-ai/deepseek-harness/blob/687f282e8625c6b8d11ff58211a90524be2e4317/packages/session/session-telemetry-otel/tests/otel.spec.ts#L129) | Generic coordinator supports live/on-demand capture; default redaction waterfall passes through unless deployment rules exist. This OTel provider defaults to feedback-only canonical prefix capture, excludes inherited/noncanonical feedback, ignores direct emits, and disabled mode creates no transport. It exports Session log records, not automatically a task-to-publication span tree. Shutdown deadline may abandon queued records; capture errors are contained. | Devtools capture policy defaults to omitted model payload categories, with explicit availability/provenance. Command events may drop; usage is measured separately. B-0018/B-0023/B-0011: event selection, egress consent, redaction and delivery loss must remain distinct. No guarantee of comprehensive PII removal or collector receipt. |

**Trust boundary:** [configured entries](https://github.com/deepseek-ai/deepseek-harness/blob/687f282e8625c6b8d11ff58211a90524be2e4317/vendor/loader/src/config/entry.ts#L225)
import a module and mount it in the process/context; injection and fiber scoping
are lifecycle mechanisms, not a security sandbox. The
[loader's optional Node-internal access](https://github.com/deepseek-ai/deepseek-harness/blob/687f282e8625c6b8d11ff58211a90524be2e4317/vendor/loader/src/internal.ts#L104)
uses exposed internals or a native helper and probes supported loader shapes.
The JSONL lock also uses platform-native support. Configured module provenance,
transitive packages, native builds, config-expression evaluation and Node-version
compatibility are supply-chain review inputs. We did not audit every dependency,
verify releases/signatures or demonstrate a vulnerability. Permission hooks on
Tools do not restrict arbitrary trusted plugin code. Developer-preview claims
are not production reliability evidence. Devtools does not need a dynamic plugin
loader merely to offer typed Tools; B-0035/B-0018 retain that distinction.

### Aider: map construction, prompt composition and freshness

| Mechanism and pinned source/test | Observed behavior / failure semantics | Devtools owner, difference and disposition |
| --- | --- | --- |
| Definition/reference tags and graph: [repomap](https://github.com/Aider-AI/aider/blob/5dc9490bb35f9729ef2c95d00a19ccd30c26339c/aider/repomap.py#L279), [ranking](https://github.com/Aider-AI/aider/blob/5dc9490bb35f9729ef2c95d00a19ccd30c26339c/aider/repomap.py#L365), [tests](https://github.com/Aider-AI/aider/blob/5dc9490bb35f9729ef2c95d00a19ccd30c26339c/tests/basic/test_repomap.py#L163) | Tree-sitter query tags, with lexical reference fallback where needed; lexical identifier names join referrers to possible defining files. Weighted directed multigraph/PageRank uses chat files, mentioned paths/identifiers and spelling heuristics; common/private names are downweighted. This is not proof of resolved imports/calls. | `context/retrieval/graph/` and `repository_map/` already rank typed native RI evidence; lexical/source owners already exist. B-0002 and pending CodeGraph proposal `ae03cda7-955e-40c6-a131-9e2ba209c9a6`: compare evidence semantics and real navigation benefit, not build a second graph. |
| Prompt inclusion: [get_repo_map/messages](https://github.com/Aider-AI/aider/blob/5dc9490bb35f9729ef2c95d00a19ccd30c26339c/aider/coders/base_coder.py#L709), [message composition](https://github.com/Aider-AI/aider/blob/5dc9490bb35f9729ef2c95d00a19ccd30c26339c/aider/coders/base_coder.py#L1281) | User mentions personalize other-file orientation. In-chat/read-only files are separated from other files; ranked definition snippets exclude chat files already supplied as file Context. Map is a user-message component before file contents, with an ask-before-edit instruction. It is neither an exact source observation nor an authorization token. | Caller-directed Planning and opt-in native `repository_map`/`expand_source(to='source')` already connect maps to attested editable source. Engineering28 availability without native map invocation is not effectiveness evidence. Opportunity is task Context ergonomics within existing ownership, not another API factory. |
| Budget and cache: [map selection](https://github.com/Aider-AI/aider/blob/5dc9490bb35f9729ef2c95d00a19ccd30c26339c/aider/repomap.py#L629), [refresh assertions](https://github.com/Aider-AI/aider/blob/5dc9490bb35f9729ef2c95d00a19ccd30c26339c/tests/basic/test_repomap.py#L49) | Binary-searches ranked prefixes with about 15% tolerance; long-text token counts are sampled estimates. With no chat files the map budget can grow subject to model-window allowance. Tags cache by file mtime; map cache keys file sets/budget and, for auto, mentions, not content identity. `files` and slow-build `auto` tests intentionally keep old content until refresh. Manual reuse can also remain stale. | Devtools retained snapshots/map identities and candidate-version invalidation offer stronger source binding; model-request capacity uses its own provider/tokenizer policy. No measured token/retrieval efficiency comparison. B-0002 should preserve freshness and explicit refresh even if borrowing orientation ergonomics. |

### Aider: host editing mechanics and lifecycle

The crucial guarantees differ from Devtools. Aider asks less exact bookkeeping
of the model and accepts more host interpretation. That can be convenient; this
audit did not measure whether it improves this local Qwen model's success rate.

| Mechanism and source/test evidence | Observed behavior / limits | Devtools contrast and backlog disposition |
| --- | --- | --- |
| Edit-block parsing: [parser/matcher](https://github.com/Aider-AI/aider/blob/5dc9490bb35f9729ef2c95d00a19ccd30c26339c/aider/coders/editblock_coder.py#L127), [assertions](https://github.com/Aider-AI/aider/blob/5dc9490bb35f9729ef2c95d00a19ccd30c26339c/tests/basic/test_editblock.py#L249) | Host parses filenames/fences and SEARCH/REPLACE blocks. First exact occurrence wins; it need not be unique. Then uniform indentation, leading blank removal and paired ellipsis strategies can apply. The edit-distance fuzzy call below the unconditional return is unreachable in this active matcher; similar-line suggestions are diagnostic, not proof of automatic fuzzy application. | Devtools `edits.py` requires exact unique authorized observed text/current version or exact absence, with component diagnostics and byte limits. Pending edit ergonomics `88246171-d102-4b62-93d7-03c1e19f8a7b` may investigate simpler presentation; no tolerant admission, argument rewriting or scope change is authorized. |
| Cross-file fallback and partial edits: [apply_edits](https://github.com/Aider-AI/aider/blob/5dc9490bb35f9729ef2c95d00a19ccd30c26339c/aider/coders/editblock_coder.py#L41), [prepare/apply](https://github.com/Aider-AI/aider/blob/5dc9490bb35f9729ef2c95d00a19ccd30c26339c/aider/coders/base_coder.py#L2296) | Failed nonempty SEARCH scans alternate in-chat files and accepts the first replacement. Dry-run returns redirected paths before `prepare_to_edit` performs file/ignore/confirmation handling. Real application writes successful blocks immediately, accumulates failures, then raises feedback telling the model not to resend successes. This is not a permission bypass claim; target interpretation and atomicity differ. | Devtools rejects the whole transaction with no sibling application or silent redirection. Local deterministic rejection/repair tests already cover wrong-owner anchors, sizes, overlap and correlated feedback. Cross-file fallback/partial behavior is verified from source; the inspected basic tests cover matching/new files/dry-run, but no direct assertion for every fallback-plus-partial combination was found. Do not overstate coverage. |
| New files and bytes: [normalization](https://github.com/Aider-AI/aider/blob/5dc9490bb35f9729ef2c95d00a19ccd30c26339c/aider/coders/editblock_coder.py#L335), [I/O](https://github.com/Aider-AI/aider/blob/5dc9490bb35f9729ef2c95d00a19ccd30c26339c/aider/io.py#L453), [newline setting tests](https://github.com/Aider-AI/aider/blob/5dc9490bb35f9729ef2c95d00a19ccd30c26339c/tests/basic/test_io.py#L16) | Empty SEARCH creates/appends after host permission handling. Wrapper stripping normalizes lines and appends a final newline; text reads use universal newline handling and writes select platform/LF/CRLF policy. PermissionError writes retry with backoff. The no-final-newline edit-block test tests response parsing, not admitted-versus-applied original-byte equality. | Devtools exact-absence creation, Git EOF markers and post-application byte equality are stronger/different obligations. Engineering26 recovery remains a host defect, not a reason to normalize away unproposed bytes. No upstream guarantee of original CRLF/EOF preservation is inferred. |
| Other editing formats: [unified diff](https://github.com/Aider-AI/aider/blob/5dc9490bb35f9729ef2c95d00a19ccd30c26339c/aider/coders/udiff_coder.py#L69), [whole-file](https://github.com/Aider-AI/aider/blob/5dc9490bb35f9729ef2c95d00a19ccd30c26339c/aider/coders/wholefile_coder.py), [udiff tests](https://github.com/Aider-AI/aider/blob/5dc9490bb35f9729ef2c95d00a19ccd30c26339c/tests/basic/test_udiff.py), [whole-file tests](https://github.com/Aider-AI/aider/blob/5dc9490bb35f9729ef2c95d00a19ccd30c26339c/tests/basic/test_wholefile.py) | Unified-diff path normalizes hunks, can reduce context/apply sections and uses flexible search preprocessing; successful hunks can remain when others fail. Its active strategy is search/replace with blank/indent/reversal preprocessing, not every diff-match-patch research helper in `search_replace.py`. Whole-file mode infers filenames/fences and writes complete content. Formats have distinct failure contracts; parser tests are not full transactional proofs. | Model-specific format choice is not exact-source authority. No new editor/format adapter should bypass existing transaction application. Pending ergonomics investigation records source mechanisms and uncertainty, not an adoption decision. |
| Model/host division: [model settings](https://github.com/Aider-AI/aider/blob/5dc9490bb35f9729ef2c95d00a19ccd30c26339c/aider/models.py#L331), [architect/editor](https://github.com/Aider-AI/aider/blob/5dc9490bb35f9729ef2c95d00a19ccd30c26339c/aider/coders/architect_coder.py#L11), [prompt](https://github.com/Aider-AI/aider/blob/5dc9490bb35f9729ef2c95d00a19ccd30c26339c/aider/coders/editblock_prompts.py) | Model metadata/configuration selects edit formats; architect mode can confirm then delegate instructions to an editor coder/model. Host constructs maps, parses edits, finds matches, writes files and reflects errors. This is a coding application, not merely a provider adapter or a model-neutral schema validator. | Devtools separates Model from Agent and external Codex integration. B-0043/B-0044/B-0046 retain orchestration/configuration decisions; no model-specific Agent subclass or new planner follows. |
| Feedback, Git and tests: [application loop](https://github.com/Aider-AI/aider/blob/5dc9490bb35f9729ef2c95d00a19ccd30c26339c/aider/coders/base_coder.py#L1589), [Git owner](https://github.com/Aider-AI/aider/blob/5dc9490bb35f9729ef2c95d00a19ccd30c26339c/aider/repo.py), [coder tests](https://github.com/Aider-AI/aider/blob/5dc9490bb35f9729ef2c95d00a19ccd30c26339c/tests/basic/test_coder.py) | Malformed edits become reflected feedback bounded by reflection policy. Dirty-file commit handling and auto-commits are configurable; source auto-commit can precede lint/test repair. Lint is enabled by default, automatic tests are not; configured failure repair can ask the user. None proves independent acceptance, rollback, exact coverage or protected promotion. | Devtools `check_changes` preserves independent outcomes/currentness, then WorkCycle separately authenticates source, review and publication. A successful command is not authority. B-0033/B-0034/B-0035 cover diagnostics/side effects; no replacement of WorkCycle. |
| Provider, reasoning and usage: [completion](https://github.com/Aider-AI/aider/blob/5dc9490bb35f9729ef2c95d00a19ccd30c26339c/aider/models.py#L985), [usage](https://github.com/Aider-AI/aider/blob/5dc9490bb35f9729ef2c95d00a19ccd30c26339c/aider/coders/base_coder.py#L1994), [model tests](https://github.com/Aider-AI/aider/blob/5dc9490bb35f9729ef2c95d00a19ccd30c26339c/tests/basic/test_models.py) | LiteLLM/provider settings adapt messages and optional function schemas; usual text edit formats are not native Tool calls. Reasoning removal/display is distinct from applied edit content. Reported usage is preferred, otherwise token estimates; cost uses provider calculator or configured prices. Streaming/provider/model differences remain. | Devtools normalized ModelResponse/ModelToolCall and InvocationMeasurement already distinguish availability/provenance and adopted versus executed usage. B-0023/B-0046 should join real failures/partial responses before claiming complete spend visibility. No provider-equivalence or billing-accuracy claim. |

### Local foundations and developer-experience conclusions

The earlier correlation table remains the local ownership map. This checkpoint
rechecked ToolRunner's semantic validate/execute boundary, ModelInteraction
capture defaults/provider completion hook, InvocationMeasurement availability,
Command event payloads, ContextTools map/source gates and Checkout recovery code.
It also identifies actual receipt paths in the
[next lifecycle audit plan](development-lifecycle-audit-plan.md).

Observed reuse candidates are deliberately narrower than a framework adoption:

1. **Tool definitions (B-0035, module proposal):** ContextTools combines
   `_SCHEMAS`, descriptors, native calls and domain admission; CodingCommands
   combines operation descriptors, argument handling and fixed managed checks.
   These are two realistic consumers for a duplication audit. Their validation
   semantics differ; common spelling is not proof a decorator/base class helps.
   Compare invalid-input feedback, coercion prohibition and descriptor drift
   before proposing a helper that delegates to current ToolRunner.
2. **Visibility (B-0023/B-0011/B-0018):** model completion Evidence, terminal
   Evidence, Command events, check journals and WorkCycle receipts are useful
   distinct substrates. The missing work is an authenticated join/loss consumer
   for actual development flows, including failed/missing occurrences and capture
   policy. Live instrumentation, immutable evidence, durable storage and usage
   should not collapse into one log. DeepSeek's log exporter is not automatically
   a solution to this local gap.
3. **Edit ergonomics (pending `88246171-d102-4b62-93d7-03c1e19f8a7b`):** simpler
   syntax/presentation may reduce model burden, but cross-file fallback,
   whitespace repair, partial writes and automatic commits change guarantees.
   Keep exact observations, UTF-8 limits, current versions and all-or-nothing
   application. No measured same-model benefit justifies changing those now.
4. **Navigation (B-0002, pending CodeGraph proposal):** graph/map/source APIs and
   native opt-in integration already exist. Investigate actual selection,
   freshness and repeated information before adding ranking or another reader.
   Aider supplies a concrete automatic prompt-composition reference, not evidence
   that Devtools lacks maps or that its tested retained-source contract is wrong.
5. **Lifecycle/maintenance (B-0043/B-0044):** typed hooks, disposal and inspection
   might serve future report-only maintenance/quality agents, but no shared
   lifecycle helper has been qualified for those consumers. First audit existing
   native-worker and WorkCycle failure paths. No generic Logger/EventBus/Agent,
   DI container, class hierarchy, session journal or upstream dependency is
   selected by this report.

Existing canonical item evidence and append-only ADVISORY proposal reviews
capture these findings. No new pending proposal is needed: the distinct pressures
are already represented. No status, parent, grant, approval or B-number changes.

### Confidence, remaining uncertainty and next bounded audit

Confidence is high for cited source control flow and selected test assertions,
bounded for whole-package/platform behavior. Upstream tests were inspected, not
run. No exploit, durability crash/power-loss, latency, token efficiency, agent
success-rate or comparative model claim was measured. Full plugin supply-chain
and exporter internals, every provider, filesystem/network-storage semantics,
and every editing-format edge remain outside this bounded inspection.

The four selected projects now have source-and-test mechanism comparisons. This
does not complete architectural reconciliation. Next execute the five-flow
[observability/lifecycle audit plan](development-lifecycle-audit-plan.md), joining
existing immutable receipts without replay, new inference, implementation or
cleanup. Then reconcile destination adoption and exact artifact custody before
the successor-session handoff. No further external harness installation or
generic infrastructure increment is authorized by this research.

### Third-checkpoint verification

Documentation/layout and existing intake tests passed (36 tests, 1.69s,
`--no-cov`). Introduced links/anchors and pinned file/line references, JSON,
intake hash chains, prior proposal states, original18 input/crosswalk preservation,
21 selected receipt fingerprints and all13 forensic identities were checked.
Only documentation/intake evidence changed. No production protected gate or
upstream tests ran, because no production source/tests changed. The evidence
metadata records the validation scope; it is not a new scientific result.

## Executed local lifecycle comparison follow-up

The [five-flow Devtools audit](development-lifecycle-observability-audit.md) now
tests the earlier join/loss map against original receipts. It authenticates all21
selected inputs, distinguishes absent observers from missing framework types,
and compares reuse of current records, a narrow tracing seam and operational
OTel spans. Existing source authority and publication remain separate. The
prospective turn06 expansion was refused; no source was disclosed by that call.
No external harness result, historical model outcome or accepted ADR changes.
Next is local destination adoption/ownership/custody reconciliation, not another
external install or tracing implementation.


## Context-compaction follow-up — 2026-10-28

The [budget-aware Context research reconciliation](agent-context-compaction.md)
adds independently pinned current harness inspection, qualified empirical papers,
the frozen Case 0003 request accounting and a proposed hybrid decision package.
It does not replace this October 23 review's versions or historical conclusions.
Only the research direction is approved; concrete implementation remains pending.
