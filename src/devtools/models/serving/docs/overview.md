# `devtools.models.serving`

## Status

Experimental and unfrozen. This first slice supports only concrete vLLM Docker
server lifecycle management.

## Purpose

`devtools.models.serving` makes a pinned Hugging Face model repository available
through a selected local serving provider and exposes that server's endpoint,
readiness, and safe owned-container lifecycle.

It does not define model invocation, chat, Agents, Runtime behavior, tools,
benchmarks, Evidence, or evaluation.

`ServingProfileIdentity` is an immutable reproducibility snapshot that may be
attached to model-interaction Evidence by observability composition. It is
distinct from launch/lifecycle configuration: ports, container IDs, readiness,
and uptime are operational facts, not serving identity. Per-request model
settings remain owned by `models.interaction`.

## Current scope

The experimental `llama_cpp` module is the second concrete provider. Slice 2A
launches one caller-supplied local `.gguf` entry artifact with a caller-supplied
tagged or digest-pinned CUDA image. It preserves the caller-visible semantic
`.gguf` path, resolves that local path only to find the host backing file, and
bind-mounts that exact file read-only at `/models/<semantic .gguf filename>`;
`--model` uses the same container path. This supports ordinary local files and
cache snapshot entries whose backing storage differs from the public artifact
path. It exposes the server only on loopback, waits for `/health` (where 503
means still loading), and owns cleanup through an exact detached Docker ID and
label. It does not benchmark, acquire models, select quantization, or fit GPU
memory automatically.

llama.cpp supports `--hf-repo`, `--hf-file`, and a cache controlled by
`LLAMA_CACHE`; devtools instead acquires one selected GGUF with an explicit
Hugging Face repository, full 40-character commit revision, filename, and
caller-visible persistent cache root. This uses `huggingface_hub` rather than
llama.cpp's convenient provider-side resolution so benchmarkable identity does
not silently resolve `main`. Repeat acquisition reuses the Hub cache normally;
there is no quant selection, cache pruning, private-token management, or
download-progress API. Serving remains separate: callers compose the returned
local artifact path into `GGUFModel`.

This acquisition slice supports one exact GGUF file only. Some distributions
are multi-shard artifact sets; their complete pinned acquisition and provenance
remain future work rather than inferred from filename patterns.

``n_cpu_ffn`` is a llama.cpp-only serving configuration because it changes FFN
tensor placement, VRAM and host-memory pressure, performance, and benchmark
reproducibility. Its zero default preserves the image default and emits no CLI
flag; a positive value emits exactly ``--n-cpu-ffn N``. Negative values are
invalid. When a positive value is requested, the lifecycle first runs the
configured image's existing ``llama-server`` entrypoint with ``--help`` and
requires it to advertise ``--n-cpu-ffn``. This provider-local preflight occurs
before the detached model-serving container can launch, so an older pinned
image cannot fail only after a GGUF is acquired. It is intentionally not a
cross-provider capability mechanism.

The vLLM implementation uses an explicit pinned image, a caller-visible Hugging
Face cache root, an exact pinned repository revision, Docker CLI execution via
`devtools.resources.commands`, readiness probes, and ownership-safe stop behavior.
Readiness waiting is caller-configurable; its default remains ten minutes.
``cpu_offload_gb`` is reproducible vLLM launch configuration: zero disables
CPU model-weight offload, while a positive GiB-per-GPU value can reduce GPU
pressure at the cost of CPU/GPU weight access during inference.
``offload_backend="prefetch"`` is a separate, explicit vLLM configuration.
It offloads selected transformer layers by group and copies their weights into
GPU buffers before execution. Its group size, layers per group, and prefetch
step are recorded with the launch configuration; the default keeps prefetch
disabled.
``wsl2_enable_pin_memory`` is an explicit vLLM WSL2 opt-in that maps to
``VLLM_WSL2_ENABLE_PIN_MEMORY=1`` inside the launched container. It defaults to
disabled, but can be needed for CPU/prefetch offload under WSL2. Pinned
(page-locked) host memory consumes host-memory resources and should be enabled
deliberately; it does not guarantee compatibility on every WSL installation.
``estimate_cudagraph_memory`` controls whether vLLM applies its profiled
CUDA-graph memory estimate to automatic KV-cache sizing. Its default preserves
vLLM behavior. Setting it to false maps to
``VLLM_MEMORY_PROFILER_ESTIMATE_CUDAGRAPHS=0`` inside the launched container:
CUDA graphs still capture and consume GPU memory, so this advanced experimental
control can instead expose a later CUDA OOM if the estimate represented needed
headroom.
If an owned container exits before readiness, the startup failure can include a
bounded provider log tail. These failure-only diagnostics are not durable logs.
If owned cleanup also fails, the established startup failure or cancellation
remains primary and carries a bounded cleanup diagnostic note.

## Required future pressure tests

vLLM is the first provider, not the provider ontology. llama.cpp and SGLang
must independently pressure-test any future common lifecycle abstraction.
Future work includes selectable providers and pinned Hugging Face references,
cache visibility, a user-facing lifecycle CLI, and benchmark consumers. The
default deployment direction is a pinned provider image plus runtime model
selection, not per-model Dockerfiles.
