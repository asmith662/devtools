# LLM harness, agent roles and memory audit

Audit of `main` at `9df553aec96c7882b523a289542cec10616d4b8a`, 2026-11-04.
This report qualifies visible integration behavior, not Qwen's general coding
capability. No new generation, native attempt, review dispatch, service change or
protected comprehensive validation occurred. Existing failed outcomes remain failed.

## Findings by severity

**High: the native coding application lacks a dedicated system-role agent
instruction and a qualified request profile.** Its task and source guidance exist,
but the application sends three user messages initially. The renderer supplies a
system Tool block; it does not supply a repository-coding procedure. Thinking is
explicitly disabled while inherited sampling differs from official instruct
guidance. These are confounds to measure before assigning failures to capability.

**Medium: repair state, budgets and output delivery need qualification.** Exact
active source ranges already exist. Coding limits are enforced internally but
remaining call/proposal/acquisition counts are not exposed in the audited coding
header. Current structured review delivery has deterministic coverage but no
authenticated live qualification. Optional semantic compaction is not activated
by native coding; none of these coding episodes needed pressure-driven reduction.

**Medium: the validation wrapper deadline is wrong for observed runtimes.** The
maintained comprehensive wrapper allows 3,600 seconds; recent unchanged-policy
protected runs took 4,092.61 and 4,503.60 seconds. B-0047 already tracks this.

**Cleared premises:** missing `--jinja` is not a disabled-engine defect in this
build. Native Tool definitions, IDs, correlated results and token measurement
are present. A new source-read ledger would duplicate existing capability.

## Evidence and limits

The compact [findings](code-audit/llm-harness-20261104/findings.json) authenticate
four coding episodes: B-0051 original/child, B-0052 and B-0053, totaling **18
historical coding responses**. Each assignment/result and referenced observation
was read through its existing digest/schema owner. All 18 responses were native
Tool-call responses. Three B-0052 reviews contributed six historical responses.
The reviewer event names are `review-model-intent`/`review-model-returned`, distinct
from coding capture names; the audit uses those actual schemas.

Historical captures are normalized `ModelRequest`/`ModelResponse`, not archived
HTTP bodies. The llama.cpp serializer blob is identical at all four coding base
commits and audit HEAD. Exact JSON bodies were reconstructed using that serializer;
current `/apply-template` and `/tokenize` were then exercised without inference.
Five selected historical input counts reproduce exactly: 1,587, 4,466, 22,143,
1,916 and 2,014 tokens. This is strong input-path correspondence, not proof that
unrecorded historical HTTP responses or model internals were inspected.
Current inherited defaults are measured; original per-response server-resolved
sampling receipts were not captured.

Raw current metadata, reconstructed bodies, rendered prompts, installed help and
pinned upstream source are retained in `.local/llm-harness-audit-20261104/`.
Publication keeps compact identities and findings rather than another historical
archive. Private oracle implementations are excluded from calibration Context.

## Actual request and rendering

The path is WorkCycle native execution → `AcceptanceHost` →
`RepositoryCodingHost` → `ModelRequest` → `LlamaCppInteraction` → llama.cpp.
Relevant owners are [coding navigation](../../src/devtools/agents/coding/navigation.py),
[coding host](../../src/devtools/agents/coding/repository.py),
[native execution](../../scripts/backlog/native/execution.py) and
[adapter](../../src/devtools/models/interaction/providers/llama_cpp.py).

| Boundary | Authenticated behavior |
| --- | --- |
| Initial coding messages | User objective (including explicitly untrusted prior public feedback for the child), user current inventory, user `active_source_status`; no application system message |
| Later messages | Assistant calls and correlated Tool results; exact source/check feedback retained in bounded history |
| Tool definitions | Native OpenAI-style function objects with names, descriptions and parsed JSON Schemas; complete definitions are in `findings.json` |
| Available coding callables | `read_source`, `replace_source`, `validate_candidate`, `find_source`, `read_source_unit` |
| Core argument contracts | Unicode half-open offsets for reads; exact unique observed replacements; fixed validation with empty arguments; scoped search and snapshot/unit-bound reads |
| Correlation | Native call IDs and `tool_call_id` are preserved; typed Prompt rejects duplicate, missing or incomplete associations |
| Generation body | `model`, `messages`, `stream:false`, `max_tokens:2048`, `chat_template_kwargs.enable_thinking:false`, `tools` |
| Missing optional fields | No `response_format`, `tool_choice`, explicit sampling or reasoning-effort field in audited native requests |
| Capacity | 65,536 context; 62,464 input ceiling; 2,048 output reservation, leaving 1,024 safety tokens |
| Source feedback | Exact text, snapshot/version/span, partial flag, continuation offset and remaining range; bounded disclosure is distinguishable from a full read |

`/apply-template` uses the same OpenAI-compatible chat parameter parser as
generation, without its inference phase, in the
[pinned server source](https://github.com/ggml-org/llama.cpp/blob/304665fe7/tools/server/server-context.cpp#L5060).
Rendered prompts begin with a system Tool block and use Qwen3.8 XML function and
parameter tags. Tool responses are rendered as native response blocks; JSON IDs
remain client-side correlation metadata rather than required visible prompt IDs.
The final generation prefix closes an empty thinking block, consistent with
`enable_thinking:false`.

The installed template explicitly requires object-form template arguments; the
adapter supplies standard JSON-string OpenAI arguments. Rendering actual history
with those calls succeeds and renders their parameters, demonstrating compatible
server normalization at that boundary. No hand-written Tool flattening is needed.

## Installed versus recommended configuration

The binary reports **0.4.0-dev, build 10868, commit `304665fe7`**. Its help says
Jinja defaults enabled; pinned `common_params.use_jinja` is true and the server
example does not disable it. No relevant environment override is present. Actual
rendering and `/props.chat_template_caps` confirm Tool, system-role, parallel-call
and reasoning-effort support. The absence of a launcher flag is therefore
functionally equivalent to explicit `--jinja` here. See
[default](https://github.com/ggml-org/llama.cpp/blob/304665fe7/common/common.h#L638)
and [argument handling](https://github.com/ggml-org/llama.cpp/blob/304665fe7/common/arg.cpp).

Model metadata reports 27,320,697,856 parameters, IQ4_XS 4.25 bpw, 14,241,849,344
bytes, vocabulary 248,320 and trained context 262,144. The approved deployment
still has one 65,536-token slot. The pinned GGUF artifact is
`40fac4050e940397dbf13087afd50f4734a11805bf9d65ef8ddd7483470e6199`;
this audit reauthenticated the existing read-only mount/configuration, without
rehashing the entire model file.

| Setting | Current effective request/server | Comparison target |
| --- | --- | --- |
| System coding role | Absent from application | Explicit trusted role/procedure, with task and source data remaining user/Tool messages |
| Thinking | Explicit false | Retain for initial calibration; separately qualify true |
| Temperature | 1.0 | Instruct 0.7 |
| top-p | Approximately .95 | Instruct .8 |
| top-k | 20 | 20 |
| min-p | Approximately .05 | 0 |
| Presence penalty | 0 | Instruct 1.5 |
| Repetition penalty | 1 | 1; already matches, not exposed as an adapter override |
| KV K/V | Both `q4_0`, verified launcher arguments | Separate q8_0/f16 comparison, subject to actual memory qualification |
| Output constraint | Native Tools, automatic choice; no forced text JSON | Qualify the intended callable/text channel separately |
| Reasoning output | Server `reasoning_format:none` | Qualify before thinking; reasoning can remain in content rather than a separate channel |

The instruct values match the [official model card](https://huggingface.co/Qwen/Qwen3.8-27B)
and existing `scripts/qwen/llama_cpp_profile.py` presets. Official thinking
guidance differs. Neither preset is installed by native execution:
`Guarded.send` expressly rejects non-None provider settings. The adapter already
supports typed sampling and `json_object`; applying either to a native assignment
requires a prospective authenticated profile/authority change, not guard removal.

The embedded template is an Unsloth modification: 9,993 UTF-8 bytes, SHA256
`12827f24b742ea4e80cdc12dbcf9622227056b9f797252a3149263d4f9aaadce`.
The [official template at revision 1d4bf0f2](https://huggingface.co/Qwen/Qwen3.8-27B/blob/1d4bf0f2ff6012fd82039f2fa52739d0dd7c60c0/chat_template.jinja)
is 8,952 bytes, SHA256
`c3cf9e34abf4f9e36c2d72165aa9c132d3e2a725b6c2586aaa3a8af9d7a81041`.
Differences include merging leading system/developer messages, effort aliasing
and argument validation. Both describe the same native XML Tool syntax. Current
rendering is qualified for the inspected requests; equivalence for every role,
template revision or unusual argument type is not claimed. The engine was not
replaced and the current official template was not installed.

Current hardware observation: RTX 4090 Laptop GPU, 16,376 MiB total, 14,742 used,
1,309 free. Another complete 27B instance cannot be assumed to fit. KV accuracy
loss is a plausible unmeasured confound, not an authenticated explanation.
The K/V types above are authenticated launch configuration. `/props` does not
enumerate every internal cache/state tensor, and the bounded 2,000-line retained
log tail contained no allocation metadata; uniform four-bit internal state is
not claimed. A precision trial must capture its actual startup allocations.

## What the failures establish

| Authenticated history | Observed boundary | Diagnosis and limits |
| --- | --- | --- |
| [B-0051 original](native-scope-followup.md), five calls | Public collection SyntaxError, later ordinary NameError; stale third proposal refused | Actual invalid/missing-helper code and edit-anchor failure; known effects restored. Private acceptance not entered |
| [B-0051 child](coding-continuation-first-live.md), six calls | Three admitted edits: 2/19, 1/20, 2/19 failed/passed | Missing helper, erased genuine conditional ambiguity, then caller-pair/helper-node mismatch. Last request had the complete current editable file. Three-proposal ceiling reached with call/read allowance remaining |
| [B-0052 coding](routine-authority-and-b0052.md), three calls | Public and independent private acceptance passed | This harness can produce a qualified candidate; no installation or general success rate follows |
| B-0052 review 1 | One call, zero reads; two-read batch rejected | Historical host one-read admission limitation, not a malformed native Tool presentation |
| B-0052 review 2 | Two calls, two reads; later batch exceeded total allowance | Budget/feedback and acquisition planning boundary; no judgment |
| [B-0052 review 3](acceptance-review-recovery.md) | Three calls/reads; final call had no Tools or JSON response constraint | Normal-stop prose with literal Tool-like tail, zero parsed native calls; JSON admission correctly failed. Current submission Tool was absent |
| [B-0053](productive-native-markdown.md), four calls | 36 public passes; frozen private `# ##` expected empty title, candidate returned `##` | Genuine semantic failure. No transport, read refusal or output-limit termination explains it. The 27 later regressions are post-hoc diagnostics, not original private acceptance |

All selected coding Context observations were `ready`, deterministic, without
pressure-driven reduction. Peak inputs: B-0051 original 19,671; child 22,143;
B-0052 6,297; B-0053 10,044 tokens. Neither truncation nor inactive compaction is
demonstrated as the cause of these failures. More calls, larger Context or a new
agent hierarchy are not established remedies. The generated code defects are
observations; attribution of their cause to sampling, prompts, quantization or
intrinsic model capability remains experimentally unresolved.

### Response safeguards already available

The adapter validates HTTP framing/status/JSON shape, native function fields,
argument JSON, usage, reasoning-channel types and termination. The coding process
refuses output-limit continuation. Typed Prompt preserves complete native
exchanges. Host admission checks exact arguments, scope, current source, edit
anchors and effect acknowledgments; schemas do not grant authority.

Current diagnostic delivery can unwrap one complete bare/JSON fence, retaining
raw versus normalized identities. It does not extract arbitrary JSON fragments
or repair prose. Current acceptance review instead exposes
`submit_review_proposal`, including during final synthesis, and validates one
proper native call, exact subject/candidate identities, finite closed fields,
references and assessed obligations. Structured delivery is not factual
correctness or host acceptance. Its live reliability remains unmeasured; the
legacy B-0052 review outcomes must not be credited to this newer transport.

### External-agent boundary

[CodexAgent](../../src/devtools/agents/integrations/codex/agent.py) is an external
Agent integration. It forwards a user turn via stdin to managed `codex exec`,
selects read-only sandbox/cwd/JSONL, and preserves provider-thread continuation.
It does not construct these llama.cpp messages, Tools or chat templates. Its
command builder does not pin a model or effort; CLI/configuration owns those.
Source inspection cannot authenticate proprietary on-wire prompts, actual model
revision or internal request counts. A future external comparison needs resolved
CLI/config/version and available transcript receipts under separately authorized
scope. No external inference was issued here; Codex must not be forced into a
raw ModelInteraction abstraction.

## Source working state and reusable memory

`active_source_status` already reports current snapshot/version/spans, partial
listing and repeated-range guidance. `source_feedback` supplies continuation and
remaining ranges; navigation exposes snapshot-bound function/class units and
parents. Internal active disclosures distinguish historical acquisition from
currently presented evidence. Projection preserves complete call/result blocks
and current required witnesses; omitted source can be reacquired through existing
source Tools. After edits, stale witnesses are cleared and current after-images
must be presented before they can ground another edit.

This is useful exact working state, not durable semantic memory. There is no
compact cross-function contract notebook or general persistent role memory.
Unread complements can be derived from the existing ranges and resource bounds;
extend that view if useful rather than creating a second ledger. Combine exact
RI/source-unit signatures and references with a small, explicitly fallible
helper/caller/guard checklist. Invalidate/re-ground notes on source-version change.
A generated summary must never become an edit witness or a passing-check fact.

`RepositoryCodingHost` supports separately bounded semantic compaction and optional
adaptive configuration, but native `AcceptanceHost` supplies no summary
collaborator. Activating auxiliary inference requires explicit budgets and
disclosure authority. It is unnecessary to explain these low-pressure episodes.

Memory remains **FUTURE** in the taxonomy. A prospective record contract should
reuse owned evidence and retrieval, with source/task/attempt identities,
authorship, observed/inferred status, visibility, applicability, validation and
supersession. It should not begin with a new database:

| Memory | Derivation and role retrieval |
| --- | --- |
| Episodic | Host-authenticated attempts, outcomes, public failures and custody; worker receives only supervisor-approved disclosure, not whole private archives |
| Semantic | Current RI/AST/source-bound facts and qualified derived summaries; researcher/coder retrieve by task and current snapshot, rechecking stale support |
| Procedural | Versioned prompt/Tool playbooks backed by exact configurations and measured outcomes, including failures; select by role/backend compatibility under host authority |

The [candidate playbooks](code-audit/llm-harness-20261104/playbook-candidates.json)
demonstrate versioned IDs, text digests, evidence, applicability and qualification
state. They are research data, not an activated registry. Promotion should bind
an approved profile digest into assignment/authority records and retain negative
results and revocation. Model-specific configuration stays in the operational
host; reusable Agents/Context remain model-neutral. Actual durable Memory schema
or authority changes need an explicit architecture/operator decision.

## Small role contract, without an orchestration platform

Reuse host-selected system instructions, native schemas, existing source Context,
ModelInteraction, coding/review processes, WorkCycle grants and Checkout. The
minimum proposed role configuration binds versioned instructions, capability
allowlist, permitted Context/memory views, actor/model/session provenance, output
contract, finite budgets and an authority reference. Configuration grants no
effects; the existing host remains the decision owner.

| Role | Scope and completion boundary |
| --- | --- |
| Planner | Read/search and bounded plan proposal; no source mutation or self-issued grants |
| Coding worker | Current task/source, approved public feedback, exact read/edit/check scope; existing candidate/outcome lifecycle |
| Independent reviewer | Fresh session/actor, exact candidate/diff/obligations and independently authenticated checks; coder conclusions remain attributed untrusted claims; private oracle implementation excluded |
| Repository researcher | Read-only source/RI queries and cited findings with observed/inferred distinctions |
| Security reviewer | Separately authorized security scope and diagnostics; not silently covered by routine coding authority or exposed to ordinary worker memory |
| Trusted supervisor | Eligibility, delegation, disclosure, budgets, source custody and host disposition through existing owners; model suggestions cannot activate policy |

Actors can share the existing serving pool serially. Actor/session and evidence
independence matter even when model weights are shared. Do not implement a
scheduler, selection algorithm or hierarchy to express these configurations.
Separate external-Agent and ModelInteraction adapters retain their own boundaries.

## Frozen calibration and execution decision

The [plan](code-audit/llm-harness-20261104/calibration-plan.json),
[exact requests](code-audit/llm-harness-20261104/requests.json) and
[render qualification](code-audit/llm-harness-20261104/render-qualification.json)
are frozen before any generation. Plan SHA256:
`33dcde98de3dc1e3cb25fb91e6c086fd3afb85fca064e86d04d9c4d956c7ae17`.
Request-set SHA256:
`d5041f55d560a1b2c0c657153b2af02d724381bf83d44c9d08ea4b2448182da2`.

| Cells | Controlled question | Count |
| --- | --- | ---: |
| P1/P2 × H0 | Native-equivalent transport/default sampling, no added role text | 2 |
| P1/P2 × H1 | Same additional role instruction in a user message | 2 |
| P1/P2 × H2 | Identical instruction moved to system role | 2 |
| P1/P2 × H3 | H2 plus explicit native-call/procedural guidance | 2 |
| P1/P2 × H4 | H3 plus official instruct sampling | 2 |
| P1 flat negative control | Schemas only in user text, no native Tools; test non-admission, not model accuracy | 1 |
| P3 text JSON / submission callable | Same revealed Markdown counterexample; transport and factual rejection scored separately | 2 |
| P4 ranges / derived coverage view | First unread Unicode gap from exact simulated read history; extend existing working-state presentation | 2 |

P2 uses the authentic B-0051 final helper/caller defect. P3's once-private case is
now explicitly public diagnostic scoring, not independent hidden acceptance.
P4 history is labeled simulated. No proposed callable is dispatched or executed.

Each positive cell separately scores native/text transport, strict schema,
source-grounded answer and zero unauthorized effects. Exact expected arguments,
reference sets and identity rules precede evaluation; malformed/unknown outcomes
remain explicit. One shot per cell is a smoke test, not a causal accuracy rate.
The adapter does not expose seed selection; stochastic output reproducibility
is not claimed. Replicates require a separately bounded scope.

**Measured now:** 15/15 typed request, installed-template and token-fit checks
passed; maximum input 3,933 tokens. **Unmeasured:** all generated responses,
accuracy and current structured-review reliability. Generation budget would be
15 calls, 60 seconds each, 960 seconds wall, 384 output tokens/call, input ≤8,192,
1 MiB capture, no retries, source writes, real Tool effects or service changes.
Likely runtime is a few minutes, bounded by 16 minutes; this is an estimate.

The existing active policy lists coding/review/Intake/host/plan/Git operations,
not generic calibration. AGENTS.md's local-worker exception requires an actual
bounded CodingTask, which these effect-free requests are not. Therefore no
generation was inferred authorized and none ran. One explicit approval of the
frozen plan **and request-set hashes** can authorize the bounded research calls;
no standing-policy extension or fabricated native assignment is necessary.

Before entry, reauthenticate the committed findings: container/image/model mount,
command, template digest, inherited generation defaults, adapter blob, health,
idle slot and capacity. Abort on drift; do not silently refresh the baseline.
The approval must identify this committed packet as well as its two input hashes.

Execution can use existing ModelInteraction and transport-test patterns. Preserve
the exact serialized request, raw response body, normalized result and usage/time.
A trusted host can wrap the existing `_read_http_response` seam, retain its exact
bounded body, and return it unchanged; ordinary observers retain normalized
responses only. Capture failure consumes entry and stops; never retry an unknown
call. This needs no production edit, proxy or new experiment framework.

### Separate configurations, requiring fresh resource/serving authorization

| Comparison | Prospective finite scope and qualification |
| --- | --- |
| Jinja/template | Current engine is already enabled. Omitted versus explicit `--jinja` is not a useful accuracy ablation. Compare installed/official pinned templates on isolated capacity: P1/P2 × two templates, four calls, output 512, call 120s; keep build/model/KV/context/sampling fixed. Treat `--no-jinja` as an effect-free negative control. Bind actual new provider and startup/restoration scope before entry |
| Thinking | P2/P3 × false/true, four calls, shared 4,096-output ceiling, medium effort, fixed sampling, call 300s/wall 1,260s. Record length/timeout censoring and reasoning channel behavior; current `reasoning_format:none` needs qualification. Do not compare a long-thinking run against a silently smaller output budget |
| KV precision | P1/P2 × q4_0/q8_0/f16, six calls on a common prequalified context, initially 16K if needed; output 384/call 60s. Same build, weights, template and request settings. Allow separately approved bounded load/restore time. A 16K result does not qualify 64K production. Use spare suitable hardware or a genuinely approved maintenance window; current 1.3 GiB free does not permit an assumed parallel 27B load |

These are prospective comparisons, not activated alternate profiles. Exact
resource identity and any service window are remaining operator decisions.

## Validation cost and bounded development

Existing receipt evidence: 119 focused tests **without coverage** took 1,468.47s;
setup totaled 157.88s and calls 1,215.82s. Slow native/review/integration scenarios
took roughly 30–43s each in authored Git repositories. The full 4,347-pass gate
took 4,503.60s. This demonstrates substantial lifecycle-fixture cost independent
of coverage; it does not isolate coverage's incremental cost or every bottleneck.
No historical validation was reproduced to obtain these numbers.

Use existing targeted/impact/recover modes and explicit owner groups during
development. Preserve failed receipts and correct before targeted reruns. Cache
content-addressed observations only against declared source/configuration,
selection/profile, Python/toolchain/environment and resource identities, with
uncertain closure explicit. Existing receipts do not establish complete ignored
configuration, installed-code or external-state closure. Broader release reuse
requires a policy decision; current final protected 100% gate remains required.

Propose a finite two-hour streaming wrapper deadline, informed by observed
75-minute runs, through the existing validation owner. Do not reduce test scope
or coverage to fit an hour. Parallelize independent read-only static checks and
proven-independent fixture groups in separate processes/receipt namespaces.
Keep canonical Checkout and the one-slot model service serial. Coverage sharding
and recombination would need separately qualified completeness/coverage semantics
and an approved release-profile change, not an audit shortcut.

The audit's [checks](code-audit/llm-harness-20261104/checks.json) record **173
deterministic adapter/projection/delivery tests passed in 187.30s**, unchanged
inputs, no new generation and no comprehensive run. These simulated transport
tests do not establish live review quality. Inspector remained clean at
`b3fa51b22b7eeabc9c74d1eff4012e597b5dc5e6`; policy, consumed attempts and service
configuration were preserved. B-0053 remains CLOSED.

## Top three hypotheses and next implementation boundary

1. **Qualified coding system/procedure profile with visible remaining budgets.**
   The role is currently absent and the public failures expose helper/caller and
   guard consistency problems. H0–H3 tests instruction content separately from role.
2. **An explicitly authorized non-thinking sampling profile.** H3/H4 tests the
   actual default mismatch without changing weights, KV, engine or source access.
   No native guard is removed or existing grant reinterpreted.
3. **Source-grounded repair notes over existing range state.** Retain current
   helper/caller/guard facts and qualified function/class summaries, with exact
   references and invalidation. P4 tests presentation value; do not build a second
   read ledger or durable memory service first.

These are likely improvement candidates, not measured gains. First run the
approved frozen calibration. Then, if supported, implement one cohesive prompt
assembly increment through the existing coding/navigation/projection owners:
separate a trusted optional system instruction from user task/public feedback,
expose existing CodingProgress counters, preserve complete source bindings and
test profile provenance/history compatibility. Do not naively prepend a message:
current inventory/status slots and source-message indices must migrate together.
Keep original public feedback out of the system-role authority text.

That bounded source change needs focused protocol/history/authority tests and one
final protected gate on the stable committed candidate. A native sampling profile
would additionally need a closed, assignment-bound request-settings contract and
explicit operator activation. Persistent Memory, generalized roles, model
selection and delegation orchestration remain separate decisions.
