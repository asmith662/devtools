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

Raw private evidence: `.local/qwen-coding-worker/native-cohort-03/`, including
baseline preflight logs, serving-template readiness, per-turn native archives,
source/diff identities and original-source restoration. Summarized measured
results are recorded here after terminal evaluation; none are assumed in advance.
