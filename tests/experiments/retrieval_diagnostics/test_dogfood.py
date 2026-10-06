# Copyright (c) 2026
# ruff: noqa: COM812, PLR2004 -- frozen scientific record assertions
"""Replay the complete 37-cell dogfood from frozen captures, never rerank."""

from __future__ import annotations

import gzip
import json
from typing import TYPE_CHECKING, Any

import pytest

from experiments.codex_dogfood.case_0009.artifacts import binary, read_json
from experiments.retrieval_diagnostics import dogfood
from experiments.retrieval_diagnostics.serialization import encode

if TYPE_CHECKING:
    from pathlib import Path


@pytest.fixture(scope="module")
def diagnostic() -> dict[str, Any]:
    """Perform one complete validated replay for this focused module."""
    return dogfood.build()


def test_case_required_partition_scores_and_stable_artifacts(
    diagnostic: dict[str, Any],
) -> None:
    """All cells reproduce existing R1 observations and deterministic JSON/Markdown."""
    assert len(diagnostic["cells"]) == 37
    for arm, burden in (("A", 8), ("B", 7)):
        assert diagnostic["summaries"][arm]["statuses"] == {"REACHED": 37}
        assert diagnostic["summaries"][arm]["score_reconstructions"] == 37
        assert (
            diagnostic["summaries"][arm]["primary_failures"][
                "RANKING_DISCRIMINATION_FAILURE"
            ]
            == burden
        )
    assert diagnostic["paired_positive_reach_rescues"] == 0
    assert diagnostic["paired_partial_hidden_match_cells"] == 12
    assert gzip.decompress(binary(dogfood.HERE / "case_0009.json.gz")) == encode(
        diagnostic
    )
    assert binary(dogfood.HERE / "case_0009.md") == dogfood.report(diagnostic).encode()


def test_requested_case_mechanics_are_exact(diagnostic: dict[str, Any]) -> None:
    """Known gains/regressions and identifier/filename sources remain inspectable."""
    cells = diagnostic["cells"]
    package = next(c for c in cells if c["resource"] == "pyproject.toml")
    assert (package["A"]["rank"], package["B"]["rank"]) == (178, 99)
    frame = next(
        c
        for c in cells
        if c["obligation"] == "frame" and c["resource"].endswith("/resource.py")
    )
    assert (frame["A"]["rank"], frame["B"]["rank"]) == (185, 231)
    assert frame["pair"]["new_overtaker_labels"]["UNNECESSARY"] == 51
    promotion = next(
        c
        for c in cells
        if c["obligation"] == "readiness" and c["resource"].endswith("/promotion.py")
    )
    terms = promotion["B"]["terms"]
    for term, identifier in (
        ("localization", "LocalizationAssessment"),
        ("assessment", "LocalizationAssessment"),
        ("supported", "supported_witnesses"),
        ("witnesses", "supported_witnesses"),
    ):
        t = next(t for t in terms if t["field"] == "content" and t["term"] == term)
        assert t["weighted_contribution"] > 0
        lineage = (
            t["query_source"] if identifier == "LocalizationAssessment" else t["source"]
        )
        assert lineage["whole_form_counts"][identifier] > 0
    tests = next(
        c
        for c in cells
        if c["obligation"] == "tests" and c["resource"].endswith("/test_resolution.py")
    )
    resolution = next(
        t
        for t in tests["B"]["terms"]
        if t["field"] == "filename" and t["term"] == "resolution"
    )
    assert resolution["source"]["examples"][0]["observed"] == "test_resolution"
    assert resolution["weighted_contribution"] == resolution["contribution"] * 0.25


def test_cli_replay_and_version_refusal(
    diagnostic: dict[str, Any], tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """CLI writes deterministic records and refuses a different sealed capture."""
    monkeypatch.setattr(dogfood, "HERE", tmp_path)
    monkeypatch.setattr(dogfood, "build", lambda: diagnostic)
    monkeypatch.setattr("sys.argv", ["dogfood", "build"])
    dogfood.main()
    dogfood.main()
    monkeypatch.setattr("sys.argv", ["dogfood", "verify"])
    dogfood.main()
    path = tmp_path / "case_0009.json.gz"
    path.write_bytes(gzip.compress(json.dumps({}).encode(), mtime=0))
    with pytest.raises(ValueError, match="replay differs"):
        dogfood.main()
    monkeypatch.setattr("sys.argv", ["dogfood", "build"])
    with pytest.raises(ValueError, match="new version"):
        dogfood.main()


def test_dogfood_rejects_frozen_capture_hash_mismatch(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """A tampered capture cannot become a replayable mechanical explanation."""
    original = read_json

    def broken(path: Path) -> dict[str, Any]:
        value = original(path)
        if path.name == "stage_b_integrity.json":
            value["sha256"]["results.json.gz"] = "0" * 64
        return value

    monkeypatch.setattr(dogfood, "read_json", broken)
    with pytest.raises(ValueError, match="hash mismatch"):
        dogfood.build()
