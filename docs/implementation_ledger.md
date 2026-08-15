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

## Verification snapshot

At the History-freeze checkpoint:

```text
Ruff: clean
mypy: clean
pytest: 326 passed, 1 skipped
branch coverage: 100%
git diff --check: clean
```

## Deferred work

Deferred work belongs primarily in package-local documentation. Examples
include path containment, additional filesystem codecs or streaming, richer
Markdown source fidelity, command process-tree management, and conversion
extensions. These are not active repository-level milestones unless they become
prerequisites for a future architectural domain.
