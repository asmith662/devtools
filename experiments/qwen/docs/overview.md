# Qwen experiment

`experiments.qwen` contains bounded Qwen repository-read experiments.

The llama.cpp transport adapter lives in
`devtools.models.interaction.providers` as `LlamaCppInteraction`. It is
configured with endpoint, served model name, and source identity; it is not
Qwen-specific.

`scripts/qwen/python_function_context_acceptance.py` is a bounded B-0002 live
checkpoint. It builds a disposable nonce-bearing Python module, exercises the
implemented Repository Intelligence, exact-name retrieval, Context disclosure,
source materialization, rendering, and ModelRequest assembly path, then sends
the resulting request directly through `LlamaCppInteraction`. The model receives
no Tools or repository access. Exact whitespace-trimmed nonce equality records
only whether that configured model consumed the supplied Context for this one
task; it is not shadow mode, assisted mode, or a general evaluation result.

This repository artifact is intentionally outside the installable `devtools`
framework API. `read_experiment.py` recognizes one exact read proposal,
permits only `read_repository_file`, uses the existing `ToolRunner` and
`ReadRepositoryFileTool`, then supplies ordered bounded result projections
through controller-authored SYSTEM Messages. It permits only two reads before
requiring a final plain-text answer. It is not generic orchestration,
authorization, Context compilation, or Action infrastructure.

The package does not implement streaming, native tool calls, generic usage
accounting, provider continuation, generic proposals, or a reusable
coding-worker framework. `ModelResponse` may carry optional provider-reported
usage and termination; the B-0009 acceptance report retains those per-turn
facts and exact cumulative usage totals only when every turn reported a count.
Termination records only the provider-reported semantic end (normal stop,
output limit, or tool call). The report also retains separately returned model
reasoning per turn for this focused provider diagnostic, without putting it in
Conversation, later prompts, console output, or generic telemetry. It does not
estimate tokens, attribute Prompt components, budget Context, or define a
metrics framework. That expanded artifact is schema
`qwen-b0009-live-acceptance/4`; `/1` and `/2` predate selection-stress
measurements, while `/3` remains historical selection-stress evidence without
the later termination, reasoning, and thinking-choice fields.

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

Before admitting a final patch, this fixture-local worker requires accepted
reads of its relevant implementation and focused test. One premature final
response receives a controller-authored inspection correction without target
path disclosure; a second ungrounded final response fails the bounded probe.
This is an epistemic readiness condition for this fixture, not reusable Context
selection or authorization.

The patch contract retains raw model text for evidence. Once the strict fixture
grammar is satisfied, a final diff ending directly at EOF is equivalent to one
with exactly one terminal newline; the host canonicalizes only the accepted
fixture patch before application. Extra output, whitespace, or patch syntax is
not normalized. A model may hypothesize a confined repository-relative filename,
but final-patch grounding still requires successful reads of both required
fixture artifacts.

The same module also owns one deterministic repository-selection stress
fixture. It retains the one-line label-matching change while placing adjacent
display-label, label-slug, test, and documentation candidates beside the
required implementation and focused test. Its seven-action cap makes one
exploratory detour observable. The schema `/4` report retains fixture-local
required-read coverage and acquisition precision, plus optional per-turn input
context utilization against the fixed Qwen experimental profile's 32,768-token
capacity. These are experiment measurements, not Context selection, budgeting,
ranking, search, or a reusable metrics framework. No live stress-fixture
acceptance has succeeded yet.

The existing patch-proposal acceptance runner defaults to the baseline fixture.
Use `--fixture selection-stress` with its caller-selected `--report-path` to
run the committed seven-action stress fixture; `--fixture baseline` explicitly
selects the unchanged five-action baseline. The schema `/4` artifact records
the selected fixture identity. An optional `--maximum-output-tokens` value is
an experiment-local cap forwarded to every ModelInteraction turn; it has no
framework default and is distinct from the Tool-action cap or Context budget.
This is fixture-selection and measurement plumbing only.

The acceptance runner may explicitly pass `--thinking default`, `--thinking
enabled`, or `--thinking disabled`. The selected value is forwarded to every
model turn through immutable `ModelSettings` and recorded in the schema `/4`
report; no thinking mode is selected by default. The optional
`--maximum-output-tokens` value follows the same experiment-local path. This
uses ADR-0001 Phase 1 request values. Phase 2 now supplies optional reusable
interaction Evidence and serving provenance through external composition; the
acceptance report remains experiment-specific and is not rewritten as reusable
Evidence. Native Tool calls and model-side Tool execution remain unimplemented.
The reusable Phase 3 native Tool boundary remains separate from this experiment:
its textual list/read proposal grammar is retained as historical control
evidence and is not automatically migrated or executed through ToolRunner.
