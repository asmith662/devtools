# Copyright (c) 2026
# ruff: noqa: EM101, TRY003 -- explicit blind projection errors
"""Allowlisted future blind packet projection, without producing adjudication."""

from __future__ import annotations

from typing import Any

from experiments.codex_dogfood.case_0009.artifacts import json_bytes, read_json
from experiments.codex_dogfood.case_0014 import protocol


def packet(design: dict[str, Any], resources: list[dict[str, Any]]) -> dict[str, Any]:
    """Project only original task, mandatory obligations and eligible resources."""
    authored_design = {k: v for k, v in design.items() if k != "frame_policy"}
    if json_bytes(authored_design) != json_bytes(protocol.authored()) or (
        "frame_policy" in design
        and json_bytes(design) != json_bytes(read_json(protocol.CASE / "protocol.json"))
    ):
        raise ValueError("Blind projection requires exact frozen authored protocol")
    identities = [r["address"] for r in resources]
    if len(identities) != len(set(identities)):
        raise ValueError("Duplicate blind resource identity")
    result = {
        "case": design["case"],
        "task_identity": design["task_identity"],
        "task_text": design["task_text"],
        "obligations": [
            {
                "identity": r["obligation"],
                "mandatory": r["mandatory"],
                "source_task_clause": r["source_task_clause"],
            }
            for r in design["requirement_matrix"]
        ],
        "eligible_resources": [
            {
                k: r[k]
                for k in (
                    "repository_id",
                    "snapshot_id",
                    "corpus_id",
                    "document_identity",
                    "address",
                    "content_identity",
                    "encoding",
                    "utf8_bytes",
                    "content",
                )
            }
            for r in resources
        ],
    }
    if tuple(result) != tuple(protocol.GOLD_POLICY["allowed"]):
        raise ValueError("Blind packet whitelist differs")
    return result
