# Copyright (c) 2026
# ruff: noqa: ANN401, S101, D103, PLR2004, E501, COM812 -- focused oracle tests; COM812 conflicts with formatter
"""POST_HOC / ORACLE / NON_GATING / NOT_RUNTIME_AVAILABLE validation on copies."""

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

from experiments.structural_discrimination.post_hoc.source_quality import (
    analysis,
    execute,
)
from experiments.structural_discrimination.stage_b import capture
from experiments.structural_discrimination.stage_d import analyze as published


@lru_cache
def fixture() -> tuple[Any, Any, Any, Any]:
    root = capture.case_root("0017")
    case = json.loads((root / "stage_d/analysis.json").read_bytes())
    trace = json.loads(
        gzip.decompress((capture.capture_root("0017") / "trace.json.gz").read_bytes())
    )
    gold = json.loads((root / "adjudication/reviewed/gold.json").read_bytes())
    design = json.loads((root / "protocol.json").read_bytes())
    return case, trace, gold, design


@lru_cache
def cohort_records() -> tuple[Any, Any, Any, Any]:
    cohort = json.loads((published.OUTPUT / "analysis.json").read_bytes())
    pairs, targets, unsupported = [], [], []
    for case in cohort["cases"]:
        root = capture.case_root(case["case"])
        trace = json.loads(
            gzip.decompress(
                (capture.capture_root(case["case"]) / "trace.json.gz").read_bytes()
            )
        )
        gold = json.loads((root / "adjudication/reviewed/gold.json").read_bytes())
        design = json.loads((root / "protocol.json").read_bytes())
        p, t, u = analysis.extract(case, trace, gold, design)
        pairs.extend(p)
        targets.extend(t)
        unsupported.extend(u)
    return pairs, targets, unsupported, cohort


@pytest.mark.parametrize(
    ("labels", "expected"),
    [
        (["REQUIRED"], "HAS_REQUIRED_SOURCE"),
        (["HELPFUL_ONLY"], "HAS_HELPFUL_SOURCE_NO_REQUIRED"),
        (["UNNECESSARY"], "ONLY_UNNECESSARY_SOURCES"),
        (["REQUIRED", "HELPFUL_ONLY", "UNNECESSARY"], "HAS_REQUIRED_SOURCE"),
        (["HELPFUL_ONLY", "UNNECESSARY"], "HAS_HELPFUL_SOURCE_NO_REQUIRED"),
    ],
)
def test_precedence(labels: list[str], expected: str) -> None:
    assert analysis.source_group(labels) == expected


@pytest.mark.parametrize("labels", [[], ["UNKNOWN"]])
def test_invalid_source_group(labels: list[str]) -> None:
    with pytest.raises(ValueError, match="source gold"):
        analysis.source_group(labels)


@pytest.mark.parametrize(
    "defect",
    [
        "missing-source-gold",
        "duplicate-source-gold",
        "missing-target-gold",
        "duplicate-target-gold",
        "foreign-frame",
        "wrong-obligation",
        "source-label",
        "target-label",
        "source-rank",
        "self-edge",
        "Reference",
        "occurrence-count",
        "source-content",
        "target-content",
        "predecessor",
        "classification",
        "missing-source",
        "duplicate-source",
    ],
)
def test_exact_joins_reject(defect: str) -> None:  # noqa: C901, PLR0912
    case, trace, gold, design = deepcopy(fixture())
    target = case["queries"][0]["targets"][0]
    source = target["sources"][0]
    address = (
        source["address"] if "source-gold" in defect else target["target"]["address"]
    )
    cell = next(
        c for c in gold["cells"] if c["obligation"] == "O1" and c["address"] == address
    )
    if defect.startswith("missing-") and defect.endswith("gold"):
        gold["cells"].remove(cell)
    elif defect.startswith("duplicate-") and defect.endswith("gold"):
        gold["cells"].append(deepcopy(cell))
    elif defect == "foreign-frame":
        target["frame"]["snapshot_id"] = "foreign"
    elif defect == "wrong-obligation":
        target["obligation_identity"]["value"] = "O4"
    elif defect == "source-label":
        source["source_gold_label"] = "REQUIRED"
    elif defect == "target-label":
        target["target_gold_label"] = "REQUIRED"
    elif defect == "source-rank":
        source["a_rank"] = target["target"]["a_rank"]
    elif defect == "self-edge":
        source["address"] = target["target"]["address"]
    elif defect == "Reference":
        source["supports"][0]["fact_identity"] = "foreign"
    elif defect == "occurrence-count":
        target["native_occurrence_count"] += 1
    elif defect == "source-content":
        source["content_identity"] = "foreign"
    elif defect == "target-content":
        target["target"]["content_identity"] = "foreign"
    elif defect == "predecessor":
        target["predecessor"]["a_rank"] -= 1
    elif defect == "classification":
        target["classification"] = "HARMFUL"
    elif defect == "missing-source":
        target["sources"].pop()
    else:
        target["sources"].append(deepcopy(source))
    with pytest.raises((ValueError, KeyError), match=r".+"):
        analysis.extract(case, trace, gold, design)


def test_cross_tabs_and_zero_denominators() -> None:
    pairs = [
        {
            "source_gold": "REQUIRED",
            "target_gold": "HELPFUL_ONLY",
            "occurrence_count": 3,
        },
        {
            "source_gold": "REQUIRED",
            "target_gold": "UNNECESSARY",
            "occurrence_count": 1,
        },
        {
            "source_gold": "UNNECESSARY",
            "target_gold": "HELPFUL_ONLY",
            "occurrence_count": 2,
        },
    ]
    primary = analysis.cross_tab(pairs)
    secondary = analysis.cross_tab(pairs, occurrence_weighted=True)
    assert primary["total"] == 3
    assert secondary["total"] == 6
    assert primary["row_percentages"]["REQUIRED"]["HELPFUL_ONLY"] == 50
    assert secondary["row_percentages"]["REQUIRED"]["HELPFUL_ONLY"] == 75
    assert primary["column_percentages"]["REQUIRED"]["HELPFUL_ONLY"] == 50
    assert secondary["column_percentages"]["REQUIRED"]["HELPFUL_ONLY"] == 60
    assert primary["row_percentages"]["HELPFUL_ONLY"]["UNNECESSARY"] is None
    assert primary["column_percentages"]["REQUIRED"]["REQUIRED"] is None
    assert primary["useful_source_collapse"]["USEFUL_SOURCE"] == {
        "USEFUL_TARGET": 1,
        "UNNECESSARY_TARGET": 1,
    }
    assert primary["collapsed_row_percentages"]["USEFUL_SOURCE"]["USEFUL_TARGET"] == 50
    assert (
        secondary["collapsed_column_percentages"]["USEFUL_SOURCE"]["USEFUL_TARGET"]
        == 60
    )
    assert (
        secondary["collapsed_column_percentages"]["UNNECESSARY_SOURCE"][
            "UNNECESSARY_TARGET"
        ]
        == 0
    )


def test_exact_completed_diagnostic() -> None:
    pairs, targets, unsupported, cohort = cohort_records()
    result = analysis.summarize(pairs, targets, unsupported, cohort)
    assert result["cohort"]["pair_weighted"]["counts"] == {
        "REQUIRED": {"REQUIRED": 6, "HELPFUL_ONLY": 3, "UNNECESSARY": 3},
        "HELPFUL_ONLY": {"REQUIRED": 1, "HELPFUL_ONLY": 11, "UNNECESSARY": 5},
        "UNNECESSARY": {"REQUIRED": 0, "HELPFUL_ONLY": 4, "UNNECESSARY": 185},
    }
    assert result["cohort"]["occurrence_weighted"]["counts"] == {
        "REQUIRED": {"REQUIRED": 81, "HELPFUL_ONLY": 12, "UNNECESSARY": 3},
        "HELPFUL_ONLY": {"REQUIRED": 12, "HELPFUL_ONLY": 55, "UNNECESSARY": 13},
        "UNNECESSARY": {"REQUIRED": 0, "HELPFUL_ONLY": 4, "UNNECESSARY": 1101},
    }
    assert (
        result["cohort"]["pair_weighted"]["collapsed_column_percentages"][
            "USEFUL_SOURCE"
        ]["USEFUL_TARGET"]
        == 84
    )
    assert (
        result["cohort"]["pair_weighted"]["collapsed_column_percentages"][
            "UNNECESSARY_SOURCE"
        ]["USEFUL_TARGET"]
        == 16
    )
    groups = result["cohort"]["target_source_quality"]
    assert [groups[g]["targets"] for g in analysis.GROUPS] == [9, 12, 100]
    assert [groups[g]["target_labels"]["REQUIRED"] for g in analysis.GROUPS] == [
        5,
        1,
        0,
    ]
    assert [groups[g]["target_labels"]["HELPFUL_ONLY"] for g in analysis.GROUPS] == [
        2,
        7,
        0,
    ]
    assert [groups[g]["target_labels"]["UNNECESSARY"] for g in analysis.GROUPS] == [
        2,
        4,
        100,
    ]
    assert [
        groups[g]["original_pair_outcomes"]["BENEFICIAL"] for g in analysis.GROUPS
    ] == [2, 5, 0]
    assert len(unsupported) == 33
    assert result["unchanged_published_categories"] == execute.EXPECTED_CATEGORIES
    assert result["unchanged_published_cohort_totals"] == cohort["cohort"]["totals"]
    strong = result["strong_beneficial_trace"]["every_supporting_source_pair"]
    assert len(strong) == 1
    assert (
        strong[0]["source"]["address"]
        == "tests/context/python/imports/test_resolution.py"
    )
    assert strong[0]["source"]["a_rank"] == 2
    assert strong[0]["source_gold"] == "REQUIRED"
    assert strong[0]["occurrence_count"] == 12
    assert len({f["target_declaration_identity"] for f in strong[0]["provenance"]}) == 1


@pytest.mark.parametrize(
    "defect", ["cross-tab", "row-percent", "column-percent", "outcomes", "group"]
)
def test_derived_mutations_rejected(defect: str) -> None:
    p, t, u, d = cohort_records()
    result = analysis.summarize(p, t, u, d)
    if defect == "cross-tab":
        result["cohort"]["pair_weighted"]["counts"]["REQUIRED"]["REQUIRED"] += 1
    elif defect == "row-percent":
        result["cohort"]["pair_weighted"]["row_percentages"]["REQUIRED"]["REQUIRED"] = (
            99
        )
    elif defect == "column-percent":
        result["cohort"]["pair_weighted"]["column_percentages"]["REQUIRED"][
            "REQUIRED"
        ] = 99
    elif defect == "outcomes":
        result["cohort"]["target_source_quality"][analysis.GROUPS[0]][
            "original_pair_outcomes"
        ]["BENEFICIAL"] += 1
    else:
        result["cohort"]["target_source_quality"][analysis.GROUPS[0]]["target_labels"][
            "REQUIRED"
        ] += 1
    with pytest.raises(ValueError, match="Incorrect cross-tab"):
        analysis.validate_summary(result, p, t, u, d)


@pytest.mark.parametrize(
    "defect",
    [
        "group",
        "occurrences",
        "self",
        "provenance",
        "duplicate-pair",
        "missing-pair",
        "duplicate-target",
        "outcome",
    ],
)
def test_record_mutations_rejected(defect: str) -> None:
    pairs, targets, _, _ = deepcopy(cohort_records())
    if defect == "group":
        targets[0]["source_group"] = "ONLY_UNNECESSARY_SOURCES"
    elif defect == "occurrences":
        pairs[0]["occurrence_count"] += 1
    elif defect == "self":
        pairs[0]["source"]["address"] = pairs[0]["target"]["address"]
    elif defect == "provenance":
        pairs[0]["provenance"][0]["source_snapshot_id"] = "foreign"
    elif defect == "duplicate-pair":
        pairs.append(deepcopy(pairs[0]))
    elif defect == "missing-pair":
        pairs.pop(0)
    elif defect == "duplicate-target":
        targets.append(deepcopy(targets[0]))
    else:
        pairs[0]["original_local_pair"] = {
            **pairs[0]["original_local_pair"],
            "classification": "HARMFUL",
        }
    with pytest.raises(ValueError, match=r".+"):
        analysis.validate_records(pairs, targets)


def test_output_integrity_and_overwrite(tmp_path: Path) -> None:
    files = {
        "integrity.json": b'{"status":"POST_HOC ORACLE NON_GATING NOT_RUNTIME_AVAILABLE"}\n'
    }
    execute.publish(tmp_path, files)
    execute.verify_bytes(tmp_path, files)
    with pytest.raises(ValueError, match="overwrite refused"):
        execute.publish(tmp_path, files)
    (tmp_path / "integrity.json").write_bytes(b"tampered")
    with pytest.raises(ValueError, match="output/integrity differs"):
        execute.verify_bytes(tmp_path, files)


def test_authenticated_repeat_has_no_acquisition(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    def forbidden(*_args: Any, **_kwargs: Any) -> Any:
        pytest.fail("Scientific acquisition forbidden in oracle diagnostic")

    for name in (
        "retrieve_repository_text_documents_by_bm25",
        "analyze_repository_text_lexical_query",
        "build_repository_text_lexical_inverted_index",
        "interpret_python_module_resources",
        "annotate",
    ):
        monkeypatch.setattr(capture, name, forbidden)
    first = asyncio.run(execute.artifacts())
    second = asyncio.run(execute.artifacts())
    assert first == second
