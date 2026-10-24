# Long engineering continuation 09

The existing coding loop now performs exact tokenizer-guided projection before
capacity refusal. It reuses native Prompt messages, Context observations, flat
observed edits, Checkout and WorkCycle; no new executor or Memory store exists.
Historical Engineering 08 outcomes remain unchanged. Binary's previously
published implementation was not rerun or counted again.

## Archived capacity diagnosis

Every archived Engineering 08 request was measured with the installed llama.cpp
template/tokenizer, including the two undispatched pending requests. The table
shows ordered tokenizer-ablation marginals; order matters, so these are not
independent calibrated costs. Residual Tool results include useful information
as well as redundant metadata and must not all be labeled waste.

| Pending request component | Source-search | Binary I/O |
|---|---:|---:|
| Task/objective | 689 | 739 |
| Exact source text | 9,204 | 10,806 |
| Refusal/validation | 555 | 1,100 |
| Residual Tool envelopes/results | 8,889 | 11,865 |
| Assistant Tool arguments | 1,214 | 1,826 |
| Assistant text | 244 | 117 |
| Tool definitions | 1,366 | 1,407 |
| Native scaffolding | 506 | 729 |
| **Total** | **22,667** | **28,589** |

| Projection | Source-search input | Binary input |
|---|---:|---:|
| Original | 22,667 | 28,589 |
| Metadata compaction; all source text retained | 19,928 | 24,716 |
| Explicit older read-only reacquisition; editable source retained | 19,928 | 22,168 |

Binary can retain all source with 6,004 safe output tokens. The full 8,192 output
plus 2,048 safety allowance requires input at most 22,528: the 22,168 projection
meets it while retaining all five editable observations R1â€“R5 and the refusal.
Four older read-only excerpts are explicitly marked for reacquisition: text
codec, BinaryFile model, generic reader and the first JSON codec range. Their
paths, versions, spans and original-message provenance remain available; source
is not replaced with an invented summary. This replay proves request fit, not
autonomous repair or correctness of either original proposal. Source-search's
wrong observation references and undefined helper remain separate code defects.

The original binary pending turn was its last permitted model call. Under that
unchanged budget, the final safety guard retains **all** source and admits a
6,004-token output alternative after metadata compaction. The 22,168/full-8K
representation is usable only when future model calls and read actions permit
reacquisition. It does not silently extend the historical task or prove that
missing dependency text is unnecessary. All five editable sources remain exact
in either representation.

Replacing the historical flat Tool description with the actual maintained
sixteen-component description adds 35 tokens: all-source input is 24,751
(5,969 safe output), or 22,203 with the four explicitly reacquirable excerpts
omitted (8,192 output still fits). Both genuine run freezes were checked against
their actual request Tool schema. These are tokenizer/capacity observations,
never authority to redispatch the already completed binary task.

Repeated repository/snapshot/revision envelopes and identical refusal bodies
refer to their original Tool call IDs. Native assistant/call/result groups stay
correlated. Latest feedback, objectives and current editable source are retained;
stale source is explicitly removed. Exact capacity measurements precede dispatch.
New raw archival uses the existing Prompt contract, before projection, so Tool
content digests can be audited directly. No historical archive is backfilled.

## Real engineering task and evaluator correction

The fresh roadmap obligation was hard-bounded filesystem consumption under file
growth, with complete short reads and existing codec/error behavior preserved.
The task initially named no implementation file and disclosed no full source.
Nineteen read resources included plausible filesystem/codec/model/paths/test
alternatives. Historical task objectives, source paths and oracle identities
were audited; the prior disappearance case shares the owner but a different
defect and an invalid oracle. It is not the consumption-bound task.

The original freeze allowed one run, 24 requests, 1,800 worker seconds, 8,192
output tokens/request, 32 investigation/check actions and three proposals.
After an evaluator defect, a separately committed amendment allocated only the
unused twelve calls/1,394 seconds to a corrected development continuation.
Neither the original frozen oracle nor its receipt was changed.

The original oracle incorrectly used TextFile's `byte_size` on BinaryFile,
whose public property is `size_bytes`. Baseline failure alone had failed to
qualify later oracle branches. The invalid diagnostic reached Qwen and prompted
two refused attempts to add an out-of-scope compatibility alias. Its first
candidate independently also fails short-read preservation under the corrected
oracle; it must not be credited as an otherwise accepted implementation.

The correction changes only that oracle attribute. It separately records public
API/fixture qualification and clarifies the prospective exclusion of two old
implementation-specific `Path.read_bytes` mocks. No solution is provided. The
corrected continuation is **not fresh confirmation**, and no prospective
fresh-task acceptance rate or causal before/after improvement is claimed.

| Run | Outcome | Requests | Input/output tokens | Worker seconds |
|---|---|---:|---:|---:|
| Original | PROPOSAL_ADMISSION_FAILED; evaluator-invalid | 12 | 188,673 / 6,507 | 405.61 |
| Corrected development continuation | ACCEPTED | 6 | 50,969 / 2,080 | 129.91 |

The original actually continued beyond the former ten-request ceiling:
request 11 received refusal feedback at 21,740 measured input tokens after
compaction; request 12 compacted 26,952 to 24,492. This validates operational
continuation without validating the erroneous behavioral diagnostic.

The corrected run investigated actual related source, submitted three coordinated
edits, passed all eleven independent behavioral cases and eighteen existing
tests, then repaired a genuine Ruff TC003 failure with two import edits. Final
behavior, Ruff, formatting and strict typing passed. Behavioral repair remains
unproven. Source was restored after both local evaluations. The same 32K IQ4_XS,
q4_0 K/V, thinking-off serving profile remained in use; no paid comparison ran.

## Maintained publication and remaining verification

Exact Qwen source `9ce530e6f0d1f42792a18b779168cbf47f7360ad1fe221e146e3410909465102`
was reviewed and feature-published by WorkCycle closeout in
`61637ff8d359742ad7028b02cd6ca40aa749cd04`, with independently authored permanent
tests. Stream consumption, short reads, zero/unlimited limits and permission
cleanup are covered. Four implementation-specific permission/growth mocks were
migrated to stream-opening mocks without removing their original assertions.

The first protected run exposed two of those dependent mocks: 2,179 passed,
two failed, two skipped, with 100% production coverage. After their correction,
2,181 passed, two skipped, 100% coverage. The original failed validation remains
archived. An earlier oversized pytest parameter ID was independently corrected;
no Qwen implementation bytes changed during closeout.

The older accepted candidates completed separate serial closeouts with their
original Qwen bytes and newly independent permanent regressions:

| Candidate | Feature commit | Protected gate |
|---|---|---|
| bsd | `86046e5a93c5db94a19ed39c2d5c1eae11aa6069` | 2194 passed, 2 skipped in 527.20s (0:08:47); 100% coverage |
| identity | `da0ac97a23ef1f313101667c69b0ce7430cc08e8` | 2208 passed, 2 skipped in 543.53s (0:09:03); 100% coverage |
| decoded-output | `9b667e597f9da160be8a9e08e1e2d24023d6f102` | 2212 passed, 2 skipped in 533.01s (0:08:53); 100% coverage |

Their immutable result hashes, source hashes, reviews, prior receipt archives and
validation-log identities are recorded in [results.json](results.json). Protected-main promotion
remains separately authorized. No parent backlog obligation is automatically
closed, and the discovery remains pending canonical review.

Capacity refusal remains correct when critical editable source itself cannot
fit, or reacquisition budgets are exhausted. Larger Context is not demonstrated
necessary by the archived pending requests. The next empirical checkpoint is
an independently qualified fresh long multi-module task with genuine behavioral
feedback; this corrected development continuation cannot replace it. Oracle
qualification must cover public API names and positive/negative fixture branches,
not only reproduce baseline failure. General reliability and Codex parity remain
unproven; Qwen remains the primary workstream.

Raw immutable evidence and measurements are under
`.local/qwen-coding-worker/continuation-09/`; original Engineering 08 and all
earlier cohorts remain unchanged. Coordination tokens, dollars and integrated
energy are UNKNOWN. One live GPU sample observed 14,006/16,376 MiB and 79.86 W;
it is not a peak or an energy measurement.
