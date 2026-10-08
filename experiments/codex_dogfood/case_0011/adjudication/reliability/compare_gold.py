"""Bounded, treatment-free comparison of two sealed Case 0011 adjudications.

This operational experiment reads only named blind files. It does not adjudicate.
JSON dictionaries intentionally retain the two independent external schemas.
"""

# Standalone non-installable JSON evidence scripts; long sealed claims remain literal.
# ruff: noqa: INP001, CPY001, E501, COM812, ANN401, D103, S101, PLR2004, PERF401
from __future__ import annotations

import argparse
import gzip
import hashlib
import itertools
import json
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parent
LABELS = ("REQUIRED", "HELPFUL_ONLY", "UNNECESSARY", "UNRESOLVED")
EXPECTED = {
    "stage_c_r_review.json": "0323ae030d05a1508336181fe3fd671c7a87762680a5e434fec404ce74143576",
    "stage_c_r_statistics.json": "c29909f92a42d388dd72123f9b15e15648015da73f8101e575c8b4dd8ce32306",
    "stage_c_r_method.md": "80a163cfe86ff879ebaec6f5ed40e264db9c5030e29eb06c928f93c4062a3338",
    "stage_c_r_build.py": "2cc7165c2966c2872f53aac48cf8c6fec5f8c26e1729ff57e2c811b835223cf8",
    "stage_c_r_test.py": "a985ecd1910d892a1b9bb8226771f149bc193f9c59e7cc295800c3c8afcf4fe8",
    "stage_c_r_pytest.ini": "19842ea2d34a3cc8434a00e29849915ea32edd925a832bc427ef64dbbdeb757e",
    "stage_c_r_validation.json": "7c82163c4b74ff43738d1f90e04f24dac2e7202c6ec33b7bc6317fcc79b4d11c",
    "stage_c_r_sha256.json": "4a267a49b2f076b2a1d9fdbf3678e58f9fa834950ee4fb800dd93ab9b3dc5a52",
}

# Manual diagnostic proposals based on statements, necessity and source support.
# Generic candidates require shared obligation and overlapping resource support.
# Explicit semantic proposals may differ in evidence account or necessity context.
PROPOSALS = {
    "U01": [("O1", "SUBSTANTIALLY_EQUIVALENT"), ("O2", "SUBSTANTIALLY_EQUIVALENT")],
    "U02": [("O1", "PARTIAL_OVERLAP"), ("O2", "PARTIAL_OVERLAP")],
    "U03": [("O3", "SUBSTANTIALLY_EQUIVALENT")],
    "U04": [("F5", "PARTIAL_OVERLAP")],
    "U05": [("B1", "SUBSTANTIALLY_EQUIVALENT")],
    "U06": [("B2", "PARTIAL_OVERLAP"), ("R1", "PARTIAL_OVERLAP")],
    "U07": [("C3", "PARTIAL_OVERLAP")],
    "U09": [("C1", "PRIMARY_BROADER")],
    "U10": [("R2", "PRIMARY_BROADER")],
    "U12": [("F1", "SUBSTANTIALLY_EQUIVALENT")],
    "U14": [("F2", "SUBSTANTIALLY_EQUIVALENT")],
    "U16": [("F3", "SUBSTANTIALLY_EQUIVALENT")],
    "U17": [("F4", "PRIMARY_BROADER")],
    "U18": [("F5", "SUBSTANTIALLY_EQUIVALENT")],
    "U19": [("F6", "PARTIAL_OVERLAP")],
    "U20": [("F6", "PARTIAL_OVERLAP"), ("F7", "PARTIAL_OVERLAP")],
    "U22": [("E1", "SUBSTANTIALLY_EQUIVALENT")],
    "U23": [("E2", "SUBSTANTIALLY_EQUIVALENT")],
    "U24": [("T1", "PRIMARY_BROADER")],
    "U25": [("T2", "PARTIAL_OVERLAP"), ("T3", "PARTIAL_OVERLAP")],
    "U27": [("T4", "REVIEW_BROADER")],
    "U28": [("T4", "PARTIAL_OVERLAP")],
    "U29": [("T3", "PARTIAL_OVERLAP")],
    "U30": [("C2", "PRIMARY_BROADER")],
    "U32": [("D1", "SUBSTANTIALLY_EQUIVALENT")],
    "U33": [("D2", "SUBSTANTIALLY_EQUIVALENT"), ("D3", "PARTIAL_OVERLAP")],
    "U37": [("V3", "SUBSTANTIALLY_EQUIVALENT")],
    "U38": [("V5", "REVIEW_BROADER")],
    "U39": [("V5", "REVIEW_BROADER")],
    "U40": [("V4", "SUBSTANTIALLY_EQUIVALENT")],
    "U41": [("V1", "SUBSTANTIALLY_EQUIVALENT"), ("V2", "PARTIAL_OVERLAP")],
}

SEMANTIC_RATIONALES = {
    (
        "U01",
        "O1",
    ): "Both locate ordered plan realization, rendering and copied assembly in common Planning, separate from automatic acquisition.",
    (
        "U01",
        "O2",
    ): "Both establish the package owner and existing plan/materialization/render/assembly pipeline; supported choice forms are supplementary detail.",
    (
        "U02",
        "O1",
    ): "Both prohibit promoting common assembly into automatic planning; capacity/no-truncation claims extend beyond the current-owner statement. Distinct architecture passages support this candidate.",
    (
        "U02",
        "O2",
    ): "Both prohibit automatic selection; the capacity-ceiling/no-replanning claim is additional. Different governing sources establish only partial overlap.",
    (
        "U03",
        "O3",
    ): "Both inspect common rendering imports and dataclass-based assembly to establish the language-independent owner.",
    (
        "U04",
        "F5",
    ): "The same adapter realization span delegates to validated materialization and retains native values. One necessity context is ownership/dependency direction, the other frame/provenance; neither claim exhausts the other.",
    (
        "U05",
        "B1",
    ): "Both enumerate the same renderer headings, plan/frame identifiers, ordered item text and explicit separators without normalization.",
    (
        "U06",
        "B2",
    ): "Both count UTF-8 Context separately from the original task and preserve outer framing; Prompt-role retention and reported byte lengths differ in emphasis.",
    (
        "U06",
        "R1",
    ): "Both preserve role and replace only Prompt; the byte/envelope claim additionally contains counting and newline semantics, while the other focuses on copied-request preservation.",
    (
        "U07",
        "C3",
    ): "Both identify the RenderedContextDisclosure entry point. Absence of capacity checks versus keyword-only signature and final replace timing are distinct claims.",
    (
        "U09",
        "C1",
    ): "The broader claim permits request and usage numeric witnesses with differing exception/range conventions; the narrower claim retains only the request-side validator.",
    (
        "U10",
        "R2",
    ): "Both enumerate frozen request fields; the broader claim additionally requires typed admission and unique Tool names.",
    (
        "U12",
        "F1",
    ): "Both require immutable ordered plan/frame values and the same blank/empty/mixed/duplicate admission invariants; lineage detail does not change this shared necessary slice.",
    (
        "U14",
        "F2",
    ): "Both establish immutable materialized item identities/text/native provenance and exact plan cardinality/order/representation matching.",
    (
        "U16",
        "F3",
    ): "Both require foreign-frame rejection, ordered option realization and identity/representation validation before publishing ContextDisclosure.",
    (
        "U17",
        "F4",
    ): "Both preserve whole-resource occurrence/content/provenance checks. The broader claim also includes exact rendering, headings/separators and byte count.",
    (
        "U18",
        "F5",
    ): "Both preserve adapter delegation, both resource identities, rendered text and native materialized values; option-identity construction is additional detail in the same adapter slice.",
    (
        "U19",
        "F6",
    ): "Both require source membership/frame/content checks; admission route/analysis membership and target/dependency checks extend in different directions.",
    (
        "U20",
        "F6",
    ): "Both require retained target and dependency checks. Exact extraction/declaration membership and source checks are distinct complementary slices.",
    (
        "U20",
        "F7",
    ): "Both validate retained target interpretation/declaration analysis; one extends to dependency support and exact extraction, the other isolates interpretation-frame agreement.",
    (
        "U22",
        "E1",
    ): "Both establish explicit common-package imports and __all__ exposure for the existing assembly API.",
    (
        "U23",
        "E2",
    ): "Both establish umbrella Context facade reexports of common planning/materialization/render/assembly symbols.",
    (
        "U24",
        "T1",
    ): "Both use exact UTF-8 byte fixtures and explicit observation; the broader fixture account additionally constructs qualified options through production analysis.",
    (
        "U25",
        "T2",
    ): "Both test mixed whole/qualified choices, CRLF/non-ASCII fidelity, provenance and render order; identity/lineage and request-copy claims extend the combined account.",
    (
        "U25",
        "T3",
    ): "Both test copied assembly and unchanged caller values; mixed-plan identities/provenance versus detailed request replacement checks are different granularities.",
    (
        "U27",
        "T4",
    ): "Both exercise changed snapshots, stale retained contents and missing resources; the broader test account additionally covers mismatched realized items.",
    (
        "U28",
        "T4",
    ): "Both exercise incompatible realized items using replacement and rejection assertions; incompatible option/cardinality and stale/missing cases are distinct slices.",
    (
        "U29",
        "T3",
    ): "Different test files establish copied-request preservation with populated request fields. Adjacent exact-CRLF/non-ASCII assembly and common Context-order/replacement tests overlap in necessity but differ in evidence and covered behavior.",
    (
        "U30",
        "C2",
    ): "Both exercise bool/string/float/negative/None numeric cases; the broader claim preserves competing ValueError and TypeError/ValueError precedents rather than only request-positive-domain tests.",
    (
        "U32",
        "D1",
    ): "Both require central architecture documentation of the current common caller-directed foundation; broader accepted semantics remain distinct from implemented behavior.",
    (
        "U33",
        "D2",
    ): "Both require package documentation of exact materialization, native values, copied assembly, concrete choices and bounded capacity claims.",
    (
        "U33",
        "D3",
    ): "Different sections of the same package document limit capacity claims: no universal/token budget versus no coverage/capacity establishment by plan_disclosures. Related constraints partially overlap, without identical support spans.",
    (
        "U37",
        "V3",
    ): "Both require the executable tests/ignore-experiments argument construction and pytest exit-code propagation.",
    (
        "U38",
        "V5",
    ): "Both preserve strict pytest and full production branch coverage; the broader combined project-config claim also includes Ruff and strict mypy.",
    (
        "U39",
        "V5",
    ): "Both preserve Ruff/Python/mypy settings; the broader combined project-config claim also includes pytest/coverage requirements.",
    (
        "U40",
        "V4",
    ): "Both require separate Ruff lint/format, mypy and whitespace checks beyond the protected test command.",
    (
        "U41",
        "V1",
    ): "Both require the protected uv command, pre-collection experiment exclusion and retained project configuration/coverage gate.",
    (
        "U41",
        "V2",
    ): "Validation documentation and operating rules independently require the same protected command/exclusion/coverage contract; the operating-rule claim additionally emphasizes separate static checks. This is an alternative evidence-account candidate, not an identical source span.",
}


def canonical(value: Any) -> bytes:
    return (
        json.dumps(
            value,
            ensure_ascii=False,
            sort_keys=True,
            separators=(",", ":"),
            allow_nan=False,
        )
        + "\n"
    ).encode("utf-8")


def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def load(path: Path) -> Any:
    return json.loads(path.read_bytes())


def partition(left: set[Any], right: set[Any]) -> dict[str, Any]:
    intersection, union = left & right, left | right
    return {
        "intersection": sorted(intersection),
        "union": sorted(union),
        "intersection_count": len(intersection),
        "union_count": len(union),
        "jaccard": len(intersection) / len(union) if union else None,
        "primary_only": sorted(left - right),
        "review_only": sorted(right - left),
        "primary_retained_by_review": len(intersection) / len(left) if left else None,
        "review_retained_by_primary": len(intersection) / len(right) if right else None,
    }


def normalized(
    primary: dict[str, Any], review: dict[str, Any]
) -> tuple[dict[str, Any], dict[str, Any]]:
    evidence = {e["evidence_id"]: e for e in primary["source_support"]}
    p_units = []
    for unit in primary["required_units"]:
        support: list[dict[str, Any]] = []
        for eid in unit["acceptable_unit_witnesses"]:
            e = evidence[eid]
            support.extend({"address": e["resource_address"], **s} for s in e["spans"])
        contexts = [
            o["obligation_id"]
            for o in primary["obligation_judgments"]
            if unit["unit_id"] in o["required_unit_ids"]
        ]
        p_units.append(
            {
                "id": unit["unit_id"],
                "statement": unit["statement"],
                "necessity": unit["necessity"],
                "obligations": contexts,
                "scope": unit["scope"],
                "supports": support,
                "rationale": unit["inferability_reason"],
            }
        )
    r_units = [
        {
            "id": u["id"],
            "statement": u["statement"],
            "necessity": "REQUIRED",
            "obligations": u["owning_obligations"],
            "scope": "FROZEN_OBLIGATIONS",
            "supports": [
                {"address": u["resource"]["address"], **s} for s in u["supports"]
            ],
            "rationale": u["necessity_rationale"],
        }
        for u in review["required_information_units"]
    ]
    p_obs = [
        {
            "id": o["obligation_id"],
            "applicability": o["applicability"],
            "rationale": o["applicability_reason"],
            "alternatives": [
                {
                    "id": a["alternative_id"],
                    "resources": a["all_resource_addresses"],
                    "units": a["all_required_unit_ids"],
                    "rationale": a["acceptance_reason"],
                    "support": [evidence[e] for e in a["all_evidence_ids"]],
                }
                for a in o["acceptable_alternatives"]
            ],
        }
        for o in primary["obligation_judgments"]
    ]
    r_obs = [
        {
            "id": o["frozen_obligation"]["identity"],
            "applicability": o["applicability"],
            "rationale": o["applicability_rationale"],
            "alternatives": [
                {
                    "id": a["id"],
                    "resources": a["all_resources"],
                    "units": a["all_units"],
                    "rationale": "ALL members complementary; ANY complete alternative suffices.",
                    "support": [],
                }
                for a in o["alternatives_any"]
            ],
        }
        for o in review["obligations"]
    ]
    p_cells = [
        {
            "obligation": c["obligation_id"],
            "address": c["resource_address"],
            "content_identity": c["content_identity"],
            "label": c["label"],
            "rationale": c["reason"],
            "units": c["required_unit_ids"],
        }
        for c in primary["cells"]
    ]
    r_cells = [
        {
            "obligation": c["obligation"],
            "address": c["resource"]["address"],
            "content_identity": c["resource"]["content_identity"],
            "label": c["label"],
            "rationale": c["rationale"],
            "units": c["required_units"],
        }
        for c in review["cells"]
    ]
    return (
        {"units": p_units, "obligations": p_obs, "cells": p_cells},
        {"units": r_units, "obligations": r_obs, "cells": r_cells},
    )


def frame_check(
    primary: dict[str, Any],
    review: dict[str, Any],
    manifest: dict[str, Any],
    resources: list[dict[str, Any]],
) -> None:
    assert primary["frame"] == review["frame"]
    assert all(manifest[k] == v for k, v in primary["frame"].items())
    assert primary["frozen_obligations"] == manifest["obligations"]
    assert review["frozen_manifest"] == manifest
    assert [o["frozen_obligation"] for o in review["obligations"]] == manifest[
        "obligations"
    ]
    assert primary["task_sha256"] == sha(manifest["task"].encode())
    assert primary["resource_frame"] == [
        {k: r[k] for k in ("address", "byte_size", "content_identity", "encoding")}
        for r in resources
    ]
    ids = {r["address"]: r["content_identity"] for r in resources}
    assert len(ids) == len(resources) == 531
    assert len(review["resources"]) == 531
    for r in review["resources"]:
        assert r["content_identity"] == ids[r["address"]]
        assert all(
            r[k] == manifest[k] for k in ("repository_id", "snapshot_id", "corpus_id")
        )
    assert len({r["address"] for r in review["resources"]}) == 531
    for cell in review["cells"]:
        assert all(
            cell["resource"][k] == manifest[k]
            for k in ("repository_id", "snapshot_id", "corpus_id")
        )
    assert all(
        primary["input_sha256"][k] == v
        for k, v in review["input_sha256"].items()
        if k != "STAGE_C_R_INSTRUCTIONS.md"
    )
    p, r = normalized(primary, review)
    expected = {
        (o["identity"], address) for o in manifest["obligations"] for address in ids
    }
    for gold in (p, r):
        cells = gold["cells"]
        assert len(cells) == len(expected) == 4779
        assert {(c["obligation"], c["address"]) for c in cells} == expected
        assert all(
            c["content_identity"] == ids[c["address"]] and c["label"] in LABELS
            for c in cells
        )
        for unit in gold["units"]:
            for s in unit["supports"]:
                content = next(
                    v["content"] for v in resources if v["address"] == s["address"]
                )
                assert (
                    content[s["start_character"] : s["end_character"]] == s["excerpt"]
                )
                assert sha(s["excerpt"].encode()) == s["excerpt_sha256"]


def structure(gold: dict[str, Any]) -> dict[str, Any]:
    choices = [o["alternatives"] for o in gold["obligations"]]
    combos = list(itertools.product(*choices))
    unions = {
        tuple(sorted({r for a in combo for r in a["resources"]})) for combo in combos
    }
    unit_unions = [{u for a in combo for u in a["units"]} for combo in combos]
    minimum = min(map(len, unions))
    return {
        "alternatives": sum(map(len, choices)),
        "combinations": len(combos),
        "distinct_unions": len(unions),
        "minimum": minimum,
        "maximum": max(map(len, unions)),
        "unions": sorted(unions),
        "minimum_unions": sorted(u for u in unions if len(u) == minimum),
        "indispensable_resources": sorted(set.intersection(*(set(u) for u in unions))),
        "indispensable_units": sorted(set.intersection(*unit_unions)),
        "by_obligation": [
            {
                "obligation": o["id"],
                "count": len(o["alternatives"]),
                "alternatives": o["alternatives"],
                "indispensable_resources": sorted(
                    set.intersection(*(set(a["resources"]) for a in o["alternatives"]))
                ),
                "indispensable_units": sorted(
                    set.intersection(*(set(a["units"]) for a in o["alternatives"]))
                ),
            }
            for o in gold["obligations"]
        ],
    }


def align_units(p: dict[str, Any], r: dict[str, Any]) -> dict[str, Any]:
    pairs = []
    for pu in p["units"]:
        for ru in r["units"]:
            common = sorted(set(pu["obligations"]) & set(ru["obligations"]))
            overlaps = [
                {
                    "address": ps["address"],
                    "primary_span": [ps["start_character"], ps["end_character"]],
                    "review_span": [rs["start_character"], rs["end_character"]],
                }
                for ps in pu["supports"]
                for rs in ru["supports"]
                if ps["address"] == rs["address"]
                and max(ps["start_character"], rs["start_character"])
                < min(ps["end_character"], rs["end_character"])
            ]
            proposed = dict(PROPOSALS.get(pu["id"], [])).get(ru["id"])
            if (not common or not overlaps) and proposed is None:
                continue
            classification = proposed or "AMBIGUOUS"
            semantic_rationale = SEMANTIC_RATIONALES.get(
                (pu["id"], ru["id"]),
                "Source/obligation overlap alone is insufficient to infer semantic compatibility; this candidate remains ambiguous.",
            )
            pairs.append(
                {
                    "primary": pu["id"],
                    "review": ru["id"],
                    "classification": classification,
                    "common_obligations": common,
                    "source_overlap": overlaps,
                    "primary_supports": pu["supports"],
                    "review_supports": ru["supports"],
                    "semantic_rationale": semantic_rationale,
                    "primary_statement": pu["statement"],
                    "review_statement": ru["statement"],
                    "rationale": f"Shared obligation(s) {common}; source accounts and overlap recorded separately. {semantic_rationale} "
                    f"Compare necessity claims: {pu['statement']} / {ru['statement']}. "
                    f"{classification}: diagnostic granularity proposal only; no identity inferred from IDs or wording.",
                    "primary_only_obligations": sorted(
                        set(pu["obligations"]) - set(ru["obligations"])
                    ),
                    "review_only_obligations": sorted(
                        set(ru["obligations"]) - set(pu["obligations"])
                    ),
                }
            )
    matched_p = {a["primary"] for a in pairs if a["classification"] != "AMBIGUOUS"}
    matched_r = {a["review"] for a in pairs if a["classification"] != "AMBIGUOUS"}
    return {
        "proposals": pairs,
        "aligned_primary_count": len(matched_p),
        "aligned_review_count": len(matched_r),
        "proposal_count": len(pairs),
        "unmatched_primary": [u["id"] for u in p["units"] if u["id"] not in matched_p],
        "unmatched_review": [u["id"] for u in r["units"] if u["id"] not in matched_r],
        "no_match_policy": "Unmatched means NO_MATCH under explicit compatible proposals; ambiguous source overlap is not a semantic match.",
    }


def compare() -> dict[str, Any]:
    for name, digest in EXPECTED.items():
        assert sha((ROOT / name).read_bytes()) == digest, name
    parent = ROOT.parent
    assert (
        sha((parent / "judgments.json").read_bytes())
        == "71da4b04a8507cc341303129dc70d4cdf4ab0ff4e0a7b700422b287e2793d4a6"
    )
    primary, review = (
        load(parent / "judgments.json"),
        load(ROOT / "stage_c_r_review.json"),
    )
    manifest = load(parent / "manifest.json")
    archive_bytes = (parent / "resources.json.gz").read_bytes()
    assert sha(archive_bytes) == manifest["archive_sha256"]
    payload_bytes = gzip.decompress(archive_bytes)
    assert sha(payload_bytes) == manifest["canonical_payload_sha256"]
    resources = json.loads(payload_bytes)["resources"]
    assert (parent / "task.txt").read_bytes() == manifest["task"].encode()
    frame_check(primary, review, manifest, resources)
    p, r = normalized(primary, review)
    pc = {(c["obligation"], c["address"]): c for c in p["cells"]}
    rc = {(c["obligation"], c["address"]): c for c in r["cells"]}
    matrix = [
        [
            sum(pc[k]["label"] == pl and rc[k]["label"] == rl for k in pc)
            for rl in LABELS
        ]
        for pl in LABELS
    ]
    agreement = sum(matrix[i][i] for i in range(4))
    chance = (
        sum(sum(matrix[i]) * sum(row[i] for row in matrix) for i in range(4)) / 4779**2
    )
    by_label = {
        label: partition(
            {k for k in pc if pc[k]["label"] == label},
            {k for k in rc if rc[k]["label"] == label},
        )
        for label in LABELS
    }
    by_obligation = {}
    for o in manifest["obligations"]:
        oid = o["identity"]
        by_obligation[oid] = {
            label: partition(
                {k[1] for k in pc if k[0] == oid and pc[k]["label"] == label},
                {k[1] for k in rc if k[0] == oid and rc[k]["label"] == label},
            )
            for label in LABELS
        }
    ps, rs = structure(p), structure(r)
    assert (
        ps["alternatives"],
        ps["combinations"],
        ps["distinct_unions"],
        ps["minimum"],
        ps["maximum"],
        len(ps["indispensable_resources"]),
    ) == (20, 144, 8, 23, 25, 22)
    assert (
        rs["alternatives"],
        rs["combinations"],
        rs["distinct_unions"],
        rs["minimum"],
        rs["maximum"],
        len(rs["indispensable_resources"]),
    ) == (12, 8, 2, 15, 17, 15)
    # Independently check the sealed statistics, including exact sufficient unions.
    pstats, rstats = (
        load(parent / "gold_statistics.json"),
        load(ROOT / "stage_c_r_statistics.json"),
    )
    assert pstats["unique_required_resources"] == 26
    assert rstats["required_union"]["resource_count"] == 17
    assert {
        tuple(sorted(c["resource_union"])) for c in pstats["complete_combinations"]
    } == set(ps["unions"])
    assert {tuple(u) for u in rstats["sufficient_resource_unions"]} == set(rs["unions"])
    assert set(pstats["required_resource_addresses"]) == {
        k[1] for k in pc if pc[k]["label"] == "REQUIRED"
    }
    assert set(rstats["required_union"]["resources"]) == {
        k[1] for k in rc if rc[k]["label"] == "REQUIRED"
    }
    alternatives = []
    for po, ro in zip(ps["by_obligation"], rs["by_obligation"], strict=True):
        matches = []
        for pa in po["alternatives"]:
            for ra in ro["alternatives"]:
                left, right = set(pa["resources"]), set(ra["resources"])
                classification = (
                    "EQUIVALENT_RESOURCE_SET"
                    if left == right
                    else "PARTIAL_OVERLAP"
                    if left & right
                    else "AMBIGUOUS"
                )
                matches.append(
                    {
                        "primary_id": pa["id"],
                        "review_id": ra["id"],
                        "classification": classification,
                        "resources": partition(left, right),
                        "unit_semantics": "Distinct IDs retained; see unit proposals. Resource equality does not establish exact semantic equality.",
                    }
                )
        alternatives.append(
            {
                "obligation": po["obligation"],
                "primary": po,
                "review": ro,
                "candidate_pairs": matches,
                "primary_only": [
                    a["id"]
                    for a in po["alternatives"]
                    if not any(
                        set(a["resources"]) == set(b["resources"])
                        for b in ro["alternatives"]
                    )
                ],
                "review_only": [
                    a["id"]
                    for a in ro["alternatives"]
                    if not any(
                        set(a["resources"]) == set(b["resources"])
                        for b in po["alternatives"]
                    )
                ],
                "complementarity": "ALL within each alternative; ANY complete alternative. No union flattening.",
            }
        )
    spans = []
    for gold in (p, r):
        spans.append(
            {
                (
                    o,
                    s["address"],
                    s["start_character"],
                    s["end_character"],
                    s["excerpt_sha256"],
                )
                for u in gold["units"]
                for o in u["obligations"]
                for s in u["supports"]
            }
        )
    required_resources = partition(
        {k[1] for k in pc if pc[k]["label"] == "REQUIRED"},
        {k[1] for k in rc if rc[k]["label"] == "REQUIRED"},
    )
    assert (
        len(required_resources["primary_only"])
        + required_resources["intersection_count"]
        == 26
    )
    assert (
        len(required_resources["review_only"])
        + required_resources["intersection_count"]
        == 17
    )
    agreed = [
        {
            "obligation": k[0],
            "address": k[1],
            "content_identity": pc[k]["content_identity"],
            "label": pc[k]["label"],
        }
        for k in sorted(pc)
        if pc[k]["label"] == rc[k]["label"]
    ]
    disputes = [
        {"obligation": k[0], "address": k[1], "primary": pc[k], "review": rc[k]}
        for k in sorted(pc)
        if pc[k]["label"] != rc[k]["label"]
    ]
    return {
        "schema": "case-0011-gold-reliability-v1",
        "frame": primary["frame"],
        "frame_integrity": {
            "resources": 531,
            "obligations": 9,
            "qualified_cells": 4779,
            "duplicates": 0,
            "missing": 0,
            "unexpected": 0,
            "exact_task_and_obligations": True,
        },
        "applicability": [
            {
                "obligation": po["id"],
                "primary": po["applicability"],
                "review": ro["applicability"],
                "primary_rationale": po["rationale"],
                "review_rationale": ro["rationale"],
            }
            for po, ro in zip(p["obligations"], r["obligations"], strict=True)
        ],
        "confusion": {
            "rows": "primary",
            "columns": "review",
            "labels": LABELS,
            "matrix": matrix,
        },
        "agreement_count": agreement,
        "disagreement_count": 4779 - agreement,
        "overall_agreement": agreement / 4779,
        "descriptive_cohen_kappa": (agreement / 4779 - chance) / (1 - chance),
        "chance_agreement": chance,
        "per_label": by_label,
        "per_obligation": by_obligation,
        "required_resources": required_resources,
        "required_resource_contexts": {
            a: {
                "primary": [
                    k[0] for k in pc if k[1] == a and pc[k]["label"] == "REQUIRED"
                ],
                "review": [
                    k[0] for k in rc if k[1] == a and rc[k]["label"] == "REQUIRED"
                ],
            }
            for a in required_resources["union"]
        },
        "exact_supported_spans": partition(*spans),
        "units": align_units(p, r),
        "alternatives": alternatives,
        "sufficient_unions": {
            "primary": ps,
            "review": rs,
            "set_overlap": partition(set(ps["unions"]), set(rs["unions"])),
            "minimum_resource_overlap": partition(
                {a for u in ps["minimum_unions"] for a in u},
                {a for u in rs["minimum_unions"] for a in u},
            ),
            "minimum_union_pairs": [
                partition(set(pu), set(ru))
                for pu in ps["minimum_unions"]
                for ru in rs["minimum_unions"]
            ],
            "indispensability": partition(
                set(ps["indispensable_resources"]), set(rs["indispensable_resources"])
            ),
            "structural_reason": "Exact named witnesses and obligation intersections above determine union sizes. Different source accounts, omitted unit claims and shared resources change cardinality; this does not decide necessity.",
            "indispensability_difference_causes": [
                {
                    "address": address,
                    "primary_all_alternative_obligations": [
                        o["obligation"]
                        for o in ps["by_obligation"]
                        if address in o["indispensable_resources"]
                    ],
                    "review_all_alternative_obligations": [
                        o["obligation"]
                        for o in rs["by_obligation"]
                        if address in o["indispensable_resources"]
                    ],
                    "review_omitting_complete_unions": [
                        u for u in rs["unions"] if address not in u
                    ],
                    "primary_omitting_complete_unions": [
                        u for u in ps["unions"] if address not in u
                    ],
                    "reason": "Intersection across the enumerated complete unions determines task indispensability; omitted unions and obligation-level intersections are exact structural evidence, not correctness judgments.",
                }
                for address in sorted(
                    set(ps["indispensable_resources"])
                    ^ set(rs["indispensable_resources"])
                )
            ],
        },
        "gaps": {
            "primary_task": primary["task_gaps"],
            "review_task": review["task_gap"],
            "review_task_rationale": review["task_gap_rationale"],
            "primary_supplemental_units": [
                u for u in p["units"] if u["scope"] == "SUPPLEMENTAL_TASK_GAP"
            ],
            "review_supplemental_units": review["supplemental_task_gap_units"],
            "primary_limitations": primary["task_interpretation_gaps"],
            "review_limitations": review["task_interpretation_limitations"],
            "limitation_proposals": [
                {
                    "primary": "I01",
                    "review": "L1",
                    "classification": "PARTIAL_OVERLAP",
                    "rationale": "Same input-type mismatch; review additionally proposes wrapper/retained pipeline interpretation.",
                },
                {
                    "primary": "I02",
                    "review": "L3",
                    "classification": "SUBSTANTIALLY_EQUIVALENT",
                    "rationale": "Same empty-plan prohibition, nonzero canonical rendering and no weakened invariants.",
                },
                {
                    "primary": "I03",
                    "review": "L5",
                    "classification": "PARTIAL_OVERLAP",
                    "rationale": "Both retain numeric error ambiguity; review prefers request precedent, primary preserves competing precedents.",
                },
            ],
            "primary_only_limitations": ["I04"],
            "review_only_limitations": ["L2", "L4"],
            "primary_repository_gaps": primary["repository_information_gaps"],
            "review_repository_gaps": review["repository_information_gap"],
            "primary_repository_rationale": primary["repository_gap_review"],
            "review_repository_rationale": review["repository_gap_rationale"],
        },
        "agreed_cells": agreed,
        "agreed_cell_sha256": sha(canonical(agreed)),
        "disputed_cells": disputes,
        "conclusion": {
            "classification": "SEVERE ARCHITECTURE-RELEVANT DISAGREEMENT",
            "assessments": {
                "frame_and_applicability": "HIGH AGREEMENT",
                "required_and_helpful_boundary": "MATERIAL DISAGREEMENT",
                "witness_structure_and_task_gap": "SEVERE ARCHITECTURE-RELEVANT DISAGREEMENT",
            },
            "basis": "Required witness structures differ (20/12 alternatives, 23/15 minimum unions, 22/15 indispensable resources), alongside necessary-cell and task-gap differences. High aggregate agreement is dominated by UNNECESSARY cells. No threshold or truth reference is used.",
            "reviewed_gold_required_before_c5": True,
            "stage_d_blocked": True,
            "primary_gold_only_conclusions_unsafe": True,
            "u1_effectiveness": "UNKNOWN",
        },
    }


def write_new(files: dict[Path, bytes]) -> None:
    if any(p.exists() for p in files):
        msg = "Refusing to overwrite generated artifacts"
        raise FileExistsError(msg)
    for path, raw in files.items():
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(raw)


def markdown(result: dict[str, Any]) -> bytes:
    lines = [
        "# Case 0011 blind gold reliability",
        "",
        "Neither adjudication is truth. All alignments are diagnostic proposals.",
        "",
        f"Frame: 531 resources, 9 obligations, 4,779 cells; exact task/frame match. Agreement {result['agreement_count']}/4779; disagreements {result['disagreement_count']}.",
        f"Overall agreement {result['overall_agreement']:.8%}; descriptive Cohen kappa {result['descriptive_cohen_kappa']:.8f}.",
        "",
        "Rows primary; columns review. Order REQUIRED, HELPFUL_ONLY, UNNECESSARY, UNRESOLVED.",
        "",
        "```",
        *[str(row) for row in result["confusion"]["matrix"]],
        "```",
        "",
    ]
    for label in ("REQUIRED", "HELPFUL_ONLY"):
        v = result["per_label"][label]
        lines.append(
            f"{label} cells: intersection {v['intersection_count']}, union {v['union_count']}, Jaccard {v['jaccard']}; directional retention primary by review {v['primary_retained_by_review']}, review by primary {v['review_retained_by_primary']}."
        )
    lines.extend(
        [
            "",
            "The JSON contains exact set partitions by obligation, every support-span partition, unit proposals and unmatched IDs, all paired alternative structures, complete sufficient unions and indispensability sets, and exact gap/limitation claims.",
            "",
            result["conclusion"]["classification"],
            result["conclusion"]["basis"],
            "",
            "Reviewed/reconciled gold is PENDING; C.5 and Stage D are BLOCKED; U1 effectiveness is UNKNOWN. Primary-only architectural conclusions are unsafe.",
            "",
        ]
    )
    return "\n".join(lines).encode()


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    result = compare()
    files = {
        ROOT / "reliability_comparison.json": canonical(result),
        ROOT / "reliability_comparison.md": markdown(result),
    }
    if args.check:
        assert all(p.read_bytes() == raw for p, raw in files.items())
    else:
        write_new(files)


if __name__ == "__main__":
    main()
