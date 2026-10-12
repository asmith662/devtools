"""Mutation checks for the unchanged primary projection and support mathematics."""

from __future__ import annotations

# ruff: noqa: INP001, CPY001, D103, S101, PLR2004, COM812, ANN401, C901, PLR0912
import copy
from typing import TYPE_CHECKING, Any

import pytest

from experiments.codex_dogfood.case_0015.adjudication.reviewed import materialize as m

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
        "class",
        "alternative",
        "witness",
        "minimality",
        "combination",
        "union",
        "minimal_union",
        "indispensability",
        "obligation_intersection",
        "gap",
        "limitation",
        "ambiguity",
        "frame",
        "hash",
        "empty_witness",
        "blindness",
    ],
)
def test_reject_mutation(gold: Any, mutation: str) -> None:
    value = copy.deepcopy(gold)
    r = value["primary"]
    if mutation == "cell":
        r["cells"][0]["obligation"] = "O9"
    elif mutation == "missing":
        r["cells"].pop()
    elif mutation == "duplicate":
        r["cells"].append(copy.deepcopy(r["cells"][0]))
    elif mutation == "label":
        r["cells"][0]["label"] = "REQUIRED"
    elif mutation == "span":
        next(c for c in r["cells"] if c["support_spans"])["support_spans"][0][
            "end"
        ] += 1
    elif mutation == "unit":
        r["semantic_units"][0]["statement"] = "changed"
    elif mutation == "class":
        r["semantic_units"][0]["evidence_class"] = "GUESSED"
    elif mutation == "alternative":
        next(u for u in r["semantic_units"] if u["alternatives"])["alternatives"][0][
            "resources"
        ].append("unknown")
    elif mutation in {"witness", "minimality"}:
        r["witnesses"]["O1"][0]["resources"].append("unknown")
    elif mutation == "empty_witness":
        r["witnesses"]["O2"][0]["resources"].append(
            r["resource_frame"][0]["document_identity"]
        )
    elif mutation == "combination":
        r["task_combinations"][0]["witnesses"][0] = "O1.W999"
    elif mutation == "union":
        r["sufficient_resource_unions"][0].pop()
    elif mutation == "minimal_union":
        r["inclusion_minimal_resource_unions"].pop()
    elif mutation == "indispensability":
        r["task_indispensable_units"].pop()
    elif mutation == "obligation_intersection":
        r["obligation_indispensability"]["O1"]["resources"].append("unknown")
    elif mutation == "gap":
        r["gaps"]["TASK_GAP"].append("changed")
    elif mutation == "limitation":
        r["limitations"][0]["statement"] = "changed"
    elif mutation == "ambiguity":
        r["ambiguities"][0]["statement"] = "changed"
    elif mutation == "hash":
        value["provenance"]["primary_sha256"]["stage_c_review.json"] = "0" * 64
    elif mutation == "blindness":
        r["blindness"]["excluded_category_access"]["rankings"] = "YES"
    else:
        value["frame"]["snapshot_id"] = "stale"
    with pytest.raises(ValueError, match=r".+"):
        m.validate(value)


def test_support_algebra_and_empty_witness(gold: Any) -> None:
    source, _, module = m.authenticate()
    algebra = module.algebra(source)
    assert all(source[k] == v for k, v in algebra.items())
    stats = m.validate(gold)
    assert stats["total_label_counts"] == {
        "REQUIRED": 21,
        "HELPFUL_ONLY": 102,
        "UNNECESSARY": 2967,
    }
    assert stats["evidence_class_counts"] == {
        "TASK_BACKED": 25,
        "REPOSITORY_SUPPORTED": 17,
        "TASK_AND_REPOSITORY_SUPPORTED": 0,
    }
    assert stats["total_witness_count"] == 12
    assert len(algebra["task_combinations"]) == 32
    assert len(algebra["sufficient_resource_unions"]) == 9
    assert len(algebra["inclusion_minimal_resource_unions"]) == 4
    assert sorted({len(v) for v in algebra["sufficient_resource_unions"]}) == [
        9,
        10,
        11,
    ]
    assert len(algebra["sufficient_unit_unions"]) == 1
    assert len(algebra["sufficient_unit_unions"][0]) == 42
    assert len(algebra["task_indispensable_resources"]) == 7
    assert len(algebra["task_indispensable_units"]) == 42
    assert algebra["witnesses"]["O2"][0]["resources"] == []
    assert m.verify()["status"] == "PASS"


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
