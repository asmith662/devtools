# Repository Intelligence, Retrieval, Localization and Context code audit

Current audit checkpoint: [source grounding, evidence boundaries and maintained tests](ri-source-grounding-audit.md).
All64 selected paths/55 distinct blobs now have applicable full-body review.
Historical review is574/606, leaving32; current fixtures are30/93, leaving63.
The separate177 older current-RI versions retain their recorded review depth.
Two distinct pending bugs and eight advisory updates preserve approval boundaries.
The next exact32-path experimental cohort and subsequent fixture/version schedule
are recorded in the version-specific ledger; no next cohort is launched here.
The task-obligation A+C recommendation remains unapproved. RI review and the
repository-wide program remain incomplete; the successor dossier stays postponed.

The [task-obligation coverage decision preparation](task-obligation-coverage-decision.md)
turns the U1 omissions into concrete trusted/reviewed consumer options. Scoped
readiness cannot certify exhaustive task decomposition; no architecture slice
is implemented or approved by this research checkpoint.

Follow-up: the [physical-line correction and deeper implementation/fixture review](ri-deep-audit-followup.md)
records a separately validated source-fix commit, expanded historical review and
exact remaining gaps. The first checkpoint's adverse reproduction and counts
below remain historical evidence; they are not the current bug disposition.

## Disposition

Deep current-source review at feature
`95efbf711c3644fb32d269d85927000cd8f4aaa9`, compared with protected remote main
`5d979920d0728775ed529457c88f5b68b440c64f`. This is the first domain of the
[comprehensive review](comprehensive-code-audit.md), **not repository-wide audit
completion**. No inference, scientific treatment replay, production fix, source
installation, protected promotion or artifact deletion occurred.

All 118 current Python modules under `src/devtools/context/` and
`src/devtools/evaluation/` were inspected at substantive-body level, with
namespace-only modules treated as export surfaces. The review includes 481
function/method definitions, not just public names. Exact per-module algorithms,
class/function cursors, identities, static callers, test assertions and omissions
are in the [coverage ledger](code-audit/README.md). Current source review does
not imply that every historical version or every test fixture was reviewed.

**Strongest findings:**

1. A reproducible physical-line source-search defect remains in maintained code.
   All 912 current focused regressions pass, demonstrating a real missing boundary
   case rather than proving the implementation correct for every input.
2. Ordinary native source search/read operations genuinely consume RI and
   Planning. “RI is unused by agents” is too broad. Conversely, whole Localization
   witness/readiness composition and SnapshotDelta have no maintained operational
   consumer; graph/map availability is not demonstrated native model adoption.
3. The native map adapter omits existing direct-base analysis. The general typed
   graph supports bases; adding another graph engine would address the wrong gap.
4. Parsing, module interpretation, native-fact replay and filename indexing repeat
   across real consumers. Some repetition protects provenance. Measure and qualify
   exact-frame reuse before replacing those checks or promising performance.
5. Several scientific policies correctly remain experimental. Their adverse or
   mixed results do not invalidate source facts, justify automatic selection, or
   prove the absence of useful Context integration.

## Evidence and review method

The source review followed all substantive implementation lines in twelve
responsibility groups. Public models, internal algorithms, guards, errors and
identity derivation were considered together. AST indexing over all 1,329 current
Python files supplied candidate consumers; imports were traced through package
exports and checked against actual application dispatch and original receipts.
Static discovery is labeled as such, not upgraded into runtime proof.

The focused command was `uv run pytest --no-cov tests/context tests/evaluation -q`:
**912 passed in 30.99 seconds**. Planning and selected repository/source/worker
boundary assertions were read directly. The ledger also indexes the actual
assertions and raise statements in all relevant current tests, while explicitly
marking unreviewed fixture/helper bodies. This is stronger than a list of test
filenames, but is not a claim that every test body has undergone independent
semantic review. No protected production gate or scientific test suite was run.

Historical research was examined below collection level: all 24 dogfood case
records, their native protocol/result locations, selection/arm definitions,
selected decision gates and algorithm implementations, and development-case
inventories from the breadth studies. Full embedded judgment-cell arrays and
every controller/helper were **not** individually rejudged or reread. Closed
primary results take precedence over retained Stage A README/STATUS prose; the
older documents are not silently repaired. Sealed/reserve payloads stay sealed.

## Implementation and semantic scope

Each row links the real owner. The machine ledger supplies the individual files,
function signatures/lines, exact current and main blobs, tests and call sites.
“Unsupported” below is qualified static coverage, not a runtime failure claim.

| Owner and meaningful algorithms | Inspected contract and boundaries | Tests, consumers and review disposition |
| --- | --- | --- |
| [Repository](../../src/devtools/context/repository/): address, discovery, observation, snapshot, document, corpus, changes | Addresses reject traversal/absolute/backslash forms. Recursive discovery skips aliases and fails as a whole on bounds/I/O; explicit discovery walks only admitted components. Observation resolves containment and uses filesystem text reads. Content identity is length-framed decoded text; snapshot orders exact retained occurrences. Corpus membership is caller-selected discovery evidence. Delta compares full occurrences: added/removed means observed collection difference, not file creation/deletion permission or rename proof. | Repository tests cover aliases, limits, empty/missing/duplicate resources, retained text, identity and full-occurrence changes despite equal snapshot IDs. ContextTools and developer task setup consume discovery/observation/corpus. Delta has only tests/exports. `SOURCE_INSPECTED / CONSUMER_TRACED / QUALIFIED_GAP`. |
| [Imports](../../src/devtools/context/python/imports/) | Direct module-body Import/ImportFrom only, one record per alias, exact AST byte coordinates, source occurrence and derivation. No import execution or implicit traversal into nested statements. | Actual module/reference/native navigation consumers; import tests retain syntax exclusions and source identities. Not a general Python import model. |
| [Module interpretation/resolution](../../src/devtools/context/python/modules/) | Caller explicit roots; package versus module interpretation, relative boundaries and ambiguous names retained. Universe identity sorts exact interpretations. Direct declaration binding differs deliberately from syntactic source selection. Imported-member support follows at most one facade to a direct function; star/nested/rebound/ambiguous routes abstain. | Module/source-selection/imported-member tests distinguish decorated syntax from binding truth. References/native relationships and experiments consume these facts. General facade class reexports are not implemented. |
| [Functions](../../src/devtools/context/python/function/declarations.py), [classes/methods](../../src/devtools/context/python/classes/) and containment | Grammar-3.12 direct module declarations; sync/async functions, module classes and direct methods, with parser/runtime/analyzer provenance. Class base expression text is retained. Native AST declaration range excludes preceding decorators; nested body content can lie inside an enclosing range. Containment validates resource, derivation, ordinal and coverage. | Function/class/containment tests cover stale frames, parse errors, duplicate lexical names and bounded source syntax. Source index, graph, map, grounding and exact source disclosure are real consumers. Recursive source-search symbols are intentionally broader than native semantic declaration coverage. |
| [Direct bases](../../src/devtools/context/python/classes/bases.py) | Name/attribute bases through unique prior local declarations, direct imports and qualified modules. Computed expressions, decorators, shadowing and ambiguous targets remain unsupported. No MRO, instance dispatch, runtime importability or installed class identity. | Base and typed graph tests exercise qualified endpoints and refusals. Framework graph consumes facts when supplied; current native map does not derive/supply them. Concrete adapter gap. |
| [References/Calls](../../src/devtools/context/python/references/) | Deterministic Name/outermost Attribute loads, source and scope assessment, direct-call syntax tag. Argument/assignment/except/match binders and dynamic constructs are conservative. Routes include same-module, direct imported member, one facade function, qualified module and class-qualified direct methods. No self/cls arbitrary receiver or runtime call proof. | Binding/reference tests cover stars, shadowing, unsupported scopes, stale facts, decorated/rebound methods and incomplete support. Native relationships/map call generalized derivation. Older imported-function record type remains a deliberate graph/structural compatibility input with tests; absence from one export is not authority to delete it. |
| [Package membership](../../src/devtools/context/python/modules/membership.py), [mirrored paths](../../src/devtools/context/python/mirrored_paths.py) | Immediate observed parent package under the same explicit root; no namespace/runtime inference. Mirrors are specifically `src/devtools/.../x.py` ↔ `tests/.../test_x.py`, excluding initializers, not general test ownership or execution coverage. | Membership, mirror, role, graph/navigation and generation tests/host compositions. Neither relation's scientific ranking policy is automatically promoted. Generic naming must not hide this repository-specific convention. |
| [Project configuration](../../src/devtools/context/python/project_configuration/) | Retained TOML; malformed parse evidence without invented declarations. Missing selector differs from present non-table obstruction. Exact semantic keys retained. Project/build/pytest/entrypoints and **top-level** dependency-groups settings preserve supported/empty/unsupported/dynamic distinctions. Group strings are raw declarations, ordered with duplicates, not validated PEP-508/installability. Include/mixed forms and normalized collisions qualify whole groups unsupported, preserving valid siblings. Resolution rederives facts before matching observed paths/modules under explicit roots/cwd. | Configuration, settings, obstruction and dependency-group regressions; role inputs consume settings and resolved targets. Derivation-v4/coverage-v3 advance is deliberate. Config selectors and settings are different contracts, not duplicate representations to collapse blindly. |
| [Lexical retrieval](../../src/devtools/context/retrieval/lexical/) | Unicode word/casefold analysis with character offsets, distinct query terms scored once; full corpus TF/DF/lengths, positive matches and stable collection ties. Canonical BM25 independently scores content and filename stem with weight .25. This is **not true BM25F** and performs no identifier expansion. Evaluation uses designated binary relevance, not semantic sufficiency. | Detailed score/statistics/filename/zero/tie/negative-frame tests. Source-search, native worker, obligation acquisition and graph/map seeds are maintained consumers. Index membership uses original document objects; it is not a durable wire contract. |
| [Direct structural projection](../../src/devtools/context/retrieval/structural.py), [composition](../../src/devtools/context/retrieval/composition.py) | Caller seeds and supplied positive import/reference/membership facts; one-hop, both directions, native supports retained. Composition correlates neutral address-ordered evidence, not relevance order or completeness. | Duplicate independent support, stale snapshot, unsupported fact-family and unknown seed tests. Real scientific host consumers exist. Native worker does not expose this full general projection interface. |
| [Source search](../../src/devtools/context/retrieval/source/) | Eager whole-file/recursive-symbol/window views, lexical indexes and explicit fallback status. Symbol syntax can include decorators/nested declarations without inventing native declarations. Mixed view consolidation preserves supports, avoids double-counting file fallback, uses one best vote per view. Scope filters full-index scores before final limit; global IDF survives. Parent expansion authenticates admitted source membership. | File/symbol/window/mixed/scope/newline/retained-state tests; source evidence reaches native Tool responses and edit observations. Concrete physical-line BUG below. Existing tests' LF/CRLF coverage omits Unicode separators within valid strings. |
| [Graph](../../src/devtools/context/retrieval/graph/) | Resource-forward versus typed-core/navigation projections, exact qualified endpoints, family-normalized transitions, no absent-edge negatives. PPR uses reciprocal lexical-rank seeds, seed-return dangling mass, convergence bound; resource projection is max native-node mass. Native provenance remains attached. | Ranking/typed tests verify probabilities, forged/missing endpoints, dangling/disconnected/empty states, convergence and retained source. Source facts and optional query ranking are different capabilities. |
| [Repository map](../../src/devtools/context/retrieval/repository_map/), [fusion](../../src/devtools/context/retrieval/fusion.py) | Canonical typed-core view changes reference/base origins to resource while preserving source occurrences; removes forward containment; query-independent resource-seeded importance shares the existing stationary walk. Lexical symbol metadata plus importance ranks, max per resource; RRF k60 retains independent channels/ties. Empty lexical evidence does not invent a map match. | Map/fusion tests verify provenance, size neutrality, repeated names, empty/stale frames and missing channels. Native opt-in navigation consumes it, but selected original model run did not invoke it. No retrieval benefit follows from those tests. |
| [Planning](../../src/devtools/context/planning/) | Explicit same-purpose/snapshot, ordered choices; materialization reauthenticates native evidence. Whole resource, source-search unit, qualified function reference, compact map orientation and exact map-selected source remain distinct representations. Selected symbol must belong to canonical orientation and admitted source index. Physical UTF-8 byte coordinates resolve against retained source, not ambient filesystem. No silent file fallback/truncation as exact source. | Mixed plan/request assembly and map-source tests exercise Unicode, CRLF/LF/no-final-newline, real AST bounds, exclusion of siblings, altered cached slices, foreign snapshots and selected order. Caller chooses; no autonomous planner or token optimizer. |
| [Roles/routing](../../src/devtools/context/localization/roles/), [routing](../../src/devtools/context/localization/routing/) | Native module/config/target/mirror evidence is rederived, supports are positive and multi-label. Dependency-group names do not infer test/tool/docs roles. Two-tier preferred/escape routing retains every native candidate/rank/order; no elimination, confidence or semantic satisfaction. | Forged/stale input, unsupported config, intrinsic conventions, duplicate normalization and complete escape-lane tests. Maintained internal consumers and research host use; no native worker role-selection Tool or policy. |
| [Grounding](../../src/devtools/context/localization/grounding/) | Exact caller resource/module/direct-declaration/method locators; explicit roots and parse limitations; missing and ambiguity retained. Source declarations are not equivalent to runtime bindings. View identities bind task anchors, locators, source and derivations. | Exact miss, decorated source, method ambiguity, stale module universe and partial parse-failure tests. Existing generation consumes grounding; native lookup_symbol is a different source-view-name operation. |
| [Candidate association/generation](../../src/devtools/context/localization/association/), [generation](../../src/devtools/context/localization/generation/) | Complementary members and competing hypotheses are explicitly caller-shaped; supports are native and revalidated. Fixed recipes and at most one branching projection; no Cartesian planner. Owner/mirror/reference/import operators have explicit work/result bounds. Incomplete/overflow yields no arbitrary successful prefix; valid independent siblings can survive. | Forged inputs/supports, duplicate targets, failed fixed members, branch overflow, work preflight, target-specific failures and explicit incomplete frontier tests. Experimental acquisition consumes these APIs, not the native coding loop. A candidate is not an accepted witness. |
| [Resolution](../../src/devtools/context/localization/resolution/), [kernel/readiness](../../src/devtools/context/localization/readiness.py), [coverage](../../src/devtools/evaluation/coverage.py) | Explicit caller supported/contradicted/unresolved/abstained records. All complementary members required; contradiction remains meaningful. Promotion returns existing witness values, does not register alternatives or approve work. Exact assessment identity coverage and evidence frame required. Conditional applicability needs evidence; open helpful differs from missing/foreign assessments. Empty task cannot claim READY; accepted deferred discovery permits CONDITIONAL only. | Complementarity/competition, unsupported promotion, stale evidence, conditional applicability, no-obligation and duplicate/missing coverage tests. No maintained app/script readiness caller found. Criterion prose and frame exhaustiveness are not mechanically proved. |

### Correctness finding: physical versus Unicode logical lines

Owner: `src/devtools/context/retrieval/source/representation.py`.
Its symbol/window and displayed-line handling uses `str.splitlines`, while AST
coordinates count physical LF/CRLF/CR lines. `_absolute_byte_offset` expects a
physical-line array. Unicode separators inside valid string literals therefore
shift the line table without shifting AST positions.

An independent 27-fixture exercise uses installed Python, real source indexing,
real declaration ranges, `ast.get_source_segment`, and the existing function
materializer. Space controls pass for all three newline forms. All **24**
separator/newline combinations fail the expected source extraction. One concrete
LS/LF result is `b"\ndef target()` instead of
`def target():\n    return 1`. This is not an oracle coordinate fabrication.
Exact outcomes/input hashes are in [the reproduction](code-audit/physical-line-reproduction.json).

The function materializer's `StringIO(..., newline="")` physical-line handling
is already correct. The new map-source adapter uses that physical-line route;
do not falsely attribute the same slicing implementation to it. It still relies
on a successfully constructed admitted source index. No edit-authorization
bypass is established: native current observation/exact-match admission remains
a separate boundary.

Pending bugs `416658bd-8ab9-43c4-bbb3-98a18a88cd4d` (B-0002) and
`5aa7a431-fd3c-4d46-a3a2-cb4e59e9c28e` (B-0009) already contain the required
acceptance scope. Both now have fresh advisory evidence; neither original
payload/status was rewritten. Operator deduplication remains a review decision.

## Actual agent consumption, not API availability

Evidence classes follow the requested distinction: A no maintained consumer;
B maintained host only; C available but not invoked; D invoked without a
demonstrated useful subsequent action; E evidence is tied to a demonstrable
decision/action; F controlled effectiveness. A capability can occupy different
classes in different runs. Tests/AST imports alone establish neither E nor F.

| Capability/path | Actual consumer and evidence | Maximum justified claim |
| --- | --- | --- |
| Discovery → retained snapshot/corpus → source index | `ContextTools.__init__/_observe/_index`; `development_task` and older `coding_loop.acquire_context` | Deterministic host composition in real native runs. Model need not explicitly request an import fact to depend on RI. |
| Source search/lookup → model Tool response | `ContextTools.execute`; original 14/25/26/27/28 Tool receipts | Genuine model selection and bounded ranked metadata. Environment13's three searches returned no matches; do not count those as useful retrieval. |
| Exact source read → current observation → admitted edit | `_read`, `reference`, observed span/version guards, `edits` and native `_turns`; original Environment13/Engineering14 admitted source and validation records | E for observed source used in exact admitted changes. This does not isolate a causal ranking benefit or prove uninterrupted map-assisted engineering. |
| Role25 search | Turn03 returns `analyze_settings` and `_dependency_groups`; turns05/09/10 return settings/models/role evidence with real unit/version/snapshot IDs; subsequent admitted source and oracle pass | Source acquisition is real; interpreting search as the cause of correctness would require stronger comparison. |
| Original map-source27 expansion | Turn06 provider call `EP2mwrJneAOLRWqsf94BcUavLG1venIp`, `expand_source(to="symbol")` | D: **REFUSED / SOURCE_PARENT_NOT_FOUND**, no source disclosed. A recorded call must not be described as successful source expansion. |
| Native opt-in map → map exact source | `RepositoryMapNavigation.orient/expand`, `CodingTask.map_navigation=True`; real ToolRunner scripted tests | B/C. Genuine original28 schemas exposed it; zero model map calls or map-source expansion. No F claim. |
| Outgoing references | `source_relationships` delegates native reference analysis with explicit roots and bounded results | Maintained reachable Tool. Six selected original series do not show its invocation; source availability differs from model use. |
| Direct bases/membership/mirrors | General graph/role/grounding APIs consume them | B in framework/experimental host composition. Native map passes no bases/membership/mirror facts. No invented runtime inheritance/test owner claim. |
| Whole Localization pipeline | Explicit task/queries/grounding/generation/resolution/readiness composed by experimental case author | A relative to maintained end-to-end coding consumer, despite rich internal framework consumers. No native witness/readiness completion or automatic candidate elimination. |
| InformationNeed → exact/selected mechanism routing | `experiments/codex_dogfood/acquisition`, `exact_hint_routing`, `mechanism_routing` | Experimental host use and bounded scientific evidence; not a maintained automatic agent planner. |
| SnapshotDelta | Repository public exports plus deterministic tests | A operationally: no maintained non-test comparison caller found. Current full rebuild is safe; absence of delta use is not a stale-source bug. |
| Exact function Context request | `scripts/qwen/python_function_context_acceptance.py`, developer task assembly | Maintained host entry point; source provenance reaches ModelRequest. No general worker strategy benefit inferred. |
| Qualified-reference request assembly | Public specialized API and tests | No separate maintained app/script caller found; intentionally bounded API, possible simplification review rather than immediate deletion. |
| `check_changes` / `is_current` | CodingCommands → delivered bundle/ToolRunner; native `_turns` invokes host freshness before acceptance | Role25 genuinely called the Tool and got **BLOCKED** by five supervisor files. No native PASS/current completion there; later Codex checks/publication do not change that live receipt. |

The [original-call inventory](code-audit/agent-use.json) freshly fingerprints six
native series, separates RETURNED/REFUSED and records provider call IDs, exact
paths/versions/spans and bounded result metadata. Raw text and provider payloads
remain in ignored custody. Fresh hashes establish the files inspected now;
where no historical per-Tool hash was originally sealed, they are not invented
retroactive seals. Original result/hash chains remain in the evaluation reports
and [five-flow audit](development-lifecycle-observability-audit.md).

Native28 is especially instructive: 19 requests; 14 inspect_source, one
lookup_symbol, one search_source, two git_inspect, one run_check(tests), four
admitted proposals and one oversized transaction refusal. It genuinely repaired
the admission error but not its behavioral/typing failures. It invoked neither
repository_map nor check_changes. Scripted nine-response map/check/currentness
success is infrastructure qualification, not Qwen performance. Original27 had
25 investigation actions and zero edits. These are separate outcomes.

### End-to-end control/data path

1. Trusted `CodingTask` supplies objective, baseline, explicit existing/new/read/
   test scope, fixed plan and resource limits. Availability is not authority.
2. ContextTools discovers/observes only that scope (maximum 32 resources), builds
   the existing corpus/index, and keeps repository/snapshot/content identities.
3. Model calls travel through current ModelTool definitions and ToolRunner;
   provider call IDs correlate native requests and Tool results.
4. Search and lookup return metadata. Ordinary `expand_source` returns indexed
   metadata for file/class/parent; it does **not** itself create an editable text
   observation. Map `to="source"` materializes exact selected source then calls
   the ordinary `_read` path; `inspect_source` also records real current spans.
5. Edit authority requires authorized path, current source/absence version,
   actual observed exact text and atomic byte/component bounds. Map identities
   alone grant nothing. Any invalid component refuses the entire transaction.
6. Admitted edits refresh source/index/observations and invalidate navigation
   frames. Unrelated source drift refuses. This is a full authorized rebuild,
   not dependency-scoped incremental RI reuse.
7. Independent behavior/quality checks and model-invoked check_changes run against
   installed candidate state. A failed test stays a failure; blocked/incomplete
   evidence does not become review eligibility.
8. Host is_current authenticates an eligible report while the candidate remains
   installed. Restoration or relevant mutation invalidates historical freshness.
9. WorkCycle independently reviews, reauthenticates and publishes; readiness,
   retrieval rank, source observation and check PASS confer no publication grant.

Repository snapshot identity, native source version, candidate/check identity,
provider call ID, review subject and Git publication are different joins. No
universal execution ID or automatic semantic decision component connects all
of them. The lifecycle audit documents where joins are direct versus inferred.

## Experiment/case reconciliation

The ledger enumerates nested artifacts and case/arm metadata, not just 35
collection labels. Its 31 research-family scopes overlap (dogfood cases use
shared algorithm packages); they are not new trials. Existing collection
closure counts and frozen outcomes remain unchanged. For all rows, a code path
or fact promoted later is distinguished from the original selection algorithm.

| Original unit / baseline and treatment | Recorded result and limits | Relationship to current code / agent use |
| --- | --- | --- |
| Dogfood0001: task versus short need, canonical lexical plus direct structure, 299-resource frame | Completed advisory documentation task; blind judgment identity coverage retained; 47 checkout newline identity differences explicitly disclosed | Production lexical/composition facts consumed by host, not controlled treatment benefit |
| 0002: same advisory mechanism, 302 resources, experiment capture implementation | Interrupted first Codex session then completed continuation; first usage incomplete | Lexical-only capture stayed experiment-owned; not uninterrupted autonomous success |
| 0003: project configuration task; full/short lexical plus typed/map advisory | RI implemented; filename weight metadata/race correction preserved; blind boundaries qualified | Configuration fact owner is maintained; cannot attribute implementation success to map ranking |
| 0004: complete-task control versus eight explicit obligation queries | All witnesses reachable; best own maximum depth193 versus global325, not satisfaction | Maintained acquisition kernel consumed experimentally, no native completion policy |
| 0005: native obligation lanes versus positive-role preferred/escape | Mixed; union151→160, some depths improve and semantic ownership14→88 worsens | Routing is maintained lossless operator, not promoted primary discriminator |
| 0006: low-fanout OWNER/MIRROR caller recipes over grounding | Limited candidate coverage, not complete task sufficiency | Grounding/generation are maintained; no inferred witness from candidate cardinality |
| 0007: add branching direct Reference candidates | Limited marginal required coverage and incomplete alternatives | Native reference facts retained; no blanket reverse-reference expansion policy |
| 0008: add Import branch families to owner/mirror/reference | Import marginal +1 REQUIRED cell; Reference adds none; routed union394 versus native241; generation-only recovery qualified | Operators maintained; recovery does not become fresh execution or general policy benefit |
| 0009 R1: canonical versus whole identifiers + unique subtokens | RETAIN AS SEPARATE RETRIEVAL VIEW; same required reach, mixed ranks/burden; provisional contaminated gold excluded | `identifier_sparse` remains experimental; canonical tokenizer unchanged |
| 0010 R1.6: four fixed canonical parameter arms | All required reach preserved; prospective completion/rank tradeoffs do not justify universal replacement | Settings remain supported API, tuned challenger is not default |
| 0011 U1: full task, obligation lanes, 18 manually authored needs | INFORMATION_NEED_AUTHORING_DEFECT; two units wholly unrequested; same-subset burden worsens | InformationNeed authoring is not implemented by native worker or a general framework planner |
| 0012 U2: lexical A, authored exact-first B, extracted exact-first C | EXACT_HINT_ROUTING_SUPPORTED locally; four completion gains, small union reduction, costs bounded; module/bare-class effectiveness unassessed | Exact native grounding maintained; experimental extraction/presentation not productionized wholesale |
| 0013 U3: lexical, always-on exact, explicit intent-role selective exact | SELECTIVE_MECHANISM_ROUTING_SUPPORTED; 10→6 requests, four nonresolutions avoided, retained gains | Frozen prefix grammar is caller authoring, **not** natural-language intent inference; policy stays experimental |
| 0014 R1.7: unchanged, generic attenuation attribution, full discrimination | QUERY_TERM_WEIGHTING_HARMFUL by required-cell regression precedence | Query-weighting policy remains experimental; no hidden production default |
| 0015 R2: canonical independently saturated fields versus true BM25F | BM25F_HARMFUL; union IDF and combined normalized TF saturated once; O6 depth137→138 and AGENTS rank2→3 fail safety | Source scorer and field-state validation inspected; no BM25F in canonical BM25. Stale STATUS is original recovery checkpoint, not final result |
| 0016 Graph3: lexical A, forward-reference incoming-flow B, fused C | GRAPH_HARMFUL despite some gains; no required reach loss, but unsafe regressions; 37 B-only occurrences all unnecessary | Reuses production stationary walk/RRF but experimental incoming-flow ranking differs from production max stationary-node ranking |
| 0017/0018/0019 structural discrimination cohort | Respectively NO_MATERIAL / SIGNAL / NO_MATERIAL; **no actual rank movement**; 0019 unconditional provider semantics unresolved | Ordinal pair diagnosis does not implement structural score or model policy. Conditional gold cannot establish unconditional satisfaction |
| 0020/0021/0022/0023/0024 source grounding | Frozen distinct tasks and parent inputs; no accepted cohort effectiveness result. Original candidate08/0022 failed pre-entry; later journal files do not establish treatment success | Preserve original13 forensics and controller boundaries; unfinished cases are not negative RI evidence |
| Increment25 development8 and confirmation16: lexical seeded one-facade function expansion versus equal-volume lexical widening | Confirmation17 useful structural additions versus15 lexical; five structural useful resources no positive lexical rank; bounded positive complementary evidence | Imported-member fact resolution maintained. Historical seed/control policy remains experimental. Later README confirmation supersedes earlier “sealed” checkpoint prose |
| Increment26 development8: pinned CodeRankEmbed token chunks/max resource similarity versus independent equal-capacity lexical | Bounded semantic complement; one model/configuration/CPU implementation, suspended confirmation | No maintained dense retriever or installer adopted. Negative/no-general-benefit claims must not exceed this configuration |
| Increment27 development24: depth, BM25+, identifier, path-only, lexical RRF, winning windows and direct imports | Saved canonical useful@5=63, identifier68, lexical RRF74; mixed overlap/escape; heldout14 not executed | Experimental lexical/window/fusion policies differ from current canonical source search. No unjudged negatives or automatic defaults |
| Increment28: qualified use of fixed direct-import binding in saved query window, plus full-source localization diagnostic | Evidence limited by small/indeterminate populations, not a new candidate treatment | Earlier conservative binding checker informed later maintained reference semantics; exact syntax use is not runtime use |
| Increment29: qualified Name references with direct-call tag, native first-five seeds | Bounded breadth, not a separate runtime Calls family or top-five policy | Maintained generalized declarations add broader explicit scope/provenance; original algorithm not copied wholesale |
| Increment30: immediate explicit-root package membership in both directions | All49 additions child→package;14 useful already in import surface;12 fully novel all not useful; reverse direction untested by these seeds | Maintained package fact is valid despite no new useful reach on that workload |
| Increment31: exact observed source/test path pairs | 34 pairs,21 useful; one beyond accumulated evidence not useful | Maintained weak mirror fact, never test execution/coverage; family-specific rule retained |
| Increment32 Graph1: one additional edge beyond direct frontier | 704 novel case/resource pairs; sampled2/128 useful, unsampled unjudged | Source `project_case` excludes backtracks/known union and retains all paths; uncapped expansion policy correctly unpromoted |
| Increment33 Graph2: third edge from Graph1 novel frontier | 987 novel pairs; sampled0/128 useful,294154 complete paths; no blanket labels for unsampled population | Explicit source excludes prior evidence and stores third-edge supports; candidate explosion is experimental, not a production graph defect |
| Increment34 structural union | Provenance union, no legitimate relevance order | Diagnostic inventory, not executable ranking or successful admission strategy |
| Increment35 heterogeneous union | Known-useful oracle ceiling99 at K5 versus canonical63 | Uses outcome labels for an oracle; not executable policy or effectiveness prediction |
| Increment36 lexical-RRF plus available dense RRF |73 useful versus canonical63 but lexical RRF74; dense only8 cases, no structural rank | Correct ranked-only RRF k60; unranked structural support cannot be assigned a fake rank. Not promoted |
| Typed graph / graph ranking / repository map baselines | Development-only full-task/short-need resource diagnostics; no controlled agent treatment | Maintained graph/map algorithms tested/used by host, no F-level autonomous benefit established |
| Earlier purpose-relative direct import / admission / ranking | Directional reservation-v1 zero net known-useful gain; offline deterministic ranking no local improvement; unjudged retained | Production direct facts/composition distinct from experimental K5 reservation/ranking. No production admission policy adoption |
| Retrieval diagnostics R1.5 and performance/retrieval | Frozen score/term/support joins and measured baseline/repaired verifier records; collection incompleteness differs from completed individual measurements | Useful experiment-local mechanics remain; repeated parsing/replay deserves current-consumer profiling, not a rerun of scientific treatments |

For source-level attribution, inspected experimental mechanisms include
`increment_25.development._resolve_seed_imported_members/_structural_additions`,
`increment_26.development.tokenize_source_chunks/_encode_token_sequences/score_snapshot_resources`,
`identifier_sparse.analysis.iter_terms`, `bm25f.scoring.score/compare`,
`task_conditioned_graph.ranking.rank/_flow_ranking/require_ranking`,
`increment_32/33.mechanics.project_case`, `increment_31.mechanics.derive_mirrors`,
`increment_36.mechanics._ranked_case`, `mechanism_routing.policy.classify/decide`,
and `structural_discrimination.decision.classify_pair/case_category`.
They differ materially: dense source chunks are not RI subjects; Graph3 ranks
incoming structural flow rather than seed restart mass; U3 intent grammar is
explicit caller syntax; pair categories are ordinal diagnostics without ranks.

Exact experiment code/protocol/result identities and **each captured development
case ID and arm key found in metadata** are in the companion ledgers. They are
not placeholders for inspecting the remaining bodies. In particular, earlier
Increment10–24 root-report versions, every nested reviewer/controller attempt,
all 606 indexed experimental Python bodies, every score/support cell and all
historical RI implementation variants have not received complete semantic review.
Those remain explicitly unreviewed; frozen negative decisions are not reopened.
No claim of exhaustive scientific revalidation is made by this checkpoint.

## Quality, cohesion and reuse findings

| Finding / severity | Actual repeated consumers or evidence | Disposition and compatibility conditions |
| --- | --- | --- |
| Physical-line extraction, correctness priority1 | Source-index symbols/windows versus existing correct function/Planning materializer; 24 reproductions | Existing two pending BUG proposals; exact text/UTF-8/newline tests, no weakened admission |
| No end-to-end native Localization consumer, integration priority1 | Native search/check loop versus maintained acquisition/grounding/generation/resolution/readiness and Cases4–13 | New concrete pending consumer proposal; trusted frame, explicit semantics, no hidden satisfaction planner |
| Native structural navigation omits direct bases, priority2 | General class/base/typed graph versus application map and relationship adapters | New enhancement; consume existing facts, bound results and retain unsupported cases |
| Delta unused operationally, priority2 | `compare_repository_snapshots` versus actual full ContextTools refresh | New integration; preserve fresh observations and full rebuild where reuse unknown, no invented deletion authority |
| Repeated parse/universe/index work, priority2 | Module lookup separately derives functions/classes/parses AST; reference/facade lookup repeats; roles/grounding replay; per-source native module universe; BM25 filename index per query | New bounded investigation using existing profiler. Cache keys must include exact occurrence, grammar/runtime/derivation, root/universe and scope. No removal of validation by assumption |
| Request framing repeated in three APIs, optional maintenance | Planning rendering, function request_assembly, qualified_reference assembly; actual developer task and acceptance-script callers, specialized last API only tests | Advisory to existing module/cohesion proposal with concrete byte/error/provenance compatibility acceptance. Prefer small function composition; verify public API use before retirement |
| Cross-package private/deferred imports | Planning/source/graph helper access, package initializers, native adapter private `_read/_reference_analysis` | Cohesion review, not a proven circular-import failure. Same-application helper access differs from framework architectural leakage; change only with a real stable public contract |
| Linear snapshot/module lookup and repeated scope binding scans | Multiple derivation, containment, reference and map builders | Potential O(resources×lookups)/candidate work, not a measured regression. Fold measurement into reuse investigation before adding indexes |
| Repeated semantic digest mechanics | Repository/function/class/module domains use length framing; role models also have deliberately different JSON hashing | Optional helper review under existing cohesion proposal. Domain tags/order/identities are contractual; do not unify hashes mechanically |
| Source declaration, binding, source-search symbol and witness representations overlap | Decorated/rebound syntax, nested declarations, complementary evidence versus accepted alternatives | **No-action consolidation disposition:** different semantics/provenance; retain distinctions unless concrete external/durable migration is qualified |
| Experimental repeated selection/capture/judgment plumbing | Imports/References/Containment/Mirror breadth controllers and later stage journals | Remaining controller-domain audit, not automatic promotion to framework Evaluation or generic workflow infrastructure |

## Prioritized RI-to-agent backlog

All new records are **PENDING_REVIEW**, not B-number stories, approvals or
implementation grants. Canonical Intake wrote proposal/review hashes. Existing
parents, statuses, scientific judgments and grants are unchanged.

| Order / record | Current → intended behavior | End-to-end acceptance and dependencies |
| --- | --- | --- |
| P1 existing BUG [416658bd](../backlog/proposals/416658bd-8ab9-43c4-bbb3-98a18a88cd4d/proposal.json), related [5aa7a431](../backlog/proposals/5aa7a431-fd3c-4d46-a3a2-cb4e59e9c28e/proposal.json) | Broken physical source-index coordinates → exact physical-line slicing | All eight separators × LF/CRLF/CR, Unicode byte columns, decorators/nested/windows/empty/no-final-line; source unchanged by audit. Operator dedup review needed |
| P1 [15bae0a6](../backlog/proposals/15bae0a6-b95d-417c-98fa-d75a8aff29d4/proposal.json) | Host-only Localization kernel → opt-in native application consumer of trusted explicit frame and decisions | Model-visible scoped evidence/readiness affects auditable acquisition/stop; complements/competition/conditional/deferred/incomplete/stale/forged cases; no automatic alternatives or publication. B-0002/B-0009/B-0035 |
| P2 [cea1b3e7](../backlog/proposals/cea1b3e7-bfa6-492a-b850-343a0c543878/proposal.json) | Existing bases absent from native navigation → qualified direct-base Tool evidence | Real ToolRunner result, exact-source follow-up, current edit, stale refresh and bounded unsupported/ambiguous routes; no MRO or new graph. B-0002/B-0009/B-0035 |
| P2 [1d0ed8bb](../backlog/proposals/1d0ed8bb-e38e-44ea-8af3-530c2516981a/proposal.json) | Exported Delta with no operational caller → existing authorized refresh consumes it | Real edit/new slot, exact partitions, unrelated drift refused, stale map/report, valid refresh/restoration; no speedup claim/cache authority. B-0008/B-0002/B-0009 |
| P2 [aedea41e](../backlog/proposals/aedea41e-804b-4fe0-ad53-8758e074885d/proposal.json) | Repeated current computation → measured minimal reuse decision | Two real consumer workloads, count/elapsed/input closure, exact positive/negative provenance equivalence; no treatment replay or generic cache. B-0002/B-0008/B-0027 |
| Advisory [ae03cda7](../backlog/proposals/ae03cda7-955e-40c6-a131-9e2ba209c9a6/proposal.json) | Broad external CodeGraph inquiry → evidence of existing adapter and unmet actual-selection milestone | Preserve optional caller selection; distinguish scripted use, real model use, action and controlled benefit; do not install another graph |
| Advisory [39c6663a](../backlog/proposals/39c6663a-bab7-43ed-8166-82e780a75d05/proposal.json) | Broad module concern → qualified framing/private-helper review | Two real consumers, exact bytes/request guards and distinct native provenance; no size-driven split/base class |

The reuse proposal's original resource cursor `references/declarations.py` was
an intake typo; the appended advisory identifies the actual package
`references/declarations/analysis.py` and `resolution.py`. The original hashed
payload is preserved. No missing production module is inferred from that typo.

These tasks are suitable for later specialized maintenance agents only with
bounded source scopes, frozen independent negatives and existing review. Broad
semantic orchestration/automatic need authoring still requires a separate
architecture/policy qualification. Candidate elimination, automatic source-search
strategy selection and causal retrieval-effectiveness studies are **not**
implicitly authorized by these records. Harmful/unsupported experimental ranking
policies have an explicit no-promotion disposition, not a maintenance bug.

## Main adoption and remaining review

Of the 118 current implementation modules, **103 match remote main exactly**,
13 differ, and two are feature-only (`repository/changes.py` and
`planning/repository_map.py`). Thus this review is mostly of already adopted
production source, not only newer feature work. Every module's exact blobs and
consumer/test cursors are in the ledger. Feature differences include explicit
discovery, request/source formatting, configuration obstruction/dependency groups,
role consumption and caller-scoped search. Application native navigation and
source-bound checks require their own destination closure and authority review.

The [prior destination grouping](production-adoption-and-architecture-reconciliation.md)
remains supporting evidence, not permission to import feature ancestry. Actual
destination tests/main-only files, public exports, source ranges, config-version
changes, optional navigation dependencies and protected final-tree validation
must be reviewed together. Known Commands adoption is retained and not reopened.

Remaining depth is explicit: all historical RI blob variants, full fixture/helper
review for the indexed tests, every experiment algorithm/controller and nested
attempt, original archived Increment10–24 payloads, case-level usage beyond six
native series, and any missing original receipts. No `AUDIT_COMPLETE` is assigned
to hide those obligations. There is no current controlled F-level demonstration
that native map/Localization integration improves autonomous engineering.

The next substantial domain audit is execution/Tool/Checkout/WorkCycle and the
application edit/check boundaries, with protected-validation reuse/input closure
prominent. It should carry forward this ledger and finish the listed RI history/
fixture/controller omissions rather than repeat the census. The final successor
ChatGPT dossier remains postponed.

Final documentation verification: 42 existing Markdown/Intake/layout tests pass
in 1.81 seconds, layout and whitespace checks pass, 1,329 current Python files,
297 prior lifecycle inputs, 84 original native Tool receipts and all 13 forensic
files retain their observed hashes. Canonical Intake validates 21 pending and
one previously approved record; none was newly approved. Ledger path/version,
case/arm-pointer and changed-link checks pass. Publication hashes and exact
changed paths belong to the [checkpoint manifest](code-audit/checkpoint.json)
and ordinary feature commit, not an invented new production validation receipt.
