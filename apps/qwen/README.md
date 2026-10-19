# Bounded local coding worker

Maintained repository-local application composition now lives here. The existing
worker, native proposal admission, LF/CRLF handling, task configuration and
host-owned validation were relocated without changing their contracts. Framework
Context/RI, ModelInteraction, Tools, managed commands and filesystem primitives
remain in `src/devtools`. Legacy fixture helpers remain because the existing
patch-proposal CLI and deterministic acceptance still consume them; they are not
a generic Agent API.

`scripts/qwen/coding_worker.py` remains the genuine default-No terminal entrypoint.
No local inference is authorized by consolidation. Historical Markdown and source
segment task definitions pin their original Git baselines; they are reproducible
evaluation definitions, not unresolved current defects. Complete evidence and
outcomes remain in `experiments/qwen/` and `.local/qwen-coding-worker/`.

The first task was accepted and its exact Markdown correction integrated; the
second task failed and received a separately attributed Codex production repair.
B-0048 is a separate accepted candidate, not integrated source. WorkCycle/delegation/integration now uses the canonical checkout and ordinary
branches under exclusive recoverable ownership. The worker applies only the
admitted source file in place, captures the candidate, and restores original
bytes; it never copies the repository or src tree. Validation binds imports to
the exact selected source. Historical task definitions require selecting their
actual baseline branch rather than substituting old bytes under a current HEAD. Old grants
are historical and cannot be reused at this new coordinator path.

## Native Context investigation

`CodingTask.context_mode="on-demand"` selects investigation in the **same**
`run_coding_task` loop. Default `"prepared"` retains caller-selected disclosures.
Mode/read scope enter the exact task digest; original prepared definitions retain
their historical digests. The initial request contains the objective, boundaries
and admitted paths, rather than complete implementation/test files.

| Native operation | Arguments | Existing owner reused |
| --- | --- | --- |
| `search_source` | `query, mode` | file/symbol/window/mixed source index and ranking |
| `lookup_symbol` | `name` | exact qualified Python source-unit names; all matches retained |
| `read_source` | `path, version, start, end` | observed source + authenticated Context materialization; half-open character offsets |
| `expand_source` | `unit, to` | existing parent-symbol identity and class/file expansion |
| `source_relationships` | `path, version` | bounded static Python declaration references/direct calls |

Descriptors use the existing model/Tool composition; `ToolRunner` validates and
executes reads. No Tool provides shell, Git, writes, approval or publication.
`propose_edit` still admits one bounded contiguous replacement in the single
authorized file, with the established LF/CRLF safeguards. Predetermined tests
and the independent oracle decide acceptance. Failed valid edits remain current
for up to two corrections; no Codex replacement is supplied.

Read scope is source, tests and optional `read_paths` (exact Python paths), frozen
in `baseline_hashes` and `context`. At most 32 resources are admitted: this is not
unrestricted repository access or automatic obligation sufficiency. Explicit-
address discovery never enumerates `.local` or unrelated directories. Observation
is bounded at 131,072 bytes/resource. Drift, stale versions/units, aliases,
unauthorized paths and malformed calls refuse. Only an exact host-admitted edit
can refresh the snapshot. Results retain repository/snapshot/revision, source
versions/spans where applicable, explicit truncation and static-analysis limits.
For range reads, `span` describes the exact returned text; `parent` retains the
original whole-file unit identity/span/line metadata without rebinding that
identity to a smaller excerpt.
`revision` names the pinned assignment base; `snapshot`/`version` identify current
observed source, including a temporary host-admitted edit before any Git commit.

`Prompt.messages` carries user/assistant/tool roles, visible assistant content,
native calls and correlated results. llama.cpp serializes native chat messages;
opaque `ConversationRef` remains unsupported by this stateless adapter.
`PromptMessage` is invocation input, not a durable `ConversationMessage` or Memory.
The installed Qwen template advertises native Tools and call/result support;
no template, service or 32K profile change was made.

On-demand limits are **up to 10 total model requests**, three proposals, eight
read actions, 4,096 requested output tokens/call, 300 seconds/call and 900 seconds
overall. Task/grant limits may be smaller. Investigation consumes reserved model
calls; it is not an extra allowance. Future policies may permit ten calls, but
existing grants retain their actual limits. After eight reads only the proposal
is disclosed. Invalid calls, output-limit responses and ambiguous outcomes
terminate without automatic retry.

Active selection is capped at 24,000 serialized message bytes, retaining the
objective, newest complete exchanges and latest actual validation feedback.
Older exchanges are explicitly omitted with archive references, never silently
summarized; assistant/call/result groups stay intact. If a pinned exchange cannot
fit, admission refuses. Reads emit at most 4,096 source UTF-8 bytes and complete
Tool responses at most 12,000 bytes. These are **byte bounds, not token estimates**.
Actual provider prompt/completion counts and configured 32,768-token occupancy
are recorded. Unknown cache/reasoning categories remain unknown.

## Execution and inspection

The existing CLI also accepts a trusted host task definition:

```powershell
uv run python scripts/qwen/coding_worker.py --task-definition .local/backlog/preparation/WORK/task.json --report-directory .local/qwen-coding-worker/NEW-RUN
```

This template grants no authority for a historical task. Paths/config are checked
before genuine default-No consent. Model-authored task JSON is never authority.
Delegated WorkCycle execution uses its existing exact-task review, reservation,
source owner and per-call guard without redundant consent. Reads must fit the
standing source/test scope; publication remains separate. Never reuse an old
path-bound grant or redispatch an existing work slot.

Existing `qwen-coding-loop-v2` captures remain the evidence contract. Each turn
retains request/response JSON and hashes, native IDs, `tools.json` call/results,
versioned selections, diffs, full validation logs, bounded feedback, UTC timing,
usage and termination. Selection never erases archives. Repairs count proposals,
not investigation requests. The existing dashboard consumes these same records
behind raw-data disclosure controls. Optional framework observation honors
independent prompt/call-argument capture policies for native input history.
Text-only Context assemblers explicitly refuse structured input rather than
discarding history. No second transcript or authority store was introduced.

[Evaluation and authority status](EVALUATION.md) separates scripted acceptance,
live read-only conformance and still-unmeasured live coding efficacy.
