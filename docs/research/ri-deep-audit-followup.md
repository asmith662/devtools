# RI implementation and fixture audit follow-up

Later checkpoint: [scientific integrity and retrieval policies](ri-policies-and-scientific-integrity-audit.md).
It supersedes this dated report's next-domain recommendation: continue the
remaining RI cohort first. Original scientific outcomes and this checkpoint's
coverage/validation claims remain historical.

## Result and limits

Starting feature checkpoint: `38957ae45d8f5c3e6b8061b749b9291f38cee19c`.
Protected remote main: `5d979920d0728775ed529457c88f5b68b440c64f`.
The Codex-authored source-index correction is committed separately at
`a0a6c22403f7df2679aa574226e420521a8accf5`. Main is not an integration target
for this assignment. No inference, scientific treatment, confirmation judgment,
historical execution, source-tree duplication or cleanup was performed.

This extends the [first RI audit](repository-intelligence-code-audit.md) and its
[existing coverage ledger](code-audit/README.md). It does **not** complete the
historical RI audit or the comprehensive repository review. The inherited census
is unchanged; this checkpoint adds exact-version review depth rather than
recounting branches or treating current replacements as reviewed old code.

The follow-up substantively inspects 48 experimental Python paths, including
namespace/export surfaces, across seven explicitly named groups. It reviews all
26 differing RI source/test versions found on historical tips by their actual
diffs against already inspected current implementations. It adds outer-fixture
review for 29 current RI test modules, with full test/fixture review explicitly
recorded for three modules. The remaining 61 of the 93 current indexed RI test
paths still have assertion-index depth only. These counts include namespace
files and must not be presented as 48 independent algorithms or 93 complete
fixture reviews.

Three independent synthetic challenges establish additional reporting/input/test
deficiencies. None reopens a scientific decision. Three additional original
native series supply 31 Tool receipt files, with no additional graph or
Localization adoption evidence.

## Corrected physical-line source index

Owner: [source representation](../../src/devtools/context/retrieval/source/representation.py).
The prior immutable [27-case reproduction](code-audit/physical-line-reproduction.json)
found 24 wrong symbol extractions and three passing space controls. Before the
repair, the new permanent regression failed on valid VT-containing source:
source index text began `\ndef target()` instead of the literal declaration.
The failure was reproduced before changing production source.

`str.splitlines()` recognizes VT, FF, FS, GS, RS, NEL, LS and PS as line
boundaries. Python AST physical coordinates do not. The smallest correction
uses `StringIO(content, newline="")`, already used by the maintained
[function materializer](../../src/devtools/context/python/function/materialization.py)
and map-source adapter. It preserves LF, CRLF and CR without translating them.
Symbol byte-offset calculation, window construction and displayed start/end
lines now use that same convention. No parser, identity authority, helper
hierarchy, source scope, admission rule or line-ending normalization was added.

The source-index namespace remains unchanged: inputs that already produced
correct coordinates retain their identity inputs. Previously wrong spans yield
corrected coordinate/content-derived unit identities; old erroneous identities
are not made authoritative. Retained resources and native declaration
occurrences keep their existing semantics. A source unit is still evidence,
not editing permission.

[Permanent regressions](../../tests/context/retrieval/source/test_physical_lines.py)
contain 81 cases:

- Original 27 literal extraction expectations, checked against real retained
  source, native AST occurrence ranges and Planning materialization.
- Forty-eight non-Python window cases: eight non-newline separators, three
  physical newlines and presence/absence of a final newline. Expected windows
  are authored from physical lines, rather than computed with the implementation.
- Six Unicode nested/decorated async cases covering parenthesized decorators,
  method/native declaration range differences, nested lexical symbols, parent
  expansion, UTF-8 endpoints and empty resources.

This does not silently redefine decorator meaning: source-search expansion
includes the selected decorator prefix, while the native declaration's range
starts at its header. Tests assert that distinction explicitly.

Validation: **224 focused tests passed**, scoped Ruff and formatting passed,
strict mypy passed for 517 files, layout and Git whitespace passed. The canonical
protected gate on the final coherent source/test tree returned **2,744 passed,
two skipped, 100% production branch coverage**. Host duration was 13m31.018s;
pytest reported 809.18s. A sandbox cache denial occurred before the actual gate
and was rerun using the existing authorized uv cache; no test waiver occurred.

[Validation identities](code-audit/ri-followup-validation.json) record the exact
source/test/documentation SHA-256 values, runner/configuration hashes, complete
log references and the digest of the 659-Python-input hash manifest. Those
inputs were authenticated before and after the gate and again for publication.
No later production/test changes are part of the research checkpoint.

The two existing source-span proposals retain their payloads, identities,
reviews and pending dispositions:
`416658bd-8ab9-43c4-bbb3-98a18a88cd4d` and
`5aa7a431-fd3c-4d46-a3a2-cb4e59e9c28e`. Explicit maintainer assignment authorized
this repair; recording implementation evidence is not proposal approval,
duplicate merging, parent closure or a newly issued grant.

## Reviewed historical mechanisms

The [606-path overlay](code-audit/ri-followup-experiments.jsonl) records exact
Git blobs, physical hashes, family overlap, implementation roles and inspected
function ranges. Roles of unread files remain provisional filename/AST triage.
Role labels do not promote those files to semantic review. Full substantive
review excludes comments/docstrings; dependent original cases, controllers and
tests have their own review status rather than inheriting the algorithm's.

| Source group inspected this checkpoint | Algorithm, control and failure semantics | Maintained relationship and disposition |
| --- | --- | --- |
| `experiments/address_lexical.py` | Independent filename/full-path lexical fields, additive weights, fixed authored controls and calibration/promotion gates. Actual repository comparison calls the canonical baseline; illustrative `_controlled_matches` uses content term counts and is not production BM25. Native address evidence is distinct from content. Lost-address report projection has the independently reproduced wrapper-serialization defect below. | Canonical filename-stem weighting is maintained; experimental full-path/weight-search arms are not new defaults. Toy controls are intentional illustrations, not agent-benefit evidence. Keep frozen reports. |
| `experiments/import_relationship/` and `import_relationship_cases.py` | Four explicit module roots, bounded actual observation, syntax parse-error accounting, qualified import-resolution relations, one-hop incoming/outgoing surfaces from one/three seeds. Fixed-five insertion protects only the first lexical result before relationship additions. Gold is used for evaluation, not relation derivation. | Maintained declaration/import facts survive; this early insertion policy differs from later protected-rank reservation. Do not describe all import studies as the same policy. |
| `experiments/purpose_relative_import/` | Explicit needs and useful/not-useful/unjudged judgments; lexical top15, top3 relation seeds, directional consideration universes, oracle size-five upper bound and blind insertion. Same query/different purpose leaves native universe unchanged before labels. Full corpus roots/parse exclusions are retained. | Oracle headroom is not an implementable selector. Native import facts do not confer semantic relevance or task completeness. |
| `experiments/purpose_relative_admission/` | Authored local/incoming/outgoing profiles, at least two distinct relation supports, protect ranks1–4 and replace rank5 only; abstain for local/no-qualified cases. Direct exact-name controls stay outside heterogeneous K5. Independent validation separates capture, blind material package, neutral mapping and frozen adjudication. Unjudged prevents definitive metrics; a contradicted negative-control expectation is retained alongside the blind USEFUL judgment. | Zero net known-useful gain and one useful loss remain historical findings; not production admission. Artifact identity checking is real but has the canonical mapping gap below. No original adjudication was rerun. |
| `experiments/purpose_relative_ranking.py` | Six grouped needs, no credible learning split, no learned model fit. Canonical, lexical15-truncated, purpose-agnostic and deterministic profile ordering keep evaluator labels out of ranking. Purpose-relative-without-relationships deliberately shares agnostic ordering. Reports retain unresolved precision and no cross-repository claim. Loader joins retained mapping/record positions. | Descriptive offline ordering remains unpromoted. Shared control ordering is intentional; positional joins need the canonical-binding integrity qualification below. |
| `experiments/codex_dogfood/acquisition/` | Caller-authored InformationNeeds/query batches bind task/obligation/provenance; they do not derive complete needs from prose. Inspecting those definitions cannot establish authoring adequacy. | U1's INFORMATION_NEED_AUTHORING_DEFECT remains adverse: needed units were never requested. No native general task planner is implied by these types. |
| `experiments/codex_dogfood/semantic_resolution/` | Exact candidate/member identity, bounded retained citations, attached native support, structured argument, explicit abstention and producer provenance. Human ACCEPT review is required for materialization. Ledger separates unprocessed, unreviewed, accepted and materialized records. Parser rejects duplicate/extra JSON fields and foreign support handles; freeze uses existing no-overwrite filesystem writer, replay requires exact serialized bytes. | The experiment adapts maintained witness/member resolution. A valid citation plus nonempty argument does not prove the criterion true. Retain review and unresolved states; not an autonomous semantic resolver or publication path. |
| `experiments/identifier_sparse/`, `retrieval_identifier.py` | Whole identifier plus deduplicated snake/camel/acronym/digit pieces, distinct query terms, postings/native BM25 primitives, additive .25 filename field in sparse R1. Older script owns independent BM25 arithmetic/control fixtures. Ranking never reads judgments; matching ties retain collection order. Empty fields/positive bounds are explicit. | R1 remains a separate experimental view, not canonical tokenization. Its per-query filename index is a reuse-investigation call site, not measured performance proof. Authored controls and real-repository comparisons differ. |
| `experiments/bm25f/` including its two test modules | True R2 normalizes content/name independently, unions document frequency, weights TF before one saturation, preserves candidate identity and replays score provenance. Tests include an independent numeric log(2) oracle, single-field equivalence, disjoint/overlapping fields, empty names, duplicated query observations, frame/score tamper, mismatched candidate sets and gate precedence. Lossless float-hex trace avoids display-rounding ambiguity. | BM25F_HARMFUL remains adverse; canonical independently saturated field scoring is unchanged. `repr` seal is local experiment tamper evidence, not a durable source/cache authority. Trace counterfactual terms explain a delta; they are not additional trials. |
| `experiments/mechanism_routing/` including policy tests | U3 classifies only frozen public prefixes `Inspect existing`, `Introduce new`, `Understand`. Plan replay checks forgery/duplicates/mixed arms, exact request coverage and task/lane provenance. Explicit no-hint/unsupported paths preserve lexical fallback. Tests exercise actual small observed source, exact resolution and lexical preservation as well as gate boundaries. | Local selective-routing support does not establish open-ended natural-language intent inference. Exact native grounding is maintained; this authoring grammar is not silently installed in the coding worker. U2's full extraction/presentation implementation still needs separate completion. |
| `experiments/increment_25/confirmation.py` | Checks partition disjointness and rejects development/reserve case execution in confirmation mode; validates exact ordered output population. Source corpus and one-facade expansion come from the development implementation. Historical execution creates temporary snapshot directories; none was invoked in this audit. | Confirmation findings remain original evidence. Reading boundary guards does not count as rereading every imported generator or confirming its full failure behavior. No old operational authority was reused. |
| `experiments/increment_26/development_evaluation.py` | Pins candidate/judgment/blind bytes and exact development order; equal distinct-resource capacity, positive lexical ranks, canonical neutral IDs, overlap and lexical reachability checked. Explicit UNJUDGED persists through aggregate surfaces. No embeddings are executed here. | Stronger local input binding than the earlier free mapping join. Dense configuration remains experimental and suspended confirmation stays suspended. Generator/embedding/controller bodies retain their prior selected-only depth. |
| `experiments/increment_31/mechanics.py` | Exact observed source↔test paths, no initializers or unmatched inferred targets. Five saved positive seeds; retain every path support, exclude original seeds, compare novelty against imports/references/containment/all saved lexical ranks. Pins parent/source metadata and development population; records no judgments loaded/heldout execution. | Maintained mirror fact is weak correspondence, not test ownership or coverage. Novel candidates are not automatically relevant. Future reuse should call the maintained derivation only after exact rule/identity compatibility is established. |
| `experiments/increment_36/mechanics.py` | Fixed source hashes, matched case/query/parent/corpus inputs; standard RRF k60 over lexical-RRF and dense where available. No dense for16 cases means one-list order; unranked structural facts and overlapping lexical channels are explicitly excluded. Freeze precedes usefulness outcomes. | Ranked-only fusion is coherent; useful73 versus lexical-RRF74 does not justify replacement. No guessed structural ranks, automatic selector or new agent-effectiveness claim. Full result-analysis/helper review remains separate. |

Known adverse or mixed policies remain unpromoted: rank-five reservation,
query-term attenuation/discrimination default, true BM25F, Graph3 incoming-flow
ranking, uncapped Graph1/Graph2 expansion and heterogeneous-oracle selection.
U2/U3 local positive results remain bounded to their authored tasks. The prior
case ledger is still the source for original numerical outcomes; this follow-up
adds implementation understanding rather than new trials or adjudication.

## Three independently demonstrated deficiencies

[Synthetic probe evidence](code-audit/ri-followup-probes.json) preserves expected
and actual behavior, exact inputs and the hash of complete local output. The
probe uses small authored fixtures and the existing implementation, not frozen
scientific case execution.

| Priority / finding | Actual consequence and qualification | Required disposition |
| --- | --- | --- |
| P1 canonical unblinding binding | Swapping two addresses in an otherwise bijective neutral mapping is accepted by `unblind_records`; USEFUL and NOT_USEFUL attach to opposite addresses while the frozen fingerprint is unchanged. Cardinality, address-set and neutral-ID-set checks do not authenticate each pair. | Pending bug: authenticate canonical capture/address→neutral binding at both unblinding and positional ranking-loader boundaries. Original externally pinned artifact hashes may protect real historical executions. No claim of historic tampering or invalidated science. Preserve frozen bytes; use versioned derived checking. |
| P2 synthetic fixture identity ambiguity | Lexical `_document("a", "bc")` and `_document("ab", "c")` have identical document IDs because `_digest` concatenates unframed parts. Some Localization fixtures also deliberately reuse caller snapshot IDs with different resource tuples. | Pending fixture maintenance: unambiguous synthetic IDs and a real observation-to-localization integration boundary. This is not a production content-hash collision. Keep explicitly forged frames and arithmetic fixtures where useful. |
| P3 legacy loss reporting | `_address_payload` serializes the retrieved-resource wrapper, giving a 1,532-byte nested representation instead of `lost.py` in its address list. | Pending bounded report-adapter bug: derived address-only reporting if still consumed; otherwise documented retirement/no-action. Preserve original reports and numerical findings. No new benchmark required. |

No other maintenance proposal is inferred just from module size, repeated class
names or an unsupported semantic fact. Unjudged, abstention, no learned model,
no runtime call proof and negative policy non-adoption are verified no-action
decisions.

Canonical Intake receipts (all **PENDING_REVIEW**, no assigned B-number):

- [2e70de9a-d09c-409d-a7a2-0f32f67c4768](../backlog/proposals/2e70de9a-d09c-409d-a7a2-0f32f67c4768/proposal.json): canonical neutral/address binding.
- [a88167f9-2688-478c-9659-202d05e61e1e](../backlog/proposals/a88167f9-2688-478c-9659-202d05e61e1e/proposal.json): fixture identity and observed-input coverage.
- [befd10cd-f382-4f40-aade-5c4119db4c44](../backlog/proposals/befd10cd-f382-4f40-aade-5c4119db4c44/proposal.json): legacy lost-address report projection.

The two original source-span proposals receive repair evidence only. The four
existing RI integration/reuse proposals receive the acceptance qualifications
below. Original22 proposal payloads, dispositions, prior reviews and parents
remain intact; six additional reviews are ADVISORY. Existing B-0002/B-0008,
B-0009 and B-0027 pressure remains related, without automatic implementation
dispatch or broader closure. These are suitable bounded maintenance-agent
obligations only after approval and independent input/negative-case qualification;
the historical integrity case needs explicit frozen-artifact compatibility review.

## Test and fixture depth

The [93-path fixture overlay](code-audit/ri-followup-fixtures.jsonl) distinguishes
complete test bodies from outer helpers and unread inline monkeypatches.
Three full modules are the new physical-line tests, existing scoped-source
tests and role-input forgery/staleness tests. The latter use actual observation
and rederivation, including missing/changed analyses, membership/mirror and
configuration facts. Scoped-source fixtures include multiple resources, empty
and no-match scope, a stronger unselected lexical distractor, retained source
after disk mutation, malformed selection and file-population admission.

Outer helpers reviewed across repository, source/Planning, roles/grounding and
generation/association establish useful distinctions:

- Source `_index` writes exact UTF-8 bytes then discovers, observes, realizes a
  corpus and builds the actual index. It is not a fake parser or injected score.
- Role/configuration helpers use real retained observation and actual native
  declarations/resolution. They complement synthetic pure arithmetic frames.
- Generic branching `_run` monkeypatches `_project`, deliberately isolating
  child accounting, bounds and bad-support behavior. It does not demonstrate
  import/reference projection algorithms or agent adoption. Separate import and
  reference helpers build actual multi-resource native analyses for that purpose.
- Generation `_frame` and lexical `_collection` manually construct some nominal
  frames. Their identity/freshness conclusions need independent observed-input
  integration, captured by the fixture maintenance proposal. Do not “fix” a
  deliberately malformed negative fixture into a valid one.
- Repository Delta `_snapshot` uses observation but default `write_text` can
  translate LF on Windows. That fixture is adequate for its current simple
  content comparisons, not proof of exact cross-platform line-ending behavior.
- Existing source-window test assertions use `splitlines()` on ordinary CRLF
  fixtures and therefore missed non-newline separators. The new window expected
  strings are authored independently. Passing old tests was not sufficient.

No universal test framework was introduced. Remaining inline patches, complete
92-original-module fixture semantics and archived test versions are explicitly
unreviewed where the ledger says so. Protected coverage100% is execution
coverage, not semantic completeness of those fixtures.

## Historical blobs and artifact custody

[Historical exact versions](code-audit/ri-followup-history.jsonl) contains203
older RI/Evaluation source/test path/blob versions from the inherited universe.
Twenty-six tip deltas were read as actual unified source/test changes against
the inspected feature implementation. They comprise Delta exports, role semantic
version/project classification, Planning/map-source adapters, physical-line
function materialization/UTF-8 endpoint validation, structured-message rejection,
TOML obstruction/dependency groups, explicit discovery, RRF helper reuse,
caller-scoped source selection and their changed regressions.

Those reviewed changes are superseded in current feature source, not orphan
capabilities requiring another selective integration. In particular, the older
function materializer has the same physical-line problem already corrected in
its current replacement; the current source-index repair fixes the remaining
distinct consumer. Main adoption remains a separate destination-tree question.

**177 other older exact versions remain NOT_REVIEWED.** A delta review is not
full independent inspection of an entire older test module. The ledger retains
commit-array/tip references to the original census and names every remaining
path/blob. No historical ref was changed or checked out.

All22 original root-report members in the existing `archive.zip` were read in
memory and checked against `experiments/archive/manifest.json`: exact lengths
and SHA-256 agree. [Archive verification](code-audit/ri-followup-archive.json)
records each identity and top-level schema. Nothing was extracted, executed,
rejudged or deleted. Schema/hash verification is not full judgment-cell review;
earlier Increment10–24 report/code-version correspondence remains a visible
follow-up, not an inaccessible-evidence excuse.

## Additional native consumption evidence

[Additional receipts](code-audit/ri-followup-agent-use.json) extend the existing
six-series evidence without rewriting it:

| Original series | Tool receipts and operations | Supported conclusion |
| --- | --- | --- |
| Engineering20 `live-v2` |8 files;8 inspect_source,2 search_source | Real model acquisition, followed by original supervisor stop; no accepted implementation or graph/Localization invocation inferred. |
| New-module22 `live` |13 files;9 inspect_source,1 search_source,2 git_inspect,26 replace_source | Real source acquisition and model proposals. Individual edit calls are not26 transactions or successful edits; original admission/implementation failure remains authoritative. |
| Dependency-groups24 `live` |10 files;13 inspect_source,4 search_source,4 replace_source | Real investigation/candidate proposal stream; wrong-parent behavior and blocked repair remain original outcomes. No passing native validation or graph use inferred. |

Each event retains the original call ID, physical receipt hash, source version
fields where present and bounded source-argument hashes. Original source/code
payloads stay in local custody. These receipts contain no `repository_map`,
`source_relationships` or `check_changes` calls. They do not prove why a model
selected a Tool, semantic readiness, controlled effectiveness or successful
publication. Deterministic host RI construction and explicit model navigation
remain different claims.

## Cohesion and integration acceptance

No timing experiment or profiling workload was run. Source inspection identifies
real repeated computation, not a measured speedup: R1 rebuilds filename fields
per query; R2 explicitly seals reusable fields; older purpose-relative flows
rebuild module interpretation/import relations; role validation and semantic
request materialization replay exact native facts; native edits safely rebuild
the admitted source frame. Removing rederivation before qualifying the exact
input closure would weaken integrity.

Use the existing profiler for the pending reuse investigation. Its comparison
must include two real maintained consumers, runtime/grammar/analyzer versions,
roots/universe, cold/fresh/stale/error paths and equality of identities, order
and refusals. A task-scoped helper is a candidate only after that measurement;
R2's `repr` hash is not an appropriate new cache authority. Historical analyzers
with different lexical/binding rules must remain distinguishable.

The four existing integration proposals receive materially more explicit
acceptance evidence, not implementation or approval:

| Existing proposal | Additional acceptance / decision boundary |
| --- | --- |
| `15bae0a6-b95d-417c-98fa-d75a8aff29d4` Localization consumption | Real observed source→trusted task/obligation→bounded candidate/citation→explicit reviewed semantic decision→readiness→native model response. Preserve unresolved/unprocessed and distinguish generic monkeypatched branch accounting from actual projection. A citation/argument is not automatic truth; determine trusted caller/review surface before coding. |
| `cea1b3e7-bfa6-492a-b850-343a0c543878` direct bases | Use current qualified static base owner and exact roots/universe. Demonstrate native selected endpoint→exact source→current admissible edit, stale rejection/refresh and unsupported/decorated/shadowed refusals. No MRO or model-effectiveness claim from exposure. |
| `1d0ed8bb-e38e-44ea-8af3-530c2516981a` Delta consumption | Real observations and byte-preserving CRLF/CR/no-final-newline transitions, full occurrence partitions and old map/check/edit invalidation. Snapshot exclusion is not deletion permission. A safe full rebuild may remain; no cache assumption. |
| `aedea41e-804b-4fe0-ad53-8758e074885d` measured reuse | Parse/index/replay counts and timings for at least two actual consumers with exact input closure and unchanged refusals. Current source evidence identifies candidates but does not yet choose caching or assert savings. |

## Completion boundary and next audit

This checkpoint fixes the proven production bug and advances historical
mechanism/fixture review. It does not satisfy “every historical implementation
reviewed.” Exact remaining work is reproducible:

1. [Experimental overlay](code-audit/ri-followup-experiments.jsonl):558 paths
   have not received full-body follow-up review. Prior named algorithm reviews
   remain valid only for their exact functions. Prioritize U2 extraction and
   presentation, Graph3 complete controller/tests, Increment25 generator/freezes,
   Increment26 embedding/controller paths, Increment27–30 controls and
   Increment32–36 sampling/judgment/report bodies. No repeated case references
   become independent trials.
2. [Fixture overlay](code-audit/ri-followup-fixtures.jsonl):29 paths have outer
   helper review but unread full test bodies/inline patches;61 remain assertion
   indexed. Current source-search scope and role-input tests are reviewed fully;
   other Planning and native worker tests do not inherit that status.
3. [Historical overlay](code-audit/ri-followup-history.jsonl):177 exact older
   versions require semantic review;26 tip deltas still need whole older
   fixture/body review if a full-version claim is needed.
4. [Archive overlay](code-audit/ri-followup-archive.json):22 original report
   identities are verified; complete report/controller-at-recorded-revision
   correspondence and judgment-cell review are not completed by hashing.

The next substantial domain is **execution, ToolRunner, Checkout and WorkCycle**:
actual admission/dispatch boundaries, partial batches, cancellation versus
rollback, unknown external effects, source restoration, exact protected-gate
input closure/reuse, review authority and post-push observation. Reuse the
existing lifecycle/observability report and cross-branch ledger. Carry the
enumerated RI depth obligations alongside that domain; do not hide them or
prepare the postponed final successor-session dossier.
