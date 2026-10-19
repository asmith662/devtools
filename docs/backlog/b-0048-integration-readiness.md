# B-0048 object-slice integration readiness

> Operational pause after canonical-checkout consolidation: these implemented
> WorkCycle/integration paths still require or create additional checkouts.
> They must not execute under the current one-checkout policy. Existing grants
> and plans retain obsolete path bindings and are not transferred. Only
> read-only history inspection is supported until the concrete compatibility
> gap in docs/development/reconciliation.md is resolved. No new grant is issued.


## Actual state

The development-integration implementation is available through the existing
[WorkCycle contract](integration.md). B-0048 itself remains **BLOCKED pending
separate integration authority**, with no installation, feature publication or
target promotion. The coding delegation does not cover these actions.

Authenticated inputs:

- Assignment: `179531289e28506c6a87508990a7d7aa0d14c76263d098c2a50ae099e659e298`.
- Accepted Qwen candidate: `9b31553ec9982cba4886eaed39e6ddb0941598b57d3d0442771083f2fd4fd88f`.
- Codex accepted-result review: `23a5dcbedbb4f6980068a8fc29ae94d1e436cc3a7078f585bb762fcb2cdc95ae`.
- Existing result: `0067bd485eef310d112b1e1f9b0bc85925075f48eb1fe01b1157e69a57e095fe`.
- Original implementation baseline: `75cc74f7acda36cf91e91251efae8f9b3054f02a`.
- Intended destination / merge base: `main`, `92250292dacfb8289d129063d5523dd87b63162b`.
- Read-only integration plan: `076684241ee2f23bb4de0d10fcaefed1519d0fee1c5ef28037fd2d02c1ac5857`.

The source baseline has ten commits beyond main, including retrieval, Qwen and
backlog work. The coordinator also has later delegation/review changes. Neither
branch is safe to merge wholesale into main for this correction. The plan
excludes those ten source commits and creates a destination-based commit with
only the exact reviewed object.py bytes plus one independently authored test
file. No replacement implementation was authored here.

## Planned independent tests

The proposed permanent path is
`tests/resources/filesystem/test_json_object_compatibility.py`.
Its prepared source SHA-256 is
`5a0856cf13f4eb3b317518dfe90c1cbd5b6acffdd25666f658e11c9447e5938a`.
Codex authored these tests independently; they are not attributed to Qwen.
They cover direct construction from nested mutable input, alias isolation,
immutable mapping storage, metadata/search and transformations, inherited field
validation and rejection of a non-object root. Ruff/formatting and strict mypy
of the prepared test source pass. They are still planned additions, not installed
maintained tests or fresh integration-validation evidence.

The existing JSON suite and pinned independent oracle remain unchanged. The
oracle covers Python 3.12.13 and the Python 3.14 host. Integration must run it,
the focused suites, static checks and the protected development gate against
the actual destination-based tree, then obtain a new exact-tree Codex review.
Historical candidate acceptance cannot substitute for these integration gates.

## Operational evidence and next action

The designated coordinator's existing local work folder contains the immutable
plan at `.local/backlog/work/B-0048/integration/<plan-sha>/plan.json` and a
content-hashed admission refusal. Preparation inputs, proposed test source and
the read-only assessment are under `.local/backlog/integration-validation/`:
`B-0048-spec.json`, `test_json_object_compatibility.py`, `B-0048-admission.json`.
No actual integration grant is installed. The old coding-grant identity is
correctly refused by the separate integration-authority loader.

The next operator decision is whether to issue the exact inactive
[`integration-policy.example.json`](integration-policy.example.json), with an
appropriate expiry and genuine decision reference. That policy covers only
this object-model source, named tests/oracle and main destination; it forbids
source corrections and parent closure. Main promotion also needs a genuine
repository protected-destination policy decision. The issuance/protection and
subsequent supervised stage commands are documented in the integration contract.
No such decision is inferred from this engineering assignment.

Once authority is genuinely issued, Codex can install, validate, review, publish,
promote, verify and record the slice without repeated human task confirmation.
An advanced destination or changed source requires a new explicit plan/review;
it must not overwrite this frozen plan. **JsonListFile and CsvFile Python 3.12
defects remain unresolved**, so the planned completion disposition is
`SLICE_ONLY`, with B-0048 left BACKLOG.
