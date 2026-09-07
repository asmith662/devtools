# `devtools.model_serving`

## Status

Experimental and unfrozen. This first slice supports only concrete vLLM Docker
server lifecycle management.

## Purpose

`devtools.model_serving` makes a pinned Hugging Face model repository available
through a selected local serving provider and exposes that server's endpoint,
readiness, and safe owned-container lifecycle.

It does not define model invocation, chat, Agents, Runtime behavior, tools,
benchmarks, Evidence, or evaluation.

## Current scope

The vLLM implementation uses an explicit pinned image, a caller-visible Hugging
Face cache root, an exact pinned repository revision, Docker CLI execution via
`devtools.commands`, readiness probes, and ownership-safe stop behavior.
Readiness waiting is caller-configurable; its default remains ten minutes.

## Required future pressure tests

vLLM is the first provider, not the provider ontology. llama.cpp and SGLang
must independently pressure-test any future common lifecycle abstraction.
Future work includes selectable providers and pinned Hugging Face references,
cache visibility, a user-facing lifecycle CLI, and benchmark consumers. The
default deployment direction is a pinned provider image plus runtime model
selection, not per-model Dockerfiles.
