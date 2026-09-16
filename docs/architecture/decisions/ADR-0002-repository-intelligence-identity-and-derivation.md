# ADR-0002 — Repository intelligence identity and derivation semantics

- Status: Accepted
- Date: 2026-09-16
- Scope: semantic architecture for future repository intelligence and coding
  Context. This decision authorizes no production implementation, storage,
  parser, graph, retrieval system, or Context compiler.

## Context

Existing filesystem and Tool boundaries establish bounded file access, not
repository identity, repository knowledge, retrieval, or Context compilation.
Earlier bounded Qwen navigation evidence proved only root-origin fact
acquisition. It did not establish reusable inventory, ranking, symbol search,
retrieval, selection, budgeting, or compilation semantics.

Repository intelligence must be useful independently of a language model. It
also must make incremental reuse and invalidation explainable without mistaking
a checkout path, Git commit, or heuristic rename for foundational identity.
Coding Context is separately the purpose-relative selection and disclosure of
such information to a task or model.

## Decision

### Repository state and identity

A **Repository** is a logical software repository across changing states. It
has nominal logical identity. Its identity is not its filesystem path, current
contents, Git commit, or a particular checkout. A repository may be backed by
a Git checkout, temporary fixture, generated workspace, extracted archive, or
another supported resource arrangement. `ResolvedPath` and filesystem
Resources remain access and location mechanisms; they do not acquire
repository-identity meaning.

A **RepositorySnapshot** is one immutable complete included repository-content
state under defined snapshot semantics. Its identity is content-derived, not
merely timestamp- or Git-commit-derived. A snapshot need not be a physical copy
of all files. Git metadata may be provenance associated with a snapshot, but
does not define snapshot identity: dirty working-tree states can share a Git
HEAD while being different snapshots.

Snapshot semantics are relevant to identity. Inclusion policy for ignored and
generated files, binaries, symlinks, submodules, multiple roots, and related
cases remains open. Merkle-compatible hierarchical content identity is strongly
motivated because it permits efficient structural comparison and incremental
reasoning, but this ADR selects neither a hash algorithm nor an exact Merkle
representation.

Do not create a magical persistent file/resource identity. A repository
resource occurrence is instead contextual: a snapshot plus a repository-
relative address/path, independently referring to content-addressed content.
Exact production naming, including whether `ResourceOccurrence` is used, is
open. Identical content has stable content identity across snapshots and
locations under applicable content semantics:

- an edit changes content identity;
- a move changes occurrence/address but can preserve content identity;
- a copy creates another occurrence referring to the same content identity;
- deletion removes the occurrence; deletion/recreation of identical content
  need not assert historical object continuity.

`RENAMED_FROM`, `MOVED_FROM`, `COPIED_FROM`, and entity evolution are derived
knowledge, not foundational identity. Likewise, symbols, document sections,
and other repository entities may have structural identity only within the
source/knowledge state establishing them. Cross-snapshot entity continuity is
future derived knowledge with evidence, never hidden inside an identity
primitive.

### Derivation and DerivedKnowledge

A **Derivation** represents the semantics of a knowledge-producing
transformation. Its effective identity accounts for analyzer/derivation kind,
implementation or semantic revision, and relevant configuration. The concrete
representation is open. The invariant is:

> Equal derivation identities imply equivalent derivation semantics for
> identical relevant inputs.

Any change capable of changing results—such as parser behavior, analysis
configuration, embedding model, or relationship-resolution semantics—must be
reflected in derivation identity or validity. A downstream ranking-policy
change must not invalidate repository knowledge that does not depend on it.

**DerivedKnowledge** is a foundational semantic concept, not a required Python
base class. It is knowledge produced by an identified Derivation over explicit
identified dependencies, with result/value and provenance. Its identity should
be reproducibly associated with derivation, dependencies, and result semantics,
not merely an arbitrary UUID. Exact digest construction is open, including
whether result participates directly when determinism permits derivation plus
dependencies to determine it.

The validity rule is:

> DerivedKnowledge is valid when its explicit dependency identities are
> satisfied under the same relevant derivation semantics.

Snapshot provenance and applicability differ. Knowledge derived from unchanged
content B while observing snapshot S1 may remain applicable at S2 when the
relevant occurrence/content dependencies still hold. Preserve its original
provenance; do not invalidate it merely because it was first observed at S1.
This enables targeted reuse, caching, persistence, replay, provenance, and
potentially distributed derivation without claiming universal cross-snapshot
continuity.

Dependency scope is separate from knowledge value shape. Resource/content-local
derivations may include parsing, syntax extraction, definitions, lexical
structures, and document structure. Multi-resource or knowledge-dependent
derivations may include resolved imports, references, calls, inheritance,
test, documentation, governance, and change-impact knowledge. The architecture
does not freeze `IntrinsicKnowledge` or `RelationalKnowledge` as categories:
“`foo.py` defines `Foo`” can be relational in value shape while depending only
on one resource. DerivedKnowledge may depend on other DerivedKnowledge.

Thus a B-content change can invalidate B parsing, then B symbol knowledge, then
cross-resource relationships depending on it, while unrelated A knowledge
remains reusable. A global transitive rebuild is not required when dependency
identities establish validity.

### Two graph families

The architecture distinguishes two non-equivalent graph families.

The **derivation dependency graph** answers what knowledge depends on which
inputs or prior knowledge. It supports provenance, validity, invalidation,
recomputation, and reuse:

```text
content -> parse knowledge -> symbol knowledge -> resolved-reference knowledge
```

The **repository semantic/knowledge relationship graph** answers how resources,
entities, and concepts relate. Eventual typed relationships may include
`DEFINES`, `REFERENCES`, `IMPORTS`, `CALLS`, `INHERITS`, `TESTS`/`EXERCISES`,
`DOCUMENTS`, `GOVERNS`, and change relationships. It supports repository
understanding, traversal, structural retrieval, impact analysis, and Context
discovery.

These graphs are not one graph merely because both use edges. Neither must be
globally materialized, share storage, or use a graph database. Semantic graph
architecture is independent of physical storage. Different task-specific views
may eventually include file-dependency, symbol-reference, call, inheritance,
test, documentation, and governance graphs; multiple views may contribute
independent relevance evidence concurrently.

Relationships are DerivedKnowledge values: subject, typed predicate, object,
and relevant evidence/metadata. They do not need a separate foundational
`RelationshipId`; their derivation, dependencies, provenance, and reproducible
knowledge identity provide lineage. One universal canonical repository graph is
not accepted.

### Repository intelligence and Context

Repository intelligence produces deterministic knowledge independently of an
LLM. Context is purpose-relative selection, transformation, representation,
and model/task disclosure of relevant information. Retrieval produces evidence
for possible relevance; ranking is not repository truth and remains distinct
from final selection; Context compilation remains distinct from retrieval.

Future mechanisms may combine exact/identifier, lexical, structural,
relationship/graph, optional semantic, and historical/change-based retrieval.
They may preserve multiple relevance signals, use task-sensitive deterministic
or learned ranking, and select representations such as whole files, source
regions, symbols, or document sections. Deduplication, overlap, diversity,
ordering, budgeting, provenance-bearing disclosure, disclosure history, and
reuse remain necessary pressure, not selected mechanisms.

Repository-derived model content is untrusted data, not policy, instruction, or
execution authority. Progressive disclosure may provide high-confidence initial
orientation, accept bounded requests for more information, and compile targeted
follow-up Context without forcing topology rediscovery. A model request remains
descriptive: materialization, validation, authorization, and execution remain
outside the model call. Repeated compilation does not make a compiler an
orchestration loop; orchestration remains above deterministic retrieval and
Context compilation.

Evaluation pressure includes retrieval/context quality, calls, input/output/
total tokens, repository operations and repeated reads, task success,
iterations, elapsed time, and cost. The intended long-term outcome is reduced
expensive-model repository archaeology, progressively reduced Codex dependence,
and eventually local Qwen-family models capable of primary or sole coding-work
roles. No metric, harness, model policy, or worker loop is selected here.

### Identity taxonomy

| Concept | Accepted semantic identity |
|---|---|
| Repository | Nominal logical identity across changing states. |
| RepositorySnapshot | Immutable content-derived complete included state under snapshot semantics. |
| Resource occurrence | Contextual snapshot plus repository-relative address. |
| Content | Content-derived identity reusable for identical content. |
| Repository entity | Structural identity in relevant source/knowledge state; no assumed permanent continuity. |
| Derivation | Semantic identity of a knowledge-producing transformation. |
| DerivedKnowledge | Reproducible identity tied to derivation/dependencies/result semantics. |
| Relationship | DerivedKnowledge value shape, not an independent foundational identity. |

## Decision consequences

| Change | Required consequence |
|---|---|
| Edit content | New snapshot and changed-content identity; affected derivations invalidate while unrelated unchanged knowledge can remain reusable. |
| Move/rename unchanged content | New snapshot and occurrence/address; same content identity and potentially reusable content-local knowledge. Rename continuity remains derived. |
| Copy unchanged content | Distinct occurrences may refer to one content identity. |
| Delete | The new snapshot lacks the occurrence; globally retained knowledge of its content need not be destroyed. |
| Git branch/checkout change | New snapshot; unchanged content knowledge may still be reusable. |
| Parser/analyzer upgrade | Snapshot can remain identical; changed Derivation identity requires affected knowledge recomputation. |
| Ranking-policy change | Repository knowledge remains valid unless it explicitly depends on ranking. |
| Cross-resource resolution | A B change need not invalidate A local parse/symbol knowledge, but can invalidate relationship knowledge depending on B. |

## Deferred and open pressure

This ADR intentionally leaves open: hash/digest and Merkle representation;
snapshot inclusion policy; ignored/generated files, binaries, symlinks,
submodules, multiple roots, and filesystem race/atomicity semantics;
persistence, cache, serialization, derivation-dependency storage, graph
storage, cross-repository content reuse, and external/environment-dependent
derivations; parser/analyzer technology and entity locators; confidence/evidence
for heuristic knowledge; lexical choices such as grep/BM25/trigram; embeddings,
vector storage, graph algorithms, learned ranking, task-sensitive strategy
selection, call graphs, historical co-change, change impact, test/code,
documentation/code, and ADR/governance relationships; disclosure-history and
Context caching ownership; progressive-acquisition orchestration; and evaluation
infrastructure and exact metrics.

## Status and implementation boundary

This decision settles semantic architecture only. It does not claim that any
new production types, protocols, indexes, parsers, graph views, persistence,
retrieval, ranking, Context compiler, Tool, Agent, Runtime loop, or evaluation
system exists. B-0002 retains the unimplemented repository-intelligence and
coding-Context pressure. B-0008 is superseded as the earlier narrow
root-navigation investigation whose semantic question is now answered here.
