# Code audit evidence ledger

This is dated research metadata for the [comprehensive audit](../comprehensive-code-audit.md)
and [RI domain report](../repository-intelligence-code-audit.md), based on feature
`95efbf711c3644fb32d269d85927000cd8f4aaa9` and remote main
`5d979920d0728775ed529457c88f5b68b440c64f`. It is neither a runtime registry nor
an alternative source, architecture or backlog authority. Raw provider receipts,
scientific captures and preserved archives remain in their original custody.

| File | Contents and qualification |
| --- | --- |
| [checkpoint.json](checkpoint.json) | Changed-path/hash overlay and actual test/integrity receipts for this documentation checkpoint; containing Git commit binds its own identity |
| [coverage.json](coverage.json) | Counts, methods, scope limits, directory census and 13 forensic fingerprints |
| [refs.json](refs.json) | All ref names, exact remote advertisement, ancestry and disposition |
| [tip-deltas.json](tip-deltas.json) | Code/config/test differences per distinct tip; not an instruction to integrate |
| [commit-identities.json](commit-identities.json) | Ordered SHA list; integer `commits`, `tips`, `commit` fields below index this array |
| [commits.jsonl](commits.jsonl) | Reachable headers/parents, with explicit unreviewed status |
| [repository-files.jsonl](repository-files.jsonl) | All historical paths and path/blob versions, occurrence commits, tip membership, current/main blobs and review depth |
| [history-edges.jsonl](history-edges.jsonl) | All reachable root/parent/merge changes; no rename inference |
| [ri-modules.jsonl](ri-modules.jsonl) | Every current RI/Evaluation module, physical SHA, Git blobs, 481 function/method cursors, classes, imports, resolved static call sites, tests and limitations |
| [tests.jsonl](tests.jsonl) | Exact tests, function assertions/raise statements; assertion indexing is not full fixture review |
| [subsystem-reviews.json](subsystem-reviews.json) | Substantive algorithm and quality review for twelve subsystem groups |
| [experiment-collections.jsonl](experiment-collections.jsonl) | 31 relevant research-family scopes, 606 Python algorithm/test/fixture modules and 126 captured-metadata artifacts; not 31 independent trials |
| [experiment-cases.jsonl](experiment-cases.jsonl) | All 24 dogfood cases, exact protocol/result cursors, nested artifact inventories, bounded conclusions and omitted work |
| [experiment-units.jsonl](experiment-units.jsonl) | 14,276 captured case references/arm/lane occurrences with exact artifact hash and JSON pointer; repeated references are not distinct trials or a claim of individual semantic review |
| [agent-use.json](agent-use.json) | Six original native receipt series, call IDs, source versions/spans and independent fresh hashes; long/edit source arguments reduced to size/hash, never copied raw |
| [physical-line-reproduction.json](physical-line-reproduction.json) | Actual installed-Python/maintained-API outcomes for 27 independently authored tiny fixtures |

JSONL is one record per line and UTF-8. Identities are strings unless the field
is explicitly a commit-array index. Blob equality means exact Git object bytes;
physical SHA means the observed checkout bytes. `NOT_REVIEWED` is deliberate.
Source inspection of a current blob does not inherit to prior or future blobs.
`ASSERTION_INDEXED_NOT_FULL_FIXTURE_REVIEW` preserves the important remaining
test-review boundary. A static call site is not proof that any model saw it.

Reproduce the census in the one checkout with read-only Git object operations:

```text
git for-each-ref --format=%(refname)%09%(objectname)%09%(subject)
git ls-remote origin
git ls-tree -rlz <each distinct tip>
git log --all --format=%H%x09%P%x09%aI%x09%s
git log --all --root -m --raw -z --format=@%H --no-renames --no-abbrev
git rev-list --objects --all
git cat-file --batch-check
```

Parse NUL-delimited paths rather than splitting filenames on whitespace. Include
every merge parent and root; without that, intermediate/deleted paths and
merge-resolution differences can be missed. AST call indexing resolves imports
and package reexports conservatively; local rebinding, dynamic dispatch and
instance methods require manual source tracing. No archived pickle was loaded,
historical operation replayed, source tree duplicated or unreachable object
promoted into authority.

The physical-line reproduction uses the existing tiny `_index` helper in
`tests/context/retrieval/source/test_search.py`. For each separator VT, FF, FS,
GS, RS, NEL, LS, PS and each physical newline LF, CRLF, CR, author:
`value = "a<separator>b"<newline>def target():<newline>    return 1`.
Parse with installed `ast`, build the existing source index, select `target`,
and compare its text to `ast.get_source_segment` and the existing physical-line
function materializer. Repeat with a space control. All inputs are valid Python;
no arbitrary UTF-8 coordinates or model output is manufactured.

The remaining work column in the reports takes precedence over an optimistic
interpretation of an index count. Future audits append version-specific evidence
and conclusions; they must not rewrite frozen historical scientific records.

## Physical-line repair and deeper RI review overlay

The [RI follow-up](../ri-deep-audit-followup.md) starts at published checkpoint
`38957ae45d8f5c3e6b8061b749b9291f38cee19c`. The original census, checkpoint,
27-fixture adverse reproduction and historical reports above are unchanged.
Source correction `a0a6c22403f7df2679aa574226e420521a8accf5` and this new overlay
are deliberately separate commits.

| File | New depth and limits |
| --- | --- |
| [ri-followup-summary.json](ri-followup-summary.json) | Explicit counts and incomplete RI-domain disposition |
| [ri-followup-experiments.jsonl](ri-followup-experiments.jsonl) | Same606 indexed paths;48 full substantive mechanism/export reviews; unread roles remain provisional and prior selected review is not expanded |
| [ri-followup-fixtures.jsonl](ri-followup-fixtures.jsonl) |93 current RI test paths:3 full modules,29 outer-helper reviews,61 assertion-index only; unread test cursors remain explicit |
| [ri-followup-history.jsonl](ri-followup-history.jsonl) |203 older exact path/blob versions:26 tip-delta reviews,177 unreviewed; current implementation review does not inherit |
| [ri-followup-agent-use.json](ri-followup-agent-use.json) |31 additional original native Tool receipts from20/22/24; source/edit arguments bounded by hash; no causal benefit inference |
| [ri-followup-probes.json](ri-followup-probes.json) |Three independently authored primitive/fixture challenges; no scientific treatment/adjudication replay |
| [ri-followup-archive.json](ri-followup-archive.json) |All22 original root-report members checked against existing manifest without extraction; not judgment-cell review |
| [ri-followup-validation.json](ri-followup-validation.json) |Exact changed source/test hashes, final protected-gate log references and input-manifest digest |
| [ri-followup-checkpoint.json](ri-followup-checkpoint.json) |Changed-document physical hashes, Intake receipts and preservation/integrity validation; containing commit supplies manifest identity |

This overlay is research metadata, not new execution, source identity or backlog
authority. Complete remaining paths and blobs are enumerated rather than hidden
behind a collection-level completion claim.

## Scientific bindings and retrieval-policy review overlay

The [policy/integrity report](../ri-policies-and-scientific-integrity-audit.md)
starts at `bb2663ff2a04dd684349d112324c134782977328`. Separate read-only verifier
commit: `0cc372503e8efbd899b3e0f724c903d8ebd040a2`. Original science is unchanged.

| File | Depth and limits |
| --- | --- |
| [ri-integrity-summary.json](ri-integrity-summary.json) | Same606 experimental paths:94 full,512 remaining;93 fixture paths:9 full,28 outer-only,56 assertion-only. Includes namespace paths, not independent algorithms. |
| [ri-integrity-experiments.jsonl](ri-integrity-experiments.jsonl) | Exact path/blob overlay with46 newly inspected full bodies and dependency limits. |
| [ri-integrity-fixtures.jsonl](ri-integrity-fixtures.jsonl) | Six newly reviewed current paths including two namespace files; full grounding/graph/map bodies and consumed helpers. |
| [ri-integrity-reviewed-additions.json](ri-integrity-reviewed-additions.json) | Read tests/helpers outside original606, new repair hashes and partial dependency cursors. |
| [ri-integrity-history.json](ri-integrity-history.json) | Four additional Graph3 experimental deltas; not subtraction from177 older current-RI versions. |
| [ri-integrity-original-bindings.json](ri-integrity-original-bindings.json) | Four manifest-authenticated original members:96 canonical bindings agree; no historical corruption established. |
| [ri-integrity-report-references.json](ri-integrity-report-references.json) | Two original report members and retained input links; Increment24 filename references do not supply Increment23's complete input-digest closure. |
| [ri-integrity-intake.json](ri-integrity-intake.json) | One pending exact-acquisition proposal, ten ADVISORY additions across nine existing records; no approvals. |
| [ri-integrity-next-cohort.json](ri-integrity-next-cohort.json) | Exact158 experimental paths in next RI cohort and84 current fixture paths lacking full review. |
| [ri-integrity-checkpoint.json](ri-integrity-checkpoint.json) | Changed-path hashes, validation/preservation checks; containing commit binds itself. |

RI remains active. No new native model receipt or empirical-effectiveness claim
follows from synthetic tests. Keep preceding ledger versions as dated evidence.

## Increment implementation and consumer review overlay

The [64-path increment report](../ri-increments-25-36-audit.md) starts at
`c6bd9ae30390d7804ed44303cb2f73a1d2907e67`. Frozen experimental implementations,
judgments, reports and previous ledgers are unchanged.

| File | Depth and limits |
| --- | --- |
| [ri-increments-summary.json](ri-increments-summary.json) |64 selected paths:53 substantive modules/11 markers,64 distinct blobs;17 named review topics, not independent trials; cumulative158/606,448 remaining. |
| [ri-increments-experiments.jsonl](ri-increments-experiments.jsonl) | Same606 paths; exact64 newly reviewed bodies, functions, controls, tests, scientific limits and consumer/disposition crosswalk. |
| [ri-increments-tests-and-dependencies.json](ri-increments-tests-and-dependencies.json) |50 fully read external test paths (40 substantive/10 markers), four complete dependency bodies and bounded current consumer cursors; no historical controller/test replay. |
| [ri-increments-artifact-identities.json](ri-increments-artifact-identities.json) |97 physical JSON/gzip/document identities with13 retained result summaries; read-only accounting, not rejudgment. |
| [ri-increments-probes.json](ri-increments-probes.json) | Complete independent probe source/outcomes: prefix truncation, resealed25 swap,51 original bindings, eight coordinate failures, absent dense/ties/foreign inputs. Original Git-byte identity proof included. |
| [ri-increments-intake.json](ri-increments-intake.json) | One new pending task-authoring bug; seven ADVISORY updates; no approvals or B-numbers. |
| [ri-increments-next-cohort.json](ri-increments-next-cohort.json) | Exactly94 dogfood0012/0013/0016 paths with unchanged blobs/depth;84 current fixtures and177 older versions remain separate. |
| [ri-increments-checkpoint.json](ri-increments-checkpoint.json) | Changed-file hashes, deterministic/preservation/link/layout/Intake checks; containing commit supplies its own identity. |

No new actual model-use evidence or controlled benefit follows from this overlay.
All64 path dispositions are substantive review claims with per-file dependencies,
not claims that every human judgment or omitted historical version was audited.

## Dogfood lifecycle and scientific-integrity overlay

The [Cases0012/0013/0016 report](../ri-dogfood-lifecycle-audit.md) starts at
`7652d125e2743140a7d90b4da08ef8e893095d86`. Original failed captures, recovered
captures, authored primary/independent reviews and final reports are unchanged.

| File | Depth and limits |
| --- | --- |
| [ri-dogfood-summary.json](ri-dogfood-summary.json) |94 paths/87 blobs:84 substantive paths/79 blobs,10 namespace paths/eight blobs,19 full test bodies;15 named lifecycle boundaries are not independent trials. Cumulative252/606,354 remaining. |
| [ri-dogfood-experiments.jsonl](ri-dogfood-experiments.jsonl) | Same606 paths with94 newly full-body dispositions, exact functions, original/recovery roles, test semantics, scientific outcomes and consumer/backlog crosswalk. |
| [ri-dogfood-tests-and-dependencies.json](ri-dogfood-tests-and-dependencies.json) |19 complete cohort test/fixture bodies and targeted dependency/current consumer identities. No inherited84 current-test or177 older-version credit. |
| [ri-dogfood-artifact-identities.json](ri-dogfood-artifact-identities.json) |3052 retained artifact identities,3026 manifest checks, ten Git seal anchors,744 original Git member checks; two current prose mismatches resolved against original Git bytes; original qualified pair joins agree. No native pickle or report reconstruction. |
| [ri-dogfood-probes.json](ri-dogfood-probes.json) | Complete independent source/eight outcomes: U2 downstream null crash, Graph3 subset-verifier flag/prose limitations, five genuine packet identity refusals. No historical verdict corruption demonstrated. |
| [ri-dogfood-intake.json](ri-dogfood-intake.json) | One new pending versioned-analysis bug; eight append-only ADVISORY records, no approvals or B-number changes. |
| [ri-dogfood-next-cohort.json](ri-dogfood-next-cohort.json) | Exact101 remaining Case0011/0014/0015 paths and blobs; no review credit or scientific execution. |
| [ri-dogfood-checkpoint.json](ri-dogfood-checkpoint.json) | Changed documentation/Intake hashes, identity/test/layout/link/preservation validation. Containing Git commit supplies manifest identity. |

94 path dispositions are not87 algorithms. Duplicate immutable bodies retain
chronology without duplicate algorithm credit. All original conclusions remain
bounded, and the separate older Graph3 algorithm deltas remain delta-only.

## U1 R1.7 and R2 source and consumer overlay

The [Cases0011/0014/0015 report](../ri-u1-r17-r2-audit.md) starts at
`555b23b13e729fcf1464b581040f8a22223cb983`. Frozen case/source/report bytes and
all preceding audit ledgers remain unchanged. This is research metadata, not a
new source registry, semantic reviewer or execution authority.

| File | Depth and limitations |
| --- | --- |
| [ri-u1-r17-r2-summary.json](ri-u1-r17-r2-summary.json) |101 paths/96 blobs;91 substantive paths/87 blobs,10 namespace paths/nine blobs,24 full test bodies; three primary research mechanisms, not101 algorithms. Cumulative353/606,253 remain. |
| [ri-u1-r17-r2-experiments.jsonl](ri-u1-r17-r2-experiments.jsonl) | Same606 paths; exact101 new dispositions,741 function cursors, source/test/control/recovery/consumer and main-blob relationships; all other prior records unchanged. |
| [ri-u1-r17-r2-tests-and-dependencies.json](ri-u1-r17-r2-tests-and-dependencies.json) |24 complete cohort test/fixture bodies and separately qualified external scoring/consumer dependencies; no inherited current-fixture/older-version credit. |
| [ri-u1-r17-r2-artifact-identities.json](ri-u1-r17-r2-artifact-identities.json) |268 original byte identities,245 manifest checks,nine Git seal anchors,676 original Git-member checks and1561 frozen-archive resource occurrences; U1 CRLF archive and C.5 supersession explicit;4779/3090/3090 original pair joins agree. No scientific replay or pickle load. |
| [ri-u1-r17-r2-probes.json](ri-u1-r17-r2-probes.json) |Complete source/fourteen bounded outcomes: U2 null failure, Graph3 assurance limits, five packet refusals, gate/empty-field and numeric examples. No historical verdict corruption claimed. |
| [ri-u1-r17-r2-intake.json](ri-u1-r17-r2-intake.json) |One distinct pending Graph3 report-assurance bug and ten ADVISORY updates. No approvals, grants or status changes. |
| [ri-u1-r17-r2-next-cohort.json](ri-u1-r17-r2-next-cohort.json) |Exact42 remaining paths:Case0009/0010, retrieval diagnostics and BM25 sensitivity. Separate84 current fixtures and177 older versions retained. |
| [ri-u1-r17-r2-checkpoint.json](ri-u1-r17-r2-checkpoint.json) |Changed documentation/Intake hashes, synthetic tests, links, source/blob/forensic/input and Intake validation; containing commit supplies final identity. |

U1 authoring coverage, R1.7 score discrimination and true BM25F are distinct
research questions. Current native source use does not demonstrate autonomous
obligation decomposition or effectiveness of either intentionally unpromoted
scorer. All101 old experimental blobs also present on main remain experimental
archives, not production adoption.

## Lexical diagnostics and sensitivity overlay

The [42-path report](../ri-lexical-sensitivity-audit.md) starts at
`45d666cd168a6add2e59bbdf2e1b10e1fb82ada6`. The accompanying
[obligation-coverage decision preparation](../task-obligation-coverage-decision.md)
is a recommendation awaiting maintainer decision, not an accepted ADR.

| Artifact | Scope and review depth |
| --- | --- |
| [ri-lexical-summary.json](ri-lexical-summary.json) |42 paths/42 blobs;37 substantive paths,five namespace surfaces,four cohort test modules; three primary mechanisms,207 function cursors. Cumulative395/606,211 remain. |
| [ri-lexical-experiments.jsonl](ri-lexical-experiments.jsonl) |Same606 paths, exact42 new applicable full-body dispositions; other prior depths unchanged. Current/main historical blob equivalence is not production adoption. |
| [ri-lexical-tests-and-dependencies.json](ri-lexical-tests-and-dependencies.json) |Four cohort tests and eighteen fully read external test/helper paths; current consumer dependencies have precise full/partial ranges. No automatic current-fixture/older-version credit. |
| [ri-lexical-artifact-identities.json](ri-lexical-artifact-identities.json) |131 artifact identities,107 manifest checks,ten original Git anchors,530 member checks,1062 corpus occurrences and4779/5310 original pair joins. Missing Case0009 instruction custody explicitly qualified. No science replay or pickle load. |
| [ri-lexical-probes.json](ri-lexical-probes.json) |Ten independent bounded outcomes with full source: bounded nonprefix defect, real identifier arithmetic and scoped readiness despite omitted fixture clause. |
| [ri-lexical-intake.json](ri-lexical-intake.json) |One new pending bounded-prefix diagnostic bug and five append-only ADVISORY records. No approvals, grants or closures. |
| [ri-lexical-next-cohort.json](ri-lexical-next-cohort.json) |Exact78 remaining paths: Cases0004–0008, shared capture/package and verification. Separate84 current fixtures and177 older versions preserved. |
| [ri-lexical-checkpoint.json](ri-lexical-checkpoint.json) |Changed documentation/Intake hashes and final link/layout/identity/Intake validation. Containing commit supplies publication identity. |

R1's separate-view mixed result and prospective sensitivity's NO SAFE REPLACEMENT
remain bounded original conclusions. Native canonical BM25 is consumed; these
experimental policies and gold-conditioned diagnostics are not adopted rankers.
The whole-task/obligation authorship seam requires the explicit maintainer
decision above; scoped readiness is never proof of exhaustive task decomposition.

## Acquisition structural and verification overlay

The [Cases0004–0008 and shared verification report](../ri-acquisition-structural-verification-audit.md)
starts at `9ecf3ff81933e84b5300ada87164b9e2afca13d3`. Original scientific
source, reports, judgments, forensics and all earlier ledgers remain unchanged.

| Artifact | Scope and depth |
| --- | --- |
| [ri-acquisition-summary.json](ri-acquisition-summary.json) |78 paths/78 blobs;74 substantive paths including23 complete test/fixture modules, four namespace surfaces; five primary case policies and seven shared verification responsibility groups. Cumulative473/606,133 remain. |
| [ri-acquisition-experiments.jsonl](ri-acquisition-experiments.jsonl) | Same606-path universe; exactly78 applicable full-body dispositions and681 function cursors, distinct original/recovery roles, test/consumer/backlog scopes. All other prior records unchanged. |
| [ri-acquisition-tests-and-dependencies.json](ri-acquisition-tests-and-dependencies.json) |23 cohort test modules, exact dependency/source bodies or targeted ranges. No transferred84 current-fixture or177 older-version credit. |
| [ri-acquisition-artifact-identities.json](ri-acquisition-artifact-identities.json) |193 retained byte identities,71 member checks,22 original ancestor anchors,934 Git-object/member checks,2588 resource occurrences and exact ordered population joins. Case7 physical mixed newlines versus Git LF equivalence explicitly separated. No pickle or scientific replay. |
| [ri-acquisition-probes.json](ri-acquisition-probes.json) | Full independent source/results:25 source-span mismatches/nine ordinary controls, one ambiguous recovery reset, Case4 required-population leakage and Case8 cross-obligation marginal-unit counterexample. Actual retained-field versus synthetic impact qualified. |
| [ri-acquisition-intake.json](ri-acquisition-intake.json) | Four distinct new pending bugs; eight append-only advisory updates. Existing approvals, grants, payloads and statuses preserved. |
| [ri-acquisition-next-cohort.json](ri-acquisition-next-cohort.json) | Exact37 remaining structural-discrimination and Case0017–0019 reviewer/packet paths; all133 remaining experimental paths also enumerated. Separate84 current-fixture/177older-version obligations retained. |
| [ri-acquisition-checkpoint.json](ri-acquisition-checkpoint.json) | Changed documentation/Intake identities and actual focused/layout/link/identity/Intake/preservation validation. Containing commit binds this file's identity. |

All78 exact historical blobs also occur on main; that is archive presence, not
production adoption. Positive source facts differ from unpromoted routing,
candidate expansion and gold-conditioned completion policies. The obligation
coverage recommendation remains unapproved; this checkpoint adds delegable
review and explicit future agent-proposal/review requirements without implementing
them. RI and the repository-wide audit remain incomplete.
