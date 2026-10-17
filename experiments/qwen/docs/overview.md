# Qwen experiment

`experiments.qwen` contains bounded Qwen repository-read and patch experiments.

## First real development task (2026-10-17)

The [measured report](first_real_task.json) records **HARNESS VALIDATED / NATIVE
TOOL COMPATIBILITY PASS / REAL TASK REJECTED**. This is one genuine local attempt,
not a fixture success presented as Qwen coding competence.

`development_task.py` composes existing RI observation, caller-selected
whole-resource DisclosurePlan, materialization, rendering and ModelRequest
assembly. It is invoked through the existing patch-proposal acceptance script;
the historical fixture worker and its exact one-line patch grammar are preserved.
No automatic Retrieval/Localization optimizer or Context-sufficiency claim is made.

The independently reproduced task is a MarkdownFile defect: a fence followed by
non-whitespace text incorrectly closes a code block and exposes a hidden heading.
Before inference, the host froze the task, Git baseline, source/test hashes, eight
behavioral scenarios, Context identities/byte sizes and bounds. Only
`src/devtools/resources/filesystem/models/markdown/file.py` may be edited. Qwen
must inspect `tests/resources/filesystem/models/markdown/test_file.py` through the
native read Tool. The host-owned oracle contains no completed implementation.

Only normalized ModelToolCall requests for the disclosed read_repository_file
are admitted. The concrete ToolInvocation materializer enforces those two paths,
rejects duplicate/extra arguments and resolved escapes, then uses the existing
ToolRunner and ReadRepositoryFileTool. Tool-like text is never executed. No shell,
Git or mutation Tool is exposed. The host accepts only a bounded exact-file plain
unified diff, runs managed `git apply --check`, applies it and executes fixed
validation. An unaccepted applied edit is preserved and restored to baseline;
there is no model self-repair or retry loop.

Bounds are 10 turns, 8 accepted reads and a 900-second host deadline. The existing
profile has 32,768-token Context; requests use 4,096 output tokens and thinking
disabled. A batch exceeding the action cap is refused in full. Provider settings
are not universal resource governance. On timeout, external completion can remain
unknown. This concrete runner is invoked from its own selected feature checkout
and interpreter; cross-checkout deployment is not established.

The live attempt used **five turns, nine proposed native reads, seven executed**
(source four times, tests three). The final two-call batch exceeded the cap.
No patch was produced, source stayed unchanged and the frozen oracle still fails.
All seven existing Markdown tests pass. No second attempt, paid fallback or
Codex-authored fix was substituted.

The worker records `TOOL_PROTOCOL / Tool-action budget exhausted` at admission;
native transport itself succeeded. The primary task failure is repeated acquisition
without progress to a patch in this stateless continuation path. The single-Prompt
API reconstructs native requests/results as text; it does not provide a native
multi-message Tool-result conversation. Model reasoning cannot be separated from
that feedback representation by this one attempt.

Worker wall time was **32.264547 s**, response latency summed to 32.230150 s, and
server logs report 15.176090 s prompt evaluation plus 16.927210 s decoding. The API
reported **37,644 input / 403 output / 38,047 total tokens**. Maximum input was
11,783 tokens (35.96% of configured Context). Initial rendered Context was 8,148
UTF-8 bytes; assembled Prompt was 9,220 bytes. Cache/reasoning categories and Codex
coordination consumption remain UNKNOWN. Server newly evaluated prompt counters
differ from full API counts; do not sum them or infer formal cached input. No
counterfactual Codex savings or accepted-task efficiency gain is established.

The dedicated `feat/qwen-real-task` worktree retains ignored raw requests,
responses, frozen oracle/source and validation logs under `.local/qwen-first-task/`.
The committed report contains measured facts and artifact hashes, not complete
transcripts. The existing service was READY with the pinned profile; it was not
started, stopped or reconfigured. Candidate-08 and its recovery were untouched.

The existing entrypoint accepts `--repository-markdown-root . --report-path
.local/qwen-first-task/attempt-01/result.json`; `--freeze-only` first captures the
failing baseline without inference. A retained attempt-start.json prevents another
run in that directory. **Do not rerun this completed attempt.** Inspect the retained
repeated-read trace before separately authorizing any revised continuation/prompt
comparison. No universal Worker, Agent or workflow API is promoted.

## Historical fixture consumers

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

The historical fixture consumers do not implement streaming, native tool calls, generic usage
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
Evidence. Native provider normalization is implemented; execution remains host-owned.
The reusable Phase 3 native Tool boundary remains separate from this historical consumer:
its textual list/read proposal grammar is retained as historical control
evidence and is not automatically migrated or executed through ToolRunner.
