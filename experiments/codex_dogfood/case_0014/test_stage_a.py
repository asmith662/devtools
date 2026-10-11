# Copyright (c) 2026
# ruff: noqa: S101, PLR2004, COM812 -- scientific fixture assertions
"""Replay Stage A, leakage, overwrite and no-execution contracts."""

from __future__ import annotations

import asyncio
import json
from contextlib import ExitStack
from typing import TYPE_CHECKING
from unittest.mock import patch

import pytest

from experiments.codex_dogfood.case_0009.artifacts import json_bytes, put_text
from experiments.codex_dogfood.case_0014 import blind, freeze, protocol

if TYPE_CHECKING:
    from pathlib import Path


def test_every_task_query_term_and_arm_binding() -> None:
    """Query-only analysis and classification are deterministic, not retrieval."""
    design = protocol.authored()
    assert design == protocol.authored()
    assert len(design["queries"]) == len(design["requirement_matrix"]) == 6
    for p in protocol.policies(design["task_text"]):
        p.validate()
        assert (
            tuple(t.analyzed_term for t in p.terms) == p.native_query.normalized_terms
        )
        assert all(w > 0 for t in p.terms for w in t.multipliers)
    assert design["no_execution"] == protocol.COUNTS


def test_prospective_operations_cannot_run_during_replay() -> None:
    """Fail immediately if Stage A invokes native indexing/retrieval or weighting."""
    targets = (
        "devtools.context.retrieval.lexical.index.build_repository_text_lexical_inverted_index",
        "devtools.context.retrieval.lexical.filename.build_repository_text_filename_lexical_index",
        "devtools.context.retrieval.lexical.bm25.retrieve_repository_text_documents_by_bm25",
        "devtools.context.retrieval.lexical.bm25.retrieve_repository_text_documents_by_content_bm25",
        "devtools.context.retrieval.lexical.statistics.calculate_repository_text_lexical_corpus_statistics",
        "experiments.query_term_weighting.scoring.score",
    )
    with ExitStack() as stack:
        for target in targets:
            stack.enter_context(
                patch(
                    target,
                    side_effect=AssertionError("Prospective execution forbidden"),
                )
            )
        asyncio.run(freeze.verify(protocol.CASE))


def test_blind_projection_leakage_guard() -> None:
    """Only task/obligation/resource content survives the future packet projection."""
    r = dict.fromkeys(
        (
            "repository_id",
            "snapshot_id",
            "corpus_id",
            "document_identity",
            "address",
            "content_identity",
            "encoding",
            "utf8_bytes",
            "content",
        ),
        "synthetic",
    )
    r["score"] = "SECRET"
    packet = blind.packet(protocol.authored(), [r])
    assert packet == blind.packet(json.loads(json.dumps(protocol.authored())), [r])
    assert list(packet) == protocol.GOLD_POLICY["allowed"]
    assert "SECRET" not in json.dumps(packet)
    assert all(
        "query" not in row and "terms" not in row for row in packet["obligations"]
    )
    changed = protocol.authored()
    changed["queries"] = []
    with pytest.raises(ValueError, match="exact frozen"):
        blind.packet(changed, [r])
    with pytest.raises(ValueError, match="Duplicate"):
        blind.packet(protocol.authored(), [r, r])


def test_overwrite_and_tamper_rejection(tmp_path: Path) -> None:
    """Use synthetic serialized Stage A bytes; never score the prospective case."""
    values = {name: json_bytes({"name": name}) for name in freeze.GENERATED}

    async def expected() -> dict[str, bytes]:
        return values

    with patch.object(freeze, "expected", expected):
        asyncio.run(freeze.publish(tmp_path))
        asyncio.run(freeze.verify(tmp_path))
        with pytest.raises(FileExistsError):
            asyncio.run(freeze.publish(tmp_path))
        (tmp_path / "trace.json").write_bytes(b"tamper")
        with pytest.raises(ValueError, match="tamper"):
            asyncio.run(freeze.verify(tmp_path))
    other = tmp_path / "other"
    put_text(other / "execution_started.json", "{}")
    with pytest.raises(ValueError, match="forbidden"):
        freeze.no_execution(other)


def test_eligibility_held_out_and_prior_case_guard() -> None:
    """Excluded paths are rejected before contents can be acquired."""
    assert freeze.eligible("src/devtools/resources/commands/models/result.py")
    for path in (
        "tests/confirmation/test.py",
        "docs/reserve/a.md",
        "tests/experiments/test.py",
        ".local/codex-result.md",
        "experiments/case_0013/analysis.json",
    ):
        assert not freeze.eligible(path)
    assert freeze.PRIOR_CASE.search(b"Case 0013 SELECTIVE_MECHANISM_ROUTING_SUPPORTED")
