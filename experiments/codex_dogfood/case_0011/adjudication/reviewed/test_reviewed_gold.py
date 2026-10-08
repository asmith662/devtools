"""Independent frame, inheritance and witness checks for frozen reviewed gold."""

# ruff: noqa: INP001, CPY001, COM812, D103, S101, PLR2004
from __future__ import annotations

import copy
import itertools
from collections import Counter
from typing import TYPE_CHECKING, Any

import pytest

from experiments.codex_dogfood.case_0011.adjudication.reviewed import (
    build_reviewed_gold as b,
)

if TYPE_CHECKING:
    from pathlib import Path


@pytest.fixture
def gold() -> dict[str, Any]:
    return b.load(b.ROOT / "reviewed_gold.json")


def test_input_hash_scopes_and_inheritance_seal() -> None:
    r, packet, _, _ = b.verify_inputs()
    assert len(packet["agreed_cells"]) == 4714
    assert b.sha(b.canonical(packet["agreed_cells"])) == b.SEAL
    assert r["input_bindings"]["files"]["packet.json"] == b.PACKET_HASHES["packet.json"]


def test_full_frame_and_identity_partitions(gold: dict[str, Any]) -> None:
    expected = set(
        itertools.product(
            (o["identity"] for o in gold["frozen_obligations"]),
            (r["address"] for r in gold["resources"]),
        )
    )
    actual = [(c["obligation"], c["address"]) for c in gold["cells"]]
    assert len(actual) == len(set(actual)) == len(expected) == 4779
    assert set(actual) == expected
    assert len(gold["resources"]) == 531
    assert len(gold["frozen_obligations"]) == 9
    assert "UNRESOLVED" not in {c["label"] for c in gold["cells"]}


def test_inherited_cells_unchanged_with_one_explicit_exception(
    gold: dict[str, Any],
) -> None:
    packet = b.load(b.ADJ / "reconciliation/packet.json")
    cells = {(c["obligation"], c["address"]): c for c in gold["cells"]}
    inherited = []
    exceptions = []
    for original in packet["agreed_cells"]:
        c = cells[original["obligation"], original["address"]]
        if c["provenance"] == "INHERITED_AGREEMENT":
            assert all(c[k] == v for k, v in original.items())
            inherited.append(c)
        else:
            assert c["provenance"] == "RECONCILED_EXCEPTION"
            exceptions.append(c)
    assert len(inherited) == 4713
    assert len(exceptions) == 1
    assert exceptions[0]["label"] == "HELPFUL_ONLY"
    assert (exceptions[0]["obligation"], exceptions[0]["address"]) == (
        "validation",
        "scripts/validate_development.py",
    )


def test_disputed_cells_match_each_explicit_decision(gold: dict[str, Any]) -> None:
    r = b.load(b.ADJ / "reconciliation/reconciliation.json")
    cells = {
        c["proposition_id"]: c
        for c in gold["cells"]
        if c["provenance"] == "RECONCILED_DISPUTE"
    }
    ds = [d for d in r["decisions"] if d["kind"] == "CELL"]
    assert len(cells) == len(ds) == 65
    for d in ds:
        assert all(
            cells[d["proposition_id"]][k] == v for k, v in d["reconciled_value"].items()
        )


def test_exact_frozen_source_support_and_tamper_rejection(gold: dict[str, Any]) -> None:
    _, _, m, resources = b.verify_inputs()
    contents = {r["address"]: r for r in resources}
    contents["task.txt"] = {"content": m["task"]}
    assert b.verify_support(gold["units"], contents) > 0
    damaged = copy.deepcopy(gold["units"])
    damaged[0]["supports"][0]["excerpt"] += "tamper"
    with pytest.raises(AssertionError):
        b.verify_support(damaged, contents)


def test_units_cells_and_alternative_membership(gold: dict[str, Any]) -> None:
    units = {u["id"]: u for u in gold["units"]}
    cells = {(c["obligation"], c["address"]): c for c in gold["cells"]}
    assert len(units) == len(gold["units"]) == 32
    referenced = set()
    for o in gold["obligations"]:
        for a in o["alternatives"]:
            assert a["member_logic"] == "ALL_COMPLEMENTARY"
            assert set(a["units"]) == set(a["evidence_bindings"])
            referenced.update(a["units"])
            for uid, supports in a["evidence_bindings"].items():
                assert a["id"] in units[uid]["alternative_membership"]
                for s in supports:
                    c = cells[o["obligation"], s["address"]]
                    assert c["label"] == "REQUIRED"
                    assert uid in c["reviewed_units"]
    assert referenced == set(units)
    assert all(u["provenance"] for u in units.values())


def test_independent_exact_cartesian_product(gold: dict[str, Any]) -> None:
    stats = b.load(b.ROOT / "reviewed_statistics.json")
    choices = [o["alternatives"] for o in gold["obligations"]]
    combos = list(itertools.product(*choices))
    resources = [{r for a in c for r in a["resources"]} for c in combos]
    units = [{u for a in c for u in a["units"]} for c in combos]
    assert len(combos) == stats["combination_count"] == 6
    assert {tuple(sorted(r)) for r in resources} == {
        tuple(r) for r in stats["sufficient_resource_unions"]
    }
    assert len({tuple(sorted(r)) for r in resources}) == 2
    assert min(map(len, resources)) == 15
    assert max(map(len, resources)) == 16
    assert sorted(set.intersection(*resources)) == stats["task_indispensable_resources"]
    assert len(set.intersection(*resources)) == 15
    assert sorted(set.intersection(*units)) == stats["task_indispensable_units"]
    assert len(set.intersection(*units)) == 30
    for o, ind in zip(
        gold["obligations"], stats["obligation_indispensability"], strict=True
    ):
        assert ind["resources"] == sorted(
            set.intersection(*(set(a["resources"]) for a in o["alternatives"]))
        )
        assert ind["units"] == sorted(
            set.intersection(*(set(a["units"]) for a in o["alternatives"]))
        )


def test_required_union_not_simultaneous_necessity(gold: dict[str, Any]) -> None:
    required = {c["address"] for c in gold["cells"] if c["label"] == "REQUIRED"}
    assert len(required) == 16
    assert "not simultaneously necessary" in gold["required_semantics"]
    st = b.structure(gold["obligations"])
    assert any(set(u) != required for u in st["sufficient_resource_unions"])


def test_decisions_task_gap_and_six_limitations(gold: dict[str, Any]) -> None:
    r = b.load(b.ADJ / "reconciliation/reconciliation.json")
    assert Counter(d["decision"] for d in r["decisions"]) == {
        "ACCEPT_POSITION_1": 35,
        "ACCEPT_POSITION_2": 33,
        "REPLACE_WITH_RECONCILED_JUDGMENT": 72,
    }
    assert gold["task_gap"]["task_gaps"] == "NONE"
    assert not gold["task_gap"]["supplemental_task_semantic_units"]
    assert len(gold["interpretation_limitations"]) == 6
    assert all(
        x["constrains_implementation"]
        and x["blocks_no_judgment"]
        and x["requires_no_inherent_discovery"]
        for x in gold["interpretation_limitations"]
    )
    assert gold["handoff_safeguard"] == b.HANDOFF
    assert not any(".local/codex-result.md" in u["statement"] for u in gold["units"])
    assert ".local/codex-result.md" not in {r["address"] for r in gold["resources"]}


def test_deterministic_replay() -> None:
    first, second = b.artifacts(), b.artifacts()
    assert first == second
    assert all(p.read_bytes() == raw for p, raw in first.items())


def test_overwrite_refusal_preserves_all_bytes(tmp_path: Path) -> None:
    one, two = tmp_path / "one", tmp_path / "two"
    one.write_bytes(b"existing")
    with pytest.raises(FileExistsError):
        b.write_new({two: b"new", one: b"replacement"})
    assert one.read_bytes() == b"existing"
    assert not two.exists()
