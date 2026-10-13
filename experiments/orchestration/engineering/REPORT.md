# Experiment controller engineering completion

EXPERIMENT_CONTROLLER = COMPLETE. This is a validated engineering lifecycle,
not a scientific effectiveness result or autonomous research Agent. The next
PURPOSE_RELATIVE_SOURCE_GROUNDING cohort remains NOT_STARTED.

The implementation is owned by `experiments/orchestration/`; its
[operator guide](../README.md) and [adapter contract](../CONTRACT.md) define the
callable API, CLI, fixed stages, approval receipt and two human gates. It does
not alter production framework ownership, Retrieval, RI, Localization or Runtime.
No real prospective run plan or Cases 0020-0022 were created.

## Proven workflow

A committed approval binds canonical plan bytes, immutable reachable Stage A,
protocol/integrity hashes, ordered cases/frames, source implementations, semantic
launcher/model/reasoning, validation, concurrency, timeouts, retry and publication.
The content-addressed run ID excludes operational clocks. Public plan/configuration
and state snapshots cannot mutate in-flight semantics.

The controller prepares frames and packets, freezes a packet checkpoint, overlaps
bounded independent B/C case workers, authenticates/imports the exact seven primary
artifacts, waits for both branches, joins D, validates and publishes serialized
checkpoints. Only its publisher writes main. A worktree lease and post-validation /
post-commit parent checks reject competing advancement without discarding work.
The local-remote tests exercise commits, pushes and remote divergence entirely in
temporary repositories; the main synthetic integration uses no remote.

ENTERED is exclusive and precedes launch. Failed or ambiguous entered attempts are
dead; automatic scientific retries are zero. Resume authenticates approval, code,
inputs, committed publications and returned outputs, skips completed work and
permits only provably never-entered work. It refuses FAILED, entered/unreturned,
changed bytes/code, stale identity and ambiguous publication. Existing independent
workers finish into quarantine after sibling failure; no new scientific entry or
D publication follows. A late sibling failure during packet validation is covered.

Workers have disjoint external workspaces. Sterile copying rejects existing roots,
checkout ancestry, links/junctions/reparse points, non-allowlisted files, Git and
initial local state. Validation/version probes cannot leave extra files before
review. No other case or B output is copied to C. Packet hashes are checked before
and after worker/validator execution. Scientific output files and deterministic
validators, never terminal prose or `.local/codex-result.md`, drive authentication.
Filesystem/input isolation is mechanical; broader behavioral blindness and host
routing remain attestation/trust boundaries, not an OS secrecy guarantee.

The real Codex adapter is complete for CLI 0.162.1, with explicit pre-entry version
refusal, frozen account model ID/reasoning, fresh `exec`, ephemeral isolated home,
ignored user rules/config, no daemon, noninteractive approval and disabled web.
Installed help/version and a managed `--version` probe were inspected; no model
was contacted. Tests use actual Python processes with fake behavior confined to
fixtures. Canonical Commands owns collection/timeouts/reaping; the documented
worker-boundary specialization adds environment/PID and Windows kill-on-close Job
ownership. Timeout and descendant cleanup are tested on Windows. POSIX support is
implemented but was not exercised on this host. Catastrophic controller/host loss
still requires manual reconciliation of ambiguous entered work; resume never
kills a reused PID or treats heartbeat as scientific proof.

Progress JSON/JSONL, case/stage/model, timestamps, elapsed durations, queue/running /
completion/dead/quarantine state, PID/exit/stream logs and archive references remain
ignored operational assistance. Invalid worker progress cannot kill scientific
execution. Status distinguishes uncommitted candidates from verified final results.
Committed artifacts and journals reconstruct status after operational/workspace
removal; a separate CLI process verifies the completed fixture. Final summaries
seal operation receipt hashes and remain deterministic on repeat.

Scientific publication attributes preserve raw CRLF and meaningful trailing spaces
(`-text -whitespace`); artifact schemas/hashes/replay authenticate those data bytes.
Controller implementation whitespace remains checked, with explicit CR-at-EOL
support rather than normalization. The exact-byte publication regression checks
raw Git blobs, including CRLF and trailing spaces. No existing primary was edited.

## Cache

The immutable preparation cache stores explicit artifact bytes, with keys binding
schema, tree, RepositoryId, full frame, observation semantics, implementation,
disclosed input digests, configuration and named surfaces. Hits recheck integrity
and run a fresh frozen validator. Corrupt entries reject/recompute before treatment;
cache write failure cannot make valid scientific output invalid. No live object is
pickled and no cache becomes authority. CACHE_HIT/MISS/REJECTED/RECOMPUTED,
digests, implementation, bytes and elapsed time are retained.

The fixture measures 632 bytes of explicit frame representations and three
validated hits. Native Corpus/index/RI representations are eligible only through
adapter-owned deterministic serializers and validators; this increment does not
pretend to retrofit every native object or historical capture. Historical immutable
preparation-byte caching is implemented. LIVE_INCREMENTAL_RI remains REQUIRED /
NOT_IMPLEMENTED, including edit-time index/relationship maintenance.

## Measurements and efficiency

These are single synthetic engineering samples on Windows with temporary Git and
fake semantic workers, not retrospective scientific timing or a 3x claim:

| Configuration | Seconds |
|---|---:|
| Serialized, cold, shared worker limit 1 | 25.2319 |
| Concurrent, cold, shared limit 6; B/C limits 3 each | 18.3622 |
| Concurrent, three validated cache hits | 15.8192 |

The observed cold difference is 6.8696s; cached versus concurrent cold
is 2.5431s. Process startup, Git, validation and concurrent host load
remain in these measurements. One sample cannot estimate variance or establish
native RI savings. The exact source hashes, case-stage durations, cache data,
publication identities and read-only adoption receipt are in
[measurements.json](measurements.json). The measured fixture substitutes validation
of its fake repository; it does not include production-suite duration.

A transparent old-workflow model has ten logical handoffs: A approval, B launch,
three reviewer launches, three imports, D launch, final review. This is an explicit
model, not a measured retrospective intervention count; workspace switching,
validation and publishing could add work and some actions may be bundled. The new
normal workflow has two decision gates and one execution command between them
(optional read-only preflight/status commands add no gates).

A serialized compute model sums per-case preparation/packet/B/C/import durations,
publication, D and validation. With enough bounded capacity, the parallel model is
max(preparation) + max(packet) + packet publication + max(max(B), max(C)) + B
publication + max(import) + C publication + D + final validation/publication.
Resource limits can lengthen that critical path. Successful runs eliminate manual
workspace switching, reviewer launching and copying. Intermediate experiment-only
checkpoints use focused validation; full protected development runs once at final
D rather than being duplicated at every intermediate publication.

## Validation and scope policy

- Controller contracts: the complete 65-test suite passed; five publication /
  integration regressions passed after the final byte-policy correction (66 unique
  controller tests passed in total), including the three-case end-to-end fixture,
  bounded concurrency, independent branches, input leakage, real-process timeout /
  descendant cleanup, failure/dead/no-retry, safe/refused resume, cache corruption,
  progress corruption, immutable API snapshots, Git races/divergence, receipt
  tampering and separate-process verification.
- Existing structural capture/packet/sealed-proof contracts: 40 passed.
- Existing synthetic exactly-once journal tests: 3 passed. No Graph-3 historical
  replay or unrelated full historical ranking fixture was run.
- Protected development: 1,588 passed, two opt-in live tests skipped; production
  statement/branch coverage 100%, run once during this increment. Subsequent changes
  remained experiment-only and received focused validation.
- Ruff `src tests experiments/orchestration`: PASS. Controller formatter: PASS.
- Strict mypy `src tests experiments/orchestration --exclude tests/experiments/`:
  PASS, 434 source files. Controller-only strict mypy: PASS, 19 files.
- Read-only completed-cohort adoption: PASS, A authenticated, B sealed, C imported,
  D complete for 0017-0019. Scientific executions/deep historical replays zero.
- Unstaged/staged whitespace and ownership/integrity checks are required before
  engineering publication and recorded with the containing commit/handoff.

Initial unqualified global static commands exposed pre-existing archived scientific
program errors: Ruff reported 22,150 findings; the global formatter crashed while
rendering old unformatted content. Broader supported-source formatting also found
62 unchanged files. Unqualified mypy (and a first scope including retained
experiment tests) was stopped after reporting legacy errors. None of those bytes
was fixed or normalized by this increment.

The explicit final policy in the development guide requires the full protected
suite and supported-source static floor, plus the approved experiment's own
complete verification/static commands. Raw imported primary builders are immutable
scientific payloads, not supported source to retrospectively style-normalize.
Protected tests and type scope consistently exclude retained outcome-dependent
`tests/experiments/`. Changed production source retains applicable formatting and
full protected validation. This scope derives from ownership, never scientific
labels or results, and does not waive failed scientific/integrity checks.

## Durable state and next action

Production Retrieval and all accepted results are unchanged: U1, U2, U3, R1.7, R2,
GRAPH-3; direct structural discrimination; the post-hoc ORACLE / NON_GATING /
NOT_RUNTIME_AVAILABLE source-quality result SOURCE_QUALITY_LOOKS_EXPLANATORY;
retrieval performance baseline; separated sealed/deep verification. Historical
population remains FROZEN. SEARCH_POLICY_FAILURE remains NOT_ASSESSED.
Confirmation/reserve remain NOT_ACCESSED; historical child implementations,
paths/diffs and holdouts were not accessed. No live reviewer, new gold or new
retrieval-effectiveness treatment was executed.

The sequence remains controller -> source grounding -> search-policy/iterative
evidence pursuit -> obligation-sufficiency/Context -> live incremental RI ->
deliberate autonomous-Agent integration. The next action is maintainer review of
the controller, then prospective freezing/approval of the already-planned source
grounding cohort and execution through this machinery, followed by final D review.
No next treatment is designed here. Source-specific adapters/packet instructions
belong to that prospective Stage A; this increment supplies their complete fixed
orchestration and authentication contract, not their scientific semantics.
