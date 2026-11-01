# Aggregate source-read admission

`RepositoryCodingHost` now checks source acquisition against the complete next
serialized `ModelRequest`, before entering the source Tool. This corrects the
capacity obstruction observed in the [first authorized B-0049 episode](../research/live-native-maintenance-task.md).
That episode and its consumed WorkCycle slot remain unchanged. This delivery
uses neutral deterministic responses; no live model, service mutation or RI
implementation repair is part of it.

## Owner and accounting

The host already owns request construction, retained messages, active Context,
source/edit witnesses, Tool correlation and coding budgets. Its admission uses
the actual `build_request` seam and `projection.request_bytes`: messages,
reasoning retained by the configured profile, complete inventory, Tool definitions,
settings, native call arguments/IDs, nested JSON escaping and all pending replies
are charged. Source UTF-8 length alone is insufficient.

For a read/check batch, existing effect-free native argument materialization and
Context `SourceRangeDisclosureOption` produce the expected feedback. If the full
batch cannot fit, all its source disclosures are refused before entry. This
avoids spending unrelated read effects and most remaining space before rejecting
the largest request. Fixed checks keep their existing separately authorized
behavior; their bounded boolean result is reserved, not invented as an outcome.
Malformed pure arguments retain their established per-call failure boundary.
Authorization, operational, currentness and post-entry failures are not caught as
capacity refusals.

Each individual source admission also reserves every remaining reply. Pending
reads reserve compact correlated refusal feedback; they are independently
admitted only if their exact payload fits. Pending fixed checks reserve the
longer boolean result. Optional navigation retains its existing execution policy;
an earlier source read reserves its declared metadata envelope with conservative
JSON escaping overhead. These reservations are hypothetical accounting inputs,
never synthetic Tool results sent to the model. A conservative reservation can
require separating operations into different responses.

No additional planner, ToolRunner, loop, model registry, state store or lock was
introduced. `coding.protocol` owns the bounded feedback representation. Existing
SourceScope, scoped source Tool validation, ToolRunner and Context range
materialization still authenticate and execute the actual read. Scope/currentness
is checked again after host consent and immediately before Tool execution.

## Feedback and recovery

A known capacity refusal has `error: SOURCE_CONTEXT_CAPACITY`,
`source_disclosure_entered: false` and `tool_operation_entered: false`. It is a
Tool reply under the exact original native call ID. The call arguments and
complete inventory already identify the resource; repeating their full metadata
in every refusal would itself consume recovery space. The bounded explanation
asks for fewer reads or a smaller explicit `end`.

The existing `read_source` contract uses half-open decoded Unicode character
offsets. For example, `{ "path": "tests/example.py", "start": 1200, "end": 1328 }`
asks for that exact range. Offsets are neither UTF-8 bytes nor physical line
numbers. Omitted `end` uses the existing per-read byte-bounded prefix, not the
remaining complete-request allowance. The returned span, continuation offset,
remaining range and partial flag describe actual disclosed text. UTF-8 characters
are never split; CRLF characters remain exact. No new line-coordinate API or
semantic summary was needed.

Known invalid ranges are also refused before disclosure execution, retaining
their existing bounds and source identities. Refusals consume the ordinary finite
action/model budgets. Repeated unavailable reads do not execute the source Tool
or accumulate source witnesses. The worker must select a feasible new request;
the host does not retry it automatically. If even the correlated refusal cannot
fit mandatory Context, the episode stops with an explicit capacity failure at
acquisition, and no source entry is claimed.

The exact expected payload is checked against the completed Tool result. A
different returned payload is retained as completed but undisclosed, without an
edit witness; it is not described as an effect-free refusal. Exceptions after
entry retain their original unknown-effect semantics, with no fabricated reply
or automatic replay. A known result and an unresolved acknowledgment are distinct.

## History, projection and authority

Complete host messages and materialized results remain retained. Refused reads
add neither source disclosures nor source-to-edit evidence. Existing exact
anchor, current snapshot, information-readiness and custody requirements are
unchanged. Metadata, refusals and summaries do not prove source possession.

Admission previews the existing pure projection only when the host explicitly
configured it. It uses the same protected check/readiness/compaction constraints,
does not invoke an auxiliary model, and does not install active Context. Actual
preparation still owns active source selection and its witnesses. Explicitly
authorized projection can keep its established partial-source presentation with
exact spans and omission provenance; complete acquisition history is not the
same thing as active source evidence. No new lossy default is activated.

Native WorkCycle previously supplied no projection policy, and still does not.
Enabling optional projection alone would not permit dropping its required current
whole-owner information witness. This correction makes its current hard profile
recoverable through refusal and narrower source selection, without changing the
meaning of that requirement.

Native execution now archives final Tool feedback through its existing bounded
Capture/writer, including feedback that no subsequent model request consumed.
Existing request/response observations, source facts, check results and custody
remain separate. Capture exhaustion remains a blocking evidence failure, never
publication authority or permission to replay. Original native and legacy Qwen
records are not rewritten or reinterpreted.

## Bytes and tokens

The 32,768-byte native ceiling is an independent host/profile resource contract,
enforced by the native packet ceiling and `CodingObjective.prompt_bytes`. General
coding hosts choose their own byte budgets. It predates this local llama.cpp
qualification; source/resulting-file byte limits are also separate contracts.
The retained code does not establish a token-to-byte derivation or demonstrate
that 32 KiB is optimal. Its suitability merits later profile review.

The provider's 32,768-token context and per-call output-token reservation are
different measurements. Both actual B-0049 requests passed provider token-fit
qualification. Only serialized-byte overflow was observed before request three.
No token overflow is inferred, no byte/token conversion is invented, and neither
limit is increased here. Any later token-aware/provider-specific policy needs
its own explicit decision and qualification.

## Verification and limits

The maintained B-0049 fixture freezes four individual authenticated input files
(51,544 UTF-8 bytes), the actual native calls, settings and two observed request
sizes. A deterministic host reconstructs the unaffordable full third request,
refuses the batch with exact per-call correlation, prepares a fitting next
request, and accepts a separately selected smaller range. It does not enter the
original WorkCycle slot or implement the unresolved RI correction.

Tiny authored repositories separately exercise a real edit, failed managed check,
selected repair and passing check; feasible batches; pending checks; complete
Tool/schema overhead; exact capacity boundaries; non-ASCII/CRLF; protected check
feedback; stale inputs; repeated attempts; no-witness refusals; completed changed
payloads; and unknown post-entry failures. Existing projection/compaction and
native review/integration consumers remain in the validation scope. These tests
establish framework mechanics, not Qwen engineering competence.

Hard mandatory input, protected check feedback, arbitrary oversized model output
or genuinely insufficient space can still stop an episode. Admission promises
bounded truthful handling, not that every future model response or source request
will fit. Publication retains the configured protected 100% production line and
branch-coverage gate.

Before another live trial, obtain a genuinely reviewed and published new linked
task with an unused native slot, freeze current source/check/model/profile inputs
and finite budgets, then obtain fresh exact default-No coding authorization and
dispatch consent. An eligible successful candidate separately requires a fresh
independent reviewer session and review-only authorization. The old B-0049 grant
and dispatch cannot be reused. No new canonical task identity or live authority
is created by this framework increment.
