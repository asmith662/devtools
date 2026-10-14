# Copyright (c) 2026
# ruff: noqa: ANN401, PLR2004, PERF401 -- bounded scientific JSON contracts
"""Exact captured-data projection; no acquisition, models or repository reads."""

from __future__ import annotations

import copy
from typing import Any

from experiments.orchestration.storage import require

VERDICTS = ("GROUNDED_SOURCE", "NOT_GROUNDED_SOURCE", "UNCERTAIN_SOURCE")
LABELS = ("REQUIRED", "HELPFUL_ONLY", "UNNECESSARY")
IDENTITY = ("address", "document_identity", "content_identity")
FRAME = ("repository_id", "snapshot_id", "corpus_id")
BLIND_OBLIGATION = ("id", "requirement", "satisfaction", "exclusions", "gap")


def endpoint(row: Any) -> Any:
    """Retain exact native document and content identity."""
    return {k: row[k] for k in IDENTITY}


def unique(rows: Any, keys: tuple[str, ...]) -> dict[tuple[Any, ...], Any]:
    """Reject duplicate scientific identities instead of silently dropping them."""
    result = {tuple(r[k] for k in keys): r for r in rows}
    require(len(result) == len(rows), "Duplicate identity")
    return result


def validate_channels(capture: Any, resources: Any) -> None:
    """Authenticate complete BROAD membership against captured native fact rows."""
    by = unique(resources, ("address",))
    facts = unique(capture["facts"], ("fact_identity",))
    for fact in facts.values():
        require(
            fact["source_snapshot_id"]
            == capture["frame"]["snapshot_id"]
            == fact["target_snapshot_id"],
            "Foreign Reference frame",
        )
        require(
            (fact["source_address"],) in by and (fact["target_address"],) in by,
            "Foreign Reference endpoint",
        )
        require(
            fact["target_content_identity"]
            == by[(fact["target_address"],)]["content_identity"],
            "Reference target content",
        )
        require(
            all(
                fact[k]
                for k in (
                    "fact_identity",
                    "derivation_identity",
                    "target_declaration_identity",
                    "target_subject_identity",
                    "native_route",
                )
            ),
            "Malformed Reference provenance",
        )
        require(
            set(fact["source_range_utf8"])
            == {"start_line", "start_column_utf8", "end_line", "end_column_utf8"},
            "Reference span",
        )
    unique(capture["queries"], ("obligation",))
    for query in capture["queries"]:
        a = query["A"]
        positions = unique(a, ("address",))
        require([r["a_rank"] for r in a] == list(range(1, len(a) + 1)), "A ranks")
        for row in a:
            require(
                endpoint(row) == endpoint(by[(row["address"],)]),
                "A stale identity",
            )
            require(
                row["score"] > 0 and row["filename_weight"] == 0.25,
                "A settings/positive universe",
            )
        require(
            [r["score"] for r in a] == sorted((r["score"] for r in a), reverse=True),
            "A score ordering",
        )
        expected = {
            (f["source_address"], f["target_address"], f["fact_identity"])
            for f in facts.values()
            if (f["source_address"],) in positions
            and (f["target_address"],) in positions
            and positions[(f["source_address"],)]["a_rank"]
            < positions[(f["target_address"],)]["a_rank"]
        }
        actual = set()
        unique(query["broad"], ("target",))
        require(
            [t["rank"] for t in query["broad"]]
            == sorted(t["rank"] for t in query["broad"]),
            "Target ordering",
        )
        for t in query["broad"]:
            require((t["target"],) in positions, "Target absent from A")
            rank = positions[(t["target"],)]["a_rank"]
            require(t["rank"] == rank and rank > 1, "Target rank")
            require(t["predecessor"] == a[rank - 2], "Original predecessor")
            require(bool(t["sources"]), "Unsupported target")
            unique(t["sources"], ("source",))
            for source in t["sources"]:
                address = source["source"]
                require(
                    (address,) in positions
                    and source["rank"] == positions[(address,)]["a_rank"] < rank,
                    "Source rank/eligibility",
                )
                require(
                    source["facts"] == sorted(set(source["facts"])) and source["facts"],
                    "Reference duplicates/order",
                )
                for fid in source["facts"]:
                    require((fid,) in facts, "Unsupported Reference")
                    fact = facts[(fid,)]
                    require(
                        fact["source_address"] == address
                        and fact["target_address"] == t["target"],
                        "Reference direction/endpoints",
                    )
                    actual.add((address, t["target"], fid))
        require(actual == expected, "BROAD exact eligible Reference membership")


def grounding_packet(design: Any, resources: Any, capture: Any) -> Any:
    """Disclose only complete own source content and obligation purpose."""
    require(
        capture["case"] == design["case"] and capture["frame"] == design["frame"],
        "Grounding case/frame identity",
    )
    validate_channels(capture, resources)
    by = {r["address"]: r for r in resources}
    queries = {q["obligation"]: q for q in capture["queries"]}
    require(
        set(queries) == {o["id"] for o in design["obligations"]},
        "Obligation completeness",
    )
    cells = []
    for o in design["obligations"]:
        sources = sorted(
            {s["source"] for t in queries[o["id"]]["broad"] for s in t["sources"]},
        )
        for address in sources:
            cells.append(
                {
                    "obligation": {k: o[k] for k in BLIND_OBLIGATION},
                    "source": {
                        **endpoint(by[address]),
                        "content": by[address]["content"],
                    },
                },
            )
    return {
        "schema": "source-grounding-packet-v1",
        "case": design["case"],
        "task": design["task_text"],
        "frame": design["frame"],
        "cells": cells,
    }


def qualify(capture: Any, judgments: Any) -> Any:
    """Project an exact subset without touching original A or predecessors."""
    verdicts = {
        (c["obligation"], c["source"]["address"]): c["verdict"] for c in judgments
    }
    require(len(verdicts) == len(judgments), "Duplicate grounding cell")
    expected = {
        (q["obligation"], s["source"])
        for q in capture["queries"]
        for t in q["broad"]
        for s in t["sources"]
    }
    require(
        set(verdicts) == expected and all(v in VERDICTS for v in verdicts.values()),
        "Grounding completeness/verdict",
    )
    result = copy.deepcopy(capture)
    for q in result["queries"]:
        for channel, accepted in (
            ("qualified", {VERDICTS[0]}),
            ("uncertain_potential", {VERDICTS[2]}),
        ):
            targets = []
            for t in q["broad"]:
                sources = [
                    s
                    for s in t["sources"]
                    if verdicts[q["obligation"], s["source"]] in accepted
                ]
                if sources:
                    targets.append({**t, "sources": sources})
            q[channel] = targets
        require(
            q["A"]
            == next(
                x["A"] for x in capture["queries"] if x["obligation"] == q["obligation"]
            ),
            "A ablation identity",
        )
    return result


def pair(target: str, predecessor: str) -> tuple[str, str | None]:
    """Use ordinal comparisons; do not assign numeric utility."""
    require(target in LABELS and predecessor in LABELS, "Unknown gold label")
    if target == predecessor:
        return "NEUTRAL", None
    beneficial = target == "REQUIRED" or predecessor == "UNNECESSARY"
    outcome = "BENEFICIAL" if beneficial else "HARMFUL"
    strong = (
        "STRONG_" + outcome
        if {target, predecessor} == {"REQUIRED", "UNNECESSARY"}
        else None
    )
    return outcome, strong


def category(strong_beneficial: int, strong_harmful: int) -> str:
    """Exactly the four prospectively frozen qualified case categories."""
    require(strong_beneficial >= 0 and strong_harmful >= 0, "Negative count")
    if strong_beneficial and strong_harmful:
        return "QUALIFIED_MIXED_STRUCTURAL_DISCRIMINATION_SIGNAL"
    if strong_beneficial:
        return "QUALIFIED_STRUCTURAL_DISCRIMINATION_SIGNAL"
    if strong_harmful:
        return "QUALIFIED_STRUCTURAL_DISCRIMINATION_CONTRADICTED"
    return "QUALIFIED_NO_MATERIAL_STRUCTURAL_DISCRIMINATION_SIGNAL"
