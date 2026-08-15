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

| Package | Role | Milestone status | Package docs |
|---|---|---|---|
| `identity` | Opaque UUID identity primitive | Documented / Frozen | Complete |
| `system` | Operating-system-family detection | Documented / Frozen | Complete |
| `paths` | Path values, parsing, and resolution | Documented / Frozen | Complete |
| `time` | Timestamp, duration, parsing, and timing primitives | Documented / Frozen | Complete |
| `commands` | Direct asynchronous process execution | Documented / Frozen | Complete |
| `regex` | Regex utilities and immutable matches | Documented / Frozen | Complete |
| `conversion` | Explicit callable conversion | Documented / Frozen | Complete |
| `filesystem` | Models, codecs, and generic file I/O | Documented / Frozen | Complete |
| `context.message` | Immutable textual communication values | Documented / Frozen | Complete |

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

## Next: Session

`devtools.context` Session is the application-owned lifecycle
for durable interaction state. Its public API, models, continuation policy, and
storage policy remain intentionally undesigned.

## After Session: Runtime

`devtools.runtime` follows session as a later composition and orchestration
layer. It may consume established primitives and session abstractions, but no
runtime architecture is specified by this roadmap.

## Package-level future work

The completed foundation can evolve through future approved capabilities.
Those possibilities are maintained in package-local documentation rather than
duplicated here. None is currently a prerequisite for session design.

See the [documentation map](documentation_map.md) to locate package-specific
future-work documentation.
