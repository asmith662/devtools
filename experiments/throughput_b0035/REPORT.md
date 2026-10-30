# Throughput-B0035-0001

**The decision checkpoint passed. Coding entered, but stopped before any edit
with a Context-capacity failure and a subsequent experiment-recorder failure.**
B-0035 remains open. No model-authored code entered production and no supervisor
patch replaced the worker.

## Frozen authority and source

Starting local/remote main was d7fd131d1f0b56f1e54e3ea7536635f7caa5882e,
with unchanged executable ancestor c2bc06f4f604c6ccb87279f6315bfa87b59ce6fa.
The [protocol](protocol.md), [freeze](decision-freeze.json) and exact runner were
committed at 59959dbe11e932ff1751d0475912a5a95549376f before inference.
The [independent decision approval](decision-review.json) was committed at
92ad84b6639ef5ad2a9e1aaf8e5ce4faf7f28f99 before coding entry.

The prior completed preparation was reused without altering its evidence. All
fourteen scope-file hashes and eleven exact disclosed units remained current;
the working set held 20,457 source bytes. The objective and complete-inventory,
identity/privacy, freshness, nonduplication, metadata-only authority and capacity
requirements were retained. Existing focused/withheld oracle predicates and the
three additional integration predicates were frozen by reference/hash. No new
oracle or reference implementation was introduced. The prior finite preflight
qualifications remain: the additional predicates need an actual candidate to
exercise their positive paths.

Repository.py remained 32,031 bytes and navigation.py 13,044 bytes, with 737 and
19,724 bytes headroom under the unchanged resulting-source bound. These were the
only editable modules. No authority, source/edit limit, provider or sampling
setting expanded. The same authenticated GGUF SHA-256
40fac4050e940397dbf13087afd50f4734a11805bf9d65ef8ddd7483470e6199,
pinned llama.cpp profile/image/template and Qwen3.8-27B configuration were used.
Thinking remained disabled. No service lifecycle operation, download, paid call,
alternate model, auxiliary summary or repeated sampling occurred.

## Actual decision and coding actions

| Phase | Serialized bytes | Input/output tokens | Model seconds | Termination |
| --- | ---: | ---: | ---: | --- |
| Response-only decision | 29,821 | 6,862 / 300 | 25.087121 | normal_stop |
| First coding request | 32,768 | 7,821 / 116 | 17.168326 | tool_call |

Both were complete normalized responses; raw bodies match normalized content and
native calls. Total known usage was 14,683 input and 416 output tokens, with
42.255447 seconds of model wait. Cached/reasoning usage was unavailable, not zero.

The checkpoint ceiling was 768 output tokens and 120 seconds, with a 160-second
watchdog. At observed 22 tokens/second plus a declared 40-second overhead allowance,
estimated time was 74.91 seconds. Coding was frozen at 2,048 output tokens and
180 seconds per call (133.09 seconds by the same estimate), ten requests,
four proposals, two natural repairs/three applications and a 1,140-second process
bound within a 1,200-second watchdog. These estimates supplied operational margin,
not a latency guarantee. Neither actual response was truncated or timed out.

Qwen correctly explained that prepare/build_request do not supply the complete
inventory, that task_entry explicitly marks its candidates incomplete, and that
current scope resources and the host editable subset supply the metadata. It
proposed request-assembly integration and refusal if complete metadata cannot fit.
It recognized currentness and current-snapshot assembly requirements. This was a
plausible direction supported by disclosed source, not a proven design covering
every edge. There was no genuine missing-dependency request and no second checkpoint.

Coding used the existing shared run_coding_agent and RepositoryCodingHost. The
actual decision was handed off as assistant content, with the frozen instruction
to implement using scoped source or grounded native edits. The concrete
[coding entry request](coding-entry-freeze.json) was recorded before custody entry.
Existing projection brought that request to exactly 32,768 bytes; initial source
disclosure is not a guarantee of perpetual complete active witnesses.

The worker then independently selected two native read_source calls:

- repository.py, Unicode range [0,8142), call Cq3d9EzKdv2VhznYbhRzCVgxsiKj9Ezb;
- navigation.py, Unicode range [0,3625), call ZBuqspjiaOZaXvKOmAJ1jNe6WLJ0jPVH.

These cover imports/setup and are relevant to the proposed integration. The model
made no edit proposal and requested no check. No source was changed, and the
archived files are byte-identical to baseline. No natural repair, candidate check,
withheld candidate grading or independent integration acceptance occurred.

## Failure and evidence qualifications

The shared process returned a CodingResult containing ProjectionCapacityError.
The experiment wrapper then failed while recording it: support.plain calls
dataclasses.asdict, which deep-copies the custom exception; reconstruction passes
a string to a constructor requiring ProjectionOutcome and raises AttributeError.
The observed wrapper exit was 1. This is a demonstrated experimental capture
defect. No production code was changed to repair it during this attempt.

The original complete result, projection outcome and native Tool feedback were
therefore not retained. We preserve the actual two request/response pairs, raw
bodies, unchanged archive, release receipts and wrapper failure qualification.
The native read selections are known; their detailed acknowledgment/result records
must not be invented. No second coding-model entry is recorded. Neither a failed
patch nor inadequate engineering judgment is demonstrated by this interruption.

A separately recorded [pure reconstruction](reconstruction.json), using the
frozen baseline, actual native selections and the expected successful source
feedback representation, produces an insufficient projection: 49,081 bytes both
before and after selection, against a 32,768-byte cap. This runs only existing
Context/projection functions; it dispatches no Tool, model, command, edit or check.
It is diagnostic reproduction, not a recovered execution receipt or exact original
outcome measurement.

The relevant mechanism is source working-set affordability. Initial host-selected
user source messages are not removable native exchanges. The shortening loop
tries one source at a time and restores it if that single reduction cannot fit;
it does not accumulate multiple insufficient reductions. With the reconstructed
large source set and two-result newest exchange, it retains the over-budget
representation. Exact original capacity bytes remain unknown because the recorder
failed. This is a concrete framework boundary to characterize before another
coding trial, not grounds for another retrieval system or speculative refactor.

## Acceptance, preservation and next action

The checkpoint passed; the maintenance attempt failed to reach an edit. Focused
worker checks and withheld candidate acceptance did not run. The three additional
integration predicates have not been validated on a changed candidate. B-0035 is
not complete, and no model-authored change entered production. No second attempt,
manual repair or settings change followed the failure.

The next single priority is a bounded characterization/correction at the existing
projection owner for jointly affordable source reduction, with exception-safe
experiment capture before another live continuation. Keep the successful decision
preparation and current model/profile as evidence; this run does not support a
model-capability failure or require a new agent subsystem. This recommendation is
not implemented or automatically authorized here.

Both Checkout owners released normally. All generated run artifacts were in ignored
storage until release; the coding entry freeze was created before ownership and
preserved as part of its original inventory. Source/index and archived baseline
bytes are unchanged. Historical experiments, original thirteen forensic files,
903 RI rows, refs and 188 outstanding obligations remain preserved. The earlier
unknown grading-wrapper receipts retain their original unknown qualifications.

Fresh focused native/Prompt/provider/oracle regressions passed 252 tests in 0.52
seconds. [Validation](validation.json) verifies raw/native correspondence and all
1,188 unchanged protected physical inputs. No production/test/configuration change
or accepted candidate exists, so the full executable gate was not repeated. Its
prior result remains 3,899 passed, two optional skips and 100% configured coverage.
Layout, JSON/JSONL, Intake, local links, whitespace, ancestry and artifact hashes
are checked at closeout. [Manifest](manifest.json) and publication receipt preserve
the exact delivered inventory and accepted main separately.

[Publication receipt](publication.json): ordinary non-force main publication at `4324818c693912109f79fce4ba12146b7376f837` was independently verified. Exact artifact blobs match physical bytes. The following receipt-only closeout changes no executable input or evaluation result.
