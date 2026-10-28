# Routine development and bounded delegation

For ordinary authorized single-owner development, use the canonical checkout
directly on main. Authenticate local/remote main, index, tracked changes and
Checkout custody first. Preserve unknown changes and original ignored evidence.
Make coherent commits, validate the final committed executable inputs using the
[protected profile](validation.md), then use an ordinary authorized Git push.
If remote main advances, stop and reconcile rather than overwrite it. Actual
branch protections, required checks/reviews and harness permissions still apply.

Branches and PRs remain useful for risky isolation, parallel work, experiments
and substantial decisions requiring review. They are no longer a routine default.
Never delete experiment, forensic, audit or ordinary branch refs merely because
a commit is reachable from main. A non-destructive reachability inventory is
evidence for a later hygiene decision, not deletion authority.

This convention does not change governed WorkCycle/delegation/integration branch
ownership, exact task/grant scope, Checkout recovery, independent review or
destination publication. Existing path-bound receipts and grants stay historical.

## Practical delegation envelope

An authorized engineering task can cover routine read-only inspection, already
selected tests/checks and bounded source edits without a new human question for
every command. A trusted developer may choose flexible commands within that
role and the actual harness permissions. A less trusted worker can receive only
specific repository scope and immutable check names through typed Tools.

Tool availability and command discovery do not grant authority. The host selects
scope, check argv/cwd/environment overrides, bounds and acceptance requirements.
Separate authorization remains necessary for destructive operations, scope
expansion, external-system changes and publication outside the existing task
envelope. Sandbox approvals and GitHub permissions cannot be bypassed by a
procedure or task-level authorization. Cancellation is not rollback; ambiguous
effects require reconciliation rather than blind retry.

This is a composition boundary for future planners/supervisors, local or external
workers, factual assessment and governed backlog work. It adds no idle daemon,
automatic promotion, task replay, memory database or new WorkCycle permission
system. Codex is one possible external worker, not a required framework owner.
