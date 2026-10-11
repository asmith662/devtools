"""Independent arithmetic oracles and adversarial sealed-capture/gold mutations."""

from __future__ import annotations

# ruff: noqa: INP001, CPY001, D103, S101, PLR2004, COM812, ANN401, C901, PLR0912
import asyncio
import copy
from typing import TYPE_CHECKING, Any

import pytest

from experiments.codex_dogfood.case_0009.artifacts import binary
from experiments.codex_dogfood.case_0014.adjudication.reviewed import materialize as m
from experiments.codex_dogfood.case_0014.stage_d import analysis as a
from experiments.codex_dogfood.case_0014.stage_d import authentication as auth
from experiments.query_term_weighting.gates import Comparison, evaluate

if TYPE_CHECKING:
    from pathlib import Path


@pytest.fixture(scope="module")
def data() -> Any:
    return auth.authenticate()


@pytest.fixture(scope="module")
def result(data: Any) -> Any:
    return a.calculate(data)


def test_frozen_input_seals_and_exact_join(data: Any, result: Any) -> None:
    assert data["provenance"]["stage_a_readme_restoration"] == auth.RESTORED
    original = auth.load(auth.CASE / "integrity.json")
    assert (
        auth.sha(binary(auth.CASE / "README.md")) == original["authored"]["README.md"]
    )
    assert result["joins"] == {
        "resources": 515,
        "cells": 3090,
        "units": 30,
        "witnesses": 36,
        "required_cells": 34,
        "missing": 0,
        "duplicate": 0,
        "unexpected": 0,
        "stale_frame": 0,
        "identity_dimensions": [
            "case",
            "task",
            "obligation",
            "RepositoryId",
            "SnapshotId",
            "CorpusId",
            "address",
            "content_identity",
            "document_identity",
        ],
    }
    assert data["journal"]["pairs"] == 27
    assert result["native_authentication"]["candidate_counts"] == {
        "Q1": 216,
        "Q2": 208,
        "Q3": 180,
        "Q4": 343,
        "Q5": 492,
        "Q6": 460,
    }
    assert result["native_authentication"]["positive_occurrences"] == 1899
    assert result["native_authentication"]["reference"] == "UNCHANGED"
    assert not any(result["required_reach_losses"].values())


def test_independent_witness_prefix_and_union_oracle(data: Any, result: Any) -> None:
    primary = data["gold"]["primary"]
    labels = {
        (c["obligation_identity"].split("/")[-1], c["resource_identity"]): c["label"]
        for c in primary["cells"]
    }
    for arm in "ABC":
        selected_prefixes = []
        selected_labels: list[str] = []
        for obligation in primary["obligation_semantics"]:
            key = obligation["obligation"]
            ordered = [
                r["document_id"] for r in data["arms"][arm]["Q" + key[1:]]["matches"]
            ]
            alternatives = []
            actual = {
                w["identity"]: w for w in result["arms"][arm]["lanes"][key]["witnesses"]
            }
            for witness in obligation["witnesses"]:
                members = set(witness["resources"])
                depth = next(
                    (
                        i
                        for i in range(1, len(ordered) + 1)
                        if members <= set(ordered[:i])
                    ),
                    None,
                )
                w = actual[witness["identity"]]
                assert w["completion_depth"] == depth
                assert w["member_ranks"] == {
                    rid: ordered.index(rid) + 1 if rid in ordered else None
                    for rid in members
                }
                assert w["units"] == witness["units"]
                if depth is not None:
                    prefix = ordered[:depth]
                    assert w["prefix_resources"] == prefix
                    assert w["metrics"]["prefix_occurrences"] == len(prefix)
                    assert w["metrics"]["unique_prefix_resources"] == len(set(prefix))
                    assert w["metrics"]["distinct_utf8_bytes"] == sum(
                        len(data["resources"][rid]["content"].encode("utf-8"))
                        for rid in set(prefix)
                    )
                    for label in ("REQUIRED", "HELPFUL_ONLY", "UNNECESSARY"):
                        assert w["metrics"]["label_occurrences"][label] == sum(
                            labels[key, rid] == label for rid in prefix
                        )
                    alternatives.append((depth, witness["identity"], prefix))
            selected = min(alternatives)
            lane = result["arms"][arm]["lanes"][key]
            assert (lane["completion_depth"], lane["selected"]) == selected[:2]
            selected_prefixes.extend(selected[2])
            selected_labels.extend(labels[key, rid] for rid in selected[2])
        burden = result["arms"][arm]["burden"]
        assert burden["prefix_occurrences"] == len(selected_prefixes)
        assert burden["unique_prefix_resources"] == len(set(selected_prefixes))
        assert burden["duplicate_occurrences"] == len(selected_prefixes) - len(
            set(selected_prefixes)
        )
        assert burden["distinct_utf8_bytes"] == sum(
            len(data["resources"][rid]["content"].encode("utf-8"))
            for rid in set(selected_prefixes)
        )
        assert burden["label_occurrences"] == {
            label: selected_labels.count(label)
            for label in ("REQUIRED", "HELPFUL_ONLY", "UNNECESSARY")
        }


def test_required_ranks_attribution_and_frozen_arithmetic(
    data: Any, result: Any
) -> None:
    for row in result["required_cells"]:
        for arm in "ABC":
            matches = data["arms"][arm][row["query"]]["matches"]
            observed = next(
                (r for r in matches if r["document_id"] == row["resource"]), None
            )
            assert row["ranks"][arm] == (None if observed is None else observed["rank"])
            assert observed is not None
            assert row["contributions"][arm]["terms"] == observed["contributions"]
        before, after = row["ranks"]["A"], row["ranks"]["C"]
        c = row["changes"]["A_to_C"]
        assert c["meaningful_rank_gain"] == (
            before - after >= 2 and after * 5 <= before * 4
        )
        assert c["bounded"] == (after * 5 <= before * 6 and after - before <= 10)
        for change in row["changes"].values():
            crossings = change["crossings"]
            assert change["rank_delta_after_minus_before"] == len(
                crossings["overtakers"]
            ) - len(crossings["overtaken"])
        if "EXPLICIT_ANCHOR_OVERWEIGHT" in row["failure_classes"]:
            assert row["ranks"]["B"] > row["ranks"]["A"]
            assert any(
                r["owning_label"] != "REQUIRED"
                for r in row["changes"]["A_to_B"]["crossings"]["overtakers"]
            )
    for case in result["query_dilution_not_reduced"]:
        assert case["proofs"]
        assert all(p["owning_label"] != "REQUIRED" for p in case["proofs"])
        assert all(
            p["ranks"][arm] < case["required_ranks"][arm]
            for p in case["proofs"]
            for arm in "BC"
        )
    ev = result["gate_evidence"]
    assert result["gates"] == evaluate(Comparison(**ev))
    assert result["gates"]["outcome"] == "QUERY_TERM_WEIGHTING_HARMFUL"
    assert result["gates"]["depth_safe"]
    assert not result["gates"]["required_rank_safe"]
    assert not result["gates"]["bounded_regressions"]
    assert result["gates"]["burden_safe"]
    assert result["gates"]["meaningful_obligation_indices"] == (4, 5)


@pytest.mark.parametrize(
    ("baseline", "treatment", "expected"),
    [
        (10, 8, True),
        (5, 4, False),
        (10, 9, False),
        (11, 9, False),
        (None, 1, False),
        (1, None, False),
    ],
)
def test_meaningful_rank_edges(
    baseline: int | None, treatment: int | None, *, expected: bool
) -> None:
    assert a.meaningful_rank(baseline, treatment) is expected


def test_witness_and_regression_integer_boundaries() -> None:
    assert a.meaningful_witness(None, 1)
    assert not a.meaningful_witness(1, None)
    assert a.meaningful_witness(5, 4)
    assert not a.meaningful_witness(6, 5)
    assert a.bounded(50, 60, 10)
    assert not a.bounded(51, 62, 10)
    assert a.bounded(25, 30, 5)
    assert not a.bounded(30, 36, 5)


def test_cost_is_captured_without_double_count(data: Any) -> None:
    times = {op["identity"]: op["runtime_ns"] for op in data["journal"]["operations"]}
    costs = data["costs"]
    shared = (
        times["frame:prepare"]
        + times["index-build"]
        + sum(times["query:Q" + str(i)] for i in range(1, 7))
    )
    assert costs["shared_charged_equally_ns"] == shared == 10479396100
    for arm in "ABC":
        construction = sum(
            times["construct:" + arm + ":Q" + str(i)] for i in range(1, 7)
        )
        assert costs["arms"][arm]["construction_ns"] == construction
        assert costs["arms"][arm]["charged_ns"] == shared + construction
    assert (
        costs["shared"]["reference_native_acquisition_ns"] == times["query:reference"]
    )
    assert data["finalization"]["derivation_publication_ns"] == 22679474600


@pytest.mark.parametrize(
    "mutation",
    [
        "rank",
        "witness_depth",
        "selected_tie",
        "prefix",
        "unique",
        "occurrence",
        "duplicate",
        "label_occurrences",
        "byte_count",
        "unit_reach",
        "meaningful_rank",
        "meaningful_witness",
        "regression_bound",
        "attribution",
        "cost",
        "gate",
        "precedence",
        "top_k",
        "join",
        "witness_member",
    ],
)
def test_output_mutations_rejected(data: Any, result: Any, mutation: str) -> None:
    value = copy.deepcopy(result)
    if mutation == "rank":
        value["required_cells"][0]["ranks"]["C"] += 1
    elif mutation == "witness_depth":
        value["arms"]["C"]["lanes"]["O5"]["witnesses"][0]["completion_depth"] += 1
    elif mutation == "selected_tie":
        value["arms"]["C"]["lanes"]["O1"]["selected"] = "O1/W002"
    elif mutation == "prefix":
        value["arms"]["C"]["lanes"]["O1"]["witnesses"][0]["prefix_resources"].pop()
    elif mutation in ("unique", "occurrence", "duplicate", "byte_count"):
        key = {
            "unique": "unique_prefix_resources",
            "occurrence": "prefix_occurrences",
            "duplicate": "duplicate_occurrences",
            "byte_count": "distinct_utf8_bytes",
        }[mutation]
        value["arms"]["C"]["burden"][key] += 1
    elif mutation == "label_occurrences":
        value["arms"]["C"]["burden"]["label_occurrences"]["UNNECESSARY"] += 1
    elif mutation == "unit_reach":
        value["arms"]["C"]["required_reach"]["units"].pop()
    elif mutation == "meaningful_rank":
        value["required_cells"][0]["changes"]["A_to_C"]["meaningful_rank_gain"] = True
    elif mutation == "meaningful_witness":
        value["obligation_comparisons"]["O1"]["comparisons"]["A_to_C"][
            "meaningful_witness_gain"
        ] = True
    elif mutation == "regression_bound":
        value["required_cells"][0]["changes"]["A_to_C"]["bounded"] = True
    elif mutation == "attribution":
        value["anchor_attribution"]["required_regressions"].pop()
    elif mutation == "cost":
        value["costs"]["arms"]["C"]["charged_ns"] += 1
    elif mutation == "gate":
        value["gates"]["bounded_regressions"] = True
    elif mutation == "precedence":
        value["precedence_application"]["outcome"] = "NO_MATERIAL_VALUE"
    elif mutation == "top_k":
        value["top_k_diagnostics"]["O1"]["C-A"]["10"]["entered_counts"]["REQUIRED"] += 1
    elif mutation == "join":
        value["joins"]["stale_frame"] = 1
    else:
        value["arms"]["C"]["lanes"]["O1"]["witnesses"][0]["member_ranks"].clear()
    with pytest.raises(ValueError, match="calculation identity"):
        a.validate(value, data)


@pytest.mark.parametrize(
    "key",
    [
        "gold",
        "design",
        "resources",
        "native",
        "stage_b_trace",
        "costs",
        "journal",
        "provenance",
        "native_validation",
    ],
)
def test_authenticated_input_mutation(data: Any, key: str) -> None:
    changed = dict(data)
    changed[key] = copy.deepcopy(data[key])
    if key == "gold":
        changed[key]["primary"]["cells"][0]["label"] = "REQUIRED"
    else:
        changed[key]["TAMPER"] = True
    with pytest.raises(ValueError, match="identity"):
        a.calculate(changed)


def test_candidate_and_application_mutations(data: Any) -> None:
    for kind in ("candidate", "contribution", "native_evidence", "policy", "tie"):
        arms = copy.deepcopy(data["arms"])
        lane = arms["C"]["Q1"]
        if kind == "candidate":
            lane["matches"].pop()
        elif kind == "contribution":
            lane["matches"][0]["contributions"][0]["multiplier"] = 1
        elif kind == "native_evidence":
            lane["matches"][0]["native_content_evidence"][0]["document_frequency"] += 1
        elif kind == "policy":
            lane["query_policy"]["terms"][0]["role"] = "SEMANTIC"
        else:
            lane["matches"][0], lane["matches"][1] = (
                lane["matches"][1],
                lane["matches"][0],
            )
        with pytest.raises(ValueError, match=r".+"):
            auth.validate_arms(arms, data["design"], data["resources"], data["native"])


def test_capture_hash_tampering(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    (tmp_path / "integrity.json").write_bytes(b"{}")
    monkeypatch.setattr(auth, "CAPTURE", tmp_path)
    with pytest.raises(ValueError, match="Stage B integrity"):
        asyncio.run(auth.checkpoints())


def test_deterministic_artifacts_overwrite_and_tamper(
    data: Any, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    files = a.outputs(data)
    assert files == a.outputs(data)
    m.write_new({tmp_path / name: raw for name, raw in files.items()})
    with pytest.raises(FileExistsError):
        m.write_new({tmp_path / "new": b"new", tmp_path / "analysis.json": b"bad"})
    assert not (tmp_path / "new").exists()
    for name in ("analysis.py", "authentication.py", "reporting.py"):
        (tmp_path / name).write_bytes((a.ROOT / name).read_bytes())
    monkeypatch.setattr(a, "ROOT", tmp_path)
    assert a.verify(data)["status"] == "PASS"
    (tmp_path / "integrity.json").write_bytes(b"{}")
    with pytest.raises(ValueError, match="Stage D replay"):
        a.verify(data)
