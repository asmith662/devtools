# Case 0016: Graph-3 Stage A

Prospective task-conditioned reference-PPR and canonical BM25 RRF experiment.
Primary comparison C versus A; B versus A is a structural diagnostic.
Stage A freezes only observations, implementation and protocol. No prospective
lexical retrieval, exact resolution, reference derivation/graph construction,
PPR, fusion, rankings, map or gold exists.

`uv run python -m experiments.codex_dogfood.case_0016.freeze --verify`
replays Stage A without retrieval or RI analysis.
Controlled tests are segregated under experiments/task_conditioned_graph.
Maintainer reviews STAGE_A_REVIEW.md before separately authorizing Stage B.
The prospective AMENDMENT.md replaces B's stationary-mass ordering with
TASK_CONDITIONED_REFERENCE_PPR_FLOW, excluding restart/dangling-only seeds from
B and RRF graph credit. Original Stage A remains immutable in its Git checkpoint.
Production behavior is unchanged; confirmation/reserve remain inaccessible.
