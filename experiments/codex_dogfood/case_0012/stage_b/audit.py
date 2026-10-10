# Copyright (c) 2026
# ruff: noqa: ANN401, COM812, EM101, TRY003, S301 -- own authenticated historical pickle
"""Audit-only failed-attempt authentication and deterministic overlap comparison."""

from __future__ import annotations

import base64
import gzip
import pickle
from dataclasses import fields
from pathlib import Path
from typing import Any, cast

from experiments.codex_dogfood.case_0009.artifacts import (
    binary,
    digest,
    json_bytes,
    read_json,
)
from experiments.codex_dogfood.case_0012.stage_b.graph import describe
from experiments.codex_dogfood.case_0012.stage_b.reporting import lexical_rows

ATTEMPT_ONE = Path(__file__).resolve().parent / "attempts/case-0012-stage-b-1"
ORIGINAL = "original/experiments/codex_dogfood/case_0012/stage_b/"


def authenticate() -> dict[str, Any]:
    """Load failed state only for audit; it can never initialize a new attempt."""
    seal = read_json(ATTEMPT_ONE / "integrity.json")
    for name, sha in seal["sha256"].items():
        if digest(binary(ATTEMPT_ONE / name)) != sha:
            raise ValueError("Attempt-1 audit digest differs")
    envelope = read_json(ATTEMPT_ONE / (ORIGINAL + "raw_checkpoint.json"))
    raw = base64.b85decode(envelope["native_gzip_b85"])
    if digest(raw) != envelope["native_archive_sha256"]:
        raise ValueError("Attempt-1 native archive differs")
    state = pickle.loads(gzip.decompress(raw))
    account = read_json(ATTEMPT_ONE / "audit.json")
    if (
        state["marker"]
        != read_json(ATTEMPT_ONE / (ORIGINAL + "execution_started.json"))
        or state["operations"] != account["operation_history"]
        or state["marker"]["execution"] != "case-0012-stage-b-1"
        or account["authoritative_use"] != "AUDIT_ONLY"
        or account["scientific_disposition"] != "ABORTED_CAPTURE_INFRASTRUCTURE_FAILURE"
        or "lexical:materialization" in state["values"]
    ):
        raise ValueError("Attempt-1 aborted boundary differs")
    return cast("dict[str, Any]", state)


def lexical_identity(lane: Any) -> dict[str, Any]:
    """Compare all deterministic native evidence; runtime is deliberately excluded."""
    other = {
        f.name: getattr(lane, f.name)
        for f in fields(lane)
        if f.name not in {"index", "matches"}
    }
    return {
        "native_type": type(lane).__module__ + "." + type(lane).__qualname__,
        "query_and_settings": describe(other),
        "rows": lexical_rows(lane),
    }


def overlap(state: dict[str, Any]) -> dict[str, Any]:
    """Read attempt 1 only after the new self-contained capture has completed."""
    if state["marker"]["execution"] != "case-0012-stage-b-2" or state["active"]:
        raise ValueError("Only complete independent attempt 2 may compare overlap")
    old = authenticate()
    if digest(json_bytes(describe(old["values"]["index-build"]))) != digest(
        json_bytes(describe(state["values"]["index-build"]))
    ):
        raise ValueError("Cross-attempt native index/settings differ")
    comparisons = {}
    for key in ("global", "source", "choices", "integrity"):
        first, second = (
            lexical_identity(s["values"]["lexical:" + key]) for s in (old, state)
        )
        if first != second:
            raise ValueError(
                "Cross-attempt deterministic lexical result differs: " + key
            )
        comparisons[key] = {
            "status": "PASS",
            "canonical_result_sha256": digest(json_bytes(first)),
            "positive_rows": len(second["rows"]),
        }
    return {
        "status": "ATTEMPT_1_VS_2_DETERMINISTIC_OVERLAP_PASS",
        "use": "CONSISTENCY_ONLY; NO_SPLICING; NO_GOLD_OR_EFFECTIVENESS_CREDIT",
        "queries": comparisons,
        "historical_counts": {
            "index_builds_entered": 2,
            "index_builds_returned": 2,
            "lexical_queries_entered": 15,
            "lexical_queries_actually_returned": 15,
            "lexical_queries_durable": 14,
            "admitted_exact_routes": 16,
            "grounding_subcalls": sum(
                o["identity"].startswith("ground:") for o in state["operations"]
            ),
            "presentation_calls": 18,
            "arm_assemblies": 3,
        },
    }
