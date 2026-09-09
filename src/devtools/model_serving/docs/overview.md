# `devtools.model_serving`

## Status

Experimental and unfrozen. This first slice supports only concrete vLLM Docker
server lifecycle management.

## Purpose

`devtools.model_serving` makes a pinned Hugging Face model repository available
through a selected local serving provider and exposes that server's endpoint,
readiness, and safe owned-container lifecycle.

It does not define model invocation, chat, Agents, Runtime behavior, tools,
benchmarks, Evidence, or evaluation.

## Current scope

The experimental `llama_cpp` module is the second concrete provider. Slice 2A
launches one caller-supplied local `.gguf` entry artifact with a caller-supplied
tagged or digest-pinned CUDA image. It mounts only the model parent directory
read-only, exposes the server only on loopback, waits for `/health` (where 503
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

The vLLM implementation uses an explicit pinned image, a caller-visible Hugging
Face cache root, an exact pinned repository revision, Docker CLI execution via
`devtools.commands`, readiness probes, and ownership-safe stop behavior.
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
