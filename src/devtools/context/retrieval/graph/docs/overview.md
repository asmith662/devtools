# Query-conditioned structural resource ranking

Repository Intelligence (RI) owns deterministic repository facts. Retrieval
projects those facts into snapshot-bound graph views and ranks resources for a
query. The graph is neither repository truth nor a disclosure decision. The
resource-only view reproduces the first forward Imports and References
baseline; typed views test whether declaration identity helps.

```text
BM25 ranks ──> resource-node personalization
                         │
                         ▼
 resource ──contains──> function / class ──contains──> method
    │                          │                         │
    └─imports─> resource        └─direct base─> class      └─references─> declaration
                         │
                         ▼
              weighted Personalized PageRank (PPR)
                         │
                         ▼
             max node mass per resource
                         │
                         ▼
              ranked Retrieval evidence
                         │
                         ├─ optional Reciprocal Rank Fusion (RRF) with BM25
                         ▼
                  Context Planning
```

All observed resources are nodes. Typed views add direct module-body
function, class, and direct method nodes. A Reference edge starts at the
innermost supported declaration containing its exact source occurrence, or
at the resource if none does, and ends at its resolved declaration. Direct
Call remains a Reference tag. Exact RI facts, spans, relation families, and
directions remain on edge contributions. Graph self-transitions are omitted,
but same-resource References between declarations survive. Occurrence nodes
are unnecessary for this comparison because edge supports retain occurrences;
package initializers remain resource nodes.

The **typed core** view projects forward Imports and References, both
navigation directions of declaration containment (resource/class to direct
declaration and back), and child class to resolved direct base class. Return
containment edges are Retrieval navigation, not reverse RI facts. Imports and
References have no reverse propagation. The **typed navigation** view adds
both directions of qualified immediate package membership and exact mirrored
source/test path correspondence. The latter does not claim testing, coverage,
or execution. Unresolved RI assessments create no edge.

In typed views, each node divides its outgoing mass equally among active
relation families, then equally among unique fact contributions in each
family. Duplicate fact identities count once. This is a transparent neutral
normalization, not an empirically tuned set of relation weights. The
resource-only view retains equal-per-fact row normalization. Every edge
records family, direction, native support, and transition probability.

Positive BM25 ranks put normalized `1/(60 + rank)` mass **only on resource
nodes**; declarations receive no independent copy of their file's lexical
mass. The unchanged PPR kernel uses damping `0.85`, personalized dangling
return, L1 tolerance `1e-10`, and at most 200 deterministic iterations.
No usable lexical mass produces an empty ranking. A typed resource's score
is the **maximum** stationary mass of its resource node or any supported
declaration in that resource. This avoids summing all declaration mass in
large files. Results retain node scores, the winning node, and incoming fact
flow. Typed resource scores do not sum to one and are not calibrated
relevance probabilities. Ties use lexical rank and canonical address.

Optional equal-channel RRF uses `1/(60 + BM25 rank) + 1/(60 + PPR rank)` and
retains both original rankings. BM25 seeds PPR, so channel agreement is not
independent corroboration. Ranking and fusion do not choose a Context budget,
span, sufficiency, or stopping rule. They operate on retained snapshot state
without reopening the working tree.

Graph-1/Graph-2 enumerated unranked reachable neighborhoods with large
candidate fan-out. This is query-conditioned ranking, not Graph-3. This PPR channel is
also not a complete Aider repository map: symbol rendering and compact
disclosure policy remain unimplemented. Global structural importance is now
implemented by the separate repository-map channel documented below, with
prospective usefulness still unestablished.

The [typed-view development replay](../../../../../../experiments/typed_graph_baseline/README.md)
finds restored declaration topology but no complete-depth gain over BM25 on
retained Case 0002. That tests these projections and aggregation rules, not
all graph ranking. The [original baseline](../../../../../../experiments/graph_ranking_baseline/README.md)
remains reproducible. Confirmation stays sealed.


## Separate global importance hypothesis

The [repository-map channel](../../repository_map/docs/overview.md) now uses
query-independent resource-uniform global PageRank on a dependency projection,
then combines it with compact symbol/path lexical relevance. Its transition
semantics and restart vector differ from PPR; both use the canonical stationary
walk arithmetic in `graph.walk`. Typed PPR remains available with unchanged
query personalization and resource projection. Aider itself can use personalized
PageRank; separating global importance and symbol relevance is an explicit
devtools adaptation, not a claim that Aider avoids diffusion.
