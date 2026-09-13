# Qwen experiment

`experiments.qwen` contains a bounded Qwen repository-read experiment with at
most two Qwen read cycles.

The llama.cpp transport adapter lives in
`devtools.models.interaction.providers` as `LlamaCppInteraction`. It is configured
with endpoint, served model name, and source identity; it is not Qwen-specific.

This repository artifact is intentionally outside the installable `devtools`
framework API.
It recognizes one exact read proposal, permits only `read_repository_file`,
uses the existing `ToolRunner` and `ReadRepositoryFileTool`, then supplies
ordered bounded result projections through controller-authored SYSTEM Messages.
It permits only `read_repository_file`, at most twice, before requiring a final
plain-text answer. It is not generic orchestration, authorization, context
compilation, or action infrastructure.

The package does not implement streaming, native tool calls, usage accounting,
provider-neutral model semantics, provider continuation, generic proposals,
or a coding worker.

`two_action_read_only_experiment.py` is a separate bounded successor probe. It
permits exactly two concrete read-only operations—non-recursive directory
listing and text-file reading—within a maximum of two accepted actions. Its
controller remains experiment-local: it uses explicit dispatch, action-specific
path materialization, bounded projections, and stateless SYSTEM reconstruction.
It is evidence about heterogeneous action selection, not generic action,
authorization, orchestration, context, or acceptance infrastructure.
