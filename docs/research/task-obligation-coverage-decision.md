# Task-obligation coverage: decision preparation

Status: **RECOMMENDED; AWAITING MAINTAINER DECISION**. This is preparation under
[ADR-0005](../architecture/decisions/ADR-0005-obligation-driven-repository-localization.md),
not an accepted ADR, implementation grant or replacement backlog authority.
Source baseline: `45d666cd168a6add2e59bbdf2e1b10e1fb82ada6`.
The implementation home is existing pending proposal
[15bae0a6](../backlog/proposals/15bae0a6-b95d-417c-98fa-d75a8aff29d4/proposal.json).

## Decision requested

Approve **A: trusted explicitly reviewed task-clause/obligation coverage**, with
**C: bounded caller-reviewed revisions** when acquisition reveals new uncertainty.
Implement one opt-in application composition. Defer **B: model-proposed obligations
with independent semantic review** until that composition has deterministic
end-to-end acceptance and a separate model-evaluation authorization.

The maintainer must decide four concrete points before implementation:

1. The trusted caller supplies the expected task-clause account, its linkage to
   existing obligations and the review of intended information needs. The model
   cannot approve its own coverage or create accepted witnesses.
2. The first integration lives in `apps/qwen`, composing existing Localization,
   ContextTools, CodingCommands and Checkout. It does not add an agent planner to
   Runtime or a universal completeness function to Localization.
3. An unaccounted mandatory clause, unreviewed need or unresolved contradiction
   prevents the opt-in semantic-completion claim. Existing bounded exploration
   may continue; it must retain the reason that completion remains blocked.
4. Task-only decisions are recorded outside the repository-witness assessment.
   They require real caller/task evidence or subsequent execution results. No
   empty `WitnessSet`, fabricated resource or false NOT_APPLICABLE is introduced.

No implementation is performed by this checkpoint. Rejecting this recommendation
leaves current scoped readiness behavior intact. The alternatives below remain
available for an explicit different maintainer decision.

## Evidence and present ownership

[U1](ri-u1-r17-r2-audit.md) independently reviewed 32 necessary semantic units.
U02 (qualified admission/re-admission and provenance) and U19 (native fixture
construction) were neither directly nor partially requested by eighteen authored
needs. Required resources were incidentally retrieved. The resource ranking did
not repair missing semantic intent. These units are historical evaluator evidence,
never a hidden runtime requirement list or training signal for this slice.

The [lexical follow-up](ri-lexical-sensitivity-audit.md) preserves the separate
R1 representation and parameter-policy questions. Reach, ordering, disclosure,
need formulation and task execution must remain distinguishable.

| Current owner | Implemented input/output and missing seam |
| --- | --- |
| [Task interpretation](../../src/devtools/context/localization/task.py) | Caller supplies anchors and obligations; validates local uniqueness and anchor membership. It holds no original task text and performs no clause extraction or semantic completeness review. |
| [Provenance](../../src/devtools/context/localization/identity.py) | `TaskProvenance` references caller material, optional `TaskTextSpan` is half-open **character** coordinates. It checks interval shape, not correspondence to retained original task text. A consumer must authenticate that correspondence. |
| [Obligations](../../src/devtools/context/localization/obligation.py) | Mandatory/helpful predicate, criterion, anchors, provenance and accepted ALL-member/ANY-alternative sets. `WitnessSet` is nonempty. A well-formed set does not establish that all real task requirements were authored. |
| [Lexical acquisition](../../src/devtools/context/localization/lexical.py) | Executes unchanged full-task and caller-authored obligation queries over one authorized index. Queries are not automatically supplied for every obligation; absence is not satisfaction. No lane fusion or semantic judgment. |
| [Grounding](../../src/devtools/context/localization/grounding/resolve.py) | Explicit locator plus retained frame; exact path/module/declaration/method result can be resolved, ambiguous, unsupported or unresolved. A resolved referent is not an accepted witness. |
| [Association](../../src/devtools/context/localization/association/hypothesis.py) / [generation](../../src/devtools/context/localization/generation/generate.py) | Caller-shaped candidates/recipes, exact native supports and bounded projections. Hypotheses remain unresolved; generation does not author missing task obligations. |
| [Resolution](../../src/devtools/context/localization/resolution/contract.py) / [promotion](../../src/devtools/context/localization/resolution/promotion.py) | Named caller decisions over exact attached evidence; complete conjunct support permits explicit promotion. Contradiction remains distinct; promotion changes neither the accepted obligation contract nor readiness automatically. |
| [Readiness](../../src/devtools/context/localization/readiness.py) | Identity coverage and caller assessments for **supplied obligations only**. Its docstring expressly disclaims discovering every real obligation. READY, CONDITIONAL, BLOCKED and INVALID_FRAME remain scoped. |
| [Planning](../../src/devtools/context/planning/plan.py) / [source materialization](../../src/devtools/context/planning/source.py) | Caller-selected representations, snapshot/purpose/order/lineage and exact retained source. Planning does not author obligations or infer that model-visible source establishes task completion. |
| [CodingTask](../../apps/qwen/tasks.py) | Objective, baseline, exact source/read/new-path scope, fixed checks and limits. No native Localization interpretation or semantic-review input. Task identity already binds configured input; a future opt-in contract must participate in freeze/receipt identity. |
| [ContextTools](../../apps/qwen/context_tools.py) | Scoped canonical source search, lookup, map, expansion and exact observations. No obligation-assessment Tool or trusted coverage contract today. Metadata is not editable source. |
| [Native loop](../../apps/qwen/coding_loop.py) / [CodingCommands](../../apps/qwen/commands.py) | Native correlated Tool results, atomic edits, independent fixed validation, model-invoked `check_changes` and host freshness. Check PASS does not certify semantic decomposition, approve review or grant publication. |

Current flow is objective → host-authorized paths/index → model search/read →
exact observation → proposal/checks. Rich Localization composition exists beside
that application path. Responsibility for **reviewing task-to-obligation/need
coverage before a semantic completion claim** is the missing consumer seam.
Moving that responsibility into a ranker, RI parser or readiness kernel would
violate established ownership rather than solve it.

## Three options and their combinations

| Question | A: trusted authored contract | B: agent proposal + independent review | C: progressive discovery |
| --- | --- | --- | --- |
| Solves | Makes the expected mandatory frame explicit; mechanically finds missing associations against that reviewed frame. | Reduces manual drafting and can expose omissions through a distinct reviewer comparing proposal to original task. | Preserves newly discovered uncertainties and allows explicit revision/reacquisition. |
| Does not solve | A caller can omit a clause or misunderstand its semantics. An explicit review is bounded assurance, not exhaustive understanding. | A second model can share the same omission. Independence of source, policy and evaluator must be stated, not inferred from two calls. | Discovery cannot prove there are no unknown requirements. A shrinking open list alone proves nothing. |
| Trusted input | Original objective, reviewed clause roster and approved interpretation/needs. | Original objective and review authority; worker proposal is untrusted until reviewed. | Last accepted frame and authority to propose revision; newly acquired facts remain scoped. |
| Clause linkage | Exact original text identity + verified spans or explicit interpretation rationale; existing task-local obligation IDs. | Proposal cites those same spans/IDs; reviewer records missing/ambiguous clauses and disposition. No second identity hierarchy. | New rationale and predecessor revision; explicit old/new clause and obligation associations. |
| Omissions | Expected roster minus accounted clauses, then semantic review of adequacy. A mere span overlap cannot certify meaning. | Independent reviewer identifies omissions against the original, including obligations absent from the proposal. | New discoveries create open review questions; no silent deletion or assumed completeness. |
| Contradictory/partial/deferred | Clause review can remain unresolved; existing candidate contradiction, partial witness, OPEN/ABSTAINED/DEFERRED assessments retain separate meaning. | Same states; model cannot approve its own contradiction or defer mandatory work by assertion. | Keep competing hypotheses, rejected explanations and deferred prerequisite/reason; expiry or budget is not satisfaction. |
| Reacquisition | Caller corrects needs; existing lexical/global lanes or explicit grounding acquire current authorized evidence. | Reviewer returns actual diagnostic; worker requests authorized acquisition under revised reviewed frame. | Invalidate affected assessments after task/source change; reacquire/reassess and create a subsequent disclosure plan. |
| Model visibility | Original task plus bounded clause/obligation/need status and exact sources, separately labeled. | Proposal/review and repair feedback remain distinguishable, with native Tool-call/result correlation. | Current frame, open questions and revision causes are shown; raw historical records remain immutable. |
| Review location | Trusted application caller before run, and at explicitly authorized revision boundaries. | Separate authorized semantic reviewer before frame admission, never implicit Tool validation. | Trusted review of changes; model observations may trigger questions but cannot grant authority. |
| Completion claim | Reviewed expected clauses accounted for, supplied mandatory localization conditions satisfied or explicitly accepted conditional handoff, task-only checks accounted for; independent engineering validation/review still required. | Same, plus authenticated review provenance and proposal/revision budget. No universal completeness oracle. | Same relative to latest reviewed revision, with unresolved items visible; exploration termination is not semantic completion. |
| Complexity | Lowest: bounded application contract, identity checks, projection and scripted end-to-end tests. | Adds reviewer invocation/permission, independent budgets, failure/ambiguity handling and possibly persistence choices. Not part of first slice. | Small for caller revisions; large if turned into an automatic planner. First slice permits explicit revisions only. |

All options reuse existing obligation/grounding/assessment/Planning semantics.
They add **no source/read scope, mutation, command, model, Git, WorkCycle or
publication authority**. Full-task lexical escape remains available. Low score,
absence from a returned list and unsupported analysis are never elimination proof.

## Minimal bounded vertical slice after approval

The recommended initial public addition is one optional **trusted application
input** to `run_coding_task`/its existing task freeze, default absent. Final Python
naming is an implementation choice. It binds the exact `CodingTask` objective
and configuration digest, reviewed clause spans/rationales, the existing
`LocalizationTaskInterpretation`, caller-authored acquisition intents/queries,
reviewer provenance and limits. It is not another framework Task model. Changing
the contract must change the frozen run input identity; historical task digests
and receipts retain their existing version. No standalone durable schema is
necessary for a first in-process composition; if durable input is later added,
compatibility must be reviewed explicitly.

Use existing `TaskProvenance`/`TaskTextSpan` and obligation identities. A clause
roster is an application account of the original objective, not a new identified
obligation layer. Every mandatory reviewed clause must point to existing
obligation IDs and an adequate caller-reviewed need, or have an explicit unresolved
or task-only disposition. Helpful/background/excluded text needs a recorded reason.
Require exact task binding, real substring bounds, unique declared references and
review provenance. These checks establish representation correspondence; the
trusted reviewer establishes semantic adequacy. A missing roster/review must
report **coverage unreviewed**, even if scoped readiness returns READY.

Reuse ContextTools' admitted snapshot/source index. Select its existing whole-file
view for `LocalizationLexicalAcquisitionRequest` rather than build a competing
index. Keep an exact association from obligation/query/native hit to source unit;
do not equate symbol-document and whole-resource corpus identities. Use existing
grounding for trusted explicit locators, association/generation where a recipe
is justified, then explicit caller member decisions/promotion/assessments.
No ranking-to-SUPPORTED conversion is allowed. The reviewer is responsible for
semantics; native contracts continue to authenticate scope and provenance.

Extend existing ContextTools' opt-in native surface with a bounded read-only
obligation-status/acquisition operation **only because current search/lookup
arguments cannot identify an obligation or report its assessment**. Do not add a
parallel read/edit Tool. The operation selects only a trusted admitted obligation
and caller-defined intent, returns candidate metadata/current status, and exposes
existing source-unit handles. Existing `inspect_source`/`read_source`/`expand_source`
must perform exact disclosure and observation before editing. A model may request
clarification or revision, but not submit accepted assessments or change the
trusted clause contract. A caller-review boundary may return bounded decisions;
it must not be mislabeled autonomous completion without intervention.

Record the reviewed contract digest/revision and obligation/query links in the
existing run and Tool receipts. Preserve exact native call IDs, snapshot/source
versions, disclosure identities, decision caller/basis, unmatched clauses and
check-report identity. No new EventBus, Trace store or universal evidence class.
Project a compact current status rather than repeatedly inserting all source or
gold. Preserve diagnostics when Context capacity cannot accommodate a review.

After an admitted source change, use existing ContextTools refresh, authenticate
the new retained source and invalidate old snapshot-bound candidate/assessment
values. Require new exact reads where existing observation rules require them.
Do not silently carry READY from the pre-edit frame. Existing CodingCommands
perform renewed `check_changes`; host `is_current` authenticates the installed
candidate. Checkout restoration makes prior candidate reports historical.
WorkCycle independently reviews and publishes, under its existing authority.

Task-backed requirements such as "use a named fixture strategy" or "run the
protected gate" need different evidence: caller/task review or actual execution,
not an invented repository file. A requirement about locating the supported gate
contract is a repository-information obligation; actually passing it is execution.
Keep task-only decisions in the application account and reference real receipts.
Do not mark them NOT_APPLICABLE merely because no repository witness is needed.
Do not change production `WitnessSet` to accept the historical empty encoding.

## Independent end-to-end acceptance

Use new tiny fixture source and an independently authored objective: preserve an
owner/version guard **and** extend a boundary regression using the native fixture
builder. The trusted expected clause roster includes both. The initial proposed
interpretation/needs cover only the guard, analogous to U1's omissions. The oracle
knows this fixture's explicit clauses; historical U1 gold is not loaded.

1. Show scoped readiness can be READY for the smaller supplied frame, while the
   application reports the second mandatory clause unaccounted and blocks its
   semantic-completion claim. Do not pretend the kernel discovered the clause.
2. Even with an obligation row, an absent or inadequately reviewed need remains
   a distinct formulation gap. A query string being nonempty is not adequacy.
3. Caller correction supplies the missing existing obligation identity and a
   reviewed need. Prove a requested-but-unretrieved source remains open; unknown,
   unsupported grounding, ambiguity and partial ALL-member support cannot pass.
4. A scripted assistant selects the actual native obligation acquisition operation,
   chooses current source handles and obtains exact disclosure through existing
   reads. Assert real ToolRunner call/result IDs and subsequent observed-source
   edit admission; metadata alone must fail admission.
5. Explicit independent caller witness decisions use exact attached evidence.
   Contradicted and unrecorded members differ; mixing alternatives cannot satisfy
   a conjunction. Task-only decisions use their actual evidence account.
6. An admitted fixture change receives independent behavioral/quality feedback;
   the scripted assistant genuinely requests `check_changes` through the native
   surface, obtains PASS, and host currentness authenticates that same candidate.
   Restoration rejects historical freshness. This is a test double, not Qwen.
7. Reject changed task text with old spans/digest, stale contract revision, foreign
   obligation/source/view, duplicated clause associations, unavailable authorized
   source, unauthorized path, overflow and unreviewed model-originated approvals.
8. Test source-change refresh, invalid old assessments, named accepted versus
   unaccepted deferral, conditional non-applicability evidence, unresolved reviewer
   failure, task-only evidence missing, and capacity refusal without data loss.

Passing establishes deterministic composition and boundary behavior. It does not
establish that Qwen authors adequate obligations, that independent review always
finds omissions, or that acquisition is more effective. Those claims require a
separately approved, frozen genuine model task and comparative evaluation.

## Scope and limits of a maintainer approval

Recommended scope is one trusted opt-in application adapter, reused native source
and validation operations, permanent independent fixtures and package/application
documentation. Expected implementation owners: `apps/qwen/tasks.py`,
`coding_loop.py`, `context_tools.py` and cohesive application helpers if needed;
`commands.py`/`change_checks.py` should retain their validation ownership. Existing
Localization APIs should remain sufficient; any demonstrated API mismatch returns
for review before changing framework semantics.

Dependencies are existing ADR-0003/4/5 boundaries and proposal15bae0a6; exact-locator
integration06c3809b is adjacent and need not block the lexical-first slice.
Delta caching, automatic decomposition, reviewer-model orchestration, graph
ranking, generalized closure and task scheduling are excluded. Existing strict
atomic limits, authorized absence, current source observations, fixed budgets,
protected validation and independent WorkCycle review remain unchanged.

The strongest permissible statement is: **the supplied reviewed clause contract
is accounted for, and its supplied localization frame has the recorded readiness
under the retained evidence and explicit review assumptions**. It is never proof
that the original task was exhaustively decomposed or the engineering work is
universally complete.
