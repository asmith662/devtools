# Qwen3.8-27B llama.cpp worker experiment

This is an experimental research-backed profile, not a permanent `devtools`
default. It selects Qwen3.8-27B because it is the first evidence-backed local
coding-worker candidate for the RTX 4090 Laptop 16 GB / 32 GB RAM system. The
Unsloth Dynamic IQ4_XS artifact is the selected 14.3 GB compromise. A 32K
context is frozen to test the intended coding workload rather than a smaller,
easier configuration. Four FFN layers are placed on CPU to relieve VRAM
pressure; this is an experiment premise, not an automatic tuning setting.

The tracked value in `scripts/model_benchmarks/qwen38_llama_cpp_profile.py`
freezes repository, commit, filename, expected published SHA-256, quant,
context, GPU-layer setting, FFN placement, cache types, Flash Attention, and
parallelism. The llama.cpp image/build identity remains an explicit unresolved
input and must be pinned before a live run. `cache_root`, output root, host
port, and intentionally provider-selected CPU-thread resolution remain
environment-specific inputs.

The expected SHA-256 is visible provenance only. Generic acquisition currently
pins repository, revision, and filename but does not verify a digest. Digest
verification is deferred for an explicit acquisition-boundary review rather
than silently changing that committed capability.

## Controlled sequence

1. **Serve and sustain:** Can this exact model/profile remain stable at 32K?
2. **CPU FFN placement A/B:** Compare only `n_cpu_ffn = 0` with
   `n_cpu_ffn = 4`.
3. **Worker acceptance:** Run 12 frozen stories: 4 × D1, 4 × D2, and 4 × D3,
   with blind supervisor review.

Do not test `n_cpu_ffn = 1,2,3,5,6,7,8` unless the controlled 0-versus-4
experiment produces new evidence requiring it. This prevents a tuning ladder.

Speculative decoding, vision/mmproj, and a second local worker are disabled or
out of scope. Native Windows llama.cpp is deferred: the existing audited
Docker/WSL2 lifecycle avoids adding another experimental substrate. Sampling
and reasoning defaults are visible unresolved inputs pending a provider-specific
recommendation; this slice does not invent them.

Tokens per second is an inference observation, not the governing worker
metric. The later worker experiment measures accepted stories per wall-clock
hour and supervisor tokens per accepted story, while retaining inference TTFT,
duration, usage, and throughput in their existing benchmark boundary. Hardware
telemetry (peak VRAM, host RAM, paging/swap) is also visible but deferred.
