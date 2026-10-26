# ModelInteraction and Serving comprehensive audit

## Baseline and authority

Reviewed integrated local and independently observed remote main
`a7a49cc18f3b40a5bf4e3897ca30d9a5cddc30d1`, tree
`922681231aa238a9ad6927dc2bf3562db4641d39`, on 2026-10-26. The ordinary audit
branch is `audit/model-interaction-serving-20261026`. The initial tracked tree
and index were clean; no Checkout owner was present. All thirteen original
untracked forensic files retain their recorded raw SHA-256 identities. Their
presence is preserved evidence, not new work to stage.

[ADR-0001](../architecture/decisions/ADR-0001-cohesive-model-interaction-boundary.md)
is accepted authority: immutable requests, one selected `send` boundary, typed
provider-local options, descriptive Tools and optional completed-success
observation. Its three implemented slices remain delivered. The taxonomy keeps
ModelInteraction, Serving, Runtime, Agent, Evidence and authority distinct. This
audit does not approve a new lifecycle, provider framework, failure-observation
policy, retry mechanism or durable schema.

This is a documentation/Intake checkpoint. Production source, tests, configuration,
frozen experiments and prior repair evidence are unchanged. The earlier
filesystem/Duration, RI, worker, Checkout, Commands and validation corrections
remain delivered. The previous 3,077-pass/two-optional-skip/100% configured
production gate is retained historical evidence; no new protected gate was run.

## Exact scope and review depth

The [frozen cohort](code-audit/model-interaction-serving-cohort.json) retains the
original selection and adds a maintenance review overlay. All **30 exact paths,
7,119 lines** were inspected completely: thirteen Interaction and six Serving
source paths, seven Interaction and four Serving test paths. This includes
public initializers, marker roles, implementations, tests, helpers, fixtures,
monkeypatches, assertions and failure branches. Both domains' selected bodies are
complete; Serving was not silently deferred. Per-path Git blobs, functions,
findings and exact additional dependency depths are in the
[assurance ledger](code-audit/model-interaction-serving-assurance.json).

Complete immediate dependency review also covered Runtime's narrow body, Tool
disclosure and Qwen's small disclosure adapter. Targeted consumer/dependency
inspection covered Qwen coding-loop admission, worker construction, persistent
llama.cpp service operations, the vLLM benchmark entry, streaming benchmark
timing, Conversation, InteractionAttempt and ModelInteraction Evidence. Tests
executed outside the cohort did **not** automatically receive full-body credit.
Agents, Runtime as a domain, Persistence, model benchmarks, applications and
developer/scientific tooling still require their proper comprehensive reviews.

## Actual lifecycle and owners

| Boundary | Implemented owner and supported claim | Failure or consumer qualification |
| --- | --- | --- |
| Request | `interaction/models.py`, `prompt.py`, `tools.py`: immutable portable controls, typed provider extension, structured message/Tool sequence checks | Capability and proposal carry no execution authority. A schema object is syntactically validated, not a complete JSON Schema metaschema. |
| Selected provider | `LlamaCppInteraction.send` creates occurrence identity/start time, projects request and invokes one HTTP POST | Foreign continuation or extension can refuse before transport. There is one maintained Interaction provider, not HF/vLLM provider parity. |
| Transport | Provider-local asyncio HTTP, explicit length/chunked/EOF handling and writer `finally` | Connect and post-write errors both normalize to TransportError; that does not establish nonentry. No built-in retry, overall deadline or full-body memory cap. |
| Normalization | Provider checks first choice/content/reasoning, termination, usage and native Tool calls | Returned calls are descriptive. Unknown termination/usage remain unknown. Malformed responses may follow real provider execution. |
| Observation | Optional transient `ModelInteractionObservation` after response construction; external observer owns capture | Successful normalization can be hidden by observation construction/callback failure. This seam is not failure Evidence or an atomic persistence protocol. |
| Runtime | Conversation lock/input retention, selected `send`, source correspondence, response/continuation retention, optional specialized attempt | Provider-observer exception becomes failed interaction invocation; terminal attempt-observer errors are contained. These are distinct callbacks and policies. |
| Native Qwen | Request disclosure, template token count, model/proposal limits, task deadline, send, response archive/source validation, Tool admission | Worker-created llama adapter has no observer by default. Source correspondence repair is present; no Tool dispatch from a foreign response. No inference was run here. |
| Observability | Policy-controlled conversion/Inspector accepts completed observations | Default capture omits sensitive categories; provider-setting **type**, not values, is captured. First-wins Inspector behavior is documented. Native Qwen journals are not automatic normalized ingestion. |
| Serving | Configured Docker processes, owned CID/label status and cleanup, readiness; HF pinned single-file acquisition | Serving is not ModelInteraction or task authority. Configured tag/fingerprint is not measured immutable model bytes or remote acceptance. |

The llama provider intentionally maps prompt/completion/total usage only. Unknown
counts stay `None`; a provider-reported total of 99 remains 99 alongside 8 input
and 4 output tokens. Cached/reasoning promotion is expressly unapproved in
B-0046; its absence is not a new defect. There is no occurrence-to-attempt
automatic correlation or failed-call usage journal. A lost/absent usage report
does not establish zero consumption or justify a refund.

The provider's token-count path uses the same request projection with
`/apply-template` and `/tokenize`. Native Qwen actually calls it for its bounded
llama context check, rather than merely exposing the API. This is an explicit
application-specific capability check, not general model-neutral effectiveness
proof. Calls/continuations, termination and response source are validated before
the actual authorized Tool path continues.

## Independently confirmed P2 defects

All failures below ran through maintained callers against the unchanged pinned
implementation. The [probe record](code-audit/model-interaction-serving-probes.json)
retains the complete independently authored source, SHA-256, execution identity,
literal expectations and observed outcomes. Forty-four cases produced eighteen
contract-failure observations across five families; twenty-six controls and
explicit existing-limit observations agreed. There were no harness errors,
unexpected control failures or unhandled event-loop errors. No Tool execution,
authorization bypass or actual autonomous-agent failure is claimed.

### Malformed UTF-8 response error normalization

Pending P2
[`8c79f8ca-20c0-434d-90f8-9418f0767e57`](../backlog/proposals/8c79f8ca-20c0-434d-90f8-9418f0767e57/proposal.json).
An otherwise correctly framed response with literal body byte `ff` raises
`UnicodeDecodeError` for both HTTP 200 and 500. Existing public error contracts
require malformed successful content to refuse as `LlamaCppResponseError` and
an HTTP error to retain status through `LlamaCppHttpError`. `_post_json` and
`_error_detail` decode outside the appropriate normalization. Each case writes
one request and closes its connection; there is no retry or observation. A
bounded fix should retain causal decoding detail, HTTP status and all valid
transport controls, without inventing a nonentry claim.

### vLLM readiness framing and shape

Pending P2
[`333df5ec-5a67-4b3c-8b1b-71dd4f544f83`](../backlog/proposals/333df5ec-5a67-4b3c-8b1b-71dd4f544f83/proposal.json).
`VLLMServer.status` reports running but not ready when valid matching-model JSON
arrives after a legal short `read(n)` returning just headers. `_http_get` reads
once; the existing test double returns the whole response and misses this case.
Complete valid JSON roots `[]` and `null` separately raise `AttributeError` in
`_probe_model_ready` instead of the existing conservative not-ready outcome.
Matching complete response and wrong-alias controls behave correctly. Repair
the existing bounded response/shape contract, not a general HTTP client.

### Owned readiness writer cleanup

Pending P2
[`54fe0021-8992-47b2-85bc-4bdce6ade4e0`](../backlog/proposals/54fe0021-8992-47b2-85bc-4bdce6ade4e0/proposal.json).
Both Serving `_http_get` implementations omit a writer-closing `finally`.
Public status/readiness paths return refusal or propagate cancellation/timeout
while the opened writer remains unclosed. Six deterministic reader-failure,
cancellation and readiness-timeout cases expose this. An actual ephemeral local
HTTP sink additionally observes a retained real `StreamWriter.is_closing()` of
false after the cancelled operation settles. The fixture then explicitly closes
all resources. This establishes missing owned-connection settlement at the
operation boundary, **not** a leaked inference process or permanent OS leak.
Preserve original failure/cancellation while closing/settling owned streams.
This is separate from the delivered Command stream-collector correction.

### Registry port mistaken for image tag

Pending P2
[`a0ccec58-586d-4f46-8da8-37d26a447bf2`](../backlog/proposals/a0ccec58-586d-4f46-8da8-37d26a447bf2/proposal.json).
Both configurations accept `registry.example:5000/team/server`: they see a colon
in the registry authority although the final image component has no explicit
tag. Existing documented admission requires a tag or digest. The same registry
with `server:cuda` or `server@sha256:<64hex>` is a legitimate control. Only
configuration construction was exercised; no actual implicit Docker pull is
claimed. A mutable explicit tag still does not prove cryptographic immutability.

### Nonstandard JSON constants in Tool representations

Pending P2
[`bf8cf791-ffc8-4d7f-ac6c-94613b87e181`](../backlog/proposals/bf8cf791-ffc8-4d7f-ac6c-94613b87e181/proposal.json).
`ModelToolDefinition` and the compatible Tool disclosure boundary accept
`{"type":"object","default":NaN}`. The actual provider's captured request
contains `NaN`; an independent strict parser rejects that wire JSON. Native
returned argument objects containing `NaN`, `Infinity` and `-Infinity` also
become ModelToolCall values despite the valid-JSON object promise. No Tool was
executed. Reject nonstandard constant tokens at the existing owned boundaries;
retain valid raw argument spelling and typed object errors. Full metaschema or
duplicate-member policy is not part of this defect. A grammar-valid JSON number
such as `1e999` is a distinct representability question, not the same token bug.

## Observer outcome and backward wall clock

The original case remains reproducible: one successful normalized response is
followed by a completed wall timestamp earlier than its start. Observation
construction raises `ValueError` before the callback; `send` returns no response.
Without the observer the same clock sequence returns normally. A callback that
raises after capturing its observation similarly produces `RuntimeError` for
the caller, though that callback has the response, usage, source and provider
response ID. Neither case retries the request.

The actual Runtime probe shows provider-observer failure leaves retained input
but no assistant response in Conversation; its specialized attempt fails at
interaction invocation. In contrast, a terminal attempt-observer failure is
contained and Runtime returns the response with a successful attempt. The
default native Qwen adapter is unobserved, so the backward-clock failure is not
a demonstrated default native-worker failure.

This is an existing acknowledged ADR-0001/B-0011/B-0046 policy limitation, not a
new Timestamp defect or permission to suppress mandatory evidence. A maintainer
decision must choose among compatible scope changes:

- Retain propagation but provide an explicit post-response/observation-failure
  outcome carrying the completed result under appropriate privacy policy. This
  changes public failure/result contracts and needs consumer migration.
- Contain optional completion-capture failure at the correct composition owner,
  preserve the primary response and independently expose capture failure. Silent
  evidence loss or suppression of pre-entry authority checks is unacceptable.
- Separately represent observed wall instants and monotonic elapsed duration or
  a clock-adjustment outcome. Canonical Stopwatch may measure duration, but
  alone cannot fix the ordered-wall-interval invariant or callback exceptions.
  Observation/Evidence compatibility must be decided explicitly.

No timestamps are clamped, successful Evidence fabricated, completed requests
retried or policies changed by this checkpoint.

## Serving lifecycle and ambiguous effects

llama.cpp and vLLM use canonical managed Commands for Docker, validate returned
64-hex CIDs, and require the managed label before owned stop/remove. Known-handle
readiness failure/cancellation attempts cleanup and preserves the primary error
with bounded cleanup notes. Readiness timeout starts after launch/preflight; it
is not a whole-start wall deadline. Liveness and model readiness remain distinct.
The API is documented experimental/unfrozen; this audit does not certify GPU,
Docker, image version or hardware compatibility.

A deterministic launch executor writes a fixture marker then raises a lost-ack
error. Each adapter has one launch attempt, no returned handle and no automatic
retry/guaranteed cleanup. This proves possible effect-before-error control flow
using a fake, not actual Docker execution. Reconciliation after real ambiguous
launch requires the separate B-0034 owner, not an exception-equals-no-effect
assumption.

The native persistent Qwen service has its own stable-name/labels/configuration
fingerprint/reuse/conflict policy. It uses four private llama Serving helpers
for launch/preflight/CID/readiness, rather than `LlamaCppServer.start` as its
lifecycle. Consequently a bounded helper cleanup fix reaches a real maintained
consumer, but transient and persistent custody must not be conflated. The vLLM
benchmark entry actually uses VLLMServer start/benchmark/stop; it was traced,
not run. Serving's HF module acquires a revision-pinned single GGUF and validates
snapshot/backing paths under cache. It is not a model-inference provider.
Cancellation of its async `to_thread` await cannot terminate the blocking
download; a controlled fake writes after cancellation. No download occurred.

## Cohesion, test quality and remaining decisions

The immutable request/provider/Serving separation follows ADR-0001. Native Tool
disclosure is an explicit application adapter; model source identity is checked
at actual Runtime/Qwen consumption. Canonical Command, path, time and identity
primitives are reused. These are supported architectural strengths, not a
claim that agents understand tasks or that model execution is sandboxed.

Concrete simplification pressure exists in repeated first-choice validation,
duplicated Serving HTTP mechanics and repeated schema parsing/canonicalization
across disclosure/application/ModelToolDefinition. Preserve domain dependencies;
do not import provider-private transport into Serving or create a universal
HTTP/schema/provider framework. A future small repair can share narrowly owned
mechanics only where semantics match. The llama-prefixed provider sibling files
also create package-organization pressure, but current public module/type names
and durable capture compatibility must be inspected before repackaging; it is
not needed to fix these bugs.

The serving overview's Status says only vLLM despite its later llama sections;
Qwen composition's docstring still calls maintained application code an
experiment. Existing B-0006 owns the stale wording. B-0007's older completed
documentation scope and B-0045's delivered request core are not reopened.

Test oracles use meaningful literal payloads, actual source-free local value
contracts and controlled command/network doubles. They establish normalized
wire/error/control behavior, not live provider conformance or performance.
Current omissions explain the five P2s: invalid UTF-8, partial HTTP body arrival,
nonobject listing shape, writer settlement, registry-port syntax and nonstandard
JSON constants. Existing native-source/budget/acceptance repairs remain in the
consumer suite. No P0/P1 defect is independently established in this cohort;
unresolved observer/recovery policies still limit operational signoff.

## Backlog and finite next step

Five new canonical pending proposals were captured after duplicate checking all
57 existing proposal payloads and scoped backlog evidence; the queue now has 62
valid chains. Each new UUID includes owner, source, reproducer, consumer impact,
independent acceptance criteria and uncertainty. No approval, grant, B-number,
status transition or parent closure was created. B-0011, B-0046, B-0041, B-0034
and B-0006 receive append-only maintenance evidence with their authority and
maturity unchanged. No duplicate clock/observer proposal was created.

Next bounded maintenance should address the five demonstrated owner-local P2
contracts with permanent baseline-failing regressions and full final committed
production validation. Keep the observation-result policy as an explicit
maintainer decision rather than silently including it in a cleanup repair.
Then proceed to the broader Agents/Runtime and Persistence/application review
under the existing comprehensive program; do not start an indefinite new
Serving research cycle. This report does not freeze or execute another cohort.

RI original fixtures remain 93/93 (augmented fixture universe 94), historical
experimental paths 606/606 at their defined depth, and 188 exact historical RI
versions remain separate obligations in their existing families. A+C task
obligations remain unapproved. Native normalized Evidence ingestion, full
lifecycle correlation, wider d58697fd validation closure and application
cohesion remain open; recent local fixes do not close those parent scopes.

## Validation and publication boundary

- `uv run pytest --no-cov tests/models/interaction tests/models/serving -q`:
  **321 passed**, 2.91 seconds, exit 0.
- `uv run pytest --no-cov tests/execution/test_runtime.py tests/observability/evidence/test_model_interaction.py tests/apps/qwen/test_coding_loop.py tests/scripts/qwen/test_llama_cpp_service.py -q`:
  **113 passed**, 57.62 seconds, exit 0.
- Final probe execution: **44 cases**, 18 reproduced contract failures, 26
  agreeing controls/known limitations, exit 0, 0.581356 seconds, CPython 3.14.3.
  Exact source and timestamps are preserved in the probe record. These are
  defect observations, not an implementation regression suite claimed green.
- [Checkpoint validation](code-audit/model-interaction-serving-checkpoint.json)
  authenticates frozen/current Git blobs, per-function depth, JSON/Intake chains,
  local file-link targets, layout, whitespace, unchanged RI ledgers, thirteen
  forensics and absence of executable changes. File-link validation does not
  certify external URLs or Markdown anchors.

Publication uses one ordinary audit branch and the normal GitHub PR. Its actual
checks/reviews/permissions must be observed; no independent review, protected-main
promotion or scientific execution authority is fabricated. This audit assignment
authorizes checkpoint publication; an open review PR is not merged/delivered
production status. Publication identity belongs to its containing commit and the
ignored completion report, not a self-referential source hash.

`audit:model-interaction-serving:a7a49cc1:20261026`

## Delivered maintenance overlay — 2026-10-26

The five independently evidenced P2 families above are corrected by production `5125ab6a847ee1844913c006d801b01f5fea7cc4`, normal PR32, verified main `a602dae60b3a7c71bdd1c1231613143c309292c1`. Original audit findings/probes remain historical evidence. [Delivered correction](../development/model-serving-contract-repair.md); [exact validation](code-audit/model-serving-contract-repair-20261026.json); [unapproved observer decision brief](../development/model-observation-policy-decision-brief.md). No observer policy or broader lifecycle signoff is implied. `repair:model-serving-contracts:5125ab6a:20261026`.
