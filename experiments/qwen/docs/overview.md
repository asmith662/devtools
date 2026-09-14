# Qwen experiment

`experiments.qwen` contains bounded Qwen repository-read experiments.

The llama.cpp transport adapter lives in
`devtools.models.interaction.providers` as `LlamaCppInteraction`. It is
configured with endpoint, served model name, and source identity; it is not
Qwen-specific.

This repository artifact is intentionally outside the installable `devtools`
framework API. `read_experiment.py` recognizes one exact read proposal,
permits only `read_repository_file`, uses the existing `ToolRunner` and
`ReadRepositoryFileTool`, then supplies ordered bounded result projections
through controller-authored SYSTEM Messages. It permits only two reads before
requiring a final plain-text answer. It is not generic orchestration,
authorization, Context compilation, or Action infrastructure.

The package does not implement streaming, native tool calls, usage accounting,
provider-neutral model semantics, provider continuation, generic proposals, or
a reusable coding-worker framework.

`two_action_read_only_experiment.py` is a separate bounded successor probe. It
permits two concrete read-only operations—non-recursive directory listing and
text-file reading—within an explicitly configured local action cap (two by
default). Its controller remains experiment-local: it uses explicit dispatch,
action-specific path materialization, bounded projections, and stateless SYSTEM
reconstruction.

Its deterministic root-navigation fixture starts at repository-relative `.`
without a target path or directory hint, descends through repeated direct
listings, and reads a discovered Python source file. This is repository fact
acquisition and controller-directed navigation, not reusable Context,
repository discovery/indexing, generic Action, authorization, orchestration,
or acceptance infrastructure.

`patch_proposal_worker.py` is a further disposable-fixture B-0009 probe. It
uses the same list/read controller with five explicit local actions to discover
one implementation file and one focused test without receiving their paths in
the task. Its final model text must be one bounded unified diff for the fixture
source file. Host-side experiment code validates and applies that diff only
inside the fixture, then checks the requested behavior. The model receives no
write or command capability. This is not reusable Context, Agent, Action,
orchestration, governance, evaluation, search, or indexing infrastructure.
