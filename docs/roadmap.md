# Roadmap

## Status model

This document records architectural sequencing, not detailed package backlogs.
Package-local documentation owns each package's deferred capability work.

- **Complete**: implemented, tested, documented, and frozen for its current
  milestone.
- **Next**: the next architectural domain to design; not authorization to
  implement it without its own approved scope.
- **Later**: dependent architectural work that follows a prior domain.

## Foundation — Complete

| Package           | Role                                                | Milestone status    | Package docs |
|-------------------|-----------------------------------------------------|---------------------|--------------|
| `identity`        | Opaque UUID identity primitive                      | Documented / Frozen | Complete     |
| `system`          | Operating-system-family detection                   | Documented / Frozen | Complete     |
| `paths`           | Path values, parsing, and resolution                | Documented / Frozen | Complete     |
| `time`            | Timestamp, duration, parsing, and timing primitives | Documented / Frozen | Complete     |
| `commands`        | Direct asynchronous process execution               | Documented / Frozen | Complete     |
| `regex`           | Regex utilities and immutable matches               | Documented / Frozen | Complete     |
| `conversion`      | Explicit callable conversion                        | Documented / Frozen | Complete     |
| `filesystem`      | Models, codecs, and generic file I/O                | Documented / Frozen | Complete     |
| `context.message` | Immutable textual communication values              | Documented / Frozen | Complete     |

The completed foundation includes command execution lifecycle hardening,
awaitable executions, streaming best-effort events, bounded command buffering,
and immediate-child cancellation cleanup. It also includes the regex and
conversion domains; text, JSON, Markdown, and CSV filesystem models/codecs;
bounded generic reads; atomic generic writes; and the package-local
documentation/freeze pass.

The Message milestone adds semantic message identities, role/source separation,
immutable textual content, and package documentation/freeze without adding
provider, session, or runtime state. It now belongs to the established
`devtools.context` domain, which will later own History and Session.

Historical implementation labels such as `PATH-1A`, `TIME-1A`,
`FILESYSTEM-1A`, `JSON-CODEC-1A`, and `FILESYSTEM-2A` are complete history, not
active roadmap items. See the [implementation ledger](implementation_ledger.md)
for the record.

## Codex integration — Complete

`devtools.codex` is the first concrete `Agent` implementation. Its frozen
milestone includes real Codex CLI execution through `CommandExecutor`, JSONL
final-turn parsing, provider thread continuation through `ConversationRef`,
read-only fresh and resumed invocations, and a real two-turn continuity
acceptance test.

`devtools.agents` is also implemented, documented, and frozen as the
provider-neutral structural contract consumed by Codex. It provides `Agent`,
`AgentTurn`, and `ConversationRef` without provider transport or session state.

## Context establishment / Message migration — Complete

`devtools.message` moved cleanly to `devtools.context.message` before History
and Session implementation. The relocation retained Message behavior exactly,
introduced no compatibility alias, and preserved the real Codex integration.

## Context History — Complete

`devtools.context.history` is the documented and frozen immutable
insertion-ordered Message transcript. Its milestone includes standard read-only
Sequence behavior, History-preserving slices, immutable append, and no history
identity, timestamps, provider state, or event-log scope.

## Context Session — Complete

`devtools.context.session` is the documented and frozen mutable lifecycle for
one retained interaction. Its milestone includes `SessionId`, immutable History
replacement, current source-keyed `ConversationRef` storage, real Codex
continuation through stored state, read-only resumed execution proof, and a
revised private per-object asynchronous turn context that serializes complete
same-Session turns while allowing different Sessions to proceed concurrently.

The current one-ref-per-`MessageSource` policy is sufficient for one logical
Agent per source. Multiple logical same-source Agents require a separate
participant/Agent-instance identity design before that topology is supported.

## Runtime â€” Complete

`devtools.runtime` is documented and frozen as a configuration-bearing but
interaction-stateless coordinator of one caller-selected Agent interaction with
one Session. Its keyword-only `send()` holds Session complete-turn coordination,
records input/output in order, validates returned source, updates non-None
continuations, and preserves forward-only failure/cancellation semantics.
Its optional fixed AttemptObserver creates no Attempt when absent and observes
an admitted Attempt through terminalization when present. Deterministic tests
prove same-Session serialization, same-source continuation handoff, and
different-Session concurrency; opt-in Codex acceptances prove both unchanged
two-turn continuation and one observed real Attempt in isolated repositories.

## Persistence â€” Complete

`devtools.persistence` is documented and frozen as the durable semantic
reconstruction boundary for Context Session state. Its milestone includes strict
versioned portable JSON, a normalized SQLite current-snapshot store, immutable
Message/Session conflict protection, atomic snapshot replacement, missing-row
corruption detection, and fresh Session turn coordination on reconstruction.
Deterministic tests prove Runtime continuation after load; an opt-in SQLite
acceptance proves a reconstructed Session resumes the same real Codex thread in
an isolated temporary repository.

## Evidence - Complete / Frozen

`devtools.evidence` is documented and frozen for its live Attempt lifecycle and
immutable terminal value-model milestones. `Attempt` remains the mutable
identified lifecycle handle with Session/Message/source attribution;
`AttemptTerminalEvidence` is a distinct immutable, hashable historical record
identified by `EvidenceId`, referring to `AttemptId`, timestamps, and a typed
terminal outcome. The six-value `AttemptStage` vocabulary records processing
location rather than cause. Runtime does not yet produce terminal Evidence, and
EvidenceSink, EvidenceRecord, delivery, and persistence remain deferred.

## Runtimeâ†”Attempt integration â€” Complete

The optional Runtime↔Attempt observation seam is implemented, audited,
corrected, documented, and frozen. It preserves no-observer Runtime behavior,
creates Attempts only after input retention, and keeps primary Runtime outcomes
authoritative over ordinary/cancellation secondary observation errors.

## Package-level future work

The completed foundation can evolve through future approved capabilities.
Those possibilities are maintained in package-local documentation rather than
duplicated here. The next architectural discussion is Runtime-to-terminal-
Evidence production and delivery design. Attempt/Evidence persistence and
retry/replay remain separate future work.

See the [documentation map](documentation_map.md) to locate package-specific
future-work documentation.
