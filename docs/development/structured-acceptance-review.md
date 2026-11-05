# Structured acceptance-review conclusion delivery

Prospective subjects can opt into [task-local working notes](agent-working-notes.md)
through the same reviewer owner. The separate working Context does not change
this Tool schema, identities, grants, strict final delivery or host disposition;
recorded hypotheses remain model-attributed claims.

New acceptance-review subjects bind `delivery` with schema
`native-review-response-delivery-v1`, rule `single-proposal-call-v1`, before
host authorization. The existing reviewer owner in
`scripts/backlog/native/review/` composes this contract using established
`ModelToolDefinition` and `ModelToolCall` values. No executable Tool, registry,
provider interface, Agent loop or review-continuation allowance is added.

## Demonstrated deficiency and options

The [authenticated third B-0052 review](../research/acceptance-review-recovery.md)
captured a raw-JSON instruction, 2,048 output-token cap, disabled thinking,
synthesis budget view, zero acquisitions remaining, empty Tools and
`provider_settings: null`. Its normally terminated response contained prose,
a Python example and a literal placeholder Tool block. No JSON object existed;
the actor correctly blocked at character zero, before schema validation.
There was no structured generation channel beyond the prose instruction.
The evidence cannot explain the model's internal choice or establish a transport
fault.

| Option | Existing support | Decision |
| --- | --- | --- |
| Typed final-proposal callable | Model-neutral schema, raw arguments and provider call ID; llama.cpp serializes and normalizes these values | Chosen: closed proposal channel in the existing reviewer owner, with no provider dependency. No forced Tool-choice setting exists, so absent calls still fail explicitly. |
| Provider-supported formatting | `LlamaCppRequestSettings(response_format="json_object")` | Could be prospectively bound and captured, but is adapter-specific and constrains JSON-object syntax rather than the review schema. Portable settings have no equivalent field; this adapter rejects `json_schema`. Not selected or injected. |

This defines admissible output; it does not guarantee a model will call the
proposal, claim provider-side enforcement of every schema keyword, or measure
Qwen's live reliability. No inference is run here. Other providers implementing
the established callable contract can transport the same proposal. Neutral
scripted implementations exercise the lifecycle; llama.cpp has a deterministic
adapter regression. No new adapter or portable structured-output API is needed.

## Prospective request and response contract

Each request advertises `submit_review_proposal` with a closed schema.
Inspection additionally advertises authorized `read_source`. Reserved synthesis
removes source Tools but retains the proposal callable. System and budget
instructions name that channel. Descriptor bytes participate in complete-request
Context/capture checks; source-batch and refusal forecasts retain the descriptor.
No call, token, response, Context, capture or time budget is increased.

Exactly one proposal call contains `subject_sha256`, `candidate_sha256` and
`conclusion`. The schema discloses the exact approved subject and archived
candidate identities and finite field/list bounds. `conclusion` keeps the existing
seven fields: `disposition` (`accept`, `reject`, `insufficient-evidence`),
`summary`, `evidence`, `findings`, `outstanding`, `requests`, and
`assessed_obligations`.

The unchanged validator rejects missing/extra/duplicate fields, unavailable
evidence, invalid finding qualifications, incomplete accepted obligations and
unresolved acceptance risks. The envelope adds identity binding; it does not
change judgment semantics. The response must have Tool-call termination and one
proposal call with a nonempty fresh provider call ID. Mixed proposal/read batches,
reused IDs, wrong identities/source, malformed arguments and unsupported forms
fail. Text alone, including raw/fenced JSON or the authentic B-0052 prose, is not
a conclusion for these subjects. Accompanying text is retained as untrusted
output; only exact call arguments supply the judgment.

The callable enters no ToolRunner, source read, command or external effect.
Capture retains the complete normalized request/response and exact raw argument
spelling before admission. A validated proposal observation binds request and
response hashes and the original call ID. No output is replaced or synthesized.
Adapter failure before normalization remains an invocation failure; provider
wire-byte archival is not added.

## Authority, history and consumers

Schema validity yields an attributed model recommendation, never certified fact.
The host independently assesses findings and may reject a favorable proposal.
Reject/insufficient-evidence proposals cannot authorize integration. Host
admission reparses the actual final request/call, checks the approved descriptor
and identities, and compares it with the saved conclusion. Existing candidate,
currentness, private-acceptance, custody and integration gates remain.

Absent, malformed, truncated, over-budget or unpersisted delivery cannot imply
acceptance. Mandatory response/proposal capture failure and terminal persistence
failure retain the consumed dispatch. Uncertain completion is not replayed;
numerical remaining calls do not refund a slot.

Historical subjects without this marker retain their raw-content parser and
durable accepted-consumer contract. Diagnostic subjects keep their distinct
presentation rule, validator, grants and advisory-only authority; their findings
cannot promote blocked candidates. New preparation in the existing continuation
paths uses this same delivery rule without changing eligibility or count.
B-0052's consumed v3 cannot chain or replay, and all historical records remain.

The next lawful live opportunity is a separately authorized independent review
of an otherwise eligible, unconsumed acceptance subject after protected validation
and publication, with actual adapter/session qualification and finite authority.
This assignment creates no task, grant or B-0052 opportunity and changes no
serving settings. Deterministic mechanics do not establish model compliance or
review usefulness; those need a later separately authorized live observation.

## Delivery and validation evidence

Executable implementation commit:
`4fe7ac6c90c50e60cf7470ae1dcfa011a6956e21`.
The [immutable validation and preservation packet](../research/code-audit/structured-acceptance-review-20261103/README.md)
retains actual receipts, output identities, input hashes, prior failures and
historical-preservation checks.

The 35 new cases cover all three dispositions, malformed/duplicate/missing
arguments, wrong identities, unsupported or mixed calls, truncation, budget
exhaustion, capture/persistence failures, non-replay, the authentic B-0052 prose,
the real adapter's deterministic wire mapping and positive historical raw-content
host/candidate consumption. Existing diagnostic and acceptance-to-integration
consumers remain protected. Scripted responses establish mechanics, not live
model competence or factual correctness.

The corrected change-aware consumer run passed 796 tests in 3,893.36 pytest
seconds (3,895.045512 managed seconds), with stable declared inputs. The final
five-case compatibility/typed/prose selection passed in 30.11 pytest seconds.
The initial four failed lifecycle assertions exposed tuple versus JSON-list
comparison; the later two offline fixture failures concerned tuple mutation and
the adapter's existing empty-text requirement. These receipts remain failures.
Supported-root Ruff and formatting, default strict mypy (632 source files),
explicit owner mypy (17 files), layout, Intake, links and diff checks passed.

The completed protected run passed **4,269 tests, two optional live skips** and
the unchanged **100% configured line/branch gate**: 14,247 statements and 3,644
branches with none missing. Pytest took 3,986.68 seconds; managed wall time was
3,999.660882 seconds. The fresh-child profile and experiment exclusion were
unchanged. All **1,077 declared executable/configuration inputs and corresponding
Git blobs** match the tested commit through documentary publication, along with
Python/platform and installed packages. The inherited-environment fingerprint
differs; complete ignored/environment/external-state equivalence is not claimed.

An earlier sandboxed launch was stopped after pytest temporary-directory setup
failed with WinError 5. It has an authentic intent and no completion receipt.
The same 20-test group passed with authorized access; the corrected invocation
then ran the unchanged committed candidate and protected profile to completion.
No source or coverage-policy workaround was introduced. Both launch histories
remain explicit rather than claiming there was only one attempted invocation.

Preservation checks authenticate all four historical native work-item folders,
standing controls/decisions, the prior immutable review packet, 630 preserved
historical files, 192 prior native files and thirteen forensic files. B-0052's
candidate and baseline source are unchanged; its review remains BLOCKED with no
native recommendation, host acceptance or integration plan. No model inference,
new Intake, policy replacement, new slot or service change occurred.
The existing Qwen container/image/command/mounts and healthy idle 65,536-token slot
authenticate. Inspector advanced independently from `e3569bb0` to `4ee14926`
and is clean at this evidence checkpoint; this task did not modify or publish
that worktree. No historical refs were deleted or rewritten.

Documentation impact is confined to maintained review contracts, navigation and
this factual packet. Framework APIs/package docs, taxonomy, architecture
decisions, backlog status and historical implementation ledger retain their
existing meanings. No empirical review success or candidate promotion follows.
