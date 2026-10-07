# Copyright (c) 2026
# ruff: noqa: COM812, E501, ISC004 -- deterministic unjudged review
"""Show treatment behavior to humans without interpreting relevance or success."""

from __future__ import annotations

from typing import Any


def stage_b(
    t: dict[str, Any],
    result: dict[str, Any],
    trace: dict[str, Any],
    cost: dict[str, Any],
) -> str:
    """Display every literal query, need, top rows, term footprint and timing."""
    lines = [
        "# Case 0011 Stage B review — NOT GOLD",
        "",
        "Effectiveness UNKNOWN. Human inspection is not Stage C adjudication. Maintainer comments/labels belong in separate MANUAL_AUDIT. "
        "All routes are CANONICAL_RESOURCE_BM25 with k1=1.2, b=0.75, filename weight=0.25; no routing, fusion or reformulation.",
        "",
        "[Stage A review](STAGE_A_REVIEW.md) preserves the full prompt, all interpretations, exact queries, analyzed terms and hints. "
        "The complete positive rows and term contributions are hash-bound in results.json.gz and trace.json. Top five here are an inspection window, not a retrieval limit.",
        "",
        "## Unjudged result counts and duplicates",
        "",
        "| Arm | Queries | Positive occurrences | Unique union | Duplicate occurrences |",
        "|---|---:|---:|---:|---:|",
    ]
    for arm, row in trace["overlap"]["arms"].items():
        lines.append(
            f"| {arm} | {row['query_count']} | {row['positive_occurrences']} | {row['unique_union']} | {row['duplicate_occurrences']} |"
        )
    lines += [
        "",
        "Duplicate occurrences = returned occurrences minus distinct union, not a relevance judgment. Every query pair's intersection/only counts are retained in trace.json.",
        "",
    ]
    needs = {n["identity"]: n for n in t["information_needs"]}
    for q in t["queries"]:
        capture = result["queries"][q["identity"]]
        lines += [
            f"## {q['identity']} — Arm {q['arm']}",
            "",
            f"Obligation: {q['obligation']}. Need: {q['information_need']}.",
        ]
        if q["information_need"]:
            lines += ["", "Exact need: " + needs[q["information_need"]]["statement"]]
        lines += [
            "",
            "Exact query:",
            "",
            "```text",
            q["text"].removesuffix("\n"),
            "```",
            "",
            "Native analyzer terms: `" + ", ".join(q["analyzed_terms"]) + "`.",
            "",
            f"Route: {q['route']}. Execution count: {capture['execution_count']}. Positive resources: {len(capture['rows'])}. Query seconds: {cost['query_seconds'][q['identity']]:.9f}.",
            "",
            "| Rank | Resource | Score | Content | Filename (raw) | Filename (weighted) |",
            "|---:|---|---:|---:|---:|---:|",
        ]
        for row in capture["rows"][:5]:
            lines.append(
                f"| {row['rank']} | `{row['address']}` | {row['score']:.9f} | {row['content_score']:.9f} | {row['filename_score']:.9f} | {row['weighted_filename_score']:.9f} |"
            )
        lines += [
            "",
            "| Term | Content DF | IDF | Content fraction | Effective matching resources | REQUIRED / HELPFUL / UNNECESSARY yield |",
            "|---|---:|---:|---:|---:|---|",
        ]
        for profile in capture["query_profile"]:
            field = next(f for f in profile["fields"] if f["field"] == "content")
            lines.append(
                f"| {profile['term']} | {field['df']} | {field['idf']:.9f} | {field['fraction_of_frame']:.6f} | {len(profile['effective_matching_resources'])} | UNKNOWN / UNKNOWN / UNKNOWN |"
            )
        high = sorted(
            capture["query_profile"],
            key=lambda p: (-len(p["effective_matching_resources"]), p["term"]),
        )[:3]
        lines += [
            "",
            "High-footprint terms (descriptive only): "
            + ", ".join(p["term"] for p in high)
            + ". No MIXED_INTENT or relevance failure is asserted before gold.",
            "",
        ]
    lines += ["## Exact hints remain lexical-only", ""]
    for hint in t["hints"]:
        usage = [q["identity"] for q in t["queries"] if hint["hint"] in q["text"]]
        lines.append(
            f"- `{hint['hint']}`: {hint['locations']}; NOT_ROUTED_IN_U1; literal query usage: {usage}."
        )
    lines += [
        "",
        "## Cost scope",
        "",
        f"Shared content index construction: {cost['shared_content_index_seconds']:.9f} seconds. Total {cost['query_count']} queries: {cost['sum_query_seconds']:.9f} seconds. "
        "These are one-run descriptive observations, not latency benchmarks. Native per-query filename index construction is included; R1.5 projection/verification is separate.",
        "",
        "STOP BEFORE GOLD. Next: fresh independent Stage C with only task/obligation/resource packet; then separate blind C.5 with needs and clean gold but no queries/results; then Stage D.",
        "",
    ]
    return "\n".join(lines)
