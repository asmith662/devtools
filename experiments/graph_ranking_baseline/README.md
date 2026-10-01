# Production-RI graph-ranking baseline: development replay

## Protocol

The production algorithm and parameters were fixed before the outcome join.
[`freeze.json`](freeze.json) records the forward RI projection, equal fact
weights, `1/(60+rank)` lexical personalization, damping `0.85`, tolerance
`1e-10`, 200-pass ceiling, and equal-channel RRF constant `60`. The ranking
path in [`evaluate.py`](evaluate.py) loads the retained Case 0002 snapshot,
lexical index, and 785 Import plus 30 Reference facts; it computes both query
arms and all three rankings before opening the independently frozen blind
adjudication. It verifies archive, snapshot, and exact resource content
identities. `development_results.json` is reproduced by:

```text
uv run python -m experiments.graph_ranking_baseline.evaluate
```

This is a post-design development replay of one real Codex task. The case was
not selected prospectively for graph ranking; its labels were frozen earlier
for a different dogfood question. No confirmation artifact was read or run.
All 302 resources in this case were adjudicated, so its ten required resources
form an exact case-local frame. The older Increment 25-36 development surfaces
do not retain compatible production RI facts and full native snapshots as this
archive does; projecting their experiment-only path edges as production facts
would change the tested mechanism. Case 0001 lacks the same retained native
input archive. Neither is silently included here.

## Results

`coverage` means required resources in the first K ranked resources; it is not
precision or a general usefulness estimate. The graph contains 302 resource
nodes and 279 aggregated forward edges. It needed 23 PPR passes in each query
arm. The complete ranked surfaces are large because all positive BM25 matches
receive seed mass. Graph PPR has 301 positive resources for the full prompt
and 294 for the short need, compared with 299 and 285 BM25 matches.

| Query | Channel | @5 | @10 | @20 | @30 | @50 | @100 | Last required rank | Candidates |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| Full prompt | BM25 | 3/10 | 4/10 | 6/10 | 6/10 | 10/10 | 10/10 | 43 | 299 |
| Full prompt | PPR | 0/10 | 0/10 | 1/10 | 4/10 | 7/10 | 10/10 | 84 | 301 |
| Full prompt | BM25 + PPR RRF | 3/10 | 4/10 | 5/10 | 7/10 | 8/10 | 10/10 | 62 | 301 |
| Short need | BM25 | 2/10 | 4/10 | 5/10 | 5/10 | 6/10 | 10/10 | 87 | 285 |
| Short need | PPR | 0/10 | 0/10 | 2/10 | 4/10 | 5/10 | 7/10 | 123 | 294 |
| Short need | BM25 + PPR RRF | 2/10 | 3/10 | 5/10 | 5/10 | 5/10 | 10/10 | 98 | 294 |

The graph adds two positive-ranked resources beyond full-prompt BM25 and nine
beyond short-need BM25; none is required. It rescues no lexical miss in this
case because both BM25 arms already reach all ten required resources. RRF
keeps the full-prompt top five unchanged but pushes the final required resource
from rank 43 to 62. It moves short-need coverage at ten from four to three and
the final required resource from rank 87 to 98. Some individual resources
improve modestly (for example full-prompt `composition.py` 13 to 12 and
`bm25.py` 33 to 30); those gains do not offset displaced required resources.

## Interpretation

This baseline does **not** earn default fusion or automatic Context admission.
Its negative result is specific to one case, one forward resource projection,
and equal fact weights. It does not prove that query-conditioned PPR is useless.
The graph has a separate coverage weakness: seven of the ten required resources
have neither incoming nor outgoing edge here. These include governance and
roadmap documents, configuration, the dogfood implementation file, and three
required test files. A forward use graph cannot structurally promote them;
their PPR mass derives only from lexical seeds and dangling redistribution.
The other three required resources each have one incoming edge. This sparse
task-relevant graph explains much of the failure without attributing all of it
to the PPR algorithm. Broad lexical personalization also seeds nearly every
resource, so this single case cannot distinguish the contribution of seed
concentration from graph structure.

For Codex, this result supplies no evidence that the graph would reduce the
35/43/87/132 candidate depths observed across the two prior dogfood cases.
Context Planning can consume ranked evidence but should not infer disclosure
or sufficiency from it. The exact next step is a prospectively frozen broader
development comparison with qualified production RI snapshots and task frames,
including explicit tests of source/test and configuration/document coverage,
before changing directionality, family weights, seed limits, or fusion weight.
Case 0001 and sealed confirmation remain outside this replay.
# Broader Reference substrate replay

`structural_replay.py` compares the frozen production graph input with the
newly derived bounded declaration References over the same retained development
snapshot. It verifies the frozen archive hash, derives rankings before reading
required-resource labels, and leaves Personalized PageRank (PPR) parameters and
the original forward Import/Reference projection unchanged. The result is
`structural_replay.json`. This is a topology diagnostic and a one-case replay,
not a prospective evaluation or a weight-tuning exercise. Confirmation remains
sealed.

The replay preserved all 30 archived positive References and produced 1,311
new-schema References. Of those, 742 use a same-module route, so the unchanged
resource graph drops their self transitions. The graph grew from 279 to 360
aggregated edges and isolated resources fell from 152 to 134. Four of seven
previously isolated required resources gained an incident edge; the remaining
three are `AGENTS.md`, `docs/roadmap.md`, and `pyproject.toml`. The full-prompt
last-required PPR rank changed from 84 to 87, and the short-need rank from 123
to 127. This is a connectivity gain with no complete-depth ranking win on the
retained case. The next graph comparison must address typed relation coverage
and resource-only projection loss before interpreting ranking weights.
