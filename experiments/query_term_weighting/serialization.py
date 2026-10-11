# Copyright (c) 2026
"""Deterministic lossless native/weighted contribution trace projection."""

from __future__ import annotations

import json
from dataclasses import asdict
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from experiments.query_term_weighting.scoring import WeightedResult


def trace(result: WeightedResult) -> dict[str, Any]:
    """Expose original contribution evidence, weighted channels and role totals."""
    result.validate()
    rows = []
    for rank, match in enumerate(result.matches, 1):
        native = match.native_match
        resource = native.document_statistics.analysis.document.resource
        totals: dict[str, float] = {}
        for value in match.contributions:
            totals[value.role.value] = (
                totals.get(value.role.value, 0.0)
                + value.weighted * value.channel_weight
            )
        rows.append(
            {
                "rank": rank,
                "collection_position": match.collection_position,
                "repository_id": str(
                    native.document_statistics.analysis.document.repository_id,
                ),
                "corpus_id": str(
                    result.native_result.index.corpus_statistics.collection_analysis.document_collection.corpus.id,
                ),
                "document_id": str(native.document_statistics.analysis.document.id),
                "address": str(resource.address),
                "content_identity": str(resource.content_identity),
                "native_score": native.score,
                "native_score_hex": native.score.hex(),
                "weighted_score": match.score,
                "weighted_score_hex": match.score.hex(),
                "native_content_evidence": [
                    asdict(t) for t in native.term_contributions
                ],
                "native_filename_evidence": [
                    asdict(t) for t in native.filename_term_contributions
                ],
                "contributions": [
                    {
                        **asdict(v),
                        "native_hex": v.native.hex(),
                        "weighted_hex": v.weighted.hex(),
                    }
                    for v in match.contributions
                ],
                "role_totals": totals,
                "role_score_shares": {
                    role: value / match.score for role, value in totals.items()
                },
            },
        )
    return {
        "arm": result.arm.value,
        "query_policy": json.loads(json.dumps(asdict(result.policy))),
        "filename_weight": 0.25,
        "matches": rows,
    }
