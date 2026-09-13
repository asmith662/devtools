# Filesystem future evolution

This document records concrete evaluation areas, not committed implementation
work. See the current [overview](overview.md) and [I/O contract](io.md).

## Binary I/O

A BinaryCodec and explicit generic binary read/write policy may be justified.
This does not imply arbitrary binary format detection.

## Strict bounded and streaming reads

Streaming or chunk-bounded reads could enforce a hard memory bound where
current stat/read/post-check behavior is insufficient. Format-specific
streaming should be added only where consumers require it.

## Source-format-preserving writes

Structured JSON and CSV transformations currently serialize current state,
not original formatting. More faithful output could be evaluated if consumers
demonstrate a need; arbitrary round-trip fidelity is not promised.

## Markdown source fidelity

Exact Markdown section source slices, and richer structure, may be justified
only by concrete consumers.

## Format evaluation

TOML, YAML, XML, and source-code models are candidates for future evaluation,
not commitments.

## Explicit non-goals

Plugin discovery, dynamic codec registries, filesystem authorization,
sandbox policy, and repository indexing remain outside the immediate
filesystem roadmap.
