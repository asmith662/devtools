# Framework-first migration 1: native model/Tool composition

Delivered the explicitly authorized first migration. Starting main was
`e84b724c18512d1659b68c0510637262506385f5`. The exact twelve documentation/Intake
paths in draft PR #47 were authenticated; the current assignment approved only
increment 1. PR #47 was made ready and normally merged at
`657d18f863521c3fb2e37901086298dc8aa06543`, tree
`57af63444462931d78e494d67be103c9a86a88c4`. No independent review or approval of
migrations 2–4 is claimed. Production `31627dcae17fa1e429fbc4c1f3d31941ef5803a7`, tree `67edde595e2ab8bade41d5bf1dabba2abf3ec910`, was
normally integrated through PR #48 at `6a331e65ebb5f5c467a32eb694ca7a95056865a1`.

## Reusable operation and actual substrate reuse

`devtools.agents.model_tools` now owns descriptor projection and one selected-call
composition: match the native call against an explicitly selected invocation
descriptor; materialize existing typed Tool input; await required host admission;
delegate to the existing ToolRunner once; return the Tool-defined result unchanged.
Tool names may differ from native operation names. A single responsibility-focused
leaf under Agents suffices; no new package family, executor, registry, BaseAgent,
Result hierarchy, session store or implicit authorization is introduced.

The existing ToolInvocation, ToolDescriptor, Tool, ToolRunner, ModelToolCall,
ModelToolDefinition, ModelRequest/Response and native Prompt remain authoritative.
The independence host additionally uses Repository/occurrence/content identity,
Context planning/materialization, ReadRepositoryFileTool, Filesystem and managed
CommandTool/CommandExecutor. Tools and Models remain independent per ADR-0001;
Agents owns the join. Runtime remains the narrow Conversation collaborator.

## Two distinct operational contexts

Both real Qwen dispatchers delegate to the shared function. Boundary entry
instrumentation observes the selected native operation and original ID, followed
by real exact source reading or a fixed managed check and archived completed
receipt. A controlled exception at that shared boundary propagates by identity,
prevents Tool execution and command reservation, and causes no retry. The legacy
descriptor facade is a direct re-export, with no second normalization body.
Application-owned OperationInvocation materializes the existing `(operation,
values)` input; task-specific scope and semantic/source validation remain intact.

The separate maintained host runs from tiny independently authored Git repositories
with a non-Qwen ModelInteraction. It imports no application implementation and
reads no Qwen task/profile/prompt/configuration. Import and file-open guards
actively deny application access before loading content. Its three actual native
requests include exact source observation/materialization, a normalized read
call, correlated `read-1` feedback, a fixed Command check under `check-1`, and final
response. The literal source returns seven; the fixed check emits exactly
`checked:7\n` and exits 0. Usage stays null/unknown. Its test-only effect Tool is
not a framework editing engine.

Thirteen child-host schedules cover success, unauthorized operation, invalid
arguments, stale source, foreign model source, missing/duplicate native IDs,
failed fixed check, admission cancellation, Tool failure, lost result, cancellation
after an effect and partial batch completion. The partial batch is a real pair
of normalized model calls: the completed read remains known, the second effect
may be known while its result is absent, no feedback is fabricated and no second
model request or automatic retry occurs. Unit controls independently protect
operation-name mismatch, typed input/result identity, exact order and once-only
ToolRunner entry, all materialization/admission/validation/execution failure and
cancellation boundaries, and a mistakenly synchronous admission callback.

## Compatibility and authority

Original task definitions/digests, wire formats, operation names, source identity,
fixed commands, active Context/mandatory witnesses, budgets, journal order,
candidate/terminal semantics, unknown usage and source restoration are unchanged.
All original function ASTs in the three changed existing test bodies remain
unchanged; only new tests and a framework-owned projection import were added.
No source change was made to task/lifecycle/turns/obligations/edit/check/currentness,
ModelInteraction, Runtime, ToolRunner, WorkCycle, Checkout, CLI or publication owners.

Host admission is required and async; it raises to refuse. Disclosure and Tool
validation do not create authority. The host still authenticates response source,
pending invocation frame and all batch IDs before effects. Existing direct-call
optional IDs are preserved; the shared operation does not invent IDs or infer
a batch. Prompt continues to refuse incomplete or uncorrelated continuation.
Exceptions and cancellation retain their original identity; communication failure
does not mean no effect occurred. One function invocation delegates once, not
exactly once across arbitrary host retries. No new retry, rollback or durability
claim is made. Codex remains an external Agent, not a native model provider.

## Validation and evidence

Original source blobs were restored only at their canonical paths for an independent
148-test original-consumer run; all passed in 159.42 pytest seconds, command exit 0.
The owned implementation delta was restored in finally. An earlier run crossed
source edits and is explicitly invalidated, not credited. Its one transient
failure does not establish an original production defect. The first attempted
baseline used a nonexistent selector; that harness error is retained.

The first framework run had 26 passes and one Windows-newline harness failure;
the independent fixed check now writes literal output bytes. Subsequent 145
composition controls and all 13 separately retained host schedules passed. The
broad focused run passed 1063 tests. Supported Ruff, formatting, strict mypy,
layout, exact-version/old-oracle, JSON/JSONL, links, Intake and whitespace checks
passed. An overbroad root Ruff check entered frozen historical builders, and its
formatter crashed there; those failures are retained separately. The successful
scope is exactly the previously used supported-source profile, with no historical
rewrite or threshold/exclusion change. The evidence helper's initial AST check
also needed explicit UTF-8, not ambient Windows text decoding.

The unchanged complete protected command on committed `31627dcae17fa1e429fbc4c1f3d31941ef5803a7` passed
3315 tests with 2 optional live skips and 100% configured `devtools`
branch coverage, command exit 0, elapsed 1132.597032 seconds. The gate's exact
selectors, source/test/configuration Git blobs and physical SHA-256 inputs,
environment versions, timestamps, command outputs and durations are recorded in
the linked receipt. The configured coverage claim does not extend to every
application branch, all environments, live model effectiveness or complete
transitive toolchain/HEAD-dependent validation closure. No live inference,
model/Docker service, scientific controller or frozen evaluation was executed.

## Canonical disposition and remaining migration

The existing 39c6663a proposal receives one append-only bounded delivered ADVISORY;
its administrative PENDING_REVIEW and broader cohesion obligations remain open.
B-0035/B-0043 get delivered-slice evidence without status/maturity changes or
generic Agent approval. Original Qwen frozen records and previous overlays remain
historical; changed Git blobs receive a separate explicit-depth maintenance overlay.
All 13 original forensic files, 903 RI ledger rows and starting historical refs
are preserved. The 188 historical RI-version obligations remain separate.

The shared composition works independently of Qwen, but exact scoped source/range
acquisition, active native disclosure and fixed validation-plan/currentness bundles
still require application owners. The generic existing read and Command Tools do
not establish those stronger contracts. Complete goal/repair/candidate/terminal
workflow remains application-owned; this is not yet a framework coding Agent.

Next recommend the already proposed increment 2: reusable source acquisition and
fixed-check services, adapting existing Context/RI/Planning and Tools over managed
Commands. Specify neutral scope/snapshot/Command inputs, preserve exact source
freshness and focused-versus-protected validation claims, and connect Qwen plus a
genuinely independent host (and the actual local-closeout consumer where applicable).
Keep task/oracle/journal/publication policy at the host. Approve those contract
changes before implementation; no increment 2 is begun here. A bounded coding
Agent under Agents is later work, not a Runtime loop expansion. Broader A+C,
observation OptionB and durable restart remain unapproved.

See [the public contract](../../src/devtools/agents/docs/model_tools.md) and
[exact receipt](../research/code-audit/native-model-tools-20261027.json).


## Accepted-main closeout controls

All 59 bounded post-main framework/independent-host/actual-Qwen-delegation tests passed on source main `6a331e65ebb5f5c467a32eb694ca7a95056865a1`, with the exact gate input hashes unchanged. A local helper filename collision interrupted evidence assembly; distinct outcome/command files now retain all thirteen fixture schedules. The already-created advisory and maintenance overlay were reused, not duplicated. No production effect was repeated and no product defect is claimed. All starting authored branch/tag refs remain intact; GitHub withdrew its service-owned `refs/pull/47/merge` preview after the normal design merge. That expected service transition is recorded separately from historical ref preservation.
