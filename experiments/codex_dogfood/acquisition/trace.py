# Copyright (c) 2026
# ruff: noqa: COM812, C901, E501, PLR0912, EM101, TRY003 -- bounded human-readable experimental projections
"""Validate and display literal acquisition provenance; no semantic generation."""

from __future__ import annotations

from typing import Any

from devtools.context.retrieval.lexical.bm25 import (
    analyze_repository_text_lexical_query,
)
from experiments.codex_dogfood.case_0009.artifacts import digest

STAGES = (
    "TASK",
    "OBLIGATION",
    "INFORMATION_NEED",
    "QUERY",
    "ROUTE",
    "RESULT",
    "JUDGMENT",
    "FAILURE",
    "NEXT_ACTION",
)


def validate(t: dict[str, Any]) -> None:
    """Require exact links, literal terms, controlled routes and unique identities."""
    obligations = {o["identity"]: o for o in t["obligations"]}
    needs = {n["identity"]: n for n in t["information_needs"]}
    queries = {q["identity"]: q for q in t["queries"]}
    if (
        len(obligations) != len(t["obligations"])
        or len(needs) != len(t["information_needs"])
        or len(queries) != len(t["queries"])
    ):
        raise ValueError("Duplicate trace identity")
    if (
        t["parameters"] != [1.2, 0.75, 0.25]
        or t["fusion"] != "NONE"
        or t["analyzer"] != "canonical"
    ):
        raise ValueError("U1 controlled retrieval configuration differs")
    if any(n["obligation"] not in obligations for n in needs.values()):
        raise ValueError("Need references unknown obligation")
    if {n["obligation"] for n in needs.values()} != obligations.keys():
        raise ValueError("An obligation lacks a frozen information need")
    if any(
        not n["identity"].startswith(t["task_identity"] + "/" + n["obligation"] + "/")
        for n in needs.values()
    ):
        raise ValueError("Need identity has foreign task/obligation scope")
    c_links = []
    b_links = []
    a = []
    for q in queries.values():
        if digest(q["text"].encode()) != t["literal_query_sha256"].get(q["identity"]):
            raise ValueError("Literal authored query changed")
        if (
            list(analyze_repository_text_lexical_query(text=q["text"]).normalized_terms)
            != q["analyzed_terms"]
        ):
            raise ValueError("Hidden query transformation")
        if (
            q["route"]["mechanism"] != "CANONICAL_RESOURCE_BM25"
            or q["route"]["exact_hint_routed"]
            or q["route"]["reason"] != "U1_CONTROLLED_LEXICAL_ONLY"
        ):
            raise ValueError("Non-U1 route")
        if q["route"]["exact_hints_detected"] != [
            h["hint"] for h in t["hints"] if h["hint"] in q["text"]
        ]:
            raise ValueError("Hint/query usage changed")
        if q["arm"] == "A":
            a.append(q)
            if (
                q["text"] != t["task"]
                or q["obligation"] is not None
                or q["information_need"] is not None
            ):
                raise ValueError("Whole task query changed")
        elif q["arm"] == "B":
            b_links.append(q["obligation"])
            if q["obligation"] not in obligations or q["information_need"] is not None:
                raise ValueError("Invalid obligation query linkage")
        elif q["arm"] == "C":
            c_links.append(q["information_need"])
            n = needs.get(q["information_need"])
            if n is None or q["obligation"] != n["obligation"]:
                raise ValueError("Invalid need query linkage")
        else:
            raise ValueError("Unknown arm")
    if (
        len(a) != 1
        or set(b_links) != obligations.keys()
        or len(b_links) != len(obligations)
        or set(c_links) != needs.keys()
        or len(c_links) != len(needs)
    ):
        raise ValueError("Incomplete one-query-per-obligation/need linkage")
    for row in [*obligations.values(), *needs.values()]:
        for span in row["task_basis"]:
            if t["task"][span["start"] : span["end"]] != span["text"]:
                raise ValueError("Task provenance span changed")


def layer(t: dict[str, Any], stage: str) -> dict[str, Any]:
    """Create explicitly empty future layers without introducing a search loop."""
    validate(t)
    return {
        "schema": "u1-acquisition-trace-v1",
        "stage": stage,
        "stages": list(STAGES),
        "TASK": {
            "identity": t["task_identity"],
            "text": t["task"],
            "sha256": t["task_sha256"],
            "hints": t["hints"],
        },
        "OBLIGATION": t["obligations"],
        "INFORMATION_NEED": t["information_needs"],
        "QUERY": t["queries"],
        "ROUTE": [{"query": q["identity"], **q["route"]} for q in t["queries"]],
        "RESULT": {},
        "JUDGMENT": [],
        "FAILURE": [],
        "NEXT_ACTION": "Fresh independent Stage C; then separate blind C.5; then D",
        "manual_inspection": "Human observation is not gold; labels/comments must remain separate MANUAL_AUDIT.",
    }


def review(t: dict[str, Any]) -> str:
    """Render every exact author input for inspection before outcomes exist."""
    lines = [
        "# Case 0011 Stage A review",
        "",
        "## Original prompt (verbatim)",
        "",
        "```text",
        t["task"].removesuffix("\n"),
        "```",
        "",
        "## Obligations (caller interpretation)",
        "",
        "| Obligation | Exact statement | Criterion | Verbatim task basis |",
        "|---|---|---|---|",
    ]
    for o in t["obligations"]:
        evidence = "<br>".join(
            f"line {b['line']}: {b['text'].strip()}" for b in o["task_basis"]
        )
        lines.append(
            f"| {o['identity']} | {o['predicate']} | {o['criterion']['statement']} | {evidence} |"
        )
    lines += [
        "",
        "All obligations are MANDATORY; applicability condition = null. Criteria and reasons are manual; spans are verbatim.",
        "",
        "## Information needs (manual)",
        "",
        "| Obligation | Need / exact statement | Reason | Task evidence |",
        "|---|---|---|---|",
    ]
    for n in t["information_needs"]:
        evidence = "<br>".join(
            f"line {b['line']}: {b['text'].strip()}" for b in n["task_basis"]
        )
        lines.append(
            f"| {n['obligation']} | `{n['identity']}`<br>{n['statement']} | {n['reason']} | {evidence} |"
        )
    lines += [
        "",
        "## Exact queries, native analyzer terms and routes",
        "",
        "| Arm | Obligation | Information need | Exact query | Analyzed terms (diagnostic) | Route |",
        "|---|---|---|---|---|---|",
    ]
    for q in t["queries"]:
        literal = (
            "full verbatim prompt above, including its terminal LF"
            if q["arm"] == "A"
            else "`" + q["text"] + "`"
        )
        lines.append(
            f"| {q['arm']} | {q['obligation']} | {q['information_need']} | {literal} | {', '.join(q['analyzed_terms'])} | {q['route']['mechanism']} |"
        )
    lines += [
        "",
        "## Explicit task hints",
        "",
        "| Hint | Source task character locations | Interpretation | Routed? | Reason |",
        "|---|---|---|---|---|",
    ]
    for h in t["hints"]:
        lines.append(
            f"| `{h['hint']}` | {h['locations']} | {h['interpretation']} | NO | {h['reason']} |"
        )
    lines += [
        "",
        "Every hint is NOT_ROUTED_IN_U1. Query route records show where it was included literally. Execution status: NOT_EXECUTED.",
        "Human inspection is not Stage C gold. Maintainer comments/labels must remain MANUAL_AUDIT.",
        "",
    ]
    return "\n".join(lines)
