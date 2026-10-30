# B0035-Effort-0001: usable calibration, incomplete implementation

Date: 2026-10-30. Starting published main:
`2e6a6d6681b3baa2867e6db3130adbae897f1439`.

**Low effort produced a usable calibration action, but the fresh coding episode
produced no edit. B-0035 remains open.** Medium was not run because low passed the
predeclared gate. No production, provider or framework change was made. The
accepted Stage A helper remains archived and unintegrated.

The [protocol](protocol.md), [low freeze](freeze-low.json), conditional
[medium freeze](freeze-medium.json), and rendered requests were committed in
`dc74b0b74361eb80bfb078ae6041c8573edc2ad4` before inference. The independently
reviewed low result and [fresh coding freeze](freeze-coding.json) were committed
in `c772b5e5f8f49afaaf421258c1fdbd5604b8f284` before coding entry. Earlier
[thinking comparison](../b0035_thinking/REPORT.md), repair and delegated outcomes
remain unchanged. No historical invocation was replayed.

## Effort reaches the actual template

The [serving audit](serving-audit.json) authenticates the same Qwen3.8-27B IQ4_XS
GGUF SHA-256 `40fac4050e940397dbf13087afd50f4734a11805bf9d65ef8ddd7483470e6199`,
llama.cpp `b10868-304665fe7` image and installed template SHA-256
`12827f24b742ea4e80cdc12dbcf9622227056b9f797252a3149263d4f9aaadce`.
Model bytes and service identity were rechecked before preparation and each live
episode. No service restart, model replacement or shared-default change occurred.

The existing typed `LlamaCppRequestSettings.reasoning_effort` accepts `low`,
`medium`, `xhigh` or unset and rejects unsupported values. The adapter forwards it
as `chat_template_kwargs.reasoning_effort`, alongside `enable_thinking=true`.
The installed template consumes that value: low inserts an instruction to keep
thinking brief and focused; medium adds neither the low nor xhigh instruction;
unset enabled mode defaults to xhigh's careful-assumption/alternatives instruction.
The template also recognizes a high alias, which the narrower provider extension
does not expose. All enabled modes open the thinking prefix. This is instruction
selection, **not a hard reasoning-token budget**.

Actual server `/apply-template` outputs were frozen and checked again before
calibration. Low rendered to 28,351 UTF-8 bytes/7,986 measured input tokens;
medium to 28,213 bytes/7,960 tokens. Normalized host requests were 29,960 and
29,963 bytes. Both use the same source, task and Tools; only the explicit effort
value differs. No compatibility implementation was required. Existing provider
serialization and response normalization retained reasoning, final content and
native calls separately; no provider defect was established.

## Common source, oracle and limits

The repaired Stage A source was authenticated byte-for-byte:
`3a3aba918649eaf9240fede6efb15289fcbbb93999ac6fa9b2649020776c936c`.
The unchanged host was
`6ef56849363adf67e3e9b46ce5e0a7cb333ccf0357412ad247c3c20228958e19`.
The same thirteen source disclosures supplied 15,127 exact bytes: host imports,
scope/state bindings, index/request construction, prepare assembly, apply,
navigation preparation, task-entry contract, complete inventory, SourceScope and
public metadata assertions. They were acquired under each new Checkout as
host-selected current source, never fabricated model-origin reads.

The task, authorized seven-resource scope, two editable files, native schemas,
projection, sampling and existing oracle were retained. Sampling remains
temperature 0.7, top_p 0.8, top_k 20, min_p 0 and presence penalty 1.5. No hidden
oracle or reference patch entered worker Context. The scope is deliberately
bounded; the initial packet is not every implementation dependency.

Two prospective feedback continuations retained all thirteen units exactly at
31,393/32,654 host bytes for low and 31,396/32,657 for medium. These were pure
projection checks, not Tool execution or predictions of model choices. Actual
later acquisitions differed and caused shortening. Repository.py remained 32,031
bytes, leaving 737 under its 32,768 resulting-source bound; the accepted navigation
candidate left 18,125. A cohesive integration remained plausible without changing
limits, but no edit tested that feasibility.

[Preflight](preflight.json) passed 18 Stage A behavioral/oracle-control tests,
10 full-task reference controls, 34 compatibility tests, Ruff, formatting and
strict mypy. Baseline Stage B failures matched the frozen names: focused 1 pass/
3 failures, withheld 1 pass/5 failures, extra integration 0 pass/3 failures.
The extra predicates retain candidate-view coexistence, installed-source refresh
with native/check feedback, and inventory capacity protection. They were not
weakened, and their positive paths were not exercised on a changed candidate here.

Calibration used one response with 4,096 total generated tokens, a 20-second
input-measurement bound, 220-second send bound and 240-second outer model bound.
The protocol's 300-second overall allowance is descriptive; the enforced model
watchdog is 240 seconds, separate from finite service authentication and custody.
Historical throughput implied about 191 generation seconds plus prefill, making
the envelope credible. Reasoning and final output share the ceiling. Provider
input was bounded at 28,160 tokens, reserving 4,096 output plus 512 within 32K.
The distinct host serialized-request ceiling stayed 32,768 bytes.

## Calibration result and selection

| Measure | Low calibration | Medium calibration | Fresh low coding |
| --- | ---: | ---: | ---: |
| Model calls | 1 | Not run | 5 |
| Known input tokens | 7,986 | None | 43,901 |
| Known output tokens | 1,065 | None | 7,869 |
| Timed model seconds | 59.877131 | None | 396.557372 |
| Dispatched acquisitions | 0 | 0 | 6 |
| Budget refusals | 0 | 0 | 1 |
| Edit proposals / worker checks | 0 / 0 | 0 / 0 | 0 / 0 |
| Outcome | Usable native action | Excluded by gate | Output limit, no candidate |

Low returned normalized `tool_call` termination and two correctly formed calls.
It requested public focused-test characters `[0,4591)` (4,592 UTF-8 bytes) while
only `[4591,5283)` was active, and navigation characters `[0,3625)` (3,625 bytes)
while its disclosed units started at 3625 or later. These were valid authorized
ranges containing genuinely absent fixture/extraction code and leading navigation
definitions. They were not requests to reread fully active source. The
[independent review](review-low.json) accepted this observable action, not the
quantity of reasoning or a purported verified implementation. No Tool was
dispatched during calibration. Empty final prose is compatible with a completed
native action; this was not unfinished output-limit reasoning.

The [selection](selection.json) therefore chose low and prohibited unnecessary
medium sampling. Calibration's server-reported prefill/generation times were
8.777594/46.490387 seconds, with 22.886 generated tokens/second. Separate reasoning
token usage was not reported; output totals include it. No monetary/energy cost
was measured. Medium's prompt was rendered, but no medium inference result exists.

## Fresh coding episode

The worker began independently from the same accepted source and initial request.
No calibration response or synthetic Tool feedback was inserted. Authority was
ten calls, six successful acquisitions, four proposals, three applications/two
natural validation-feedback repairs, no auxiliary summary, 1,140 process seconds
inside a 1,200-second watchdog. The same 4,096-token/240-second call envelope was
retained based on the completed calibration and observed throughput.

The first response used 3,094 tokens and selected repository `[2762,8142)` plus
navigation `[0,3625)`. The next two responses selected four additional repository/
navigation ranges. The fourth requested another repository interval and received
the established correlated `action_budget` refusal. The fifth returned 4,096
tokens, empty final content, no native call and `finish_reason=length`, normalized
as `output_limit`. It completed in 190.481616 seconds, before timeout. The shared
process retained that response and stopped before dispatching any incomplete action.

All six source effects were acknowledged; the refusal was not an acquisition.
No proposal, admission, application, fixed check, validation repair or summary
occurred. The safe recorder retained the response-phase `ValueError` while
withholding its message under the established policy. The output-limit diagnosis
uses the actual raw/normalized termination and process branch, not an invented
exception message. No timeout, uncertain retry or recording loss occurred.

Complete request sizes were **29,960; 32,768; 32,768; 32,768; 30,866 bytes**.
Corresponding unreduced sizes were 29,960; 55,861; 63,691; 69,898; 70,804.
The initial exact-unit counts were **13, 1, 7, 11, 13**. Returned reasoning and
additional native exchanges contributed to growth. Joint projection shortened
eligible source and later omitted completed exchanges while preserving native
correlation and protected instructions. Fitting did not imply sufficient continuous
working evidence or useful engineering behavior.

Actual reads disclosed 17,549 bytes: 11,532 new and 6,017 historically repeated
relative to the initial packet and prior acknowledged reads. None of the six
requested ranges was fully active beforehand. Historical repetition therefore
cannot simply be called unnecessary. The final request restored all initial units
but omitted the three completed acquisition exchanges. The generated reasoning
ended while considering lifecycle integration alternatives; it was not a completed
patch or final decision. No private intent or correctness is inferred from it.

The worker interval was 399.271901 seconds. Raw responses report 18,133 cached
input tokens for coding; normalized cache subtotals remain unknown. Server cache
reuse of the common initial prompt occurred, but no generated answer was shared.
Sampling was unseeded. Calibration success did not predict sustained implementation;
one calibration plus one episode is not a general model-performance estimate.

## Acceptance, preservation and next action

Independent byte comparison found the archived candidate identical to its starting
accepted-A-plus-original-host state. [Assessment](coding/assessment.json) therefore
rejects Stage B acceptance without manufacturing changed-candidate validation.
No model-authored source entered production; B-0035 and B-0043 remain open. Original
Stage A conditional acceptance and the earlier rejected delegation remain distinct.

The next bounded action is a controlled comparison with a different locally feasible
coding model on this same delegated Stage B task and independently checked oracle,
after separate availability/authorization preflight. Retain the active-source and
output-limit confounds. Low effort demonstrably enabled native actions at practical
latency, but did not establish a productive integration worker. Another Qwen-only
effort sweep, increased xhigh budget or generic Context/navigation layer is not
justified by this result. No such follow-on work was performed.

All **595 focused provider/Prompt/coding/evaluation tests** passed. Maintained-source
Ruff, supported formatting (457 files), strict mypy (612 files), layout, native
request/raw-response/usage integrity, JSON/JSONL, Intake, local links and whitespace
checks passed. An initial sandbox cache denial ran no tests. A broad `ruff check .`
also encountered immutable historical experiment-builder violations and failed;
its truncated output and failure receipt are preserved rather than reported green.
No historical builder was reformatted. See [validation](validation.json).

All **1,191 protected physical inputs and executable blobs** remain identical to
`72379015cf4f34f74a9282661aac8aa0362c9977` (historical 3,906 passed, two optional
skips, 100% configured production line/branch coverage). No new full protected gate
is claimed for this evidence-only delivery. New Checkout owners released normally,
production was restored byte-for-byte, and exact staged artifacts were reconciled
only after release. [Reconciliation](reconciliation.json), [manifest](manifest.json),
[preservation](preservation.json) and [publication](publication.json) bind the
retained source, raw requests/responses, custody and ordinary non-force publication.
Thirteen forensic files, all earlier experiments, 903 RI rows, historical refs and
188 outstanding historical obligations remain intact.
