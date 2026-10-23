# Agent harness mechanism review: Qwen Code and Pydantic AI

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
captures original CANDIDATE-08 with those concrete distinctions. Aider editing
mechanisms and their tests are a **next** research area, not analyzed/selected
here. No live comparison, adapter, argument rewriting or admission relaxation
follows from this source review.

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

## Next bounded external research

Inspect pinned DeepSeek Harness and Aider implementation **and tests**, especially
session-event versus operational-event ownership, plugin trust/reversal, Tool
guard/cancellation paths, repository-map initial disclosure and edit-block failure
semantics. Do not launch it automatically. Then deepen Devtools' real successful/
failed receipt joins, dependency-complete destination adoption and custody/recovery
qualification. This review narrows questions; it neither completes the finite
audit nor authorizes a new Agent/Trace/EventBus/ModelAdapter.
