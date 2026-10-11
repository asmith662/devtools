"""Reject changes to sealed semantics and deterministic publication artifacts."""

from __future__ import annotations

# ruff: noqa: INP001, CPY001, D103, S101, PLR2004, COM812, ANN401, C901, PLR0912
import copy
from typing import TYPE_CHECKING, Any

import pytest

from experiments.codex_dogfood.case_0014.adjudication.reviewed import materialize as m

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
        "evidence_class",
        "support_alternative",
        "witness",
        "witness_minimality",
        "combination",
        "union",
        "minimal_union",
        "indispensability",
        "obligation_intersection",
        "gap",
        "limitation",
        "ambiguity",
        "frame",
        "scientific_hash",
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
        r["cells"].append(copy.deepcopy(r["cells"][0]))
    elif mutation == "label":
        r["cells"][0]["label"] = "REQUIRED"
    elif mutation == "span":
        next(c for c in r["cells"] if c["support_spans"])["support_spans"][0][
            "end"
        ] += 1
    elif mutation == "unit":
        r["semantic_units"][0]["statement"] = "changed"
    elif mutation == "evidence_class":
        r["semantic_units"][0]["evidence_class"] = "REPOSITORY_SUPPORTED"
    elif mutation == "support_alternative":
        next(u for u in r["semantic_units"] if u["support_alternatives"])[
            "support_alternatives"
        ][0]["resources"].append("unknown")
    elif mutation == "witness":
        r["obligation_semantics"][0]["witnesses"][0]["resources"].pop()
    elif mutation == "witness_minimality":
        r["obligation_semantics"][0]["witnesses"][0]["resources"].append(
            r["resource_frame"][0]["document_identity"]
        )
    elif mutation == "combination":
        r["task_sufficiency"]["combinations"][0]["witnesses"][0] = "O1/W999"
    elif mutation == "union":
        r["task_sufficiency"]["sufficient_resource_unions"][0]["resources"].pop()
    elif mutation == "minimal_union":
        r["task_sufficiency"]["inclusion_minimal_resource_unions"].pop()
    elif mutation == "indispensability":
        r["task_sufficiency"]["indispensable_resources"].pop()
    elif mutation == "obligation_intersection":
        r["obligation_semantics"][0]["indispensable_resources"].append("unknown")
    elif mutation == "gap":
        r["gaps"]["TASK_GAP"]["status"] = "PRESENT"
    elif mutation == "limitation":
        r["limitations"][0]["statement"] = "changed"
    elif mutation == "ambiguity":
        r["ambiguities"][0]["statement"] = "changed"
    elif mutation == "scientific_hash":
        value["provenance"]["primary_sha256"]["stage_c_review.json"] = "0" * 64
    else:
        value["frame"]["snapshot_id"] = "stale"
    with pytest.raises(ValueError, match=r".+"):
        m.validate(value)


def test_replay_and_counts(gold: Any) -> None:
    assert m.verify()["status"] == "PASS"
    stats = m.validate(gold)
    assert stats["label_counts_total"] == {
        "REQUIRED": 34,
        "HELPFUL_ONLY": 47,
        "UNNECESSARY": 3009,
    }
    assert (stats["resources"], stats["obligations"], stats["cells"]) == (515, 6, 3090)
    assert stats["semantic_unit_count"] == 30
    assert stats["evidence_class_counts"] == {
        "TASK_BACKED": 19,
        "REPOSITORY_SUPPORTED": 11,
        "TASK_AND_REPOSITORY_SUPPORTED": 0,
    }
    assert stats["witness_counts"] == {
        "O1": 3,
        "O2": 5,
        "O3": 5,
        "O4": 14,
        "O5": 6,
        "O6": 3,
    }
    assert stats["task_combination_count"] == 18900
    assert stats["sufficient_resource_union_count"] == 2850
    assert stats["inclusion_minimal_resource_union_count"] == 126
    assert stats["resource_count_range"] == [4, 10]
    assert stats["sufficient_unit_union_count"] == 1
    assert stats["unit_count_range"] == [30, 30]
    assert stats["required_resource_count"] == 18
    assert len(stats["task_indispensable_resources"]) == 1
    assert len(stats["task_indispensable_units"]) == 30


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
