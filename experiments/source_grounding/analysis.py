# Copyright (c) 2026
# ruff: noqa: ANN401, E501, PLR2004 -- exact future deterministic joins
"""Future D consumes sealed B and imported C only. No model or acquisition."""

from __future__ import annotations

import gzip
import json
import math
import statistics
from collections import Counter
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from pathlib import Path

from experiments.codex_dogfood.case_0009.artifacts import digest, json_bytes
from experiments.orchestration.isolation import PRIMARY
from experiments.orchestration.storage import load, require
from experiments.source_grounding import contracts
from experiments.source_grounding.capture import sealed
from experiments.source_grounding.cases import CASES


def rate(numerator: int, denominator: int) -> Any:
    """Preserve undefined denominators instead of reporting zero success."""
    return {
        "numerator": numerator,
        "denominator": denominator,
        "proportion": numerator / denominator if denominator else None,
    }


def channel(query: Any, name: str, gold: Any) -> Any:
    """Join every endpoint/predecessor to its own obligation's exact cell."""
    targets = query[name]
    a = query["A"]
    oid = query["obligation"]
    required = {
        r["address"] for r in a if gold[oid, r["address"]]["label"] == "REQUIRED"
    }
    counts = Counter(gold[oid, t["target"]]["label"] for t in targets)
    pairs = []
    for target in targets:
        label = gold[oid, target["target"]]["label"]
        predecessor = target["predecessor"]
        plabel = gold[oid, predecessor["address"]]["label"]
        outcome, strong_outcome = contracts.pair(label, plabel)
        pairs.append(
            {
                "obligation": oid,
                "target": target["target"],
                "rank": target["rank"],
                "target_label": label,
                "predecessor": predecessor["address"],
                "predecessor_rank": predecessor["a_rank"],
                "predecessor_label": plabel,
                "outcome": outcome,
                "strong": strong_outcome,
                "sources": target["sources"],
            },
        )
    outcomes = Counter(p["outcome"] for p in pairs)
    strong = Counter(p["strong"] for p in pairs if p["strong"])
    return {
        "targets": len(targets),
        "labels": {k: counts[k] for k in contracts.LABELS},
        "useful_target_rate": rate(
            counts["REQUIRED"] + counts["HELPFUL_ONLY"],
            len(targets),
        ),
        "required_in_A_support": rate(counts["REQUIRED"], len(required)),
        "unsupported_required_in_A": sorted(required - {t["target"] for t in targets}),
        "local_pairs": len(pairs),
        "outcomes": {k: outcomes[k] for k in ("BENEFICIAL", "NEUTRAL", "HARMFUL")},
        "strong": {k: strong[k] for k in ("STRONG_BENEFICIAL", "STRONG_HARMFUL")},
        "pairs": pairs,
    }


def analyze(root: Path) -> Any:
    """Reject bad joins; never drop malformed support or tune a threshold."""
    require(
        {p.name for p in (root / "B").iterdir()}
        == set(CASES)
        == {p.name for p in (root / "C").iterdir()},
        "Cohort identity",
    )
    cases = []
    trace: list[Any] = []
    timings = []
    threads = set()
    for case in CASES:
        b, c = root / "B" / case, root / "C" / case
        design = load(b / "design.json")
        rows = json.loads(gzip.decompress((b / "resources.json.gz").read_bytes()))
        sealed(b, rows)
        captured, projection = load(b / "analysis_input.json"), load(c / "gold.json")
        require(
            captured["case"] == projection["case"] == case
            and captured["frame"] == projection["frame"] == design["frame"],
            "Case/frame joins",
        )
        require(
            projection["primary_sha256"]
            == {n: digest((c / "primary" / n).read_bytes()) for n in PRIMARY},
            "Stage C primary artifact integrity",
        )
        primary = load(c / "primary/stage_c_review.json")
        require(
            primary["cells"] == projection["cells"]
            and primary["case"] == case
            and primary["frame"] == projection["frame"]
            and load(c / "primary/stage_c_statistics.json") == projection["statistics"],
            "Primary/gold exact projection",
        )
        cells = projection["cells"]
        gold = {(cell["obligation"], cell["source"]["address"]): cell for cell in cells}
        require(
            len(gold) == len(cells)
            and set(gold)
            == {(o["id"], r["address"]) for o in design["obligations"] for r in rows},
            "Gold cell completeness",
        )
        by = {r["address"]: r for r in rows}
        for (_oid, address), cell in gold.items():
            require(
                cell["source"] == contracts.endpoint(by[address])
                and cell["label"] in contracts.LABELS,
                "Gold stale identity/label",
            )
        require(
            [q["obligation"] for q in captured["queries"]]
            == [o["id"] for o in design["obligations"]],
            "Exact obligation identities",
        )
        for query in captured["queries"]:
            for resource in query["A"]:
                require(
                    contracts.endpoint(resource)
                    == gold[query["obligation"], resource["address"]]["source"],
                    "A/gold document join",
                )
        verdicts = load(b / "grounding/review.json")["cells"]
        for cell in verdicts:
            require(
                cell["source"]
                == gold[cell["obligation"], cell["source"]["address"]]["source"],
                "Grounding source/gold exact identity",
            )
        grounding = Counter(
            (
                cell["verdict"],
                "USEFUL"
                if gold[cell["obligation"], cell["source"]["address"]]["label"]
                != "UNNECESSARY"
                else "UNNECESSARY",
            )
            for cell in verdicts
        )
        table = {
            v: {k: grounding[v, k] for k in ("USEFUL", "UNNECESSARY")}
            for v in contracts.VERDICTS
        }
        obligations = []
        for query in captured["queries"]:
            oid = query["obligation"]
            a_addresses = {r["address"] for r in query["A"]}
            broad, qualified = (
                channel(query, "broad", gold),
                channel(query, "qualified", gold),
            )
            timings.append(sum(query["timings"].values()) / 1000000)
            sources = {s["source"] for t in query["broad"] for s in t["sources"]}
            label_counts = Counter(
                gold[oid, address]["label"] for address in a_addresses
            )
            baseline = {k: label_counts[k] for k in contracts.LABELS}
            noise = [
                {"source": s["source"], "target": t["target"]}
                for t in query["qualified"]
                for s in t["sources"]
                if gold[oid, s["source"]]["label"] != "UNNECESSARY"
                and gold[oid, t["target"]]["label"] == "UNNECESSARY"
            ]
            obligations.append(
                {
                    "obligation": oid,
                    "A_count": len(a_addresses),
                    "A_labels": baseline,
                    "baseline_useful_rate": rate(
                        baseline["REQUIRED"] + baseline["HELPFUL_ONLY"],
                        len(a_addresses),
                    ),
                    "baseline_lexical_non_reach_required": sorted(
                        address
                        for (o, address), cell in gold.items()
                        if o == oid
                        and cell["label"] == "REQUIRED"
                        and address not in a_addresses
                    ),
                    "broad": broad,
                    "qualified": qualified,
                    "uncertain_potential_targets": len(query["uncertain_potential"]),
                    "qualified_structural_noise_from_useful_grounded_sources": noise,
                    "grounding_sources": len(sources),
                },
            )
            for channel_name, analysis in (("BROAD", broad), ("QUALIFIED", qualified)):
                trace.extend(
                    {"case": case, "channel": channel_name, **pair}
                    for pair in analysis["pairs"]
                )
        sb = sum(o["qualified"]["strong"]["STRONG_BENEFICIAL"] for o in obligations)
        sh = sum(o["qualified"]["strong"]["STRONG_HARMFUL"] for o in obligations)
        costs = load(b / "costs.json")
        require(
            costs["grounding_thread_id"] not in threads,
            "Grounding session reused across cases",
        )
        threads.add(costs["grounding_thread_id"])
        cases.append(
            {
                "case": case,
                "frame": design["frame"],
                "grounding_table": table,
                "grounded_source_useful_rate": rate(
                    table["GROUNDED_SOURCE"]["USEFUL"],
                    sum(table["GROUNDED_SOURCE"].values()),
                ),
                "failure_taxonomy": {
                    "GROUNDING_FALSE_POSITIVE": table["GROUNDED_SOURCE"]["UNNECESSARY"],
                    "GROUNDING_FALSE_NEGATIVE": table["NOT_GROUNDED_SOURCE"]["USEFUL"],
                    "GROUNDING_UNCERTAIN_USEFUL": table["UNCERTAIN_SOURCE"]["USEFUL"],
                    "STRUCTURAL_TARGET_NOISE_AFTER_GROUNDING": sum(
                        len(
                            o[
                                "qualified_structural_noise_from_useful_grounded_sources"
                            ],
                        )
                        for o in obligations
                    ),
                    "STRUCTURAL_SIGNAL_ABSENT_AFTER_GROUNDING": sb == 0,
                },
                "category": contracts.category(sb, sh),
                "obligations": obligations,
                "costs": costs,
                "gold_sufficiency_and_gaps": projection["statistics"],
                "input_hashes": {
                    "B_integrity": digest((b / "integrity.json").read_bytes()),
                    "gold_projection": digest((c / "gold.json").read_bytes()),
                },
            },
        )
    cohort = {}
    for name in ("broad", "qualified"):
        all_channels = [o[name] for c in cases for o in c["obligations"]]
        counts = {
            k: sum(v["labels"][k] for v in all_channels) for k in contracts.LABELS
        }
        required = sum(v["required_in_A_support"]["denominator"] for v in all_channels)
        cohort[name] = {
            "targets": sum(v["targets"] for v in all_channels),
            "labels": counts,
            "useful_target_rate": rate(
                counts["REQUIRED"] + counts["HELPFUL_ONLY"],
                sum(v["targets"] for v in all_channels),
            ),
            "required_in_A_support": rate(counts["REQUIRED"], required),
            "local_pairs": sum(v["local_pairs"] for v in all_channels),
            "outcomes": {
                k: sum(v["outcomes"][k] for v in all_channels)
                for k in ("BENEFICIAL", "NEUTRAL", "HARMFUL")
            },
            "strong": {
                k: sum(v["strong"][k] for v in all_channels)
                for k in ("STRONG_BENEFICIAL", "STRONG_HARMFUL")
            },
        }
    return {
        "schema": "source-grounding-D-v1",
        "cases": cases,
        "cohort_descriptive": cohort,
        "performance": {
            "captured_online_ms": timings,
            "median_ms": statistics.median(timings),
            "nearest_rank_p95_ms": sorted(timings)[math.ceil(len(timings) * 0.95) - 1],
            "median_250ms_target": statistics.median(timings) <= 250,
            "p95_over_1s_concern": max(timings) > 1000,
            "model_time_separate": True,
        },
        "trace": trace,
        "join_defects": 0,
        "actual_rank_modifications": 0,
        "cohort_gate": None,
        "interpretation": "NON_GATING: compare qualification precision, retained useful/REQUIRED coverage, local outcomes and full grounding cost. No scalar pass/fail, causal improvement, reranker validation or production authorization. Maintainer chooses consumption experiment, stronger Localization semantics or stopping. A-only universe cannot rescue lexical non-reach.",
        "limitations": "Three development cases; locality/confounding; incidental references; sparse relation surfaces; uncertainty recall loss; semantic/model cost; conditional gold gaps retained. Controller progress logs separately retain operational orchestration timings; these are not scientific authority. No child/confirmation/reserve.",
    }


def render(result: Any) -> str:
    """Keep every exact count, identity and provenance inspectable."""
    return (
        "# Purpose-relative source grounding\n\nNON_GATING development evidence; no ranking changes.\n\n```json\n"
        + json_bytes(result).decode()
        + "```\n"
    )
