# Documentation Map

## Authority and ownership

- [Central architecture](architecture.md) is the canonical current and accepted
  system-architecture overview: domains, boundaries, dependency direction,
  cross-domain composition, and whether architecture is implemented/current or
  accepted but not implemented. It must be understandable without replaying all
  ADRs.
- [Architecture taxonomy](architecture/taxonomy.md) defines semantic vocabulary
  and non-equivalence. It does not replace the architecture overview.
- [Retrieval foundation](architecture/retrieval.md) owns detailed current
  Retrieval/RI/Localization capability status, lexical representation and fielding,
  empirical limits, retrieval-family hypotheses and the label constraint.
  [Roadmap](roadmap.md#current-sequencing) owns the coordinated tracks and mandatory
  R1, R1.5 diagnostics, R1.6 sensitivity, R1.7 query terms, then unconditional
  R2 BM25F experiments; these are not production behavior.
  The taxonomy owns governing retrieval/localization failure classes.
  [R1 experimental method](../experiments/identifier_sparse/README.md) owns its
  frozen whole-identifier/subtoken semantics; [prospective Case 0009](../experiments/codex_dogfood/case_0009/README.md)
  owns treatment, execution and the independent blind-adjudication boundary;
  [Case 0009 Stage D](../experiments/codex_dogfood/case_0009/analysis.md) owns the
  joined prospective result (retain separate view; R2 remains mandatory).
  [R1.5 diagnostics](../experiments/retrieval_diagnostics/README.md) owns reusable
  experimental mechanical diagnostics and conservative failure assertions;
  [Case 0009 dogfood](../experiments/retrieval_diagnostics/case_0009.md) owns its
  deterministic 37-cell development capture.
  [R1.6 protocol](../experiments/bm25_sensitivity/PROTOCOL.md) owns eligibility,
  the frozen full factorial grid and deterministic challenger rules;
  [development analysis](../experiments/bm25_sensitivity/analysis.md) and
  [interpretation](../experiments/bm25_sensitivity/interpretation.md) own surfaces,
  diagnostics and limits; [variant audit](../experiments/bm25_sensitivity/VARIANTS.md)
  owns BM25+/BM25L evidence and the no-R1.6b-prerequisite decision.
  [Case 0010](../experiments/codex_dogfood/case_0010/README.md) owns the prospective
  treatment and sterile blind packet; [Case 0010 Stage D](../experiments/codex_dogfood/case_0010/analysis.md)
  owns the clean-gold prospective join: MIXED / NO SAFE REPLACEMENT, with production
  parameters unchanged. R1.6 is complete. The roadmap now sequences upstream
  U1 manual decomposition before query weighting, preserving U2/U3 and mandatory R2.
  [U1 acquisition contracts](../experiments/codex_dogfood/acquisition/README.md)
  own experimental InformationNeed and inspectable trace semantics;
  [Case 0011](../experiments/codex_dogfood/case_0011/README.md) owns its manual
  treatment, Stage A/B review and separate C/C.5 blindness protocols.
  [Case 0011 Stage D](../experiments/codex_dogfood/case_0011/stage_d/analysis.md)
  owns the reviewed-gold/need-mapping join, case-local authoring-defect outcome,
  responsible subset burdens and separate unconstrained oracle. Its
  [practical review](../experiments/codex_dogfood/case_0011/stage_d/STAGE_D_REVIEW.md)
  owns inspectable task/obligation/unit/need/query/result/failure correspondence.
  An implementation or treatment capture is not an effectiveness claim.
  [U2 exact-hint experiment](../experiments/exact_hint_routing/README.md) owns
  task-only extraction, associations, native grounding composition and exact-first
  presentation; its [capability inventory](../experiments/exact_hint_routing/CAPABILITIES.md)
  records supported/deferred native contracts without moving RI ownership.
  [Case 0012](../experiments/codex_dogfood/case_0012/README.md) owns the prospective
  Stage A task/requirement matrix, separate caller/rule inventories, locator
  requests, lexical safety lanes and decision rule. Its
  [PRIMARY BLIND STAGE C publication](../experiments/codex_dogfood/case_0012/adjudication/PUBLICATION.md)
  owns the immutable import and independent-review preparation. PRIMARY is
  complete; reliability is unmeasured, C-R is not performed, Stage D is blocked
  and effectiveness is unknown. The comparison protocol is frozen before C-R.
- [Localization continuity](architecture/localization.md) owns the single
  current [status matrix](architecture/localization.md#capability-status-matrix),
  [Cases 0004–0008 history](architecture/localization.md#prospective-cases-0004-0008-and-structural-breadth-closure)
  and downstream [resumption boundary](architecture/localization.md#external-semantic-resolution-boundary-and-resumption).
  Start here to distinguish implemented contracts, parked structural breadth,
  experimental semantic decisions and future frontier/acquisition/sufficiency.
  It links the [resolution research](research/evidence-to-witness-resolution-policy.md),
  [external experimental adapter](../experiments/codex_dogfood/semantic_resolution/README.md)
  and frozen case summaries; prior conversation history is not needed.
- [Accepted architecture decisions](architecture/decisions/) preserve decision
  rationale, alternatives, consequences, and historical evolution. They explain
  why architecture was chosen; they are not the sole current-state specification.
  ADR-0001 defines ModelInteraction/Tool semantics; ADR-0002 repository identity,
  snapshot observation/delta/maintenance, subjects/source occurrences,
  repository DerivedKnowledge jurisdiction, epistemic-derivation/
  representational-transformation boundary, semantic-result coverage/absence,
  repository conflict/source-role knowledge, external-semantic-dependency and
  observation boundaries, capability-realization contract, and graph semantics;
  ADR-0003
  InformationNeed/retrieval/ranking; and
  [ADR-0004](architecture/decisions/ADR-0004-context-disclosure-planning-and-assembly.md)
  Context/disclosure planning, purpose-relative synthesis, materialization of
  explicitly planned transformations, semantic-strength preservation,
  representation-origin, and model-input assembly semantics.
  [ADR-0005](architecture/decisions/ADR-0005-obligation-driven-repository-localization.md)
  defines accepted repository Localization semantics: stated task obligations,
  bounded satisfaction/applicability, proof-scoped elimination and handoff limits.
  Its caller-authored obligation/witness kernel, one-way full-task/obligation
  BM25 adapter, unresolved candidate association and explicit resolution-recording
  kernel are implemented;
  exact grounding, bounded owner/mirror/Reference/import generation and role
  routing are also implemented; automatic acquisition planning, semantic
  decisions, elimination and Context integration remain future work. ADR status
  and next-increment language describe adoption checkpoints, not today's API.
- [AGENTS.md](../AGENTS.md) defines repository-operating rules.
- [Research evidence](research/README.md) preserves investigations, alternatives,
  criticisms, recommendations, and deferred/rejected possibilities. Research is
  durable evidence and historical reasoning, not automatically accepted
  architecture, implementation authorization, an ADR replacement, or a current
  architecture specification. Navigate research to its disposition, then to an
  ADR, central architecture, and implementation evidence as applicable.
  The [retrieval architecture synthesis](research/retrieval-architecture-synthesis.md)
  is the recovery/navigation point for the retrieval, purpose-relative decision,
  Context-disclosure, and Increment 10-24 evidence lineage. It records a
  heterogeneous future portfolio as research evidence; ADR-0003 remains the
  authority for accepted retrieval/ranking semantics and current production
  behavior remains defined by source and tests.
  The [structural repository retrieval investigation](research/structural-repository-retrieval.md)
  preserves the focused evidence for typed structural candidate generation,
  the semantic-versus-physical graph distinction, lexical-widening controls,
  and deferred semantic/learned alternatives; ADR-0002 and ADR-0003 disposition
  its accepted conclusions.
  The [repository retrieval algorithm landscape](research/repository-retrieval-algorithm-landscape.md)
  interprets Increment 25 and Increment 26 development evidence and records the
  then-prospective foundational sequence. The
  [breadth production gate](research/repository-retrieval-breadth-production-gate.md)
  owns the completed Increment 25-36 empirical map and disposition rationale;
  central architecture owns accepted current boundaries, and the roadmap owns
  the next research/implementation sequence. Its current retrieval-state claims
  are qualified by the retrieval foundation; historical gates do not imply
  retrieval is solved.
  The [Context Planning and graph-assisted retrieval research](research/repository-context-planning-and-graph-assisted-retrieval.md)
  compares progressive disclosure and token-efficient repository maps with
  Aider-style/PPR graph ranking, heterogeneous retrieval, and RRF. Its
  recommendations remain research evidence until accepted in current
  architecture or implemented under a bounded roadmap increment.
  The [heterogeneous Context admission and recovery investigation](research/heterogeneous-context-admission-and-recovery.md)
  preserves the earlier alternatives and deterministic development policy,
  sufficiency limits, recovery contract and prospective measurement plan.
  ADR-0004 dispositions its Context-owned semantic decisions; its policy is not
  implemented or empirically validated by this documentation checkpoint.
  Its question-lane policy is now historical rather than the next build.
  The [obligation-driven Localization research](research/obligation-driven-repository-localization.md)
  is the supplied report retained intact, including citation identifiers and
  qualifications. ADR-0005 owns accepted reconciliation, concrete experiment
  inventory, minimum contracts and next-increment boundaries. The roadmap owns
  implementation sequencing; the research is not an implementation specification.
- Package-local documentation defines detailed implemented public APIs, package
  design, lifecycle/operational behavior, and usage. Central architecture
  summarizes system-level ownership and links outward; it does not duplicate
  every package contract.
- The [Localization package overview](../src/devtools/context/localization/docs/overview.md)
  documents the implemented semantic kernel and its boundaries from Retrieval,
  Context Planning, agent execution, and Evaluation.
  Its [role-evidence contract](../src/devtools/context/localization/roles/docs/overview.md)
  owns the bounded vocabulary, positive supports, native provenance, static
  pattern scope; the separate routing package implements post-acquisition views.
  RI retains deterministic fact ownership.
  Its [routing package](../src/devtools/context/localization/routing/docs/overview.md) documents
  caller-authored per-query role preferences and lossless preferred/escape views.
  Its [exact grounding contract](../src/devtools/context/localization/docs/overview.md#exact-task-anchor-grounding)
  owns explicit task-anchor locators, bounded native RI resolution and
  unresolved/ambiguous provenance without witness satisfaction.
  Its [bounded generation contract](../src/devtools/context/localization/docs/overview.md#bounded-candidate-witness-generation)
  owns caller-shaped fixed recipes and optional single-branch families, exact
  owner/mirror, explicit Python Reference and direct import projection, child lineage,
  target-specific structural support,
  independent work/result bounds and bounded abstention diagnostics.
  The [Localization package overview](../src/devtools/context/localization/docs/overview.md#candidate-witness-association)
  also owns the bounded candidate-hypothesis contract and its native provenance.
  Its [resolution contract](../src/devtools/context/localization/docs/overview.md#explicit-evidence-to-witness-resolution)
  owns explicit member judgments, partial immutable views, exact evidence lineage
  and complete-support promotion into existing accepted witness values. Automatic
  resolution policy and assessment/readiness mutation are outside that kernel.
- Source and tests define the final implemented behavior where documentation is
  incomplete.
- Backlog records unresolved/future pressure; [roadmap](roadmap.md) records
  sequencing; the implementation ledger records implementation/history; and
  experiments are evidence. None is canonical current architecture or
  independently authorizes implementation. Historical terminology remains
  historical unless a clarification is needed to prevent a current-state error.

## Package documentation

- Core: [identity](../src/devtools/core/identity/docs/overview.md),
  [paths](../src/devtools/core/paths/docs/overview.md),
  [time](../src/devtools/core/time/docs/overview.md),
  [regex](../src/devtools/core/regex/docs/overview.md), and
  [conversion](../src/devtools/core/conversion/docs/overview.md).
- Resources: [commands](../src/devtools/resources/commands/docs/overview.md)
  and [filesystem](../src/devtools/resources/filesystem/docs/overview.md).
- Models: [interaction](../src/devtools/models/interaction/docs/overview.md),
  [serving](../src/devtools/models/serving/docs/overview.md), and
  [benchmarks](../src/devtools/models/benchmarks/docs/overview.md).
- Agents: [conversation](../src/devtools/agents/conversation/docs/overview.md)
  and [Codex integration](../src/devtools/agents/integrations/codex/docs/overview.md).
- Execution: [Runtime](../src/devtools/execution/docs/overview.md).
- Observability: [Evidence](../src/devtools/observability/evidence/docs/overview.md).
- Persistence: [overview](../src/devtools/persistence/docs/overview.md),
  [JSON](../src/devtools/persistence/docs/json.md), and
  [SQLite](../src/devtools/persistence/docs/sqlite.md).
- Tools: [overview](../src/devtools/tools/docs/overview.md).
- Evaluation: [identity coverage](../src/devtools/evaluation/docs/overview.md).
- Retrieval: [production mechanisms](../src/devtools/context/retrieval/docs/overview.md).
  The [query-conditioned graph ranking view](../src/devtools/context/retrieval/graph/docs/overview.md)
  specifies its resource-only and typed projection and PPR/RRF evidence
  semantics. The [first baseline replay](../experiments/graph_ranking_baseline/README.md)
  and [typed-view replay](../experiments/typed_graph_baseline/README.md) own
  their respective development outcomes and limitations.
- Python configuration RI: [static build/project metadata, script/entry-point
  declarations, pytest naming/recursion settings, intrinsic path inventory,
  declarations, resolution, provenance, ownership and
  future Retrieval boundary](../src/devtools/context/python/project_configuration/docs/overview.md).
  The [Python overview](../src/devtools/context/python/docs/overview.md) navigates
  this capability and mirrored-path facts. Shared exact module-name lookup
  belongs to the [modules package](../src/devtools/context/python/modules/docs/overview.md).

The `context` domain exposes narrow Repository Intelligence APIs. Its current
implementation can recursively discover regular-file addresses beneath an
explicit root using metadata only, caller-supplied maximum counts for examined
filesystem entries and discovered resources, lexical ordering, and conservative
link skipping. Discovery produces addresses, not contents, occurrences,
language classification, relevance, or snapshot state. A separate bounded
`RepositoryTextCorpusDefinition` retains a completed discovery and the exact
caller-selected subset of its discovered addresses in discovery order. It records
only future textual-corpus membership intent: it performs no observation and
makes no content, text-validity, classification, or relevance claim. Bounded
observation can subsequently acquire the selected collection, and an identified
`RepositoryTextCorpus` can retain exactly those selected observed occurrences.
Its identity is dependency-scoped to the logical Repository and selected
address/content identities, not all observed snapshot state. It is not an index
or retrieval mechanism. A separate bounded
whole-resource representation can turn every `RepositoryTextCorpus` member into
one `RepositoryTextDocument`, retaining exact observed text and resource
correlation in corpus order. This is a current representation strategy rather
than a universal one-resource-one-document rule; it does not tokenize, index,
rank, or retrieve. Resource addresses remain available for later structural or
path-sensitive retrieval evidence. A separate bounded
`context.retrieval` baseline lexical mechanism observes each document's ordered
Unicode-regex `\w+` spans, retaining exact text, offsets, encounter order, and
casefolded terms. It is heterogeneous rather than Python-specific: punctuation
and whitespace separate spans, repeated spans remain repeated, and camelCase,
PascalCase, and snake_case are not decomposed. Corpus-level statistics now retain
observation-count document lengths, document-local term frequencies,
distinct-document frequencies, and average document length (`0.0` for an empty
collection); a content-only inverted index retains direct observation/document
correlation in first-encounter vocabulary and document posting order. It has no
parser or path scoring. The current bounded BM25 operation analyzes query text
with the same spans and `casefold()` rule, retains repeated query evidence while
scoring distinct terms, and uses `k1 = 1.2`, `b = 0.75`, and
`ln(1 + (N - df + 0.5) / (df + 0.5))` IDF. It retains local score-contribution
evidence, and combines that content score with `0.25` times an independently
indexed final filename-stem BM25 score. Filename extensions and directories are
unscored; filename evidence does not alter content lexical statistics. Combined
positive matches use document-order tie breaking and require a positive bound.
Empty/OOV cases are successful zero matches; it has no identifier decomposition,
full-path, structural, Context-selection, or quality claim. A bounded deterministic evaluator consumes retained BM25 results
and fixture-designated native resource addresses without rescoring: it retains
recovered/missed relevance evidence and reports Hit@K, Recall@K, reciprocal
rank, and same-K aggregate hit rate, mean recall, and MRR. Controlled fixtures
expose both content-match strengths and identifier, path, package, and distractor
gaps; they do not establish broad retrieval quality. A repository-owned
operational benchmark can also run the unchanged pipeline over a bounded,
heterogeneous selected `devtools` checkout corpus, with manually designated
native-address relevance and a caller-selected JSON report. Its local suffix
eligibility and operational exclusions are not repository classification or
relevance semantics; it provides a small real-repository baseline checkpoint,
not a general benchmark framework or retrieval-sufficiency claim. A separate bounded
Python-function-path projection nominates exact, case-sensitive `.py` addresses
for observation without inspecting content; this is candidacy evidence rather
than proof of Python source. The observation operation then reads a finite
caller-declared collection of UTF-8 text resources into identified snapshot
state. For an exact Python function-name
purpose, a bounded pre-analysis selector filters an explicit caller-ordered set
of those resources by exact stdlib `NAME` token presence. Its candidates are
purpose-relative predictions with expected false positives, not declaration
knowledge, and zero applies only to the eligible set. The domain derives
source-grounded knowledge from one explicitly selected occurrence for direct
module-body Python function declarations with exhaustive bounded coverage. A
bounded composition operation retains independent analyses for an explicit
caller-ordered resource selection and exposes their existing knowledge as one
sequence for retrieval. The package exposes a snapshot-validated direct
declaration-containment view over the same function knowledge. Both navigation
directions preserve native occurrence,
resource dependency, derivation, and coverage; no new ownership fact or
retrieval relevance is asserted. The package also provides exact declared-name
retrieval over supplied declaration knowledge,
with purpose-relative match evidence and no ranking. A bounded projection of
that evidence identifies distinct matching resources in first-match order while
retaining every supporting declaration match; it does not choose resources to
analyze or drive Context disclosure. The
[Python function package overview](../src/devtools/context/python/function/docs/overview.md)
documents both bounded paths. The domain also provides a bounded all-match
Context disclosure that projects established declaration and source-location
information. A separate bounded materializer validates explicitly supplied
identified snapshot state and adds exact UTF-8 source segments without
filesystem reacquisition or parsing. A purpose-specific renderer transforms
that materialized Context into deterministic human-readable text while
preserving exact source, order, duplicates, and correlation; it does not create
a model message or request. A bounded composition operation separately accepts
an existing caller-owned `ModelRequest`, preserves its request semantics, and
places that rendered Context after its distinct primary task in a new request
without execution or Conversation mutation. A sibling path accepts an explicit
purpose and one caller-chosen qualified Reference/direct Call fact, validates
its source and target against retained snapshot state, and renders the exact
Reference Name and resolved declaration source with relationship provenance
and navigation pointers. It does not choose the fact, infer sufficiency, or
reacquire files. The domain does not provide
Git-aware or language-classifying discovery, capability/execution
infrastructure, broader retrieval, a generic Context compiler, or general
ModelRequest assembly. Current durable
conversation semantics remain in `agents.conversation`, and `context` does not
own former Message/History/Session semantics.

The [Python classes package](../src/devtools/context/python/classes/docs/overview.md)
owns direct module-body class and direct class-body method declarations over
retained snapshot resources. It distinguishes occurrence resource from direct
lexical class parent, retains exact base-expression syntax, and provides
validated containment navigation. A separate bounded direct-base derivation
assesses each expression and establishes a repository class target only for
supported local or import-qualified forms. It does not broaden the existing
direct module-body function or qualified Reference/Call contracts.

The [Context Planning package](../src/devtools/context/planning/docs/overview.md)
owns a bounded caller-directed DisclosurePlan over one explicit purpose and
snapshot. It currently composes qualified Python Reference and whole retained
resource representations, rejects stale dependencies, preserves native
provenance in realized ContextDisclosure items, and renders/assembles them
after materialization. It does not retrieve, rank, autonomously select,
optimize budgets, or judge sufficiency.

The adjacent `context.python.imports`
[package contract](../src/devtools/context/python/imports/docs/overview.md)
documents native module-only relations and the separate one-facade member slice.
The Localization direct import dependency consumer takes one forward module
relation step with exact provenance, branching and independent work/result
bounds. Imported-module candidates do not claim successful member bindings,
exports, runtime dependencies, relevance or witness acceptance.
The package retains direct module-body import
aliases as source-grounded syntax and resolves eligible module portions only
within an explicit interpretation universe. Its `relations.py` derives directed,
declaration-grounded relations only for uniquely resolved outcomes with one
available source interpretation; unresolved, ambiguous, unsupported, or
source-unavailable cases do not produce relations, and repeated declarations
remain distinct. These do not establish runtime import execution or retrieval
relevance. The
`context.python.modules` package interprets caller-selected observed `.py`
resources under an explicit repository-relative module root as ordinary or
package modules with dotted names. Address is not module identity: the explicit
root and exact observed resource remain part of the interpretation, duplicate
names are preserved, and no root precedence exists. Neither package implements
runtime importability, source-root discovery, namespace packages, generic graph
infrastructure, retrieval, or Context behavior.

The [Python modules package](../src/devtools/context/python/modules/docs/overview.md)
also owns qualified immediate package membership over one explicit-root
selected interpretation analysis. A single fact supports child-to-package and
package-to-child questions, with bounded missing and ambiguous assessments;
it does not establish Imports or retrieval relevance.

The [Python mirrored-path RI overview](../src/devtools/context/python/docs/overview.md)
defines the exact observed `src/devtools/.../<stem>.py` to
`tests/.../test_<stem>.py` convention, source/test roles, derivation identity,
and bounded coverage. Correspondence asserts path convention only; it is not
a semantic test or retrieval relation.

Import resolution is limited to an explicit interpretation universe and retains
resolved, unresolved-in-universe, ambiguous, or unsupported outcomes. It neither
emulates runtime imports; the separate relation derivation records only the
qualified source-to-target relations established by resolved outcomes.

`context/python/imports/members.py` owns bounded imported-member binding
resolution: a direct module-body `ImportFrom` member occurrence may resolve
through exactly one direct facade binding to one direct function declaration in
a uniquely resolved target module. It retains qualified outcomes and source,
facade, target-module, and declaration provenance, with a source-resource to
defining-resource projection where relevant. This is distinct from the
module-only import relation and does not provide runtime import, export or
`__all__`, general reference, recursive facade, other-target, or retrieval
semantics.

The [Python References package](../src/devtools/context/python/references/docs/overview.md)
owns bounded source-occurrence References to supported direct functions,
classes, and direct methods through same-module, imported, module-qualified,
and statically class-qualified routes. Direct Call syntax specializes that
same Reference; coverage is non-exhaustive. Direct declaration lookup belongs
to the [Python modules package](../src/devtools/context/python/modules/docs/overview.md).
Neither package owns retrieval relevance or Context selection.

`context.retrieval` now also exposes direct Python structural resource
projection over supplied production Imports, References/direct Calls, and
qualified immediate package membership facts. Its purpose-bearing request and
snapshot-scoped result retain each candidate's seed, direction, and native RI
support without source parsing, ranking, or Context disclosure. The lexical
baseline keeps its own query, corpus, ranked matches, scores, and contributions.
The production lexical/structural composition operation accepts an explicit
snapshot and purpose, checks the entire lexical corpus against exact observed
snapshot resources, and correlates native evidence per resource in neutral
address order. It produces an inventory without cross-mechanism ranking,
budgeted Selection, or Context disclosure. The
[retrieval package overview](../src/devtools/context/retrieval/docs/overview.md)
defines its API and validation contract.

The [roadmap dogfood protocol](roadmap.md#controlled-advisory-codex-dogfooding)
owns the current evaluation sequence. Its narrow
[`experiments/codex_dogfood` capture](../experiments/codex_dogfood/capture.py)
compares full-prompt and short-need lexical arms, adds direct structural facts
when qualified seeds exist, and prepares advisory orientation. It is research
orchestration, not a production Selector, Codex command adapter, or Context
compiler.
The [first blind dogfood case](../experiments/codex_dogfood/case_0001/README.md)
records its frozen judgments, retrieval inventories, agent observations, and
post-freeze analysis as development evidence.
The [second blind dogfood case](../experiments/codex_dogfood/case_0002/README.md)
records the lexical-only capture implementation task and its separate frozen
judgments, inventories, agent observations, and post-freeze analysis.
The [third blind dogfood case](../experiments/codex_dogfood/case_0003/README.md)
owns the prospective full/short BM25, typed PPR, repository-map and RRF
comparison preceding configuration RI implementation. It retains the expanded
pre-task frame, protocol metadata correction, native rankings, advisory handoff,
independent adjudication, exploration limits, protected validation and cross-case
synthesis. Production configuration facts remain outside Retrieval projection.

The [fourth prospective case protocol](../experiments/codex_dogfood/case_0004/README.md)
freezes the repository-role intelligence task, caller-authored obligations and
explicit lexical queries before Retrieval. It owns the fixed corpus, native
input archive, acquisition settings, blind adjudication and measurement rules;
this checkpoint contains no retrieval outputs or resource judgments.

The `orchestration` and `governance` domains remain recognized sparse
namespaces without reusable implementation APIs. Evaluation now provides the
bounded expected-versus-observed identity coverage API documented in its
package overview. Broader Evaluation architecture remains unimplemented.

## Experiments and scripts

`experiments/` is non-installable composition and may depend on `devtools`;
reusable source must not import it. [Qwen experiment documentation](../experiments/qwen/docs/overview.md)
describes the bounded read-only experiments. Operational entry points remain
under `scripts/`. The [protected development validation contract](development/validation.md)
documents the canonical test command, its pre-collection experiment-tree
exclusion, and the separate confirmation-validation boundary.

## Backlog navigation

[Backlog overview](backlog/overview.md) is the canonical record index, grouped
by stable ID, lifecycle status, and primary domain. [Backlog metadata](backlog/metadata.md)
defines ownership, split-lineage, dependency, and promotion terminology.

## Update workflow

For an implemented behavior change, update package documentation first, then
this map and architecture documentation when navigation or cross-package
ownership changes. Update an accepted ADR when an approved cross-package
decision changes. Preserve historical records as history rather than rewriting
them to conceal a former architecture.


## Repository-map retrieval navigation

The [repository-map package contract](../src/devtools/context/retrieval/repository_map/docs/overview.md)
owns current global importance, symbol metadata relevance, symbol ranking,
resource aggregation and compact disclosure ingredients. The
[frozen repository-map investigation and diagnostic replay](../experiments/repository_map_baseline/README.md)
owns external Aider implementation evidence, alternatives, Case 0002 results,
and the pending prospective evaluation protocol. ADR-0003 and ADR-0004 continue
to govern Retrieval/Context ownership; the research disposition distinguishes
this devtools adaptation from Aider's task-weighted PageRank/rendering pipeline.


The [Python modules source selector](../src/devtools/context/python/modules/docs/overview.md#exact-source-declaration-selection)
owns exact native class/function selection independently of conservative direct
binding lookup. [Localization grounding](../src/devtools/context/localization/docs/overview.md#exact-task-anchor-grounding)
consumes that selection for static declaration identities, including decorated
declarations, without runtime/import identity or witness acceptance claims.
