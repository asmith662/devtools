# Approved experiment cohort controller

This experiment-owned controller executes an approved, immutable Stage A contract.
It is engineering infrastructure, not a researcher or the production autonomous
Agent. It selects no hypothesis, semantic interpretation, treatment, retry, ranking
policy or architectural disposition. Production Retrieval, RI, Localization,
Context and Runtime do not depend on it.

## Operator guide

1. Commit the scientific Stage A protocol/artifacts **first**. Then create and
   commit the prospective run plan naming that exact Stage A commit. These are
   two commits, with no self-reference and no approval receipt. Together they
   form the prospective package for Gate 1.
2. Validate without authority, and return both commits and the exact run ID for
   maintainer review:

   ```text
   uv run python -m experiments.orchestration plan experiments/<experiment>/run-plan.json
   ```

   This reports PLAN_VALID and EXECUTION_AUTHORIZED = NO. It starts no worker,
   creates no approval and does not change plan bytes. Plan validity != approval;
   a plan commit != approval. Models, cases, dependencies, validation/publication
   policy and the immutable run ID are visible before approval.
3. After review, the maintainer issues **one explicit command**, without prompts:

   ```text
   uv run python -m experiments.orchestration run experiments/<experiment>/run-plan.json --approve <exact-reviewed-run-id> --work-root C:/ExperimentWorkers
   ```

   The exact ID protects against approving a different plan. The controller
   commits/pushes an immutable approval receipt, authenticates remote durability,
   and only then enters scientific work. Approval does not change run identity.
   Workspaces remain outside any checkout on a trusted local disk. Workers never
   publish. A publication failure stops before scientific entry and preserves
   local state for reconciliation; no automatic push or scientific retry occurs.
4. Inspect progress and eventually review Stage D (Gate 2):

   ```text
   uv run python -m experiments.orchestration status experiments/<experiment>/run-plan.json
   uv run python -m experiments.orchestration verify-approval experiments/<experiment>/run-plan.json
   uv run python -m experiments.orchestration status <run-id>
   uv run python -m experiments.orchestration verify <run-id>
   uv run python -m experiments.orchestration resume <run-id> --work-root C:/ExperimentWorkers
   ```

   Plan-address status works before a run exists: PLANNED or authenticated
   APPROVED. Run status reconstructs RUNNING/interrupted, COMPLETE-candidate and
   DEAD/BLOCKED from scientific receipts; verify authenticates completed results.
   Operational progress/streams/PIDs remain ignored and non-authoritative.
   An already-durable approval can be used with `run <plan> --work-root ...`
   without `--approve`; approval publication is never overwritten. An approved
   never-entered run starts this way. An unapproved plan has nothing scientific
   to resume. Entered failures retain the existing dead-attempt semantics.

The [live visibility and preservation record](engineering/observability/README.md)
documents the blocked source-grounding run and operational reporting contract.
Its old approval is historical-only after implementation changes. Replacement
prospective checkpoints require separate maintainer review and new exact-run
approval. Do not manufacture scientific authority from a synthetic test fixture.

Normal execution flushes lifecycle events to stderr and leaves final JSON on
stdout. Use `status <run-id> --follow` for a read-only live viewer, or add `--json`
for JSONL. Ctrl-C detaches the viewer only. A 15-second heartbeat reports continued
supervisor observation, not useful model progress. Full child logs flush during
execution; failures immediately show diagnostics, identities and absolute log
paths. Historical status authenticates original bindings even after code upgrades.

## Callable contract and ownership

```python
controller = await Controller.from_plan(repository, committed_plan_address, work_root)
preview = controller.plan_report()  # no approval required; grants no authority
# Only a trusted host may deliver a pre-existing explicit maintainer grant:
authorization = await controller.approve(host_supplied_approval_request)
# After restart: authenticate the existing immutable approval, without minting one.
authorization = await controller.execution_authorization()
result = await controller.run(authorization)  # bare run() rejects, even after approval
status = await controller.verify()
```

`Controller`, `RunPlan`, `ApprovalRequest` and `ExecutionAuthorization` form the
narrow experiment-owned callable seam. A future Agent may validate/report freely;
its Tool must receive a host-issued authority value and must not expose grant
construction or `approve` as an ungoverned model capability. The trusted host
verifies the maintainer identity and decision. The CLI's explicit `--approve`
action is that boundary for human operators. Principal/reference fields retain
that decision, rather than treating model text or successful validation as approval.

This is not an OS/cryptographic authorization framework: arbitrary trusted Python
or a process with repository push credentials cannot be distinguished from a human
by this package. Do not grant an untrusted Agent unrestricted CLI/Git/approval
access. Mechanical checks require both the explicit API value and the committed,
unchanged, exact-run receipt before entry. There is no new universal governance
registry, Tool wrapper, Agent loop or production orchestration API.

The [adapter contract](CONTRACT.md) specifies declarative metadata and exact
transport. The original [engineering report](engineering/REPORT.md) records validation,
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

The current [host-disclosure boundary](engineering/host_disclosure/README.md)
supersedes the filesystem-interacting launcher described historically below.
Models return schema-constrained judgments and exact-content locators through
stdin/final-message transport; the host derives canonical spans, writes artifacts
and executes builders. A compatible successful real synthetic runtime receipt is
required before real-case semantic entry. The default console is compact; detailed
events remain retained and available with `--verbose-events` or on failure.

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

## Authority contract correction

The [authority correction record](engineering/authority/README.md) owns current
plan/approval validation evidence. The original engineering manifest and report
remain byte-identical historical records at commit
`c26d8efaf89ec8bcbe999be23a103e233016a801`; their original source hashes describe
that implementation, not the corrected current implementation. Legacy v1 plans
remain readable; old Boolean approval receipts cannot authorize v2 execution.
Historical adoption of 0017-0019 is independent and requires no retroactive receipt.

## Prospective completed-branch and capacity bindings

A v2 plan may explicitly bind a committed prospective compatibility statement for
an immutable completed branch. It names the unchanged origin seal, original and
prospective scientific-contract byte maps, and the reviewed unchanged scientific
semantics claim. This is visible prospective authority, never a fabricated old
publication. The source-grounding adapter additionally proves its limited capture
change by AST comparison. Existing seals and original usage are not rewritten.

Plans can name exact path/hash pairs for preserved historical run journal JSON
files. Those files may remain untracked; changed bytes or unrelated untracked
files still reject authentication. This does not waive index/worktree checks.
An explicit closed list of adapter-specific primary artifacts travels unchanged
through C publication and import, alongside the existing canonical primary set.

The output-capacity receipt complements the large-input receipt. It certifies a
measured lower bound for the exact pinned semantic-worker profile, not a provider
maximum. The output-only synthetic probe demonstrates 63357 canonical bytes with
complete five-field usage, no tools and unchanged isolated CWD. Its authority is
engineering evidence only; scientific approval remains separate.
