"""Exact capture/gold joins, empty witnesses, gates, burden and tamper rejection."""

from __future__ import annotations

# ruff: noqa: INP001, CPY001, D103, S101, PLR2004, COM812, ANN401
import asyncio
import copy
from typing import TYPE_CHECKING, Any

import pytest

from experiments.bm25f.gates import Comparison, evaluate
from experiments.codex_dogfood.case_0015.adjudication.reviewed import git_identity
from experiments.codex_dogfood.case_0015.adjudication.reviewed import (
    materialize as publication,
)
from experiments.codex_dogfood.case_0015.stage_d import analysis as a
from experiments.codex_dogfood.case_0015.stage_d import authentication as auth
from experiments.codex_dogfood.case_0015.stage_d.reporting import artifacts

if TYPE_CHECKING:
    from pathlib import Path


@pytest.fixture(scope="module")
def data() -> Any:
    return auth.authenticate()


@pytest.fixture(scope="module")
def result(data: Any) -> Any:
    return a.calculate(data)


def test_o2_empty_repository_witness_is_complete_zero(data: Any, result: Any) -> None:
    primary = data["gold"]["primary"]
    witness = primary["witnesses"]["O2"][0]
    assert witness["resources"] == []
    assert not any(
        c["label"] == "REQUIRED" for c in primary["cells"] if c["obligation"] == "O2"
    )
    for arm in "AB":
        m = result["witness_calculations"]["O2"][arm][0]
        assert m["complete"] is True
        assert m["completion_status"] == "COMPLETE"
        assert m["depth"] == 0
        assert m["repository_member_ranks"] == {}
        assert (
            m["prefix_occurrences"]
            == m["unique_prefix_resources"]
            == m["distinct_utf8_bytes"]
            == 0
        )
        assert m["label_occurrences"] == dict.fromkeys(a.LABELS, 0)
    comparison = result["obligation_comparisons"]["O2"]["change"]
    assert comparison["classification"] == "TIED"
    assert comparison["meaningful_improvement"] is False
    evidence = Comparison(
        contract=True,
        application=True,
        reach=True,
        depths=((0, 0),),
        required_ranks=((1, 1),),
        unique_resources=(0, 0),
        occurrences=(0, 0),
        utf8_bytes=(0, 0),
    )
    gates = evaluate(evidence)
    assert gates["meaningful_obligation_indices"] == ()
    assert gates["outcome"] == "NO_MATERIAL_VALUE"


def test_all_witnesses_independent_prefix_math(data: Any, result: Any) -> None:
    assert sum(len(v["A"]) for v in result["witness_calculations"].values()) == 12
    labels = {
        (c["obligation"], c["resource"]): c["label"]
        for c in data["gold"]["primary"]["cells"]
    }
    for o, arms in result["witness_calculations"].items():
        for arm, witnesses in arms.items():
            lanes = data["arms"][arm]["Q" + o[1:]]["matches"]
            ranks = {r["document_identity"]: r["rank"] for r in lanes}
            for w in witnesses:
                expected = {rid: ranks.get(rid) for rid in w["repository_member_ranks"]}
                assert w["repository_member_ranks"] == expected
                assert w["complete"] == all(v is not None for v in expected.values())
                assert w["depth"] == max(
                    (v for v in expected.values() if v is not None), default=0
                )
                prefix = [r["document_identity"] for r in lanes[: w["depth"]]]
                assert w["prefix_resources"] == prefix
                assert w["prefix_occurrences"] == len(prefix)
                assert w["unique_prefix_resources"] == len(set(prefix))
                assert w["distinct_utf8_bytes"] == sum(
                    data["resources"][rid]["utf8_bytes"] for rid in set(prefix)
                )
                for label in a.LABELS:
                    assert w["label_occurrences"][label] == sum(
                        labels[(o, rid)] == label for rid in prefix
                    )
            assert result["selected_witnesses"][arm][o] == min(
                witnesses, key=lambda w: (w["depth"], w["witness"])
            )


def test_stable_selection_and_missing_member() -> None:
    empty = {"id": "O2.W1", "resources": [], "units": ["T04"]}
    assert a.witness_metrics(empty, [], "O2", {}, {})["depth"] == 0
    missing = {"id": "O1.W1", "resources": ["absent"], "units": ["R01"]}
    m = a.witness_metrics(
        missing, [], "O1", {}, {"absent": {"address": "a", "utf8_bytes": 1}}
    )
    assert m["complete"] is False
    assert m["depth"] is None
    first = {"complete": True, "depth": 4, "witness": "O1.W1"}
    second = {"complete": True, "depth": 4, "witness": "O1.W2"}
    assert a.select([second, first]) == first


def test_exact_integer_gain_and_boundaries() -> None:
    assert a.change(10, 8)["meaningful_improvement"] is True
    assert a.change(10, 9)["meaningful_improvement"] is False
    assert a.change(None, 7)["meaningful_improvement"] is True
    assert a.change(0, 0)["meaningful_improvement"] is False
    assert a.change(3, 2, rank=True)["meaningful_improvement"] is False
    assert a.change(10, 8, rank=True)["meaningful_improvement"] is True
    assert a.change(2, 3, rank=True)["complementary_bound"] is False
    assert a.change(50, 60, rank=True)["complementary_bound"] is True
    assert a.change(100, 111, rank=True)["complementary_bound"] is False
    assert a.change(25, 30)["complementary_bound"] is True
    assert a.change(100, 106)["complementary_bound"] is False
    assert a.change(1, None, rank=True)["classification"] == "WORSENED"
    assert a.change(None, None, rank=True)["meaningful_improvement"] is False


def test_case_wide_prefix_union(data: Any, result: Any) -> None:
    for arm in "AB":
        selected = result["selected_witnesses"][arm]
        occurrences = [rid for w in selected.values() for rid in w["prefix_resources"]]
        unique = set(occurrences)
        burden = result["case_wide_burden"][arm]
        assert burden["prefix_occurrences"] == len(occurrences)
        assert burden["unique_prefix_resources"] == len(unique)
        assert burden["duplicate_occurrences"] == len(occurrences) - len(unique)
        assert burden["distinct_utf8_bytes"] == sum(
            len(data["resources"][rid]["content"].encode("utf-8")) for rid in unique
        )
        assert sum(burden["label_occurrences"].values()) == len(occurrences)


def test_all_required_cells_and_frozen_outcome(result: Any) -> None:
    assert len(result["required_cells"]) == 21
    assert all(
        r["query"] == "Q" + r["obligation"][1:] for r in result["required_cells"]
    )
    for arm in "AB":
        reach = result["required_reach"][arm]
        assert tuple(
            len(reach[k]) for k in ("resources", "cells", "repository_units", "units")
        ) == (11, 21, 17, 42)
    assert result["gates"]["outcome"] == "BM25F_HARMFUL"
    assert result["gates"]["depth_safe"] is False
    assert result["gates"]["required_rank_safe"] is False
    assert result["gates"]["bounded_regressions"] is False
    assert (
        result["meaningful_witness_gains"]
        == result["meaningful_required_rank_gains"]
        == []
    )
    assert len(result["required_regressions"]) == 2


@pytest.mark.parametrize(
    "field",
    [
        "joins",
        "required_cells",
        "witness_calculations",
        "selected_witnesses",
        "obligation_comparisons",
        "case_wide_burden",
        "required_reach",
        "gate_evidence",
        "gate_arithmetic",
        "gates",
        "precedence",
        "costs",
        "failure_attribution",
        "top_k_gold_diagnostics",
    ],
)
def test_reject_analysis_mutation(data: Any, result: Any, field: str) -> None:
    value = {**result, field: {"tampered": True}}
    with pytest.raises(ValueError, match="deterministic calculation"):
        a.validate(value, data)


def test_field_and_candidate_tamper(data: Any) -> None:
    fields = copy.deepcopy(data["fields"])
    fields["documents"][0]["CONTENT"]["length"] += 1
    with pytest.raises(ValueError, match="observations"):
        auth.validate_fields(
            fields, data["union"], data["statistics"], data["resources"]
        )
    union = copy.deepcopy(data["union"])
    next(iter(union["terms"].values()))["df_union"] += 1
    with pytest.raises(ValueError, match="union"):
        auth.validate_fields(
            data["fields"], union, data["statistics"], data["resources"]
        )


def test_overwrite_refusal_and_output_tamper(
    data: Any, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    files = a.outputs(data)
    for name, raw in files.items():
        (tmp_path / name).write_bytes(raw)
    with pytest.raises(FileExistsError):
        publication.write_new(
            {tmp_path / "new": b"new", tmp_path / "analysis.json": b"bad"}
        )
    assert not (tmp_path / "new").exists()
    (tmp_path / "analysis.json").write_bytes(b"{}")
    monkeypatch.setattr(a, "ROOT", tmp_path)
    # Implementation hashes retain the real source owner during output replay.
    for name in (
        "analysis.py",
        "authentication.py",
        "reporting.py",
        "test_analysis.py",
    ):
        (tmp_path / name).write_bytes((auth.ROOT / name).read_bytes())
    with pytest.raises(ValueError, match="Stage D replay"):
        a.verify(data)


def test_mechanism_crossing_consequence(result: Any) -> None:
    for cell in result["required_cells"]:
        causal = cell["causal"]
        for crossing in causal.get("crossings", []):
            ranks = crossing["ranks"]
            if crossing["direction"] == "OVERTAKES_REQUIRED":
                assert ranks["required_A"] < ranks["other_A"]
                assert ranks["required_B"] > ranks["other_B"]
            effects = crossing["relative_mechanism_effects"]
            assert all(k in effects for k in a.MECHANISMS)
            for name, key in (
                ("UNION_IDF_HARM", "union_idf_delta"),
                ("CROSS_FIELD_SATURATION_HARM", "cross_field_single_saturation_delta"),
                ("FILENAME_FIELD_OVERWEIGHT", "pre_saturation_weight_delta"),
            ):
                if name in crossing["failure_classes"]:
                    assert crossing["direction"] == "OVERTAKES_REQUIRED"
                    assert effects[key]["numerator"] < 0


def test_index_cli_mapping_preserves_blob_bytes(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    calls = []

    async def fake_git(*args: str) -> bytes:
        calls.append(args)
        name = args[1].rsplit("/", 1)[1]
        return (publication.ADJ / "primary" / name).read_bytes()

    monkeypatch.setattr(git_identity, "git", fake_git)
    assert asyncio.run(git_identity.verify("INDEX")) == publication.HASHES
    assert all(args[1].startswith(":experiments/") for args in calls)


def test_markdown_has_exactly_one_final_newline() -> None:
    value = auth.decoded(auth.load(auth.ROOT / "analysis.json"))
    for name, raw in artifacts(value).items():
        if name.endswith(".md"):
            assert raw.endswith(b"\n")
            assert not raw.endswith(b"\n\n")
