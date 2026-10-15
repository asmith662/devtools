# Bounded blind-gold C-v2

[METHOD.md](METHOD.md) describes the current A1/A2/global procedure and its
limitations. `execution`, `fresh` and `lifecycle` wire those mechanics into the
existing deterministic controller. `prospective` builds and exactly replays a
separate Stage A and unapproved plan. Approval and execution remain separate.

The cohort remains 0022/0023/0024. A1 partitions retain the engineering digests
and require 3/3/2 calls. Dynamic A2 permits at most 24 calls per case, with
whole-partition rejection before entry. Consolidation adds at most one call per
case. With adopted B22/B23 and fresh B24 the maximum is 84 fresh invocations:
83 Astra/High and one Sol/High.

Current all-positive global maxima are 678468 / 584114 / 406140 characters
(64.7038% / 55.7055% / 38.7325% of the observed transport ceiling). Worst-case
Unicode bytes exceed the certified allowance; actual dynamic inputs must pass
both 700000 characters and 700000 bytes before entry. A2 output is at most
61326 bytes; global maxima are 55922 / 55090 / 53522 bytes. The separate output
receipt attains 63357 bytes. These are workload claims, not runtime maxima.

The following notes preserve earlier candidate-02/03 design and sizing history.
They are superseded by the current method and execution bindings.

## Historical candidate-02/03 notes

The current [A1/A2 method candidate](METHOD.md) supersedes the combined Pass-A
description below. This retained description records candidate-02/03 history;
it does not describe the current state-only A1 contract or freeze science.

This package does not yet implement or authorize the C2 scientific workflow.
There is no new frozen Stage A, replacement plan, approval or semantic result.
The old run and its six journals remain unchanged. No model is invoked by these
mechanics or their tests.

## Representation and exact evidence

`archive.assemble` consumes host-authenticated synthetic or future Pass-A response
values and the complete authorized parent packet. It requires one cell for every
source/obligation pair, rejecting duplicates, foreign cells and missing coverage.
States remain USEFUL / NO_USEFUL / UNCERTAIN. Incomplete representation fails;
it is never a negative judgment. Summary/uncertainty bounds are 512/256 Unicode
characters; there are at most four locators and 4,096 aggregate exact quote
characters per cell. Exact overlapping-occurrence resolution uses the existing
host locator implementation, without trimming, normalization, repair or guessing.

Canonical address order and obligation ID determine cell IDs. Evidence IDs are
packet-local deterministic slots within those cells, not globally reusable IDs:
the archive packet digest, coverage root and exact archive digest bind their
meaning. The archive contains original canonical identities/spans/quotes and
invocation/response/runtime provenance. Invocation validity and frozen batch
membership remain caller-owned and are not established by this projection.
`reattach` rejects foreign evidence and cross-cell references. Full unit/witness
assembly is still unimplemented.

`disclosure.render` receives only the blind task/obligations, coverage root/count,
and bounded cards. It does not receive raw resources or the exact quote archive.
Task and obligation context use compact JSON once; card metadata uses fixed
column order. Summaries and uncertainty notes are literal Unicode strings prefixed
by their exact decimal code-point length and a colon. A reader consumes exactly
that many code points. Embedded delimiters, controls, CRLF and supplementary
characters require no escaping. Strict UTF-8 rejects unpaired surrogates.
`decode` must reproduce the original disclosure bytes exactly. No content is
removed to meet a bound.

The old ASCII JSON sizing fixture remains a regression. With actual frozen task
and obligation context and every permitted free-text card field at maximum,
the new candidate renderer gives:

| Case | Cells | Unicode characters | Maximum UTF-8 bytes | Transport percentage |
| --- | ---: | ---: | ---: | ---: |
| 0022 | 744 | 669,423 | 2,383,599 | 63.8412% |
| 0023 | 640 | 576,317 | 2,050,877 | 54.9619% |
| 0024 | 444 | 400,695 | 1,423,671 | 38.2133% |

Counts include this candidate's instruction/context envelope. They do not claim
an integrated production invocation, model token estimate or hidden system-prefix
measurement. All cards, including uncertainty, are present; no sparse-usefulness
assumption is used. This renderer is not wired to the existing semantic transport.
Transport argv, stdin delivery, final-message extraction and sandbox are unchanged.

## Workload readiness, not maximum discovery

Character fit is independent of context/output readiness. Codex 0.162.1 cached and
bundled catalogs report context_window=272000, max_context_window=872000 and
effective_context_window_percent=95. These are reported runtime metadata, not
proof that the maximum is active. Neither catalog provides an active output-token
cap or reasoning reservation. The locally generated experimental app-server
protocol exposes context/usage observations, but no output-token reservation.
The official configuration reference does not establish one either.

The separate Astra API output limit is not substituted for the Codex profile.
No authenticated exact-model tokenizer or response-token upper-bound estimator
has been established. Unicode character fit therefore does not prove context fit.
The amended policy does not require absolute maximum output discovery. The
method owns a 65,536-byte canonical semantic response envelope; the constructive
schema proof includes JSON control escaping and the host's aggregate quote
assertion. Output-aware packing admits one resource/two obligations per Pass-A
batch. Pass B permits eight units, eight alternatives per unit and four
conjunctive references per alternative, with explicit finite text bounds.
Insufficient representation must report incomplete and fail closed.

A compatible engineering CapacityReceipt must establish the exact Astra/High
profile's finite workload lower bound before prospective science. The candidate
input allowance is 700,000 Unicode characters AND 700,000 UTF-8 bytes. The Unicode
worst-case byte counts above exceed that allowance; actual dynamically rendered
inputs must pass both checks before semantic ENTERED. Nothing is truncated or
repacked to force fit. Unknown exact token/output maxima remain unknown and are
not replaced with API model-card limits. See the
[capacity contract](../../orchestration/engineering/host_disclosure/CAPACITY.md).

Until successful workload certification and integration, no batch partition, branch
adoption seal, superseding Stage A or prospective plan is published. The intended
procedure remains raw-resource Pass A → exact host archive → card-only Pass B →
host exact reattachment. It is an amended measurement procedure, not equivalent
to the former one-shot primary. Pass A remains a selection bottleneck, uncertainty
must survive, and no scientific retry is introduced.
