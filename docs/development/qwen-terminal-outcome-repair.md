# Qwen terminal worker outcome correction

The existing P2 `835a203f-8fd4-4bc2-ace8-8772137eaf2f` is delivered by production
`5e16b832429789ea9dd63989476a163b376f20db`, tree `b938753f20b8fd69cc8c97f97579620a596a5637`, normal PR #41, independently accepted main
`9ea992f347c18b5206b50e1cd6c7ad89b2f564a8`. Starting main `31d7e178843e9ecd55f2541c573d7f468f4d2d26` already
contained the [Qwen operational audit](../research/qwen-operational-lifecycle-audit.md)
through PR #40 and all prior repairs. The [machine receipt](../research/code-audit/qwen-terminal-repair-20261027.json)
records exact source/test/configuration identities, commands, timestamps, durations,
versions, exits, negative reproduction and accepted-main checks.

## Result semantics and minimal correction

The existing qwen-coding-loop-v2 schema is unchanged. Returned terminal `accepted`
is worker completion eligibility, not a standalone candidate/test verdict. A
fatal caught exception or timeout makes it false even if a candidate was valid
and shared checks/currentness succeeded. The CLI still consumes that authoritative
flag; local closeout still requires it before candidate installation. Neither
consumer gained weaker admission, review or publication rules.

The implementation adds `accepted=False` to the existing TimeoutError and generic
Exception handlers in run_coding_task. Its docstring and application README clarify
the existing distinction. All other production AST is unchanged. The already
correct cancellation, source-restoration/input-integrity and final I/O propagation
paths remain. No new result wrapper, field, durable schema or lifecycle owner
exists. CLI, WorkCycle, Checkout, ModelInteraction and Evidence source are unchanged.

Per-turn validation, `change_check`, installed-currentness observation, admitted
source/diff/candidate archives, response/usage, error type/message, dispositions
and counters remain factual. They are not rewritten as failed tests or never-entered
operations. Known currentness before restoration is not a claim about the restored
baseline. Fatal worker failure can coexist with known candidate validation success;
it cannot coexist with an unqualified successful terminal worker signal.

Final archive/restoration/result-write exceptions propagate without returning a
successful worker result or repeating model/Tool/Git effects. Persistence may fail
after an effect, and lost acknowledgment after a completed write remains a separate
uncertainty. These tests do not establish power-loss durability, rollback of arbitrary
effects, exactly-once execution or safe task replay. A failed worker's candidate
remains inspectable; it does not become publication authority by changing a Boolean.

## Independent baseline and permanent regressions

Before production edits, maintained tests reached the actual public worker with a
tiny authored Git repository, native source acquisition, one exact typed source
replacement, real tests/oracle/Ruff/format/mypy, model-invoked check_changes and host
is_current. Fault callbacks observed acceptance already true, without seeding it.
An OSError and a TimeoutError at completion-stage persistence both returned a
failure disposition with accepted=True. The actual CLI returned 0 from those real
results. The qualified original run has **two intended failures, nine passing
controls, zero setup errors**. The successful no-fault control passed.

The eleven permanent cases now pass. They protect actual worker/CLI return values,
local-closeout refusal before mutation, retained passing candidate/check evidence,
one proposal/three shared-completion calls/two actions, source restoration and
unknown final usage despite known earlier usage. Other schedules cover one stage
write fault before acceptance, one real Git application then lost local reporting,
final result-write failure after restoration, restoration failure, preserved unknown
bytes, cancellation before model entry and during validation, and possible provider
entry followed by timeout. Final I/O failures preserve the original exception object;
no result is invented. Existing controls cover prepared/native success, failed checks
and repair feedback, admission refusals and cancellation during model entry.

The source/test change preserves all 26 preexisting top-level test/helper/class
bodies by AST. New test helpers isolate actual CLI and closeout consumers without
repeating model execution. No existing assertion, selector, coverage threshold or
exclusion was weakened. Initial tuple/list comparison and repeated fault-injection
harness mistakes were corrected before the qualified baseline; they are not product
failure evidence. Test-only formatting/type/import issues were subsequently resolved.

## Validation and production acceptance

On committed `5e16b832429789ea9dd63989476a163b376f20db`, the unchanged protected command
`uv run python scripts/validate_development.py` passed **3229 tests, two
optional live skips, 100% configured production branch coverage**, exit 0, in
1074.732007 recorded seconds. The receipt records pytest time separately. The final
focused command passed 173 tests and supported Ruff/format/strict mypy/layout
checks pass. Exact committed source/test/app/script/package-document/configuration
physical hashes were preserved through integration; this is not universal ignored
environment/toolchain dependency closure or reusable validation-cache authority.

Bounded post-main regression evidence is retained separately. Validation ran on the
recorded installed Python/tool versions; no additional runtime, inference server,
model, private data source or scientific controller was installed or invoked. No
complete cross-runtime or autonomous-effectiveness claim follows from these tests.

The ordinary PR merge was independently checked against actual GitHub permissions,
checks, rules and reviews. Accepted source/test blobs equal the committed protected
implementation; local main advanced by ancestry only. A documentation-only closeout
records delivered evidence after the production merge, without a second implementation
branch or any manufactured review/grant.

## Canonical evidence and preservation

The sole proposal receives an append-only ADVISORY with implemented-and-merged
evidence. Administrative PENDING_REVIEW remains and does not schedule this bounded
correction again. Original Qwen audit fields/findings and frozen cohort remain
historical; changed source/test/README versions receive separate maintenance overlays.
All thirteen forensic files, 903 RI ledger rows, experiments/scientific manifests and
historical refs remain preserved. RI 93/93 and 606/606 retain their defined completion;
188 exact historical versions remain separate in seven families. A+C remains unapproved.

One task-local command recorder name initially overwrote its startup manifest. Its
command evidence was preserved; startup checks had already passed and were printed.
The manifest was explicitly reconstructed from pinned audit/Git identities and
reobserved refs/forensics/Intake, and compared against the previous audit's retained
ref snapshot. This is recorded as an evidence-tooling limitation, not a production
defect or a claimed byte-identical recovery of the original ignored manifest.

## Next decisions, not implementation in this increment

**Obligation-driven Context (15bae0a6/B-0002/B-0035).** The minimum useful native
consumer is an opt-in host-owned composition next to ContextTools/coding_loop:
admit one explicit frozen obligation/scope frame, obtain existing Localization
lexical evidence, retain complementary/competing candidates and explicit supported,
contradicted or unresolved witness decisions, then expose exact readiness/assessment
identity and outstanding requirements to a native Tool response or Prompt. A real
bounded acquisition/stop or completion decision must consume that assessment.
Ranking, map availability and model claims cannot declare obligations satisfied.
The host-frame representation and mandatory-versus-helpful admission/stop policy
still need maintainer approval. Reuse existing Localization/Planning APIs; no new
search layer, universal planner or automatic A+C approval is implied.

**Application cohesion/edit feasibility (39c6663a).** Future extraction seams are
already visible: immutable CodingTask and legacy digest compatibility; request/history
projection in continuation; fixed check/runner composition in commands/change_checks;
exact admission/render/apply primitives now shared with historical development_task
runners; and task-terminal accounting/known-source restoration. Keep these under
existing application ownership, preserve current imports/callers or migrate them
explicitly, and preserve task digests, qwen-coding-loop-v2 filenames/fields/native
correlations, errors, validation and source/byte/authority limits. Removing historical
runner coupling is different from moving an agent loop into narrow Runtime. Decide
the first responsibility-based extraction and compatibility boundary separately;
do not raise edit limits merely to make the large owners editable.

**Recovery/Evidence (B-0028/B-0034/B-0011/B-0023).** Native archives still do not
constitute verified resumable working state. Missing completion never permits
redispatch. No automatic Runtime/Conversation checkpoint, new store, normalized
Evidence ingestion or external-effect reconciliation was added. Observation Option B
is preferred in principle but unapproved: per-invocation correlation, secondary
reporter failure, privacy-safe payload/retention and trusted host mandatory-versus-
optional evidence admission remain explicit decisions. Optional capture reporting
does not require a new persistence backend. No observer suppression, retry/refund
or response-schema change occurred.

Recommend next a bounded maintainer decision on the native obligation consumer:
the trusted task frame, witness/readiness admission and the acquisition/stop consumer
under 15bae0a6. Implementation needs explicit approval and independent native negative
controls. Keep application extraction under 39c6663a a separately selected increment.
Remaining dashboard/application/tooling and
cross-cutting audits stay in the comprehensive inventory. None was started here;
no successor dossier or new research program was prepared.
