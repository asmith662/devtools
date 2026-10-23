# Representative development lifecycle audit plan

## Disposition

Source selection and bounded audit plan, 2026-10-23, against feature
`177098f4edd3dd7ea1b6bd889e1a1b1d5074a5fd`. This is the next research assignment,
not an implemented observer, new execution authority or completed causal audit.
The [finite reconciliation charter](../development/reconciliation.md) and
[mechanism comparison](agent-harness-mechanism-review.md#deepseek-harness-and-aider-source-and-test-audit-2026-10-23)
govern its scope. B-0023/B-0011 retain observability/Evidence pressure;
B-0028/B-0034 retain durable-state/uncertain-effect pressure.

The [evidence metadata](agent-harness-mechanism-evidence-20261023.json), under
`deepseek_aider_checkpoint.audit_flow_inputs`, fingerprints 21 actual input files.
They were located/read and selected joins checked; the full historical
request-to-publication timeline has not been reconstructed. Ignored `.local`
paths below are custody references to existing originals, not newly copied
archives or portable public downloads. Reauthenticate their recorded hashes at
the beginning of the next audit. A missing original must remain unavailable;
never regenerate it by replay and call it historical evidence.

## Five selected real flows

| Flow and authoritative entry | Existing original receipts and correlation fields | Next audit question / important limit |
| --- | --- | --- |
| Successful Qwen implementation and feature publication: [Environment13](../../apps/qwen/evaluation/environment-13/README.md), [results](../../apps/qwen/evaluation/environment-13/results.json) | `.local/qwen-coding-worker/environment-13/devtools-environment/`: `result.json`, turn request/response/stage/tools/capacity files, `supervisory-review.json`, `closeout.json`. Result SHA-256 `c1630cc4df16533c96e9bc84400d008dc81fe8e10c6b7f09828ca53d78c3de7f` equals closeout result reference. Task definition/oracle hashes, turn numbers, provider call IDs, source versions, admitted candidates and review subject join to publication `b81891ceeafa88d21741ef9b69155180a260e75f`. | Fourteen genuine calls and five admitted proposals, accepted model implementation with feedback corrections. Confirm each edge's strength and missing measurement; do not infer native check_changes, which was delivered later. No Pi diagnostic outcome is substituted for this Devtools condition. |
| Failed Qwen edits and incomplete validation: [New-module22](../../apps/qwen/evaluation/new-module-22/README.md), [results](../../apps/qwen/evaluation/new-module-22/results.json) | `.local/qwen-coding-worker/new-module-22/live/result.json`, `provider-response-*.json`, `turn-*/{request,response,stage,tools}.json`, admitted candidate/validation records. Start with turn06 stage: request/response SHA-256, tool_calls, proposal_attempted/proposal_valid, source_before and refusal disposition. Task `0ee51c4604c795d96e75b927273dfa6f38a572a65e7d8469edbb4775f9b2c7ab`, oracle `e60d40dfa5faf6143703cc8d103db8107a0abdd42475abd341b14d0aa17a9e93`. | Four refusals/two admitted transactions, missing public integration; neither check_changes nor is_current invoked by model. Join bad owner/anchor arguments to refusal, unchanged sibling state and next feedback. Later Codex fallback is a separate implementation. Do not call quality improvement behavioral acceptance. |
| Completed Codex WorkCycle publication: [Map-source27](../../apps/qwen/evaluation/map-source-27/README.md), [results](../../apps/qwen/evaluation/map-source-27/results.json) | `.local/qwen-coding-worker/map-source-27/codex-delivery/closeout.json`: result `09a5ef2a90f8cf0630f70ed785b85dcc303f0cb911609c3d7476201ca1a28daf`, exact candidate hashes, implementation_by/supervision_by Codex, validation_inputs, review and commit `0bdc8507601dcf65a742ab3ce5cca4bb8e6f590a`. `host-change-check.json`, `host-current-installed.json`, `host-stale-restored.json` preserve actual source-bound checks/currentness. Checkout history `ec03cb4c0a4f821366ebed9e2daa82396c268accbbcfca6499147f1c6a904e5a.json` names the same closeout result. | Authenticate validation inputs and subject before treating gate logs as exact-tree evidence. Host currentness was true installed and false restored; old report status PASS stays historical while readiness becomes false. These supervisor calls are not Qwen Tool use or authorization from freshness. |
| Real stopped-owner source recovery: [Map-disclosure26](../../apps/qwen/evaluation/map-disclosure-26/README.md), [results](../../apps/qwen/evaluation/map-disclosure-26/results.json) | `.local/qwen-coding-worker/map-disclosure-26/live/result.json` SHA-256 `50aca50e491c797bf8ff63fe7bf66dd57eac32e659cf47ec572e700e5feb43a1`; `recovery-authentication.json`; `failed-installed-source.txt`. Actual SHA-256 `4be84c11291b90bd1fbeb3d9d302957a510e7e4858ee8011a24072b80b24824f` versus admitted `8f1a69b4367337656a5cd0f97d2033531496889bc5ad4ea5f6ed67f4ce2faa86`. Sealed Checkout history `037716b374f7ad457648ddb0753355772b919ea6ce4a9e32c7e547a6ed45eab9.json` binds operation `local-evaluation:c5b9d451b27f04ed39b97df80dbac3dd002e83400deb3461270f632e310665a1`, original PID, branch/root/base, admitted file fingerprints, final return HEAD and seal. | Original CLEANUP_RECONCILIATION_REQUIRED/source_restored=false remains true of the failed receipt. Recovery separately reconciled one unproposed LF then used existing restoration. Inspect stopped-process evidence/authorization and recovery chronology; a sealed finish receipt alone does not prove the process-stop step or external-effect rollback. This is a genuine recovery case, not a scripted cancellation fixture. |
| Genuine source navigation: Map-source27's original live session [record](../../apps/qwen/evaluation/map-source-27/README.md#genuine-qwen-attempt--failed-before-editing) | `.local/qwen-coding-worker/map-source-27/live/turn-06/tools.json` contains actual `expand_source`; companion `stage.json` binds request/response digests and timing. `call.provider_call_id` correlates with request/response native messages; result has source unit/parent/version/span and observation provenance. Environment13 turn01 also shows actual `inspect_source`, edit_ref R1 and observation_call_id `5dT8JtsooVYsXQt5Qv62VHIfIB4u6N8g`. | Trace disclosed bytes to source eligibility and later source invalidation. This is ordinary native source navigation; do not call it adoption of the subsequently added map-to-source adapter. Engineering28's scripted map qualification and absent live map invocation remain separate. |

## Owners and exact audit edges

1. **Objective/task → provider request:** `apps/qwen/tasks.py`,
   `development_task.py`, `coding_loop.py`; bind task definition/oracle/profile,
   baseline/source/check plan, turn/request SHA and raw provider messages.
   Determine whether task identity is identical, linked or absent at each edge.
2. **Provider → normalized model Evidence:**
   `models/interaction/providers/llama_cpp.py`,
   `observability/evidence/model_interaction.py`. Inspect whether the particular
   historical invocation installed a completion observer before expecting a
   ModelInteractionId/EvidenceId. Provider failure before normalization and
   observer failure afterward have different missing-record semantics.
3. **Native call → Tool → source/edit:** `tools/execution.py`, application
   ContextTools/CodingCommands and `edits.py`. Follow call IDs and native message
   pairs, exact observed versions/absence, component diagnostics and candidate
   hashes. A ToolRunner return is not proof of an accepted edit or publication.
4. **Candidate → validation → freshness:** `commands.py`, `change_checks.py`;
   authenticate saved report/evidence digest, checked versus after candidate,
   plan/input/Git hashes and independent statuses. Distinguish cancellation,
   unavailable checks and incomplete evidence from ordinary failing behavior.
5. **Checkout → review → publication:** `scripts/backlog/checkout.py`,
   `integration/local.py`, `work.py`. Verify owner root/branch/revision/PID,
   restoration, exact candidate/review subject, protected-gate inputs, commit and
   recorded remote. Do not redispatch or grant authority during inspection.

Narrow Runtime/InteractionAttempt may not participate in these application flows.
Its terminal Evidence is a separate representative source-level contract,
corroborated by `tests/execution/test_runtime.py`, not a missing span that may be
invented. Command events are live, bounded and potentially dropped; raw stdout/
stderr/evidence references are separate. InvocationMeasurement and usage windows
are measured records with availability/provenance, not guaranteed billing.

## Required report from the next audit

Produce one timeline/join table per flow with exact original path/hash, producer,
consumer, correlation keys, timestamps/clock boundaries, source/plan identity,
effect/authority, capture policy, missing events and confidence. Mark edges as
direct authenticated reference, deterministically derived association,
chronological inference or unknown. Keep live instrumentation distinct from
immutable Evidence and storage durability; do not create a universal run ID to
paper over absent joins.

Inspect relevant existing deterministic tests for failure, cancellation, partial
batches, stale checks and recovery. Do not reexecute historical models or
production publication. Preserve originals and the 13 forensics. Any missing
stop confirmation, remote receipt, provider usage or capture decision becomes an
explicit gap; no synthesized historical record. Route qualified gaps through
existing B-0023/B-0011/B-0028/B-0034 and pending proposals without approval or
implementation. Follow with bounded destination-adoption and custody audits,
then a comprehensive successor-session handoff. This plan does not launch them.
