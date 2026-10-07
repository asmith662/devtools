# Copyright (c) 2026
# ruff: noqa: C901, COM812, E501, PLR0915, PLR2004 -- bounded frozen JSON analysis
"""Join sealed prospective evidence; replay R1.5, never execute treatments."""

from __future__ import annotations

import argparse
import asyncio
import gzip
import importlib
import itertools
import json
import math
import statistics
from dataclasses import replace
from fractions import Fraction
from typing import Any, cast

from experiments.bm25_sensitivity.cases import Case
from experiments.bm25_sensitivity.metrics import measure, normalize
from experiments.bm25_sensitivity.protocol import select
from experiments.bm25_sensitivity.storage import HERE, get
from experiments.codex_dogfood.case_0009.artifacts import (
    ROOT,
    binary,
    digest,
    git,
    json_bytes,
    put_json,
    put_text,
    read_json,
)
from experiments.codex_dogfood.case_0010 import execute
from experiments.codex_dogfood.case_0010.freeze import CASE, load_inputs
from experiments.codex_dogfood.case_0010.reporting import INTERPRETATION, report
from experiments.retrieval_diagnostics.adapters import fields, from_rows
from experiments.retrieval_diagnostics.comparison import compare
from experiments.retrieval_diagnostics.mechanics import Mechanics
from experiments.retrieval_diagnostics.models import (
    DiagnosticPolicy,
    Frame,
    Judgment,
    Label,
)

# This sealed, standard-library-only verifier is an external scientific boundary.
# Dynamic import avoids imposing repository typing/style on its immutable bytes.
SC: Any = importlib.import_module(
    "experiments.codex_dogfood.case_0010.adjudication.stage_c"
)
GOLD_HASHES = {
    "judgments.json": "d4ab1a2aa752da6b07f4535100cbbeda9dd716a45abbee3dba15749e78d42cec",
    "gold_statistics.json": "cc31aa4402a12841ebd4cd60e849357c16a6db9013608d1a9e35a49c69059b1a",
    "judgments.sha256": "7cab5ddb6e7e7615679cba45674eb465a9cbc6b6cc5110a22b9f0e1be6ad7e3f",
    "METHOD.md": "7ee6301e4b92003a845de083de84f1a3c25c103ec9ac22391393df042f95d2c3",
    "build_judgments.py": "ddbf550575aa99c174079246062deb1ac9ef65cc3009855c3726dce793ea5dfb",
    "stage_c.py": "a8e74685242bcde4548da4ae0a669c2bf1855948982e864219530c05cc27edd9",
    "test_stage_c.py": "8d4c41e3baf0565ccbe468f755fce97f5a89eb0653a01daf7269774c2092062c",
    "stage_c_pytest.ini": "9f557adf7d93f2a36fdbd765290b5023bd374df10736f0f31a5a4e18768a58f3",
}
CHAIN = (
    ("9850885", "Freeze BM25 sensitivity protocol"),
    ("0fec2dc", "Validate BM25 sensitivity replay and case eligibility"),
    ("7edac36", "Analyze BM25 sensitivity development"),
    ("b0069d3", "Freeze Case 0010 BM25 sensitivity treatment"),
    ("ae97daf", "Capture Case 0010 BM25 sensitivity treatments"),
    ("84b99243", "Freeze Case 0010 blind obligation judgments"),
)


async def provenance() -> dict[str, Any]:
    """Check ancestry and original committed bytes before opening joined outcomes."""
    chain = []
    previous = None
    for short, subject in CHAIN:
        commit = (await git("rev-parse", short)).decode().strip()
        SC.require(
            (await git("show", "-s", "--format=%s", commit)).decode().strip()
            == subject,
            "Frozen checkpoint subject differs",
        )
        await git("merge-base", "--is-ancestor", commit, "HEAD")
        if previous is not None:
            await git("merge-base", "--is-ancestor", previous, commit)
        chain.append({"commit": commit, "subject": subject})
        previous = commit
    hashes = {}
    base = "experiments/codex_dogfood/case_0010/"
    pins = [
        ("0fec2dc", "experiments/bm25_sensitivity/protocol.json"),
        ("0fec2dc", "experiments/bm25_sensitivity/PROTOCOL.md"),
        ("7edac36", "experiments/bm25_sensitivity/development.json.gz"),
    ]
    for commit, seal in (
        ("b0069d3", "integrity.json"),
        ("ae97daf", "stage_b_integrity.json"),
    ):
        record = json.loads(await git("show", commit + ":" + base + seal))
        pins.append((commit, base + seal))
        for name, expected in record["sha256"].items():
            data = await git("show", commit + ":" + base + name)
            SC.require(digest(data) == expected, "Committed seal binding differs")
            pins.append((commit, base + name))
    for name, expected in GOLD_HASHES.items():
        path = base + "adjudication/" + name
        data = await git("show", "84b99243:" + path)
        # Exact bytes are required here, without the text-normalization boundary.
        SC.require(
            digest(data)
            == expected
            == digest((CASE / "adjudication" / name).read_bytes()),
            "Sealed gold hash differs",
        )
        hashes[path] = expected
    pins.extend(("ae97daf", base + "adjudication/" + name) for name in SC.INPUT_HASHES)
    for commit, path in pins:
        data = await git("show", commit + ":" + path)
        SC.require(
            data == binary(ROOT / path), "Frozen committed input differs: " + path
        )
        hashes[path] = digest(data)
    return {"chain": chain, "input_sha256": dict(sorted(hashes.items()))}


def joined_case() -> tuple[Case, dict[str, Any], dict[str, Any]]:
    """Adapt exact clean gold to existing alternative-aware evaluation primitives."""
    native = load_inputs()
    manifest, packet = SC.load_packet(CASE / "adjudication")
    gold = read_json(CASE / "adjudication/judgments.json")
    SC.verify_judgments(manifest, packet, gold)
    stats = SC.statistics(manifest, packet, gold)
    SC.require(
        SC.canonical(stats)
        == (CASE / "adjudication/gold_statistics.json").read_bytes(),
        "Gold statistics replay differs",
    )
    SC.require(
        stats["coverage"]["resources"] == 531
        and stats["coverage"]["obligations"] == 10
        and stats["coverage"]["cells"] == 5310
        and stats["cell_labels"]
        == {"REQUIRED": 39, "HELPFUL_ONLY": 47, "UNNECESSARY": 5224, "UNRESOLVED": 0},
        "Clean gold summary differs",
    )
    for key, expected in {
        "applicable_obligations": 10,
        "distinct_required_information_units": 40,
        "obligation_relative_required_unit_judgments": 45,
        "unique_required_resources_across_all_alternatives": 22,
        "acceptable_alternative_count": 14,
        "valid_cross_obligation_combinations": 9,
        "minimum_sufficient_unique_resource_union": 22,
        "maximum_sufficient_unique_resource_union": 22,
    }.items():
        SC.require(stats[key] == expected, "Gold count differs: " + key)
    SC.require(
        stats["inferability"]
        == {"INFERABLE_AT_START": 40, "INHERENT_DISCOVERY_REQUIRED": 0},
        "Gold inferability differs",
    )
    treatment = read_json(CASE / "treatment.json")
    task = native["task"].identity
    SC.require(
        manifest["task_identity"] == task.value == treatment["task_identity"]
        and gold["task"] == treatment["task"] == treatment["full_task_query"],
        "Task join differs",
    )
    frame = Frame(
        native["snapshot"].repository_id,
        native["snapshot"].id,
        native["documents"].corpus.id,
    )
    resources = {
        d.resource.address.value: d.resource for d in native["documents"].documents
    }
    SC.require(
        len(resources) == 531
        and set(resources) == {r["address"] for r in packet["resources"]},
        "Native resource join differs",
    )
    for key, value in (
        ("repository_id", frame.repository),
        ("snapshot_id", frame.snapshot),
        ("corpus_id", frame.corpus),
    ):
        SC.require(
            str(value) == manifest[key] == gold[key],
            "Native/gold identity join differs",
        )
    for r in packet["resources"]:
        SC.require(
            resources[r["address"]].content == r["content"]
            and resources[r["address"]].content_identity.value == r["content_identity"],
            "Native content join differs",
        )
    queries = tuple(
        (q.identity.value, q.obligation.value, q.text) for q in native["queries"]
    )
    SC.require(
        len(queries) == len({q[0] for q in queries}) == 10
        and [(q, o, t) for q, o, t in queries]
        == [
            (o["query_identity"], o["identity"], o["query"])
            for o in treatment["obligations"]
        ],
        "Query-lane identities differ",
    )
    alternatives = {
        o["identity"]: tuple(
            (a["identity"], tuple(a["resource_addresses"]))
            for a in o["acceptable_alternatives"]
        )
        for o in gold["obligations"]
    }
    judgments = {
        o: tuple(
            Judgment(
                frame,
                resources[c["resource_address"]],
                q.obligation,
                cast("Label", c["label"]),
                tuple(c["required_unit_ids"]),
            )
            for c in gold["cells"]
            if c["obligation_id"] == o
        )
        for q in native["queries"]
        for o in (q.obligation.value,)
    }
    unions = tuple(
        tuple(sorted({p for _, members in choice for p in members}))
        for choice in itertools.product(
            *(alternatives[o] for o in sorted(alternatives))
        )
    )
    required = {
        j.resource.address.value
        for js in judgments.values()
        for j in js
        if j.label == "REQUIRED"
    }
    SC.require(
        len(unions) == 9
        and all(set(u) == required for u in unions)
        and len(required) == 22,
        "Global completion does not reduce to the complete REQUIRED union",
    )
    return (
        Case(
            10,
            native["snapshot"],
            native["documents"],
            None,
            gold["task"],
            queries,
            frame,
            judgments,
            alternatives,
            unions,
            {},
            {},
        ),
        gold,
        stats,
    )


def engines(
    case: Case, captured: dict[str, Any], treatment: dict[str, Any]
) -> dict[str, dict[str, Mechanics]]:
    """Validate all 44 captured lanes against shared exact R1.5 statistics."""
    expected = [[1.2, 0.75, 0.25], [2.4, 0.0, 2.0], [2.4, 0.5, 1.0], [2.4, 0.75, 0.25]]
    SC.require(
        [a["arm"] for a in treatment["arms"]] == list("ABCD")
        and [a["parameters"] for a in treatment["arms"]] == expected
        and all(
            a["analyzer"] == "canonical"
            and a["architecture"]
            == "independent content BM25 + filename_weight * independent filename-stem BM25"
            for a in treatment["arms"]
        ),
        "Frozen arm definitions differ",
    )
    SC.require(set(captured["arms"]) == set("ABCD"), "Captured arm partition differs")
    common = fields(case.documents, execute.configuration(treatment["arms"][0]))
    lanes = [
        ("global", None, case.task),
        *[
            (identity, case.judgments[ob][0].obligation, text)
            for identity, ob, text in case.queries
        ],
    ]
    output = {}
    for arm in treatment["arms"]:
        cfg = execute.configuration(arm)
        data = captured["arms"][arm["arm"]]
        SC.require(
            data["configuration_identity"] == cfg.identity
            and data["parameters"] == arm["parameters"]
            and set(data["lanes"]) == {i for i, _, _ in lanes},
            "Arm/lane join differs",
        )
        state = tuple(
            replace(f, weight=cfg.filename_weight if f.name == "filename" else 1.0)
            for f in common
        )
        current = {}
        for identity, ob, text in lanes:
            lane = data["lanes"][identity]
            SC.require(
                lane["query_text"] == text
                and lane["obligation"] == (ob.value if ob else None),
                "Captured query join differs",
            )
            current[ob.value if ob else "global"] = Mechanics(
                from_rows(
                    case.snapshot,
                    case.documents,
                    identity,
                    text,
                    tuple(lane["query_terms"]),
                    lane["rows"],
                    cfg,
                    state,
                    complete=True,
                    obligation=ob,
                ),
                case.judgments[ob.value] if ob else (),
                # Changed competitors are explicitly explained below; avoid
                # recursively duplicating five term-pair trees in every record.
                policy=DiagnosticPolicy(overtaker_limit=0),
            )
        output[arm["arm"]] = current
    return output


def gates(
    current: dict[str, Any],
    baseline: dict[str, Any],
    cost: dict[str, Any],
    base_cost: dict[str, Any],
    development_worst: Fraction,
) -> dict[str, bool]:
    """Apply the frozen prospective conjunction with exact rank-ratio arithmetic."""
    ratio = {
        k: Fraction(current[k], baseline[k])
        for k in ("global", "max_own", "prefix_union")
    }
    own = [
        Fraction(current["own_depths"][o], d) for o, d in baseline["own_depths"].items()
    ]
    return {
        "required_reach_safe": current["reach_safe"],
        "global_le_1_05": ratio["global"] <= Fraction(105, 100),
        "max_own_le_1_05": ratio["max_own"] <= Fraction(105, 100),
        "meaningful_primary_improvement": min(ratio["prefix_union"], ratio["max_own"])
        <= Fraction(9, 10),
        "no_obligation_gt_1_25": all(r <= Fraction(5, 4) for r in own),
        "half_obligations_nonworse": sum(r <= 1 for r in own) * 2 >= len(own),
        "cost_le_3": all(
            cost[k] <= 3 * base_cost[k]
            for k in ("median_query_seconds", "p95_query_seconds")
        ),
        "development_safe_le_1_25": development_worst <= Fraction(5, 4),
    }


def outcome(arms: dict[str, Any]) -> tuple[str, list[str]]:
    """Preserve all passing candidates; protocol defines no prospective winner tie."""
    candidates = [a for a in "BCD" if all(arms[a]["gates"].values())]
    if candidates:
        return "NONBASELINE_PARAMETER_CANDIDATE", candidates
    robust = all(
        arms[a]["metrics"]["reach_safe"]
        and all(
            Fraction(95, 100)
            <= Fraction(*arms[a]["metrics"]["normalized_exact"][k])
            <= Fraction(105, 100)
            for k in ("global", "max_own", "prefix_union")
        )
        and not arms[a]["gates"]["meaningful_primary_improvement"]
        for a in "BCD"
    )
    return ("BASELINE_ROBUST" if robust else "MIXED / NO SAFE REPLACEMENT"), []


def rank_pairs(
    case: Case, base: dict[str, Mechanics], changed: dict[str, Mechanics]
) -> dict[str, Any]:
    """Partition every REQUIRED cell; null ranks remain explicit misses."""
    pairs: list[dict[str, Any]] = []
    for ob, js in case.judgments.items():
        for j in js:
            if j.label == "REQUIRED":
                address = j.resource.address.value
                a, b = base[ob].rows.get(address), changed[ob].rows.get(address)
                pairs.append(
                    {
                        "obligation": ob,
                        "resource": address,
                        "A": a.rank if a else None,
                        "challenger": b.rank if b else None,
                        "delta": b.rank - a.rank if a and b else None,
                    }
                )
    deltas = [r["delta"] for r in pairs if r["delta"] is not None]
    return {
        "cells": pairs,
        "improved": sum(d < 0 for d in deltas),
        "unchanged": deltas.count(0),
        "worsened": sum(d > 0 for d in deltas),
        "unpaired": len(pairs) - len(deltas),
        "median_delta": statistics.median(deltas),
        "best_improvement": min(deltas),
        "worst_regression": max(deltas),
    }


def build(proof: dict[str, Any]) -> dict[str, Any]:
    """Freeze primary metrics before development interpretation and diagnostics."""
    case, gold, stats = joined_case()
    treatment = read_json(CASE / "treatment.json")
    seal = read_json(CASE / "stage_b_integrity.json")
    for name, expected in seal["sha256"].items():
        SC.require(digest(binary(CASE / name)) == expected, "Stage B seal differs")
    raw = gzip.decompress(binary(CASE / "results.json.gz"))
    SC.require(
        digest(raw) == seal["canonical_payload_sha256"],
        "Stage B payload digest differs",
    )
    captured = json.loads(raw)
    for k in ("repository_id", "snapshot_id", "corpus_id"):
        SC.require(captured[k] == gold[k], "Captured/gold frame join differs")
    SC.require(
        captured["resource_count"] == 531
        and captured["task_sha256"] == digest(case.task.encode()),
        "Captured task/resource frame differs",
    )
    replay = engines(case, captured, treatment)
    # Primary prospective measurements are constructed first and never optimized.
    primary = {a: measure(case, replay[a]) for a in "ABCD"}
    for a in "ABCD":
        normalize(primary[a], primary["A"])
        ranks = replay[a]["global"].rows
        SC.require(
            primary[a]["global"]
            == max(ranks[p].rank for p in primary[a]["required_resource_reach"]),
            "Alternative/global REQUIRED-union completion disagreement",
        )
    primary_digest = digest(json_bytes(primary))
    costs = read_json(CASE / "costs.json")
    for a in "ABCD":
        c = costs["arms"][a]
        values = sorted(c["query_seconds"].values())
        SC.require(
            len(values) == 11
            and c["median_query_seconds"] == statistics.median(values)
            and c["p95_query_seconds"] == values[math.ceil(0.95 * len(values)) - 1]
            and c["sum_query_seconds"] == sum(values),
            "Captured cost summaries differ",
        )
    development = get(HERE / "development.json.gz")
    SC.require(
        digest(binary(HERE / "development.json.gz")) == treatment["development_sha256"]
        and select(development["rows"]) == development["selection"]
        and development["selection"]["roles"] == treatment["selected_roles"]
        and development["selection"]["unique_challengers"]
        == [a["parameters"] for a in treatment["arms"][1:]],
        "Frozen development selection differs",
    )
    arms = {}
    for a, arm in zip("ABCD", treatment["arms"], strict=True):
        own = replay[a]
        own_union = set().union(
            *(set(e.rows) for ob, e in own.items() if ob != "global")
        )
        dev = next(
            r for r in development["rows"] if r["parameters"] == arm["parameters"]
        )
        complete = [c for c in dev["cases"] if c["selection_eligible"]]
        worst = max(
            Fraction(*c["normalized_exact"][k])
            for c in complete
            for k in ("max_own", "prefix_union")
        )
        global_labels = {
            p: "REQUIRED"
            if any(
                j.label == "REQUIRED"
                for js in case.judgments.values()
                for j in js
                if j.resource.address.value == p
            )
            else "HELPFUL_ONLY"
            if any(
                j.label == "HELPFUL_ONLY"
                for js in case.judgments.values()
                for j in js
                if j.resource.address.value == p
            )
            else "UNNECESSARY"
            for p in replay[a]["global"].resources
        }
        global_top = {
            str(k): {
                label: sum(
                    global_labels[r.resource.address.value] == label
                    for r in own["global"].capture.rows[:k]
                )
                for label in ("REQUIRED", "HELPFUL_ONLY", "UNNECESSARY")
            }
            for k in (5, 10, 20)
        }
        arms[a] = {
            "parameters": arm["parameters"],
            "metrics": primary[a],
            "positive": {
                "global_resources": len(own["global"].rows),
                "own_union": len(own_union),
                "own_cells": sum(
                    len(e.rows) for ob, e in own.items() if ob != "global"
                ),
                "global_members": sorted(own["global"].rows),
                "own_members": sorted(own_union),
            },
            "global_top_k": global_top,
            "cost": costs["arms"][a],
            "development": {
                "worst_own_union_exact": [worst.numerator, worst.denominator],
                "cases": [
                    {
                        k: c[k]
                        for k in (
                            "case",
                            "global",
                            "max_own",
                            "prefix_union",
                            "normalized",
                        )
                    }
                    for c in dev["cases"]
                ],
            },
            "gates": gates(
                primary[a], primary["A"], costs["arms"][a], costs["arms"]["A"], worst
            ),
        }
        arms[a]["own_ratios"] = {
            o: [
                Fraction(d, primary["A"]["own_depths"][o]).numerator,
                Fraction(d, primary["A"]["own_depths"][o]).denominator,
            ]
            for o, d in primary[a]["own_depths"].items()
        }
        arms[a]["completion_alternatives"] = {
            o: [
                {
                    "identity": identity,
                    "resources": members,
                    "depth": max(own[o].rows[p].rank for p in members)
                    if all(p in own[o].rows for p in members)
                    else None,
                }
                for identity, members in choices
            ]
            for o, choices in case.alternatives.items()
        }
        if a != "A":
            arms[a]["paired_required"] = rank_pairs(case, replay["A"], own)
            partitions = {}
            for key in (
                "required_resource_reach",
                "required_cells_reached",
                "required_unit_judgments_reached",
                "distinct_units_reached",
            ):
                left, right = primary["A"][key], primary[a][key]
                if key in {"required_cells_reached", "required_unit_judgments_reached"}:
                    left_set, right_set = set(map(tuple, left)), set(map(tuple, right))
                else:
                    left_set, right_set = set(left), set(right)
                totals: dict[str, set[Any]] = {
                    "required_resource_reach": {
                        j.resource.address.value
                        for js in case.judgments.values()
                        for j in js
                        if j.label == "REQUIRED"
                    },
                    "required_cells_reached": {
                        (ob, j.resource.address.value)
                        for ob, js in case.judgments.items()
                        for j in js
                        if j.label == "REQUIRED"
                    },
                    "required_unit_judgments_reached": {
                        (ob, u)
                        for ob, js in case.judgments.items()
                        for j in js
                        if j.label == "REQUIRED"
                        for u in j.units
                    },
                    "distinct_units_reached": {
                        u
                        for js in case.judgments.values()
                        for j in js
                        if j.label == "REQUIRED"
                        for u in j.units
                    },
                }
                total = totals[key]
                partitions[key] = {
                    "A_only": sorted(left_set - right_set),
                    "challenger_only": sorted(right_set - left_set),
                    "missed_by_both": sorted(total - left_set - right_set),
                }
            arms[a]["reach_partitions"] = partitions
        arms[a]["positive_membership_partitions"] = {
            lane: {
                "A_only": sorted(replay["A"][lane].rows.keys() - e.rows.keys()),
                "challenger_only": sorted(
                    e.rows.keys() - replay["A"][lane].rows.keys()
                ),
            }
            for lane, e in own.items()
        }
    verdict, candidates = outcome(arms)
    diagnostic_records = []
    for a in "BCD":
        pairs = arms[a]["paired_required"]["cells"]
        selected = [
            min(pairs, key=lambda r: (r["delta"], r["obligation"], r["resource"])),
            min(pairs, key=lambda r: (-r["delta"], r["obligation"], r["resource"])),
        ]
        regression_ob = min(
            case.alternatives,
            key=lambda o: (
                -Fraction(primary[a]["own_depths"][o], primary["A"]["own_depths"][o]),
                o,
            ),
        )
        best = min(
            arms[a]["completion_alternatives"][regression_ob],
            key=lambda choice: (choice["depth"], choice["identity"]),
        )
        bottleneck = max(
            best["resources"], key=lambda p: replay[a][regression_ob].rows[p].rank
        )
        selected.append({"obligation": regression_ob, "resource": bottleneck})
        for role, row in zip(
            (
                "largest_required_gain",
                "largest_required_regression",
                "largest_completion_regression",
            ),
            selected,
            strict=True,
        ):
            ob, p = row["obligation"], row["resource"]
            left, right = replay["A"][ob], replay[a][ob]
            resource = right.resources[p]
            pair = compare(left, right, resource)
            labels = {j.resource.address.value: j.label for j in case.judgments[ob]}
            overtakers = [
                {
                    "resource": address,
                    "change": "new" if address in pair["new_overtakers"] else "removed",
                    "A": left.explain(left.resources[address]),
                    "challenger": right.explain(right.resources[address]),
                }
                for address in sorted(
                    set(pair["new_overtakers"]) | set(pair["removed_overtakers"])
                )
                if labels[address] == "UNNECESSARY"
            ]
            diagnostic_records.append(
                {
                    "arm": a,
                    "selection": role,
                    "obligation": ob,
                    "resource": p,
                    "A": left.explain(resource),
                    "challenger": right.explain(resource),
                    "pair": pair,
                    "unnecessary_overtakers": overtakers,
                }
            )
        global_target = max(
            primary[a]["required_resource_reach"],
            key=lambda p: replay[a]["global"].rows[p].rank,
        )
        left, right = replay["A"]["global"], replay[a]["global"]
        diagnostic_records.append(
            {
                "arm": a,
                "selection": "global_completion_bottleneck",
                "obligation": "global",
                "resource": global_target,
                "A": left.explain(left.resources[global_target]),
                "challenger": right.explain(right.resources[global_target]),
                "pair": compare(left, right, right.resources[global_target]),
                "unnecessary_overtakers": [],
            }
        )
    profiles = {o: replay["A"][o].query_profile() for o in case.judgments}
    SC.require(
        digest(json_bytes(primary)) == primary_digest,
        "Diagnostics/development mutated primary measurements",
    )
    return {
        "schema": "case-0010-stage-d-v1",
        "provenance": proof,
        "join": {
            **{k: gold[k] for k in ("repository_id", "snapshot_id", "corpus_id")},
            "task_identity": treatment["task_identity"],
            "coverage": stats["coverage"],
            "arms": 4,
            "lanes_per_arm": 11,
            "content_identities": "EXACT",
            "query_identities": "EXACT",
            "alternatives_validated": 14,
            "complete_combinations_validated": 9,
            "global_completion_equals_last_required_resource": True,
        },
        "gold": stats,
        "task_gap": gold["task_gap"],
        "repository_information_gap": gold["repository_information_gap"],
        "stage_c_blindness_attestation": gold["blindness_attestation"],
        "decision_rule": treatment["decision_rule"],
        "primary_metrics_sha256": primary_digest,
        "arms": arms,
        "outcome": verdict,
        "passing_candidates": candidates,
        "multiple_candidates_policy": "All passing candidates retained; no pre-frozen prospective winner precedence.",
        "diagnostics": diagnostic_records,
        "query_profiles": profiles,
        "interpretation": INTERPRETATION,
        "production_parameters_changed": False,
        "confirmation_accessed": False,
        "reserve_accessed": False,
        "variant_status": "R1.6b NOT REQUIRED BEFORE BM25F",
        "next": "R1.7",
        "R2": "MANDATORY",
    }


def main() -> None:
    """Publish once or require exact deterministic JSON/Markdown replay."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("operation", choices=("build", "verify"))
    args = parser.parse_args()
    data = build(asyncio.run(provenance()))
    markdown = report(data)
    if args.operation == "build":
        SC.require(
            not any((CASE / n).exists() for n in ("analysis.json", "analysis.md")),
            "Analysis overwrite refused",
        )
        put_json(CASE / "analysis.json", data)
        put_text(CASE / "analysis.md", markdown)
    else:
        SC.require(
            json_bytes(data) == binary(CASE / "analysis.json"),
            "Analysis JSON replay differs",
        )
        SC.require(
            markdown.encode() == binary(CASE / "analysis.md"),
            "Analysis Markdown replay differs",
        )
    print(  # noqa: T201 -- explicit analysis CLI completion
        {
            "outcome": data["outcome"],
            "candidates": data["passing_candidates"],
            "operation": args.operation,
        }
    )


if __name__ == "__main__":
    main()
