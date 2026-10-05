# Repository Localization semantic kernel

The independent [soft repository-role evidence package](../roles/docs/overview.md)
also provides snapshot-bound, multi-label positive supports from intrinsic
addresses and supplied native RI analyses. Explicit support kinds explain the
basis without scores, negative inference, hard filters or obligation satisfaction.
It executes no Retrieval and changes none of the lexical adapter's ordering.

The `devtools.context.localization` package owns caller-authored task information
obligations and a deterministic assessment of the supplied obligation frame. It
does not infer task obligations, choose Context
representations, or execute agent work.

```text
task interpretation (snapshot independent)
  shared anchors + task/source provenance
                 |
                 v
         information obligations
         mandatory/helpful + conditional applicability
                 |
                 v
       alternative witness sets
       (all members in one set)
                 |
                 v
       snapshot-qualified assessments
                |
                v
       frame readiness + diagnostics
```

## BM25 evidence acquisition

The Localization-side lexical adapter keeps task purpose and mechanism queries
distinct:

```text
task purpose -------------------------------+
                                             |
complete caller task text -> global BM25 safety lane
obligation identity + explicit query ------> obligation BM25 lane(s)
                                             |
                                             v
                      separate native ranked BM25 results
                                             |
                                             v
                  later Localization evidence resolution
```

`LocalizationLexicalAcquisitionRequest` binds the caller's task interpretation,
overall purpose, verbatim full-task query, ordered obligation queries, snapshot,
eligible lexical index, BM25 result limit, and settings. The full-task query is
executed as supplied; it is not shortened, rewritten, role-filtered, or weighted.
It provides a global lexical safety lane within the caller-authorized corpus.
Each explicit obligation query names a task-local query identity and an
obligation in that interpretation. Multiple queries may refer to one obligation.
The caller owns their wording. No query is synthesized from the obligation
predicate.

Every lane uses the existing production content-plus-filename BM25 operation
with the same supplied index, settings, and per-lane result limit. Output retains
the native `RepositoryTextLexicalBm25RetrievalResult` itself, including its exact
query, index/corpus, settings, limit, ordered matches, native scores, content and
filename contributions, and filename index. One-based rank is the match's
position in that native result. The overall purpose and selected repository /
snapshot identities are retained beside the lanes because BM25's result does not
own task purpose.

The global result is stored separately; obligation results remain in caller query
order. A resource surfaced by multiple lanes consequently has multiple
independently inspectable native results. There is no merged candidate ranking,
score comparison, agreement bonus, score normalization, or evidence fusion.
Rank and score are not confidence and never resolve an obligation. A zero-result
lane means only that the query surfaced no lexical result in that frame; it is
not non-applicability or negative evidence. No `src/`, `tests/`, or `docs/` role
scoping is applied. Acquisition validates obligation/query task identity and
membership, unique query identities, and the indexed resource occurrences
against the supplied repository snapshot before publishing the result.

## Caller-directed role routing

The optional `devtools.context.localization.routing` package transforms an
already acquired `LocalizationLexicalAcquisition` into a routed view. For each
query identity the caller supplies exactly one `ObligationRolePreference`,
including an explicit empty role tuple when no role is preferred. The preference
also names that lane's obligation. No mapping is inferred from obligation text,
identity, anchors or query wording. Several query lanes for one obligation keep
separate preferences and separate views.

```text
native obligation lane ----+-------------------------+
                           |                         |
                           v                         v
                 any preferred role?             escape
                           |                         |
                           +------ routed view -------+

native global full-task lane ---- retained unchanged
```

There are exactly two tiers: `PREFERRED_ROLE_SUPPORTED` and `ESCAPE`. Any
positive support for any caller-preferred role places that candidate in the
preferred tier. A candidate supporting several selected roles gets no extra
priority. The tier exposes the matching `ResourceRoleEvidence` records, which
retain their original support kinds and provenance. Candidates without a
matching role support remain in the complete escape tier. This means only “no
positive support for this preference”; it is not negative evidence.

Within each tier candidates keep their native BM25 order. Each view entry points
to the original match and exposes its one-based native rank, one-based routed
position and tier. A routed position is a presentation position, not a score or
new rank estimate. The full-task retrieval stays the exact original result, and
the complete acquisition plus each native obligation lane remain available.
Routing performs no retrieval, score calculation or comparison across lanes.
It preserves every candidate and does not alter Localization assessments,
witnesses, applicability, satisfaction or readiness. Tier order changes
attention only; it is neither filtering nor elimination.

The router checks repository/snapshot identity, retained role-frame entries and
support provenance, verifies native lexical corpora against that frame, and
requires preferences to cover exactly the acquired query lanes with matching
obligation identities and supported role enum values. Routing remains an
interpretation layer over the caller-authorized lexical corpus, not a new
Retrieval channel or success claim. Any effectiveness evaluation must be
prospective and freeze its obligations, queries and preferences before
Retrieval.

`LocalizationTaskIdentity`, `LocalizationAnchorIdentity`, and
`LocalizationObligationIdentity` use caller-named stable keys. Anchors retain
task-local text and optional task-source provenance; they do not assert that a
repository entity exists. An obligation states a desired-information predicate,
its shared anchors and provenance, mandatory/helpful status, optional conditional
applicability, a named satisfaction criterion, and one or more alternative
witness sets. Every target in one witness set is conjunctive; any complete set is
an acceptable alternative. Targets remain native or caller-owned hashable
identities rather than being wrapped in a new universal information-unit type.

Assessment evidence references and obligation assessments bind to a repository
and retained snapshot identity. The package stores no repository content. The
task interpretation itself may precede snapshot selection; only assessments
derived from repository evidence are snapshot-bound. Frame assessment rejects
missing, duplicate, unexpected, stale, cross-repository, or internally
inconsistent dispositions. It reuses the generic identity-coverage primitive
from Evaluation for frame accounting; Localization retains obligation meaning.

`READY` means every applicable mandatory obligation in the supplied frame has a
supported resolved or non-applicable disposition. `CONDITIONAL` permits handoff
only when a caller explicitly accepts a named deferred observation; it is not
full readiness. Open, abstained, or unaccepted deferred mandatory obligations
block handoff. Unresolved helpful obligations remain diagnostic and do not block
mandatory readiness. The result makes no claim that the frame lists every real
task obligation or that a coding agent will succeed.

Localization is not Retrieval ranking, Context representation choice, agent
execution, or Evaluation outcome ownership. This adapter associates native BM25
results with caller-authored obligations, but it does not create witnesses,
assess applicability, or change readiness. Context Planning may later use
obligation provenance when selecting representations; that integration is not
part of this package's current contract.

## Exact task-anchor grounding

`devtools.context.localization.grounding` connects a shared task anchor to
native RI referents only through a caller-authored `AnchorGroundingRequest`.
Anchor text is task interpretation, not a Python symbol, module, path or
repository fact. The request names its task and anchor, repository and snapshot,
an explicit typed locator, and the caller's interpretation provenance. No
locator kind is inferred from anchor text.

```text
SharedAnchor -> GroundingRequest -> bounded native resolver
                                    |-> RESOLVED native referent
                                    |-> AMBIGUOUS native candidates
                                    |-> UNRESOLVED exact locator miss
                                    +-> UNSUPPORTED current RI scope
                                      -> future witness-hypothesis generation
```

V1 locators are an exact `RepositoryResourceAddress`; a canonical dotted
Python module name in an explicitly supplied, snapshot-checked module universe
(optionally constrained to ordinary module or package); a directly supported
module-body function/class declaration under that module locator; and an exact
direct method name under an already identified native class declaration. The
resolver delegates to snapshot resource lookup, Python module lookup, direct
source declaration selection and class-method containment. It preserves native
`RepositoryResourceOccurrence`, module interpretation, declaration knowledge,
and analysis/lookup evidence. It invents neither spans nor a universal entity
identity. Multiple exact module or declaration matches remain unranked and
ambiguous. Declaration locators consume
`select_python_module_source_declarations`, independently of direct-binding
lookup. Decorated direct ClassDef, FunctionDef and AsyncFunctionDef resolve
when exactly one native source declaration matches the requested kind/name.
Direct method grounding preserves its known native class-parent contract,
including decorated methods; it makes no descriptor or callability claim.

For declaration locators, RESOLVED means exactly one supported native source
declaration satisfies the locator. AMBIGUOUS retains multiple matching native
declarations or an incompletely interpreted competing module that prevents
uniqueness. UNRESOLVED means no supported direct declaration matches; a kind
mismatch, assignment, nested declaration or dynamic construction is not silently
coerced. UNSUPPORTED means the requested frame/form cannot be soundly interpreted
by current RI (for example, source parse failure or no explicit module universe).
Runtime binding uncertainty alone does not cause UNSUPPORTED. A source result
does not identify the post-decoration module attribute or imported runtime
object, including effects of descriptors, metaclasses and rebinding. Binding
and imported-member resolution retain their independent existing contracts.
A miss is bounded to that locator and supplied native frame; it is not evidence
that the task concept is absent from the repository.

The immutable `AnchorGroundingView` orders explicit requests deterministically,
finds results by anchor or disposition, and maps a native referent back to all
task anchors that grounded to it. It also lists anchors with no resolved locator,
including those with no request. It does not assign a referent to an obligation,
create a candidate witness hypothesis, accept a witness, change assessment or
readiness, rank candidates, eliminate alternatives or produce confidence.
Grounding is language-neutral task-relative state; its Python adapters consume
Python RI. Imported-member and configuration declaration locators, free-text
semantic matching, and automatic locator inference are outside this bounded
contract. The bounded generator below consumes successful groundings; the
grounding contract itself still creates no hypothesis.

## Candidate witness association

`devtools.context.localization.association` holds caller-supplied, unresolved
`CandidateWitnessHypothesis` alternatives for one task obligation. A hypothesis
contains one or more `CandidateWitnessMember` values: every member is proposed
together, while several hypotheses for the same obligation compete. The
`WitnessHypothesisIdentity` is a caller-named task-obligation-local key for
inspection and replay, not a second repository identity or scored assignment.
One observed resource may appear in hypotheses for several obligations.

```text
native Retrieval / role / routing evidence
                 |
                 v
candidate witness members + explicit caller reasons
                 |
                 v
unresolved competing or complementary hypotheses
                 |
                 v
future evidence resolution (not implemented)
                 |
                 v
accepted WitnessSet alternatives -> LocalizationAssessment -> readiness
```

The current member target is an exact `RepositoryResourceOccurrence` in the
supplied `RepositorySnapshot`. This bounded target admits exact frame checking;
finer declarations and source occurrences require their own native identity and
containment validation before joining this API. It does not create a universal
information-unit model. Members retain an explicit human-readable association
reason and individual native supports: a `LexicalMatchSupport` references the
actual BM25 match, its global or obligation query lane and native rank;
`ResourceRoleEvidence` retains its native support kinds and derivation identity;
`RoutedMatchSupport` references the original routed candidate and its native
rank, routed position, tier and selected role evidence. `OwnerResourceSupport`
and `MirroredResourceSupport` retain exact grounding and, for mirrors, the
native source/test correspondence. The builder checks the
task, repository, snapshot, target, query/obligation lane and exact native
support membership against the supplied acquisition, role view and routed view.
It retains those native input views beside the hypotheses, so original query
text, index semantics, role derivation and routing explanation remain inspectable.
Several supports remain separate and are never aggregated into a number.

`build_candidate_witness_view` only validates and orders caller-supplied
hypotheses. Member, support and hypothesis ordering use stable native keys,
not evidence strength or relevance. `for_obligation`, `for_target`, and
`cross_obligation_targets` inspect them without ranking. It generates no
hypothesis from rank, role, tier, path or score. The view neither mutates
accepted witness sets nor produces a `SupportedWitness` or
`LocalizationAssessment`. Candidate association is thus
distinct from Retrieval, ranking, accepted witness satisfaction and readiness.
There is no confidence, rejection, elimination or automatic resolution.

## Explicit evidence-to-witness resolution

The language-neutral `devtools.context.localization.resolution` package records
explicit caller judgments over an existing validated `CandidateWitnessView`.
Caller-associated lexical candidates and generated structural candidates use
the same contract. It does not associate every lexical match automatically.

```text
candidate association / generation
        |
        v
explicit member decisions with exact native evidence
        |
        v
completely supported candidate hypothesis
        |
        v
explicit promotion: WitnessSet + SupportedWitness values
        |
        v
caller-created assessment -> existing readiness
```

`CandidateMemberResolution` retains the exact candidate view, hypothesis and
member, the obligation's `SatisfactionCriterion`, a claim, reason, named caller
and `TaskProvenance`. Task, obligation, repository and snapshot identities derive
from that retained context. `basis` uses existing `LocalizationEvidenceReference`
values whose identities are exact support objects attached to that member:
lexical, role, routed or structural support. Foreign frames, substituted support,
equal-but-copied support and duplicate references are rejected. Basis order follows
the member's canonical native support order. No new universal evidence identity
is introduced. This is an in-memory contract, not a durable serialization format.

Member dispositions are `SUPPORTED`, `UNRESOLVED`, `ABSTAINED` and `CONTRADICTED`.
Support and contradiction require nonempty explicit evidence bases. Unresolved
means current evidence does not establish the member; it is not negative evidence.
Abstention records a caller declining to decide. Contradiction records the caller's
explicit incompatible-fact claim and cited basis; absent support never implies it.
The kernel validates evidence lineage, not the logical truth of a caller's claim.
V1 bases cite attached native candidate evidence; it does not introduce an external
repository-evidence ontology. Rank, routing tier, relation kind and support count
never determine a decision. Contradiction does not remove a candidate.

`WitnessResolutionView` validates the retained association frame and admits an
explicit subset with at most one decision per candidate/member. An empty view is
valid over a nonempty candidate frame. `for_member` and `for_hypothesis` return
`None` when no decision exists, separately from explicitly unresolved records.
For recorded hypotheses, any contradicted member yields `CONTRADICTED`; every
complementary member explicitly supported yields `COMPLETELY_SUPPORTED`; all
other shapes yield `UNRESOLVED`, including abstentions and unrecorded members.
The immutable view canonicalizes by association order and member resource address.
It exposes complete, unresolved, contradicted and unrecorded hypotheses, supported
obligation presence and concrete child decisions by family. Competing hypotheses
and siblings remain independent. Family identity stays on each generated child;
no family-level judgment is inferred.

`promote_supported_hypothesis(view, identity)` is an explicit operation requiring
complete all-member support. Its `PromotedWitnessHypothesis` retains the resolution
and exposes the existing complementary `WitnessSet` plus `SupportedWitness` values
with native targets. Each witness retains the cited native evidence references
and a snapshot-qualified reference to its immutable member decision. The criterion,
caller, provenance and candidate lineage remain available through that decision.
Promotion neither registers a new accepted alternative nor mutates an assessment.
The caller uses existing assessment APIs and accepted alternatives; readiness
still checks normal applicability and mandatory witness coverage. Supporting a
candidate alone does not satisfy an obligation or make a task ready.

There is no automatic resolver, ranking, scoring, elimination, temporal event
history, frontier/acquisition request, autonomous execution or Context admission.
The four existing structural operators remain bounded candidate channels.
Aggregate prospective evidence motivates this semantic seam, without replay or
an effectiveness claim for the new kernel.

## Bounded candidate-witness generation

`devtools.context.localization.generation` instantiates caller-authored
`WitnessGenerationRecipe` alternatives. Every `GroundedMemberRecipe` names an
exact grounding result, one operator, a caller key, reason and interpretation
provenance. Members within one recipe are caller-proposed complements; distinct
named recipes compete. Neither relationship, anchor text, obligation predicate,
lexical query nor role preference invents this shape.

```text
SharedAnchor -> exact Grounding -> caller recipe -> typed RI projection
                                           |             |
                                           |             + native relationship support
                                           v
                         unresolved CandidateWitnessHypothesis
                                           + native lexical/role/routing support
                                           |
                                           v
                                  FUTURE resolution
```

| Native relation inspected | Classification | V1 use |
| --- | --- | --- |
| Referent to its observed owner resource | Low-fanout exact projection | `OWNER_RESOURCE`: resource, module, direct declaration or method to one resource |
| Exact observed Python source/test mirror | Low-fanout exact projection | `MIRRORED_RESOURCE`: one supported counterpart in either direction; correspondence is a path fact, not test coverage |
| Immediate package membership / initializer surface | Bounded direct relation | Deferred: its explicit selected module-analysis frame and surface meaning need a separate input contract; initializer presence is not public API proof |
| Exact direct containment and declaration ownership | Low-fanout exact projection | Already represented by owner projection |
| Configuration declarations/selectors and import/member binding | Bounded multi-target or qualified relation | Deferred pending a task-relative target and operator contract |
| Exact declaration References, including direct Call tags | Bounded explicit inverse relation | `REFERENCING_RESOURCE`: caller-supplied Python native analyses to distinct referencing resources; requires explicit branching |
| Exact resolved module-import relations | One forward static import step | `DIRECT_IMPORT_DEPENDENCY_RESOURCE`: caller-supplied import analyses and resolutions to target module resources; requires explicit branching |
| Direct bases and package children | Potentially high-fanout | Deferred; no implicit incident-edge expansion |
| Recursive containment, import closure, graph neighbors/PPR/RRF | High-fanout or semantically unsafe as a witness | Excluded from v1 |

When a mirror recipe has resolved grounding, the mirror operator runs the
canonical RI derivation over the explicitly supplied snapshot. Each attempt
retains that native analysis, including coverage, and any exact
`PythonMirroredPathCorrespondence`; unresolved sources do not trigger it.
Fixed `GroundedMemberRecipe` values still accept **one** target. No target yields
`NO_TARGET`; ambiguous, unresolved or unsupported grounding abstains; more than
one result yields `MULTI_TARGET` and no candidate hypothesis. Every fixed member
must succeed. Repeated complementary resource targets yield `DUPLICATE_TARGET`.
OWNER and MIRRORED retain their existing single-target semantics.
REFERENCING_RESOURCE consumes the explicit Python Reference input described
below and requires a branching member. Branching itself adds no automatic
relation selection or fanout policy.

### Caller-authorized branching families

A caller may supply one `BranchingGroundedMemberRecipe`, including an explicit
positive `max_results`, alongside zero or more fixed members. Two branching
members are rejected. There is no Cartesian expansion. A branching recipe must
use `WitnessHypothesisFamilyIdentity`; a fixed recipe retains its caller-named
`WitnessHypothesisIdentity`. These task-local identities are distinct from RI
identities and accepted witness identities.

For example, a future relation could support this caller-authored shape:

```text
family: owner + one-of(reference targets)
complete targets: T1, T2, T3
children: (owner, T1), (owner, T2), (owner, T3)
```

REFERENCING_RESOURCE now supports this shape when explicitly selected.
It never produces `(owner, T1, T2, T3)`. Members within each child are proposed
complements; children within a family compete as unresolved explanations.
Other caller-authored families may also compete for the same obligation.
Competition neither proves sufficiency nor requires exactly one child to be
accepted. The family, branch target, concrete child, accepted witness alternative
and satisfied obligation remain distinct.

Every concrete child is an ordinary `CandidateWitnessHypothesis` constructed
through the existing association validation. Its distinct
`GeneratedWitnessHypothesisIdentity` retains the caller family, branching member
key, repository/snapshot and exact native resource occurrence. Its canonical JSON
key encodes task, obligation, family, slot, repository, snapshot, address and
content identity with explicit versioning. It uses no ordinal, random value,
rank or execution order. Caller literal and generated identity types have
separate namespaces. Duplicate candidate identities are rejected. Unequal target
or structural support values colliding under canonical native keys are rejected
rather than selected by insertion order. Caller keys continue to own the meaning
of their frozen task/recipe; no durable serialization schema is introduced.

### Complete enumeration and independent bounds

`MemberProjectionAttempt.projections` retains `ProjectedMemberTarget` values:
one exact resource with only its supporting native structural facts. Repeated
identical targets are grouped; identical support is retained once, and distinct
support is preserved in canonical order. Its legacy `targets` and `structural`
queries expose diagnostics; child construction uses target-specific support.
A child never receives other branches' support. Fixed support is retained in
every successful child.

The projection owns `work_performed`, optional relation-specific `work_limit`,
`complete`, and `uncovered_frontier`. Work units are operator-owned: OWNER
examines one resource; MIRRORED examines the supplied snapshot resource set and
retains its native analysis. Generation does not interpret relation scan
mechanics or impose a hidden work quota. Projection accounting must stay within
the declared work limit. `examined_resources` preserves existing operator
work diagnostics; `truncated` reports incomplete enumeration.

The branching member owns the independent result admission bound. After complete
enumeration, `result_count` is the exact distinct projected target count; when
work is incomplete it is `None`, even if diagnostic targets are retained.
Incomplete work yields `WORK_BOUND_EXCEEDED` and **zero children**. A complete
set exceeding `max_results` yields `RESULT_BOUND_EXCEEDED`, retains the exact
count and yields **zero children**. No first-K, path prefix, source prefix or
insertion prefix is admitted. Deterministic ordering is reproducibility order,
never relevance rank. A result cap is not a computational work bound.

### Family outcomes and failure atomicity

A `HypothesisGenerationAttempt` retains one attempted recipe/family and all
member diagnostics. `hypothesis` remains singular for fixed recipes and is
`None` for branching families; `children` exposes successful hypotheses for
both paths. A branching family retains independent `BranchGenerationAttempt`
values containing exact child identity, target-specific projection, disposition,
hypothesis when generated, and diagnostic reason.

Before branch instantiation, any fixed member failure yields
`FIXED_MEMBER_FAILED` with its exact member outcome and zero children. Invalid
fixed frame/support is retained as `INVALID_MEMBER` with its reason. Repeated
fixed complementary targets yield `DUPLICATE_TARGET` and zero children. Source
failure, incomplete work and result overflow also admit no branches. A complete
zero-target branch yields `NO_TARGET`; it remains visible as an attempted empty
family. One target takes the same child identity path as several targets.

After complete, in-bound enumeration, branch-specific duplicate complementary
targets yield `DUPLICATE_TARGET`; invalid frame/support combinations yield
`INVALID_BRANCH` and retain the validation reason. Valid siblings may succeed.
Family disposition is `GENERATED`, `GENERATED_WITH_BRANCH_FAILURES`, or
`ABSTAINED` when every enumerated combination fails. No incomplete child is
emitted. Zero children never prove that no satisfying witness exists.

The immutable view retains all families, children and failures. Existing
obligation, anchor, target, no-target and cross-obligation queries remain;
`for_family` exposes the attempted family, `children` and `failed_branches`
inspect its results, and `parent_family` resolves successful or failed child
lineage. Plan, recipe, member, grounding, native support and frame remain
available through that lineage. Flat `generated` convenience queries preserve
ordinary association semantics without losing family provenance.

For generated targets, existing global and owning-obligation lexical matches,
positive role records and own-obligation routed candidates attach by exact
resource identity. They cannot prune branches or alter cardinality; ESCAPE
remains eligible. The association builder validates native supports and replays
grounding and mirror relationships. Generation changes neither accepted
`WitnessSet` alternatives nor `LocalizationAssessment`/readiness. It performs no
scoring, ranking, acceptance, satisfaction, resolution or elimination. Reference
RI remains unchanged; Case 0007 is neither frozen nor executed. Effectiveness
requires a later prospective case.


### Exact Python referencing-resource projection

`REFERENCING_RESOURCE` selects only positive native
`PythonDeclarationReferenceKnowledge` facts whose exact `target_subject` and
`target_declaration` match the resolved grounded function, class or supported
direct method declaration. Resource/module groundings are not guessed into
seeds. Existing ambiguous, unresolved and unsupported grounding outcomes remain.
Class seeds never absorb references targeting their methods. Decorated source
declarations can ground while binding-oriented Reference RI yields no matching
facts; no decorator guard is weakened.

The caller supplies `WitnessGenerationPlan.python_references`: an immutable
`PythonReferenceProjectionRequest` containing the exact module interpretation
universe, finite `PythonReferenceSourceInput` analyses with their original source
interpretations, and an explicit nonnegative `work_limit`. There is no filesystem
scan, implicit universe acquisition, cache or inverse index. Native input order
inside universe/source interpretation provenance is preserved for exact replay;
analysis, fact and target presentation use canonical identities without ranking.

Work units are **distinct supplied source analyses** authorized for canonical
replay and complete positive-fact enumeration. The adapter preflights the entire
source-analysis count: if it exceeds `work_limit`, no native analysis is replayed
or enumerated, work performed is zero, completeness is false, target count is
unknown and all source resources remain an uncovered frontier. The retained
request identifies every unexamined native analysis, including multiple analyses
of one resource. Metadata/frame checks are independent integrity checks. This
analysis-count bound is not a byte, fact-count, CPU-time or total validation-cost
budget; one analysis can contain many assessments and facts. Acquisition happened
before projection and is not represented as projection work. Association may
replay native support again for integrity, without acquiring or replacing truth.

When the whole frame is authorized, each supplied analysis is compared to
`derive_python_declaration_references` replay over retained snapshot content and
the exact supplied native inputs. Foreign repository/snapshot/resource/universe
metadata, missing interpretations, altered coverage/assessments or forged facts
are rejected. Replay validates supplied RI; it does not silently replace it or
reopen the working tree. Enumeration considers all positive facts and excludes
unresolved/ambiguous/unsupported assessments, textual matches and imports alone.

Several matching References in one source resource become one
`ProjectedMemberTarget`, retaining all distinct exact facts in
`PythonReferenceResourceSupport`. Support preserves grounding/request, native
source analysis, occurrence/span, declaration/subject, resolution route, import
provenance, Call tag, frame and operator identity. Association replays grounding
and native analysis, checks authorized-frame membership, exact fact membership,
seed equality and source occurrence/resource ownership. Duplicate facts are
canonicalized; conflicting equal identities are rejected. Children receive only
support establishing their own target. No occurrence-count score is computed.

`direct_call` remains a syntax tag on a Reference, not another candidate or
operator and not runtime invocation. An import may participate in retained
resolution provenance but does not itself generate a target. A base-expression
Reference can qualify as a Reference without asserting inheritance. Existing
one-facade Reference resolution may qualify without adding a public-export or
facade-generation relation. There is no package, `__all__`, recursive import or
neighbor traversal.

Same-owner exact References remain eligible. A fixed owner and identical branch
resource are handled by existing `DUPLICATE_TARGET` branch outcomes; the adapter
never filters that resource. Complete zero targets yields scoped `NO_TARGET`,
not a claim that the declaration is unused at runtime. One or several in-bound
targets use existing family/child identities and branching unchanged. The sole
result bound is the branching member's `max_results`: complete overflow retains
the exact count and creates no children or first-K subset. Lexical/role/routing
support attaches afterward and cannot determine Reference eligibility or fanout.

### Direct static Python import dependency resources

`DIRECT_IMPORT_DEPENDENCY_RESOURCE` consumes the existing qualified
`PythonResolvedModuleImportRelation`, in the forward direction only. The native
chain is an explicit-root source module, direct `Module.body` import declaration,
unique `PythonImportResolution`, exact target module interpretation and that
module's observed resource. Localization defines candidate use of this fact;
it adds no Python binding or dependency truth. See the
[import RI contract](../../python/imports/docs/overview.md).

The caller supplies `WitnessGenerationPlan.python_import_dependencies`, a
`PythonImportDependencyProjectionRequest` with the exact module universe,
`PythonImportDependencySourceInput` records and a nonnegative `work_limit`.
Each source record retains its module, exhaustive native declaration analysis
and one canonical resolution for every declaration, including nonpositive
outcomes. Sources are canonicalized by native module identity. There is no
implicit acquisition, working-tree read, source-root discovery or text search.

Module groundings use their exact interpretation; direct class/function
groundings use the module retained by native source selection. Direct method
groundings require exactly one owner-resource interpretation in the supplied
universe. Arbitrary resource groundings are unsupported. Missing source inputs
abstain as unsupported; competing method owner interpretations are ambiguous.
Grounding replay remains mandatory before generation and association.

Targets are deliberately **module-level**: `import P.M` and its alias select
the exact interpreted `P.M` resource; `from P.M import Name` selects the same
module resource. This asserts only resolved module-portion import provenance,
even if `Name` has no supported declaration binding. It does not assert that
Name exists, is importable or exported. `from . import Name` targets the resolved
package module, with no member-to-submodule fallback. Relative imports use RI's
source-package interpretation and beyond-package guards. A package target owns
its actual interpreted initializer resource; an ordinary module is never
redirected to an initializer. One-facade imported-member RI remains separate:
the operator does not follow facade imports or select a final defining member.

Only unique positive native module resolutions create candidates. Missing,
ambiguous and unsupported module resolutions yield no target. Star declarations
are explicitly excluded even when their module portion resolves. Dynamic calls,
module `__getattr__`, nested and control-flow imports are outside direct
module-body coverage. These boundaries do not claim exhaustive runtime imports.
Target modules are never expanded: A importing B and B importing C produces B
from A, with no C unless A directly imports C itself.

Several declarations resolving to one resource yield one projected target with
all exact native relation support. `PythonImportDependencyResourceSupport`
retains grounding, request, source analysis and every positive relation, including
declaration ordinal/span, alias, relative qualification, source/target module,
universe, resource/content and repository/snapshot provenance. Association checks
authorized membership and replays the canonical import analysis, resolutions
and relation derivation against retained snapshot content. Foreign frames,
forged resolutions, altered coverage, wrong subjects and mismatched target
resources fail validation. Ordering uses native resource/identity keys only.

One work unit is the exact selected source-module analysis replayed in full,
including every declaration resolution. Work quota is per member projection,
not cumulative across a plan. A limit below one performs no source replay,
returns incomplete work with the source resource as frontier, and admits no
children. Metadata/frame checks and subsequent integrity replay are separate
from this analysis-count bound; it is not a declaration, byte or CPU budget.

The existing branching `max_results` is the independent result bound. Complete
zero results produces `NO_TARGET`; one or several in-bound resources create one
competing child each, optionally with fixed complementary members. Complete
overflow retains all diagnostic targets and the exact distinct count, with no
children or first-K prefix. Self-import targets are preserved, so fixed-owner
collisions retain the existing duplicate-target branch disposition. No family
model or automatic complementary structure is introduced.

Import dependency support stays distinct from Reference support. Neither creates
export/public-API truth, runtime import results, relevance, scores, ranks,
accepted witnesses, obligation satisfaction or readiness. Aggregate Case 0007
evidence motivates this hypothesis only; this increment neither replays that
case nor claims effectiveness. The subsequent prospective Case 0008 closed the
current structural-breadth phase; aggregate conclusions motivate explicit
resolution while retaining lexical safety and the four bounded operators.
