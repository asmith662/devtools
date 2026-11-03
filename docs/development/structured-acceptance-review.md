# Structured acceptance-review conclusion delivery

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
