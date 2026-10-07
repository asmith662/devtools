# Copyright (c) 2026
# ruff: noqa: PLR2004 -- frozen capture checks
"""Prospective evidence replay without rerunning arms or importing gold."""

from __future__ import annotations

from shutil import copyfile
from typing import TYPE_CHECKING, NoReturn

import pytest

from experiments.codex_dogfood.case_0009.artifacts import read_json
from experiments.codex_dogfood.case_0010 import execute, packet
from experiments.codex_dogfood.case_0010.freeze import CASE

if TYPE_CHECKING:
    from pathlib import Path


def forbidden_scoring(*_args: object, **_kwargs: object) -> NoReturn:
    """Reject a second retrieval query during captured-evidence replay."""
    message = "Treatment rerun during replay"
    raise AssertionError(message)


def test_complete_treatment_score_replay_without_scoring(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """All four arms/44 lanes pass R1.5 frame, term, score, tie and universe checks."""
    monkeypatch.setattr(execute, "retrieve", forbidden_scoring)
    assert execute.verify() == {
        "status": "R1.5 exact score/universe replay PASSED",
        "arms": 4,
        "lanes_per_arm": 11,
        "effectiveness": "UNKNOWN",
    }


def test_exclusive_execution_and_packet_overwrite_refusal() -> None:
    """No second execution or overwrite can silently replace frozen captures."""
    with pytest.raises(FileExistsError):
        execute.run()
    with pytest.raises(FileExistsError):
        packet.build()


def test_parameter_identity_cost_and_packet_replay(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """All selected configurations, explicit costs and full blind inputs persist."""
    treatment = read_json(CASE / "treatment.json")
    configs = [execute.configuration(arm) for arm in treatment["arms"]]
    assert len({c.identity for c in configs}) == 4
    assert [(c.k1, c.b, c.filename_weight) for c in configs] == [
        (1.2, 0.75, 0.25),
        (2.4, 0, 2),
        (2.4, 0.5, 1),
        (2.4, 0.75, 0.25),
    ]
    costs = read_json(CASE / "costs.json")
    assert costs["index_reused_all_arms"]
    assert costs["diagnostics_excluded_from_query_cost"]
    for arm in "ABCD":
        captured = costs["arms"][arm]
        assert len(captured["query_seconds"]) == 11
        assert captured["median_query_seconds"] > 0
        assert captured["p95_query_seconds"] >= captured["median_query_seconds"]
    # The frozen Stage B verifier requires precisely five blind inputs. Stage C
    # adds sealed outputs to the repository directory; reconstruct Stage B's
    # original boundary instead of changing its immutable producer/verifier.
    target = tmp_path / "adjudication"
    target.mkdir()
    for name in packet.BLIND_FILES:
        copyfile(CASE / "adjudication" / name, target / name)
    monkeypatch.setattr(packet, "CASE", tmp_path)
    assert packet.verify() == read_json(CASE / "adjudication/integrity.json")
