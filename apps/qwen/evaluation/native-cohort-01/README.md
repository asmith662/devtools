# Native Qwen coding cohort 01

**Executed locally. Overall Qwen effectiveness remains OPEN.**

Local development/evaluation is distinct from production WorkCycle operations.
The maintainer explicitly authorized these bounded local calls and temporary
edits. The existing `run_coding_task` API needed no grant; routing evaluation
through production assignments and the CLI's terminal gate was unnecessary.
The maintained CLI now invokes that same worker without approval rituals, under
the existing exclusive Checkout owner. Production governance is unchanged.

## Genuine results

| Condition | Task | Outcome | Model requests | Input / output tokens | Worker seconds |
| --- | --- | --- | ---: | ---: | ---: |
| Original worker | Duration boundary | ACCEPTED by frozen behavioral checks | 8 | 55,578 / 2,552 | 165.58 |
| Original worker | CSV dialect | Version argument refused; no edit | 1 | 1,257 / 141 | 10.22 |
| Read-version feedback/descriptions | CSV dialect | Nonexistent old-text helper; no edit | 5 | 25,739 / 1,564 | 85.37 |
| Final selected worker, held-out | Source physical spans | Corrected version, then out-of-range read; no edit | 2 | 6,188 / 243 | 17.92 |
| Same final worker, development comparison | CSV dialect | Three exact-match proposal refusals; no edit | 9 | 52,321 / 2,841 | 159.99 |

Total: **25 requests, 141,083 input / 7,341 output tokens, 439.08 seconds**
worker time (432.29 seconds summed model wait, 4.41 seconds validation).
Cached-input/reasoning categories, local energy cost and Codex coordination
usage are UNKNOWN. Overlapping categories were not added to totals. All calls
used the existing local profile with 4,096 requested output tokens/call, 32K
Context and thinking disabled. No paid fallback or service reconfiguration ran.
The cohort stayed below the initial 30-request/2,700-second resource envelope.
Source/result byte counts are cumulative, including repeated reads; Context
result JSON counts cover read-only acquisition, not edit/validation feedback.
Worker seconds exclude time spent on Codex engineering between conditions.

One of three unique tasks passed the frozen behavioral acceptance. Duration's
28 existing tests and independent oracle passed, but independent Ruff review
found ten EM101/TRY003 violations. Its exact candidate is preserved, with
supervisory disposition **BEHAVIOR_ACCEPTED_STYLE_REWORK_REQUIRED**. It is not a
production-ready published change. No code was silently repaired by Codex.
Candidate SHA-256:
`1d029fa2f37a310f53a2396b1eaa6aacd078978682dbdcba71571f313dd9fb0c`.

CSV produced no admitted patch in any condition. The held-out task never
reached editing or its post-edit oracle. No fresh successful live test-failure
repair was demonstrated; deterministic repair tests are a separate claim.
The final worker condition did not produce an accepted coding candidate in
this small sample. These results do not establish parity/superiority over Codex.

## Frozen task integrity and evidence

`manifest.json` records the original preparation state and pins the unchanged
task definitions, oracles and baseline commit
`e02c9044311036883134df955438b1b809db353b`. `results.json` records terminal
execution, source/receipt identities, Tool counts, inspected resources, Context
bytes/occupancy, omissions, timings and review. The policy JSON is retained as
an **unused historical preparation artifact**, not a prerequisite or authority.
The three original proposals remain pending; local evaluation did not promote
them, reuse B-0048's slot or modify any production work assignment.

Two cases were development tasks: duration boundaries and CSV dialect behavior.
Source physical spans was held out until development changes were selected and
tested. Its outcome did not drive subsequent worker changes or a held-out rerun.
Task read corpora (6/8/7 resources) and one-file edit scopes stayed distinct.
The one-file target is disclosed, so this tests scoped investigation rather
than blind repository-wide localization. Source-span semantics are related to
historical materialization work, although the new target and retrieval oracle
are different. This is a small initial cohort, not a representative benchmark.

Raw `qwen-coding-loop-v2` receipts remain under
`.local/qwen-coding-worker/native-cohort-01/{baseline,improved,held-out,final-development}/`.
Each contains original requests/responses, native call IDs/results, source
versions, actual proposals, validation and bounded feedback. Failed-run
`final-source.py` captures are baseline bytes, not successful candidates.
Every original source/test hash was rechecked after restoration. No complete
repository copy, worktree, new executor or second transcript store was created.
The existing dashboard projection reads all five receipts as LOCAL_MODEL_RECEIPT
with zero projection errors when these four parents are supplied as configured
`--worker-root` values. Default shallow discovery need not be changed.

## Measured failures and selected corrections

1. CSV initially supplied literal `CURRENT` as a source version. Host refusal
   was correct, but terminal handling prevented correction. Descriptions now
   explain metadata lookup first; safe version refusals return correlated Tool
   feedback and consume the same action budget. The held-out model actually
   corrected its version after this feedback, then failed a different bound.
2. CSV lost its earlier codec body during pruning and proposed an unseen helper.
   Selection now protects a current edit-target prefix exchange (otherwise its
   latest read), alongside latest validation/newest exchange. Archived-trace
   replay retained the missing body in 18,492 bytes under the unchanged 24,000
   byte cap. This deterministic selection result is not coding competence.
3. Exact old-text mismatch now returns no-effect native feedback, bounded by
   the original three proposals. Final CSV exercised all three refusals; no
   approximation or unauthorized patch was applied.

The retention heuristic **did not resolve CSV grounding**: the final model chose
the quoting helper in an omitted tail, inventing an if-chain instead of the
actual mapping. All eight read actions were spent, preventing reacquisition.
Omissions were explicit, but Qwen still proposed unsupported source. Native
message correlation worked; literal newline escaping was not the cause.
The held-out end=20000 request exceeded the real source length. Strict read
admission refused it; that failed held-out result is preserved without tuning.

Next Qwen optimization: retain the model-selected edit region rather than an
arbitrary file prefix, reduce redundant result metadata, and make valid read
bounds actionable. Add repository style checks to a separately frozen future
acceptance contract. Evaluate on fresh cases; do not reinterpret these failures
as successes or rerun the held-out case until favorable. Pure behavior-preserving
refactors and multi-file work remain unsupported/unevaluated. No controlled
equal-task Codex baseline exists; historical tasks cannot establish savings.

## Direct local use

Trusted operators/Codex may run a host-owned task directly, without grants or
interactive prompts. Use a new evidence directory for each explicit condition:

```powershell
uv run --python C:/Python314/python.exe python scripts/qwen/coding_worker.py --task-definition <host-task.json> --report-directory .local/qwen-coding-worker/<new-run>
```

Do not blindly repeat these completed cohort runs. The CLI validates paths,
selects/creates an ordinary feature branch at the exact baseline, enforces task
scope and validation, restores source, and returns to the administrative branch.
It refuses dirty/index/collision/owned states and existing report directories.
There is no arbitrary model shell/Git/write authority. Local candidates confer
no production integration or protected publication permission. WorkCycle still
owns separately governed production assignment and closeout.
