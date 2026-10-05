# ruff: noqa: INP001, CPY001, PLR2004, COM812, S101, D103, I001, PT018
"""Focused integrity and deterministic-freeze tests for Stage D."""

import hashlib
import json

import pytest

import analyze


def test_joined_analysis_covers_frozen_gold_and_structural_surfaces() -> None:
    result = analyze.analyze()
    assert result["integrity"]["resources"] == 523
    assert result["integrity"]["obligations"] == 13
    assert result["integrity"]["judgment_cells"] == 6799
    assert result["gold"]["alternative_count"] == 15
    assert result["gold"]["combination_count"] == 4
    assert (result["gold"]["minimum_union"], result["gold"]["maximum_union"]) == (
        21,
        22,
    )
    assert result["surface_sizes"]["ALL FOUR"] == 19
    assert result["marginals"]["reference_over_owner_mirror"]["new_required_cells"] == 0
    assert result["decision"] == "MOVE_TO_EVIDENCE_RESOLUTION"


def test_analysis_serialization_replays_exactly() -> None:
    first = analyze.analyze()
    second = analyze.analyze()
    assert json.dumps(
        first, sort_keys=True, indent=2, ensure_ascii=False
    ) == json.dumps(second, sort_keys=True, indent=2, ensure_ascii=False)


def test_freeze_refuses_overwrite_and_replay_matches_frozen_files() -> None:
    json_path = analyze.ROOT / "analysis.json"
    markdown_path = analyze.ROOT / "analysis.md"
    assert json_path.exists() and markdown_path.exists()
    before = (
        hashlib.sha256(json_path.read_bytes()).hexdigest(),
        hashlib.sha256(markdown_path.read_bytes()).hexdigest(),
    )
    with pytest.raises(FileExistsError):
        analyze.freeze()
    result = analyze.analyze()
    expected_json = (
        json.dumps(result, sort_keys=True, indent=2, ensure_ascii=False) + "\n"
    )
    expected_markdown = analyze.render(result)
    assert json_path.read_text(encoding="utf-8") == expected_json
    assert markdown_path.read_text(encoding="utf-8") == expected_markdown
    after = (
        hashlib.sha256(json_path.read_bytes()).hexdigest(),
        hashlib.sha256(markdown_path.read_bytes()).hexdigest(),
    )
    assert before == after
