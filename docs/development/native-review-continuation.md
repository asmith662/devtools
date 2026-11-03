# Bounded acceptance-review continuation

`WorkCycle.native.reviewer` now supports one prospective continuation of an
authenticated qualified candidate whose original acceptance review stopped at
the established legacy single-read batch barrier. This is repository
administration under the existing reviewer, not a generic Attempt hierarchy,
retry engine, scheduler or new Evidence store. The engineering task, coding
assignment, consumed coding dispatch and immutable candidate remain unchanged.

## Identities and records

| Identity | Owner and binding |
| --- | --- |
| Engineering task | Existing reviewed Intake item; no replacement obligation |
| Coding assignment/dispatch | Original native v1 records, never redispatched |
| Candidate | Exact archived source SHA256, diff and qualified native result |
| Original review subject/attempt | Existing `reviewer/` v1 records, immutable |
| Continuation subject/attempt | `reviewer/continuation/subject.json`, version 2; its sealed hash selects this attempt |
| Execution authority and dispatch | Separate v2 authorization and one immutable v2 dispatch for that exact subject |
| Model recommendation | v2 proposal binding subject, grant, dispatch, raw observations and candidate |
| Trusted host disposition | Native review v2 record explicitly naming the subject and proposal |
| Integration plan | Existing owner; exact accepted host-review hash plus explicit continuation-subject hash |

Version 2 has one fixed continuation slot. The prospective version 3 allowance
below adds one content-addressed subject, not an open-ended numbered registry.
Creating it uses the existing exclusive administrative writer and directory
claim; concurrent or duplicate preparation fails. Persistence failure does not
refund the slot. Legacy v1 subjects/readers and manual review retain their
meanings. No reader selects the latest or most favorable proposal.

## Supported preparation and selection

```python
packet = await cycle.native.reviewer.prepare_continuation(
    item,
    previous=original_blocked_proposal_sha256,
    reviewer=fresh_review_policy,
    correction_reference=authenticated_correction_reference,
)
actor = cycle.native.reviewer.select(packet["sha256"])
grant = await cycle.routine.authorize_reviewer(
    active_policy_version, item, attempt=packet["sha256"],
    assessment=trusted_scope_assessment, provider=current_provider_qualification,
)
proposal = await actor.execute(
    item, interaction=fresh_model_interaction, profile=approved_profile,
    authorize=cycle.routine.callback(grant["reference"]),
)
```

Preparation confers no ModelInteraction or Tool authority. A valid active standing
policy may authorize the exact new subject using its existing `acceptance-review`
operation, permitted profile/scope and finite ceilings. The packet includes the
prior subject, authorization, dispatch and terminal proposal identities and the
trusted correction reference. Those fields are part of the policy-derived
decision; the model cannot authorize or alter them. Policy is not broadened and
there is no per-task human prompt for an eligible operation.

Existing manual CLI authority remains default-No:

```text
uv run python -m scripts.backlog native-review-continue <item> --previous <original-proposal-sha256> --policy <fresh-policy.json> --correction <correction-reference>
uv run python -m scripts.backlog native-review-authorize <item> --attempt <subject-sha256> --reference <host-decision> --expires <ISO-time>
uv run python -m scripts.backlog native-review-proposal <item> --attempt <subject-sha256>
uv run python -m scripts.backlog native-review-decide <item> --attempt <subject-sha256> --proposal <proposal-sha256> --decision accept --reference <host-decision> --rationale <independent-assessment>
```

Omitting `attempt` selects the legacy path. A continuation hash never selects an
arbitrary directory. Diagnostic review cannot create or select this continuation.

## Closed eligibility

Version 2 initially permits only the proven legacy failure:
`PermissionError: Review permits one bounded read per response`. The original
proposal must be blocked, with no conclusion or host disposition, one completed
model request/response, zero reads and exactly the corresponding two captured
observations. The returned response must be a normally terminated Tool proposal
with distinct read-only call IDs and authorized source paths within the original
total read allowance. Source, profile, grant/dispatch links, request subject,
settings, Tools and historical authority timing must authenticate.

There is no qualifying transition from a substantive acceptance, rejection,
insufficient-evidence judgment, missing return, unknown effect, entered read or
arbitrary error string. The new source/check inputs, configuration, private
qualification, custody and original candidate must satisfy existing currentness
rules. The freshly constructed candidate subject must equal the original one.
The new reviewer session must differ from the old session and remain independent
of implementation and private oracle/reference access.

The historical grant may now be expired: that does not erase its valid known
completion, and it supplies no new authority. New grants retain finite expiry,
model/read/output/capture/time budgets and policy revocation/denial checks.
An expired new grant cannot be reused or silently renewed. The continuation
cannot itself create another continuation, even after an infrastructure failure.
Additional failure families or another allowance require explicit prospective
contract work, not approval shopping or a caller-supplied retry reason.

## Prospective recovery of the v2 budget interruption

The operator authorized one additional attempt against the existing B-0052
qualified candidate after its authenticated v2 acquisition-budget interruption.
Version 3 supports exactly that failure grammar: two returned model requests,
two completed authorized reads, then a two-read batch refused before entry with
one acquisition remaining, no structured conclusion and no native host judgment.
All nine historical observations, content identities, source/settings/Tool scope,
grant/dispatch/proposal links, timing and completed-read references authenticate.
Missing returns, partial or unknown effects, changed candidate, substantive
judgment and a v3 predecessor are ineligible. Earlier reads remain historical
completions; the new session receives the ordinary independent subject.

Pass `attempt=<v2-subject-sha256>` alongside the exact previous proposal to
`prepare_continuation`, or `--attempt` to `native-review-continue`. Preparation
claims `reviewer/attempts/<new-subject-sha256>/` under the exclusive writer.
Subject, authorization, dispatch and proposal use v3 schemas. A nonempty attempt
directory consumes the finite allowance even if later persistence fails.
No second v3 subject or continuation of v3 is permitted. V1/v2 records remain
immutable; explicit selectors also bind existing host and integration readers.

New acceptance subjects include the shared completion policy: remaining-budget
visibility, one reserved synthesis call and correlated recovery of known
zero-entry refusals within the same approved limits. The final call exposes no
source Tools. Capacity failure, authority/currentness loss and ambiguous effects
remain terminal. This policy is prospective and does not rewrite historical
subjects or refund consumed dispatches. Fresh standing-policy authorization is
required for the new exact subject; preparation alone grants no effects.

## Host and integration consumers

The host supplies the exact attempt to `cycle.routine.host_review(...,
attempt=subject_sha256, proposal=proposal_sha256, ...)`. The native owner verifies
the actual final response, evidence references and candidate; the host separately
assesses factual claims. V2 host records require an explicit subject and model
proposal. V1 records cannot silently carry a continuation selector. Accepted
candidate readers reauthenticate both the selected attempt and exact standing
host-decision scope; changing a selector or recommendation cannot reuse a grant.

The existing read-only plan binds that exact host record and subject. Downstream
integration context checks preserve the binding. A structurally valid proposal
is not a correct diagnosis or host acceptance. Diagnostic, incomplete, stale,
adverse or source-tampered evidence cannot authorize integration. No new
installation, publication, parent closeout or reviewer-driven repair authority
is granted.

## Qualification and confidentiality

Existing `NativeMaintenance.validate`, candidate authentication and review subject
projection remain authoritative. Missing temporary public inputs may be restored
from their exact authenticated frozen preparation archive through existing
filesystem preparation, then rechecked by the native owner. Expectations and the
candidate are not edited. Historical validation is not relabeled fresh, and
matching declared inputs is not a new global coverage claim.

A fresh model conversation contains the approved task, baseline/candidate/diff,
qualified public/private outcomes and authorized read-only source. It does not
inherit coder conversation, the earlier review transcript, private oracle
implementation or hidden host scoring. Session separation does not establish
model-weight diversity. Actual review quality must be evaluated separately from
scripted lifecycle tests, schema admission and passing candidate tests.
