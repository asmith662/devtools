# Verified coordinated engineering — measured cohort 04

Frozen definitions use source baseline `39a3fd95900a583d1b8578523dd6acd8b86ba038`.
Two new development tasks exercise overlapping regex iteration across related
functions and explicit text-codec error policies across encode/decode. A separate
held-out public whole-string regex API requires coordinated changes to source and
the package export. None reuses a historical held-out solution.

The legacy and coordinated development definitions share exact objectives,
source/read scope, baseline hashes, oracle, regressions, managed strict typing,
Ruff/format and model/time/action limits. The improved condition adds the declared
installed API observations and coordinated proposal protocol; this bundles two
capabilities and does not isolate either mechanism. One non-seeded paired sample
per task is exploratory. The manifest records exception/quality compatibility
review; preflight verifies intended baseline failures and passing original checks,
not specification satisfiability. Host oracle content is never in model prompts.

Maximum cumulative budget: six runs, 60 model calls, 5,400 worker seconds. Each
run retains ten model calls, eight combined Context/API actions, three proposals,
4,096 output tokens per call, 300 seconds per call, 900 seconds overall and the
unchanged 32K Qwen3.8-27B IQ4_XS profile, thinking disabled. Four paired development
runs precede configuration freeze and once-only held-out execution. The sixth
slot is reserved only if a separately frozen repair-only case is needed; genuine
validation-feedback repair already occurs in the two unchanged controls.

Raw evidence remains in `.local/qwen-coding-worker/native-cohort-04/`. Original
cohorts 01–03 and their duration, regex and timestamp candidates remain unchanged.
Local results do not confer production integration or protected publication
authority. Exact source/receipt identities, per-turn native actions, checks and
costs are in [results.json](results.json).

## Actual outcomes

| Condition | Task | Full acceptance | Calls | Input / output tokens | Seconds |
|---|---|---|---:|---:|---:|
| Unchanged | Regex overlap | No; behavior passed, typing failed | 7 | 48,158 / 3,532 | 198.17 |
| Unchanged | Text codec policy | No; encode incomplete | 5 | 35,750 / 1,213 | 84.91 |
| Initial coordinated | Regex overlap | No; read-budget failure | 3 | 12,473 / 629 | 37.88 |
| Final coordinated | Text codec policy | **Yes**, two regions | 3 | 14,090 / 2,014 | 98.37 |
| Final coordinated | Regex overlap | **Yes**, one real repair | 4 | 25,256 / 1,924 | 101.15 |
| Held-out final | Whole-string/public export | **Yes**, two files | 5 | 36,583 / 1,505 | 81.66 |

Controls used code-equivalent `39a3fd95` (data-only freeze `6783b438`); initial
transactions used `2760b7cf`; final development/held-out used `06c394cb`. The
initial improved regex run inspected both required APIs, then executed two reads
before an oversized batch exhausted the remaining allowance. The tested fix
refuses the entire batch before dispatch. The [prospective amendment](development-amendment.json)
allocates the reserved sixth slot to final regex evaluation after that code
change; the failed receipt and original checks remain unchanged. Final live runs
did not require batch recovery, so its proof is deterministic, not live success.

Final paired acceptance was **0/2 versus 2/2**. Text passed eight regressions,
13 independent behavior checks, typing, Ruff/format in one two-region transaction.
Regex's first edit failed overlap behavior, E501 and formatting; its second
changed the progress rule and passed all 14 behavior checks, four regressions,
typing and quality. This is genuine behavioral/quality repair without a Codex
patch. The once-only held-out case passed four regressions, 11 independent public
API checks, typing of both files and Ruff/format in one atomic transaction.

Six runs used **27 calls, 172,310 input / 10,817 output tokens, 602.14 worker
seconds**, including 585.93 model-response seconds, 39,565 source bytes and seven
authenticated API observations. All remain within the original cumulative limits.
No profile, weights, thinking or Context/output limit changed. Cache/reasoning
subtotals, Codex coordination and monetary/energy costs are UNKNOWN.

Independent in-memory replay verified six runs, ten applied proposals, twelve
exact anchors, API digests, native correlation, combined patches and final bytes.
All source was restored. Thirteen historical receipts and the prior duration,
regex and timestamp candidate hashes were verified. Final accepted runs omitted
no exchanges; controls explicitly omitted some older groups. Peak reported input
occupancy stayed below 35% of 32K. No candidate was installed into maintained code.
The two regex snapshots overlap one baseline file and require composition and
revalidation before authorized integration.

Protected validation ran once: **2,063 passed, two skipped, 100% production branch
coverage, 459.74s**. Strict mypy passed 482 files; relevant Ruff/format/layout,
seven React tests, TypeScript and frontend build passed.
This protected gate validates the maintained worker after source restoration;
it is not combined production validation of the unintegrated task candidates.
Those candidates received their frozen focused checks during isolated evaluation.

This is a small non-seeded paired sample with bundled changes, fixed order and
one development repetition. Held-out shares a source package with development,
but has a distinct frozen objective, fresh conversation and original baseline.
There is no reliability-rate, causal-mechanism or Codex-parity claim. Next: fresh,
more diverse multi-module/API-dependent tasks and repeated requirement-preserving
repair under fixed independent acceptance. Qwen remains primary.

Current scope is existing Python implementation files and the fixed stdlib API
allowlist; new-file creation and arbitrary package introspection are refused.
The production governed assignment-v1 still requires one file. These explicit
boundaries do not grant broader integration or protected publication authority.
