"""Focused identity, alternative, arithmetic and immutable-publication tests."""

from __future__ import annotations

# ruff: noqa: INP001, CPY001, ANN401, D103, COM812, S101, PLR2004
import copy
from typing import TYPE_CHECKING, Any

import pytest

from experiments.codex_dogfood.case_0016.adjudication.reviewed import materialize as m
from experiments.codex_dogfood.case_0016.stage_d import (
    analysis,
    metrics,
    reporting,
    validation,
)
from experiments.codex_dogfood.case_0016.stage_d import (
    authentication as a,
)

if TYPE_CHECKING:
    from pathlib import Path


@pytest.fixture(scope="module")
def data() -> Any:
    return a.read_inputs(
        {"stage_a": a.surface("execution_started.json")["authentication"]}
    )


@pytest.fixture(scope="module")
def result(data: Any) -> Any:
    return reporting.enrich(data, metrics.analyze(data))


def test_independent_support_and_flow_checks(data: Any, result: Any) -> None:
    assert validation.validate(data, result)["status"] == "PASS"
    assert len(result["exact_rank_bindings"]) == sum(
        len(data["arms"][arm][q]["matches"] if arm == "A" else data["arms"][arm][q])
        for arm in "ABC"
        for q in data["arms"][arm]
    )
    for r in result["required_cells"]:
        f = r["flow"]
        assert (
            abs(
                f["incoming_self_flow"]
                + f["incoming_cross_resource_flow"]
                - f["incoming_structural_flow"]
            )
            < 2e-10
        )
        if r["graph_contributed_gain"]:
            assert f["native_reference_identities"]
            assert r["graph_ablation"]["gain_disappears"]


@pytest.mark.parametrize(
    "field",
    ["rank", "flow", "witness", "selected", "burden", "alternative", "gate", "novel"],
)
def test_metric_tamper(data: Any, result: Any, field: str) -> None:
    changed = copy.deepcopy(result)
    if field == "rank":
        changed["required_cells"][0]["ranks"]["A"] = 999
    elif field == "flow":
        changed["required_cells"][0]["flow"]["incoming_cross_resource_flow"] += 1
    elif field == "witness":
        changed["witnesses"][0]["arms"]["A"]["member_ranks"] = {}
    elif field == "selected":
        changed["selected_witnesses"]["O1"]["arms"]["C"]["id"] = "O1.W999"
    elif field == "burden":
        changed["burdens"]["C"]["distinct_utf8_bytes"] += 1
    elif field == "alternative":
        changed["unit_reach"][0]["arms"]["C"]["complete_alternatives"].append("invalid")
    elif field == "gate":
        changed["gate_inputs"]["required_ranks"] = ((None, 1),)
    else:
        changed["graph_novel"]["O2"]["resources"][0]["address"] = "AGENTS.md"
    with pytest.raises(ValueError, match=r".+"):
        validation.validate(data, changed)


def test_owning_query_and_identity_tamper(data: Any) -> None:
    changed = copy.deepcopy(data)
    changed["arms"]["A"]["Q1"]["matches"][0]["content_identity"] = "stale"
    with pytest.raises(ValueError, match="identity"):
        metrics.analyze(changed)
    changed = copy.deepcopy(data)
    changed["design"]["requirement_matrix"][0]["obligation"] = "O2"
    with pytest.raises(ValueError, match="owner"):
        metrics.analyze(changed)


def test_empty_incomplete_and_tie_semantics() -> None:
    empty = {"id": "O1.W001", "obligation": "O1", "resources": []}
    view = metrics.witness(empty, {}, [], {}, {}, [])
    assert view["complete"]
    assert view["depth"] == 0
    assert view["prefix"]["occurrences"] == 0
    one = {"id": "O1.W002", "obligation": "O1", "resources": [0]}
    missing = metrics.witness(one, {}, [], {}, {}, ["r"])
    assert not missing["complete"]
    assert missing["depth"] is None
    assert missing["prefix"] is None
    assert metrics.select([missing])["id"] is None
    assert metrics.select([missing, view]) == view
    tie = {**view, "id": "O1.W000"}
    assert metrics.select([view, tie]) == tie


def test_publication_determinism_overwrite_and_tamper(
    data: Any, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    files = analysis.expected(data)
    assert files == analysis.expected(data)
    m.write_new({tmp_path / n: b for n, b in files.items()})
    with pytest.raises(FileExistsError):
        m.write_new({tmp_path / "new": b"new", tmp_path / "analysis.json": b"bad"})
    assert not (tmp_path / "new").exists()
    # Keep the implementation source directory stable during reconstruction.
    original = analysis.PACKAGE
    monkeypatch.setattr(analysis, "PACKAGE", tmp_path)
    monkeypatch.setattr(analysis, "expected", lambda _: files)
    assert analysis.verify(data)["status"] == "PASS"
    (tmp_path / "analysis.json").write_bytes(b"{}")
    with pytest.raises(ValueError, match="deterministic replay"):
        analysis.verify(data)
    assert original != tmp_path
