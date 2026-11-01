# Native Context capacity assessment — 2026-11-01

Later [approved operational qualification](qwen64-qualification-trial.md) established
bounded 64K operation with actual long-input inference, followed by mandatory 32K
restoration. This earlier increment's timeout and qualification limits remain dated
historical observations; current persistent capacity is still 32K.

Subsequent [operational diagnosis and count reconciliation](qwen64-operational-qualification.md)
measures the original-profile restoration at about 283.7 seconds, distinguishes
4,081 tests from 4,096 passing call/subtest reports, and preserves the original
receipts unchanged. It does not infer a 64K OOM from a startup timeout.

Starting local and remote main were
`41303319c93c8dc1605207a171dc3ea551b1c2a6`. The canonical tracked/index tree
was clean; Checkout ownership was absent. Inspector remained a separately active
`feat/agent-inspector` worktree and advanced independently. Its files and branch
were not changed by this assignment.

The [production policy](../development/native-context-policy.md) integrates
existing projection and navigation through a prospective, exact approved profile.
This assessment distinguishes implementation tests from operational qualification.

## Hardware and model evidence

Read-only preflight observed an RTX 4090 Laptop GPU with 16,376 MiB total,
13,998 MiB used and 2,053 MiB free. Windows reported 33,271,672 KiB visible RAM
and 4,652,484 KiB free. These are point-in-time available resources, not a promise
of capacity during concurrent development.

The existing pinned model is Qwen3.8-27B UD-IQ4_XS, artifact SHA-256
`40fac4050e940397dbf13087afd50f4734a11805bf9d65ef8ddd7483470e6199`,
served by llama.cpp image build `b10868-304665fe7`, image SHA-256
`7625abb46c6bb8357e214f949b409a152c0944228e5a653fbab112f98ad2de7e`.
The original service used all GPU layers, flash attention on, q4_0 K/V caches,
32,768 context tokens and one sequence on loopback port 8080. Its healthy idle
slot was observed before the approved trial. No alternate model was downloaded.

The [official model configuration](https://huggingface.co/Qwen/Qwen3.8-27B/raw/main/config.json)
declares 262,144 positions and a hybrid 64-layer architecture: sixteen full
attention layers, four K/V heads of dimension 256, plus linear-attention layers.
The [model card](https://huggingface.co/Qwen/Qwen3.8-27B) describes native long-context
support. Neither establishes local capacity for this quantized artifact/build.
The [llama.cpp server configuration](https://github.com/ggml-org/llama.cpp/blob/master/tools/server/README.md)
separately controls context, parallel sequences, flash attention and K/V types.
Weight-file size alone does not determine usable Context.

For orientation only, sixteen full-attention layers with 1,024 K/V dimensions,
both caches, and [q4_0's 18-byte/32-value blocks](https://github.com/ggml-org/llama.cpp/blob/master/ggml/src/ggml-common.h) imply approximately 576 MiB of
additional full-attention K/V payload per additional 32,768 tokens. That estimate
excludes recurrent state, graph/compute buffers, padding, allocator/workspace,
Windows/WSL residency, build-specific layouts and contention. It is an inference
from architecture and cache representation, not an observed allocation or an
out-of-memory diagnosis.

| Context tokens | Estimated additional full-attention K/V versus 32K | Operational conclusion |
| --- | --- | --- |
| 65,536 | 576 MiB | Plausible first target; startup trial did not qualify it |
| 98,304 | 1,152 MiB | Less headroom; defer until reliable 64K startup/performance |
| 131,072 | 1,728 MiB | Little margin against observed free VRAM; defer |

No throughput, sustained generation, first-token latency, long-context retrieval
quality or native Tool competence was measured at these larger capacities.
Changing cache types or CPU/GPU placement would require a separately qualified
configuration and coordination, not an assumption that the table predicts fit.

## Explicitly approved bounded service exercise

The operator answered `+approve` to the concrete proposal to temporarily recreate
only the existing service, retain the same pinned image/model, q4_0 K/V, flash
attention and one sequence, change context to 65,536, run at most three neutral
probes (up to 63K measured input tokens and 128 output tokens each; ten-minute
trial envelope), and restore the exact 32K configuration. The question explicitly
required shared-service interruption coordination. This approval did not authorize
coding inference, B-0049 execution or service-default publication.

The bounded local driver composed existing service inspection/stop/launch/readiness
owners and `LlamaCppInteraction`; it added no permanent service controller or
provider registry. Its first invocation failed on an import path before service
inspection, mutation or inference. After that correction the actual exercise:

1. Captured original container configuration and an idle slot.
2. Stopped the authenticated original service and launched the same configuration
   with context 65,536.
3. Did not obtain readiness within the 180-second startup allowance. No neutral
   inference request or token probe was entered. The three probes were not retried.
4. Stopped that known trial container and recreated the original 32K configuration.
   Its initial 180-second readiness wait also timed out. The process was left
   loading rather than repeatedly restarted.
5. Subsequently authenticated the original configuration as `READY`, with identical
   command, image ID, image reference, labels, environment, mount and port binding.
   GPU use was 13,978 MiB, with 2,073 MiB free.

The original container was `61a6a7f977910ce5f7c03e6f1d33f19c51e6e7ea1cc1ae065941183cced85348`;
the trial was `bacffdb10c907b93a0f50cc4fb3a2783b65f7cdcaae1664fa5f8fd2d8a550f11`;
the restored original-profile container is
`723f6596044c52021beed7b764ffffbd419c0f2ee6719f25250366065bf2888b`.
Container identity necessarily changed; service configuration and model identity
were restored. Initial restoration diagnostics showed loading and very low GPU
allocation. No measured evidence attributes the startup delay to K/V allocation,
model Context capacity or out-of-memory failure. The short readiness deadline
also failed at the previously working 32K configuration, limiting conclusions.

The exact restoration was authenticated at `2026-11-01T04:43:28.016469+00:00`.
Observation timestamps do not identify the instant readiness first became true.
Trial and restoration receipts remain locally under `.local/context-policy/`;
the durable delivery receipt retains their digests and qualified observations.

The 64K target remains unqualified. The current server remains at 32K. Its
qualification integer cannot lawfully satisfy the example 64K profile, and the
native owner refuses that mismatch before dispatch. A source profile supporting
64K is not a claim that the local deployment supports it.

## Deterministic usefulness and remaining work

The maintained frozen B-0049 source scenario previously needed correlated
capacity refusals and smaller-range recovery at 32,768 serialized bytes. Under
the new 128 KiB request envelope it acquires all four original payloads, totaling
51,544 exact UTF-8 bytes, without duplicate acquisition. The test retains the
original task/settings; no WorkCycle slot or model is invoked. Different request
metadata changes serialized size, so byte measurements must retain their exact
envelope and never be described as provider tokens.

A separate read-only measurement used the restored server's existing
`/apply-template` and `/tokenize` adapter operations, with scripted responses and
no inference. It included the actual five Tool definitions and current source
status annotations:

| Prepared request | Complete serialized bytes | Installed-template input tokens |
| --- | --- | --- |
| Initial | 5,053 | 1,501 |
| After implementation read | 30,347 | 7,235 |
| After the three-read batch | 69,214 | 17,023 |

Four source reads delivered 51,544 exact bytes with zero duplicate acquisitions.
The final request plus a 2,048-token generation reservation fits the current
32K provider, including a separate 1,024-token safety margin. This is useful
token-fit evidence for this exact envelope on the installed template, not a
64K deployment result or a future universal byte/token ratio. A fresh approved
task could explicitly qualify a 32K-token provider with larger independent byte
budgets (`context_tokens=32768`, `input_tokens=29696`,
`reserved_output_tokens=2048`). No historical task/grant is changed by that option.

The maintained native consumer now exercises symbol metadata, exact file-unit
acquisition, current whole-owner readiness, grounded wrong edit, actual failed
public check, model-selected repair, public/private acceptance, archive/restore,
independent review and authenticated integration planning with the new profile.
The authored tokenizer is explicitly a deterministic control. It establishes no
real provider token count or model engineering competence.

Deferred obligations are categorized in [B-0043](../backlog/items/B-0043-investigate-reusable-agent-semantics.md):
operational 64K qualification; optional native semantic/adaptive grants and
model-requested compaction; durable actor-assessment semantics; and phase-specific
Tool presentation. No status/maturity/closeout authority is inferred.

## Protected delivery

Executable commit `2c0be91335512a3db2600dd0fafb2a690cd59355` passed the protected gate:
4,081 passed, two optional skips, 100% configured production line and branch
coverage (14,247 statements and 3,644 branches; none missing or partial).
Exactly one comprehensive execution occurred, taking 2247.213302 seconds
(pytest: 2,244.77 seconds). All 1,059 declared protected physical inputs and their
indexed Git blobs remained unchanged. The current source profile and old consumers
passed; no old full-coverage observation was substituted for changed executable code.

Development observations include 434 passing coding/native cases in 103.15 seconds,
164 passing source/navigation/native cases in 52.99 seconds, and the final 28-case
capacity selection in 4.47 seconds. Failed assertions were repaired with focused
selections. One earlier 434-case observation had input drift and is retained as
drifted, not a valid final pass. The [durable receipt](code-audit/native-context-policy-20261101.json)
records every executed receipt's original status, selection, elapsed time, failed
IDs and input freshness relative to the final tree. Focused development passes do
not manufacture comprehensive success. No additional full run was used for repairs.

Supported-root Ruff and formatting (762 files), strict mypy (623 files), canonical
layout, offline lock consistency, Intake, JSON, documentation links, Git ancestry
and diff checks passed. All 100 preserved evidence-file hashes matched, including
the thirteen forensic files and frozen B-0048/B-0049 records. The three RI ledgers
retain 903 rows; historical refs and 188 historical obligations are preserved.
Checkout ownership is absent; Inspector remains independently registered on its
feature branch. B-0035 closure and B-0049's consumed slot remain unchanged.

The synthetic metadata-only reduction measured 26,798 to 8,834 serialized bytes,
retaining all 26 original history messages while presenting eight active messages.
It had zero source disclosures and invoked no model or Tool effect. This is a
reducer measurement, not semantic-summary adoption or engineering competence.

The authenticated tokenizer payloads and their canonical serialization hash are
included in the receipt. An earlier preliminary measurement of the same request
shape returned 1,495/7,215/16,961 tokens without retaining its full payload archive;
fresh archived payloads returned 1,501/7,235/17,023. Generated repository/unit
identities differ. Both observations are kept distinct; the archived measurement
is the exact-input reference. Its canonical LF JSON hash and the physical CRLF
Windows archive hash are explicitly distinguished. No inference occurred.

Publication uses an ordinary documentation/evidence child of the tested executable
commit, with protected file hashes and blobs reauthenticated before non-force push.
Final local/remote identities are reported in the handoff rather than embedding a
self-referential commit hash in this receipt.
