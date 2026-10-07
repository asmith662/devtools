# Canonical BM25 parameter sensitivity — R1.6

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

Run `python -m experiments.bm25_sensitivity.study verify` for deterministic
selection/surface/report replay. Reconstruct diagnostics via `diagnostics(data)`
and compare stable serialization to the retained capture; the original publish
operations refuse overwrite. Test fixtures exercise native-score parity and
selection/tie/safety/alternative/identity rules. No production default changes.

[Case 0010](../codex_dogfood/case_0010/README.md) tests baseline against the three
unique selected challengers after development freeze. Stage A precedes the
one-time treatment capture. Independent clean Stage C and the
[Stage D join](../codex_dogfood/case_0010/analysis.md) are complete:
**MIXED / NO SAFE REPLACEMENT**. All REQUIRED reach is retained, but all three
challengers fail the frozen 10% meaningful-improvement and per-obligation safety
gates. Production remains (1.2, 0.75, 0.25). R1.6 is DONE; the roadmap now places
U1 manual upstream formulation next, with R1.7 retained and R2 true BM25F still
mandatory. The [variant audit](VARIANTS.md) explicitly preserves open BM25+/BM25L
questions without requiring an additional pre-BM25F variant experiment.
