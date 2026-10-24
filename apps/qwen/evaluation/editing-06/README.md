# Flat observed editing: matched development and confirmation

## Original frozen plan (retained)

The frozen manifest and task definitions precede inference. Budget: at most eight
runs, 80 model calls, 7,200 worker seconds; each run ten calls, 4,096 output
tokens/call, 900 seconds, original q4/32K/thinking-off server and sampler.
Two development cases compare the improved Devtools interface with scoped Pi
1.3.0: immutable Command arguments and a new lazy conversion API/module/export.
A distinct file-disappearance normalization case is confirmation, run only after
freezing the chosen worker configuration. No tuning to its model result.

Both harnesses use identical pinned source, objectives, oracles, original tests,
Ruff/formatting and strict typing. Devtools allows 24 read/check/API calls plus
three atomic proposals of at most eight flat calls. Pi allows 24 total Tool
actions including edits/checks; both have ten model calls. Interfaces are the
treatment; these action populations are not identical. Two unused slots reserve
conditional independently frozen repair-only work if development produces no
genuine feedback repair. No completed run is blindly retried.

`replace_source(reference, old_text, new_text)` uses short `edit_ref` handles
returned by actual source reads. Paths, exact versions and required API evidence
are resolved by the host. Empty old text means the complete referenced span or
authorized absent file. Nonempty old text remains an exact unique source snippet.
All calls in one assistant response form one atomic proposal through the existing
transaction admission/application implementation. No staged mutation or second
patch engine exists. Native results correlate every provider call; the first
result contains shared validation and subsequent calls reference it.

Historical single-edit/nested contracts and receipts remain supported. References
are task-local observation handles, not replacement RI identities or authority.
Stale, overlapping, malformed, oversized, unobserved or unauthorized proposals
refuse without partial mutation. No suffix trimming or approximate source matching.
`diagnosis.json` distinguishes verified adapter behavior from unavailable historical
pre-decoder evidence. Actual outcomes are recorded after execution.


## Editing comparison 06 — measured outcome

Flat observed native edits reuse existing atomic admission and source ownership.
On valid paired development tasks, Devtools accepted 1/2 versus Pi 2/2. The
Command correction genuinely repaired a typing failure while preserving passed
behavior; the lazy new-module task failed before editing. Safe unit/schema
feedback and a direct bounded source-read adapter were selected from those
development failures; no third run of that task was performed.

A replacement fresh confirmation passed both harnesses (5 versus 4 requests).
The original disappearance confirmation is excluded: its independently authored
oracle incorrectly assumed CPython 3.14 Path.exists/is_file call overridden stat.
Its two failed receipts remain immutable. The replacement Pi allocation followed
Devtools success, limiting the independence of pair selection. No general parity
or comparative correctness improvement is established by this small sample.

Nine real runs consumed 53 calls, 363,197 input / 12,030 output tokens and
745.01 summed worker seconds. Five admitted Devtools transactions contained 14
flat native edit calls with zero admission refusals and zero omitted exchanges.
The original 80-call/7,200-second budget was unchanged when the run-count cap was
prospectively amended from eight to nine to replace the invalid confirmation.
See [frozen definitions and detailed results](results.json).
The Command candidate is selected for shared reviewed closeout; the decoded
output candidate remains evidence pending separate integration.

| Frozen task | Devtools | Pi | Requests Devtools / Pi | Worker seconds Devtools / Pi |
| --- | --- | --- | --- | --- |
| Command argument immutability | ACCEPTED; typing repair | ACCEPTED | 8 / 5 | 161.71 / 109.12 |
| Lazy conversion/new module | Failed before edit; one bounded recovery also failed | ACCEPTED | 1 + 2 / 8 | 13.11 + 20.28 / 64.58 |
| Read disappearance — INVALID ORACLE | Call budget exhausted | REJECTED | 10 / 10 | 196.18 / 79.54 |
| Decoded CommandResult output — replacement confirmation | ACCEPTED | ACCEPTED | 5 / 4 | 51.88 / 48.61 |

Historical malformed arguments already existed in the normalized provider
function.arguments before Devtools admission. The adapter preserves them; no
host-added suffix was demonstrated. Archived pre-decoder HTTP/token evidence is
absent, so generation versus llama.cpp/template decoding remains UNKNOWN.
No suspicious suffix is stripped. See diagnosis.json and oracle-review.json.

All new Devtools provider responses are captured before normalization and match
native call arguments exactly. Independent reconstruction authenticates every
admitted observation, source version, exact anchor, transaction diff and final
candidate. All 493 environment-05 evidence files retained their original hashes.
Raw evidence is under `.local/qwen-coding-worker/editing-06/`; results.json
contains hashes and per-turn metrics. No source-tree copies or extra checkouts.

The Pi adapter uses pinned SDK 1.3.0 with native read/edit/write, fixed validation,
authorized path wrappers, local endpoint only and no bash/cloud fallback. The
replacement output case additionally exposes the same allowlisted installed API
inspection; both harnesses actually inspected bytes.decode before editing.
The Tool surfaces and action-count populations differ as recorded above. No
worker changes followed the original confirmation outcomes. The original frozen
plan is retained above; final-reference-allocation.json records the ninth-run
amendment before dispatch, not a retroactive budget increase.

Command final source: SHA-256
`1d6ba377cbd443271a7550956d0f16506c1d313a9870af0554112136e02c6d71`.
Its implementation is Qwen-authored; permanent regressions and oracle review are
Codex-authored. Other accepted candidates remain evidence, not production claims.
Codex coordination tokens, energy, incremental hardware cost and monetary cost
are UNKNOWN. No paid-model or scientific-controller invocation occurred.


## Verified feature closeout

The exact Command candidate above was independently reviewed and published through
the existing WorkCycle `closeout_local` operation in commit `0f121bca1baf4c896050a92994fca5023699eec5`
on `origin/feat/qwen-context-worker`. Source SHA-256 is unchanged from the genuine
Qwen run. Codex authored ten permanent regression cases (twenty focused tests
total), not a replacement implementation. The frozen oracle, Ruff, formatting,
strict typing and the canonical protected development gate passed before
publication. Full check timings and exact receipt/review hashes are in
`results.json`. Feature publication does not imply protected-main integration.
The decoded-output and Pi candidates remain evidence only.

Focused application/CLI checks: 282 passed in 81.89 seconds. Maintained source,
tests, applications and scripts passed Ruff; strict mypy passed 486 files.
Changed Python files passed formatting and layout/diff checks. Frozen generated
scientific payloads were not reformatted or validated as maintained code.
