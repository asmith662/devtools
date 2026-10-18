# Backlog Metadata

## Required identity and lifecycle fields

Each record has id, type, title, status, and decision_maturity. Unknown values
must be written as explicit uncertainty, not guessed.

| Field | Controlled values |
| --- | --- |
| type | EPIC, STORY, INVESTIGATION |
| status | BACKLOG, BLOCKED, DEFERRED, ACTIVE, IMPLEMENTED, VALIDATED, SUPERSEDED, CLOSED |
| decision_maturity | DISCOVERED, NEEDS_INVESTIGATION, SEMANTICS_PARTIAL, READY_FOR_DESIGN, READY_FOR_IMPLEMENTATION |
| necessity | REQUIRED, OPTIONAL, EXPLORATORY, FUTURE_REQUIRED |
| architectural_significance | FOUNDATIONAL, STRUCTURAL, SUPPORTING, HARNESS_LOCAL, PROVIDER_LOCAL |
| urgency | NOW, SOON, DEFERRED |
| validation_level | NONE, UNIT, INTEGRATION, LIVE_SINGLE_HARNESS, LIVE_MULTI_HARNESS |

Status describes lifecycle selection; decision_maturity describes how well the
semantics are understood. They are intentionally independent.

## Architectural ownership

Each canonical record also identifies one `primary_domain` and, when needed,
`supporting_domains`.

- **Primary domain** owns the architectural pressure and is accountable for
  its eventual semantic boundary.
- **Supporting domains** participate in the concern without taking ownership
  of that boundary.
- Use `supporting_domains: none` when no secondary domain participates.
- `experiments` is permitted as a primary domain only for non-reusable
  composition whose semantics have not been promoted into `src/devtools/`.

Allowed reusable domains are `core`, `resources`, `models`, `agents`,
`context`, `tools`, `execution`, `orchestration`, `governance`,
`observability`, `persistence`, and `evaluation`.

`documentation` is a narrow non-reusable administrative owner for records
about the repository's authoritative documentation itself. It is not a
thirteenth framework domain. `experiments` is the corresponding non-reusable
owner for unpromoted composition.

Cross-domain participation never removes the need for a primary owner. The
field describes architectural ownership, not current Python package location.

## Split lineage and semantic decisions

When a record is decomposed, the original record remains canonical historical
lineage. It uses `status: SUPERSEDED`, names `split_children`, and explains the
scope that was separated. Each surviving child uses `split_from: B-XXXX`.

`semantic_decision: RESOLVED` records that an investigation's terminology or
ownership question is answered by authoritative architecture. It does not
authorize implementation. A resolved decision can therefore remain
`status: DEFERRED` while its reusable implementation lacks a consumer.

## Evidence, scope, dependencies, and risk

Records preserve these independent dimensions when meaningful. Unknown values
are written explicitly as `unknown`, rather than inferred merely to complete a
template:

    evidence_basis
    scope
    consumers
    hard_dependencies
    pressure_dependencies
    operational_dependencies
    blocked_by
    risk_if_deferred
    risk_if_implemented_early
    established_invariants
    unresolved_semantics
    promotion_trigger
    validation_level
    live_validation_trigger
    first_harness_consumer
    second_harness_trigger

Evidence basis may name RESEARCH, REPOSITORY, REAL_USE, or MULTIPLE; it is
descriptive rather than a score.

## Promotion discipline

Promotion requires sufficient evidence that a semantic boundary is stable
independently of an experimental or local implementation. Useful evidence may
include independent consumers, heterogeneous repeated use, multiple
architectural pressures converging on the same boundary, demonstrated reuse
without experiment-specific assumptions, or requirements that cannot remain
cleanly local. No universal consumer count automatically authorizes promotion.

Dependency meanings are distinct:

- **Hard prerequisite:** the dependent work cannot responsibly proceed first.
- **Pressure dependency:** concepts are related, but the relationship is not
  frozen.
- **Operational prerequisite:** needed for an implementation or experiment,
  not conceptually foundational.

## Record body

Every epic or item records problem/value, evidence, consumers, invariants,
prerequisites/dependencies, unresolved semantics, risks, promotion trigger,
validation expectations, and related records. Investigations must not invent
final acceptance criteria before their semantics are known.

## Governed proposal intake (repository administration)

`uv run python -m scripts.backlog` administers this existing Markdown backlog.
It is the initial governed intake boundary, not a framework work lifecycle,
Agent supervisor, authorization service or second backlog database. Source
ownership is `scripts/backlog`; installed `devtools` does not import it. It reuses
Core identities/time/resolved paths and filesystem bounded reads/atomic writes.

Proposals live in `docs/backlog/proposals/<host-assigned UUID>/proposal.json`.
They do not receive a B-number until an authorized review approves a precise
canonical publication. Required input fields are:

- `kind`: bug, enhancement, refactor or investigation.
- `title`, `summary`, `benefit`, `uncertainty`: explicit bounded text.
- `discovery`: human/tool/agent/research `kind` and original `reference`.
- `parent`: existing work reference or null; it does not change that work.
- `resources`, `evidence`, `dependencies`: reference lists; evidence is required.
  Dependencies remain possible relations, never inferred hard prerequisites.

Payloads are limited to 64 KiB serialized JSON; stored records must fit the
1 MiB bounded reader. Unknown authority/configuration fields are rejected. References are provenance,
not instructions, commands or automatically disclosed Context. Discovery-source
attribution is a provenance claim and never authenticates a human reviewer. No target code,
active task, Git branch or model service is changed by capture/review.

### Operator commands

Run from the repository root (or use global `--root <checkout>`). Relative input
paths resolve against the caller's current working directory.

```powershell
uv run python -m scripts.backlog capture proposal-input.json
uv run python -m scripts.backlog list --pending
uv run python -m scripts.backlog show <proposal-id>
uv run python -m scripts.backlog review <proposal-id> --decision ADVISORY --advisor Codex --reference <advice-provenance> --rationale <advice> --duplicates <disposition>
uv run python -m scripts.backlog review <proposal-id> --decision APPROVED --domain resources --reference <human-decision-provenance> --rationale <reason> --duplicates <disposition>
uv run python -m scripts.backlog promote <proposal-id>
```

Default output is structured JSON, including pending/error dispositions. The
read-only consumer is `Intake(Path.cwd())`; a trusted host binds mutations with
`Intake(root, coordinator=await locate(root))`, then `capture(payload)`, `get(id)`,
`queue()`, `duplicates(id)`, `review(...)` and `promote(...)`. The same bounded
schema is used by humans, deterministic tools and future agents.

### Review and authority

New proposals are `PENDING_REVIEW`. `ADVISORY` appends attributed advice without
changing review state. `DEFERRED` keeps history and permits later review;
`REJECTED` is terminal. `APPROVED` is terminal review of exact backlog inclusion
bytes, not execution selection. A rejected/approved concern requiring a new
scope needs a new related proposal; original history is never erased.

Non-advisory decisions require a separately supplied trusted-host authorization
callback; absent/negative authorization fails closed. The callback receives the
complete original proposal, exact decision, reviewer/reference, duplicate
candidates/disposition, scope and proposed Markdown/index publication. Untrusted
proposal data cannot provide this callback. Host integrations must authenticate
and scope their own reviewer delegation; an agent/model response is not a grant.

The local CLI's trusted host is an actual interactive operator console. It
attributes non-advisory decisions to the current OS account, shows the exact
request and defaults confirmation to No. Noninteractive authority/publication
is refused; there is no `--yes` or agent-approval bypass. OS account attribution
and operator-supplied provenance are not remote identity certification. This
boundary assumes trusted repository tooling, terminal and filesystem access.

Codex advisory output remains advisory unless the host has explicit delegated
authority. Approval/publication here grants **canonical backlog inclusion only**.
It does not grant implementation, Qwen/model invocation, protected Git publication
or scientific execution authority; existing governance remains separate.

Duplicate candidates use title-token Jaccard overlap >= 0.5 or shared affected
resource references, across proposals and canonical items/epics. This is a
review aid with incomplete recall, not semantic equivalence or automatic merging.
Every review preserves candidates and an explicit reviewer disposition.

### Canonical publication, integrity and recovery

`backlog-proposal-v1` retains the original payload and its SHA-256. Append-only
`review-NNNN.json` files use `backlog-review-v1`, bind the original proposal, and
chain exact prior review hashes. Readers validate identity/schema/hash/order;
checksums detect corruption, not cryptographic human authority. Git review and
trusted-host access remain the publication boundary. No mutable latest index or
independent authoritative backlog database is introduced.

An approved review reserves the next unused B-number under one checkout-local
writer lease and records exact Markdown/index bytes. Promotion rechecks host
authority, writes the ordinary `items/B-xxxx-<title>.md` and inserts its row into
`overview.md`'s existing table. The record retains proposal/review links, begins
`BACKLOG / DISCOVERED`, leaves unresolved metadata explicit, and carries
`execution_authorization: NONE`. Later canonical backlog edits remain normal
repository work, never edits to historical approval bytes.

Individual writes use canonical atomic replacement; item plus index are not a
multi-file transaction. If interrupted, inspect the approved receipt and existing
Git diff, then explicitly re-run promotion under fresh host confirmation: equal
existing content is retained and only the missing publication is completed.
Conflicting item/index content is never overwritten. This re-observation does
not reserve or execute engineering/scientific work.

Malformed/missing records remain visible as queue errors; repair from verified
Git/history or reconcile explicitly, never silently reset them. Sibling atomic
writer `.tmp` files are not canonical records. Concurrent writer contention or a
crash leaving `proposals/.writer/` fails closed without retry. An operator must
verify no active writer and inspect incomplete files before removing a stale
empty lease. This follows the existing exclusive-directory local-writer pattern;
there is no cross-worktree/distributed lock. Git conflicts between separate
checkouts require normal explicit reconciliation. Filesystem power-loss limits
remain those documented by the canonical atomic writer.

### First real discovery

Proposal `f47f3925-6988-4d84-81f4-c5b97a571484` captures the still-reproducing
Python 3.12 `JsonObjectFile` constructor incompatibility. The
[reproduction record](proposals/python312-reproduction.json) preserves source
identity, existing interpreter, exact constructor and error. A Codex advisory
review recommends maintainer triage; it remains **PENDING_REVIEW**, with no
human approval, B-number, implementation or Qwen invocation. Related B-0009
pressure is retained without duplicating it as an accepted item.

## Governed backlog-to-Qwen cycle

`scripts/backlog/work.py` connects one intake-approved, published canonical
B-number to the existing `CodingTask` and `run_coding_task` consumer. It owns
scope binding and work receipts; retrieval, Context, edit admission, isolated
application, tests, feedback repair and provider accounting remain in the Qwen
worker. This is repository-local composition, not reusable Orchestration, an
Agent API, a scheduler or another task/backlog representation.

### Designated coordinator

Exactly one checkout is designated in the repository's shared local Git config,
`devtools.backlogCoordinator`. All administrative CLI writes resolve that value
through Git's own common-directory interfaces. A first designation uses:

```powershell
uv run python -m scripts.backlog designate
```

This genuine terminal decision defaults to No and authorizes administration
only. Existing different/multiple designations are refused. This increment
selected the existing `qwen-context-worker` feature checkout as coordinator;
no implementation authority was granted. Relocation is a later explicit host
administrative reconciliation, never an automatic fallback.

An unbound `Intake(root)` is now read-only. Trusted programmatic hosts must
resolve `coordinator.locate(root)` before binding the existing synchronous Intake
API; coordinator binding is host capability, never model data. The CLI refuses
mutations from linked feature worktrees. `WorkCycle` rechecks shared designation
for every mutation. Linked feature worktrees share Git objects/configuration but
never independently publish canonical backlog state. Existing local writer leases
serialize coordinator writes; no cross-node/distributed locking is introduced.

### Preparation and separate implementation authority

The host supplies an existing `CodingTask` (or its exact `dataclasses.asdict`
JSON representation), target checkout and expected branch. There is no new task
DSL, command registry or model-originated configuration. The oracle field is
host-owned executable validation code; it must be reviewed as such before any
implementation grant, and is never disclosed as a solution to Qwen.

Preparation requires one approved review plus a published `BACKLOG` item/index
row, actual review/proposal provenance and the current canonical item content.
Pending proposals, advisory-only reviews, missing publication and ambiguous
bindings are refused. Legacy hand-authored items without intake approval
provenance are also refused; do not fabricate a duplicate B-number to bypass
that requirement. Supporting another review provenance requires explicit later
host integration. The one editable file must be an affected resource of the
reviewed proposal. Targets must be clean, separate feature worktrees of the same
Git repository, at the exact supplied `CodingTask.baseline_revision`, with matching
source/test hashes. Caller data cannot substitute an old task baseline under a
new HEAD. The branch, objective, one-file scope, Context choices, oracle/tests,
source identities and existing model/time/action limits are frozen together.

The subsequent implementation grant is separate: exact assignment digest,
principal, real decision reference, issue time, expiry and implementation-only
scope. A trusted-host callback must authenticate this request. The CLI displays
it, uses the actual local OS principal and genuine default-No confirmation.
Noninteractive execution and self-approved model data are refused. This is a
trusted local-host boundary, not remote identity certification or a new general
approval service. Backlog approval and a stored grant receipt alone never suffice.

Immediately before dispatch, the bridge revalidates current coordinator,
backlog/review/status, source/branch/base, exact scope, grant and current host
consent. It rechecks after a potentially long terminal prompt. Grant expiry is
an admission deadline for the whole bounded worker run, not a new per-model-turn
reservation engine. Current host refusal/revocation stops admission. Bounds stay
at three proposals/model calls, one native edit per call, 4,096 output tokens per
call, 300 seconds per call, 900 seconds total and the existing local 32K profile;
smaller task limits remain supported. There is no paid fallback or model shell,
Git, direct-write or protected-publication capability.

```powershell
uv run python -m scripts.backlog work-prepare B-xxxx --target <absolute-feature-worktree> --branch <feature-branch> --task-definition <host-task.json>
uv run python -m scripts.backlog work-authorize B-xxxx --reference <actual-human-decision-reference> --expires <explicit-UTC-expiry>
uv run python -m scripts.backlog work-execute B-xxxx
uv run python -m scripts.backlog work-status B-xxxx
uv run python -m scripts.backlog work-discover B-xxxx <discovery-input.json>
```

All commands run at the coordinator (or with global `--root` selecting it).
Preparation is non-executing. Authorization and execution have distinct terminal
gates; this engineering assignment grants neither for a real item. A task JSON
can be produced by a trusted caller from its existing `CodingTask`; no arbitrary
model-generated command strings are accepted.

### Work evidence, review and conservative stopping

Operational receipts live under coordinator `.local/backlog/work/B-xxxx/`;
the B-number remains the work identity. `assignment.json`, `authorization.json`,
`dispatch.json` and `result.json` bind exact content hashes. Existing worker
receipts remain under `worker/`, with the original request/response/stage logs,
source hashes, full validation evidence, final source and resource observations.
`candidate.patch` describes the consolidated isolated edit against frozen source;
no target checkout change is applied. No mutable parallel backlog state is added.

There is one assignment/dispatch slot per B-number in this first increment.
Duplicate preparation or a durable prior dispatch never blindly launches another
operation. A crash/cancellation after claim gives `RECONCILIATION_REQUIRED`, with
usage UNKNOWN until established from existing worker evidence. Do not delete the
claim or invent a replacement identity to retry. Reconciliation/reassignment
requires deliberate host review; generic resume and automatic retry are absent.
Missing/corrupt receipts fail visibly. Existing atomic writer and local lease
recovery limitations continue to apply.

The result references work/grant identity, branch/base, allowed and actual candidate
files, frozen/final source hashes and diff, tests/oracle, usage, validation/worker
and bridge elapsed time, repair cycles, worker disposition and uncertainties.
An accepted worker output becomes `REVIEW_CANDIDATE`, never integrated code or
canonical completion. A failed/unknown outcome becomes `ESCALATION_REQUIRED`;
unknown consumption is not zero. The host's recommendation is explicitly advisory,
not a performed Codex review or protected publication grant. Canonical status is
not automatically changed to ACTIVE/CLOSED. A later reviewer must authenticate
the candidate/evidence and obtain integration authority separately.

`WorkCycle.discover(item, payload)` forwards a supervisory/worker observation to
`Intake.capture`, attaches the parent B-number and frozen assignment reference,
and preserves original discovery/evidence. It creates only PENDING_REVIEW work,
without altering objective, authority, limits or active source. Qwen still has
only `propose_edit`; this increment does not add a new model Tool.

The Python 3.12 proposal is now approved and published as B-0048. Its object-only
assignment is prepared, with execution authorization NONE. Deterministic acceptance uses explicitly synthetic
approval/grants and temporary Git fixtures, exercising the real worker path;
it does not establish a new live Qwen success.

### Standing routine-Qwen delegation

The same coordinator and WorkCycle support an optional standing local-host grant.
This is repository administration under `scripts/backlog/delegation.py`, not a
framework policy service. Existing manual `work-authorize` and `work-execute`
retain their independent genuine default-No terminal gates. Proposal review and
backlog promotion retain their existing gates; delegation cannot promote work.

Issue/revocation require the actual local OS principal and real terminal consent.
The CLI has no `--yes` switch. Trusted host callers may attest Codex supervisory
decisions under an active grant; worker/model text has no such API or Tool.
This is the existing local trust boundary, **not cryptographic authentication of
Codex or protection against a malicious process with coordinator write access**.
Do not feed arbitrary model output into the administrative CLI.
The worker's disposable workspace isolates source changes, not operating-system
privileges. This increment does not sandbox arbitrary Python executed by tests
or make adversarial generated code safe; existing host/OS controls and supervisory
scope assessment remain necessary. No credential or financial operation is
permitted by this delegation.

The closed policy names exact source/test paths, reviewed proposal categories,
SHA-256 identities of host-owned acceptance code, per-task calls/output/time/edit
limits and cumulative task/call/output/time allowances. Pinning acceptance code
is required because CodingTask oracles are executable host code. Scientific,
financial, credential, grant-expansion and protected-publication effects are
prohibited. Consequential execution/governance/model/agent infrastructure paths
are excluded from routine edit scope. Only clean separate feature worktrees of
the same repository, exact baselines and independently approved backlog items
can qualify. Low risk remains a mandatory Codex supervisory judgment, not a
classification inferred from task text or a guarantee about arbitrary code.

The grant also pins `qwen38-local`, loopback port 8080 and the existing complete
Qwen3.8 IQ4_XS/32K profile. Profile readiness/fingerprint checks occur before
inference. Authority is checked again before every initial/repair call. Revoking
a grant stops subsequent admission/calls; it cannot undo or forcibly cancel an
already dispatched external invocation. Existing worker timeouts still apply.

Records are immutable and content-hashed beneath `.local/backlog/delegations/`;
the existing Intake atomic writer and coordinator lease serialize reservations,
revocation and dispatch claims. An exact pre-dispatch `APPROVE_ROUTINE` record
binds Codex review to the assignment and delegation. `work-delegate` then writes
the existing per-assignment authorization plus a worst-case reservation. A valid
delegated authorization makes `work-execute` noninteractive; it uses the same
worker, isolation and closeout. It does not bypass OS or Codex execution controls.

Every reservation consumes the task's maximum calls, calls multiplied by output
allowance, and wall-time allowance. There are no refunds or automatic retries,
including crashes between reservation/authorization and unknown call outcomes.
Incomplete/corrupt records fail closed and require manual reconciliation. No
input-token, monetary or subscription quota is implied. Output/time values are
request/host admission bounds, not hard provider consumption guarantees. Missing
usage remains unknown. An observed provider output overrun blocks that grant
and forces escalation while retaining the response. Cached/reasoning categories
remain the existing worker's separate overlapping observations.

After execution, existing result/diff/test/usage/repair/branch/base evidence plus
the original objective is available for review. `work-review --result-sha256`
records `ACCEPT_RECOMMENDED`, `REWORK_RECOMMENDED`, `ESCALATE` or `REJECT`, with
reviewer, rationale and provenance. Failed results cannot be recommended as
accepted. These records confer no commit, integration, merge or backlog-close
authority. Rework is a bounded recommendation; completed/ambiguous assignments
cannot be reset or redispatched by this increment. Up to two test-feedback
repairs already occur inside the reserved worker run.

#### Proposed initial policy and one-time operator action

[`routine-qwen-policy.example.json`](routine-qwen-policy.example.json) is an
**inactive example**, not authority. It covers only object.py bug/refactor work,
the existing JSON tests and the prepared B-0048 oracle. Per task: three calls,
4,096 output tokens per call, 900 seconds, three one-file proposals. Cumulative:
three tasks, nine calls, 36,864 requested output tokens and 2,700 reserved seconds.
Each call retains the worker's 300-second timeout. It does not cover the sibling
JsonListFile/CsvFile compatibility defects or arbitrary new acceptance commands.
New host validation code requires explicit policy review and a newly issued grant.

From the designated coordinator, inspect applicability without granting anything:

```powershell
uv run --python C:/Python314/python.exe python -m scripts.backlog delegation-check B-0048 --policy docs/backlog/routine-qwen-policy.example.json
```

To activate **only after deciding this policy and expiry are suitable**, run this
single line directly in PowerShell. It prints the exact grant and defaults No;
the seven-day expiration is computed when the operator runs it:

```powershell
uv run --python C:/Python314/python.exe python -m scripts.backlog delegation-issue --policy docs/backlog/routine-qwen-policy.example.json --reference 'Maintainer standing decision: routine local Qwen object-model maintenance under the displayed policy; no protected publication' --expires ([DateTimeOffset]::UtcNow.AddDays(7).ToString('o'))
```

Keep the returned delegation SHA. Codex can then review the exact assignment,
record that decision, reserve and dispatch without further terminal consent:

```text
uv run python -m scripts.backlog work-review B-0048 --delegation <grant-sha> --decision APPROVE_ROUTINE --reference <actual-supervisory-decision> --rationale <scope-and-risk-assessment>
uv run python -m scripts.backlog work-delegate B-0048 --delegation <grant-sha> --supervision <review-sha>
uv run python -m scripts.backlog work-execute B-0048
uv run python -m scripts.backlog work-review B-0048 --delegation <grant-sha> --decision ACCEPT_RECOMMENDED --result-sha256 <result-sha> --reference <actual-result-review> --rationale <evidence-based-assessment>
```

Revocation uses the same genuine default-No interactive host boundary:

```text
uv run python -m scripts.backlog delegation-revoke <grant-sha> --reference <actual-revocation-decision>
```

No real grant or supervisory approval is issued by implementing this capability.
The prepared B-0048 assignment and its pinned execution baseline remain intact;
administrative authority is consumed by the coordinator, not imported into the
authenticated implementation target. No new target revision is required merely
to use this repository-local administrative feature.
