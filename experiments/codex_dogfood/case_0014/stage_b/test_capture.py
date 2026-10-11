# Copyright (c) 2026
# ruff: noqa: S101, EM101, TRY003 -- controlled synthetic failure boundaries
"""Synthetic journal/attribution tests; no prospective execution or gold oracle."""

from __future__ import annotations

from typing import TYPE_CHECKING
from unittest.mock import patch

import pytest

from experiments.codex_dogfood.case_0012.stage_b.durability import Journal, exclusive
from experiments.codex_dogfood.case_0014.stage_b import reporting
from experiments.query_term_weighting.classification import Arm
from experiments.query_term_weighting.scoring import score
from experiments.query_term_weighting.serialization import trace
from experiments.query_term_weighting.test_weighting import native, policy

if TYPE_CHECKING:
    from pathlib import Path


def test_exact_attribution_and_crossings() -> None:
    """Only permitted roles change; float summation residuals reconstruct exactly."""
    p = policy()
    n = native(p)
    a, b, c = (trace(score(n, p, arm)) for arm in Arm)
    assert reporting.attribution(a, b, c)["status"] == "PASS"
    assert set(reporting.pairwise(a, c)["top_k"]) == {"10", "20", "50"}
    c["matches"][0]["contributions"][0]["native"] += 1
    with pytest.raises(ValueError, match="changed"):
        reporting.attribution(a, b, c)


def test_append_only_claim_return_recovery(tmp_path: Path) -> None:
    """Recover exact shared identities and block every duplicate native call."""
    j = Journal.start(tmp_path, {"execution": "synthetic-only"})
    value = ["native"]
    assert j.call("once", {}, lambda: value) is value
    with pytest.raises(ValueError, match="already entered"):
        j.call("once", {}, lambda: value)
    j.complete()
    loaded = Journal.load(tmp_path)
    assert loaded.state["values"]["once"] == value
    with pytest.raises(ValueError, match="Loaded"):
        loaded.call("other", {}, lambda: value)
    with pytest.raises(FileExistsError):
        Journal.start(tmp_path, {"execution": "synthetic-only"})


def test_return_publication_failure_never_retries(tmp_path: Path) -> None:
    """A returned-but-undurable operation leaves an unrecoverable entered claim."""
    j = Journal.start(tmp_path, {"execution": "synthetic-only"})
    calls = []

    def invoke() -> int:
        calls.append(1)
        return 7

    original = j.event

    def event(sequence: int, status: str, payload: dict[str, object]) -> None:
        if status == "RETURNED":
            raise OSError("synthetic publication failure")
        original(sequence, status, payload)

    with patch.object(j, "event", event), pytest.raises(OSError, match="publication"):
        j.call("once", {}, invoke)
    assert calls == [1]
    with pytest.raises(ValueError, match="already entered"):
        j.call("once", {}, invoke)
    with pytest.raises(ValueError, match="Unrecoverable"):
        Journal.load(tmp_path).ready()


def test_native_exception_and_exclusive_tamper(tmp_path: Path) -> None:
    """Exceptions are durable failures; exclusive claims cannot be overwritten."""
    j = Journal.start(tmp_path, {"execution": "synthetic-only"})

    def fail() -> None:
        raise RuntimeError("synthetic native failure")

    with pytest.raises(RuntimeError, match="native failure"):
        j.call("once", {}, fail)
    with pytest.raises(ValueError, match="Unrecoverable"):
        Journal.load(tmp_path).ready()
    with pytest.raises(FileExistsError):
        exclusive(tmp_path / "execution.claim", {})
