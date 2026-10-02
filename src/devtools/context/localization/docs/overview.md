# Repository Localization semantic kernel

The `devtools.context.localization` package owns caller-authored task information
obligations and a deterministic assessment of the supplied obligation frame. It
does not retrieve repository information, infer task obligations, choose Context
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
