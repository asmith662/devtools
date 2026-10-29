# Maintenance-feedback-0001: trustworthy oracles, refused oversized edits

## Outcome

One real local Qwen3.8-27B attempt investigated B-0035's first-request authorized
resource inventory and produced two source-grounded proposals. Both exceeded the
unchanged resulting-source bound and were refused before application. Eight
acting requests exhausted the frozen call budget. No edit or worker validation
ran; no model-authored change was accepted into production. This is a clean,
attributable maintenance failure, not an oracle-confounded repair result.

Authenticated starting main: `2bdf66b6a111e961047a563a258a821bd39ea0fa`.
Preparation implementation: `41a7624ba9f06cc923b7f9db034155f344c9209a`.
Frozen execution main: `9ddc8efb532dd6a968514a1cbf859d9fe52a655a`.
Task digest: `6018a1b99e9d5f7d6321a2210bb8621cab6ae58b409dc53c1ca556305f16c6a8`.
Snapshot: `9a065bcd63f1b4aedb0d71a4e81b9f843aace5c8d9fc048795c99bb0bb808354`.
The [freeze](freeze.json) binds source bytes/blobs, model, task, oracles,
controller, privacy, Tools and finite budgets before inference.

## Independent review of Reliability-0001

Intersecting `[1,3)` and `[5,8)` with `[2,6)` gives `[2,3)` and `[5,6)`.
Their lengths total two. Independent integer unit-cell membership gives `{2,5}`,
also two. The old expected three was a supervisor mistake. Its original fixture,
feedback, responses and outcome are unchanged. The new Evaluation comparison
detects that discrepancy; it does not reinterpret the old trial as successful.

The old second proposal's anchors overlap at character interval `[411,491)`:
both include sorting the intervals and initializing the current interval. The
retained native IDs each received `REFUSED` / `Edit anchors overlap.`. The whole
batch was rejected before application. Its second proposal exhausted the old
two-proposal limit, so there was no next provider request to consume that refusal.
The shared process otherwise permits a newly selected proposal when budget
remains. New maintained tests prove atomic refusal, unchanged source and a
separate succeeding proposal; they also protect terminal limit behavior.
The existing feedback is adequate to identify this two-anchor conflict when read
with the original proposal. No edit-engine modification is justified here.

## Oracle integrity preflight

The [preflight record](preflight.json) retains exact commands and outcomes.
`devtools.evaluation.preflight` adds finite expectation comparison, reusing
Evaluation's identity coverage. It requires named obligations, normal/boundary/
empty observations, documented independent derivations and agreement. It performs
no execution and cannot certify the honesty or semantic independence of a
derivation. Existing pytest, Commands and fixed checks remain execution owners.

The task has four focused tests and six separate withheld checks. A private
reference observation host derives sizes/content identities from raw authorized
files rather than candidate metadata. All ten predicates pass against those
observations. Additional controls reject wrong byte size, missing/foreign/
duplicate resources, false edit authority, source-witness credit and identity.
Ten reference tests passed, including the full ten-predicate positive control.
The reference code and withheld oracle were never in the model's read scope.

Baseline: three focused and five held-out assertion failures; stale-source and
no-witness controls passed. JUnit had no collection/runtime errors or skips.
Expected failures were checked by exact test identity, not just nonzero exit.
UTF-8 command output was explicitly selected. This is a finite empirical
cross-check, not proof of the entire API. No expectations changed after inference.

## Task selection and operational envelope

B-0035 remained the preferred genuine backlog obligation: the neutral coding
host still lacked a complete first-request metadata inventory, requiring a
listing-only inference step. The task specified observable metadata, scope,
identity, freshness, privacy, no-witness and capacity semantics without a patch.
Sixteen resources were readable; seven existing top-level coding modules were
editable. Tests, docs, configuration and private references were not editable.

The preflight explicitly recorded that `repository.py` was 32,648 bytes, leaving
120 bytes under the 32,768-byte resulting-source limit. The model could select
among cohesive coding owners, but no limit increase or broad refactor was allowed.
This proved a substantial feasibility obstacle; it was not hidden or changed
after the outcome, and no easier replacement task was selected.

The already-running llama.cpp b10868 service and Qwen3.8-27B UD-IQ4_XS artifact
were authenticated, including actual GGUF SHA-256
`40fac4050e940397dbf13087afd50f4734a11805bf9d65ef8ddd7483470e6199` and profile
`03758e5bc51c9aa9fbdd1850c1f25541d1eba76a80a54b74598886d882264bf1`.
No service restart, download, paid fallback or model substitution occurred.

The frozen envelope was eight acting requests, four proposals, at most three
applied candidates/two validation-feedback repairs, twenty acquisition actions,
150 seconds per request, 1,080 seconds for the shared process and a 1,200-second
outer timeout. Input/output ceilings remained 28,160/4,096 tokens, host Prompt
32,768 bytes, source/disclosure 32,768/8,192 bytes, edit region/aggregate
4,096/8,192 bytes, two operations per batch. No arbitrary commands were offered.

Deterministic projection used explicit 24,576/20,000 trigger/target watermarks.
No auxiliary summary call was configured: this fresh task had no useful prior
working-state history warranting one. Consequently no summary was produced,
normalized, adopted, presented or consumed, and no semantic benefit is claimed.

## Real investigation, proposals and feedback

| Request | Actual model-selected operations |
| --- | --- |
| 1 | List authorized resources; search repository metadata/snapshot terms |
| 2 | Read projection.py `[0,7500)` and focused.py `[4459,5140)` |
| 3 | Read repository.py `[0,8192)` |
| 4 | Read test_repository.py `[0,8192)` |
| 5 | Read test_repository.py from 8192 to its observed end, 11114 |
| 6 | Read repository.py `[8192,16384)` |
| 7 | Propose metadata initialization in repository.py; size refusal |
| 8 | Propose a metadata helper in repository.py; size refusal |

There were six successful reads, with no natural invalid range. Search candidates
and listing metadata are retained separately from actual source disclosures.
The model located the relevant host, but did not acquire the repository-resource
data contract. Both proposed anchors were covered by current active source at
proposal time; missing source was not their refusal cause.

The first proposal would produce **32,990 bytes**; the second **33,568 bytes**,
against 32,768 allowed. Each received the original call-correlated
`Structured edit exceeds the bounded source size` refusal. The first refusal
was in the eighth request actually consumed by the model. The next proposal
still added source, so it did not resolve the stated bound. This was a
model-selected response to admission feedback, not an effective repair and not
a failed-check repair. The last refusal was retained but not consumed by a ninth
request. No call was repeated automatically and no proposal was rewritten/split.

## Measurements and independent grading

| Measurement | Observed |
| --- | --- |
| Acting / auxiliary requests | 8 / 0 |
| Input / output tokens | 46,979 / 1,326 |
| Measured acting inference | 114.149613 seconds |
| Shared coding process | 115.151166 seconds |
| Acquisition actions | 8: list, search, six reads |
| Proposals / admitted / applied | 2 / 0 / 0 |
| Worker checks / model-requested procedures | 0 / 0 |
| Terminal disposition | `model_limit`, accepted=false |
| Custody | Restored, no reconciliation required |

Unknown cached/reasoning usage remains unknown. The deterministic procedure and
fixed checks were available but not entered during the worker run. Supervisor
preflight and independent grading commands are separate, known execution facts.

Complete-request original/projected bytes across the eight preparations were:
4,653/4,653; 12,600/12,600; 23,514/23,514; 34,250/26,303;
44,687/25,826; 48,979/30,118; 58,946/29,349; 61,134/31,537.
All active requests fit the unchanged hard limit, although reductions did not
reach the lower target. Native correlation and current edit witnesses remained
valid; original history was retained. Thus Case 0003's capacity blocker did not
recur, but fitting Context did not establish maintenance success.

Every archived editable file equals its frozen starting bytes. Independent
post-run focused/withheld grading on that exact restored state again produced
three/five intended assertion failures and no harness errors. There was no need
to install an unexecuted proposal or copy the repository. The
[independent review](independent-review.json) rejects integration. No model-authored
production change exists; the only new supported implementation is the
supervisor's explicitly separate oracle-preflight comparator and tests.

## Decision, preservation and reproduction

The immediate limiting boundary is **edit feasibility in the nearly full
repository host**, compounded by six investigation requests before the first
proposal. The highest-leverage next increment is a separately authorized,
cohesive extraction that restores practical source-size margin while preserving
the existing coding contracts, followed by a new real maintenance task. Do not
raise limits, retroactively repair this attempt or infer general model inability
from one sample. Better size diagnostics may help, but both the initial prompt
and consumed refusal already disclosed the relevant constraint.

The original thirteen forensic files, earlier cases, Adaptive-0001,
Reliability-0001, 903 RI rows and historical refs remain unchanged. B-0035 stays
open; B-0043 and existing cohesion/recovery/Evidence obligations remain separate.
No grants, new B-number, parent closure or broader architecture approval follows.

Run `uv run python experiments/local_maintenance_feedback/verify.py` for effect-free
freeze, native-correlation, archive and refusal checks. It invokes no model or
old effects. The only post-run analysis correction was reading snapshot identity
from the existing source-unit field rather than a nonexistent serialized property;
original records and measurements were unaffected. New inference requires a new
identity and authorization; the primary entry marker prevents a second attempt.
Final protected/static validation is recorded in the
[delivery contract](../../docs/development/oracle-integrity-preflight.md).
