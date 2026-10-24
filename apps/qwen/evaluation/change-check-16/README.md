# Shared change-check16: failed implementation attempt

**check_changes was not delivered.** Qwen submitted no edit; no candidate was
accepted, independently reviewed for publication or installed through closeout.
The unchanged baseline source captured by the worker is not a new implementation.
This is not infrastructure-test success relabeled as an engineering capability.

## Minimum ownership decision and frozen qualification

[Decision](decision.md), [task](task.json), [manifest](manifest.json) and
[results](results.json) preserve the proposed application-level composition.
CodingCommands already exposes Git/run_check through ToolRunner. run_check owns
fixed existing pytest/oracle/Ruff/format/mypy execution over managed Commands;
WorkCycle reuses those checks and owns installation/review/publication/promotion.
The missing operation would bind scoped changes, source/plan/Git identities and
independent categorized checks into one bounded report with a freshness check.
No new framework Tool, executor, generic validation plan or publication API is
needed. This same provider-neutral application ToolRunner boundary can serve
Qwen and future Codex consumers without a Codex executor.

The current task admission only allowed src/devtools implementations, preventing
Qwen from extending this existing app owner. Codex authored a narrow prerequisite
in e48d8c745c2c775d1632762e6374c8783ef40a54: admit explicitly enumerated maintained
application Python source/read/new paths, and authenticate local app imports in
worker/integration runners. Six focused regressions preserve canonical-address,
hash/scope matching and isolated-import behavior. No existing grant is enlarged;
no extra checkout or execution owner is introduced. Qwen authored no semantic
implementation, and this prerequisite is not check_changes.

Python 3.14.3 preflight uses independently authored tiny Git fixtures, not copied
Devtools trees. It confirms pytest fails for VALUE 1 versus required VALUE 2, all
five positive checks pass, actual Ruff F401/import-not-found typing negatives
occur, and source/runner/Git drift is observable. A short Windows temporary-path
canonicalization error was corrected before inference. Thirty-six original
regressions and scoped static checks pass. Post-implementation protocol tests
for new files, scope, exact versions, no changes, missing plans, failure logs,
drift and cancellation were frozen, not claimed already implemented or proven.

## Authentic live outcome

One prospective attempt: 24 requests/1,800 worker seconds/6 proposals/16 components,
32 read/check actions, unchanged byte limits and verified 32K/q4/thinking-off model.
Qwen used 15 requests, 282,701 input/972 output tokens and 253.096 worker seconds.
Twenty read actions succeeded, disclosing 40,998 source bytes/96,850 response bytes.
Qwen found CodingCommands via the first search/lookup and inspected its source,
then repeatedly investigated task and closeout behavior. It never edited.

Before request 16, exact token accounting measured 43,006 tokens in source-preserving
form and 28,489 after maximum existing compaction/reacquisition projection. With
2,048 safety tokens, only 2,231 generation tokens remained, below the 4,096 investigation
minimum. The host correctly refused dispatch: CONTEXT_BUDGET_FAILED. The pending
37-message request retains native relationships; serialized role sizes are
7,895 user/5,428 assistant/54,143 tool bytes (not token counts), plus 4,693 schema bytes.
Nine read-only observations were considered for reacquisition; no whole native
exchanges were deleted. This identifies retained search-history overhead and
unproductive repeated investigation; it does not establish inability to implement
the contract, edit refusal, behavioral repair failure or an invalid oracle.

Source and branch were restored, all 13 forensic files survive, and one canonical
checkout remains. No retry, budget extension, semantic Codex substitute, model
configuration change or speculative harness correction occurred. The operation
and end-to-end demonstration remain missing. The draft additional regressions
are retained in ignored .local state and are not installed as failing tests.

## Verification and next decision

The prerequisite passes 26 focused regressions, scoped Ruff/format and strict mypy
(499 maintained files). The one protected gate passed on the final prerequisite tree: 2367 passed, 2 skipped in 594.15s,100% production coverage. Its result and publication provenance are recorded in results.json. No accepted-Qwen closeout or protected-main merge is claimed.

Next remains delivery of this same shared Tool, not a different feature. Address
the measured non-source search-history replay in the existing projection and/or
the model's investigation stop behavior before a new prospectively bounded
development attempt. Keep this failed receipt immutable and treat the exposed
contract as development, not future fresh confirmation. No new validator,
retrieval framework or memory/planning subsystem is justified by this result.
