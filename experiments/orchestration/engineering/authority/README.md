# Plan validity and execution authority correction

This bounded engineering correction separates prospective plan validity from
maintainer authority. EXPERIMENT_CONTROLLER remains COMPLETE. Production behavior,
accepted scientific results and historical population selection are unchanged.
PURPOSE_RELATIVE_SOURCE_GROUNDING remains NOT_STARTED. No Cases 0020-0022,
scientific plan, treatment acquisition, gold or Stage D result are created here.

## Problem and contract

At `c26d8efaf89ec8bcbe999be23a103e233016a801`, `plan` called an authentication
path that required a committed `approved: true` receipt. This conflated validity
and authority. A single Stage A/plan commit also cannot contain its own Git hash.
The preceding read-only validation stop and these source checks are accepted
problem evidence, not scientific results.

The corrected workflow uses a Stage A commit, then a separate prospective plan
commit naming it. Both constitute Gate 1's review package. `plan` authenticates
canonical committed bytes, exact Stage A and disclosed case/implementation inputs,
then returns PLAN_VALID, EXECUTION_AUTHORIZED = NO and the exact prospective run
ID. It neither creates approval nor launches workers.

After review, `run <plan> --approve <exact-run-id> --work-root <external-root>` is
one explicit maintainer action. It authenticates clean synchronized main, publishes
an immutable approval commit/push and reauthenticates its durability before any
scientific ENTERED event. The receipt binds schema, plan digest, unchanged run ID,
exact Stage A, controller implementation, plan/review commits, authority decision,
audit Timestamp and content digest. Approval changes no plan bytes or run identity.
Commit/push failure preserves state and authorizes no scientific entry. No rollback,
force push, automatic push retry or scientific replacement attempt is introduced.

The Python seam accepts a host-supplied `ApprovalRequest` and returns a committed
`ExecutionAuthorization`; after restart it authenticates the existing receipt.
`run()` without the explicit value rejects even if a receipt exists. A future
Agent may validate a plan, but its trusted host must supply the authority decision;
grant issuance must not be exposed as a model capability. These local values are
not a security sandbox against arbitrary Python or holders of repository write/
push credentials. That existing trust boundary is explicit rather than disguised
as human identity authentication by string fields.

This remains experiment-owned infrastructure. Taxonomy/architecture distinguish
validation, availability and approval from authority; framework governance remains
reserved, and B-0038 remains a deferred generic investigation. No framework
governance primitive, Agent Tool, Runtime lifecycle or production dependency is
added. Dependencies remain experiments -> devtools for canonical time, paths,
filesystem and managed commands. The [operator guide](../../README.md) and
[adapter contract](../../CONTRACT.md) own the current public behavior.

## Compatibility and recovery

Plan schema v2 removes the old approval locator/status dependency. Legacy v1
plans remain canonically parseable for inspection; their Boolean receipts cannot
authorize new execution. The original engineering report, measurements, validation
and integrity bytes remain historical records at their original checkpoint.
Current implementation integrity is separate in this directory. Cases 0017-0019
predate controller execution and retain read-only adoption without retroactive
approval or scientific replay.

An approved never-entered run may start using the existing receipt. Completed
operations authenticate and skip on resume. Entered/unreturned or failed operations
remain dead and cannot be resurrected by a new approval. `.local`, worker handoffs,
progress and caller-supplied token contents alone never supply authority. Git
receipts and exact prospective inputs must authenticate on every execution/restart.

## Validation evidence

The separate [validation record](validation.json) records the final focused/full
controller tests, fake three-case lifecycle, temporary-Git failure probes, restart/
dead-attempt tests, read-only adoption, protected development validation, static
checks and diff checks. The synthetic fixture proves separate A/plan commits,
unapproved validation, denied entry, explicit durable approval, stable run ID,
parallel fake execution, reconstructed status and committed verification.
No test invokes a live semantic worker or scientific effectiveness treatment.
Prior fixtures now pass explicit authorization. In particular, cache probes use
separately approved synthetic attempts; an unapproved controller cannot enter
preparation merely because its cache key matches. Concurrent authority inspection
does not temporarily remove an active grant. Resume rejects a run context naming
an approval checkpoint other than its authenticated receipt.

The complete controller scope can be reproduced with
`uv run pytest --no-cov experiments/orchestration/tests`. Final validation uses
three bounded, disjoint pytest partitions covering that same scope. The earlier
development sweep exposed the old unapproved-cache fixture and the focused
authority sweep exposed malformed-timestamp exception normalization; both were
corrected without weakening execution guards. Final commands/counts are retained
in the validation record, separately from those development failures.

## Next action

Resume source-grounding Stage A in a separate task. Publish the scientific
checkpoint first, then the prospective unapproved controller plan checkpoint.
Validate and return both checkpoints and the exact run ID for maintainer review.
Do not execute that run during the Stage A task. SEARCH_POLICY_FAILURE remains
NOT_ASSESSED; LIVE_INCREMENTAL_RI remains REQUIRED / NOT_IMPLEMENTED. Confirmation,
reserve and historical child holdouts remain NOT_ACCESSED.
