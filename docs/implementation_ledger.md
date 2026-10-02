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
