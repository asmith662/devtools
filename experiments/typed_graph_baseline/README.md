# Typed graph ranking: retained development replay

This bounded Retrieval experiment tests whether typed declaration topology
improves query-conditioned resource ranking. It uses only the retained
Case 0002 development snapshot and adjudicated required resources.
Confirmation was not opened. The [freeze](freeze.json) fixed four graph
configurations, node and edge directions, family normalization, resource
aggregation, lexical personalization, Personalized PageRank (PPR) parameters,
and equal-channel Reciprocal Rank Fusion (RRF) before the evaluator joined
required-resource labels. The evaluator constructs all graphs and rankings
before reading the adjudication file. Later changes added diagnostics and
input validation, not ranking parameters. Run
`uv run python -m experiments.typed_graph_baseline.evaluate` to reproduce
the [development result](development_results.json).

Repository Intelligence (RI) is the sole source of graph facts. This replay
does not infer new repository relationships. The frozen-input resource view
uses the original retained Imports and References. The current-RI resource
view uses broadened References. The typed core adds declaration nodes,
containment, and direct bases. The typed navigation view adds qualified
package membership and exact mirrored-path correspondence. All use one
production graph builder and one PPR kernel.

| View | Nodes | Aggregated edges | Isolated resource nodes | Resources in no cross-resource component |
| --- | ---: | ---: | ---: | ---: |
| Original resource forward | 302 | 279 | 152 | 152 |
| Current-RI resource forward | 302 | 360 | 134 | 134 |
| Typed core | 1,512 | 3,598 | 118 | 134 |
| Typed navigation | 1,512 | 3,935 | 99 | 99 |

Typed nodes comprise 302 resources, 509 direct module functions, 282
direct module classes, and 419 direct methods. Core edge contributions
include 785 forward Imports, 1,310 References, 32 direct bases, and
2,420 declaration containment/return directions. Navigation adds 398
package-membership and 54 mirrored-path directions. One of 1,311
Reference facts is a same-node transition and is excluded; many
same-resource References remain as declaration-to-declaration edges.
Every view leaves three required resources without a cross-resource
component: `AGENTS.md`, `docs/roadmap.md`, and `pyproject.toml`.
These are missing documentation/governance and configuration relations
in production RI, not reasons to invent graph edges.

The table shows the number of ten required resources covered by each
depth. “Last” is the rank at which all ten are covered; no fixed top-five
admission rule is assumed.

| Full prompt channel | @5 | @10 | @20 | @50 | @100 | Last |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| BM25 | 3 | 4 | 6 | 10 | 10 | 43 |
| Original resource PPR | 0 | 0 | 1 | 7 | 10 | 84 |
| Current-RI resource PPR | 1 | 1 | 3 | 9 | 10 | 87 |
| Typed core PPR | 0 | 1 | 2 | 6 | 9 | 146 |
| Typed navigation PPR | 0 | 1 | 2 | 4 | 6 | 207 |
| BM25 + typed core RRF | 3 | 4 | 6 | 8 | 10 | 82 |
| BM25 + typed navigation RRF | 3 | 4 | 7 | 9 | 10 | 96 |

| Short need channel | @5 | @10 | @20 | @50 | @100 | Last |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| BM25 | 2 | 4 | 5 | 6 | 10 | 87 |
| Original resource PPR | 0 | 0 | 2 | 5 | 7 | 123 |
| Current-RI resource PPR | 0 | 2 | 3 | 7 | 9 | 127 |
| Typed core PPR | 0 | 0 | 2 | 5 | 9 | 175 |
| Typed navigation PPR | 1 | 1 | 2 | 5 | 7 | 237 |
| BM25 + typed core RRF | 2 | 4 | 6 | 6 | 9 | 129 |
| BM25 + typed navigation RRF | 1 | 4 | 5 | 9 | 9 | 140 |

The typed graph restores topology but does **not** improve complete
required-resource depth here. Full-prompt typed core promotes
`retrieval/composition.py` from BM25 rank 13 to 6 but displaces
the dogfood capture implementation from 3 to 17 and `AGENTS.md` from
5 to 89, `docs/roadmap.md` from 2 to 84, and `pyproject.toml`
from 43 to 146. The navigation view promotes the capture implementation
to 6 and BM25 implementation from 33 to 13, but pushes the three
unconnected documents/config resources still deeper. RRF restores some
lexical strength, yet neither fused view beats BM25 complete depth.
All ten required resources are already in the BM25 list; no lexical
miss is rescued. Beyond the positive BM25 lists, typed core ranks two
additional resources for the full prompt and nine for the short need;
typed navigation ranks three and seventeen, respectively. These are
mostly package initializers and none is required. Required-resource ranks
and native edge provenance
are in the machine-readable result.

The typed core walk converged in 128 passes (about 0.41 seconds in one
warm replay); navigation converged in 112 (about 0.41 seconds), versus
23 passes (0.34 seconds) for the original resource view. These timings
are approximate, not a benchmark. About 46% of typed-core stationary
mass occupies declaration nodes, yet only 17 of 301 resource winners
are declarations under the prospectively fixed max aggregation. This
identifies an aggregation/propagation question, without licensing a
post-outcome adjustment on this case.

The result is case-local: one retained development task, known required
resources rather than exhaustive relevance judgments, and lexical seeds
in every PPR view. Never-adjudicated resources are not counted as
not-useful. Graph ranking remains optional evidence; Selection and
Context Planning retain disclosure authority. A stronger next comparison
needs a newly frozen task/frame and should prospectively distinguish
resource aggregation and repository-map-style global structural priors
from query-conditioned walk behavior. It must not tune this case.
