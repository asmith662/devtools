# Copyright (c) 2026
# ruff: noqa: D103, PLR2004
"""Completed development join retains exact candidate and judgment identities."""

from __future__ import annotations

from typing import Any, cast

from experiments.increment_27.depth_diagnostic import _read_json, sha256_file
from experiments.increment_27.structural_imports.mechanics import _digest
from experiments.increment_29.analysis import RESULT_NAME, ROOT, build_results
from experiments.increment_29.judgments import OUTPUT_NAME as JUDGMENTS_NAME
from experiments.increment_29.mechanics import CANDIDATES_NAME


def test_completed_join_covers_every_frozen_pair_without_relabeling() -> None:
    result = cast("dict[str, Any]", _read_json(ROOT / RESULT_NAME))
    assert result == build_results()
    assert result["content_identity"] == _digest(result["payload"])
    payload = result["payload"]
    assert payload["source_sha256"][CANDIDATES_NAME] == sha256_file(
        ROOT / CANDIDATES_NAME,
    )
    assert payload["source_sha256"][JUDGMENTS_NAME] == sha256_file(
        ROOT / JUDGMENTS_NAME,
    )
    assert len(payload["development_case_ids"]) == 24
    assert not payload["confirmation_executed"]
    assert not payload["candidate_mechanics_changed"]
    joined = payload["joined_pairs"]
    assert len(joined) == 71
    assert len({(row["case_id"], row["address"]) for row in joined}) == 71
    assert payload["surface_counts"]["union"] == {
        "candidate_pairs": 71,
        "USEFUL": 35,
        "NOT_USEFUL": 36,
        "UNJUDGED": 0,
        "judged_total": 71,
    }
    assert payload["surface_counts"]["exact_reuse"]["candidate_pairs"] == 52
    assert payload["surface_counts"]["new_blinded"]["candidate_pairs"] == 19
    assert payload["surface_counts"]["lexical_and_import_escape"] == {
        "candidate_pairs": 11,
        "USEFUL": 4,
        "NOT_USEFUL": 7,
        "UNJUDGED": 0,
        "judged_total": 11,
    }
    assert len(payload["useful_escape_pairs"]["lexical_and_import_escape"]) == 4
    assert payload["surface_counts"]["reference_without_call"]["candidate_pairs"] == 0
