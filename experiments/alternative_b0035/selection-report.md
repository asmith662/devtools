# Alternative-B0035-0001: selected worker, blocked serving qualification

Date: 2026-10-30. Starting published main:
`6e57ad0c17b93ea0d1983797593b0e62e567536c`.

**Selection evidence; later compatibility and coding status are in REPORT.md.** The selected
gpt-oss-20b artifact was downloaded under explicit human authorization and fully
authenticated. Its owned llama.cpp container did not become ready within 240
seconds. Native compatibility and Stage B implementation were therefore not run.
This is a serving qualification blocker, not an observed coding failure.

## Authentication and local availability

Local and remote main matched the reported baseline; index/tracked source were
clean, no Checkout owner existed, and the thirteen historical forensic files were
preserved. The prior [effort assessment](../b0035_effort/REPORT.md),
[thinking comparison](../b0035_thinking/REPORT.md), and
[accepted repair](../b0035_repair/REPORT.md) were inspected without replay.
Protected executable ancestor remains
`72379015cf4f34f74a9282661aac8aa0362c9977`.

The inspected Hugging Face cache contained only Qwen3.8-27B and CodeRankEmbed.
Standard LM Studio/Ollama model locations yielded no alternative coding worker.
This is a scoped inventory, not a claim to have searched every disk directory.
Only the existing Qwen service was running. Initial GPU observation was 16,376 MiB
total, 14,006 MiB used and 2,045 MiB free. Windows reported 33,271,672 KiB physical
RAM, 5,335,780 KiB free and 143,722,131,456 free disk bytes. These are point-in-time
observations, not guaranteed memory available to a new model. Docker's later
resource report exposed a 15.48-GiB Linux memory envelope, distinct from host RAM.

## Candidate comparison and selection

| Candidate | Parameters / intended behavior | Selected quantization sizes | Practical assessment |
| --- | --- | --- | --- |
| gpt-oss-20b | About 21B total, 3.6B active; agentic reasoning and function calling | Native MXFP4: 12,109,566,624 bytes (11.28 GiB) | Primary: most comfortable weight footprint and low active compute, with existing llama.cpp support. Harmony and reasoning normalization require actual qualification. |
| Devstral Small 2 24B | Dense coding-agent specialist; all text parameters active | Q4_K_M: 14,334,446,752 bytes; IQ4_XS: 12,780,424,352 bytes | Strong coding-specific candidate, but less room for full attention KV and runtime buffers. IQ4 at smaller Context is plausible; not downloaded. |
| Qwen3-Coder-30B-A3B-Instruct | 30.5B total, 3.3B active; non-thinking coding/Tool model | Q4_K_M: 18,556,689,568; IQ4_XS: 16,378,076,320; Q3_K_M: 14,711,850,144 bytes | Q4 weights exceed GPU capacity before KV. Smaller quants or CPU offload introduce quality/latency tradeoffs. A different model from Qwen3.8, but not the best first hardware fit here. |

These are primary-card and exact-artifact observations, not measured local coding
rankings. Sources: [OpenAI model card](https://huggingface.co/openai/gpt-oss-20b),
[official local deployment guidance](https://developers.openai.com/cookbook/articles/gpt-oss/run-locally-lmstudio),
[Mistral model card](https://huggingface.co/mistralai/Devstral-Small-2-24B-Instruct-2512),
[Qwen model card](https://huggingface.co/Qwen/Qwen3-Coder-30B-A3B-Instruct).
The OpenAI deployment recipe is marked archived; its consumer-hardware guidance
supports feasibility, not this pinned server's measured fit. Mistral's desktop
RTX 4090 claim must not be transferred to this 16-GB laptop GPU.

Configuration-based conservative f16 KV estimates at 32,768 tokens are 1.5 GiB
for gpt-oss if every layer retains full Context, 5 GiB for Devstral and 3 GiB for
Qwen3-Coder. Formula: layers × KV heads × head width × K/V × tokens × two bytes.
GPT-oss alternates full/sliding attention, so a runtime exploiting sliding-window
allocation may need less. These estimates exclude allocator, graph, batch,
CUDA/display and other runtime buffers. Quantized KV can reduce memory but is not
free or assumed equivalent in quality. No advertised 128K/256K Context was treated
as usable on this laptop. Native MXFP4 avoids an additional aggressive post-training
quantization choice; IQ4/Q3 alternatives trade more weight precision for capacity.

The proposed first profile was 32K Context, one slot, all GPU layers, f16 KV,
Flash Attention and the already pinned CUDA image. Estimated weights plus
conservative KV are about 12.78 GiB before an unmeasured 1–2-GiB buffer allowance.
CPU offload was not silently substituted. Lower active parameter count suggests
potential generation efficiency but gives no defensible local tokens/second
prediction; prompt throughput and generation speed remain unmeasured.

Base cards license all three models Apache-2.0. The selected ggml-org conversion
also declares Apache-2.0. The Unsloth Devstral conversion metadata says `other`,
unlike the base card; that discrepancy would require separate artifact-license
inspection before its acquisition. No source/code reuse was proposed.

## Exact selected artifact and authority

[Selected repository revision](https://huggingface.co/ggml-org/gpt-oss-20b-GGUF/tree/15dcfc7e7c608c6161507211ed43c5b590801b4b):
`15dcfc7e7c608c6161507211ed43c5b590801b4b`.
File: `gpt-oss-20b-MXFP4.gguf`.
SHA-256: `27cd6c432c7672cb812a92f611cf3ba7bbc35928262bb1e1253ff4ee6ae35901`.
The existing Hugging Face acquisition owner downloaded exactly this 12.11-GB
artifact into its normal cache; the complete file hash matched. No other weights
were downloaded. [Acquisition receipt](acquired.json) retains exact provenance.

The user explicitly answered `+Authorize` after being asked to approve this exact
single-artifact download and a temporary Qwen service switch, with restoration.
No blanket service or provider migration authority was inferred. The existing
`LlamaCppServer` and managed Commands owner performed launch/readiness/cleanup.
An experiment-wrapper `.gguf` path validation error occurred before any service
change; it was corrected using the acquisition owner's validated snapshot path.
No production correction was required.
