# Precise source navigation and active working-set continuity

## Ownership decision before implementation

Authenticated main: `eb053c735c7edbdfb8058170adfc3786fcf28fa3`.
The [previous case](../../experiments/local_maintenance_cohesion/REPORT.md)
remains frozen. Its complete requests fit, but three model-selected broad reads
were repeated after the corresponding exact exchanges were omitted. This
sequence does not establish why the model reread them.

Effect-free reconstruction shows that all five distinct broad source exchanges
would cost 52,210 serialized bytes. Even the three repository-host chunks alone,
with objective and native schemas, cost 35,067 bytes: more than the unchanged
32,768 hard ceiling. Keeping every broad read is not a feasible remedy.
The old search already returned `RepositoryCodingHost.build_request` at exact
Unicode offsets `[11205,11747)`, among other symbol candidates. Qwen instead
read file chunks. No source/version change explains the eviction.

Existing `SourceSearchIndex` owns file, Python-symbol and physical-line-window
representations, exact unit identities and enclosing expansion. Its symbol
units reuse RI declarations/occurrences; they are not a new universal subject.
`search_repository_source` already supports mode and resource selection.
`ScopedSourceTool` already materializes exact unit ranges through Context
planning. The neutral host builds this index but exposes only path/range reads;
the old experiment supplied mixed search through an application adapter.

The authorized integration will add an opt-in native navigation composition to
the shared host. Tools will adapt the existing bounded scoped index; Agents
will project metadata and resolve exact current unit selections into existing
source-read requests. No index, parser, ranker, graph, source identity, execution
loop or Context history is recreated. Native calls still enter through host
admission and Model/Tool composition plus ToolRunner. Metadata never acquires
source or grants edit-witness credit. Generic character-range reads remain.

The existing projection already retains distinct current exact source whenever
it fits. First test a smaller coherent source working set through that mechanism;
do not add pinning, another relevance policy or a summary trigger without a
demonstrated residual gap. Exact source omitted by projection remains unavailable
for edits. Existing mandatory/readiness/check protection can refuse an impossible
minimum rather than silently weakening it. Semantic/adaptive compaction, original
history, native validation and custody remain independent.

The default legacy native surface will remain unchanged. The new opt-in path
must be used by maintained non-Qwen tests and the separately frozen real host.
No first-request inventory implementation (B-0035), large-file edit-contract
change, legacy Qwen policy migration or additional authority is included.

## Validation plan and limits

Before live entry: characterize existing consumers; compare the frozen broad
trace with precise unit acquisition under unchanged byte limits; verify literal
source text, versions, native correlation and an admitted edit through the real
shared loop. Negative controls cover stale/foreign/unauthorized units, non-Python
fallbacks, Unicode/CRLF, partial disclosure and protected capacity failure.
The committed executable tree must pass the unchanged protected development
gate. A new B-0035 task requires independent oracle and feasibility preflight.
Deterministic savings do not establish real model source-selection or coding
competence. One live attempt, if feasible, receives its own freeze and grading.

## Implemented contract

`RepositoryCodingHost(..., navigation=True)` adds `find_source` and
`read_source_unit` to the complete request schema before byte accounting.
The default remains disabled. `find_source` accepts a bounded query, optional
authorized path, `file`/`symbol`/`window`/`mixed` mode and page offset. An empty
query pages the existing representation. Eight results at most enter a page;
native metadata is additionally bounded by the host disclosure-byte allowance.
A full page advertises a possible next page, which may be empty.

`devtools.tools.source.ScopedSourceNavigationTool` validates the selected index,
scope and currentness and uses the existing source search. Agents'
`coding.navigation` projects only metadata and resolves a unit ID plus exact
snapshot ID into the existing `SourceReadRequest`. ToolRunner and host admission
remain on both paths. `ScopedSourceTool` performs actual Context materialization.
No additional source identity, index, parser or executor is introduced.

Metadata identifies resource/version, unit kind/name, half-open Unicode offsets,
one-based physical lines, UTF-8 size and enclosing/file IDs. Python declaration
support comes from existing RI; unsupported languages explicitly fall back to
file representation. Generic `read_source` remains available for adjacent,
partial and non-Python reads. A partial unit read reports its actual disclosed
span and remaining range; an entire symbol is not claimed as acquired.

The host can select `find_source` as an eligible metadata operation in the
existing `ProjectionPolicy`. There is no new pinning policy: current exact
disclosures retain the existing priority and affordability rules. Metadata alone
does not establish edit evidence; a source reference omitted from active Prompt
cannot authorize a later edit. Invalid identity/currentness and ambiguous
operational failures remain refusals/failures under existing semantics, with no
automatic replay or fabricated source acknowledgment.

The legacy Qwen compatibility adapter keeps its native operations, task hashes,
readiness and continuation policy. Shared coding/Tool regressions cover it; this
increment does not claim that its separate application presentation adopts the
new neutral-host navigation operations.

## Deterministic measurements

The maintained fixture uses one bounded frozen source input and scripted native
selections through the actual neutral coding loop. It does not replay historical
effects or implement B-0035. Its exact-source edit inserts a fixture marker and
runs an independent literal Command check, then restores the source.

| Measurement | Broad range fixture | Precise method fixture |
|---|---:|---:|
| Source bytes disclosed | 24,576 | 7,891 |
| Read actions | 3 | 3 |
| Navigation actions | 0 | 3 |
| Acting requests | 4 | 3 |
| Final complete-request bytes | 24,604 | 22,365 |
| Final active exact regions | 2 | 3 |
| Omitted source witnesses | 1 | 0 |
| Duplicate acquisitions | 0 | 0 |
| Fixture edit/check | no proposal | admitted/passed |

The precise methods are constructor (3,010 bytes), request assembly (542) and
preparation (4,339). The fixture deliberately selects them; it proves availability,
correlation and grounded editing, not autonomous relevance selection. Keeping
every broad historical source exchange is impossible at 52,210 bytes. A protected
minimum that cannot fit still produces explicit `insufficient` capacity evidence.

Before the committed protected gate, 2,380 focused compatibility tests passed.
A targeted branch diagnostic covered all changed production owners at 100%.
New controls include foreign/stale units, changed source between metadata/read,
metadata-only edit refusal, Unicode/CRLF, non-Python fallback, bounded partial
disclosure, cancellation, missing navigation acknowledgment and impossible
protected Context. No limit, test selector, coverage threshold or exclusion was
changed. The separately preflighted live protocol is
[Maintenance-navigation-0001](../../experiments/local_maintenance_navigation/protocol.md).

## Frozen ten-request trace

`P` denotes projection.py and `R` repository.py in the coding package.
Ranges are actually disclosed half-open Unicode offsets, not requested ends.
The receipt retains native IDs, content/snapshot identities and marginal serialized
exchange costs. The source versions did not change during the original run.

| Request | Complete input bytes | Active exact ranges before response | Next selected acquisition |
|---|---:|---|---|
| 1 | 4,625 | none | list_repository |
| 2 | 8,254 | none | search_source, search_source |
| 3 | 17,126 | none | P[0, 8192] |
| 4 | 14,597 | P[0, 8192] | P[8192, 14095] |
| 5 | 21,768 | P[0, 8192], P[8192, 14095] | R[0, 8192] |
| 6 | 32,196 | P[0, 8192], P[8192, 14095], R[0, 8192] | R[8192, 16384] |
| 7 | 32,049 | P[8192, 14095], R[0, 8192], R[8192, 16384] | R[16384, 24576] |
| 8 | 24,639 | R[8192, 16384], R[16384, 24576] | R[0, 8192] |
| 9 | 25,256 | R[16384, 24576], R[0, 8192] | R[8192, 16384] |
| 10 | 24,892 | R[0, 8192], R[8192, 16384] | R[16384, 24576] |

Metadata exchanges were omitted at request four. Source-capacity eviction began
at request seven; repeated/superseded exchanges were later eligible as recorded
in the receipt. Requests eight through ten reread R ranges that were absent from
their active inputs. That correspondence is observable; the model's motivation
is not. Search had supplied a precise request-assembly symbol, but the worker
selected broad ranges. The final acquired range was not consumed by another
request because the original ten-request envelope ended.

## Protected implementation validation

Committed executable tree `e3be8f8e7890ede763ba5770c7ac08621c57d294` passed 3866 tests,
2 optional live skips, and 100% configured production line/branch coverage.
The unchanged command was `uv run python scripts/validate_development.py`;
recorded wall duration was 1592.236 seconds. Ruff, supported formatter,
strict mypy and layout also passed against the same 1189 physical
inputs. [Machine-readable receipt](../research/code-audit/source-navigation-continuity-20261029.json)
retains commands, timestamps, versions, identities, trace and preservation.
No live effectiveness follows from this gate.

## Real maintenance outcome

[Maintenance-navigation-0001](../../experiments/local_maintenance_navigation/REPORT.md)
failed B-0035: ten global metadata pages, zero source reads/proposals/edits/checks.
Eighty units returned, 72 consumed; relevant host methods arrived only in the
final unconsumed page. Smaller active input did not yield coding progress.
The unchanged archive reproduces the preflight failure sets. No model-authored
implementation was accepted. Task-directed navigation entry/stopping is the
next observed pressure; no redesign or new inference is begun here.

## Verified publication - 2026-10-29

Ordinary non-force publication was independently verified at
`75d511694bf2971645c7fca3f3fb2134514f19b0`, containing protected implementation
`e3be8f8e7890ede763ba5770c7ac08621c57d294`. All 1,189 physical gate inputs and
accepted source/test blobs still match. The explicit human-authorized default-No
recovery released the grading owner without redispatch or authority transfer.
The failed evaluation remains unchanged: ten metadata pages, zero source reads,
proposals, edits or worker checks. Missing grading-wrapper exit receipts remain
unknown. No model-authored code, B-0035 closure or next increment is implied.
