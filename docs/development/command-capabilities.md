# Command capabilities, deterministic procedures and observed patterns

This increment promotes repository inspection and fixed change validation into
reusable Tools, plus bounded command observations and diagnostic pattern analysis.
It is framework-first: the independent host and operator entry points require no
Qwen application, Codex implementation, prompt, profile or model invocation.

## Ownership decision

Keep `devtools.resources.commands` in Resources. Immutable Command, managed
CommandExecutor/CommandExecution, byte streams, output limits, timeout and child
cleanup are reusable resource mechanics. Existing consumers include serving,
Codex, Tools and repository scripts. Moving them to `execution.commands` would
change imports/dependency ownership without fixing a demonstrated defect;
Execution still owns narrow Conversation/ModelInteraction coordination and
InteractionAttempt. No package relocation or second executor is introduced.

| Responsibility | Owner and reused substrate |
| --- | --- |
| Native executable availability | `resources.commands.availability.discover_executable`; native PATH/PATHEXT via the standard library and canonical resolved paths |
| Typed Git inspection | `tools.repository.git.GitInspectionTool`; existing managed Commands and explicit host root |
| Immutable fixed checks | Existing `tools.checks.FixedCheckPlan`, `FixedCheckTool`, `FixedCheckResult`; ToolRunner and CommandExecutor |
| Inspect/select/check/report | `tools.repository.validation.InspectAndValidateTool`; a single finite deterministic procedure, not a workflow engine |
| Privacy-selected command facts | `observability.commands`; existing live handles/results and canonical Duration |
| Codex JSONL projection | `agents.integrations.codex.commands`; available external-agent records, no change to default invocation |
| Pattern candidates | `observability.commands.patterns.summarize_patterns`; bounded deterministic grouping, no store or promotion authority |
| Operational consumers | `scripts/check_change.py`, `scripts/command_patterns.py`, the guarded independent host and explicit capture in the current development host |

Tools and Models remain independent. Agents may expose a selected procedure
through existing native Model/Tool composition and explicit admission. Neither
Tool schemas nor normalized command observations are execution authority.

## Repository and environment contract

The host supplies an exact canonical working-checkout root. Git inspection uses
`--no-optional-locks`, authenticates Git's reported root and committed HEAD, reads
porcelain-v1 NUL-delimited status, then rechecks HEAD and status. The result retains
separate staged/worktree/untracked states and literal UTF-8 path spelling. The
parser also supports the documented reversed destination/original rename fields;
the actual inspection disables rename inference. Malformed, truncated, duplicate
or unsupported-encoding records refuse rather than silently dropping a path.
Unborn/bare repositories without the required working-root/revision contract
refuse. A changing observation is explicitly unstable.

The [Git machine-output contract](https://git-scm.com/docs/git-status#_porcelain_format_version_1)
supplies framing; this is not English-console parsing. Ignored files and
submodule contents retain Git's stated visibility semantics. Repeated equal
status/HEAD observations are not an atomic snapshot, content hash, sandbox or
universal input closure. SourceScope provides separate declared-source
correspondence when the host requires it. Git configuration/executables remain
part of the selected trusted environment.

Executable discovery reports a native selected path or explicit absence, with
platform classification. It does not install software, prove executable versions,
infer credentials or grant permission. One direct argv contract supports Windows
and POSIX; there are no parallel shell implementations. Windows spaces/Unicode/
special-character paths are exercised with real subprocesses. Parser tests cover
literal special filenames independently. Native POSIX execution is not claimed
from a Windows run.

## Inspect and validate an authorized change

The host constructs ChangeValidationPlan from an existing FixedCheckPlan, pinned
revision, exact allowed changed addresses and immutable CheckSelection values.
Each rule names an already selected check and either always applies or applies
when its explicit path set intersects observed changes. Optional structural
CommandPattern labels are host-selected, not derived from private argv.

The procedure inspects the root/revision/worktree, refuses foreign scope or
unmerged state, selects checks deterministically, invokes FixedCheckTool through
ToolRunner, retains sequential results, and reinspects Git and any declared
SourceScope. No model is called to choose routine branches. No model argument can
substitute a command, repository or environment override. The host allowlists
explicit Command environment-override names; the existing parent environment
inheritance contract remains, without an environment-isolation claim.

Statuses distinguish passed, failed, skipped, refused, incomplete and cancelled.
An invocation with no applicable checks is reported as skipped. CheckExecution retains a
known FixedCheckResult or unavailable acknowledgment plus the original error.
Process exit success, a passing declared check, task/candidate acceptance,
protected validation, independent review and publication remain separate facts.
Diagnostics/exit/duration are those actually returned by managed Commands; no
individual test assertions are manufactured from a console summary.

Each procedure Tool instance represents one host-associated invocation. A second
or concurrent dispatch with that instance refuses before effects; a new explicit
invocation needs a fresh host origin/instance. This is not cross-process locking
or exactly-once replay. Earlier results survive a later error, and cancellation
is retained in last_report before the original cancellation propagates. A lost
acknowledgment may follow a completed effect; it is never retried automatically.

The library result retains host-bounded diagnostics for the selected caller. The
operator JSON projection omits command/env/output/error payloads. It should be
used for ordinary metadata reporting rather than serializing arbitrary runtime
results into permanent analytics.

```text
uv run python scripts/check_change.py REPOSITORY --revision PINNED_HEAD \
  --run UNIQUE_HOST_INVOCATION --allow src/example.py --check whitespace
```

This repository's operator selects from a finite whitespace/tests/lint/typing
vocabulary; tests invokes the unchanged protected development entry point,
including its experiment exclusion and production coverage gate. The
library accepts other immutable host-fixed check plans without a command plugin
system. These scripts delegate actual work to the framework procedure. Governed
WorkCycle validation and publication remain separate and unchanged.

## Observation strength and privacy

CommandInspector opts into one existing CommandExecution handle. It consumes
lifecycle facts and awaits that same execution; it does not execute a second
command. A known CommandResult establishes local completion/entry even when
events were dropped. Error or cancellation without a retained start event leaves
entry unknown. Collector failure/loss is qualified separately and cannot replace
a known result. Its owned reader is settled, and cancellation still reaches the
original managed child cleanup.

The procedure has reliable local lifecycle evidence for its Git handles. Fixed
checks project known returned results; interrupted check entry remains unknown
because the existing Tool does not expose its internal handle. This is useful
partial instrumentation, not automatic observation of every Tool/Command in an
application. Existing EvidenceSink and invocation inspectors are specialized
contracts and are not overloaded with command records. No new persistence store,
EventBus, global tracer or normalized durable Evidence ingestion is added.

CommandOrigin supplies host-associated agent/task/run/call keys. CommandPattern
contains curated family/operation labels, value-free argument roles, capability
tags and an optional known equivalent Tool. Observation retains known entry,
outcome, exit and elapsed duration, plus capture qualification. Raw argv, shell
text, stdin, environment values, credentials, source and stdout/stderr are absent
from normalized analytics. Labels themselves must be nonprivate host choices.
The current development host explicitly projects its own authorized framework
validation commands; this is real developer-agent activity, not evidence that all
commands inside Codex pass through devtools.

## Codex external-agent boundary

Installed Codex CLI0.162.1 help confirms `exec --json` JSONL output. The
[official non-interactive documentation](https://learn.chatgpt.com/docs/non-interactive-mode#make-output-machine-readable)
describes item command events. The bounded adapter handles selected
item.started/updated/completed command_execution records. Synthetic fixtures
exercise exit/status fields, repeats, missing completion, malformed input and
out-of-order observations; no live command feed or paid model call is claimed.

The adapter uses a host-selected run/item namespace, preserves partial known
fields, deduplicates repeated facts and exposes contradictory measurements as
conflicts. Only bounded numeric `item_N` identities in the selected CLI surface
are admitted; unexpected identities are qualified as unsupported rather than
copied into analytics. CLI reported completion is not locally verified process entry;
entry and duration remain unknown. A turn terminal event never proves complete
command coverage, and missing events never establish that nothing was attempted.
The current CodexAgent returns its established final response/usage interface and
does not expose a complete command feed. Its default invocation is unchanged.

Only a small exact command vocabulary is projected by default; shell wrappers,
unknown arguments and private commands stay opaque. A trusted host can supply a
different value-free projector. Aggregated output, messages and raw command
strings are not retained. Transient parsing/digests are not a privacy guarantee
or a substitute for controlling the source archive and exception retention.

```text
uv run python scripts/command_patterns.py AUTHORIZED_EVENTS.jsonl \
  --agent EXTERNAL_WORKER --task TASK --run UNIQUE_CLI_INVOCATION
```

This reads only the explicitly selected bounded file. It does not search personal
session logs, start Codex or scrape private implementation records.

## Procedural candidates and future autonomous composition

Pattern analysis deduplicates stable origin keys and refuses contradictory input
records; CLI partial reconciliation happens before analysis. It reports family,
operation/argument roles, capabilities, frequency, distinct tasks/agents,
success/failure/cancellation/unknown/conflict counts and same-run co-occurrence.
Co-occurrence does not establish order, preconditions, safety or a recipe. An
output bound limits related-operation suggestions and marks truncation explicitly.
A known equivalent Tool is retained so repeated use does not automatically create a
duplicate capability. Frequency alone never promotes a command to trusted code.

A future candidate needs an explicit behavioral/environment/authority contract,
independent tests and host approval before implementation. These capabilities can
serve provider-independent planners/supervisors, delegated local or external
workers and factual assessment. Backlog discoveries remain proposals; consequential
work retains governance. Durable task recovery and uncertain-effect reconciliation
remain existing cross-cutting obligations. No idle daemon, automatic backlog
promotion, generic orchestrator, Memory database or new Qwen feature is delivered.

The [routine development envelope](workflow.md) reduces repeated approval friction
within already authorized read/check/edit work while preserving actual sandbox,
host and publication requirements.
