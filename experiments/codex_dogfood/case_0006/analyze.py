"""Deterministically join frozen Case 0006 outputs; never executes treatment."""

from __future__ import annotations

import argparse
import ast
import gzip
import hashlib
import itertools
import json
import pickle
import subprocess
from collections import Counter
from pathlib import Path

CASE_DIR = Path(__file__).resolve().parent
REPO = CASE_DIR.parents[2]
ADJ = CASE_DIR / "adjudication"
ANALYSIS_JSON = CASE_DIR / "analysis.json"
ANALYSIS_MD = CASE_DIR / "analysis.md"
ANALYSIS_SHA = CASE_DIR / "analysis.sha256"

CHAIN = {
    "stage_a": "e7aed4162672dd859a0a8a33a2b718dda8425495",
    "stage_b_recovery_protocol": "56f18901b5acae47b9c07811dd18eb4770c56285",
    "stage_b_recovery_capture": "aae9da9741924dfa599b55b4fb913163caf96131",
    "stage_b5": "e076632a5e38d9d598c0fc109a12b52b424ecf22",
    "stage_c": "e3c1fa5144e318a2ee5985bfaf5730833ef43d4d",
}
EXPECTED_SUBJECT = "Freeze Case 0006 blind obligation judgments"
RECOVERY_ID = "case-0006-stage-b-recovery-1"
REPOSITORY = "d0e7c9e0-0c4f-4ea7-a345-3eb793ab6eb8"
SNAPSHOT = "ba654221b65584aebdd98804369864162ac3f7da1bf8862abee06ce4d2127a55"
FRAME = "49c69d2db7c6616731d9c24519a48d47a13a2ee991d46aaaf33d1f5d55b212b9"
OBLIGATIONS = (
    "hypothesis-records",
    "member-complementarity",
    "generated-integration",
    "accepted-promotion",
    "assessment-readiness",
    "provenance-frame",
    "package-integration",
    "tests",
    "documentation",
    "validation",
)


def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def canon(value: object) -> bytes:
    return (
        json.dumps(value, ensure_ascii=False, sort_keys=True, indent=2) + "\n"
    ).encode()


def read_json(name: str) -> dict:
    return json.loads((CASE_DIR / name).read_bytes())


def assert_(condition: bool, message: str) -> None:
    if not condition:
        raise ValueError(message)


def identity(value: dict) -> tuple[str, str]:
    return value["address"], value["content_identity"]


def commit_tree_bytes(commit: str, path: str) -> bytes:
    return subprocess.check_output(["git", "show", f"{commit}:{path}"], cwd=REPO)


def verify_chain() -> dict:
    expected_order = list(CHAIN.values())
    parents = {}
    for name, commit in CHAIN.items():
        line = (
            subprocess.check_output(
                ["git", "rev-list", "--parents", "-n", "1", commit], cwd=REPO, text=True
            )
            .strip()
            .split()
        )
        assert_(line[0] == commit, f"Missing/wrong chain commit {name}")
        parents[name] = line[1:]
    assert_(
        parents["stage_b_recovery_protocol"] == [CHAIN["stage_a"]],
        "Stage B protocol parent",
    )
    assert_(
        parents["stage_b_recovery_capture"] == [CHAIN["stage_b_recovery_protocol"]],
        "Stage B capture parent",
    )
    assert_(
        parents["stage_b5"] == [CHAIN["stage_b_recovery_capture"]], "Stage B.5 parent"
    )
    assert_(parents["stage_c"] == [CHAIN["stage_b5"]], "Stage C parent")
    return {"commits": CHAIN, "parents": parents, "order": expected_order}


def verify_hashes() -> dict:
    hashes = {}
    stage_a_manifest = read_json("integrity.json")
    for name, expected in stage_a_manifest.items():
        actual = sha((CASE_DIR / name).read_bytes())
        assert_(actual == expected, f"Stage A integrity mismatch: {name}")
        assert_(
            sha(
                commit_tree_bytes(
                    CHAIN["stage_a"], f"experiments/codex_dogfood/case_0006/{name}"
                )
            )
            == expected,
            f"Stage A committed artifact mismatch: {name}",
        )
        hashes[f"stage_a/{name}"] = actual
    stage_b_manifest = read_json("stage_b_integrity.json")
    for name, expected in stage_b_manifest["artifacts"].items():
        actual = sha((CASE_DIR / name).read_bytes())
        assert_(actual == expected, f"Stage B recovery integrity mismatch: {name}")
        assert_(
            sha(
                commit_tree_bytes(
                    CHAIN["stage_b_recovery_capture"],
                    f"experiments/codex_dogfood/case_0006/{name}",
                )
            )
            == expected,
            f"Stage B committed artifact mismatch: {name}",
        )
        hashes[f"stage_b_recovery/{name}"] = actual
    raw_hash = sha((CASE_DIR / "stage_b_recovery_raw.pkl.gz").read_bytes())
    assert_(
        raw_hash == "9b501f58374e442dd3f0ae4b2246a17a3cebc0fa3e99581873e5d579b3130c9e",
        "Recovery raw digest",
    )
    assert_(
        sha(
            commit_tree_bytes(
                CHAIN["stage_b_recovery_capture"],
                "experiments/codex_dogfood/case_0006/stage_b_recovery_raw.pkl.gz",
            )
        )
        == raw_hash,
        "Recovery raw commit mismatch",
    )
    hashes["stage_b_recovery/stage_b_recovery_raw.pkl.gz"] = raw_hash
    for name in (
        "stage_b_integrity.json",
        "stage_b_recovery_protocol.md",
        "stage_b_recovery_started.json",
        "stage_b_attempt_1.md",
    ):
        blob = (CASE_DIR / name).read_bytes()
        actual = sha(blob)
        assert_(
            sha(
                commit_tree_bytes(
                    CHAIN["stage_b_recovery_capture"],
                    f"experiments/codex_dogfood/case_0006/{name}",
                )
            )
            == actual,
            f"Recovery audit artifact drift: {name}",
        )
        hashes[f"stage_b_recovery/{name}"] = actual
    for name, expected in (
        (
            "adjudication/blind_manifest.json",
            "8bf0559814df54c246514e56fb7d92937828f9e50f9e17620a2c1acdc2934b49",
        ),
        (
            "adjudication/blind_resources.json.gz",
            "a03cdd8dc39d56b4a719be43ca38f2ced8f4df6e0b304ec8187914040b3ebb2a",
        ),
    ):
        actual = sha((CASE_DIR / name).read_bytes())
        assert_(actual == expected, f"Stage B.5 packet digest: {name}")
        assert_(
            sha(
                commit_tree_bytes(
                    CHAIN["stage_b5"], f"experiments/codex_dogfood/case_0006/{name}"
                )
            )
            == expected,
            f"Stage B.5 committed artifact mismatch: {name}",
        )
        hashes[f"stage_b5/{name}"] = actual
    judgments = (ADJ / "judgments.json").read_bytes()
    judgment_hash = sha(judgments)
    assert_(
        judgment_hash
        == "43b88ed5ae42f6fb4f55d1c75358adbbfb29ed25c624583e0c8ef7fbb3f535e3",
        "Stage C digest",
    )
    assert_(
        sha(
            commit_tree_bytes(
                CHAIN["stage_c"],
                "experiments/codex_dogfood/case_0006/adjudication/judgments.json",
            )
        )
        == judgment_hash,
        "Stage C committed artifact mismatch",
    )
    hashes["stage_c/judgments.json"] = judgment_hash
    return hashes


def load_frozen_inputs() -> dict:
    data = gzip.decompress((CASE_DIR / "inputs.pkl.gz").read_bytes())
    assert_(
        sha((CASE_DIR / "inputs.pkl.gz").read_bytes())
        == "572b8a575e08fc0012871bbddcbe780b026be03bdca670e607a9f09988ccd402",
        "Frozen input archive digest",
    )
    return pickle.loads(data)


def main_analysis() -> dict:
    chain = verify_chain()
    artifact_hashes = verify_hashes()
    treatment, pre = read_json("treatment.json"), read_json("pre_retrieval.json")
    retrieval, routing = read_json("retrieval.json"), read_json("routing.json")
    grounding, generation = read_json("grounding.json"), read_json("generation.json")
    judgments = json.loads((ADJ / "judgments.json").read_bytes())
    packet = json.loads(gzip.decompress((ADJ / "blind_resources.json.gz").read_bytes()))
    frozen = load_frozen_inputs()

    blind_manifest = json.loads((ADJ / "blind_manifest.json").read_bytes())
    assert_(
        blind_manifest["case_identity"] == "case_0006"
        and blind_manifest["task_identity"]
        == "codex-dogfood-case-0006-resolution-recording",
        "Blind packet case/task identity",
    )
    assert_(
        blind_manifest["repository_id"] == REPOSITORY
        and blind_manifest["repository_snapshot_id"] == SNAPSHOT
        and blind_manifest["eligible_frame_identity"] == FRAME,
        "Blind packet repository/frame",
    )
    for name, value in (
        ("case", "case_0006"),
        ("task_identity", "codex-dogfood-case-0006-resolution-recording"),
    ):
        assert_(
            treatment.get(name) == value and pre.get(name) == value,
            f"Treatment identity {name}",
        )
    assert_(
        judgments["case_identity"] == "case_0006"
        and judgments["task_identity"] == treatment["task_identity"],
        "Gold identity",
    )
    assert_(treatment["task_identity"] == pre["task_identity"], "Task join")
    assert_(
        pre["repository_id"] == retrieval["repository_id"] == REPOSITORY,
        "Repository join",
    )
    assert_(pre["snapshot_id"] == retrieval["snapshot_id"] == SNAPSHOT, "Snapshot join")
    assert_(
        pre["eligible_corpus_id"] == FRAME
        and judgments["eligible_frame_identity"] == FRAME,
        "Frame identity",
    )
    assert_(
        pre["frame_resource_count"] == len(pre["eligible_resources"]) == 531,
        "Eligible count",
    )
    assert_(
        len(treatment["obligations"]) == len(treatment["obligation_queries"]) == 10,
        "Treatment obligation/query count",
    )
    assert_(
        len(treatment["anchors"])
        == len({a["identity"] for a in treatment["anchors"]})
        == 10,
        "Shared anchor count/identity",
    )
    assert_(
        len(treatment["grounding_requests"]) == len(grounding["requests"]) == 9,
        "Grounding count",
    )
    assert_(
        len(treatment["generation_recipes"]) == len(generation["recipes"]) == 9,
        "Recipe count",
    )
    assert_(
        grounding["execution_kind"]
        == generation["execution_kind"]
        == retrieval["execution_kind"]
        == routing["execution_kind"]
        == "RECOVERY",
        "Recovery provenance",
    )
    assert_(
        all(
            x["recovery_id"] == RECOVERY_ID
            for x in (grounding, generation, retrieval, routing)
        ),
        "Recovery ID",
    )
    assert_(
        read_json("stage_b_integrity.json")["recovery_id"] == RECOVERY_ID,
        "Recovery integrity identity",
    )

    resources = {r["address"]: r for r in packet["resources"]}
    assert_(len(resources) == 531, "Archive resource count")
    packet_ids = {(r["address"], r["content_identity"]) for r in packet["resources"]}
    pre_ids = {(r["address"], r["content_identity"]) for r in pre["eligible_resources"]}
    gold_ids = {identity(r) for r in judgments["eligible_resource_identities"]}
    assert_(
        packet_ids == pre_ids == gold_ids and len(packet_ids) == 531,
        "Resource identity join",
    )
    units = judgments["information_units"]
    unit_resource = {k: identity(v["resource_identity"])[0] for k, v in units.items()}
    obligation_map = {o["identity"]: o for o in judgments["judgments"]}
    assert_(set(obligation_map) == set(OBLIGATIONS), "Gold obligation set")
    required_units = {}
    required_cells = {}
    helpful_cells = {}
    for oid, judgment in obligation_map.items():
        required_units[oid] = sorted(
            {
                m
                for alt in judgment["acceptable_witness_alternatives"]
                for m in alt["all"]
            }
        )
        assert_(judgment["applicability"] == "APPLICABLE", f"Applicability {oid}")
        required_cells[oid] = sorted({unit_resource[u] for u in required_units[oid]})
        helpful_cells[oid] = {
            r["resource_identity"]["address"] for r in judgment["helpful_resources"]
        }
    assert_(sum(map(len, required_units.values())) == 33, "Gold unit-judgment count")
    required_resources = set().union(*(set(v) for v in required_cells.values()))
    assert_(
        len(units) == 22 and len(required_resources) == 18, "Gold unit/resource counts"
    )
    assert_(
        sum(map(len, required_cells.values())) == 28
        and sum(map(len, helpful_cells.values())) == 25,
        "Gold cells",
    )
    cell_statuses = {}
    for oid, judgment in obligation_map.items():
        required_addresses = {unit_resource[u] for u in required_units[oid]}
        helpful_addresses = {
            r["resource_identity"]["address"] for r in judgment["helpful_resources"]
        }
        assert_(not required_addresses & helpful_addresses, f"Gold cell overlap {oid}")
        assert_(
            judgment["default_resource_classification"] == "UNNECESSARY",
            f"Gold default classification {oid}",
        )
        for address in required_addresses | helpful_addresses:
            cell_statuses[(address, oid)] = (
                "REQUIRED" if address in required_addresses else "HELPFUL_ONLY"
            )
    expected_cells = {(path, oid) for path in resources for oid in OBLIGATIONS}
    assert_(len(expected_cells) == 5310, "Gold expected cell identities")
    assert_(set(cell_statuses) <= expected_cells, "Gold unexpected special cells")
    assert_(
        len(expected_cells - set(cell_statuses)) == 5257,
        "Gold deterministic UNNECESSARY defaults",
    )
    assert_(
        judgments["task_interpretation_gaps"]["items"] == [], "Task interpretation gaps"
    )
    assert_(
        all(
            u["inferability"] == "INFERABLE_AT_START"
            for j in judgments["judgments"]
            for u in j["required_units"]
        ),
        "Gold inferability",
    )

    combinations = []
    alternatives = {
        oid: j["acceptable_witness_alternatives"] for oid, j in obligation_map.items()
    }
    for selections in itertools.product(*(alternatives[o] for o in OBLIGATIONS)):
        units_in = sorted({u for a in selections for u in a["all"]})
        resources_in = sorted({unit_resource[u] for u in units_in})
        combinations.append(
            {
                "alternative_ids": [a["identity"] for a in selections],
                "information_units": units_in,
                "resources": resources_in,
            }
        )
    assert_(
        len(combinations) == 4
        and all(
            len(c["information_units"]) == 20 and len(c["resources"]) == 16
            for c in combinations
        ),
        "Sufficient witness combinations",
    )

    global_lane = retrieval["global_lane"]
    global_ranks = {m["resource"]["address"]: m["rank"] for m in global_lane["matches"]}
    assert_(
        len(global_ranks) == len(global_lane["matches"]) <= 531
        and global_lane["maximum_results"] == 531,
        "Global lane result integrity",
    )
    retrieval_lanes = {
        lane["obligation_identity"]: lane for lane in retrieval["obligation_lanes"]
    }
    route_lanes = {lane["obligation_identity"]: lane for lane in routing["lanes"]}
    assert_(
        set(retrieval_lanes) == set(route_lanes) == set(OBLIGATIONS),
        "Native/routed lane identities",
    )
    assert_(
        routing["global_lane_unchanged"] is True
        and routing["global_lane"] == global_lane,
        "Global lane preservation",
    )
    preferences = {p["obligation"]: p for p in treatment["obligation_queries"]}
    assert_(set(preferences) == set(OBLIGATIONS), "Preference coverage")
    query_ids = {q["identity"] for q in treatment["obligation_queries"]}
    assert_(
        len(query_ids) == 10
        and {x["lane_identity"] for x in retrieval["obligation_lanes"]} == query_ids,
        "Query/lane identity join",
    )
    assert_(
        {x["query_identity"] for x in routing["lanes"]} == query_ids,
        "Query/preference routed join",
    )
    correspondence = []
    for oid in OBLIGATIONS:
        native = retrieval_lanes[oid]["matches"]
        routed = route_lanes[oid]["candidates"]
        native_map = {m["resource"]["address"]: m for m in native}
        routed_map = {m["resource"]["address"]: m for m in routed}
        assert_(
            len(native_map) == len(native) == len(routed_map) == len(routed),
            f"Candidate duplicate {oid}",
        )
        assert_(
            native_map.keys() == routed_map.keys(), f"Routed candidate survival {oid}"
        )
        assert_(
            all(
                routed_map[a]["native_rank"] == native_map[a]["rank"]
                and routed_map[a]["score"] == native_map[a]["score"]
                for a in native_map
            ),
            f"Routed native correspondence {oid}",
        )
        assert_(
            sorted(m["routed_position"] for m in routed)
            == list(range(1, len(routed) + 1)),
            f"Routed positions {oid}",
        )
        assert_(
            all(r["tier"] in {"preferred-role-supported", "escape"} for r in routed),
            f"Routed tier {oid}",
        )
        correspondence.append(
            {
                "obligation": oid,
                "native_candidates": len(native),
                "routed_candidates": len(routed),
                "all_native_candidates_survive": True,
            }
        )
    assert_(
        sum(map(lambda x: x["native_candidates"], correspondence))
        == sum(len(lane["matches"]) for lane in retrieval["obligation_lanes"]),
        "Own lane resource count",
    )
    assert_(
        sum(map(lambda x: x["routed_candidates"], correspondence))
        == sum(len(lane["candidates"]) for lane in routing["lanes"]),
        "Routed candidate count",
    )

    def alt_depth(oid: str, rank_map: dict[str, int]) -> tuple[int | None, str | None]:
        candidates = []
        for alt in alternatives[oid]:
            paths = {unit_resource[u] for u in alt["all"]}
            ranks = [rank_map[p] for p in paths if p in rank_map]
            if len(ranks) == len(paths):
                candidates.append((max(ranks), alt["identity"]))
        return min(candidates) if candidates else (None, None)

    global_occurrences = []
    global_obligations = []
    for oid in OBLIGATIONS:
        lane_best, alt_id = alt_depth(oid, global_ranks)
        for u in required_units[oid]:
            path = unit_resource[u]
            global_occurrences.append(
                {
                    "obligation": oid,
                    "unit": u,
                    "resource": path,
                    "native_rank": global_ranks.get(path),
                    "reached": path in global_ranks,
                }
            )
        global_obligations.append(
            {
                "obligation": oid,
                "best_completion_depth": lane_best,
                "alternative": alt_id,
            }
        )
    global_task_depth = max(
        r["best_completion_depth"]
        for r in global_obligations
        if r["best_completion_depth"] is not None
    )
    global_all_required_resource_depth = (
        max(global_ranks[p] for p in required_resources)
        if required_resources <= global_ranks.keys()
        else None
    )
    global_combo_depths = [
        {
            "alternatives": c["alternative_ids"],
            "depth": max(global_ranks[p] for p in c["resources"])
            if set(c["resources"]) <= global_ranks.keys()
            else None,
        }
        for c in combinations
    ]

    own_ranks = {
        o: {m["resource"]["address"]: m["rank"] for m in retrieval_lanes[o]["matches"]}
        for o in OBLIGATIONS
    }
    routed_positions = {
        o: {
            m["resource"]["address"]: m["routed_position"]
            for m in route_lanes[o]["candidates"]
        }
        for o in OBLIGATIONS
    }
    routed_tiers = {
        o: {m["resource"]["address"]: m["tier"] for m in route_lanes[o]["candidates"]}
        for o in OBLIGATIONS
    }
    own_results = []
    route_results = []
    for oid in OBLIGATIONS:
        d, a = alt_depth(oid, own_ranks[oid])
        own_results.append(
            {"obligation": oid, "best_completion_depth": d, "alternative": a}
        )
        d2, a2 = alt_depth(oid, routed_positions[oid])
        route_results.append(
            {"obligation": oid, "best_completion_position": d2, "alternative": a2}
        )
    own_max = max(
        x["best_completion_depth"]
        for x in own_results
        if x["best_completion_depth"] is not None
    )
    route_max = max(
        x["best_completion_position"]
        for x in route_results
        if x["best_completion_position"] is not None
    )
    route_vs_native = []
    for n, r in zip(own_results, route_results, strict=True):
        a, b = n["best_completion_depth"], r["best_completion_position"]
        status = (
            "unresolved"
            if a is None or b is None
            else "improved"
            if b < a
            else "worsened"
            if b > a
            else "unchanged"
        )
        route_vs_native.append(
            {
                "obligation": n["obligation"],
                "native_depth": a,
                "routed_position": b,
                "change": status,
            }
        )

    def prefix_surface(rank_maps: dict[str, dict[str, int]], depth_key: str) -> dict:
        per_ob = []
        all_occurrences = []
        for oid in OBLIGATIONS:
            depth = next(
                x[depth_key]
                for x in (
                    own_results
                    if depth_key == "best_completion_depth"
                    else route_results
                )
                if x["obligation"] == oid
            )
            rank_map = rank_maps[oid]
            selected = {
                p for p, r in rank_map.items() if depth is not None and r <= depth
            }
            cells = []
            for p in sorted(selected):
                category = (
                    "REQUIRED"
                    if p in required_cells[oid]
                    else "HELPFUL_ONLY"
                    if p in helpful_cells[oid]
                    else "UNNECESSARY"
                )
                cells.append({"resource": p, "classification": category})
                all_occurrences.append((oid, p))
            per_ob.append(
                {
                    "obligation": oid,
                    "completion_depth": depth,
                    "prefix_size": len(selected),
                    "resources": cells,
                }
            )
        return {
            "per_obligation": per_ob,
            "summed_prefix_occurrences": len(all_occurrences),
            "unique_resource_union": len({p for _, p in all_occurrences}),
            "unique_resources": sorted({p for _, p in all_occurrences}),
            "required_cells": sum(
                1 for o, p in all_occurrences if p in required_cells[o]
            ),
            "helpful_only_cells": sum(
                1 for o, p in all_occurrences if p in helpful_cells[o]
            ),
            "unnecessary_cells": sum(
                1
                for o, p in all_occurrences
                if p not in required_cells[o] and p not in helpful_cells[o]
            ),
            "unresolved_cells": 0,
        }

    native_prefix = prefix_surface(own_ranks, "best_completion_depth")
    routed_prefix = prefix_surface(routed_positions, "best_completion_position")

    request_results = {r["request_identity"]: r for r in grounding["requests"]}
    req_treatment = {r["identity"]: r for r in treatment["grounding_requests"]}
    assert_(set(request_results) == set(req_treatment), "Request join")
    assert_(
        Counter(r["disposition"] for r in grounding["requests"])
        == {"unsupported": 8, "resolved": 1},
        "Observed grounding counts",
    )
    archive_text = {r["address"]: r["content"] for r in packet["resources"]}
    resource_id_by_path = {
        r["address"]: r["content_identity"] for r in packet["resources"]
    }
    module_universe = frozen["module_universe"]
    mirror_analysis = frozen["mirrored_paths"]
    request_owner = {}
    grounding_diagnostics = []
    for request_id, result in request_results.items():
        frozen_request = req_treatment[request_id]
        locator = frozen_request["locator"]
        locator_kind = frozen_request["locator_kind"]
        if locator_kind == "PYTHON_DECLARATION":
            module = locator["module"]
            path = "src/" + module.replace(".", "/") + ".py"
            assert_(path in archive_text, f"Declaration resource absent {request_id}")
            exact_modules = [
                m for m in module_universe.interpretations if m.dotted_name == module
            ]
            assert_(
                len(exact_modules) == 1
                and exact_modules[0].resource.address.value == path,
                f"Universe module missing/ambiguous {request_id}",
            )
            module_names = [m.dotted_name for m in module_universe.interpretations]
            assert_(module in module_names, f"Frozen universe omits {module}")
            tree = ast.parse(archive_text[path], filename=path)
            matches = [
                n
                for n in tree.body
                if isinstance(n, ast.ClassDef | ast.FunctionDef | ast.AsyncFunctionDef)
                and n.name == locator["name"]
            ]
            assert_(len(matches) == 1, f"Exact direct declaration count {request_id}")
            node = matches[0]
            decorators = [ast.unparse(d) for d in node.decorator_list]
            assert_(
                isinstance(node, ast.ClassDef) and node.decorator_list,
                f"Expected decorated direct class {request_id}",
            )
            request_owner[request_id] = path
            reason = result["reason"]
            assert_(
                result["disposition"] == "unsupported"
                and reason
                == "Relevant syntax cannot establish the requested direct declaration.",
                f"Unexpected unsupported reason {request_id}",
            )
            assert_(
                result["resolver"] == "python-direct-module-declaration-lookup",
                f"Resolver mismatch {request_id}",
            )
            assert_(
                result["native_evidence"]
                and result["native_evidence"][0]["type"]
                == "PythonModuleDeclarationLookup",
                f"No native lookup evidence {request_id}",
            )
            gold_status = [
                {
                    "obligation": j["identity"],
                    "classification": "REQUIRED"
                    if any(
                        unit_resource[u] == path for u in required_units[j["identity"]]
                    )
                    else "HELPFUL_ONLY"
                    if path in helpful_cells[j["identity"]]
                    else "UNNECESSARY",
                }
                for j in judgments["judgments"]
            ]
            grounding_diagnostics.append(
                {
                    "request_identity": request_id,
                    "anchor_identity": frozen_request["anchor"],
                    "locator_kind": locator_kind,
                    "locator": locator,
                    "expected_declaration": locator["name"],
                    "exact_reason": reason,
                    "native_resolver": result["resolver"],
                    "native_lookup_evidence": result["native_evidence"],
                    "inferred_native_lookup_outcome_from_exact_branch": "NOT_DECLARATION",
                    "module_universe_identity": result["module_universe_identity"],
                    "module_universe_contains_exact_module": True,
                    "declaration_exists_in_snapshot": True,
                    "resource": path,
                    "resource_content_identity": resource_id_by_path[path],
                    "direct_module_body_declaration": True,
                    "declaration_kind": type(node).__name__,
                    "decorators": decorators,
                    "declaration_line": node.lineno,
                    "declaration_ri_representation": "PythonClassDeclarationKnowledge is produced for every direct module-body ClassDef, regardless of decorators; exact lookup computes class analysis but its binding scan rejects any decorated class before using the class fact.",
                    "primary_failure_class": "DECLARATION_KIND_MISMATCH",
                    "contributing_failure_classes": [
                        "NATIVE_RI_CAPABILITY_GAP: existing class RI records source ClassDef identity but the exact resolver does not project decorated ClassDef knowledge to an accepted direct binding."
                    ],
                    "gold_relevance_by_obligation": gold_status,
                    "in_sufficient_union": any(
                        path in c["resources"] for c in combinations
                    ),
                }
            )
        else:
            path = locator["address"]
            request_owner[request_id] = path
            grounding_diagnostics.append(
                {
                    "request_identity": request_id,
                    "anchor_identity": frozen_request["anchor"],
                    "locator_kind": locator_kind,
                    "locator": locator,
                    "exact_reason": result["reason"],
                    "native_resolver": result["resolver"],
                    "disposition": result["disposition"],
                    "resource": path,
                    "in_sufficient_union": path in required_resources,
                    "gold_relevance": "HELPFUL_ONLY"
                    if any(path in helpful_cells[o] for o in OBLIGATIONS)
                    else "UNNECESSARY",
                }
            )
    assert_(
        len(grounding_diagnostics) == 9
        and sum(
            d.get("disposition", "unsupported") == "unsupported"
            for d in grounding_diagnostics
        )
        == 8,
        "Grounding diagnostics",
    )

    recipe_specs = {r["identity"]: r for r in treatment["generation_recipes"]}
    observed_recipes = {r["recipe_identity"]: r for r in generation["recipes"]}
    assert_(set(recipe_specs) == set(observed_recipes), "Recipe identity join")
    observed_members = sum(len(r["members"]) for r in generation["recipes"])
    assert_(
        observed_members == 14 and generation["summary"]["recipes_attempted"] == 9,
        "Member attempt count",
    )
    actual_hypotheses = [
        r for r in generation["recipes"] if r["hypothesis_identity"] is not None
    ]
    assert_(
        generation["summary"]["generated_hypotheses"] == len(actual_hypotheses) == 0,
        "Actual hypotheses",
    )
    assert_(
        generation["hypotheses_unresolved"] is True
        and all(not r["hypothesis_members"] for r in generation["recipes"]),
        "No captured generated members",
    )
    assert_(
        generation["summary"]["member_occurrences"]
        == generation["summary"]["unique_resources"]
        == 0,
        "Actual generation surface",
    )
    assert_(
        generation["summary"]["projection_operators"]
        == {"OWNER_RESOURCE": 12, "MIRRORED_RESOURCE": 2},
        "Actual operators",
    )
    assert_(
        generation["summary"]["projection_dispositions"] == {"unsupported-source": 14},
        "Actual member outcomes",
    )
    mirrors = {
        m.source.address.value: m.test.address.value
        for m in mirror_analysis.correspondences
    }
    target_by_recipe = {}
    recipe_comparison = []
    for recipe_id, spec in recipe_specs.items():
        observed = observed_recipes[recipe_id]
        observed_member_map = {m["member_identity"]: m for m in observed["members"]}
        assert_(
            set(observed_member_map) == {m["identity"] for m in spec["members"]},
            f"Member identity join {recipe_id}",
        )
        for member_spec in spec["members"]:
            observed_member = observed_member_map[member_spec["identity"]]
            assert_(
                observed_member["grounding_request_identity"]
                == member_spec["grounding_request"],
                f"Member/request binding {recipe_id}",
            )
            assert_(
                observed_member["projection"] == member_spec["projection"],
                f"Member/operator binding {recipe_id}",
            )
        targets = []
        for member in spec["members"]:
            source = request_owner[member["grounding_request"]]
            target = (
                source
                if member["projection"] == "OWNER_RESOURCE"
                else mirrors.get(source)
            )
            targets.append(target)
        materialized = [t for t in targets if t is not None]
        assert_(
            len(materialized) == len(set(materialized)),
            f"Counterfactual duplicate target in {recipe_id}",
        )
        # A recipe yields a hypothesis only when every member projection has a target.
        target_by_recipe[recipe_id] = (
            materialized if all(t is not None for t in targets) else []
        )
        oid = spec["obligation"]
        alt_resources = [
            {unit_resource[u] for u in a["all"]} for a in alternatives[oid]
        ]
        got = set(target_by_recipe[recipe_id])
        exact = any(got == expected for expected in alt_resources)
        subset = any(got < expected for expected in alt_resources)
        superset = any(expected <= got for expected in alt_resources)
        category = (
            "EXACT_STRUCTURAL_MATCH"
            if exact
            else "PARTIAL_MATCH"
            if got and subset
            else "RESOURCE_MATCH_WRONG_STRUCTURE"
            if got and superset
            else "NO_GOLD_MATCH"
        )
        recipe_comparison.append(
            {
                "obligation": oid,
                "recipe": recipe_id,
                "member_shape": [m["identity"] for m in spec["members"]],
                "projections": [m["projection"] for m in spec["members"]],
                "projected_member_targets": targets,
                "counterfactual_targets": sorted(got),
                "gold_alternative_resource_sets": [sorted(s) for s in alt_resources],
                "overlap_resources": sorted(got & set().union(*alt_resources)),
                "missing_complementary_resources": sorted(
                    set().union(*alt_resources) - got
                ),
                "unnecessary_targets": sorted(got - set().union(*alt_resources)),
                "classification": category,
            }
        )
    cf_by_ob = {o: set() for o in OBLIGATIONS}
    cf_recipe_counts = Counter()
    for recipe_id, spec in recipe_specs.items():
        oid = spec["obligation"]
        cf_by_ob[oid].update(target_by_recipe[recipe_id])
        cf_recipe_counts[oid] += 1
    actual_by_ob = {o: set() for o in OBLIGATIONS}
    assert_(not any(actual_by_ob.values()), "Actual candidates should be empty")
    cf_cells = sum(len(cf_by_ob[o] & set(required_cells[o])) for o in OBLIGATIONS)
    cf_required_units = sum(
        1
        for o in OBLIGATIONS
        for u in required_units[o]
        if unit_resource[u] in cf_by_ob[o]
    )
    cf_unique_req_resources = set().union(
        *(cf_by_ob[o] & set(required_cells[o]) for o in OBLIGATIONS)
    )
    cf_complete_obligations = [
        o
        for o in OBLIGATIONS
        if any(
            {unit_resource[u] for u in a["all"]} <= cf_by_ob[o] for a in alternatives[o]
        )
    ]
    cf_complete_structures = []
    for oid in OBLIGATIONS:
        found = False
        for spec in (s for s in recipe_specs.values() if s["obligation"] == oid):
            targets = set(target_by_recipe[spec["identity"]])
            if any(
                targets == {unit_resource[u] for u in a["all"]}
                for a in alternatives[oid]
            ):
                found = True
        if found:
            cf_complete_structures.append(oid)
    assert_(
        cf_cells == 12
        and cf_required_units == 15
        and len(cf_unique_req_resources) == 7,
        "Counterfactual coverage totals",
    )

    obligation_diagnostics = []
    miss_cells = []
    for oid in OBLIGATIONS:
        specs = [r for r in recipe_specs.values() if r["obligation"] == oid]
        alt_sets = [{unit_resource[u] for u in a["all"]} for a in alternatives[oid]]
        addressable = any(
            set(target_by_recipe[s["identity"]]) == alt
            for s in specs
            for alt in alt_sets
        )
        any_partial = any(
            set(target_by_recipe[s["identity"]]) & alt
            for s in specs
            for alt in alt_sets
        )
        status = (
            "TREATMENT_ADDRESSABLE"
            if addressable
            else "PARTIALLY_ADDRESSABLE"
            if any_partial
            else "NOT_ADDRESSABLE"
        )
        member_details = []
        for spec in specs:
            for member in spec["members"]:
                req = request_results[member["grounding_request"]]
                source = request_owner[member["grounding_request"]]
                projected_target = (
                    source
                    if member["projection"] == "OWNER_RESOURCE"
                    else mirrors.get(source)
                )
                member_details.append(
                    {
                        "recipe": spec["identity"],
                        "member": member["identity"],
                        "request": member["grounding_request"],
                        "projection": member["projection"],
                        "source_grounding_disposition": req["disposition"],
                        "actual_generation_disposition": next(
                            m["disposition"]
                            for r in observed_recipes.values()
                            if r["recipe_identity"] == spec["identity"]
                            for m in r["members"]
                            if m["member_identity"] == member["identity"]
                        ),
                        "counterfactual_target": projected_target,
                        "counterfactual_recipe_materializes": bool(
                            target_by_recipe[spec["identity"]]
                        ),
                    }
                )
        obligation_diagnostics.append(
            {
                "obligation": oid,
                "grounding_requests": sorted(
                    {m["grounding_request"] for s in specs for m in s["members"]}
                ),
                "has_recipe": bool(specs),
                "recipe_count": len(specs),
                "recipes": member_details,
                "required_resource_cells": sorted(required_cells[oid]),
                "acceptable_alternatives": [
                    {
                        "identity": a["identity"],
                        "resources": sorted({unit_resource[u] for u in a["all"]}),
                        "unit_shape": a["all"],
                    }
                    for a in alternatives[oid]
                ],
                "counterfactual_targets": sorted(cf_by_ob[oid]),
                "treatment_addressability_posthoc": status,
            }
        )
        for path in required_cells[oid]:
            if path in cf_by_ob[oid]:
                primary, contributing = "GROUNDING_UNSUPPORTED", []
            elif not specs:
                primary, contributing = "NO_RECIPE", ["OPERATOR_CAPABILITY_GAP"]
            else:
                primary, contributing = "OPERATOR_CAPABILITY_GAP", []
                if any(
                    request_results[m["grounding_request"]]["disposition"]
                    == "unsupported"
                    for s in specs
                    for m in s["members"]
                ):
                    contributing.append("GROUNDING_UNSUPPORTED")
            miss_cells.append(
                {
                    "obligation": oid,
                    "resource": path,
                    "classification": "REQUIRED",
                    "primary_miss_reason": primary,
                    "contributing_reasons": contributing,
                }
            )
    miss_counts = Counter(m["primary_miss_reason"] for m in miss_cells)
    assert_(
        len(miss_cells) == 28 and sum(miss_counts.values()) == 28,
        "Miss taxonomy totals",
    )

    actual_resource_cells = sum(
        len(actual_by_ob[o] & set(required_cells[o])) for o in OBLIGATIONS
    )
    actual_unit_judgments = sum(
        1
        for o in OBLIGATIONS
        for u in required_units[o]
        if unit_resource[u] in actual_by_ob[o]
    )
    actual_unique_required = set().union(
        *(actual_by_ob[o] & set(required_cells[o]) for o in OBLIGATIONS)
    )
    actual_complete_structures = []
    for oid in OBLIGATIONS:
        if any(
            {unit_resource[u] for u in alt["all"]} <= actual_by_ob[oid]
            for alt in alternatives[oid]
        ):
            actual_complete_structures.append(oid)

    member_count = 14
    funnel = {
        "task_obligations": 10,
        "shared_anchors": 10,
        "grounding_requests": 9,
        "grounding_dispositions": dict(
            Counter(r["disposition"] for r in grounding["requests"])
        ),
        "generation_recipe_specifications": 9,
        "recipe_member_attempts": 14,
        "generation_attempt_dispositions": generation["summary"][
            "generation_dispositions"
        ],
        "generated_hypotheses": len(actual_hypotheses),
        "generated_member_occurrences": member_count if actual_hypotheses else 0,
        "generated_unique_resources": len(set().union(*actual_by_ob.values())),
        "required_resource_cell_coverage": actual_resource_cells,
    }

    analysis = {
        "schema": "case-0006-stage-d-joined-analysis-v1",
        "case_identity": "case_0006",
        "task_identity": treatment["task_identity"],
        "repository_id": REPOSITORY,
        "repository_snapshot_id": SNAPSHOT,
        "corpus_frame_identity": FRAME,
        "chain": chain,
        "artifact_sha256": artifact_hashes,
        "execution_provenance": {
            "execution_kind": "RECOVERY",
            "recovery_id": RECOVERY_ID,
            "prior_failed_execution_count": 1,
            "treatment_unchanged": True,
            "attempt_1_semantic_outputs_retained_or_used": False,
            "recovery_preauthorized": True,
            "recovery_outputs_durably_captured": True,
            "recovery_capture_limit": "Harness member-order correspondence failed after treatment before native outputs persisted; recovery used frozen member identity/key correspondence. No effectiveness effect is inferred.",
        },
        "joins": {
            "resources_expected": 531,
            "resources_joined": len(packet_ids & pre_ids & gold_ids),
            "resource_duplicates_missing_unexpected": {
                "duplicates": 0,
                "missing": 0,
                "unexpected": 0,
            },
            "obligations_expected": 10,
            "obligations_joined": len(
                set(OBLIGATIONS)
                & set(retrieval_lanes)
                & set(route_lanes)
                & set(obligation_map)
            ),
            "lexical_lanes_expected": 10,
            "lexical_lanes_joined": len(retrieval_lanes),
            "role_preferences_expected": 10,
            "role_preferences_joined": len(preferences),
            "grounding_requests_expected": 9,
            "grounding_requests_joined": len(set(req_treatment) & set(request_results)),
            "recipe_specs_expected": 9,
            "recipe_specs_joined": len(set(recipe_specs) & set(observed_recipes)),
            "judgment_cells_expected": 5310,
            "judgment_cells_joined": 5310,
            "routed_native_correspondence": correspondence,
            "global_lane_unchanged": True,
        },
        "gold": {
            "applicable_obligations": 10,
            "distinct_required_information_units": 22,
            "required_unit_judgments": 33,
            "unique_required_resources": 18,
            "required_resource_obligation_cells": 28,
            "helpful_resource_obligation_cells": 25,
            "unnecessary_resource_obligation_cells": 5257,
            "unresolved": 0,
            "inherent_discovery": 0,
            "task_interpretation_gaps": 0,
            "acceptable_combinations": combinations,
            "minimum_sufficient_resource_union": 16,
            "maximum_sufficient_resource_union": 16,
        },
        "global_native_bm25": {
            "required_unit_resource_occurrences": global_occurrences,
            "required_unit_resource_reach": sum(
                1 for x in global_occurrences if x["reached"]
            ),
            "required_unit_resource_occurrence_count": len(global_occurrences),
            "obligations": global_obligations,
            "task_complete_obligation_depth": global_task_depth,
            "complete_18_resource_witness_universe_depth": global_all_required_resource_depth,
            "sufficient_combination_depths": global_combo_depths,
            "best_sufficient_combination_depth": min(
                x["depth"] for x in global_combo_depths if x["depth"] is not None
            ),
        },
        "own_obligation_native": {
            "required_occurrences": [
                {
                    "obligation": o,
                    "unit": u,
                    "resource": unit_resource[u],
                    "native_rank": own_ranks[o].get(unit_resource[u]),
                    "reached": unit_resource[u] in own_ranks[o],
                }
                for o in OBLIGATIONS
                for u in required_units[o]
            ],
            "obligations": own_results,
            "obligation_wise_maximum_completion_depth": own_max,
        },
        "role_routed": {
            "required_occurrences": [
                {
                    "obligation": o,
                    "unit": u,
                    "resource": unit_resource[u],
                    "native_rank": own_ranks[o].get(unit_resource[u]),
                    "routed_position": routed_positions[o].get(unit_resource[u]),
                    "tier": routed_tiers[o].get(unit_resource[u]),
                }
                for o in OBLIGATIONS
                for u in required_units[o]
            ],
            "obligations": route_results,
            "obligation_wise_maximum_completion_position": route_max,
            "comparison_to_own_native": route_vs_native,
            "improved": sum(x["change"] == "improved" for x in route_vs_native),
            "unchanged": sum(x["change"] == "unchanged" for x in route_vs_native),
            "worsened": sum(x["change"] == "worsened" for x in route_vs_native),
            "unresolved": sum(x["change"] == "unresolved" for x in route_vs_native),
            "empty_validation_role_preference": preferences["validation"][
                "preferred_roles"
            ]
            == [],
        },
        "completion_prefixes": {
            "own_native": native_prefix,
            "routed": routed_prefix,
            "sufficient_bound": 16,
            "native_unique_over_bound": native_prefix["unique_resource_union"] / 16,
            "routed_unique_over_bound": routed_prefix["unique_resource_union"] / 16,
            "native_excess_over_bound": native_prefix["unique_resource_union"] - 16,
            "routed_excess_over_bound": routed_prefix["unique_resource_union"] - 16,
        },
        "actual_generation": {
            "generation_unranked": True,
            "generated_hypotheses": 0,
            "generated_member_occurrences": 0,
            "unique_generated_targets": 0,
            "generated_obligation_resource_occurrences": 0,
            "required_resource_cell_coverage": actual_resource_cells,
            "required_resource_cell_denominator": 28,
            "required_unit_judgment_coverage": actual_unit_judgments,
            "required_unit_judgment_denominator": 33,
            "unique_required_resources_covered": len(actual_unique_required),
            "unique_required_resource_denominator": 18,
            "complete_alternative_resource_coverage": {o: False for o in OBLIGATIONS},
            "complete_witness_structures": actual_complete_structures,
            "complete_witness_structure_obligations": 0,
            "applicable_obligation_denominator": 10,
            "generated_required_precision": None,
            "precision_status": "undefined (0 generated candidates; denominator is zero)",
        },
        "grounding_diagnosis": {
            "requests": grounding_diagnostics,
            "primary_class_counts": dict(
                Counter(
                    x["primary_failure_class"]
                    for x in grounding_diagnostics
                    if "primary_failure_class" in x
                )
            ),
            "exact_production_path": {
                "grounder": "src/devtools/context/localization/grounding/resolve.py::_ground_declaration lines 159-224; calls lookup_python_module_declaration, maps NOT_DECLARATION to unsupported, then gives generic reason at lines 202-215.",
                "native_lookup": "src/devtools/context/python/modules/declarations.py::lookup_python_module_declaration lines 74-192; line 107-108 appends None for every decorated direct ClassDef before consulting class-analysis results; lines 179-181 returns NOT_DECLARATION.",
                "ri_representation": "src/devtools/context/python/classes/declarations.py::derive_python_class_method_declarations records each module.body ClassDef as PythonClassDeclarationKnowledge without excluding decorators. The lookup computes that class analysis but does not use its exact source class fact when decorators are present.",
            },
            "module_universe_identity": module_universe.identity,
            "module_universe_interpretations": len(module_universe.interpretations),
        },
        "treatment_addressability_posthoc": obligation_diagnostics,
        "counterfactual_diagnostic_not_observed_treatment_output": {
            "assumption": "Each of the eight exact frozen declaration lookups resolves to its observed direct ClassDef referent; every frozen recipe and owner/mirror operator stays unchanged; use only captured Stage A correspondence identities.",
            "generated_hypotheses": 9,
            "generated_member_occurrences": 14,
            "unique_generated_resources": len(set().union(*cf_by_ob.values())),
            "unique_generated_resources_by_obligation": {
                o: sorted(v) for o, v in cf_by_ob.items()
            },
            "required_resource_cell_coverage": cf_cells,
            "required_resource_cell_denominator": 28,
            "required_unit_judgment_coverage": cf_required_units,
            "required_unit_judgment_denominator": 33,
            "unique_required_resources_covered": len(cf_unique_req_resources),
            "unique_required_resource_denominator": 18,
            "obligations_with_complete_acceptable_resource_alternative": cf_complete_obligations,
            "complete_resource_alternative_count": len(cf_complete_obligations),
            "obligations_with_complete_witness_structure": cf_complete_structures,
            "complete_witness_structure_count": len(cf_complete_structures),
            "misses_remaining": [
                m for m in miss_cells if m["resource"] not in cf_by_ob[m["obligation"]]
            ],
            "recipe_structure_comparison": recipe_comparison,
        },
        "miss_classification": {
            "required_resource_cells": miss_cells,
            "primary_counts_no_double_count": dict(miss_counts),
            "grounding_unsupported_contributing_cells": sum(
                "GROUNDING_UNSUPPORTED" in m["contributing_reasons"] for m in miss_cells
            ),
        },
        "operator_capability": {
            "OWNER_REACHABLE": sorted(
                {
                    p
                    for spec in recipe_specs.values()
                    for m in spec["members"]
                    if m["projection"] == "OWNER_RESOURCE"
                    for p in target_by_recipe[spec["identity"]]
                    if p in required_resources
                }
            ),
            "MIRROR_REACHABLE": sorted(
                {
                    p
                    for spec in recipe_specs.values()
                    for m in spec["members"]
                    if m["projection"] == "MIRRORED_RESOURCE"
                    for p in target_by_recipe[spec["identity"]]
                    if p in required_resources
                }
            ),
            "REQUIRES_OTHER_TYPED_RELATION": [
                "Public package exports/facade-to-declaration relations for package-integration.",
                "Documentation ownership/authority navigation for documentation.",
                "Validation-contract documentation link or targeted documentation association; exact script grounding alone names the entry point, not its contract.",
                "Import/reference relation from grounding.view to grounding.contract for the separately REQUIRED grounding account.",
            ],
            "NONSTRUCTURAL_OR_POLICY_DISCOVERY": [
                "Full task-frame/provenance information in src/devtools/context/localization/task.py has no named anchor locator or frozen recipe member; caller/task-frame association is needed."
            ],
        },
        "primary_failure_interpretation": {
            "task_interpretation": "not primary: all 10 frozen obligations are applicable and 16-resource alternatives are explicit.",
            "acquisition": "not primary for gold scope: BM25 surfaces are joined and scored below; generation has an independent structural route.",
            "role_routing": "not primary: routed lanes preserve all native candidates and the global lane; positions change attention only.",
            "grounding": "primary observed bottleneck for 13/28 required resource-obligation cells; all eight named declaration sources exist but conservative decorated-binding semantics reject them.",
            "generation_operator_and_recipe_coverage": "independent secondary bottleneck for 7/28 required cells with recipes and 8/28 cells in obligations with no recipe. Fixing grounding alone reaches 13/28 cells and only 2/10 complete obligation alternatives.",
            "witness_structure": "for five partially addressed obligations recipes omit complementary gold resources; no observed generated structure exists, and the grounding-fixed counterfactual matches only two alternatives.",
        },
        "minimum_next_architectural_change_justified": "A narrowly specified deterministic bridge from existing direct class-syntax RI to grounding for explicitly decorated module-body class declarations, preserving the current abstention rule for unsupported/ambiguous binding semantics and never asserting runtime/public binding from a ClassDef alone. First define what evidence licenses the referent; then a new frozen prospective case should measure it together with explicitly authored owner/mirror recipes and the required package/documentation relations. This case does not justify automatic decorator execution or broad semantic linking.",
        "not_justified_by_this_case": [
            "BM25/embedding/LLM entity linking",
            "automatic candidate ranking or resolution policy",
            "broad graph expansion",
            "claims of general superiority/inferiority",
            "treating Stage A frozen measurements as threshold success/failure",
            "implementing a new relation family without a separately bounded contract",
        ],
        "limitations": [
            "One prospective case establishes this frozen configuration's outcomes, not general architecture performance.",
            "The post-hoc counterfactual assumes exact declaration referents and existing captured mirror facts; it is not executed treatment output.",
            "Counterfactual complete witness structure means exact coverage of all distinct gold resource members by one recipe's complementary target members; it does not prove semantic adequacy beyond frozen gold.",
            "Recovery capture fixed a harness correspondence bug after Attempt 1 failed before native output persistence. It did not change treatment or establish any effectiveness effect.",
        ],
        "execution_firewall": {
            "retrieval_rerun": False,
            "routing_rerun": False,
            "grounding_rerun": False,
            "generation_rerun": False,
            "treatment_changed": False,
            "judgments_changed": False,
            "production_source_changed": False,
            "confirmation_accessed": False,
            "effectiveness_threshold_inferred": False,
        },
    }
    analysis["primary_failure_funnel"] = funnel
    analysis["joins"]["shared_anchors_expected"] = 10
    analysis["joins"]["shared_anchors_joined"] = len(treatment["anchors"])
    analysis["joins"]["routed_candidates_total"] = sum(
        row["routed_candidates"] for row in correspondence
    )
    analysis["joins"]["judgment_identity_coverage"] = {
        "expected_identities": len(expected_cells),
        "observed_identities": len(expected_cells),
        "duplicate_expected": 0,
        "duplicate_observed": 0,
        "missing": 0,
        "unexpected": 0,
    }
    cf = analysis["counterfactual_diagnostic_not_observed_treatment_output"]
    analysis["global_native_bm25"]["global_candidate_count"] = len(global_ranks)
    cf["generated_hypotheses"] = sum(bool(target_by_recipe[s]) for s in recipe_specs)
    cf["generated_member_occurrences"] = sum(
        len(target_by_recipe[s]) for s in recipe_specs
    )
    cf["unresolved_mirror_member_targets"] = sum(
        1
        for spec in recipe_specs.values()
        for member in spec["members"]
        if member["projection"] == "MIRRORED_RESOURCE"
        and mirrors.get(request_owner[member["grounding_request"]]) is None
    )
    analysis["primary_failure_interpretation"] = {
        "task_interpretation": "not primary: all ten obligations are applicable and sufficient alternatives are explicit.",
        "acquisition": "global and own-lane lexical surfaces reach every REQUIRED witness resource; acquisition is not the observed generation bottleneck.",
        "role_routing": "all native candidates survive; routing changes positions but does not explain generation's empty surface.",
        "grounding": "largest single primary miss class: 12/28 required resource-obligation cells are owner/mirror targets blocked by unsupported exact declaration grounding.",
        "generation_operator_coverage": "8/28 cells remain unreachable by the frozen owner/mirror projections even if exact grounding is fixed.",
        "recipe_authoring": "8/28 cells belong to package, documentation, and validation obligations with no generation recipe; among recipe obligations, complementary gold resources are omitted.",
        "witness_structure": "only two of ten obligations have a complete counterfactual recipe structure matching a gold alternative; observed generation emitted no structures.",
    }
    return analysis


def render_markdown(a: dict) -> str:
    g, n, r, p, gen = (
        a["global_native_bm25"],
        a["own_obligation_native"],
        a["role_routed"],
        a["completion_prefixes"],
        a["actual_generation"],
    )
    cf = a["counterfactual_diagnostic_not_observed_treatment_output"]
    lines = [
        "# Case 0006 Stage D joined analysis",
        "",
        "## 1. Frozen experiment integrity",
        "",
        f"Verified chain: Stage A `{CHAIN['stage_a']}` → recovery protocol `{CHAIN['stage_b_recovery_protocol']}` → recovery capture `{CHAIN['stage_b_recovery_capture']}` → Stage B.5 `{CHAIN['stage_b5']}` → Stage C `{CHAIN['stage_c']}`.",
        f"All {len(a['artifact_sha256'])} listed/pinned artifacts match their frozen digests and committed blobs. Starting checkout was clean `main` at `{CHAIN['stage_c']}`.",
        f"Recovery provenance: execution kind RECOVERY, ID `{RECOVERY_ID}`, prior failed execution count 1. Attempt 1 failed in the experiment harness's complementary-member list-order correspondence after treatment and before persisting semantic outputs. The preauthorized recovery matched by frozen member identity/key; treatment remained byte-identical and recovery outputs were durably captured. No effectiveness impact is inferred.",
        "",
        "## 2. Primary frozen measurements",
        "",
        f"Identity joins: resources {a['joins']['resources_joined']}/531; obligations {a['joins']['obligations_joined']}/10; shared anchors {a['joins']['shared_anchors_joined']}/10; lexical lanes {a['joins']['lexical_lanes_joined']}/10; role preferences {a['joins']['role_preferences_joined']}/10; grounding requests {a['joins']['grounding_requests_joined']}/9; recipes {a['joins']['recipe_specs_joined']}/9; gold cells {a['joins']['judgment_cells_joined']:,}/5,310. Duplicate, missing and unexpected resource identities: 0. All {a['joins']['routed_candidates_total']:,} routed-lane candidates map to exact native candidates and survive routing; the global lane is unchanged.",
        "Gold: 22 distinct required units, 33 required unit judgments, 18 unique required resources, 28 REQUIRED cells, 25 HELPFUL_ONLY cells, and 5,257 UNNECESSARY cells. All ten obligations apply. There are four valid combinations of alternatives, each with 20 units in 16 resources (minimum and maximum sufficient union both 16). No unresolved gold, inherent discovery, or task-interpretation gap.",
        "",
        "## 3. Baseline lexical and routing comparison",
        "",
        f"Global native BM25 has {g['global_candidate_count']} positive-match candidates and reaches {g['required_unit_resource_reach']}/{g['required_unit_resource_occurrence_count']} REQUIRED unit/resource occurrences. Best acceptable completion depths by obligation: "
        + ", ".join(
            f"{x['obligation']} {x['best_completion_depth']}" for x in g["obligations"]
        )
        + f". Global task-complete obligation depth: **{g['task_complete_obligation_depth']}**. Full 18-resource witness-universe depth: {g['complete_18_resource_witness_universe_depth']}; best 16-resource gold combination depth: {g['best_sufficient_combination_depth']}.",
        f"Own-obligation native maximum of the ten independently best completion depths: **{n['obligation_wise_maximum_completion_depth']}**. Routed maximum of ten best completion positions: **{r['obligation_wise_maximum_completion_position']}**. Routing changed obligation completion positions: {r['improved']} improved, {r['unchanged']} unchanged, {r['worsened']} worsened; empty validation-role preference control: {r['empty_validation_role_preference']}.",
        f"Native prefixes: {p['own_native']['summed_prefix_occurrences']} summed occurrences, {p['own_native']['unique_resource_union']} unique resources ({p['native_unique_over_bound']:.2f}× the 16-resource sufficient bound; excess {p['native_excess_over_bound']}). Routed prefixes: {p['routed']['summed_prefix_occurrences']} summed occurrences, {p['routed']['unique_resource_union']} unique resources ({p['routed_unique_over_bound']:.2f}×; excess {p['routed_excess_over_bound']}). Prefix cell classes are retained per obligation in JSON.",
        "",
        "| Surface | Candidate surface type | Size | Required coverage | Complete-obligation coverage |",
        "| --- | --- | ---: | ---: | ---: |",
        f"| Global lexical | ranked native BM25 | 528 | {g['required_unit_resource_reach']}/{g['required_unit_resource_occurrence_count']} unit/resource occurrences | 10/10 at task-complete depth {g['task_complete_obligation_depth']} |",
        f"| Own native prefixes | ranked prefixes | {p['own_native']['unique_resource_union']} unique; {p['own_native']['summed_prefix_occurrences']} occurrences | {p['own_native']['required_cells']}/28 REQUIRED cells in prefixes | 10/10; max depth {n['obligation_wise_maximum_completion_depth']} |",
        f"| Routed prefixes | ranked prefixes | {p['routed']['unique_resource_union']} unique; {p['routed']['summed_prefix_occurrences']} occurrences | {p['routed']['required_cells']}/28 REQUIRED cells in prefixes | 10/10; max position {r['obligation_wise_maximum_completion_position']} |",
        f"| Actual generation | unranked set | 0 | {gen['required_resource_cell_coverage']}/28 | 0/10 |",
        "| Sufficient gold bound | semantic lower bound | 16 | 100% by definition | 10/10 |",
        "",
        "## 4. Actual generation result",
        "",
        "Observed recovery output: 9 recipes, 14 member attempts (12 OWNER_RESOURCE and 2 MIRRORED_RESOURCE); all 9 recipes and 14 members ended `unsupported-source`. Generated hypotheses 0, member occurrences 0, unique targets/resources 0, and generated obligation/resource occurrences 0. REQUIRED resource-cell coverage 0/28; REQUIRED unit-judgment coverage 0/33; unique REQUIRED resources 0/18; complete acceptable witness structures 0/10. Generated precision is **undefined** because there are zero generated candidates.",
        "",
        "## 5. Grounding failure diagnosis",
        "",
        "Eight exact Python declaration locators were supported locator forms, matched an exact module in the frozen 399-interpretation universe, and produced native `PythonModuleDeclarationLookup` evidence. All eight named classes exist once as direct module-body ClassDefs in the frozen snapshot. Each has a decorator (`@dataclass`); the frozen class RI emits `PythonClassDeclarationKnowledge` for direct ClassDefs, but `lookup_python_module_declaration` appends an unsupported binding marker for every decorated direct definition before consulting that class fact. The lookup returns NOT_DECLARATION, which `_ground_declaration` maps to UNSUPPORTED with the captured generic reason. Primary classification for all eight: **DECLARATION_KIND_MISMATCH**. This is not a missing module universe, locator spelling mismatch, absent class, or public-export path mismatch.",
        "| Request | Anchor → exact declaration | Frozen owner resource | Disposition | Captured reason | Gold relevance |",
        "| --- | --- | --- | --- | --- | --- |",
    ]
    for d in a["grounding_diagnosis"]["requests"]:
        loc = d["locator"]
        target = (
            f"{loc.get('module', '')}.{loc.get('name', '')}"
            if d["locator_kind"] == "PYTHON_DECLARATION"
            else loc["address"]
        )
        status = d.get("disposition", "unsupported")
        rel = ", ".join(
            f"{x['obligation']}={x['classification']}"
            for x in d.get("gold_relevance_by_obligation", [])
            if x["classification"] != "UNNECESSARY"
        )
        if not rel:
            rel = d.get("gold_relevance", "UNNECESSARY for all obligations")
        lines.append(
            f"| {d['request_identity']} | {d['anchor_identity']} → `{target}` | `{d['resource']}` | {status} | {d['exact_reason']} | {rel} |"
        )
    lines += [
        "",
        "All eight failed declaration-owning resources appear in at least one 16-resource sufficient union, and all are REQUIRED for at least one obligation (see the full per-obligation classification in JSON). The ninth request, `g-validation`, resolved its exact address `scripts/validate_development.py`; that file is HELPFUL_ONLY for the validation obligation, while the REQUIRED validation contract is documented in `docs/development/validation.md`.",
        "",
        "## 6. Gold miss classification",
        "",
        "Every actual required resource cell is missed. Primary causes partition the 28 cells without double-counting: "
        + ", ".join(
            f"{k} {v}"
            for k, v in sorted(
                a["miss_classification"]["primary_counts_no_double_count"].items()
            )
        )
        + f". Grounding also contributes to {a['miss_classification']['grounding_unsupported_contributing_cells']} operator-limited cells, so contributing reasons overlap and are not added to the primary total.",
        "Per-obligation: "
        + "; ".join(
            f"{x['obligation']} {x['treatment_addressability_posthoc']} ({len(x['required_resource_cells'])} required resource cells)"
            for x in a["treatment_addressability_posthoc"]
        ),
        "No recipe was authored for package-integration, documentation, or validation. The validation address was grounded, but no recipe promoted the exact required documentation contract. For tests, the frozen mirror recipes can reach test examples but omit the complementary production candidate-validation and readiness resources.",
        "",
        "## 7. Post-hoc counterfactual diagnostic — NOT OBSERVED TREATMENT OUTPUT",
        "",
        f"Assuming only that all eight exact frozen declaration requests resolve to their exact direct ClassDef referents, while retaining every recipe/operator and captured mirror fact, the frozen recipes would materialize {cf['generated_hypotheses']} hypotheses with {cf['generated_member_occurrences']} members and {cf['unique_generated_resources']} unique targets. {cf['unresolved_mirror_member_targets']} mirrored member has no captured target. Coverage is {cf['required_resource_cell_coverage']}/28 REQUIRED resource cells, {cf['required_unit_judgment_coverage']}/33 unit judgments, and {cf['unique_required_resources_covered']}/18 unique REQUIRED resources. It completes alternatives for {cf['complete_resource_alternative_count']}/10 obligations and complete structures for {cf['complete_witness_structure_count']}/10: {', '.join(cf['obligations_with_complete_witness_structure'])}. Remaining misses: {len(cf['misses_remaining'])}/28.",
        "Fixing grounding alone does not make generation competitive by coverage with lexical/routed prefixes: it reaches 42.9% of REQUIRED cells and 38.9% of unique required resources, with only two complete obligations; the own-native and routed completion prefixes reach all ten. Generated candidates remain unranked. Exact recipe-by-recipe overlaps and missing complementary resources are in the JSON.",
        "",
        "## 8. Architectural interpretation",
        "",
        "Observed primary bottleneck: conservative decorated-class direct-declaration grounding; under the explicit counterfactual 12 required resource-obligation cells become reachable. Independently, owner/mirror operator coverage leaves 8 cells unreachable even after resolving named declarations, and three no-recipe obligations account for 8 cells. Task interpretation is sufficient; role routing preserves all candidates and is not the generation bottleneck. The counterfactual recipe structures exactly match gold resource structures only for hypothesis-records and member-complementarity; five obligations are partial and three are not addressable.",
        "Gold also points to distinct typed relations: public facade/export-to-declaration links; exact imports/references between view and contract modules; documentation ownership/authority navigation; and a task-frame association for provenance. The required test gold combines production source contracts with tests, beyond the mirror-only test recipes. Package, documentation and validation require another acquisition/association route; OWNER/MIRRORED alone cannot express their gold targets.",
        "Minimum justified next change: specify a narrow deterministic bridge from existing direct class syntax RI to grounding for explicitly decorated module-body class declarations, with explicit treatment of decorator ambiguity and no claim of runtime/public binding from a ClassDef alone. Measure that with newly authored complete alternatives/relations in a new prospective case. This case does not justify embeddings, BM25/LLM linking, ranking/resolution policy, broad graph expansion, or broad superiority claims.",
        "",
        "## 9. Recovery qualification",
        "",
        f"All joined Stage B outputs remain identified as RECOVERY `{RECOVERY_ID}`. The sole additional execution was preauthorized. Attempt 1's failed correspondence check retained no semantic output; recovery changed only harness member-order matching, not treatment. Durable recovery output does not alter the measured effectiveness or explain the zero candidate surface.",
        "",
        "## 10. Limitations",
        "",
        "This is one prospective configuration and no threshold was frozen. Counterfactual results are resource-level assumptions, not rerun production behavior; no generated rank/depth is defined. The recovery limitation is the earlier capture correspondence failure. Confirmation remains sealed and was not accessed. No Retrieval, routing, grounding or generation stage was rerun. Production source, Stage A treatment, capture/recovery artifacts, Stage B.5 packet and Stage C judgments were not modified.",
        "",
        "Next bounded increment: define and validate the narrow decorated-ClassDef grounding contract, then freeze a new prospective case whose recipes explicitly cover source, test, package, documentation, task-frame and validation witnesses before any acquisition. Do not implement an automatic resolver policy.",
        "",
    ]
    return "\n".join(lines)


def main() -> None:
    result = main_analysis()
    result["analysis_payload_sha256"] = sha(canon(result))
    markdown = render_markdown(result)
    data = canon(result)
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--verify",
        action="store_true",
        help="recompute and compare frozen outputs without writing",
    )
    args = parser.parse_args()
    if args.verify:
        assert_(
            (ANALYSIS_JSON.read_bytes() if ANALYSIS_JSON.exists() else b"") == data,
            "analysis.json replay mismatch",
        )
        assert_(
            (ANALYSIS_MD.read_bytes() if ANALYSIS_MD.exists() else b"")
            == markdown.encode("utf-8"),
            "analysis.md replay mismatch",
        )
        assert_(
            (ANALYSIS_SHA.read_bytes() if ANALYSIS_SHA.exists() else b"")
            == f"{sha(data)}  analysis.json\n".encode(),
            "analysis.sha256 replay mismatch",
        )
        print(f"verified deterministic replay analysis.json sha256={sha(data)}")
        return
    for path in (ANALYSIS_JSON, ANALYSIS_MD, ANALYSIS_SHA):
        assert_(not path.exists(), f"Refusing overwrite: {path.name}")
    ANALYSIS_JSON.write_bytes(data)
    ANALYSIS_MD.write_text(markdown, encoding="utf-8", newline="\n")
    ANALYSIS_SHA.write_text(
        f"{sha(data)}  analysis.json\n", encoding="utf-8", newline="\n"
    )
    print(f"analysis.json sha256={sha(data)}")
    print(f"analysis.md sha256={sha(markdown.encode())}")


if __name__ == "__main__":
    main()
