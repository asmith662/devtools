# Implementation Ledger

This ledger is an ordered historical record of meaningful implementation
milestones, important corrective decisions, and verification state. It is not
an API reference or a backlog; see package-local documentation and the
[roadmap](roadmap.md) for those concerns.

## Foundation milestones

- Established one `devtools` distribution with capability-oriented source
  domains rather than separately distributed packages.
- Implemented `devtools.identity`: immutable UUID identities with generation
  and parsing.
- Implemented `devtools.system`: coarse operating-system-family detection.
- Implemented `devtools.paths`: `ResolvedPath`, filesystem-path and dot-path
  parsing, explicit resolution, and known-location constructors.
- Implemented `devtools.time`: UTC timestamps, non-negative durations,
  bounded parsing, and a monotonic stopwatch.
- Implemented `devtools.regex`: immutable match values and explicit regex
  compilation, search, iteration, and replacement.
- Implemented `devtools.commands`: immutable fluent command specifications,
  awaitable execution handles, structured events, bounded output/event
  buffering, and immediate-child timeout/cancellation cleanup.
- Implemented `devtools.conversion`: explicit callable-based single and batch
  conversion with stable fail-fast, indexed failure normalization; JSON and
  CSV models consume it through thin adapters.
- Implemented Message: semantic MessageId composition, stable
  conversational roles, open source provenance, and immutable textual message
  values with explicit local construction timestamps.
- Implemented `devtools.filesystem` model foundations: immutable binary, text,
  JSON, Markdown, and CSV models, including recursively frozen JSON values.
- Implemented `JsonCodec`, `TextCodec`, `MarkdownCodec`, and `CsvCodec`.
- Implemented codec-backed generic filesystem reads for JSON, text, Markdown,
  and CSV with size bounds, suffix inference, and explicit format overrides.
- Implemented generic filesystem writes from model format through sibling
  temporary-file replacement; structured JSON and CSV writes serialize current
  state rather than stale source provenance.
- Corrected atomic-write cleanup so a sibling temporary path is available for
  cleanup immediately after temporary-file creation.
- Completed authoritative package-local documentation and milestone-freeze
  passes for all eight foundational packages and Message.
- Declared the collective foundational tooling and Message milestones complete
  and frozen.

## Agent integration milestone (historical terminology)

This historical milestone used the former `devtools.agents.Agent` terminology.
The current implementation supersedes that boundary with
`devtools.interactions.Interaction` and `InteractionTurn`; the old package and
compatibility aliases were removed. The entries below describe the state at the
time of that milestone rather than the current public API.

- Implemented `devtools.agents` as the provider-neutral structural Agent
  contract: async `Agent`, immutable `AgentTurn`, and opaque
  source-owned `ConversationRef` values with source ownership invariants and
  stateless-turn support. Its only production dependency is `context.message`.
- Implemented and froze `devtools.interactions.providers.codex` as the first concrete Agent adapter:
  Codex CLI command construction through `CommandExecutor`, focused JSONL
  parsing, Codex thread-to-`ConversationRef` mapping, and final output-to-
  `Message` mapping.
- Corrected Windows direct launch by resolving the default npm `codex.cmd`
  launcher rather than relying on the PowerShell shim.
- Corrected resumed execution to force the supported read-only sandbox
  configuration override.
- Verified real fresh/resumed thread continuity, unchanged provider thread ID,
  and read-only resumed write denial in an isolated temporary repository.
- Completed package-local documentation and freeze reconciliation for
  `devtools.agents`, with Codex as its first validating implementation.
- Established `devtools.context` by relocating `devtools.message` to
  `devtools.context.message` before History and Session. Message is retained
  interaction context; no compatibility alias was retained, and Agent/Codex
  semantics plus the live Codex acceptance remained unchanged.
- Implemented and froze `devtools.context.history`: immutable tuple-backed,
  insertion-ordered Message-only transcripts with standard Sequence semantics,
  History-preserving slices, and immutable append. History has no identity,
  timestamps, provider continuation state, or event-log scope.
- Implemented and froze `devtools.context.session`: `SessionId` semantic
  identity and mutable slotted Session lifecycle state with immutable History
  replacement, read-only live source-keyed `ConversationRef` mapping, duplicate
  reconstruction-source rejection, object-identity equality, and
  unhashability. The first milestone stores one current ref per source; it does
  not yet identify multiple logical same-source participants.
- Verified Session against the real Codex adapter: stored continuation resumed
  the same provider thread, retained an exact four-Message transcript, kept
  Session ID and creation time stable, and preserved resumed read-only write
  denial in an isolated temporary repository.
- Revised the frozen Session milestone after Runtime design exposed a
  same-Session async race risk. Session now owns private per-object turn
  coordination spanning complete logical turns, including awaited Agent calls;
  different Session objects remain independent. Cancellation and exception
  cleanup are verified, coordination state is non-semantic and reconstructed
  fresh, and the real Session/Codex acceptance runs each turn inside
  `Session.turn()`.
- Implemented and froze `devtools.runtime`: zero-field, keyword-only
  `Runtime.send()` composes complete `Session.turn()` coordination with one
  caller-selected Agent invocation, input retention, returned-source validation,
  returned-Message-before-continuation commit, and non-destructive
  `conversation=None` handling.
- Verified Runtime forward-only ordinary-failure and cancellation behavior,
  same-Session serialization, same-source replacement-continuation handoff,
  and different-Session concurrency. A real Runtime/Codex acceptance retained
  an exact two-turn/four-Message transcript, resumed the same provider thread,
  preserved Session identity/time, and denied a disposable write in an isolated
  temporary repository.
- Implemented and froze `devtools.persistence`: strict versioned portable JSON
  plus a normalized SQLite current-snapshot store sharing private semantic
  capture/restoration. SQLite preserves global immutable Message identity and
  ordered History occurrences, atomically replaces Session snapshots, protects
  Session/Message identity conflicts, rejects missing referenced Message rows,
  and validates essential columns before claiming a version-1 schema.
- Verified rollback removes candidate Session, Message, and association rows;
  reconstructed Sessions receive fresh local turn coordination and work directly
  with Runtime. A real SQLite-to-reconstructed-Session-to-Runtime-to-Codex
  acceptance resumed the same provider thread, retained the exact four-Message
  History, and preserved read-only execution in an isolated temporary repository.
- Implemented and froze `devtools.evidence` for its Attempt-only milestone:
  `AttemptId`, four-state `AttemptState`, and a mutable one-way Attempt
  lifecycle with immutable SessionId/MessageId/source attribution and observed
  start/completion timestamps.
- Corrected Attempt terminalization to obtain `Timestamp.now()` before any
  lifecycle mutation, so timestamp failure propagates without partially
  terminalizing the Attempt. Attempt uses object-identity equality and is
  unhashable; result, diagnostic, retry, Runtime, and Persistence integration
  remain deliberately absent.
- Integrated Runtime with Evidence through the narrow structural synchronous
  `AttemptObserver` Protocol. Runtime now retains only optional fixed observer
  configuration and remains interaction-stateless; `Runtime()` creates no
  Attempt. Observed Attempts are created after input retention, started before
  Agent work, and span continuation lookup through final Runtime commit.
- Defined primary Runtime outcome precedence over ordinary/cancellation
  secondary lifecycle or observer errors, while deliberately leaving
  non-cancellation `BaseException` unsuppressed. Terminalization and callbacks
  are each at most once, finished callbacks receive the same terminal live
  Attempt, and all callbacks occur under Session turn coordination.
- Added deterministic finalization regressions proving the no-observer path
  never calls `Attempt.new()` and started observation sees retained input and a
  RUNNING Attempt before Agent invocation. Verified same-Session lifecycle
  ordering, continuation handoff, different-Session concurrency, and real
  no-observer plus observed read-only Codex acceptance. No Persistence,
  concrete Evidence, retry, or participant-identity behavior was added.
- Implemented and froze immutable terminal Evidence values: `EvidenceId`, the
  six-value `AttemptStage` location vocabulary, empty `AttemptSucceeded`,
  required-stage `AttemptFailed` and `AttemptCancelled`, their closed terminal
  outcome union, and keyword-only `AttemptTerminalEvidence`.
- Terminal Evidence is a frozen, slotted, hashable structural value with
  `EvidenceId`, `AttemptId`, caller-supplied terminal `occurred_at`,
  construction-time `observed_at`, and no wall-clock ordering invariant. It
  embeds no live Attempt and duplicates no Attempt attribution. Stages state
  where processing stopped, not failure cause or side-effect/retryability facts.
- The terminal submodule now declares its exact public `__all__`; direct
  regressions freeze the empty success payload and required failed/cancelled
  stages. At that value-model freeze checkpoint, Runtime production/delivery,
  EvidenceSink, EvidenceRecord, and Attempt/Evidence persistence remained
  deferred.
- Implemented and froze Runtime-to-immutable-terminal-Evidence
  production/delivery. Added the structural synchronous `EvidenceSink` protocol
  and fixed `Runtime.evidence_sink` configuration. Runtime creates an Attempt
  iff observer or sink configuration requires it, after input retention, and
  maps the six frozen Runtime boundaries to terminal failure/cancellation
  Evidence stages.
- Runtime now terminalizes before constructing one optional immutable terminal
  record using exact `Attempt.completed_at` as `occurred_at`; construction
  precedes finished observation and at-most-once sink acceptance. Finished runs
  before sink operationally. Ordinary/cancellation construction, observer, and
  sink failures preserve primary Runtime outcome; non-cancellation
  `BaseException` short-circuits later secondary work. Delivery is synchronous
  under `Session.turn()`, preserving same-Session order, with no retry or
  replacement Evidence record.
- A read-only audit identified missing freeze-critical cancellation coverage for
  construction failure and late Runtime stages. The bounded regression correction
  added exact primary-cancellation identity, one-construction/no-sink proofs and
  RESULT_VALIDATION, OUTPUT_RETENTION, and CONTINUATION_REPLACEMENT cancellation
  stage/partial-Session-state regressions before this freeze.
- Designed and implemented experimental `ExecutionInspector` as an in-memory,
  process-local diagnostic consumer of `AttemptObserver` and `EvidenceSink`.
  A real one-turn local Codex/Runtime exercise found that retained Attempt IDs
  were not publicly discoverable after `Runtime.send()`.
- A narrow experimental ergonomic correction added
  `attempt_ids() -> tuple[AttemptId, ...]` without Runtime changes or new
  attribution, persistence, or query architecture. A real two-turn local
  Codex/Runtime exercise validated unordered ID discovery: caller-held input
  `MessageId` values and `Attempt.message_id` distinguished executions, and
  `get_evidence_for_attempt()` remained sufficient. No query, latest,
  Persistence, or AttemptAttribution pressure emerged. The capability is
  retained as active experimental work: submodule-only, non-durable, and not
  frozen.

- Established the repository-owned architecture backlog with stable opaque
  identifiers, canonical epic/item records, distinct lifecycle, dependency,
  risk, and validation metadata, and a live-harness validation cadence. The
  backlog preserves pressure and unresolved semantics without authorizing
  implementation; roadmap, architecture, package documentation, and this
  ledger retain separate authority roles.

## Verification snapshot

At the Runtime-to-Attempt integration-freeze checkpoint:

```text
Ruff: clean
mypy: clean
pytest: 453 passed, 5 skipped
branch coverage: 100%
git diff --check: clean
live Runtime/Codex acceptance: no-observer and observed paths passed
```

At the immutable terminal Evidence value-model freeze checkpoint:

```text
focused terminal tests: 11 passed
Evidence suite: 42 passed
deterministic suite: 464 passed, 5 skipped
branch coverage: 100.00%
Ruff: clean
mypy: clean, 153 files
git diff --check: clean apart from existing harmless CRLF warnings
```

At the Runtime-to-terminal-Evidence production/delivery freeze checkpoint:

```text
focused Runtime tests: 72 passed
focused Evidence tests: 43 passed
deterministic suite: 498 passed, 5 skipped
branch coverage: 100.00% (2,274 statements, 404 branches)
Ruff: clean
mypy: clean, 153 files
git diff --check: clean apart from existing harmless CRLF warnings
```

## Deferred work

Deferred work belongs primarily in package-local documentation. Examples
include path containment, additional filesystem codecs or streaming, richer
Markdown source fidelity, command process-tree management, and conversion
extensions. These are not active repository-level milestones unless they become
prerequisites for a future architectural domain.

## Architecture decision checkpoints

- Accepted ADR-0002 for future repository intelligence and coding Context:
  nominal Repository identity; content-derived RepositorySnapshots; contextual
  resource occurrences and reusable content identity; derivation-aware
  DerivedKnowledge validity and incremental reuse; distinct derivation and
  repository-relationship graph semantics; and purpose-relative, untrusted
  Context disclosure. This is a documentation-only architectural decision; no
  repository intelligence, Context compiler, storage, retrieval, graph, or
  production API was implemented. It supersedes B-0008's earlier narrow
  repository-navigation investigation while B-0002 retains unimplemented
  architectural pressure.
- Amended ADR-0002 within its accepted repository-intelligence boundary:
  RepositorySubject and SourceOccurrence are distinct snapshot-local referents;
  subjecthood is orthogonal to DerivedKnowledge; source location, names, AST
  nodes, graph nodes, chunks, containment, and cross-snapshot continuity are
  not universal subject identity. This documentation-only refinement preserves
  analyzer, graph, identity, incremental-maintenance, retrieval, and Context
  implementation mechanisms as deferred.
- Further amended ADR-0002 within the same boundary: RepositorySnapshot is a
  logically complete successfully observed state under explicit semantics;
  SnapshotDelta and IncrementalMaintenance are distinct from state; and
  dependency-scoped DerivedKnowledge applicability, invalidation discovery,
  rederivation, and cache lookup remain separate. Observation, identity,
  storage, and maintenance mechanisms remain deferred.
- Further amended ADR-0002 within the same boundary: DerivationDefinition,
  Derivation, execution, and DerivedKnowledge are distinct; dependencies are
  direct, role-bearing semantic inputs rather than execution incidental inputs;
  applicability/provenance/coverage/execution evidence remain distinct. This
  documentation-only refinement defers concrete models, identity, capability,
  execution, maintenance, and storage mechanisms.
- Further amended ADR-0002 within the same boundary: repository-intelligence
  capability is available semantic realization, distinct from definition and
  implementation binding; bounded dependency accounting, internal admission,
  execution evidence, and scheduling remain separate from Tools, retrieval,
  Context, Agent, and Runtime ownership. Concrete mechanisms remain deferred.
- Accepted ADR-0003 for the next semantic layer: immutable purpose-relative
  InformationNeed; bounded, dependency-aware multi-strategy retrieval planning;
  ContextCandidates; provenance-bearing RelevanceEvidence; and ranking distinct
  from Context selection/compilation. It preserves progressive disclosure and
  evaluation seams without implementing retrieval, ranking, Context compilation,
  planning, concurrency, persistence, or an Agent/Runtime loop.
- Accepted ADR-0004 for post-ranking Context semantics: conditional disclosure
  planning; coupled subject/representation choices; coverage, marginal value,
  complementarity, applicability, sufficiency, budgets, and ContextDisclosure;
  distinct repository/disclosure/Conversation histories; and model-input
  assembly separate from disclosure planning. This documentation-only decision
  preserves unresolved compiler, representation, authority, coherence, and
  evaluation work without implementing any Context infrastructure.
- Amended ADR-0004 within its accepted disclosure-planning boundary: disclosure
  selects information rather than prompt strings; DisclosureOption,
  DisclosurePlan, ContextDisclosure, and ModelRequest are distinct; source,
  knowledge-projection, and synthesized origins have different provenance
  semantics; new assertions remain explicit DerivedKnowledge; and coherence,
  authority, conflict, applicability-at-realization, and materialization
  boundaries are semantically settled while their mechanisms remain deferred.
- Reconciled ADR-0002 and ADR-0004 after adversarial review within their existing
  ownership boundaries. DerivedKnowledge now explicitly owns repository-relative
  semantic intelligence rather than every semantic assertion; representational
  transformation is distinct from epistemic derivation; and purpose-relative
  Context synthesis can remain provenance-bearing without automatic repository-
  knowledge promotion. Materialization can perform semantic transformation when
  explicitly selected by the DisclosurePlan, while assembly remains non-
  semantic. Provenance does not itself establish authority, certainty,
  correctness, or truth. This documentation-only amendment supersedes the prior
  universal-promotion assumption without implementing Context infrastructure or
  resolving synthesis, uncertainty, completeness, authority, or conflict
  mechanisms.
- Further reconciled ADR-0002 and ADR-0004 after repeated external reviews
  exposed a plausible hard-fact reading of DerivedKnowledge. The documentation
  now makes result-vocabulary semantics, qualified/approximate knowledge,
  semantic-result coverage and absence discipline, assumption/scope boundaries,
  repository conflict/source-role knowledge, and future learned-analyzer
  compatibility explicit. ADR-0004 now requires semantic-strength preservation
  through representation, synthesis, materialization, disclosure, and assembly.
  This documentation-only refinement selects no universal Claim/confidence
  model, coverage object, conflict engine, authority hierarchy, source-role
  taxonomy, analyzer, storage, or API.
- Completed a read-only architecture-preservation audit and preserved its
  accepted handoff findings in canonical documentation. Broad archaeology,
  steelmanning, adversarial/Deep Research review, focused reconciliation, and
  preservation review have settled the core semantic architecture. Two focused
  preimplementation investigations remain: external semantic state/dependency
  identity/applicability/replay, and integrated evaluation/causal attribution.
  The preservation refinement also records cross-layer replay correlation,
  distinguishes implementation-shaped choices from foundational research, and
  defines evidence-based reopen discipline without creating a WorkspaceSnapshot,
  universal replay artifact, evaluation architecture, API, storage design, or
  implementation.
- Reconciled the focused external-semantic-state Deep Research investigation
  within ADR-0002's existing dependency/applicability responsibility. External
  semantic inputs remain open and heterogeneous; relevant ambient state must be
  explicit, observation guarantees cannot exceed their mechanism, and identity,
  equality, equivalence, compatibility, applicability, and replay strength stay
  distinct. The refinement selects no universal WorkspaceSnapshot/environment
  ontology, mandatory independent identity, hermetic execution, generated-
  resource model, retention system, applicability algorithm, or replay
  mechanism. Integrated evaluation architecture/causal attribution remains the
  final focused preimplementation research investigation.
- Reconciled the focused evaluation-architecture/causal-attribution
  investigation after subsequent architectural review. Evaluation is now
  explicitly preserved as a distinct assessment/comparison responsibility that
  correlates layer-local artifacts and Evidence without owning them. The
  reconciliation retains assessment basis, intended condition, realization,
  evaluator/criterion, heterogeneous outcome, and later inference distinctions;
  rejects universal EvaluationCase/Treatment/Episode/score/causal-graph/
  trajectory/knowledge-closure infrastructure; and records ADR-0001
  observation/correlation conformance pressure. The investigation dossier's
  producing process did not complete its final mechanical artifact-integrity
  verification, so the dossier remains research evidence rather than an
  accepted or mechanically verified decision artifact. The implementation-start
  assessment is SAFE WITH PRESERVED SEAMS; later external confirmation remains
  a reopen gate, and B-0002 remains backlog work.

## Bounded direct-base Repository Intelligence checkpoint

- After the class/method declaration checkpoint, added snapshot-bound direct
  Python base assessments to production Repository Intelligence. The bounded
  resolver reuses qualified module/import interpretation, accepts unambiguous
  local class, imported class member, and imported module attribute forms, and
  retains an outcome for every direct base expression. Positive relations are
  structural class-to-class facts; Personalized PageRank and fusion were not
  changed. Broader qualified References/Calls precede prospective richer graph
  evaluation.

## Query-conditioned graph-ranking checkpoint

- Added a Retrieval-owned, snapshot-bound resource graph projection over
  production qualified Imports and References/direct Calls, with exact RI fact
  provenance, forward transitions, equal per-fact weights, and outgoing
  normalization. Added deterministic lexical-rank-personalized PPR and optional
  equal-channel RRF retaining both native result lists. This is ranked evidence,
  not Graph-1/Graph-2 path expansion or Context disclosure.
- Replayed the baseline on the retained Case 0002 development snapshot after
  fixing mechanism parameters. BM25 covered ten required resources by full-
  prompt rank 43; PPR required 84 and fusion 62. Seven required resources were
  graph-isolated. The graph remains optional evidence; confirmation is sealed.
  Exact protocol, counts, and limitations are in the graph-ranking development
  report. Full-suite verification encountered repository discovery of `.venv`
  over a pre-existing 10,000-resource test ceiling and the configured 100%
  coverage threshold; focused retrieval and RI regressions passed.
# Broader bounded declaration References (2026-10-01)

One active production derivation now resolves supported direct module functions,
classes, and direct methods through same-module, named-import, module-qualified,
and statically class-qualified syntax. The old function-only derivation was
removed; its passive fact value classes remain for frozen development pickle
replay. Module declaration lookup is shared with bounded base resolution.
The unchanged Case 0002 forward graph replay changed 279 to 360 aggregated
edges and 152 to 134 isolated resources. Required isolated resources fell from
seven to three; unchanged Personalized PageRank last-required depth worsened
from 84 to 87 on the full prompt. This establishes improved topology, not a
ranking win. The next hypothesis is a richer typed Retrieval graph view.

# Typed Retrieval graph development checkpoint (2026-10-01)

One canonical production graph builder now supports the historical
resource-forward configuration and typed resource/function/class/method views
over retained Repository Intelligence. Typed edges retain exact fact provenance,
declaration containment, forward References/Imports, direct bases, and optional
package and mirrored-path navigation. The unchanged PPR kernel uses resource
lexical seeds; typed resource ranking takes the maximum node mass per resource.
The prospective [development replay](../experiments/typed_graph_baseline/README.md)
increased graph size from 302 nodes/279 edges to 1,512 nodes/3,598 core edges
(3,935 with navigation). It preserved same-resource Reference topology but
worsened full-prompt last-required rank from BM25 43 and resource PPR 84 to
typed core 146 and navigation 207. No lexical required miss was rescued.
The result withholds a default graph policy and motivates an independently
frozen comparison of structural priors and resource aggregation. Confirmation
remains sealed.


## Repository-map structural retrieval checkpoint (2026-10-01)

- Started from clean main at `a24a70cc0511ce6fc56969ea7d46b438f79a7df0`.
- Inspected governing architecture/research and Aider's public implementation;
  distinguished its task-weighted file PageRank, definition flow and compact
  rendering from a separately inspectable devtools global-importance channel.
- Implemented `context.retrieval.repository_map`: dependency-only global
  importance, compact symbol/path BM25 relevance, symbol RRF, maximum-symbol
  resource projection and optional lexical-resource RRF. Preserved exact RI
  subjects/spans and incoming fact supports, without adding repository truth or
  Context rendering. Shared canonical walk/resource-fusion arithmetic with PPR.
- Froze algorithm/parameters before Case 0002 diagnostic retrieval; retained
  initial hashes and AST-identical final formatting provenance. Full-prompt map
  omits three required non-symbol resources; BM25/map fusion needs rank 139 for
  complete coverage versus BM25 43. Short-need fusion needs 152 versus 87.
  No parameter is tuned and no general usefulness/default fusion is promoted.
- No legitimate fresh independent task was established; prospective evaluation
  awaits the next naturally occurring task. No Case 0003 was manufactured.
- Validation: Ruff, touched-file formatting, mypy and diff checks pass. Default
  pytest has seven local virtualenv discovery-bound failures. Protected run uses
  a bounded cwd corpus for those seven benchmarks, excludes 22 retained-artifact
  tests, and passes 1,749 tests with two live skips and 100% production branch
  coverage. Initial default tests automatically ran old confirmation audits;
  those outcomes were not used in algorithm choice or replay. Full conditions,
  comparative diagnostics and source hashes are in the
  [retained baseline](../experiments/repository_map_baseline/README.md).
- One checkpoint commit; no push or subsequent production increment.

## Bounded Python project configuration RI (2026-10-01)

- Implemented the authorized frozen Case 0003 task from clean main
  `0bcb2caaf7ae4b6a776bd9505efa1dc87e8325a5`, preserving host-owned experiment
  artifacts. No staging, commit or push is part of this implementation.
- Added `context.python.project_configuration` with separate models,
  retained-`tomllib` declaration analysis and qualified observed resolution for
  project README, Hatch wheel packages, pytest testpaths, Coverage source,
  mypy files and mypy search paths. Semantic TOML key/item anchors preserve
  duplicate ordinals and exact configuration provenance without invented spans.
- Explicit command cwd and pytest rootdir assumptions remain separate from
  README/Hatch configuration-parent routes. Native resource/module dependencies
  and versioned identities support deterministic facts and explicit missing,
  ambiguous and unsupported assessments. Prefix membership implies neither
  directory existence nor execution. Coverage retains competing path/module/root
  readings. Entrypoint presence is unsupported, without speculative bindings.
- Extracted bounded exact dotted-name lookup into modules and migrated imports
  without changed lookup order/outcomes. No Retrieval ranking, graph projection,
  fusion or Context policy changed. Package docs include ownership, rejected
  universal configuration/entrypoint machinery and a separate future relation
  decision boundary. B-0019 stays deferred; B-0047 records protected development
  validation-profile pressure without designing a harness.
- Focused new-package/shared-lookup suite: 50 passed, 100% branch coverage.
  Final Python RI and Evaluation run: 248 passed, retaining 100% new-package
  and shared-lookup branch coverage. Ruff and mypy pass across `src`,
  `tests/context` and `tests/evaluation`; diff whitespace checks pass.
  Tests use explicit safe directories, coverage overrides and writable
  `.devtools` temporary locations. Initial cache and default temporary-directory
  access were denied by the sandbox before test execution; existing virtualenv
  executables and explicit local basetemp resolved those operational limits.
- Default repository-wide pytest, live services and sealed confirmation files
  were not accessed. Host-owned protected comprehensive validation and blind
  evaluation remain separate. No retrieval-quality or cross-case conclusion is
  drawn from advisory suggestions or implementation tests.

## Case 0003 prospective retrieval evaluation and checkpoint (2026-10-01)

- Frozen real configuration task and separately authored InformationNeed before
  retrieval; retained 472 pre-task resources and all eight unchanged BM25,
  typed Personalized PageRank (PPR), repository-map and Reciprocal Rank Fusion
  (RRF) ranking arms. Candidate frames differ from earlier cases. A handwritten
  filename-weight metadata typo and capture/correction race are retained in
  initial/corrected manifests; the prospectively fixed scorer used 0.25 and no
  ranking parameter changed. Host architecture guidance is recorded intervention.
- Implementation and validation frozen before an independent read-only
  adjudicator saw only the pre-task export and neutral frame. Production
  Evaluation identity accounting is exact: 472 judged, nineteen required, ten
  helpful only, 443 unnecessary, no unresolved judgments. No labels changed after
  provenance joining. No sealed confirmation outcomes were accessed.
- Complete full/short BM25 depths: 348/180; typed PPR: 314/278; map incomplete
  at five required resources; BM25/map RRF: 372/279. Full PPR's depth gain comes
  with lower early recall. Structural channels rescued no required lexical miss.
  Thirteen map omissions lack supported structural evidence; one import-only
  facade has structural evidence but no eligible symbol. Centrality/private
  helper and compact-lexical promotions retain distinct provenance.
- Codex trace: 22 completed commands, one search, 39 direct-open events across
  24 resources. Nine required resources opened outside the compact advisory
  display demonstrate recovery from handoff omissions, not lexical misses.
  Opens/edits do not define requiredness; there is no unaided control or savings
  claim. Root review adds one fixture formatting correction and documentation
  clarifications; production behavior remains frozen.
- Host validation excludes the entire retained experiment test tree before
  collection and admits only capture/new protocol files: 1,299 passed, two live
  skips, 100% of 8,226 production statements and 1,902 branches. Repository Ruff,
  mypy (582 source files), sixteen touched Python formatting checks and diff
  checks pass. The earlier 22-test/7-benchmark profile remains planned evidence,
  not the actual invocation. B-0047 retains supported-profile pressure.
- The new configuration RI yields eight resolved declarations and 1,026
  qualified target facts on the original snapshot, but remains unconsumed by
  Retrieval. The next recommendation is a separate bounded selector/target
  projection and resource-participation decision, accounting for prefix fan-out;
  no default fusion or production Selection rule is promoted. Detailed
  [protocol, native results and cross-case synthesis](../experiments/codex_dogfood/case_0003/README.md)
  remain reproducible with immutable artifact byte handling. One checkpoint
  commit is authorized; no push or next increment is begun.

## Localization semantic kernel (2026-10-02)

- Implemented `devtools.context.localization` as a caller-authored semantic
  kernel: deterministic task-local anchors/obligations; separate mandatory,
  helpful, and conditional applicability semantics; alternative conjunctive
  witness sets using native/caller target identities; and snapshot-qualified
  evidence/dispositions.
- Readiness uses the Evaluation identity-coverage primitive for exact supplied
  frame accounting. It reports resolved, non-applicable, open, abstained,
  deferred, and helpful states. Accepted deferred discovery permits conditional
  handoff only; it is not full readiness. Full statement and branch coverage
  for the new package is 100% (30 focused tests).
- No Retrieval acquisition, task inference, repository-role inference, graph
  traversal, Context integration, or agent execution was added. The next
  production slice is full-task and obligation-scoped Retrieval evidence
  adapters, with native provenance and no satisfaction from rank alone.

## Localization BM25 evidence adapter (2026-10-02)

- Added a one-way Localization-side adapter that retains the complete caller
  task text as a global lexical safety query and runs each explicitly authored
  obligation query independently through production content-plus-filename BM25.
- Each obligation lane carries its task-local query identity, obligation identity,
  exact query string, and untouched native BM25 result. Lane order follows caller
  query order. Repeated resources remain independently surfaced; no cross-lane
  ranking, score normalization, fusion, role filter, or rank-to-satisfaction rule
  was introduced. Snapshot and eligible-resource correspondence are validated
  with Retrieval's existing corpus/snapshot check.
- The adapter is owned by `devtools.context.localization`; Retrieval has no
  dependency on Localization. Focused Localization/Retrieval tests pass with
  100% statement and branch coverage across the Localization package. No
  historical retrieval outcomes were used for tuning or replay.
- Next: prospectively freeze a naturally justified task, caller-authored
  obligation queries, snapshot/frame, BM25 settings and measurements; obtain
  blind obligation-relative resource judgments before joining lane provenance.
  This evaluates acquisition coverage, not satisfaction from rank.

## Deterministic project/test configuration substrate (2026-10-02)

- Extended `context.python.project_configuration` declaration analysis with
  bounded build/project metadata, named script/GUI-script/entry-point strings,
  pytest filename/class/function naming, recursion patterns and opaque addopts.
  Recognized tool-table presence is retained separately. Existing README and
  testpaths selector declarations remain canonical rather than duplicated.
- Added `settings.py` within the established package, immutable setting models
  and explicit absence/unsupported coverage. Semantic key anchors retain exact
  repository/snapshot/resource provenance without invented offsets. The v2
  derivation identifies expanded semantics. Named entry-point declarations
  replace the old unsupported presence-only derivation; no runtime binding or
  configuration execution is implemented.
- Documented intrinsic address/path operations, existing module/package,
  import/member and mirrored-path facts. Added path tests without parallel path
  facts. Public export/`__all__` intelligence remains deferred; validation-command
  ownership remains documented repository convention. No role labels, Retrieval
  routing, filtering, elimination, ranking changes or Case 0004 replay/tuning.
- Focused checks: 72 passed, including 21 setting tests and two intrinsic-path
  tests. Neighboring Python RI/repository checks: 329 passed. Configuration
  package coverage is 100% statements and branches (309 statements, 94 branches).
  Protected development: 1,364 passed, two live skips, 100% of 8,727 production
  statements and 2,036 branches; retained experiment tests excluded.
- Ruff passes for `src`, `tests`, `scripts` and touched-file formatting. Mypy
  passes for `src`/`tests` (463 files). Repository-wide Ruff/mypy were run and
  remain blocked by unchanged Case 0004 experiment helpers (459 lint findings;
  41 typing errors in six files). Frozen experiments remain untouched; these
  unrelated failures are reported rather than repaired in this increment.
- Next: obligation-relative soft repository-role evidence consuming deterministic
  RI and intrinsic resource semantics, retaining the global lexical safety lane
  and avoiding hard path filters. Performance claims require a new prospective
  case; no next-slice implementation is included. Confirmation remains sealed.

## Soft repository-role evidence (2026-10-02)

- Added `context.localization.roles` with responsibility-specific models,
  native-input validation, configuration interpretation and deterministic
  derivation. Its immutable view exposes resource/role explanations and retains
  the complete observed frame. RI and core Retrieval do not depend on it.
- Implemented overlapping Python code, test, documentation, project/test/build/
  tool configuration, package surface and package member support families.
  Exact support kinds distinguish address conventions, native structural facts,
  declaration/table presence and observed configuration targets; no strength
  scale, numeric confidence, relevance judgment or satisfaction rule is added.
- Consumed existing canonical facts rather than duplicating path/configuration
  RI. Bounded array-only case-sensitive basename glob observations reference
  both naming declaration and supplied testpaths target facts. Unsupported
  forms retain limitations. No pytest collection, ignore application, negative
  inference, candidate elimination, BM25 execution or routing is implemented.
  Validation roles, dynamic public exports and semantic document subtypes remain
  deferred. Snapshot provenance and native owner reproduction reject stale,
  foreign and altered analyses; repeated presentation is deterministic.
- Focused tests: 19 passed; new package coverage: 100% of 280 statements and
  86 branches. Neighboring Localization/Python RI/repository tests: 389 passed.
  Protected development: 1,383 passed, two live skips, 100% of 9,007 production
  statements and 2,122 branches. Ruff for `src tests scripts`, touched-file
  formatting and `mypy src tests` pass (473 files); both Git diff checks pass.
  Repository-wide frozen experiment lint/type gates were not rerun or repaired.
- Documented vocabulary, support provenance, static pattern scope, non-claims
  and future routing seam in package docs, architecture/taxonomy, documentation
  map, roadmap and B-0002. ADR-0005 is unchanged. Case 0004 gold/resource-level
  artifacts were not read, replayed or used for tuning; confirmation remains
  sealed. No performance claim follows from this semantic increment.
- Next: consume soft supports in a caller-directed obligation-aware lexical
  routing policy retaining the global BM25 safety lane and an unfiltered escape
  path, then freeze a new prospective case before measurement. That slice is
  not implemented here.

## Candidate witness association (2026-10-02)

- Added a Localization-owned immutable view of caller-supplied unresolved
  candidate witness hypotheses. Alternative hypotheses compete per obligation;
  their individually supported resource members complement one another. One
  observed resource can participate across obligations.
- Kept native BM25 match/lane/rank, repository-role evidence and routed candidate
  provenance intact; checked task, snapshot and exact lane/support membership.
  The association view does not generate hypotheses, rank them, accept witnesses,
  change readiness, assign confidence or eliminate candidates. Finer native
  targets await a native validation contract.
- Case 0005 aggregate evidence motivated the increment; no gold resource or
  witness identity was encoded or replayed. Confirmation remains sealed.
- The focused association suite passes 26 tests with 100% of 132 new
  statements and 52 branches covered. Adjacent Localization/Retrieval/Evaluation
  tests pass (173). Protected development passes 1,418 tests with two live
  skips and 100% of 9,276 production statements and 2,216 branches.

## Caller-directed lexical role routing (2026-10-02)

- Added `context.localization.routing` as a pure view over existing native
  Localization lexical acquisition and soft role evidence. Every acquired
  obligation query requires one caller-authored preferred-role preference,
  including an explicit empty set. No mapping is inferred from obligation or
  query language. Multiple queries for one obligation remain separate.
- Routing uses exactly `PREFERRED_ROLE_SUPPORTED` and `ESCAPE`. Any selected
  positive role qualifies; multi-role support adds no priority. Original BM25
  matches and role-evidence records are referenced, not regenerated. Native
  order/rank/score remain available; routed position identifies presentation
  order. Every obligation candidate appears once in one tier. The global lane
  and complete acquisition remain directly available.
- Validates repository/snapshot scope, role evidence and source frame, lexical
  corpora, query/obligation associations, exact preference coverage and
  acquisition index/settings/bound consistency. No BM25 rerun, score change,
  query fusion, readiness/satisfaction, elimination or candidate filtering.
- Nine focused routing tests pass with 100% of 137 new statements and 42
  branches covered. The focused routing/roles/lexical set passes all 39 tests.
  Protected development passes 1,392 tests, has two live skips, and covers all
  9,144 production statements and 2,164 branches. Production Ruff, touched-file
  formatting and `mypy src tests` (478 files) pass; both diff checks pass.
  Documentation updated in Localization package docs,
  architecture/taxonomy, documentation map, roadmap and B-0002. ADR-0005 is
  unchanged. Case 0004 details were not accessed for tuning; confirmation is
  sealed.
- Next freeze a naturally occurring Case 0005 with obligations, lexical queries
  and role preferences committed before Retrieval; independently adjudicate and
  compare native obligation-lane depth with routed depth. No Case 0005 work or
  effectiveness claim is part of this increment.

## Exact task-anchor grounding (2026-10-03)

- Added caller-authored exact grounding locators under Localization for observed
  resource addresses, explicit-root Python modules, supported direct module
  declarations and directly contained methods. Requests retain task/anchor,
  interpretation provenance and repository/snapshot frame.
- Results retain native referents and RI analysis/lookup evidence, including
  ambiguous, unresolved and unsupported outcomes. The immutable view supports
  deterministic anchor and referent inspection. No free-text inference,
  ranking, witness generation, acceptance, confidence or elimination was added.
- The implementation uses existing RI resolvers and changes no Retrieval,
  routing, Context Planning or repository truth. Case 0005 resource-level gold
  and confirmation outcomes were not accessed.
- Focused grounding tests pass (7); new modules cover all 267 statements and
  70 branches. Neighboring Localization and Python RI tests pass (104). The
  protected development profile passes 1,425 tests, skips two live tests and
  covers all 9,543 production statements and 2,286 branches. Ruff, touched
  formatting, mypy and diff checks pass.

## Bounded candidate-witness generation (2026-10-03)

- Added Localization-owned, caller-authored hypothesis and member generation
  recipes. Each member names an already bounded grounding and one explicit
  operator; each hypothesis recipe supplies complementary shape and a stable
  competing alternative identity. No operator is inferred from task text,
  obligation, query or role preference.
- V1 projects only exact owner resource and canonical observed Python
  source/test mirror. Existing association members now retain validated native
  owner or mirrored-path support. Matching global/own-obligation lexical,
  positive role and own-obligation routed records supplement structural targets
  without generating candidates. ESCAPE remains eligible.
- Single-target admission prevents Cartesian expansion. No target, ambiguous,
  unsupported and unresolved groundings, multi-target results and duplicate
  complementary targets retain attempt diagnostics without partial hypotheses.
  Generated hypotheses remain unresolved. No graph expansion, ranking,
  confidence, acceptance, elimination, or readiness change was added.
- Nine focused generation tests and 26 adjacent association tests cover all
  227 new generation/structural-support statements and 52 branches. The
  focused generation/grounding/association/mirror/membership selection passes
  54 tests. Protected development passes 1,434 tests, skips two live tests and
  covers all 9,779 production statements and 2,342 branches. No Case 0005
  resource-level gold or confirmation outcome was accessed; no prospective
  effectiveness claim follows. Next freeze a new prospective Case 0006 before
  comparing generated-hypothesis coverage and candidate-set size.


## Separate source declaration grounding from binding semantics (2026-10-04)

- Preserved `lookup_python_module_declaration`: its native analyses support a
  conservative static direct-binding target, with decorator/rebinding/dynamic
  guards consumed by Reference and class-base resolution. Grounding previously
  misused NOT_DECLARATION as inability to identify an existing source subject.
- Added package-local `python.modules.selection` over canonical class/function
  RI. Exact module, declaration kind and name retain every matching native
  source declaration and both analyses, without a new parser or subject.
  Decorated ClassDef, FunctionDef and AsyncFunctionDef remain represented;
  repeated same-kind declarations retain ambiguity. Method grounding already
  uses native lexical containment and remains unchanged.
- Localization now consumes source selection, retaining the explicit request,
  native module/subject, snapshot frame, resolver semantics, provenance and
  reason. No runtime/import object identity, callability, public export,
  Retrieval, automatic hypothesis, satisfaction or readiness claim follows.
- Generic regressions cover decorated/rebound declarations, exact kinds,
  duplicate names, methods (plain, staticmethod, classmethod and arbitrary
  decorators), native provenance, frame rejection and imported/member binding
  abstention. The focused selector/grounding tests pass (32); all neighboring
  Python RI and Localization tests pass (402), including association/generation
  and imported-member tests. Protected development passes 1,462 tests with two
  live skips and 100% of 9,798 production statements and 2,340 branches covered.
  Ruff `src tests scripts`, mypy `src tests` (496 files), touched-file formatting
  and worktree/index diff checks pass.
- Updated Python and Localization package contracts, taxonomy clarification,
  documentation map, roadmap and B-0002. ADR-0002/ADR-0005 remain unchanged;
  no accepted-semantic contradiction or durable-schema change was found.
- Case 0006 remains frozen: no Retrieval/routing/grounding/generation replay,
  performance measurement or improved coverage claim. Confirmation outcomes
  remain sealed. Broader candidate-generation relations remain deferred.
- Next reassess the Case 0006 blind-gold diagnosis and choose the smallest
  empirically justified missing candidate-generation relation before freezing
  Case 0007; that relation is not implemented in this checkpoint.


## Bounded branching witness generation (2026-10-04)

- Preserved fixed generation recipes, their caller-named hypothesis identities,
  exactly-one-target admission, and current OWNER/MIRRORED operators. Added one
  explicitly caller-authored `BranchingGroundedMemberRecipe` per recipe family,
  with a positive result bound; two branching members are rejected.
- Separated caller family identity from generated concrete child identity.
  Canonical child keys retain task/obligation/family/member, repository/snapshot
  and native addressed content identity. Typed namespaces, duplicate identity
  checks and canonical native support/target collision checks prevent overwrite
  or order-dependent selection. No random/ordinal identity or durable schema.
- Complete in-bound targets instantiate ordinary unresolved hypotheses with all
  fixed complementary members and exactly one branch target per child. Children
  compete within a retained family; several families can compete per obligation.
  Per-branch duplicate or invalid combinations retain reasons while valid siblings
  may succeed. Fixed failure blocks all children. Empty families remain visible.
- Projection work accounting/completeness/frontier is distinct from the branching
  result bound. Incomplete work admits no child and reports unknown total;
  complete overflow retains exact count and admits no arbitrary prefix. Repeated
  exact targets group their native support, without evidence votes. Each child
  retains only its branch support and identical fixed support. Native lexical,
  role and routing support attaches afterwards without changing cardinality.
- Extended the immutable generation view with family/child lineage and failed
  branch inspection, preserving existing obligation/anchor/target/cross-obligation
  queries. Existing validated association remains the candidate construction path.
  No Reference operator, RI change, Cartesian expansion, graph, score, ranking,
  accepted witness, satisfaction, elimination or readiness change was introduced.
- Added 27 controlled-projection test cases without a fake production relation.
  All 146 neighboring Localization tests pass. After the final production edit,
  protected development passes 1,489 tests with two live skips and covers all
  9,987 production statements and 2,398 branches (100%). Ruff `src tests scripts`,
  mypy `src tests` (497 files), six touched Python format checks and worktree/index
  diff checks pass. ADR-0005 remains unchanged: no accepted boundary contradiction
  or persistence change was found.
- Updated the Localization contract, taxonomy, documentation map, roadmap and
  B-0002; the epic remains open. Frozen experiments and confirmation outcomes
  remain untouched, and Case 0007 is neither frozen nor executed. Next implement
  the narrow exact direct-Reference to referencing-resource generation adapter
  under the settled branching contract; do not freeze Case 0007 in that request.


## Exact direct-Reference witness generation (2026-10-04)

- Added explicit `REFERENCING_RESOURCE` projection over supplied frozen Python
  declaration Reference analyses. Only exact positive native target subject and
  declaration matches qualify. Native function/class/supported method identities
  remain distinct; resource/module groundings are not guessed into declarations.
- Added immutable source-analysis/universe/work inputs and exact native Reference
  structural support under Localization association, with the narrow projection
  adapter under generation. Native RI and Retrieval remain independent. No
  universal reference model, index, cache, graph or new parser was introduced.
- Grouped all matching facts by referencing resource, preserving source spans,
  native analysis/route/import provenance and direct Call tags. Same-owner facts
  remain eligible and use existing duplicate-complement branch failures. Calls
  are not a second relation; imports alone, inheritance and exports are not new
  generation semantics. Decorated source grounding preserves native binding guards.
- Canonical native replay over retained snapshot content validates supplied
  analyses without replacing them or reopening files. Association replays native
  seed/fact membership and exact referencing-resource ownership. Foreign/stale
  metadata, forged facts, inconsistent coverage and identity collisions are
  rejected. Native universe/source interpretation provenance remains intact.
- Work is explicitly bounded by distinct supplied source analyses. Whole-frame
  preflight abstains before replay/enumeration if oversized, retaining zero work,
  unknown target total, full source frontier and its native analysis identities.
  This is not a byte/fact-count/time budget; metadata and association integrity
  replay remain distinct validation costs. The settled branching member alone
  owns the result bound: complete overflow admits no arbitrary prefix.
- Existing branching family/child identity, outcome and complementarity semantics
  remain unchanged, as do OWNER_RESOURCE and MIRRORED_RESOURCE. Reference targets
  produce unresolved child hypotheses only; lexical/role/routing support attaches
  afterward. No relevance, rank, confidence, accepted witness, satisfaction,
  runtime binding/invocation, inheritance, export or readiness claim was added.
- Added 44 adapter/frame/support/integration test cases. The 266-test focused
  Localization/Reference/imported-member regression selection passes. Protected
  validation after the final production edit passes 1,533 tests with two live
  skips and covers all 10,110 production statements and 2,446 branches (100%).
  Both new modules cover all 103 statements and 36 branches (100%). Ruff
  `src tests scripts`, mypy `src tests` (500 files), seven touched Python format
  checks and worktree/index diff checks pass; the protected gate is unchanged.
- Updated Localization and Python Reference consumer documentation, taxonomy,
  documentation map, roadmap and B-0002. ADRs remain unchanged and B-0002 remains
  open. Frozen experiments and confirmation outcomes remain untouched. No Case
  0006 replay/coverage claim or Case 0007 freeze/effectiveness treatment occurred.
- Next freeze prospective Case 0007 evaluating exact declaration grounding plus
  OWNER_RESOURCE, MIRRORED_RESOURCE and direct-Reference branching against
  independently adjudicated witness coverage and candidate-surface size.

## Direct static Python import dependency generation

- Inspected canonical Python declaration, module interpretation, resolved
  module-import relation, direct binding, one-facade member and Reference RI,
  Localization grounding/association/generation and ADR-0002/ADR-0005. Existing
  `PythonResolvedModuleImportRelation` already supplies the exact directed
  source/declaration/resolution/target chain. No native RI semantic change was
  needed or made.
- Added `DIRECT_IMPORT_DEPENDENCY_RESOURCE` with explicit frozen native source
  analyses and exhaustive module resolutions. It projects one forward step to
  the exact target module resource. `ImportFrom` targets the resolved module
  portion, without asserting member identity or following facade imports.
  Relative imports and aliases retain native semantics; nonpositive module
  outcomes and star declarations produce no target. Dynamic/nested imports
  remain outside direct module-body coverage. Ordinary/package resource
  ownership remains exact, with no initializer substitution or recursion.
- Association retains grounding, request, source and all positive native import
  relations per resource. Replay over retained snapshot content verifies native
  analyses/resolutions, module interpretation, frame and target; no current
  filesystem acquisition or independent parser duplicates RI. Repeated imports
  group once with all support; self-import candidates retain fixed/branch
  duplicate-target behavior. Reference provenance remains a separate support.
- One selected source-analysis replay is one per-member work unit; insufficient
  authorization retains an incomplete frontier and no children. This is not a
  declaration/byte/time or total integrity-validation budget. Complete distinct
  resource overflow uses existing `max_results` and admits no prefix. Existing
  family/child, OWNER, MIRROR and REFERENCE semantics remain unchanged.
- Added 46 generic adapter/frame/support/boundary test cases. The 356-test
  focused Localization/import/module/Reference selection passes. Protected
  development validation after the final production edit passes 1,579 tests
  with two live skips, covering all 10,251 production statements and 2,502
  branches (100%). The two new modules cover 119 statements and 44 branches
  (100%). Ruff `src tests scripts`, mypy `src tests` (503 files), seven
  touched-file format checks and worktree/index diff checks pass.
- Updated Localization/import/module consumer docs, taxonomy, documentation
  map, roadmap and B-0002. ADRs remain unchanged; B-0002 remains open. Candidates
  imply no exports, runtime imports, Reference, relevance, ranking, acceptance,
  obligation satisfaction or readiness. Aggregate Case 0007 motivation was used
  without gold-identity/path/obligation tuning or replay; confirmation is sealed.
- Next freeze a NEW prospective Case 0008 evaluating OWNER_RESOURCE,
  MIRRORED_RESOURCE, REFERENCING_RESOURCE and direct import dependency generation
  together. No effectiveness claim or Case 0008 freeze occurs in this increment.

## Explicit evidence-to-witness resolution-recording kernel

- Inspected accepted Localization/ADR-0005 contracts, native association support,
  caller/generated identities, family lineage, accepted witness algebra,
  assessment/readiness and aggregate Case 0008 stopping conclusions. No case
  replay, gold-resource tuning or confirmation access occurred.
- Added language-neutral `localization.resolution` with immutable member decisions,
  hypothesis aggregates, partial views and explicit complete-support promotion.
  Member decisions retain criterion, caller claim/reason, TaskProvenance and exact
  attached native supports through existing LocalizationEvidenceReference values.
  View admission revalidates association frames; copied/stale/foreign contexts,
  substituted supports and duplicate decisions fail.
- Supported and contradicted decisions require explicit evidence. Missing records,
  unresolved evidence and abstention remain distinct. Contradiction dominates the
  aggregate without deleting candidates; complete support needs every complementary
  member. Competing hypotheses and concrete generated children remain independent.
- Explicit promotion reuses native targets, WitnessSet and SupportedWitness,
  retaining both native basis and immutable decision references. Assessment and
  readiness change only through their existing caller-created flow. No automatic
  policy, rank/score, support-count inference, channel preference, elimination,
  frontier/acquisition or Context Planning integration was implemented. Structural
  operators and bounds remain unchanged.
- Nine focused resolution cases exercise lexical-only, OWNER, Reference and Import
  channels, complementarity, competition, sibling lineage, exact frame/basis guards
  and downstream promotion. New production code covers 202 statements and 48
  branches (100%). The 245-test Localization regression selection passes. Protected
  development validation passes 1,588 tests with two live skips and 100% production
  statement/branch coverage. Ruff `src tests scripts`, mypy `src tests` (509 files),
  six touched Python format checks and worktree/index diff checks pass.
- Updated Localization overview, central architecture, taxonomy, documentation map,
  roadmap and B-0002. ADR-0005 remains unchanged; B-0002 remains open. This kernel
  has no prospective automatic-resolution effectiveness claim or durable schema.
- Next investigate and prospectively test the minimum automatic evidence-resolution
  policy producing explicit records from obligation criteria plus native/lexical
  evidence, without numeric confidence or global ranking prematurely.

## Retrieval-foundation reconciliation and roadmap checkpoint (2026-10-05)

- Started from clean `main` at
  `1ec0d2f44267f6034b8981bba1b30d72aa86e6e1`, `Add external semantic resolution
  decision adapter`. Inspected taxonomy/map, central architecture, ADR-0002 through
  ADR-0005, roadmap, B-0002, package contracts, production source and published
  development aggregates. No production source or accepted ADR semantics changed.
- Added [current retrieval foundation](architecture/retrieval.md) as the bounded
  detailed architecture owner, linked from central architecture/documentation map.
  Documented exact/lexical/direct structural/PPR/map/RRF and Localization surfaces,
  canonical unsplit Unicode word/casefold representation, independent content plus
  0.25 filename BM25 (not BM25F), absence of production dense/learned sparse/learned
  ranking, granularity limits, query and discrimination gaps, native provenance
  and Retrieval/Localization/Context boundaries. Corrected stale package statuses.
- Retained verified historical identifier counts 63/63/68/31/74, direct relation
  novelty, weak fixed-window result, sampled graph fan-out, Case 0002 negative
  complete-depth diagnostics, narrow CodeRankEmbed interpretation and prospective
  Localization completion/prefix evidence. No frozen result or judgment was edited.
  Union counts distinguish never-adjudicated pairs from explicit UNJUDGED; neither
  becomes NOT_USEFUL without a scientifically justified labeling/sampling protocol.
- Added six governing failure classes to taxonomy. Future protocols declare the
  primary class before treatment. Preserved open algorithm families and a future
  obligation/resource usefulness formulation without choosing a learning model.
- Rewrote [current roadmap](roadmap.md#current-sequencing) into coordinated tracks:
  mandatory R1 additive whole identifiers/subtokens, then unconditional R2 true
  BM25F irrespective of R1 outcome, A–D comparison arms, independent attribution,
  explicit candidate field investigation and coverage/discrimination/cost metrics;
  then query representation, verified mismatch, valid-label reranking and
  complementary fusion. No algorithm or experimental treatment was implemented.
- Preserved ADR-0005, grounding, candidate/witness contracts, generation, explicit
  resolution recording and the experimental external decision adapter. Prospective
  semantic-resolution effectiveness pauses pending R1/R2 progress unless a concrete
  earlier parallel justification is recorded. Stronger retrieval and semantic
  witness sufficiency remain separate. ADR review found no semantic contradiction
  requiring an ADR change; adoption-time status/next language remains historical.
- Documentation link inspection across architecture/research/backlog and package
  Markdown passes; worktree/index whitespace checks pass. Historical numbers were
  checked against committed published summaries/development records, without
  rerunning retrieval or accessing sealed confirmation outcomes. No effectiveness
  experiment, production test suite, dependency installation or push occurred.
- B-0002 remains open. Next implementation is R1's bounded experimental code-aware
  sparse view, preserving canonical BM25; after its evaluation, benchmark true
  BM25F in R2 whether R1 improves, ties or worsens the baseline.

## Localization continuity audit before retrieval R1 (2026-10-06)

- Started from clean `main` at
  `e136d16d9a746243f3b9a95fee2a296e19b02b53`, `Reconcile retrieval foundation and
  roadmap`. Inspected current architecture/taxonomy/map/roadmap/backlog, accepted
  ADR-0002 through ADR-0005, package contracts, current source and committed
  prospective analysis summaries. No production, test, dependency or frozen
  experiment file changed. No treatment was executed or confirmation outcome accessed.
- Found continuity gaps rather than a new semantic decision: no single
  Localization status/history view, insufficiently explicit resumed experiment
  boundary, central architecture's stale broad nonlexical-acquisition absence,
  and a frontier/handoff diagram without future-status qualification.
- Added [Localization continuity](architecture/localization.md) as the one
  status-matrix/history owner, with caller-directed current flow, resolution
  rationale, Cases 0004-0008 links and source/binding, promotion, assessment and
  readiness distinctions. Central architecture/map/taxonomy/Retrieval/research
  link to it; package API detail remains in existing package documentation.
- Existing earlier entries preserve completed candidate association, grounding,
  decorated-source selection correction, branching, Reference and Import
  generation, and resolution recording. The subsequent
  [semantic-resolution investigation](research/evidence-to-witness-resolution-policy.md)
  is completed research, not accepted automatic policy. The
  [external semantic decision adapter](../experiments/codex_dogfood/semantic_resolution/README.md)
  already implemented at `1ec0d2f44267f6034b8981bba1b30d72aa86e6e1` is
  non-production, model-free, human-review-gated infrastructure. Its three pilot
  dispositions exclude contradiction; no effectiveness case exists yet.
- Preserved Case 0008's structural-breadth stopping decision: retain OWNER,
  MIRROR, REFERENCE and direct Import; no fifth family justified. Prospective
  Reference marginal REQUIRED-cell gain was zero in Cases 0007/0008, while
  Import added a small real Case 0008 gain. Case 0006's repaired-grounding numbers
  remain counterfactual, not a replay. Frozen artifacts and digest qualifications
  remain with their existing summaries.
- Made the [Localization resumption point](roadmap.md#localization-resumption-after-the-retrieval-checkpoints)
  explicit after immediate R1 and unconditional R2 BM25F: a new prospective
  claim-level semantic-resolution case, with candidate inclusion distinct from
  conditional judgments, frozen bounded disclosure/policy/review/gold, proposals,
  human review, explicit materialization and support/abstention/cost evaluation.
  Retrieval findings may change batch/association prerequisites; the semantic
  problem remains. No model or automatic trust policy is selected.
- B-0002 remains open. Proof-scoped contradiction/elimination, unresolved
  frontier, bounded acquisition requests, iterative reacquisition/sufficiency,
  automatic Context handoff and autonomous coding-agent evaluation remain future.
  Case 0008's task and generation-local enumeration diagnostics implement none
  of those APIs. Agent/orchestration retains execution/retry ownership; Context
  retains representation/capacity; unknown labels are not negatives.
- Documentation link/heading checks, roadmap/status/source consistency inspection
  and worktree/index whitespace checks pass. ADR semantics remain consistent and
  unchanged; historical adoption-time/next statements remain historical. No
  production test suite, effectiveness experiment, model call or push occurred.
- Next work remains R1's bounded experimental whole-identifier-plus-subtoken
  sparse view with canonical BM25 unchanged, then true BM25F R2 regardless of
  R1 outcome. This checkpoint implements neither.

## Experimental R1 implementation and prospective protocol (2026-10-06)

- Started from clean `main` at
  `d71d741f3a91bf4c4a2b40619d1b8042853f6881`. Added an experiment-owned
  [whole-identifier-plus-subtoken view](../experiments/identifier_sparse/README.md)
  and [prospective Case 0009](../experiments/codex_dogfood/case_0009/README.md).
  No production source, existing production test, dependency or public API changed.
- Reused Increment 27's deterministic splitter (already whole plus subtokens)
  and production BM25 IDF/contribution arithmetic. Experiment-owned indexes
  preserve whole-resource granularity, independent content/filename statistics,
  `k1=1.2`, `b=0.75` and filename weight `0.25`. Content, filename and query
  analysis change together; no BM25F, expansion, tuning or structural/fusion arm.
- Pinned analyzer source bytes before checking three saved development query
  strings. Exact historical term-stream parity is a mechanical diagnostic,
  not a historical effectiveness replay or new effectiveness claim.
- Case 0009 selects a realistic future explicit assessment-bridge task, with
  nine caller-authored obligation queries plus the complete task lane. No gold
  resource selection. Its Stage A pins native snapshot/corpus/document identities,
  implementation and representation-record digests, unchanged scoring parameters,
  paired gain/loss metrics, cost limits and the pre-result decision rule.
- Stage B execution and full-frame treatment-free packet are separate checkpoints;
  independent blind judgments and joined effectiveness are not part of this
  implementation freeze. Effectiveness remains UNKNOWN. No production promotion,
  sealed confirmation access, model call or push. R2 true BM25F remains mandatory
  whether R1 improves, ties or worsens; Localization's resumption point is unchanged.

## R1 Case 0009 Stage B capture (2026-10-06)

- Committed Stage A at `eb4060ff8ffd1ff0bf18e11c47d162a6c02bd0f2` before
  executing either arm. Then executed each arm once, across ten identical query
  lanes over the native frozen 531-resource frame. No retries, tuning, fusion,
  structural arm or production change.
- [Stage B record](../experiments/codex_dogfood/case_0009/stage_b.md) links
  costs and the independent full-frame packet. Capture replay verifies digests,
  identities, positive rank ordering and field contributions without reranking.
  The packet exports 531 contents and nine obligation criteria, no treatment
  ranks/scores/terms or membership. Leakage/coverage and integrity checks pass.
- R1 and existing lexical tests: 66 pass. Scoped Ruff, format and mypy pass;
  documentation links/anchors and worktree/index whitespace checks pass. Full
  protected development validation is not required: production code is unchanged.
- **Effectiveness UNKNOWN**: no Stage C judgments, gold join or promotion decision.
  Next is independent blind adjudication from packet files only, then paired
  gain/loss and representation-attribution analysis. R2 remains unconditional;
  Localization's resumption point and sealed confirmation remain untouched.

## R1 Case 0009 Stage D joined evaluation (2026-10-06)

- Verified ordered Stage A/B/packet-repair/clean Stage C ancestry and immutable
  committed gold bytes. Joined 531 resources, 9 obligations and 10 frozen lanes
  with exact repository/snapshot/corpus/task/resource/query identities.
- [Stage D](../experiments/codex_dogfood/case_0009/analysis.md) prospectively
  evaluates R1: **RETAIN AS SEPARATE RETRIEVAL VIEW**. Both arms reach all 23
  REQUIRED resources, 37 cells, 42 obligation-relative unit judgments and 40
  distinct units; positive-reach gains/losses/rescues are zero.
- Global completion improves 342 to 331, but maximum own completion worsens
  185 to 231. Own prefix occurrences fall 454 to 423 and union 257 to 252:
  only 5/257 = 1.9455%, below the frozen 20% promotion threshold. Paired required
  ranks: 13 improved, 9 tied, 15 worsened. One required top-20 entry and three
  improved obligation completions satisfy the frozen separate-view rule.
- Exact source/query/filename attribution and captured-statistic verification
  distinguish ranking gains from representation rescues and record regressions.
  Captured costs pass all frozen 3x gates; different provenance representations
  prevent attributing footprint differences solely to lexical expansion.
- 15 focused Stage D tests pass; deterministic JSON/Markdown replay, scoped
  Ruff/format and diff checks pass. Frozen gold/treatment and production code
  remain unchanged. Invalid quarantined gold and confirmation were not accessed.
- Mandatory **R2 true BM25F / field-aware sparse retrieval is next regardless
  of R1 outcome**. No production adoption, fusion, BM25F implementation or
  semantic-resolution resumption is authorized by this checkpoint.

## R1.5 Retrieval Diagnostics and Failure Attribution (2026-10-06)

- Added [experimental retrieval diagnostics](../experiments/retrieval_diagnostics/README.md)
  over existing native lexical scoring/statistics and optional independent
  obligation judgments. Native repository/snapshot/corpus/resource identities,
  exact query/lane, treatment/index identity and explicit settings are retained.
  Production Retrieval, RI and Localization gain no dependency on evaluation gold.
- Query footprints/yields, field/term decomposition, source/query identifier
  lineage, zero-score/bounded/excluded states, overtakers and paired treatments
  serialize deterministically. Captured scores and contributions are checked
  against the existing canonical arithmetic. Failure certainty and multi-factor
  observations remain explicit; lexical evidence cannot prove semantic equivalence
  or why a structural relation makes a witness necessary.
- [Case 0009 dogfood](../experiments/retrieval_diagnostics/case_0009.md) covers all
  37 REQUIRED cells in each arm with 74 reproduced required scores and the original
  paired ranks/overtaker sets. At the descriptive threshold of 20 unnecessary
  overtakers, ranking burden is established for 8 A cells and 7 B cells. Twelve
  partial hidden identifier-match cells provide zero positive REQUIRED reach
  rescues. Frozen R1 conclusions and its original replay helper remain unchanged.
- 41 focused tests pass; reusable diagnostic modules have 100% branch coverage,
  overall package coverage is 99% including the dogfood CLI. Deterministic capture
  replay, score reconstruction, partition/identity/tamper checks, scoped
  Ruff/format/mypy and worktree/index whitespace checks pass. Production source,
  frozen gold/treatments, quarantine and confirmation remain untouched.
- Current roadmap: R1 done, retain separate view; R1.5 done; **R1.6 canonical
  BM25 parameter sensitivity next**, then R1.7 query-term investigation, mandatory
  R2 true BM25F, R3–R6 and the preserved Localization continuation. No parameter
  tuning, query weighting, BM25F or semantic-resolution experiment in this increment.

## R1.6 canonical BM25 parameter sensitivity, through prospective Stage B (2026-10-06)

- Precommitted the full 6 x 5 x 6 parameter protocol, native frozen-input audit,
  normalized multi-objective selection, safety/tie rules and prospective thresholds.
  A pre-grid baseline check found two Case 0008 own-lane lexical misses; corrected
  eligibility before historical nonbaseline outcomes. Five complete cases select
  challengers; all six participate in required-reach safety and 180-point replay.
- All 180 configurations preserve required reach. Native historical scores/order,
  parameter scoring oracles and R1.5 decomposition agree. Complete grid/surfaces,
  98 Pareto configurations, losing points, exact alternatives and representative
  deterministic diagnostics are retained under `experiments/bm25_sensitivity/`.
  Three unique challengers: completion (2.4, 0, 2), burden (2.4, 0.5, 1), robust
  (2.4, 0.75, 0.25). Cross-case effects remain mixed, including global regressions;
  no development point is adopted into production.
- Audited retained BM25+ evidence and available BM25L/other library formulas;
  no additional variant prerequisite is justified before BM25F. Open variant
  hypotheses remain in the audit; no new variant benchmark was run.
- Selected Case 0010's realistic unimplemented caller line-range disclosure task
  after development freeze. Committed Stage A over the starting R1.5 Git snapshot,
  531 resources and ten obligations; then executed four arms x eleven queries
  once using identical canonical representation and shared native indexes.
  Captured timing excludes diagnostic construction; evidence replay does not
  rerun treatments. Full-frame deterministic blind packet and external sterile
  workspace contain only blind inputs. Stage C NOT PERFORMED; effectiveness UNKNOWN.
- Production parameters, historical treatment/gold and Localization continuation
  remain unchanged. R1.7 follows completed prospective R1.6, then mandatory true
  BM25F R2. No query weighting, BM25F or semantic-resolution work in this checkpoint.
- Validation: 62 focused experimental tests, exact deterministic diagnostic
  replay, 44-lane captured score/universe reconstruction, cross-case partitions,
  challenger/tie/alternative checks, packet double-build/leakage/overwrite checks,
  scoped Ruff/format and strict mypy pass. No production source changes;
  protected production and confirmation profiles were not invoked.
