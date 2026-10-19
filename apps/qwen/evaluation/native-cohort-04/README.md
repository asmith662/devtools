# Verified coordinated engineering — prospective cohort 04

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
authority. Measured results and source identities are recorded after execution.
