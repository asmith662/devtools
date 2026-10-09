# Copyright (c) 2026
# ruff: noqa: COM812 -- literal protocol prose or fixture assertions; formatter owns commas
"""Future packet projection contract; Stage A tests fixtures, publishes no packet."""

from __future__ import annotations

from typing import Any


def packet_projection(
    treatment: dict[str, Any], resources: list[dict[str, Any]]
) -> dict[str, Any]:
    """Allowlist task/obligation/content fields, excluding all routing metadata."""
    fields = (
        "identity",
        "key",
        "statement",
        "criterion",
        "applicability",
        "task_basis",
    )
    return {
        "case": "case-0012",
        "task_identity": treatment["task_identity"],
        "task_text": treatment["task_text"],
        "obligations": [{k: o[k] for k in fields} for o in treatment["obligations"]],
        "resources": [
            {
                k: r[k]
                for k in (
                    "address",
                    "content_identity",
                    "text",
                    "encoding",
                    "byte_size",
                )
            }
            for r in resources
        ],
    }
