# Output policy15: qualified development continuation

The original Cohort02 output-limit obligation is now reviewed and feature-published
at `c93e5bf0f50818a9b9648dc315625af394abdee9`. This is exposed development material, not fresh confirmation.
Original held-out results, requests, proposals and oracle remain unchanged.

## Contract and preflight

Maintained output policy documented invalid integer bounds as ValueError but did
not promise ValueError for wrong types. Current Command arguments, stdin,
environment and successful-exit specifications distinguish TypeError for wrong
types from ValueError for invalid values. Cohort02 imposed ValueError for types
while enforcing unsuppressed Ruff TRY004. Its first proposal passed behavior,
then failed lint; later TypeError and unused hybrid-class repairs failed its
frozen oracle. This is a preventable contract/lint tension, not proof that its
specification was impossible: a justified narrow lint exception could have
preserved that task's requirement. No such public compatibility promise exists.

Before inference, this continuation freezes exactly TypeError for bool/noninteger
values in all three fields; int subclasses are accepted without coercion.
Nonnegative stdout/stderr (including zero) and positive pending-event integers
retain exactly ValueError for invalid bounds. Defaults and immutable/slotted
value/hash/replace behavior stay compatible. No hybrid exception or lint
suppression is introduced. [Task](task.json), [manifest](manifest.json) and
[measured evidence](results.json) retain source/oracle/qualification identities.

Python 3.14.3 preflight passes an independent private value adapter, real unchanged
child/Tool retention fixtures and 116 original regressions. The baseline oracle
fails specifically because bool is admitted. Ruff, formatting and strict typing
are compatible. A sandbox-only pytest temporary-directory access error was
resolved by running the same qualification with required OS access, before
inference. No acceptance expectation changed after Qwen execution.

## Genuine Qwen outcome

One frozen attempt: 20 requests/1,200 seconds/6 atomic proposals/16 components,
24 read/check actions, 8,192 requested output, unchanged byte safeguards and 32K
profile. Qwen used 6 requests, 54,807 input/1,044 output tokens and 73.718 worker seconds.
Eight read/check actions succeeded: 4 direct reads, 2 searches, Git history and baseline
oracle. Source disclosure was 11,834 bytes. One two-region transaction was admitted;
zero refusals, zero repair cycles. Input occupancy peaked at 15,056 tokens; no
whole-exchange omissions. Initial source/Git state was restored by Checkout.

Qwen's private local type validator rejects bool before integer checks and checks
all fields before existing bound comparisons. No worker, Context, edit, serving,
executor, Tool or other Command implementation changed. The first implementation
passes the complete behavior and quality contract. Receiving the baseline failure
before editing is not behavioral repair. This outcome does not establish fresh
generalization, long-session repair or comparative improvement.

## Reviewed maintained publication

Exact Qwen source SHA256:
`543ead05721b8d977b452f0862ced5a4493338d1ac8f80104a0fd97bd54882c8`.
Codex authored 60 permanent regressions; source was not rewritten or reformatted by
Codex. Existing WorkCycle closeout authenticates candidate/scope, validates the
exact installed tree, binds independent review and publishes the ordinary feature
branch. 176 focused cases, scoped Ruff/format/strict typing and the protected gate
pass. Exact gate output/timing and review/commit identities are in results.json.
One protected gate ran; publication reuses its subject-bound passing evidence.
The 13 forensic files and one physical checkout are preserved; no scientific work,
backlog approvals or protected-main promotion occurred. Parent B-0009 stays open.

## Next shared developer-tool increment (not implemented)

Expose a fixed `check_changes` bundle through the existing coding-command and
closeout owners. Bind scoped Git changes and source hashes to the existing
focused test/Ruff/format/mypy validation plan and return one categorized report.
Reuse current Commands, ToolRunner and validation functions, not a new executor
or validator. Qwen and Codex could then request the same coherent pre-review
check with fewer manual commands and less drift between checks and reviewed
source. Review, commit/push and protected promotion remain WorkCycle-owned.
