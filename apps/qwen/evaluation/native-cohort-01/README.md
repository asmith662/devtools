# Native Qwen coding cohort 01

**FROZEN / PENDING_AUTHORITY_AND_BACKLOG_REVIEW. No model attempts yet.**
This initial engineering cohort is not a representative proof of Codex parity.
It uses existing `CodingTask`, native Tools, WorkCycle and receipt contracts.

## Cases and independent acceptance

Source baseline: `e02c9044311036883134df955438b1b809db353b`.
`manifest.json` binds task/oracle/file hashes and pending proposal identities.
The adjacent Git attributes preserve exact LF JSON bytes across checkouts.

| Case | Split | Reproduced obligation | Read resources | One edit target |
| --- | --- | --- | --- | --- |
| duration-boundary | development | Negative sub-resolution factory inputs round to zero instead of rejecting | 6 | `src/devtools/core/time/models/duration.py` |
| csv-dialect | development | NONNUMERIC parsing violates the documented exact string-cell contract | 8 | `src/devtools/resources/filesystem/codecs/csv.py` |
| source-physical-spans | held-out | Unicode separators corrupt Python source-symbol/window coordinates | 7 | `src/devtools/context/retrieval/source/representation.py` |

Each JSON is decoded by existing `scripts.backlog.work.task_from_dict`. No new
executor/task schema exists. Objectives do not supply implementations. Initial
requests disclose boundaries, not full files; Qwen must acquire source through
native Tools. A one-file edit target necessarily identifies the authorized file:
this measures bounded investigation/helper selection, not unrestricted file
localization. Development corpora exclude held-out resources.

The duration oracle checks negative inputs across factories, zero, positive
rounding and arithmetic. CSV checks lexical cell spelling, custom delimiters,
parse/decode consistency, serialization round trips and malformed input. Source
acceptance covers 15 separator/newline combinations, decorated async spans,
window boundaries/coverage and source search. Existing listed regression tests
must pass too. On unchanged Python 3.14.3 source, all three oracles failed their
intended assertions while **83 existing regression/task-selection tests passed**.
Private baseline output: `.local/qwen-coding-worker/native-cohort-01/`.

These are real defects, not inserted bugs. Historical Markdown, function
materialization and B-0048 object-model tasks are excluded. The held-out source
representation case is related to historical separator semantics, but targets
new retrieval integration. Do not claim independent language diversity or use
its model feedback to tune development improvements before its evaluation.

## Standing policy: inactive

`policy.proposed.json` SHA-256:
`e5061f9d294c0fd503888fef6f658050e79858fae3d2dd2d6987eb05423ac5da`.
It names 15 exact sources, six exact test resources and three host-oracle hashes;
bug/refactor categories only. It is compatible with all three task definitions
under pure schema/scope checks. That is not genuine exact-assignment admission.
It supersedes the previous narrow JSON-list policy as the proposed initial
cohort scope, without changing or activating that policy or historical grants.

Per task: ten total model requests, 4,096 requested output tokens/request,
900 seconds, three proposals. Existing worker bounds also enforce eight reads,
300 seconds/call, 32K Context and thinking off. Cumulative reservation: three
tasks, 30 requests, 122,880 output tokens and 2,700 seconds. Output/time settings
are request/host bounds, not provider-runtime guarantees; no cumulative input
or paid-cost ceiling is implied. Existing `qwen38-local` profile, prohibited
effects, Codex review, revocation/expiry and separate integration authority apply.

The standing source allowlist is shared; each exact assignment separately binds
one editable file and its read-only corpus. Reading never expands edit authority.
Consequential worker/governance/provider code and protected publication are not
covered. Future new acceptance code requires compatible genuine authority.

From the canonical root in a genuine PowerShell terminal, inspect the displayed
grant and confirm only if acceptable. This is one grant decision, default No:

```powershell
uv run --python C:/Python314/python.exe python -m scripts.backlog delegation-issue --policy apps/qwen/evaluation/native-cohort-01/policy.proposed.json --reference 'Maintainer standing decision: native Qwen cohort 01 under displayed exact policy; Codex supervision; no protected publication' --expires ([DateTimeOffset]::UtcNow.AddDays(7).ToString('o'))
```

Save the returned SHA. The reference becomes provenance only if adopted by the
actual operator. This command does not dispatch Qwen or approve backlog work.
Do not repeat ambiguous issuance blindly. Existing interactive revocation:
`delegation-revoke <sha> --reference <actual-revocation-decision>`.

## Backlog decisions remain separate

Three proposals remain PENDING_REVIEW, with no duplicates found by Intake:

- Duration: `ea7c18ff-8ca5-46b8-a230-1bfdf92c7f74` (core).
- CSV: `67f7d086-86d9-400f-bfaf-d9bc4df9aea1` (resources).
- Source: `5aa7a431-fd3c-4d46-a3a2-cb4e59e9c28e` (context).

The existing policy cannot delegate their review/promotion. This single-line
PowerShell command uses the existing CLI with **six real default-No decisions**,
stopping on refusal. Do not rerun already completed decisions; reconcile their
actual records. B-0048's approval and consumed slot are untouched.

```powershell
@(@{id='ea7c18ff-8ca5-46b8-a230-1bfdf92c7f74';domain='core'},@{id='67f7d086-86d9-400f-bfaf-d9bc4df9aea1';domain='resources'},@{id='5aa7a431-fd3c-4d46-a3a2-cb4e59e9c28e';domain='context'}) | ForEach-Object { uv run --python C:/Python314/python.exe python -m scripts.backlog review $_.id --decision APPROVED --domain $_.domain --reference 'Maintainer cohort-01 backlog decision under displayed scope' --rationale 'Approve the reproduced one-file maintenance obligation for separately delegated native Qwen implementation and independent acceptance' --duplicates 'No equivalent proposal found by Intake; retain parent B-0009 and original evidence'; if ($LASTEXITCODE -ne 0) { throw 'Review refused; stop and reconcile' }; uv run --python C:/Python314/python.exe python -m scripts.backlog promote $_.id; if ($LASTEXITCODE -ne 0) { throw 'Promotion refused; stop and reconcile' } }
```

One execution grant cannot truthfully replace these independent decisions under
the current contract. No governance expansion was implemented to bypass them.

## Continuation of the same Qwen objective

1. Authenticate the issued current-root grant and actual promoted B-numbers;
   commit the authorized backlog records on the administrative branch.
2. Create ordinary task branches at the pinned baseline, never extra checkouts.
   Use existing `work-prepare <actual-B-number> --target . --branch <feature>
   --task-definition <case.json>`, genuine Codex `work-review APPROVE_ROUTINE`,
   `work-delegate`, `work-execute` and `work-status`. Use actual documented flag
   syntax from `docs/backlog/metadata.md`. Do not reserve a real task as a test.
3. Run the two development tasks with the unchanged native worker first. Retain
   exact requests/responses, correlated Tools, source versions/bytes, usage,
   Context occupancy/omissions, edits/repairs, test feedback, time and supervisor
   interventions. Never reset a failed/ambiguous consumed work slot.
4. Diagnose real failures before changing worker behavior. Validate justified
   improvements with focused checks and one appropriate production gate. Then
   evaluate the held-out task once without oracle/source-hash changes. Any new
   executable binding must be frozen explicitly before dispatch, preserving
   earlier condition identities rather than silently mixing worker revisions.
5. Independently review exact accepted candidates; use separate governed
   integration authority for publication. Do not substitute Codex code or merge
   protected main. Existing dashboard receipts remain the trace contract.

No controlled Codex run or paid-model comparison occurred. Historical tasks are
descriptive references only. A fair paired comparison needs fresh cases, equal
source/acceptance/constraints, isolated solutions and explicit budget/authority.
Codex coordination usage is UNKNOWN; no superiority or savings are established.

Coverage remains limited. The worker requires baseline-oracle failure, excluding
a pure behavior-preserving refactor whose oracle already passes. Multi-file
changes and broad coding generality are also untested. Do not manufacture an
artificial failing behavior or change the worker before its genuine baseline.
This Qwen workstream remains the immediate priority; no transition to Learned
Intelligence, trading, swarming or Memory implementation is recommended here.
