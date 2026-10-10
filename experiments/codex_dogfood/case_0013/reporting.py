# Copyright (c) 2026
# ruff: noqa: COM812, E501 -- formatter owns commas; complete prospective prose
"""Reconstruct human review directly from frozen prospective values."""

from __future__ import annotations

import json
from typing import Any


def matrix(t: dict[str, Any]) -> str:
    """Expose every exact clause and its complete obligation/exclusion mapping."""
    lines = ["# Case 0013 task requirement matrix", ""]
    for row in t["task_requirement_matrix"]:
        lines += [
            "## " + row["requirement"],
            "",
            row["basis"]["text"].strip(),
            "",
            "Obligations: " + (", ".join(row["obligations"]) or "NONE"),
            "",
            "Exclusion: " + (row["exclusion"] or "NONE"),
            "",
        ]
    return "\n".join(lines)


def review(t: dict[str, Any], frame: dict[str, Any]) -> str:
    """Render a self-contained treatment-aware Stage A manual challenge surface."""
    lines = [
        "# Case 0013 — U3 Stage A review",
        "",
        "**FROZEN PROSPECTIVE DESIGN; no treatment execution or gold.**",
        "",
        "Hypothesis: task-only mechanism permission preserves useful exact-first witness gains while reducing unnecessary invocations/cost. U2 is development evidence only; this is a new task, not reused evaluation.",
        "",
        "## Exact future task",
        "",
        "```text",
        t["task_text"].rstrip(),
        "```",
        "",
        matrix(t),
        "## Obligations and lexical queries",
        "",
        "| Obligation | Satisfaction criterion | Exact query |",
        "| --- | --- | --- |",
    ]
    lines += [
        f"| {o['key']} | {o['criterion']} | {o['query']} |" for o in t["obligations"]
    ]
    lines += [
        "",
        "## Hints, roles, native inputs and route decisions",
        "",
        "B admits all ten explicit hints; C selects the six existing-evidence hints. Four new-destination hints retain full lexical coverage. These are requests, not claims that a native target exists or is relevant.",
        "",
        "| Hint | Literal | Family | Obligation | Role | B | C |",
        "| --- | --- | --- | --- | --- | --- | --- |",
    ]
    for index, h in enumerate(t["hint_inventory"]):
        b, c = (t["route_decisions"][a][index] for a in ("B", "C"))
        lines.append(
            f"| {h['key']} | `{h['text']}` | {h['category']} | {b['basis']['need']['obligation']['value']} | {t['acquisition_intents'][index]['role']} | {b['disposition']} | {c['disposition']} |"
        )
    lines += [
        "",
        "## Router contract",
        "",
        t["router_rules"],
        "",
        "Caller role grammar: Inspect existing / Introduce new / Understand. Unknown grammar is an authoring error. Every obligation also has a conceptual purpose. These purposes do not replace complete obligation query coverage. No rank, score, resolution, gold or repository content is accepted by the policy API.",
        "",
        "## Frozen arms, settings and safety lane",
        "",
        "```json",
        json.dumps(
            {
                "arms": t["arms"],
                "settings": t["settings"],
                "global_safety_query": t["global_safety_query"],
            },
            indent=2,
        ),
        "```",
        "",
        "## Frame preparation",
        "",
        f"Source HEAD: `{frame['source_head']}`; resources: {frame['resource_count']}; RepositoryId: `{frame['repository_id']}`; SnapshotId: `{frame['snapshot_id']}`; CorpusId: `{frame['corpus_id']}`; exact frame: `{frame['frame_identity']}`.",
        "",
        f"Module universe: `{frame['module_universe_identity']}` ({frame['module_count']} address-only interpretations). Native resource/content/document/module identities and the complete Python declaration resource universe are in frame.json; retained contents in inputs.json.gz/resources.json.gz. No declaration analysis, exact lookup, index build or retrieval has occurred. Source frame excludes all experiment/operational/confirmation/reserve data.",
        "",
        "## Prospective metrics",
        "",
        "\n".join("- " + m for m in t["metrics"]),
        "",
        "All gold-dependent metrics are unavailable until a separately authorized blind adjudication.",
        "",
        "## Cost plan",
        "",
    ]
    for key, value in t["cost_accounting"].items():
        lines += ["### " + key, "", value, ""]
    lines += ["## Frozen decision rule", ""]
    for key, value in t["decision_rule"].items():
        lines += ["### " + key, "", value, ""]
    lines += [
        "## Failure taxonomy",
        "",
        "\n".join("- " + m for m in t["failure_taxonomy"]),
        "",
        "SEARCH_POLICY_FAILURE = NOT_ASSESSED.",
        "",
        "## Future blind gold",
        "",
        "```json",
        json.dumps(t["future_gold"], indent=2),
        "```",
        "",
        "## Exact execution counters and exclusions",
        "",
        "```json",
        json.dumps(
            {
                "execution": t["execution"],
                "stage_b": t["stage_b"],
                "gold": t["gold"],
                "excluded": t["excluded"],
            },
            indent=2,
        ),
        "```",
        "",
        "## Complete task-only intent and locator trace",
        "",
        "This appendix includes every native task/obligation/query identity, exact span, purpose, role, association, locator and per-arm deterministic decision identity. The complete machine trace is trace.json. It contains no acquisition outcome.",
        "",
        "```json",
        json.dumps(
            {
                k: t[k]
                for k in (
                    "native_task_interpretation",
                    "native_obligation_queries",
                    "hint_inventory",
                    "hint_associations",
                    "acquisition_intents",
                    "route_decisions",
                    "extraction_decisions",
                )
            },
            indent=2,
        ),
        "```",
        "",
        "Next: maintainer reviews this Stage A. Only after authorization execute frozen A/B/C once. No Stage B, feature implementation, productionization, R1.7 or BM25F is authorized by this freeze.",
        "",
    ]
    return "\n".join(lines)
