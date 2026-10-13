# Approved experiment cohort controller

This experiment-owned controller executes an approved, immutable Stage A contract.
It is engineering infrastructure, not a researcher or the production autonomous
Agent. It selects no hypothesis, semantic interpretation, treatment, retry, ranking
policy or architectural disposition. Production Retrieval, RI, Localization,
Context and Runtime do not depend on it.

## Operator guide

1. Freeze the experiment-specific adapters, packet instructions, Stage A, ordered
   cases and run plan. Commit a separate explicit approval receipt binding the
   canonical plan digest and Stage A checkpoint. Review both before approval.
2. From the clean synchronized main worktree:

   ```text
   uv run python -m experiments.orchestration plan experiments/<experiment>/run-plan.json --work-root C:/ExperimentWorkers
   uv run python -m experiments.orchestration run experiments/<experiment>/run-plan.json --work-root C:/ExperimentWorkers
   ```

   `plan` is a read-only preflight; `run` needs no intermediate interaction.
   Workspaces must be outside the canonical worktree and on a trusted local disk.
3. Use the returned immutable digest as the run ID:

   ```text
   uv run python -m experiments.orchestration status <run-id>
   uv run python -m experiments.orchestration verify <run-id>
   uv run python -m experiments.orchestration resume <run-id> --work-root C:/ExperimentWorkers
   ```

   Status/verify emit structured JSON with per-case stages, failure boundaries and
   publication receipts. Operational `progress.json`, `progress.log`, `state.json`,
   bounded process logs, PIDs, exit codes and archive references live under ignored
   `.local/experiment-runs/<run-id>/`. No terminal scrollback is required.
4. Review the final Stage D result. This is the second normal human gate.
   A failed or ambiguous operation instead requires a maintainer decision.

No live scientific run plan is supplied by this increment. The next cohort is
**PURPOSE_RELATIVE_SOURCE_GROUNDING / NOT_STARTED**. Do not manufacture a plan by
copying the synthetic test fixture into a scientific protocol.

## Callable contract and ownership

```python
controller = await Controller.from_plan(repository, committed_plan_address, work_root)
preview_identity = controller.run_id
result = await controller.run()  # or explicit resume=True for a proven safe state
status = await controller.verify()
```

`experiments.orchestration.controller.Controller` and `model.RunPlan` are the
Agent-callable seam. Results include run identity, current state, failure boundary,
publication commits and review readiness. The eventual trusted Tool can wrap this
API without screen scraping. There is no Tool wrapper, general workflow DSL,
Agent loop, recursive planning or framework orchestration API here.

The [adapter contract](CONTRACT.md) specifies declarative metadata and exact
transport. The [engineering report](engineering/REPORT.md) records validation,
measurements and limits. The fixed stages are preparation, packet, B, C, import
and D; publication boundaries are PACKET, B, C and D. Earlier completed scientific
packages retain their ownership and byte identity.

## Execution and isolation

Preparation and packet construction are bounded concurrent per-case work. All
packets publish before semantic workers start. B and C then run concurrently in
separate per-case directories, with independent case/semantic limits and one
shared process limit. B receives prepared frame bytes; C receives only its own
allowlisted frozen packet. C never receives B outputs; B never receives C outputs.
Imports wait for both branches to validate, and D waits for committed B and C.
The current implementation publishes B after both branches finish; computation
still overlaps. This conservative publication order can be relaxed in later
engineering work without changing scientific semantics.

Only the controller publishes to main. Workers use external fresh staging roots,
never commit or push, and never receive the publisher object. A cooperative
worktree OS lease and serialized publisher enforce one controller writer. Starting
main, origin/main and actual remote main must agree. An unexpected advancement,
index/worktree change, failed commit or ambiguous push stops publication and
preserves candidate outputs. No force push, reset, rollback or blind retry occurs.
Immutable receipts identify parent commits; the resulting commit is recovered
from Git rather than self-referentially embedded. Published scientific artifacts use `-text -whitespace` attributes to preserve
original bytes, including CRLF and meaningful trailing spaces. Hashes, schemas
and deterministic validation authenticate these data; implementation whitespace
remains checked, with explicit CR-at-EOL support. The controller checks bytes again after validation.

The sterile builder rejects existing destinations, links, junctions and reparse
points, `.git`, initial `.local`, non-allowlisted paths and known treatment metadata
keys. It checks packet bytes before/after the worker and validator. Case validators
remain responsible for exact task/resource/obligation schemas and content joins;
key scanning does not prove arbitrary prose free of leakage. Packet/source
allowlists are approved scientific inputs, not discovered heuristically.
This enforces filesystem/input separation; it is **not an OS-level secrecy
sandbox**. Trusted adapters and reviewer behavioral blindness attestations remain
necessary. Repository code paths used by managed process supervision do not enter
reviewer input, inherited PYTHONPATH or Codex session state.

## Semantic and process boundary

The complete local Codex adapter targets installed **codex-cli 0.162.1** and uses a
fresh `exec` with ephemeral sessions, ignored user config/rules, no daemon,
noninteractive approval, explicit sterile CWD, workspace-write sandbox, disabled
web and frozen model/reasoning. It never uses resume/fork. Only authentication
bytes may be copied to a fresh per-case CODEX_HOME; no prior session/config is
copied. CLI JSONL thread IDs are checked for accidental within-run reuse.
Pre-entry verification requires the frozen CLI version `0.162.1`; a mismatch
stops before any reviewer claim. The plan freezes the actual account model ID; the controller does not guess an
alias for the display designation GPT-6 Astra / High. Host routing is not
independently proven. No live reviewer was run during development.

The generic direct-process launcher also supports frozen external worker commands;
only tests supply fake semantic workers. The small stable launcher prompt points
to detailed immutable packet instructions. A real experiment must supply those
instructions, the exact seven scientific outputs and a deterministic standalone
validator. Terminal text and `.local/codex-result.md` are operational handoff only.
Single-primary designation, no second reviewer/reconciliation, complete blindness
attestation, expected files, hashes, packet preservation and deterministic replay
are required through the frozen validator plus controller checks.

Commands use the canonical managed CommandExecutor collection, bounded streams,
timeout, cancellation and reap lifecycle. Its process-creation/termination hooks
are specialized only at this external-worker boundary because current canonical
Commands lacks per-child environments, retained PID and descendant ownership.
Windows supervisors join a kill-on-close Job **before** spawning workers; normal
timeout first terminates/reaps the immediate child and process exit kills remaining
descendants. POSIX uses owned sessions with TERM/KILL cleanup and a supervisor
termination handler. Only Windows behavior was exercised on this host.
This documented exception does not introduce a parallel general command framework
or modify production Commands. Standalone supervision uses isolated Python startup;
worker environments are explicit allowlists and do not inherit PYTHONPATH,
PYTHONSTARTUP or shared CODEX_HOME. No credential values are logged.

## Failure, retry and recovery

An exclusive ENTERED claim is written **before launch**. This deliberately makes
ambiguous launch failures dead even if no scientific work actually started.
Without ENTERED, a pristine never-entered workspace may resume. With RETURNED,
exact identity/input/output receipts are authenticated and the operation is skipped.
Entered/unreturned, FAILED, changed code/plan, altered output or ambiguous publication
states cannot resume. No replacement attempt ID is silently selected. A maintainer
must approve an explicit new attempt/plan after scientific failure. Automatic
scientific retries are zero.

A sibling failure blocks new queued/dependent work. Already-entered independent
workers finish and are quarantined; they cannot cause B/C/D publication. They are
neither canceled merely for a sibling failure nor retried. A timeout ends the
owned process tree and marks the attempt dead. Parent cancellation also reaps owned
processes. A host crash cannot prove an entered operation returned; resume refuses
it rather than trusting a PID or operational log. A surviving detached worker on
host/controller catastrophe requires operator reconciliation, not PID-only kill.

Claims, returned receipts, run identity and checkpoint artifacts are immutable
repository-owned scientific provenance outside `.local`. Operational state is
replaceable. Completed canonical outputs, including preparation artifacts, remain
verifiable after temporary workspaces and operational files are removed. Stage D
contains a deterministic controller summary without timestamps. Operational timing
and progress have timestamps/elapsed durations; these never define run identity.
The writer lease is cooperative concurrency control, not scientific authority.

## Cache and validation

The non-authoritative cache stores explicit deterministic artifact bytes, never
pickled live Corpus/RI objects. A preparation adapter can serialize tree
materialization manifests, observation/Corpus, lexical fields/statistics/index,
Python candidacy/module analysis and structural views **only when its frozen
semantics and deterministic validator support those representations**. This
increment supplies the mechanism and tests explicit frame bytes; it does not
retrofit old scientific capture owners or claim native-object cache coverage.
Keys bind schema, parent tree, RepositoryId, observation semantics, adapter
implementation digests, relevant configuration, disclosed input digests and named
surfaces. Every hit checks integrity and runs the frozen preparation validator.
Corrupt or invalid entries are rejected and recomputed before scientific treatment,
with CACHE_HIT/MISS/REJECTED/RECOMPUTED, digest, bytes, implementation and elapsed
observability. Cache state can never authorize capture or revive a dead operation.
**Live incremental RI/index/relationship maintenance remains REQUIRED /
NOT_IMPLEMENTED**, independently of this historical immutable preparation cache.

LOCAL: focused experiment contracts/static checks during development. CHECKPOINT:
stage validators/replay, integrity and focused declared checks for experiment-only
intermediate publication. FINAL: declared final verification plus mandatory protected
development validation and supported-source static checks once before D
publication.
Any production `src/devtools` publication selects FINAL. Controller publication is
experiment-owned, so it cannot publish production sources through its transport.
This tier policy is documented in the repository validation guide; it never opens
confirmation/reserve or removes production coverage gates.

## Static scope and immutable scientific inputs

FINAL always schedules protected development validation, Ruff over supported
`src`, `tests` and this controller, strict mypy over `src`, protected `tests` and
this controller, and formatter verification of this controller. The run plan must
also declare complete verification and static checks for its active experiment
adapters. LOCAL is callable through `checkpoint_validation("LOCAL", paths)` for
development; successful immutable run checkpoints do not redundantly repeat it.

Whole-repository blanket commands also traverse frozen reviewer builders and old
scientific programs. They currently fail, and the global formatter crashes while
reporting an old archive. Those outcomes remain recorded in the engineering
report. They do not authorize reformatting imported primary bytes or changing
accepted results. The explicit ownership-based scopes above preserve full protected
production validation and current-source lint/type checks while keeping scientific
payloads immutable. Changed production code still requires applicable formatting
and full protected validation before publication. This is an engineering scope
policy, never a scientific-outcome or gold-dependent selection rule.
