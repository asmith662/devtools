# Investigation-to-implementation transition

## Diagnosis and ownership decision before production changes

Baseline `8d56601c680a245bb4d1ce6f0ef8675ff8ee1903` preserves the
[failed task-navigation attempt](../../experiments/local_maintenance_task_navigation/REPORT.md).
All ten requests and normalized responses were inspected, including complete
schemas, settings, source feedback and projection records. Each had only user,
assistant and native Tool roles: no hidden system/developer instruction was sent
by the application. The first user message was the unchanged engineering objective;
the second was qualified candidate metadata. Tools included read, precise unit
read, search, exact replacement, fixed validation and the fixed repository procedure.

The adapter sent no forced Tool choice, JSON format or grammar. It set
`enable_thinking=false`, maximum output 4,096, temperature 0.7, top_p 0.8, top_k 20,
min_p 0 and presence_penalty 1.5. All responses terminated as native Tool calls;
none hit output limit. Only the first two contained ordinary assistant text.
`RepositoryCodingHost.classify` accepts plain text as stop, and the shared process
does not dispatch another read unless a normalized model call selects it. A stop
does not certify validation. No deterministic retry or forced read was found.

The pinned llama.cpp b10868 [request parser](https://github.com/ggml-org/llama.cpp/blob/b10868/tools/server/server-common.cpp)
defaults missing `tool_choice` to auto. Its [response accounting](https://github.com/ggml-org/llama.cpp/blob/b10868/tools/server/server-task.cpp)
maps generated-token count to completion_tokens; the local adapter maps that to
output_tokens. These tagged source URLs were inspected; a tag is not an immutable
commit proof. The 779 reported output tokens include the serialized generated
completion, not an independent measure of reasoning quality. Thinking was explicitly
disabled and no separate reasoning content/count was observed. No provider defect
or evidence justifying a provider-setting change was established.

| Hypothesis | Supporting evidence | Limit / counterevidence | Cheap discriminator |
| --- | --- | --- | --- |
| Context eviction | Each of seven repeated ranges was absent from its selecting Prompt; all three chunks exceeded the host byte cap | Repetition is model-selected, not a proved causal consequence; precise alternatives existed | Present a bounded exact method/contract set and inspect the next decision |
| Tool interaction | Read feedback advertises remaining range/continuation; no repeat/active-history facts were visible | Calls were free, edits/checks/plain stop were permitted | Expose truthful acquisition and active-source status without forcing an action |
| Navigation relevance | Initial view ranked file/class and an irrelevant compaction method; worker selected the file | Correct file was found immediately; exact method search remained available | Measure selectable method units, not another retrieval algorithm |
| Task difficulty | No implementation hypothesis or proposal despite multiple reads | No trial supplied the complete coherent small working set; output brevity alone is not evidence of inability | One read-only four-call diagnostic with public contracts and specific action/blocker scoring |

B-0035 requires complete authorized metadata, current repository/snapshot/content
identities, UTF-8 byte sizes, editable flags, no source credit, no duplicates,
refresh after application, valid native continuation and complete-request budgeting.
An informed implementation must understand constructor state, request assembly,
preparation/projection, applied-source refresh, SourceScope and the public focused
metadata/budget assertions. Withheld or reference implementations are unnecessary.

Existing RI symbol units and Context materialization measured: entire file 31,897
source bytes / complete request 46,030; constructor/build_request/prepare/apply 11,378
source bytes / request 23,977; those methods plus SourceScope and public focused
assertions 15,141 source bytes / request 29,755. Those first exploratory measurements
used a 32,768-byte materialization ceiling; they do not authorize a whole-file Tool
read. The maintained reconstruction uses the actual 8,192-byte per-read ceiling,
fits each of seven units completely, and measures **29,748** complete request bytes
(seven fewer metadata digits). Frozen broad chunks required **40,312** bytes.
These are host-selected source measurements, not autonomous discovery or edit
authority. Source scopes and schema/JSON overhead are included. The existing host
had 871 resulting-file bytes of margin; the adjacent navigation owner had 19,724.
A small composition change using existing owners is plausible, but a smaller
Prompt does not make arbitrary growth admissible. No B-0035 solution is supplied
or implemented here and neither limit is raised.

The selected minimum shared correction is an **opt-in active-source status
annotation in the existing projection owner**. It derives prior exact acquisitions,
previous active availability and the actual selected working set from existing
source bindings; no extra history or source identity is introduced. It clarifies
that continuation offsets are options, and that the model may refine, acquire,
propose, validate or explicitly stop with a blocker. It neither chooses an edit
nor forces progress. Native messages, original facts and exact-source authority
remain distinct. Complete-request accounting must include the annotation itself;
failure to fit remains explicit. Default projection remains unchanged.

The separately frozen live diagnostic will supply a small exact working set as
explicit host disclosures, never fabricated model Tool calls. It will use the
same genuine objective, at most four real local calls, no source mutation and no
full maintenance trial. Success requires a concrete evidence-grounded next action
or missing obligation; smaller Context or fewer reads alone do not pass. This is
a diagnostic of plausibility, not a measurement of completed maintenance or the
causal effect of the annotation alone.

## Delivered mechanism and compatibility

`ProjectionPolicy.report_source_state` defaults to false. When selected by the
host, `project_request` appends one ephemeral user-role `active_source_status`
message. It lists at most four exact current ranges, explicitly flags a partial
list, counts omitted current disclosure records and describes one disclosure in
the latest current record. Its same-range count refers to retained disclosures,
not a fabricated number of Tool executions. Host disclosures and admitted
after-images can also be disclosure records. A separate boolean says whether one
previously active disclosure covered that range; false is not proof that a union
of separate previous ranges lacked it. Snapshot/content identity and half-open
Unicode offsets remain explicit. Stale records are excluded.

The coding host supplies its existing `active_disclosures` to both deterministic
and semantic projection. No new history list, Tool, source identity, inference
setting or mutable policy state was introduced. The status does not infer why
a model chose a read. Original native calls/results stay unchanged and correctly
correlated. Exact source still comes only from authenticated Context materialization;
metadata, a prior acquisition and the status itself cannot authorize an edit.

The complete annotation is counted before pressure selection, including during
partial-disclosure affordability searches. Selected partial ranges and reported
active ranges agree. A protected minimum that cannot fit still fails before
model entry. Failed projection leaves prior active availability intact. Optional
semantic summaries retain their existing validation and fallback; the annotation
does not trigger auxiliary inference. Legacy Qwen behavior remains unchanged
unless a neutral host explicitly selects this option; no complete legacy
continuation migration is claimed.

Maintained tests use the actual neutral host, native composition, ToolRunner,
source admission, managed fixed checks and custody. They distinguish successful
scripted edit/check, deliberate continued rereading, plain blocker, eviction and
redisclosure, bounded status rows, partial text, changed snapshot, insufficient
capacity and immutable historical reconstruction. Scripted behavior demonstrates
interface correctness, not local-model competence.

The read-only diagnostic uses the existing nonempty `CodingObjective` custody
surface for compatibility, while removing edit/check descriptors, rejecting those
calls before dispatch and supplying an effect collaborator that always refuses.
Its restoration collaborator only verifies unchanged bytes. This does not turn
source admission into an OS sandbox or broaden the production objective contract.
Host-preloaded source is recorded as host disclosure through `ScopedSourceTool`,
never as a model-selected native call. Public focused assertions are in scope;
withheld acceptance and reference implementations are not.

## Protected implementation evidence

Final executable commit `c2bc06f4f604c6ccb87279f6315bfa87b59ce6fa` passed **3899 tests**,
2 optional skips and 100% configured production line/branch coverage through
`uv run python scripts/validate_development.py` in 1427.358 seconds.
All 1188 captured physical inputs were unchanged. Supported Ruff,
formatter, strict mypy and layout checks passed on that commit. Baseline focused
characterization passed 1,896 tests; broader changed-consumer validation passed
1,905; the final narrow compatibility suite passed 153. A superseded gate was
explicitly stopped before a disabled-semantic-trigger compatibility correction;
its exit 1 is retained, not reported as a passing gate or test assertion failure.
[Machine-readable evidence](../research/code-audit/investigation-transition-20261029.json)
records identities, commands, timing, versions and physical inputs. Final physical
repository.py is 32,031 bytes, leaving 737 bytes under the unchanged source ceiling.
That small margin remains a separate maintenance risk.
