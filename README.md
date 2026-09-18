# devtools

## Purpose

`devtools` provides composable infrastructure for building governed intelligent
systems.

Its long-term direction is:

> **A governed evolving intelligence framework capable of acquiring, creating,
> evaluating, composing, modifying, and retiring heterogeneous intelligence
> capabilities.**

"Heterogeneous intelligence capabilities" is intentionally broader than LLMs
or Agents. It can include deterministic software, retrieval and selection
mechanisms, Tools, learned components, specialized Agents, models, and
capability forms not yet anticipated. This is a project direction, not a claim
that autonomous self-evolution, continual learning, self-modification, model
training, or governance automation is currently implemented.
Its present scope is intentionally narrower than that long-term horizon.

## Current direction

Current work establishes the foundational substrates and semantic boundaries
needed for increasingly capable systems. Repository Intelligence is intended to
produce deterministic, explicit, reusable knowledge about identified repository
state. Retrieval discovers potentially useful information for a purpose, while
Context governs bounded selection, representation, materialization, and
disclosure.

Together, these capabilities support evidence-backed understanding of software.
A future governed system may use that understanding to reason about and evaluate
changes to its own software or capabilities. Repository Intelligence itself does
not own self-modification, Agent behavior, learning, or governance; those remain
separate responsibilities.

The repository currently contains implemented lower-level primitives alongside
accepted but unimplemented architecture. Architectural acceptance must not be
read as implementation completion.

## Engineering posture

The project favors explicit semantics, deterministic foundations where
appropriate, stable identity and provenance, factual Evidence, evaluation, and
bounded authority. Responsibilities remain composable rather than being
absorbed into one universal Agent or Runtime. Semantic distinctions are
preserved early, while generalized registries, lifecycle machinery, storage,
and other universal abstractions wait for concrete evidence.

## Documentation

- [Architecture](docs/architecture.md)
- [Roadmap](docs/roadmap.md)
- [Documentation map](docs/documentation_map.md)
