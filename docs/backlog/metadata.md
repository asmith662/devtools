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
programmatic consumer is `Intake(Path.cwd()).capture(payload)`, then `get(id)`,
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
