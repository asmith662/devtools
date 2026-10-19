# Governed development integration

`WorkCycle.integration` is the repository administrator for an accepted worker
candidate through verified destination publication and canonical work progress.
It extends the existing work item, coordinator, Intake writer and immutable
content-hashed operational records. It is not a framework scheduler, executor,
second backlog or source of human authority. Coding delegation and
`ACCEPT_RECOMMENDED` do not confer integration permission.

## Lifecycle and ownership

| Phase | Required evidence / effect |
| --- | --- |
| CANDIDATE / SUPERVISORY_REVIEW | Existing assignment, coding authorization, accepted result, exact source/diff and Codex `ACCEPT_RECOMMENDED` authenticate. |
| INTEGRATION_PLAN | Read-only destination ref, original source, merge base, excluded source commits, target diff, final file bytes/authorship, tests and parent obligations are frozen. |
| INSTALLED | Separate standing integration authority reserves allowance and installs exact bytes in an ordinary isolated worktree based on the destination. |
| VALIDATED / REWORK_REQUIRED | Host-owned acceptance, focused tests, Ruff, formatting, strict mypy and the protected development gate run against the installed tree. Failure never inherits candidate approval. |
| APPROVE_INTEGRATION / REJECT | Codex records a decision, rationale and reference against that exact validated Git tree, plan and grant. |
| FEATURE_PUBLISHED | One attributed commit is created and its exact remote feature ref verified. |
| TARGET_PROMOTED | The reviewed commit advances the pinned destination using an exact expected-ref lease. |
| DESTINATION_VERIFIED / POST_INTEGRATION_FAILED | A separate detached worktree authenticates the actual destination tree and reruns acceptance/focused tests. Protected validation is reused only for the identical tree. |
| COMPLETION_REVIEWED / VERIFIED_COMPLETION | Explicit Codex parent-vs-slice review precedes committed/pushed canonical backlog progress and verified publication. |

The worker remains responsible for coding and bounded repair. WorkCycle owns
integration sequencing and progress. Core paths/time, filesystem atomic writes,
managed commands and Git own their existing responsibilities. The designated
coordinator remains the single writer. Integration uses no model calls.

## Plan and source identity

Call `await cycle.integration.plan(item, accepted_review_sha, spec)` or use the
existing CLI. The closed JSON specification has:

```json
{
  "remote": "origin",
  "destination": "main",
  "feature": "feat/integrate-reviewed-slice",
  "worktree": "C:/absolute/unused/integration-worktree",
  "additions": [],
  "parent_complete": false,
  "remaining": ["Explicit unresolved parent obligation"],
  "rationale": "Integrate the reviewed slice, preserving parent scope",
  "validation_seconds": 900
}
```

Each optional addition is `{path, text, author, reference}`. Tests must be exact
`tests/*.py` resources; a separately authorized correction may replace the one
candidate source. Original Qwen bytes/diff/review remain immutable. Independent
test/correction authorship and provenance are recorded in the plan and commit.
No later change inherits the old exact-tree review. Test code is executable
host-reviewed code; a grant must explicitly cover its path and the pinned task
oracle. Arbitrary model-authored commands are never accepted.

Planning requires the destination's original source to agree with the frozen
worker baseline (allowing Git LF/CRLF checkout representation). Candidate
installation and pre-publication validation preserve exact captured source bytes. Git tree
identity separately authenticates committed representation. The plan retains
the original candidate/diff identity, destination source digest and normalized
target diff. Both evidence identities remain visible.
Post-promotion checkout first authenticates that exact reviewed tree. It permits
only Git's LF/CRLF-equivalent checkout representation, rejects other content
changes, and records both planned and materialized byte hashes. Thus a new LF
regression file may be checked out as CRLF without replacing its original
evidence identity or turning a newline conversion into a scientific/code change.
Acceptance and protected-gate launchers explicitly bind imports to the selected
checkout. The canonical protected script runs unchanged; an editable installation
in the coordinator environment cannot substitute different implementation bytes.

The supported strategy is a reviewed, destination-based, single-parent commit.
It deliberately excludes all unrelated commits from the worker's source branch.
Diverged source refuses; an advanced destination refuses target promotion and requires
a new explicit plan/review. No implicit rebase, whole-feature merge, conflict
resolution or history rewriting occurs. Remote branch protections still apply;
a server requiring a PR refuses this direct operation. This increment does not
bypass it or automate a hosting-service PR workflow.
The implementation uses Git's existing [worktrees](https://git-scm.com/docs/git-worktree)
and [expected-ref leases](https://git-scm.com/docs/git-push). Parent/tree checks
separately ensure that promotion advances the reviewed base rather than
replacing unrelated history.

## Separate standing integration authority

[`integration-policy.example.json`](integration-policy.example.json) is an
**inactive proposed B-0048 policy**, not an issued grant. It covers the object
candidate and explicitly named independent regression path, one integration,
bounded file/byte counts and two bounded validation phases. The printed grant
also binds local principal/provenance, expiry, coordinator/administrative branch,
existing remote URL, Codex supervision and exact destinations. Policy actions
separately permit installation, validation/test additions, feature commit/push,
destination promotion, verification and closeout. Source corrections and full
parent closure are separately denied by this example.

The host uses the existing default-No trusted-terminal boundary. No `--yes`
policy bypass exists. From the designated coordinator, the maintainer can issue
or revoke a grant with genuine consent:

```powershell
uv run --python C:/Python314/python.exe python -m scripts.backlog integration-issue --policy docs/backlog/integration-policy.example.json --reference 'Actual maintainer integration decision and scope' --expires ([DateTimeOffset]::UtcNow.AddDays(1).ToString('o'))
uv run --python C:/Python314/python.exe python -m scripts.backlog integration-revoke <grant-sha> --reference 'Actual maintainer revocation decision'
```

The example names main, so its promotion additionally requires a separate real
repository-policy decision. `main` and `master` are locally protected by default:

```powershell
uv run --python C:/Python314/python.exe python -m scripts.backlog integration-protection --remote origin --destination main --reference 'Actual protected destination policy decision' --allow
```

This command also defaults No; omission of `--allow` removes the local permission.
The grant must independently set `protected: true`. Server-side protections are
never changed. Other named branches retain server protections and exact grant
selectors. Grant issuance/revocation do not dispatch a worker or install code.
Changing policy files cannot expand an issued content-hashed grant.

At every stage authority is reauthenticated, including before consequential
publication after validation. Revocation prevents later stages; it cannot undo
an already dispatched Git operation. Reservations consume the worst-case
integration count, per-integration file/byte limits and twice the admitted
validation time. No refunds or automatic retries follow uncertain effects.
All local-host administrative records share the existing trust boundary; hashes
detect corruption/rebinding, not compromise of the same operating-system user.
Installation binds the plan to its reserving grant for all later stages. A new
grant cannot inherit another grant's reservation, review or pending effects.
Expiry/revocation therefore stops an in-flight integration for explicit
reconciliation; no automatic grant transfer or implicit renewal is supported.

## Operating sequence

After a genuine grant exists, Codex performs real review and invokes the fixed
commands below with actual references/rationale. No repeated terminal approval
is needed within that grant:

```text
python -m scripts.backlog integration-plan B-0048 --review <accepted-review-sha> --spec <host-reviewed-spec.json>
python -m scripts.backlog integration-install B-0048 <plan-sha> --grant <grant-sha>
python -m scripts.backlog integration-validate B-0048 <plan-sha> --grant <grant-sha>
python -m scripts.backlog integration-review B-0048 <plan-sha> --grant <grant-sha> --decision APPROVE_INTEGRATION --reference <actual-review> --rationale <scope-tree-tests-ancestry-assessment>
python -m scripts.backlog integration-publish B-0048 <plan-sha> --grant <grant-sha>
python -m scripts.backlog integration-promote B-0048 <plan-sha> --grant <grant-sha>
python -m scripts.backlog integration-verify B-0048 <plan-sha> --grant <grant-sha>
python -m scripts.backlog integration-close-review B-0048 <plan-sha> --grant <grant-sha> --decision SLICE_ONLY --reference <actual-completion-review> --rationale <remaining-obligations>
python -m scripts.backlog integration-closeout B-0048 <plan-sha> --grant <grant-sha>
python -m scripts.backlog integration-status B-0048 <plan-sha>
python -m scripts.backlog work-status B-0048
```

Use Python 3.14 with the existing development dependencies. Validation commands
are fixed host code; the pinned B-0048 oracle additionally invokes the existing
Python 3.12 interpreter. A missing interpreter/dependency is a failed gate,
not permission to relax acceptance. Before closeout the administrative branch
must be clean and synchronized; unrelated work is never staged. The coordinator
and destination branches must be distinct; planning refuses otherwise.
Full parent closure requires
`parent_close`, a complete plan with no remaining obligations, and explicit
`COMPLETE_PARENT` review. Partial integration leaves canonical status BACKLOG
and appends commit, validation, review and outstanding-work evidence.

## Recovery, evidence and limitations

Work records extend `.local/backlog/work/<B-id>/integration/<plan-sha>/` with
`backlog-integration-<phase>-v1` hashes. Grants/reservations remain under the
existing `.local/backlog/` administrative state. Intents precede external
effects. Interrupted/duplicate installation, commit/push, target promotion and
backlog publication inspect exact bytes/parents/trees/refs and reuse the same
commit. Divergence or ambiguous state is `RECONCILIATION_REQUIRED`; never reset,
force overwrite or blindly dispatch a replacement operation.

Interrupted pre/post validation retains its reservation and partial progress/logs
and stops for reconciliation/new reviewed plan rather than rerunning automatically.
The existing coordinator writer lease also fails closed after a crash; reconcile
its ownership using the existing Intake procedure before another mutation.
Failed validation is inspectable and supports a separately attributed rework
plan. `progress.json` and per-command logs retain timestamps, durations, command
identities, complete captured output and explicit bounded excerpts/truncation.
Raw log bytes, including non-UTF-8 output, are preserved exactly; only the
operator excerpts use replacement decoding.
Post-promotion failure cannot automatically roll back a published commit.
Receipts retain prior commit and `git revert` provenance; a revert needs separate
authority and review. Local Git worktrees are preserved, never automatically
cleaned or deleted.

`WorkCycle.status()` adds an `integration` projection with plan/destination,
recorded disposition, pending intents, chronological phase evidence and parent
scope. Existing worker outcome fields are unchanged. The dashboard branch's
current projection selects only older work fields; its UI does not yet render
this additive integration history. It can consume this authoritative projection
without adding storage. No dashboard source or data is changed here.
The status `sha256` still identifies the original worker receipt, not the whole
expanded projection; each integration record has its own authenticated hash.
CLI refusals preserve bounded error/provenance records. A refusal with a pending
effect remains reconciliation-required; a refusal before effects is BLOCKED.
Git failures retain bounded stderr so a server protection or transport refusal
is distinguishable from successful publication. Direct Python callers receive
the original exception and can record it through `integration.refusal()`.

The [first actual B-0048 plan](b-0048-integration-readiness.md) authenticates the
candidate, excludes ten unrelated source commits and is truthfully blocked by
missing integration authority. No real source is installed during preparation.

Disposable Git fixtures exercise actual installation, commit/push, target ref
promotion, verification sequencing and canonical closeout, including protected
policy, failures and interruption. Their expensive validation runner is explicitly
scripted; separate tests verify the shipped fixed command gates, and the actual
protected development profile validates this implementation. Synthetic evidence
does not establish a real integration grant or a newly completed Qwen task.
