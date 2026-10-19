# graph_ranking_baseline: CLOSED

## Objective and method

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

## Result and decision

Diagnostic replay: expanded connectivity without a complete-depth ranking win.

## Provenance and reproduction

The manifest binds every preserved input/output byte and the committed source revision. Existing source documents contain exact datasets, baselines, configuration, commands, per-case outcomes and scientific decision rules; their original content is unchanged. Restore using the manifest before replay. No model operation or new adjudication occurred during closeout.

## Limits and subsequent work

A closed diagnostic/development checkpoint is not confirmation, a production policy or general agent competence. Unknown outcomes remain unknown. Frozen dependency-bearing originals remain in place; the root-report archive is the only compacted current-tree payload. Local packets share the SSD and do not protect against disk loss.

## Reopening

Preserve this manifest, original revision and packet. A separately authorized continuation must identify a new linked run/protocol and reason for reopening; never overwrite these results or infer an execution grant from restoration.
