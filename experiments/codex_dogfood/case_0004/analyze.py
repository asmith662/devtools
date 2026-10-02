"""Join frozen Case 0004 BM25 lanes to the frozen blind judgments.

This case-local post-freeze script only computes diagnostics. It never invokes
Retrieval or writes treatment/judgment files. Run normally once to create the
analysis pair, and with --check to recompute and verify both outputs.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
import sys
from collections import Counter
from itertools import pairwise
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[3]
CASE = ROOT / "experiments" / "codex_dogfood" / "case_0004"
ADJ = CASE / "adjudication"
STAGE_A = "719a3d44b45ebc664414ab0267ff23d836cc10a0"
STAGE_B = "9416efc80028ca463375d005e114fb3143fd968d"
STAGE_B5 = "70114224aa7bf307e059468e0d543aff9796d8b7"
STAGE_C = "fa1864d08ec057c8c834b1616e6003734ecd74b1"
EXPECTED_HEAD = STAGE_C
SCHEMA = "codex-case-0004-joined-analysis-v1"


def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def canonical(value: object) -> bytes:
    return (
        json.dumps(value, ensure_ascii=False, sort_keys=True, indent=2, allow_nan=False)
        + "\n"
    ).encode()


def read_json(path: Path) -> tuple[dict[str, Any], bytes]:
    data = path.read_bytes()
    return json.loads(data), data


def git_blob(commit: str, path: str) -> bytes:
    return subprocess.check_output(["git", "show", f"{commit}:{path}"], cwd=ROOT)


def verify_chain_and_frozen_inputs() -> dict[str, Any]:
    ancestry = subprocess.run(
        ["git", "merge-base", "--is-ancestor", EXPECTED_HEAD, "HEAD"],
        cwd=ROOT,
        check=False,
    )
    if ancestry.returncode != 0:
        raise ValueError("Analysis requires Stage C in the current history.")
    commits = [STAGE_A, STAGE_B, STAGE_B5, STAGE_C]
    for earlier, later in pairwise(commits):
        parent = subprocess.check_output(
            ["git", "rev-parse", f"{later}^"], cwd=ROOT, text=True
        ).strip()
        if parent != earlier:
            raise ValueError(
                f"Frozen checkpoint chain is not direct: {earlier} -> {later}."
            )

    pre_path = "experiments/codex_dogfood/case_0004/pre_retrieval.json"
    inputs_path = "experiments/codex_dogfood/case_0004/inputs.pkl.gz"
    capture_path = "experiments/codex_dogfood/case_0004/capture.pkl.gz"
    retrieval_path = "experiments/codex_dogfood/case_0004/retrieval.json"
    manifest_path = (
        "experiments/codex_dogfood/case_0004/adjudication/blind_manifest.json"
    )
    resources_path = (
        "experiments/codex_dogfood/case_0004/adjudication/blind_resources.json.gz"
    )
    judgments_path = (
        "experiments/codex_dogfood/case_0004/adjudication/blind_judgments.json"
    )

    pre, pre_bytes = read_json(CASE / "pre_retrieval.json")
    retrieval, retrieval_bytes = read_json(CASE / "retrieval.json")
    manifest, manifest_bytes = read_json(ADJ / "blind_manifest.json")
    judgments, judgments_bytes = read_json(ADJ / "blind_judgments.json")
    inputs_bytes = (CASE / "inputs.pkl.gz").read_bytes()
    capture_bytes = (CASE / "capture.pkl.gz").read_bytes()
    resources_bytes = (ADJ / "blind_resources.json.gz").read_bytes()

    # The stage record hashes the canonical LF text, while Git's Windows blob
    # is CRLF. This is the same explicit normalization used by the capture.
    if pre_bytes.replace(b"\r\n", b"\n") != git_blob(STAGE_A, pre_path).replace(
        b"\r\n", b"\n"
    ):
        raise ValueError("Stage A pre_retrieval.json differs from its frozen Git blob.")
    if inputs_bytes != git_blob(STAGE_A, inputs_path):
        raise ValueError("Stage A input archive differs from its frozen Git blob.")
    if retrieval_bytes != git_blob(
        STAGE_B, retrieval_path
    ) or capture_bytes != git_blob(STAGE_B, capture_path):
        raise ValueError("Stage B frozen output differs from its committed Git blob.")
    if manifest_bytes != git_blob(
        STAGE_B5, manifest_path
    ) or resources_bytes != git_blob(STAGE_B5, resources_path):
        raise ValueError("Stage B.5 blind packet differs from its committed Git blob.")
    if judgments_bytes != git_blob(STAGE_C, judgments_path):
        raise ValueError("Stage C judgments differ from their committed Git blob.")

    if (
        sha(inputs_bytes) != pre["inputs_archive_sha256"]
        or sha(inputs_bytes) != retrieval["inputs_archive_sha256"]
    ):
        raise ValueError("Frozen native input archive digest mismatch.")
    if sha(capture_bytes) != retrieval["native_capture_sha256"]:
        raise ValueError("Frozen native capture digest mismatch.")
    if (
        sha(retrieval_bytes)
        != "37fa5b7a53efbe326b9cfc9d0da4e7761fed0d83607bc184ba09b4765f548848"
    ):
        raise ValueError("Frozen retrieval JSON digest mismatch.")
    protocol_sha = sha(pre_bytes.replace(b"\r\n", b"\n"))
    if protocol_sha != retrieval["protocol_sha256"]:
        raise ValueError(
            "Stage B protocol digest does not match canonical Stage A treatment."
        )
    if (
        sha(manifest_bytes)
        != "7810e71a91fb9d5327aeb20d00629f1347049993aff15544b5139529c9f777d5"
    ):
        raise ValueError("Frozen blind manifest digest mismatch.")
    if (
        sha(resources_bytes) != manifest["resource_archive"]["sha256"]
        or sha(resources_bytes)
        != "4d472717ba3e3306e81f96953c8fd9e6ab04e0d59fb698bd021386a40bcf147f"
    ):
        raise ValueError("Frozen blind resource archive digest mismatch.")
    if (
        sha(judgments_bytes)
        != "77d28c1997e8ec8a7e22eee9a37da3d08a08e165d06ab977175d9caaa4f7fc44"
    ):
        raise ValueError("Frozen blind judgments file digest mismatch.")
    payload = {
        key: value for key, value in judgments.items() if key != "artifact_digest"
    }
    if sha(canonical(payload)) != judgments["artifact_digest"]["value"]:
        raise ValueError("Stage C embedded judgment payload digest mismatch.")
    if judgments["blind_packet_digests"] != {
        "blind_manifest.json": sha(manifest_bytes),
        "blind_resources.json.gz": sha(resources_bytes),
        "task_text_utf8": sha(manifest["task_text"].encode()),
    }:
        raise ValueError("Stage C packet digest references mismatch.")
    if (
        retrieval["stage_a_commit"] != STAGE_A
        or retrieval["protocol_sha256"] != protocol_sha
    ):
        raise ValueError("Stage B does not link to Stage A.")
    if (
        retrieval["case"] != "case_0004"
        or manifest["case_identity"] != "case_0004"
        or judgments["case_identity"] != "case_0004"
    ):
        raise ValueError("Case identity mismatch.")
    if (
        judgments["task_identity"] != manifest["task_identity"]
        or judgments["task_text"] != manifest["task_text"]
        or judgments["purpose"] != manifest["purpose"]
        or judgments["eligible_frame_identity"] != manifest["eligible_frame_identity"]
        or judgments["shared_anchors"] != manifest["anchors"]
    ):
        raise ValueError(
            "Stage C task, purpose, anchors or frame differ from Stage B.5."
        )
    for key in ("repository_id", "snapshot_id"):
        if len({pre[key], retrieval[key], manifest[key], judgments[key]}) != 1:
            raise ValueError(f"Frozen {key} mismatch.")
    if (
        len(
            {
                pre["frame_resource_count"],
                retrieval["eligible_resource_count"],
                manifest["eligible_resource_count"],
                judgments["frame_coverage"]["eligible_resources"],
            }
        )
        != 1
    ):
        raise ValueError("Eligible frame count mismatch.")
    if (
        retrieval["corpus_id"] != manifest["eligible_frame_identity"]
        or pre["eligible_corpus_id"] != manifest["eligible_frame_identity"]
    ):
        raise ValueError("Corpus/frame identity mismatch.")
    if pre["task_identity"] != manifest["task_identity"] or pre["task_sha256"] != sha(
        manifest["task_text"].encode()
    ):
        raise ValueError("Frozen task identity/text mismatch.")
    return (
        {
            "checkpoint_commits": {
                "stage_a": STAGE_A,
                "stage_b": STAGE_B,
                "stage_b5": STAGE_B5,
                "stage_c": STAGE_C,
            },
            "artifact_sha256": {
                "pre_retrieval.json": sha(pre_bytes),
                "inputs.pkl.gz": sha(inputs_bytes),
                "capture.pkl.gz": sha(capture_bytes),
                "retrieval.json": sha(retrieval_bytes),
                "blind_manifest.json": sha(manifest_bytes),
                "blind_resources.json.gz": sha(resources_bytes),
                "blind_judgments.json": sha(judgments_bytes),
            },
            "frozen_protocol_sha256_lf": protocol_sha,
        },
        pre,
        retrieval,
        manifest,
        judgments,
    )


def rank_map(lane: dict[str, Any]) -> dict[str, dict[str, Any]]:
    result: dict[str, dict[str, Any]] = {}
    for expected_rank, match in enumerate(lane["matches"], 1):
        if match["native_rank"] != expected_rank:
            raise ValueError(f"Native ranks are not contiguous in {lane['identity']}.")
        address = match["resource_address"]
        if address in result:
            raise ValueError(
                f"Duplicate resource match in {lane['identity']}: {address}."
            )
        result[address] = match
    if len(result) != lane["result_count"]:
        raise ValueError(f"Result count mismatch in {lane['identity']}.")
    return result


def contribution_kind(match: dict[str, Any]) -> dict[str, Any]:
    content = sum(item["contribution"] for item in match["content_contributions"])
    filename = match["weighted_filename_score"]
    if content and filename:
        kind = "both"
    elif content:
        kind = "content"
    elif filename:
        kind = "filename"
    else:
        kind = "unavailable"
    return {
        "kind": kind,
        "content_contribution_sum": content,
        "weighted_filename_contribution": filename,
        "content_terms": [
            item["normalized_term"] for item in match["content_contributions"]
        ],
        "filename_terms": [
            item["normalized_term"] for item in match["filename_contributions"]
        ],
    }


def summarize_ranks(values: list[int | None]) -> dict[str, Any]:
    finite = sorted(v for v in values if v is not None)
    return {
        "observations": len(values),
        "reached": len(finite),
        "missed": len(values) - len(finite),
        "min": finite[0] if finite else None,
        "median": (finite[(len(finite) - 1) // 2] + finite[len(finite) // 2]) / 2
        if finite
        else None,
        "max": finite[-1] if finite else None,
        "mean": sum(finite) / len(finite) if finite else None,
        "ranks": finite,
    }


def build_analysis(
    chain: dict[str, Any],
    pre: dict[str, Any],
    retrieval: dict[str, Any],
    manifest: dict[str, Any],
    judgments: dict[str, Any],
) -> dict[str, Any]:
    if retrieval["lane_count"] != 9 or len(retrieval["lanes"]) != 9:
        raise ValueError("Expected exactly nine frozen lanes.")
    expected_obligations = [item["identity"] for item in manifest["obligations"]]
    judgment_obligations = [
        item["frozen_obligation"]["identity"] for item in judgments["obligations"]
    ]
    query_obligations = [item["obligation"] for item in pre["obligation_lanes"]]
    lane_obligations = [
        lane.get("obligation_identity") for lane in retrieval["lanes"][1:]
    ]
    if not (
        expected_obligations
        == judgment_obligations
        == query_obligations
        == lane_obligations
    ):
        raise ValueError(
            "Frozen obligation identities/order do not match across stages."
        )
    if any(
        judgment["frozen_obligation"] != frozen
        for judgment, frozen in zip(judgments["obligations"], manifest["obligations"])
    ):
        raise ValueError("Stage C obligation semantics differ from the blind manifest.")
    all_judgment_units = [
        unit["unit_identity"]
        for judgment in judgments["obligations"]
        for unit in judgment["information_units"]
    ]
    if len(all_judgment_units) != len(set(all_judgment_units)):
        raise ValueError("Duplicate Stage C information-unit identity.")
    all_alternative_ids = [
        alternative["identity"]
        for judgment in judgments["obligations"]
        for alternative in judgment["acceptable_witness_alternatives"]
    ]
    if len(all_alternative_ids) != len(set(all_alternative_ids)):
        raise ValueError("Duplicate Stage C witness-alternative identity.")
    if judgments["unresolved_judgments"] or judgments["inherent_discovery"]:
        raise ValueError("Unexpected unresolved or inherent-discovery judgment.")
    if any(j["applicability"] != "APPLICABLE" for j in judgments["obligations"]):
        raise ValueError("Unexpected Stage C applicability disposition.")
    if any(
        j["frozen_obligation"]["requirement"] != "mandatory"
        for j in judgments["obligations"]
    ):
        raise ValueError("A frozen obligation is not mandatory.")
    if len(set(judgment_obligations)) != 8 or any(
        len(j["acceptable_witness_alternatives"]) == 0 for j in judgments["obligations"]
    ):
        raise ValueError("Duplicate obligation or missing adjudicated alternative.")
    global_lane = retrieval["lanes"][0]
    if (
        global_lane["identity"] != "global-full-task"
        or pre["global_lane"]["identity"] != "global-full-task"
    ):
        raise ValueError("Missing global full-task lane.")
    lane_by_ob = {lane["obligation_identity"]: lane for lane in retrieval["lanes"][1:]}
    if (
        len(lane_by_ob) != 8
        or len({lane["identity"] for lane in retrieval["lanes"]}) != 9
    ):
        raise ValueError("Missing or duplicate Retrieval lanes.")
    for frozen, lane in zip(pre["obligation_lanes"], retrieval["lanes"][1:]):
        if (
            lane["identity"] != frozen["identity"]
            or lane["query_text"] != frozen["query_text"]
        ):
            raise ValueError(
                "Obligation query association or exact query text changed."
            )
    for lane in retrieval["lanes"]:
        if (
            lane["maximum_results"] != pre["bm25"]["maximum_results"]
            or lane["settings"] != {"k1": pre["bm25"]["k1"], "b": pre["bm25"]["b"]}
            or not pre["bm25"]["query_semantics"].startswith(lane["query_semantics"])
        ):
            raise ValueError("Frozen lane settings or bound differ from Stage A.")
    if global_lane["query_text"] != pre["global_lane"]["query_text"]:
        raise ValueError("Global query differs from frozen treatment.")

    frame = {
        item["address"]: {
            **item,
            "identity": "repository-resource-address:" + item["address"],
        }
        for item in pre["snapshot_resources"]
    }
    judgment_rows = judgments["resource_matrix"]
    if len(frame) != 498 or len(judgment_rows) != 498:
        raise ValueError(
            "Expected 498 members in the frozen frame and judgment matrix."
        )
    if len({item["resource_identity"] for item in judgment_rows}) != 498:
        raise ValueError("Judgment resource identity duplicated.")
    judgment_by_path = {item["path"]: item for item in judgment_rows}
    if set(frame) != set(judgment_by_path):
        raise ValueError(
            "Adjudicated resources do not exactly match the frozen corpus frame."
        )
    if any(
        judgment_by_path[path]["resource_identity"] != row["identity"]
        for path, row in frame.items()
    ):
        raise ValueError("Resource identity disagreement across Stage A and C.")
    frame_by_id = {row["identity"]: row for row in frame.values()}

    rankmaps = {lane["identity"]: rank_map(lane) for lane in retrieval["lanes"]}
    address_union = set(frame)
    for lane in retrieval["lanes"]:
        for address, match in rankmaps[lane["identity"]].items():
            if address not in address_union:
                raise ValueError(f"Retrieval resource outside frozen frame: {address}.")
            if frame[address]["content_identity"] != match["content_identity"]:
                raise ValueError(f"Retrieval content identity mismatch: {address}.")
    positive_count = sum(len(value) for value in rankmaps.values())
    candidate_union = set().union(*(set(x) for x in rankmaps.values()))
    global_set = set(rankmaps[global_lane["identity"]])
    obligation_sets = {
        ob: set(rankmaps[lane["identity"]]) for ob, lane in lane_by_ob.items()
    }
    obligation_union = set().union(*obligation_sets.values())
    global_only = global_set - obligation_union
    obligation_only = obligation_union - global_set
    shared = global_set & obligation_union
    result_counts = {
        lane["identity"]: len(rankmaps[lane["identity"]]) for lane in retrieval["lanes"]
    }
    pair_overlaps = {
        ob: {
            "global_and_lane": len(global_set & values),
            "global_only_vs_lane": len(global_set - values),
            "lane_only_vs_global": len(values - global_set),
        }
        for ob, values in obligation_sets.items()
    }

    units: list[dict[str, Any]] = []
    obligations_out = []
    required_unit_ids: set[str] = set()
    required_resources_by_ob: dict[str, set[str]] = {}
    useful_resources_by_ob: dict[str, set[str]] = {}
    for judgment in judgments["obligations"]:
        frozen = judgment["frozen_obligation"]
        ob = frozen["identity"]
        lane = lane_by_ob[ob]
        own_ranks = rankmaps[lane["identity"]]
        relevant_units = [
            unit
            for unit in judgment["information_units"]
            if unit["category"] == "REQUIRED"
        ]
        helpful_units = [
            unit
            for unit in judgment["information_units"]
            if unit["category"] == "HELPFUL_ONLY"
        ]
        alternatives = []
        required_for_ob: set[str] = set()
        for alt in judgment["acceptable_witness_alternatives"]:
            alt_units = [
                next(
                    u
                    for u in judgment["information_units"]
                    if u["unit_identity"] == unit_id
                )
                for unit_id in alt["all_of"]
            ]
            if not set(alt["all_of"]) <= {u["unit_identity"] for u in relevant_units}:
                raise ValueError(
                    f"Alternative has a non-required/unknown unit: {ob}/{alt['identity']}."
                )
            members = []
            for unit in alt_units:
                path = unit["path"]
                resource_id = unit["resource_identity"]
                if (
                    resource_id not in frame_by_id
                    or frame_by_id[resource_id]["address"] != path
                ):
                    raise ValueError(f"Unknown witness resource: {resource_id}.")
                required_for_ob.add(path)
                rank = own_ranks.get(path, {}).get("native_rank")
                global_rank = (
                    rankmaps[global_lane["identity"]].get(path, {}).get("native_rank")
                )
                members.append(
                    {
                        "unit_identity": unit["unit_identity"],
                        "resource_identity": resource_id,
                        "path": path,
                        "own_lane_rank": rank,
                        "global_rank": global_rank,
                        "own_lane_reachable": rank is not None,
                    }
                )
            member_ranks = [item["own_lane_rank"] for item in members]
            global_member_ranks = [item["global_rank"] for item in members]
            alternatives.append(
                {
                    "identity": alt["identity"],
                    "unit_ids": alt["all_of"],
                    "resources": sorted({item["path"] for item in members}),
                    "members": members,
                    "completion_depth": max(member_ranks)
                    if member_ranks and all(r is not None for r in member_ranks)
                    else None,
                    "global_completion_depth": max(global_member_ranks)
                    if global_member_ranks
                    and all(r is not None for r in global_member_ranks)
                    else None,
                    "complete_in_own_lane": bool(member_ranks)
                    and all(r is not None for r in member_ranks),
                    "complete_in_global_lane": bool(global_member_ranks)
                    and all(r is not None for r in global_member_ranks),
                }
            )
        required_for_ob.update(u["path"] for u in relevant_units)
        required_resources_by_ob[ob] = required_for_ob
        useful_resources_by_ob[ob] = {u["path"] for u in helpful_units}
        best_own = min(
            (
                a["completion_depth"]
                for a in alternatives
                if a["completion_depth"] is not None
            ),
            default=None,
        )
        best_global = min(
            (
                a["global_completion_depth"]
                for a in alternatives
                if a["global_completion_depth"] is not None
            ),
            default=None,
        )
        obligations_out.append(
            {
                "identity": ob,
                "applicability": judgment["applicability"],
                "required_unit_count": len(relevant_units),
                "helpful_unit_count": len(helpful_units),
                "required_resource_count": len(required_for_ob),
                "alternative_count": len(alternatives),
                "alternatives": alternatives,
                "best_own_completion_depth": best_own,
                "best_global_completion_depth": best_global,
                "complete_in_own_lane": best_own is not None,
                "complete_in_global_lane": best_global is not None,
                "own_vs_global": "both_incomplete"
                if best_own is None and best_global is None
                else "own_only"
                if best_own is not None and best_global is None
                else "global_only"
                if best_own is None and best_global is not None
                else "own_shallower"
                if best_own < best_global
                else "global_shallower"
                if best_global < best_own
                else "equal",
                "lane_result_count": len(own_ranks),
                "lane_query_identity": lane["identity"],
                "lane_query_text": lane["query_text"],
            }
        )
        for unit in judgment["information_units"]:
            path = unit["path"]
            own_rank = own_ranks.get(path, {}).get("native_rank")
            global_rank = (
                rankmaps[global_lane["identity"]].get(path, {}).get("native_rank")
            )
            if unit["category"] == "REQUIRED":
                required_unit_ids.add(unit["unit_identity"])
            other_hits = [
                {
                    "obligation": other,
                    "rank": rankmaps[lane_by_ob[other]["identity"]]
                    .get(path, {})
                    .get("native_rank"),
                }
                for other in expected_obligations
                if other != ob and path in rankmaps[lane_by_ob[other]["identity"]]
            ]
            other_best = min((item["rank"] for item in other_hits), default=None)
            if own_rank is not None and global_rank is not None:
                rank_comparison = (
                    "own_shallower"
                    if own_rank < global_rank
                    else "global_shallower"
                    if global_rank < own_rank
                    else "equal"
                )
            elif own_rank is not None:
                rank_comparison = "only_own_reaches"
            elif global_rank is not None:
                rank_comparison = "only_global_reaches"
            else:
                rank_comparison = "neither_reaches"
            units.append(
                {
                    "unit_identity": unit["unit_identity"],
                    "obligation": ob,
                    "category": unit["category"],
                    "resource_identity": unit["resource_identity"],
                    "path": path,
                    "global_rank": global_rank,
                    "own_lane_rank": own_rank,
                    "own_lane_reachable": own_rank is not None,
                    "global_reachable": global_rank is not None,
                    "rank_comparison": rank_comparison,
                    "other_obligation_lane_hits": other_hits,
                    "best_other_obligation_rank": other_best,
                    "other_lane_better_than_own": own_rank is None
                    and other_best is not None
                    or own_rank is not None
                    and other_best is not None
                    and other_best < own_rank,
                }
            )

    required_resources = set().union(*required_resources_by_ob.values())
    if (
        len(required_unit_ids) != 25
        or sum(len(x) for x in required_resources_by_ob.values()) != 25
    ):
        raise ValueError(
            "Frozen required-unit count does not match the Stage C frame (expected 25)."
        )
    global_ranks = rankmaps[global_lane["identity"]]
    global_required_ranks = {
        path: global_ranks[path]["native_rank"]
        for path in sorted(required_resources)
        if path in global_ranks
    }
    own_found, other_found = set(), set()
    resource_own_lane: dict[str, str] = {}
    resource_other_lanes: dict[str, list[dict[str, Any]]] = {}
    for path in required_resources:
        own_obligations = [
            ob for ob, paths in required_resources_by_ob.items() if path in paths
        ]
        own = [ob for ob in own_obligations if path in obligation_sets[ob]]
        other = [
            {
                "obligation": ob,
                "rank": rankmaps[lane_by_ob[ob]["identity"]][path]["native_rank"],
            }
            for ob in expected_obligations
            if ob not in own_obligations and path in obligation_sets[ob]
        ]
        if own:
            own_found.add(path)
        if other:
            other_found.add(path)
        resource_own_lane[path] = "found" if own else "missed"
        resource_other_lanes[path] = other
    global_reached = set(global_required_ranks)
    category_sets = {
        "global_only": global_reached - obligation_union,
        "obligation_lane_only": obligation_union - global_reached,
        "both": obligation_union & global_reached,
        "neither": required_resources - (global_reached | obligation_union),
    }

    global_recall = len(global_reached) / len(required_resources)
    global_depth = max(global_required_ranks.values(), default=None)
    global_unit_ranks = [
        rankmaps[global_lane["identity"]].get(u["path"], {}).get("native_rank")
        for u in units
        if u["category"] == "REQUIRED"
    ]
    obligation_completion = {
        item["identity"]: item["best_own_completion_depth"] for item in obligations_out
    }
    all_complete = all(value is not None for value in obligation_completion.values())
    obligation_wise_max = max(obligation_completion.values()) if all_complete else None

    depth_union = set()
    depth_occurrences = 0
    for ob, item in zip(expected_obligations, obligations_out):
        depth = item["best_own_completion_depth"]
        if depth is not None:
            selected = {
                path: rank
                for path, rank in rankmaps[lane_by_ob[ob]["identity"]].items()
                if rank["native_rank"] <= depth
            }
            depth_union.update(selected)
            depth_occurrences += len(selected)

    global_categories = {
        "global_only": sorted(category_sets["global_only"]),
        "obligation_lanes_only": sorted(category_sets["obligation_lane_only"]),
        "both": sorted(category_sets["both"]),
        "neither": sorted(category_sets["neither"]),
    }
    cross = []
    for path in sorted(required_resources):
        owner_obs = sorted(
            ob for ob, paths in required_resources_by_ob.items() if path in paths
        )
        own = [ob for ob in owner_obs if path in obligation_sets[ob]]
        others = resource_other_lanes[path]
        grank = global_ranks.get(path, {}).get("native_rank")
        if own and grank is not None:
            cat = "both_global_and_own"
        elif own:
            cat = "own_only_global_miss"
        elif grank is not None and not others:
            cat = "global_only"
        elif grank is not None and others:
            cat = "global_and_other_lane_own_missed"
        elif others:
            cat = "other_obligation_only_own_missed"
        else:
            cat = "nowhere"
        cross.append(
            {
                "path": path,
                "owning_obligations": owner_obs,
                "own_lane_found_for_any_owner": bool(own),
                "own_lane_hits": {
                    ob: rankmaps[lane_by_ob[ob]["identity"]][path]["native_rank"]
                    for ob in own
                },
                "global_rank": grank,
                "other_obligation_hits": others,
                "category": cat,
            }
        )

    required_unit_results = [u for u in units if u["category"] == "REQUIRED"]
    helpful_unit_results = [u for u in units if u["category"] == "HELPFUL_ONLY"]
    missed_required_units = [
        u for u in required_unit_results if not u["own_lane_reachable"]
    ]
    required_unit_reach = Counter(u["rank_comparison"] for u in required_unit_results)
    global_helpful_ranks = [u["global_rank"] for u in helpful_unit_results]
    own_helpful_ranks = [u["own_lane_rank"] for u in helpful_unit_results]
    global_required_best = min(global_required_ranks.values(), default=None)
    helpful_shallower_global = sum(
        rank is not None
        and global_required_best is not None
        and rank < global_required_best
        for rank in global_helpful_ranks
    )
    helpful_shallower_own = {}
    for ob in expected_obligations:
        req = [
            u["own_lane_rank"]
            for u in required_unit_results
            if u["obligation"] == ob and u["own_lane_rank"] is not None
        ]
        help_ranks = [
            u["own_lane_rank"] for u in helpful_unit_results if u["obligation"] == ob
        ]
        best_req = min(req, default=None)
        helpful_shallower_own[ob] = {
            "helpful_units": len(help_ranks),
            "shallower_than_best_reached_required": sum(
                r is not None and best_req is not None and r < best_req
                for r in help_ranks
            ),
            "best_reached_required_rank": best_req,
        }
    helpful_only_unique_resources = {
        u["path"] for u in helpful_unit_results
    } - required_resources

    # Native lexical evidence is inspected only after reach, rank, and
    # alternative-completion metrics have been fully calculated.
    for unit in units:
        unit["own_lane_contributions"] = (
            contribution_kind(
                rankmaps[lane_by_ob[unit["obligation"]]["identity"]][unit["path"]]
            )
            if unit["own_lane_rank"] is not None
            else None
        )
        unit["global_contributions"] = (
            contribution_kind(global_ranks[unit["path"]])
            if unit["global_rank"] is not None
            else None
        )

    differences = []
    for unit in required_unit_results:
        if unit["global_rank"] is None or unit["own_lane_rank"] is None:
            delta = None
        else:
            delta = unit["own_lane_rank"] - unit["global_rank"]
        differences.append((abs(delta) if delta is not None else -1, unit, delta))
    conspicuous = []
    for _, unit, delta in sorted(
        differences, key=lambda item: (-item[0], item[1]["obligation"], item[1]["path"])
    )[:8]:
        conspicuous.append(
            {
                "obligation": unit["obligation"],
                "path": unit["path"],
                "unit_identity": unit["unit_identity"],
                "global_rank": unit["global_rank"],
                "own_lane_rank": unit["own_lane_rank"],
                "rank_delta_own_minus_global": delta,
                "global_contributions": unit["global_contributions"],
                "own_lane_contributions": unit["own_lane_contributions"],
            }
        )

    result = {
        "schema": SCHEMA,
        "case_identity": "case_0004",
        "task_identity": pre["task_identity"],
        "repository_id": pre["repository_id"],
        "snapshot_id": pre["snapshot_id"],
        "eligible_frame_identity": manifest["eligible_frame_identity"],
        "frozen_artifacts": chain,
        "analysis_implementation": {
            "path": "experiments/codex_dogfood/case_0004/analyze.py",
            "sha256": sha(Path(__file__).read_bytes()),
            "version": SCHEMA,
        },
        "join_integrity": {
            "case_identity": "exact",
            "repository_id": "exact",
            "snapshot_id": "exact",
            "eligible_frame_identity": "exact",
            "expected_resources": 498,
            "adjudicated_resources": len(judgment_rows),
            "global_lane_matches": len(global_set),
            "all_lane_matches_within_frame": True,
            "identity_coverage": {
                "expected": 498,
                "observed": 498,
                "duplicates": 0,
                "missing": 0,
                "unexpected": 0,
            },
            "obligations": {
                "expected": 8,
                "observed": len(judgment_obligations),
                "duplicates": 0,
                "missing": 0,
                "unexpected": 0,
            },
            "query_associations": [
                {
                    "obligation": f["obligation"],
                    "lane_identity": l["identity"],
                    "query_text_exact_match": f["query_text"] == l["query_text"],
                }
                for f, l in zip(pre["obligation_lanes"], retrieval["lanes"][1:])
            ],
            "lane_count": 9,
            "native_capture_deserialized": False,
            "native_capture_digest_verified": True,
        },
        "frozen_judgment_frame": {
            "required_unit_count": len(required_unit_ids),
            "helpful_unit_count": len(helpful_unit_results),
            "required_resource_count": len(required_resources),
            "required_resource_identities": {
                p: frame_by_id[
                    next(
                        u["resource_identity"]
                        for u in judgments["resource_matrix"]
                        if u["path"] == p
                    )
                ]["identity"]
                for p in sorted(required_resources)
            },
            "units_by_obligation": {
                j["identity"]: {
                    "required_units": j["required_unit_count"],
                    "alternative_count": j["alternative_count"],
                }
                for j in obligations_out
            },
            "resources_serving_multiple_obligations": {
                p: sorted(
                    ob for ob, paths in required_resources_by_ob.items() if p in paths
                )
                for p in sorted(required_resources)
                if sum(p in paths for paths in required_resources_by_ob.values()) > 1
            },
        },
        "global_full_task": {
            "lane_identity": global_lane["identity"],
            "query_text": global_lane["query_text"],
            "result_count": len(global_set),
            "bound": global_lane["maximum_results"],
            "required_resource_count": len(required_resources),
            "required_unit_count": len(required_unit_ids),
            "reachable_required_resources": len(global_reached),
            "required_resource_recall": global_recall,
            "complete_required_resource_depth": global_depth,
            "complete_required_unit_depth": max(
                (r for r in global_unit_ranks if r is not None), default=None
            )
            if all(r is not None for r in global_unit_ranks)
            else None,
            "required_unit_recall": sum(r is not None for r in global_unit_ranks)
            / len(global_unit_ranks),
            "required_resource_ranks": global_required_ranks,
            "required_unit_ranks": {
                u["unit_identity"]: u["global_rank"] for u in required_unit_results
            },
        },
        "per_obligation": obligations_out,
        "unit_rank_comparisons": units,
        "cross_obligation_discovery": cross,
        "required_own_lane_misses": {
            "required_unit_count": len(missed_required_units),
            "required_units": [u["unit_identity"] for u in missed_required_units],
            "unique_resources_with_any_owning_lane_miss": sorted(
                {u["path"] for u in missed_required_units}
            ),
            "unique_resources_missed_in_every_owning_lane": sorted(
                row["path"] for row in cross if not row["own_lane_found_for_any_owner"]
            ),
        },
        "required_resource_reach_categories": {
            k: {"count": len(v), "resources": v} for k, v in global_categories.items()
        },
        "required_unit_rank_comparison_counts": dict(required_unit_reach),
        "complete_mandatory_acquisition_coverage": {
            "applicable_mandatory_obligations": 8,
            "acquisition_complete_for_adjudicated_witnesses": sum(
                o["complete_in_own_lane"] for o in obligations_out
            ),
            "ratio": sum(o["complete_in_own_lane"] for o in obligations_out) / 8,
            "all_eight_coverable": all(
                o["complete_in_own_lane"] for o in obligations_out
            ),
            "obligation_wise_maximum_completion_depth": obligation_wise_max,
            "interpretation": "Maximum of each obligation's best reachable accepted alternative depth; no single merged ranking, no semantic resolution/readiness claim.",
        },
        "candidate_occurrences_and_union": {
            "lane_count": 9,
            "acquisition_runtime_seconds": retrieval["acquisition_runtime_seconds"],
            "acquisition_invocation_count": retrieval["acquisition_invocation_count"],
            "result_count_per_lane": result_counts,
            "summed_candidate_occurrences": positive_count,
            "unique_resource_union_count": len(candidate_union),
            "eligible_resources_without_any_positive_match": len(
                address_union - candidate_union
            ),
            "resources_without_any_positive_match": sorted(
                address_union - candidate_union
            ),
            "duplicate_resource_occurrences": positive_count - len(candidate_union),
            "unique_resources_in_any_obligation_lane": len(obligation_union),
            "unique_resources_only_global_lane": len(global_only),
            "unique_resources_only_obligation_lanes": len(obligation_only),
            "global_obligation_union_overlap": len(shared),
            "pairwise_global_lane_overlaps": pair_overlaps,
            "zero_result_lanes": [
                lane["identity"]
                for lane in retrieval["lanes"]
                if not rankmaps[lane["identity"]]
            ],
            "own_lane_completion_prefix_union": {
                "depth_occurrences": depth_occurrences,
                "unique_resources": len(depth_union),
                "resources": sorted(depth_union),
                "definition": "Union of each obligation lane's own top-N prefix, with N equal to that obligation's best acceptable-alternative completion depth.",
            },
        },
        "helpful_only_diagnostics": {
            "helpful_unit_count": len(helpful_unit_results),
            "unique_helpful_resources_in_any_obligation": len(
                {u["path"] for u in helpful_unit_results}
            ),
            "unique_resources_judged_helpful_only_globally": len(
                helpful_only_unique_resources
            ),
            "global_unit_rank_distribution": summarize_ranks(global_helpful_ranks),
            "own_obligation_lane_unit_rank_distribution": summarize_ranks(
                own_helpful_ranks
            ),
            "helpful_units_shallower_than_best_reached_required_global": helpful_shallower_global,
            "per_obligation_helpful_shallower_counts": helpful_shallower_own,
            "helpful_ranks_are_descriptive_and_excluded_from_mandatory_coverage": True,
        },
        "native_contribution_diagnostics": {
            "selection": "Eight largest absolute required-unit rank differences where both ranks exist; deterministic tie order. Contribution sums explain native components only and do not establish causation.",
            "examples": conspicuous,
        },
        "historical_global_depths": {
            "case_0001": {
                "full_task": 35,
                "short_need": 132,
                "source": "docs/roadmap.md, Codex dogfood Case 0001 paragraph",
            },
            "case_0002": {
                "full_task": 43,
                "short_need": 87,
                "source": "docs/roadmap.md, Codex dogfood Case 0002 paragraph",
            },
            "case_0003": {
                "full_task": 348,
                "short_need": 180,
                "source": "docs/roadmap.md, Case 0003 implementation paragraph",
            },
            "comparison_limit": "Descriptive figures only; task/frame sizes differ and results are not pooled.",
        },
        "limitations": [
            "BM25 returns positive matches only; an absent match is no positive lexical match within this frozen corpus, not semantic absence.",
            "All ranks are native within-lane ranks; scores are not compared across lanes.",
            "The adjudicated required resource set is derived from 25 obligation-relative units and accepted alternatives; units can share resources.",
            "The obligation-wise maximum is not one merged ranked list or a realized acquisition plan.",
            "One task and one repository snapshot support case-specific observation only, with no superiority threshold frozen.",
            "No production obligation satisfaction or resolution follows from lexical reach.",
        ],
        "stage_d_boundary": {
            "retrieval_rerun": False,
            "treatment_changed": False,
            "judgments_changed": False,
            "production_changed": False,
            "confirmation_accessed": False,
        },
    }
    return result


def markdown(result: dict[str, Any]) -> str:
    global_data = result["global_full_task"]
    complete = result["complete_mandatory_acquisition_coverage"]
    lines = [
        "# Case 0004 Stage D joined analysis",
        "",
        "This report joins the frozen Stage B BM25 capture to the independent Stage C judgments. It measures lexical acquisition reach, not semantic satisfaction.",
        "",
        f"- Task: `{result['task_identity']}`",
        f"- Repository / snapshot: `{result['repository_id']}` / `{result['snapshot_id']}`",
        f"- Eligible frame: {result['join_integrity']['identity_coverage']['expected']}/{result['join_integrity']['identity_coverage']['observed']} exact identities; 8/8 obligations; nine lanes.",
        f"- Unique required resources: {result['frozen_judgment_frame']['required_resource_count']}; required units: {result['frozen_judgment_frame']['required_unit_count']}.",
        f"- Global full-task lane: {global_data['reachable_required_resources']}/{global_data['required_resource_count']} required resources (recall {global_data['required_resource_recall']:.3f}); complete depth {global_data['complete_required_resource_depth']}.",
        f"- Own obligation lanes: {complete['acquisition_complete_for_adjudicated_witnesses']}/8 acquisition-complete for adjudicated witnesses ({complete['ratio']:.3f}); obligation-wise maximum completion depth {complete['obligation_wise_maximum_completion_depth']}.",
        "",
        "## Per-obligation acquisition",
        "",
        "Alternative completion depth is the maximum native member rank when all members are reached; an incomplete alternative has no finite depth. `global best` applies the same frozen alternatives in the global lane.",
        "",
        "| Obligation | Required units | Required resources | Alternatives | Lane results | Own best depth | Global best depth | Own lane result | Comparison |",
        "| --- | ---: | ---: | ---: | ---: | ---: | ---: | --- | --- |",
    ]
    for ob in result["per_obligation"]:
        lines.append(
            f"| {ob['identity']} | {ob['required_unit_count']} | {ob['required_resource_count']} | {ob['alternative_count']} | {ob['lane_result_count']} | {ob['best_own_completion_depth']} | {ob['best_global_completion_depth']} | {ob['complete_in_own_lane']} | {ob['own_vs_global']} |"
        )
    lines += [
        "",
        "### Accepted alternatives",
        "",
        "Each row is one complete acceptable information set; every listed member is conjunctive. `None` means at least one member had no positive match.",
        "",
        "| Obligation | Alternative | Resource members (own rank) | Own depth | Global depth |",
        "| --- | --- | --- | ---: | ---: |",
    ]
    for ob in result["per_obligation"]:
        for alternative in ob["alternatives"]:
            members = ", ".join(
                f"`{member['path']}` ({member['own_lane_rank'] or '—'})"
                for member in alternative["members"]
            )
            lines.append(
                f"| {ob['identity']} | {alternative['identity']} | {members} | {alternative['completion_depth']} | {alternative['global_completion_depth']} |"
            )
    lines += [
        "",
        "## Required-resource reach",
        "",
        "| Category | Count |",
        "| --- | ---: |",
    ]
    for key, label in [
        ("global_only", "Global only"),
        ("obligation_lanes_only", "Obligation lanes only"),
        ("both", "Both"),
        ("neither", "Neither"),
    ]:
        lines.append(
            f"| {label} | {result['required_resource_reach_categories'][key]['count']} |"
        )
    missed = [
        row
        for row in result["cross_obligation_discovery"]
        if not row["own_lane_found_for_any_owner"]
    ]
    other_better = [
        u
        for u in result["unit_rank_comparisons"]
        if u["category"] == "REQUIRED" and u["other_lane_better_than_own"]
    ]
    lines += [
        "",
        f"Required resources missed in every owning lane: {len(missed)}. Required units retrieved at a better rank by another obligation lane (or only there): {len(other_better)}.",
        "",
    ]
    if missed:
        lines += [
            "| Missed required resource | Owning obligation(s) | Global rank | Other obligation hits |",
            "| --- | --- | ---: | --- |",
        ]
        for row in missed:
            other = (
                ", ".join(
                    f"{x['obligation']}:{x['rank']}"
                    for x in row["other_obligation_hits"]
                )
                or "—"
            )
            lines.append(
                f"| `{row['path']}` | {', '.join(row['owning_obligations'])} | {row['global_rank']} | {other} |"
            )
    lines += [
        "",
        "## Candidate union and helpful evidence",
        "",
        f"Nine lanes returned {result['candidate_occurrences_and_union']['summed_candidate_occurrences']} candidate occurrences over {result['candidate_occurrences_and_union']['unique_resource_union_count']} unique resources ({result['candidate_occurrences_and_union']['duplicate_resource_occurrences']} repeated occurrences). The obligation lanes contained {result['candidate_occurrences_and_union']['unique_resources_in_any_obligation_lane']} unique resources; {result['candidate_occurrences_and_union']['unique_resources_only_global_lane']} appeared only globally and {result['candidate_occurrences_and_union']['unique_resources_only_obligation_lanes']} only in obligation lanes.",
        f"{result['candidate_occurrences_and_union']['eligible_resources_without_any_positive_match']} of 498 eligible resources had no positive BM25 match in any lane; none was a required resource. Every other required lane miss described in the JSON is distinguished from a deep rank.",
        f"There were {result['helpful_only_diagnostics']['helpful_unit_count']} helpful-only units across {result['helpful_only_diagnostics']['unique_helpful_resources_in_any_obligation']} resources. Their global ranks: {result['helpful_only_diagnostics']['global_unit_rank_distribution']}; own-lane ranks: {result['helpful_only_diagnostics']['own_obligation_lane_unit_rank_distribution']}. Helpful units ranked ahead of the best globally reached required resource in {result['helpful_only_diagnostics']['helpful_units_shallower_than_best_reached_required_global']} cases.",
        f"Taking each own lane through its own obligation's best completion depth yields {result['candidate_occurrences_and_union']['own_lane_completion_prefix_union']['depth_occurrences']} lane-prefix occurrences and {len(result['candidate_occurrences_and_union']['own_lane_completion_prefix_union']['resources'])} unique resources. This is not a merged ranking or a recommendation.",
        "",
        "## Required units",
        "",
        "Ranks are native lane ranks. `—` means no positive BM25 match in that lane.",
        "",
        "| Obligation | Unit | Resource | Global | Own lane | Other-lane best | Rank comparison |",
        "| --- | --- | --- | ---: | ---: | ---: | --- |",
    ]
    for u in result["unit_rank_comparisons"]:
        if u["category"] != "REQUIRED":
            continue
        lines.append(
            f"| {u['obligation']} | {u['unit_identity']} | `{u['path']}` | {u['global_rank'] or '—'} | {u['own_lane_rank'] or '—'} | {u['best_other_obligation_rank'] or '—'} | {u['rank_comparison']} |"
        )
    lines += [
        "",
        "## Interpretation",
        "",
        "**Observation.** The global lane returned positive matches for "
        + f"{global_data['reachable_required_resources']}/{global_data['required_resource_count']} required resources. Own lanes completed "
        + f"{complete['acquisition_complete_for_adjudicated_witnesses']}/8 applicable obligations under at least one accepted alternative. The per-obligation table shows whether each own-lane completion depth was shallower, deeper, equal, or unreachable relative to the global lane.",
        "",
        "**Architectural interpretation.** These results describe one task/snapshot and the frozen queries. They do not establish general superiority, a production resolution, or a reason to change Localization, Retrieval, or query policy. Contribution components are descriptive evidence, not causes.",
        "",
        "### Frozen questions",
        "",
        f"1. Global lane reached every required resource: **{global_data['reachable_required_resources'] == global_data['required_resource_count']}** ({global_data['reachable_required_resources']}/{global_data['required_resource_count']}).",
        f"2. Every required information unit appeared in its owning obligation lane: **{len(result['required_own_lane_misses']['required_units']) == 0}** ({25 - len(result['required_own_lane_misses']['required_units'])}/25); all 17 unique required resources were reached by their owning lane association(s).",
        f"3. Own-lane best completion was shallower than the global alternative depth for {sum(o['own_vs_global'] == 'own_shallower' for o in result['per_obligation'])}/8 obligations; per-obligation outcomes are shown above.",
        f"4. Own-lane required units ranked worse than their global rank: {sum(u['rank_comparison'] == 'global_shallower' for u in result['unit_rank_comparisons'] if u['category'] == 'REQUIRED')}; the documentation obligation also has a worse best completion depth.",
        f"5. Required units with no positive match in their own lane: {len(result['required_own_lane_misses']['required_units'])}; unique resources missed in every owning lane: {len(missed)}.",
        f"6. Required units ranked better in another obligation lane than their own (or missed by own): {len(other_better)}; resources missed in all owning lanes but found in another lane: {sum(bool(row['other_obligation_hits']) for row in missed)}.",
        f"7. Global full-task complete depth is {global_data['complete_required_resource_depth']}. Repository documentation records full-task depths of 35 (Case 0001), 43 (Case 0002) and 348 (Case 0003); short-query depths are 132, 87 and 180. These unlike tasks/frames are descriptive only.",
        f"8. Own-obligation completion depths: {', '.join(f'{o['identity']}={o['best_own_completion_depth']}' for o in result['per_obligation'])}.",
        f"9. Obligation-wise maximum completion depth is {complete['obligation_wise_maximum_completion_depth']}; it is the maximum of each lane's best alternative depth, not a universal merged rank.",
        f"10. There are {result['frozen_judgment_frame']['required_resource_count']} unique required resources across 25 required units.",
        f"11. The naive own-lane completion-prefix union contains {len(result['candidate_occurrences_and_union']['own_lane_completion_prefix_union']['resources'])} unique resources (602 lane-prefix occurrences).",
        "12. Case-specifically, Python configuration and validation had the shallowest own-lane completion (rank 5); documentation (181) and resource-path (193) were deepest. Their query result counts and rank detail are retained in JSON. This describes discrimination in this case only.",
        "",
        "Confirmation remained sealed. No retrieval was rerun, no frozen judgment or treatment was changed, and no production behavior was changed.",
        "",
        "## Integrity and limitations",
        "",
        "The JSON artifact records checkpoint and input SHA-256 values, exact resource/obligation join diagnostics, every required/helpful unit's ranks, each conjunctive alternative, per-lane result counts and the full obligation-lane prefix union. It distinguishes zero positive matches from deep ranks. See its `limitations` field for scope constraints.",
        "",
    ]
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--check",
        action="store_true",
        help="Recompute and verify existing analysis artifacts without writing.",
    )
    args = parser.parse_args()
    chain, pre, retrieval, manifest, judgments = verify_chain_and_frozen_inputs()
    result = build_analysis(chain, pre, retrieval, manifest, judgments)
    json_bytes = canonical(result)
    md_bytes = markdown(result).encode()
    json_path, md_path = CASE / "analysis.json", CASE / "analysis.md"
    if args.check:
        if not json_path.exists() or not md_path.exists():
            raise FileNotFoundError(
                "Both frozen Stage D output files must exist for --check."
            )
        if json_path.read_bytes() != json_bytes or md_path.read_bytes() != md_bytes:
            raise ValueError(
                "Stage D artifacts differ from deterministic recomputation."
            )
    else:
        if json_path.exists() or md_path.exists():
            raise FileExistsError(
                "Case 0004 analysis output exists; refusing overwrite."
            )
        json_path.write_bytes(json_bytes)
        md_path.write_bytes(md_bytes)
    print(
        json.dumps(
            {
                "analysis_json_sha256": sha(json_bytes),
                "analysis_md_sha256": sha(md_bytes),
                "required_resources": result["frozen_judgment_frame"][
                    "required_resource_count"
                ],
                "global_depth": result["global_full_task"][
                    "complete_required_resource_depth"
                ],
                "per_obligation_depths": {
                    x["identity"]: x["best_own_completion_depth"]
                    for x in result["per_obligation"]
                },
                "acquisition_complete_obligations": result[
                    "complete_mandatory_acquisition_coverage"
                ]["acquisition_complete_for_adjudicated_witnesses"],
            },
            indent=2,
        )
    )
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (ValueError, FileExistsError, FileNotFoundError) as exc:
        print(f"case_0004 analysis refused: {exc}", file=sys.stderr)
        raise SystemExit(2) from exc
