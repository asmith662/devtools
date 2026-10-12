# Copyright (c) 2026
"""Allowlisted future blind input projection; no packet or gold published yet."""

from typing import Any


def project(design: dict[str, Any], resources: list[dict[str, Any]]) -> dict[str, Any]:
    """Keep natural task/content but exclude all treatment-origin metadata."""
    return {
        "case": design["case"],
        "task_identity": design["task_identity"],
        "task": design["task_text"],
        "obligations": [
            {
                key: row[key]
                for key in (
                    "obligation",
                    "mandatory",
                    "task_clause",
                    "satisfaction_criteria",
                )
            }
            for row in design["requirement_matrix"]
        ],
        "resources": [
            {
                key: row[key]
                for key in (
                    "repository_id",
                    "snapshot_id",
                    "corpus_id",
                    "address",
                    "document_identity",
                    "content_identity",
                    "content",
                )
            }
            for row in resources
        ],
    }
