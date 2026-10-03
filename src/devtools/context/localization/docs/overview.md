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
rank, routed position, tier and selected role evidence. The builder checks the
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
