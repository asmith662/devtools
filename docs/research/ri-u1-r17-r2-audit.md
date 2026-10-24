# RI deep audit: U1 InformationNeeds, R1.7 discrimination and R2 BM25F

This source-and-evidence audit starts at feature
`555b23b13e729fcf1464b581040f8a22223cb983`, on
`feat/qwen-context-worker`. Remote feature and protected main
`5d979920d0728775ed529457c88f5b68b440c64f` were independently advertised at
entry. There was no Checkout owner and no tracked/index change. All thirteen
original forensic files retain their original raw Git hashes. The containing
commit supplies this checkpoint's final identity; the
[checkpoint receipt](code-audit/ri-u1-r17-r2-checkpoint.json) records validation.

This continues the [RI audit](repository-intelligence-code-audit.md) and
[preceding dogfood lifecycle review](ri-dogfood-lifecycle-audit.md). It does not
change taxonomy, grant implementation authority, reopen science, or complete the
repository-wide review. No model, historical capture, adjudication, archived
pickle loader, treatment controller or protected-main integration was run.

## Findings and exact review scope

The three cases test different failure boundaries. U1 omitted semantic requests;
its required resources were nevertheless reachable. R1.7 and R2 preserved
candidates but changed their ordering. Improving a score cannot author an absent
obligation. Better obligation coverage cannot authenticate a wrong source or
correct an erroneous scoring formula.

| Case | Paths / distinct blobs | Research mechanism | Preserved conclusion |
| --- | ---: | --- | --- |
| 0011 | 42 / 41 | Manually authored InformationNeeds versus whole-task and obligation queries | `INFORMATION_NEED_AUTHORING_DEFECT` |
| 0014 | 22 / 21 | Task-only term multipliers over canonical BM25 evidence | `QUERY_TERM_WEIGHTING_HARMFUL` |
| 0015 | 37 / 34 | True BM25F versus independently saturated content/filename BM25 | `BM25F_HARMFUL` |

The [frozen 101-path manifest](code-audit/ri-dogfood-next-cohort.json) hashes to
`4a2d0a7a5bebbee7702dfd424aff245a44e1f8049bc2cc1bf160424df55ab893`.
All paths, physical hashes and Git blobs were checked before review. Full
substantive bodies, fixtures, error paths and historical recovery versions were
read. The [version-specific ledger](code-audit/ri-u1-r17-r2-experiments.jsonl)
preserves each path's chronology: **96 distinct blobs**, including **91 substantive
paths / 87 blobs**, **10 namespace paths / nine blobs**, and **24 complete
test/fixture modules**. Namespace markers and duplicate bodies are not extra
algorithms. The 741 function/method cursors are navigation evidence, not 741
independent mechanisms or trials. There are three primary research mechanisms,
with distinct capture, review, reconciliation, arithmetic and reporting owners.

All 101 historical experimental blobs are also present unchanged on the actual
main destination. That is archival code presence, not production promotion of
authored-need planning, R1.7 weighting or true BM25F. The
[dependency/test overlay](code-audit/ri-u1-r17-r2-tests-and-dependencies.json)
separately records fully read mathematical policy dependencies and bounded
current-consumer traces. It grants no automatic historical-version/current-test
credit. Authored semantic data embedded as R1.7's compressed literal was decoded
as inert JSON and hash-authenticated; this was not a fresh cell-by-cell judgment.

## Case0011: request authorship before ranking

### Task, population and acquisition

The actual task was an optional nonnegative UTF-8 Context byte ceiling in common
copied ModelRequest assembly, preserving rendered payload, task/role fields,
frame/plan provenance and existing behavior. It prohibited truncation and a new
planner. Nine obligations cover ownership, bytes, ceiling, request/frame,
exports, tests, documentation and validation. The
[protocol](../../experiments/codex_dogfood/case_0011/protocol.py) binds the exact
task and pre-inspection authoring; `authoring.json` SHA is
`5f60a2d04a0b94c34c5b0014282f9393ce8bc4ff947d3d5754e84ff320a1e7ff`.

The source start is `85f9f088c5be2afb7861803ee1a96ac7db0448a2`.
A broad, task-independent freeze selects 531 retained source/test/doc/config
resources, excluding experiments and operational/held-out material. Native
decoded-text/content identities and raw source-blob hashes are separate scopes.
The historical temporary-tree observer is inspected, not executed in this audit.

| Arm | Queries | Contract |
| --- | ---: | --- |
| A | 1 | Exact verbatim whole task |
| B | 9 | One manually authored obligation query per obligation |
| C | 18 | Queries for eighteen manually authored InformationNeeds |

All 28 queries use canonical content BM25 plus 0.25 filename-stem BM25,
`k1=1.2`, `b=0.75`, identical retained corpus and full positive matches. No
fusion, exact-route intervention, reformulation or retry is hidden in C. Three
task literal class hints were recorded as `NOT_ROUTED_IN_U1`: this case did not
test failure of exact grounding. The experimental
[InformationNeed](../../experiments/codex_dogfood/acquisition/needs.py) is a
caller-authored purpose associated with native task/obligation/provenance, not
an autonomous decomposition result or a new production type.

The [execution owner](../../experiments/codex_dogfood/case_0011/execute.py)
claims exclusively before queries and refuses re-entry. It accumulates query
returns before final capture publication, rather than journaling each return.
An interruption can therefore leave an incomplete observation; the marker is
not proof of a durable result or permission to repeat effects. No actual failed
U1 capture is inferred from that possible path. A later
[read-only erratum](../../experiments/codex_dogfood/case_0011/replay.py) restores
authored query order after sorted JSON for the derived overlap trace. It does
not rerun retrieval or replace original query outcomes; its native-pickle path
was not invoked.

### Separate resource gold, need coverage and reconciliation

The resource frame is 531 × 9 = 4,779 cells. Primary and independent review
disagreed on 65 cells and substantially on semantic units/witnesses. Aggregate
agreement was not treated as sufficient: severe disagreement blocked C.5 and
Stage D until a fresh 140-proposition reconciliation. The final reviewed gold
preserves 4,713 agreed cells, resolves 65 disputed cells and records **one explicit
agreed-cell exception** for `scripts/validate_development.py`, REQUIRED to
HELPFUL_ONLY. It contains 23 REQUIRED, 84 HELPFUL_ONLY and 4,672 UNNECESSARY cells;
32 units; twelve obligation alternatives; six task combinations; sixteen
resources in the required union. The ignored local handoff is not a repository
semantic witness or an invented mandatory repository gap.

C.5 separately asks whether the eighteen authored requests express the 32
reviewed necessary units: **576 pairs**. The packet omits queries, ranks, arms
and answer paths, binds native units through an external projection and preserves
semantic statements/provenance. It is an assessment after acquisition, not gold
available to the selector. Primary versus independent matrices have 32 disputed
pairs, plus disagreements in rationale, classifications, alternatives and
granularity. Neither a literal ID match nor agreement count establishes semantic
truth.

The original reconciliation-v1 packet exposed only 50 of 576 pairs, through
110 propositions. It received no decisions that could legitimately invent the
526 omitted labels. The versioned v2 contract explicitly limits adjudication to
those propositions, pins the independent comparison, and requires original
primary/independent matrices for inheritance. The
[reviewed C.5 materializer](../../experiments/codex_dogfood/case_0011/adjudication/stage_c5/reviewed/materialize_reviewed_c5.py)
inherits 544 agreed labels and applies the 32 disputed decisions, with separate
rationale/granularity/alternative provenance. The final matrix is 15 DIRECT,
55 PARTIAL and 506 NON_COVERING pairs; unit coverage is **15 covered, 15 partial,
two uncovered**. Three collective diagnostic sets increase covered units to
eighteen, but twelve remain partial and two absent. None of twelve complete
obligation alternatives is fully requested, even under that diagnostic view.

`AMBIGUOUS_ONLY`, PARTIAL and UNCOVERED are distinct. PARTIAL is not automatically
MISFORMULATED, and an unrequested fact is not an unretrieved source. Task-backed
facts do not acquire fictional source ranks. Full semantic builders and mutation
tests were read; reproducing their authored decisions is structural verification,
not another independent adjudicator.

### Authenticated chain and actual conclusion

| Transition | Original checkpoint / owner | Assurance and limitation |
| --- | --- | --- |
| Task/freeze | `9b8f0f65fc34bdad0f1a4a7c2ec0077278555ae9` | Authored task/source/treatment closure, zero prospective execution |
| Capture | `65e8f22587c11eb54684861ba39e3e7acc7def03` | Original 28-query capture; no model implementation trial |
| Primary resource review | `1ae9b07c69d2fec89b5735db12a81bff30d91702` | Complete primary semantic population |
| Reviewed gold | `918e90bc3c01aaf54621e52d8c0435396005239a` | Independent comparison/reconciliation and explicit exception |
| Primary C.5 | `d16ca97b506627ccd5bdfa9e5fc11cc0333015f1` | Need/unit coverage distinct from resource relevance |
| C.5 reliability | `53e1681d2bbea393bdf7233a279dd176f0d780ee` | Disagreement preserved, downstream blocked |
| Bounded v2 protocol | `d242ed95c85c3b74ae71e16aae9b82e0b6d68b39` | No omitted-pair default, original competing matrices required |
| Final C.5 | `471acb53b131ccb51d5c5799cb8933624700af33` | Final versioned reviewed population and decisions |
| Stage D | [original analysis](../../experiments/codex_dogfood/case_0011/stage_d/analysis.json) | Post-capture accounting, fixed precedence; not a new treatment |

Stage A's old `C5_PROTOCOL.md` hash differs from the current file by a documented
supersession at reviewed-gold publication: original `6206a674…` versus current
`d47f381c…`. Both original Git bytes and the intentional successor are retained.
The primary C.5 publication preface is also explicitly version-qualified in
`stage_d.inputs.provenance`. Old Stage-A-only replay commands are not current
case acceptance instructions. Original treatment/capture bytes remain unchanged.

**U02** (qualified admission/re-admission, purpose/type/route/derivation checks)
and **U19** (native fixture construction through module interpretation and
reference analysis) were never directly or partially requested. The final
`INFORMATION_NEED_AUTHORING_DEFECT` has precedence over effectiveness gates.
All required resources are incidentally reachable in the full A/B/C unions;
there is no observed REQUIRED reach loss or rescue. The complete A witness depth
is 370; B's chosen lane depths sum to 589 with union 269. For the same fifteen
directly covered units, B versus C union burden worsens 220 → 371 and noise
337 → 737; five unit depths improve and ten regress. These are bounded diagnostic
subsets, not a complete successful C arm.

The post-gold per-resource best-query oracle (135-resource union, maximum rank
104) is explanatory and not a deployable request-selection strategy. U05's query
mix and U27's whole-identifier representation provide specific ranking/query
diagnostics; no ablation established an alternative policy. `SEARCH_POLICY_FAILURE`
remains NOT_ASSESSED. Current lexical/graph ranking cannot repair the fact that
the two semantic requests were absent.

## Case0014: task-only weighting preserves reach but harms required order

The exact task concerns pure rendering of completed CommandResult diagnostics:
raw facts, byte-preserving UTF-8 replacement decoding, display versus retention
limits, event-loss/execution-failure boundaries, public API and tests/docs.
[Protocol](../../experiments/codex_dogfood/case_0014/protocol.py) starts at
`3aafd897a6a46a201180dc51dbef5e5201669a58`. Six independently authored obligation
queries use 515 retained resources. Whole-task canonical search is a separate,
unchanged safety/reference lane, not a rescue selected after results.

[Classification](../../experiments/query_term_weighting/classification.py)
accepts only task/query text and exact backtick-marked copied task spans. Repeated
native observations are retained; distinct normalized terms score once. Anchor
evidence dominates repeated non-anchor occurrences. Five frozen generic verbs
are `add`, `build`, `create`, `implement`, `update`; all other terms remain neutral.
Unknown identifiers are not secretly split or assigned a useful label.

| Arm | Explicit anchor | Semantic | Generic verb |
| --- | ---: | ---: | ---: |
| A | 1 | 1 | 1 |
| B | 2 | 1 | 1 |
| C | 2 | 1 | 0.5 |

[Scoring](../../experiments/query_term_weighting/scoring.py) requires the same
native full-bound positive content-or-filename population, reconstructs native
contributions and both channel statistics, rejects foreign/duplicate/missing
candidates and applies only positive multipliers. Native channel grouping is
preserved: content sum plus 0.25 filename sum, then descending score/original
collection position. No expansion, cutoff repair, labels, query-frequency boost
or post-hoc choice of B enters selection. Calling the intervention “reranking”
must not suggest a new candidate generator: only the scores/order change.

The frozen Stage A is `6d26f3c9cce5bc059226a0fe4023dc3ec75832ce`;
capture `06e816693fed9165467c3afde42298e6dcefe615`; blind packet
`15417485eba52eb07631c54dcb141ff8d3294606`; reviewed materialization
`466e0a7a473d5baf7ff0fd75ec9ae3031760649a`; Stage-A README restoration
`c43d46607e55d7999ac0277cd196ca9d9e07b9b5`. The sole capture has **27 operations /
54 ENTERED/RETURNED events**, one shared index, six native queries plus one
reference and eighteen arm constructions. Candidate counts are
216/208/180/343/492/460 (1,899 occurrences, not independent resources).

The reused Journal records immutable claims/returns before the next operation;
a native return followed by failed durability remains ambiguous and cannot be
retried. Finalization accepts only a complete schedule and byte-identical
already-published derived fragments. These are inspected failure paths, not an
observed failed R1.7 capture. Cost attribution charges shared preparation/native
acquisition equally, adds each arm's construction once, and keeps publication,
reference and wall timing separate. Single-run timings are not production speed
evidence. Rational diagnostics expose floating summation residuals without
regrouping scientific scores.

One designated Astra High primary plus a separate self-review supplies the
3,090 cells, thirty units and 36 witnesses. There is **no second independent
semantic adjudication or reliability result**. Sterile input whitelist,
externally pinned packet/import hashes, full ordered native bindings and spans
protect the unchanged materialization. R1.7's large encoded semantic seed hashes
after decoding to `67bd7204f6dfd63f9410c237e10d6fa44b6e3f937860e7a9a545dce2e98f1014`.
Its deterministic builder is not evidence of another reviewer.

The [original Stage D result](../../experiments/codex_dogfood/case_0014/stage_d/analysis.json)
retains all 34 required cells and evaluates all witnesses separately. C/A is the
sole outcome comparison; B/A isolates anchors and C/B attenuation. O5 selected
depth improves 180 → 108, O6 65 → 39; unique resources 196 → 118, occurrences
249 → 151 and bytes 1,585,757 → 1,159,546. Yet **seven required cells exceed the
frozen complementary rank bound**, including O1 Command documentation 1 → 2,
Command implementation 11 → 14, O4 execution tests 4 → 8 and O5 Command
documentation 264 → 303. Relative and absolute bounds both apply; favorable
aggregate sums cannot offset individual regressions. Thus the frozen gate
selects **`QUERY_TERM_WEIGHTING_HARMFUL`** after contract/application/reach pass.

The full Stage D validator compares the complete deterministic calculation, and
tests independently exercise prefix unions, rank crossings, threshold integers,
field/candidate changes and input/output tampering. That is stronger than the
Graph3 metric-subset validator discussed below. It still relies on the
authenticated input owner; a self-consistent forged input/hash population is
not authentic merely because arithmetic reproduces.

## Case0015: actual BM25F, capture repair and a bounded adverse result

The task was strict bounded filesystem reading, compatible codec/rich-model and
error behavior, deterministic stream tests and documentation/protected policy.
[Protocol](../../experiments/codex_dogfood/case_0015/protocol.py) starts at
`53a1d087a24e7880f305e167e2d5f3bbb727ff61`. Its six queries, 515-resource frame,
field representations and positive candidate population are fixed before
execution. This is not the same task or gold population as U1/R1.7.

Both fields use native Unicode word/casefold tokenization. CONTENT is exact whole
retained text. FILENAME is basename stem only, with no directories/extensions,
identifier subtokens or AST fields. Each field's average includes zero-length
documents. Parameters are fixed `k1=1.2`, `b_content=b_filename=0.75`, weights
1 and 0.25, with no post-outcome tuning.

| Property | A: canonical additive | B: true BM25F |
| --- | --- | --- |
| DF/IDF | Independent per-field document frequencies/IDFs | Union document frequency, each document once; one IDF |
| Field normalization | Inside each field's BM25 | Each `tf / (1-b+b*length/average)` first |
| Weighting | 0.25 after filename saturation | 0.25 on normalized filename tf before saturation |
| Saturation | Separately in each matching field | Once on combined weighted normalized tf |
| Candidates/ties | Full positive content-or-filename; collection-order ties | Same set and tie convention; mismatch refused, never repaired |

[Scorer](../../experiments/bm25f/scoring.py),
[fields](../../experiments/bm25f/fields.py) and
[independent arithmetic validator](../../experiments/codex_dogfood/case_0015/stage_b/validation.py)
were read completely, along with their synthetic numerical fixtures. For two
equal-length documents with a term present in both fields of one document,
combined tf is 2.25 and union IDF is log(2): single saturation gives
0.9945155199338345, additive channels 1.126364168409911. Empty fields contribute
zero; positive tf with zero average is inconsistent and refused. No-match
candidates disappear; repeated query observations do not multiply terms. Full
traces retain float.hex inputs/intermediates, exact field/source identities and
stable ties. Synthetic fixture snapshots use a deliberately fake ID for arithmetic;
they do not test retained-source authority.

### Original attempt versus metadata-only amendment

| Event | Original retained evidence | Meaning |
| --- | --- | --- |
| Stage A | `d7e28de0e103bdf0e494a0156311fa1c14b6c9f8` | Frozen task/field/scorer semantics |
| Attempt 1 | [capture failure](../../experiments/codex_dogfood/case_0015/stage_b/attempts/case-0015-stage-b-1/capture_failure.json) | `MemoryError`; frame/fields returned, index preparation active/failed; no treatment or completed capture |
| Recovery freeze | `cc9aaef40dec218e63fae7de835298ef76bd241f` | Separate capture-metadata authorization, immutable failed source/receipts |
| Attempt 2 | `a4e3f6ee2446e0b54ec1477c0fab69abfbd4c716` | Fresh 17-operation/34-event capture, not reuse of old scoring returns |
| Blind packet | `6646f369af5e4b7908288d5c2af673148c2805c9` | Exact original task/six obligations/515 whole resources only |
| Reviewed publication | `c29d73cc48f1428eb93a184261ce815cf4e6b1c0` | Raw primary bytes and unchanged gold; no second reviewer |

The failed implementation hashes `repr((collection,snapshot,content,filename))`:
shared rich structures cause enormous repeated expansion. The amended
[fingerprint](../../experiments/codex_dogfood/case_0015/stage_b/fingerprint.py)
streams typed length-prefixed scalars and posting references, and uses stable
importable `PreparedFrame/PreparedFields` records rather than launcher `__main__`
identities. A narrowly pinned legacy loader exists only for the failed attempt;
it was inspected, not invoked. `FunctionType` preserves scorer code/defaults and
rebinds only metadata validation. Independent synthetic tests compare scores,
field mutations, bounded allocation, durable type identity and separate-process
loading. This is historical capture repair, not a new production cache or a
changed retrieval treatment.

Attempt 2 candidate counts are 290/307/156/221/425/408 (1,807 occurrences).
Its inert Stage D graph reader validates schedule/entry/return chains, source
closure, native field/count/DF statistics, every A/B/reference rank and score,
decomposition and costs without deserializing native pickles. Sealed native
pickle bytes can be hashed as opaque data without being loaded. The three
telescoping diagnostic components—union IDF, inside-tf filename weight, single
saturation—are unranked explanations, not three additional scientific arms or
uniquely sufficient causal claims.

One primary plus self-review provides 3,090 cells: 21 REQUIRED, 102 HELPFUL_ONLY,
2,967 UNNECESSARY; 42 units (25 TASK_BACKED, seventeen repository-supported),
twelve witnesses, 32 task combinations, nine sufficient resource unions and
four minimal unions. O2 is a legitimate **repository-empty** task-backed witness:
complete at depth zero, zero acquisition bytes, no invented source/rank, no
zero-to-zero gain. Missing repository support instead yields None/INCOMPLETE.
The production `WitnessSet` requires nonempty targets; do not transplant this
experimental empty-resource encoding into it or equate source absence with
task-backed semantic support.

The [original result](../../experiments/codex_dogfood/case_0015/stage_d/analysis.json)
preserves eleven required resources, 21 cells and all 42 units in both full
candidate lanes. All obligations remain complete; no meaningful witness or rank
gain qualifies. O6 depth worsens 137 → 138, and required `AGENTS.md` rank 2 → 3
fails `5*3 <= 6*2`. There are two required-cell regressions. Unique prefix resources
tie 162, occurrences worsen 203 → 204, bytes decline 1,364,603 → 1,346,862.
The original **`BM25F_HARMFUL`** follows frozen precedence, not a cost veto or a
claim that every field-aware approach fails. Frozen unfavorable policy remains
unpromoted; current canonical BM25 is not replaced.

## Integrity, test quality and assurance boundaries

The [artifact record](code-audit/ri-u1-r17-r2-artifact-identities.json) records
268 retained byte identities, 245 successful manifest-member checks, nine
original Git seal anchors and 676 original Git member checks, plus 1,561 original
source/resource occurrences checked against their frozen Git archive policies.
Original Git/source
closure is independent of self-consistent current hashes. The only old-seal versus
current member mismatch is U1's documented C.5 protocol supersession, not a changed
query/capture. All retained address/content cell associations agree across
4,779 / 3,090 / 3,090 cells. R1.7/R2 packet checks rederive native document and
snapshot/corpus IDs. U1's older packet has address/content but no document-identity
field; no invented observation fills that absence.

U1's original archive inherits `core.autocrlf=true`, so its retained CRLF source
is not byte-identical to the LF Git blob. R1.7/R2 explicitly freeze
`core.autocrlf=false`. Independent in-memory Git archive reads reproduce every
retained source text under those respective policies, without extraction or a
second source tree. Raw blob hashes, archive bytes and native content identities
remain separate; the audit never normalizes source and calls it exact. Future
versioned capture should pin that configuration rather than infer it from the
operator's current Git settings. This is original representation provenance,
not demonstrated judgment corruption or a production RI parser defect.

These are different task populations, not 10,959 independent scientific trials.
No current counterexample establishes corruption of original judgments. Reviewer
isolation is supported by packet whitelists, pinned inputs and attestations; a
complete external provider/browser-access trace was not available and is not
inferred from model labels. No result rejudgment occurred.

All 24 cohort test modules, inline builder mutation suites and associated fixtures
were inspected. Useful independent tests include alternative prefix enumeration,
integer gate boundaries, explicit two-field numerical examples, lossless hex,
candidate/source/pair/tie tampering, exclusive overwrite and failed-return paths.
Rebuilding authored gold/reports checks reproducibility, not independent semantic
correctness. Legacy own-capture pickle/replay tests were not executed. Historical
line helpers using `splitlines` remain versioned; exact support quotes and original
hashes protect the stated originals, but do not make those helpers generally safe
against adversarial Unicode separators. No new original-span impact is shown.

Fourteen [bounded probes](code-audit/ri-u1-r17-r2-probes.json) check the previously
reported U2 missing-completion failure, Graph3 partial validation, five genuine
packet refusals, synthetic gate precedence/zero cases and independent field math.
They neither re-rank nor re-adjudicate original cases. The 101 synthetic tests
run here are the external weighting/BM25F arithmetic suites and versioned canonical
binding-verifier regressions, not a new effectiveness result.

**Distinct Graph3 finding:** `stage_d.validation.validate` returns PASS/check
claims mentioning source ancestry, capture replay and deterministic artifact
replay, yet accepts changed `graph_contributed_gain` and arbitrary
`primary_answers`. Its actual current callers in `analysis.expected/verify`
authenticate inputs, calculate their own result and compare exact bytes; those
protect the original publication. It is not a safe standalone whole-report
authenticator. This contract/assurance problem is separate from neutral-resource
pair binding and now has pending BUG
[5fa23957-703a-4de9-9619-316f8f7740ed](../backlog/proposals/5fa23957-703a-4de9-9619-316f8f7740ed/proposal.json).
Future versioned consumers must either expose a truthful metric-only contract or
fully verify flags/prose/input closure and reject unsupported formats. Frozen
Graph3 code/results remain unchanged; no historical verdict corruption is claimed.

## Actual maintained consumers and integration obligations

| Capability | Maintained owner and actual path | Maximum supported utilization |
| --- | --- | --- |
| Canonical lexical BM25 | lexical `bm25/scoring/filename` → source `search_repository_source` → `ContextTools.search_source` | Actual native model searches/reads and subsequent edits in retained receipts; no comparative benefit from these three cases |
| Authored needs/obligations | experimental `acquisition.needs`; maintained `LocalizationTaskInterpretation`, `LocalizationObligation`, lexical acquisition and readiness | Host APIs/experiments; no complete native trusted-need/witness consumer established |
| Exact hints | maintained grounding/Planning and native lookup/expand source primitives | Bounded native source navigation exists; no authored-need selective bridge proven; U1 intentionally did not route hints |
| R1.7 multipliers | experiment-only `query_term_weighting` | Intentionally unpromoted adverse policy; no model-facing production scorer |
| True BM25F | experiment-only `bm25f` | Intentionally unpromoted adverse configuration; no production/native consumer |
| Localization sufficiency | caller assessments, ALL/ANY targets and `assess_localization_readiness` | Checks the supplied frame; explicitly cannot decide whether every real task obligation was authored |

Current `ContextTools` constructs only task-authorized retained resources/index,
checks current source, exposes bounded search metadata and separately materializes
exact observed source. Metadata/rank is not sufficiency or edit authority. Neither
its Tool schema nor `CodingTask` currently carries the complete trusted authored
obligation/need/readiness composition investigated here. Source changes still
require exact current observation/version and task-authorized path, followed by
source-bound checks and independent WorkCycle publication.

All 84 original Tool-receipt files across the six previously selected native
series were rehashed. They include real source search/read/edits but no
`repository_map` invocation in native-map28, no full Localization/readiness
consumer, and no U1/R1.7/R2 autonomous policy adoption. This reauthentication adds
no new empirical effectiveness level and does not infer why a model chose a Tool.

Priority integration remains existing pending
[Localization consumer 15bae0a6](../backlog/proposals/15bae0a6-b95d-417c-98fa-d75a8aff29d4/proposal.json),
now qualified with task-clause/obligation/need coverage. A trusted caller must
provide or review that frame; omissions, requested-but-unretrieved, partial and
unsupported evidence remain distinct. Acceptance must demonstrate an omitted
mandatory obligation blocking semantic completion, a caller-corrected need
reacquiring current authorized source, reviewed witness/uncertainty handling,
actual native model action/edit, `check_changes` PASS and host currentness. A
passing lexical rank or supplied-frame readiness cannot certify task completeness.
The separate [exact-hint consumer 06c3809b](../backlog/proposals/06c3809b-f80c-461d-9585-2d4a973f8252/proposal.json)
owns acquisition rather than semantic truth. Neither requires another Context
compiler, locator hierarchy or automatic planner.

## Cohesion, reuse and actionable dispositions

There is real reuse: R1.7/R2 use U2's immutable Journal; R2 uses R1.7's inert graph
reader; all use native lexical/resource/time/command primitives where applicable.
Physical-byte import helpers intentionally differ from canonical-LF capture
helpers. Deliberately independent review algebra must not be consolidated merely
because minimal-set functions look similar. Deferred metrics/diagnostic imports
are a bounded case composition, not evidence for a generic base evaluator.

Repeated filename-index construction has two concrete maintained consumers:
Localization's global/obligation lanes and native SourceSearch's selected views.
R2 also records seven intrinsic filename builds. This establishes measurement
targets, not a current latency regression or permission for a cache. Existing
[measured-reuse proposal aedea41e](../backlog/proposals/aedea41e-804b-4fe0-ad53-8758e074885d/proposal.json)
requires representative profiling and exact snapshot/analyzer/runtime closure,
with stale-source invalidation before any optimization. The historical rich-repr
failure motivates compact capture metadata, not inference that all current
derivation recomputation is unnecessary.

| Finding | Disposition / next operator action |
| --- | --- |
| Graph3 metric-subset versus whole-report assurance | One distinct new pending BUG 5fa23957; versioned report-only consumer contract and full negative tests, no frozen edits |
| U1 omitted semantic requests; native need/readiness bridge absent | Material advisory on existing 15bae0a6; explicit trusted caller coverage/uncertainty/action/check acceptance |
| Exact-hint acquisition bridge | Existing 06c3809b sufficient, evidence expanded; U1 hint non-use is not failed grounding |
| U2 downstream None completion | Existing [edfb9e28](../backlog/proposals/edfb9e28-34fb-497f-8ff1-d3a4c7320eb0/proposal.json) reauthenticated; future full-pipeline null/zero tests, original selected witnesses complete |
| Increment23 binding verifier optional; old analysis APIs unchecked | Existing [2e70de9a](../backlog/proposals/2e70de9a-d09c-409d-a7a2-0f32f67c4768/proposal.json) expanded; tests call `verification_v1`, original evaluation/positional loaders still bypass it; Increment24 report digest closure remains open |
| Increment25 task prefix-normalization bug | Existing [dabfa1f7](../backlog/proposals/dabfa1f7-b4ae-4ed0-82c9-179f47e31630/proposal.json) remains pending versioned authoring repair; U1/14/15 exact task authoring does not use that helper or repair it |
| Production physical-line defect | Fix `a0a6c22403f7df2679aa574226e420521a8accf5` implemented, prior gate unchanged; operator should reconcile implemented/duplicate scopes on 416658bd and 5aa7a431 without closing historical/versioned obligations automatically |
| Scientific binding verifier delivered | `0cc372503e8efbd899b3e0f724c903d8ebd040a2` implemented for supported Increment23 schemas; operator separate implemented subset from still-open entry-point guards |
| Repeated indexing, fixture/assurance scope and module reuse | Existing aedea41e, a88167f9 and 39c6663a advisory updates; measurement or compatible extraction only after real consumer/version qualification |
| Harmful R1.7/R2 treatments | Verified intentional non-adoption; no production ranking bug inferred, no automatic tuning/promotion |

[Intake receipts](code-audit/ri-u1-r17-r2-intake.json) distinguish **one new
PENDING_REVIEW proposal** from **ten append-only ADVISORY updates**. None is an
approved B-number story or grant. No approval, closure, dispatch or backlog-parent
status changed. Report-only maintenance agents could check original seal/roster/
pair/schema relationships under a read-only contract; that would not confer
judgment, treatment or publication authority.

## Validation and remaining RI work

Validation: **101 external synthetic tests passed**, fourteen bounded probes
passed, exact cohort/source/blob and original-input checks passed, canonical
Intake hash chains and added links/JSON/layout/whitespace checked. The checkpoint
receipt records final counts and preserved artifacts. Production source/tests,
frozen science and original outcomes are unchanged, so no protected production
gate was rerun; rehashing old protected inputs is preservation evidence, not a
new gate or an exact-tree reuse claim.

Experimental applicable review advances **252 → 353 of 606 paths**, leaving
**253**. The **84 current RI fixture paths** and **177 older current-RI versions**
remain separate obligations. Previously read external policy/helper bodies have
their own dependency depth and do not silently add experimental-cohort credit.
No RI or repository-wide completion is claimed.

The [next frozen cohort](code-audit/ri-u1-r17-r2-next-cohort.json) contains **42
paths**: Case0009 (15), Case0010 (10), `retrieval_diagnostics` (nine) and
`bm25_sensitivity` (eight). It follows the lexical diagnostic/control lineage:
review full original controllers, population/identity closure, scoring diagnostics,
tests and report assurance before drawing policy conclusions. Exact remaining
path/blob identities and prior partial depths are retained. This cohort was not
launched. Later source-grounding, structural-discrimination, verification and
performance histories remain visible in the full ledger. No new domain or
successor-session preparation begins here.
