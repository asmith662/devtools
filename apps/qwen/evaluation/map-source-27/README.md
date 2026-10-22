# Map-to-source progressive Context27

## Delivered capability

The existing Context Planning owner now provides:

```python
choose_repository_map_source_disclosure(
    purpose=purpose,
    snapshot=snapshot,
    map_disclosure=orientation,
    symbol=chosen_symbol,
    source_index=admitted_source_index,
)
```

This is an explicit adapter, not a new retriever or planner. The caller already
has a canonical map, an orientation disclosure selecting native map symbols,
and an existing SourceSearchIndex on the same retained snapshot. The index is
an explicit admitted source corpus; it prevents the adapter from acquiring an
unadmitted resource or inventing document/source identities. The chosen symbol
must be represented in that orientation, not merely exist elsewhere in its view.

The immutable RepositoryMapSourceDisclosureOption retains map, symbol, index and
existing RepositorySourceUnit. It reauthenticates canonical map evidence,
selected membership, exact snapshot/index and full source-unit frame. It uses
the existing physical-line UTF-8 offset conversion and source-unit construction,
then delegates exact text materialization/presentation to
SourceSearchDisclosureOption. Materialized native_provenance is (symbol,unit),
preserving exact declaration, source occurrence and resource/content identity.
Option identity binds source purpose, original map choice and exact source/native
selection. Later materialization recomputes the binding and rejects altered
cached slices or incompatible state. No ambient filesystem reads occur.

The source representation is map-selected-exact-source-v1, distinct from the
existing selected-repository-map-metadata-v1 orientation. Other source-search,
map and disclosure identities are unchanged. No durable schema is modified.

The exact span is the RI declaration range: one-based physical lines, zero-based
UTF-8 byte columns, exclusive end. It includes the declaration header/body and
nested content within the range. Preceding decorators outside that RI range are
excluded even when an indexed source-search symbol is decorator-expanded. A
selected class naturally contains methods; a selected method does not expand to
the class, neighboring method or file. Unicode, multiline syntax, LF/CRLF and
unterminated last lines remain exact. Impossible/missing/forged inputs fail with
existing ValueError/DisclosureMaterializationError conventions; no silent
truncation or whole-file fallback exists. Model capacity is still caller-owned.

Context Planning owns selection/representation. RI owns declaration ranges;
Retrieval owns map/source units; retained snapshots own source identity.
ToolRunner/Checkout/native edit authority and WorkCycle publication are unchanged.
Only planning/repository_map.py and its existing package exports have semantic
production changes; source.py and source/representation.py are scoped but unchanged.

## Frozen contract and preparation

Baseline:14daf9cbfae16c023650601441067c6a1567cc08.
Task SHA256:`1b225286fff53e1fb380829efec6020a3fa3e0b9e3feabcd26a1f01f677c0616`.
Oracle SHA256:`0e4decc8e180a146703ed3600619e2a88aa5237dd720b7fae3cd5d7c10bb9e01`.

The public objective states the API, admitted source-index input, true RI range
semantics, decorator distinction, identities, provenance and negative cases.
No private adapter/oracle or patch was disclosed to Qwen. Actual maintained RI,
source-index, planning and ModelRequest fixtures qualify behavior on Python3.14.3.
Expected extraction is independently matched against ast.get_source_segment
from real AST nodes, not arbitrary fabricated byte coordinates. A Unicode endpoint
fixture was strengthened BEFORE inference and requalified. The private runtime-only
positive adapter passes; baseline fails exactly for the missing expansion API.

The existing106 worker/edit/native-loop regressions passed in31.50s, including
the8 real-Git EOF cases added in26, CRLF/Unicode, exact byte application and
rejection/restoration. This is deterministic evidence, not Qwen edit success.

All prospective files remained ignored under .local. Existing ToolRunner/Checkout
readiness authenticated source/plan/Git state, actual fixed checks, installed
currentness/restored staleness and all13 original forensic fingerprints. Only
the expected missing-feature oracle failed. An initial preflight incorrectly
overlapped the host readiness edit and correctly refused nonbaseline bytes;
the final sequential preflight and readiness both passed before inference.
The initial receipts remain in .local. New paths are not required by this task;
absence/new-file byte handling was independently covered by existing regressions.
No scope exemption, new allowlist or Git-integrity relaxation was introduced.

## Genuine Qwen attempt — failed before editing

Unchanged Qwen3.8-27B IQ4_XS,32K,q4 K/V,thinking off. Frozen ceilings:24 genuine
requests,1800 worker seconds,6 proposals,16 components,32 read/check actions;
4096-byte region/8192 aggregate/16384 patch bounds. No eight-response cutoff,
budget extension, source intervention, repeated task treatment or recovery run.

14 genuine requests consumed256,729 input/1,142 output tokens in194.803 worker
seconds (187.877 model seconds,1.299 direct baseline-validation seconds).
25 native dispatches:13 inspect_source,9 search_source,2 lookup_symbol and1
expand_source. It inspected established owners and dependencies, then repeatedly
searched for the absent adapter and helper names rather than proposing changes.
There were ZERO proposals/admissions/refusals, no implementation candidate,
behavioral/quality repair, native check_changes or host native is_current.
The actual provider-bound first request exposes check_changes, is_current,
run_check and replace_source; native-tool-surface.json preserves that evidence.
Availability was genuine, but the model did not reach their implementation/check use.

Request15 was not dispatched. Source-preserving input was47,002 tokens; existing
compact projection reduced it to33,420, and allowed read-only reacquisition to
28,478. With2048 safety,2242 safe generation tokens remained, below the existing
4096 investigation minimum by1854. Original disposition CONTEXT_BUDGET_FAILED,
accepted=false,source_restored=true. This is an investigation-to-implementation
failure followed by a host capacity refusal, not evidence that a produced
implementation failed semantics or the corrected patch boundary failed.

Original live result SHA256:`b6d81c21dbfaa811a89aca1836c49fcaf337c2643ab82761d1d988b0f2a827db`.
Raw requests/responses/source observations/tool correlations/capacity records:
.local/qwen-coding-worker/map-source-27/live/. They and previous26 receipts remain
unchanged. No host-created evaluation artifact contaminated the candidate.
No Context/harness/serving change was made. The corrected EOF path was NOT
exercised by live Qwen because it never edited. No general autonomy improvement
or need for a larger model window is established by this failure alone.

## Separate Codex delivery and progressive demonstration

All semantic source is Codex-authored; Qwen produced no code to transplant.
The original frozen task/oracle did not change after inference. Codex fixed a
trailing-comma style diagnostic in its own candidate, moved the supervisor demo
to a fresh managed interpreter to avoid cached pre-install imports, and corrected
independent fixture list annotations before final validation. These are not
Qwen repairs or oracle revisions. Earlier check logs remain separate.

Real host ToolRunner check_changes passes all five checks. Host is_current is
true with that exact candidate installed and false after Checkout restoration.
These are supervisor invocations, never credited to the model.

The fresh-interpreter [progressive demonstration](progressive-context.json)
selects Worker.run and calculate for metadata orientation, then expands only
Worker.run to77 exact UTF-8 bytes (76 characters) of CRLF/Unicode source.
The RI span is[3:4,5:29), using one-based lines/UTF-8 columns; source character
slice[35,111). It starts at async def, omits its preceding decorator and excludes
unrelated method bodies, calculate's body and the unselected private resource.
The native declaration, source occurrence, original content identity and map
support remain in the option/item provenance. Orientation plus source are planned,
materialized, rendered and assembled after the original unchanged task.
Metadata text773 bytes, exact-source item408 bytes, assembled request1988 bytes.
No comparative token/cost or automatic retrieval-performance claim is made.
The [exact assembled text](progressive-context.txt) preserves source boundaries.
Its narrow Git attribute preserves physical CRLF bytes inside the LF-framed
request; the JSON source_text also retains those exact line endings.
A fresh observation of changed physical source has a different snapshot ID and
rejects the old source option; the original retained observation remains valid.

## Independent validation, review and feature publication

61 focused tests pass:23 new permanent map-to-source cases plus38 existing
planning/map/source-search cases. Extended map module coverage is100%:
105 statements,24 branches. Scoped Ruff/format, strict mypy513 files, layout and
whitespace pass. Tests cover exact real declaration ranges, repeated names,
Unicode UTF-8 endpoints, async, CRLF/LF/no final LF, nested contents, full native
provenance, original-task assembly, order/identity, explicit source scope,
stale/foreign/missing resources and forged admitted/cached unit frames.

WorkCycle ran one final protected development gate, with100% production coverage
and no waivers or experiment/confirmation runs. Gate passed:True;
protected command elapsed:783.804s.
================= 2635 passed, 2 skipped in 782.08s (0:13:02) =================
TOTAL                                                                     11888      0   2970      0   100%

Exact installed source/test hashes:

```json
{
  "src/devtools/context/planning/repository_map.py": "a22f91cc97e1eeb8d29270ed034f8dd34f0d2a7ae42e88f007937402aed48984",
  "src/devtools/context/planning/source.py": "26071bc42f223b71122306c6a033c716a62cb2d779183480964c80ebe99f995a",
  "src/devtools/context/planning/__init__.py": "5d44d109b097ef74ee365192c212773d9a5e821d95c2c53d8bdd61bdc8e6cf9f",
  "src/devtools/context/retrieval/source/representation.py": "96dea804f6adaac562146ba32b597fca5bcea5674fc3f0ebfe0cf07a2b2bb33d",
  "tests/context/planning/test_map_source.py": "d3a6f8b10ff05e22d270184f2279a721ae145d633e909fd5a8058b935d34093b"
}
```

Feature publication:`0bdc8507601dcf65a742ab3ce5cca4bb8e6f590a`.
Exact review subject:`9d27ac7f9f3305f05fe138209b07f51415034f7f6a464249a92d9e69c09e81bf`.
Codex supervisory review and existing WorkCycle exact-tree publication are
recorded in review.txt/results.json and the original ignored closeout record.
This is not fabricated human approval or protected-main promotion. No worker,
Context projection or serving source changed. Protected main remains the merged
Commands state5d979920d0728775ed529457c88f5b68b440c64f.

Model calls/tokens and worker time are measured separately from the protected
gate and host check timings. Paid Codex usage/cost, active supervision time,
VRAM/RAM/energy were not sampled. Source/test hashes and the live receipt are
reauthenticated after publication; tracked state is restored/clean except the
preserved forensic files. Durable docs/evidence are created only after Checkout
has released its candidate.

## What is possible now, and next

An explicit caller can prepare native map/source views, select an orientation,
expand one represented symbol to exact source and assemble both alongside its
objective. It has not become a native coding-worker acquisition strategy.
The Qwen run used existing inspect/search tools and never used these new APIs.

The next bounded graph-assisted milestone is an opt-in application ContextTool
adapter exposing current scoped map orientation and explicit symbol expansion,
using these Planning APIs and the existing source-observation/edit-admission
owner. Metadata alone must not become edit authority. Exact expanded text needs
ordinary host-attested span/version handles; candidate edits must invalidate
stale map/RI frames and permit legitimate refresh. Preparation cost, scope and
native model Tool selection need their own qualification before claiming worker
adoption or retrieval benefit. Do not add ranking, another graph engine or a
universal planner. That integration is NOT implemented here. A distinct future
task must test native check_changes/freshness completion; this exposed task is
not retried. B-0002/B-0009 parents and selective main integration remain open.
