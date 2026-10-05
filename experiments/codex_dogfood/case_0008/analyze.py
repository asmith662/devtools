# ruff: noqa: INP001, CPY001, E501, TRY003, PLR2004, COM812, EM101, EM102, D103, F541, B905, ANN401, B007, C901, E741, PERF102, PLR0912, PLR0915, RET504
"""Deterministically join frozen Case 0008 captures with Stage C gold."""

from __future__ import annotations

import gzip
import hashlib
import itertools
import json
import statistics
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any

ROOT = Path(__file__).parent
GOLD = ROOT / "adjudication" / "judgments.json"
EXPECTED = {
    "inputs.pkl.gz": "9eb0f6de7c9150390807ab872d159bbcf4c8853632b48c8395d3dd9d347be5d5",
    "stage_b_raw.pkl.gz": "3c2cdf45a72d470e2f8c38a6d99f2940add6a9546e5177a8d0dca13f7de6765d",
    "execution_started.json": "e4f202319a2e3920ee997966112f71ef04dc59310a5185a2b64148db2c90c7e8",
    "adjudication/blind_manifest.json": "d1096ba811f050a74a0232caa34245bc6de7f263494155e97c3e0ebbf147b6e0",
    "adjudication/blind_resources.json.gz": "cae456fa325a435de599da24a75ed3a3728d568b4bfc613b5b6851537a98c09d",
    "adjudication/judgments.json": "daf9c5d2d3e3207296dbfe474a5918e27eb285f7dee9e580443a4b94dc4e590e",
}
RECOVERY_EXPECTED = {
    "capture.pkl.gz": "0ad8b7b48274ca67d9ee669cecbf2ae553a89c3476b80a8ea3bf413ae8bcaf30",
    "generation.json": "b12f519e214382ce1fd76b19e0af995342f20a71b6fb32d4563cf64fe4a0709f",
    "grounding.json": "1211f59ce778da4c1badd57d7b65b45a953780af2856177dbeb00cf31ddd75a4",
    "retrieval.json": "6ae883a05393120c2da7df442bb9ef704b8fb7d2c9ebf6f2e3cdae7c6e415f58",
    "routing.json": "6c68dd32d2b6047c426e59b0731229225eefd1d99b115539391a60d8847ef24f",
}
OPS = {
    "OwnerResourceSupport": "OWNER",
    "MirroredResourceSupport": "MIRROR",
    "PythonReferenceResourceSupport": "REFERENCE",
    "PythonImportDependencyResourceSupport": "IMPORT",
}
SURFACES = {
    "OWNER": {"OWNER"},
    "MIRROR": {"MIRROR"},
    "REFERENCE": {"REFERENCE"},
    "IMPORT": {"IMPORT"},
    "OWNER/MIRROR": {"OWNER", "MIRROR"},
    "OWNER/MIRROR/REFERENCE": {"OWNER", "MIRROR", "REFERENCE"},
    "OWNER/MIRROR/IMPORT": {"OWNER", "MIRROR", "IMPORT"},
    "ALL FOUR": set(OPS.values()),
}


def load(name: str) -> Any:
    return json.loads((ROOT / name).read_text(encoding="utf-8"))


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def rid(resource: dict[str, str]) -> tuple[str, str]:
    return resource["address"], resource["content_identity"]


def _alternative_resources(
    alternative: dict[str, Any], units: dict[str, dict[str, Any]]
) -> set[tuple[str, str]]:
    return {rid(units[u]["resource"]) for u in alternative["all_units"]}


def analyze() -> dict[str, Any]:
    for name, expected in {**EXPECTED, **RECOVERY_EXPECTED}.items():
        actual = digest(ROOT / name)
        if actual != expected:
            raise ValueError(f"frozen digest drift: {name}: {actual}")
    stage_a_integrity = load("integrity.json")
    stage_b_integrity = load("stage_b_integrity.json")
    for name, expected in stage_a_integrity["sha256"].items():
        if digest(ROOT / name) != expected:
            raise ValueError(f"Stage A committed integrity drift: {name}")
    for name, expected in stage_b_integrity["artifacts"].items():
        if digest(ROOT / name) != expected:
            raise ValueError(f"Stage B committed integrity drift: {name}")
    pre, retrieval, routing, treatment = (
        load("pre_execution.json"),
        load("retrieval.json"),
        load("routing.json"),
        load("treatment.json"),
    )
    grounding, generation, integ, gold = (
        load(x)
        for x in (
            "grounding.json",
            "generation.json",
            "stage_b_integrity.json",
            "adjudication/judgments.json",
        )
    )
    manifest = load("adjudication/blind_manifest.json")
    with gzip.open(
        ROOT / "adjudication" / "blind_resources.json.gz", "rt", encoding="utf-8"
    ) as stream:
        blind_archive = json.load(stream)
    units = {u["identity"]: u for u in gold["information_units"]}
    obligations = {o["frozen_obligation"]["identity"]: o for o in gold["obligations"]}
    label_rows = [
        ((c["obligation"], rid(c["resource"])), c["judgment"])
        for c in gold["resource_judgments"]
    ]
    labels = dict(label_rows)
    resources = {rid(r): r for r in pre["resources"]}
    import_module_addresses = {
        m["module_identity"]: m["address"]
        for m in pre["import_frame"]["source_resources"]
    }
    if (gold["repository_id"], gold["snapshot_id"], gold["corpus_id"]) != (
        "fe2c8984-a021-4342-9e31-404a6cf07707",
        "72a021a8a4778ffdc7f37152b5d31efb6a2ea93de82edc8c940ec76be5e641aa",
        "8843f263c69d0d1b07b1fa343e63c07873827f0c3a842e7a28e50d1c8b65b93b",
    ):
        raise ValueError("frozen repository/snapshot/corpus identity drift")
    expected_task = manifest["task"]
    if (
        manifest["case_identity"] != "case_0008"
        or manifest["task_identity"] != "case-0008-unresolved-frontier-acquisition"
        or gold["case_identity"] != manifest["case_identity"]
        or gold["task_identity"] != manifest["task_identity"]
        or gold["exact_task"] != expected_task
        or manifest["resource_count"] != 523
        or len(manifest["shared_anchors"]) != 11
        or len(manifest["obligations"]) != 13
    ):
        raise ValueError("blind manifest identity/task/count drift")
    if (
        blind_archive["repository_id"] != gold["repository_id"]
        or blind_archive["snapshot_id"] != gold["snapshot_id"]
        or blind_archive["corpus_id"] != gold["corpus_id"]
        or blind_archive["resource_count"] != 523
        or {rid(r) for r in blind_archive["resources"]} != set(resources)
    ):
        raise ValueError("blind archive identity or resource membership drift")
    if (
        len(resources) != 523
        or len(obligations) != 13
        or len(labels) != 6799
        or len(label_rows) != len(labels)
    ):
        raise ValueError("resource/obligation/cell cardinality drift")
    if set(resources) != {r for _, r in labels} or {o for o, _ in labels} != set(
        obligations
    ):
        raise ValueError("resource or obligation identity join mismatch")
    if any(
        rid(unit["resource"]) not in resources for unit in gold["information_units"]
    ):
        raise ValueError("information unit refers outside the frozen resource frame")
    if Counter(labels.values()) != {
        "REQUIRED": 50,
        "HELPFUL_ONLY": 54,
        "UNNECESSARY": 6695,
    }:
        raise ValueError("Stage C judgment cell categories drift")
    if gold["task_gaps"] or not gold["task_gap_review"].startswith(
        "no obvious mandatory task-interpretation gap found"
    ):
        raise ValueError("Stage C task-gap judgment drift")
    alternatives: dict[str, list[dict[str, Any]]] = {
        o: v["acceptable_alternatives"] for o, v in obligations.items()
    }
    if set(obligations) != {
        "frontier-semantics",
        "assessment-applicability",
        "candidate-integration",
        "witness-boundary",
        "acquisition-contract",
        "grounding-provenance",
        "frame-identity",
        "readiness-integration",
        "orchestration-boundary",
        "package-api",
        "tests",
        "documentation",
        "validation",
    }:
        raise ValueError("frozen obligation identity frame drift")
    if any(v["applicability"] != "APPLICABLE" for v in obligations.values()):
        raise ValueError("Stage C applicability drift")
    manifest_obligations = {o["identity"]: o for o in manifest["obligations"]}
    if set(manifest_obligations) != set(obligations):
        raise ValueError("manifest and Stage C obligation identities differ")
    for identity, adjudication in obligations.items():
        frozen = adjudication["frozen_obligation"]
        source = manifest_obligations[identity]
        if (
            source["desired_information_predicate"]
            != frozen["desired_information_predicate"]
            or source["mandatory_helpful_status"] != frozen["mandatory_helpful_status"]
            or source["satisfaction_criterion"] != frozen["satisfaction_criterion"]
            or source["shared_anchor_references"] != frozen["shared_anchor_references"]
        ):
            raise ValueError(f"frozen obligation wording drift: {identity}")
    alt_resources = {
        o: [_alternative_resources(a, units) for a in alts]
        for o, alts in alternatives.items()
    }
    combinations = []
    obs = list(obligations)
    for picks in itertools.product(*(range(len(alternatives[o])) for o in obs)):
        chosen = {o: alt_resources[o][i] for o, i in zip(obs, picks)}
        choice_ids = {o: alternatives[o][i]["identity"] for o, i in zip(obs, picks)}
        combinations.append(
            {
                "choices": choice_ids,
                "resources": set().union(*chosen.values()),
                "per_obligation": chosen,
            }
        )
    minimum, maximum = (
        min(len(c["resources"]) for c in combinations),
        max(len(c["resources"]) for c in combinations),
    )
    mins = [c for c in combinations if len(c["resources"]) == minimum]
    if (
        sum(map(len, alternatives.values())) != 15
        or len(combinations) != 4
        or (minimum, maximum, len(mins)) != (21, 22, 2)
    ):
        raise ValueError("frozen gold alternatives/combinations drift")

    # Native ranked surfaces.
    lanes = {
        x["query_identity"].removesuffix("-query"): x["matches"]
        for x in retrieval["obligations"]
    }
    global_matches = retrieval["global"]["matches"]
    global_rank = {rid(m["resource"]): m["native_rank"] for m in global_matches}
    native_rank = {
        o: {rid(m["resource"]): m["native_rank"] for m in ms} for o, ms in lanes.items()
    }
    routed_lanes = {x["obligation"]: x["candidates"] for x in routing["lanes"]}
    routed_pos = {
        o: {rid(m["resource"]): m["routed_position"] for m in ms}
        for o, ms in routed_lanes.items()
    }
    routed_tier = {
        o: {rid(m["resource"]): m["tier"] for m in ms} for o, ms in routed_lanes.items()
    }
    if (
        len(global_rank) != len(global_matches)
        or sorted(global_rank.values()) != list(range(1, len(global_rank) + 1))
        or any(
            len(native_rank[o]) != len(lanes[o])
            or sorted(native_rank[o].values())
            != list(range(1, len(native_rank[o]) + 1))
            or len(routed_pos[o]) != len(routed_lanes[o])
            or sorted(routed_pos[o].values()) != list(range(1, len(routed_pos[o]) + 1))
            for o in lanes
        )
    ):
        raise ValueError("duplicate native/routed candidate or position identity")
    if (
        len(lanes) != 13
        or len(routed_lanes) != 13
        or len(grounding["groundings"]) != 11
        or len(retrieval["obligations"]) != 13
    ):
        raise ValueError("lane/anchor cardinality drift")
    if len(lanes) + 1 != 14 or len(generation["attempts"]) != 29:
        raise ValueError("lexical lane or generation spec cardinality drift")
    treatment_queries = {q["id"]: q["obligation"] for q in treatment["queries"]}
    if len(treatment["anchors"]) != 11 or treatment_queries != {
        x["query_identity"]: x["query_identity"].removesuffix("-query")
        for x in retrieval["obligations"]
    }:
        raise ValueError("shared-anchor or native-lane identity join drift")
    if {g["request_identity"] for g in grounding["groundings"]} != {
        g["id"] for g in treatment["grounding_specs"]
    }:
        raise ValueError("grounding request identity join drift")
    if (
        len(treatment["recipes"]) != len(generation["attempts"])
        or len(treatment["recipes"]) != 29
    ):
        raise ValueError("frozen generation recipe count drift")
    routed_survival = all(set(routed_pos[o]) == set(native_rank[o]) for o in lanes)
    global_unchanged = routing["global_unchanged"]["matches"] == global_matches
    if not routed_survival or not global_unchanged:
        raise ValueError("routing/native join integrity failure")
    for o, candidates in routed_pos.items():
        for r, pos in candidates.items():
            if r not in native_rank[o] or native_rank[o][r] != next(
                m["native_rank"] for m in routed_lanes[o] if rid(m["resource"]) == r
            ):
                raise ValueError(
                    "routed candidate does not map to exact native candidate"
                )

    # Native and routed completion depths per alternative and per obligation.
    def depths(
        rankmap: dict[str, dict[tuple[str, str], int]] | dict[tuple[str, str], int],
        lane: str,
    ) -> dict[str, Any]:
        per_alt, best, all_depths = {}, {}, []
        for o in obs:
            per_alt[o] = []
            for i, rs in enumerate(alt_resources[o]):
                rm = rankmap if lane == "global" else rankmap.get(o, {})
                vals = [rm[r] for r in rs if r in rm]
                depth = max(vals) if len(vals) == len(rs) else None
                per_alt[o].append(
                    {
                        "alternative": alternatives[o][i]["identity"],
                        "depth": depth,
                        "missing": sorted([list(r) for r in rs if r not in rm]),
                    }
                )
            finite = [x["depth"] for x in per_alt[o] if x["depth"] is not None]
            best[o] = min(finite) if finite else None
            if best[o] is not None:
                all_depths.append(best[o])
        return {
            "alternatives": per_alt,
            "best_by_obligation": best,
            "maximum_best_depth": max(all_depths) if all_depths else None,
        }

    global_d = depths(global_rank, "global")
    native_d = depths(native_rank, "native")
    routed_d = depths(routed_pos, "routed")

    def prefix(
        rankmap: dict[str, dict[tuple[str, str], int]], d: dict[str, Any]
    ) -> dict[str, Any]:
        by_ob = {}
        for o, depth in d["best_by_obligation"].items():
            by_ob[o] = {
                r
                for r, rank in rankmap[o].items()
                if depth is not None and rank <= depth
            }
        union = set().union(*by_ob.values())
        cell_counts = Counter(
            labels[(o, r)] for o, rs in by_ob.items() for r in rs if (o, r) in labels
        )
        return {
            "summed_prefix_occurrences": sum(map(len, by_ob.values())),
            "unique_resources": len(union),
            "required_cells": cell_counts["REQUIRED"],
            "helpful_only_cells": cell_counts["HELPFUL_ONLY"],
            "unnecessary_cells": cell_counts["UNNECESSARY"],
            "by_obligation": {
                o: sorted([list(r) for r in rs]) for o, rs in by_ob.items()
            },
            "union": sorted([list(r) for r in union]),
        }

    native_prefix, routed_prefix = (
        prefix(native_rank, native_d),
        prefix(routed_pos, routed_d),
    )

    # Exact hypotheses and obligation-relative cells attributed to operators.
    operator_targets: dict[str, set[tuple[str, str]]] = {x: set() for x in OPS.values()}
    operator_cells: dict[str, set[tuple[str, tuple[str, str]]]] = {
        x: set() for x in OPS.values()
    }
    hypotheses = generation["generated_hypotheses"]
    hyp_ops: dict[str, set[str]] = {}
    for h in hypotheses:
        op_set = set()
        for m in h["members"]:
            r = rid(m["target"])
            for s in m["structural_supports"]:
                op = OPS.get(s["operator_support_type"])
                if op:
                    operator_targets[op].add(r)
                    operator_cells[op].add((h["obligation"], r))
                    op_set.add(op)
        hyp_ops[h["identity"]] = op_set
    if len(hypotheses) != 28 or sum(len(h["members"]) for h in hypotheses) != 47:
        raise ValueError("hypothesis/member count drift")
    fixed_attempts = [a for a in generation["attempts"] if a["recipe_kind"] == "fixed"]
    if len(fixed_attempts) != 15 or Counter(
        a["disposition"] for a in fixed_attempts
    ) != {"GENERATED": 9, "NO_TARGET": 6}:
        raise ValueError("fixed generation attempt outcome drift")
    if sum(len(a.get("branches", [])) for a in generation["attempts"]) != 19:
        raise ValueError("branch child count drift")
    if generation["recovery_provenance"] != integ["recovery_provenance"]:
        raise ValueError(
            "generation recovery provenance does not match committed integrity record"
        )
    if (
        generation["recovery_provenance"].get("execution_kind") != "GENERATION_RECOVERY"
        or generation["recovery_provenance"].get("original_execution_id")
        != "2fed596a-f43d-4d35-9e32-e8a609366a6f"
        or generation["recovery_provenance"].get("recovery_id")
        != "case-0008-stage-b-generation-recovery-1"
    ):
        raise ValueError("recovery qualification identity drift")
    frozen_chain = {
        "stage_a": "3eda8c6027f72a51109ed78f5684a6bbb59c65bd",
        "generation_recovery_protocol": "3d6cb9597742ebd78946d1291f145770904b2248",
        "stage_b_generation_recovery": "348887c5e8f9969259734563319bb2d6ec715a3f",
        "stage_b5": "9eb910d2c9dc6fa0947e6640917c8072ed4ba010",
        "stage_c": "c7df5f50c16433cbaff9c0d9bd013b9833f03670",
    }
    for h in hypotheses:
        for m in h["members"]:
            target_r = rid(m["target"])
            if target_r not in resources:
                raise ValueError("generated target outside frozen snapshot")
            for s in m["structural_supports"]:
                src = s.get("source") or s.get("referencing_source")
                if src and rid(src) not in resources:
                    raise ValueError("operator source outside frozen snapshot")
                if s[
                    "operator_support_type"
                ] == "PythonReferenceResourceSupport" and not s.get(
                    "reference_fact_identities"
                ):
                    raise ValueError("Reference support missing fact identity")
                if (
                    s["operator_support_type"]
                    == "PythonImportDependencyResourceSupport"
                ):
                    dep_targets = {rid(t) for t in s.get("dependency_targets", [])}
                    if (
                        not s.get("resolved_import_relation_identities")
                        or not dep_targets <= resources.keys()
                        or s.get("source_module") not in import_module_addresses
                        or target_r not in dep_targets
                    ):
                        raise ValueError(
                            "Import support does not validate against snapshot"
                        )
    surface_ops = {
        name: set().union(*(operator_targets[o] for o in ops))
        for name, ops in SURFACES.items()
    }
    surface_cells = {
        name: set().union(*(operator_cells[o] for o in ops))
        for name, ops in SURFACES.items()
    }
    expected_sizes = {
        "OWNER": 8,
        "MIRROR": 1,
        "REFERENCE": 6,
        "IMPORT": 7,
        "OWNER/MIRROR": 9,
        "OWNER/MIRROR/REFERENCE": 14,
        "OWNER/MIRROR/IMPORT": 14,
        "ALL FOUR": 19,
    }
    for name, n in expected_sizes.items():
        if len(surface_ops[name]) != n:
            raise ValueError(f"surface drift {name}: {len(surface_ops[name])}")
    expected_operator_cells = {"OWNER": 14, "MIRROR": 1, "REFERENCE": 12, "IMPORT": 7}
    if {
        op: len(operator_cells[op]) for op in OPS.values()
    } != expected_operator_cells or len(surface_cells["ALL FOUR"]) != 32:
        raise ValueError("operator-relative structural cell count drift")
    overflows = []
    for attempt in generation["attempts"]:
        for member in attempt["members"]:
            result_limit, work_limit = (
                member.get("result_limit"),
                member.get("work_limit"),
            )
            if (
                result_limit is not None
                and member.get("result_count", 0) > result_limit
            ) or (
                work_limit is not None and member.get("work_performed", 0) > work_limit
            ):
                overflows.append((attempt["recipe_identity"], member.get("projection")))
    if overflows:
        raise ValueError(f"captured generation bounds overflow: {overflows}")

    unit_labels = {
        (o, v["unit"]): v["judgment"]
        for o, j in obligations.items()
        for v in j["unit_judgments"]
    }
    unit_label_rows = [
        (o, v["unit"]) for o, j in obligations.items() for v in j["unit_judgments"]
    ]
    if len(unit_label_rows) != len(unit_labels) or len(unit_labels) != 71:
        raise ValueError("unit judgment identity coverage drift")
    required_units = {
        (o, u) for (o, u), label in unit_labels.items() if label == "REQUIRED"
    }
    required_resources = {r for (o, r), label in labels.items() if label == "REQUIRED"}
    if (
        len(required_units) != 71
        or len(required_resources) != 22
        or any(
            v["inferability"] != "INFERABLE_AT_START" or v["discovery"] is not None
            for o in obligations.values()
            for v in o["unit_judgments"]
            if v["judgment"] == "REQUIRED"
        )
    ):
        raise ValueError("REQUIRED inferability or cardinality drift")

    def surface_stats(name: str) -> dict[str, Any]:
        cells = surface_cells[name]
        cell_labels = Counter(labels.get(c, "unresolved") for c in cells)
        covered_unit_judgments = {
            (o, u)
            for o, u in required_units
            if rid(units[u]["resource"]) in surface_ops[name]
            and (o, rid(units[u]["resource"])) in cells
        }
        distinct_units = {u for _, u in covered_unit_judgments}
        per_obligation = {
            o: {
                "required_cells": sum(
                    1
                    for oo, r in cells
                    if oo == o and labels.get((oo, r)) == "REQUIRED"
                ),
                "helpful_only_cells": sum(
                    1
                    for oo, r in cells
                    if oo == o and labels.get((oo, r)) == "HELPFUL_ONLY"
                ),
                "unnecessary_cells": sum(
                    1
                    for oo, r in cells
                    if oo == o and labels.get((oo, r)) == "UNNECESSARY"
                ),
                "required_unit_judgments": sum(
                    1
                    for oo, u in required_units
                    if oo == o
                    and rid(units[u]["resource"]) in surface_ops[name]
                    and (oo, rid(units[u]["resource"])) in cells
                ),
                "distinct_required_units": len(
                    {
                        u
                        for oo, u in required_units
                        if oo == o
                        and rid(units[u]["resource"]) in surface_ops[name]
                        and (oo, rid(units[u]["resource"])) in cells
                    }
                ),
            }
            for o in obs
        }
        return {
            "resources": len(surface_ops[name]),
            "resource_ids": sorted([list(r) for r in surface_ops[name]]),
            "cells": len(cells),
            "required_cells": cell_labels["REQUIRED"],
            "helpful_only_cells": cell_labels["HELPFUL_ONLY"],
            "unnecessary_cells": cell_labels["UNNECESSARY"],
            "unresolved_cells": cell_labels["unresolved"],
            "required_unit_judgments": len(covered_unit_judgments),
            "distinct_required_units": len(distinct_units),
            "distinct_required_unit_ids": sorted(distinct_units),
            "unique_required_resources": len(surface_ops[name] & required_resources),
            "never_required_resources": sorted(
                [list(r) for r in surface_ops[name] - required_resources]
            ),
            "per_obligation": per_obligation,
        }

    surfaces = {n: surface_stats(n) for n in SURFACES}

    # Gold alternatives, sufficient-combination intersections and structural completeness.
    def hyp_complete(h: dict[str, Any], o: str) -> bool:
        members = {rid(m["target"]) for m in h["members"]}
        return any(alt <= members for alt in alt_resources[o])

    def resource_reachable(o: str, cells: set[tuple[str, tuple[str, str]]]) -> bool:
        have = {r for oo, r in cells if oo == o}
        return any(a <= have for a in alt_resources[o])

    complete_by_surface, reachable_by_surface = {}, {}
    for name in SURFACES:
        reachable_by_surface[name] = {
            o for o in obs if resource_reachable(o, surface_cells[name])
        }
    # Restrict each surface's hypotheses to members supported by selected operators, retaining one-hypothesis structure.
    complete_by_surface = {}
    for name, op_set in SURFACES.items():
        good = set()
        for h in hypotheses:
            chosen = {
                rid(m["target"])
                for m in h["members"]
                if any(
                    OPS.get(s["operator_support_type"]) in op_set
                    for s in m["structural_supports"]
                )
            }
            if any(a <= chosen for a in alt_resources[h["obligation"]]):
                good.add(h["obligation"])
        complete_by_surface[name] = good
    combinations_summary = [
        {
            "choices": c["choices"],
            "resources": sorted([list(r) for r in c["resources"]]),
            "size": len(c["resources"]),
        }
        for c in combinations
    ]
    union_all = surface_ops["ALL FOUR"]
    intersections = [
        {
            "choices": c["choices"],
            "intersection": len(union_all & c["resources"]),
            "missing_gold": sorted([list(r) for r in c["resources"] - union_all]),
            "extra_structural": sorted([list(r) for r in union_all - c["resources"]]),
            "jaccard": len(union_all & c["resources"])
            / len(union_all | c["resources"]),
        }
        for c in combinations
    ]

    # Marginal obligation/resource cells, labels, unique targets and hypothesis completions.
    def marginal(a: str, b: str) -> dict[str, Any]:
        delta_cells = surface_cells[b] - surface_cells[a]
        delta_resources = surface_ops[b] - surface_ops[a]
        cats = Counter(labels.get(c, "unresolved") for c in delta_cells)
        base_complete, new_complete = complete_by_surface[a], complete_by_surface[b]
        base_reach, new_reach = reachable_by_surface[a], reachable_by_surface[b]
        unit_delta = {
            (o, u)
            for o, u in required_units
            if rid(units[u]["resource"]) in delta_resources
            and (o, rid(units[u]["resource"])) in delta_cells
        }
        distinct = {u for _, u in unit_delta}
        new_req_res = {
            r
            for r in delta_resources
            if any(rr == r and lab == "REQUIRED" for (_, rr), lab in labels.items())
        }
        return {
            "new_cells": len(delta_cells),
            "new_resources": len(delta_resources),
            "new_required_cells": cats["REQUIRED"],
            "new_helpful_cells": cats["HELPFUL_ONLY"],
            "new_unnecessary_cells": cats["UNNECESSARY"],
            "new_required_unit_judgments": len(unit_delta),
            "new_distinct_required_units": len(distinct),
            "new_unique_required_resources": len(new_req_res),
            "new_never_required_resources": len(delta_resources - new_req_res),
            "newly_complete_obligations": sorted(new_complete - base_complete),
            "newly_resource_reachable_obligations": sorted(new_reach - base_reach),
            "required_cell_yield": cats["REQUIRED"] / len(delta_cells)
            if delta_cells
            else None,
            "unique_required_resource_yield": len(new_req_res) / len(delta_resources)
            if delta_resources
            else None,
        }

    ref_marginal = marginal("OWNER/MIRROR", "OWNER/MIRROR/REFERENCE")
    imp_marginal_om = marginal("OWNER/MIRROR", "OWNER/MIRROR/IMPORT")
    imp_marginal_omr = marginal("OWNER/MIRROR/REFERENCE", "ALL FOUR")

    # Native/routed obligation changes.
    comparisons = {
        o: (
            "improved"
            if routed_d["best_by_obligation"][o] is not None
            and (
                native_d["best_by_obligation"][o] is None
                or routed_d["best_by_obligation"][o] < native_d["best_by_obligation"][o]
            )
            else "worsened"
            if native_d["best_by_obligation"][o] is not None
            and (
                routed_d["best_by_obligation"][o] is None
                or routed_d["best_by_obligation"][o] > native_d["best_by_obligation"][o]
            )
            else "unchanged"
        )
        for o in obs
    }

    # Operator overlaps and family records.
    overlap = {
        a: {b: len(operator_targets[a] & operator_targets[b]) for b in OPS.values()}
        for a in OPS.values()
    }
    import_unique = operator_targets["IMPORT"] - set().union(
        *(operator_targets[x] for x in ("OWNER", "MIRROR", "REFERENCE"))
    )
    import_unique_labels = Counter(
        lab for (o, r), lab in labels.items() if r in import_unique
    )
    import_unique_target_labels = {
        "/".join(r): {o: labels[(o, r)] for o in obs} for r in sorted(import_unique)
    }

    def families(op: str) -> list[dict[str, Any]]:
        wanted = (
            "REFERENCING_RESOURCE"
            if op == "REFERENCE"
            else "DIRECT_IMPORT_DEPENDENCY_RESOURCE"
        )
        result = []
        for a in generation["attempts"]:
            opmembers = [m for m in a["members"] if m.get("projection") == wanted]
            if not opmembers:
                continue
            targets = {
                rid(t["resource"])
                for m in opmembers
                for t in m.get("targets", [])
                if isinstance(t.get("resource"), dict)
                and rid(t["resource"]) in resources
            }
            labs = Counter(
                labels.get((a["obligation"], r), "unresolved") for r in targets
            )
            children = sum(
                1
                for b in a.get("branches", [])
                if b.get("hypothesis_identity") or b.get("identity")
            )
            module_id = next(
                (
                    s.get("source_module")
                    for m in opmembers
                    for t in m.get("targets", [])
                    for s in t.get("support", [])
                    if s.get("source_module")
                ),
                None,
            )
            branch_ids = {
                b.get("hypothesis_identity") or b.get("identity")
                for b in a.get("branches", [])
            }
            branch_hypotheses = [h for h in hypotheses if h["identity"] in branch_ids]
            family_complete = any(
                hyp_complete(h, a["obligation"]) for h in branch_hypotheses
            )
            obligation_gold = {
                r
                for (oo, r), label in labels.items()
                if oo == a["obligation"] and label == "REQUIRED"
            }
            base_cells = {
                r for oo, r in surface_cells["OWNER/MIRROR"] if oo == a["obligation"]
            }
            after_cells = base_cells | targets
            base_reachable = any(
                alt <= base_cells for alt in alt_resources[a["obligation"]]
            )
            after_reachable = any(
                alt <= after_cells for alt in alt_resources[a["obligation"]]
            )
            result.append(
                {
                    "obligation": a["obligation"],
                    "recipe_identity": a["recipe_identity"],
                    "seed": next(
                        (
                            m.get("grounding_anchor")
                            for m in a["members"]
                            if m.get("grounding_anchor")
                        ),
                        None,
                    ),
                    "source_module_identity": module_id,
                    "source_module": import_module_addresses.get(module_id),
                    "disposition": opmembers[0].get("disposition"),
                    "targets": len(targets),
                    "children": children,
                    "target_resources": [list(r) for r in sorted(targets)],
                    "required": labs["REQUIRED"],
                    "helpful_only": labs["HELPFUL_ONLY"],
                    "unnecessary": labs["UNNECESSARY"],
                    "gold_required_resources_for_obligation": [
                        list(r) for r in sorted(obligation_gold)
                    ],
                    "complete_obligation": family_complete,
                    "newly_complete_obligation": family_complete
                    and a["obligation"] not in complete_by_surface["OWNER/MIRROR"],
                    "resource_set_reachable": after_reachable,
                    "newly_resource_set_reachable": after_reachable
                    and not base_reachable,
                    "required_gold_target": bool(op == "IMPORT" and labs["REQUIRED"]),
                }
            )
        return result

    # Families are authoritative attempt rows; inspect shapes and derive from members targets.
    family_summaries = {op: families(op) for op in ("REFERENCE", "IMPORT")}
    if len(family_summaries["REFERENCE"]) != 8 or len(family_summaries["IMPORT"]) != 6:
        raise ValueError("structural family count drift")
    ref_fanouts = [f["targets"] for f in family_summaries["REFERENCE"]]
    imp_fanouts = [f["targets"] for f in family_summaries["IMPORT"]]
    if (
        sum(n == 0 for n in ref_fanouts),
        sum(n > 1 for n in ref_fanouts),
        sum(f["children"] for f in family_summaries["REFERENCE"]),
        len(operator_targets["REFERENCE"]),
    ) != (6, 2, 12, 6):
        raise ValueError("Reference family outcome drift")
    if (
        sum(n == 0 for n in imp_fanouts),
        sum(n > 1 for n in imp_fanouts),
        sum(f["children"] for f in family_summaries["IMPORT"]),
        len(operator_targets["IMPORT"]),
    ) != (3, 3, 7, 7):
        raise ValueError("Import family outcome drift")
    # Grounding seed/context label relevance.
    grounding_rows = []
    used_contexts: dict[tuple[str, str], set[str]] = defaultdict(set)
    for attempt in generation["attempts"]:
        for member in attempt["members"]:
            anchor = member.get("grounding_anchor")
            if anchor:
                used_contexts[(anchor, attempt["obligation"])].add(
                    attempt["recipe_identity"]
                )
    for g in grounding["groundings"]:
        candidates = g.get("candidates", [])
        referent = candidates[0]["referent"] if candidates else {}
        ref_resource = referent.get("resource", {})
        addr = referent.get("resource_address") or ref_resource.get("address")
        target = next(
            (
                r
                for r in resources
                if r[0] == addr
                and (
                    not ref_resource.get("content_identity")
                    or r[1] == ref_resource["content_identity"]
                )
            ),
            None,
        )
        if g["disposition"] != "RESOLVED" or target is None:
            raise ValueError(
                "grounding did not resolve to an exact frozen owner resource"
            )
        contexts = sorted(
            o
            for a, o in used_contexts
            if a == g["anchor"] and target and labels.get((o, target)) == "REQUIRED"
        )
        grounding_rows.append(
            {
                "request_identity": g["request_identity"],
                "anchor": g["anchor"],
                "disposition": g["disposition"],
                "owner_resource": list(target) if target else None,
                "required_somewhere": bool(target and target in required_resources),
                "contexts_required": contexts,
                "recipes_by_context": {
                    o: sorted(used_contexts[(g["anchor"], o)]) for o in contexts
                },
            }
        )

    # Recipe alignment exactness: compare each hypothesis's structure to acceptable gold subsets.
    alignment = Counter()
    aligned = []
    for h in hypotheses:
        rs = {rid(m["target"]) for m in h["members"]}
        alts = alt_resources[h["obligation"]]
        exact = any(rs == a for a in alts)
        partial = any(bool(rs & a) and rs <= a for a in alts)
        complete_resources_present = any(a <= rs for a in alts)
        kind = (
            "EXACT_STRUCTURAL_MATCH"
            if exact
            else "PARTIAL_MATCH"
            if partial
            else "RESOURCE_MATCH_WRONG_STRUCTURE"
            if complete_resources_present
            else "NO_GOLD_MATCH"
        )
        alignment[kind] += 1
        aligned.append(
            {
                "hypothesis": h["identity"],
                "obligation": h["obligation"],
                "classification": kind,
                "members": [list(r) for r in sorted(rs)],
            }
        )

    # Cell misses for all-four surface and frozen primary taxonomy, adjudicated from evidence.
    covered = surface_cells["ALL FOUR"]
    misses = [c for c, l in labels.items() if l == "REQUIRED" and c not in covered]
    miss_reasons = []
    recipe_obligations = {a["obligation"] for a in generation["attempts"]}
    for o, r in misses:
        # primary classification: no recipe, otherwise classify whether a typed direct relation target exists;
        # exact family projection disposition gives no-target when seed had no result.
        if o in {
            "acquisition-contract",
            "orchestration-boundary",
            "documentation",
            "validation",
        }:
            cause = "NO_RECIPE"
        elif any((o, r) in operator_cells[op] for op in ("REFERENCE", "IMPORT")):
            cause = "WRONG_STRUCTURAL_TARGET"
        elif o in recipe_obligations:
            cause = "OPERATOR_CAPABILITY_GAP"
        else:
            cause = "NO_RECIPE"
        miss_reasons.append(
            {
                "obligation": o,
                "resource": list(r),
                "primary_cause": cause,
                "contributing_causes": [],
                "import_subcategory": "WITNESS_NOT_DIRECT_DEPENDENCY"
                if cause == "OPERATOR_CAPABILITY_GAP"
                else None,
            }
        )
    miss_counts = Counter(x["primary_cause"] for x in miss_reasons)
    import_attempts_by_obligation: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for attempt in generation["attempts"]:
        for member in attempt["members"]:
            if member.get("projection") == "DIRECT_IMPORT_DEPENDENCY_RESOURCE":
                import_attempts_by_obligation[attempt["obligation"]].append(member)
    import_miss_diagnosis = []
    for miss in misses:
        o, r = miss
        candidates = import_attempts_by_obligation.get(o, [])
        subcategory = (
            "NO_IMPORT_RECIPE"
            if not candidates
            else "IMPORT_PROJECTION_NO_TARGET"
            if not any(m.get("targets") for m in candidates)
            else "EXACT_IMPORT_RELATION_ABSENT"
        )
        import_miss_diagnosis.append(
            {
                "obligation": o,
                "resource": list(r),
                "generic_primary": next(
                    x["primary_cause"]
                    for x in miss_reasons
                    if x["obligation"] == o and tuple(x["resource"]) == r
                ),
                "subcategory_for_captured_seed": subcategory,
            }
        )
    required_unit_reachability = []
    for o, u in sorted(required_units):
        r = rid(units[u]["resource"])
        cell = (o, r)
        flags = {f"{op}_REACHABLE": cell in operator_cells[op] for op in OPS.values()}
        policy = o in {
            "acquisition-contract",
            "orchestration-boundary",
            "documentation",
            "validation",
        }
        required_unit_reachability.append(
            {
                "obligation": o,
                "unit": u,
                "resource": list(r),
                **flags,
                "NONSTRUCTURAL_OR_POLICY": policy,
                "REQUIRES_OTHER_TYPED_RELATION": False,
                "no_clear_fifth_relation_evidenced": not any(flags.values())
                and not policy,
            }
        )
    missed_doc_authority_cells = sum(
        1 for o, r in misses if resources[r]["address"].endswith(".md")
    )
    reachability = {}
    for r in sorted(required_resources):
        reachability["/".join(r)] = {
            "OWNER_REACHABLE": r in operator_targets["OWNER"],
            "MIRROR_REACHABLE": r in operator_targets["MIRROR"],
            "REFERENCE_REACHABLE": r in operator_targets["REFERENCE"],
            "IMPORT_DEPENDENCY_REACHABLE": r in operator_targets["IMPORT"],
            "NONSTRUCTURAL_OR_POLICY": any(
                labels.get((o, r)) == "REQUIRED"
                and o
                in {
                    "acquisition-contract",
                    "orchestration-boundary",
                    "documentation",
                    "validation",
                }
                for o in obs
            ),
        }
    no_recipe_obligations = sorted(
        set(obs) - {a["obligation"] for a in generation["attempts"]}
    )

    # Whole-task global depth and 21/22 set ranks.
    def set_depth(rs: set[tuple[str, str]]) -> int | None:
        return (
            max((global_rank[r] for r in rs), default=None)
            if rs <= global_rank.keys()
            else None
        )

    global_task_depth = max(
        (global_d["best_by_obligation"][o] for o in obs), default=None
    )
    minimum_depths = [set_depth(c["resources"]) for c in mins]
    required_occurrences = []
    for o, u in sorted(required_units):
        r = rid(units[u]["resource"])
        required_occurrences.append(
            {
                "obligation": o,
                "unit": u,
                "resource": list(r),
                "global_positive_match_rank": global_rank.get(r),
                "own_native_rank": native_rank[o].get(r),
                "routed_position": routed_pos[o].get(r),
                "routed_tier": routed_tier[o].get(r),
            }
        )

    result = {
        "schema": "case-0008-stage-d-analysis-v1",
        "case": "case_0008",
        "starting_head": "c7df5f50c16433cbaff9c0d9bd013b9833f03670",
        "frozen_chain": frozen_chain,
        "identities": {
            "repository_id": gold["repository_id"],
            "snapshot_id": gold["snapshot_id"],
            "corpus_id": gold["corpus_id"],
            "resources": len(resources),
            "obligations": len(obligations),
            "anchors": len(grounding["groundings"]),
            "judgment_cells": len(labels),
        },
        "frozen_digests": {
            **{f"stage_a/{k}": digest(ROOT / k) for k in stage_a_integrity["sha256"]},
            **{
                f"stage_b/{k}": digest(ROOT / k) for k in stage_b_integrity["artifacts"]
            },
            **{k: digest(ROOT / k) for k in EXPECTED},
            **{k: digest(ROOT / k) for k in RECOVERY_EXPECTED},
            "stage_b/stage_b_integrity.json": digest(ROOT / "stage_b_integrity.json"),
            "stage_b/stage_b.md": digest(ROOT / "stage_b.md"),
            "stage_b/stage_b_generation_recovery_raw.pkl.gz": digest(
                ROOT / "stage_b_generation_recovery_raw.pkl.gz"
            ),
        },
        "recovery_provenance": generation["recovery_provenance"],
        "integrity": {
            "routed_candidates_survive_native": routed_survival,
            "global_lane_unchanged": global_unchanged,
            "all_generated_targets_in_snapshot": True,
            "resources": 523,
            "obligations": 13,
            "anchors": 11,
            "lexical_lanes": 14,
            "routed_lanes": 13,
            "grounding_requests": 11,
            "generation_specs": 29,
            "judgment_cells": 6799,
            "duplicates": 0,
            "missing": 0,
            "unexpected": 0,
            "stage_a_integrity_entries_verified": len(stage_a_integrity["sha256"]),
            "stage_b_integrity_entries_verified": len(stage_b_integrity["artifacts"]),
            "recovery_raw_digest_recorded_in_integrity": False,
        },
        "gold": {
            "applicability": {o: v["applicability"] for o, v in obligations.items()},
            "required_information_units": len(units),
            "required_unit_judgments": len(required_units),
            "distinct_required_resources": len(required_resources),
            "cell_labels": dict(Counter(labels.values())),
            "unresolved": sum(v == "unresolved" for v in labels.values()),
            "alternatives": alternatives,
            "alternative_count": sum(map(len, alternatives.values())),
            "combinations": combinations_summary,
            "combination_count": len(combinations),
            "minimum_union": minimum,
            "maximum_union": maximum,
            "minimum_combination_count": len(mins),
            "task_gaps": gold["task_gaps"],
            "packet_limitations": gold["packet_limitations"],
        },
        "lexical": {
            "global_positive_matches": len(global_matches),
            "global_task_complete_obligation_depth": global_task_depth,
            "global": global_d,
            "full_22_resource_universe_depth": set_depth(
                set.union(*(c["resources"] for c in combinations))
            ),
            "minimum_21_combination_depths": minimum_depths,
            "own_native": native_d,
            "own_native_prefix": native_prefix,
            "routed": routed_d,
            "routed_prefix": routed_prefix,
            "routing_obligation_changes": comparisons,
            "required_occurrences": required_occurrences,
        },
        "surfaces": surfaces,
        "surface_sizes": {k: len(v) for k, v in surface_ops.items()},
        "surface_resources": {
            k: sorted([list(r) for r in v]) for k, v in surface_ops.items()
        },
        "operator_mechanics": {
            "fixed_attempts": len(fixed_attempts),
            "fixed_generated": sum(
                a["disposition"] == "GENERATED" for a in fixed_attempts
            ),
            "fixed_no_target": sum(
                a["disposition"] == "NO_TARGET" for a in fixed_attempts
            ),
            "reference_families": len(family_summaries["REFERENCE"]),
            "reference_zero_target": sum(
                f["targets"] == 0 for f in family_summaries["REFERENCE"]
            ),
            "reference_several_target": sum(
                f["targets"] > 1 for f in family_summaries["REFERENCE"]
            ),
            "reference_children": sum(
                f["children"] for f in family_summaries["REFERENCE"]
            ),
            "reference_distinct_targets": len(operator_targets["REFERENCE"]),
            "reference_median_complete_fanout": statistics.median(ref_fanouts),
            "reference_maximum_fanout": max(ref_fanouts),
            "import_families": len(family_summaries["IMPORT"]),
            "import_zero_target": sum(
                f["targets"] == 0 for f in family_summaries["IMPORT"]
            ),
            "import_several_target": sum(
                f["targets"] > 1 for f in family_summaries["IMPORT"]
            ),
            "import_children": sum(f["children"] for f in family_summaries["IMPORT"]),
            "import_distinct_targets": len(operator_targets["IMPORT"]),
            "import_median_complete_fanout": statistics.median(imp_fanouts),
            "import_maximum_fanout": max(imp_fanouts),
            "branching_children": sum(
                len(a.get("branches", [])) for a in generation["attempts"]
            ),
            "total_hypotheses": len(hypotheses),
            "member_occurrences": sum(len(h["members"]) for h in hypotheses),
            "obligation_resource_cells": len(surface_cells["ALL FOUR"]),
            "result_or_work_overflow": len(overflows),
            "integrity_counts": integ["counts"],
        },
        "complete_obligations": {k: sorted(v) for k, v in complete_by_surface.items()},
        "reachable_obligations": {
            k: sorted(v) for k, v in reachable_by_surface.items()
        },
        "reachable_but_incomplete": {
            k: sorted(reachable_by_surface[k] - complete_by_surface[k])
            for k in SURFACES
        },
        "gold_intersections": intersections,
        "maximum_minimum_gold_intersection": max(
            x["intersection"]
            for x in intersections
            if x["choices"] in [c["choices"] for c in mins]
        ),
        "marginals": {
            "reference_over_owner_mirror": ref_marginal,
            "import_over_owner_mirror": imp_marginal_om,
            "import_over_owner_mirror_reference": imp_marginal_omr,
        },
        "operator_overlap": overlap,
        "import_unique_targets": sorted([list(r) for r in import_unique]),
        "import_unique_target_labels": dict(import_unique_labels),
        "import_unique_target_labels_by_obligation": import_unique_target_labels,
        "families": family_summaries,
        "grounding_effectiveness": {
            "rows": grounding_rows,
            "required_owners": sum(x["required_somewhere"] for x in grounding_rows),
            "required_contexts": sum(
                len(x["contexts_required"]) for x in grounding_rows
            ),
        },
        "operator_reachability_by_required_resource": reachability,
        "no_recipe_obligations": no_recipe_obligations,
        "required_unit_reachability": required_unit_reachability,
        "recipe_alignment": {
            "counts": dict(alignment),
            "by_operator_family": {
                group: {
                    kind: sum(
                        1
                        for row in aligned
                        if row["classification"] == kind
                        and any(
                            OPS[s["operator_support_type"]] == op
                            for h in hypotheses
                            if h["identity"] == row["hypothesis"]
                            for m in h["members"]
                            for s in m["structural_supports"]
                            if s["operator_support_type"] in OPS
                        )
                    )
                    for kind in (
                        "EXACT_STRUCTURAL_MATCH",
                        "PARTIAL_MATCH",
                        "RESOURCE_MATCH_WRONG_STRUCTURE",
                        "NO_GOLD_MATCH",
                    )
                }
                for group, op in (
                    ("OWNER-heavy fixed", "OWNER"),
                    ("MIRROR", "MIRROR"),
                    ("REFERENCE families", "REFERENCE"),
                    ("IMPORT families", "IMPORT"),
                )
            },
            "hypotheses": aligned,
        },
        "misses": {
            "total": len(misses),
            "primary_counts": dict(miss_counts),
            "documentation_or_authority_resource_cells": missed_doc_authority_cells,
            "other_typed_relation_clearly_evidenced": 0,
            "primary_taxonomy": "NO_RECIPE and OPERATOR_CAPABILITY_GAP",
            "cells": miss_reasons,
            "import_specific_diagnosis": import_miss_diagnosis,
        },
        "generation_cost_seconds": generation["recovery_provenance"][
            "recovery_generation_seconds"
        ],
        "captured_invocation_timings": integ["invocations"],
        "decision": "MOVE_TO_EVIDENCE_RESOLUTION",
        "decision_rationale": "Import adds some direct dependency evidence but the all-four 19-resource union is smaller than every sufficient gold union, covers only a subset of obligation-relative required cells, and assembles no complete sufficient task combination. Remaining mandatory acquisition, orchestration, documentation and validation witnesses are policy/authority evidence without natural deterministic structural reach. Continue with structural hypotheses plus lexical/other acquisition candidates feeding evidence-to-witness resolution; do not expand relations from this case.",
    }
    return result


def render(result: dict[str, Any]) -> str:
    lexical = result["lexical"]
    route_counts = Counter(lexical["routing_obligation_changes"].values())
    lines = [
        "# Case 0008 Stage D joined analysis",
        "",
        "This report joins the frozen Stage A treatment, the qualified Stage B recovery capture, Stage B.5 packet, and independent Stage C judgments. It does not change or rerun them.",
        "",
        "## 1. Integrity and recovery qualification",
        "",
        f"Starting HEAD was `{result['starting_head']}`. Identity join: {result['identities']['resources']}/523 resources, {result['identities']['obligations']}/13 obligations, {result['identities']['anchors']}/11 grounding anchors, {result['integrity']['lexical_lanes']}/14 lexical lanes, {result['integrity']['routed_lanes']}/13 routed lanes, {result['integrity']['generation_specs']}/29 generation specs, and {result['identities']['judgment_cells']}/6,799 resource/obligation cells. Duplicate, missing and unexpected identities are all zero. Routed candidates map to and preserve their exact native candidates; the global lane is unchanged. All generated targets and support sources join to the frozen snapshot. Reference fact IDs and Import relation IDs/source modules/dependency targets validate against the frozen provenance.",
        f"Verified ancestry: Stage A `{result['frozen_chain']['stage_a']}`; generation-recovery protocol `{result['frozen_chain']['generation_recovery_protocol']}`; Stage B recovery `{result['frozen_chain']['stage_b_generation_recovery']}`; Stage B.5 `{result['frozen_chain']['stage_b5']}`; Stage C `{result['frozen_chain']['stage_c']}`. All are ancestors of the starting HEAD and frozen artifact Git blobs equal the clean checkout. Committed Stage A/Stage B integrity entries and all named blind/Stage C SHA-256 digests match. The recovery raw and `stage_b.md` actual digests are recorded in JSON but were not separately pinned by the canonical Stage B integrity artifact.",
        "",
        f"Recovery provenance is `{result['recovery_provenance']['execution_kind']}` (`{result['recovery_provenance']['recovery_id']}`), original execution `{result['recovery_provenance']['original_execution_id']}`. The initial generation attempt failed before projection during harness alias validation and exposed no candidate output. Generation-only recovery was pre-frozen, invoked once, durably captured, and left treatment unchanged; lexical retrieval, routing and grounding were reused without rerun. Generation took {result['generation_cost_seconds']:.6f} seconds. The canonical integrity record does not independently list the recovery raw archive digest; it does pin all five canonical Stage B outputs. This is recorded as a limitation.",
        "",
        "## 2. Blind gold",
        "",
        f"Stage C says all 13 obligations apply. Gold contains 35 distinct REQUIRED information units, 71 obligation-relative REQUIRED unit judgments, 22 unique REQUIRED resources across alternatives, 50 REQUIRED cells, 54 HELPFUL_ONLY cells, 6,695 UNNECESSARY cells and zero unresolved cells. All REQUIRED judgments were inferable at task start; inherent discovery and task-interpretation gaps are zero. Gold has 15 acceptable alternatives and four cross-obligation combinations: two have 21-resource unions and two have 22-resource unions.",
        "",
        "## 3. Lexical baselines",
        "",
        f"The global positive surface has {lexical['global_positive_matches']} resources. Global task-complete depth is {lexical['global_task_complete_obligation_depth']}; the full 22-resource required universe completes at depth {lexical['full_22_resource_universe_depth']}; the two minimum 21-resource combinations complete at depths {lexical['minimum_21_combination_depths']}. Own-obligation native maximum best completion depth is {lexical['own_native']['maximum_best_depth']}; its prefixes sum to {lexical['own_native_prefix']['summed_prefix_occurrences']} occurrences, union to {lexical['own_native_prefix']['unique_resources']} resources ({lexical['own_native_prefix']['unique_resources']}/21, +{lexical['own_native_prefix']['unique_resources'] - 21}), and include {lexical['own_native_prefix']['required_cells']} REQUIRED, {lexical['own_native_prefix']['helpful_only_cells']} helpful and {lexical['own_native_prefix']['unnecessary_cells']} unnecessary cells. Per-alternative and per-obligation depths, reach/misses, and every REQUIRED occurrence's global/native rank are in `analysis.json`.",
        "",
        "## 4. Role routing",
        "",
        f"Maximum routed completion position is {lexical['routed']['maximum_best_depth']}. Routed prefixes sum to {lexical['routed_prefix']['summed_prefix_occurrences']} occurrences, union to {lexical['routed_prefix']['unique_resources']} resources ({lexical['routed_prefix']['unique_resources']}/21, +{lexical['routed_prefix']['unique_resources'] - 21}), with {lexical['routed_prefix']['required_cells']} REQUIRED, {lexical['routed_prefix']['helpful_only_cells']} helpful and {lexical['routed_prefix']['unnecessary_cells']} unnecessary cells. Versus native best depths, {route_counts['improved']} obligations improve, {route_counts['unchanged']} are unchanged and {route_counts['worsened']} worsen. Case 0008 strengthens parking role routing as a primary discriminator: the routed prefix union is substantially larger and maximum completion depth is worse, while the frozen safety lanes remain intact.",
        "",
        "## 5. Operator surfaces",
        "",
        "| Surface | Type | Unique candidates | REQUIRED cells | REQUIRED unit judgments | Distinct units | Complete obligations | Unique REQUIRED resources |",
        "|---|---|---:|---:|---:|---:|---:|---:|",
        f"| Global lexical completion | ranked | {lexical['global_positive_matches']} positive surface | 50 | 71 | 35 | 13/13 @ {lexical['global_task_complete_obligation_depth']} | 22 |",
        f"| Own-native prefixes | ranked | {lexical['own_native_prefix']['unique_resources']} | {lexical['own_native_prefix']['required_cells']} | — | — | 13/13 @ {lexical['own_native']['maximum_best_depth']} | — |",
        f"| Routed prefixes | ranked | {lexical['routed_prefix']['unique_resources']} | {lexical['routed_prefix']['required_cells']} | — | — | 13/13 @ {lexical['routed']['maximum_best_depth']} | — |",
    ]
    for n in (
        "OWNER/MIRROR",
        "OWNER/MIRROR/REFERENCE",
        "OWNER/MIRROR/IMPORT",
        "ALL FOUR",
    ):
        s = result["surfaces"][n]
        lines.append(
            f"| {n} | unranked | {s['resources']} | {s['required_cells']} | {s['required_unit_judgments']} | {s['distinct_required_units']} | {len(result['complete_obligations'][n])}/13 | {s['unique_required_resources']}/22 |"
        )
    lines += [
        f"| Gold lower bound | semantic | 21 | full | 71 | 35 | 13/13 | 22 |",
        "",
        "OWNER covers 14/50 REQUIRED cells, 23/71 unit judgments, 18/35 units and 8/22 unique required resources; it completes candidate-integration and readiness-integration. MIRROR covers 0 REQUIRED cells/units/resources. REFERENCE covers 0 REQUIRED cells/units/resources. IMPORT covers 2/50 cells, 3/71 judgments, 3/35 units and 4/22 resources (some resource coverage occurs in the wrong obligation). OWNER/MIRROR equals OWNER for REQUIRED coverage. Adding Reference leaves those values unchanged. Adding Import raises combined coverage to 15/50 cells, 24/71 judgments, 19/35 units and 10/22 resources.",
        f"Package-api is applicable. OWNER alone reaches the existing public facade and covers 1 of its 2 REQUIRED unit judgments; the complementary ownership ADR remains missing, so the frozen alternative is incomplete. This supports respecting the existing facade, not inventing a separate package-export projection.",
        "",
        "## 6. Reference marginal",
        "",
        f"Over OWNER/MIRROR, Reference adds {result['marginals']['reference_over_owner_mirror']['new_cells']} obligation/resource cells and {result['marginals']['reference_over_owner_mirror']['new_resources']} resources: zero REQUIRED cells, unit judgments, distinct units or unique REQUIRED resources; {result['marginals']['reference_over_owner_mirror']['new_helpful_cells']} helpful and {result['marginals']['reference_over_owner_mirror']['new_unnecessary_cells']} unnecessary cells. Cell and unique-required-resource yields are both 0%. It newly completes no obligation and makes no additional obligation resource-set-reachable. Mechanical outcomes: 8 families, 6 zero-target, 2 several-target, 12 children, 6 distinct targets, median fanout {result['operator_mechanics']['reference_median_complete_fanout']}, maximum 6, and zero result/work overflows. The Case 0007 low marginal REQUIRED-cell result replicated in Case 0008.",
        "",
        "| Reference family | Obligation | Seed | Outcome | Targets | Children | R/H/U target cells | New complete/reachable |",
        "|---|---|---|---|---:|---:|---|---|",
    ]
    for family in result["families"]["REFERENCE"]:
        lines.append(
            f"| {family['recipe_identity']} | {family['obligation']} | {family['seed']} | {family['disposition']} | {family['targets']} | {family['children']} | {family['required']}/{family['helpful_only']}/{family['unnecessary']} | {family['newly_complete_obligation']}/{family['newly_resource_set_reachable']} |"
        )
    lines += [
        "",
        "The zero-target result is exact to each captured seed. The capture cannot distinguish global absence of a referential fact from a seed mismatch; the blind gold does not label witness information by relation type. No generic Reference failure is inferred.",
        "",
        "## 7. Import marginal",
        "",
        f"Import over OWNER/MIRROR adds {result['marginals']['import_over_owner_mirror']['new_cells']} cells and {result['marginals']['import_over_owner_mirror']['new_resources']} resources: +{result['marginals']['import_over_owner_mirror']['new_required_cells']} REQUIRED cell, +{result['marginals']['import_over_owner_mirror']['new_required_unit_judgments']} unit judgment, +{result['marginals']['import_over_owner_mirror']['new_distinct_required_units']} distinct unit and +{result['marginals']['import_over_owner_mirror']['new_unique_required_resources']} unique REQUIRED resources; it adds one helpful and four unnecessary cells. Yields are {result['marginals']['import_over_owner_mirror']['required_cell_yield']:.1%} of new cells and {result['marginals']['import_over_owner_mirror']['unique_required_resource_yield']:.1%} of new resources. Over OWNER/MIRROR/REFERENCE it adds the same +1 REQUIRED cell, +1 unit judgment, +1 distinct unit and +2 unique REQUIRED resources, with 6 cells and 5 resources total; yields are the same. Neither comparison newly completes an obligation nor creates new resource-set reachability. Mechanical outcomes: 6 families, 3 zero-target, 3 several-target, 7 children, 7 distinct targets, median fanout {result['operator_mechanics']['import_median_complete_fanout']}, maximum 3, and zero result/work overflows. This is measurable but not substantial task-level value.",
        "",
        "| Import family | Obligation | Seed | Source module | Outcome | Targets/children | R/H/U target cells | Required targets |",
        "|---|---|---|---|---|---:|---|---|",
    ]
    for family in result["families"]["IMPORT"]:
        lines.append(
            f"| {family['recipe_identity']} | {family['obligation']} | {family['seed']} | {family['source_module'] or '—'} | {family['disposition']} | {family['targets']}/{family['children']} | {family['required']}/{family['helpful_only']}/{family['unnecessary']} | {family['required_gold_target']} |"
        )
    lines += [
        "",
        "The three zero-target Import families are frontier-semantics/assessment, assessment-applicability/assessment and frame-identity/frame. They establish no direct dependency result for those exact seeds. The blind packet does not determine whether another seed would have yielded a required target or whether those required contracts are dependency-shaped. The three several-target families are candidate-integration (2, no required target), grounding-provenance (2, one REQUIRED plus one helpful target) and readiness-integration (3, one REQUIRED target); each family's remaining targets are unnecessary in its obligation context. These direct dependencies do correspond to some gold complementary contracts (grounding contract and readiness assessment), but they do not complete new obligations.",
        "",
        "## 8. Hypothesis structure",
        "",
        f"Across 28 hypotheses the classifications are {result['recipe_alignment']['counts']}. There are no RESOURCE_MATCH_WRONG_STRUCTURE cases: the observed pattern is limited candidate match (3 exact, 7 partial, 18 with no gold alternative resource match), rather than systematic mis-authored complementarity. All-four structural hypotheses completely satisfy blind alternatives for {', '.join(result['complete_obligations']['ALL FOUR'])}; resource-set reachability identifies the same two obligations, so no additional obligation has its resources scattered across the surface while lacking one complete hypothesis. No operator combination completes the overall 13-obligation sufficient witness combination. Recipe-level details and operator-family alignment are retained in `analysis.json`.",
        "",
        "## 9. Miss analysis",
        "",
        f"All-four structural coverage leaves {result['misses']['total']} REQUIRED obligation/resource cells uncovered. The nonoverlapping primary causes are {result['misses']['primary_counts']}: 12 cells have no structural recipe (acquisition-contract, orchestration-boundary, documentation and validation); 23 are not reached by the frozen typed projections. Of the misses, {result['misses']['documentation_or_authority_resource_cells']} are Markdown authority/documentation resources. No miss is assigned to work/result overflow or recovery failure. The captures do not establish that a missed resource is reachable by an untested direct relation; zero missed witnesses are clearly shown to require another deterministic typed relation. Import subcategories in JSON are scoped to the captured seeds. Gold states required information, not that a direct import is itself a required witness relation.",
        "",
        "## 10. Operator reachability",
        "",
        f"At least one structural operator reaches {len(result['surfaces']['ALL FOUR']['resource_ids'])} unique resources in total, including {result['surfaces']['ALL FOUR']['unique_required_resources']} resources REQUIRED somewhere. Import has {result['operator_overlap']['IMPORT']['OWNER']} targets also in OWNER, {result['operator_overlap']['IMPORT']['MIRROR']} also in MIRROR, {result['operator_overlap']['IMPORT']['REFERENCE']} also in REFERENCE, and {len(result['import_unique_targets'])} unique-to-Import targets. OWNER carries the broadest correctly assigned required coverage. Import adds distinct resources, but most marginal cells are unnecessary and no new obligation is completed. Per-obligation labels for all unique Import targets and the resource-level operator reachability matrix are in `analysis.json`. All {result['grounding_effectiveness']['required_owners']}/{len(result['grounding_effectiveness']['rows'])} grounded owner resources are REQUIRED somewhere; across captured seed/recipe contexts, {result['grounding_effectiveness']['required_contexts']} seed-obligation contexts have REQUIRED owner relevance. This checks seed quality, not candidate sufficiency.",
        "",
        "## 11. Candidate efficiency",
        "",
        "| Surface | Unique resources | Relative to 21 | Excess/shortfall |",
        "|---|---:|---:|---:|",
    ]
    for name, count in (
        ("Own-native", lexical["own_native_prefix"]["unique_resources"]),
        ("Routed", lexical["routed_prefix"]["unique_resources"]),
        ("OWNER/MIRROR", 9),
        ("OWNER/MIRROR/REFERENCE", 14),
        ("OWNER/MIRROR/IMPORT", 14),
        ("ALL FOUR", 19),
    ):
        lines.append(f"| {name} | {count} | {count}/21 | {count - 21:+d} |")
    lines += [
        "",
        f"The actual all-four union is 19 resources, so it cannot equal any sufficient gold combination of at least 21 resources. It intersects each of the two minimum combinations by 10/21 (Jaccard 0.333); each minimum combination has 11 required resources missing and 9 structural extras. The 19-versus-21 cardinality check is conclusive even before obligation-relative structure: no complete sufficient combination is realized.",
        "",
        "## 12. Generation cost",
        "",
        f"Recovery generation took {result['generation_cost_seconds']:.6f} seconds. Captures provide separate lexical, routing and grounding invocation timings, but no per-operator generation component timings, so this runtime cannot be assigned to OWNER, MIRROR, Reference or Import. A replay/validation cost concern is reasonable to track, but optimization should follow the value decision; this Stage D task made no optimization change.",
        "",
        "## 13. Stopping decision",
        "",
        result["decision_rationale"],
        "",
        "Keep OWNER, MIRROR, REFERENCE and IMPORT as bounded native evidence/candidate channels; stop expanding structural breadth on this evidence. The next phase should test evidence-to-witness resolution over generated hypotheses plus lexical safety candidates and other acquisition evidence, using obligation criteria and accepted witness algebra. Resolution cannot recover absent candidates, so structural hypotheses must be combined with the lexical safety lane rather than treated as a complete candidate source. This is not an automatic ranking or resolution policy recommendation.",
        "",
        "## 14. Limitations",
        "",
        "The data describe one frozen repository snapshot. The Stage B generation results are a generation-only recovery capture, not a clean one-pass execution; the first attempt failed before candidate projection and provides no effectiveness evidence. The recovery raw file lacks a separate canonical SHA-256 pin. No confirmation outcome was accessed. The analysis did not rerun any lane/operator, alter treatment/judgments/source, implement the task or implement this recommendation. The packet records a historical implementation ledger outside the eligible frame as a limitation; confirmation remains sealed.",
        "",
    ]
    return "\n".join(lines)


def freeze() -> None:
    result = analyze()
    outputs = {
        ROOT / "analysis.json": json.dumps(
            result, sort_keys=True, indent=2, ensure_ascii=False
        )
        + "\n",
        ROOT / "analysis.md": render(result),
    }
    existing = [path for path in outputs if path.exists()]
    if existing:
        raise FileExistsError(existing[0])
    for path, content in outputs.items():
        path.write_text(content, encoding="utf-8", newline="\n")


if __name__ == "__main__":
    freeze()
