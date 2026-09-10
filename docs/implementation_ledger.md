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

## Agent integration milestone

- Implemented `devtools.agents` as the provider-neutral structural Agent
  contract: async `Agent`, immutable `AgentTurn`, and opaque
  source-owned `ConversationRef` values with source ownership invariants and
  stateless-turn support. Its only production dependency is `context.message`.
- Implemented and froze `devtools.codex` as the first concrete Agent adapter:
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
