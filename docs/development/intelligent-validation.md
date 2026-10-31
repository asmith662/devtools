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

For B-0043, preview impact, explicitly select native-host, Context, Tools,
Checkout/WorkCycle, integration and Qwen compatibility groups, and use saved
failed IDs during repairs. Preserve independent review and the final fresh
protected gate. Passing local tests never grants dispatch or publication rights.
