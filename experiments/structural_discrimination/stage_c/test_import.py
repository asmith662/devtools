# Copyright (c) 2026
# ruff: noqa: S101, D103, PLR2004 -- primary authentication tests
"""Verify imported sole primaries and reject semantic/identity/hash tampering."""

from __future__ import annotations

import asyncio
import gzip
import json
from copy import deepcopy

import pytest

from experiments.structural_discrimination.stage_b.capture import CASES, case_root
from experiments.structural_discrimination.stage_c import import_gold as gold


@pytest.mark.parametrize("case", CASES)
def test_imported_primary_separate_process(case: str) -> None:
    result = asyncio.run(gold.authenticate(case, verify_builder=True))
    assert result["status"] == "PASS"
    assert result["blindness"]["second_reviewer_count"] == 0
    assert result["blindness"]["reconciliation_count"] == 0


@pytest.mark.parametrize(
    "defect",
    [
        "case",
        "frame",
        "obligation",
        "resource",
        "content",
        "label",
        "duplicate",
        "missing",
    ],
)
def test_gold_projection_rejects(defect: str) -> None:
    review = json.loads(
        (gold.primary_root("0017") / "stage_c_review.json").read_bytes(),
    )
    packet = json.loads(
        gzip.decompress(
            (case_root("0017") / "stage_c/packet/resources.json.gz").read_bytes(),
        ),
    )
    altered = deepcopy(review)
    cell = altered["cells"][0]
    if defect == "case":
        altered["case_id"] = "foreign"
    elif defect == "frame":
        altered["parent_frame"]["snapshot_id"] = "foreign"
    elif defect == "obligation":
        cell["obligation_identity"]["value"] = "foreign"
    elif defect == "resource":
        cell["address"] = "foreign"
    elif defect == "content":
        cell["content_identity"] = "foreign"
    elif defect == "label":
        cell["label"] = "UNKNOWN"
    elif defect == "duplicate":
        altered["cells"].append(deepcopy(cell))
    else:
        altered["cells"].pop()
    with pytest.raises(ValueError, match=r"identity|frame|cell|label"):
        gold.project("0017", altered, packet)


def test_primary_summaries_and_corrections() -> None:
    stats = {
        c: json.loads((gold.primary_root(c) / "stage_c_statistics.json").read_bytes())
        for c in CASES
    }
    assert stats["0017"]["semantic_unit_classes"] == {
        "TASK_BACKED": 10,
        "REPOSITORY_SUPPORTED": 4,
        "TASK_AND_REPOSITORY_SUPPORTED": 0,
    }
    assert stats["0017"]["witness_counts_by_obligation"] == {"O1": 2, "O2": 2, "O3": 2}
    assert stats["0017"]["sufficient_resource_union_count"] == 3
    assert len(stats["0017"]["inclusion_minimal_sufficient_resource_unions"]) == 2
    review = json.loads(
        (gold.primary_root("0017") / "stage_c_review.json").read_bytes(),
    )
    assert all(
        c["label"] == "HELPFUL_ONLY"
        for c in review["cells"]
        if c["resource_id"] in {"R092", "R268"} and c["obligation_id"] == "O2"
    )
    assert stats["0018"]["minimal_complete_witness_counts"] == {
        "O1": 16,
        "O2": 6,
        "O3": 12,
    }
    assert (
        stats["0018"]["task_combination_count"],
        stats["0018"]["distinct_sufficient_resource_union_count"],
        stats["0018"]["minimal_sufficient_resource_union_count"],
    ) == (1152, 182, 12)
    assert stats["0019"]["unit_class_counts"] == {
        "TASK_BACKED": 10,
        "REPOSITORY_SUPPORTED": 6,
        "TASK_AND_REPOSITORY_SUPPORTED": 0,
    }
    assert stats["0019"]["resource_count_range"] == [2, 2]
    unconditional = stats["0019"]["unconditional_future_task_satisfaction"]
    assert unconditional["complete_task_combination_count"] == 0
    assert unconditional["distinct_sufficient_resource_unions"] == []
    assert unconditional["resource_count_range"] is None
    assert unconditional["task_indispensable_resources"] is None


def test_import_overwrite_refused() -> None:
    with pytest.raises(ValueError, match="destination exists"):
        asyncio.run(gold.import_all())
