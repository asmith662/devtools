# bm25_sensitivity: CLOSED

## Objective and method

This non-installable evaluation consumer depends on native Retrieval and R1.5
diagnostics; production never imports it. The [protocol](PROTOCOL.md) was
committed before historical nonbaseline scoring. A baseline integrity audit
corrected Case 0008's eligibility before the full grid: two own-lane misses make
full completion undefined. All six frozen cases are replayed, and required-reach
safety includes all six; deterministic role selection uses five complete cases.

The 180-point [machine-readable development capture](development.json.gz)
retains absolute/normalized metrics, identities, ranking digests, full surfaces,
all alternatives, reach partitions, prefix compositions and top-K data. Native
historical baseline order/scores and every parameter pair's native field scoring
oracle agree with R1.5 reconstruction. No historical source is replaced by current
files. [Analysis](analysis.md), [interpretation](interpretation.md) and
[representative R1.5 diagnostics](diagnostics.json.gz) preserve tradeoffs and losing
configurations. Timing in `costs.json` is development replay, not runtime latency.
`sensitivity_details.json` retains per-case main slices, every obligation's range
and finite pair-interaction contrasts. `summary.summarize` replays those descriptive
projections from the frozen grid without new scoring or challenger selection.

## Result and decision

MIXED / NO SAFE REPLACEMENT; frozen Case 0010 result; no production parameter change.

## Provenance and reproduction

The manifest binds every preserved input/output byte and the committed source revision. Existing source documents contain exact datasets, baselines, configuration, commands, per-case outcomes and scientific decision rules; their original content is unchanged. Restore using the manifest before replay. No model operation or new adjudication occurred during closeout.

## Limits and subsequent work

A closed diagnostic/development checkpoint is not confirmation, a production policy or general agent competence. Unknown outcomes remain unknown. Frozen dependency-bearing originals remain in place; the root-report archive is the only compacted current-tree payload. Local packets share the SSD and do not protect against disk loss.

## Reopening

Preserve this manifest, original revision and packet. A separately authorized continuation must identify a new linked run/protocol and reason for reopening; never overwrite these results or infer an execution grant from restoration.
