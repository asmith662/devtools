# Standing authority for bounded local work

The activated [reviewer-provider enrollment](reviewer-provider-enrollment.md)
adds explicit per-profile providers and reasoning budgets through a separately
approved v4 amendment. Query current activation; this v3 history does not itself
authorize an alternate service or expand a historical grant.

Activated through the existing operator-control owner after the actual
`+activate` decision and protected pass on 2026-11-05. The activation version is
`26b93f4ae7ca8dcfbf228f62dd0ffa4ea94057cf953e529e2f7db61e27f46978`;
the policy digest is
`7a2b7e6265f2f73a9b8e0a12e006596bcd6a0ba4013fecfbe25d03786032e479`.
The [delivery receipt](../research/code-audit/routine-local-authority-20261105.json)
preserves the operator decision, exact control, historical hashes and two real
zero-inference automatic grants. Future runs must query current policy rather
than assume this historical activation remains unrevoked.

This operator-requested amendment extends `WorkCycle.routine`, not framework
governance. The reviewed [v3 policy](routine-local-policy.json) adds local
calibration, public-source research, role evaluation, working-memory/playbook
experiments and development diagnostics. Its activation uses the same explicit
default-No operator control as [routine development](routine-development-authority.md).
The implementation alone does not activate it. After one genuine activation,
eligible grants and bounded delegations require no per-run human prompt.

Earlier research and executed packets retain their recorded approval conditions.
For new eligible packets, derive fresh standing-policy grants instead of
repeating an older research document's prospective operator-approval procedure.
Do not reuse historical grants or silently broaden a frozen experiment.

## Grant and execution boundaries

`cycle.routine.local.authorize(version, scope, assessment=..., provider=...)`
issues a fresh existing `backlog-routine-decision-v1` and `routine-v1:` reference.
Scope binds the existing engineering subject, frozen plan hash, canonical
Repository identity and exact public source content identities, actor, role,
profile, callable names, fixed-check definition hashes and finite budgets.
There is no new task database, Attempt abstraction, scheduler or provider registry.
v1/v2 policies, prior grants and historical experiments remain readable and
unchanged; they do not acquire new authority. Replacement invalidates old
policy-derived authority at its next admission boundary.

For a host-frozen scope and request, the existing composition is:

```python
version = cycle.routine.active()["sha256"]
grant = await cycle.routine.local.authorize(
    version, scope, assessment=host_assessment, provider=qualified_provider,
)
response = await cycle.routine.local.interact(
    grant["reference"], request, interaction=selected_interaction,
    qualify=observe_current_provider, measure=measure_actual_input,
)
```

Neither callback asks for interactive consent. The scope's actor must match the
selected interaction's source. Measurement/provider qualification are trusted
host callbacks over the actual selected adapter, not worker declarations.

Trusted supervisors supply semantic classification and provenance. Models
cannot invoke the authorizer through the allowed read-only Tools or declare
their output authorized. Major architecture, security, destructive effects,
secrets, paid services, persistent serving changes and validation relaxation
still escalate. Broad roots do not authorize bulk disclosure: every run names
exact resources, excludes private oracle material, and the supervisor selects
the actual role-specific Context. `.local/backlog/` is excluded from local
model-read authority. Historical candidate evidence is never current source or
installation authority merely because it was read.

Source admission reuses `SourceScope` and RI observations, including alias
refusal, bounded source reads, source identities and snapshot correspondence.
Reauthentication occurs before each governed entry. Grant expiry, wall time,
revocation, subject denials and source drift fail closed. The trusted host must
qualify the actual adapter/provider before each model call; a worker's claim
of health or model identity is not qualification.

`local.interact(reference, request, interaction=..., qualify=..., measure=...)`
wraps **one existing ModelInteraction**, not an agent loop. It measures actual
input tokens, binds the request/actor, checks allowed callable names and output
reservation, consumes an immutable entry before model invocation, applies the
call/wall deadlines and records the response or ambiguous failure. Portable and
adapter-owned sampling settings remain in the captured request. Response delivery
does not establish factual correctness, acceptance or publication authority.

For existing source/check owners, `local.enter(reference, operation, payload)`
admits an exact `read`, fixed `check`, or evidence capture; `local.complete`
records the observed result. It does not execute a shell or Tool. A read needs
an explicitly granted path/bound; a check needs its exact frozen definition hash.
Existing effect owners remain responsible for executing the bound definition,
enforcing its timeout, source custody and recording full native/wire evidence
where applicable. Generated Tool descriptions never become executed actions.

Consumed entries form an ordered hash chain beneath the existing routine owner.
Missing or failed completions stop further effects under that grant. Failed,
cancelled and unknown entries remain consumed; no retry/refund or automatic
reconciliation is introduced. Observed results can still be preserved after
revocation, without creating fresh execution authority. Hosts must not issue a
new grant merely to replay an uncertain operation.
A completed check's ordinary nonzero validation exit is a known returned
observation; it does not authorize installation or waive validation.

The amended policy ceilings are 16 model calls, 32,768 input tokens/call,
2,048 output tokens/call, 32,768 total reserved output tokens, 32 source reads,
16 fixed checks, four delegated grants and 4 MiB capture. Calls have a 120-second
ceiling; each grant and operation has at most 10,800 seconds. Actual plans must
select smaller exact budgets. Input plus output reservation must fit the pinned
64K provider. Output reservations are spent even when actual output is shorter;
available budgets cannot be multiplied by delegation. Protected development
validation and its configured coverage gate remain mandatory for changed
production executable inputs.

## Delegation

The trusted supervisor calls the same `authorize(..., parent=reference)`.
Child grants preserve the subject, plan, Repository, purpose and provider/profile;
they may select only a parent-permitted role and subsets of resources, Tools,
fixed checks and further roles. Every budget must fit the parent's bounds and
remaining account. Issuance permanently reserves the child's finite counters
from the parent, including descendant delegation allowance; it inherits the
parent expiry and rechecks parent authority. Failed child issuance does not
refund a consumed reservation. A child cannot mint authority or widen a scope.

This permits supervisor-controlled handoff through existing model-neutral
interfaces. It does not implement automatic actor selection or launch workers.
Native coding edits still use native exact-task grants, Checkout restoration
and consumed-attempt limits. Local coding-role evaluation is read-only; this
amendment does not install candidates or bypass independent acceptance,
Integration, protected publication or backlog disposition.

## Codex CLI is a separate boundary

Read-only inspection found CLI **0.166.0**, a trusted canonical project entry
and Windows `sandbox = "elevated"`. User configuration supplies no explicit
approval policy or sandbox mode; there is no repository `.codex/config.toml`.
The active session nevertheless enforces workspace-write filesystem boundaries
and restricted network access. Devtools policy cannot override those controls.
No user or project Codex configuration is changed by this amendment.

The installed CLI supports `codex exec --approve-for-me`, which routes approval
requests through automatic review while retaining the workspace-write sandbox.
That is the practical trusted-workspace choice when routine Git, cache or
network operations sometimes need an escalation. Automatic review uses additional
Codex review calls and may deny an action; it does not supply Devtools authority.
See [OpenAI sandbox and approvals documentation](https://learn.chatgpt.com/docs/agent-approvals-security).

For strictly noninteractive runs with prearranged filesystem/network access:

```powershell
codex exec -C C:/Users/recoveryadmin/Workspace/tools/devtools `
  --sandbox workspace-write -c 'approval_policy="never"' '<bounded task>'
```

`never` suppresses interactive approval but does not authorize sandbox escape;
blocked operations must be prepared or handled separately. Keep credentials
outside model Context, use a repository-local `UV_CACHE_DIR` where practical,
and provision only necessary cache paths and network destinations. Do not use
the approvals-and-sandbox bypass. Managed requirements can further constrain
settings. The [official configuration reference](https://learn.chatgpt.com/docs/config-file/config-reference)
documents these independent controls. Config recommendations do not expand
Devtools task authority or authorize paid/external inference.

## Verification and historical preservation

Deterministic fixtures exercise fresh automatic grants, actual simulated
ModelInteraction entry, exact request budgets, revoked/expired authority,
source drift, unknown-effect refusal, fixed checks and parent budget carve-outs.
They distinguish authority mechanics from live model quality. This amendment
runs no live inference and does not rewrite calibration approvals or outcomes.

Implementation `f17745601605290d05503f3f53902fcd67edabdb` passed the protected
profile once: **4,444 tests passed, two opt-in live tests skipped, 100% production
branch coverage**, with unchanged executable inputs. The managed run took
4,550.74 seconds under a 7,200-second deadline. All 51 routine-authority tests
were included; focused development also passed 50 owner tests and 21 targeted
delegation/resource checks. Strict mypy checked 643 files; maintained-source
Ruff/format, layout and diff checks passed. Thirteen preexisting routine records
were preserved byte-for-byte. No persistent provider, Inspector or Codex CLI
configuration changes were made.
