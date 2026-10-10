# Case 0012 Stage B execution recovery contract

This supplement corrects execution/capture durability only. The scientific Stage A
at `4ff6d3950e6c0be834f136a649c1a127f91fdba3` remains authoritative and byte-identical.
It supersedes an interpretation of globally exactly-once calls across all history.
**Each explicitly authorized execution attempt may invoke each frozen operation at
most once.** Historical counts remain separate from per-attempt counts.

## Immutable failed attempt

`case-0012-stage-b-1` is permanently ABORTED_CAPTURE_INFRASTRUCTURE_FAILURE,
NOT_EVALUABLE and AUDIT_ONLY. Its four durable lexical returns and index are
retained, together with original source and failure bytes and original inventory.
The successful materialization return was lost at mutable checkpoint replacement.
No missing result may be inferred, reconstructed, resumed or re-executed under
attempt 1. No exact routes, grounding, presentations, arms or Stage C ran.

Attempt-1 outputs MUST NOT be spliced into the official result, receive gold labels
or contribute to effectiveness. They MAY be used only for serialization tests and
deterministic consistency comparison against an independent attempt.

## Explicit fresh authorization

The maintainer authorized `case-0012-stage-b-2` in the recovery task. It starts from
operation zero, with a fresh index, global safety lane, nine obligation queries,
both arms' admitted routes/native grounding, presentations and all three arms.
It is permitted because the failure concerns capture infrastructure for pure
read-only deterministic operations, not treatment science. All source checkpoint,
repository/snapshot/corpus/frame, semantic treatment, queries, analysis, BM25,
routes, associations, exact/presentation semantics, decision thresholds and blind
gold protocol remain unchanged. No partial result is used to tune those values.
The recovery infrastructure and failed audit must be committed and pushed first.

## Durability boundary

`execution.claim` and `execution_started.json` use exclusive creation. Before each
operation, an exclusively created `operations/NNNNNN.entered.json` binds identity,
sequence, exact input/digest, invocation count one, runtime identity, frame and
prior chain. Immediately after return, a NEW exclusive `NNNNNN.returned.json`
retains canonical complete native value, trusted native serialization segment,
physical/canonical digests, runtime and entered-record binding. Complete write,
flush, fsync and close precede the next native operation. A partial immutable file
blocks recovery; no native operation is retried. Parent-directory crash durability
remains subject to OS/filesystem behavior, as with the native filesystem writer.

The canonical native graph describes every field/container order/type/alias.
It avoids exponential repetition of index graphs. A single incremental pickle
memo preserves original Python types and reference identities across immutable
returned segments. This is a trusted repository-owned capture codec, never a
blind-packet input. Native domain objects and behavior projections are unchanged.
Event order and digest chains preserve nested native grounding/composite calls.

`raw_checkpoint.json` is derived metadata only. It is reconstructable exclusively
from immutable context and journal records. Replacement failure after a durable
return writes an exclusive summary-failure diagnostic and does not rerun the
native operation. Loaded journals allow finalization only, never new calls.
Readers close files immediately and never hold a summary handle across publication.
The focused Windows test denies delete sharing on the summary, observes replacement
failure, recovers the immutable native value, closes the handle, and reconstructs
the summary without invoking the native operation again. No sleep/retry loop.

## Previously exposed partial mechanics

PREVIOUSLY_EXPOSED_PARTIAL_MECHANICS:

| Operation | Positive rows | Seconds |
| --- | ---: | ---: |
| global | 529 | 0.026131900 |
| source | 355 | 0.008188400 |
| choices | 364 | 0.008447900 |
| integrity | 321 | 0.007886500 |
| index build | unavailable | 0.459217800 |

These were seen before recovery design. They must not influence query, route,
scoring, association, threshold, interpretation or treatment design. The new
capture layer addresses persistence durability solely. They are neither gold nor
effectiveness evidence; timing differences between attempts are descriptive only.

## Publication gates

Attempt 2 alone supplies the official native result. Compare all deterministic
content of the four overlapping retained queries, excluding time. Any discrepancy
blocks authoritative publication. Validate corrected frozen B/C behavioral
projections while preserving distinct complete task-extraction provenance.
Require full fallback/native rank/score/contribution and global safety preservation.
Only then publish Stage B and prepare a blind packet. Stage C remains unperformed,
gold absent, effectiveness unknown and final U2 outcome unselected. U3 future,
R1.7 retained, true R2 BM25F mandatory, downstream Localization preserved.
