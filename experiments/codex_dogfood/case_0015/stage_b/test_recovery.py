# Copyright (c) 2026
# ruff: noqa: S101, PLR2004 -- synthetic capture boundaries
"""Metadata-only mutation, bounded allocation and durable launcher invariants."""

from __future__ import annotations

import asyncio
import pickle
import sys
import tracemalloc
from dataclasses import replace
from pathlib import Path
from unittest.mock import patch

import pytest

from devtools.context.retrieval.lexical.bm25 import (
    analyze_repository_text_lexical_query,
)
from devtools.core.paths import resolve_path
from devtools.resources.commands import Command, CommandExecutor
from experiments.bm25f import scoring
from experiments.bm25f.test_scoring import fixture
from experiments.codex_dogfood.case_0012.stage_b.durability import Journal
from experiments.codex_dogfood.case_0015.stage_b import fingerprint as metadata
from experiments.codex_dogfood.case_0015.stage_b.records import (
    PreparedFields,
    PreparedFrame,
)


def test_frozen_scientific_code_and_results_equal() -> None:
    """Only metadata validation is rebound; scoring bytecode/defaults are identical."""
    state = fixture(("alpha.txt", "alpha alpha quiet"), ("---.txt", "quiet"))
    query = analyze_repository_text_lexical_query(text="alpha quiet absent")
    original = scoring.score(state, query, snapshot_id=state.snapshot.id)
    amended = replace(state, observation_sha256=metadata.fingerprint(state))
    assert metadata._score.__code__ is scoring.score.__code__  # noqa: SLF001
    assert metadata._score.__kwdefaults__ is scoring.score.__kwdefaults__  # noqa: SLF001
    assert metadata.score(amended, query, snapshot_id=state.snapshot.id) == original


def test_forbidden_rich_repr_repeat_stream_and_memory() -> None:
    """Explosive graph repr cannot run; peak metadata allocation stays compact."""
    state = fixture(("alpha.txt", "alpha quiet " * 2000), ("quiet.txt", "quiet"))
    with (
        patch.object(type(state.content), "__repr__", side_effect=AssertionError),
        patch.object(type(state.filename), "__repr__", side_effect=AssertionError),
        patch.object(type(state.collection), "__repr__", side_effect=AssertionError),
    ):
        tracemalloc.start()
        first = metadata.fingerprint(state)
        _current, peak = tracemalloc.get_traced_memory()
        tracemalloc.stop()
        assert first == metadata.fingerprint(state)
        assert peak < 2 << 20  # generous compact-state bound, independent of RSS


@pytest.mark.parametrize(
    "mutation",
    ["average", "length", "observation", "tf", "df", "posting", "order", "identity"],
)
def test_each_compact_state_mutation_changes_digest(mutation: str) -> None:
    """Independent scalar/order/identity changes cannot keep the metadata seal."""
    state = fixture(("alpha.txt", "alpha quiet"), ("quiet.txt", "quiet"))
    baseline = metadata.fingerprint(state)
    if mutation == "average":
        changed = replace(
            state,
            filename=replace(state.filename, average_document_length=2.0),
        )
    elif mutation == "identity":
        changed = replace(
            state,
            collection=replace(
                state.collection,
                documents=state.collection.documents[::-1],
            ),
        )
    elif mutation == "order":
        changed = replace(
            state,
            content=replace(
                state.content,
                term_postings=state.content.term_postings[::-1],
            ),
        )
    elif mutation == "posting":
        term = state.content.term_postings[0]
        posting = replace(term.postings[0], normalized_term="changed")
        changed = replace(
            state,
            content=replace(
                state.content,
                term_postings=(
                    replace(term, postings=(posting,)),
                    *state.content.term_postings[1:],
                ),
            ),
        )
    elif mutation == "df":
        stats = state.content.corpus_statistics
        df = replace(stats.document_frequencies[0], document_frequency=999)
        changed = replace(
            state,
            content=replace(
                state.content,
                corpus_statistics=replace(
                    stats,
                    document_frequencies=(df, *stats.document_frequencies[1:]),
                ),
            ),
        )
    else:
        filename_stats = state.filename.document_statistics[0]
        if mutation == "length":
            item = replace(filename_stats, document_length=999)
        elif mutation == "tf":
            tf = filename_stats.term_frequencies[0]
            item = replace(
                filename_stats,
                term_frequencies=(replace(tf, observations=()),),
            )
        else:
            analysis = filename_stats.analysis
            obs = replace(analysis.observations[0], normalized_term="changed")
            item = replace(
                filename_stats,
                analysis=replace(analysis, observations=(obs,)),
            )
        # Preserve reference identity consistently while mutating the local value.
        index = state.filename
        postings = tuple(
            replace(
                t,
                postings=tuple(
                    replace(p, document_statistics=item)
                    if p.document_statistics is filename_stats
                    else p
                    for p in t.postings
                ),
            )
            for t in index.term_postings
        )
        changed = replace(
            state,
            filename=replace(
                index,
                document_statistics=(item, *index.document_statistics[1:]),
                term_postings=postings,
            ),
        )
    assert metadata.fingerprint(changed) != baseline


def test_record_encoding_unambiguous_incremental() -> None:
    """Length and scalar type disambiguate values; multiple updates are streamed."""
    a, b, c = metadata.Records(), metadata.Records(), metadata.Records()
    a.record("test", "ab", "c")
    b.record("test", "a", "bc")
    c.record("test", 1, "1")
    assert len({a.digest.hexdigest(), b.digest.hexdigest(), c.digest.hexdigest()}) == 3
    with pytest.raises(TypeError):
        a.record("invalid", object())  # type: ignore[arg-type]


@pytest.mark.parametrize(
    "name",
    ["content_identity", "resource_address", "document_identity"],
)
def test_resource_content_and_document_identity_mutations(name: str) -> None:
    """Exact semantic identities are part of the seal, independent of text/tf."""
    state = fixture(("alpha.txt", "alpha"))
    document = state.collection.documents[0]
    if name == "content_identity":
        resource = replace(
            document.resource,
            content_identity=type(document.resource.content_identity)("b" * 64),
        )
        changed_document = replace(document, resource=resource)
    elif name == "resource_address":
        resource = replace(
            document.resource,
            address=type(document.resource.address)("altered.txt"),
        )
        changed_document = replace(document, resource=resource)
    else:
        changed_document = replace(document, id=type(document.id)("b" * 64))
    changed = replace(
        state,
        collection=replace(state.collection, documents=(changed_document,)),
    )
    assert metadata.fingerprint(changed) != metadata.fingerprint(state)


def test_stable_imported_records_and_separate_durable_replay(tmp_path: Path) -> None:
    """New returns identify the stable records module; no main aliases exist."""
    state = fixture(("alpha.txt", "alpha"))
    values = (
        PreparedFrame(state.collection, state.snapshot),
        PreparedFields(
            state.content.corpus_statistics.collection_analysis,
            state.filename,
        ),
    )
    for value in values:
        assert type(value).__module__.endswith("stage_b.records")
        assert b"__main__" not in pickle.dumps(value)
        assert pickle.loads(pickle.dumps(value)) == value  # noqa: S301
    journal = Journal.start(tmp_path / "new", {"execution": "synthetic-stable-types"})
    journal.call("frame", {}, lambda: values[0])
    journal.call("fields", {}, lambda: values[1])
    journal.complete()
    replay = Journal.load(tmp_path / "new")
    assert replay.state["values"] == {"frame": values[0], "fields": values[1]}


def test_module_launcher_and_independent_audit_process(tmp_path: Path) -> None:
    """Actual -m writer and separate reader need no __main__ compatibility aliases."""
    for mode in ("write", "read"):
        command = (
            Command(sys.executable)
            .args(
                "-B",
                "-m",
                "experiments.codex_dogfood.case_0015.stage_b.probe",
                mode,
                str(tmp_path / "launcher"),
            )
            .cwd(resolve_path(Path.cwd()))
        )
        result = asyncio.run(CommandExecutor().execute(command))
        assert not result.failed, result.stderr
        assert b"SYNTHETIC STABLE RECORD PASS" in result.stdout
