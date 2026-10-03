# Copyright (c) 2026
# ruff: noqa: ANN001, ANN201, D103, INP001, S101, PLR2004, C901, PLR0912, PLR0915, E501
"""Case 0005 Stage D: deterministic join of frozen treatment and blind gold.

This script reads retained artifacts. It never invokes acquisition or routing.
Use --write once; --check recomputes and compares exact existing outputs.
"""

from __future__ import annotations

import argparse
import gzip
import hashlib
import itertools
import json
import pickle
import statistics
import subprocess
import sys
from collections import Counter
from pathlib import Path

CASE = Path(__file__).resolve().parent
ROOT = CASE.parents[2]
sys.path.insert(0, str(ROOT / "src"))

from devtools.context.repository.resource import RepositoryResourceAddress  # noqa: E402
from devtools.evaluation.coverage import compare_identity_coverage  # noqa: E402

STAGES = {
    "A": "e9764cde6dc6c2f379e4b08561974cd6b59c30d3",
    "B": "c233625dc2d0714ffda2b0b88df8cd73e22ea144",
    "B.5": "1643c567c095b6bb3355dd265181b59bc978bf2e",
    "C": "28330bb3a3424fca6bbf5ddc0b12be39f50089e8",
}
PINNED = {
    "treatment.json": "0e9e4cee88e660c04d5d5542449e4a304dd3a95919f09671e043c764810cde2d",
    "pre_retrieval.json": "640ca317683b9e956755716b6d4d5add949813e6f582788a6e0751f9fd68d3ef",
    "inputs.pkl.gz": "9e9c663b71a8579e63956b89737b707acc5282a7909f1f79ea7c1b4751fd0d3b",
    "capture.pkl.gz": "92bd11162fc11ddc75af6e6535c10eadd50bf62701f44100e049d37353cd315a",
    "retrieval.json": "b234079844a6d4f46793c08730c7c577213c003fadbcb511793272c8ce1ddd67",
    "routing.json": "315836a83a12f5ffe263ad238796f4e2dd8fa82680752b6720bb2ac2e4a794dd",
    "adjudication/blind_manifest.json": "c3d6455d09bcd53beec75c7d325489096f3b4a44c8b2aa6c4266233d93ca1177",
    "adjudication/blind_resources.json.gz": "01c786e7c74ae72ffd93e6d861fb080fb613d941788d0c6ea987c2dcb67889b7",
    "adjudication/judgments.json": "78ded9af961e780a7db7563275452582e9db49ad48da3883cc23028d4c251879",
}
SURFACES = ("global", "native", "routed")
LABELS = ("REQUIRED", "HELPFUL_ONLY", "UNNECESSARY", "UNRESOLVED")


def sha(data: bytes) -> str:
    """Hash exact artifact or canonical lane bytes."""
    return hashlib.sha256(data).hexdigest()


def canonical(value) -> bytes:
    """Match the frozen Stage B lane-reference serialization."""
    return (json.dumps(value, ensure_ascii=True, indent=2) + "\n").encode()


def output_json(value) -> bytes:
    """Serialize analysis deterministically."""
    return (
        json.dumps(value, ensure_ascii=True, indent=2, sort_keys=True) + "\n"
    ).encode()


def git(*args: str) -> str:
    """Read Git identity without changing a checkout or index."""
    return (
        subprocess.check_output(  # noqa: S603 -- fixed read-only Git calls
            ["git", *args],  # noqa: S607
            cwd=ROOT,
        )
        .decode()
        .strip()
    )


def verify_frozen():
    """Reject drift in every frozen input and its committed stage lineage."""
    assert git("merge-base", STAGES["C"], "HEAD") == STAGES["C"]
    for stage, commit in STAGES.items():
        assert git("rev-parse", commit) == commit, stage
    chain = list(STAGES.values())
    for parent, child in itertools.pairwise(chain):
        assert git("rev-parse", f"{child}^") == parent
    assert git("branch", "--show-current") == "main"
    assert not git("status", "--porcelain=v1", "--untracked-files=no")
    for relative, expected in PINNED.items():
        assert sha((CASE / relative).read_bytes()) == expected, relative
    integrity = json.loads((CASE / "integrity.json").read_bytes())
    for relative, expected in integrity.items():
        assert sha((CASE / relative).read_bytes()) == expected, relative
    assert (
        sha((CASE / "adjudication/judgments.json").read_bytes())
        == ((CASE / "adjudication/judgments.sha256").read_text().split()[0])
    )
    stage_owner = {
        "A": [*integrity, "integrity.json"],
        "B": ["capture.pkl.gz", "retrieval.json", "routing.json"],
        "B.5": [
            "adjudication/blind_manifest.json",
            "adjudication/blind_resources.json.gz",
        ],
        "C": ["adjudication/judgments.json"],
    }
    for stage, files in stage_owner.items():
        for relative in files:
            path = f"experiments/codex_dogfood/case_0005/{relative}"
            assert git("rev-parse", f"{STAGES[stage]}:{path}") == git(
                "rev-parse", f"{STAGES['C']}:{path}"
            ), (stage, relative)
    return {name: sha((CASE / name).read_bytes()) for name in PINNED}


def load():
    """Load retained objects only after the integrity barrier."""
    hashes = verify_frozen()
    items = {
        name: json.loads((CASE / name).read_bytes())
        for name in (
            "treatment.json",
            "pre_retrieval.json",
            "retrieval.json",
            "routing.json",
            "adjudication/blind_manifest.json",
            "adjudication/judgments.json",
        )
    }
    # This verified local pickle retains the full positive role inventory needed
    # to diagnose escape, including roles not selected by caller preferences.
    items["capture"] = pickle.loads(  # noqa: S301
        gzip.decompress((CASE / "capture.pkl.gz").read_bytes())
    )
    items["hashes"] = hashes
    return items


def identity_key(identity: dict) -> str:
    """Use exact resource identity, including repository and snapshot."""
    return json.dumps(identity, sort_keys=True, separators=(",", ":"))


def coverage(expected, observed, label: str) -> dict:
    """Use Evaluation only for identity presence mechanics."""
    result = compare_identity_coverage(expected=expected, observed=observed)
    summary = {
        "expected": len(expected),
        "observed": len(observed),
        "duplicate_expected": list(result.duplicate_expected),
        "duplicate_observed": list(result.duplicate_observed),
        "missing": list(result.missing),
        "unexpected": list(result.unexpected),
    }
    assert result.is_exact, (label, summary)
    return summary


def check_join(items):
    """Prove all frames, lanes, candidates, preferences and global preservation."""
    t, p, r, v = (
        items[k]
        for k in (
            "treatment.json",
            "pre_retrieval.json",
            "retrieval.json",
            "routing.json",
        )
    )
    b, j, c = (
        items[k]
        for k in (
            "adjudication/blind_manifest.json",
            "adjudication/judgments.json",
            "capture",
        )
    )
    assert all(x["case"] == "case_0005" for x in (t, p, r, v, b, j, c))
    assert len({x["task_identity"] for x in (t, p, r, v, b, j)}) == 1
    assert (
        t["task_full_prompt"]
        == p["task_full_prompt"]
        == b["task_text"]
        == j["task_text"]
    )
    assert len({x["purpose"] for x in (t, p, r, b, j)}) == 1
    assert len({x["repository_id"] for x in (p, r, v, b, j)}) == 1
    assert len({x["snapshot_id"] for x in (p, r, v, b, j)}) == 1
    frame = p["eligible_corpus_id"]
    assert frame == b["eligible_frame_identity"] == j["eligible_frame_identity"]
    assert frame == r["corpus_id"] == v["corpus_id"]
    assert len(p["eligible_resources"]) == b["eligible_resource_count"] == 515
    assert len(j["resource_obligation_judgments"]) == 4635
    assert r["stage_a_commit"] == v["stage_a_commit"] == STAGES["A"]
    assert (
        r["stage_a_manifest_sha256"]
        == v["stage_a_manifest_sha256"]
        == items["hashes"]["pre_retrieval.json"]
    )
    assert (
        r["stage_a_inputs_sha256"]
        == v["stage_a_inputs_sha256"]
        == items["hashes"]["inputs.pkl.gz"]
    )
    assert r["capture_sha256"] == items["hashes"]["capture.pkl.gz"]
    assert v["retrieval_sha256"] == items["hashes"]["retrieval.json"]
    assert (
        v["role_derivation_identity"]
        == p["role_derivation"]["identity"]
        == c["role_evidence"].derivation_identity
    )
    assert v["routing_policy_identity"] == t["routing"]["identity"]
    assert c["invocation_counts"] == {"acquisition": 1, "routing": 1}

    frame_addresses = [x["address"] for x in p["eligible_resources"]]
    frame_by_address = {x["address"]: x for x in p["eligible_resources"]}
    assert len(frame_by_address) == 515
    blind_resources = json.loads(
        gzip.decompress((CASE / "adjudication/blind_resources.json.gz").read_bytes())
    )["resources"]
    frame_coverage = coverage(
        frame_addresses, [x["address"] for x in blind_resources], "blind frame"
    )
    frame_coverage = {
        **frame_coverage,
        "native_role_view_resources": len(c["role_evidence"].resources),
    }
    assert coverage(
        frame_addresses,
        [x.address.value for x in c["role_evidence"].resources],
        "role frame",
    )
    assert c["role_evidence"].repository_id.__str__() == p["repository_id"]
    assert c["role_evidence"].snapshot_id.__str__() == p["snapshot_id"]
    for resource in blind_resources:
        original = frame_by_address[resource["address"]]
        assert resource["content_identity"] == original["content_identity"]
        assert resource["repository_id"] == p["repository_id"]
        assert resource["snapshot_id"] == p["snapshot_id"]
    frame_ids = [identity_key(x["resource_identity"]) for x in blind_resources]
    obligations = [x["identity"] for x in t["obligations"]]
    assert len(obligations) == 9
    obligation_join = coverage(
        obligations, [x["identity"] for x in b["obligations"]], "blind obligations"
    )
    assert coverage(
        obligations,
        [x["frozen_obligation"]["identity"] for x in j["obligations"]],
        "judgments",
    )
    assert coverage(
        obligations,
        [x["obligation_identity"] for x in r["lanes"][1:]],
        "retrieval obligations",
    )
    assert coverage(
        obligations,
        [x["obligation_identity"] for x in v["lanes"]],
        "routing obligations",
    )
    for frozen, gold in zip(b["obligations"], j["obligations"], strict=True):
        assert frozen == gold["frozen_obligation"]
        assert gold["applicability"] == "APPLICABLE"
        assert not gold["unresolved_judgments"]
    queries = [x["identity"] for x in t["obligation_queries"]]
    assert len(queries) == 9
    query_join = coverage(
        queries, [x["query_identity"] for x in r["lanes"][1:]], "retrieval queries"
    )
    assert coverage(
        queries, [x["query_identity"] for x in v["lanes"]], "routing queries"
    )
    assert coverage(
        queries, [x.query.value for x in c["preferences"]], "capture preferences"
    )
    assert len(v["lanes"]) == v["routed_lane_count"] == 9
    assert len(r["lanes"]) == r["lane_count"] == 10
    assert r["global_lane_reference"] == "global-full-task"
    assert not v["global_lane_routed"]
    assert v["global_lane_reference"] == sha(canonical(r["lanes"][0]))
    assert r["lanes"][0]["query_identity"] == "global-full-task"
    assert r["lanes"][0]["query_text"] == t["task_full_prompt"]
    assert r["lanes"][0]["result_count"] == len(r["lanes"][0]["matches"])
    assert c["routed"].global_retrieval is c["acquisition"].full_task_retrieval
    global_addresses = [x["resource_address"] for x in r["lanes"][0]["matches"]]
    assert len(global_addresses) == len(set(global_addresses))
    for rank, match in enumerate(r["lanes"][0]["matches"], 1):
        assert match["native_rank"] == rank
        assert match["resource_address"] in frame_by_address
        assert match["resource_identity"]["repository_id"] == p["repository_id"]
        assert match["resource_identity"]["snapshot_id"] == p["snapshot_id"]
        assert (
            match["resource_identity"]["content_identity"]
            == frame_by_address[match["resource_address"]]["content_identity"]
        )
    for requested, native, routed, pref in zip(
        t["obligation_queries"],
        r["lanes"][1:],
        v["lanes"],
        c["preferences"],
        strict=True,
    ):
        assert (
            requested["identity"]
            == native["query_identity"]
            == routed["query_identity"]
            == pref.query.value
        )
        assert (
            requested["obligation"]
            == native["obligation_identity"]
            == routed["obligation_identity"]
            == pref.obligation.value
        )
        assert requested["text"] == native["query_text"]
        assert (
            requested["preferred_roles"]
            == routed["preferred_roles"]
            == [x.name for x in pref.preferred_roles]
        )
        assert routed["preference_query_identity"] == requested["identity"]
        assert routed["preference_obligation_identity"] == requested["obligation"]
        assert routed["native_result_reference"] == sha(canonical(native))
        assert (
            native["result_count"]
            == routed["native_result_count"]
            == len(native["matches"])
        )
        assert (
            len(routed["candidates"])
            == routed["preferred_count"] + routed["escape_count"]
        )
        seen = []
        for position, candidate in enumerate(routed["candidates"], 1):
            rank = candidate["native_rank"]
            assert 1 <= rank <= len(native["matches"])
            original = native["matches"][rank - 1]
            assert candidate["routed_position"] == position
            assert candidate["resource_address"] == original["resource_address"]
            assert candidate["content_identity"] == original["content_identity"]
            assert original["native_rank"] == rank
            assert original["resource_identity"]["address"] in frame_by_address
            assert (
                original["resource_identity"]["content_identity"]
                == frame_by_address[original["resource_address"]]["content_identity"]
            )
            assert original["resource_identity"]["repository_id"] == p["repository_id"]
            assert original["resource_identity"]["snapshot_id"] == p["snapshot_id"]
            # Verify positive support payloads without invoking the router.
            available = c["role_evidence"].for_resource(
                RepositoryResourceAddress(original["resource_identity"]["address"])
            )
            selected = [
                x for role in pref.preferred_roles for x in available if x.role == role
            ]
            assert candidate["matching_preferred_roles"] == [
                x.role.name for x in selected
            ]
            assert len(candidate["role_evidence"]) == len(selected)
            for payload, source in zip(
                candidate["role_evidence"], selected, strict=True
            ):
                assert payload["identity"] == source.identity
                assert payload["role"] == source.role.name
                assert payload["resource_address"] == source.resource.address.value
                assert (
                    payload["content_identity"]
                    == source.resource.content_identity.value
                )
                assert payload["supports"] == [
                    {
                        "identity": s.identity,
                        "kind": s.kind.value,
                        "source_address": s.source_address.value,
                        "native_identities": list(s.native_identities),
                        "observation": list(s.observation),
                    }
                    for s in source.supports
                ]
            assert candidate["tier"] == (
                "PREFERRED_ROLE_SUPPORTED" if selected else "ESCAPE"
            )
            seen.append(candidate["resource_address"])
        assert len(seen) == len(set(seen)) == len(native["matches"])
        assert set(seen) == {x["resource_address"] for x in native["matches"]}
        assert all(
            x["tier"] == "PREFERRED_ROLE_SUPPORTED"
            for x in routed["candidates"][: routed["preferred_count"]]
        )
        assert all(
            x["tier"] == "ESCAPE"
            for x in routed["candidates"][routed["preferred_count"] :]
        )
        if not requested["preferred_roles"]:
            assert [x["resource_address"] for x in routed["candidates"]] == [
                x["resource_address"] for x in native["matches"]
            ]
            assert all(
                x["routed_position"] == x["native_rank"] for x in routed["candidates"]
            )
    cells = j["resource_obligation_judgments"]
    expected_cells = [(o, x) for o in obligations for x in frame_ids]
    observed_cells = [
        (x["obligation_identity"], identity_key(x["resource_identity"])) for x in cells
    ]
    judgment_coverage = coverage(expected_cells, observed_cells, "gold cells")
    assert all(x["judgment"] in LABELS for x in cells)
    assert not any(x["judgment"] == "UNRESOLVED" for x in cells)
    return {
        "frame": frame_coverage,
        "obligations": obligation_join,
        "queries_and_preferences": query_join,
        "judgments": judgment_coverage,
        "global_lane_unchanged": True,
        "routed_candidate_loss": 0,
        "empty_preference_exact_order": True,
    }


def label_map(j):
    """Index frozen obligation-relative cell labels by canonical address."""
    labels = {}
    for cell in j["resource_obligation_judgments"]:
        labels[cell["obligation_identity"], cell["resource_identity"]["address"]] = (
            cell["judgment"]
        )
    return labels


def distribution(values):
    """Report reached ranks without inventing a relevance score."""
    if not values:
        return {"count": 0, "minimum": None, "median": None, "maximum": None}
    return {
        "count": len(values),
        "minimum": min(values),
        "median": statistics.median(values),
        "maximum": max(values),
    }


def prefix(lane, depth, labels, obligation, field):
    """Count actual ordered prefix candidates and retain exact addresses."""
    if depth is None:
        return None
    entries = [x for x in lane if x[field] <= depth]
    assert len(entries) == depth
    counts = Counter(labels[obligation, x["resource_address"]] for x in entries)
    return {
        "depth": depth,
        "candidate_occurrences": len(entries),
        "resources": [x["resource_address"] for x in entries],
        "labels": {k: counts[k] for k in LABELS},
    }


def basis_group(kind: str) -> str:  # noqa: PLR0911
    """Group native support kinds for descriptive diagnostics only."""
    if kind in {
        "python-suffix-convention",
        "test-directory-convention",
        "initializer-name-convention",
        "markdown-suffix-convention",
        "documentation-directory-convention",
        "readme-name-convention",
        "pyproject-name-convention",
    }:
        return "path_or_name_convention"
    if kind in {"pytest-testpath-target", "pytest-basename-glob"}:
        return "configured_testpath_or_filename_pattern"
    if kind in {"module-interpretation", "package-interpretation"}:
        return "module_or_package_interpretation"
    if kind == "package-membership":
        return "package_membership"
    if kind == "mirrored-test-path":
        return "mirrored_test_path"
    if kind in {
        "project-declaration",
        "build-declaration",
        "pytest-declaration",
        "tool-table",
        "tool-declaration",
        "readme-target",
    }:
        return "project_configuration_or_target"
    return "other_" + kind


def support_kinds(candidate):
    """Deduplicate bases per candidate so repeated supports are not extra votes."""
    return sorted(
        {s["kind"] for e in candidate["role_evidence"] for s in e["supports"]}
    )


def escape_reason(address, preferred, role_view):
    """Diagnose a required escape using the complete frozen positive role view."""
    all_roles = role_view.for_resource(RepositoryResourceAddress(address))
    names = sorted({x.role.name for x in all_roles})
    if not preferred:
        category = "EMPTY_CALLER_PREFERENCE_CONTROL"
        target = "caller preference (deliberately empty control)"
    elif not names:
        category = "NO_POSITIVE_ROLE_EVIDENCE"
        target = "role derivation or vocabulary"
    elif not set(names).intersection(preferred):
        category = (
            "CROSS_ROLE_REQUIRED_INFORMATION"
            if ("DOCUMENTATION" in names and "PYTHON_CODE" in preferred)
            else "POSITIVE_ROLE_PREFERENCE_MISMATCH"
        )
        target = (
            "evidence-to-witness reasoning across roles"
            if category.startswith("CROSS")
            else "caller preference or role vocabulary"
        )
    else:
        msg = "Supported preferred role cannot be escape"
        raise AssertionError(msg)
    return {
        "category": category,
        "all_positive_roles": names,
        "caller_preferred_roles": preferred,
        "diagnostic_target": target,
        "all_support_kinds": sorted(
            {s.kind.value for e in all_roles for s in e.supports}
        ),
    }


def analyze(items):
    """Compute alternative-aware three-surface measures from retained JSON."""
    integrity = check_join(items)
    t, r, v, j, capture = (
        items[k]
        for k in (
            "treatment.json",
            "retrieval.json",
            "routing.json",
            "adjudication/judgments.json",
            "capture",
        )
    )
    labels = label_map(j)
    units = {x["identity"]: x for x in j["information_units"]}
    global_lane = r["lanes"][0]
    global_by = {x["resource_address"]: x for x in global_lane["matches"]}
    native_by_obligation = {x["obligation_identity"]: x for x in r["lanes"][1:]}
    routed_by_obligation = {x["obligation_identity"]: x for x in v["lanes"]}
    all_required_addresses = {
        u["resource_identity"]["address"]
        for o in j["obligations"]
        for record in o["information_unit_judgments"]
        for u in [units[record["unit_identity"]]]
    }
    assert len(all_required_addresses) == 24
    assert len(units) == 25
    assert sum(len(o["information_unit_judgments"]) for o in j["obligations"]) == 27
    assert all(
        x["inferability"] == "INFERABLE_AT_START"
        for o in j["obligations"]
        for x in o["information_unit_judgments"]
    )
    assert not j["task_interpretation_gaps"]["findings"]

    result_obligations = []
    required_occurrences = []
    promoted_bases = {
        "REQUIRED": Counter(),
        "UNNECESSARY": Counter(),
        "HELPFUL_ONLY": Counter(),
    }
    promoted_groups = {x: Counter() for x in promoted_bases}
    all_combinations = []
    for ob in j["obligations"]:
        alternatives = [
            {
                "identity": alt["identity"],
                "units": alt["all_members"],
                "resources": sorted(
                    {
                        units[k]["resource_identity"]["address"]
                        for k in alt["all_members"]
                    }
                ),
            }
            for alt in ob["acceptable_witness_alternatives"]
        ]
        all_combinations.append(alternatives)
    combinations = []
    for choice in itertools.product(*all_combinations):
        union = sorted({a for alt in choice for a in alt["resources"]})
        combinations.append(
            {
                "alternative_ids": [x["identity"] for x in choice],
                "resource_count": len(union),
                "resources": union,
            }
        )
    minimum = min(x["resource_count"] for x in combinations)
    sufficient = [x for x in combinations if x["resource_count"] == minimum]

    for ob in j["obligations"]:
        oid = ob["frozen_obligation"]["identity"]
        native = native_by_obligation[oid]
        routed = routed_by_obligation[oid]
        by_native = {x["resource_address"]: x for x in native["matches"]}
        by_routed = {x["resource_address"]: x for x in routed["candidates"]}
        required = [units[x["unit_identity"]] for x in ob["information_unit_judgments"]]
        required_addresses = sorted(
            {x["resource_identity"]["address"] for x in required}
        )
        assert len(required) == len(required_addresses)
        alternative_metrics = []
        for alt in ob["acceptable_witness_alternatives"]:
            addresses = sorted(
                {units[x]["resource_identity"]["address"] for x in alt["all_members"]}
            )
            positions = {"global": global_by, "native": by_native, "routed": by_routed}
            depths = {}
            for surface, index in positions.items():
                field = "routed_position" if surface == "routed" else "native_rank"
                depths[surface] = (
                    max(index[a][field] for a in addresses)
                    if all(a in index for a in addresses)
                    else None
                )
            alternative_metrics.append(
                {
                    "identity": alt["identity"],
                    "units": alt["all_members"],
                    "resources": addresses,
                    "completion": depths,
                    "all_preferred": all(
                        by_routed[a]["tier"] == "PREFERRED_ROLE_SUPPORTED"
                        for a in addresses
                        if a in by_routed
                    )
                    and all(a in by_routed for a in addresses),
                    "depends_on_escape": any(
                        by_routed[a]["tier"] == "ESCAPE"
                        for a in addresses
                        if a in by_routed
                    ),
                    "unreachable_resources": {
                        s: [a for a in addresses if a not in index]
                        for s, index in positions.items()
                    },
                }
            )
        choices = {}
        for surface in SURFACES:
            eligible = [
                x for x in alternative_metrics if x["completion"][surface] is not None
            ]
            choices[surface] = (
                min(eligible, key=lambda x: x["completion"][surface])
                if eligible
                else None
            )
        best = {
            s: choices[s]["completion"][s] if choices[s] else None for s in SURFACES
        }
        native_prefix = prefix(
            native["matches"], best["native"], labels, oid, "native_rank"
        )
        routed_prefix = prefix(
            routed["candidates"], best["routed"], labels, oid, "routed_position"
        )
        tier_counts = Counter(x["tier"] for x in routed["candidates"])
        preferred = [
            x for x in routed["candidates"] if x["tier"] == "PREFERRED_ROLE_SUPPORTED"
        ]
        preferred_labels = Counter(
            labels[oid, x["resource_address"]] for x in preferred
        )
        required_tiers = Counter(
            by_routed[a]["tier"] if a in by_routed else "MISSING"
            for a in required_addresses
        )
        selected_addresses = (
            set(choices["routed"]["resources"]) if choices["routed"] else set()
        )
        selected_preferred = sum(
            a in selected_addresses
            and by_routed.get(a, {}).get("tier") == "PREFERRED_ROLE_SUPPORTED"
            for a in selected_addresses
        )
        useful_examples = []
        unnecessary_examples = []
        for cand in preferred:
            if cand["routed_position"] >= cand["native_rank"]:
                continue
            label = labels[oid, cand["resource_address"]]
            kinds = support_kinds(cand)
            for kind in kinds:
                promoted_bases[label][kind] += 1
                promoted_groups[label][basis_group(kind)] += 1
            example = {
                "obligation": oid,
                "address": cand["resource_address"],
                "native_rank": cand["native_rank"],
                "routed_position": cand["routed_position"],
                "kinds": kinds,
            }
            if label == "REQUIRED":
                useful_examples.append(example)
            elif label == "UNNECESSARY":
                unnecessary_examples.append(example)
        for record in ob["information_unit_judgments"]:
            uid = record["unit_identity"]
            address = units[uid]["resource_identity"]["address"]
            g, n, rr = (
                global_by.get(address),
                by_native.get(address),
                by_routed.get(address),
            )
            global_rank = g["native_rank"] if g else None
            native_rank = n["native_rank"] if n else None
            routed_position = rr["routed_position"] if rr else None
            if global_rank is None and native_rank is None:
                decomp = "neither_reaches"
            elif global_rank is None or native_rank is None:
                decomp = "only_own_reaches" if native_rank else "only_global_reaches"
            elif native_rank < global_rank:
                decomp = "own_native_shallower"
            elif native_rank > global_rank:
                decomp = "global_shallower"
            else:
                decomp = "equal"
            route_change = (
                "unreachable"
                if rr is None
                else (
                    "routed_earlier"
                    if routed_position < native_rank
                    else "routed_later"
                    if routed_position > native_rank
                    else "unchanged"
                )
            )
            escape = (
                escape_reason(
                    address, routed["preferred_roles"], capture["role_evidence"]
                )
                if rr and rr["tier"] == "ESCAPE"
                else None
            )
            required_occurrences.append(
                {
                    "obligation": oid,
                    "unit": uid,
                    "resource": address,
                    "global_native_rank": global_rank,
                    "own_native_rank": native_rank,
                    "own_routed_position": routed_position,
                    "tier": rr["tier"] if rr else "MISSING",
                    "matching_preferred_roles": rr["matching_preferred_roles"]
                    if rr
                    else [],
                    "selected_support_kinds": support_kinds(rr) if rr else [],
                    "selected_role_supports": [
                        {
                            "role": e["role"],
                            "evidence_identity": e["identity"],
                            "supports": [
                                {
                                    "identity": s["identity"],
                                    "kind": s["kind"],
                                    "source_address": s["source_address"],
                                    "native_identities": s["native_identities"],
                                }
                                for s in e["supports"]
                            ],
                        }
                        for e in rr["role_evidence"]
                    ]
                    if rr
                    else [],
                    "all_positive_roles": sorted(
                        {
                            x.role.name
                            for x in capture["role_evidence"].for_resource(
                                RepositoryResourceAddress(address)
                            )
                        }
                    ),
                    "decomposition_effect": decomp,
                    "routing_effect": route_change,
                    "escape_diagnosis": escape,
                }
            )
        helpful_addresses = [
            a
            for (o, a), label in labels.items()
            if o == oid and label == "HELPFUL_ONLY"
        ]
        helpful_native = [
            by_native[a]["native_rank"] for a in helpful_addresses if a in by_native
        ]
        helpful_routed = [
            by_routed[a]["routed_position"] for a in helpful_addresses if a in by_routed
        ]
        helpful_global = [
            global_by[a]["native_rank"] for a in helpful_addresses if a in global_by
        ]
        result_obligations.append(
            {
                "identity": oid,
                "query_identity": native["query_identity"],
                "preferred_roles": routed["preferred_roles"],
                "required_unit_occurrences": len(required),
                "required_resource_universe": required_addresses,
                "alternatives": alternative_metrics,
                "best_alternatives": {
                    s: choices[s]["identity"] if choices[s] else None for s in SURFACES
                },
                "best_completion": best,
                "native_prefix": native_prefix,
                "routed_prefix": routed_prefix,
                "prefix_occurrence_change": routed_prefix["candidate_occurrences"]
                - native_prefix["candidate_occurrences"]
                if native_prefix and routed_prefix
                else None,
                "tier_sizes": {
                    "preferred": tier_counts["PREFERRED_ROLE_SUPPORTED"],
                    "escape": tier_counts["ESCAPE"],
                },
                "required_tiers": {
                    "preferred": required_tiers["PREFERRED_ROLE_SUPPORTED"],
                    "escape": required_tiers["ESCAPE"],
                    "missing": required_tiers["MISSING"],
                },
                "preferred_tier_labels": {k: preferred_labels[k] for k in LABELS},
                "preferred_quality": {
                    "required_precision_all_alternatives": preferred_labels["REQUIRED"]
                    / len(preferred)
                    if preferred
                    else None,
                    "required_recall_all_alternatives": required_tiers[
                        "PREFERRED_ROLE_SUPPORTED"
                    ]
                    / len(required_addresses),
                    "required_precision_best_routed_alternative": selected_preferred
                    / len(preferred)
                    if preferred
                    else None,
                    "required_recall_best_routed_alternative": selected_preferred
                    / len(selected_addresses)
                    if selected_addresses
                    else None,
                    "selected_required_preferred": selected_preferred,
                    "selected_required_total": len(selected_addresses),
                    "denominators": {
                        "preferred_tier": len(preferred),
                        "all_acceptable_required_resources": len(required_addresses),
                        "best_routed_alternative_resources": len(selected_addresses),
                    },
                },
                "helpful_only": {
                    "frame_resources": len(helpful_addresses),
                    "global_native_reached": distribution(helpful_global),
                    "own_native_reached": distribution(helpful_native),
                    "own_routed_reached": distribution(helpful_routed),
                    "preferred": sum(
                        by_routed[a]["tier"] == "PREFERRED_ROLE_SUPPORTED"
                        for a in helpful_addresses
                        if a in by_routed
                    ),
                    "escape": sum(
                        by_routed[a]["tier"] == "ESCAPE"
                        for a in helpful_addresses
                        if a in by_routed
                    ),
                    "native_ahead_of_completion": native_prefix["labels"][
                        "HELPFUL_ONLY"
                    ],
                    "routed_ahead_of_completion": routed_prefix["labels"][
                        "HELPFUL_ONLY"
                    ],
                },
                "useful_promotions": useful_examples,
                "unnecessary_promotions": unnecessary_examples,
                "alternative_changed_by_routing": choices["native"]["identity"]
                != choices["routed"]["identity"],
            }
        )
    reach = {
        "global_witness_universe": sum(a in global_by for a in all_required_addresses),
        "global_witness_universe_total": len(all_required_addresses),
        "global_required_unit_occurrences": sum(
            x["global_native_rank"] is not None for x in required_occurrences
        ),
        "own_native_required_unit_occurrences": sum(
            x["own_native_rank"] is not None for x in required_occurrences
        ),
        "own_routed_required_unit_occurrences": sum(
            x["own_routed_position"] is not None for x in required_occurrences
        ),
        "required_unit_occurrences_total": len(required_occurrences),
    }
    assert len(required_occurrences) == 27
    depths = {
        s: max(x["best_completion"][s] for x in result_obligations)
        if all(x["best_completion"][s] is not None for x in result_obligations)
        else None
        for s in SURFACES
    }
    universe_depth = (
        max(global_by[a]["native_rank"] for a in all_required_addresses)
        if reach["global_witness_universe"] == len(all_required_addresses)
        else None
    )
    native_prefixes = [x["native_prefix"] for x in result_obligations]
    routed_prefixes = [x["routed_prefix"] for x in result_obligations]
    native_union = sorted({a for x in native_prefixes for a in x["resources"]})
    routed_union = sorted({a for x in routed_prefixes for a in x["resources"]})
    native_sum = sum(x["candidate_occurrences"] for x in native_prefixes)
    routed_sum = sum(x["candidate_occurrences"] for x in routed_prefixes)
    aggregate_labels = {
        s: {label: sum(x["labels"][label] for x in prefixes) for label in LABELS}
        for s, prefixes in (("native", native_prefixes), ("routed", routed_prefixes))
    }
    required_unique_tiers = {
        tier: sorted({x["resource"] for x in required_occurrences if x["tier"] == tier})
        for tier in ("PREFERRED_ROLE_SUPPORTED", "ESCAPE", "MISSING")
    }
    cross = []
    for x in required_occurrences:
        own = x["obligation"]
        address = x["resource"]
        elsewhere = []
        for oid, lane in native_by_obligation.items():
            if oid == own:
                continue
            n = next(
                (c for c in lane["matches"] if c["resource_address"] == address), None
            )
            rr = next(
                (
                    c
                    for c in routed_by_obligation[oid]["candidates"]
                    if c["resource_address"] == address
                ),
                None,
            )
            if n:
                assert rr
                elsewhere.append(
                    {
                        "obligation": oid,
                        "native_rank": n["native_rank"],
                        "routed_position": rr["routed_position"],
                        "tier": rr["tier"],
                        "matching_preferred_roles": rr["matching_preferred_roles"],
                    }
                )
        better_native = (
            sorted(
                (e for e in elsewhere if e["native_rank"] < x["own_native_rank"]),
                key=lambda e: (e["native_rank"], e["obligation"]),
            )
            if x["own_native_rank"]
            else []
        )
        earlier_routed = (
            sorted(
                (
                    e
                    for e in elsewhere
                    if e["routed_position"] < x["own_routed_position"]
                ),
                key=lambda e: (e["routed_position"], e["obligation"]),
            )
            if x["own_routed_position"]
            else []
        )
        supported_elsewhere = [
            e
            for e in elsewhere
            if x["tier"] == "ESCAPE" and e["tier"] == "PREFERRED_ROLE_SUPPORTED"
        ]
        if better_native or earlier_routed or supported_elsewhere:
            cross.append(
                {
                    "obligation": own,
                    "unit": x["unit"],
                    "resource": address,
                    "better_native_other_lanes": better_native,
                    "earlier_routed_other_lanes": earlier_routed,
                    "preferred_elsewhere_while_own_escape": supported_elsewhere,
                }
            )
    optional = {
        "frame_helpful_cells": sum(
            x["judgment"] == "HELPFUL_ONLY" for x in j["resource_obligation_judgments"]
        ),
        "frame_helpful_unique_resources": len(
            {
                x["resource_identity"]["address"]
                for x in j["resource_obligation_judgments"]
                if x["judgment"] == "HELPFUL_ONLY"
            }
        ),
        "native_reached_helpful_occurrences": sum(
            x["helpful_only"]["own_native_reached"]["count"] for x in result_obligations
        ),
        "global_reached_helpful_occurrences": sum(
            x["helpful_only"]["global_native_reached"]["count"]
            for x in result_obligations
        ),
        "routed_preferred_helpful_occurrences": sum(
            x["helpful_only"]["preferred"] for x in result_obligations
        ),
        "routed_escape_helpful_occurrences": sum(
            x["helpful_only"]["escape"] for x in result_obligations
        ),
    }
    comparison = Counter(
        "improved"
        if x["best_completion"]["routed"] < x["best_completion"]["native"]
        else "worsened"
        if x["best_completion"]["routed"] > x["best_completion"]["native"]
        else "unchanged"
        for x in result_obligations
    )
    classifications = {
        label: [
            x["identity"]
            for x in result_obligations
            if (
                (x["best_completion"]["routed"] < x["best_completion"]["native"])
                if label == "improved"
                else (x["best_completion"]["routed"] > x["best_completion"]["native"])
                if label == "worsened"
                else (x["best_completion"]["routed"] == x["best_completion"]["native"])
            )
        ]
        for label in ("improved", "unchanged", "worsened")
    }
    return {
        "schema": "case-0005-stage-d-joined-analysis-v1",
        "case": "case_0005",
        "stage_c_head": STAGES["C"],
        "frozen_stage_commits": STAGES,
        "frozen_input_sha256": items["hashes"],
        "identity": {
            "task": t["task_identity"],
            "repository": j["repository_id"],
            "snapshot": j["snapshot_id"],
            "eligible_frame": j["eligible_frame_identity"],
        },
        "join_integrity": integrity,
        "semantics": {
            "alternative": "ALL members of one set; ANY complete set. Best alternative independently selected per surface, frozen order breaks ties.",
            "prefix": "Actual ordered own-lane candidates through that surface's best complete alternative; labels remain obligation-relative.",
            "precision": "Diagnostic required resources in preferred / all preferred candidates; required recall uses all acceptable required resources or the chosen best routed alternative as labelled. No threshold or probability.",
            "rank": "One-based native rank and one-based routed presentation position remain distinct.",
        },
        "required": {
            "unit_occurrences": len(required_occurrences),
            "distinct_units": len(units),
            "witness_universe_unique_resources": len(all_required_addresses),
            "witness_universe_resources": sorted(all_required_addresses),
            "minimum_semantically_sufficient_resource_union": minimum,
            "minimum_union_solutions": sufficient,
            "all_semantically_valid_combinations": combinations,
            "reach": reach,
            "occurrences": required_occurrences,
            "unique_resources_by_tier": required_unique_tiers,
            "occurrences_by_tier": dict(
                Counter(x["tier"] for x in required_occurrences)
            ),
            "decomposition_classifications": dict(
                Counter(x["decomposition_effect"] for x in required_occurrences)
            ),
            "routing_classifications": dict(
                Counter(x["routing_effect"] for x in required_occurrences)
            ),
            "escape_categories": dict(
                Counter(
                    x["escape_diagnosis"]["category"]
                    for x in required_occurrences
                    if x["escape_diagnosis"]
                )
            ),
        },
        "global": {
            "positive_matches": len(global_lane["matches"]),
            "witness_universe_resource_recall": reach["global_witness_universe"]
            / len(all_required_addresses),
            "required_unit_recall": reach["global_required_unit_occurrences"]
            / len(required_occurrences),
            "task_complete_obligation_depth": depths["global"],
            "complete_witness_universe_depth": universe_depth,
        },
        "own_lanes": {
            "maximum_native_completion_depth": depths["native"],
            "maximum_routed_completion_position": depths["routed"],
            "comparison": classifications,
            "comparison_counts": {k: comparison[k] for k in classifications},
            "obligations": result_obligations,
        },
        "review_surface": {
            "native_summed_occurrences": native_sum,
            "native_unique_resources": len(native_union),
            "native_resource_union": native_union,
            "routed_summed_occurrences": routed_sum,
            "routed_unique_resources": len(routed_union),
            "routed_resource_union": routed_union,
            "occurrence_change": routed_sum - native_sum,
            "occurrence_relative_change": (routed_sum - native_sum) / native_sum
            if native_sum
            else None,
            "unique_change": len(routed_union) - len(native_union),
            "unique_relative_change": (len(routed_union) - len(native_union))
            / len(native_union)
            if native_union
            else None,
            "both_unions": sorted(set(native_union) & set(routed_union)),
            "only_native_union": sorted(set(native_union) - set(routed_union)),
            "only_routed_union": sorted(set(routed_union) - set(native_union)),
            "native_over_sufficient_ratio": len(native_union) / minimum,
            "routed_over_sufficient_ratio": len(routed_union) / minimum,
            "native_excess_over_sufficient": len(native_union) - minimum,
            "routed_excess_over_sufficient": len(routed_union) - minimum,
            "prefix_label_totals": aggregate_labels,
        },
        "helpful_only": optional,
        "role_support_diagnostics": {
            "promoted_candidate_support_kind_counts": {
                k: dict(sorted(v.items(), key=lambda x: (-x[1], x[0])))
                for k, v in promoted_bases.items()
            },
            "promoted_candidate_support_group_counts": {
                k: dict(sorted(v.items(), key=lambda x: (-x[1], x[0])))
                for k, v in promoted_groups.items()
            },
            "basis_count_semantics": "Candidate/support-kind incidences for earlier-routed preferred candidates; one candidate may have multiple kinds. These are overlapping explanations, not causal attributions.",
            "cross_obligation_required_observations": cross,
        },
        "limits": [
            "Single prospective task and frozen 515-resource corpus; no general superiority claim.",
            "Role support is positive, overlapping evidence; placement is not satisfaction or negative evidence.",
            "One resource is the proxy for each adjudicated information unit in this v1 frame; source spans are retained in the frozen gold.",
            "No implementation, confirmation outcome, learned score or additional treatment arm was inspected or produced.",
        ],
    }


def markdown(data):
    """Render measurements and interpretation directly from machine artifact."""
    rows = data["own_lanes"]["obligations"]
    review = data["review_surface"]
    req = data["required"]
    lines = [
        "# Case 0005 Stage D joined analysis",
        "",
        "## Frozen measurements",
        "",
        f"Stage A/B/B.5/C identities and pinned hashes verified. Join: {data['join_integrity']['frame']['observed']}/515 resources, 9/9 obligations, 9/9 query/preferences, 4,635/4,635 judgments; no duplicates, misses or unexpected identities. The global lane is unchanged, and every routed lane retains every native match exactly once.",
        "",
        f"Required gold: {req['unit_occurrences']} obligation/unit occurrences, {req['distinct_units']} distinct units, {req['witness_universe_unique_resources']} unique witness-universe resources. Minimum semantically sufficient adjudicated union: **{req['minimum_semantically_sufficient_resource_union']} resources**; this is an information witness bound, not an implementation file set.",
        "",
        f"Global native: {data['global']['positive_matches']} positive matches; task-complete obligation depth **{data['global']['task_complete_obligation_depth']}**; complete 24-resource witness-universe depth **{data['global']['complete_witness_universe_depth']}**. All required resources and units are globally reachable. Own-lane maximum best native depth **{data['own_lanes']['maximum_native_completion_depth']}**; maximum best routed position **{data['own_lanes']['maximum_routed_completion_position']}**. These latter maxima span nine separate lanes.",
        "",
        "| Obligation | Global best | Own native | Own routed | Native prefix | Routed prefix | Change | Required preferred / escape | Preferred size / escape size |",
        "| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |",
    ]
    for x in rows:
        b = x["best_completion"]
        lines.append(
            f"| {x['identity']} | {b['global']} | {b['native']} | {b['routed']} | {x['native_prefix']['candidate_occurrences']} | {x['routed_prefix']['candidate_occurrences']} | {x['prefix_occurrence_change']:+d} | {x['required_tiers']['preferred']} / {x['required_tiers']['escape']} | {x['tier_sizes']['preferred']} / {x['tier_sizes']['escape']} |"
        )
    lines += [
        "",
        f"Completion improved: {', '.join(data['own_lanes']['comparison']['improved']) or 'none'}. Unchanged: {', '.join(data['own_lanes']['comparison']['unchanged']) or 'none'}. Worsened: {', '.join(data['own_lanes']['comparison']['worsened']) or 'none'}.",
        "",
        f"Native completion prefixes: **{review['native_summed_occurrences']} occurrences / {review['native_unique_resources']} unique resources**. Routed: **{review['routed_summed_occurrences']} occurrences / {review['routed_unique_resources']} unique resources**. Changes: {review['occurrence_change']:+d} occurrences ({review['occurrence_relative_change']:+.1%}) and {review['unique_change']:+d} unique resources ({review['unique_relative_change']:+.1%}).",
        "",
        f"Relative to the {req['minimum_semantically_sufficient_resource_union']}-resource sufficient union: native {review['native_over_sufficient_ratio']:.2f} times / +{review['native_excess_over_sufficient']}; routed {review['routed_over_sufficient_ratio']:.2f} times / +{review['routed_excess_over_sufficient']}. Prefix label occurrences (native to routed): REQUIRED {review['prefix_label_totals']['native']['REQUIRED']} to {review['prefix_label_totals']['routed']['REQUIRED']}, HELPFUL_ONLY {review['prefix_label_totals']['native']['HELPFUL_ONLY']} to {review['prefix_label_totals']['routed']['HELPFUL_ONLY']}, UNNECESSARY {review['prefix_label_totals']['native']['UNNECESSARY']} to {review['prefix_label_totals']['routed']['UNNECESSARY']}; unresolved 0.",
        "",
        f"Union overlap: {len(review['both_unions'])} in both, {len(review['only_native_union'])} native only, {len(review['only_routed_union'])} routed only. All are still present in their full routed lanes; prefix boundaries alone differ.",
        "",
        "### Alternative-aware completion and prefix composition",
        "",
    ]
    for x in rows:
        alts = "; ".join(
            f"{a['identity']}: global {a['completion']['global']}, native {a['completion']['native']}, routed {a['completion']['routed']}, {'escape needed' if a['depends_on_escape'] else 'all preferred'}"
            for a in x["alternatives"]
        )
        n, rr = x["native_prefix"]["labels"], x["routed_prefix"]["labels"]
        lines.append(
            f"- **{x['identity']}** — {alts}. Best G/N/R: {x['best_alternatives']['global']} / {x['best_alternatives']['native']} / {x['best_alternatives']['routed']}. Prefix R/H/U: native {n['REQUIRED']}/{n['HELPFUL_ONLY']}/{n['UNNECESSARY']}; routed {rr['REQUIRED']}/{rr['HELPFUL_ONLY']}/{rr['UNNECESSARY']}."
        )
    lines += [
        "",
        "## Observations",
        "",
        f"Required unit occurrences by routed tier: {req['occurrences_by_tier']}. Unique resources: preferred {len(req['unique_resources_by_tier']['PREFERRED_ROLE_SUPPORTED'])}, escape {len(req['unique_resources_by_tier']['ESCAPE'])}; a resource can occur in both categories across obligations. Required escape in the best routed alternative: {', '.join(x['identity'] for x in rows if next(a for a in x['alternatives'] if a['identity'] == x['best_alternatives']['routed'])['depends_on_escape']) or 'none'}.",
        "",
        "The validation lane has an empty preference. Its complete routed order equals native order, including every required witness and completion depth.",
        "",
        f"Unit-level decomposition classifications: {req['decomposition_classifications']}. Unit-level routing movement: {req['routing_classifications']}. All 27 required occurrences reach their own native and routed lanes; all 24 witness-universe resources reach the global lane.",
        "",
        f"Helpful-only: {data['helpful_only']['frame_helpful_cells']} obligation/resource cells, {data['helpful_only']['frame_helpful_unique_resources']} unique resources; {data['helpful_only']['native_reached_helpful_occurrences']} own native matches, {data['helpful_only']['routed_preferred_helpful_occurrences']} preferred and {data['helpful_only']['routed_escape_helpful_occurrences']} escape. Rank distributions by obligation are retained in analysis.json.",
        "",
        "### Preferred-tier quality",
        "",
        "Precision uses all preferred candidates as denominator. Recall uses all acceptable REQUIRED witness resources, then the best routed alternative separately.",
        "",
        "| Obligation | Required/Helpful/Unnecessary preferred | Precision, all alternatives | Recall, all alternatives | Precision, best routed alternative | Recall, best routed alternative |",
        "| --- | ---: | ---: | ---: | ---: | ---: |",
    ]
    for x in rows:
        q = x["preferred_quality"]
        p = x["preferred_tier_labels"]
        lines.append(
            f"| {x['identity']} | {p['REQUIRED']}/{p['HELPFUL_ONLY']}/{p['UNNECESSARY']} | {q['required_precision_all_alternatives']:.1%} | {q['required_recall_all_alternatives']:.1%} | {q['required_precision_best_routed_alternative']:.1%} | {q['required_recall_best_routed_alternative']:.1%} |"
            if q["required_precision_all_alternatives"] is not None
            else f"| {x['identity']} | 0/0/0 | n/a (empty tier) | 0.0% | n/a (empty tier) | 0.0% |"
        )
    lines += [
        "",
        "## Diagnostic post-hoc breakdown",
        "",
        "Required witness ranks, routed tiers, exact selected supports, escape reasons and cross-obligation observations are recorded per unit in analysis.json. The following counts are overlapping support-kind incidences among earlier-routed preferred candidates, not unique resources or causal effects.",
        "",
    ]
    for label in ("REQUIRED", "UNNECESSARY", "HELPFUL_ONLY"):
        counts = data["role_support_diagnostics"][
            "promoted_candidate_support_kind_counts"
        ][label]
        groups = data["role_support_diagnostics"][
            "promoted_candidate_support_group_counts"
        ][label]
        lines.append(
            f"- **{label} promoted:** kinds {', '.join(f'{k} {v}' for k, v in counts.items()) or 'none'}; grouped {', '.join(f'{k} {v}' for k, v in groups.items()) or 'none'}."
        )
    lines += [
        "",
        f"Required escape categories: {req['escape_categories']}. A preferred-role mismatch or cross-role requirement is still a retained candidate, not a false negative.",
        "",
        "### Required escape witnesses",
        "",
    ]
    for occurrence in req["occurrences"]:
        if occurrence["escape_diagnosis"]:
            d = occurrence["escape_diagnosis"]
            lines.append(
                f"- {occurrence['obligation']} / {occurrence['unit']}: `{occurrence['resource']}`, native {occurrence['own_native_rank']} → routed {occurrence['own_routed_position']}; {d['category']}; positive roles {', '.join(d['all_positive_roles']) or 'none'}; preferred {', '.join(d['caller_preferred_roles']) or '(empty)'}. Diagnostic target: {d['diagnostic_target']}."
            )
    cross = data["role_support_diagnostics"]["cross_obligation_required_observations"]
    lines += [
        "",
        f"Cross-obligation: {len(cross)} required unit occurrences have a better native rank, earlier routed position or other-lane preferred role; {sum(bool(z['better_native_other_lanes']) for z in cross)} rank better natively elsewhere, {sum(bool(z['earlier_routed_other_lanes']) for z in cross)} route earlier elsewhere, and {sum(bool(z['preferred_elsewhere_while_own_escape']) for z in cross)} are preferred elsewhere while escaped in their own lane. Examples: the Localization package overview and ADR-0005 escape source-oriented obligations but are preferred in the documentation lane. These other lanes are excluded from primary completion.",
        "",
        f"Alternative selection: {', '.join(x['identity'] for x in rows if x['alternative_changed_by_routing']) or 'none'} changed cheapest acceptable alternative from own native to routed. The global lane instead selects the third testing alternative; native and routed select the first. No cross-surface alternative is forced.",
        "",
        "## Architectural interpretation",
        "",
        "The nine scoped queries reduce the case-wide maximum completion depth from global 342 to own-lane native 110, while preserving global recall; the documentation obligation alone is slightly shallower globally. Positive role routing changes review order unevenly: it removes 26 summed prefix occurrences but expands the unique prefix union by 9 resources. Source-oriented preferences promote code contracts and delay required documentation in semantic ownership and witness algebra. The retained escape tier prevents candidate loss. These outcomes directly motivate evidence-to-witness resolution that reasons across resource roles and keeps alternatives explicit, rather than treating a preferred role or position as satisfaction.",
        "",
        "The directly evidenced bottlenecks are lexical discrimination (many unnecessary candidates before completion), role discrimination (large preferred tiers and cross-role escape), and the missing evidence-to-witness resolution capability. Acquisition recall did not fail for these frozen required witnesses. The nine-obligation interpretation had no adjudicated gap, though this one task cannot prove general interpretation quality.",
        "",
        "The next question is whether a bounded production association record can identify and retain cross-role witness hypotheses with native provenance and unresolved status, then prospectively measure its review cost. No implementation or new arm is introduced here.",
        "",
        "## Limitations",
        "",
        "One prospective task and one 515-resource frozen frame support only case-specific descriptive effects. Positive roles are overlapping hints. Counts before completion depend on the independently frozen witness frame and per-surface best acceptable alternative. No numeric success threshold, learned score, confirmation result or general superiority claim is inferred.",
        "",
    ]
    return "\n".join(lines).encode("utf-8")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument(
        "--write", action="store_true", help="create analysis outputs once"
    )
    mode.add_argument(
        "--check", action="store_true", help="read-only deterministic replay"
    )
    args = parser.parse_args()
    items = load()
    data = analyze(items)
    outputs = {"analysis.json": output_json(data), "analysis.md": markdown(data)}
    if args.write:
        if any((CASE / name).exists() for name in outputs):
            msg = "Stage D outputs already exist; frozen outputs are never overwritten"
            raise FileExistsError(msg)
        for name, contents in outputs.items():
            with (CASE / name).open("xb") as stream:
                stream.write(contents)
    else:
        for name, contents in outputs.items():
            assert (CASE / name).read_bytes() == contents, name
    sys.stdout.write(
        json.dumps(
            {
                "mode": "write" if args.write else "check",
                "analysis_sha256": sha(outputs["analysis.json"]),
                "markdown_sha256": sha(outputs["analysis.md"]),
                "depths": {
                    "global": data["global"]["task_complete_obligation_depth"],
                    "native": data["own_lanes"]["maximum_native_completion_depth"],
                    "routed": data["own_lanes"]["maximum_routed_completion_position"],
                },
                "review_surface": {
                    k: v
                    for k, v in data["review_surface"].items()
                    if k.endswith(("occurrences", "unique_resources"))
                    or k in {"unique_change", "unique_relative_change"}
                },
            },
            indent=2,
        )
        + "\n"
    )


if __name__ == "__main__":
    main()
