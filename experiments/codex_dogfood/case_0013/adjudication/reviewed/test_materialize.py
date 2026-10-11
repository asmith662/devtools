"""Reject semantic changes, frame changes, tampering and overwrites."""

from __future__ import annotations

# ruff: noqa: INP001, CPY001, D103, S101, PLR2004, COM812, ANN401, C901, PLR0912 -- explicit independent mutations
import copy
from typing import TYPE_CHECKING, Any

import pytest

from experiments.codex_dogfood.case_0013.adjudication.reviewed import materialize as m

if TYPE_CHECKING:
    from pathlib import Path


@pytest.fixture(scope="module")
def gold() -> Any:
    return m.construct_gold()


@pytest.mark.parametrize(
    "mutation",
    [
        "cell",
        "missing",
        "duplicate",
        "label",
        "span",
        "unit",
        "witness",
        "combination",
        "union",
        "indispensability",
        "obligation_intersection",
        "gap",
        "limitation",
        "ambiguity",
        "frame",
    ],
)
def test_reject_mutation(gold: Any, mutation: str) -> None:
    value = copy.deepcopy(gold)
    r = value["primary"]
    if mutation == "cell":
        r["cells"][0]["identity"] = "changed"
    elif mutation == "missing":
        r["cells"].pop()
    elif mutation == "duplicate":
        r["cells"][1] = copy.deepcopy(r["cells"][0])
    elif mutation == "label":
        r["cells"][0]["label"] = "REQUIRED"
    elif mutation == "span":
        next(c for c in r["cells"] if c["support_evidence"])["support_evidence"][0][
            "end"
        ] += 1
    elif mutation == "unit":
        r["semantic_units"][0]["statement"] = "changed"
    elif mutation == "witness":
        r["obligations"][0]["witnesses"][0]["resources"].pop()
    elif mutation == "combination":
        r["task_sufficiency"]["complete_combinations"].pop()
    elif mutation == "union":
        r["task_sufficiency"]["sufficient_resource_unions"][0].append("R999")
    elif mutation == "indispensability":
        r["task_sufficiency"]["indispensable_resources"].pop()
    elif mutation == "obligation_intersection":
        r["obligations"][0]["indispensable_resources"].pop()
    elif mutation == "gap":
        r["gaps"][0]["rationale"] = "changed"
    elif mutation == "limitation":
        r["limitations"][0]["statement"] = "changed"
    elif mutation == "ambiguity":
        r["unresolved_ambiguity"][0]["status"] = "changed"
    else:
        value["frame"]["snapshot_id"] = "stale"
    with pytest.raises(ValueError, match=r".+"):
        m.validate(value)


def test_replay_and_source_counts(gold: Any) -> None:
    assert m.verify()["status"] == "PASS"
    stats = m.validate(gold)
    assert stats["labels"] == {"REQUIRED": 45, "HELPFUL_ONLY": 126, "UNNECESSARY": 4608}
    assert stats["resource_count"] == 531
    assert stats["obligation_count"] == 9
    assert stats["cell_count"] == 4779
    assert stats["unresolved_cell_count"] == 0
    assert stats["semantic_unit_count"] == 49
    assert stats["evidence_classes"] == {
        "TASK_BACKED": 32,
        "REPOSITORY_SUPPORTED": 17,
        "TASK_AND_REPOSITORY_SUPPORTED": 0,
    }
    assert sum(stats["witness_counts"].values()) == 48
    assert stats["complete_task_combination_count"] == 38400
    assert stats["distinct_sufficient_resource_union_count"] == 280
    assert (stats["minimum_resource_count"], stats["maximum_resource_count"]) == (9, 14)
    assert stats["distinct_sufficient_unit_union_count"] == 1
    assert (stats["minimum_unit_count"], stats["maximum_unit_count"]) == (49, 49)
    assert stats["globally_minimal_resource_union_count"] == 32
    assert len(stats["indispensable_resources"]) == 6
    assert stats["required_resource_count"] == 18
    assert stats["limitation_count"] == 7
    assert stats["bounded_ambiguity_count"] == 2
    assert not any(stats["gap_counts"].values())


def test_overwrite_and_hash_rejection(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    files = m.outputs()
    for name, raw in files.items():
        (tmp_path / name).write_bytes(raw)
    with pytest.raises(FileExistsError):
        m.write_new({tmp_path / "new": b"new", tmp_path / "reviewed_gold.json": b"bad"})
    assert not (tmp_path / "new").exists()
    (tmp_path / "reviewed_hashes.json").write_bytes(b"{}")
    monkeypatch.setattr(m, "ROOT", tmp_path)
    with pytest.raises(ValueError, match="reconstruction"):
        m.verify()
