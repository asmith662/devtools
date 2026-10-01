# Retrieval

Production retrieval owns purpose-relative use of repository information. It
does not establish repository relationship truth or decide Context disclosure.

## Query-conditioned graph ranking

The [graph-ranking package](../graph/docs/overview.md) projects already-derived
Repository Intelligence (RI) facts into either the reproducible resource-only
view or typed resource/declaration views. Query-derived lexical rank mass seeds
weighted Personalized PageRank (PPR), which returns snapshot-bound structural
evidence. Optional equal-channel Reciprocal Rank Fusion (RRF) combines native
BM25 and PPR ranks while retaining both originals. The typed core view includes
declaration containment and direct bases; an additional navigation view
includes qualified package membership and weak mirrored paths. Neither
enumerates graph paths nor determines disclosure. The
[first replay](../../../../../experiments/graph_ranking_baseline/README.md)
and [typed replay](../../../../../experiments/typed_graph_baseline/README.md)
found worse complete required-resource depth than BM25 on one retained
development case. Graph ranking remains optional evidence.

## Direct Python structural projection

`retrieve_python_direct_structural_resources` accepts an identified
`RepositorySnapshot`, a `PythonDirectStructuralRetrievalRequest` containing a
nonempty purpose and distinct seed resource addresses, and already-derived
production RI facts: `PythonResolvedModuleImportRelation`,
`PythonFunctionReferenceKnowledge`, and `PythonImmediatePackageMembership`.
All seeds and fact endpoints must belong to the supplied snapshot. The caller
chooses and bounds the RI fact inputs; an omitted fact family produces no
negative knowledge.

For each seed, the operation projects one direct relation to its other resource
endpoint. Imports and References can project in either direction; immediate
package membership projects child to package or package to child. A direct Call
is the `direct_call` tag on the same Reference fact, not another relation.
Self relations do not yield a new resource candidate. No transitive traversal,
ranking, score, or fixed result limit is applied.

The result retains the request and snapshot identity. Each distinct candidate
resource is keyed by its snapshot identity and repository address, ordered by
its first support. Its supports retain the seed, direction, and exact native RI
fact; repeated presentation of the same fact for the same seed/direction is
deduplicated, while distinct declarations, occurrences, and relation families
remain independently visible. The native fact supplies derivation, source span,
target, resolution, and qualification provenance as applicable. Surfacing a
resource predicts possible usefulness for this request; it does not establish
relevance, select a resource for a budget, or choose a Context representation.

## Snapshot-bound resource evidence composition

`compose_lexical_structural_resource_evidence` accepts a caller-selected
`RepositorySnapshot` and explicit nonempty purpose alongside one native lexical
BM25 result and one native direct structural result. It does not make the lexical
query text into an InformationNeed or change either mechanism's result type.
The structural result and its candidates must match the invocation snapshot;
its request purpose must exactly match the invocation purpose.

The lexical corpus retains selected observed occurrences rather than a snapshot
identity. Composition therefore checks the corpus repository, every represented
document and indexed statistic, and each returned match. Every corpus resource
must be the exact observed resource at that address in the supplied snapshot.
This checks content identity even for corpus members that were not returned as
matches, since they can affect BM25 statistics. Missing or changed resources
reject composition; no cross-snapshot applicability is inferred.

One `LexicalStructuralResourceEntry` retains the snapshot ID and observed
resource, an optional native `RepositoryTextLexicalBm25Match`, and all distinct
native `PythonDirectStructuralResourceEvidence` supports. Repeated presentation
of the same match or structural support is deduplicated; independent supports
remain separate. The `LexicalStructuralResourceInventory` also retains the
original results and invocation purpose. Entries iterate by ascending canonical
repository address, a neutral deterministic inventory order. Native lexical
rank is retained as a separate one-based lexical rank on matching entries;
scores, field contributions, query, index, structural seed, direction, and RI
fact provenance remain available in their original forms. Missing
support from either mechanism makes no negative relevance claim.

```text
Repository Intelligence
        |
        v
mechanism-specific retrieval
   |             |
 lexical      structural
   |             |
   +------v------+
          |
resource evidence composition
          |
          v
optional rank fusion -> explicit Context disclosure choices
```

The composed result is a candidate/evidence inventory, not an actionable file
set. Resource selection under a limited budget remains an explicit unresolved
decision.
The historical structural union experiments remain reproduction evidence;
future production consumers use this composition operation for native direct
facts and lexical evidence.
