# Copyright (c) 2026
# ruff: noqa: COM812, E501 -- bounded experimental diagnostic records
"""Conservative failure assertions separated from mechanically observed factors."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from experiments.retrieval_diagnostics.models import DiagnosticPolicy


def classify(record: dict[str, Any], policy: DiagnosticPolicy) -> dict[str, Any]:
    """Establish ranking burden only with independent REQUIRED judgments."""
    required = (
        record["judgment"] is not None and record["judgment"]["label"] == "REQUIRED"
    )
    unnecessary = record["ranking"]["ahead_labels"].get("UNNECESSARY", 0)
    verified = (
        required
        and record["status"] == "REACHED"
        and unnecessary >= policy.substantial_unnecessary_ahead
    )
    contributors = []
    if unnecessary:
        contributors.append(
            {
                "code": "UNNECESSARY_OVERTAKERS",
                "count": unnecessary,
                "threshold": policy.substantial_unnecessary_ahead,
            }
        )
    common = sorted(
        {
            t["term"]
            for t in record["terms"]
            if t["df"] / t["corpus_size"] >= policy.common_fraction
            and t["idf"] <= policy.low_idf
        }
    )
    if common:
        contributors.append(
            {
                "code": "COMMON_QUERY_TERM",
                "terms": common,
                "meaning": "Descriptive footprint, not badness or a weighting recommendation.",
            }
        )
    if any(t["normalized_length_factor"] != 1 for t in record["terms"]):
        contributors.append(
            {
                "code": "LENGTH_NORMALIZATION",
                "meaning": "Observable saturation component, not an independently isolated rank cause.",
            }
        )
    structural = [s for s in record["support_references"] if s["kind"] == "STRUCTURAL"]
    findings = [
        {
            "classification": "RANKING_DISCRIMINATION_FAILURE",
            "diagnostic": "VERIFIED_RANKING_DISCRIMINATION_FAILURE"
            if verified
            else "NOT_ESTABLISHED",
            "certainty": "DETERMINISTICALLY_ESTABLISHED"
            if verified
            else "INSUFFICIENT_EVIDENCE",
            "evidence": {
                "required": required,
                "positive_rank": record["rank"],
                "unnecessary_ahead": unnecessary,
                "threshold": policy.substantial_unnecessary_ahead,
            },
        },
        {
            "classification": "REPRESENTATION_FAILURE",
            "diagnostic": "COMPARISON_REQUIRED",
            "certainty": "INSUFFICIENT_EVIDENCE",
        },
        {
            "classification": "VOCABULARY_SEMANTIC_MISMATCH",
            "diagnostic": "AVAILABLE_REPRESENTATIONS_NOT_COMPARED",
            "certainty": "INSUFFICIENT_EVIDENCE",
        },
        {
            "classification": "RELATIONAL_RELEVANCE",
            "diagnostic": "RELATIONAL_SUPPORT_PRESENT"
            if structural
            else "NOT_ASSESSED",
            "certainty": "STRONGLY_EVIDENCED" if structural else "NOT_ASSESSED",
            "limit": "Support presence does not establish why independent gold requires this resource.",
        },
        *[
            {
                "classification": name,
                "diagnostic": "NOT_ASSESSED",
                "certainty": "OUTSIDE_DIAGNOSTIC_SCOPE",
            }
            for name in (
                "CONTEXT_DISCLOSURE_FAILURE",
                "INFORMATION_NEED_OBLIGATION_FAILURE",
            )
        ],
    ]
    return {
        "primary": "RANKING_DISCRIMINATION_FAILURE" if verified else None,
        "findings": findings,
        "contributors": contributors,
        "scope": "One explicit judged subject and descriptive threshold; no global ranker defect claim.",
    }
