# Copyright (c) 2026
# ruff: noqa: COM812, D103, PLR2004
"""Exact joined development result for the completed containment baseline."""

from __future__ import annotations

from typing import Any, cast

from experiments.increment_27.depth_diagnostic import _read_json, sha256_file
from experiments.increment_27.structural_imports.mechanics import _digest
from experiments.increment_30.analysis import RESULT_NAME, ROOT, build_results
from experiments.increment_30.judgments import OUTPUT_NAME as JUDGMENTS_NAME
from experiments.increment_30.mechanics import CANDIDATES_NAME
from experiments.increment_30.population import BLINDED_NAME, JUDGMENT_FREEZE_NAME


def test_completed_result_is_exact_and_preserves_frozen_mechanics() -> None:
    saved = cast("dict[str, Any]", _read_json(ROOT / RESULT_NAME))
    rebuilt = build_results(ROOT)
    assert saved == rebuilt
    assert saved["content_identity"] == _digest(saved["payload"])
    payload = saved["payload"]
    candidates = cast("dict[str, Any]", _read_json(ROOT / CANDIDATES_NAME))
    population = cast("dict[str, Any]", _read_json(ROOT / JUDGMENT_FREEZE_NAME))[
        "payload"
    ]
    judgments = cast("dict[str, Any]", _read_json(ROOT / JUDGMENTS_NAME))["payload"]
    assert (
        payload["source_content_identities"][CANDIDATES_NAME]
        == candidates["content_identity"]
    )
    assert payload["source_sha256"][CANDIDATES_NAME] == sha256_file(
        ROOT / CANDIDATES_NAME
    )
    assert judgments["blinded_input_sha256"] == sha256_file(ROOT / BLINDED_NAME)
    assert population["candidate_identity"] == candidates["content_identity"]
    assert population["candidate_sha256"] == sha256_file(ROOT / CANDIDATES_NAME)
    assert candidates["judgments_loaded"] is False
    assert payload["candidate_mechanics_changed"] is False
    assert payload["confirmation_executed"] is False
    assert len(payload["development_case_ids"]) == 24
    assert len(payload["joined_pairs"]) == 49
    assert (
        len(
            {
                (row["case_id"], row["parent_snapshot_sha"], row["address"])
                for row in payload["joined_pairs"]
            }
        )
        == 49
    )
    surfaces = payload["surface_counts"]
    assert surfaces["union"] == {
        "candidate_pairs": 49,
        "USEFUL": 14,
        "NOT_USEFUL": 35,
        "UNJUDGED": 0,
        "judged_total": 49,
    }
    assert surfaces["exact_reuse"]["USEFUL"] == 14
    assert surfaces["exact_reuse"]["NOT_USEFUL"] == 15
    assert surfaces["new_blinded"]["NOT_USEFUL"] == 20
    assert surfaces["child_to_package"]["candidate_pairs"] == 49
    assert surfaces["package_to_child"]["candidate_pairs"] == 0
    assert surfaces["all_saved_lexical_escape"]["USEFUL"] == 1
    assert surfaces["import_escape"]["USEFUL"] == 0
    assert surfaces["references_calls_escape"]["USEFUL"] == 14
    assert surfaces["complete_existing_evidence_escape"] == {
        "candidate_pairs": 12,
        "USEFUL": 0,
        "NOT_USEFUL": 12,
        "UNJUDGED": 0,
        "judged_total": 12,
    }
    assert payload["useful_escape_pairs"]["complete_existing_evidence_escape"] == []
