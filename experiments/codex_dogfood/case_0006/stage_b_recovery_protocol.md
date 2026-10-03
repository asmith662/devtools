# Case 0006 Stage B Recovery Protocol

**FROZEN BEFORE RECOVERY EXECUTION.** Stage A treatment remains byte-identical at `e7aed4162672dd859a0a8a33a2b718dda8425495`.

Recovery identity: `case-0006-stage-b-recovery-1`.

This is a second execution of the exact unchanged Stage A treatment, authorized only because Attempt 1's post-treatment capture failed before native outputs were persisted. It is not the original exactly-once Stage B execution.

Maximum additional treatment executions: **1**. This single recovery may call lexical acquisition once, routing once, each of the nine grounding requests once, and generation once (the minimum production plan execution). If this recovery executes treatment and capture fails again, do not retry. Mark Case 0006 capture-failed and use a new prospective case.

The authorization in this committed protocol is the sole additional execution allowance. No treatment operation was run while preparing or validating this checkpoint.

The corrected correspondence validator matches complementary members by frozen member identity/key and checks the exact key set and each member's frozen grounding request, projection, and key. It does not depend on constructor presentation order and does not relax semantic recipe validation.

Before production calls, the harness writes an exclusive recovery-start marker. After each successful native operation it writes an `INCOMPLETE_UNVALIDATED` raw checkpoint to `stage_b_recovery_raw.pkl.gz`, retaining prior native values, invocation counts, runtimes, Stage A identity, and recovery metadata. Updates use a same-directory temporary file and replacement; the checkpoint itself remains explicitly incomplete and cannot be mistaken for canonical Stage B output. If a raw checkpoint exists, the harness resumes from the first missing operation and never repeats completed operations. If all production results exist, it performs validation/finalization only. A start marker without raw results blocks another treatment execution. Existing canonical outputs always block entry.

Only after correspondence and target-origin validation succeeds may canonical outputs be created with exclusive file creation. Each canonical artifact carries `execution_kind=RECOVERY`, `recovery_id=case-0006-stage-b-recovery-1`, and `prior_failed_execution_count=1`. Raw recovery material and the start marker remain as the audit trail. A finalization failure may be resumed read-only from raw material; no operation is repeated.

The checkpoint records execution mechanics only. It does not adjudicate resources, evaluate effectiveness, inspect candidate quality, repair a failed grounding/recipe, or access confirmation outcomes.
