# B-0009 — Build the first bounded local coding-worker harness

- type: STORY
- status: VALIDATED
- decision_maturity: READY_FOR_IMPLEMENTATION
- necessity: REQUIRED
- architectural_significance: HARNESS_LOCAL
- urgency: SOON
- evidence_basis: REAL_USE
- scope: experimental Qwen coding-worker vertical slice
- primary_domain: experiments
- supporting_domains: agents, context, tools, models, execution, evaluation
- parent: B-0003

## Problem / value

### Current real-task integration checkpoint

The [concrete coding worker](../../../experiments/qwen/docs/overview.md#retrieved-context-markdown-coding-worker)
now consumes multi-resolution Context, isolated native proposals and focused
test-feedback repair, capped at three calls. Scripted responses validate initial
acceptance, a corrected second edit, refusal, exhaustion and cleanup against the
unchanged eight-scenario oracle. The first real Markdown run is now accepted:
two Qwen calls, one repair, 8,178 input / 525 output tokens, 34.76 seconds.
The exact captured edit is integrated with eight permanent regressions and
[verified provenance](../../../experiments/qwen/docs/first_accepted_coding_task.json).
No new inference occurred during closeout. General reliability and reusable
Agent promotion remain unestablished; the next checkpoint is a different real task.
The existing loop now accepts host-owned one-file task configuration through
`run_coding_task(..., task=...)` and CLI `--task`. Original Markdown compatibility
and second-task Context/validation/repair/refusal are deterministically tested.
The [second task preparation](../../../experiments/qwen/docs/second_task_preparation.json)
freezes an existing Python source-materialization defect, independent checks and
all bounds. The live [second-task result](../../../experiments/qwen/docs/second_task_result.json)
remains REPAIR_BUDGET_EXHAUSTED: three calls, two repairs, 19,587 input / 1,848
output tokens, 105.74 seconds. Codex corrected the production materializer and
added primary-exception feedback capture after this failure. Neither correction
constitutes Qwen task acceptance or reusable Agent-framework promotion.
Task-local native structured continuation and five read-only Context operations
are now connected to that same coding loop on `feat/qwen-context-worker`.
Scripted search/read/edit/failure/repair passes the unchanged oracle and genuine
local native search/read completed (3 requests, 4 reads, 12,152 input / 645 output
tokens, 40.037 seconds). No new coding authority exists at the canonical checkout,
so this is not another accepted Qwen task or demonstrated coding improvement.
See the [maintained contract and evaluation](../../../apps/qwen/README.md).
General continuation, atomic task-local state, long-term memory and 32K/64K
benchmarking remain planned.

The existing WorkCycle now provides a [separately governed integration lifecycle](../integration.md)
for accepted candidates: destination-based installation, validation, exact-tree
supervisory review, feature publication, authorized target promotion, verification
and canonical backlog progress. Coding authority still grants no integration
permission. B-0048 remains an accepted object-only candidate pending a genuine
integration grant; sibling compatibility obligations remain open. No new Qwen
run or protected merge is part of this engineering increment.

Build one bounded experimental coding worker after B-0008 establishes the
minimum repository fact-acquisition boundary. It may exercise
ModelInteraction, experiment-local relevance choice, bounded Tool use,
execution, and task-specific acceptance without promoting a generic Context,
Agent, Action, authorization, or orchestration framework.

The deterministic fixture now proves a bounded patch-proposal worker can start
without source or test paths, acquire both through existing bounded list/read
Tools, return one permitted diff, and have host-side experimental code apply
and validate it only inside a disposable fixture. It uses no model-directed
mutation, reusable Context, Agent, Action, authorization, orchestration, or
evaluation implementation.

The final bounded live single-harness acceptance succeeded: Qwen inspected the
fixture, read both required artifacts, returned the permitted semantic patch,
and the host applied it only inside the disposable fixture before behavioral
validation passed. The durable live report remains temporary evidence rather
than reusable framework state.

Earlier live attempts safely exposed and corrected fixture-local grounding and
EOF-diff-admission issues before the final success. The worker retains raw
responses separately from the canonical patch it applies. It now also records
optional provider-reported ModelUsage per turn and complete cumulative reported
totals in the acceptance artifact when every turn supplies a count. This is
measurement evidence only, not a reusable Context, Agent, Action, governance,
or orchestration promotion.

A second deterministic repository-selection stress fixture now retains the
same small one-line label-matching change while adding plausible source, test,
and documentation alternatives. It uses seven bounded list/read actions and
records fixture-local required, plausible-unnecessary, and clearly-irrelevant
file-read facts alongside ModelUsage, projections, and duration. It is the
first measured selection-stress reference; no successful live result exists
for it yet, and scripted success does not establish Context pressure.

- hard_dependencies: B-0008
- pressure_dependencies: B-0012, B-0016, B-0035, B-0036, B-0043, B-0044
- operational_dependencies: pinned Qwen serving profile
- blocked_by: none
- promotion_trigger: deterministic worker composition plus live task evidence
- validation_level: LIVE_SINGLE_HARNESS


## Canonical consolidation checkpoint

The standalone worker is at `apps/qwen`. The first accepted Markdown correction
is adopted; Task 02 remains failed with a separate Codex repair. Single-checkout
WorkCycle/integration is implemented on `feat/qwen-context-worker`; main adoption
and dashboard dependency review remain separate. No model task ran during cleanup.
The later native Context increment adds measured read-only conformance, not a new
coding result. General reliability, durable continuation and Memory remain open.

The next bounded native coding population is frozen in
`apps/qwen/evaluation/native-cohort-01/`: duration boundaries, CSV dialect
behavior and a held-out source-representation case. Three distinct Intake
proposals are pending; no review/promotion or current-root standing grant has
been fabricated. Baseline defect checks and 83 existing regressions pass their
expected dispositions. No new Qwen coding task, improvement measurement or
Codex comparison has run. Qwen effectiveness remains the immediate program
priority; see the cohort README for exact authority and continuation steps.

## Native coding cohort execution

The later cohort is genuinely executed under trusted local development authority:
duration passed behavioral acceptance but requires style rework; CSV failed and
the held-out source task failed before editing. Five local runs used 25 requests,
141,083 input / 7,341 output tokens and 439.08 worker seconds. No production
candidate integration occurred. Local execution no longer depends on backlog
promotion or grants; production WorkCycle authority is unchanged. See the cohort
README/results for exact identities, Tool/evidence coverage and limitations.
General proficiency, fresh native test-feedback repair and fair Codex comparison
remain open; no historical result or proposal status was converted into success.


## Verified coordinated native cohort 04

The later [cohort 04](../../../apps/qwen/evaluation/native-cohort-04/README.md)
implements and measures atomic observed/versioned multi-region editing and
allowlisted installed API inspection through the existing worker. Final paired
development acceptance is 0/2 unchanged versus 2/2 final; one fresh two-file
held-out task also passes. One genuine behavioral/quality repair is observed.
The initial improved read-budget failure remains recorded and a prospective
development amendment accounts for its corrected comparison. Six runs used
27 calls, 172,310 input / 10,817 output tokens and 602.14 worker seconds.

Local candidates remain unintegrated. Multi-file local capability does not expand
one-file governed assignment-v1 or protected publication authority. Broader task
reliability, repeated repair, external-package API scope and a fair Codex baseline
remain open; this does not close the overarching autonomous-worker obligation.

## Requirement-preserving native cohort 03

Contract/quality preflight, source-version/check-category feedback, exact refresh
of already observed unchanged source and bounded nonduplicate pytest feedback
are implemented on the existing worker. Six genuine local runs consumed 39
requests, 248,998 input / 13,100 output tokens and 730.07 worker seconds. Paired
development acceptance was 0/2 before and 0/2 after. Fresh held-out timestamp
compatibility passed 19 tests, 16 scenarios, typing, Ruff and formatting after
one edit without repair. Thinking enabled did not improve acceptance and hit
output limit; default remains off. See the maintained cohort 03 records.

Reliable live behavioral repair, coherent multi-region editing, external API
verification and a fair Codex comparison remain unresolved. Neither this local
candidate nor prior regex/duration candidates were integrated. Historical
cohorts retain their original outcomes; no backlog approval or authority changed.

## Source-grounded native cohort 02

The maintained working set retains all current observed source regions instead
of pinning arbitrary prefixes. Authorized range errors are recoverable; native
edits require observed current source; optional frozen Ruff/format gates feed
bounded repair. Two fresh cases ran: regex consistency ACCEPTED (4 calls), command
output limits REPAIR_BUDGET_EXHAUSTED (7 calls, 2 repairs). Total 53,865 input /
2,085 output tokens and 122.62 worker seconds. The held-out first edit passed
behavior but conflicted with Ruff TRY004; repairs failed to reconcile the explicit
ValueError contract. This task-design tension limits the conclusion. No active
source exchanges were evicted and all admitted edits reconstruct exactly.

See `apps/qwen/evaluation/native-cohort-02/README.md` and `results.json` for fixed
criteria, raw evidence references and limitations. One genuinely accepted native
coding case is evidence of capability, not general reliability or measured
superiority. Live successful behavioral repair and a fair Codex comparison remain
open. The historical duration style-rework candidate and all cohort 01 records
remain unchanged. No candidate was integrated or protected source published.

## Verified coding environment 05

The mounted model bytes match the pinned upstream GGUF. A scoped Pi 1.3.0 SDK
accepted both fresh development tasks versus 0/2 for the original worker. The
maintained worker now exposes scoped Git/check Tools, explicit new-file admission,
measured native prompt capacity and shared reviewed local closeout. JSON overflow
passed all behavioral/quality gates; separate q8 and medium-thinking runs exercised
genuine behavioral/typing repair. The final path proposal still failed admission.
These small development results do not establish general reliability or Codex parity.
See `apps/qwen/evaluation/environment-05/README.md` for budget, conditions and
limitations. Prior accepted candidates and failed evaluations retain their original
attribution and integration status. This item remains open.


## Flat observed editing comparison 06

Simplified native edit arguments retain exact versioned atomic admission and
shared closeout. Valid paired development accepted 1/2 in Devtools versus 2/2
in Pi; a replacement fresh confirmation passed both. The invalid original
confirmation oracle and its failures remain recorded, excluded from scoring.
Zero edit-admission refusals in five transactions do not establish general
reliability. Multi-file/new-module investigation remains a demonstrated gap.
See `apps/qwen/evaluation/editing-06/README.md`. This item remains open.


## Recoverable source investigation 07

Fresh native development accepted 2/2 in both Devtools and scoped Pi; separately
frozen confirmation accepted in both. Devtools demonstrated new-module/export
creation, coordinated two-file edits and two Ruff repairs preserving behavior.
No live read errors occurred; safe recovery is deterministically tested.
See `apps/qwen/evaluation/investigation-07/README.md`. This small admitted-corpus
sample does not establish general reliability, behavioral repair competence or
Codex parity. This work item remains open.

## Substantive engineering checkpoint 08

Two local attempts consumed 17 requests, 238,990 input / 4,120 output tokens and
260.10 worker seconds, both ending before behavioral validation. A late novelty
audit classifies source search as reuse of the observed cohort-01 physical-span
case, not fresh evidence. Fresh binary I/O is 0/1 live acceptance. Corrected
practical edit bounds allow its unchanged captured transaction to pass behavior
and typing; host-only AST-equivalent formatting completes quality acceptance.
The reviewed feature and independent regressions are published in `f799be1d`.
This is supervisory recovery, not autonomous live success. The read-only Codex
session produced no deliverable and no calibrated comparison is claimed.

See `apps/qwen/evaluation/engineering-08/README.md` and its eligibility correction.
Source-search proposal `416658bd-8ab9-43c4-bbb3-98a18a88cd4d` remains unresolved;
binary proposal `b3cc8ac0-bccc-4df2-8e78-7bbaa7d9933e` remains pending canonical
review despite explicitly authorized local feature publication. Neither was
automatically promoted or approved. BSD, Identity and decoded-output candidates
have separate passing focused closeouts but still require permanent regressions
and their own exact-tree protected publication. This item remains open.


## Long-task continuation and candidate closeouts 09

The existing worker now compacts actual native inputs before tokenizer-based
capacity refusal, preserves editable spans/handles and recent feedback, and
archives exact unprojected Prompts without a new Memory owner. Read-only source
omission requires remaining reacquisition budgets. Engineering 08 pending inputs
now fit safely; their original failed outcomes remain unchanged.

The new bounded-read task's initial oracle used the wrong BinaryFile attribute.
Its failure is preserved as evaluator-invalid, with a real remaining short-read
defect in its first candidate. A separately frozen corrected development
continuation passed independent behavior and repaired Ruff, then published exact
Qwen source and independent permanent regressions in `61637ff8`. It is not fresh
confirmation and does not demonstrate behavioral repair. BSD, Identity and
decoded-output candidates completed their own protected, reviewed publications
in `86046e5a93c5`, `da0ac97a23ef` and `9b667e597f9d` respectively. The old pending-queue note
above describes checkpoint 08, not their current publication state.

See [the measured record](../../../apps/qwen/evaluation/continuation-09/README.md).
The discovery `038c927f-a59b-4010-89e8-becceabe991d` remains pending canonical
review; local publication does not promote it or close this broader item.
Fresh qualified long-task confirmation, behavioral repair and production target
adoption remain outstanding. This item remains open.

## Qualified substantial engineering 10

Two distinct documented managed-command obligations were independently qualified
before inference: immutable environment overrides and binary stdin. Both failed
live engineering (0/2 accepted). The first uncovered pre-edit receipt observations
bypassing stale-source projection; the maintained correction reuses the existing
rules and has focused regressions. The distinct stdin task received real behavior
feedback within 32K capacity but exhausted atomic attempts through wrong region
handles. Neither capability is installed; no behavioral repair success or parent
completion is claimed. The two discoveries remain pending intake proposals,
without canonical promotion or implementation grants. See the
[qualified record](../../../apps/qwen/evaluation/qualified-10/README.md) for frozen
contracts, actual usage, exact evidence identities and remaining obligations.

## Stdin development continuation 11

The exact Qwen subprocess-stdin implementation is independently reviewed and
ordinary-feature published; see [the record](../../../apps/qwen/evaluation/stdin-11/README.md)
for commit/source identities and full validation. This required a separately
recorded offline qualification after only adding standard stdin=None attributes
to seven existing Process doubles. All prior assertions, oracle and live failed
receipts remain unchanged. One real model repair corrected behavior and typing;
both live runs still terminated at Context capacity. This is not fresh or
uninterrupted autonomous success. Path-resolved current observed anchoring,
separated source presentation and bounded repair-capacity handling are tested.
Environment overrides remains incomplete and is the next Commands priority.
No proposal promotion, parent completion or protected adoption is inferred.

## Environment development continuation 12

The original qualified environment contract was requalified against maintained
stdin before inference. The first segment failed Context after ten requests;
exact completed-transaction and contained-observation projection enabled one
source-authenticated supervised continuation inside the original 24-call,
six-proposal, 1,800-second ceilings. The new edit was admitted but regressed the
slotted frozen constructor; the final result exhausted repairs and failed the
oracle, regressions, formatting, Ruff and typing. No partial implementation was
installed. This is not successful behavioral repair, fresh confirmation or parent
completion. Environment overrides remains the immediate Commands obligation.

The bounded 48K native probes were feasible, but provided no coding-quality
comparison; the original 32K service/profile is restored and retained. See
[the record](../../../apps/qwen/evaluation/environment-12/README.md) for original
contract, failed receipts, actual Context recovery, measured resource limits and
protected validation of the worker corrections. No proposal approval, promotion
or implementation grant is inferred from local evaluation/publication.

## Environment development 13

The previously exposed qualified contract now passes through the unchanged native
worker: 14 requests, five atomic proposals, no refusals; exact Qwen source and 15
independent regressions are reviewed and feature-published at `b81891ceeafa`.
The full original model/child oracle, 78 focused tests and protected validation
pass. See [the measured record](../../../apps/qwen/evaluation/environment-13/README.md).
Missing constructor/fluent behavior and quality failures were corrected using
actual feedback; an incorrect already-implemented child-overlay repair was not
exercised. Pi's single bounded diagnostic did not finish and has explicit
adapter/output/timeout limitations. No worker/serving redesign or Codex semantic
substitution occurred. This is development on an exposed task, not fresh
confirmation, parent completion, proposal promotion or protected adoption.
Environment overrides is no longer missing on this feature branch. Remaining
pressure is reliable fresh cross-component completion and requirement-preserving
behavioral repair, with production adoption separately authorized.

## Fresh engineering 14: successful exit codes

New discovery `d9416198-66c7-40b9-b566-e2a8806a81b5` remains PENDING_REVIEW; no canonical
promotion or parent completion occurred. The trusted local assignment separately
authorized Qwen development of this reusable developer-command capability.
Qwen located specification/result/Tool owners and delivered the full public
behavior in 10 requests/two atomic proposals, correcting a genuine boolean-
deduplication validation defect without losing passing requirements. Exact source
and 28 independent regressions are feature-published at `73e5ee07ee49` through
existing closeout; 116 focused tests, static checks and protected validation pass.
See [measured evidence](../../../apps/qwen/evaluation/engineering-14/README.md).
The worker/profile are unchanged. One fresh accepted repair is useful progress,
not general proficiency or protected-main adoption.

## Output policy development15

The exposed output-limit validation obligation is feature-published at
`c93e5bf0f508` with exact Qwen source, 60 independent regressions and protected
validation. See [measured evidence](../../../apps/qwen/evaluation/output-policy-15/README.md).
TypeError for noninteger/bool inputs and ValueError for invalid integer bounds
were independently reconciled before inference. One proposal/six requests passed;
no repair was needed, no worker changed, and old Cohort02 evidence is unchanged.
Parent reliability/protected adoption remain open. The next practical shared-tool
increment is a scoped Git/test/Ruff/format/mypy check bundle reusing current
Commands/ToolRunner/validation owners; it is not implemented here.

## Shared change-check16 attempt

check_changes remains unimplemented. The frozen useful application-level Tool
composition received 15 Qwen investigation requests but no edit before Context
admission failed; see [evidence](../../../apps/qwen/evaluation/change-check-16/README.md).
Source was restored. The Codex-authored explicit application task/import
prerequisite is distinct from feature delivery. No accepted candidate, closeout,
parent completion or protected adoption is claimed. Next finish this same Tool
after a bounded decision about measured search-history overhead/investigation
stop behavior; do not replace it with another framework.

## Change-check17 development continuation

The approved shared Tool remains missing. Narrowed owner/dependency scope and
explicit implementation checkpoints removed closeout investigation but did not
elicit any edit:11requests/20actions, then Context refusal with no reacquisition
allowance. The original16oracle and all prior evidence remain unchanged. See
[measured continuation](../../../apps/qwen/evaluation/change-check-17/README.md).
No source, projection or serving change, accepted closeout or protected adoption
is claimed. Next assess an independently useful fixed all-checks bundle within
existing run_check under its own prospective acceptance; it is not full
check_changes and does not resolve this parent reliability obligation.

## Fixed check-bundle18 attempt

The smaller independent `run_check(check="all")` contract also remains missing.
Qwen inspected the complete owner and actual helpers, then continued investigation
instead of editing: nine requests, 16 successful read actions, zero proposals and
Context refusal before request ten. See [evidence](../../../apps/qwen/evaluation/check-bundle-18/README.md).
No maintained source, worker, serving or projection change was made. Original
full 16/17 contracts/results, forensic evidence and source are preserved. The
parent stays open; the smaller bundle must not be counted as full check_changes.
Next assess implementation-oriented essential-source guidance for this same
bundle before considering the subsequent Git discovery/report freshness increment.
No automatic recovery, new framework or protected-main adoption is authorized by
this diagnostic outcome.

## Source-supplied19 implementation treatment

Authentic owner/helper Context was supplied before inference through existing
ToolRunner/Context observations, with a three-response implementation-start guard.
Qwen proposed implementation on response two, but all four transactions were
refused atomically for oversized/no-op text. Six requests ended in
PROPOSAL_ADMISSION_FAILED, not Context exhaustion. Source remains unchanged;
see [evidence](../../../apps/qwen/evaluation/source-supplied-19/README.md).
This is progress to proposals only, not a delivered check bundle, behavioral
repair, or general reliability result. The original18oracle and16/17/18failures
are preserved. Deliver this fixed operation directly with separate Codex source
attribution before composing the full check_changes contract; no semantic
substitute was installed in this Qwen evaluation. The parent stays open.

## Direct Codex fixed-bundle delivery

`run_check(check="all")` is implemented and feature-published at `f26b36238e7f412ed736ca1d8cda6acdb4592b7d`.
The existing CodingCommands/managed Commands/ToolRunner owners provide independent
check outcomes, source/plan-bound evidence, fail-closed admission and cancellation.
The unchanged18oracle, permanent regressions and protected validation pass; see
[the contract](../../../apps/qwen/README.md#fixed-all-check-bundle) and
[delivery evidence](../../../apps/qwen/EVALUATION.md#direct-codex-bundle-delivery--not-a-qwen-evaluation).
This increment is Codex-authored, with no Qwen inference or relabeled historical
outcome. The parent remains open. Full check_changes discovery/freshness and
protected-main adoption are unresolved; compose this bundle in the next increment.

## Direct Codex full shared change-check delivery

`check_changes` / `is_current` are feature-published at `4d401c828b5fef4e2d4db949c2f80549ea445fe0` with explicit
Codex implementation and regression authorship. They compose the delivered bundle,
authenticate scoped Git/source/index/plan evidence and reject stale or incomplete
validation through the existing shared ToolRunner. The unchanged16oracle and
protected development gate pass; see [delivery](../../../apps/qwen/evaluation/change-check-codex/README.md).

No Qwen call, new success claim, governance expansion or protected-main adoption
occurred. All earlier failures remain immutable. The parent remains open: next
use this Tool in actual Qwen engineering and reauthenticate before independent
review; selective destination-authorized production integration is still required.

## Shared engineering20: available Tools, no implementation

The new qualified configuration-obstruction task reached the prospective supervisor
stop with eight genuine Qwen requests, ten successful read/search actions and zero
edits. No live check_changes/is_current use, behavioral repair or candidate closeout
occurred. Context still fit; this is not a Context or edit-admission failure.
A narrow Codex prerequisite adds opt-in post-edit check completion and pristine
report presentation, tested deterministically with host freshness before source
restoration. It does not establish improved model performance. See
[record and separate fallback](../../../apps/qwen/evaluation/shared-engineering-20/README.md).
The parent remains open. No retry, serving experiment, new governance or protected
adoption followed; the RI obligation remains unfinished.
