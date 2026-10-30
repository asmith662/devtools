# B0035-Thinking-0001: controlled prospective mode comparison

Date: 2026-10-30. Starting accepted main:
`5d026524d3a5b0ddea352bb966e736c9d225a765`.
Both treatments were frozen in `512e75965d9c5adc982fa4e2aa47fa905dcf7a23`
before either entered inference. This is one independently started episode per
mode, not a comparison against substituted historical controls.

**Neither treatment proposed a Stage B edit. B-0035 remains open.** Thinking off
exhausted ten model calls; thinking on exhausted its first 8,192-token response
before returning a Tool call or final answer. No production code or framework
change resulted. The accepted Stage A helper remains an archived conditional
candidate, without an independently justified standalone production consumer.

## Authenticated mechanism and common starting point

The [serving audit](serving-audit.json) binds the running `b10868-304665fe7`
server to image digest
`7625abb46c6bb8357e214f949b409a152c0944228e5a653fbab112f98ad2de7e`,
the existing Qwen3.8-27B IQ4_XS artifact SHA-256
`40fac4050e940397dbf13087afd50f4734a11805bf9d65ef8ddd7483470e6199`,
and installed template SHA-256
`12827f24b742ea4e80cdc12dbcf9622227056b9f797252a3149263d4f9aaadce`.
The artifact was rehashed and service identity checked before preparation and
each treatment. No download, replacement, restart or model substitution occurred.

The existing provider maps `thinking_enabled` into boolean template kwargs and
preserves final text, separate reasoning and native calls independently. The
installed template closes an empty reasoning block for off and opens it for on.
Enabled mode also inserts its default `xhigh` reasoning instruction. The pinned
[server request handling](https://github.com/ggml-org/llama.cpp/blob/304665fe7ac957df95e3ff8c8c4ffdf92dd6ffa3/tools/server/server-common.cpp#L1295)
passes the flag and native Tools into template/parser selection. Generated-token
limits use the shared generation count, including reasoning, in
[server-context.cpp](https://github.com/ggml-org/llama.cpp/blob/304665fe7ac957df95e3ff8c8c4ffdf92dd6ffa3/tools/server/server-context.cpp#L459).
The [server contract](https://github.com/ggml-org/llama.cpp/blob/304665fe7ac957df95e3ff8c8c4ffdf92dd6ffa3/tools/server/README.md)
distinguishes chat reasoning controls from raw completion defaults. In particular,
`props.default_generation_settings.reasoning_format=none` alone does not describe
the rendered chat parser. This run actually returned separate reasoning content.

Earlier [native-cohort-03](../../apps/qwen/evaluation/native-cohort-03/README.md)
used the same template/artifact with thinking enabled and returned native calls
in two requests, then hit 4,096 tokens in a third. That is supplementary support
for compatibility, not this assessment's prospective control or proof that a
new enabled Tool call occurred here. No material provider defect was established.

Both episodes temporarily installed repaired Stage A SHA-256
`3a3aba918649eaf9240fede6efb15289fcbbb93999ac6fa9b2649020776c936c`
and repository host SHA-256
`6ef56849363adf67e3e9b46ce5e0a7cb333ccf0357412ad247c3c20228958e19`.
Their repository/snapshot identity, source bytes, task, Tools, scope, oracles and
initial source disclosures match. Fresh current observations were made in each
Checkout; no archived acquisition was promoted into a current witness. The original
delegated rejection and subsequent independent A acceptance remain unchanged.

## Prospective protocol, resources and feasibility

See [protocol](protocol.md), [off freeze](freeze-off.json), [on freeze](freeze-on.json)
and [task](task.md). Only the thinking boolean differs in normalized initial
requests. Both use temperature 0.7, top_p 0.8, top_k 20, min_p 0 and presence penalty
1.5. Alternative recommended thinking sampling was not substituted; this tests
thinking mode under common instruct sampling, not an optimized reasoning profile.
`reasoning_effort` is unset, so enabled mode inherits the template's `xhigh` default.

Both receive ten calls, six acquisition actions, four proposals, three possible
applications/two managed-check repairs, no auxiliary summaries, 8,192 output tokens
per call, a 430-second transport timeout, 450 seconds including input measurement,
and 1,140 process seconds inside a 1,200-second outer watchdog. At historical
22-23 tokens/second, a full response needs 356-373 generation seconds; the allowance
was operationally credible and returned the actual enabled response before timeout.
Equal ceilings do not imply equal consumed compute. The first-response output bound
proved insufficient for this particular default-xhigh generation; it was not raised
after observing it, and the incomplete response was not retried.

The unchanged 32,768-byte host request limit is distinct from 32K provider Context.
Input is measured through the same provider serialization/template/tokenizer and
capped at 24,064 tokens, reserving 8,192 output plus 512 safety. Reasoning/final text
share the output ceiling. No hidden capacity increase, new policy or generic budget
mechanism was added. Both episodes use the established shared coding process.

The common thirteen-region packet supplies 15,127 exact source bytes: repository
imports, scope binding, initial-state tail, `_index`, `build_request`, initial/final
`prepare` assembly, `apply`, `prepare_navigation`, `task_entry` contract, accepted
`complete_inventory`, SourceScope and public metadata assertions. Initial requests
were **29,960/29,959 host bytes** and **7,988/8,024 input tokens** (off/on).
Native rendered prompts were 28,224/28,422 bytes. The difference comes from the
boolean and template's instruction/prefix, not different supplied implementation.

Two common prospective disclosure continuations measured 31,393/32,654 bytes off
and 31,392/32,653 on, preserving the initial exact packet. They did not predict the
model's choices. Actual off-mode source calls later shortened several initial units.
The packet supplies necessary assembly/lifecycle contracts but does not guarantee
understanding or continuous retention after arbitrary additional source requests.

Repository.py retained 737 bytes of source-size headroom; the accepted navigation
candidate retained 18,125 bytes. A cohesive representation/integration arrangement
through these existing owners remained plausible under unchanged limits; no exact
implementation recipe or reference patch was disclosed. New files were unauthorized.

## Independent oracle preflight

[Preflight](preflight.json) records 18 passing Stage A behavioral/oracle-control
tests, 10 passing full-task reference controls, 34 compatibility tests, Ruff,
formatting and strict mypy. The accepted-A baseline still failed the intended Stage B
assertions: focused 1 pass/3 failures; withheld 1 pass/5 failures; additional
integration predicates 0 pass/3 failures. Failures were matched by exact test names,
with runtime/setup errors distinguished. The original assertions and hidden reference
logic were unchanged and excluded from worker read scope.

The additional predicates cover candidate-view coexistence, installed-edit refresh
with real fixed-check/native feedback, and inability to silently omit inventory for
capacity. They remain meaningful checks, but their positive paths were not exercised
on a changed candidate here. No baseline failure was relabeled as a passed test.

## Measured outcomes

| Measure | Thinking off | Thinking on (default xhigh) |
| --- | ---: | ---: |
| Model requests | 10 | 1 |
| Known input tokens | 85,454 | 8,024 |
| Known output tokens | 810 | 8,192 |
| Timed model interactions, seconds | 98.942995 | 395.157483 |
| Worker interval, seconds | 101.905162 | 399.252244 |
| Server prompt processing, seconds | 43.682323 | 8.552677 |
| Server generation, seconds | 36.334015 | 382.109671 |
| Native acquisition requests | 13 | 0 |
| Acknowledged source effects | 6 | 0 |
| Action-budget refusals | 7 | 0 |
| Additional source bytes disclosed | 18,458 | 0 |
| New / historically repeated source bytes | 6,222 / 12,236 | 0 / 0 |
| Edit proposals / admissions / changes | 0 / 0 / 0 | 0 / 0 / 0 |
| Worker checks / repairs | 0 / 0 | 0 / 0 |
| Terminal | model_limit | output_limit, response-phase failure |
| Full B-0035 acceptance | Not accepted | Not accepted |

The timer around provider send includes HTTP/normalization overhead; worker time
also includes input measurement and Tool processing. Server timing fields are
provider-reported, not independent hardware telemetry. Raw responses report 44,714
cached input tokens off and zero on; the normalized adapter leaves cache subtotals
unknown. Separate reasoning-token counts are unavailable and not inferred from
character length. Energy, monetary cost and supervisor inference usage are unknown.

### Thinking off

The first response requested repository imports (already fully active) and the
first public-test interval. The second requested the test tail and `prepare` prefix.
Calls three/four reread public-test intervals, exhausting six acquisition actions.
Later requests continued source/search selection and received seven correlated
action-budget refusals. These refusals did not enter Tools or claim source witnesses.
No edit or blocker response followed. All thirteen selected native calls are
preserved with actual arguments/IDs and feedback in [history](off/history.json).

Actual complete requests were 29,960; 32,766; 32,768; 32,768; 32,767; 30,448;
30,939; 31,754; 32,226; 32,701 bytes. Exact initial-unit counts were
13,7,9,11,12,13,13,13,13,13. Imports were fully active for the first read; none of
the other five read ranges was fully active before its acquisition. Working-set
pressure therefore materially affected available source and repeat interpretation.
All initial units were exact again after budget-refusal exchanges. No private
reasoning or causal intention is inferred from repeated selections.

### Thinking on

All thirteen initial units were exact for its sole request; no preceding source
eviction occurred. The provider returned empty final content, no native calls,
35,350 characters of separate reasoning and `finish_reason=length`. Normalization
reported `output_limit`, with 8,192 generated tokens, within the frozen timeout.
The server measured 21.436 generated tokens/second. The response was retained before
the process stopped without dispatching an incomplete action.

Independent inspection found an initial restatement of the actual obligations and
discussion of source-supported integration concerns. It ended mid-discussion of
idempotence while contemplating reading public tests. This is not a complete final
decision, source acquisition, patch, verified design or implementation success.
More reasoning text does not establish better engineering performance.

The safe result recorder retained `ValueError` and response-phase failure but withheld
its message under the existing known-capacity-only message policy. The output-limit
classification follows the actual normalized termination and inspected shared process
branch; it is not an invented original exception receipt. Complete result, raw response,
usage and normal custody restoration survived. This was not a timeout, transport
failure or provider normalization failure. No uncertain call was replayed.

## Independent acceptance and interpretation

[Comparison](comparison.json), [independent supervisory review](review.json), [off assessment](off/assessment.json), and
[on assessment](on/assessment.json) verify both archived candidates are byte-identical
to their common starting accepted-A-plus-original-host state. Neither reached a first
edit, so there is no sooner-edit winner, changed candidate to accept, failed-check
feedback to repair, or full B-0035 implementation to publish. The baseline oracle
still characterizes the missing behavior; we did not rerun it to manufacture new
positive-path evidence. No standalone Stage A helper was integrated.

The enabled mode consumed about four times the interaction time and ten times the
generated tokens in this pair without an implementation action. This is a censored,
bounded outcome: default xhigh did not finish within 8,192 tokens. It does not show
that every reasoning profile is worse, that a larger budget would succeed, or that
this model cannot implement the task. One unseeded sequential pair under common
instruct sampling cannot estimate reliability. Cache reuse differs, trajectories
diverge, off-mode source pressure constrains investigation, and on-mode output
truncation prevents observing its next intended action. No causal superiority claim.

The next justified action is **bounded profile calibration**, separately authorized:
use the installed template's supported lower reasoning effort on the same task and
oracle before another full maintenance attempt. Its purpose would be to obtain a
complete actionable response inside an operational budget, not reward verbosity.
No profile default is changed here. The evidence does not justify a new Context,
navigation or coding-loop increment. No additional treatment was run.

## Validation, custody and publication

The frozen comparison was preceded by **510 passing focused provider, Prompt, coding
and evaluation tests**. Final Ruff, supported formatting, strict mypy, layout,
native request/response/usage integrity, JSON, Intake, local links and whitespace
checks passed. [Validation](validation.json) verifies all eleven sent Prompts and
normalized responses, source scope separation and matching raw reasoning/calls.

All **1,191 protected physical inputs and executable blobs** remain identical to
`72379015cf4f34f74a9282661aac8aa0362c9977` (historically 3,906 tests, two optional skips,
100% configured line/branch coverage). No new full protected-gate result is claimed:
this is evidence-only closeout with restored production, not accepted source changes.

New Checkout owners released normally. Staged artifacts were reconciled only after
release; no source was restored from unrecognized bytes or owner removed manually.
[Reconciliation](reconciliation.json), [preservation](preservation.json),
[manifest](manifest.json) and [publication](publication.json) retain exact inventory,
hashes and ordinary Git publication. Earlier experiments, thirteen forensic files,
903 RI rows, historical refs and 188 unresolved RI obligations remain unchanged.
B-0035/B-0043 links are append-only evidence, without grants or project closure.
