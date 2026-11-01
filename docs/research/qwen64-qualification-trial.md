# Approved Qwen 64K qualification — 2026-11-01

The single prepared operational trial succeeded within its tested scope. The
pinned service reached a verified 65,536-token slot, parsed a real native Tool
proposal, and returned correct bounded neutral responses for 49,152- and
62,464-token inputs. The mandatory exact original 32K configuration was restored
and verified READY. Current persistent service capacity remains 32K.

This is a finite single-sequence qualification under exclusive reservation. It
does not establish repeated-start reliability, concurrent-workload safety,
engineering competence, long-range retrieval quality or sustained 2,048-token
generation. The actual tested output ceiling was 128 tokens.

## Authority and immutable inputs

Starting local/remote main was `eec8a01a8627fd6494fffe0fd2d1fc7999dde556`, with
clean tracked/index state and no Checkout owner. The operator answered `+approve`
to the fresh exact-plan default-No question, including provider reservation for
Inspector and other consumers. Approval was recorded at
`2026-11-01T14:11:27.625516+00:00`, expiring at `14:41:27.625516+00:00`.
The previous service grant was not reused.

The existing prepared plan SHA-256 was
`f435c68f23cbe4c01989c31a82d2a0ddcbd6e48fa9dd7108a4f42b93ae563f8c`;
the executed, unchanged prepared driver SHA-256 was
`64019ae253db90cd37245ea3eae5e53e48bd404bc1b4068d5c9328e8b6617b61`.
An exclusive intent record preceded entry. Exactly one 64K launch and one 32K
restoration occurred, with three actual inference requests and no replay.

The full local GGUF hash verified in 23.965 seconds:
`40fac4050e940397dbf13087afd50f4734a11805bf9d65ef8ddd7483470e6199`.
The same pinned Qwen3.8-27B UD-IQ4_XS artifact and llama.cpp build
`b10868-304665fe7`, image SHA-256
`7625abb46c6bb8357e214f949b409a152c0944228e5a653fbab112f98ad2de7e`,
were used. Flash attention, q4_0 K/V, all requested GPU layers, one sequence,
mount, port and image remained unchanged. Only temporary context size and its
truthful profile label changed. Artifact reading can warm filesystem caches;
this was not a controlled cold-cache comparison. Nothing was downloaded,
rebuilt or removed from the model cache.

## Startup and restoration

| Observation | 64K trial | Original-profile 32K restoration |
| --- | --- | --- |
| Container started, UTC | `14:11:55.816400275` | `14:18:28.717193895` |
| Model loaded, UTC | `14:16:34.500995677` | `14:22:32.020783075` |
| Container start to model loaded | 278.685 s | 243.304 s |
| Container start to observed READY | 278.708 s | 243.420 s |
| Controller readiness-wait duration | 276.394 s | 242.187 s |
| Actual slot context | 65,536 | 32,768 |

The controller wait begins after Docker returns the detached launch result,
which explains its shorter interval. Both starts exceeded the old 180-second
allowance and completed within the approved 600-second windows. The earlier
successful 32K restoration measured 283.724 seconds. These observations support
a longer loading allowance; changing cache/host conditions prevent attributing
the timing difference solely to context size.

During loading, HTTP returned responsive 503 `Loading model` responses while the
process remained alive. Docker's healthcheck labelled it unhealthy during this
interval; that label was not an allocation-failure diagnosis. Process read bytes
and resident memory increased, with repeated disk-sleep observations before GPU
allocation. Full timestamped logs were captured throughout loading and before
stopping the trial. No CUDA allocation error, OOM event, unexpected termination,
inference timeout or restoration timeout was observed.

The entire prepared driver finished at `14:22:36.255765+00:00`, taking
667.912 seconds (about 11 minutes 8 seconds), well within the 1,800-second bound.
The restoration reserve was never consumed by optional inference.

## Actual inference results

All requests used existing `LlamaCppInteraction`, its installed template/tokenizer,
thinking disabled, temperature 0, top-p 0.8, top-k 20, min-p 0 and presence penalty
0. These were request settings; persistent serving defaults were not changed.
No ToolRunner, source read, edit, check, coding worker or reviewer was invoked.

| Probe | Actual input tokens | Cached / freshly processed | Provider prefill | End-to-end response | Output tokens | Provider generation rate | Result |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Short native schema | 511 | 0 / 511 | 2.661 s | 4.986 s | 49 | 21.04 tokens/s | Valid `read_source` proposal; `tool_call` termination |
| Beyond old window | 49,152 | 294 / 48,858 | 55.533 s | 62.756 s | 89 | 17.20 tokens/s | Exact requested numeric response; normal stop |
| Optional near-window | 62,464 | 48,636 / 13,828 | 21.867 s | 27.124 s | 89 | 16.96 tokens/s | Exact requested numeric response; normal stop |

The short request proposed exactly `read_source` with
`{"path":"qualification_fixture.py","start":0,"end":8}` and a native call ID.
The fictional Tool operation was never executed. This establishes actual native
proposal transport/parsing for this probe, without claiming file-inspection or
engineering competence.

Both long requests returned exactly `READY` followed by integers 1 through 32.
The 49,152-token request freshly processed 48,858 tokens, providing actual
inference evidence beyond the old 32K window. The optional probe was admitted
only after completed preceding probes, adequate VRAM and enough remaining time
for its full allowance plus restoration. Its substantial prompt-cache reuse is
part of the observation; 27.124 seconds is not fresh 62K-prefill latency.

Provider-reported prompt throughput was respectively 192.06, 879.80 and 632.37
fresh tokens/s. Generation rates above are provider-reported timing fields.
The nonstreaming adapter exposes no first-token timestamp, so first-token latency
is unknown. Prefill time is not substituted for that measurement. No response
hit the 128-token cap, and no request was automatically retried.

## Actual resource observations

The GPU was an RTX 4090 Laptop with 16,376 MiB reported total VRAM. Fifteen-second
samples observed a 64K maximum of **14,732 MiB used**, with a minimum **1,319 MiB
free**, compared with the original 32K baseline's 13,978 MiB used/2,073 MiB free.
The observed difference was 754 MiB. These are whole-GPU samples, not a continuous
CUDA allocation high-water measurement. GPU compute utilization reached 100%.

The 64K process resident high-water was 14,287,132 KiB (about 13.63 GiB), and
sampled Docker memory reached 13.24 GiB against its 15.48 GiB total. Windows
sampled free physical memory fell to **327,232 KiB (about 320 MiB)** and free
virtual/commit headroom to **592,696 KiB (about 579 MiB)** during the trial.
No sampled cgroup `oom` or `oom_kill` event occurred. The restored 32K process had
a similar 14,283,540 KiB resident high-water and sampled Docker memory of 13.22
GiB, also with loading pressure. The record does not establish that context size
alone caused the host-memory minimum.

This shows adequate GPU capacity for the tested 64K requests, alongside significant
temporary host loading pressure. It warrants memory preflight and coordination,
not an unconditional safety claim for arbitrary desktop or concurrent workloads.
No 96K/128K configuration was tried or qualified. The remaining headroom does not
authorize a broader parameter search.

## Restoration, usable profile and next milestone

The trial container was stopped only after preserving its complete log and final
diagnostics. Original 32K container
`723f6596044c52021beed7b764ffffbd419c0f2ee6719f25250366065bf2888b`
was replaced by restored container
`d3bfde7803d37ccd4c498308f9dd30408184e710d9a2a1b9ee7b33e32a81e21f`.
Command, image reference/ID, labels, environment, mount and port bindings matched
the original exactly. Actual READY, HTTP health and the idle 32,768-token slot
were verified. No persistent 64K adoption was authorized or performed; the
provider reservation was released after restoration.

The result supports seeking separate authority for this exact persistent 64K
profile, with the measured host-pressure and single-sequence limits. A future
native task can select 65,536 context tokens only after the running provider is
actually qualified and deployed at that capacity. The demonstrated input ceiling
is 62,464, with the plan's 2,048-token generation reservation and 1,024-token safety
margin. Actual generation was capped at 128 and reached 89 tokens; sustained
2,048-token output and engineering-quality results remain untested. Observed
prefill/generation times must inform finite task call/output budgets.

Independent request bytes may still be configured up to 128 KiB through the
existing native profile, with actual token measurement, deterministic projection,
precise navigation and unchanged edit limits. The existing 1 MiB capture ceiling
still requires room for every request, response and other observation. Current
restored 32K operation retains the already qualified larger-byte alternative.

The next productive milestone is one fresh, separately authorized bounded native
coder–reviewer episode using the existing workflow. Persistent 64K adoption is a
separate operator decision. B-0049's original consumed slot is not reopened, and
this operational trial grants no WorkCycle, installation or backlog-closeout power.

## Evidence and proportionate verification

The [authenticated execution receipt](code-audit/qwen64-qualification-trial-20261101.json)
contains genuine approval/intent, exact requests and returned raw/parsed responses,
timings, resource observations, all startup/probe/restoration logs, identities and
the one-launch/no-replay checks. Earlier unentered and timed-out records retain
their original identities and outcomes.

No production executable inputs, native Context implementation or validation
policy changed. All 1,059 protected inputs remain identical to the existing
successful protected candidate. No new pytest or comprehensive run was justified
by changed inputs. Operational checks instead authenticated exact approved bounds,
actual token use, output/termination correctness, timing consistency, absence of
Tool effects, restoration identity, JSON/JSONL, repository layout, Intake,
documentation links, Git ancestry and historical preservation. Inspector remains
independently registered on its original feature branch and was not modified.
