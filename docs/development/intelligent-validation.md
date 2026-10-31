# Intelligent validation delivery

Starting canonical and remote main: `ff9a17885b2e65034b606da85ba1c8da25a7bafb`.
Inspector was independently registered on `feat/agent-inspector`; its files,
branch and worktree are outside this assignment. Pre-existing untracked
source-grounding artifacts remain owned by their original session.

The retained coding-host decomposition receipt records 3,948 passes, two optional
skips, 100% configured production branch coverage and 1,667.514 seconds command
time (pytest: 1,665.13 seconds). Its focused run records 447 passes in 58.04
seconds. These are different selections, not an isolated coverage benchmark.
They demonstrate approximately 96.5% less elapsed pytest time for that historical
focused selection. Neither log contains per-test timings. No honest attribution
of the 28 minutes to individual fixtures follows from those logs.

Source inspection finds serial pytest execution, real interpreter startups in
Commands/Tool timeout tests, authored Git repositories in Checkout/WorkCycle
tests, repeated repository/index construction and full branch instrumentation.
These are plausible costs, not measured proportions. Integration validation
intentionally runs an oracle, focused tests and protected tests before publication;
the focused oracle and full gate express different contracts. This assignment
does not delete either contract. Ordinary focused development now avoids repeated
full-suite and global coverage execution. Receipts retain individual phase times
so subsequent fixture optimization can be evidence-driven.

No parallelism is enabled: Windows spawn, Git/SQLite/temp isolation and shared
resources need a separate measured safety case. No cache is treated as proof of
current results. The selector is a repository developer script consuming existing
Commands, time, paths and atomic filesystem writing, not a new framework
dependency graph, Evaluation store or lifecycle. There is no production API,
durable compatibility or architectural ownership change. B-0043 and Inspector
implementation remain outside scope.

## Measured delivery

The [machine receipt](../research/code-audit/validation-workflow-20261031.json)
retains authenticated executable inputs, environment qualifications, every test's
phase outcomes/timings, module totals and scenario selections. Final committed
executable candidate: `76b3db55` (full identity in the receipt). Protected result:
3,966 passes, two optional skips, 100% configured production line and branch
coverage, 1,760.69 seconds including managed child execution. This does not claim
the comprehensive suite became faster; the everyday loop avoids its cost.

Measured cumulative module phase time is concentrated in backlog integration
(468.14 seconds), Qwen change checks (191.69), Checkout (151.53), coding loop
(117.88), delegation (107.53), WorkCycle (101.09) and local closeout (86.01).
The slowest individual call is the complete Git/integration/parent-closeout
scenario at 37.15 seconds. Setup costs are separately retained in the receipt;
fresh mutable Git/Intake/Checkout fixtures and repeated real interpreter/check
execution dominate these groups. Increasing fixture lifetime would share mutable
governance state, so no such optimization is activated. Coverage overhead has not
been isolated with an A/B experiment. Teardown is a small measured contribution.

| Scenario | Selection / observed tests | Timing and assurance |
| --- | --- | --- |
| Narrow benchmark-storage implementation | 3 groups / 507 tests | Actual no-coverage impact execution: 8.11 seconds pytest; receipt includes command wall time |
| Coding-host/Tool protocol | 16 groups / 1,634 tests | 1,679.82 seconds cumulative phases in protected run; uncertainty requires review |
| Shared Context planning | 89 groups / 2,563 tests | 1,697.48 seconds cumulative protected phases; uncertainty requires review |
| Test-only development | 18 selector tests plus 2 protected-command controls | Actual focused execution: 1.09 seconds pytest |
| Failed regression then repair | 31 tests, failed IDs plus correction impact | Actual recovery execution: 3.73 seconds pytest; original failure retained |
| Broad architecture/configuration | Full 3,968-test population including skips | Comprehensive acceptance mandatory; actual final run above |

Phase sums are observations within the instrumented full run, not separately
executed focused wall benchmarks. Narrow impact execution avoids 3,461 other
test instances from that population and about 99.5% of the historical/full wall
cost; it does not pass those omitted tests. Broad shared changes can legitimately
retain almost the entire runtime despite selecting fewer tests. There is no
claim that every change can be validated in seconds.

An initial complete invocation passed all 3,965 then-current tests but failed
coverage at 96.19%: the frontend had imported framework modules before pytest
started instrumentation. That command remains failed in its own receipt. A
fresh managed interpreter now starts pytest/hooks before framework imports, with
isolated coverage data. A tiny authored import-time coverage regression verifies
the correction. Focused diagnosis/repair preceded the second complete invocation;
the final success applies only to the corrected committed candidate. No threshold
was lowered, failure erased, or historical full result reused as acceptance.

Safe speed improvements are scoped no-coverage execution, static impact preview
without RI index construction, deduplication of covered targets, saved failed-ID
recovery and avoiding unconditional repeated full commands. Durable phase timing
supports later fixture optimization. No existing test contracts, production code,
WorkCycle/integration gates, historical results or external services were changed.

For B-0043, preview impact, explicitly select native-host, Context, Tools,
Checkout/WorkCycle, integration and Qwen compatibility groups, and use saved
failed IDs during repairs. Preserve independent review and the final fresh
protected gate. Passing local tests never grants dispatch or publication rights.
