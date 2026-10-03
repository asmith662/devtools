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
declaration lookup and class-method containment. It preserves native
`RepositoryResourceOccurrence`, module interpretation, declaration knowledge,
and analysis/lookup evidence. It invents neither spans nor a universal entity
identity. Multiple exact module or declaration matches remain unranked and
ambiguous. Dynamic/decorated or otherwise unsupported declaration binding
abstains. A miss is bounded to that locator and supplied native frame; it is
not evidence that the task concept is absent from the repository.

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
| References, calls/callers, direct bases and package children | Potentially high-fanout | Deferred; no implicit incident-edge expansion |
| Recursive containment, import closure, graph neighbors/PPR/RRF | High-fanout or semantically unsafe as a witness | Excluded from v1 |

When a mirror recipe has resolved grounding, the mirror operator runs the
canonical RI derivation over the explicitly supplied snapshot. Each attempt
retains that native analysis, including coverage, and any exact
`PythonMirroredPathCorrespondence`; unresolved sources do not trigger it.
Each v1 member accepts **one** target. No target yields `NO_TARGET`; ambiguous,
unresolved or unsupported grounding abstains; more than one result yields
`MULTI_TARGET` and no candidate hypothesis. A multi-member recipe with any
failed member creates no partial hypothesis and no Cartesian product. Two
member recipes reaching the same resource within one complementary recipe
yield `DUPLICATE_TARGET`; separate caller-named competing recipes retain their
distinct explanations and may share a target. Exact duplicate structural
support is rejected rather than counted twice.

`MemberProjectionAttempt` records source referent, target count, accepted
cardinality bound of one, examined resource count, truncation flag and frontier
(empty for these exhaustive exact operators). Owner projection examines its
one resource; mirror derivation examines the supplied snapshot resource set.
No hidden graph walk or candidate rank is performed. The immutable view keeps
all recipe and member outcomes and exposes obligation, anchor, target,
no-target and cross-obligation queries. Zero target is a bounded projection
miss, never an irrelevance or repository-absence claim.

For a generated target, existing global and owning-obligation lexical matches,
positive role records and own-obligation routed candidates are attached by
exact resource identity when supplied. They are supplemental native evidence;
lexical-only results never create a hypothesis, and ESCAPE remains eligible.
The association builder validates all native supports and replays grounding
and mirror relationships. Generation changes neither accepted `WitnessSet`
alternatives nor `LocalizationAssessment`/readiness. It does no scoring,
confidence assignment, ranking, resolution or elimination. Effectiveness and
coverage remain untested pending a new prospective case.
