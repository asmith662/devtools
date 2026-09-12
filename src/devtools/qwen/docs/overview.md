# Qwen

`devtools.qwen` contains an experimental provider-local llama.cpp/Qwen adapter
and a bounded repository-read experiment with at most two Qwen read cycles.

`QwenAgent` implements the existing narrow `Agent` protocol for one
non-streaming `POST /v1/chat/completions` interaction. It maps the existing
Message role/content to llama.cpp chat input, maps one validated final assistant
response to `AgentTurn`, and returns no continuation. Transport and provider
response failures remain Qwen-local.

The experimental controller is intentionally not part of the package-root API.
It recognizes one exact read proposal, permits only `read_repository_file`,
uses the existing `ToolRunner` and `ReadRepositoryFileTool`, then supplies
ordered bounded result projections through controller-authored SYSTEM Messages.
It permits only `read_repository_file`, at most twice, before requiring a final
plain-text answer. It is not generic orchestration, authorization, context
compilation, or action infrastructure.

The package does not implement streaming, native tool calls, usage accounting,
provider-neutral model semantics, provider continuation, generic proposals,
or a coding worker.
