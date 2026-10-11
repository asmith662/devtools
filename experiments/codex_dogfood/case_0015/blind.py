# Copyright (c) 2026
# ruff: noqa: COM812, EM101, TRY003 -- explicit future blind projection
"""Allowlisted future gold interface; no adjudication or packet publication now."""

from __future__ import annotations

from typing import Any

from experiments.codex_dogfood.case_0009.artifacts import json_bytes
from experiments.codex_dogfood.case_0015 import protocol


def packet(design: dict[str, Any], resources: list[dict[str, Any]]) -> dict[str, Any]:
    """Exclude experimental metadata by construction while preserving natural text."""
    # JSON round trips turn tuples to lists; compare the deterministic bytes.
    if json_bytes(design) != json_bytes(protocol.authored()):
        raise ValueError("Not exact frozen design")
    identities = [
        (
            r["repository_id"],
            r["snapshot_id"],
            r["corpus_id"],
            r["address"],
            r["content_identity"],
            r["document_identity"],
        )
        for r in resources
    ]
    if len(set(identities)) != len(identities) or len(
        {r["address"] for r in resources}
    ) != len(resources):
        raise ValueError("Duplicate/ambiguous resources")
    keys = (
        "repository_id",
        "snapshot_id",
        "corpus_id",
        "address",
        "content_identity",
        "document_identity",
        "content",
        "encoding",
        "utf8_bytes",
    )
    return {
        "case": design["case"],
        "task_identity": design["task_identity"],
        "task_text": design["task_text"],
        "obligations": [
            {
                k: row[k]
                for k in (
                    "identity",
                    "title",
                    "mandatory",
                    "applicability",
                    "task_span",
                    "task_clause",
                    "satisfaction",
                )
            }
            for row in design["requirement_matrix"]
        ],
        "eligible_resources": [{k: r[k] for k in keys} for r in resources],
    }
