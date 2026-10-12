# Copyright (c) 2026
# ruff: noqa: D103, S101, TC003, EM101, TRY003, COM812
"""Controlled leakage/overwrite tests; no real packet before Stage B checkpoint."""

from __future__ import annotations

import asyncio
import copy
from pathlib import Path

import pytest

from experiments.codex_dogfood.case_0016.blind import project
from experiments.codex_dogfood.case_0016.stage_c import packet, validate_packet


@pytest.mark.parametrize("key", sorted(validate_packet.FORBIDDEN))
def test_deep_metadata_leakage_rejected(key: str) -> None:
    with pytest.raises(ValueError, match="metadata leakage"):
        validate_packet.tripwire({"wrapper": [{key: "TREATMENT_SENTINEL"}]})


@pytest.mark.parametrize(
    "value", ["pagerank", "PPR", "RRF", "query", "rank", "stage_b"]
)
def test_deep_value_leakage_rejected(value: str) -> None:
    with pytest.raises(ValueError, match="value leakage"):
        validate_packet.tripwire({"wrapper": [{"unexpected": value}]})


def test_natural_text_not_censored_and_allowlist_projection() -> None:
    text = "query rank graph pagerank RRF seeds are natural source identifiers"
    design = {
        "case": "0016",
        "task_identity": "synthetic",
        "task_text": text,
        "requirement_matrix": [
            {
                "obligation": "O1",
                "mandatory": True,
                "task_clause": text,
                "satisfaction_criteria": text,
                "query": "TREATMENT_SENTINEL",
                "query_id": "Q1",
            }
        ],
    }
    row = dict.fromkeys(validate_packet.RESOURCE, "synthetic")
    row["content"] = text
    row["address"] = "synthetic.py"
    row["seeds"] = "TREATMENT_SENTINEL"
    value = project(design, [row])
    assert value["task"] == text
    assert "TREATMENT_SENTINEL" not in str(value)
    validate_packet.tripwire(value)
    bad = copy.deepcopy(value)
    bad["obligations"][0]["seeds"] = []
    with pytest.raises(ValueError, match="metadata leakage"):
        validate_packet.tripwire(bad)


def test_packet_build_overwrite_refusal_before_capture_access(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    async def forbidden() -> None:
        raise AssertionError("Existing packet must refuse before capture access")

    monkeypatch.setattr(packet, "authenticate", forbidden)
    with pytest.raises(FileExistsError, match="overwrite"):
        asyncio.run(packet.build(tmp_path))
    with pytest.raises(FileExistsError, match="overwrite"):
        packet.publish(tmp_path, {})


def test_whitelist_extra_directory_rejected(tmp_path: Path) -> None:
    (tmp_path / "extra").mkdir()
    with pytest.raises(ValueError, match="five-file whitelist"):
        validate_packet.validate(tmp_path)
