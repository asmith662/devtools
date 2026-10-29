# Adaptive Context compaction

Implementation 3 starts from `d5d18b589948f19f457a29161b8811da8f7cf0ee`.
The ownership decision precedes production changes: the coding host continues
to assemble active Prompts; Context owns source representation; the existing
semantic compactor owns auxiliary dispatch, provenance, cache and fallback.
A small optional policy in that same package selects automatic requests. No
second history, executor, tokenizer, provider or coding loop is introduced.

The initial policy is deliberately conservative. After deterministic projection,
it considers semantic inference only when host-identified valuable original
records would be omitted, the original request meets an explicit pressure
threshold, sufficient byte headroom remains, and the existing auxiliary budget
permits entry. Value is a host judgment, not retrieval score or model authority.
Protected-context overflow remains an explicit capacity failure. Automatic
selection does not recover it by discarding protected facts. Explicit bounded
compaction retains its existing separate contract.

A previously failed/uncertain auxiliary attempt suppresses further automatic
requests for this host; explicit requests still use existing no-replay checks.
An accepted, still-valid cached summary is reused without another inference.
Thresholds are host configuration, not empirically established universal values.
The planned frozen comparison will assess their usefulness, not assume it.

Exact policy, current source, failed-check feedback, effects and custody remain
independent of derived notes. Auxiliary cancellation propagates. Valid
deterministic continuation survives optional strategy failure.

## Configuration and decision path

Supply `SummaryCompaction(adaptive=AdaptiveCompaction(pressure_bytes,
reserve_bytes, valuable))` through the existing `RepositoryCodingHost(summary=...,
projection=...)`. `valuable(original_messages)` returns a frozen set of original
indices. It identifies working information worth retaining, not authority to
disclose or omit it: `SummarySelection` independently controls both. No automatic
policy exists unless explicitly configured. No-summary hosts remain deterministic.

The existing compactor first revalidates any cached notes against history,
snapshot, source bindings, protected recent/check evidence and current replacement
permission. Valid reuse spends no inference. Otherwise the optional policy:

1. Refuses automatic work after auxiliary exhaustion or a prior strategy failure.
2. Requires an already affordable deterministic continuation.
3. Checks the explicit original complete-request pressure threshold and reserved
   headroom under the hard bound.
4. Requires valuable original indices inside a whole exchange actually omitted
   by deterministic projection.
5. Schedules one existing semantic attempt. Existing disclosure, bounded input,
   provenance, no-replay and final complete-request checks remain authoritative.

`compactor.decisions` records `no-pressure`, `deterministic-sufficient`,
`insufficient-headroom`, `protected-context-unaffordable`, `cached-summary`,
`auxiliary-budget-exhausted`, `prior-strategy-failure`, `policy-failed` or
`semantic-requested`. These accompany existing `SummaryAttempt` stage outcomes
and `ProjectionOutcome` exact sizes/selections. Requested is not entered, validated
or adopted. An explicit manual request remains distinct from an automatic decision.
There is no model-requested compaction Tool.

Invalid host value selection preserves fallback and records the original error.
Failure suppresses subsequent automatic attempts for this host, including unknown
entry and insufficient reduction; explicit requests remain subject to existing
budgets and identical-request replay refusal. Cancellation still propagates.
All automatic inference remains inside the coding process's wall timeout and the
auxiliary per-call timeout. There is no prediction of remaining wall-time value.

Reserve is an explicit conservative heuristic, not a token counter or guarantee
that notes fit. Final projection measures the complete request and may refuse a
structurally valid summary. The policy does not automatically solve a protected
minimum that cannot fit, shorten mandatory source evidence, or infer semantic
importance from age, filenames, frequency or model assertions. Explicit semantic
compaction can still exercise its previously supported bounded recovery path.

## Real assessment and architectural decision

The [frozen assessment](../../experiments/context_compaction/REPORT.md) used one
authored pressure/working-state history and three actual local treatments. The
40,010-byte original projected to 4,306 bytes. Two auxiliary responses preserved
the principal recorded conclusions but used Markdown-fenced JSON and were refused.
No acting request consumed summary text. One fallback candidate passed 4 focused
and 5 held-out cases; two treatments stopped on invalid source ranges. No live
repair was needed or demonstrated. Threshold optimality and semantic benefit
remain unestablished. Keep the policy opt-in, with no universal threshold defaults.

Qwen's `apps/qwen/turns/loop.py::_LegacyHost` continues to call
`apps/qwen/continuation.py::select_messages` and the shared coding process through
its original task/journal representation. Adopting neutral `RepositoryCodingHost`
projection would require reconciling those message/source bindings and legacy
prompt projection in `apps/qwen/turns/prompt.py`; it is not just passing a new
configuration value. The application adapter continues to use its original continuation projection
while sharing the coding process; this change does not alter task hashes or claim
full adapter adoption. The new live consumer is the neutral repository host with
the existing local ModelInteraction. Deterministic maintained tests exercise
non-Qwen identities, automatic adoption/cache/failure and original-history retention.

The next practical improvement is source-range discovery and recoverable pre-effect
argument feedback. Summary format compliance deserves a separate bounded decision
before another semantic-continuation comparison. No additional live trial, parser
relaxation, provider change, durable recovery, broad Evidence integration or
observation Option B was introduced to improve this result.

## Committed validation

Implementation `7cf1eb79dc638dece63ae80971d3de342758f71b`, tree `d89481534a3bd849ba1e3562f9f820e8498dd311`, passed the unchanged command
`uv run python scripts/validate_development.py`: **================ 3769 passed, 2 skipped in 1514.92s (0:25:14) =================**.
Started `2026-10-29T01:32:00.717422+00:00`, finished `2026-10-29T01:57:18.034117+00:00`, elapsed
1517.038 seconds, exit 0. Configured production line/branch coverage is
100%, with 0 missing lines and 0 missing
branches. All 1054 physical validation inputs remained unchanged.
Supported Ruff/formatting, strict mypy (595 files) and layout passed on that same
committed tree. No selector, coverage threshold, exclusion or configuration changed.

Before implementation, 251 baseline tests passed. The broad focused suite passed
1,264 tests; its capture correctly flagged a package-document update during the
run, so it is not claimed as immutable-input evidence. The final protected gate
supersedes that limitation. The final semantic/adaptive diagnostic suite passed
91 tests and covered all compaction branches; its subset naturally failed the
unchanged whole-production coverage threshold, which was never lowered.

Windows Python 3.14.3, pytest 9.1.1, coverage 7.15.4, Ruff 0.16.2, mypy 2.3.0,
uv 0.12.2 and Git 2.53.0.windows.2 were recorded. This is not cross-platform
certification or general live-model effectiveness. Exact commands, versions,
source/test blobs, physical hashes, times, outcomes and preservation qualifications
are in the [receipt](../research/code-audit/adaptive-context-compaction-20261029.json).

Canonical Intake remains at 68 valid chains; 903 RI rows, thirteen forensic
records, original local cases and historical refs are preserved. JSON/JSONL,
new links, layout and whitespace pass; two old B-0002 scratch links remain
qualified. Existing B-0002/B-0035/B-0043 stay open, as do the 188 historical
RI-version obligations and separate recovery/Evidence/Option B/A+C decisions.
