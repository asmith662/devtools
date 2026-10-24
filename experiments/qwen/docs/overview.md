# Qwen experiment

`experiments.qwen` contains bounded Qwen repository-read and coding consumers.

## Governed backlog consumer

The repository-local [work bridge](../../../docs/backlog/metadata.md#governed-backlog-to-qwen-cycle)
now calls this same `run_coding_task` after approved backlog provenance, exact
source/branch preparation and separate host implementation consent. It does not
add a worker loop, task DSL or provider. The local-profile factory in
`scripts/qwen/coding_worker.py` is shared by both entrypoints. Scripted integration
covers actual retrieval/materialization, failed edit, test-feedback repair,
independent acceptance, pending side discovery and conservative interruption.
The [scripted measurement record](governed_work_cycle.json) retains two fixture
turns, one repair, passing tests/oracle and 15.30 seconds end-to-end. Its token
counts are synthetic, never Qwen usage. This is host integration evidence, not
another live Qwen task acceptance. The
Python 3.12 proposal is approved as B-0048. Its first genuinely delegated local
Qwen run is now independently accepted as a review candidate; the rejected
Task 02 remains failed.

### First delegated B-0048 review candidate

On 2026-10-18 the existing standing grant
`a5b20e0b6ade4af3603b40521d9a3d3a3c69b3fc3fab221d14c6e1324b1946f0`
admitted the exact prepared assignment
`179531289e28506c6a87508990a7d7aa0d14c76263d098c2a50ae099e659e298`.
Codex recorded actual pre-dispatch review, reserved the existing allowance and
dispatched once, without another human confirmation. The worker used the pinned
Qwen3.8-27B IQ4_XS/32K profile, thinking disabled, native `propose_edit` only.

The objective was the reproduced Python 3.12.13 JsonObjectFile constructor
failure, scoped to `src/devtools/resources/filesystem/models/json/object.py`.
Baseline source/test bytes and the host-owned cross-version oracle were unchanged.
The first proposal introduced an invalid custom constructor (four regressions);
the second restored Python 3.14 behavior but retained the Python 3.12 failure.
The third passed both the frozen oracle and all 11 JSON regressions. All three
proposals were admitted; two test-feedback repairs occurred within the original
three-call allowance, without any replacement attempt.

| Turn | UTC model request | Input / output tokens | Outcome |
| --- | --- | --- | --- |
| 1 | 21:57:34.064620 | 4,079 / 270 | Oracle and tests failed |
| 2 | 21:57:52.619435 | 6,308 / 138 | Python 3.14 tests passed; 3.12 oracle failed |
| 3 | 21:58:05.987119 | 5,003 / 122 | Oracle and all 11 tests passed |

Actual provider totals: **15,390 input / 530 output tokens**. Cached-input,
cache-write and reasoning observations are unknown; no overlapping categories
are added. Model response time totals 40.77 seconds. Worker time was 101.10
seconds; bridge execution 102.23 seconds. Host validation took 59.67 seconds,
including 55.92 seconds in baseline pytest startup. These timings do not imply
model-time or subscription savings. Codex coordination consumption is UNKNOWN.

The consolidated candidate replaces the problematic zero-argument inherited
post-initialization call with an explicit base call, checks the mapping root
and retains recursive freezing. Constructor signature, frozen slots, mapping
and transformation APIs remain intact. Final source SHA-256:
`9b31553ec9982cba4886eaed39e6ddb0941598b57d3d0442771083f2fd4fd88f`.
Independent supervisory replay reconstructed all three captured native proposals
through the same host admission/application, reproduced that exact source,
and reran the unchanged oracle successfully on Python 3.12.13 and 3.14.3 plus
all 11 JSON tests. Ruff and direct-file formatting checks passed.

Work result `0067bd485eef310d112b1e1f9b0bc85925075f48eb1fe01b1157e69a57e095fe`
is `REVIEW_CANDIDATE`; Codex review
`23a5dcbedbb4f6980068a8fc29ae94d1e436cc3a7078f585bb762fcb2cdc95ae`
records `ACCEPT_RECOMMENDED`, with integration authority false. Existing local
evidence is under coordinator `.local/backlog/work/B-0048/`: assignment,
authorization, dispatch, worker turns/result/final source, candidate diff,
supervisory-validation and the two supervisory records. Captures remain local;
this documentation does not publish the candidate source or raw model messages.

The target branch remains clean at `75cc74f7acda36cf91e91251efae8f9b3054f02a`.
Neither maintained source nor the frozen acceptance criteria were modified.
Worst-case reservation is retained: one task, three calls, 12,288 requested
output tokens and 900 seconds. Remaining grant allowance is two tasks, six
calls, 24,576 requested output tokens and 1,800 seconds; unused reservation is
not refunded. No further B-0048 dispatch is permitted by this completed slot.
JsonListFile/CsvFile compatibility defects remain outside scope, so B-0048 is
not closed and full Python 3.12 compatibility is not established. Separately
authorized integration and permanent regression publication are the next step.

The maintained [WorkCycle integration contract](../../../docs/backlog/integration.md)
now supports that transition through independent test additions, exact-tree
review/gates, feature publication, authorized destination promotion and verified
work closeout. Its standing integration grant is separate from the Qwen coding
delegation. Implementing this lifecycle does not install this candidate or grant
main publication; B-0048 remains open until its separate obligations are resolved.

## Task selection and second-task closeout

The same `coding_loop.run_coding_task(..., task=...)` now accepts the
experiment-local immutable `CodingTask` configuration in `tasks.py`. The CLI
selects `--task markdown-fences` (legacy default) or `--task python-source-segments`.
There is no task-name branching in the edit/validation/repair loop, no plugin
registry and no model-originated configuration. A host definition supplies its
objective, one source, focused tests, exact Git baseline and byte hashes,
retrieval queries/views/expansions, host-only oracle and bounded execution values.
Its complete definition SHA-256 is frozen in v2 run receipts; old v1 receipts
and all historical outcomes remain unchanged.

The source/test baseline is authenticated against the exact configured Git
revision before any inference. Only isolated copies are restored, with LF/CRLF
restoration admitted solely by the frozen byte hashes. This makes the original
Markdown task reproducible after its accepted fix landed, without reverting the
maintained file. Existing tests now consume this shared preparation path instead
of duplicating Git baseline reconstruction. Supported library imports come from
the current host source, whose HEAD is recorded; task source/tests are the pinned
inputs. No scientific target-checkout contract is claimed.

The second task fixes a demonstrated defect in
`src/devtools/context/python/function/materialization.py`: valid Python AST
ranges containing non-newline separators in strings/comments previously raised
out-of-range errors or materialize incorrect segments. Context admits only that
source and `tests/context/python/function/test_materialization.py`. Symbol query
`extract source segment UTF8 byte offset` expands the selected source to its file;
the tests use file query `materializes source utf8 range`. Existing canonical
search and disclosure APIs retain exact identities/spans/bytes. No solution or
test-only reference implementation is disclosed in model Context.

The [frozen preparation record](second_task_preparation.json) binds baseline
`11225000d7c1e728fa1313f92a0c54214b75a426`, source/test SHA-256, queries, limits,
complete objective and independent oracle. The baseline passes all ten existing
tests and fails independent acceptance. The host oracle compares 48 valid AST
segments against Python's standard-library source extraction, covering eight
non-newline separators, LF/CRLF/CR and sync/async functions. Existing focused
tests additionally retain malformed-range and UTF-8 boundary refusals.

Scripted responses prove both task configurations, cross-task refusal, repair,
exhaustion, provider/tool failure and cleanup. A CPython reference-only stand-in
passes tests/oracle in isolation after an intentionally bad edit; it is neither a
Qwen result nor a proposed maintained solution. That preparation record remains
historical. The subsequent [Task 02 result](second_task_result.json) is
**REPAIR_BUDGET_EXHAUSTED**: three admitted proposals, two repairs, 19,587 input
and 1,848 output tokens in 105.74 seconds. No proposal passed the frozen oracle.
The production repair is a separate Codex-authored engineering escalation;
it is not Qwen-generated acceptance. The frozen task/oracle and original receipts
remain unchanged.

The corrected materializer uses physical LF/CRLF/CR lines without translating
source, and rejects invalid UTF-8 endpoints. All 48 original oracle cases pass.
Future worker feedback captures primary pytest exception facts before traceback
formatting, retaining full command logs in stage/result evidence. Bounded
head/tail excerpts explicitly mark truncation; primary failures identify the test,
phase, exception and message. Secondary pytest reporting errors remain separate
from these primary facts. Outcome summaries remain in stdout; an interrupted
pytest report does not establish complete test outcomes.

The historical operator command was:

```powershell
uv run --python C:/Python314/python.exe python scripts/qwen/coding_worker.py --task python-source-segments --report-directory .local/qwen-coding-worker/task-02-run-01
```

Paths resolve before prompting. Genuine terminal confirmation defaults to No;
the selected objective is shown. Existing Qwen3.8-27B IQ4_XS/32K profile, thinking
off, at most three calls, 4,096 output tokens per call, 300 seconds per call and
900 seconds total remain enforced. The model sees one native proposal operation
whose path enum and admission both name only the selected source. Validation
commands are generated by the host from test paths/oracle, not supplied by a
model or arbitrary command string. There is no paid fallback or unrestricted
write/shell/Git capability. A fresh report directory retains full evidence and
accepted source; disposable edits are removed on normal completion/failure.
Process death may require manual workspace reconciliation; automatic resume
and durable working memory are still unimplemented.

Next: review failure-guided worker improvements before selecting another genuinely
unresolved task; no additional live attempt is authorized by this closeout. Multi-task autonomy, native structured
continuation, durable task-local memory, long-term memory and 32K/64K benchmarking
remain future work. Python 3.14 is the verified environment; the separate known
Python 3.12 compatibility issue is unchanged.

## Retrieved-Context Markdown coding worker

`coding_loop.py` is a concrete task-specific worker consuming production
multi-resolution search, `SourceSearchDisclosureOption` and existing Context
materialization. It reuses `development_task.py` native proposal admission,
LF/CRLF compatibility and managed Git application. Only maintained worker,
CLI and tests were selectively integrated from Qwen commit
`e84def2d08dfc59739fab8f778478d9a63604c7c`; no scientific ancestry was merged.

The host admits only the frozen Markdown implementation and focused tests.
Symbol search for `MarkdownFile fence headings` selects source; explicit file
expansion supplies surrounding patterns/imports. Focused tests are independently
retrieved by file. `acquire_context(..., mode=...)` accepts file, symbol, window
or mixed. Receipts preserve selected/expanded unit identities, exact spans,
snapshot, content identity, ranks and bytes. Caller-selected scope is not an
automatic sufficiency policy or evidence of superior ranking.

The existing entrypoint, when operating on the frozen task baseline, is:

```powershell
uv run --python C:/Python314/python.exe python scripts/qwen/coding_worker.py --report-directory .local/qwen-coding-worker/run-01
```

Relative report paths resolve against the caller's current
working directory; absolute paths remain supported. Invalid/occupied locations
are rejected before confirmation. Do not repeat completed run-01 or reuse its
directory. Task-configured preparation now restores the original source/tests
from checkpoint `d9a118315450b1e3df8bc00b6bbc29798845877b` only in isolation,
so the original task remains reproducible without altering its maintained fix.

Closeout validation on Python 3.14: 208 focused tests passed in 21.95 seconds;
the protected gate passed once (1,654 passed, two skipped, 100% production branch
coverage; 44.90 seconds host). Ruff, five-file formatting and strict mypy over
250 files passed. The original oracle was separately rerun against maintained
source. This validation made no model or scientific calls.

The genuine terminal prompt defaults to No; no noninteractive bypass exists in
this entrypoint. Confirmation precedes service inspection. An unavailable or
mismatched existing Qwen3.8-27B IQ4_XS profile prevents inference; no serving
lifecycle change occurs. Bounds: three requests, two test-feedback repairs,
4,096 output tokens each, thinking disabled, existing 32K profile, 300 seconds
per call and 15 minutes total. Cancellation cannot prove provider work stopped.
The model sees only native `propose_edit`, never shell, Git or direct writes.

The host authenticates frozen source/test/oracle hashes, proves baseline tests
pass and the unchanged eight-scenario oracle fails, then records the task,
settings/schema and each request before dispatch. It admits one bounded,
unambiguous region on the one authorized path and applies the host-generated
patch in a disposable workspace. Application must reproduce admitted bytes.
Predetermined validation explicitly imports that isolated source, runs seven
Markdown tests and the unchanged independent oracle, and excludes inherited
pytest configuration/conftests. Valid edits failing tests may receive a repair;
malformed proposals, unauthorized operations, provider failures, unknown
completion and exhausted bounds stop. No model-controlled command exists.

The llama.cpp adapter remains stateless. Each turn reconstructs objective,
current source Context and latest correlated proposal, assistant content and
test feedback, instead of accumulating redundant source copies. Full responses
are preserved separately; this is not native conversation support or Memory.

Each new report directory contains `freeze.json`, per-turn request/response/stage
JSON, host `proposal.patch`, `final-source.py` and `result.json`. Directory reuse
is refused. Both accepted and rejected edits are removed with the workspace;
accepted source remains an inspectable artifact with no automatic application
or publication. After process death, inspect preserved records/workspace manually;
the worker does not resume or overwrite an existing run. Receipts are local
records, not a general recovery framework.

Reports retain call/proposal counts, repair cycles, phase timings, validation
time, provider usage and Context bytes. Unknown categories remain unknown;
cached input/reasoning remain independent subcategories, never added twice.
Per-resource token attribution is unknown; aggregate utilization uses reported
input / 32,768. Codex coordination usage is UNKNOWN.

The first operator-run coding loop is **ACCEPTED**. Its
[provenance record](first_accepted_coding_task.json) retains both native proposals,
the source hash chain, captured artifact hashes and model profile. Qwen made
two calls and one test-feedback repair: 8,178 input tokens, 525 output tokens,
34.7609 seconds total. Seven existing tests and the unchanged independent
eight-scenario oracle passed. Cache/reasoning categories remain unknown.

Closeout replayed those captured proposals through existing admission, verified
each intermediate hash and byte equality with saved `final-source.py`, and
freshly reran tests/oracle before installing those exact bytes in maintained
source. No Codex-authored Markdown implementation was substituted. All eight
scenarios are now permanent regressions. The original run and earlier failures
remain immutable; historical attempt-04 is still rejected, with six scenarios
passing only in its separately identified newline replay.

This establishes one accepted controlled task, now integrated, not general Qwen
coding reliability or automatic Context sufficiency. The next milestone is a
different real development task through the existing bounded worker approach.
Python 3.14 is verified; the known Python 3.12 slotted-dataclass `super()` issue
remains separate. This closeout made zero new model calls.

Earlier integration validation: 320 focused checks passed in 22.24 s. The protected
development gate passed once (1,640 passed, two skipped, 100% production branch
coverage; 58.75 s host). Ruff, formatting and strict mypy passed. A preserved
SCRIPTED_HOST_TEST_ONLY demonstration selected `MarkdownFile._parse_headings`,
expanded the source to 5,764 bytes, and disclosed 5,346 bytes of focused tests.
Its failed first edit and passing second repair took 2.69 s total / 2.28 s
validation. Those are host timings with scripted responses, not inference
performance or Qwen-generated acceptance evidence. Calls/tokens at that checkpoint: zero;
Codex coordination tokens and per-resource model token burden: UNKNOWN.

## Earlier bounded consumers

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
