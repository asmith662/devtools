# Evidence-to-witness resolution policy investigation

## Disposition

**Proposed architecture; investigation complete; no policy implemented.**

Current sequencing qualification: the bounded
[external decision adapter](../../experiments/codex_dogfood/semantic_resolution/README.md)
is implemented as non-production review-gated infrastructure; it executes no
resolver or effectiveness experiment. The semantic-resolution direction remains
open and intact. Under the [coordinated roadmap](../roadmap.md#current-sequencing),
prospective effectiveness evaluation pauses until mandatory R1 and unconditional
R2 true BM25F progress unless a concrete earlier parallel justification is
recorded. The original recommendation below does not override that order or
establish that retrieval representation, fielding or query formulation is adequate.

Primary recommendation: **IMPLEMENT EXTERNAL SEMANTIC RESOLVER FIRST**.
Start with a bounded, caller-owned, review-gated experimental policy over existing
associated hypotheses. A human may be the semantic resolver; a model may propose
decisions in a separately authorized prospective experiment. Neither is required
inside Localization. Machine validation admits records; semantic review accepts
judgments. Automatic promotion into a live assessment is outside this first slice.

Do not implement a criterion-name rule system, universal claim ontology, fifth
structural relation, production model integration or automatic resolver on the
authority of this document. The [taxonomy](../architecture/taxonomy.md),
[documentation authority](../documentation_map.md),
[ADR-0005](../architecture/decisions/ADR-0005-obligation-driven-repository-localization.md)
and [implemented Localization contract](../../src/devtools/context/localization/docs/overview.md)
remain authoritative. [B-0002](../backlog/epics/B-0002-coding-context-substrate.md)
remains open. This proposal requires separate implementation authorization and
new prospective effectiveness evidence.

## Scope and inspected evidence

Starting checkpoint: `3c0ff8ee19f10036d39a94e0a553e8d48d954168`,
`Add evidence-to-witness resolution kernel`, clean `main` and index.
This investigation reads current contracts/docs/tests and committed aggregate
analysis conclusions from Cases 0004–0008. It does not replay a case or use gold
resource identities to author policy. Confirmation remains sealed.

Production evidence inspected:

- [obligation.py](../../src/devtools/context/localization/obligation.py):
  `LocalizationObligation`, `SatisfactionCriterion`, `WitnessSet`.
- [task.py](../../src/devtools/context/localization/task.py) and
  [identity.py](../../src/devtools/context/localization/identity.py): anchors,
  task-local identities, caller source provenance.
- [association/hypothesis.py](../../src/devtools/context/localization/association/hypothesis.py),
  [structural.py](../../src/devtools/context/localization/association/structural.py),
  [references.py](../../src/devtools/context/localization/association/references.py),
  [imports.py](../../src/devtools/context/localization/association/imports.py):
  candidate shapes, lexical/routed supports, exact structural evidence and replay.
- [roles/models.py](../../src/devtools/context/localization/roles/models.py),
  [routing/models.py](../../src/devtools/context/localization/routing/models.py),
  [BM25 contract](../../src/devtools/context/retrieval/lexical/bm25.py),
  [grounding contract](../../src/devtools/context/localization/grounding/contract.py):
  positive observations, presentation tiers and bounded native source identities.
- [resolution contract](../../src/devtools/context/localization/resolution/contract.py),
  [view](../../src/devtools/context/localization/resolution/view.py),
  [promotion](../../src/devtools/context/localization/resolution/promotion.py),
  [assessment](../../src/devtools/context/localization/assessment.py),
  [readiness](../../src/devtools/context/localization/readiness.py).
- [resource.py](../../src/devtools/context/repository/resource.py): exact content;
  [resolution tests](../../tests/context/localization/resolution/test_resolution.py):
  explicit lexical/structural decisions, frame rejection and downstream behavior.

## Current inputs have different semantic strengths

| Input | Actual representation and executable semantics | Missing semantics |
| --- | --- | --- |
| Desired information | `LocalizationObligation.predicate: str`, nonblank | No callable predicate or entailment evaluator |
| Satisfaction criterion | `SatisfactionCriterion(name: str, statement: str)`, both nonblank | No rule registry, formal claim or execution contract |
| Applicability condition | Optional nonblank string | No evaluation of whether the condition holds |
| Shared anchor | Task-local identity and nonblank text; optional provenance | Text does not assert existence or bind a repository subject |
| Candidate member | Observed resource, nonblank reason and at least one native support | No explicit pre-resolution member claim or proof requirement |
| Hypothesis | Nonempty distinct resource members; complementary within it, competing with peers | No assurance its resources establish the desired information |
| Native supports | Typed observations with exact frame/membership checks | No implication from proposal evidence to obligation satisfaction |
| Resolution | Explicit disposition, criterion, claim/reason/caller, provenance, attached basis | Validates lineage, not logical truth of the judgment |
| Accepted witness algebra | Hashable targets; all-of inside a `WitnessSet`, any complete alternative accepted | Target presence alone is not semantic proof |
| Assessment/readiness | Frame checks, applicability/disposition consistency, supported target coverage | Does not inspect prose/content for entailment or prove interpretation exhaustive |

**Can current criteria be executed without new semantic interpretation? No.**
`name` is a caller label, not a registered executable identity; `statement` is
semantic prose. A name such as `native-source-identity-boundary` supplies no more
formal meaning than any other nonblank string. Even equal names need not mean
equal statements. The kernel checks the supplied criterion against the obligation
value, not a predicate implementation. Applicability prose has the same limitation.

Reject `if criterion.name == ...: accept OWNER`. That would introduce an
unacknowledged interpretation policy. Renaming a label must not change evidence
truth. Parsing criterion prose is semantic interpretation even when deterministic.

## Evidence-strength matrix

In this matrix, **exact** means scoped to the retained snapshot, supplied analysis
universe and the supported native syntax, not universal runtime truth. A fact can
prove a criterion only if an explicit interpretation equates that criterion/member
claim with the precise fact. No row supplies that interpretation today. Multiple
sources remain independent observations, not votes.

| Family | Proposition established | Explicit nonclaims | Deterministic support possible? | Deterministic contradiction possible? | Bridge needed |
| --- | --- | --- | --- | --- | --- |
| `LexicalMatchSupport` | Exact query lane, native match/rank and content/filename term contributions in the eligible lexical corpus | Correctness, authoritative contract, necessary information, semantic entailment; rank is not certainty | A formally specified lexical-observation claim only | An exact incompatible lexical fact only with a formal claim and adequate observed scope; missing match is insufficient | Task relevance and content meaning require interpretation |
| `ResourceRoleEvidence` | Positive supported role interpretation with convention/native observation lineage | Exclusive role, exhaustive role inventory, satisfaction or authoritative ownership | Exact named convention/native observation claims, not generic role-to-witness claims | An underlying exclusive native fact may conflict with a typed claim; absent/other role cannot | Distinguish convention, RI observation and task meaning |
| `RoutedMatchSupport` | Same native match, presentation position and preferred/escape explanation under caller preference | New repository fact, better witness, positive/negative satisfaction | Only a presentation/provenance claim | Not task contradiction; escape is not a negative | No entailment bridge to substantive obligations |
| `OwnerResourceSupport` | Exact resolved grounding's native referent is owned by this observed resource | Resource contains every required contract, correct behavior, runtime identity, satisfied obligation | Exact owner/source-identity claim if caller explicitly requires that fact | Exclusive owner identity can conflict with a different declared exact owner under identical referent/frame; not general insufficiency | Ownership must be the claim, not inferred to imply adequacy |
| `MirroredResourceSupport` | Observed native source/test path correspondence in either permitted direction | Test exercises required behavior, covers source, passes or is necessary | Exact correspondence claim | Exact exclusive address mismatch under a formal claim; absent mirror is not contradiction | Path correspondence does not establish test semantics |
| `PythonReferenceResourceSupport` | Retained resource has exact positive native References to the grounded declaration, with occurrence/route support | All consumers, runtime invocation, correctness, binding beyond RI scope, complementary witness necessity | Exact supported static reference claim | A mutually exclusive identity for one exact occurrence could conflict with a typed claim; zero targets cannot | A reference is not the information required by the task |
| `PythonImportDependencyResourceSupport` | Exact direct source import declaration uniquely resolves its module portion to the candidate module resource | Member binding, export, transitive/facade dependency, runtime import, task necessity | Exact one-hop module-import claim | A different asserted unique target for the same declaration/universe can conflict; zero targets cannot | Dependency fact does not prove contract adequacy |
| `AnchorGrounding` | One supported native source referent for a caller locator when resolved; bounded ambiguity/miss/unsupported states otherwise | Witness support, runtime decorated identity, applicability, semantic absence from the repository | Exact locator/source-identity claim | Resolved exclusive source identity could conflict with a different exact claim; a locator miss cannot | Grounding is a fact bridge, not a satisfaction bridge; not independently admissible member basis |
| `LocalizationEvidenceReference` | Hashable caller-owned identity qualified by repository/snapshot | Truth of the referenced content, existence verification or entailment by itself | Never by the wrapper alone | Never by the wrapper alone | Inspect and validate its referent; current resolution further requires exact attached support membership |

Role evidence is not uniformly weak. All current `RoleSupportKind` values fall
into the following scopes; none establishes generic witness adequacy:

| Role bases | Exact scope / strength |
| --- | --- |
| `PYTHON_SUFFIX_CONVENTION`, `MARKDOWN_SUFFIX_CONVENTION`, `TEST_DIRECTORY_CONVENTION`, `DOCUMENTATION_DIRECTORY_CONVENTION`, `README_NAME_CONVENTION`, `PYPROJECT_NAME_CONVENTION`, `INITIALIZER_NAME_CONVENTION` | Observed address conventions; weak semantic hints |
| `MODULE_INTERPRETATION`, `PACKAGE_INTERPRETATION`, `PACKAGE_MEMBERSHIP`, `MIRRORED_TEST_PATH` | Qualified native RI observations; package membership/path truth is distinct from public API or test behavior |
| `PROJECT_DECLARATION`, `BUILD_DECLARATION`, `PYTEST_DECLARATION`, `TOOL_TABLE`, `TOOL_DECLARATION` | Recognized static declarations/table presence; not executed configuration or complete tool behavior |
| `PYTEST_TESTPATH_TARGET`, `PYTEST_BASENAME_GLOB`, `README_TARGET` | Bounded positive target/pattern interpretation; not exhaustive collection, authority or necessity |

Accepted `SupportedWitness` is an assertion with nonempty evidence references,
not another evidence-strength family. Readiness verifies accepted target coverage
and frame consistency. It cannot independently certify a resolver's reasoning.

## Proof standards and conservative outcomes

For **automatic proof-based SUPPORTED**, require a declared member claim, an exact
evidence proposition, and a validated machine-readable rule establishing that
proposition entails the claim under the named criterion and frame. The implication
from repository fact F to task criterion C must be explicit. Current native RI can
establish F, but current prose criteria and candidate reasons do not encode F ⇒ C.
Association integrity alone therefore cannot soundly auto-support semantic tasks.

For **semantic SUPPORTED**, require inspection of the relevant frozen content,
an explicit account of which information establishes the member's role in the
criterion, verifiable citations and reviewer acceptance in the initial slice.
This is an accountable semantic judgment, not a machine-verified entailment proof.
A model assertion, valid JSON or accurate quotation alone does not meet the proof
standard. Any future unreviewed acceptance requires prospective precision evidence
and an explicit authorization decision; this investigation supplies neither.

For **CONTRADICTED**, require an explicit incompatible claim/fact pair, identical
subject/frame, and the exclusivity/coverage conditions that make both incompatible.
For example, a caller-declared claim about the unique resolved target of one exact
import declaration can conflict with the native unique target in the same universe.
This requires formal claim meaning absent from current candidate reasons. It is
not evidence that the resource is useless. A positive owner/reference/import fact
usually cannot contradict a candidate's broad information-adequacy claim.

Do not infer contradiction from no match, low rank, no preferred role, an escape
tier, zero Reference/Import targets or missing channel membership. These sources
have positive/bounded semantics. Do not treat invalid/stale input as contradiction:
reject it at validation. Automatic contradiction should be disabled in the first
semantic pilot; an explicit reviewer may record it only with sufficient cited
incompatibility evidence. Evaluate proposals separately if a later frozen policy
includes automatic contradiction. Candidates remain represented in all cases.

Preserve **UNRESOLVED** for a policy that can judge the named claim but cannot
establish it or an incompatible fact from what it inspected. Preserve **ABSTAINED**
for declining adjudication: unsupported criterion/evidence capability, absent
required observation or unavailable semantic reasoning. Missing observation can
cause either, depending on whether the policy can adjudicate the claim with current
evidence; reasons must disambiguate. Neither disposition proves falsehood. No record
means unprocessed, not an explicit abstention. No frontier request is introduced.

## Architecture options challenged

| Option | Viable scope | Principal risk | Decision now |
| --- | --- | --- | --- |
| A: Localization-owned deterministic resolver | Integrity and typed entailment after a separately defined proof contract | Prose parsing/name conditionals leak task policy into kernel; proliferation and false support | Reject for current prose obligations; keep existing validation, not semantic acceptance |
| B: Caller-authored proof policy | Caller explicitly states a narrow native fact is sufficient for a member claim | Caller must author the difficult F ⇒ C bridge; a general proof DSL recreates task interpretation | Useful future niche; not the primary next implementation |
| C: External semantic resolver | Human/caller reasoner inspects task-relative content; optional model proposals with review | Inconsistent interpretation, hallucinated proof, cost, nondeterministic decisions | Selected: bounded semi-automatic pilot, provenance validation and review gating |
| D: Hybrid proof-first policy | Typed exact claims proven first; semantic remainder separately judged | No typed sufficiency contract exists now; trivial proof lane adds machinery while substantive tasks remain semantic | Plausible later convergence, not a minimal first increment |

An LLM is not logically required. A human already can supply current records.
A model might reduce repetitive inspection cost, but must demonstrate useful
selective precision against that baseline. Deterministic rules can be sufficient
for genuinely typed identity/relation obligations; they are not sufficient for
arbitrary contractual, test or documentation prose. Localization's accepted
responsibility does not imply that model invocation or task-specific reasoning
must live in its policy-free kernel.

A narrowly bounded future proof requirement could bind an exact subject and native
relation plus the caller's explicit assertion that this is sufficient for the
member criterion. All required facts would be conjunctive; alternatives would
remain explicit. Exact owner, reference and module-import requirements would need
separate native semantics. A `review-required` marker routes work but proves
nothing. Start with one fact family only if a prospective workload shows value;
do not build a general DSL/registry now. Proof-only success on trivial ownership
does not establish progress on information adequacy.

If hybrid becomes justified later, run exact declared proofs first. Run typed
contradiction only where exclusive claim semantics and coverage are validated;
otherwise abstain and pass the undecided claim to semantic review. Do not let a
later reasoner silently override a verified incompatible fact; a conflict requires
review of claim interpretation/frame. No support-count voting or winner selection.

## Claims, resources and content

Candidate association authoring asserts plausibility and complementary shape,
not sufficiency. Its mandatory `reason: str` is not a member proposition with a
formal truth condition. Generated relation supports explain how the resource was
proposed. [Candidate association documentation](../../src/devtools/context/localization/docs/overview.md#candidate-witness-association)
explicitly keeps these unresolved. Resolution must often inspect content, not
merely verify native evidence already replayed by association.

The current `CandidateWitnessMember.target` is specifically a
`RepositoryResourceOccurrence`, even though accepted `WitnessSet` targets are
general hashable identities. Grounding may retain finer native declarations, but
association projects them to resource targets. Do not propose switching candidate
targets to spans/declarations as though current typing already supports it.

Whole-resource support is defensible only as shorthand for an explicit claim
about information inside that resource. A file may supply several contracts, one
of them, or none; its candidacy cannot tell which. Fine-grained unit evidence and
whole-file necessary-witness labels are different. Even a HELPFUL or non-required
resource can prove a narrower fact: historical REQUIRED labels measure necessity
for implementing a task, not all possible true semantic claims.

Keep the existing resource target plus an explicit caller-owned claim and selected
content citations first. Do not add a universal `CandidateMemberClaim` ontology:
"declares D", "tests behavior B" and "authoritative validation guidance" have
different proof/authority semantics. If repeated precise claim families earn
promotion, introduce a narrow typed requirement later. Native finer subjects may
be cited as reasoning context through current support; changing member target
typing would be a separate authorized architecture increment.

Exact content is already present in `RepositoryResourceOccurrence.content`, with
address/content identity/encoding/byte size retained, and reachable through the
candidate view. The kernel does not provide selection of a documentation section,
interpret test behavior or certify content citations. An external policy should
receive bounded relevant retained content, not read the current checkout, fetch
an entire repository or put raw copies into each resolution record.

## Smallest governed external seam

For one existing candidate member, a caller-owned decision artifact should bind:

1. Exact task/obligation/repository/snapshot, concrete hypothesis identity and
   member target; generated family lineage retained.
2. Relevant task text/provenance, obligation predicate, criterion statement/name,
   applicability context and an explicit member claim supplied before adjudication.
3. Each selected native support independently, including scope/limitations.
   Native ranks and routing positions are provenance, not proof preferences.
4. Bounded retained target content, optionally exact excerpts and offsets; the
   complementary-member context needed to understand what this member must supply.
   Include competing context only when needed for interpretation, not choosing a
   winner. Supporting multiple competitors is allowed.
5. Policy identity/version and capability limits; input/citation and work limits.
   Exceeding disclosure/reasoning limits leads to abstention, not truncated proof.

Output proposes an existing disposition, claim, reason, exact attached-support
basis and caller/policy provenance. An excerpt sidecar records resource/content
identity, offsets and verbatim text where used. Validate offsets/substrings against
retained content. Excerpt correctness is not entailment correctness.

**Current basis limitation:** `CandidateMemberResolution` accepts only identities
that are the exact attached lexical/role/routed/structural support objects. It does
not accept an arbitrary content-span reference, unattached grounding or sidecar as
`basis`. Resolve opaque output handles to the retained support objects; never let
a reasoner forge Python identities. Citation sidecars belong to the external
decision artifact; `TaskProvenance.source_identity` can reference its hashable
caller-owned identity, with explanation retaining the link. Do not misuse
`TaskTextSpan` as a repository-content span. This proposed external artifact is not
a new production durable schema. Selected content is already in the retained
member target; citing attached proposal evidence preserves lineage but still does
not certify the semantic inference drawn from that content.

Deterministically validate output enum, nonblank text, exact criterion, candidate
and member membership, repository/snapshot/task/obligation compatibility, attached
basis membership and duplicate decisions using existing constructors/view. Validate
the sidecar independently and retain its immutable input/output definition. Reject
malformed citations rather than silently repairing them into SUPPORTED. Semantic
review verifies claim adequacy, authority, complementarity and entailment. No
validator can turn syntactically valid model output into repository truth. Do not
substitute another member's support or pretend new external evidence is attached;
if an adequate admissible basis is unavailable, abstain.

The initial adapter records review-accepted judgments; unreviewed proposals remain
external. Human review is an explicit decision, not the model's self-certification.
It can change a proposed disposition with its own provenance. Maintain a snapshot
with one final record per member, not event sourcing in Localization. Record
proposal/review differences in the external experiment artifact. Promotion is a
separate explicit downstream operation, not a default consequence of a proposal.

The caller/agent composition owns semantic policy and authorized invocation.
Existing model infrastructure, if selected, provides inference capability; it does
not own Localization criteria. Do not put provider/model code into Localization,
Retrieval, Python RI, association or generation. No new learned-intelligence domain
is justified. A future reusable language-neutral adapter could be promoted only
after bounded empirical evidence; orchestration still owns execution limits and
authorization. Reusing current record validation does not authorize general Agent
loops in narrow Runtime.

Retain policy/rule/prompt definition identity and version, input artifact identity,
evidence/task frames, output artifact and review decision. If model-mediated,
retain exact model/provider/configuration and rendered input/output as externally
owned provenance. Deterministic validation can replay; model output need not be
bitwise reproducible, even with fixed settings. Capture returned output once and
replay admission, rather than claiming identical regeneration. No full ML lifecycle
or numeric confidence contract is needed.

## Candidate association is upstream, not semantic resolution

Lexical acquisition does not populate `CandidateWitnessView` automatically. Future
end-to-end recall needs a bounded association policy; resolution cannot consume
raw lanes or recover unassociated resources. That pressure is real, especially
for nonstructural policy/docs/test evidence.

It is **not a prerequisite to the first resolution-policy experiment**. There are
existing caller-associated hypotheses and generated children; callers can freeze
a bounded lexical-associated batch using current APIs before policy outputs or
gold are observed. Preserve native support and explicit member claims/shape. This
tests conditional resolution ability without pretending candidate association is
solved. Include lexical and non-code candidates, not only structural examples.

Do not flood association with every match, create a new ranker or use gold to pick
the batch. Freeze candidate inclusion and report its independently adjudicated
recall separately. The resource surface is incomplete by design; conditional
resolver recall must not be reported as task-wide witness recall. If the pilot
shows good supported precision but low candidate-set recall dominates completion,
bounded lexical association becomes the next concrete prerequisite. It should
produce unresolved hypotheses and plausible claims, never pre-accept witnesses.

## Aggregate historical motivation

Only the following aggregate committed measurements inform this recommendation;
no resource paths, gold identities or individual missed cells define policy.
Own-native and routed unions are completion prefixes, not new shared rankings.

| Case / committed source | Global positive surface / task completion | Own / routed prefix unique resources | Structural aggregate conclusion |
| --- | --- | --- | --- |
| [0004](../../experiments/codex_dogfood/case_0004/analysis.md#interpretation) | 17/17 required resources globally reached; completion 325 | Own 256; routing not this treatment | Obligation decomposition shallower for 7/8 obligations; large review surface remains |
| [0005](../../experiments/codex_dogfood/case_0005/analysis.md#frozen-measurements) | 512 positive; completion 342; all required globally reached | 151 / 160, versus minimum 22 | Role routing reduces summed occurrences but enlarges resource union; cross-role witnesses matter |
| [0006](../../experiments/codex_dogfood/case_0006/analysis.md#3-baseline-lexical-and-routing-comparison) | 528 positive; completion 155; 33/33 required occurrences reached | 81 / 216, versus minimum 16 | Observed generation zero: unsupported source grounding, not proof that relations/resolution fail |
| [0007](../../experiments/codex_dogfood/case_0007/analysis.md#4-actual-structural-surfaces) | 518 positive; completion 346 | 249 / 378, versus minimum 19 | 19 structural resources; 10/55 required cells, 1/11 complete obligations; Reference adds zero required cells |
| [0008](../../experiments/codex_dogfood/case_0008/analysis.md#5-operator-surfaces) | 520 positive; completion 361 | 241 / 394, versus minimum 21 | 19 structural resources; 15/50 required cells, 24/71 unit judgments, 19/35 units, 10/22 required resources, 2/13 complete obligations |

Case 0007 has 32 hypotheses: 1 exact resource-structural match, 17 partial and 14
no-gold matches. Case 0008 has 28: 3 exact, 7 partial and 18 no-gold matches.
These labels concern resource/alternative structure, not measured semantic
resolver precision. A sound resolver should not promote such candidates merely
because their supports replay. It also cannot manufacture missing complements.

Case 0008 Reference adds zero required cells beyond OWNER/MIRROR. Import adds one
required cell/unit judgment/distinct unit and two unique required resources, with
no new complete obligation. The [stopping decision](../../experiments/codex_dogfood/case_0008/analysis.md#13-stopping-decision)
retains all four channels, lexical safety and other evidence, and selects no fifth
relation. Gold's fine-grained units and alternative structures make resource-level
match an inadequate semantic-resolution target.

Case 0006 is recovery-qualified and its grounding counterfactual is not observed
generation. Case 0008 is `GENERATION_RECOVERY`: initial harness aliasing failure
occurred before candidate projection; generation-only recovery did not rerun
lexical/routing/grounding or change treatment. Its limitations remain, including
the recorded lack of a separate recovery-raw canonical SHA-256 pin. None of these
historical aggregates measures the new recording kernel or this proposed policy.
One repository and differing tasks/frames do not establish universal superiority.

## Prospective design before policy implementation

Use a **new** prospective task after this investigation. Freeze an experimental
protocol before executing the policy; independently blind adjudicate afterward.
The following are proposed protocol requirements, not a newly frozen case:

1. Freeze exact task interpretation/applicability frame, candidate inclusion,
   caller claims and complementary/competing shape. Freeze exact snapshot/content,
   supports, disclosure/call/work limits, policy definition and output protocol.
   Neither associator nor policy may see adjudication. Do not revise a claim after
   seeing its verdict. Preserve lexical safety independently.
2. Include source contracts, tests and authority/documentation criteria; include
   lexical-only and structural candidates, multiple complementary members,
   plausible distractors, explicitly insufficient evidence and inapplicable cases.
   Applicability adjudication is separate from member resolution. Include typed
   exact-fact diagnostic claims without letting trivial claims dominate results.
3. Compare explicit human-review baseline with bounded semantic proposals on the
   same frozen members/content budget. If a model arm is authorized, freeze model,
   prompt/settings/call limits before outputs. Use no ranking, scores or confidence.
   Existing deterministic lineage checks are a control, not a resolution policy.
4. Gold adjudicators inspect criterion, claim, target and exactly the evidence
   available to the arm. Independently determine whether the claim is established,
   incompatible, insufficient or outside adjudication scope, with exact content
   evidence and reasons. A separate full-snapshot task-witness adjudication measures
   missing candidates/alternatives; do not conflate unavailable evidence with falsehood.
5. Preserve valid gold alternatives and acceptable extra supportive hypotheses;
   all members must establish the intended conjunctive information claim. A
   redundant true member need not be REQUIRED. If gold cannot decide, retain
   unresolved gold and report it separately, not as a forced negative.
6. Capture returned proposals, machine rejection, review corrections and final
   admitted records separately. Evaluate promotion in a sandboxed experiment;
   do not let pilot outputs mutate production assessment/readiness or live tasks.

### Prediction target and metrics

Primary gold target: **does the cited available evidence establish this frozen
member information claim under this obligation criterion?** Include content/span
evidence where defensible without inventing universal information-unit identities.
This matches the existing semantic judgment contract most directly.

Historical REQUIRED membership is secondary necessity/coverage evidence; it is
not a binary truth label for every proposed claim. Whole-hypothesis gold additionally
asks whether all conjunctive claims together form an acceptable satisfying witness
alternative. Exact resource-set equality is a diagnostic, not the sole success
definition: multiple valid or redundant supported candidates can coexist.

Freeze denominators and semantic review procedure before execution:

- **Supported precision:** correct established claims among emitted SUPPORTED
  decisions, separately for unreviewed proposals and review-accepted records.
- **Supported recall:** correctly supported claims among gold-supportable members
  in the supplied candidate/evidence frame. Separately report task-wide required
  unit/alternative recall including unassociated resources.
- **Contradiction precision:** correct explicit incompatibilities among emitted
  CONTRADICTED decisions. If none emitted, precision is undefined, not 100%.
  Report gold-incompatible recall only where gold has decisive incompatibility.
- **Selective risk:** incorrect decisive support/contradiction among decisive
  decisions; also report each class separately so one cannot conceal the other.
  **Decision coverage:** decisive decisions divided by eligible member cases.
  Report the coverage/precision pair and coverage meeting the prospectively chosen
  accepted-precision gate. Choose that gate in the future protocol, not post hoc.
  No confidence threshold or production confidence field is implied.
- **Abstention**, **unresolved** and **unprocessed** rates separately; provenance/
  citation rejection rates separately from semantic errors. Abstention is safer
  than false support but must not win by doing no work: pair it with recall and
  completion. Undefined denominators remain undefined.
- **Hypothesis precision:** genuinely satisfying complementary explanations among
  completely supported hypotheses. Count false complete support on distractors,
  missing complements and wrong shapes. **Witness-completion recall:** applicable
  obligations with at least one sound complete alternative relative to gold,
  reported both conditional on candidates and end to end.
- **Promotion precision:** sound complete accepted witness sets among explicit
  promotions; applicable-obligation coverage through normal assessment separately.
  Supporting a single member is not completing an obligation.
- **Burden:** hypotheses/members inspected, distinct resources and excerpts read,
  disclosed bytes/tokens, reasoning calls, reviewer corrections/time and latency.
  Count native validation/replay separately from reasoning cost where measurable.

False support is the principal initial risk because it permits false promotion.
Conservative abstention reduces that risk without eliminating alternatives.
An excessively strict policy can safely prove trivial facts but fail substantive
completion; measure both precision and coverage. Overall accuracy is inappropriate
as the headline because unnecessary resources dominate historical cell frames.

Old Cases 0004–0008 may supply aggregate baselines, architecture diagnostics and
generic fixture ideas. Do not select claims/rules/seeds by their gold paths, tune
prompts against their verdicts or report replay as prospective validation. New
policy effectiveness requires a new frozen policy/task/candidate/evidence frame
and independent blind claim judgments. No confirmation outcomes are inspected.

## Exact first bounded slice and next step

### Experimental adapter implementation status

The non-production [external decision adapter](../../experiments/codex_dogfood/semantic_resolution/README.md)
now packages existing members, caller-authored claims, exact criteria and explicit
bounded target-resource excerpts. It validates structured proposals and exact
citations/support lineage, retains separate human ACCEPT/REJECT reviews and permits
only explicit ACCEPT-gated materialization into existing kernel records. Pilot
proposals exclude contradiction. Stable JSON artifacts support contextual replay
and overwrite refusal. No model, automatic policy, association, promotion,
effectiveness-case freeze/execution or production semantic change accompanies it.
This is experimental support, not accepted resolution behavior or evidence of
semantic accuracy. The next step is the separately frozen prospective evaluation.

The implemented experimental adapter supplies the bounded slice over a
caller-frozen `CandidateWitnessView`: one member, explicit claim, criterion and
bounded frozen-content citations. It preserves exact native supports and requires
human semantic acceptance before recording. This initial pilot excludes
CONTRADICTED proposals entirely; explicit human contradiction remains available
outside the pilot through the kernel. Promotion remains separately explicit.
No general associator or proof DSL is prerequisite to this small slice.

Freeze a new prospective evaluation protocol before running this adapter. Test
whether a constrained external semantic policy improves safe supported precision,
witness completion and inspection cost over explicit human review on the same
inputs. If justified by a separately authorized arm, test model proposals with
review; no model/provider is chosen here. Only after this evidence decide whether
to promote a reusable adapter, formalize a narrow typed proof requirement, or
address bounded lexical association as the limiting upstream operation.

No production semantics, provider coupling, numeric confidence, learned policy,
ranking, candidate elimination, frontier acquisition, Context Planning, structural
operator/bound changes, historical replay or automatic resolver implementation
is authorized or performed by this investigation.
