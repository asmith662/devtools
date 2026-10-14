# Live operational visibility and failed-run preservation

This engineering increment adds default live stderr lifecycle reporting while
keeping final stdout JSON machine-readable. It grants no execution authority and
changes no production behavior or scientific design. No live model or scientific
treatment is used to validate it. The controller remains experiment-owned;
framework Runtime, Commands and observability ownership are unchanged.

## Preserved failure

Run `5cb532eb162b3d8f7cf7c8f96c424c9a9d905307b19fbe18ad7a99ee7e91dc7a`
is historical **FAILED/BLOCKED / GENERATED_ARTIFACT_SCOPE_DEFECT**. Its approval
commit is `5afa0433d3720c03714cd1d57d641af55c014612`, with exact tracked artifact
`experiments/source_grounding/runs/5cb532eb162b3d8f7cf7c8f96c424c9a9d905307b19fbe18ad7a99ee7e91dc7a/authorization/approval.json`
and receipt `authorization/publications/APPROVAL.json` beneath that same run root.
Those artifacts remain unchanged. That approval binds only the original plan and
implementation; it cannot approve this engineering change or a replacement run.

All three prepare and packet operations and validators completed. Checkpoint 0
passed focused contracts; checkpoint 1 ran
`uv run ruff check experiments/source_grounding` and failed with 1,221 diagnostics
in six generated reviewer/packet Python payloads. PACKET never committed.
B, lexical acquisition, Reference treatment, Sol, C, Astra, gold and D never
entered; automatic scientific retries were zero. The old run cannot resume.

The ignored archive is
`.local/experiment-failures/5cb532eb162b3d8f7cf7c8f96c424c9a9d905307b19fbe18ad7a99ee7e91dc7a/`.
Its deterministic `manifest.json` has SHA-256
`8e931a868bf204e4ea4ef2c8074df83bd54a47eb01fb49ee3ed1b02a10d693b9`.
It records original/archive addresses, byte lengths, SHA-256, Git status and roles
for 208 files / 17,208,113 bytes: repository candidates, tracked approval copies,
original operational files and worker-root files. The 51 untracked repository
candidates total 6,848,242 bytes. Each was attributed to this run, copied, reread
and hash-verified before its original untracked copy was explicitly removed.
No tracked artifact or original operational/worker-root file was altered.
The complete Ruff stdout is retained (1,496,067 bytes; SHA-256
`e836e900c0e544651ca5357c4f99815ec794a750ef26678aa80aada6be8f23e6`).
The manifest preserves exact failure-log addresses. The archive is a forensic
copy, not scientific authority; the tracked original approval and Git checkpoints
authenticate historical identity independently.

## Human interface

Default events are flushed to stderr:

```text
HH:MM:SS +MM:SS case operation STARTED|HEARTBEAT|COMPLETE model/reasoning pid=PID duration
```

The latest [runtime hardening](../host_disclosure/README.md) makes normal lines
compact. Detailed paths, commands, identities and PID/queue updates remain retained;
`--verbose-events` exposes them and failures always display full diagnostics.
Authentication, plan progress, approval publication, case queues, owned child
starts/PIDs, completion, validation progress, publication and final run state are
visible. Codex prompt bodies and credential arguments are redacted; prompt,
instruction and packet identities are shown instead. Stage C explicitly identifies
the blind semantic gold worker; nested B grounding uses the same small operational
allowlist through `B/operational.log`, outside the sterile reviewer input and
scientific candidate outputs. A malformed bridge line is ignored, never authority.
The bridge changes neither model inputs, blindness, output seals nor retry policy.

Every active subprocess gets a rate-limited 15-second heartbeat with operation
elapsed, frozen timeout remaining, PID/workspace/model when known, counters and
time since useful stream output. Authentication/publication waits also heartbeat.
This means the supervisor still observes the operation, **not** that the model
is progressing usefully or that science is succeeding.

The existing external-worker CommandExecutor specialization mirrors full raw
stdout/stderr chunks to retained logs before bounded event-queue loss. Logs flush
during execution. Canonical capture limits, timeout, cancellation and tree reap
remain in force; full retained logs do not relax truncation failure policy.
The child PID record includes observed launch UTC; child-exit/exit records include
exit UTC and monotonic duration. Filesystem mtimes are never exact launch evidence.
Supervisor stderr is separate from child stderr. Raw model streams are retained
without flooding the normal console.

Failures immediately print a FAILED banner, case/stage/operation, command,
workspace, exit/category, duration, useful prefix and bounded tails, truncation
flags and absolute full-log paths before final JSON. The operational summary
separates B/C entry claims, observed Sol/Astra PIDs, gold completion receipts and
zero automatic scientific retries. OS launch observation is distinct from the
durable scientific ENTERED claim. Operational data cannot authorize retry.

```text
uv run python -m experiments.orchestration status <run-id> --follow
uv run python -m experiments.orchestration status <run-id> --follow --json
```

The viewer authenticates the original approved plan/controller-map identity and
tracked approval receipt, displays an initial snapshot/log locations, tails
progress (including heartbeat/PID events), and stops at COMPLETE or BLOCKED.
Ctrl-C cancels only the viewer, without worker cleanup, execution-state writes,
approval, resume, publication or retry. JSON follow emits JSONL on stdout.
Historical status works after controller upgrades using the original frozen
bindings, without treating old authority as executable by changed code.

Uncommitted publication receipts are BLOCKED / MAINTAINER_DECISION_REQUIRED.
A viewer may wait while the operational supervisor still reports RUNNING during
an in-progress publication; that observation never permits resume. Callable
status is conservative until receipt bytes and Git publication authenticate.

## Validation ownership

Maintained implementation files are static-check inputs. Generated PREPARATION,
PACKET, primary builders and scientific results are data with separate schemas,
byte hashes and replay validators. Replacement source-grounding plans must pin
explicit maintained source addresses, never discover run payloads recursively.
The controller's mandatory FINAL protected/static floor is unchanged.

Deterministic tests use bounded fake subprocesses and temporary repositories to
exercise start/PID, live exact logs, heartbeat, completion/failure, timestamps,
nested semantic metadata, approval/publication reporting, stdout JSON, read-only
follow/detach and conservative publication status. No live model is necessary.
