# Evidence, usage custody and operator audit — 2026-10-25

Delivered follow-through: [provider-local usage, partial/conflicting facts and operator identity integrity](../development/usage-evidence-integrity-repair.md), production `8f34dbdee381cf4493dd1f5e2a5508653dfe2891`, PR#20, verified main `3e59c20f4c9276a7f28682a127ff95428e673564`. Final committed gate 2937 passed/2 opt-in live skips/100% configured production branch coverage;350 focused post-main tests and13 frontend tests pass. Existing bbba08b8/ca5a0aac/a823db65 retain implemented-and-merged evidence; do not schedule these repairs again. Broader B-0011/B-0023/B-0034 consumers and d586 closure remain open. All12 Core/Resources pinned bodies match main and remain unaudited: that is the next major domain. RI93/93,606/606,188 historical obligations and A+C-unapproved status are unchanged. Earlier notices below retain their dated meaning.

Reviewed integrated main `138adc07fa758032743cf5d79ff4b2fe0bb790cc`. All **twelve** frozen source/test bodies received
substantive review; [exact blobs and review depths](code-audit/evidence-usage-assurance.json)
separate complete bodies from selected dependencies. **Three P2 accounting/operator
defects** are independently reproduced and pending repair. No production source or
test was changed. This is not whole-lifecycle or autonomous-effectiveness signoff.

## Actual producer, custody and consumer flow

| Boundary | Actual owner and supported claim |
| --- | --- |
| Assignment → grant/reservation | WorkCycle and Delegations bind task/grant/scope; reservations are allowances, not observed use. Immutable reservation is not refunded after ambiguous dispatch. Checkout custody is separate from task authority. |
| Dispatch → native invocation | WorkCycle writes DISPATCH_CLAIMED, explicitly NOT_PROOF_OF_MODEL_ENTRY. Qwen writes request/stage before send, response/usage after return, and terminal task JSON after restoration/accounting. Missing completion is UNKNOWN, not0. |
| Provider → framework Evidence | Optional ModelInteraction observation is successful-normalized-response-only; capture policy defaults to omission. Runtime optionally constructs attempt terminal facts via ExecutionInspector. It does not automatically correlate ModelInteractionId with InteractionAttemptId or retain failed-provider usage. |
| Tool → Command/source effect | ToolRunner validates then executes once, preserving failures/cancellation. Host task/Checkout authorize and journal effects separately. Commands output/events are not durable transaction proof. Qwen command intent/results and edit/check records retain app-specific evidence. |
| Native usage → task/WorkCycle | Per-stage optional usage aggregates conservatively: any missing category makes that task category unknown; no turns also remains unknown. WorkCycle copies app totals or reports UNKNOWN. These JSON records are not automatically normalized InvocationMeasurement or usage persistence. |
| Normalized usage → snapshot/report | Repository usage CLI imports allowlisted Codex session/retained experimental capture metadata. InvocationMeasurement is produced by the retained experimental measurement adapter; native Qwen does not emit it. Public UsageObservation/storage/report APIs have real CLI consumers. |
| Snapshot → operator | Usage CLI reports PARTIAL known subtotals with separate unknown/conflict counts. Dashboard reads canonical Intake/WorkCycle and configured worker JSON directly, not framework usage ledger or inspectors. It is not account-wide accounting or a source of authority. |
| Validation/review/publication | Existing fixed checks, current scoped freshness, semantic review and publication receipts remain separate. Worker ACCEPTED is not Checkout release, a commit is not remote acceptance, and a snapshot is not current authority. Prior remote-ref reconciliation was already tested; no new GitHub fault injection here. |

## Confirmed defects and practical impact

**P2 — provider-local identity alias contamination**, proposal `bbba08b8-234e-4f31-bbef-972ac90189e2`.
`usage/collection.py` prefixes backend/provider in its final component key but
constructs thread→turn and invocation→thread indexes from bare strings. Adding
unrelated provider-B evidence makes a valid provider-A unknown-turn alias conflict.
Reusing a local invocation label across providers can exclude both valid records.
The public report and snapshot consumer are affected; current native CLI imports
primarily Codex/OpenAI, so no actual mixed-provider billing or budget bypass is
claimed. Repair all alias indexes within the existing owner, preserving valid
within-provider ambiguity. Independent acceptance uses public report plus storage
roundtrips and unchanged A-only consumption after adding B.

**P2 — compatible partial response copies lose known usage**, proposal `ca5a0aac-65b3-4d3c-b115-59a398a4087e`.
`responses[response_id] = row` chooses the last compatible copy. Input10 followed by
unknown input for the same response reports known subtotal0/unknown1; reversing
order reports10. Mutable snapshot whole-row dedup retains both nonidentical copies
and sorts by content hash, so adding metadata can change which facts survive.
Merge compatible known categories independently of order; preserve conflicts,
unknown provenance and disjoint response identity. No retained original balance
or historical scientific result is alleged corrupted.

**P2 — missing operator call identities falsely match**, proposal `a823db65-08fd-43d1-91dd-5602ebb47b11`.
`details.turn_detail` compares optional IDs without requiring a present identity.
A stage without proposal_id and a read_file response with provider_call_id=None
produce MATCH, which RunDetail displays as proposal_response_correlation. The
actual maintained projection was probed on literal temporary archived files.
Missing identity must yield NOT_ESTABLISHED; valid nonempty matches must remain.
This is a read-only evidence-join defect, not a demonstrated edit-authority bypass.

The [fourteen distinct probes and authored sources](code-audit/evidence-usage-probes.json)
retain literal expectations, inputs, actual results and qualifications. These three
bounded corrections need a subsequent authorized source/test increment, not a new
accounting engine. No new P0/P1 production defect was demonstrated in this cohort.

## Unknowns, durable records and supported no-action findings

- Disjoint known+unknown usage keeps a known subtotal and explicit unknown count;
  the subtotal is not a complete total. Overlapping provider categories are not
  added into a fabricated total. Pure configured budgets refuse UNKNOWN required
  dimensions; an unset limit is different from an unknown measurement.
- Exact serialized duplicate snapshots deduplicate. The authored two-row conflicting
  known-count control is excluded. A further partial-TURN probe finds a missing
  conflict: input10/output2 is chosen ahead of reasoning1 and reasoning2 partial
  rows, so the contradiction between those other rows is hidden. The same partial-
  fact repair proposal above now has explicit TURN acceptance as well as RESPONSE
  permutations; no third proposal. Snapshot save does not acquire a lease itself:
  the real CLI does.
- Snapshot writes use canonical atomic sibling replacement and file fsync, not
  parent-directory fsync or power-loss certainty. After a real tiny subprocess
  writes an external effect and exits9, the writer lease remains and blocks retry.
  Stale-lease recovery needs an operator; it is not silently cleared.
- Corrupt/schema-invalid snapshots refuse. Valid JSON altered under the same
  asserted source digest still loads: this mutable local metadata store never
  claimed independent source authentication. Missing snapshot means an empty
  partial observation set, not no real consumption. Source digests are provenance
  assertions unless a producer/consumer independently binds original bytes.
- Runtime fake-model entry followed by cancellation produces process-local
  InteractionAttemptCancelled, with no returned usage, no durable store and no
  retry. Tool entry followed by cancellation preserves its observed effect and
  propagates cancellation. Neither is rollback or proof of zero token use.
- ExecutionInspector is first-wins by EvidenceId; its duplicate fixture is actually
  identical. A future durable consumer must define conflict handling and source
  correspondence under B-0011; this is not a demonstrated durable-store bug.
- Usage report deliberately gives accepted observations precedence over failed
  observations. Our incompatible-looking synthetic flags expose a domain/progression
  limitation, not proof of same-domain production corruption. B-0023 must retain
  provider completion, capture failure, scientific acceptance and host outcome as
  separate claims before changing that policy. A supplied bool is not review proof.

## Real dashboard and privacy boundaries

The seven existing frontend cases and Python projections show unknown/missing
usage, an explicit stale-data alert after refresh failure, inert archived text and
source references. Projected TIMEOUT_COMPLETION_UNKNOWN_NO_RETRY stays uncertain;
no null became numeric zero. Successful tests/oracle exit codes remain recorded
checks, not semantic review or remote publication.

Overview consumes WorkCycle.status but drops its additive integration details;
original REVIEW_CANDIDATE is a worker outcome, not the final integration state.
This is missing end-to-end visibility under existing B-0011/B-0023, not evidence
that the UI falsely asserts main promotion. Worker schema/model/profile labels
are source-reported, not independently authenticated live inference. Default
metadata omits raw prompts/credentials; detail is allowlisted and raw disclosure
requires explicit server configuration. Server/details were selected dependencies,
not a complete dashboard security review. No personal sessions were ingested.

## Cohesion, reuse and architecture decision

Existing boundaries are useful: observations do not own execution, persistence
does not own Evidence meaning, and dashboard is a read-only consumer. No EventBus,
new store, Trace platform or database is justified. Real missing joins are task /
assignment → model occurrence → Tool/check/result → Checkout release → exact
review/remote acceptance, plus an app-to-normalized-usage consumer.

Prefer an explicit adapter/projection over existing immutable app records for one
real operator consumer (B-0011/B-0023), with exact source references, unknown states
and separate authority. Alternatives are retaining app-only inspection for now or
approving a broader durable Evidence contract after actual consumer requirements.
The adapter is smaller and reuses existing models; it still needs a maintainer
decision on identity joins, acceptance domains, capture/privacy, retention and
compatibility. This audit approves no durable schema or architecture change.

Native and framework token arithmetic look similar but empty populations differ:
`sum_usage(())` is mathematical zero, while no native turns remain UNKNOWN. Any
consolidation under39c6663a must preserve that distinction, completed versus
attempted calls, and category provenance. Do not blindly replace one with another.

The prior private closeout helper appended duplicate advisory records after an
interrupted reporting step and checked the wrong reference key on retry. Original
records are preserved in the [repair closeout](../development/validation-evidence-path-repair.md).
This is concrete caller retry reliability under B-0034/B-0024; Intake.review is an
append-only decision API, not an idempotent operation API. Correct callers must
observe the exact previous effect/receipt before retrying; automatic content
dedup could erase legitimate repeated reviews. This audit's capture/review calls
check canonical identity, decision_reference and rationale before appending. No
replacement Intake system or newly claimed production Intake defect is proposed.

## Backlog, validation and finite operational exit

Three new pending P2 proposals; two advisory updates to39c6663a and d58697fd plus a
material partial-TURN acceptance advisory on the second new proposal; dated
evidence notes on B-0011/B-0023/B-0034 preserve DEFERRED states and promotion triggers.
All prior RI, module/facade, worker, Checkout and PR17/18 repairs remain delivered.
d58697fd remains partially open for transitive/toolchain/environment/HEAD-sensitive
closure; unsafe local saved-proof reuse is already repaired and is not rescheduled.

**149 focused Python tests and7 frontend tests passed.** Fourteen distinct deterministic
probes ran; an initial nonexistent test-directory invocation selected no tests and
is excluded from passing evidence. No production tests or source changed; no new
full protected gate is claimed. Prior2903/2 live skips/100% is prior repair evidence.
Publication additionally validates exact blobs, unchanged executable/configuration
trees, JSON/JSONL, local links/layout, Intake chains, whitespace and13 forensic hashes.

Whole-lifecycle signoff still needs the three P2 repairs, explicit normalized/operator
consumers and correlation/privacy decisions, broader validation-input closure and
uncertain-effect/durability semantics. These are finite tracked obligations, not a
reason to repeat the same lifecycle audit indefinitely. No automatic follow-on audit.

The next major domain is **Core/Resources**, starting with the [frozen twelve-body
path/IO/process failure-contract cohort](code-audit/core-resources-next-cohort.json).
It was selected, not reviewed. Resource primitives underlie custody and effect
claims and deserve complete owner-level review, beyond previously traversed helpers.
After that: ModelInteraction/serving providers, Agents/Runtime composition,
Persistence/representation recovery, complete Qwen/dashboard consumers and
developer/scientific tooling. Each has partial evidence, not whole-domain signoff.
RI93/93 original fixtures and606/606 experiment source stay reviewed at their
defined depth;188 historical exact versions remain a separate assurance program.
Autonomous RI effectiveness and A+C remain incomplete/unapproved, respectively.
