# Acceptance read batches and B-0052 continuation boundary

This increment corrects the acceptance reviewer's read-only Tool batching. It
does not repeat B-0052 coding, reinterpret its blocked review, or install its
candidate. The [existing review owner](../development/native-independent-review.md)
retains candidate qualification, closed conclusions, host disposition and
integration separation. The [standing authority](../development/routine-development-authority.md)
remains active and unchanged.

## Authenticated observations

Starting local and remote main were both
`aa1e9529c7dd8ce37e01b6eaf8e77cc60a5d7fc2`. Inspector was independently registered
on `feat/agent-inspector`. The unchanged Qwen provider reported healthy, idle,
one actual 65,536-token slot. No model inference or service mutation was needed
to establish the administrative boundary.

B-0052's original result is `REVIEW_CANDIDATE`:
`f1971ed020430afcf064e88f9cacb193ce1f0a900233759ac78aa66788d2eed2`.
The exact archived candidate SHA256 remains
`a7471ffeec9a21cdb12ddc3bcb0cb315680f109ff70d168ade03310c24bef255`;
the patch SHA256 is
`385da31f1b570482b187d89c5c63f6b8474fd68d45fda197b6c17b6b31ca9b04`.
Its original 54 public passes and successful frozen private acceptance remain
historical observations, not a new execution. Source is the restored baseline.
The temporary public task file is no longer materialized in the working tree;
its exact frozen archive is preserved. No fresh current review subject or fresh
acceptance result is claimed.

The original review observation
`53b838703666782203e3649bfe256d004bf8c72d22213ea9ce89586a0f20fda6`
contains two `read_source` calls: the maintained CSV row tests and the frozen
public checks. Both were authorized paths. The hardcoded one-call check refused
the batch before entry: one model call, zero reads, three total read acquisitions
still unused. This was an implementation simplification, not acquisition-budget
exhaustion or a transactional safety guarantee. The actual proposal
`4e0b440d370b65187eb2d121cac6a542f888681bcb149be3b3ffb7fc36c4efca`
remains blocked, without a conclusion or host approval.

## Narrow correction

`scripts/backlog/native/review/acquisition.py` owns acceptance-only batch
preflight and ordered acquisition beneath the existing actor. It reuses native
argument materialization, `SourceScope`, the existing search index, Context
`SourceRangeDisclosureOption`, `ScopedSourceTool`, ToolRunner and Capture.
No new scheduler, source parser, effect protocol or database is introduced.

Every read is validated before any read Tool enters. Unique fresh IDs, the
total acquisition allowance, exact current scope/ranges, complete next request
and conservative capture reservations are checked together. Results remain
individually correlated. Later operational uncertainty does not erase earlier
completion; there is no automatic replay. Invalid or oversized batches are
recorded as unentered and terminate safely. Diagnostic batching and coding Tool
semantics remain unchanged. Passing structural admission does not establish
review correctness or host acceptance.

## Why no live continuation occurred

The current reviewer explicitly owns **one non-replayable slot per native
assignment**. `folder` selects `<item>/reviewer/`; `prepare` creates it exactly
once, and immutable `dispatch.json` claims that slot. There is no second subject
ID, attempt selector, or downstream reader branch for another acceptance review.
`WorkCycle.routine.authorize_reviewer` independently refuses an existing dispatch
with `Consumed review slot cannot replay`, before producing a new policy decision.

The active standing policy was consulted through that owner. No interactive
prompt was introduced, no grant was fabricated, and the policy was not expanded.
No new model request, reviewer finding, host acceptance or integration plan was
produced. No coding task or feature branch was created to evade this constraint.
This is an administrative capability boundary, not a model refusal or provider
failure. The user's instruction explicitly requires stopping before live
inference when another subject is prohibited.

The smallest subsequent increment is a prospective, bounded acceptance-review
continuation through the same administrative owner, binding the immutable
qualified candidate, prior terminal review, new exact subject/grant/dispatch and
unambiguous downstream host/integration references. It requires explicit contract
authorization; it must not renew a consumed dispatch or create another coding
obligation. B-0052 remains unresolved and uninstalled.

## Verification

Maintained tests use the exact preserved two-call IDs/arguments over tiny authored
source, including non-ASCII and CRLF. They distinguish preflight rejection from
known completion and later uncertainty, verify prompt/capture/acquisition bounds,
and exercise the actual scripted candidate-to-review-to-host-to-plan consumers.
Scripted results are framework mechanics, not a new Qwen review or evidence of
model judgment. Final validation receipts and preservation identities accompany
this report; original failed development receipts remain failed.

## Final delivery measurements

Executable commit: `91b3676f5c9f10c4cfac44fbfc7a66c46f386c3a`.
The final explicit selection passed 21 tests in 141.57 seconds of pytest
execution: 19 new batch/partial-effect scenarios and two existing acceptance
review-to-plan consumers. Supported-root Ruff and formatting (772 files), strict
mypy (628 maintained files plus explicit reviewer-owner checks), layout, Intake
(71 proposal chains, no errors), links and diff checks passed.

Exactly one comprehensive execution passed: **4,205 passed, two optional skips,
100% configured production line/branch coverage**. Pytest took 3,235.00 seconds
(53m 54s); the command receipt measured 3,237.78 seconds. The configured source
table reports 14,247 production statements and 3,644 branches, with zero missing
statements/partial branches. All 1,070 protected raw input hashes and executable
Git blobs match the tested tree. Runtime/interpreter/packages match; a changed
tool-invocation environment fingerprint is disclosed rather than called complete
environment equivalence. The CSV candidate did not receive a new full-suite pass.

The first focused run remains failed: three fixture failures and 14 passes in
29.93 seconds. Fixture corrections used a malformed argument object that passes
the core ModelToolCall container boundary, the actual stale-source domain error,
and a serializable request assertion. The automatic recovery selection expanded
to 731 administrative/static-consumer tests and was interrupted to avoid
duplicating the mandatory full gate. Its original intent and explicit
interruption remain preserved; no passing result is claimed for that incomplete
run. Final focused and protected results are separate fresh observations.

[The evidence index](code-audit/acceptance-read-batches-20261102/index.json)
links the original receipts, interruption, exact authentication and quality
checks. [Protected output](code-audit/acceptance-read-batches-20261102/protected-output.json)
retains the exact saved stdout/stderr as JSON string values with SHA256 identities,
preserving CRLF and UTF-8 independently of checkout newline conversion. The TXT
copies are convenience displays, not byte authority. The original local outputs
remain untouched.

[Final integrity](code-audit/acceptance-read-batches-20261102/integrity.json)
verified 630 historical files, 118 original B-0052/archive files, 13 forensic
files, 903 RI rows, historical refs, released canonical Checkout and Inspector
registration on its independent feature branch. The provider's exact container,
image, command and mounts match the pinned original; health is OK, one idle slot
reports 65,536 tokens. No provider restart/configuration change, new coding or
review inference, policy replacement, candidate installation, host acceptance,
integration plan or backlog closeout occurred. The final publication contains
only the tested administration correction and its tests/docs/evidence.
