"""Independent arithmetic and adversarial tests for the captured-treatment join."""

from __future__ import annotations

# ruff: noqa: INP001, CPY001, D103, S101, PLR2004, COM812, ANN401, FBT001
import copy
from typing import TYPE_CHECKING, Any

import pytest

from experiments.codex_dogfood.case_0009.artifacts import binary
from experiments.codex_dogfood.case_0012.stage_d import analysis as a
from experiments.codex_dogfood.case_0012.stage_d import authentication as auth
from experiments.codex_dogfood.case_0012.stage_d import reporting

if TYPE_CHECKING:
    from pathlib import Path


@pytest.fixture(scope="module")
def captured() -> Any:
    return auth.authenticate()


@pytest.fixture(scope="module")
def evaluated(captured: Any) -> Any:
    return a.construct(captured)


def test_authenticated_capture(captured: Any) -> None:
    assert len(captured["resources"]) == 531
    assert len(captured["operations"]) == 72
    assert captured["behaviors"]["B"] == captured["behaviors"]["C"]
    assert captured["checkpoints"]["ancestry"] == "PASS"


def test_every_prefix_and_witness(captured: Any, evaluated: Any) -> None:
    labels = a.cell_labels(captured["gold"])
    bytes_by_address = {
        r["address"]: len(r["text"].encode("utf-8")) for r in captured["resources"]
    }
    for arm in ("A", "B", "C"):
        prefixes = []
        for ob, lane in evaluated["arms"][arm]["lanes"].items():
            order = [
                r["address"]
                for r in captured["arms"][arm][ob]["rows" if arm == "A" else "entries"]
            ]
            for witness in lane["all_witnesses"]:
                independent_depth = next(
                    (
                        i
                        for i in range(len(order) + 1)
                        if set(witness["resources"]) <= set(order[:i])
                    ),
                    None,
                )
                assert witness["completion_depth"] == independent_depth
                assert set(witness["resources"]) <= set(order[:independent_depth])
                if independent_depth:
                    assert not set(witness["resources"]) <= set(
                        order[: independent_depth - 1]
                    )
            best = min(
                lane["all_witnesses"],
                key=lambda w: (w["completion_depth"], w["identity"]),
            )
            assert lane["selected_witness"] == best["identity"]
            expected_prefix = order[: best["completion_depth"]]
            assert lane["metrics"]["prefixes"][ob] == expected_prefix
            assert lane["metrics"]["unique_utf8_bytes"] == sum(
                bytes_by_address[r] for r in set(expected_prefix)
            )
            for label, count in lane["metrics"]["label_occurrences"].items():
                assert count == sum(labels[ob, r] == label for r in expected_prefix)
            prefixes.extend(expected_prefix)
        task = evaluated["arms"][arm]["task"]
        assert task["prefix_occurrences"] == len(prefixes)
        assert task["unique_prefix_resources"] == sorted(set(prefixes))
        assert task["duplicate_occurrences"] == len(prefixes) - len(set(prefixes))
        assert task["unique_utf8_bytes"] == sum(
            bytes_by_address[r] for r in set(prefixes)
        )
    assert evaluated["arms"]["B"] == evaluated["arms"]["C"]


def test_complete_combinations(evaluated: Any) -> None:
    for arm in evaluated["arms"].values():
        assert len(arm["all_complete_task_combinations"]) == 32
        assert len(arm["minimal_complete_resource_unions"]) == 4
        assert all(len(x) == 14 for x in arm["minimal_complete_resource_unions"])
        for combination in arm["all_complete_task_combinations"]:
            resources: set[str] = set()
            prefixes: set[str] = set()
            occurrence_count = 0
            for ob, identity in combination["witnesses"].items():
                witness = next(
                    w
                    for w in arm["lanes"][ob]["all_witnesses"]
                    if w["identity"] == identity
                )
                resources.update(witness["resources"])
                prefixes.update(combination["metrics"]["prefixes"][ob])
                occurrence_count += witness["completion_depth"]
            assert sorted(resources) == combination["sufficient_resources"]
            assert sorted(prefixes) == combination["metrics"]["unique_prefix_resources"]
            assert occurrence_count == combination["metrics"]["prefix_occurrences"]


def test_hint_labels_and_bottlenecks(captured: Any, evaluated: Any) -> None:
    labels = a.cell_labels(captured["gold"])
    for arm, hints in evaluated["hints"].items():
        for hint in hints:
            if hint["hint"] in {"H05", "H06"}:
                assert hint["disposition"] == "UNSUPPORTED"
                assert not hint["targets"]
                assert hint["unsupported_concept_repository_evidence"]
            for target in hint["target_effects"]:
                assert target["label"] == labels[hint["obligation"], target["address"]]
                assert (
                    target["depth_saved"]
                    == target["native_rank"] - target["routed_position"]
                )
                for effect in target["witness_effects"]:
                    before = next(
                        w
                        for w in evaluated["arms"]["A"]["lanes"][hint["obligation"]][
                            "all_witnesses"
                        ]
                        if w["identity"] == effect["witness"]
                    )
                    after = next(
                        w
                        for w in evaluated["arms"][arm]["lanes"][hint["obligation"]][
                            "all_witnesses"
                        ]
                        if w["identity"] == effect["witness"]
                    )
                    assert effect["A_completion_depth"] == max(
                        before["member_depths"].values()
                    )
                    assert effect["exact_first_completion_depth"] == max(
                        after["member_depths"].values()
                    )
    h04 = next(h for h in evaluated["hints"]["C"] if h["hint"] == "H04")[
        "target_effects"
    ][0]
    assert h04["native_rank"] == 138
    assert h04["routed_position"] == 1
    assert all(w["exact_first_completion_depth"] == 113 for w in h04["witness_effects"])


def test_cost_and_all_frozen_gates(captured: Any, evaluated: Any) -> None:
    runtime = captured["summary"]["runtime_ns"]
    baseline = runtime["index-build"] + sum(
        v for k, v in runtime.items() if k.startswith("lexical:")
    )
    for arm in ("B", "C"):
        charged = (
            baseline
            + runtime["inventory:" + arm]
            + sum(runtime[f"route:{arm}:H{i:02}"] for i in range(1, 11))
            + sum(
                runtime[f"present:{arm}:{o['key']}"]
                for o in captured["gold"]["obligations"]
            )
        )
        assert charged == evaluated["costs"]["arms"][arm]["charged_treatment_ns"]
        gates = evaluated["frozen_gates"]["arms"][arm]
        assert gates["cost"]["pass"] == (charged <= 3 * baseline)
        assert gates["meaningful_value"]["branch_1_required_rank_gt20_position_le3"][
            "hints"
        ] == ["H04"]
        meaningful = gates["meaningful_value"]
        union = meaningful["case_union_le_twenty_one_twentieths"]
        assert union["lhs"] == 20 * union["exact_first"]
        assert union["rhs"] == 21 * union["A"]
        assert union["pass"] == (union["lhs"] <= union["rhs"])
        prefix = meaningful["branch_2_prefix_le_four_fifths"]
        assert prefix["lanes"] == [
            ob
            for ob, values in prefix["lane_evidence"].items()
            if 5 * values["exact_first"] <= 4 * values["A"]
        ]
        noise = meaningful["branch_3_unnecessary_le_four_fifths"]
        assert noise["lhs"] == 5 * noise["exact_first"]
        assert noise["rhs"] == 4 * noise["A"]
        assert noise["pass"] == (
            noise["A"] > 0 and noise["lhs"] <= noise["rhs"] and union["pass"]
        )
        for evidence in gates["obligation_safety"]["evidence"].values():
            assert evidence["pass"] == (
                4 * evidence["exact_first"] <= 5 * evidence["A"]
            )
        assert all(gate["pass"] for gate in gates.values())
    assert evaluated["outcome"] == "EXACT_HINT_ROUTING_SUPPORTED"


@pytest.mark.parametrize(
    ("contract", "extraction", "supported", "positive", "expected"),
    [
        (True, True, True, True, "EXPERIMENTAL_CONTRACT_DEFECT"),
        (False, True, True, True, "EXTRACTION_OR_RESOLUTION_DEFECT"),
        (False, False, True, True, "EXACT_HINT_ROUTING_SUPPORTED"),
        (False, False, False, True, "COMPLEMENTARY_BUT_LIMITED"),
        (False, False, False, False, "NO_MATERIAL_VALUE"),
    ],
)
def test_outcome_precedence(
    contract: bool, extraction: bool, supported: bool, positive: bool, expected: str
) -> None:
    assert (
        a.choose_outcome(
            contract_defect=contract,
            extraction_defect=extraction,
            c_passes=supported,
            complementary=positive,
        )
        == expected
    )


def test_missing_completion_is_null() -> None:
    assert (
        a.completion(
            {"resources": ["missing"], "required_unit_ids": ["unit"]}, ["other"]
        )["completion_depth"]
        is None
    )


def test_canonical_implementation_digest_scope(tmp_path: Path) -> None:
    source = tmp_path / "implementation.py"
    source.write_bytes(b"# exact captured code\r\nvalue = 1\r\n")
    assert auth.sha(binary(source)) == auth.sha(b"# exact captured code\nvalue = 1\n")
    assert auth.sha(source.read_bytes()) != auth.sha(binary(source))


def test_native_fallback_schema(captured: Any) -> None:
    for behavior in captured["behaviors"].values():
        for view in behavior["presentations"].values():
            assert view["fallback_native_order"] == [
                entry for entry in view["entries"] if entry["exact"] is None
            ]


@pytest.mark.parametrize(
    "field", ["prefix", "union", "bytes", "gate", "outcome", "hint", "witness"]
)
def test_analysis_tamper(captured: Any, evaluated: Any, field: str) -> None:
    changed = copy.deepcopy(evaluated)
    if field == "prefix":
        changed["arms"]["C"]["task"]["prefix_occurrences"] += 1
    elif field == "union":
        changed["arms"]["C"]["task"]["unique_prefix_resources"].pop()
    elif field == "bytes":
        changed["arms"]["C"]["task"]["unique_utf8_bytes"] += 1
    elif field == "gate":
        changed["frozen_gates"]["arms"]["C"]["cost"]["pass"] = False
    elif field == "outcome":
        changed["outcome"] = "NO_MATERIAL_VALUE"
    elif field == "hint":
        changed["hints"]["C"][0]["target_effects"][0]["label"] = "UNNECESSARY"
    else:
        changed["arms"]["C"]["lanes"]["source"]["all_witnesses"][0]["resources"].pop()
    with pytest.raises(ValueError, match="reconstruction"):
        a.verify_analysis(changed, captured)


@pytest.mark.parametrize(
    "field", ["candidate", "rank", "score", "contribution", "global", "duplicate"]
)
def test_candidate_tamper(captured: Any, field: str) -> None:
    changed = copy.deepcopy(captured)
    if field == "candidate":
        changed["arms"]["C"]["source"]["entries"].pop()
    elif field == "duplicate":
        changed["arms"]["C"]["source"]["entries"].append(
            changed["arms"]["C"]["source"]["entries"][0]
        )
    elif field == "rank":
        changed["arms"]["C"]["source"]["entries"][0]["native_rank"] += 1
    elif field == "score":
        changed["arms"]["C"]["source"]["entries"][0]["score"] += 1
    elif field == "contribution":
        changed["behaviors"]["C"]["presentations"]["source"]["original_lexical"][
            "native_order"
        ][0]["content_contributions"][0]["contribution"] += 1
    else:
        changed["behaviors"]["C"]["presentations"]["source"]["global_safety"][
            "maximum_results"
        ] -= 1
    with pytest.raises(
        ValueError,
        match=r"candidate|Candidate|Native|native|Global|Duplicate|Original|Routed",
    ):
        a.safety(changed)


def test_deterministic_surfaces(captured: Any, evaluated: Any) -> None:
    assert a.encoded(evaluated) == a.encoded(a.construct(captured))
    assert reporting.markdown(evaluated) == reporting.markdown(copy.deepcopy(evaluated))
    assert a.encoded(reporting.trace(evaluated)) == a.encoded(
        reporting.trace(copy.deepcopy(evaluated))
    )


def test_published_exact_replay() -> None:
    assert a.verify()["status"] == "PASS"


def test_overwrite_preflight(tmp_path: Path, monkeypatch: Any) -> None:
    monkeypatch.setattr(a, "ROOT", tmp_path)
    (tmp_path / "existing").write_bytes(b"original")
    with pytest.raises(FileExistsError, match="overwrite"):
        a.write_new({"absent": b"new", "existing": b"replace"})
    assert (tmp_path / "existing").read_bytes() == b"original"
    assert not (tmp_path / "absent").exists()


def test_output_hash_and_tamper(tmp_path: Path, monkeypatch: Any) -> None:
    files = {"analysis.json": b"trusted", "integrity.json": b"seal"}
    for name, raw in files.items():
        (tmp_path / name).write_bytes(raw)
    monkeypatch.setattr(a, "ROOT", tmp_path)
    monkeypatch.setattr(a, "outputs", lambda: files)
    # Verification checks exact reconstructed bytes, so a resealed altered output
    # cannot pass merely by updating a local digest manifest.
    (tmp_path / "analysis.json").write_bytes(b"altered")
    with pytest.raises(ValueError, match="tamper"):
        a.verify()
