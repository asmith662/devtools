# typed_graph_baseline: CLOSED

## Objective and method

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

## Result and decision

Completed typed-view diagnostic replay, not a prospective effectiveness claim.

## Provenance and reproduction

The manifest binds every preserved input/output byte and the committed source revision. Existing source documents contain exact datasets, baselines, configuration, commands, per-case outcomes and scientific decision rules; their original content is unchanged. Restore using the manifest before replay. No model operation or new adjudication occurred during closeout.

## Limits and subsequent work

A closed diagnostic/development checkpoint is not confirmation, a production policy or general agent competence. Unknown outcomes remain unknown. Frozen dependency-bearing originals remain in place; the root-report archive is the only compacted current-tree payload. Local packets share the SSD and do not protect against disk loss.

## Reopening

Preserve this manifest, original revision and packet. A separately authorized continuation must identify a new linked run/protocol and reason for reopening; never overwrite these results or infer an execution grant from restoration.
