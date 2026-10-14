# Prospective plan v2 and immutable execution approval v1

A plan is declarative orchestration metadata. The scientific question, obligations,
labels, treatment, adjudication instructions, joins and gates belong to the
approved Stage A/packet, not controller code. Plans are canonical sorted ASCII JSON
with a final newline. `RunPlan.parse()` rejects unknown top-level fields, missing
stages, unbounded concurrency, duplicate case IDs/disclosures and automatic retry.

Required fields:

| Field | Contract |
|---|---|
| `schema` | `experiment-controller-plan-v2` |
| `name`, `attempt` | Administrative name; explicit positive attempt number |
| `stage_a` | `checkpoint` (full immutable Git OID, reachable from the approved main checkpoint); `protocol` and `integrity`, each `{path, sha256}` at that commit |
| `cases` | Ordered `{id, frame, inputs}`; frame includes `repository_id`, `snapshot_id`, `corpus_id`, `parent_tree`; inputs are `{path, name, sha256}` Stage A Git blobs |
| `commands` | Nonempty direct argv for `prepare`, `prepare_validate`, `packet`, `packet_validate`, `B`, `B_validate`, `C_validate`, `import`, `import_validate`, `D`, `D_validate` |
| `semantic` | `kind: codex` or `process`; model display designation, reasoning, packet `prompt_file`, environment allowlist; Codex also needs frozen `model_id`, `cli_version: 0.162.1`, optional executable/auth_file; process needs frozen direct `argv` |
| `publication` | `root` under experiments, `remote`, `branch: main`, Boolean `push`, and subjects for `PACKET`, `B`, `C`, `D` |
| `validation` | Nonempty lists of direct argv at `local`, `checkpoint`, `final`; mandatory protected and supported-source checks are appended independently; include active adapter static checks here |
| `concurrency` | Positive integer `cases`, `semantic`, `workers`; shared workers bounds all stage processes |
| `timeouts` | Positive seconds `worker`, `validation`, `grace` |
| `retry` | Exactly `NEVER_SCIENTIFIC` |
| `controller_implementation` | Complete `controller.implementation()` digest map frozen before approval |
| `implementation` | Explicit adapter repository path -> committed exact SHA-256; include all transitive derivation/validator dependencies |
| `cache` | `enabled`, `observation_semantics`, `configuration`, `surfaces`; only pure deterministic preparation qualifies |

## Prospective validation and authority

The scientific Stage A commit precedes the plan commit. `Controller.from_plan`
authenticates canonical committed plan bytes, the exact reachable Stage A
protocol/integrity, case disclosures and pinned implementations. The v2 plan must
have a separate commit from its Stage A checkpoint. It never reads or creates
approval to establish plan validity. `plan_report()` reports PLAN_VALID and no
execution authority, including the prospective run ID, cases, models, fixed
branch dependencies and publication/validation policy.

A v2 plan has no `approval` field or mutable approval status. Run identity remains
SHA-256 of canonical prospective plan plus complete controller implementation map.
Timestamps and subsequent approval are excluded. Approval cannot select a new
attempt, alter scientific semantics or revive an entered failed operation.

An explicit `ApprovalRequest(run_id, principal, reference, kind)` carries a
maintainer decision delivered by the trusted CLI/host. `approve(request)` requires
freshly validated clean synchronized main, an exact matching run ID, and no
existing approval/run. It publishes once under:

```text
<publication.root>/<run-id>/authorization/approval.json
<publication.root>/<run-id>/authorization/publications/APPROVAL.json
```

The canonical approval JSON has exactly:

| Field | Meaning |
|---|---|
| `schema` | `experiment-execution-approval-v1` |
| `plan_sha256`, `run_id` | Exact immutable prospective plan and run |
| `stage_a_checkpoint` | Exact scientific Stage A commit |
| `controller_sha256` | SHA-256 of canonical complete controller implementation map |
| `plan_path`, `plan_checkpoint` | Committed prospective plan address and latest owning commit |
| `review_checkpoint` | Clean synchronized main authenticated for explicit approval |
| `authority` | Exact `kind` (MAINTAINER_CLI or TRUSTED_HOST), nonempty `principal`, `reference`, `action: EXECUTE_EXACT_RUN_ONCE` |
| `approved_at` | Canonical UTC Timestamp; audit metadata, not scientific identity |
| `sha256` | SHA-256 of canonical approval excluding this field |

The publication receipt separately binds the complete approval artifact hash and
actual Git parent. The commit subject is `Approve experiment run <first-12-run-id>`.
With push policy enabled, push and clean local/origin/actual-remote agreement must
succeed before authorization is returned. A local commit with failed push remains
NOT_AUTHORIZED; retain it and reconcile explicitly. No rollback/retry occurs.

`execution_authorization()` authenticates this immutable single-publication
history, exact committed/current bytes, prospective bindings, source versions,
Stage A and synchronized repository, then returns `ExecutionAuthorization` with
run ID, plan hash, full approval hash and approval commit. It creates nothing.
`run(authorization)` requires that value and reauthenticates it under the writer
lease before any scientific ENTERED event. Mere `run()` is insufficient even on
an approved controller. Resume authenticates the same receipt and immutable run
context; existing failed/ambiguous attempts remain dead.

Normal CLI: `plan <plan>` validates without authority; `run <plan> --approve
<exact-run-id> --work-root <external-root>` is the explicit one-command maintainer
action; `verify-approval <plan>` authenticates authority; `verify <run-id>`
authenticates scientific completion. `status <plan>` covers PLANNED/APPROVED before
entry; `status <run-id>` covers the scientific lifecycle. Approval is separate
from the PACKET/B/C/D scientific checkpoints and does not add a human gate.

The host must authenticate the authority decision. These experiment-local Python
values and Git receipts are not protection against malicious arbitrary Python or
an untrusted process granted repository credentials. Future Agent exposure must
not grant approval issuance to model proposals. Existing governance/Tool docs
establish no universal authorization substrate; none is invented here.

`approved-experiment-controller-v1` remains parseable with its old `approval`
locator, preserving canonical legacy identity. Legacy Boolean receipts are not
accepted for new execution; they cannot be implicitly migrated. The original
engineering records remain authoritative at their original commit. Read-only
adoption of historical 0017-0019 remains independent of this flow.

`push: false` remains an explicitly frozen isolated/offline-fixture policy. Normal
live plans require `push: true`. No synthetic approval grants scientific authority.

## Stage transport

Commands are direct argv without a shell. Only fixed named tokens are replaced:
`{python}`, `{repository}`, `{workspace}`, `{case}`, `{stage}`, `{frame}` (JSON),
`{run_id}`, `{packet_commit}`, `{stage_b_commit}`, `{gold_commit}`. Literal JSON
braces remain unchanged. Pass tokens as distinct argv where appropriate; no shell
quoting/interpolation is performed. Frozen trusted code may execute from the
repository; its **data inputs** come only from that stage's external workspace.
It must not use checkout discovery, other-case/gold/treatment side reads or write
main. The environment is the explicit allowlist, not the controller's full process
environment. Do not put credentials in argv.

Preparation receives only its case's disclosed Stage A blobs. Packet construction
receives prepared bytes. The packet builder must produce the approved blind file
set and a standalone validator. `packet_validate` runs inside the case's sterile
workspace immediately before C, and must authenticate the original scientific
packet including frame, resources, obligations and immutable instruction content.
B receives prepared bytes and the frozen packet checkpoint token. C receives only
its own packet. Import receives `primary/<seven files>` and `packet/<packet files>`.
D receives `B/<case>/<files>` and `C/<case>/<files>` in prospective case order, plus
the committed B/C checkpoint tokens. Its transport envelope uses the first case
as administrative owner; its scientific analyzer must validate **all** case frames
and joins. This is not permission to treat the cohort as one scientific frame.

Every non-C operation writes `candidate.json`, exactly:

```json
{
  "schema": "experiment-candidate-v1",
  "case": "<case ID>",
  "frame": {"<exact keys>": "<exact values>"},
  "stage": "<prepare|packet|B|import|D>",
  "files": {"<relative scientific artifact>": "<SHA-256>"}
}
```

The file list is explicit, nonempty, content-authenticated and confined. Unknown
scratch files are never imported. `.local`, `.scratch`, bytecode, Git metadata,
links, reparse points and restricted population paths are rejected. Output
ownership is limited to the run publication prefix. Source and target scientific
schemas remain adapter-owned. A final immutable controller summary and publication
receipts supplement, rather than replace, stage-specific validation/integrity.

Validators are separate processes, exit zero, emit a final JSON line with
`status: PASS`, and must perform exact deterministic replay where scientifically
required. They must refuse malformed identities, content or duplicate/missing
joins. B validation additionally returns `mode: SEALED`,
`native_archives_decoded: 0`, `deep_correspondence_executions: 0`, and the exact
`completion_proof_sha256` matching `completion_proof.json`. It authenticates the
capture-time deep proof without scientific retrieval or RI reacquisition.
Import validation returns `semantic_transformation: NONE`; the controller separately
requires every `primary/<file>` byte to match the original primary.

## Primary worker outputs

Exactly these scientific artifacts are collected:

```text
stage_c_review.json
stage_c_statistics.json
STAGE_C_REVIEW.md
stage_c_validation.json
stage_c_hashes.json
stage_c_method.md
stage_c_builder.py
```

The frozen C validator must execute the primary's deterministic verification
command in a separate process, authenticate hash manifests, preserve all packet
bytes, validate every cell/unit/witness under the packet contract and return the
normalized receipt below. This is an adapter responsibility because historical
primary builder CLIs and semantic schemas differ. It must not fix labels or
reconcile reviewers. The controller invokes the validator in a separate process,
then independently checks expected files, exact packet preservation, known
forbidden JSON keys and normalized blindness/designation evidence.

Receipt fields: `status`, `model`, `reasoning`, `second_reviewer: false`,
`reconciliation: false`, `host_routing_independently_verified` (false is a recorded
limitation; true requires `routing_evidence_sha256`), and `blindness` with every key
below present and false:

```text
repository git_history parent_siblings prior_session web queries ranks_scores
annotations references_treatment pairs timings graph_ppr_rrf other_cases child
prior_gold confirmation_reserve
```

These are normalized behavioral attestation categories, not a claim that filesystem
isolation independently proves every category. Provider-specific extra restrictions
belong in the prospective packet and validator. Host routing is not introspected.
The real Codex adapter uses no conversation continuation and separate CODEX_HOME
per case. Its auth file must be an authentication-only JSON artifact, not a session
or configuration directory. An operational final answer never supplies gold.

## Cache and publication adaptation

Only explicitly serialized preparation bytes qualify for cache. The producer and
validator must support their representation. Native Python objects, mutable live
working-copy state and treatment execution are ineligible. A cache hit is verified
again under the exact frame/config/implementation binding; invalid entries
recompute preparation. Cached files cannot replace disclosed Stage A inputs.

PACKET publishes prepared bytes under `PREPARATION/<case>` and packets under
`PACKET/<case>`. B and C publish under their boundary/case directories, retaining
primary bytes in `C/<case>/primary`. D publishes one cohort package and deterministic
`controller_summary.json`. All immutable journals and the approved run context
are committed with boundaries. Future adapters may retain existing scientific
formats inside those run-owned packages; no canonical label projection is invented
by the controller.

Completed Cases 0017-0019 use the legacy owners and can be audited with
`uv run python -m experiments.orchestration adopt`. That runs only existing normal
sealed/published verification. Their original B-before-packet dependency is not
rewritten. This compatibility audit does not make them controller executions or
retroactively change their protocol. New protocol adapters must explicitly support
the independent packet/B construction contract before the single-command workflow
is authorized.

Scientific paths are rejected before any Git blob read. Operational `.local`,
`.scratch` and bytecode directories are forbidden at every artifact-path depth.
Source/target receipt output sets must exactly equal their published manifests;
publication receipts bind the actual Git parent, and the final summary seals every
returned operation receipt. Status distinguishes uncommitted candidates from
verified final publication and retains non-authoritative live progress.

Run-owned scientific artifacts use `-text -whitespace` publication attributes:
raw CRLF/trailing-space data must not be normalized or rejected as code style.
Artifact hashes, expected ownership and deterministic validators remain mandatory.
The controller package itself retains whitespace checking with CR-at-EOL support.

## Operational observation contract

The [operational guide](engineering/observability/README.md) owns live event fields,
15-second heartbeat semantics, stream retention and read-only follow behavior.
UTC launch/exit observations and monotonic durations are persisted explicitly.
Default events use stderr; final execution JSON remains stdout. Full child streams
are mirrored before bounded event-queue loss; canonical capture bounds and failure
policy remain unchanged. Model/prompt content is never printed by lifecycle events.

An adapter may append JSONL `operational.log` in its outer B workspace to expose
the nested grounding process. Only `observation.PROCESS_FIELDS` are forwarded;
the role must be `source grounding`. This is an experiment-specific operational
bridge, not a scientific input, completion proof, authority receipt, retry decision
or framework Event/Trace/Telemetry substrate. It remains outside sterile reviewer
inputs and scientific candidate sets. The maintained adapter pins its implementation
through Stage A; bridge observations never alter scientific inputs or outputs.

Implementation static validation uses explicit maintained file ownership in all
tiers. Run payloads, imported primaries and generated builders retain their
scientific schema/hash/replay checks and are excluded from source lint/type/style
discovery. The mandatory FINAL controller/production floor remains required.
