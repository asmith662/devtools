# First live 64K native maintenance task

Preparation is complete for one genuine bounded engineering episode. Actual
model execution has not yet been authorized at this preparation checkpoint.
This document will retain the observed outcome, including failure if it occurs.

## Reviewed task and provenance

The operator approved proposal
`f3f3068e-cb95-4718-9def-ba432b1f3ea4` through an actual default-No decision.
Existing Intake APIs reviewed and published
[B-0050](../backlog/items/B-0050-repair-local-namespace-import-interference-with-module-facade-reexports-b-0049-follow-up.md),
with review SHA256
`acfa427db8fd3ab7a40912216b5e66307011dd63276b575da8272101b726dfcd`.
This is a related child of B-0049, not a new independent copy of its broader
obligation. Intake requires a new related proposal after terminal review, and
WorkCycle has one assignment slot per canonical item. The original B-0049
dispatch and its authentic failed trajectory remain unchanged and consumed.

Repair only `src/devtools/context/python/imports/members.py`: unrelated
function-local, async-function-local and class-local imports must not invalidate
a valid module-level reexport. Preserve exact target/provenance, conservative
module conditional/try/star imports, genuine competing bindings, aliases and
the maintained pattern/handler guards. No general scope evaluator is proposed.
The baseline source SHA256 is
`3f9924ab29602d2b1c1b11712a18cf94aca1a7ee8edf4f7515c462dbc046f6ed`.

The [fresh preflight](code-audit/live-native64-20261101/preflight.json) on
synchronized main `97e8e2fad933afcddf87b4da482eb5d511646a85` reproduced three
public failures and 58 passing public/maintained cases. Independent unchanged
private acceptance reproduced six failures and twelve passing controls. These
remain failed baseline observations, not a passing validation. The oracle was
authored before any acting response and reused unchanged; no reference repair
was authored. Its implementation and diagnostics are excluded from worker and
reviewer Context. Host-only task/assignment archives must not be added to model
read scope merely because they are preserved as audit evidence.

## Frozen operating scope

The running Qwen3.8-27B UD-IQ4_XS provider is the same pinned artifact/image and
container as the [persistent adoption](../development/qwen-persistent-profile.md).
Health and `/slots` actually report one idle 65,536-token slot. No restart,
serving change, download or capacity benchmark was performed. Actual unchanged
server defaults are temperature 1.0, top-p approximately 0.95, top-k 20,
min-p approximately 0.05 and presence penalty 0. Native portable requests disable
thinking and cap output at 2,048 tokens; they do not override provider sampling.
This is an explicitly disclosed profile limitation, not an optimality claim.
The earlier neutral qualification proved only 128-token generation.

The [final prospective task](code-audit/live-native64-20261101/task.json) and
[preparation identity](code-audit/live-native64-20261101/preparation.json) bind:

- Eight model calls, six acquisitions, three proposals including at most two
  repairs; 120 seconds per call and 900 seconds coding/private-acceptance time.
- `native-context-v1`: 65,536 provider tokens, 62,464 input tokens, 2,048 output
  reservation and 1,024 safety tokens; actual complete-template measurement.
- 128 KiB complete serialized requests; 64 KiB source disclosures; unchanged
  32 KiB editable/resulting source; deterministic 112 KiB trigger toward 96 KiB,
  with warnings at 96 KiB.
- 960 KiB native capture plus at most 64 KiB supporting provider/resource facts,
  within a combined 1 MiB episode envelope. No hidden unbounded transcript.
- Existing `read_source`, `replace_source`, `validate_candidate`, `find_source`
  and `read_source_unit`; no shell, invented checks or publication Tools.
- Complete current editable-file acquisition before editing, as required by the
  existing whole-resource obligation; smaller dependency/test ranges are allowed.

Public managed checks invoke the exact temporary public diagnostic and maintained
`tests/context/python/imports/test_members.py`, without global coverage. The
temporary diagnostic is materialized only from its authenticated frozen text.
Private acceptance runs separately before archival/restoration and is never fed
back as private diagnostics. All acting work must use the existing native
WorkCycle and shared coding process. A provider error or uncertain effect cannot
authorize a replay. Source custody and Checkout must restore known baseline
bytes and release ownership; unknown effects remain explicitly blocked.

## Review and integration boundary

Only a lawful reviewable candidate can enter the existing native reviewer. A
fresh independent adapter/session receives authenticated task, baseline,
candidate/diff, public evidence, qualified private outcome and custody facts.
It receives no coder conversation/reasoning, oracle implementation or reference
repair. Same model weights do not establish independence of model judgment.
Review requires its own exact-subject approval; a favorable model recommendation
still requires a separate trusted host disposition. Existing integration planning
is read-only and grants no installation, publication or backlog closeout.

## Proportionate verification

The maintained native Context/provider contract selection passed 150 tests.
The public baseline command ran 61 cases: three expected behavioral failures and
58 passes, retained verbatim in its local authenticated receipt. No production
executable input changed. After removing the owned temporary public-test
materialization, all 1,059 protected input identities match the existing successful
protected candidate. No fresh comprehensive pass is asserted or required solely
to record this live assessment. Any actual framework correction would require
separate provenance, focused repair and its mandatory final protected gate.

Inspector remains independently registered on `feat/agent-inspector`; its active
session and source were not modified. B-0035, B-0048/B-0049 history, forensic
evidence, RI ledgers, historical refs and outstanding obligations are preserved.
