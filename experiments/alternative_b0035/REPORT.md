# Alternative-B0035-0001: feasible worker, interrupted coding assessment

Date: 2026-10-30. Starting main:
`6e57ad0c17b93ea0d1983797593b0e62e567536c`.

**gpt-oss-20b MXFP4 fits the laptop and passed real native Tool compatibility.
Its Stage B episode stopped on call two at navigation argument validation, before
any edit. B-0035 remains open.** No production/provider code changed.

Selection/compatibility was committed at `72444145`; coding freeze and oracle
preflight at `b63129438b2c6cd115e12bc5fd3fdea7f27f4f38` before coding inference.
Earlier experiments retain their original outcomes.

## Selection, authorization and actual fit

[Selection comparison](selection-report.md), [selection](selection.json) and the
pinned configuration records compare gpt-oss-20b, Devstral Small 2 24B and
Qwen3-Coder-30B-A3B-Instruct. The selection report preserves the initial preflight
phase; final outcomes are here. Primary model/artifact sources are linked there.

Only Qwen and CodeRankEmbed existed in inspected caches. gpt-oss was selected for
native MXFP4, about 21B total/3.6B active parameters and a smaller memory footprint.
Devstral is a coding specialist but needs more KV space; Qwen3-Coder ordinary Q4
weights exceed this GPU before KV. No local coding superiority was assumed.

The user explicitly authorized the single 12,109,566,624-byte download and temporary
service switch. Exact repository: `ggml-org/gpt-oss-20b-GGUF`; revision
`15dcfc7e7c608c6161507211ed43c5b590801b4b`; file `gpt-oss-20b-MXFP4.gguf`;
SHA-256 `27cd6c432c7672cb812a92f611cf3ba7bbc35928262bb1e1253ff4ee6ae35901`.
The full hash matched. Base and conversion declare Apache-2.0. No other model,
paid inference or new framework was introduced. [Acquisition receipt](acquired.json).

The existing pinned llama.cpp CUDA image/build `b10868-304665fe7` served port 8081.
Profile: 32,768 provider Context, all GPU layers requested, no CPU FFN offload,
f16 K/V, Flash Attention, one slot. Ready-state total GPU use was 12,124 MiB with
3,927 MiB free; container RAM later measured about 11.25 GiB within Docker's
15.48-GiB envelope. Host RAM is 32 GB. These are sampled observations, not peaks.
Exact per-tensor residency was not printed at this log verbosity; all-layer GPU
placement is a requested setting. Useful Context and inference were actually exercised.

First cold start timed out at 240 seconds without inference; managed cleanup
removed its container. Restoring Qwen also took longer than four minutes, then
returned healthy. One final serving-only preflight therefore allowed 600 seconds,
unchanged artifact/configuration, and became ready at about 250 server-log seconds.
The first failure and log-capture race remain recorded. No model response was
resampled. An early wrapper snapshot-path validation typo and a dirty-documentation
Checkout refusal occurred before model entry or source mutation and were corrected
before coding freeze. No provider correction resulted.

## Real compatibility and settings

The [smoke](smoke/result.json) used two actual ModelInteractions. The model first
selected `read_source` for repository.py [0,512). The shared host dispatched it
with the original native ID and exact authorized source. Its next response correctly
reported the module docstring and `import asyncio` from that feedback. No edit/check
was permitted. Raw bodies, normalized responses, rendered requests and actual
feedback are retained in smoke/. The historical filename
smoke-protocol-not-entered.txt reflects its pre-entry plan, not the later outcome.

Smoke costs: 381/58 input/output tokens in 1.109165 seconds, then 792/43 in
0.537751 seconds. Existing provider/host contracts worked; no correction was needed.
Output-limit and timeout classification were checked through existing deterministic
provider tests, not claimed as newly observed live failures.

Selected settings differ from Qwen: temperature 1, top_p 1, top_k 0, min_p 0,
presence penalty 0, typed low reasoning and thinking-enabled history retention.
Actual rendered coding input contains `Reasoning: low`; the native Harmony template
renders roles/Tools and preserves reasoning/final/call fields. These are bounded
selected settings, not a claim of optimized sampling. Model, quantization, template,
sampling, caches and trajectories differ, so architecture alone is not isolated.

## Frozen engineering opportunity

Accepted Stage A SHA-256 was exactly
`3a3aba918649eaf9240fede6efb15289fcbbb93999ac6fa9b2649020776c936c`;
repository.py remained
`6ef56849363adf67e3e9b46ce5e0a7cb333ccf0357412ad247c3c20228958e19`.
Current SourceScope/materialization, native effects and candidate restoration used
the existing Checkout/Context/Tools/coding process. Archived reads were not witnesses.

The same thirteen units supplied 15,127 exact bytes. Initial complete request:
29,959 bytes, 6,720 provider input tokens, 26,841 rendered UTF-8 bytes. Prospective
feedback continuations retained the packet at 31,392/32,653 bytes. Seven authorized
resources, two editable modules, original privacy/currentness rules, native Tools,
projection and 32,768-byte Prompt/resulting-source limits were retained. Source
headroom was 737 bytes in repository.py and 18,125 in accepted navigation.py; no
proposal tested that constraint. No reference patch/withheld oracle entered Context.

[Preflight](preflight.json) passed 18 Stage A/control tests, 10 reference controls,
34 compatibility tests and quality checks. Baseline Stage B failures matched frozen
names: focused 1 pass/3 failures, withheld 1/5, extra integration 0/3. Extra positive
paths cover candidate-view coexistence, installed-source refresh with native/check
feedback and capacity protection. They were not exercised on a changed candidate.

[Coding freeze](freeze-gptoss.json): ten calls, six acquisition actions, four
proposals, three applications/two natural validation-feedback repairs, 4,096 output
tokens, 240 seconds per model call (220 provider send), 1,140 process seconds within
1,200 outer seconds, no auxiliary summary. Provider input bound 28,160 reserves
4,096 output plus 512 safety within 32K. Smoke throughput made the envelope credible.
No limits or oracle expectations changed during coding.

## Actual behavior and diagnosis

| Measure | Observed |
| --- | ---: |
| Coding calls | 2 |
| Known input/output tokens | 13,685 / 192 |
| Model seconds / worker interval | 4.841366 / 8.345777 |
| Acknowledged metadata search effects | 1 |
| Second claimed action, unacknowledged | 1 |
| Model-selected exact reads / bytes | 0 / 0 |
| Proposals / applications / checks / repairs | 0 / 0 / 0 / 0 |
| Request bytes | 29,959; 31,138 |
| Initial exact source units active | 13; 13 |

Call one searched `_READ` within navigation.py and received valid empty metadata.
Call two searched `complete_inventory` with `path="src"`. Both calls normalized
correctly. The second acquisition raised `ToolInputError`, terminating the shared
process without a correlated refusal reaching a later request. No capacity,
output-limit, timeout or provider-normalization failure occurred. All initial
source stayed active. Tentative generated reasoning considered an inventory Tool;
that alone would not meet initial-request metadata requirements. No complete design
or patch was submitted and accepted as correct.

The exact source shows `ScopedSourceNavigationTool.validate` admits only paths
equal to authorized file-resource addresses. Directory `src` fails that predicate.
`ToolRunner` validates before execute. The frozen model descriptor says only
"path narrows scope" and its schema accepts a string without explaining file-only
semantics. The model selected an unsupported argument, and the host did not offer
recoverable feedback for that recognized pre-execution case. Owners are Tools'
scoped navigation validation and Agents' candidate acquisition/native feedback.

The recorder retains the error class but withholds its message. Diagnosis uses
actual retained arguments, unchanged source/index and the exact validation
predicate, not a fabricated original exception message or replayed Tool effect.
The original second action remains unacknowledged. No result, receipt or source
witness is invented. Terminal history contains the unfinished call; both requests
actually sent before it have valid native correlation.

Server generation rates were 78.99/88.24 tokens per second. Prompt processing was
3,005 tokens/second for 6,397 newly processed tokens, then 1,343 for 151 with cache
reuse. Raw cached input subtotals were 323/6,814; normalized cache/reasoning subtotals
remain unknown. Short samples do not predict full-patch latency, reliability or
coding quality. No energy/monetary cost was measured and no paid model was used.

## Acceptance, interpretation and next action

Independent grading found the archived candidate byte-identical to its starting
accepted-A-plus-original-host state. No changed candidate, focused worker check,
patch repair, withheld acceptance or positive integration path occurred. No
model-authored code entered production; no unused Stage A helper was integrated.
B-0035 and B-0043 remain open.

This is an argument/interface/recovery boundary, not proof that the alternative
cannot implement B-0035. The worker had no opportunity to correct its argument from
feedback. One short unseeded attempt cannot rank coding quality against Qwen.
Faster generation is not productive maintenance by itself.

Next bounded action: clarify this existing navigation argument contract and decide
on truthful correlated feedback for proven pre-execution invalid selections. Preserve
scope, budgets, original calls and unknown effects. Do not broaden directory access,
catch arbitrary post-entry failures or replay this historical invocation. No generic
retrieval/Context/agent layer is justified. A separately frozen follow-up could then
assess the already qualified alternative's actual implementation competence.

The alternative was stopped/removed through its managed owner; the original Qwen
container/configuration was restarted. Final health returned HTTP 200 on the original container; [receipt](final-health.json).
This is separate from the intermediate restoration between preflights. No further inference was launched.

194 maintained provider/serving/host tests and supported Ruff, formatting, strict
mypy and layout checks passed. Native request/raw-response integrity, JSON/JSONL,
Intake, links, whitespace and Git/source/blob preservation are recorded in
[validation](validation.json). Protected executable inputs remain identical to the
historical validated ancestor, so no new full protected gate is claimed. Artifacts
were reconciled only after Checkout release. All earlier cases, thirteen forensic
files, 903 RI rows, historical refs and 188 outstanding RI obligations remain intact.
See [preservation](preservation.json), [manifest](manifest.json) and
[publication](publication.json).
