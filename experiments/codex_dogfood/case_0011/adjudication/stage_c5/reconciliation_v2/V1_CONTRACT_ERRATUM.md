# C.5 reconciliation v1 status and erratum

Status: **EXPERIMENTAL_CONTRACT_DEFECT / NO DECISIONS**.

The sterile reviewer reported that the required complete reconciliation output
could not be supported by the bounded disagreement packet. The repository-side
regression confirms 576 possible need-to-unit pairs, but only 50 distinct pairs
have explicit labels in PAIR_LABEL, DIRECT_RATIONALE and unit-status rationales.
The remaining 526 labels were omitted because v1 projected disagreements and
selected rationale evidence, without supplying a complete inherited baseline.
No absent-pair default was declared. A complete mapping would therefore require
unrestricted fresh adjudication or an invented default; neither is authorized.

V1 packet integrity passed. V1 remained treatment-blind. Reconciliation stopped
before any semantic decisions. No v1 proposition was adjudicated and no v1
reconciliation output exists. This is an experimental contract defect, not a
semantic C.5 result. The failure and zero-decision outcome are the sterile
reviewer's report supplied for this correction; the 50/526 accounting and packet
integrity are independently reproduced by this checkpoint's regression test.

The v1 output contract incorrectly required a full mapping without supplying the
inherited mapping baseline. The committed five-file INSTRUCTIONS.md describes
bounded dispute resolution and does not itself explicitly enumerate a 576-row
output table; it also lacks an executable output schema that would prevent that
incompatible full-output requirement. This erratum records the reported effective
contract defect without rewriting the committed instructions or attributing text
to them that they do not contain.

**V1 must not be used for reconciliation.** Its committed packet, instructions,
validation and publication remain unchanged historical artifacts. Primary C.5
and independent C.5-R remain immutable. V2 corrects output scope without changing
any semantic disagreement proposition, frozen semantic frame or neutral position
ordering. Use only the versioned v2 packet for the next sterile session.
