# Case 0009 Stage B: capture and blind-packet boundary

Stage A was committed separately at
`eb4060ff8ffd1ff0bf18e11c47d162a6c02bd0f2` (`Add identifier-aware sparse retrieval
experiment`) **before** execution. The source snapshot remains
`d71d741f3a91bf4c4a2b40619d1b8042853f6881`; newly added experiment and status
files are outside that frozen frame. No frozen Stage A artifact was edited.

Both arms executed once across ten identical lanes (full task plus nine caller
obligation queries). Complete positive universes are in `results.json.gz`;
the start marker, costs and result bytes are sealed by `stage_b_integrity.json`.
The deterministic rankings SHA-256 is
`94fe9266ef0ef85d2a60956a34c0bf31e3b74e9c768f2f127930e4adcb700837`.
Verification checks identities, hashes, ordering and field-score decomposition
without another treatment execution.

| Instrumented cost | Arm A | Arm B |
|---|---:|---:|
| Content index build seconds | 1.579 | 3.388 |
| Median query seconds | 0.0264 | 0.0214 |
| Index plus ten queries seconds | 1.921 | 3.635 |
| Content vocabulary | 10,054 | 10,338 |
| Content postings | 86,320 | 97,054 |
| Serialized native index bytes | 22,291,111 | 4,244,482 |
| Traced peak bytes | 259,903,337 | 19,333,169 |

Exact observations are in `costs.json`. This is one instrumented execution, not
a latency benchmark. Serialization and allocation peaks include different
provenance representations and projection; native Arm A retains richer span
objects. Their footprint difference is not evidence that added terms reduce
memory. Filename indexes are rebuilt per query in both arms. No RSS is measured.

## Blind packet and next stage

[Independent packet instructions](adjudication/README.md) accompany a neutral
task manifest and all 531 resource contents, giving 4,779 obligation/resource
cells. The builder reads Stage A only, never results or costs. Whitelist/leakage,
full-frame coverage, identity and digest checks pass. Mechanical fixture tests
also prohibit result/cost reads during packet construction. Ordinary source
text is retained; no arm membership, rank, score, term or analyzer metadata is
exported. No blind judgments or effectiveness join have occurred.

**Effectiveness is UNKNOWN.** No usefulness, recall, completion, burden reduction,
gain/loss or promotion conclusion is available. Independent Stage C must freeze
identity-qualified gold from `adjudication/` alone before a later treatment/gold
join. Do not give the adjudicator this file, parent implementation, protocol,
results, costs or earlier case outcome records.

Canonical production retrieval is unchanged. R1 remains experimental and has
not earned production adoption. **R2 true BM25F / field-aware sparse retrieval
proceeds regardless of whether R1 improves, ties or worsens canonical BM25.**
Localization's post-R1/R2 semantic-resolution resumption boundary is unchanged.
