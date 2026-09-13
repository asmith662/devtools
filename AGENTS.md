# Repository Operating Guide

## Purpose and authority

This file defines repository-operating rules for coding agents. It does not
replace semantic architecture, package documentation, source/tests, accepted
architecture decisions, or backlog records.

Use this authority order:

1. [Architecture taxonomy](docs/architecture/taxonomy.md) defines terminology
   and distinctions.
2. [Documentation map](docs/documentation_map.md) defines documentation
   authority and navigation.
3. Current source and tests define implemented behavior.
4. `docs/architecture.md` and any accepted future ADRs define cross-package
   architectural decisions.
5. Canonical `docs/backlog/` records preserve unresolved pressure and do not
   authorize implementation.

The implementation ledger is historical evidence, not an API or future-work
authority. If these sources materially conflict, stop and report the evidence.

## Inspect before inventing

Before introducing or materially changing a reusable primitive, type,
abstraction, protocol, helper, package, parser, execution mechanism,
persistence representation, lifecycle concept, or provider/model abstraction:

1. Read this file and the relevant taxonomy terms.
2. Use the documentation map to find authoritative package and architecture
   documentation.
3. Locate relevant backlog records, including dependencies and promotion
   triggers when unresolved architecture is involved.
4. Inspect relevant source and tests.
5. Search for canonical primitives and substrates already owning the work.
6. Determine dependency, public-API, persistence, test, and documentation
   impact.
7. Surface a contradiction before editing; only then implement.

Do not read the entire repository for bounded work. Read enough to establish
the owner, boundary, and existing mechanism.

## Reuse canonical primitives and substrates

If the repository provides a canonical primitive or substrate for a
responsibility, higher layers must use it unless an explicit architectural
decision justifies bypassing it.

- Use `devtools.core.time` values such as `Timestamp` for framework timestamps;
  do not independently use `datetime.now()`, `datetime.utcnow()`, or similar
  wall-clock construction outside the time domain or a documented external
  boundary.
- Use domain semantic identity wrappers built on `devtools.core.identity.Identity`
  when the repository owns that identity concept. Do not invent parallel UUID
  strings for the same semantic identity.
- Use `devtools.core.paths` for semantic resolved paths and resolution policy. Do
  not reimplement path normalization, repository-root resolution, or existing
  containment behavior.
- Use `devtools.resources.commands` for managed subprocess work. Higher domains must
  not call direct `subprocess` or `asyncio` subprocess APIs without explicit
  architectural justification.
- Use `devtools.resources.filesystem` for its existing file models, decoding, bounded
  reads, and atomic writes. Do not recreate those semantics in Tools, Context,
  Agents, or experiments.

These rules do not prohibit unrelated external UUIDs, timestamps, paths, or
processes at genuine external boundaries; verify ownership first.

## Taxonomy and transitional names

Consult [the taxonomy](docs/architecture/taxonomy.md) before adding or changing
architectural concepts. In particular, preserve these distinctions:

```text
Model != Agent                    Conversation != Run
ConversationTurn != ModelInteraction
ConversationMessage != Prompt     ModelResponse != AgentResult
Run != Step != Attempt            Context != Memory != Persistence
Resource != Tool != Action        Capability != Authorization
Evidence != Trace != Telemetry    ModelServing != ModelInteraction
Provider != model identity        Orchestration != narrow Runtime
```

Current source names are transitional and do not override taxonomy meanings:

- `Conversation`, `ConversationMessage`, and `ModelInteraction` are current
  names; do not reintroduce their predecessor names as compatibility APIs.
- `InteractionAttempt` is the current specialized execution lifecycle, not a
  generic Step Attempt.
- Codex is an external Agent integration.
- Qwen experiments are experimental agent/action-loop evidence.

Do not rename these during unrelated work. Terminology migration requires
explicit authorization.

## Backlog and promotion

Find canonical architectural pressure in `docs/backlog/overview.md`,
`docs/backlog/metadata.md`, and the linked `epics/` and `items/` records.
Respect the distinction among hard, pressure, and operational dependencies, as
well as each record's decision maturity and promotion trigger.

Backlog presence is not implementation authorization. Do not mark a concern
resolved because one experiment resembles it. Update a record only when the
authorized task requires it and evidence actually changes it.

## Stop and report

Stop instead of improvising when work would require an unapproved change to:

- taxonomy meaning, package ownership, or dependency direction;
- Model/Agent separation or Conversation/execution lifecycle semantics;
- Runtime/orchestration ownership;
- Tool/Action/Capability/Authorization boundaries;
- persistence or durable-schema compatibility;
- Evidence/Trace/Telemetry boundaries; or
- authority, governance, or destructive external-state ownership.

Also stop when authoritative docs contradict implementation, a new top-level
reusable package lacks an architectural home, existing worktree changes overlap
ambiguously, or a request would silently broaden a narrow abstraction. Report
the conflict and supporting files rather than choosing architecture locally.

Before creating a reusable type or package, be able to state its taxonomy
concept, responsibility, allowed dependencies, likely dependents, why an
existing domain does not own it, whether it is framework or experiment code,
and what evidence authorizes promotion. If not, stop and report.

## Framework, experiments, and integrations

`src/devtools/` contains reusable supported framework capabilities.
`experiments/` contains repository-owned, non-installable probes and bounded
consumer composition. `scripts/` contains operational/developer entry points.

```text
experiments -> devtools    allowed
devtools -> experiments    prohibited
```

Model-specific experiment composition stays outside reusable source until its
semantics are explicitly promoted. Conversely, a provider implementation that
genuinely implements reusable infrastructure is not automatically an
experiment.

Model identity is normally configuration, not a new `QwenAgent` or
`DeepSeekAgent` class. A Model is inference capability; an Agent owns a
goal-directed process. Codex is semantically an external Agent, not merely a
raw Model provider; do not move or redesign that integration without explicit
authorization.

Resources such as filesystem and commands may be adapted into Tools. A Tool is
not an Action; an Action request is not authority. Preserve:

```text
model proposal != authority       visibility != authorization
Tool validation != authorization  approval != automatically authority
capability availability != authorization
```

Local experiments may use explicit parsing and branching. Do not introduce an
Action/Capability registry, policy framework, or generic dispatcher merely to
remove local branches.

## Runtime, lifecycle, Context, and evidence

Current Runtime is intentionally narrow: one selected ModelInteraction
coordinated with one Conversation plus optional specialized InteractionAttempt
observation. Evidence construction remains in observability. Do not put general Agent loops, workflow graphs, multi-Agent
coordination, scheduling, supervisor/worker logic, generic retries, or
orchestration policy into Runtime.

Conversation is distinct from Run. Generic Run, Step, and Attempt are taxonomy
concepts, not authorization to create framework classes. Do not broaden current
`Attempt` into Tool or Command attempts without explicit lifecycle work.

Context is information selected as relevant to a purpose, not a universal
mutable state bag. It may draw from Conversation, Resources, Memory, Tool
results, Evidence, documentation, or Run state without owning those sources.

Persistence stores/restores representations owned by other domains. It does
not thereby own Conversation, Run, Memory, Evidence, Agent, or Context. Do not
casually change durable compatibility or assume a wire representation equals a
runtime representation.

Evidence is factual/historical observation, not Trace, Telemetry, or current
authority. Do not create Event/Trace/Telemetry infrastructure merely for one
bounded report. Preserve:

```text
cancellation != rollback
communication failure != proof an external effect failed
persistence != exactly-once external effects
```

Do not blindly retry side-effecting work after ambiguous failure. Stop or use
explicitly authorized reconciliation semantics.

## Documentation and validation

For every source change, perform a documentation-impact check: package docs,
architecture docs, documentation map, backlog, and historical ledger as
applicable. Update behavior claims where behavior changes. Update authoritative
architecture only for actual architectural changes. Do not rewrite historical
records as if older terminology never existed.

The normal deterministic validation suite is:

```text
uv run ruff check .
uv run mypy
uv run pytest
git diff --check
```

Pytest is configured for branch coverage with `--cov-fail-under=100`. When
finalizing staged work, also run `git diff --cached --check`. Do not run live
model/Docker tests for ordinary work; live tests require explicit authorization
and are reported separately.

For read-only audits: do not fix while inspecting; list evidence inspected,
separate fact from interpretation, report findings by severity, and do not
stage or commit.

## Git and external-state safety

- Inspect HEAD, branch, index, worktree, and `git diff --check` before edits.
- Never discard pre-existing user work. Do not reset, clean, checkout, stage,
  commit, or push unless explicitly authorized.
- Preserve staged/unstaged distinctions and do not commit temporary/live
  artifacts.
- Do not start, stop, restart, or otherwise mutate Docker/model services
  unless explicitly authorized.
- Do not delete model caches. Verify ownership before destructive lifecycle
  operations.
- Treat live acceptance artifacts as temporary unless explicitly designated
  repository artifacts.
