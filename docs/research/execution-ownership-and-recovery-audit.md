# Checkout, WorkCycle, delegation and recovery audit — 2026-10-25

Delivered follow-through: [Checkout fencing, exact recovery consent and filesystem custody](../development/checkout-custody-repair.md), production `ce1a8ea523cdfe9772c7e8b5ed0479528d3aba50`, PR#14, verified main `f54b4a0a6d1b81be805b2d1d63ea43f23df0100a`. Full committed-tree gate 2889 passed/2 opt-in live skips/100% configured production branch coverage. Proposals69688104/30bd833e/3b2f566b retain implemented-and-merged advisory evidence; do not repeat these repairs. Broader custody, check-input closure and cohesion remain separate. RI93/93,606/606 and188 historical obligations are unchanged. A+C remains unapproved; the next frozen validation/publication audit has not begun. Earlier pending-repair statements below are dated history.

Reviewed integrated main `264915928a9045795d5e07c728ffa1aaba4c1704` in the
canonical checkout. The nine frozen source/test versions have received complete
body-level review. **Three independently reproduced P1 Checkout defects remain
unrepaired.** No production source, tests, configuration, authority or scientific
artifact changed in this audit. Operational lifecycle signoff is not justified.

The existing architecture separates task authority, source serialization, worker
acceptance, review and publication. Much of that separation is implemented and
tested. Recovery has two owner/consent race windows, and branch admission misses
an ignored dangling filesystem entry. These are bounded defects in existing
owners, not evidence that a new execution architecture is needed.

## Evidence and exact scope

The [frozen manifest](code-audit/execution-ownership-next-cohort.json) remains
unchanged. [Exact path/blob/function review records](code-audit/execution-ownership-assurance.json)
extend the existing code-audit ledger. They distinguish these nine complete
bodies from additional full source review and selected dependency traversal.

| Complete selected body | Assurance and limitation |
| --- | --- |
| `scripts/backlog/checkout.py` | Initial claim, root/path/branch/source admission, expected-byte journal, normal finalization, refusal, restoration and explicit recovery. Three missing cases below. |
| `scripts/backlog/work.py` | Assignment, approval binding, execution grant, durable dispatch claim, worker/result/status and review-candidate closeout. A result is not proof that Checkout exit completed. |
| `scripts/backlog/delegation.py` | Standing policy, expiry/revocation, exact supervision, reservation, task authorization, selected-model guard and conservative usage accounting. Eligibility alone grants nothing. |
| `scripts/qwen/coding_worker.py` | Trusted local task adapter, client/settings selection, canonical source materialization, Checkout, result/report and optional closeout admission. No live model invoked. |
| `tests/scripts/backlog/test_checkout.py` | Complete tiny-Git fixtures and refusal/recovery assertions. Missing replacement-owner, delayed-consent and dangling-entry cases. |
| `tests/scripts/backlog/test_work.py` | Actual tiny-Git lifecycle with scripted interactions and explicit fixture approvals; result/status and failed-dispatch paths. |
| `tests/scripts/backlog/test_delegation.py` | Scope, expiry, revocation, reservation, assignment/profile and guard tests. Synthetic grants belong only to the fixtures. |
| `tests/scripts/backlog/test_local_closeout.py` | Actual commit/push wiring and reconciliation, but protected validation is stubbed and reviews are constructed. |
| `tests/scripts/qwen/test_coding_worker.py` | Real bounded worker entry/admission/restoration and CLI failures with deterministic model doubles. |

Additional complete source review: `coordinator.py`, the backlog CLI,
`integration/authority.py`, `integration/git.py`, `integration/local.py` and
`integration/validation.py`. Integration lifecycle `_operate`, `_context`,
`_intent`, `_files`, `_publish`, `_promote` and portions of `_verify` were inspected
as dependencies; this is not full review of that module or its entire test suite.
Intake writer/source-idle/hash-chain boundaries were inspected selectively.
The already audited application loop, Runtime and ToolRunner contracts are reused
as prior evidence, with current blobs recorded; they receive no new whole-body
credit merely from this traversal.

## Actual authority and data flow

| Transition | Owner, authority and outcome |
| --- | --- |
| Approved work → assignment | WorkCycle validates current canonical B-record/scope, source/test/oracle, ordinary feature branch and exact baseline. Assignment-v1 is bounded; it is not every possible CodingTask shape. |
| Assignment → execution permission | Manual grant uses trusted confirmation and future expiry; standing delegation additionally binds principal, category, scope, limits, supervision and reservation. Neither backlog presence nor eligibility is permission. |
| Permission preparation → source claim | Checkout atomically creates the owner directory, refuses existing owners and unfinished Git/index state, and records return branch/HEAD, target and permitted bytes before effects. Ownership serializes source operations; it is not task or publication authority. |
| Grant → worker entry | WorkCycle rechecks authority, saves `DISPATCH_CLAIMED_NOT_PROOF_MODEL_ENTRY`, then calls the guarded worker factory. A claim without result has unknown entry/usage, not zero usage or permission to retry. |
| Task → model/Tool action | Existing CodingTask host scope and limits admit model proposals. ToolRunner validates/executes supported calls; the caller retains authorization responsibility. Qwen application admission and `Checkout.expect` bind permitted source bytes before edits. |
| Worker → review candidate | Acceptance, original-input integrity, result/task hashes, final source and actual Git state are checked. The result can establish `REVIEW_CANDIDATE`; it does not integrate, publish or close the story. |
| Review → integration/publication | Separate IntegrationAuthority and exact plan/review/validation/commit contracts apply. Remote observation/CAS and actual repository protection are separate boundaries. Coding grants do not become protected promotion grants. |
| Failure → reconciliation | Surviving owner and known-byte journal retain custody. Explicit recovery restores only authenticated known states. It does not renew a grant, refund unknown usage, retry inference or undo an external effect. |

WorkCycle acquires Checkout before the inner execution-grant check. This permits
trusted administrative branch preparation, not model entry under an expired
grant: dispatch is still checked afterwards. Ordinary maintainer-authorized Git
development is a separate supported route; WorkCycle's autonomous worker protocol
is not a universal prerequisite for every developer commit or PR.

Direct `run_local_task` is trusted host-owned bounded evaluation, supported by the
operating guide without requiring a backlog grant for every local call. It still
requires exact task/source/check/budget scope and Checkout. CLI task files and
explicit commit/push flags are trusted administrative inputs, not model authority.

## Checkout guarantees and recovery failures

Canonical resolved paths refuse scope aliases/escapes. Initial directory creation
serializes competing claims; raw unfiltered Git hashes and NUL-delimited path
lists preserve opaque bytes and unusual names. Tracked/index state, branch/HEAD,
unknown modifications and ordinary untracked entries are checked. Unexpected
bytes remain with the owner for reconciliation rather than being discarded.

Owner records contain root, process, return branch/HEAD, target revision, allowed
effects and expected byte identities. A record's age is not permission to remove
it. Its checksum establishes consistency under trusted local custody, not an
unforgeable grant against an arbitrary malicious local writer. The recovery
caller must actually stop the old process; the PID is not an automated proof of
cessation. Missing or corrupt journals fail closed and require manual evidence.

Atomic writes of individual records and initial directory creation do not make
the complete filesystem/Git workflow transactional. Actual branch and source
state must be reconciled after interrupted operations. The following cases use
only independently authored temporary repositories; no Devtools source or real
Checkout owner was altered.

### P1: a stale recovery can overwrite a replacement owner

Proposal **69688104-098b-404c-acca-745bebac6653** owns recovery/finalization fencing.
A genuine child acquired owner A, admitted `value = 1`, and exited successfully
without releasing it. Recovery R1 authenticated A and paused before restoration.
R2 recovered A completely; legitimate new owner B then admitted and wrote
`value = 2`. R1 resumed its previously checked restore and release.

Observed: source became `value = 0`, B's owner record/directory disappeared, and
R1 returned without an error. The old object's release has no epoch check against
the current owner. Initial exclusive creation therefore does not guarantee
exclusive restoration/finalization across awaited effects. The repair must fence
admission, effect and release together; an unlocked pre-effect digest comparison
alone leaves another race. Normal stale finalization needs the same protection.
No protected publication or grant bypass was demonstrated.

### P1: terminal confirmation can authorize a different owner

Proposal **30bd833e-f19d-4a4c-bbb6-465fd22db403** owns recovery consent binding.
The CLI displays stopped owner A, waits for default-No terminal confirmation,
then passes only `authorize=True`; recovery rereads whichever owner now exists.
During the synthetic terminal callback, A was legitimately recovered and live B
was acquired. The callback then answered yes to A's displayed question.

Observed: CLI returned `CHECKOUT_RECOVERED`, B's source changed from `value = 2`
to `value = 0`, and B's claim vanished. B's PID was the still-live fixture process.
This is distinct from effect serialization: consent must bind the displayed
owner digest/epoch, validated inside the fenced recovery admission. Changed
owners require a new genuine default-No decision. The callback is explicit test
I/O, not fabricated real human approval or authority to recover this checkout.

### P1: an ignored dangling link can disappear during branch switching

Proposal **3b2f566b-8733-4b1d-a840-1e361612ebf8** owns ignored-entry collision
admission. Entry checks `Path.exists()`, which follows a symlink target. A real
ignored dangling link had `is_symlink=True` and `exists=False`; the target branch
tracked an ordinary file at the same path. Checkout admitted the switch. Git
replaced the link; returning to the original branch removed that file, and the
original link was gone without an error.

Use compatible lexical-entry/lstat semantics and refuse before Git switches,
including supported link/junction forms. Do not delete unknown entries to make
switching work. This proves custody loss for this ignored entry, not off-root
target mutation or loss of the thirteen actual forensic files.

## Other observed failure and interruption behavior

The [independent scripts and observed results](code-audit/execution-ownership-probes.json)
include ten basic Checkout cases, the three violating cases above and five pure
delegation-policy cases. Literal fixture source and expected outcomes are retained.

Competing claims, corrupt/foreign owner identity, changed branch, explicit refusal
and unrecognized source bytes refused while retaining custody. Known stopped-owner
recovery restored the original and released the claim; repeated recovery reported
the canonical filesystem-not-found condition rather than a second success.
Injected failure immediately before an actual Git switch left the original
branch; failure after the switch but before its return left the target branch.
Both retained the owner and subsequently reconciled actual Git state safely.
Entering the fault adapter is explicitly distinguished from entering the actual
Git switch; a returned/refused label is not inferred proof of non-entry.

Pure standing-policy applicability created no authority. Foreign source/oracle,
excessive model-call allowance and category mismatch refused. Maintained tests
add expiry/revocation/reservation/foreign-assignment/profile coverage under their
own explicit fixture authorities. This audit issued no production execution grant.

WorkCycle journals dispatch admission before factory entry and conservatively
retains possible entry/unknown usage on cancellation or missing result. Worst-case
reservation is durable; per-model-call counters are process-local and do not
promise exactly-once external inference. Existing assignment dispatch records
prevent simple redispatch. Failure after a remote push or before receipt saving
may leave an external effect without a completed phase record: reobserve remote
and local identities instead of blindly retrying. Cancellation is not rollback.

Worker result writing precedes Checkout context exit. A result may exist while
restoration/branch return/release subsequently fails. Status/review must retain
that distinction. No existing result alone proves all source ownership ended.

## Cohesion, consumers and limits

WorkCycle owns repository orchestration, Checkout owns source serialization,
delegation owns scoped standing admission, the Qwen application owns its bounded
proposal/check/feedback loop, ToolRunner owns call validation/execution, and narrow
Runtime owns one selected interaction. Those are meaningful existing boundaries.
Qwen/Codex-specific local policy does not turn reusable framework Models into Agents.
No additional generic executor, transaction engine or Agent framework is warranted
by these findings.

There is concrete application-cohesion pressure in the multi-responsibility Qwen
loop and its composition with script-owned Git helpers. Existing proposal
**39c6663a-bab7-43ed-8166-82e780a75d05** now records caller evidence and scope.
Raw source Git operations and trimmed administrative Git output have different
contracts; merge helpers only where semantics and consumers match. Managed
Commands is already the shared subprocess substrate. Stale fixture docstrings
mention linked worktrees although these tests use tiny ordinary branches; that is
clarity debt, not evidence of extra Devtools copies or a new reusable abstraction.

Proposal **d58697fd-bb03-4e98-bdac-fa29444fc6ff** remains the broader check-input
closure/reuse owner. Local closeout's review subject covers result/base/files and
can reuse prior `protected_validation`. That does not establish configuration,
runner, toolchain and all read/check dependencies. Selected closeout tests replace
`validate_tree` with `SCRIPTED-FIXTURE-ONLY` and construct review decisions. They
protect wiring and actual tiny-Git commits, not full independent validation or
semantic review. No invalid retained publication is asserted here. The next audit
must inspect the full input-mutation/reuse matrix and actual publication callers.

Proposal **0385a359-399f-40bb-aed4-caf5239c9fc8** retains broader custody and archive
maintenance scope. Ignored content is not disposable. Missing owner journals and
unknown bytes require operator reconciliation; the dangling-link defect has its
own precise repair record. No cleanup or authority recovery was performed here.

Native source search/read/edit and checks have existing real worker consumers.
This deterministic audit establishes no new autonomous model behavior or coding
effectiveness. Localization candidate resolution/witness/readiness integration
still lacks a complete native agent consumer; A+C remains recommended and
unapproved. Owner claims, valid source evidence and successful checks each remain
different from semantic task completion and publication authority.

## Validation, backlog and remaining program

[Focused test evidence](code-audit/execution-ownership-tests.json): **114 passed**,
pytest 558.50 seconds, managed elapsed 559.59 seconds, exit zero, no captured output
truncation. The five selected test bodies were fully read. Integration and
integration-validation suites were additionally executed; execution alone gives
them no full-body review credit. Harness setup/exception-expectation errors were
corrected before results and are not product defects.

[Canonical Intake evidence](code-audit/execution-ownership-intake.json): three new
pending proposals and three append-only advisories, 48 verified chains, no errors.
No approvals, B-numbers, grants, dispatches or closures were created. The three
bounded worker repairs 41a497a8/660900a1/751451cb remain implemented and merged;
the source-index, exact-name and binding repairs are also delivered. Their pending
administrative states are not instructions to implement them again.

[Checkpoint validation](code-audit/execution-ownership-checkpoint.json) binds exact
changed documentation blobs, JSON/JSONL and link/layout checks, Intake chains,
whitespace, unchanged executable inputs and all thirteen raw forensic hashes.
The prior 2,867-pass/two-live-skip/100% production gate belongs to the delivered
worker repair; it is not a new gate run for this documentation-only audit.

Original RI fixtures remain **93/93**, historical experimental sources **606/606**
at defined review depth, and **188 older RI versions remain** in seven existing
families (168 unread,20 tip-only;15 full). No historical credit was added, no
scientific evidence changed and no current fixture census was reopened.

Prioritize a separately authorized bounded repair of the three Checkout defects,
with independent race/consent/link regressions and the full protected gate on its
final implementation. Then take the [frozen validation/publication cohort](code-audit/execution-validation-next-cohort.json):
fixed Commands, model checks versus host checks, complete input closure/freshness,
validation reuse, exact review subject, commit/push ambiguity and evidence durability.
It is selected but not started. Further operational signoff needs those results;
the wider Core/Resources/Models/Agents/Persistence/Observability/application/tooling
audit remains active. This is an audit checkpoint, not a successor-session dossier.
