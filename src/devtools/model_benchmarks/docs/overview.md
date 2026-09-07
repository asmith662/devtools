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

When vLLM reports completion-token usage, `completion_tokens_per_second` means
reported completion tokens divided by total benchmark request duration, from
request start through the terminal stream completion. It is an end-to-end output
throughput metric, not a pure decode-rate measurement.
