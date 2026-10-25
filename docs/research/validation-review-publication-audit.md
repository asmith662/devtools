# Validation, review, publication and evidence audit — 2026-10-25

Delivered bounded follow-through: [validation freshness, command receipt custody and Git path identity](../development/validation-evidence-path-repair.md), production `1a9e3ff1e56aebb8522c4d437d46de5f31679389`, PR#17, verified main `ae88c69267961cf6a73bf41454a08cb8f97a14c4`. Committed gate 2903 passed/2 opt-in live skips/100% configured production branch coverage; 265 focused post-main tests pass. Existing proposals d58697fd/84a5d9b1/b0c02dbf retain implemented-and-merged evidence; broader d586 input closure/HEAD/toolchain work remains open. No delivered bounded repair should be repeated. RI93/93,606/606,188 historical obligations and A+C-unapproved status are unchanged. Next Evidence/usage cohort is frozen and not started; earlier pending notices below are dated history.

Reviewed integrated main `5b0bb0b769c2db8d698c86c0e669db820537eec1`.
All ten frozen implementation/test bodies received full review. **Protected
validation reuse is not sound for all inputs it currently permits**: an ignored
but relevant configuration change can inherit old passing evidence and allow an
ordinary feature commit. Existing proposal d58697fd owns this confirmed P1 scope.
Two distinct P2 reliability defects have new pending records. This audit repairs
none of them and does not grant operational lifecycle signoff.

## Exact scope and assurance

The [frozen manifest](code-audit/execution-validation-next-cohort.json) remains
unchanged; its ten blobs match current main. The [version-specific review ledger](code-audit/validation-publication-assurance.json)
records every function, role, test limitation and dependency depth.

| Complete selected bodies | Actual review |
| --- | --- |
| `apps/qwen/commands.py`, `change_checks.py` | Fixed selectors, runners/plan identity, before/between/after checks, Git/index/source joins, durable report projection, freshness, cancellation and error paths. |
| `integration/validation.py` | All fixed pre/post commands, exact target import prelude, raw logs, progress, truncation/timeouts and failure handling. |
| `integration/local.py` | Candidate/result/source admission, independent additions, scoped fresh checks, protected reuse, review subject, commit intent/reconciliation and feature publication. |
| `integration/lifecycle.py` | Complete candidate/plan/authority context, installation/reservation, validation/review, commit/publish/promote/verify, status/refusal, parent/slice decision and backlog closeout. |
| `integration/git.py` | Exact remote observation, raw source blobs, clean state and expected-ref publication. |
| Four frozen test modules | Every helper, fixture, monkeypatch, assertion and failure case in change-checks, local-closeout, integration-validation and integration tests. |

Additional full source review covers IntegrationAuthority/CLI, Commands execution,
handle/result, filesystem writing, usage ingestion and usage storage. Application
loop, WorkCycle, delegation, initial usage reconciliation and dashboard projection
were selected dependencies or reused prior review, not newly complete subsystem
reviews. Other Commands tests were run without blanket body-review credit.

## Actual validation-to-publication ownership

| Boundary | Owner, evidence and invalidation |
| --- | --- |
| Host task → fixed checks | CodingTask binds editable Python paths, tests, Python read inputs, oracle, selectors and limits. CodingCommands owns fixed argv and host-generated runners. Model text cannot supply arbitrary commands. ToolRunner validates then executes; it supplies no task/publication authority. |
| Checks → scoped report | The bundle authenticates source and a bound plan before/between/after checks. `check_changes` additionally observes branch/HEAD/index/status, rejects outside tracked/source/test changes, and hashes full bundle/report evidence. |
| Report → current | `is_current` reloads the actual host receipt, compares the exact supplied projection/task, checks underlying bundle identity and reobserves scoped state. It does not rerun checks or grant review authority. Fresh FAIL is possible; NO_CHANGES is not review-ready. |
| Worker → candidate | WorkCycle checks task/result/source/diff and accepted validation, then produces REVIEW_CANDIDATE. Dispatch admission is not model entry; worker result precedes Checkout release and is not proof release succeeded. |
| Candidate → integration plan | Governed integration authenticates assignment/result/review, pins remote destination/source/merge base, excludes unrelated source ancestry and freezes exact additions, tests, parent scope and target diff. Its supported strategy is destination-based, single-parent publication, not an arbitrary branch merge. |
| Plan → destination validation | Separate authority reserves capacity. Checkout materializes only planned bytes on the pinned destination base. The fixed validator runs oracle/tests/Ruff/format/mypy/protected checks. Source checks and the staged Git tree bind the resulting validation record. |
| Validation → semantic review | A trusted external reviewer supplies decision/reference/rationale. Integration checks the validated staged tree and seals tree/plan/grant/validation identities. It does not invoke a reviewer or prove semantic independence merely by recording `reviewer: Codex`. |
| Review → publication | Fresh authority, parent/tree/footer, clean state and exact remote-ref expectations gate one attributed commit and push. Protected promotion additionally requires repository policy; server requirements remain effective. |
| Publication → closeout | Local/remote destination and identical prevalidated tree are reobserved; focused post checks run. Explicit parent-vs-slice review then authorizes canonical backlog progress. Completion follows verified remote publication, not merely intent. |

Ordinary explicitly authorized developer Git/PR work remains separate from the
accepted-worker API. Maintained WorkCycle uses Git directly; it does not implement
a hosting-service PR/check/review client. Our audit publication uses the normal
operator GitHub workflow, with actual server conditions checked independently.
Local bare-remote probes do not test GitHub API ambiguity or review enforcement.

## Input closure: strong scoped guarantees, incomplete broader claims

CodingCommands binds tests/read hashes against the task baseline, required source
presence, task definition, oracle-derived runners, Python executable/version,
four implementation files, selected root/lint/test configuration and relevant
ancestor configuration/conftest files. Module imports assert the exact selected
source path. Current task checking and final worker acceptance reuse that bound
owner, preserving the previously merged frozen-input repair.

This is a declared scope, not transparent tracking of every file a Python process
reads. Installed package contents, arbitrary environment variables, transitive
data/config inputs and all toolchain dependencies are not universally attested.
Python-only task read paths cannot express every possible non-Python fixture.
Git-tree equality covers tracked representation, not ignored files, installed
tools or process environment. These exclusions must remain visible when deciding
which evidence can be reused or promoted.

The independent real-five-check fixture confirms that unchanged reports remain
current; changing a test, declared dependency, configuration, runner or oracle
selector invalidates them. Unrelated untracked evidence does not invalidate the
scoped claim. Tampered check-report projections refuse. That last case is not a
test of semantic integration review. No universal whole-workspace hash is needed
to preserve these legitimate distinctions.

`validate_tree` is a fixed command executor/recorder, not an input-closure verifier.
Governed Integration adds destination/file/tree checks. It runs pre-publication
checks before creating the final commit; HEAD/worktree-sensitive validation needs
explicit qualification or a committed-candidate check. The present audit has not
demonstrated a HEAD-sensitive failure in retained production publication. The
existing d58697fd acceptance scope now includes that specific remaining question.

## Confirmed findings

### P1 — stale protected-validation reuse: existing d58697fd

`local.closeout_local` derives its subject from result/base/files and can reuse a
previous `protected_validation.passed` record for that subject. An independent
tiny repository first passed an adapter executing an actual Ruff check. Its
ignored `.ruff.toml` then changed from an admitted configuration to an incompatible
required-version. A fresh command using the exact production Ruff selector and
default config discovery exited2. Basic task tests/oracle still passed; local
closeout reused the old record, reported `publication_eligible=True`, and actually
created a feature commit. The review subject stayed equal and the closeout
protected-check dispatch count remained one.

The adapter is explicitly `INDEPENDENT_SINGLE_REAL_RUFF_CHECK_NOT_PROTECTED_GATE`.
It tests the real reuse consumer and commit decision without pretending to run or
fabricate the full production gate. No actual protected-main/remote write or
corruption of a retained historical validation record is demonstrated. Initial
unchanged reuse is a positive control. Existing tracked-tree guards are useful
but cannot prevent this ignored-input drift.

The bounded next repair should refuse reuse unless its supported input profile
is current, or require fresh protected validation until that profile is defined.
Bind relevant selectors/runners/configuration, explicit ignored/read dependencies,
toolchain/environment assumptions and exclusions. Old/unsupported receipts may
remain historical evidence without silently becoming current publication proof.
Keep independent source review and validation freshness distinct. Do not add a
generic validator/cache or silently require every unrelated file to invalidate a
scoped check. Implementation remains a subsequent authorized task.

### P2 — fresh single-check receipt collision

Proposal **84a5d9b1-2bef-47e0-991c-77b4d8cdda49**: a valid fresh CodingCommands
adapter dispatches a real test through ToolRunner into an existing evidence
directory. The command exits0, then saving `coding-command-01.json` raises
FileExistsError. Original receipt bytes survive; the new completed result lacks
its promised archive. The all-bundle/change-report paths avoid existing names,
while the individual path restarts its counter without doing so.

The normal native loop retains one adapter, so this is a demonstrated reusable
host/Tool API defect, not an observed live-worker failure. Reserve a compatible
unused evidence identity before entry or refuse before execution. Reuse the
existing application owner; do not introduce another execution or logging layer.

### P2 — Git presentation mistaken for path identity

Proposal **b0c02dbf-0eab-47fd-bcc6-5d503d7d65fd**: actual Integration `_files`
rejects a legitimately staged `tests/test_π.py` with exactly planned bytes under
real Checkout. Plain Git output quotes and octal-escapes its UTF-8 name;
the validator compares that presentation to the literal plan and reports an
unapproved file. NUL-delimited output independently returns the exact path.

This is conservative false refusal, not unauthorized publication. Use managed
Git's existing `-z`/untrimmed semantics in relevant population/replay joins, keeping
scope checks strict. Similar line-based joins in local committed replay need
bounded follow-up, not assumed automatic proof of the same executed failure.

## Review, publication, durability and accounting conclusions

The governed path binds review to the staged validated tree, plan, grant and
validation receipt; local closeout binds source/result/base/files. Neither path
automatically performs semantic review. The trusted caller must actually inspect
task objective, diff, additions, ancestry, outputs and limitations before submitting
a genuine decision. Constructed fixture decisions prove plumbing only. Hashes
detect corruption/rebinding under trusted local custody, not a fully forged
population or a malicious same-user administrator.

The real local bare-remote probe lost acknowledgment after a successful push.
Retry observed the intended commit and issued no second push. An independent
remote advance then refused without overwrite. Parent/tree checks and explicit
authority live above this exact-ref helper. A publication exception is not proof
that nothing happened. Existing integration tests add commit/push resume, partial
installation, expired/revoked grants, failed post-checks and parent-close controls,
with protected validation and semantic reviews explicitly substituted.

Individual filesystem writes use a sibling temporary file, flush/fsync and atomic
replace, without parent-directory fsync. That protects ordinary readers from
partial replacement; it is not a cross-record/Git/remote transaction or guaranteed
power-loss durability. Immutable intents precede effects; result/phase records
follow effects. Missing completion remains reconciliation-required. Interrupted
pre/post validation retains reservation and partial logs rather than blindly
repeating. Coding/validation reservations are authorized worst-case capacity,
not observed usage or automatically refundable failed attempts.

Commands executes once per live handle; that does not mean exactly-once effects
across new handles/processes. It kills/reaps the immediate child on timeout or
cancellation, not all descendants, and retains no fabricated completed result.
Output is bounded with explicit truncation; the integration gate refuses truncated
capture. Dropped live events do not invalidate complete retained bytes, but cannot
be treated as a complete event history. Partial output on exceptional completion
requires observed events/progress, not a nonexistent CommandResult.

WorkCycle's missing result preserves unknown model usage; dispatched admission
does not prove entry. Application totals propagate unknown categories rather than
turning them into zero. The independent arithmetic control returns2+3=5 and
2+UNKNOWN=UNKNOWN; it is not complete usage-ledger verification. Worker JSON and
selected dashboard projections are real consumers, but do not automatically
populate the framework's normalized usage/Evidence store. B-0011/B-0034 receive
append-only consumer/effect evidence, with deferred states unchanged. Broader
custody0385a359 remains sufficient; no cleanup or new persistence layer is needed.

## Validation and remaining program

[Tests](code-audit/validation-publication-tests.json): **252 passed**, exit0,
513.06 seconds pytest/515.35 seconds managed, no truncation. This includes the
four fully inspected modules and executed Commands dependencies. The [probe
artifact](code-audit/validation-publication-probes.json) retains source, identities,
actual outputs, profile limits and corrected harness errors. No model, frozen
scientific controller, real grant or protected-main fault injection ran.

[Intake](code-audit/validation-publication-intake.json): two new P2 proposals and
two append-only advisories, including the material confirmed P1 update to existing
d58697fd; two existing B-story evidence additions, no state changes. All prior RI,
binding, worker and Checkout corrections stay delivered. Do not schedule them again.

[Checkpoint](code-audit/validation-publication-checkpoint.json) authenticates exact
Git blobs, JSON/links/layout/Intake/whitespace, unchanged executable inputs and
all thirteen forensic hashes. No new protected gate is required or claimed for
this documentation-only checkpoint. The ce1a8ea5 gate remains prior repair evidence.

Operational signoff is blocked by the demonstrated reuse defect and incomplete
durable/semantic-review assurance. Prioritize its bounded repair, with the P2
records retained separately. Then take the [frozen Evidence/usage/consumer cohort](code-audit/execution-evidence-next-cohort.json).
It is not begun. Subsequent Persistence, Core/Resources, Models/Agents,
applications/dashboard and tooling audits remain necessary. RI fixtures93/93,
experimental source606/606 and188 historical obligations are unchanged. A+C
remains unapproved; this checkpoint is not a successor-session dossier.
