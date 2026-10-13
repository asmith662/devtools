# Copyright (c) 2026
# ruff: noqa: ANN401, S101, D103, PLR2004, E501 -- adversarial captured-input tests
"""Reject malformed joins and derived results; never acquire or inspect child state."""

from __future__ import annotations

import asyncio
import gzip
import json
from copy import deepcopy
from functools import lru_cache
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from pathlib import Path

import pytest

from experiments.codex_dogfood.case_0009.artifacts import json_bytes
from experiments.codex_dogfood.verification.proof import authenticate_proof
from experiments.structural_discrimination.decision import (
    Label,
    case_category,
    classify_pair,
)
from experiments.structural_discrimination.stage_b import authentication, capture
from experiments.structural_discrimination.stage_c import import_gold
from experiments.structural_discrimination.stage_d import analyze, join


@lru_cache
def fixture() -> tuple[Any, Any, Any]:
    case = capture.case_root("0017")
    design = json.loads((case / "protocol.json").read_bytes())
    trace = json.loads(
        gzip.decompress((capture.capture_root("0017") / "trace.json.gz").read_bytes()),
    )
    gold = json.loads((case / "adjudication/reviewed/gold.json").read_bytes())
    return design, trace, gold


@pytest.mark.parametrize(
    "defect",
    [
        "case",
        "frame",
        "obligation",
        "target",
        "predecessor",
        "source",
        "A-rank",
        "source-rank",
        "self",
        "Reference",
        "label",
        "duplicate-gold",
        "missing-gold",
        "duplicate-pair",
        "missing-pair",
        "predecessor-rank",
        "source-frame",
        "content",
        "occurrences",
        "duplicate-support",
    ],
)
def test_join_mutations_rejected(defect: str) -> None:  # noqa: C901, PLR0912
    design, trace, gold = deepcopy(fixture())
    q = trace["queries"][0]
    annotation = q["annotations"][0]
    pair = q["local_pairs"][0]
    source = annotation["sources"][0]
    if defect == "case":
        gold["case"] = "foreign"
    elif defect == "frame":
        gold["frame"]["snapshot_id"] = "foreign"
    elif defect == "obligation":
        pair["obligation"] = "O4"
    elif defect == "target":
        annotation["target"]["address"] = "foreign"
    elif defect == "predecessor":
        pair["predecessor"]["address"] = "foreign"
    elif defect == "source":
        source["address"] = "foreign"
    elif defect == "A-rank":
        q["A"][0]["a_rank"] = 99
    elif defect == "source-rank":
        source["a_rank"] = annotation["target"]["a_rank"]
    elif defect == "self":
        source["address"] = annotation["target"]["address"]
    elif defect == "Reference":
        source["supports"][0]["fact_identity"] = "foreign"
    elif defect == "label":
        gold["cells"][0]["label"] = "UNKNOWN"
    elif defect == "duplicate-gold":
        gold["cells"].append(deepcopy(gold["cells"][0]))
    elif defect == "missing-gold":
        gold["cells"].pop()
    elif defect == "duplicate-pair":
        q["local_pairs"].append(deepcopy(pair))
    elif defect == "missing-pair":
        q["local_pairs"].pop()
    elif defect == "predecessor-rank":
        pair["predecessor"]["a_rank"] -= 1
    elif defect == "source-frame":
        source["snapshot_id"] = "foreign"
    elif defect == "content":
        gold["cells"][0]["content_identity"] = "foreign"
    elif defect == "occurrences":
        annotation["native_occurrence_count"] += 1
    else:
        source["supports"].append(deepcopy(source["supports"][0]))
    with pytest.raises(
        (ValueError, KeyError),
        match=r"identity|frame|obligation|binding|source|Source|count|Count|cell|label|pair|predecessor|fact|content|join|Reference|occurrence|evidence|target|A identities",
    ):
        join.validate_join("0017", design, trace, gold)


def test_ablation_exact_captured_a() -> None:
    _, trace, _ = fixture()
    for q in trace["queries"]:
        ablated = join.ablate(q)
        assert ablated["A"] is q["A"]
        assert json_bytes(ablated["A"]) == json_bytes(q["A"])
        assert ablated["annotations"] == ablated["local_pairs"] == []


@pytest.mark.parametrize(
    ("beneficial", "harmful", "expected"),
    [
        (0, 0, "NO_MATERIAL_STRUCTURAL_DISCRIMINATION_SIGNAL"),
        (1, 0, "STRUCTURAL_DISCRIMINATION_SIGNAL"),
        (0, 1, "STRUCTURAL_DISCRIMINATION_CONTRADICTED"),
        (1, 1, "MIXED_STRUCTURAL_DISCRIMINATION_SIGNAL"),
    ],
)
def test_category_boundaries(beneficial: int, harmful: int, expected: str) -> None:
    assert case_category(beneficial, harmful) == expected


@pytest.mark.parametrize(
    ("target", "predecessor", "direction"),
    [
        ("REQUIRED", "UNNECESSARY", "BENEFICIAL"),
        ("UNNECESSARY", "REQUIRED", "HARMFUL"),
        ("REQUIRED", "HELPFUL_ONLY", "BENEFICIAL"),
        ("HELPFUL_ONLY", "REQUIRED", "HARMFUL"),
        ("HELPFUL_ONLY", "UNNECESSARY", "BENEFICIAL"),
        ("UNNECESSARY", "HELPFUL_ONLY", "HARMFUL"),
        ("REQUIRED", "REQUIRED", "NEUTRAL"),
        ("HELPFUL_ONLY", "HELPFUL_ONLY", "NEUTRAL"),
        ("UNNECESSARY", "UNNECESSARY", "NEUTRAL"),
    ],
)
def test_ordinal_pair_table(target: str, predecessor: str, direction: str) -> None:
    result = classify_pair(Label(target), Label(predecessor))
    assert result.direction == direction
    assert result.strong_beneficial == (
        target == "REQUIRED" and predecessor == "UNNECESSARY"
    )
    assert result.strong_harmful == (
        target == "UNNECESSARY" and predecessor == "REQUIRED"
    )


def case_result() -> Any:
    design, trace, gold = fixture()
    return join.analyze_case(
        "0017",
        design,
        trace,
        gold,
        {o: {} for o in ("O1", "O2", "O3")},
    )


@pytest.mark.parametrize(
    "defect",
    ["category", "classification", "strong", "aggregation"],
)
def test_case_result_mutation(defect: str) -> None:
    case = case_result()
    if defect == "category":
        case["category"] = "STRUCTURAL_DISCRIMINATION_SIGNAL"
    elif defect == "classification":
        case["queries"][0]["targets"][0]["classification"] = "HARMFUL"
    elif defect == "strong":
        case["queries"][0]["targets"][0]["strong_harmful"] = True
    else:
        case["totals"]["supported_targets"] += 1
    with pytest.raises(ValueError, match="calculation"):
        join.validate_case_result(case)


def test_primary_artifact_hash(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    source = import_gold.primary_root("0017")
    root = tmp_path / "primary"
    root.mkdir()
    (root.parent / "IMPORT.json").write_bytes(
        (source.parent / "IMPORT.json").read_bytes(),
    )
    (root / "stage_c_review.json").write_bytes(
        (source / "stage_c_review.json").read_bytes() + b"tampered",
    )
    monkeypatch.setattr(import_gold, "primary_root", lambda _case: root)
    with pytest.raises(ValueError, match="Primary artifact hash"):
        asyncio.run(import_gold.authenticate("0017"))


def test_stage_b_completion_proof_tamper() -> None:
    root = capture.capture_root("0017")
    seal = json.loads((root / "integrity.json").read_bytes())
    hashes = {p: h for p, h in seal["sha256"].items() if p != "completion_proof.json"}
    bindings = authentication.bindings(root, hashes, seal["implementation"])
    raw = (root / "completion_proof.json").read_bytes()
    authenticate_proof(raw, seal["sha256"]["completion_proof.json"], bindings)
    with pytest.raises(ValueError, match=r"proof|Proof|hash|bytes"):
        authenticate_proof(
            raw + b"tampered",
            seal["sha256"]["completion_proof.json"],
            bindings,
        )


def test_output_integrity_and_overwrite(tmp_path: Path) -> None:
    path = tmp_path / "integrity.json"
    files = {path: b'{"scope":"exact"}\n'}
    analyze.publish(files)
    analyze.verify_bytes(files)
    with pytest.raises(ValueError, match="overwrite refused"):
        analyze.publish(files)
    path.write_bytes(b'{"scope":"forged"}\n')
    with pytest.raises(ValueError, match="exact output/integrity differs"):
        analyze.verify_bytes(files)


def test_cohort_exact_repeated_and_no_acquisition(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    def forbidden(*_args: Any, **_kwargs: Any) -> Any:
        pytest.fail("Scientific acquisition is forbidden in Stage D")

    for name in (
        "retrieve_repository_text_documents_by_bm25",
        "analyze_repository_text_lexical_query",
        "build_repository_text_lexical_inverted_index",
        "interpret_python_module_resources",
        "annotate",
    ):
        monkeypatch.setattr(capture, name, forbidden)
    analysis, inputs = asyncio.run(analyze.calculate())
    repeated, repeated_inputs = asyncio.run(analyze.calculate())
    assert analyze.artifacts(analysis, inputs) == analyze.artifacts(
        repeated,
        repeated_inputs,
    )
    totals = analysis["cohort"]["totals"]
    assert totals["local_pairs"] == 121
    assert totals["pair_counts"] == {
        "BENEFICIAL": 7,
        "NEUTRAL": 110,
        "HARMFUL": 4,
        "STRONG_BENEFICIAL": 1,
        "STRONG_HARMFUL": 0,
    }
    assert totals["supported_gold_labels"] == {
        "REQUIRED": 6,
        "HELPFUL_ONLY": 9,
        "UNNECESSARY": 106,
    }
    assert totals["qualifying_support_occurrences"] == 1281
    assert totals["distinct_source_target_obligation_pairs"] == 218
    assert totals["A_candidate_occurrences"] == 1560
    assert totals["baseline_A_useful_candidate_occurrences"] == 144
    assert totals["required_in_A"] == 39
    assert all(
        not q["baseline_lexical_non_reach"]
        for c in analysis["cases"]
        for q in c["queries"]
    )
    join.validate_cohort_result(analysis["cases"], analysis["cohort"])
    altered = deepcopy(analysis["cohort"])
    altered["totals"]["supported_gold_labels"]["REQUIRED"] += 1
    with pytest.raises(ValueError, match="Cohort aggregation calculation"):
        join.validate_cohort_result(analysis["cases"], altered)
