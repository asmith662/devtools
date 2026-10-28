# Case 0001: stock delivery replay correctness

## Frozen question and authority

Can the existing model-independent coding process complete one fresh nontrivial
Python repair with a real configured local model? The maintainer explicitly
authorized one task and necessary local inference, not cloud fallback, downloads,
new providers, production edits by the model or repeated task selection.

Canonical baseline: `8f1466ec0f7b71984a63cb6b0512d075b8e282a4`.
Authored task Git baseline: `e17f0ecd500f07a07b095193e56ba6399b08c90e`.
Task digest: `f1720633ff5b1fc9f1592458e757f8c4aa8c7128ea85498d95c58d8ec0612605`.
Source snapshot: `70b559e66aab2c237cd2e67d40cda54f44193bdf9d3778e51bc6a354f84073b9`.
The [freeze](freeze.json) binds objective, initial files, experimental host,
source snapshot, oracles, model settings and limits before inference. No intended
patch was given to the model, and Codex supplied no corrective implementation.

## Task and independent grading

The package has event, key, projection and reporting modules. Only projection.py
is editable; the other modules define actual interacting contracts or an
irrelevant reporting candidate. The task requires per-warehouse replay identity,
canonical key compatibility, exact opaque event IDs, conflict rejection,
single-pass iterable support, independent output ownership and valid zero/negative
quantities. Initial maps and unrelated entries must survive success and failure.

The frozen focused oracle has five tests. The independently specified held-out
oracle has eight tests, including interleaved replays, Unicode canonicalization,
opaque case/space IDs, late conflicts, empty independent results and per-call
replay state. Before inference, focused grading ran all five tests with three
assertion failures; held-out grading ran all eight with five assertion failures.
Neither was an import, fixture or syntax failure. Tests and held-out source were
outside the model's read/edit scope. Grading was not changed after output.

## Selected model and execution envelope

The already-running `devtools-qwen38-llama-cpp` service was reused at
`http://127.0.0.1:8080`, alias `qwen38-local`, container
`61a6a7f977910ce5f7c03e6f1d33f19c51e6e7ea1cc1ae065941183cced85348`.
Profile fingerprint:
`03758e5bc51c9aa9fbdd1850c1f25541d1eba76a80a54b74598886d882264bf1`.
The mounted Qwen3.8-27B UD-IQ4_XS GGUF was streamed through the native host path
and matched pinned SHA-256
`40fac4050e940397dbf13087afd50f4734a11805bf9d65ef8ddd7483470e6199`.
The pinned serving image, artifact revision, read-only mount, 32K context and
template hash are recorded in the freeze. No service restart, model download,
conversion or alternative model occurred. The service was READY afterward.

Limits were fixed: five model requests, two edit proposals, eight acquisition
actions, one available repair, 180 seconds per request and a 900-second outer
managed process ceiling. Each request permits at most 4,096 generated tokens;
input template/tokenizer measurement must be at most 28,160 tokens, reserving
output and margin inside 32,768. Prompt bytes, disclosure and edit bounds remain
explicit and at or below existing worker limits. Thinking was disabled and the
existing instruct sampling settings were fixed before entry. Nothing was tuned
after observing model output.

## Real lifecycle and capability adoption

The host composes `RepositoryCodingHost` and calls the actual
`run_coding_agent`. Model invocation is the existing `LlamaCppInteraction`, with
provider-specific measurement/configuration outside Agents. RI observation,
corpus/index ownership, SourceScope and ScopedSourceTool materialize actual
current regions. Model/Tool composition and ToolRunner preserve host admission
and native IDs. The existing exact replacement, source custody, fixed checks,
Resources writes/Commands and terminal reconciliation do the work.

Four native operations were offered: read_source, replace_source,
validate_candidate and inspect_and_validate_change. Experiment composition adds
the last operation through the existing CodingHost seam; it introduces no second
coding/repair loop. Model-controlled arbitrary shell commands, external paths,
Git mutation and publication were unavailable.

| Stage | Observed fact |
| --- | --- |
| Request 1 | Three native read_source calls: events.py `[0,477)`, keys.py `[0,200)`, projection.py `[0,563)` |
| Source feedback | Exact text, content identity and frozen snapshot retained under each original native call ID |
| Request 2 | All three read results present in the actual input; one replace_source call with an exact acquired anchor |
| Admission/effect | Required current full-source witnesses satisfied; one permitted edit batch applied and installed bytes verified |
| Host validation | InspectAndValidateTool inspected authorized Git state and ran the immutable focused check through FixedCheckTool/ToolRunner |
| Focused result | All five tests passed; currentness remained known |
| Feedback | Actual passing diagnostics/current source appended under the edit ID; no subsequent model call consumed them |
| Completion | Candidate archived; known original source restored; worker validated, completed and accepted |
| Independent grading | Archived candidate passed all eight held-out tests and a fresh five-test focused invocation |

The model did not request either validation operation. Procedure use was
deterministic host validation, not voluntary Tool selection. Source reads were
model-requested and their feedback was consumed. The internal after-image Context
materialization was host-driven. No validation-feedback repair was necessary;
real repair effectiveness remains unmeasured here.

## Usage, effects and capture strength

There were two real inference entries and normalized responses, one edit proposal,
three acquisition actions and one applied source batch. Provider-reported input
tokens were 913 and 1,884; output tokens 158 and 363. Totals: 2,797 input,
521 output and 3,318 total. Server template counts agreed with reported input.
Cached-input, cache-write and reasoning-token counts are unknown, not zero.

Provider request elapsed times were 38.185245 and 16.103570 seconds. The coding
worker took 55.298485 seconds including completion custody. The outer controlled
evaluation, including retained grading/reporting, took 56.236926 seconds.
Preparation/model hashing and later repository validation are separate timings.
No automatic retry, repeated effect or unknown installed source was observed.
The original task Git worktree was clean after restoration.

Seventeen selected command observations and deterministic pattern summaries are
retained in outcome.json. They contain normalized families, roles, provenance and
known results, not arbitrary stdout, source or environment analytics. Returned
fixed-check results establish completion; this does not prove a complete global
Command event feed or durable Evidence integration. Bounded authored test logs
and model inputs/outputs are retained separately as experimental evidence.
No personal conversation logs, credentials or unrestricted environment capture
were used. Model narrative is not treated as access to its internal reasoning.

## Setup diagnosis and framework findings

Before the freeze, the experimental script needed the repository root on its
import path to read existing profile data. An attempted diagnostic one-liner also
had a syntax error. Neither entered inference or constituted a framework defect.
A full GGUF checksum inside Docker exceeded a 120-second inspection timeout; the
client timeout left its read-only hash process running. That exact owned process
was cancelled, the server was preserved, and hashing the same read-only mounted
artifact through the native host cache completed and matched. These adjustments
preceded the frozen task and primary run; no corrected follow-up is counted as
the original attempt.

No production integration blocker or correctness defect was demonstrated. The
existing CodingHost seam was sufficient to compose the command procedure, though
its concrete default RepositoryCodingHost offers only its original three native
operations and this experiment supplies explicit selection/feedback wiring.
No production source/test/configuration correction was necessary. There is no
claim that these host adapters are a new reusable capability or that their
publication promotes them into framework ownership.

## Limits and next step

Tool scope constrains admitted file writes; host-fixed Python checks are not an
OS sandbox for adversarial candidate code. This candidate added no external I/O,
and the canonical tracked tree and forensic bytes remained unchanged. Broader
untrusted-code confinement is not established by a scoped Tool or this sample.

This is one successful, fresh small-task sample, with a host-authored objective,
four-path manifest, one editable module and explicit readiness witnesses. It does
not test autonomous large-repository discovery, host-independent planning,
multi-file repair, live failure recovery, provider interchangeability or repeated
effect recovery. Prior deterministic regressions cover some of those mechanics;
they are not substituted for a real model in this result.

The next high-leverage evaluation is one separately authorized harder task that
requires source-discovery choices and, if naturally needed, actual failed-check
feedback consumption and bounded repair. Keep deterministic host validation;
do not add infrastructure or claim model-selected procedure use merely to improve
the narrative. Any shared host Tool-composition refinement needs its own concrete
contract and real consumers. A+C, observation Option B, durable recovery and the
188 historical RI-version obligations remain open. No successor experiment was
launched here.
