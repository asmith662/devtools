# Filesystem future evolution

This document records concrete evaluation areas, not committed implementation
work. See the current [overview](overview.md) and [I/O contract](io.md).

## Completed bounded binary I/O

`BinaryCodec`, static resolution, public exports, explicit generic binary reads
and atomic binary writes are maintained on `feat/qwen-context-worker` in
`f799be1d32c2dffc22a39ff5110a0a4af5714b07`. No arbitrary binary format detection
was added. The [engineering record](../../../../../apps/qwen/evaluation/engineering-08/README.md)
distinguishes Qwen source, host-only formatting and independent regressions from
the unsuccessful live task. Protected-main adoption remains separate.

## Completed bounded stream reads

Qwen's bounded reader is feature-published in `61637ff8`, with independent
stream-consumption and Repository-observation regressions. Finite reads stop at
the limit plus one sentinel byte even after growth; legal short reads accumulate.
The [continuation record](../../../../../apps/qwen/evaluation/continuation-09/README.md)
distinguishes the original invalid oracle from the accepted corrected development
continuation. Format-specific streaming remains conditional on concrete consumers;
this does not promise an exact total-process memory cap or protected-main adoption.

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
