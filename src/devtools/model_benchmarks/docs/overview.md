# Experimental model benchmarks

`devtools.model_benchmarks` runs and stores one streamed benchmark request
against an already-ready vLLM server. It is experimental and unfrozen.

Benchmarking consumes model serving; it does not start or stop servers, define
model invocation semantics, or integrate with Agents or Runtime. Artifacts are
JSON experiment records and can contain benchmark prompt and response text, so
they are not suitable for sensitive production traffic.

The first implementation is validated only against vLLM's OpenAI-compatible
streaming endpoint. llama.cpp and SGLang must pressure-test any future common
benchmark semantics. This package intentionally has no statistical evaluation,
database, CLI, or hardware telemetry support.

Persisted vLLM serving snapshots include CPU model-weight offload configuration,
including its zero-disabled setting, because it materially changes serving
behavior and results.
They also include explicit vLLM prefetch-offload backend and grouping settings,
including their disabled defaults, because they change weight placement and
benchmark performance.
They include the explicit WSL2 pinned-memory opt-in as well, because it can
change whether vLLM CPU/prefetch offload works and how it uses host memory.
They also include whether vLLM applies its CUDA-graph memory estimate during
automatic KV-cache sizing, because that can determine startup viability and
later graph-capture headroom.

Worker acceptance telemetry is a separate, currently in-memory experimental
value (`WorkerStoryResult`), not a vLLM benchmark result or a generic metrics
dictionary. It records a story name and bounded difficulty (1--5), wall-clock
start and duration, a boolean gate summary, closed supervisor review outcome,
local repair attempts, correction turns, optional supervisor token usage,
worker escalation, architecture-violation count, and human intervention.
Persistence is deferred until a worker-story runner exists; when earned, it
should use a separate schema-versioned JSON artifact with the same explicit
output-root and atomic-write principles as benchmark storage. It deliberately
does not duplicate TTFT, request duration, provider usage, or inference
throughput.

When vLLM reports completion-token usage, `completion_tokens_per_second` means
reported completion tokens divided by total benchmark request duration, from
request start through the terminal stream completion. It is an end-to-end output
throughput metric, not a pure decode-rate measurement.
