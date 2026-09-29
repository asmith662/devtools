# Retrieval

Production retrieval owns purpose-relative use of repository information. It
does not establish repository relationship truth or decide Context disclosure.

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

The lexical BM25 baseline remains a separate retrieval mechanism with its own
query and score evidence. No production union or ranking API combines it with
direct structural candidates yet.
