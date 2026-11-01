# Governed diagnostic review of blocked native candidates

`WorkCycle.native.diagnostic_reviewer` independently investigates an authenticated
unsuccessful native candidate. It is a second explicit administrative purpose of
the existing bounded [review operation](native-independent-review.md), not a new
Agent hierarchy, coding loop, integration pathway or Evidence database.

Acceptance review still requires a qualified `REVIEW_CANDIDATE`, successful public
and private acceptance, known effects and released custody. Its gate, original
schemas, manual decision path and integration readers are unchanged. Diagnostic
v1 accepts a released **BLOCKED native result** with an authenticated candidate
archive. It produces attributed findings, not an acceptance recommendation.
Successful candidates and legacy Qwen results are outside this historical reader.

## Operator entry and separate authority

```text
uv run python -m scripts.backlog native-diagnostic-prepare B-0050 --archive <exact-candidate.json> --policy <review-policy.json>
uv run python -m scripts.backlog native-diagnostic-authorize B-0050 --reference <operator-decision> --expires <ISO-time>
uv run python -m scripts.backlog native-diagnostic-proposal B-0050
```

A trusted configured host injects a real supported ModelInteraction into
`await cycle.native.diagnostic_reviewer.execute(item, interaction=model,
profile=approved_profile, authorize=current_host_decision)`. Preparation does not
dispatch. The existing default-No confirmation applies to authorization; a fresh
grant and current host dispatch consent bind the actual subject, actor/session,
profile, source/Tool scope, finite budgets, principal and expiry. Original coding
grants and acceptance-review grants confer no diagnostic authority.

There is one non-replayable `diagnostic-reviewer/` slot under the existing native
work-item folder. It does not reuse or replace the consumed coding slot or the
acceptance `reviewer/` slot. Prospective records are
`backlog-native-diagnostic-{subject,authorization,dispatch,proposal}-v1`, written by
the existing immutable WorkCycle writer. Observations reuse
`backlog-native-observation-v1` and bounded native Capture. An intent precedes
entry; uncertain completion or failed proposal persistence never authorizes replay.

The policy reuses the existing review actor's closed fields and ceilings. A fresh
session, distinct coder/reviewer actor and host independence attestations remain
mandatory. Same model weights and different labels do not prove judgment diversity.
No paid fallback, service switch or automatic model retry follows from failure.

## Exact historical evidence and current Context

The host explicitly supplies a canonical resource containing the exact escaped
`source_text` and `native_patch_text`, with their recorded hashes. B-0050 uses
`docs/research/code-audit/live-native64-20261101/unaccepted-candidate.json`.
Display `.py.txt`/`.diff.txt` copies may undergo Git newline normalization and are
not candidate authority. The reader verifies the archived UTF-8 bytes against the
terminal candidate hash, the patch against an exact baseline-to-candidate diff,
and original native source/patch bytes when present. Missing local duplicate
copies are disclosed; the exact content-authenticated archive remains required.

The reader authenticates original assignment/packet/baseline identity, historical
authorization/dispatch/result/execution bindings, observation hashes and the
Checkout release. Historical expiry does not erase the observation or create new
authority. No historical result is converted into a passing candidate. Missing or
tampered core authentication refuses preparation, rather than manufacturing facts.

The subject discloses original task/obligations, baseline and Git identity,
candidate/diff, actual edit intent/completion facts, public check history including
failures/truncation qualifications, terminal disposition, custody and acknowledged
or unresolved effects. Missing historical test materializations and unselected or
changed current inputs receive explicit status. Public success is limited evidence.
Private acceptance may be failed or not executed; neither is promoted to a pass.

Private implementation, counterexamples, expected results, private diagnostic
output, host controls and worker reasoning/conversation are withheld. Private
acceptance exposes only qualified outcome, exit status, elapsed time and input
currentness, when executed. The original result identity also binds withheld data.
The reviewer receives no reference repair. A failed outcome alone does not reveal
the hidden cause. Diagnostic findings must not be scored as blind discovery when
their facts were already disclosed in public evidence.

Current source is independently selected and identity-bound under fresh read-only
authority. It may include relevant dependencies beyond the old coding inventory.
It is not silently relabeled as historical source. The candidate is never installed
for review. Source changes after preparation invalidate the subject; an active
Checkout owner blocks entry. Absent historical temporary tests need not be recreated
or added to original authority merely to read current dependencies.

The operation reuses SourceScope, SourceSearchIndex, scoped source/navigation Tools,
Context range materialization and native call correlation. It advertises only
`read_source`, `find_source` and `read_source_unit`. Search results are versioned
metadata, not disclosed source or proof that a region was assessed. Exact reads
retain current provenance, physical boundaries and source identities. Each bounded
source/navigation operation consumes the existing read allowance; duplicate native
call identities are refused. Only one Tool operation is admitted per response.
No edits, checks, arbitrary shell or Git Tools exist.

## Findings and trusted evaluation

The closed model conclusion uses `schema: native-diagnostic-conclusion-v1`,
`scope: diagnostic-only`, exact `candidate_sha256`, `disposition` (`findings`,
`insufficient-evidence`, `refused`), `summary`, `evidence`, `findings`,
`outstanding` and `requests`. Each finding labels its claim `observed`, `inference`
or `uncertain`, with supporting evidence references and optional attributed
physical-line locations. Locations and labels are model claims; syntactic and
reference validation is not host verification that they are correct.

Malformed output, invalid references/identity, output limits, unauthorized Tools,
exhaustion, capture failure and provider uncertainty produce a blocked proposal or
propagated persistence failure. A truthful inability/refusal is representable and
does not force a fictitious defect. Unsupported semantic findings may be retained
as attributed claims for independent host evaluation, not certified as truth.

There is no diagnostic acceptance decision. `admit` and `decide` explicitly refuse
this purpose. Native integration readers still require their original native
review/result schemas and acceptance gate. “Approved” in model prose cannot change
the blocked result, issue an install grant or authorize publication/closeout.

The trusted supervisor records usefulness, unsupported/incorrect claims and blind
discovery separately, bound to the exact proposal. That evaluation is evidence,
not native candidate acceptance. Suggested validation or engineering work returns
to the supervisor and requires its own authority; no review-driven repair loop is
launched. B-0043 and the original failed tasks remain open.

The B-0051 sampler-setting gap remains recorded in its
[original outcome](../research/native-scope-followup.md). No sampler pass-through,
server-default change or attribution of failure to temperature is introduced here.
