# RI policies, scientific bindings and consumer audit

## Result and scope

This continues the [RI follow-up](ri-deep-audit-followup.md) from feature
`bb2663ff2a04dd684349d112324c134782977328`. Remote main remains
`5d979920d0728775ed529457c88f5b68b440c64f`. The separate Codex-authored repair is
`0cc372503e8efbd899b3e0f724c903d8ebd040a2`. This report does not reopen a
scientific judgment, authorize a policy promotion or finish the RI audit.

The [version overlay](code-audit/ri-integrity-summary.json) gives computed
counts; [experimental paths](code-audit/ri-integrity-experiments.jsonl),
[current fixtures](code-audit/ri-integrity-fixtures.jsonl) and
[historical deltas](code-audit/ri-integrity-history.json) identify exact bodies
and remaining work. Counts include namespace files and are not algorithm or
independent-trial counts. Earlier ledgers and frozen records remain unchanged.

Coverage advances from48 to94 full substantive experimental path reviews in the
same606-path universe;512 remain. Separately26 existing test/helper paths outside
that universe were fully read. Current fixture depth advances from3 to9 of93
paths: four substantive test modules and two namespace files were added;84 paths
still lack full review. Four additional experimental historical deltas are
recorded without reducing the separate177 unreviewed older RI versions.

No model inference, historical treatment execution, sampling, adjudication,
scientific report reconstruction, pickle loading, Checkout replay, protected-main
write, artifact cleanup or additional source tree was used. Existing policy
tests were read even where executing them would reconstruct historical results.

## Canonical binding defect and safe correction

The original process has five different identities, not one interchangeable
fingerprint:

| Boundary | Original owner | What is bound / what was missing |
| --- | --- | --- |
| Candidate population | `purpose_relative_admission/validation_capture.py` | Ordered lexical, eligible relationship, retained/admitted and adjudication addresses; checkpoint and case capture descriptor. |
| Neutralization | `validation_adjudication.build_blinded_adjudication_package` | For each material address, `resource-` plus the first16 SHA-256 hex digits of `design_fingerprint + "\u007c" + case_name + "\u007c" + address`. This provides a retained canonical pair anchor. |
| Blind package and freeze | `validation_adjudication` / `validation_execution` | Package evidence, protocol, capture/design and ordered records are fingerprinted. The hidden address map is not part of the frozen judgment fingerprint. |
| Envelope correspondence | `validation_execution.validate_artifact_correspondence` | Checks content envelopes and shared capture/design links; does not reconstruct the canonical pairs or mapping-set descriptor. Resealing a swapped map can pass. |
| Evaluation | `validation_evaluation.evaluate_frozen_case`, `validation_reporting.build_increment_23_report`, `purpose_relative_ranking.load_ranking_cases` | Original unblinding checks bijection and membership, not pair derivation. Increment24 joins mapping and frozen records positionally. Same sets are insufficient in both paths. |

The synthetic counterexample assigns USEFUL to `l1.py` and NOT_USEFUL to `l2.py`,
then exchanges only their mapped addresses. The original consumer returns the
wrong association under the unchanged frozen fingerprint. This is a confirmed
input-integrity bug, **not evidence of actual historical corruption**.

The original implementations remain frozen. The new experiment-specific,
read-only [verification_v1](../../experiments/purpose_relative_admission/verification_v1.py)
offers `verified_unblind_records` for native values and
`verify_artifact_bindings` for four supported retained JSON envelopes. Its
[contract](../../experiments/purpose_relative_admission/VERIFICATION.md) requires
canonical pairs and order before labels are returned for any new analysis.
It reconstructs original capture/mapping descriptors, checks supported schemas,
case membership/order, package/frozen correspondence, visibility and positional
record alignment. Incomplete or unsupported inputs fail closed; there is no
silent migration or fallback to unchecked unblinding.

This is a verifier of the original binding contract, not a new retrieval policy,
judgment, source authority or authenticity service. A caller must authenticate
original input bytes separately. A completely forged, consistently resealed
input population cannot become historical truth merely by passing consistency
checks. Original entry points remain unsafe for **new unauthenticated analysis**;
their continued presence is scientific custody, not an endorsed bypass.

### Authenticated historical impact

[Original binding evidence](code-audit/ri-integrity-original-bindings.json)
records exact archive, manifest and member hashes. Four original members were
read in memory from the existing preservation archive, checked against the
existing archive manifest, and passed through the new verifier. No member was
extracted, rewritten, ranked or rejudged.

| Original Increment23 case | Canonical pairs checked |
| --- | ---: |
| content-bm25-term-formula | 17 |
| baseline-lexical-analysis-definition | 15 |
| content-bm25-analysis-consumer | 15 |
| python-function-token-candidate-boundary | 19 |
| import-declaration-source-evidence-contract | 15 |
| repository-context-taxonomy-boundary | 15 |
| Total | 96 |

All96 pairs agree with their original capture, package and records. The raw
capture, package, mapping and freeze are the shared original inputs to the
Increment23 report and Increment24 ranking loader. This finding supports their
retained mapping consistency; it does not independently validate every label,
ranking, metric, controller execution or effectiveness conclusion. Earlier
unsupported package versions are deliberately not admitted by this verifier.

[Original report references](code-audit/ri-integrity-report-references.json)
authenticate both retained report members without rebuilding them. Increment23
embeds input raw hashes and content identities matching all four verified
members. Increment24 records source filenames/checkpoint, not the equivalent
complete per-input digest closure. Its source loader demonstrably uses these
artifact names, but that is code correspondence, not the same authenticated
report-to-input edge. Do not invent a stronger historical link. This limitation
is appended to the existing integrity proposal for future versioned analysis.

The new permanent tests cover swaps with unchanged sets, resealed mapping
envelopes, duplicate/missing/foreign bindings, altered neutral IDs, positional
reordering, changed visibility/questions, incomplete schemas and changed
capture/package/freeze identities. Positive tests preserve three-state labels
and inputs. Original historical tests covered duplicates and missing rows but
missed the bijective-swap challenge.

## Purpose-relative facts, selection and evaluation

The previous exact-version algorithm review remains the starting point; this
checkpoint adds the complete admission/import/ranking test bodies and relevant
producer/loader checks. The fixture overlay distinguishes synthetic values,
mocked branch accounting, real native parsing and outcome-dependent reports.

| Mechanism | Semantics and failure boundary | Disposition |
| --- | --- | --- |
| Import consideration universe | `purpose_relative_import.comparison` groups lexical and directional relationship surfaces without erasing repeated encounters. Unknown judgments remain UNJUDGED; a relationship is not usefulness. | Useful factual surface; no automatic useful-candidate claim. |
| Authored need/profile | `cases`, admission `design` and `validation_design` freeze purpose, query, controls and calibration/held-out partitions. Identical query text can have distinct needs and labels. Profiles are authored input, not model intent inference. | Keep task authorship separate from retrieval. |
| Blind insertion | Fixed relationship insertion can displace lexical resources. It is an explicit control, not an oracle or generally safe improvement. | Preserve adverse findings. |
| Reservation-v1 | Local profile abstains; incoming/outgoing profiles filter direction, count distinct supporting relation identities, require two, admit at most one nonlexical target at rank5 with deterministic ties. No usefulness input enters practical construction. | Do not promote adverse fixed-K replacement. A loss does not invalidate imports or references. |
| Oracle | `oracle_size_five` explicitly uses frozen usefulness after universe construction. It measures potential coverage, not a deployable selector. | Retain as labeled evaluation-only control. |
| Ranking | Increment24 features are lexical/native directional evidence; selector arms do not read usefulness. Labels are separate evaluation values. Unjudged candidates are excluded from definitive precision/pairwise comparisons, not converted to negatives. | Original policy conclusions remain bounded; binding verification precedes any new analysis. |
| Failure accounting | `validation_evaluation` distinguishes unavailable evidence, insufficient judgment, control exposure, qualification/admission, displaced useful resources and appropriate abstention. A test intentionally supplies a qualified-but-abstained result to exercise accounting; it is not proof the practical selector generates that state. | Preserve mechanical test scope and original NOT_READY_FOR_SHADOW / NOT_JUSTIFIED outcome. |

Tests for `construct_frozen_rankings` verify the API has no judgment/control
argument. That is useful separation evidence, not a complete proof against all
possible data leakage. The mocked aggregate test checks calibration exclusion,
not real native candidate projection. Direct-resolution tests are an isolated
route control and explicitly excluded from heterogeneous K5 metrics.

## U1, U2 and U3 implementation and controller review

U1's authored InformationNeed is a purpose linked to an existing obligation;
it is not itself a lexical query or inferred task completeness. Its complete
test module uses a real two-resource observed corpus for native BM25 calls,
checks one execution per selected lane and no fusion, and separately checks
trace mutation, packet whitelisting and gold/query withholding. Other tests
load frozen authored task files or verify retained traces. No whole historical
suite was executed here.

U2's entire `exact_hint_routing` package and tests were reviewed:

- Extraction examines task text only: bounded inline exact hints and introduced
  paths; fenced blocks and designated operational text are excluded. Generic
  prose, unqualified type names and unsupported syntax do not become exact
  repository knowledge. Task spans are character offsets, not source UTF-8 columns.
- Route admission accepts closed typed locator forms. `ExactFrame.validate`
  authenticates retained occurrence content, byte size, module interpretations,
  admitted addresses and native provenance. Grounding reuses maintained APIs.
  Qualified methods resolve their class first, then direct method evidence.
- Ambiguity remains ambiguity even if multiple declarations share one owner
  file. Decorated source declarations are source facts, not runtime binding
  identities. Missing, foreign, partial or inconsistent frames fail or abstain.
- Presentation promotes only uniquely resolved owner resources, in task-hint
  order. It retains complete obligation lexical fallback and the unchanged
  global task lane. It does not substitute symbol bodies or confer editing
  authority. Partial lexical lanes cannot be described as no-loss fallback.
- Behavioral equivalence removes only task-extraction authorship metadata for
  comparison; native facts, decisions, scores, order and evidence stay visible.
  Synthetic score fixtures test equivalence accounting, not BM25 effectiveness.

The newly inspected case0012 StageB controller restores native frozen inputs,
checks corpus/document identities, admits independently authored B hints and
mechanically extracted C hints, compares their route inputs and executes the
existing exact resolver/presenter. It journals entered/returned native calls,
restores monkeypatches in `finally`, rejects conflicting final evidence and
requires a complete schedule before finalization. Failure records preserve
UNKNOWN effectiveness and prohibit native retry. Reading this controller does
not certify all its durability, reporting or adjudication dependencies as fully
reviewed; those exact remaining files stay in the ledger.

The case0013 adapter rehydrates native resources and module interpretations,
checks universe/frame identities and frozen routing-purpose/decision equality.
U3's existing `mechanism_routing.policy` uses exactly `Inspect existing `,
`Introduce new ` and `Understand ` prefixes. Unknown grammar fails authorship.
It is not natural-language intent recognition. Baseline A is lexical-only;
B tries supported exact hints; C permits exact lookup only for inspect-existing
purposes. Unsupported exact syntax retains lexical fallback. Duplicate/foreign
need or hint links fail. A route permission does not establish satisfaction.

The positive bounded U1/U2/U3 findings do not establish an autonomous task
planner or a useful universal ranking policy. Current maintained exact
grounding already includes module, direct declaration and direct method
locators. Promoting another experimental locator hierarchy would duplicate
ownership. What is missing is a trusted caller-to-native-worker composition,
not another parser or Context compiler.

Original U2 closeout records `EXACT_HINT_ROUTING_SUPPORTED` for case0012;
U3 records `SELECTIVE_MECHANISM_ROUTING_SUPPORTED` for case0013. These remain
bounded case outcomes, not new measurements or general competence claims.

## Graph1, Graph2, Graph3 and maintained graph/map distinctions

### Expansion controllers and evaluation populations

The complete Increment32/33 algorithm, population, sampling, judgment and
analysis modules and all their test bodies were inspected. Graph1 expands one
additional edge from the frozen direct frontier; Graph2 adds exactly one more
edge from Graph1's novel frontier. Both reuse original import, reference/call,
immediate-package and mirrored-path producers, not a new graph engine.

Known lexical/direct surfaces and return-to-origin overlaps remain separately
accounted. Multiple paths preserve distinct native supports but do not create
multiple independent case/resource trials. Source/snapshot mismatches fail.
Unsupported and absent relationships do not become universal known negatives.
Historical Name-reference projection is narrower than the current generalized
reference owner; an experiment's policy is not identical to today's facts.

Graph1 retains704 novel pairs: two reused labels,128 sampled decisions and574
unjudged pairs. Graph2 retains987 pairs: two reused,128 newly sampled and857
unjudged. Its294,154 reconstructed novel typed paths are provenance paths, not
294,154 independent semantic judgments. Compact prefix/third-edge storage
avoids persisting all Cartesian paths, while counting still traverses them.

Both samplers use frozen neutral populations, fixed seeds and sampling without
replacement before new outcomes. Full identity includes purpose, query,
snapshot, address and usefulness semantics. Shared judgment coverage checks
compare each decision's full identity to its frozen neutral target, unlike the
set-only Increment23 unblinding defect. This still depends on authentic targets.

Graph1's judgment builder materializes two hardcoded USEFUL IDs and fixed
remaining NOT_USEFUL decisions. Reproducing it proves a frozen artifact is
reproduced, **not independent semantic adjudication quality**. Graph2 accepts
explicit complete decisions. Neither analysis assigns negatives to unsampled
pairs. Wilson intervals are documented binomial approximations without finite
population correction. Graph2's zero useful sampled decisions do not establish
zero useful candidates in its entire population.

Mechanics tests supply synthetic edges and assert depth limits, novelty,
deduplication and snapshot rejection. The Graph1 direction test mocks all four
RI producers; it verifies projection of supplied facts, not real parsing or
resolution. Graph2's eight-direction fixture has the same limit. Artifact tests
also reconstruct historical results, so they were inspected rather than run.

### Task-conditioned flow and original versions

Graph3's full policy, view, evidence, diagnostics, seed and test bodies were
reviewed. It takes resolved native reference occurrences, deduplicates fact
identities, rejects conflicting occurrence support and uses sqrt(pair occurrence
count) edge weights with normalized outbound probabilities. Seeds are the union
of up to ten positive lexical resources and explicit exact-query resources;
no seed means abstention. No usefulness labels enter graph construction/ranking.

It reuses the maintained stationary-distribution kernel, but its **ranked score
is incoming structural flow**, excluding restart and dangling-return mass.
Those masses remain in complete state evidence. Definition flow is divided
among native reference occurrences, checked against resource totals and retains
exact definition/source provenance. Diagnostic maps have explicit byte budgets
and omission status; they are not exact source or an effectiveness arm.

Four older exact Graph3 blobs were inspected by full deltas against inspected
current bodies. Earlier ranking used stationary mass, including unreferenced
seed mass, and earlier definition order was parent-first. The updated version
uses incoming flow and definition-flow order, with v2 evidence. These are
substantive superseded experiment realizations, not semantically identical code.
The historical ledger labels **delta review**, not full independent old-body
review. These four versions are additional experimental versions, not four
subtractions from the separate177 unreviewed older RI source/test versions.

The newly inspected case0016 execution/authentication owners bind amended StageA,
recovery, source hashes, clean exact Git checkpoint and full operation schedule.
They forbid preexisting gold/result contamination and retries, keep first-failed
attempt audit evidence separate, journal per-resource reference derivations,
and capture native PPR entry/return counts without rescoring in final reporting.
Live progress errors are nonauthoritative warnings; capture failures preserve
active and returned operations. No such controller was invoked in this audit.

### Baselines versus current production semantics

Complete `graph_ranking_baseline`, `typed_graph_baseline` and
`repository_map_baseline` source bodies were inspected. They call maintained
graph/map/fusion owners on a pinned retained case; labels are loaded after
rankings. Their gzip/pickle loaders require trusted original input custody and
are not suitable generic untrusted-artifact readers. No pickle was loaded here.

Typed baselines compare frozen forward facts, broader current references,
typed core and typed navigation. Core contains declarations/direct bases;
navigation adds membership/mirrors. Maintained PPR ranks stationary node mass
with maximum-per-resource collapse; it is not Graph3 incoming-flow ranking.
Repository-map diagnostics separately compare symbol lexical, global importance,
combined map and RRF channels, retaining winning symbols and native supports.
One development case and two query forms do not establish general effectiveness.
Do not transplant a negative automatic-expansion policy into native navigation,
or infer that such a result makes typed relationships useless.

Original Graph3 closeout explicitly records `GRAPH_HARMFUL`. It remains an
adverse development result, not a promoted production policy. No new judgment
or inference in this audit changes that disposition.

## Current fixtures and agent consumption

Full bodies and inline setup were reviewed for current grounding, graph ranking,
typed graph and repository-map ranking tests, including their actual `_facts`
and `_lexical` dependencies. Real tiny filesystem observation, parsing, import
resolution, references, bases and retained-source checks are present. Independent
two-node numerical expectations and explicit RRF arithmetic provide stronger
checks than deterministic self-equality alone. Equality/reconstruction tests are
still useful consistency tests, not independent effectiveness oracles.

Grounding's duplicate-method fixture changes `content` without changing content
identity/byte size; other fixtures correctly update both. Its synthetic snapshot
ID is also reused across mutations. This is concrete additional scope for
existing fixture proposal `a88167f9-2688-478c-9659-202d05e61e1e`, not a new
production identity conclusion. Graph ranking has two compatibility tests that
load original pickles; these were read but excluded from the bounded test run.

Current native `ContextTools.execute` dispatch was traced: `lookup_symbol`
matches qualified source-index units, `search_source` uses maintained source
search, `expand_source` selects an indexed enclosing unit or delegates a map
handle to current navigation, and `source_relationships` requires a current
content version. `RepositoryMapNavigation` uses existing map/Planning source
adapters. None is an authored InformationNeed/obligation/readiness consumer.

| Capability | Evidence category justified now | Missing step |
| --- | --- | --- |
| Source search and exact reads | Existing original native receipts show model-visible evidence and subsequent edits; prior outcome qualifications stand. | No new benefit claim. |
| Graph/map navigation | Maintained opt-in Tool exists and deterministic source/edit integration is tested. Prior original map-assisted attempts did not establish an uninterrupted benefit. | Actual successful native use and a later controlled comparison, separately authorized. |
| Exact authored hints | Native grounding exists; U2/U3 host experimental compositions and synthetic tests are real. | Trusted caller input to existing native lookup/read workflow, honest ambiguity/fallback and edit observations. |
| Localization witnesses/readiness | Maintained APIs and host experiments exist. | Existing pending consumer proposal: explicit decisions and output reaching a model, not automatic truth from rank. |
| Direct-base navigation | Maintained native RI/typed graph exists; worker navigation omits it. | Existing pending bounded source-navigation integration. |
| Delta / analysis reuse | Existing proposal scopes remain valid. | Real freshness-safe consumers and measured input-closure/cost evidence. |

No additional original model receipts were inspected this checkpoint. The prior
115-file native receipt evidence is not inflated by scripted regressions.
Offering a Tool does not prove invocation or influence; a host exact lookup does
not prove a model chose a strategy; no controlled effectiveness claim is added.

## Actionable dispositions and cohesion

[Intake evidence](code-audit/ri-integrity-intake.json) records canonical review
chains and the distinct new pending proposal. No approvals, grants, B-number
assignments, parent closure or proposal-payload rewrite occur.

| Finding | Disposition / acceptance direction |
| --- | --- |
| Canonical unblinding pair gap | Existing `2e70de9a-d09c-409d-a7a2-0f32f67c4768`: versioned repair and26 independent regressions implemented; original96 bindings verified. Authorized administration can reconcile status after reviewing exact scope; do not silently close. |
| Repaired source-span duplicate proposals | `416658bd-8ab9-43c4-bbb3-98a18a88cd4d` / `5aa7a431-fd3c-4d46-a3a2-cb4e59e9c28e`: recommend one canonical implemented-bug disposition and duplicate cross-reference, retaining both identities/reviews. Source repair and original exact protected evidence are already concrete; no new approval implied. |
| Explicit exact-hint worker consumer | Distinct pending enhancement referenced in Intake metadata: caller-authored bounded locator input, existing grounding/native source observations, complete fallback, no hidden ranking or satisfaction claim. Actual ToolRunner-to-edit-to-check acceptance required. |
| Grounding fixture identity mutation | Material ADVISORY addition to `a88167f9-2688-478c-9659-202d05e61e1e`: migrate dependent fixtures deliberately; distinguish intentionally forged negatives from asserted valid frames. |
| Localization/direct-base/Delta/reuse | Existing four concrete proposals remain pending; new evidence strengthens acceptance and ownership, not permission to implement. |
| Graph expansion/ranking adverse outcomes | Verified no automatic promotion. Preserve factual navigation; do not turn unsampled absence or a fixed-K loss into a language-model or RI-fact defect. |
| Fixed judgment materializer and artifact self-reproduction | Document scientific assurance limit; no label corruption shown, no rejudgment authorized. Future study must distinguish authored decisions, independent review and reproducibility tests. |

Repeated computations are visible in exact-frame native validation, module
universe construction, graph/map revalidation and separate historical controllers.
Some repetition is necessary stale/foreign-evidence rejection. No timing workload
was measured, and no cache or speedup is recommended without the existing reuse
proposal's exact input-closure and two-consumer measurement.

Small helper opportunities have actual consumers: Increment32/33 duplicate
sampling envelopes, population partitions and Wilson reporting while already
sharing `retrieval_judgment_coverage`; case0012 and0016 reuse a durable entered/
returned journal but add distinct schedules/progress/failure policies. The
minimum investigation is extraction of genuinely identical deterministic
serialization/partition mechanics with byte-compatible protocols and error
semantics. Do not merge distinct declaration, source, hint, judgment or witness
identities; do not generalize retired controllers into framework orchestration.
Existing cohesion/reuse proposals receive advisory evidence rather than another
generic framework story.

## Validation and remaining cohort

The bounded run passed **194 tests, two deliberately deselected**, including the
26 new binding regressions, shared full-identity coverage, U2/U3, Graph3 and
current grounding/graph/map tests. It did not run frozen-result reconstruction
or original scientific controllers. One initial command used a nonexistent
Graph3 tests directory and stopped before collection; the corrected explicit
paths passed. Scoped Ruff, formatting, strict typing, layout, document links,
JSON/ledger identity checks, canonical Intake hash chains and Git whitespace
are recorded in checkpoint metadata.

No maintained production source, application, controller-dispatch implementation
or protected test changed. The repair is a separately versioned read-only
experiment analysis utility with tests under `tests/experiments`; applicable
experiment-specific deterministic/static checks were run. The protected
production gate was therefore not rerun, and the earlier source-index gate is
not represented as a new exact-tree run. Its100% requirement remains unchanged.

The ledger preserves exact remaining paths rather than calling RI complete.
The next coherent RI cohort is **dense/eligibility controls and mixed ranking**:
all remaining `experiments/increment_25/`, `increment_26/`, `increment_27/`,
`increment_28/`, `increment_29/`, `increment_30/`, `increment_34/`,
`increment_35/`, `increment_36/`, their test counterparts, and dogfood
case0012/0013/0016 reporting/durability/adjudication dependencies not already
marked reviewed. Exact path/blob/role sets are in
[next cohort](code-audit/ri-integrity-next-cohort.json).

The separate177 older current-RI source/test versions and remaining current
fixture bodies are still obligations; four Graph3 experimental deltas do not
resolve them. Do not advance to the execution domain or prepare the postponed
successor-session dossier until the maintainer-directed RI work is reconciled.
