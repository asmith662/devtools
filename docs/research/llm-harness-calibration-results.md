# Frozen Qwen harness calibration: actual results

Executed 2026-11-05 UTC against `main` at
`3d10ef4b2529d3f6be54b828f2a219fc68d3fc33`, following the
[published audit](llm-harness-role-memory-audit.md). **All 15 approved requests
ran once.** Eleven of fourteen positive cells passed the frozen full contract;
the separate negative control passed. This is a diagnostic count across different
probes, not an estimate of coding accuracy.

The matched tasks showed **no correctness improvement from moving the coding
instruction to system role or changing sampling**: their baselines already passed.
Both review profiles exhausted the 384-token output reservation. A supplied source
coverage view coincided with correct native delivery where the matched range-only
response supplied the correct answer in prose. No production change follows
automatically from these observations.

## Frozen inputs, authority and environment

The original [plan](code-audit/llm-harness-20261104/calibration-plan.json),
[requests](code-audit/llm-harness-20261104/requests.json), scoring and v1 playbook
remain byte-identical. Plan SHA256 is
`33dcde98de3dc1e3cb25fb91e6c086fd3afb85fca064e86d04d9c4d956c7ae17`;
request-set SHA256 is
`d5041f55d560a1b2c0c657153b2af02d724381bf83d44c9d08ea4b2448182da2`.
Every actual serialized request also matched its frozen individual wire hash.

The operator explicitly replied `+approve` after presentation of the entire
packet, bound to scope
`ef5f7b32b82293cd5574dd06db1e61632d515fefa300d8f65799671466f27c0c`.
The [approval and preflight](code-audit/llm-harness-calibration-20261105/authorization.json)
record that decision separately from standing routine authority, which does not
authorize generic calibration. No native assignment or synthetic grant was made.
Two host invocation errors preceded all generation: an unawaited asynchronous Git
inspection and an omitted repository import path. They were corrected before any
adapter entry; neither consumed an inference nor caused a replay.

The [environment capture](code-audit/llm-harness-calibration-20261105/environment.json)
authenticates the same healthy, idle 65,536-token persistent service before/after:

| Property | Actual setting |
| --- | --- |
| Endpoint/model | `http://127.0.0.1:8080`, `qwen38-local` |
| llama.cpp fingerprint | `b10868-304665fe7` |
| Image SHA256 | `7625abb46c6bb8357e214f949b409a152c0944228e5a653fbab112f98ad2de7e` |
| GGUF SHA256 | `40fac4050e940397dbf13087afd50f4734a11805bf9d65ef8ddd7483470e6199` |
| Template SHA256 | `12827f24b742ea4e80cdc12dbcf9622227056b9f797252a3149263d4f9aaadce` |
| Serving | Existing Jinja template, one slot, flash attention, q4_0 K/V caches |
| All requests | Nonstreaming, `max_tokens:384`, `enable_thinking:false` |
| H0–H3/default | Temperature 1, top_p approximately .95, top_k 20, min_p approximately .05, presence penalty 0, repeat penalty 1 |
| H4 request overrides | Temperature .7, top_p .8, top_k 20, min_p 0, presence penalty 1.5 |
| Response constraints | No `response_format` or `tool_choice` in any frozen request |

The adapter does not expose `tool_choice`. `/apply-template` accepted `required`
during non-generating preflight, but generation-time enforcement was not tested
and was not relied on. P3-json means an instruction to return JSON; it did not
activate JSON-object grammar. No model, template, server flag, global default,
cache precision, standing policy or native limit changed.

Limits were 15 requests, 60 seconds each, 960 seconds wall, input at most 8,192
tokens, 384 output tokens each, 1 MiB capture and 65,536 raw response bytes per
call. There were zero retries, Tool effects or source mutations. Runtime capture
used 286,060 bytes. All calls finished within their deadlines.

## All actual generation results

H0 is baseline; H1 adds coding instructions as user text; H2 moves identical
instructions to system role; H3 adds explicit native-call procedure; H4 changes
only the sampling preset relative to H3, apart from visible cell IDs.

T = declared delivery channel/name/count/fresh ID; S = strict complete schema;
G = substantive answer; A = scope/effect safety. `?` means a complete judgment
cannot be established. The frozen rules require all four for a positive pass.
Content can be correct despite failed delivery. The negative control is excluded
from positive comparisons.

| Cell | Input/output tokens | Seconds | T/S/G/A | Actual result |
| --- | --- | --- | --- | --- |
| P1-H0 | 372 / 49 | 8.918 | 1/1/1/1 | Correct native `read_source`, fixture.py [6,10) |
| P1-H1 | 452 / 49 | 2.616 | 1/1/1/1 | Same correct call |
| P1-H2 | 448 / 49 | 2.564 | 1/1/1/1 | Same correct call |
| P1-H3 | 515 / 49 | 2.664 | 1/1/1/1 | Same correct call |
| P1-H4 | 515 / 49 | 2.543 | 1/1/1/1 | Same correct call |
| P2-H0 | 2,512 / 64 | 8.012 | 1/1/1/1 | Correct iterator-item-shape diagnosis and both source citations |
| P2-H1 | 2,592 / 64 | 5.811 | 1/1/1/1 | Same diagnosis; no more source needed |
| P2-H2 | 2,588 / 64 | 9.125 | 1/1/1/1 | Same correct diagnosis |
| P2-H3 | 2,655 / 64 | 9.103 | 1/1/1/1 | Same correct diagnosis |
| P2-H4 | 2,655 / 64 | 3.406 | 1/1/1/1 | Same correct diagnosis |
| P1-flat-negative | 312 / 31 | 2.171 | 1/–/–/1 | Tool-shaped JSON text; zero native calls, control passed |
| P3-json | 2,922 / 384 | 20.099 | 0/0/?/1 | Prose regex analysis; `length`, no completed JSON conclusion |
| P3-call | 3,933 / 384 | 24.862 | 1/0/?/1 | Native proposal with truncated arguments; `length`, adapter refused |
| P4-ranges | 1,103 / 143 | 8.197 | 0/0/1/1 | Correct [10,20) gap in prose; no native call |
| P4-view | 1,157 / 64 | 4.308 | 1/1/1/1 | Correct native `read_source`, fixture.py [10,20) |

Total usage was **24,731 input and 1,571 output tokens**, with 3,590 cached input
tokens reported in raw server usage. Peak input was 3,933 tokens. All fifteen
`/apply-template` + `/tokenize` input measurements exactly matched returned prompt
usage. No Context projection, compaction or source acquisition occurred. P4 used
two frozen simulated assistant/Tool exchanges with correlated IDs; the worker
issued no real reads.

Generation-loop wall time was **114.756 seconds**, including 114.400 seconds
inside adapter calls. All fifteen HTTP responses were 200; fourteen normalized
`ModelResponse` values returned. There were twelve raw native-call envelopes,
eleven of which normalized successfully, and three text responses. Eleven calls
ended `tool_calls`, one truncated native call ended `length`, one text response
ended `length`, and two text responses ended `stop`. These are nonstreaming
elapsed measurements, not time-to-first-token measurements. Prefix-cache and
fixed-order effects prevent attributing latency differences to sampling.

## What failed, and what did not

**No serialization failure was observed.** Exact wire hashes matched; native
schemas and correlated IDs worked. P2 correctly diagnosed the public B-0051
caller/helper mismatch in all five variants with full source supplied. This
demonstrates recognition under this disclosure, not successful autonomous repair
or a reinterpretation of the historical failed coding episode.

**P3-call failed output completion and admission.** The server returned a native
`submit_review_proposal` envelope with a fresh ID. Its visible argument prefix
binds the correct subject/candidate, rejects, cites both required references and
names both obligations. It then runs out of tokens inside an unfinished string.
The adapter raises `LlamaCppResponseError: Model Tool call arguments must be valid
JSON.` That fail-closed admission is correct. The prefix also contains a confusing
claim that the trailing hash is stripped although the supplied observed title is
`##`. Neither a complete nor a factually validated review exists. No real review
lifecycle, host disposition or integration planning was entered.

**P3-json failed instruction compliance and completion.** It spends the entire
reservation tracing the regex in prose, without the requested JSON object or
disposition. This is not a broken JSON grammar: none was requested at the provider
layer. Both P3 outputs are budget-censored. A minimal constructed callable fitted
214 tokenizer tokens in preflight, so the contract was possible within 384; this
model response did not remain concise enough. The result does not establish that
the native review pathway, whose request budget differs, necessarily has the same
failure or needs a blanket token-limit increase.

**P4-ranges failed delivery while reasoning correctly.** It explicitly says it
will not issue a read because “No Tool executes,” then prints the exact correct
call as prose. P4-view receives the additional existing-style coverage/gap view
and returns a native call. Both identify [10,20), so this pair does not show better
range arithmetic. It suggests a Context/presentation opportunity and exposes an
ambiguity between proposing a call and executing its effect.

No response is a recoverable single JSON fence. Truncated P3 arguments cannot be
completed without inventing content. P4 prose and the flat control cannot be
promoted into native calls without changing delivery/authority semantics.
Normalization therefore recovers **zero additional admissible successes**.

## Limits and comparisons

- H0/H1/H2 all pass P1 and P2. Dedicated system-role placement is compatible,
  but this packet demonstrates no incremental correctness benefit. H2/H3 likewise
  provide no measured gain from additional procedural instructions.
- H3/H4 have identical correctness and output lengths. The tested sampling preset
  neither improved nor worsened these answers. H4's faster P2 response had 2,139
  cached input tokens; a sampling speed claim would be unsound.
- P3-call improves the observed delivery channel relative to P3-json, but neither
  completes. Its longer system instruction and advertised callable are a bundle;
  this is not an isolated causal Tool-channel comparison.
- P4-view adds 54 input tokens and uses 79 fewer output tokens in this one pair.
  The frozen synthetic first read starts with ASCII `?`, while its resource
  metadata's version came from the intended alpha fixture. The disclosed spans
  remain ten characters and the gap answer is unchanged. These cells qualify
  coordinate selection only, not authentic source-version or Unicode fidelity.
- Cell IDs are model-visible nuisance differences. There is one uncontrolled
  sample per cell, no randomization, and no observed per-call resolved random
  seed. Easy P1/P2 tasks have a ceiling effect. These results neither rank general
  models nor prove an optimal prompt, sampler or coding success rate.

## Three evidence-supported improvement priorities

1. **Make final review delivery concise and output-budget aware.** Both P3 cells
   truncate, while the callable prefix demonstrates usable delivery. The smallest
   production increment is a bounded change in the existing reviewer synthesis
   instruction: prioritize a complete schema, concise summary and essential
   supported findings within the existing reservation; distinguish proposal from
   execution. Retain strict parsing, identities, independent factual checking and
   fail-closed truncation. Add focused deterministic boundary coverage. Qualify
   with a separately approved small live comparison before claiming improvement;
   do not silently increase native limits or reconstruct partial JSON.
2. **Project canonical source coverage/gaps into worker Context.** Reuse existing
   range ownership rather than add a ledger. P4-view completed a correct native
   request where range-only presentation produced correct prose. This is promising
   evidence for explicit source state, subject to the synthetic-pair limits above.
3. **Preserve native Tool transport and clarify effect-free proposal semantics.**
   The flat control yields literal Tool-shaped text, native P1/P2 schemas work,
   and P4 confuses “no execution” with “no invocation.” Use explicit role-scoped
   delivery guidance through existing owners; never dispatch prose or relax host
   admission. Role placement and sampler changes remain candidates, not measured
   improvements from this packet.

The versioned [candidate playbook v2](code-audit/llm-harness-calibration-20261105/candidate-playbook-v2.json)
retains model/provider/template, defaults and overrides, tested conditions, cells,
confidence and limitations. It is not activated policy, universal memory or a
replacement for v1. No additional inference is authorized by this report.

## Evidence, preservation and publication checks

The [manifest](code-audit/llm-harness-calibration-20261105/manifest.json) binds the
compact packet. [Raw calls](code-audit/llm-harness-calibration-20261105/calls.json)
preserve exact UTF-8 request/response body strings and hashes, native IDs, HTTP
status, entry receipts, normalized responses when available, observation times,
usage and server timings. [Scores](code-audit/llm-harness-calibration-20261105/scores.json)
retain each frozen-rule decision and failure; strict parsing reuses existing
coding/review validators. Original local receipts remain in
`.local/llm-harness-calibration-frozen15/`.

Publication is evidence/documentation only. Frozen input and evidence hashes,
request/response round trips, score consistency, local links, layout, Git object
integrity and diff checks are checked; see the [validation receipt](code-audit/llm-harness-calibration-20261105/validation.json).
No production executable inputs changed and no comprehensive protected suite was
rerun. Inspector remains clean at `b3fa51b22b7eeabc9c74d1eff4012e597b5dc5e6`.
Standing authority, the healthy service, B-0051's consumed failed attempts,
CLOSED B-0053 and all historical/forensic records are preserved. Existing
untracked source-grounding artifacts are excluded from publication.
