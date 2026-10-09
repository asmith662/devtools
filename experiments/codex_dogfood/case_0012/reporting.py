# Copyright (c) 2026
# ruff: noqa: COM812, E501 -- literal protocol prose or fixture assertions; formatter owns commas
"""Human Stage A review of exact authored task-to-locator correspondence."""

from __future__ import annotations

import json
from typing import Any

from experiments.codex_dogfood.case_0012 import amendment


def matrix(treatment: dict[str, Any]) -> str:
    """Expose every mandatory clause and explicit operational exclusion."""
    lines = [
        "# Task requirement matrix",
        "",
        "Every non-operational task line (including all semicolon clauses) maps to an obligation. Criteria explicitly inventory its complete contract. This is task-interpretation review, not repository witness completeness.",
        "",
    ]
    for row in treatment["task_requirement_matrix"]:
        lines += [
            f"## {row['requirement']} [{row['basis']['start']},{row['basis']['end']})",
            "",
            row["basis"]["text"].strip(),
            "",
            "Obligations: " + ", ".join(row["obligations"])
            if row["obligations"]
            else "Exclusion: " + row["exclusion"],
            "",
        ]
    lines += [
        "## Operational exclusions outside the feature task",
        "",
        "Stage A freezes acquisition only: no future feature implementation, treatment, gold, confirmation/reserve or live services. `.local/codex-result.md` is operational handoff only, excluded from task text, obligations, hints, queries, witnesses, eligible resources, scientific hashes and gap judgments. These operations are not repository-information obligations.",
        "",
    ]
    return "\n".join(lines).rstrip("\n") + "\n"


def review(treatment: dict[str, Any], frame: dict[str, Any]) -> str:
    """Show every input, association, locator, query, rule and exclusion before lookup."""
    lines = [
        "# Case 0012 Stage A review",
        "",
        "**Stage A FROZEN; Stage B NOT EXECUTED; effectiveness UNKNOWN.**",
        "",
        "Challenge task interpretation, clause coverage, extraction, typing, association, locator admission, arm design and decision arithmetic before authorization. No Case 0012 hints were resolved, no lexical query executed, and no rank/score/gold or treatment outcome is present.",
        "",
        amendment.review(amendment.definition(treatment)),
        "## Original task verbatim",
        "",
        "```text",
        treatment["task_text"].rstrip("\n"),
        "```",
        "",
        matrix(treatment),
        "## Obligations, conceptual requirements and unchanged lexical queries",
        "",
    ]
    for obligation in treatment["obligations"]:
        lines += [
            "### " + obligation["identity"],
            "",
            obligation["statement"],
            "",
            "Criterion: " + obligation["criterion"],
            "",
            "Applicability: " + obligation["applicability"],
            "",
            "Task basis:",
            "",
            "```text",
            "".join(b["text"] for b in obligation["task_basis"]).rstrip(),
            "```",
            "",
            "Exact query: `" + obligation["query"] + "`",
            "",
            "Canonical analyzed terms: " + json.dumps(obligation["analyzed_terms"]),
            "",
            "Route: native canonical resource BM25; complete positive fallback retained in all arms. Exact hints supply only candidate evidence; the whole conceptual criterion still requires independent gold/witness evaluation.",
            "",
        ]
    lines += [
        "## Hint inventories and extraction decisions",
        "",
        "Caller reference was independently authored from task text, syntax and obligation interpretation before frame construction. No repository content, lookup outcome, rank, gold or historical answer was used for its review. Bare names stay unsupported; agreement does not establish repository identity.",
        "",
        "```json",
        json.dumps(treatment["extraction_agreement"], indent=2),
        "```",
        "",
    ]
    for name in ("caller_reviewed_hint_reference", "rule_extracted_hints"):
        lines += ["### " + name, ""]
        for hint in treatment[name]:
            start, end = hint["span"]["start"], hint["span"]["end"]
            context = treatment["task_text"][
                max(0, start - 45) : min(len(treatment["task_text"]), end + 45)
            ]
            lines += [
                f"- `{hint['text']}` [{start},{end}), {hint['category']}; identity `{hint['identity']['value']}`; rule `{hint['rule']}`; form {hint['syntactic_form']}. Context: {json.dumps(context)}"
            ]
        lines += [""]
    lines += [
        "Per-observation caller/rule flags:",
        "",
        "```json",
        json.dumps(treatment["hint_inventory"], indent=2),
        "```",
        "",
    ]
    lines += [
        "All scanned code/path decisions. Operational handoff instructions are outside the feature task and query text:",
        "",
        "```json",
        json.dumps(treatment["extraction_decisions"], indent=2),
        "```",
        "",
        "## Every frozen hint association and exact route request",
        "",
    ]
    for arm, requests in treatment["exact_route_requests"].items():
        lines += ["### Arm " + arm, ""]
        for route in requests:
            lines += [
                f"- `{route['identity']}`: `{route['hint']['text']}` → **{route['association']['lane']['value']}** → {route['mechanism']}",
                "  - Typed locator: `"
                + json.dumps(route["locator"], sort_keys=True)
                + "`",
                "  - Association: " + route["association"]["reason"],
                "  - Admission: " + route["reason"],
            ]
        lines += [""]
    lines += ["## Prospective arms", ""]
    lines += [f"- {arm}: {definition}" for arm, definition in treatment["arms"].items()]
    lines += [
        "",
        "Shared settings: `" + json.dumps(treatment["settings"], sort_keys=True) + "`",
        "",
        "The unchanged full-task global safety query is the original task verbatim, separately retained. Its analyzed terms:",
        "",
        "```json",
        json.dumps(treatment["global_safety_query"]["analyzed_terms"]),
        "```",
        "",
        "## Exact-first semantics",
        "",
        "Resolve supported associated hints only after authorization. RESOLVED alone promotes an occurrence. Retain all other diagnostics without promotion. Deduplicate exact occurrences; order by source span, route identity, native occurrence identity; append every remaining native lexical row in unchanged order. Native scores/contributions/ranks and lexical misses remain explicit. Global lexical safety is separately unchanged; no fusion, score invention, candidate loss or post-outcome association.",
        "",
        "## Frozen decision rule and prospective metrics",
        "",
    ]
    for key, value in treatment["decision_rule"].items():
        lines += [
            "### " + key,
            "",
            value if isinstance(value, str) else json.dumps(value, indent=2),
            "",
        ]
    lines += [
        "## Frame and exact native input universes",
        "",
        "```json",
        json.dumps(frame, indent=2, sort_keys=True),
        "```",
        "",
        "Frame membership is broad and query-independent. Python interpretation is address-only native preparation, not declaration analysis or hint lookup. Declaration universe is the full listed Python selection; direct RI is invoked only later for requested modules/classes.",
        "",
        "## Explicit exclusions and future blind gold",
        "",
        "No repository result, native referent selection, lexical rank, score, gold, treatment execution or effectiveness claim. Operational instructions are separately excluded; `.local/codex-result.md` is never a scientific input. Stage C protocol is PREPARED ONLY and must receive only task, obligations and eligible contents after separate authorization. No blind packet or gold is created here.",
        "",
        "Next: maintainer manually reviews this complete trace. Only explicit authorization permits Stage B exact resolution, one canonical lexical capture, A/B/C presentation and blind packet creation.",
        "",
    ]
    return "\n".join(lines).rstrip("\n") + "\n"
