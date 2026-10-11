"""Independently check all witness accounting and reject changed evaluation bytes."""

from __future__ import annotations

# ruff: noqa: INP001, CPY001, D103, S101, ANN401, PLR2004, COM812 -- formatter owns commas
import copy
import json
from collections import Counter
from dataclasses import replace
from typing import TYPE_CHECKING, Any

import pytest

from experiments.codex_dogfood.case_0013.adjudication.reviewed import materialize
from experiments.codex_dogfood.case_0013.stage_d import analysis as m
from experiments.codex_dogfood.case_0013.stage_d import authentication as auth
from experiments.mechanism_routing.gates import GateEvidence, evaluate

if TYPE_CHECKING:
    from pathlib import Path


@pytest.fixture(scope="module")
def data() -> Any:
    return auth.authenticate()


@pytest.fixture(scope="module")
def analysis(data: Any) -> Any:
    return m.calculate(data)


def test_all_witnesses_and_selected_prefixes(data: Any, analysis: Any) -> None:
    primary = data["gold"]["primary"]
    labels = {
        (c["obligation"].split("/")[-1], c["address"]): c["label"]
        for c in primary["cells"]
    }
    addresses = {r["identity"]: r["address"] for r in primary["resources"]}
    checked = 0
    for arm in "ABC":
        chosen_prefixes = []
        chosen_labels: list[str] = []
        for ob in primary["obligations"]:
            key = ob["key"]
            rows = data["arms"][arm][key]["rows" if arm == "A" else "entries"]
            order = [r["address"] for r in rows]
            lane = analysis["arms"][arm]["lanes"][key]
            assert len(lane["all_witnesses"]) == len(ob["witnesses"])
            pairs = []
            for source, actual in zip(
                ob["witnesses"], lane["all_witnesses"], strict=True
            ):
                resource_list = [addresses[r] for r in source["resources"]]
                positions = {
                    address: next(
                        (n for n, row in enumerate(order, 1) if row == address), None
                    )
                    for address in resource_list
                }
                complete = all(position is not None for position in positions.values())
                depth = (
                    max((p for p in positions.values() if p is not None), default=0)
                    if complete
                    else None
                )
                assert actual["completion_depth"] == depth
                assert actual["member_depths"] == positions
                assert actual["units"] == source["units"]
                if depth is not None:
                    prefix = order[:depth]
                    metric = actual["metrics"]
                    assert metric["prefix_occurrences"] == depth
                    assert metric["unique_prefix_count"] == len(set(prefix))
                    assert metric["label_occurrences"] == {
                        label: sum(labels[key, address] == label for address in prefix)
                        for label in m.LABELS
                    }
                    assert metric["unique_utf8_bytes"] == sum(
                        len(data["resources"][address]["text"].encode("utf-8"))
                        for address in set(prefix)
                    )
                    pairs.append((depth, source["identity"]))
                checked += 1
            chosen = min(pairs) if pairs else None
            assert (lane["completion_depth"], lane["selected"]["identity"]) == chosen
            chosen_prefixes.extend(order[: lane["completion_depth"]])
            chosen_labels.extend(
                labels[key, address] for address in order[: lane["completion_depth"]]
            )
        burden = analysis["arms"][arm]["selected_prefix_burden"]
        assert burden["prefix_occurrences"] == len(chosen_prefixes)
        assert burden["unique_prefix_count"] == len(set(chosen_prefixes))
        assert burden["duplicate_occurrences"] == len(chosen_prefixes) - len(
            set(chosen_prefixes)
        )
        assert burden["label_occurrences"] == dict(Counter(chosen_labels))
        assert burden["unique_utf8_bytes"] == sum(
            len(data["resources"][address]["text"].encode("utf-8"))
            for address in set(chosen_prefixes)
        )
    assert checked == 144


def test_hint_classifications_and_nonresolution(data: Any, analysis: Any) -> None:
    hints = analysis["hints"]
    assert [h["hint"] for h in hints] == [f"H{n:02}" for n in range(1, 11)]
    cells = {
        (c["obligation"].split("/")[-1], c["address"]): c
        for c in data["gold"]["primary"]["cells"]
    }
    for h in hints:
        if h["resolved_resource"] is not None:
            cell = cells[h["obligation"], h["resolved_resource"]]
            assert h["reviewed_label"] == cell["label"]
            assert h["reviewed_units"] == cell["units"]
            assert h["native_rank"] - h["routed_position"] == h["depth_saved"]
            assert h["C_admission"] is True
        else:
            assert h["frozen_role"] == "INTRODUCE_NEW"
            assert h["B_admission"] is True
            assert h["B_native_disposition"] == "UNRESOLVED"
            assert h["B_native_candidates"] == []
            assert h["C_native_disposition"] == "NOT_INVOKED"
            assert h["C_policy_disposition"] == "LEXICAL_ONLY"
            assert h["C_native_invocations"] == 0
            assert h["reviewed_label"] is None
            assert h["low_value_avoided_subtype"] == "genuine native nonresolution"
            assert h["route_selection_miss"] is False
    assert [h["hint"] for h in analysis["skipped_routes"]] == [
        "H04",
        "H05",
        "H06",
        "H08",
    ]


def test_joins_reach_costs_and_frozen_gates(data: Any, analysis: Any) -> None:
    for arm in "ABC":
        reached = analysis["arms"][arm]["required_reach"]
        assert len(reached["resources"]) == 18
        assert len(reached["cells"]) == 45
        assert len(reached["units"]) == 49
    assert all(
        not v
        for rows in analysis["required_reach_losses"].values()
        for v in rows.values()
    )
    assert all(analysis["contract_checks"].values())
    assert all(analysis["soundness_checks"].values())
    assert analysis["gates"]["outcome"] == "SELECTIVE_MECHANISM_ROUTING_SUPPORTED"
    assert analysis["gates"]["preserve_b_gains_and_reduce"] is True
    assert analysis["gates"]["burden_10_percent_gain_without_cost_increase"] is False
    assert [
        (g["obligation"], g["A_depth"], g["B_depth"], g["C_depth"])
        for g in analysis["meaningful_B_gains"]
    ] == [("compatibility", 2, 1, 1), ("validation", 4, 2, 2)]
    assert analysis["failure_attribution"]["ROUTE_SELECTION_MISS"] == []
    assert analysis["search_policy_failure"] == "NOT_ASSESSED"
    assert data["journal"]["pairs"] == 73
    assert data["journal"]["native_retries"] == 0
    for arm in "BC":
        cost = analysis["costs"]["arms"][arm]
        rows = [h for h in data["summary"]["hint_rows"] if h["arm"] == arm]
        assert cost["route_ns"] == sum(h["runtime_ns"] for h in rows)
        assert cost["presentation_ns"] == sum(
            data["arms"][arm][key]["presentation_runtime_ns"]
            for key in data["arms"][arm]
        )
        assert cost["mechanism_ns"] == cost["route_ns"] + cost["presentation_ns"]
    assert analysis["gate_arithmetic"]["invocations_25_percent"] == {
        "left": 24,
        "operator": "<=",
        "right": 30,
        "passes": True,
    }
    evidence = GateEvidence(**analysis["gate_evidence"])
    assert (
        evaluate(replace(evidence, contract_valid=False))["outcome"]
        == "EXPERIMENTAL_CONTRACT_DEFECT"
    )
    for field in ("router_sound", "reach_safe", "obligation_safe"):
        assert (
            evaluate(replace(evidence, **{field: False}))["outcome"] == "ROUTER_DEFECT"
        )
    assert (
        evaluate(replace(evidence, b_meaningful_gain_count=0))["outcome"]
        == "COMPLEMENTARY_BUT_NOT_CLEARLY_BETTER"
    )
    equality = replace(
        evidence,
        b_meaningful_gain_count=0,
        invocations_c=evidence.invocations_b,
        mechanism_ns_c=evidence.mechanism_ns_b,
        positive_selective_value=False,
    )
    assert evaluate(equality)["outcome"] == "NO_MATERIAL_VALUE"
    assert (
        evaluate(replace(evidence, invocations_b=4, invocations_c=3))[
            "invocations_25_percent_reduction"
        ]
        is True
    )
    assert (
        evaluate(replace(evidence, invocations_b=4, invocations_c=4))[
            "invocations_25_percent_reduction"
        ]
        is False
    )
    assert (
        evaluate(replace(evidence, mechanism_ns_b=10, mechanism_ns_c=9))[
            "mechanism_cost_10_percent_reduction"
        ]
        is True
    )
    assert (
        evaluate(replace(evidence, mechanism_ns_b=10, mechanism_ns_c=10))[
            "mechanism_cost_10_percent_reduction"
        ]
        is False
    )


@pytest.mark.parametrize(
    "field",
    [
        "joins",
        "hints",
        "arms",
        "required_reach_losses",
        "costs",
        "gate_evidence",
        "gates",
        "gate_arithmetic",
        "meaningful_B_gains",
        "families",
        "preservation",
        "precedence_application",
        "failure_attribution",
    ],
)
def test_calculation_tamper_rejection(field: str, data: Any, analysis: Any) -> None:
    changed = copy.deepcopy(analysis)
    changed[field] = "tampered"
    with pytest.raises(ValueError, match="deterministic calculation identity"):
        m.validate(changed, data)


def test_stale_content_join(data: Any) -> None:
    changed = dict(data)
    changed["arms"] = copy.deepcopy(data["arms"])
    changed["arms"]["C"]["integrity"]["entries"][0]["content_identity"] = "stale"
    with pytest.raises(ValueError, match="content join"):
        m.calculate(changed)


def test_missing_and_empty_witness() -> None:
    witness = {"identity": "fixture:W1", "resources": ["r"], "units": ["u"]}
    assert m.completion(witness, [], {"r": "resource"})["completion_depth"] is None
    witness["resources"] = []
    assert m.completion(witness, [], {})["completion_depth"] == 0


def test_exact_replay(data: Any) -> None:
    assert m.verify(data)["status"] == "PASS"
    assert m.outputs(data) == m.outputs(data)


@pytest.mark.parametrize(
    "filename",
    [
        "analysis.json",
        "analysis.md",
        "STAGE_D_REVIEW.md",
        "trace.json",
        "TRACE.md",
        "validation.json",
        "integrity.json",
    ],
)
def test_resealed_output_tamper(
    filename: str, tmp_path: Path, monkeypatch: pytest.MonkeyPatch, data: Any
) -> None:
    files = m.outputs(data)
    for name, raw in files.items():
        (tmp_path / name).write_bytes(raw)
    for name in ("analysis.py", "authentication.py", "reporting.py"):
        (tmp_path / name).write_bytes((m.ROOT / name).read_bytes())
    (tmp_path / filename).write_bytes(files[filename] + b"\n")
    seal = json.loads((tmp_path / "integrity.json").read_bytes())
    if filename != "integrity.json":
        seal["sha256"][filename] = m.sha((tmp_path / filename).read_bytes())
        (tmp_path / "integrity.json").write_bytes(m.encoded(seal))
    monkeypatch.setattr(m, "ROOT", tmp_path)
    with pytest.raises(ValueError, match="Stage D replay"):
        m.verify(data)


def test_overwrite_refusal(tmp_path: Path) -> None:
    (tmp_path / "existing").write_bytes(b"sealed")
    with pytest.raises(FileExistsError, match="Refusing to overwrite"):
        materialize.write_new(
            {tmp_path / "new": b"new", tmp_path / "existing": b"changed"}
        )
    assert not (tmp_path / "new").exists()
    assert (tmp_path / "existing").read_bytes() == b"sealed"


def test_compressed_hash_tamper() -> None:
    with pytest.raises(ValueError, match="archive hash"):
        auth.unpack({"gzip_b85": "00000", "sha256": "0" * 64})
