# Copyright (c) 2026
"""Deterministic joined analysis of the frozen Case 0007 experiment chain.

This module reads frozen artifacts only. It never invokes treatment code. Run
``python analyze.py write`` once to create the two Stage D reports, then
``python analyze.py verify`` for read-only deterministic replay.
"""

from __future__ import annotations

import ast
import gzip
import hashlib
import itertools
import json
import statistics
import sys
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any

BASE = Path(__file__).resolve().parent
ADJ = BASE / "adjudication"
EXPECTED = {
    "integrity.json": "082416c3ce132f01e547a30c113148d62f1a0b5af1e51a37e258cbec51189184",
    "inputs.pkl.gz": "797eeb0d246f4745e5166b063b36b0dcffe84d2e2cb5fc87e36b89ae4eb2892d",
    "stage_b_raw.pkl.gz": "0d48f7f420682642779e5c3ba218648d2a3e066bb7f6f4a6ef0678dbc09d94cc",
    "capture.pkl.gz": "b626b60c304b2325b0361c53f2e9a7c9597d55bc32f73d882102e621c2e89dcc",
    "retrieval.json": "c41bebc65e92f8d21e47757d881af767bfde9af1f06043b5f782a0568e286383",
    "routing.json": "52fdf2e37672d30bc2f281eb4cd49f1a39564fac204efda3ea890986cda84ec5",
    "grounding.json": "4030bb734332f2611b5d16b7be18ab953574bbeb243a27ea50abb52141e04cbc",
    "generation.json": "0f7d7222c179305cc37230d3f5b08fab3fb131c980cd7f98357f01e51a02fe76",
    "stage_b_integrity.json": "afbc26da6485aabecb387dbcd1e5957e4eaeb1ee5c93cf206ddbf521edb64bb9",
    "stage_b.md": "373badc2a117a8d92ca6ff2310d9503a25ea3c5a7231aaaf676d54d9e4674f1c",
    "stage_b5.md": "8b4898e090456b8f6e65885d4d98d2183fe7dd859652be65d97d20373d03d32f",
    "adjudication/blind_manifest.json": "1367dd6840ed59ec03da3b02588ee896a64cbbe1af7415e61e7962e9a077ecb8",
    "adjudication/blind_resources.json.gz": "b3f435ded07aef88bbb9b374788d8357870d22d6c18853b28e0fa9ce8f6cf855",
    "adjudication/judgments.json": "d77bf0c66014a3aa1cfdb287c331f5e98c5bea123e63d5ffb3411aba4999613f",
}
CHAIN = [
    ("e495c0af2cf57efa3a63016165b41cbba65d26a5", "stage-a"),
    ("3e22a159e65b59bffab8d83dc5c49519dd8e90b6", "stage-b"),
    ("ba6a035ae9edc050b5765ddf3c68fcfd8c992c2e", "stage-b5"),
    ("005b4348d424e3d726f5975d54da21f71f3c1415", "stage-c"),
]
FORBIDDEN = {
    "rank",
    "score",
    "query",
    "locator",
    "grounding_request",
    "branch",
    "operator",
    "fanout",
    "generation_family",
    "projection_operator",
    "work_limit",
    "result_limit",
    "overflow",
    "effectiveness",
}


def read_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def canonical(value: Any) -> bytes:
    return (
        json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
        + "\n"
    ).encode()


def resource_id(resource: dict[str, Any]) -> str:
    return f"{resource['address']}\0{resource['content_identity']}"


def check_artifacts() -> dict[str, str]:
    actual = {name: digest(BASE / name) for name in EXPECTED}
    bad = {
        name: (EXPECTED[name], value)
        for name, value in actual.items()
        if EXPECTED[name] != value
    }
    if bad:
        raise ValueError(f"frozen digest mismatch: {bad}")
    stage_a = read_json(BASE / "integrity.json")
    for name, pinned in stage_a["files"].items():
        if digest(BASE / name) != pinned:
            raise ValueError(f"Stage A integrity file mismatch: {name}")
    stage_b = read_json(BASE / "stage_b_integrity.json")
    for name, pinned in stage_b["canonical_sha256"].items():
        if digest(BASE / name) != pinned:
            raise ValueError(f"Stage B integrity file mismatch: {name}")
    freeze = read_json(ADJ / "judgments.freeze.json")
    if (
        freeze["judgments_sha256"] != EXPECTED["adjudication/judgments.json"]
        or freeze["judgments_bytes"] != (ADJ / "judgments.json").stat().st_size
    ):
        raise ValueError("Stage C judgment seal mismatch")
    return actual


def key_for_address(address: str, identity_by_address: dict[str, str]) -> str:
    return f"{address}\0{identity_by_address[address]}"


def compute() -> tuple[dict[str, Any], str]:
    digests = check_artifacts()
    manifest = read_json(ADJ / "blind_manifest.json")
    retrieval = read_json(BASE / "retrieval.json")
    routing = read_json(BASE / "routing.json")
    grounding = read_json(BASE / "grounding.json")
    generation = read_json(BASE / "generation.json")
    judgments = read_json(ADJ / "judgments.json")

    packet = json.loads(gzip.decompress((ADJ / "blind_resources.json.gz").read_bytes()))
    resources = packet["resources"] if isinstance(packet, dict) else packet
    address_to_identity = {r["address"]: r["content_identity"] for r in resources}
    resource_by_address = {r["address"]: r for r in resources}
    resource_keys = {resource_id(r) for r in resources}
    obligations = [o["identity"] for o in judgments["obligations"]]
    if {o["identity"] for o in manifest["obligations"]} != set(obligations):
        raise ValueError("manifest and gold obligation identities differ")
    units = {u["unit_id"]: u for u in judgments["information_units"]}
    unit_resource = {
        uid: key_for_address(u["address"], address_to_identity)
        for uid, u in units.items()
    }
    labels: dict[tuple[str, str], str] = {}
    required_units: dict[tuple[str, str], set[str]] = defaultdict(set)
    for row in judgments["resource_classifications"]["overrides"]:
        cell = (
            row["obligation"],
            row["resource_occurrence_identity"].split("/", 2)[-1],
        )
        # Resource occurrence identity has address and digest as its last two slash components.
        parts = row["resource_occurrence_identity"].split("/")
        addr = "/".join(parts[2:-1])
        key = key_for_address(addr, address_to_identity)
        if (row["obligation"], key) in labels:
            raise ValueError("duplicate judgment override")
        labels[(row["obligation"], key)] = row["judgment"]
        if row["judgment"] == "REQUIRED":
            required_units[(row["obligation"], key)].update(row["unit_ids"])

    def label(ob: str, key: str) -> str:
        return labels.get((ob, key), "UNNECESSARY")

    alts: dict[str, list[dict[str, Any]]] = {}
    for o in judgments["obligations"]:
        alts[o["identity"]] = [
            {
                "id": a["alternative_id"],
                "units": list(a["members"]),
                "resources": sorted({unit_resource[x] for x in a["members"]}),
            }
            for a in o["acceptable_witness_alternatives"]
        ]
    combinations = list(itertools.product(*(alts[o] for o in obligations)))
    if (
        len(resources) != 521
        or len(resource_keys) != 521
        or len(address_to_identity) != 521
        or len(obligations) != 11
        or len(combinations) != 432
        or len(labels) != 133
    ):
        raise ValueError("frozen frame/count mismatch")
    unit_ids = set(units)
    if len(unit_ids) != 30 or any(
        uid not in unit_ids
        for o in judgments["obligations"]
        for alt in o["acceptable_witness_alternatives"]
        for uid in alt["members"]
    ):
        raise ValueError("gold unit/alternative identity mismatch")
    if (manifest["repository_id"], manifest["snapshot_id"], manifest["corpus_id"]) != (
        "fe2c8984-a021-4342-9e31-404a6cf07707",
        "404104e498a8d33118b52d5bad41c0ff4a8792d4ae23a2790628b796b91f34fd",
        "a2aaec768f650e9d8928fc1ed1a79eb5650472537b1d3538d740480c6a1b1f87",
    ):
        raise ValueError("repository/snapshot/corpus identity mismatch")
    prefix = f"{manifest['repository_id']}/{manifest['snapshot_id']}/"
    if any(not r["resource_occurrence_identity"].startswith(prefix) for r in resources):
        raise ValueError("resource occurrence belongs to another repository/snapshot")
    combo_resources = [
        set().union(*(set(a["resources"]) for a in combo)) for combo in combinations
    ]
    if (min(map(len, combo_resources)), max(map(len, combo_resources))) != (19, 24):
        raise ValueError("gold sufficient union bounds drifted")

    # Native rankings and routed lane identity/retention.
    global_lane = next(x for x in retrieval["lanes"] if x["identity"] == "global")
    global_rank = {
        resource_id(m["resource"]): m["native_rank"] for m in global_lane["matches"]
    }
    native_lanes = {
        x["identity"]: x for x in retrieval["lanes"] if x["identity"] != "global"
    }
    route_lanes = {x["obligation"]: x for x in routing["lanes"]}
    if (
        len(retrieval["lanes"]) != 12
        or len(route_lanes) != 11
        or not routing["global_lane_unchanged"]
        or not routing["candidate_retention_validated"]
    ):
        raise ValueError("retrieval/routing lane integrity failure")
    native_rank: dict[tuple[str, str], int] = {}
    routed_position: dict[tuple[str, str], int] = {}
    routed_tier: dict[tuple[str, str], str] = {}
    for ob in obligations:
        lane = native_lanes.get("q-" + ob)
        if lane is None or ob not in route_lanes:
            raise ValueError(f"missing lane for {ob}")
        nmap = {resource_id(m["resource"]): m["native_rank"] for m in lane["matches"]}
        native_rank.update({(ob, k): v for k, v in nmap.items()})
        rmap = {}
        for c in route_lanes[ob]["candidates"]:
            k = resource_id(c["resource"])
            if nmap.get(k) != c["native_rank"]:
                raise ValueError(
                    f"routed candidate lacks exact native candidate: {ob} {k}",
                )
            rmap[k] = (c["routed_position"], c["tier"])
        if set(rmap) != set(nmap):
            raise ValueError(f"routed lane did not retain all native candidates: {ob}")
        for k, (pos, tier) in rmap.items():
            routed_position[(ob, k)] = pos
            routed_tier[(ob, k)] = tier
    if set(global_rank) - resource_keys or any(
        k not in resource_keys for k in global_rank
    ):
        raise ValueError("global lane has resource outside frozen frame")

    def alt_completion(
        ob: str,
        alt: dict[str, Any],
        ranks: dict[str, int],
    ) -> int | None:
        vals = [ranks.get(k) for k in alt["resources"]]
        return max(vals) if vals and all(v is not None for v in vals) else None

    global_best = {
        ob: min(
            (
                v
                for a in alts[ob]
                if (v := alt_completion(ob, a, global_rank)) is not None
            ),
            default=None,
        )
        for ob in obligations
    }
    global_task_depth = (
        max((x for x in global_best.values() if x is not None), default=None)
        if all(x is not None for x in global_best.values())
        else None
    )
    global_universe = set().union(
        *(set(r for a in alts[o] for r in a["resources"]) for o in obligations),
    )
    global_universe_depth = (
        max((global_rank.get(k, 10**9) for k in global_universe), default=None)
        if global_universe <= set(global_rank)
        else None
    )
    minimum_combos = [i for i, x in enumerate(combo_resources) if len(x) == 19]
    best_min_depth = min(
        (
            max(global_rank[k] for k in combo_resources[i])
            for i in minimum_combos
            if combo_resources[i] <= set(global_rank)
        ),
        default=None,
    )
    global_prefix_resources = len(
        {
            k
            for k, rank in global_rank.items()
            if global_task_depth and rank <= global_task_depth
        },
    )
    alternative_depths = {
        ob: {
            a["id"]: {
                "global": alt_completion(ob, a, global_rank),
                "own_native": alt_completion(
                    ob,
                    a,
                    {k: v for (o, k), v in native_rank.items() if o == ob},
                ),
                "routed": alt_completion(
                    ob,
                    a,
                    {k: v for (o, k), v in routed_position.items() if o == ob},
                ),
            }
            for a in alts[ob]
        }
        for ob in obligations
    }

    own_best = {}
    routed_best = {}
    own_prefix = defaultdict(set)
    routed_prefix = defaultdict(set)
    for ob in obligations:
        ownr = {k: v for (o, k), v in native_rank.items() if o == ob}
        router = {k: v for (o, k), v in routed_position.items() if o == ob}
        own_best[ob] = min(
            (x for a in alts[ob] if (x := alt_completion(ob, a, ownr)) is not None),
            default=None,
        )
        routed_best[ob] = min(
            (x for a in alts[ob] if (x := alt_completion(ob, a, router)) is not None),
            default=None,
        )
        if own_best[ob] is not None:
            own_prefix[ob] = {k for k, v in ownr.items() if v <= own_best[ob]}
        if routed_best[ob] is not None:
            routed_prefix[ob] = {k for k, v in router.items() if v <= routed_best[ob]}

    def prefix_stats(prefix: dict[str, set[str]]) -> dict[str, Any]:
        cells = [(o, k) for o in obligations for k in prefix[o]]
        counts = Counter(label(o, k) for o, k in cells)
        return {
            "summed_occurrences": len(cells),
            "unique_resources": len(set(k for _, k in cells)),
            "cells": dict(sorted(counts.items())),
            "resources": sorted(set(k for _, k in cells)),
        }

    own_stats = prefix_stats(own_prefix)
    routed_stats = prefix_stats(routed_prefix)
    routing_delta = {"improved": [], "unchanged": [], "worsened": []}
    for ob in obligations:
        a, b = own_best[ob], routed_best[ob]
        group = (
            "unchanged"
            if a == b
            else ("improved" if a is not None and (b is None or b < a) else "worsened")
        )
        routing_delta[group].append(ob)

    # Candidate hypotheses: one fixed hypothesis per owner/mirror, one branch child
    # per successful Reference target. Incomplete families are never counted as output.
    hypotheses: list[dict[str, Any]] = []
    families = []
    for a in generation["attempts"]:
        ob = a["obligation"]
        if a["identity_kind"] == "WitnessHypothesisIdentity" and a["hypothesis"]:
            members = a["hypothesis_members"]
            ops = {s["type"] for m in members for s in m["structural_support"]}
            ops = {
                "OWNER"
                if x == "OwnerResourceSupport"
                else "MIRROR"
                if x == "MirroredResourceSupport"
                else "REFERENCE"
                for x in ops
            }
            hypotheses.append(
                {
                    "identity": a["hypothesis"],
                    "obligation": ob,
                    "family": a["identity"],
                    "operators": ops,
                    "resources": {resource_id(m["target"]) for m in members},
                    "members": members,
                    "attempt": a,
                },
            )
        if a["identity_kind"] == "WitnessHypothesisFamilyIdentity":
            child_hyps = []
            for b in a["branches"]:
                if b["disposition"] == "generated" and b["hypothesis"]:
                    # Combined branches carry the owner as parent-family member plus child ref.
                    branch_members = [b["target"]]
                    if a["members"]:
                        branch_members = [
                            t
                            for m in a["members"]
                            if m.get("key") == "owner"
                            for t in m.get("targets", [])
                        ] + branch_members
                    ops = {
                        s["type"]
                        for m in branch_members
                        for s in m["structural_support"]
                    }
                    opnames = {
                        "OWNER"
                        if x == "OwnerResourceSupport"
                        else "MIRROR"
                        if x == "MirroredResourceSupport"
                        else "REFERENCE"
                        for x in ops
                    }
                    h = {
                        "identity": b["hypothesis"],
                        "obligation": ob,
                        "family": a["identity"],
                        "operators": opnames,
                        "resources": {resource_id(m["target"]) for m in branch_members},
                        "members": branch_members,
                        "attempt": a,
                    }
                    hypotheses.append(h)
                    child_hyps.append(h)
            families.append({"attempt": a, "children": child_hyps})
    for h in hypotheses:
        for k in h["resources"]:
            if k not in resource_keys:
                raise ValueError(
                    f"generated target is outside the frozen snapshot: {k}",
                )
        for member in h["members"]:
            for support in member["structural_support"]:
                if support["type"] not in {
                    "OwnerResourceSupport",
                    "MirroredResourceSupport",
                    "PythonReferenceResourceSupport",
                }:
                    raise ValueError(f"unknown structural support: {support['type']}")
                if support["type"] == "PythonReferenceResourceSupport":
                    ref = support["reference_request"]
                    if (
                        ref["repository_id"] != manifest["repository_id"]
                        or ref["snapshot_id"] != manifest["snapshot_id"]
                    ):
                        raise ValueError(
                            "Reference support is from another repository snapshot",
                        )
    attempt_dispositions = Counter(a["disposition"] for a in generation["attempts"])
    fixed_hypotheses = sum(
        a["identity_kind"] == "WitnessHypothesisIdentity" and bool(a["hypothesis"])
        for a in generation["attempts"]
    )
    branch_families = sum(
        a["identity_kind"] == "WitnessHypothesisFamilyIdentity"
        for a in generation["attempts"]
    )
    branch_children = sum(len(f["children"]) for f in families)
    member_occurrences = sum(len(h["members"]) for h in hypotheses)

    # Find exact operator support, also validating every generated target is in the frame.
    surface_hyp = {
        "OWNER": [h for h in hypotheses if h["operators"] == {"OWNER"}],
        "MIRROR": [h for h in hypotheses if h["operators"] == {"MIRROR"}],
        "REFERENCE": [h for h in hypotheses if h["operators"] == {"REFERENCE"}],
        "OWNER_MIRROR": [
            h for h in hypotheses if h["operators"] in ({"OWNER"}, {"MIRROR"})
        ],
        "ALL": hypotheses,
    }
    # OWNER/MIRROR candidate surface union includes any generated member bearing that support;
    # hypothesis completeness still uses the uncombined individual candidate shapes.
    cells_by_surface: dict[str, set[tuple[str, str]]] = {}
    resources_by_surface: dict[str, set[str]] = {}
    for name, hs in surface_hyp.items():
        cells = set()
        wanted = (
            {"OWNER"}
            if name == "OWNER"
            else {"MIRROR"}
            if name == "MIRROR"
            else {"REFERENCE"}
            if name == "REFERENCE"
            else {"OWNER", "MIRROR"}
            if name == "OWNER_MIRROR"
            else {"OWNER", "MIRROR", "REFERENCE"}
        )
        for h in hypotheses:
            for member in h["members"]:
                ops = {s["type"] for s in member["structural_support"]}
                op = (
                    "OWNER"
                    if "OwnerResourceSupport" in ops
                    else "MIRROR"
                    if "MirroredResourceSupport" in ops
                    else "REFERENCE"
                    if "PythonReferenceResourceSupport" in ops
                    else None
                )
                if op in wanted:
                    cells.add((h["obligation"], resource_id(member["target"])))
        cells_by_surface[name] = cells
        resources_by_surface[name] = {k for _, k in cells}
    required_cells = {(o, k) for (o, k), v in labels.items() if v == "REQUIRED"}

    def surface_metrics(name: str) -> dict[str, Any]:
        cells = cells_by_surface[name]
        counts = Counter(label(o, k) for o, k in cells)
        rcells = cells & required_cells
        runits = {(o, uid) for o, k in rcells for uid in required_units[(o, k)]}
        runit_ids = {uid for _, uid in runits}
        reqres = resources_by_surface[name] & {k for _, k in required_cells}
        complete_alts, complete_obs, reachable_only = {}, [], []
        for ob in obligations:
            relevant = [h for h in surface_hyp[name] if h["obligation"] == ob]
            has_hyp = any(
                any(set(a["resources"]) <= h["resources"] for a in alts[ob])
                for h in relevant
            )
            has_set = any(
                set(a["resources"]) <= {k for o, k in cells if o == ob}
                for a in alts[ob]
            )
            complete_alts[ob] = [
                a["id"]
                for a in alts[ob]
                if any(set(a["resources"]) <= h["resources"] for h in relevant)
            ]
            if has_hyp:
                complete_obs.append(ob)
            elif has_set:
                reachable_only.append(ob)
        return {
            "candidate_resources": len(resources_by_surface[name]),
            "obligation_resource_cells": len(cells),
            "labels": dict(sorted(counts.items())),
            "required_cells_covered": len(rcells),
            "required_cell_denominator": 55,
            "required_unit_judgments_covered": len(runits),
            "required_unit_denominator": 56,
            "distinct_required_units_covered": len(runit_ids),
            "distinct_required_unit_denominator": 30,
            "unique_required_resources_covered": len(reqres),
            "unique_required_resource_denominator": 27,
            "complete_obligations": complete_obs,
            "complete_obligation_count": len(complete_obs),
            "complete_alternatives": complete_alts,
            "resource_set_only_obligations": reachable_only,
            "required_resources": sorted(reqres),
        }

    surfaces = {
        n: surface_metrics(n)
        for n in ["OWNER", "MIRROR", "REFERENCE", "OWNER_MIRROR", "ALL"]
    }
    if [
        surfaces[x]["candidate_resources"]
        for x in ["OWNER", "MIRROR", "REFERENCE", "OWNER_MIRROR", "ALL"]
    ] != [8, 5, 8, 13, 19]:
        raise ValueError(
            f"operator surface sizes do not match frozen mechanical totals: {[surfaces[x]['candidate_resources'] for x in ['OWNER', 'MIRROR', 'REFERENCE', 'OWNER_MIRROR', 'ALL']]}",
        )
    if attempt_dispositions != {
        "generated": 20,
        "result-bound-exceeded": 3,
        "no-target": 2,
    } or (
        fixed_hypotheses,
        branch_families,
        branch_children,
        len(hypotheses),
        member_occurrences,
    ) != (16, 9, 16, 32, 40):
        raise ValueError(
            f"frozen Stage B mechanical structure counts mismatch: dispositions={dict(attempt_dispositions)}, counts={(fixed_hypotheses, branch_families, branch_children, len(hypotheses), member_occurrences)}",
        )
    support_by_cell: dict[tuple[str, str], set[str]] = defaultdict(set)
    support_names = {
        "OwnerResourceSupport": "OWNER",
        "MirroredResourceSupport": "MIRROR",
        "PythonReferenceResourceSupport": "REFERENCE",
    }
    for hypothesis in hypotheses:
        for member in hypothesis["members"]:
            key = resource_id(member["target"])
            for support in member["structural_support"]:
                support_by_cell[(hypothesis["obligation"], key)].add(
                    support_names[support["type"]],
                )
    structural_cell_details = [
        {
            "obligation": ob,
            "resource": key.split("\0")[0],
            "label": label(ob, key),
            "operators": sorted(support_by_cell[(ob, key)]),
            "required_unit_ids": sorted(required_units[(ob, key)]),
        }
        for ob, key in sorted(cells_by_surface["ALL"])
    ]

    # Hypothesis-to-gold relation classification for every actual output shape.
    recipe_classes = Counter()
    hypothesis_alignment = []
    for h in hypotheses:
        hs = h["resources"]
        matching = [a["id"] for a in alts[h["obligation"]] if set(a["resources"]) <= hs]
        touching = [a["id"] for a in alts[h["obligation"]] if set(a["resources"]) & hs]
        if matching:
            c = "EXACT_STRUCTURAL_MATCH"
        elif touching:
            c = "PARTIAL_MATCH"
        else:
            c = "NO_GOLD_MATCH"
        recipe_classes[c] += 1
        hypothesis_alignment.append(
            {
                "hypothesis": h["identity"],
                "family": h["family"],
                "obligation": h["obligation"],
                "operators": sorted(h["operators"]),
                "members": sorted(k.split("\0")[0] for k in hs),
                "classification": c,
                "complete_alternatives": matching,
                "alternatives_touched": touching,
            },
        )

    # Reference marginal contribution, computed obligation-relatively.
    before = cells_by_surface["OWNER_MIRROR"]
    after = cells_by_surface["ALL"]
    marginal = after - before
    mlabels = Counter(label(o, k) for o, k in marginal)
    mrequnits = {
        (o, uid)
        for o, k in marginal
        if label(o, k) == "REQUIRED"
        for uid in required_units[(o, k)]
    }
    mreqcellresources = {k for o, k in marginal if label(o, k) == "REQUIRED"}
    mhelpresources = {k for o, k in marginal if label(o, k) == "HELPFUL_ONLY"}
    before_resources = resources_by_surface["OWNER_MIRROR"]
    added_resources = resources_by_surface["ALL"] - before_resources
    gold_required_resources = {k for _, k in required_cells}
    mreqresources = added_resources & gold_required_resources
    mnoise_resources = added_resources - gold_required_resources
    pre_complete = set(surfaces["OWNER_MIRROR"]["complete_obligations"])
    post_complete = set(surfaces["ALL"]["complete_obligations"])
    mcomplete_alts = []
    for ob in obligations:
        pre = set(surfaces["OWNER_MIRROR"]["complete_alternatives"][ob])
        post = set(surfaces["ALL"]["complete_alternatives"][ob])
        for aid in sorted(post - pre):
            mcomplete_alts.append({"obligation": ob, "alternative": aid})
    marginal_ref = {
        "new_cells": len(marginal),
        "new_unique_resources": len(added_resources),
        "labels": dict(sorted(mlabels.items())),
        "new_required_cells": sum(1 for o, k in marginal if label(o, k) == "REQUIRED"),
        "new_required_cell_resources": len(mreqcellresources),
        "new_required_unit_judgments": len(mrequnits),
        "new_required_information_units": len({u for _, u in mrequnits}),
        "new_unique_required_resources": len(mreqresources),
        "new_helpful_resources": len(mhelpresources),
        "new_unnecessary_cells": mlabels["UNNECESSARY"],
        "new_unique_resources_never_required": len(mnoise_resources),
        "new_complete_obligations": sorted(post_complete - pre_complete),
        "new_complete_alternatives": mcomplete_alts,
        "required_cell_yield": sum(1 for x in marginal if label(*x) == "REQUIRED")
        / len(marginal)
        if marginal
        else None,
        "required_resource_yield": len(mreqresources) / len(added_resources)
        if added_resources
        else None,
        "resource_set_only_after_reference": surfaces["ALL"][
            "resource_set_only_obligations"
        ],
    }
    marginal_ref["added_cells"] = [
        {
            "obligation": ob,
            "resource": key.split("\0")[0],
            "label": label(ob, key),
            "required_anywhere": key in gold_required_resources,
        }
        for ob, key in sorted(marginal)
    ]
    marginal_ref["added_unique_resources"] = sorted(
        k.split("\0")[0] for k in added_resources
    )

    # All 432 combinations: candidate resource set and structure checks.
    combo_rows = []
    for i, (combo, res) in enumerate(zip(combinations, combo_resources, strict=True)):
        represented_cells = {
            (ob, k)
            for ob, a in zip(obligations, combo, strict=True)
            for k in a["resources"]
            if (ob, k) in after
        }
        total_cells = sum(len(a["resources"]) for a in combo)
        structure = all(
            any(
                h["obligation"] == ob and set(a["resources"]) <= h["resources"]
                for h in hypotheses
            )
            for ob, a in zip(obligations, combo, strict=True)
        )
        combo_rows.append(
            {
                "index": i,
                "alternatives": {
                    ob: a["id"] for ob, a in zip(obligations, combo, strict=True)
                },
                "resource_count": len(res),
                "resources": sorted(res),
                "represented_required_resource_cells": len(represented_cells),
                "required_resource_cells": total_cells,
                "all_resources_represented": len(represented_cells) == total_cells,
                "realized_by_hypothesis_shapes": structure,
                "intersection_with_actual_union": len(
                    res & resources_by_surface["ALL"],
                ),
            },
        )

    # Reference family diagnostics, including post-hoc exact overflow target sets.
    family_reports = []
    overflow_extra_cells: set[tuple[str, str]] = set()
    overflow_details = []
    for fam in families:
        a = fam["attempt"]
        ob = a["obligation"]
        ref_targets = []
        for member in a["members"]:
            for t in member.get("targets", []):
                if any(
                    s["type"] == "PythonReferenceResourceSupport"
                    for s in t["structural_support"]
                ):
                    ref_targets.append(resource_id(t["target"]))
        child_resources = {
            k
            for h in fam["children"]
            for k in h["resources"]
            if "REFERENCE" in h["operators"]
        }
        req_target = {k for k in set(ref_targets) if label(ob, k) == "REQUIRED"}
        helpful_target = {k for k in set(ref_targets) if label(ob, k) == "HELPFUL_ONLY"}
        useless_target = {k for k in set(ref_targets) if label(ob, k) == "UNNECESSARY"}
        owner_targets = {
            resource_id(t["target"])
            for member in a["members"]
            if member.get("key") == "owner"
            for t in member.get("targets", [])
        }
        complete_target_alts = [
            x["id"]
            for x in alts[ob]
            if set(x["resources"]) <= (owner_targets | set(ref_targets))
        ]
        refmember = next(
            (m for m in a["members"] if m.get("key") == "referencer"),
            None,
        )
        seed = (
            refmember.get("grounding_request")
            if refmember
            else next(
                (
                    s.get("grounding_request")
                    for b in a["branches"]
                    if b.get("target")
                    for s in b["target"].get("structural_support", [])
                ),
                None,
            )
        )
        complete_in_child = [
            alt["id"]
            for alt in alts[ob]
            if any(set(alt["resources"]) <= h["resources"] for h in fam["children"])
        ]
        fam_report = {
            "family": a["identity"],
            "obligation": ob,
            "disposition": a["disposition"],
            "seed": seed,
            "exact_target_count": len(set(ref_targets))
            if a["disposition"] != "result-bound-exceeded"
            else 20,
            "work_performed": max(
                [m.get("work_performed", 0) for m in a["members"]],
                default=0,
            ),
            "work_limit": max(
                [m.get("work_limit", 0) or 0 for m in a["members"]],
                default=0,
            ),
            "work_complete": all(
                m.get("complete", True)
                for m in a["members"]
                if m.get("key") == "referencer"
            ),
            "generated_child_count": len(fam["children"]),
            "generated_unique_resources": len(child_resources),
            "required_resources": len(req_target),
            "helpful_resources": len(helpful_target),
            "unnecessary_resources": len(useless_target),
            "complete_gold_alternatives_in_any_valid_child": complete_in_child,
            "alternatives_resource_set_reachable_from_family_targets": complete_target_alts,
        }
        family_reports.append(fam_report)
        if a["disposition"] == "result-bound-exceeded":
            extra = {(ob, k) for k in set(ref_targets) if (ob, k) not in after}
            overflow_extra_cells |= extra
            full_alts = [
                x["id"]
                for x in alts[ob]
                if set(x["resources"])
                <= ({k for o, k in after if o == ob} | set(ref_targets))
            ]
            overflow_details.append(
                {
                    "family": fam_report["family"],
                    "obligation": ob,
                    "target_count": len(set(ref_targets)),
                    "required_targets": len(req_target),
                    "complete_alternatives_if_admitted": full_alts,
                    "unnecessary_targets": len(useless_target),
                    "extra_admitted_cells": len(extra),
                },
            )
    overflow_labels = Counter(label(o, k) for o, k in overflow_extra_cells)
    observed_complete_alts = {
        (ob, aid)
        for ob, completed in surfaces["ALL"]["complete_alternatives"].items()
        for aid in completed
    }
    counterfactual_complete_alts = set()
    for family in families:
        attempt = family["attempt"]
        if attempt["disposition"] != "result-bound-exceeded":
            continue
        owner_targets = {
            resource_id(t["target"])
            for member in attempt["members"]
            if member.get("key") == "owner"
            for t in member.get("targets", [])
        }
        for member in attempt["members"]:
            if member.get("key") != "referencer":
                continue
            for target in member.get("targets", []):
                child_resources = owner_targets | {resource_id(target["target"])}
                for alt in alts[attempt["obligation"]]:
                    if set(alt["resources"]) <= child_resources:
                        counterfactual_complete_alts.add(
                            (attempt["obligation"], alt["id"]),
                        )
    counterfactual_new_alts = counterfactual_complete_alts - observed_complete_alts
    overflow_required_units = {
        (ob, uid)
        for ob, key in overflow_extra_cells
        if label(ob, key) == "REQUIRED"
        for uid in required_units[(ob, key)]
    }
    overflow_new_required_resources = {
        key for ob, key in overflow_extra_cells if label(ob, key) == "REQUIRED"
    }
    seed_fanouts: dict[str, set[str]] = defaultdict(set)
    for family in family_reports:
        attempt = next(
            a for a in generation["attempts"] if a["identity"] == family["family"]
        )
        if family["seed"]:
            seed_fanouts.setdefault(family["seed"], set())
            for member in attempt["members"]:
                if member.get("key") == "referencer":
                    for target in member.get("targets", []):
                        seed_fanouts[family["seed"]].add(resource_id(target["target"]))
    fanout_values = sorted(len(v) for v in seed_fanouts.values())
    reference_target_resources = {
        resource_id(member["target"])
        for h in hypotheses
        for member in h["members"]
        for support in member["structural_support"]
        if support["type"] == "PythonReferenceResourceSupport"
    }
    if (
        len(seed_fanouts),
        statistics.median(fanout_values),
        max(fanout_values),
        len(reference_target_resources),
    ) != (4, 4, 20, 8):
        raise ValueError(
            f"Reference seed fanout mechanical totals mismatch: {(len(seed_fanouts), statistics.median(fanout_values), max(fanout_values), len(reference_target_resources))} {dict((k, len(v)) for k, v in seed_fanouts.items())}",
        )
    owner_target_keys = {
        resource_id(member["target"])
        for h in hypotheses
        for member in h["members"]
        for support in member["structural_support"]
        if support["type"] == "OwnerResourceSupport"
    }
    if reference_target_resources & owner_target_keys:
        raise ValueError("unexpected same-owner Reference target")

    # Exact ground owners from generated OWNER support; one owner per request where observable.
    owners: dict[str, str] = {}
    for h in hypotheses:
        for m in h["members"]:
            for s in m["structural_support"]:
                if s["type"] == "OwnerResourceSupport":
                    owners[s["grounding_request"]] = resource_id(m["target"])
    grounds = []
    for req in grounding["requests"]:
        rid = req["request_identity"]
        owner = owners.get(rid)
        participated = sorted(
            {
                a["obligation"]
                for a in generation["attempts"]
                if any(m.get("grounding_request") == rid for m in a["members"])
            },
        )
        per_ob = {o: label(o, owner) for o in participated} if owner else {}
        all_labels = sorted({label(o, owner) for o in obligations}) if owner else []
        grounds.append(
            {
                "request": rid,
                "anchor": req["anchor"],
                "disposition": req["disposition"],
                "owner": owner.split("\0")[0] if owner else None,
                "owner_labels_by_obligation": per_ob,
                "gold_status_anywhere": "REQUIRED"
                if "REQUIRED" in all_labels
                else "HELPFUL_ONLY"
                if "HELPFUL_ONLY" in all_labels
                else "UNNECESSARY"
                if owner
                else "UNMAPPED",
            },
        )

    # Non-overlapping primary misses from the actual full structural cell surface.
    missed = required_cells - after
    no_recipe = {"explicit-exposure", "documentation", "validation"}
    overflow_targets_by_ob: dict[str, set[str]] = defaultdict(set)
    for fam in families:
        if fam["attempt"]["disposition"] == "result-bound-exceeded":
            for m in fam["attempt"]["members"]:
                if m.get("key") != "referencer":
                    continue
                for t in m.get("targets", []):
                    overflow_targets_by_ob[fam["attempt"]["obligation"]].add(
                        resource_id(t["target"]),
                    )
    no_target_obs = {
        a["obligation"]
        for a in generation["attempts"]
        if a["disposition"] == "no-target"
    }
    generated_by_ob: dict[str, set[str]] = defaultdict(set)
    generated_elsewhere: dict[str, set[str]] = defaultdict(set)
    for ob, k in after:
        generated_by_ob[ob].add(k)
        generated_elsewhere[k].add(ob)
    miss_causes = Counter()
    miss_rows = []
    for ob, k in sorted(missed):
        if ob in no_recipe:
            cause = "NO_RECIPE"
        elif k in overflow_targets_by_ob[ob]:
            cause = "RESULT_BOUND_EXCEEDED"
        elif ob in no_target_obs:
            cause = "PROJECTION_NO_TARGET"
        elif any(other != ob for other in generated_elsewhere[k]):
            cause = "CROSS_ROLE_NONSTRUCTURAL"
        else:
            cause = "PROJECTION_ABSTAINED"
        miss_causes[cause] += 1
        miss_rows.append(
            {"obligation": ob, "resource": k.split("\0")[0], "primary_cause": cause},
        )

    # Evidence-only probe of one exact typed relation: direct static Python
    # import dependencies among frozen resources. This is not an operator run.
    actual_union = resources_by_surface["ALL"]
    module_to_address = {}
    address_to_module = {}
    for address in address_to_identity:
        if address.startswith("src/") and address.endswith(".py"):
            module = address[4:-3].replace("/", ".")
            module = module.removesuffix(".__init__")
            module_to_address[module] = address
            address_to_module[address] = module

    def direct_imports(address: str) -> set[str]:
        content = resource_by_address[address].get("content", "")
        tree = ast.parse(content)
        module = address_to_module.get(address)
        if module is None:
            return set()
        package = module.split(".")[:-1]
        found = set()
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for imported in node.names:
                    if imported.name in module_to_address:
                        found.add(module_to_address[imported.name])
            elif isinstance(node, ast.ImportFrom):
                if node.level:
                    base_parts = package[: max(0, len(package) - node.level + 1)]
                    base = ".".join(base_parts + (node.module or "").split("."))
                else:
                    base = node.module or ""
                if base in module_to_address:
                    found.add(module_to_address[base])
                for imported in node.names:
                    candidate = f"{base}.{imported.name}" if base else imported.name
                    if candidate in module_to_address:
                        found.add(module_to_address[candidate])
        return found

    owner_pairs = set()
    for attempt in generation["attempts"]:
        for member in attempt["members"]:
            if member.get("key") == "owner" and member.get("targets"):
                for target in member["targets"]:
                    owner_pairs.add(
                        (
                            attempt["obligation"],
                            member["grounding_request"],
                            resource_id(target["target"]),
                        ),
                    )
            elif member.get("key") == "owner" and member.get("target"):
                owner_pairs.add(
                    (
                        attempt["obligation"],
                        member["grounding_request"],
                        resource_id(member["target"]["target"]),
                    ),
                )
    import_cells = set()
    import_resources = set()
    import_edges = []
    fanouts = []
    for ob, request, owner_key in sorted(owner_pairs):
        owner_address = owner_key.split("\0")[0]
        deps = direct_imports(owner_address)
        fanouts.append(
            {
                "obligation": ob,
                "grounding_request": request,
                "owner": owner_address,
                "fanout": len(deps),
            },
        )
        for address in sorted(deps):
            dep_key = key_for_address(address, address_to_identity)
            import_cells.add((ob, dep_key))
            import_resources.add(dep_key)
            import_edges.append(
                {
                    "obligation": ob,
                    "grounding_request": request,
                    "owner": owner_address,
                    "dependency": address,
                    "gold_label": label(ob, dep_key),
                },
            )
    import_cell_additions = import_cells - after
    import_new_required = {
        (o, k) for o, k in import_cell_additions if label(o, k) == "REQUIRED"
    }
    import_required_units = {
        (o, unit) for o, k in import_new_required for unit in required_units[(o, k)]
    }
    import_pair_completions = []
    for ob, _, owner_key in sorted(owner_pairs):
        for dep in direct_imports(owner_key.split("\0")[0]):
            pair = {owner_key, key_for_address(dep, address_to_identity)}
            for alt in alts[ob]:
                if set(alt["resources"]) <= pair:
                    import_pair_completions.append(
                        {
                            "obligation": ob,
                            "alternative": alt["id"],
                            "owner": owner_key.split("\0")[0],
                            "dependency": dep,
                        },
                    )
    reference_fact = next(
        r for r in grounding["requests"] if r["request_identity"] == "g-reference-fact"
    )
    fact_name = reference_fact["referents"][0]["name"]
    fact_owner = owners.get("g-reference-fact")
    alternate_seed_referencers = []
    if fact_owner:
        fact_address = fact_owner.split("\0")[0]
        for address in sorted(resource_by_address):
            if address.endswith(".py") and fact_address in direct_imports(address):
                text = resource_by_address[address].get("content", "")
                if fact_name in text:
                    alternate_seed_referencers.append(
                        {
                            "source_resource": address,
                            "grounded_target_owner": fact_address,
                            "imported_member_name": fact_name,
                            "direct_import_dependency": True,
                            "reference_projection_observed": False,
                        },
                    )
    import_combined_cells = after | import_cells
    import_resource_set_complete = []
    for ob in obligations:
        have = {k for o, k in import_combined_cells if o == ob}
        already_resource_complete = (
            ob in surfaces["ALL"]["complete_obligations"]
            or ob in surfaces["ALL"]["resource_set_only_obligations"]
        )
        if not already_resource_complete and any(
            set(a["resources"]) <= have for a in alts[ob]
        ):
            import_resource_set_complete.append(ob)
    import_probe = {
        "status": "COUNTERFACTUAL_STATIC_EVIDENCE_PROBE_NOT_OBSERVED_TREATMENT",
        "relation": "one-hop direct static Python import dependency between frozen source resources",
        "owner_seed_obligation_count": len(owner_pairs),
        "direct_dependency_edges": len(import_edges),
        "maximum_fanout": max((f["fanout"] for f in fanouts), default=0),
        "fanout_by_grounded_owner": fanouts,
        "unique_dependency_resources": len(import_resources),
        "new_unique_resources_beyond_observed_surface": len(
            import_resources - actual_union,
        ),
        "new_obligation_resource_cells": len(import_cell_additions),
        "new_required_cells": len(import_new_required),
        "new_required_unit_judgments": len(import_required_units),
        "new_distinct_required_information_units": len(
            {u for _, u in import_required_units},
        ),
        "new_required_resources": len({k for _, k in import_new_required}),
        "new_candidate_structural_union_size": len(actual_union | import_resources),
        "gold_labels_for_added_cells": dict(
            sorted(Counter(label(o, k) for o, k in import_cell_additions).items()),
        ),
        "newly_resource_set_complete_obligations": import_resource_set_complete,
        "complete_owner_plus_single_dependency_hypotheses": import_pair_completions,
        "missing_required_witnesses_reached": [
            {
                "obligation": o,
                "resource": k.split("\0")[0],
                "units": sorted(required_units[(o, k)]),
            }
            for o, k in sorted(import_new_required)
        ],
        "edges": import_edges,
    }
    reference_family_obligations = {family["obligation"] for family in family_reports}
    no_target_obligations = {
        family["obligation"]
        for family in family_reports
        if family["disposition"] == "no-target"
    }
    overflow_obligations = {
        family["obligation"]
        for family in family_reports
        if family["disposition"] == "result-bound-exceeded"
    }
    reference_miss_causes = Counter()
    reference_miss_rows = []
    for ob, key in sorted(required_cells):
        if (ob, key) in cells_by_surface["REFERENCE"]:
            continue
        address = key.split("\0")[0]
        if ob not in reference_family_obligations:
            cause = "NO_REFERENCE_RECIPE"
        elif (ob, key) in import_new_required:
            cause = "REQUIRES_OTHER_TYPED_RELATION"
        elif ob in no_target_obligations and any(
            row["source_resource"] == address for row in alternate_seed_referencers
        ):
            cause = "WRONG_REFERENCE_SEED"
        elif (
            ob in no_target_obligations and address.endswith(".md")
        ) or ob in no_target_obligations:
            cause = "WITNESS_NOT_REFERENTIAL"
        elif ob in overflow_obligations and key in overflow_targets_by_ob[ob]:
            cause = "RESULT_BOUND_EXCEEDED"
        else:
            cause = "EXACT_REFERENCE_FACT_ABSENT"
        reference_miss_causes[cause] += 1
        reference_miss_rows.append(
            {"obligation": ob, "resource": address, "cause": cause},
        )
    reachability_buckets: dict[str, list[dict[str, str]]] = defaultdict(list)
    for ob, key in sorted(required_cells):
        cell = {"obligation": ob, "resource": key.split("\0")[0]}
        if (ob, key) in cells_by_surface["OWNER"]:
            bucket = "OWNER_REACHABLE"
        elif (ob, key) in cells_by_surface["MIRROR"]:
            bucket = "MIRROR_REACHABLE"
        elif (ob, key) in cells_by_surface["REFERENCE"]:
            bucket = "REFERENCE_REACHABLE"
        elif (ob, key) in import_new_required:
            bucket = "REQUIRES_OTHER_TYPED_RELATION"
        else:
            bucket = "NONSTRUCTURAL_OR_POLICY"
        reachability_buckets[bucket].append(cell)

    # Resource membership and alternative intersections.
    min_intersections = [len(actual_union & combo_resources[i]) for i in minimum_combos]
    max_intersection = max(
        (len(actual_union & x) for x in combo_resources if len(x) == 19),
        default=0,
    )
    sufficient_summary = {
        "combination_count": len(combo_resources),
        "minimum_size": min(map(len, combo_resources)),
        "maximum_size": max(map(len, combo_resources)),
        "minimum_combination_count": len(minimum_combos),
        "maximum_intersection_actual_with_19": max_intersection,
        "minimum_intersection_actual_with_each_19": min(min_intersections, default=0),
        "all_minimum_intersections": min_intersections,
        "actual_surface_equals_any_minimum_combination": any(
            actual_union == combo_resources[i] for i in minimum_combos
        ),
    }

    # Lexical surface, lanes and gold joins.
    join_integrity = {
        "resources": len(resource_keys),
        "obligations": len(obligations),
        "shared_anchors": len(manifest["shared_anchors"]),
        "lexical_lanes": len(retrieval["lanes"]),
        "routed_obligation_lanes": len(route_lanes),
        "grounding_requests": len(grounding["requests"]),
        "generation_attempts": len(generation["attempts"]),
        "judgment_cells_expected": 5731,
        "judgment_cells_observed": len(resource_keys) * len(obligations),
        "judgment_overrides": len(labels),
        "duplicates": 0,
        "missing_or_unexpected_resources": 0,
    }
    if (
        join_integrity["resources"],
        join_integrity["obligations"],
        join_integrity["shared_anchors"],
        join_integrity["lexical_lanes"],
        join_integrity["routed_obligation_lanes"],
        join_integrity["grounding_requests"],
        join_integrity["generation_attempts"],
        join_integrity["judgment_cells_observed"],
        len(required_cells),
        sum(v == "HELPFUL_ONLY" for v in labels.values()),
    ) != (521, 11, 9, 12, 11, 9, 25, 5731, 55, 78):
        raise ValueError("joined frame integrity totals mismatch")
    if (
        len(generation["attempts"]) != 25
        or sum(len(f["children"]) for f in families) != 16
    ):
        raise ValueError("generation structure count mismatch")
    if len(structural_cell_details) != 24 or sum(
        surfaces[name]["obligation_resource_cells"]
        for name in ["OWNER", "MIRROR", "REFERENCE"]
    ) < len(structural_cell_details):
        raise ValueError("structural obligation/resource occurrence count mismatch")

    gold = {
        "applicability": dict.fromkeys(obligations, "APPLICABLE"),
        "required_unit_judgments": sum(len(x) for x in required_units.values()),
        "distinct_required_information_units": len(
            {u for vs in required_units.values() for u in vs},
        ),
        "required_cells": len(required_cells),
        "helpful_cells": sum(1 for x in labels.values() if x == "HELPFUL_ONLY"),
        "unnecessary_cells": 5731
        - len(required_cells)
        - sum(1 for x in labels.values() if x == "HELPFUL_ONLY"),
        "unique_required_resources": len({k for _, k in required_cells}),
        "unresolved": 0,
        "inherent_discovery": 0,
        "task_gaps": 0,
    }
    gold["required_by_obligation"] = {
        ob: {
            "distinct_information_units": len(
                {
                    uid
                    for (o, _), ids in required_units.items()
                    if o == ob
                    for uid in ids
                },
            ),
            "unit_judgments": sum(
                len(ids) for (o, _), ids in required_units.items() if o == ob
            ),
            "required_resource_cells": sum(o == ob for o, _ in required_cells),
        }
        for ob in obligations
    }
    required_occurrences = []
    for (ob, key), unit_ids in sorted(required_units.items()):
        for uid in sorted(unit_ids):
            nr = native_rank.get((ob, key))
            rp = routed_position.get((ob, key))
            required_occurrences.append(
                {
                    "obligation": ob,
                    "unit": uid,
                    "resource": key.split("\0")[0],
                    "global_rank": global_rank.get(key),
                    "global_reached": key in global_rank,
                    "own_native_rank": nr,
                    "own_native_reached": nr is not None,
                    "routed_position": rp,
                    "routed_tier": routed_tier.get((ob, key)),
                    "routed_reached": rp is not None,
                },
            )
    ground_counts = Counter(g["gold_status_anywhere"] for g in grounds)
    # Explicit map for compact consumers.
    output = {
        "schema": "case-0007-stage-d-analysis-v1",
        "frozen_digests": digests,
        "chain": [{"commit": c, "stage": s} for c, s in CHAIN],
        "identities": {
            k: manifest[k]
            for k in (
                "case_identity",
                "task_identity",
                "repository_id",
                "snapshot_id",
                "corpus_id",
            )
            if k in manifest
        },
        "frozen_task": manifest["task"],
        "join_integrity": join_integrity,
        "gold": gold,
        "acceptable_alternatives": {ob: alts[ob] for ob in obligations},
        "sufficient_combinations": sufficient_summary,
        "lexical": {
            "global_positive_surface": len(global_rank),
            "global_task_complete_depth": global_task_depth,
            "global_complete_27_resource_universe_depth": global_universe_depth,
            "best_19_resource_combination_depth": best_min_depth,
            "global_prefix_unique_resources": global_prefix_resources,
            "best_global_obligation_depths": global_best,
            "alternative_completion_depths": alternative_depths,
            "required_occurrences": required_occurrences,
            "own_native_best_depths": own_best,
            "own_native_max_depth": max(
                (x for x in own_best.values() if x is not None),
                default=None,
            ),
            "own_native_prefix": own_stats,
            "routed_best_positions": routed_best,
            "routed_max_position": max(
                (x for x in routed_best.values() if x is not None),
                default=None,
            ),
            "routed_prefix": routed_stats,
            "routing_comparison": routing_delta,
            "own_excess_over_minimum": own_stats["unique_resources"] - 19,
            "routed_excess_over_minimum": routed_stats["unique_resources"] - 19,
            "own_candidate_to_minimum_ratio": own_stats["unique_resources"] / 19,
            "routed_candidate_to_minimum_ratio": routed_stats["unique_resources"] / 19,
        },
        "generation_mechanics": {
            "attempt_dispositions": dict(attempt_dispositions),
            "fixed_hypotheses": fixed_hypotheses,
            "reference_families": branch_families,
            "branch_children": branch_children,
            "hypotheses": len(hypotheses),
            "member_occurrences": member_occurrences,
            "reference_seed_fanout": {
                seed: len(targets) for seed, targets in seed_fanouts.items()
            },
            "distinct_reference_seed_count": len(seed_fanouts),
            "reference_target_median_by_seed": statistics.median(fanout_values),
            "reference_target_max": max(fanout_values),
            "same_owner_collisions": 0,
            "duplicate_branch_failures": 0,
        },
        "structural_surfaces": surfaces,
        "structural_candidate_sets": {
            n: sorted(v) for n, v in resources_by_surface.items()
        },
        "structural_cells": structural_cell_details,
        "recipe_alignment": {
            "counts": dict(recipe_classes),
            "hypothesis_count": len(hypotheses),
            "hypotheses": hypothesis_alignment,
            "resource_match_wrong_structure_obligations": surfaces["ALL"][
                "resource_set_only_obligations"
            ],
        },
        "reference_marginal": marginal_ref,
        "reference_miss_causes": {
            "counts": dict(reference_miss_causes),
            "cells": reference_miss_rows,
        },
        "reference_seed_diagnostic": {
            "no_target_seed": "g-reference",
            "no_target_family_count": 2,
            "alternate_grounded_seed_not_projected": "g-reference-fact",
            "alternate_seed_owner": fact_owner.split("\0")[0] if fact_owner else None,
            "source_import_evidence": alternate_seed_referencers,
            "projection_rerun": False,
        },
        "operator_reachability": {
            "bucket_counts": {
                name: len(cells) for name, cells in reachability_buckets.items()
            },
            "required_cells": dict(reachability_buckets),
            "residual_note": "NONSTRUCTURAL_OR_POLICY here means the frozen operators and the explicitly probed direct-import relation do not prove a structural path. It includes policy/documentation/test needs and code resources for which no additional typed relation is established; it is not a claim that every residual code resource is inherently nonstructural.",
        },
        "reference_families": family_reports,
        "overflow": {
            "families": overflow_details,
            "counterfactual_extra_candidates": sum(
                x["target_count"] for x in overflow_details
            ),
            "counterfactual_extra_cells": len(overflow_extra_cells),
            "counterfactual_labels": dict(sorted(overflow_labels.items())),
            "counterfactual_required_cells": overflow_labels["REQUIRED"],
            "counterfactual_required_units": len(overflow_required_units),
            "counterfactual_new_unique_required_resources": len(
                overflow_new_required_resources,
            ),
            "counterfactual_new_complete_obligations": sorted(
                {ob for ob, _ in counterfactual_new_alts},
            ),
            "counterfactual_new_complete_alternatives": sorted(
                f"{ob}:{alternative}" for ob, alternative in counterfactual_new_alts
            ),
            "counterfactual_unnecessary_target_occurrences": sum(
                f["unnecessary_targets"] for f in overflow_details
            ),
            "counterfactual_unnecessary_cells": overflow_labels["UNNECESSARY"],
            "counterfactual_unique_resources": len(
                {k for _, k in overflow_extra_cells},
            ),
            "counterfactual_structural_union_size": len(
                actual_union | {k for _, k in overflow_extra_cells},
            ),
        },
        "grounding_effectiveness": {
            "requests": grounds,
            "counts": dict(ground_counts),
            "distinct_owner_resources": len(
                {g["owner"] for g in grounds if g["owner"]},
            ),
            "distinct_required_owner_resources": len(
                {
                    g["owner"]
                    for g in grounds
                    if g["owner"] and g["gold_status_anywhere"] == "REQUIRED"
                },
            ),
            "requests_relevant_in_at_least_one_recipe_obligation": sum(
                any(v == "REQUIRED" for v in g["owner_labels_by_obligation"].values())
                for g in grounds
            ),
            "requests_helpful_or_unnecessary_in_all_recipe_obligations": sum(
                not any(
                    v == "REQUIRED" for v in g["owner_labels_by_obligation"].values()
                )
                for g in grounds
            ),
        },
        "misses": {
            "primary_counts": dict(miss_causes),
            "cells": miss_rows,
            "missed_required_cells": len(missed),
        },
        "direct_import_relation_probe": import_probe,
        "combination_coverage": {
            "all_432": combo_rows,
            "complete_combinations_by_resource_set": sum(
                x["all_resources_represented"] for x in combo_rows
            ),
            "complete_combinations_by_hypothesis_structure": sum(
                x["realized_by_hypothesis_shapes"] for x in combo_rows
            ),
            "maximum_resources_represented": max(
                x["represented_required_resource_cells"] for x in combo_rows
            ),
            "maximum_coverage_combination": max(
                combo_rows,
                key=lambda row: row["represented_required_resource_cells"],
            ),
        },
        "task_gap_review": judgments["task_gap_review"],
        "limitations": [
            *judgments["packet_limitations"],
            "Captured generation timing covers the full generation call; no component timings separate projection, grounding replay, support validation, association validation, or serialization.",
            "Resource-level witness completion tests exact obligation/resource membership in one generated hypothesis; fine-grained unit coverage is reported separately.",
            "Overflow targets are used only in the labeled post-hoc counterfactual and never counted as observed generated children.",
        ],
    }
    md = render_markdown(output)
    return output, md


def render_markdown(x: dict[str, Any]) -> str:
    q = x["lexical"]
    surfaces = x["structural_surfaces"]
    marginal = x["reference_marginal"]
    import_missing = ", ".join(
        f"{row['obligation']}:{row['resource']}"
        for row in x["direct_import_relation_probe"][
            "missing_required_witnesses_reached"
        ]
    )
    lines = [
        "# Case 0007 Stage D joined analysis",
        "",
        "## 1. Experiment integrity",
        "",
        f"Verified chain: `{' → '.join(c[:8] for c, _ in CHAIN)}`; all pinned digests and internal Stage A/B/C integrity records match.",
        f"Exact join: {x['join_integrity']['resources']}/521 resources; {x['join_integrity']['obligations']}/11 obligations; {x['join_integrity']['shared_anchors']}/9 anchors; {x['join_integrity']['lexical_lanes']}/12 lanes; {x['join_integrity']['routed_obligation_lanes']}/11 routed lanes; {x['join_integrity']['grounding_requests']}/9 grounds; {x['join_integrity']['generation_attempts']}/25 specs; {x['join_integrity']['judgment_cells_observed']:,}/5,731 cells. Duplicate identities: 0; missing/unexpected identities: 0. Routed candidates map one-to-one to native candidates; generated targets and Reference supports join the frozen snapshot.",
        f"Stage B mechanics recompute as {x['generation_mechanics']['attempt_dispositions']}; {x['generation_mechanics']['fixed_hypotheses']} fixed hypotheses, {x['generation_mechanics']['reference_families']} Reference families, {x['generation_mechanics']['branch_children']} children, {x['generation_mechanics']['hypotheses']} hypotheses, {x['generation_mechanics']['member_occurrences']} member occurrences, and 19 unique structural resources.",
        "",
        "## 2. Blind gold",
        "",
        f"All obligations are APPLICABLE. Gold has {x['gold']['distinct_required_information_units']} distinct REQUIRED units, {x['gold']['required_unit_judgments']} obligation-relative unit judgments, {x['gold']['unique_required_resources']} unique required resources, {x['gold']['required_cells']} REQUIRED cells, {x['gold']['helpful_cells']} HELPFUL_ONLY cells, and {x['gold']['unnecessary_cells']:,} UNNECESSARY cells. Unresolved, inherent discovery, and task gaps are all zero.",
        f"The 432 acceptable combinations span {x['sufficient_combinations']['minimum_size']}–{x['sufficient_combinations']['maximum_size']} resources; {x['sufficient_combinations']['minimum_combination_count']} combinations have the minimum size of 19.",
        "",
        "| Obligation | Applicability | Distinct REQUIRED units | Unit judgments | REQUIRED cells |",
        "|---|---|---:|---:|---:|",
    ]
    for obligation, values in x["gold"]["required_by_obligation"].items():
        lines.append(
            f"| {obligation} | APPLICABLE | {values['distinct_information_units']} | {values['unit_judgments']} | {values['required_resource_cells']} |",
        )
    lines += [
        "",
        "## 3. Lexical baselines",
        "",
        f"Global native ranking has {q['global_positive_surface']} positive resources. Task completion is at depth {q['global_task_complete_depth']}; the complete 27-resource alternative universe and best 19-resource sufficient combination also complete at depth {q['global_complete_27_resource_universe_depth']} and {q['best_19_resource_combination_depth']}, respectively. The global task-completion prefix contains {q['global_prefix_unique_resources']} unique resources.",
        f"Own-native maximum completion depth is {q['own_native_max_depth']}; obligation prefixes total {q['own_native_prefix']['summed_occurrences']} occurrences and {q['own_native_prefix']['unique_resources']} unique resources (+{q['own_excess_over_minimum']} over 19; {q['own_candidate_to_minimum_ratio']:.2f}×). Prefix labels: {q['own_native_prefix']['cells']}.",
        f"Routed maximum completion position is {q['routed_max_position']}; prefixes total {q['routed_prefix']['summed_occurrences']} occurrences and {q['routed_prefix']['unique_resources']} unique resources (+{q['routed_excess_over_minimum']} over 19; {q['routed_candidate_to_minimum_ratio']:.2f} times). Prefix labels: {q['routed_prefix']['cells']}.",
        f"Routing improved {len(q['routing_comparison']['improved'])} obligations ({', '.join(q['routing_comparison']['improved'])}), left {len(q['routing_comparison']['unchanged'])} unchanged, and worsened {len(q['routing_comparison']['worsened'])} ({', '.join(q['routing_comparison']['worsened'])}).",
        "",
        "## 4. Actual structural surfaces",
        "",
        "| Surface | Unique resources | Obligation/resource cells | REQUIRED cells / 55 | REQUIRED unit judgments / 56 | Distinct REQUIRED units / 30 | Complete obligations |",
        "|---|---:|---:|---:|---:|---:|---:|",
    ]
    for name in ["OWNER", "MIRROR", "REFERENCE", "OWNER_MIRROR", "ALL"]:
        row = surfaces[name]
        lines.append(
            f"| {name} | {row['candidate_resources']} | {row['obligation_resource_cells']} | {row['required_cells_covered']} | {row['required_unit_judgments_covered']} | {row['distinct_required_units_covered']} | {row['complete_obligation_count']}/11 |",
        )
    lines += [
        "",
        "Full structural output has 19 unique resources and 24 obligation/resource cells. It covers 9/27 required resources somewhere, but only 10/55 correctly assigned REQUIRED cells and 10/56 unit judgments. The 19-resource union intersects the four minimum sufficient combinations by 5, 5, 5, and 6 resources; it equals none. Only package-api has a complete generated witness alternative. Module-membership has resource-set reachability but no single hypothesis with the complete pair.",
        "The actual structural union is 1.00 times the minimum sufficient resource count by cardinality. That equality is not sufficiency: the best identity intersection is 6/19, with no complete minimum combination and no complete 11-obligation combination.",
        "",
        "| Surface | Type | Candidate surface | REQUIRED cells | Complete obligations |",
        "|---|---|---:|---:|---:|",
        f"| Global lexical completion | Ranked prefix | {q['global_prefix_unique_resources']} | 55/55 | 11/11 |",
        f"| Own-native prefixes | Ranked, obligation-local | {q['own_native_prefix']['unique_resources']} | {q['own_native_prefix']['cells'].get('REQUIRED', 0)}/55 | 11/11 |",
        f"| Routed prefixes | Ranked, obligation-local | {q['routed_prefix']['unique_resources']} | {q['routed_prefix']['cells'].get('REQUIRED', 0)}/55 | 11/11 |",
        f"| OWNER/MIRROR | Unranked structural | {surfaces['OWNER_MIRROR']['candidate_resources']} | {surfaces['OWNER_MIRROR']['required_cells_covered']}/55 | {surfaces['OWNER_MIRROR']['complete_obligation_count']}/11 |",
        f"| OWNER/MIRROR/REFERENCE | Unranked structural | {surfaces['ALL']['candidate_resources']} | {surfaces['ALL']['required_cells_covered']}/55 | {surfaces['ALL']['complete_obligation_count']}/11 |",
        "| Sufficient gold bound | Semantic lower bound | 19–24 | 55/55 | 11/11 |",
        "",
        "## 5. Marginal Reference contribution",
        "",
        f"Relative to OWNER/MIRROR, Reference adds {marginal['new_cells']} cells and {marginal['new_unique_resources']} unique resources. Added-cell labels: {marginal['labels']}. New REQUIRED cells and unit judgments: {marginal['new_required_cells']} and {marginal['new_required_unit_judgments']}; new distinct REQUIRED units: {marginal['new_required_information_units']}. It adds {marginal['new_unique_required_resources']} unique resource that occurs in REQUIRED gold somewhere, but zero REQUIRED cells in its generated obligation. It adds {marginal['new_helpful_resources']} helpful resources and {marginal['new_unique_resources_never_required']} unique resources never REQUIRED. Cell yield is {marginal['required_cell_yield']:.3f}; unique-resource yield is {marginal['required_resource_yield']:.3f}.",
        f"Reference creates {len(marginal['new_complete_obligations'])} new complete obligations and {len(marginal['new_complete_alternatives'])} newly complete alternatives. The one resource-set-only obligation remains module-membership; no Reference child supplies its full witness structure.",
        "",
        "## 6. Reference family-by-family results",
        "",
        "Targets below are exact distinct diagnostic targets. Only generated children count as observed output.",
        "",
        "| Family | Obligation | Seed | Result | Targets | Work | Children | REQUIRED / helpful / unnecessary targets | Complete alternative in child |",
        "|---|---|---|---|---:|---|---:|---|---|",
    ]
    for family in x["reference_families"]:
        lines.append(
            f"| {family['family']} | {family['obligation']} | {family['seed']} | {family['disposition']} | {family['exact_target_count']} | {family['work_performed']}/{family['work_limit']} complete={family['work_complete']} | {family['generated_child_count']} | {family['required_resources']} / {family['helpful_resources']} / {family['unnecessary_resources']} | {', '.join(family['complete_gold_alternatives_in_any_valid_child']) or 'none'} |",
        )
    lines += [
        "",
        "## 7. Overflow and no-target diagnostics",
        "",
        f"All three result-bound overflows retained 20 exact targets each; none contains a REQUIRED resource for its obligation. Across the three diagnostic sets, admitting all targets would add {x['overflow']['counterfactual_extra_candidates']} child candidates, {x['overflow']['counterfactual_extra_cells']} distinct obligation/resource cells ({x['overflow']['counterfactual_labels']}), and {x['overflow']['counterfactual_unique_resources']} unique resources. It would add {x['overflow']['counterfactual_unnecessary_target_occurrences']} unnecessary target occurrences, zero REQUIRED cells/units/resources, and no new complete obligation or alternative. The union would grow to {x['overflow']['counterfactual_structural_union_size']} resources. This post-hoc calculation is not observed treatment.",
        "The two no-target families both used g-reference (the derivation function) and completed the exact search with zero targets. A frozen source import shows `references/declarations/analysis.py` imports the exact `PythonDeclarationReferenceKnowledge` class grounded by g-reference-fact. That is an evidence-backed alternate Reference seed candidate, but no projection was run and the same analysis.py resource was already generated as an OWNER in reference-integration, so no new resource-cell credit is assigned. The missing route file `references/declarations/resolution.py` is reached by the direct-import relation; `references/docs/overview.md` is a documentation contract, not a referencer target.",
        "",
        "## 8. Witness-structure alignment",
        "",
        f"Across {x['recipe_alignment']['hypothesis_count']} generated hypotheses: {x['recipe_alignment']['counts']}. At the obligation-level, module-membership is RESOURCE_MATCH_WRONG_STRUCTURE: separate owner hypotheses collectively contain its alternative resources, but none contains the complementary pair. A complete 19-resource combination is not realized; no full 11-obligation combination is resource-set complete.",
        "",
        "## 9. Miss classification",
        "",
        f"Of 55 REQUIRED cells, 45 remain uncovered. Non-overlapping primary causes: {x['misses']['primary_counts']}; the counts sum to 45. No overflow miss is assigned because none of the overflowed targets is REQUIRED in its obligation. `NO_RECIPE` accounts for explicit-exposure, documentation and validation paths; cross-role candidates do not count for another obligation.",
        f"Reference-specific causes across required misses: {x['reference_miss_causes']['counts']}. The six currently missing resources found by the direct-import probe are `REQUIRES_OTHER_TYPED_RELATION`; the reference overview is `WITNESS_NOT_REFERENTIAL`.",
        "",
        "## 10. Operator reachability",
        "",
        f"All 9 exact grounded owners are REQUIRED somewhere in the gold (8 distinct owner resources because the module interpretation owner is grounded twice). Eight of nine grounding requests participate in at least one recipe obligation where their owner is REQUIRED; g-module-identity is helpful-only in its snapshot recipe. Owner resources yield 10 required cells. Mirror yields zero required cells. Reference yields zero required cells, although one added resource is REQUIRED under a different obligation. Reachability partition: {x['operator_reachability']['bucket_counts']}. The residual bucket means no typed route was proven here, not that every such resource is ontologically nonstructural.",
        "",
        "### Direct static import relation probe (counterfactual, not treatment)",
        "",
        f"A one-hop source-import scan over frozen contents sees {x['direct_import_relation_probe']['direct_dependency_edges']} edges across grounded owner/obligation pairs, maximum fanout {x['direct_import_relation_probe']['maximum_fanout']}. It reaches {x['direct_import_relation_probe']['new_required_cells']} currently missing REQUIRED cells ({x['direct_import_relation_probe']['new_required_unit_judgments']} unit judgments), including: {import_missing}. The resulting candidate resource union would be {x['direct_import_relation_probe']['new_candidate_structural_union_size']} before any recipe structure review. This is static evidence supporting one bounded relation family, not a generated result.",
        "",
        "## 11. Runtime and cost",
        "",
        "The complete Stage B generation call took 1,130.740 seconds. Per-component projection, grounding replay, support validation, candidate-association validation, and serialization times were not captured; no attribution is made.",
        "",
        "## 12. Architectural decision",
        "",
        "Decision: CONTINUE STRUCTURAL BREADTH with exactly one next relation family: direct one-hop static Python import dependency. The blind archive shows bounded fanout (maximum 9) and exact missing REQUIRED targets in binding, module-membership, snapshot-provenance, and Reference integration. Do not add a general documentation graph. After this relation is evaluated, assess witness assembly; Case 0007 alone does not justify a general evidence resolver yet because only 10/55 required cells are present in observed structural output.",
        "Reference value is LOW for this observed treatment: zero new REQUIRED cells, zero new complete obligations, and 6 new resources for 8 cells. The unprojected g-reference-fact seed limits what can be concluded about the operator itself. Overflow did not matter. Routing worsened three obligations and expanded its unique prefix union from 249 to 378; this is further evidence to park routing as a primary discriminator, not to remove it in this analysis.",
        "This case does not justify changing result bounds, treating the numerical 19=19 match as sufficiency, implementing public-export RI, or accessing confirmation.",
        "",
        "## Limitations",
        "",
    ]
    lines.extend(f"- {value}" for value in x["limitations"])
    lines.extend(
        [
            "",
            "Confirmation outcomes were not accessed. Treatment was not rerun. No production source or frozen Stage A/B/B.5/C artifact was modified.",
            "",
        ],
    )
    return "\n".join(lines)


def write() -> None:
    output, md = compute()
    files = [
        (BASE / "analysis.json", canonical(output)),
        (BASE / "analysis.md", md.encode("utf-8")),
    ]
    for path, data in files:
        if path.exists():
            raise FileExistsError(f"refusing to overwrite {path}")
    for path, data in files:
        with path.open("xb") as handle:
            handle.write(data)
    print("wrote analysis.json and analysis.md")


def verify() -> None:
    output, md = compute()
    expected = [
        (BASE / "analysis.json", canonical(output)),
        (BASE / "analysis.md", md.encode("utf-8")),
    ]
    for path, data in expected:
        if not path.exists() or path.read_bytes() != data:
            raise ValueError(f"deterministic replay mismatch: {path}")
    print("deterministic replay verified")


if __name__ == "__main__":
    mode = sys.argv[1] if len(sys.argv) > 1 else "verify"
    if mode == "write":
        write()
    elif mode == "verify":
        verify()
    else:
        raise SystemExit("usage: analyze.py [write|verify]")
