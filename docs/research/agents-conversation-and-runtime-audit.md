# Agents, Conversation and Runtime comprehensive audit

## Baseline, authority and exact scope

Authenticated local and independently observed remote main
`87f5b9d2cbe8f92538af8510da7bca6e148d31b6`, tree
`0a0ad1f97e7c15c6cd22da4aa638d26bda8fe7ac`, on 2026-10-26. Tracked tree
and index were clean, no Checkout owner was present, and all thirteen original
untracked forensic files matched their recorded raw hashes. Ordinary branch:
`audit/agents-conversation-runtime-20261026`. No additional checkout or source
copy was created.

The [frozen cohort](code-audit/agents-conversation-runtime-cohort.json) records
**35 paths, 3,921 lines** before substantive review: seventeen implementation,
export or marker paths and eighteen test/marker paths. All selected bodies,
fixtures, helpers, assertions and significant failure branches received full
review. Both opt-in live-test bodies were inspected but not enabled. Runtime's
matching 177-line body had prior full review and was reauthenticated/reread;
earlier targeted Conversation, attempt and test inspection did not silently
become full credit. No subdivision or selected remainder is hidden.

The [assurance ledger](code-audit/agents-conversation-runtime-assurance.json)
records exact blobs, per-path/function depth, test quality and each additional
dependency's complete versus targeted scope. Immediate dependency work is not
whole Persistence, Evidence, application, tooling or historical experiment credit.

Authority remains the taxonomy, accepted ADR-0001, current source/tests and
canonical documentation/backlog distinctions. B-0017's execution/Evidence
ownership is settled; B-0026 is superseded by its children. No generic Run,
ConversationTurn, BaseAgent, executor, orchestration or persistence API is
authorized by this review. PRs31–33 and their five P2 corrections remain
delivered. The prior 3,142-pass/two-live-skip/100% production gate is retained
historical validation, not a new audit result.

## Ownership and actual lifecycle traces

| Flow | Actual implementation and retained outcome | Supported boundary |
| --- | --- | --- |
| A: normal model exchange | Runtime acquires Conversation.turn, appends the caller message, optionally starts an InteractionAttempt, selects continuation by source, builds Prompt/ModelRequest, awaits one send, validates response source, appends a fresh assistant message and replaces only a supplied continuation | Prompt contains the current message, not automatic replay of History. A missing replacement retains the existing ref. Returned ModelResponse remains available to the caller. |
| B: failure/cancellation | Admission failure stops before provider; provider/source-validation failure retains input without assistant output. Cancellation while waiting for the turn admits nothing; cancellation after invocation retains input and terminalizes the optional attempt as cancelled | No rollback, retry, model-entry certificate or zero-usage inference. Reusing the same message explicitly is a second call and another transcript position. |
| C: observation | llama provider normalizes the response, then constructs completed observation and calls optional observer. Backward wall order or callback error can hide the known result; Runtime records invocation-stage failure | Execution attempt observation and provider completion capture are separate. Terminal attempt-callback failures are contained. Current APIs do not report capture failure separately. |
| D: external Codex | CodexAgent validates user role/ref source, constructs a managed fresh/resume CLI command, checks exit/truncation, parses JSONL, captures optional usage and returns CodexConversationResult | It is not ModelInteraction, not a Runtime Agent loop, and does not itself append Conversation state. Caller supplies turn/add/set composition. Role/source admission is not publication authority. |
| E: native Qwen | local_interaction checks the existing service profile and constructs an unobserved llama adapter. coding_loop owns PromptMessage history, explicit request/capacity/task limits, direct send, response archive and selected-source validation before Tool admission | Default worker bypasses Runtime/Conversation/Inspectors. Offering these APIs does not establish native adoption. Cancellation during MODEL_REQUEST records unknown completion/no retry; existing restoration/Checkout ownership remains separate. |

Conversation is a mutable entity with durable ID, timestamp, immutable History
snapshots and a live read-only continuation mapping. Object equality is not
semantic-ID equality. History preserves insertion order, duplicate positions
and supplied message identity/content; it does not sort by time or deduplicate.
Direct add/set methods are cooperative synchronous mutations. The turn lock is
object-local, nonreentrant and process-local; separately reconstructed equal-ID
objects do not share it. It is not Checkout fencing or source authorization.

Message retains text, role, source, identity and time. Runtime's text projection
does not put reasoning, Tool calls or usage into Message. Those remain in the
returned response and appropriately retained application/Evidence records. A
persisted Conversation is not a complete model-request/Agent Run replay.
Targeted strict JSON and SQLite tests show semantic identity/history/ref
round trips with fresh object coordination; the Persistence domain is not yet
fully audited.

InteractionAttempt is allocated only with an observer and has one terminal
transition. Timestamp acquisition precedes mutation, so a timestamp failure
leaves it RUNNING. Earlier wall completion is expressly permitted as observed
fact, unlike ModelInteractionObservation's ordered interval. Runtime suppresses
secondary terminalization/callback failures; known output can therefore survive
while terminal Evidence is unavailable, or an attempted terminalization leaves
a live RUNNING reference. This is existing qualified secondary-failure behavior,
not a new successful-Evidence or monotonic-time promise.

## Actual consumers and adoption limits

Maintained source/caller searches find no native CodexAgent.send composition
outside tests; the opt-in live Conversation test explicitly performs
turn/add/send/add/set. Its older live evidence is not refreshed by this audit.
The adapter's parser/usage helpers do have consumers: retained semantic workers
parse stdout and apply stronger exactly-one-thread/completion and no-Tools host
checks; metadata ingestion calls read_session_usage; scripts/usage.py consumes
read_exec_usage and separately checks trusted thread lineage. No controller was
run and no historical version received additional closure credit.

WorkCycle/local integration accepts source-bound host review records labelled
Codex. A reviewer string is not invocation of CodexAgent or evidence that an
independent review occurred. IntegrationAuthority and delegation retain distinct
host scope/grant/publication ownership. Existing read-only acceptance scripts
compose Runtime, while the native coding worker uses its direct bounded loop.
This is concrete application composition, not a reason to force every consumer
through Runtime or build a universal Agent interface.

ExecutionInspector retains local terminal Evidence before optional sink
delivery. The independent sink-failure case returns the known response with
one locally retained record, despite failed external delivery. That is neither
durable acceptance nor a currently exposed capture-failure channel.
ModelInteractionInspector accepts completed observations only. There is no
existing native capture-failure consumer or automatically joined provider-ID /
attempt-ID / task record. CodexConversationResult.usage_error is an actual
optional-accounting separation precedent; it does not authorize copying
metadata fields into ModelResponse.

## Confirmed P2 findings

The [probe artifact](code-audit/agents-conversation-runtime-probes.json) retains
complete independently authored source, exact baseline/execution/hash, literal
expectations and observations. Thirty-three cases produced four contract
failures across two families, with twenty-nine agreeing controls or explicitly
qualified existing limits. No harness errors or unhandled loop errors occurred.

### Literal text is interpreted as CLI options

Pending P2
[`b8cf4f09-0b9b-4592-8bd3-4d42d5a1778d`](../backlog/proposals/b8cf4f09-0b9b-4592-8bd3-4d42d5a1778d/proposal.json).
CodexAgent.send appends the message directly to argv without an option
terminator. Installed codex-cli **0.162.1** consumes the literal user message
`--help` as an option in both fresh and resumed paths: exit0, CLI help instead
of JSONL, then CodexOutputError. The resumed test used a synthetic all-zero
thread ID and still exited in help parsing; no real session was resumed.

Direct argv protects shell argument boundaries, not interpretation by the CLI.
Existing fake-executor tests assert shape but miss this boundary. The current
[official CLI reference](https://learn.chatgpt.com/docs/developer-commands?surface=cli)
documents positional prompt text, the stdin dash and configuration options;
local version/help and actual help-only public-adapter calls establish this
installed behavior. They do not certify current live sandbox effectiveness.

A bounded repair should protect leading-dash prompt and continuation values,
explicitly account for the dash/stdin sentinel, and reuse existing Command stdin
or supported positional mechanics. Preserve readonly/cwd/source/role/error/usage
behavior and no retry. No dangerous option, model invocation, sandbox bypass or
source mutation was executed. The baseline-only probe explicitly refuses a
corrected positional delimiter before process entry: do not rerun it unchanged
after repair, when literal `--help` could become an actual model request. Future
permanent tests should use deterministic executors and safe parser/help checks.

### Escaped unknown fields bypass metadata-only admission

Pending P2
[`f99678ae-c7d8-4574-a057-da582647d540`](../backlog/proposals/f99678ae-c7d8-4574-a057-da582647d540/proposal.json).
Both read_session_usage and read_exec_usage check raw field names with an
ASCII-only regex before json.loads. The valid escaped key `priv\u0061te` is
invisible to that check. An authored private sentinel reaches the decoder and
one usage row is admitted in both paths. Equivalent plain `private` controls
skip/refuse before decoding. Existing test_sources privacy spies cover only
plain keys and miss the equivalent JSON spelling.

This violates the supported metadata-only/unknown-shape boundary. It is not
evidence of returned private content or external exfiltration, and no personal
log was opened. Actual ingestion/report consumers establish relevance. The
repair must refuse unsupported/private field spellings before payload decoding,
including nesting, while preserving supported metadata/value escaping and
existing unavailable/skip/error policy. Decode-everything-then-filter would not
repair this contract. A new JSON framework or persistence store is unnecessary.

## Correct behavior, limitations and test quality

Independent Runtime cases confirm one call, primary-error preservation, exact
source refusal before assistant retention, admission refusal before invocation,
serialized turns and cancelled waiters without admission. Explicit repeat after
failure makes two calls and retains two copies of the same input ID. Controlled
output-retention failure leaves input only; controlled continuation-replacement
failure leaves input/assistant plus the old ref. These latter cases inject a
host Conversation subclass fault; they are not a demonstrated failure of native
list/dict storage. They establish partial boundaries and no rollback claim.

The parser expressly documents presence-based acceptance. A completed first
answer followed by another turn.started remains accepted as that earlier answer;
this is not final-open-turn assurance. Stronger chronology/thread correspondence
would need a separately justified contract and consumer migration. It is not
silently promoted into a new bug during this audit. Recoverable error events,
last completed message selection and semantic success despite optional malformed
usage match current docs. Nonzero CLI exit can preserve reported tokens;
truncated stdout refuses complete usage; command cancellation without a returned
CommandResult cannot fabricate usage or prove no process entry.

Value/lock/state tests have independent literal assertions and barriers. Test
execution alone does not confer review depth. The Runtime invalid-settings test
constructs an invalid ModelSettings before send: it proves the value boundary,
not a second Runtime validator. Synthetic private terminal guards establish
secondary containment but not durable capture. Two live bodies remain skipped.
No autonomous-agent effectiveness, OS sandbox certification or backend-level
exactly-once property was measured.

## Concrete observation-policy feasibility

**Maintainer preference: Option B in principle. Status: not approved or
implemented.** The current source and all prior observer behavior remain
unchanged. The existing [decision brief](../development/model-observation-policy-decision-brief.md)
and ADR-0001 continue to govern.

| Question | Concrete recommended scope and compatibility consequence |
| --- | --- |
| Producer/owner | The provider that has just constructed ModelResponse owns separation of invocation from observation. Catch only ordinary completion-construction/callback failures around that exact region; never suppress pre-entry request validation, Runtime admission or genuine cancellation indiscriminately. |
| Failure contract | A narrow companion transient capture-failure fact/protocol under interaction.observation can carry occurrence ID, source/provider, construction-versus-callback stage, safe error category and actually available wall instants/usage. Do not put transport metadata in ModelResponse or mutable request/provider settings. Names are proposals, not new APIs. |
| Existing consumer | Extend ModelInteractionInspector's process-local inspection with a separate failure collection under existing capture/privacy policy. It currently cannot receive such facts. Completed Evidence remains distinct; failure is not fabricated successful Evidence. No default raw exception text, prompt, response content or provider ID retention. |
| Minimal compatible rollout | Prefer explicit opt-in through a separately supplied failure reporter at the existing provider constructor/composition seam. An absent reporter retains legacy propagation initially. Keep send(ModelRequest)->ModelResponse unchanged. A default-on behavior change requires an explicit compatibility decision. |
| Correlation | Current ModelResponse exposes no occurrence ID. Use an invocation-local reporter/adapter or the demonstrably serial task-local worker scope. Shared concurrent adapters need a separately specified correlation route; request-value equality, source label or last Inspector record is insufficient. Do not create a registry or smuggle identity into ModelResponse. |
| Runtime/attempt | When a known valid response returns and output/ref retention succeeds, the specialized attempt can remain SUCCEEDED: that fact concerns Runtime mechanics, not task acceptance or durable capture. Keep real admission/retention/cancellation failures distinct. No new attempt state or Conversation schema is necessary for this first scope. |
| Mandatory evidence | A trusted host examines the matching report after receiving/retaining the known response. For opt-in Qwen, place a required-capture guard after response archival/source validation and before proposal/Tool admission. Refuse workflow acceptance without erasing known response/usage, dispatching Tools or automatically retrying. This app-report compatibility must be approved before implementation. |
| Native/default behavior | Current Qwen adapter is unobserved; it remains unchanged unless the host explicitly opts into capture. Existing custom observed clients need migration tests. Codex optional usage_error demonstrates separation in a different domain, not permission to alter ModelResponse. |

Backward wall time may prevent completed-observation construction before callback
entry; preserve the two actual instants or mark the unavailable instant, rather
than clamp a clock or fake ordered Evidence. Canonical Stopwatch could provide
elapsed time later, but is not necessary to return the known result and cannot
solve callback failure. A callback may have retained or externally delivered
facts before raising: capture failure is partial/uncertain, not proof that no
Evidence exists. Known usage remains known; missing usage is not zero/refundable.

The failure reporter can itself fail. Existing ExecutionInspector illustrates
local retention before an external sink, but its swallowed sink exception is
not a sufficient new reporting contract. Approval must choose guaranteed local
inspection before fallible delivery and specify secondary-report failure. One
narrow alternative is Option A as an explicit post-response exceptional fallback
with controlled access to the known result; it changes failure APIs and requires
privacy/no-retry consumer migration. Silently dropping both failures while
returning success is not an acceptable implementation of Option B.

Option A alone is feasible and preserves failure-first caller control flow,
but encourages generic retry mistakes and puts known results on exceptional
paths. Option B better matches optional capture and the maintainer preference.
It is feasible for the bounded opt-in/serial scope without a Runtime/Agent
rewrite. Transparent global/default concurrent support is **not** established
by current interfaces. Required decisions are rollout/default, report fields
and privacy, correlation, secondary-report failure, cancellation semantics,
mandatory-host guard and any additive durable app-schema compatibility.

Minimal future acceptance must cover observed/unobserved success, construction
and callback failure, backwards clock, sink-after-effect failure, known/unknown
usage, primary response identity, same-value concurrent requests, retained
Conversation/attempt outcome, failed mandatory capture before Tool dispatch,
real cancellation and exactly one provider call. Test one current provider plus
Inspector and one explicit host consumer; do not introduce EventBus, global
tracing, response wrapper, persistence database, generic observer framework or
retry supervisor. No such implementation is authorized here.

## Cohesion, backlog and remaining work

The dependency direction is coherent: Agents/Conversation reuse Core values;
Execution coordinates Agents and Models; Observability consumes execution facts;
Persistence stores other domains' snapshots; apps own concrete task loops.
Codex shares source/ref/usage values without pretending to implement the model
request protocol. Runtime's narrow one-invocation scope is useful but is not
task interpretation, model Context assembly, Tool authorization or publication.

Concrete duplicated lifecycle/capture handling exists across Runtime, Codex
optional usage and Qwen reports, with intentionally different claims. Improve
the demonstrated owner-local contracts and explicit consumer joins before
consolidating. No generic BaseAgent/Run hierarchy is justified by these fields.
Current root Codex docstring calls it a ModelInteraction provider; tests retain
Context/Session/ModelResponse wording; CLI docs reference an obsolete live-test
path and older0.147 acceptance. B-0006 owns stale wording. Historical session
wire names remain deliberate durable compatibility, not rename authority.

Two new pending P2 proposals follow duplicate checking all62 existing payloads
and relevant backlog scopes. The queue now has64 valid chains. B-0011/B-0046
receive the concrete unapproved capture recommendation; B-0043/B-0041/B-0023/
B-0034/B-0006 receive bounded consumer/limit evidence. B-0017 ownership stays
settled and B-0026 superseded. No approval, grant, B-number, terminal state or
parent closure was created. All prior delivered P2/RI/worker/Checkout/validation
repairs remain delivered despite administrative pending proposal states.

Next bounded maintenance should address the two confirmed P2s with permanent
independent regressions and a final committed protected gate; the observation
decision remains separate. Then begin Persistence's actual snapshot/schema,
SQLite conflict/atomicity/recovery and current-consumer audit, reusing targeted
identity evidence without claiming it complete. Remaining applications,
developer/scientific tooling and cross-domain consolidation remain explicit.
RI original fixtures93/93, experimental paths606/606,188 historical exact versions
and unapproved A+C are unchanged. No next cohort or successor dossier began.

## Validation and publication

- `uv run pytest --no-cov tests/agents tests/execution -q`: **141 passed,
  two opt-in live skips**, 0.65s, exit0.
- Focused Evidence/usage-source/JSON+SQLite persistence/Runtime-Tool/Qwen
  consumer command in the assurance ledger: **125 passed**, 62.76s, exit0.
- **33 independent cases**, four contract failures across two new P2 families,
  twenty-nine agreeing controls/known limits; no harness, unexpected-control or
  unhandled-loop failures. Final exact-source run0.63182s, exit0, CPython3.14.3.
- Installed Codex0.162.1 version/help plus help-only adapter probes. No model,
  live acceptance test, Docker, service startup, download or scientific replay.
- [Checkpoint](code-audit/agents-conversation-runtime-checkpoint.json): exact
  frozen/dependency blobs, JSON/Intake chains, local link targets/layout,
  whitespace, unchanged executable inputs, RI ledgers and13 forensic hashes.
  Local link validation does not certify external URLs or Markdown anchors.

One ordinary documentation/Intake branch and normal review PR publish this audit.
No new protected gate is required for unchanged executable inputs, no review is
fabricated, and an open PR is not protected-main adoption. The ignored completion
report records the actual containing commit/remote/PR state.

`audit:agents-conversation-runtime:87f5b9d2:20261026`
