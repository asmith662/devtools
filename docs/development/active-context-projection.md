# Budget-aware active Context projection

Implementation increment 1, authorized 2026-10-28. Starting main:
`c4ce821e24ca20cb7d2dd9ff97b13ff1581f6a95`.

## Ownership decision before production changes

The existing `RepositoryCodingHost` owns retained native messages and assembles
`ModelRequest`; the coding process already calls its `prepare` seam before any
provider entry. Context Planning owns exact source representation, snapshot
correspondence, UTF-8 bounds and materialization. `Prompt` owns complete native
correlation. These owners suffice: no new Context representation, history store,
executor, coding loop, token counter or provider dependency is warranted.

A coding-specific projection helper under `devtools.agents.coding` will select
complete native exchanges and return an immutable decision account. It will reuse
`SourceRangeDisclosureOption` and `materialize_source_range` to represent smaller
truthful source disclosures. The neutral host will retain original messages and
Tool materializations separately from its last successfully assembled active
request. Edit admission will use current exact disclosures actually present in
that request when the optional policy is enabled.

Explicit host configuration will select a soft byte trigger, a lower target and
metadata-only operation names eligible for omission. This is presentation policy,
not a dispatcher or authorization grant. All instructions, unknown operations,
unacknowledged effects, latest check feedback and newest native exchange remain
protected. Metadata and redundant/stale source exchanges are cheaper removal
candidates than distinct current source; age only breaks ties within a category.
If the hard ceiling still cannot be met, older unprotected source may be omitted
and the newest exact read may be presented as a smaller, explicitly qualified
Context range. An opaque readiness callback conservatively protects all current
source support rather than guessing which obligation is mandatory.

Complete-request accounting includes settings and Tool schemas. Byte capacity is
not provider token measurement. Projection is effect-free and constructed before
committing active availability; failure leaves retained facts and prior active
state intact and refuses model entry. Source scope/currentness, edit authorization,
fixed checks and SourceCustody remain independent.

Qwen retains its legacy task-specific envelope projection, budgets, source/readiness
semantics and wire formats. Its complete-exchange boundary mechanics can reuse the
shared helper; it must not stack the neutral host policy on its different adapter.
Existing Qwen operational/readiness tests will protect compatibility. The neutral
host is the actual opt-in operational consumer, exercised independently of Qwen.

This records the pre-edit ownership decision. The implementation below realizes the
[research direction](../research/agent-context-compaction.md), not a universal
summary API or revision of ADR-0001/0004/0005. Delivery evidence and observed
limitations are qualified below; final validation is recorded separately.

## Implemented activation and accounting

`devtools.agents.coding.projection` implements `ProjectionPolicy`,
`ProjectionOutcome`, `ProjectionCapacityError` and the effect-free
`project_request` operation. These are coding-input decisions, not another
Context value, generic policy framework or Agent result hierarchy.

Pass `projection=ProjectionPolicy(trigger_bytes, target_bytes,
metadata_operations=frozenset({...}))` when constructing `RepositoryCodingHost`.
Both watermarks must be positive integers, target must not exceed trigger, and
trigger must not exceed `CodingObjective.prompt_bytes`. For the frozen 32,768-byte
case, the deterministic test chooses 28,672/24,576; these are test policy inputs,
not new universal defaults or a changed worker limit. Omission names must be
host-classified metadata-only operations. They do not make an operation available
or authorize its execution. The default `projection=None` preserves legacy
request construction and capacity refusal.

`build_request(messages)` assembles the complete ModelRequest before accounting.
Hosts adding native operations override this pure assembly seam so every schema
and setting counts. Appending schemas after `prepare` would evade that accounting
and is not the supported extension. `request_bytes` retains the established
`json.dumps(asdict(request), ensure_ascii=False).encode()` representation; it is
neither a tokenizer nor an estimate of provider HTTP bytes. Provider capacity and
output reservation remain separately owned.

## Retained facts and active availability

The host retains original `messages`, `responses`, successful prepared `requests`,
actual `source_results`, check results and effect acknowledgments. Original native
feedback is never replaced by its active projection. These are available
in-memory facts under existing capture boundaries, not a durable restart log.
`projection_outcomes` retains successful and insufficient decisions;
`projection_error` retains an original projection failure/cancellation. The coding
process preserves its existing terminal error and candidate/custody semantics.

`native_exchange_ranges` validates the existing typed Prompt and locates complete
assistant-call/result blocks. Selection never drops a member of a batch, changes
a call ID, invents feedback or invokes a Tool. Repeated native IDs are refused.
User/system instructions and ordinary assistant text remain protected. The newest
exchange, latest fixed-check feedback and unclassified operations are protected;
an unacknowledged effect refuses continuation outright. An opaque readiness
callback conservatively protects all current source support rather than guessing
which witness a mandatory obligation needs.

Under soft pressure, duplicate current source ranges, stale source and explicitly
classified inventory/search metadata are eligible before distinct current source.
Ordering within a tier is deterministic. Distinct current source is removed only
under hard pressure, and retained above the lower target when the complete request
already fits. The lower watermark is therefore a useful target, not permission to
erase important Context. Unknown/effectful history may eventually make a safe fit
impossible; this increment has no semantic summary to replace it.

Source-message bindings use existing `SourceRangeDisclosureOption` objects.
Context materialization authenticates repository/snapshot/resource identity and
exact presented text, version and span. Only selected current disclosures become
`active_disclosures`. Removed or stale options cannot authorize an edit. Admission
still checks permitted paths, current bytes, exact anchors, limits and host policy.
After an edit, old active availability is cleared; current after-images in fixed
check feedback acquire active status only in a successfully prepared next Prompt.
Snapshot checks are not an atomic filesystem snapshot or a concurrent-writer lock.

## Disclosure affordability and failure

If complete exchanges cannot make the request fit, an unprotected plain source
result can be presented as a smaller truthful prefix using existing
`materialize_source_range` UTF-8 bounds. The active Tool message retains its call
ID and explicitly records `partial`, the actual span, original message SHA256,
acquired span and acquired partial status. The original materialization and
feedback remain unchanged: a completed read is not relabeled as failed. Compound
check feedback and protected source are not shortened. Empty source does not
become fabricated content. No summary supplies source text.

This happens at host request assembly before provider entry, after the actual
bounded Tool result has been captured. It avoids a costly model-facing disclosure,
not the original read or capture cost. The next explicit authorized read can
reacquire omitted source through existing Tools; projection itself never replays
an operation. A retained prefix permits only anchors inside that prefix.

Outcomes report original/result bytes, trigger, target/hard limits, selected
message indices, omitted block ranges/reasons, shortened messages, active sources
and invalidated source identities. `target_reached` distinguishes useful headroom
from a merely usable hard-limit fit. If the protected minimum cannot fit,
`ProjectionCapacityError` exposes an `insufficient` outcome before model entry.
Unexpected failures and cancellation retain their original identity. No partially
constructed projection is installed; previous active state and historical facts
remain intact, and the normal coding process stops rather than using stale state
to continue after a failed preparation.

## Compatibility and deterministic evidence

The neutral host is the real opt-in consumer. A guarded independent application
uses the shared coding process, actual source Tools, file effects, fixed checks,
failed-check repair, candidate archival and known-source restoration with
projection enabled. Its guards reject application/experiment imports and reads.
Unknown usage remains unknown; omission does not repeat effects.

Qwen retains its existing `select_messages` policy and envelope representation.
Its complete native exchange boundary now delegates to the shared validator; a
controlled boundary fault proves actual delegation without fallback. Existing
native/prepared, obligation/readiness, source admission, repair, terminal, CLI and
closeout regressions remain authoritative. No task/hash/journal, source/edit limit,
ModelInteraction observer, Runtime, Checkout or publication contract changes.

The read-only Case 0003 regression reconstructs the original base-host request at
36,640 bytes and produces **24,070 bytes** under the unchanged 32,768 ceiling.
It omits the listing exchange (3,821 bytes) and two-search exchange (8,749 bytes).
The objective and all three exact source exchanges remain; no source is shortened
or invalidated. In original character-span notation, source ranges remain
`[1,6754)`, `[10250,11200)` and `[1,8193)`. The two repository ranges are disjoint.
Tests separately account for all six experimental Tool schemas, which the
original base-host guard had not yet assembled: **37,468 to 24,898 bytes**. That
result fits the hard ceiling but intentionally misses the 24,576 target by
322 bytes rather than discarding distinct current source. Source currentness
here means the original frozen snapshot, not today's modified checkout.

This is an effect-free reconstruction, not a sixth provider request, a rescue of
the original attempt or evidence of improved model effectiveness. Original case
bytes and outcomes stay unchanged. Separate host tests prove omitted-source edit
refusal, retained-source admission, explicit reacquisition, partial presentation,
mandatory support, failure/cancellation, repeated projection and accurate sizes.

## Subsequent increments, not implemented here

Increment 2 is optional structured model-assisted compaction: separately budgeted
provider-independent summary requests, exact constraints/obligations, progress,
decisions, failed hypotheses and next actions; provenance, validation, recent
exact history and deterministic fallback. Model choice, privacy, failure and
budget contracts need their own authorized implementation.

Increment 3 evaluates adaptive tier selection, thresholds/watermarks, summary
timing, grounded reacquisition and model/operator requests using separately frozen
deterministic and real continuation assessments. Request fit alone does not prove
coding effectiveness. Neither increment authorizes new providers, durable replay,
an autonomous supervisor, broad A+C or observation Option B.

## Committed-tree validation

Implementation commit `75692067b3c7dc8b21a3be2eb5d794f650b11d87`, tree `6b701a6c4b879f68fe183b6aa090edf9522953fb`, is based on
`c4ce821e24ca20cb7d2dd9ff97b13ff1581f6a95`. The full unchanged protected command was
`uv run python scripts/validate_development.py`, started
`2026-10-28T21:55:26.222414+00:00` and finished `2026-10-28T22:21:15.734704+00:00` in
1549.302 seconds, exit 0. Its result: **3677 passed, 2 skipped in 1547.31s (0:25:47)**.
Configured production line and branch coverage is 100%, with zero missing lines
or branches; no selector, threshold, exclusion or scientific protocol changed.

Baseline characterization passed 263 tests before production edits; its initial
wall timestamp was not captured. The broad focused run passed 1,172 tests;
124 final targeted tests include the last UTF-8 and actual failed-check controls.
The committed full gate includes every final maintained regression. Strict mypy
passes 586 files, supported formatting passes 709, and supported Ruff and layout
pass. Windows Python 3.14.3, pytest 9.1.1, coverage 7.15.4, Ruff 0.16.2 and mypy
2.3.0 were used; this does not certify other runtime/platform environments.

The literal `ruff check .` discovery also scanned immutable scientific builders
and failed on their retained style. It is recorded, not hidden or repaired by
rewriting history. The established `src tests apps scripts` lint scope and
formatter scope excluding retained experiment tests pass. Development fixture,
format/type and diagnostic subset-coverage failures are separately qualified in
the receipt; they were not original product failures or threshold exceptions.

The [machine-readable receipt](../research/code-audit/active-context-projection-20261028.json)
retains changed Git blobs, review depth, complete physical protected inputs,
commands, timings, exact size/source selections, outcomes and limitations.
Historical Qwen assurance and the research evidence JSON receive separate
changed-version overlays; original fields and prior credit remain unchanged.
All three cases, thirteen forensic files, 903 RI rows and historical references
remain intact; 188 historical RI-version obligations and broader B-0002/B-0035/
B-0043 remain open. Two preexisting B-0002 links to removed root scratch reports
remain qualified; no new broken local links were introduced.
