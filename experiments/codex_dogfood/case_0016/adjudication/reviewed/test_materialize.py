"""Mechanical projection checks, with no semantic reviewer or treatment call."""

from __future__ import annotations

# ruff: noqa: INP001, CPY001, D103, S101, PLR2004, COM812, ANN401
import copy
from typing import TYPE_CHECKING, Any

import pytest

from experiments.codex_dogfood.case_0016.adjudication.reviewed import materialize as m

if TYPE_CHECKING:
    from pathlib import Path


@pytest.fixture(scope="module")
def gold() -> Any:
    return m.construct_gold()


@pytest.mark.parametrize(
    "field",
    [
        "cells",
        "primary",
        "minimal_witnesses",
        "obligation_indispensability",
        "task_sufficiency",
        "resource_frame",
        "exact_task",
    ],
)
def test_projection_tamper(gold: Any, field: str) -> None:
    changed = copy.deepcopy(gold)
    changed["primary"][field] = None
    with pytest.raises((ValueError, TypeError, KeyError)):
        m.validate(changed)


def test_semantics_and_algebra(gold: Any) -> None:
    stats = m.validate(gold)
    assert stats["total_labels"] == {
        "REQUIRED": 36,
        "HELPFUL_ONLY": 49,
        "UNNECESSARY": 2999,
    }
    assert stats["evidence_class_counts"] == {
        "TASK_BACKED": 21,
        "REPOSITORY_SUPPORTED": 27,
        "TASK_AND_REPOSITORY_SUPPORTED": 0,
    }
    assert stats["total_witnesses"] == 22
    assert stats["complete_task_combination_count"] == 864
    assert stats["sufficient_resource_union_count"] == 90
    assert stats["inclusion_minimal_resource_union_count"] == 12
    assert stats["resource_count_range"] == [12, 17]
    assert len(stats["task_indispensable_resources"]) == 9
    assert len(stats["task_indispensable_units"]) == 48
    assert m.verify()["status"] == "PASS"


def test_adversarial_primary_replay() -> None:
    review, packet, module = m.authenticate()
    checks = module.adversarial(review, packet)
    assert len(checks) == 22
    assert all(c["result"] == "REJECTED" for c in checks)


def test_overwrite_and_output_tamper(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    for name, raw in m.outputs().items():
        (tmp_path / name).write_bytes(raw)
    with pytest.raises(FileExistsError):
        m.write_new({tmp_path / "new": b"new", tmp_path / "reviewed_gold.json": b"bad"})
    assert not (tmp_path / "new").exists()
    (tmp_path / "reviewed_gold.json").write_bytes(b"{}")
    monkeypatch.setattr(m, "ROOT", tmp_path)
    with pytest.raises(ValueError, match="reconstruction"):
        m.verify()


def test_physical_primary_tamper(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    primary = tmp_path / "primary"
    primary.mkdir()
    for name in m.HASHES:
        (primary / name).write_bytes((m.ADJ / "primary" / name).read_bytes())
    with (primary / "stage_c_review.json").open("ab") as stream:
        stream.write(b"\n")
    monkeypatch.setattr(m, "ADJ", tmp_path)
    with pytest.raises(ValueError, match="Sealed primary"):
        m.authenticate()
