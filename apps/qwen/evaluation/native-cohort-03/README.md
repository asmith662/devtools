# Requirement-preserving repair evaluation

The manifest freezes three fresh tasks at `d8741a52f9342bd180e414832e8f31b52f4c8c9a`.
The two development cases cover a callable regex API across related source
regions and JSON duplicate-member rejection with existing domain errors. The
timestamp wrong-type/valid-string compatibility case remains held out until
development configuration selection. No intended implementation is disclosed.

Each definition independently requires behavior, existing regressions, strict
scoped mypy, Ruff and formatting. The fixed oracle prints a behavior-pass marker
before running managed typing, so a typing failure need not be mistaken for a
behavioral regression. Baseline checks established intended oracle failures,
passing original tests, and passing original quality/typing checks. The manifest
records the Codex contract review, alternatives and exception/lint compatibility;
this is engineering judgment rather than a satisfiability proof.

Budget: six runs, at most 60 model calls and 5,400 cumulative worker seconds;
each run retains the same ten-call/three-proposal/eight-read, 4,096-output-token,
900-second bounds. Compare unchanged versus improved worker on both development
tasks; compare thinking disabled versus enabled on the regex development task
only; then freeze configuration and run the timestamp held-out case once. All
use the same local Qwen3.8-27B IQ4_XS weights and 32K service. A single paired
sample is exploratory, not an estimate of general reliability or causality.

Historical cohort 02's held-out failure remains unchanged. Its first proposal
passed 22 behavioral scenarios and ten regressions, but Ruff TRY004 recommended
TypeError against the explicit ValueError contract. Qwen's next visible response
called TypeError “more specific” than the task's “generic ValueError guidance”
and broke the passing oracle. All requirements and source were still visible;
source eviction did not cause that failure. Task preparation should surface
this tension, and repair feedback should preserve passed behavioral obligations.

The new baseline development traces additionally exposed import edits
invalidating observations of unchanged functions. The correction refreshes only
verified, previously observed unchanged source intervals with exact provenance;
it does not invent unseen source or relax edit matching.

Development comparisons completed with no accepted task in either condition.
The unchanged regex case made import-only edits then fabricated source; the
unchanged JSON case referenced an undefined helper and fabricated later source.
With improved feedback/source refresh, regex still misinterpreted a callback
assertion and proposed an oversized replacement. JSON added a helper but used
an unsupported standard-library keyword; the latest duplicated test diagnostics
then exhausted active Context. Thinking enabled on regex exhausted 4,096 output
tokens in its third request before proposing an edit (220.18 worker seconds).
The off default is retained; these results do not demonstrate improved acceptance.

Before held-out evaluation, a deterministic replay narrowed the JSON Context
failure to duplicated latest pytest diagnostics. Keeping captured primary
exceptions, the outcome tail and nonduplicate stderr reduced the reconstructed
next request from 37,793 to 33,806 bytes, with identical current source regions
and no exchanges omitted. This final feedback projection is tested; it is not a
successful rerun of JSON. The original terminal receipt remains unchanged.

Raw private evidence: `.local/qwen-coding-worker/native-cohort-03/`, including
baseline preflight logs, serving-template readiness, per-turn native archives,
source/diff identities and original-source restoration. Summarized measured
results are in [results.json](results.json).

## Terminal outcomes

| Condition | Task | Accepted | Calls | Input / output tokens | Worker seconds |
|---|---|---|---:|---:|---:|
| Unchanged, thinking off | Regex callback | No | 8 | 59,142 / 1,780 | 127.13 |
| Unchanged, thinking off | JSON duplicate members | No | 10 | 69,319 / 1,440 | 107.12 |
| Improved, thinking off | Regex callback | No | 6 | 36,335 / 2,947 | 146.12 |
| Improved, thinking off | JSON duplicate members | No | 7 | 52,247 / 1,468 | 93.80 |
| Improved, thinking on | Regex callback | No | 3 | 14,724 / 4,864 | 220.18 |
| Final configuration, held-out | Timestamp input contract | **Yes** | 5 | 17,231 / 601 | 35.71 |

Total: 39 calls, 248,998 input / 13,100 output tokens, 730.07 worker seconds and
53,541 source bytes disclosed, within the six-run/60-call/5,400-second budget.
The timestamp candidate passed 19 original tests, all 16 independent behavior
scenarios, strict mypy, Ruff and formatting after one edit. It needed no repair.
Its SHA-256 is
`d2f1f59bc0288cd8623b6d70d4ba5b9677841e828c3c119dcbc671508448dd27`.
Codex independently recommends this local candidate; it remains unintegrated.

Seven admitted edits reconstruct exactly through the existing host parser;
request/response hashes, native call/result correlation, frozen task/oracle
identities and restoration pass for all six runs. Both JSON runs explicitly
omitted older complete exchanges; the held-out and regex runs omitted none.
The improved JSON failure was a budget refusal despite successful reads, with
an already incorrect implementation. The final feedback fix was tested by replay,
not a second JSON attempt. Maximum reported input occupancy ranged from 20.18%
to 37.96% per run; the byte cap is conservative and not a tokenizer guarantee.

Paired acceptance remains **0/2 versus 0/2**. The single held-out success has no
matched old-worker comparator and establishes no acceptance-rate improvement.
Thinking on supported native Tools but hit its final output ceiling before an
edit; provider reasoning-token subtotals remain unknown. No serving profile or
default was changed. There was no Codex comparator inference, model-side
supervisor intervention or manually supplied replacement patch. Codex selected
tasks, reviewed contracts/traces, changed the harness between development stages,
and reviewed terminal candidates. Coordination usage and local energy/cost are
UNKNOWN.

Protected validation: 2,042 passed, two skipped, 100% production branch coverage
in 441.23 seconds; strict mypy 479 files, scoped Ruff/format and layout passed.
The prior regex accepted candidate and duration style-rework candidate retain
their original hashes. Historical held-out outcomes, production main, scientific
branches and the thirteen untracked forensic files remain unchanged.

The next reliability target is coherent multi-region editing and verification
of external API assumptions. Requirement-preserving live repair and a fair,
separately budgeted Codex comparison remain open. Do not count scripted repair
tests or this no-repair held-out success as proof of reliable repair.
