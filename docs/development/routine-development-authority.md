# Standing routine-development authority

The operator explicitly requested this prospective authority mechanism on
2026-11-02. It belongs to repository administration, `WorkCycle.routine` in
`scripts/backlog/routine/`. It reuses Intake's canonical coordinator, exclusive
writer, bounded reader and immutable receipts. It is not framework governance,
a scheduler, an Agent hierarchy, a provider registry or another coding loop.
Legacy Qwen delegations and historical manual approvals retain their meanings.

## Operator control

Activation is a genuine, default-No operator decision about the **complete
policy**, not approval inferred from a task or an unanswered prompt:

```text
uv run python -m scripts.backlog routine-activate --policy <policy.json> --reference <actual-operator-decision>
uv run python -m scripts.backlog routine-show
uv run python -m scripts.backlog routine-deny --subject B-0052 --reference <operator-stop>
uv run python -m scripts.backlog routine-revoke --reference <operator-stop>
```

Activate a reviewed replacement policy through the same command to modify it.
There is no `--yes` bypass. Trusted API hosts may supply an authenticated actual
operator decision callback instead of the terminal. A model cannot activate or
expand its own policy. Policy itself has no inactivity or wall-clock expiry.
Replacement and revocation invalidate earlier policy-derived authority at the
next admission boundary. Explicit subject denials survive policy replacement;
proposal and published-task aliases are checked together.
This first contract does not silently clear denials; exceptional manual handling
remains separate.

`backlog-routine-control-v1` records form an immutable ordered hash chain in
canonical `.local/backlog/routine/`. The active activation record's SHA256 is
the policy version. Preserve these local records across sessions; copying them
to another checkout does not transfer authority. Root and current OS principal
must match. As with existing grants, local hashes establish correspondence,
not signatures or protection from a hostile principal controlling the host.

## Policy scope and escalation

The [v3 local-work amendment](routine-local-work.md) adds bounded calibration,
role/memory/playbook evaluation, source research, diagnostics and supervisor
delegation through this same owner. Once explicitly activated, it derives fresh
exact grants automatically; routine packets no longer need individual `+approve`
responses. Historical experiment approvals remain historical. Native candidate
acceptance, custody and Integration requirements below remain authoritative.

The closed `routine-development-policy-v1` contains categories, edit/read roots,
allowed operations and profiles, a pinned local provider, coding/review limits,
output limits, individual grant lifetime, Git constraints and the unchanged
protected validation contract. Source addresses retain existing repository
validation. Each coding task still repairs one existing Python implementation;
the native task validator, fixed checks and private acceptance remain owners.

Routine operations include Intake review/publication, native coding and bounded
repair, qualified diagnostic/acceptance review, **trusted host assessment**,
read-only integration planning and permission assessment for routine commits
and non-force main publication. Existing owners perform those operations.

Each operation requires a trusted supervisor's explicit engineering assessment
and provenance. Task labels, retrieval scores, passing tests or valid model JSON
do not establish routine classification or correctness. Major architecture,
security, destructive effects, secret access, paid services/spending, persistent
service changes and validation relaxation always require human escalation.
Policy cannot delegate edits to authority, execution, model, Tool, persistence or
command-execution owners through a broad source root. Unassessed work, provider
drift, unavailable/busy capacity and exceeded limits fail closed.

The first contract permits only the pinned loopback provider, ordinary commit
assessment and `push origin main`; force, rewritten history, protected exceptions,
model-authored shell and Git publication engines are absent. Permission receipts
bind HEAD, index identity, changed paths and the validation reference. They do
not execute Git or certify validation. The trusted existing development
workflow must authenticate protections and required final protected inputs.
Native candidate installation, integration execution, publication and backlog
closeout are **not** added by this policy. Their existing separate contracts
remain authoritative. Provider reservation is the trusted host's bounded serial
use of an authenticated idle service, with runtime availability checks; it is
not an exclusive lock over unrelated external clients or permission to restart.

## Per-task authority and audit

The [coding-continuation amendment](coding-continuation.md) adds a versioned
finite total-attempt ceiling, initially two including the original. Existing
policies retain one slot. Each eligible prospective child receives a fresh exact
grant through the same owner; consumed dispatches are never replayed or renewed.

The policy supplies existing owners' callbacks; it does not replace their grants:

```python
grant = await cycle.routine.authorize_native(
    version, item, assessment=host_assessment, provider=qualified_runtime,
)
result = await cycle.native.execute(
    item, interaction=selected_model, profile=approved_profile,
    authorize=cycle.routine.callback(grant["reference"]),
    measure_input=actual_token_measurement, provider_context_tokens=actual_capacity,
)
```

`authorize_reviewer`, `intake_review`, `host_review` and `plan` similarly compose
their existing owners. Selection and preparation are still host responsibilities;
there is no automatic task picker or unbounded continuation loop. Provider
qualification is a trusted-host observation of the actual configured adapter,
artifact/image, health, idle state and capacity, not evidence supplied by a model.
Runtime consumers must recheck actual service state before model entry.

When planning from the destination branch, `plan` uses the existing Checkout
owner for a zero-edit visit to the assignment's exact branch/base and restores
the administrative branch. It preserves the integration owner's distinct-branch
rule and creates no second checkout or installation authority.

Every `backlog-routine-decision-v1` binds the exact owner request, task/subject,
assessment, provider qualification, finite expiry and policy version. Existing
grant `reference` fields carry
`routine-v1:<policy-version-sha256>:<decision-sha256>`. Existing grant schemas and
old readers remain compatible; no historical record gains new authority.
Native/reviewer authority checks reauthenticate this link before governed effects.
Integration candidate admission also checks policy-derived host decisions.

Individual grants retain expiry and native budgets. Expired decisions cannot
be reused. Issue just before execution; consumed or uncertain dispatches are
never replayed, refunded or silently replaced. This first contract does not renew
an already written expired one-slot authorization. Reconciliation of such a slot
requires the existing owner rather than overwriting its history. Revocation
cannot undo a call already entered; known source restoration remains mandatory.

An eligible [acceptance-review continuation](native-review-continuation.md) may
receive a fresh policy-derived grant for its explicit new subject. This is a
separate bounded attempt, not renewal of the old grant or replay of its dispatch.
The closed v3 continuation similarly uses a fresh exact-subject grant after
authentication of the v2 budget interruption; its single prospective allowance
does not alter policy ceilings or permit another attempt after v3 is consumed.
Use `authorize_reviewer(..., attempt=subject_sha256)` and
`host_review(..., attempt=subject_sha256)`. The existing acceptance-review and
host-review operations, profile/resource ceilings and escalation remain unchanged.

Successful public/private acceptance still precedes acceptance-review entry.
Independent actors and sessions, private-oracle exclusion, grounded findings,
closed conclusion validation and separately reasoned host disposition remain
required. Diagnostic findings cannot promote blocked candidates. A favorable
model recommendation never approves itself.

## B-0052 and validation

B-0052's Intake approval, frozen checks and prepared unused dispatch remain intact.
The old pending interactive prompt is not a grant. After genuine standing-policy
activation, a fresh policy-derived grant may be issued if the current assignment,
provider and supervisor assessment qualify. No acceptance criteria may change
merely to obtain a successful result.

Maintained tests use tiny authored repositories and neutral scripted models to
exercise policy-derived grants, actual native edit/check/repair, independent
acceptance review, host disposition and authenticated integration planning.
They establish authority mechanics, not live-model competence. Changed executable
administration still requires the final protected development gate with 100%
configured production line/branch coverage before publication.
