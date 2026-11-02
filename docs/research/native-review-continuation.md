# B-0052 acceptance-review continuation — 2026-11-02

The bounded continuation contract is delivered and protected-validated. One new
real Qwen review entered against B-0052's unchanged qualified candidate. Its first
two-read batch succeeded. Its second two-read batch exceeded the **one remaining
acquisition**, so preflight refused both operations before entry. The attempt
ended **BLOCKED**, with no structured judgment, host acceptance or integration
plan. Coding was not repeated and the CSV candidate was not installed.

This establishes lawful continuation and actual multi-read execution, not
completed acceptance review or end-to-end integration success. The negative
outcome is retained without another sample or a replacement coding task.

## Contract and identities

The [existing reviewer owner](../development/native-review-continuation.md) now
has one prospective `reviewer/continuation/` slot, selected by its exact sealed
subject hash. Legacy `reviewer/` files and readers retain their meanings. New
subject, authorization, dispatch and proposal records use version 2. Native host
review v2 and the existing integration-plan reader explicitly bind that selected
subject and proposal; neither chooses the latest or most favorable attempt.

| Identity | Authenticated value |
| --- | --- |
| Starting local/remote main | `9ad77e0f28b78bbc5900a389a174216251b2f35e` |
| Protected executable/source publication | `f06442f6b4c65b60adc379e697555c564b6a7a8f` |
| Engineering obligation | Existing approved B-0052; no new Intake item |
| Original coding assignment | `7489f593e0b23b4a8b118201394d738f62febf3f606d2efec83d7a5e394b33ef` |
| Original consumed coding dispatch | `91c533aa6a38b2036a8ac1f19f16ea300fbdf82f3e4b577142999025abd46ee3` |
| Qualified native result | `f1971ed020430afcf064e88f9cacb193ce1f0a900233759ac78aa66788d2eed2` |
| Unchanged candidate SHA256 | `a7471ffeec9a21cdb12ddc3bcb0cb315680f109ff70d168ade03310c24bef255` |
| Candidate patch SHA256 | `385da31f1b570482b187d89c5c63f6b8474fd68d45fda197b6c17b6b31ca9b04` |
| Original blocked review proposal | `4e0b440d370b65187eb2d121cac6a542f888681bcb149be3b3ffb7fc36c4efca` |
| New exact review subject/attempt | `35264a7eba5fcceb17b341208eaf9b6c98874bd84d1e0e9382825b9b398cba33` |
| New review authorization | `14a8561621b485a7462a9cc76f4b9acdc22ea98fcce0450e2fbfcca79b4ed05f` |
| New consumed review dispatch | `c59bb403474a27503b2b690f475bb7f63e8cef9784435e34fdaea27e9e648936` |
| New blocked review proposal | `2b1ac4fa7bd5855548d9eb53738acccb8dce9cc32c7660eb86e78118c6986e85` |
| Active standing policy | `f712a8e21f0c07485fa46f904ea6f63a984e1fb6ae69637a5242b045fe2defcf` |
| New policy decision | `4fbae08187bd448bd8c65b1ef062523c0151232c5aaa26080c79339e10772d7f` |

The predecessor must prove the specific legacy single-read-per-response barrier:
one returned model call, zero entered reads, no engineering conclusion or host
judgment, authenticated request/response and grant timing, and an authorized
read-only batch within the original total allowance. Expired historical grants
remain historical; a fresh policy-derived grant supplies new authority. One
exclusive continuation claim prevents duplicate/concurrent preparation and
further chaining. Completed judgments, unknown effects, source drift or candidate
tampering do not qualify. Standing authority does not override these limits.

The original blocked slot was not refunded or rewritten. Its error was a
one-read-per-response restriction, not total acquisition exhaustion. The new
failure has a different boundary: the requested batch exceeded the remaining
total acquisition allowance.

## Qualification and actual model operation

The exact frozen public file was rematerialized from its authenticated archive,
without changing expectations, and removed after the episode. Existing native
currentness validation admitted the subject and it equaled the original candidate
subject. Declared source/check/configuration inputs matched; all `src/` Git blobs
were unchanged since the coding baseline. The original 54 public passes and
independent private acceptance are **authenticated prior executions**, not freshly
rerun checks or a new candidate coverage claim. The candidate remained archived;
working source was the restored baseline throughout.

The trusted host used `routine.authorize_reviewer(..., attempt=subject_hash)`.
There was no per-task operator prompt and no reuse of the consumed original grant.
The fresh grant expired at `2026-11-03T00:09:35.436035+00:00` and permitted four
model calls, three acquisitions, 120 seconds per call and 480 seconds overall;
2,048 output tokens per response; 128 KiB request, 64 KiB response and 960 KiB
native capture limits. Another 64 KiB bounded support capture kept the combined
episode allowance at 1 MiB.

The unchanged Qwen3.8-27B UD-IQ4_XS container and pinned image were authenticated.
`/health` was healthy and `/slots` reported one idle 65,536-token slot before
entry and after completion. The existing `LlamaCppInteraction` measured template
input fit with 2,048 generation tokens and a 1,024-token safety reservation. The
new session received no coding conversation, previous review transcript, private
oracle implementation, reference solution or host scoring. Same model weights
do not establish diversity of judgment. Provider sampling defaults, including
temperature 1.0, remained unchanged. No serving operation was performed.

| Call | Actual input/output tokens | Read-only proposal and result |
| --- | --- | --- |
| 1 | 11,047 / 111 | Read `tests/resources/filesystem/models/csv/test_row.py` and `test_file.py`; both completed with distinct correlated IDs |
| 2 | 13,558 / 153 | Read frozen `tests/live_native_csv_row_public.py` and `src/devtools/resources/filesystem/codecs/csv.py`; both refused before entry because only one acquisition remained |

Two actual adapter entries returned normally with Tool-call termination. There
was no provider timeout, truncated response, Context-capacity failure or unknown
Tool effect. The two successful reads disclosed 6,535 source bytes with exact
source versions/spans. Total usage was 24,605 input and 264 output tokens. Review
wall time was 54.184 seconds; measured adapter time was 30.673 seconds. First-token
latency is unavailable from this nonstreaming adapter. Observation envelopes
occupied 99,742 on-disk bytes and support capture used 3,221 bytes; these are
capture observations, not provider-token counts or additional authority.

## Host assessment and gates

The model's partial statement that the `set` length comparison detects exact
duplicate string names while preserving distinct case/whitespace/codepoint names
is supported by the candidate. It did not complete findings, risk assessment or
a structured recommendation. Its requested codec/public-file inspection did
not execute. No substantive engineering rejection or acceptance can be inferred.

The [host assessment](code-audit/native-review-continuation-20261102/host-assessment.json)
is explicitly advisory: **NO_ADMISSIBLE_REVIEW_PROPOSAL**. No native host-review
decision was issued and no integration-plan consumer was invoked. Historical
public/private qualification alone does not complete independent review.

The acceptance path advertises static total budgets but does not provide the
diagnostic path's dynamic remaining-budget view or reserved synthesis behavior.
The refused batch requested two reads after two of three were used. Two model
calls and one acquisition remained numerically available, but the existing owner
terminated and sealed the attempt. Those unused allowances do not refund a
consumed dispatch. No additional sample or continuation was entered.

The next bounded improvement is budget-aware acceptance-review completion through
the existing reviewer: reuse the established budget view/final synthesis policy
and return truthful correlated refusal feedback within the approved call count.
Do not increase acquisitions or replay this attempt. A future B-0052 review would
also require explicitly authorized prospective continuation eligibility beyond
this increment's consumed single allowance. No new coding task is necessary.

Installation would additionally require a genuinely completed accepted review,
trusted host disposition, destination-current plan, maintained regression
additions and exact integration authority. A separately observed existing limit
also needs reconciliation: integration's fixed pre-publication profile includes
the protected suite but permits at most 1,800 validation seconds. This session's
complete gate took over 3,000 seconds. No validation control was relaxed here.

## Verification and preservation

Focused intelligent validation passed 2-, 5- and 2-test selections, covering the
new authored-repository refusal/concurrency and exact policy/review/plan scenarios
plus legacy acceptance and standing-authority consumers. These are deterministic
mechanics, not evidence of model review competence.

There were **two comprehensive entries** against the same committed executable
candidate. The maintained `comprehensive` wrapper timed out at 3,600.037 seconds
while still progressing, with unchanged inputs and no completed phase receipt;
it remains a timeout. No passing count or completed coverage is inferred from it.
The second run reused the installed `scripts.validation.protected` fresh-child
entry point, identical protected arguments/configuration and a separate fresh
coverage file, with a finite 7,200-second managed Command deadline. It passed
**4,207 tests, two optional skips and 100% configured production line/branch
coverage**: 14,247 statements and 3,644 branches, zero misses/partial branches.
Pytest reported 3,058.55 seconds; the operational receipt reported 3,073.895
seconds. Different elapsed times do not establish a diagnosed performance cause.
No validation-policy or executable change was made to obtain the second result.

Supported-root Ruff/formatting, strict mypy (629 configured source files and an
explicit 15-file administrative selection), layout, Intake and link checks passed.
All 1,072 protected file hashes and Git blobs matched the passed executable tree
after cleanup. Runtime/packages matched; invocation environment fingerprints
differed, so complete external-state equivalence is not claimed. Documentation
and observational publication require no further comprehensive execution.

The 630 preserved historical files, 179 original native files, thirteen forensic
files, 903 RI-ledger rows and historical refs were verified. B-0049/B-0050/B-0051
and both original B-0052 dispatches remain unchanged. B-0035 closure, B-0043's open
status and the 188 historical RI obligations remain intact. CSV baseline raw
SHA256 remains `b49914a0c9cab47724e2670f182a58b09e4f00e98bb87930d7504d5f88ccb80c`.
Checkout is released. Inspector remained registered on `feat/agent-inspector`
and advanced independently; no Inspector files/ref or service configuration were
modified by this work.

The [audit directory](code-audit/native-review-continuation-20261102/) retains
qualification, both validation outcomes, policy-derived authority, raw review
request/response/Tool observations, measurements, host evaluation and integrity
receipts. UTF-8 text envelopes preserve exact captured JSON bytes and their
hashes despite Git newline handling. Host-only private acceptance implementation
and controls remain withheld. Raw model content and factual host assessment are
separate. The original and new blocked outcomes remain blocked.
