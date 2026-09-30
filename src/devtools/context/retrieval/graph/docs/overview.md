# Query-conditioned structural resource ranking

This production Retrieval mechanism projects qualified Python Repository
Intelligence into a snapshot-bound, purpose-specific resource graph view. It
does not create repository relationship truth. The view's nodes are all observed
resources in the supplied snapshot. Edges are forward `importer -> imported`
and `reference occurrence resource -> declaration resource` transitions.
`direct_call` is a tag on a Reference contribution and is counted once.
Distinct source occurrences contribute separate equal weights; duplicate
presentations of the same RI fact identity contribute once. Self edges are
omitted. Every edge retains the exact native fact, its relation kind, aggregate
weight, and row-normalized transition probability. The view has no package
membership or reverse transitions. Missing RI facts establish no negative
knowledge.

```text
                  query
                    |
                    v
               BM25 ranking ---------------------+
                    |                             |
                    v                             |
        reciprocal-rank personalization          |
                    |                             |
                    v                             |
             typed RI graph view                  |
                    |                             |
                    v                             |
          weighted PPR ranking                    |
                    |                             |
                    +-------------+---------------+
                                  v
                           equal-channel RRF
                                  |
                                  v
                       ranked retrieval evidence
                                  |
                                  v
                         Context Planning
```

The default personalization weight of a positive BM25 match at one-based rank
`r` is `1/(60+r)`, normalized over all retained matches. BM25 scores are not
probabilities. No positive lexical matches produces an empty graph ranking.
PPR uses `p_next = 0.15*s + 0.85*P^T*p`, with dangling mass returned to `s`,
an L1 tolerance of `1e-10`, and at most 200 deterministic passes. It starts at
`s`, normalizes final mass, and sorts by descending score, then lexical rank,
then canonical address. The result records convergence, iteration count,
parameters, the graph view, the native lexical query/result, resource rank,
score, seed mass, and per-fact incoming stationary flow. Scores are stationary
walk mass, not calibrated relevance probabilities. A disconnected resource can
rank only when it receives lexical seed mass.

`fuse_lexical_graph_rankings` uses equal-channel reciprocal rank fusion:
`1/(60+BM25 rank) + 1/(60+PPR rank)`, omitting absent terms. It retains both
original result objects and native matches/supports. The PPR list is seeded by
the BM25 list, so fused channel agreement is not independent corroboration.
Neither ranking nor fusion selects disclosure, a budget, or sufficiency.
Callers supply already-derived RI and a retained snapshot/index; ranking never
reads the working tree.

This differs from Graph-1/Graph-2. Those historical experiments enumerated
one- and two-step reachable neighborhoods and accumulated a large unranked
candidate surface. This mechanism asks which resources carry stationary mass
relative to a query, bounds hub fan-out by outgoing normalization, attenuates
long paths by restart, and emits a total ranked evidence list. It is not
Graph-3 and does not enumerate paths. It is inspired by repository-map-style
structural importance, but is query-conditioned and ranks whole resources; it
does not implement Aider's symbol rendering, weights, or token budget. A global
prior could be evaluated separately later, without changing RI truth.

## Architecture decisions

| Choice | Decision | Alternatives and reason | Owner, exclusions, and what it enables |
| --- | --- | --- | --- |
| Graph abstraction | Derived typed resource view over production RI | A universal repository graph would assign retrieval weighting to repository truth. | Retrieval owns the view; RI owns facts. No graph store. Allows other views later. |
| Node model | Snapshot resource addresses | Symbol nodes preserve finer flow but add a graph ontology before resource-level value is shown. | Retrieval owns diffusion state; exact symbol/occurrence RI stays in edge supports. Enables later symbol projection. |
| Relations | Imports and qualified References, including direct Call tags | Containment describes organization, not use; duplicate Call facts would overcount. | RI owns semantics; Retrieval selects transitions. Direct structural retrieval still offers membership and reverse lookup. |
| Direction | Forward use/dependency only | Symmetric transitions produced historical reverse-import fan-out and return paths. | Retrieval projection, not reverse RI truth. A separate dependent view remains possible. |
| Weights | One per unique fact, then normalize each source row | Research suggests differentiated weights but gives no validated constants. | Retrieval owns an untuned v1 policy; labels cannot alter it. Retained types permit future ablation. |
| Seeds | Positive lexical ranks converted by `1/(60+r)` | Raw BM25 scores are not calibrated across queries; uniform seeds discard query evidence. | Retrieval owns query conditioning; explicit anchors can be added later with a separate rule. |
| Walk | Damping 0.85, L1 tolerance `1e-10`, 200 passes, personalized dangling redistribution | Hop counts omit ranked multi-step flow; global PageRank loses the task. | Retrieval owns score and convergence; no path enumeration. |
| Evidence | Native PPR ranks with incoming RI flow and full input provenance | An opaque graph dictionary or universal relevance score loses mechanism meaning. | Retrieval result informs Context Planning without deciding disclosure. |
| Fusion | Equal RRF at constant 60 | Adding raw BM25 and PPR scores assumes a common scale. A provisional unequal graph weight lacks validation. | Retrieval owns a transparent optional fusion; both rankings remain intact. |

The [development replay](../../../../../../experiments/graph_ranking_baseline/README.md)
found that this first graph does not improve required-resource depth on the one
retained production-RI dogfood case. It remains an independently testable
structural evidence mechanism, not a default Context admission policy. The
[research synthesis](../../../../../../docs/research/repository-context-planning-and-graph-assisted-retrieval.md)
motivates the hypothesis; the replay tests this particular projection.
