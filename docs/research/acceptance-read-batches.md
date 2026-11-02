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
