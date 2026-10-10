"""Reconstruct Case 0012 reliability from two sealed, treatment-blind reviews.

This is bounded research publication tooling, not framework Evaluation or gold.
It reads only explicitly named adjudication inputs and the sealed blind payload.
Independent unit IDs are never compared as semantic identities. ALIGNMENTS.json
contains authored, provenance-preserving hypotheses, not reconciled conclusions.
Filesystem I/O here is the standalone publication boundary; no managed resource
acquisition, repository discovery, treatment join or external process is used.
"""

from __future__ import annotations

# ruff: noqa: INP001, CPY001, E501, PLR2004
# Standalone research entry point, fixed protocol numbers, and exact review prose.
import argparse
import ast
import gzip
import hashlib
import itertools
import json
import re
import sys
from collections import Counter
from pathlib import Path
from typing import Any

LABELS = ("REQUIRED", "HELPFUL_ONLY", "UNNECESSARY", "UNRESOLVED")
ROOT = Path(__file__).resolve().parent
SEALED = ROOT.parent
SOURCE = Path(
    r"C:\Users\recoveryadmin\CodexSterile\case_0012_stage_c_r_2cbc95afb120",
)
PROTOCOL_HASHES = {
    "PROTOCOL.json": "8315600ceda3006123ce2b4601a99e5a948278730ae26ab4bad9b5adb0ff45b3",
    "PROTOCOL.md": "54261d3bd8131dd35a4f0c35acda31db1057b81feb30462b49608a91f4c9ac0a",
}


def require(condition: bool, message: str) -> None:  # noqa: FBT001 -- predicate guard
    """Reject a failed publication invariant, including under optimized Python."""
    if not condition:
        raise ValueError(message)


def encoded(value: Any) -> bytes:  # noqa: ANN401 -- sealed heterogeneous JSON
    """Return deterministic publication bytes."""
    return (
        json.dumps(value, sort_keys=True, indent=2, ensure_ascii=True) + "\n"
    ).encode()


def sha(raw: bytes) -> str:
    """Return the physical SHA-256, distinct from native identity and Git OID."""
    return hashlib.sha256(raw).hexdigest()


def load(path: Path) -> Any:  # noqa: ANN401 -- validated sealed JSON boundary
    """Load one explicitly named JSON file."""
    return json.loads(path.read_bytes())


def overlap(a: set[str], b: set[str]) -> dict[str, Any]:
    """Retain exact sets, Jaccard and both directional retention scopes."""
    return {
        "primary_count": len(a),
        "c_r_count": len(b),
        "intersection_count": len(a & b),
        "union_count": len(a | b),
        "intersection": sorted(a & b),
        "union": sorted(a | b),
        "jaccard": len(a & b) / len(a | b) if a | b else 1.0,
        "primary_only": sorted(a - b),
        "c_r_only": sorted(b - a),
        "primary_retention": len(a & b) / len(a) if a else None,
        "c_r_retention": len(a & b) / len(b) if b else None,
    }


def authenticate() -> tuple[dict[str, Any], dict[str, Any], dict[str, Any]]:
    """Authenticate both sources and the original packet before comparison."""
    pmeta = load(SEALED / "IMPORT.json")
    cmeta = load(SEALED / "INDEPENDENT_IMPORT.json")
    for name, digest in PROTOCOL_HASHES.items():
        require(sha((ROOT / name).read_bytes()) == digest, "Frozen protocol changed")
    for directory, meta in [("primary", pmeta), ("independent", cmeta)]:
        for name, digest in meta["immutable_artifact_sha256"].items():
            require(sha((SEALED / directory / name).read_bytes()) == digest, name)
    for name, digest in pmeta["source_packet_sha256"].items():
        require(sha((SOURCE / name).read_bytes()) == digest, name)
    for name, digest in cmeta["immutable_artifact_sha256"].items():
        require(sha((SOURCE / name).read_bytes()) == digest, name)
    raw = gzip.decompress((SOURCE / "resources.json.gz").read_bytes())
    require(
        sha(raw) == pmeta["packet_digest_scopes"]["canonical_payload_sha256"],
        "Canonical payload seal",
    )
    payload = json.loads(raw)
    primary = load(SEALED / "primary/stage_c_review.json")
    independent = load(SEALED / "independent/stage_c_r_review.json")
    require(
        set(independent["blindness_attestation"].values()) == {"NO"}
        and len(independent["blindness_attestation"]) == 21,
        "C-R blindness attestation",
    )
    require(
        set(primary["blind_access_attestation"].values()) == {"NO"},
        "PRIMARY blindness attestation",
    )
    for key in ("case", "task_identity", "task_text", "frame"):
        require(primary[key] == independent[key] == payload[key], key)
    for a, b, original in zip(
        primary["obligations"],
        independent["obligations"],
        payload["obligations"],
        strict=True,
    ):
        require(
            {k: v for k, v in a.items() if k != "assessment"} == b == original,
            "Obligation binding",
        )
        require(
            a["assessment"]["status"]
            == next(
                x["status"]
                for x in independent["applicability"]
                if x["obligation"] == b["key"]
            )
            == "APPLICABLE",
            "Applicability",
        )
    fields = (
        "address",
        "byte_size",
        "encoding",
        "content_identity",
        "document_identity",
    )
    for a, b, original in zip(
        primary["resources"],
        independent["resources"],
        payload["resources"],
        strict=True,
    ):
        require(
            {k: a[k] for k in fields}
            == {k: b[k] for k in fields}
            == {k: original[k] for k in fields},
            "Resource frame",
        )
        require(b["text_sha256"] == sha(original["text"].encode()), "Retained text")
    require(len(payload["resources"]) == 531, "Resource universe")
    return primary, independent, payload


def span(e: dict[str, Any]) -> dict[str, Any]:
    """Retain exact support text/coordinates without reviewer provenance."""
    return {
        "origin": "TASK"
        if e.get("kind") == "task" or e.get("origin") == "TASK"
        else "RESOURCE",
        "address": e.get("address", e.get("resource_address")),
        "content_identity": e.get("content_identity"),
        "start": e["start"],
        "end": e["end"],
        "text": e["text"],
        "coordinate_system": "Unicode code points; zero-based; half-open",
    }


def normalized_units(
    p: dict[str, Any],
    c: dict[str, Any],
    payload: dict[str, Any],
) -> tuple[dict[str, Any], dict[str, Any]]:
    """Retain semantic positions and support bundles in one neutral shape."""
    cevidence = {e["id"]: e for e in c["evidence"]}
    addresses = [r["address"] for r in payload["resources"]]
    pu = {}
    for u in p["required_information_units"]:
        pu[u["identity"]] = {
            "claim": u["statement"],
            "scope": u["semantic_scope"],
            "obligations": [u["obligation"].rsplit("/", 1)[-1]],
            "necessity_rationale": u["why_necessary"],
            "supports": [
                {
                    "resources": s["resources"],
                    "mode": s["mode"],
                    "inference": s["inferability_rationale"],
                    "evidence": [span(e) for e in s["evidence"]],
                }
                for s in u["supports"]
            ],
        }
    cu = {}
    for u in c["units"]:
        cu[u["id"]] = {
            "claim": u["statement"],
            "scope": u["scope"],
            "obligations": u["obligations"],
            "necessity_rationale": u["necessity_rationale"],
            "supports": [
                {
                    "resources": [addresses[i] for i in s["resources"]],
                    "mode": s["support_mode"],
                    "inference": s["inferability_rationale"],
                    "evidence": [span(cevidence[e]) for e in s["evidence"]],
                }
                for s in u["support_bundles"]
            ],
        }
    texts = {r["address"]: r["text"] for r in payload["resources"]}
    for u in [*pu.values(), *cu.values()]:
        for s in u["supports"]:
            for e in s["evidence"]:
                text = (
                    payload["task_text"]
                    if e["origin"] == "TASK"
                    else texts[e["address"]]
                )
                require(text[e["start"] : e["end"]] == e["text"], "Support span")
    return pu, cu


def cell_metrics(pairs: list[tuple[str, str, str]]) -> dict[str, Any]:
    """Calculate every matrix and label set directly from qualified cells."""
    matrix = {a: dict.fromkeys(LABELS, 0) for a in LABELS}
    for _, a, b in pairs:
        matrix[a][b] += 1
    agreement = sum(matrix[a][a] for a in LABELS)
    sets = {
        label: overlap(
            {key for key, a, _ in pairs if a == label},
            {key for key, _, b in pairs if b == label},
        )
        for label in LABELS
    }
    n = len(pairs)
    require(sum(sum(row.values()) for row in matrix.values()) == n, "Matrix total")
    require(sum(x["primary_count"] for x in sets.values()) == n, "Row total")
    require(sum(x["c_r_count"] for x in sets.values()) == n, "Column total")
    return {
        "cells": n,
        "matrix": matrix,
        "agreement": agreement,
        "disagreement": n - agreement,
        "agreement_rate": agreement / n,
        "labels": sets,
    }


def alternatives(
    p: dict[str, Any],
    c: dict[str, Any],
    payload: dict[str, Any],
    pu: dict[str, Any],
    cu: dict[str, Any],
) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    """Keep exact all-member evidence and independent completeness/minimality."""
    addresses = [r["address"] for r in payload["resources"]]
    pa = [
        {
            "source_id": a["identity"],
            "obligation": a["obligation"].rsplit("/", 1)[-1],
            "resources": a["required_resources"],
            "units": a["required_units"],
            "claims": [pu[i] for i in a["required_units"]],
            "completeness": a["rationale_for_completeness"],
            "minimality": a["rationale_for_minimality"],
            "inference": a["inferability_assumptions"],
            "proofs": a["proof_variants"],
        }
        for a in p["alternatives"]
    ]
    ca = [
        {
            "source_id": a["id"],
            "obligation": a["obligation"],
            "resources": [addresses[i] for i in a["resources"]],
            "units": a["units"],
            "claims": [cu[i] for i in a["units"]],
            "completeness": a["completeness_rationale"],
            "minimality": a["minimality_rationale"],
            "inference": a["inferability_assumptions"],
            "proofs": a["support_relationships"],
        }
        for a in c["alternatives"]
    ]
    return pa, ca


def structure(alts: list[dict[str, Any]], obligations: list[str]) -> dict[str, Any]:
    """Enumerate all cross-obligation choices, retaining shared evidence reuse."""
    by = {o: [a for a in alts if a["obligation"] == o] for o in obligations}
    combinations = [
        {
            "alternatives": [a["source_id"] for a in combo],
            "resources": sorted(set().union(*(set(a["resources"]) for a in combo))),
            "units": sorted(set().union(*(set(a["units"]) for a in combo))),
        }
        for combo in itertools.product(*(by[o] for o in obligations))
    ]
    resource_unions = sorted({tuple(x["resources"]) for x in combinations})
    unit_unions = sorted({tuple(x["units"]) for x in combinations})
    return {
        "alternatives": len(alts),
        "complete_combinations": combinations,
        "combination_count": len(combinations),
        "sufficient_resource_unions": resource_unions,
        "sufficient_unit_unions": unit_unions,
        "resource_range": [
            min(map(len, resource_unions)),
            max(map(len, resource_unions)),
        ],
        "unit_range": [min(map(len, unit_unions)), max(map(len, unit_unions))],
        "task_indispensable_resources": sorted(
            set.intersection(*(set(x["resources"]) for x in combinations)),
        ),
        "task_indispensable_units": sorted(
            set.intersection(*(set(x["units"]) for x in combinations)),
        ),
        "obligation_indispensable": {
            o: {
                "resources": sorted(
                    set.intersection(*(set(a["resources"]) for a in by[o])),
                ),
                "units": sorted(set.intersection(*(set(a["units"]) for a in by[o]))),
            }
            for o in obligations
        },
    }


def route_categories(payload: dict[str, Any]) -> dict[str, list[str]]:
    """Identify only task-named paths and static owners from blind text."""
    task = payload["task_text"]
    literals = re.findall(r"`([^`]+)`", task)
    result: dict[str, list[str]] = {}
    for r in payload["resources"]:
        address = r["address"]
        reasons = []
        if address in literals:
            reasons.append("explicitly named task path")
        if address.startswith("src/") and address.endswith(".py"):
            module = address[4:-3].replace("/", ".")
            module = module.removesuffix(".__init__")
            if any(x == module or x.startswith(module + ".") for x in literals):
                reasons.append(
                    "task-named module or qualified declaration/method owner",
                )
            try:
                tree = ast.parse(r["text"])
            except SyntaxError:
                continue
            if any(
                isinstance(n, ast.ClassDef) and n.name in literals for n in tree.body
            ):
                reasons.append("static owner of an explicitly named class concept")
        if reasons:
            result[address] = reasons
    return result


def reconstruct() -> tuple[dict[str, Any], dict[str, bytes]]:  # noqa: C901, PLR0915 -- explicit independent scientific scopes
    """Apply the unchanged protocol and build a complete inspection surface."""
    p, c, payload = authenticate()
    pu, cu = normalized_units(p, c, payload)
    authored = load(ROOT / "ALIGNMENTS.json")
    obligations = [o["key"] for o in payload["obligations"]]
    resource = {r["address"]: r for r in payload["resources"]}

    def identity(o: str, a: str) -> str:
        return "|".join(
            (
                payload["task_identity"] + "/" + o,
                a,
                resource[a]["content_identity"],
                resource[a]["document_identity"],
            ),
        )

    pcells = {
        identity(x["obligation"].rsplit("/", 1)[-1], x["address"]): x
        for x in p["cells"]
    }
    ccells = {identity(x["obligation"], x["resource_address"]): x for x in c["cells"]}
    expected = {identity(o, a) for o in obligations for a in resource}
    require(
        len(p["cells"]) == len(pcells) == len(c["cells"]) == len(ccells) == 4779
        and set(pcells) == set(ccells) == expected,
        "Qualified cell frame",
    )
    pairs = [(k, pcells[k]["label"], ccells[k]["label"]) for k in sorted(expected)]
    metrics = cell_metrics(pairs)
    by = {
        o: cell_metrics([x for x in pairs if x[0].split("|", 1)[0].endswith("/" + o)])
        for o in obligations
    }
    cevidence = {e["id"]: e for e in c["evidence"]}
    categories = route_categories(payload)
    disputed = []
    for key, a, b in pairs:
        if a == b:
            continue
        x, y = pcells[key], ccells[key]
        address = x["address"]
        disputed.append(
            {
                "identity": key,
                "obligation": x["obligation"].rsplit("/", 1)[-1],
                "address": address,
                "primary_label": a,
                "c_r_label": b,
                "required_membership_disagreement": (a == "REQUIRED")
                != (b == "REQUIRED"),
                "route_flag": "ROUTE_FAMILY_RELEVANT_SEMANTIC_DISAGREEMENT"
                if (a == "REQUIRED") != (b == "REQUIRED") and address in categories
                else None,
                "route_reason": categories.get(address, []),
                "primary_position": {
                    "label": a,
                    "rationale": x["rationale"],
                    "inference": x["inferability_rationale"],
                    "evidence": [span(e) for e in x["evidence"]],
                },
                "c_r_position": {
                    "label": b,
                    "rationale": y["rationale"],
                    "inference": y["inferability_rationale"],
                    "evidence": [span(cevidence[e]) for e in y["evidence"]],
                },
            },
        )
    required = overlap(
        {x["address"] for x in p["cells"] if x["label"] == "REQUIRED"},
        {x["resource_address"] for x in c["cells"] if x["label"] == "REQUIRED"},
    )
    required["disputed_membership"] = {
        a: {
            "primary": sorted(
                {
                    x["obligation"].rsplit("/", 1)[-1]
                    for x in p["cells"]
                    if x["address"] == a and x["label"] == "REQUIRED"
                },
            ),
            "c_r": sorted(
                {
                    x["obligation"]
                    for x in c["cells"]
                    if x["resource_address"] == a and x["label"] == "REQUIRED"
                },
            ),
        }
        for a in sorted(
            {x["address"] for x in disputed if x["required_membership_disagreement"]},
        )
    }
    alignments = [
        {
            **row,
            "primary_positions": [pu[i] for i in row["primary_units"]],
            "c_r_positions": [cu[i] for i in row["c_r_units"]],
        }
        for row in authored["units"]
    ]
    pcovered = set().union(*(set(x["primary_units"]) for x in alignments))
    ccovered = set().union(*(set(x["c_r_units"]) for x in alignments))
    require(pcovered == set(pu) and ccovered == set(cu), "Unit alignment coverage")
    pa, ca = alternatives(p, c, payload, pu, cu)
    ps, cs = structure(pa, obligations), structure(ca, obligations)
    pstats = load(SEALED / "primary/stage_c_statistics.json")
    cstats = load(SEALED / "independent/stage_c_r_statistics.json")
    for s, stats in [(ps, pstats), (cs, cstats)]:
        require(
            s["combination_count"] == stats["complete_task_combination_count"],
            "Combinations",
        )
        require(
            len(s["sufficient_resource_unions"])
            == stats["distinct_sufficient_resource_union_count"],
            "Resource unions",
        )
        require(
            len(s["sufficient_unit_unions"])
            == stats["distinct_sufficient_unit_union_count"],
            "Unit unions",
        )
        require(
            s["resource_range"]
            == [
                stats["minimum_sufficient_resource_count"],
                stats["maximum_sufficient_resource_count"],
            ],
            "Resource range",
        )
        require(
            s["unit_range"]
            == [
                stats["minimum_sufficient_unit_count"],
                stats["maximum_sufficient_unit_count"],
            ],
            "Unit range",
        )
    require(
        ps["task_indispensable_resources"] == pstats["task_indispensable_resources"],
        "PRIMARY intersection",
    )
    addresses = [r["address"] for r in payload["resources"]]
    require(
        cs["task_indispensable_resources"]
        == sorted(addresses[i] for i in cstats["task_indispensable"]["resources"]),
        "C-R intersection",
    )
    # Independently check every obligation's intersection against sealed values.
    for o in obligations:
        require(
            ps["obligation_indispensable"][o]
            == p["witness_structure"]["obligation_indispensable"][o],
            "PRIMARY obligation intersection",
        )
        ci = cstats["obligation_indispensable"][o]
        require(
            cs["obligation_indispensable"][o]
            == {
                "resources": sorted(addresses[i] for i in ci["resources"]),
                "units": sorted(ci["units"]),
            },
            "C-R obligation intersection",
        )
    require(
        ps["task_indispensable_units"]
        == p["witness_structure"]["task_indispensable_units"],
        "PRIMARY unit intersection",
    )
    require(
        cs["task_indispensable_units"] == cstats["task_indispensable"]["units"],
        "C-R unit intersection",
    )
    for alts, cells, unit_values in [(pa, p["cells"], pu), (ca, c["cells"], cu)]:
        cell_resources = {
            x.get("address", x.get("resource_address"))
            for x in cells
            if x["label"] == "REQUIRED"
        }
        require(
            set().union(*(set(a["resources"]) for a in alts)) == cell_resources,
            "REQUIRED alternative union",
        )
        require(
            set().union(*(set(a["units"]) for a in alts)) == set(unit_values),
            "Necessary unit alternatives",
        )

    def project_units(ids: list[str], side: str) -> set[str]:
        projected = set()
        field = "primary_units" if side == "PRIMARY" else "c_r_units"
        for unit in ids:
            equivalents = [
                x["identity"]
                for x in alignments
                if unit in x[field]
                and x["classification"] == "SUBSTANTIALLY_EQUIVALENT"
            ]
            projected.update(equivalents or [side + "/" + unit])
        return projected

    aligned_structures: dict[str, dict[str, Any]] = {}
    for side, s in [("PRIMARY", ps), ("C-R", cs)]:
        unions = sorted(
            {
                tuple(sorted(project_units(list(ids), side)))
                for ids in s["sufficient_unit_unions"]
            },
        )
        aligned_structures[side] = {
            "sufficient_unit_unions": unions,
            "unit_range": [min(map(len, unions)), max(map(len, unions))],
            "task_indispensable_units": sorted(
                project_units(s["task_indispensable_units"], side),
            ),
            "obligation_indispensable_units": {
                o: sorted(
                    project_units(s["obligation_indispensable"][o]["units"], side),
                )
                for o in obligations
            },
        }
    aligned_unit_comparison = {
        "method": "Only SUBSTANTIALLY_EQUIVALENT rows share a neutral proposition identity. Uncertain, broader and unmatched units retain source-local tokens; equality is not forced. Counts reflect proposed grouping, not reconciled facts.",
        "sources": aligned_structures,
        "task_indispensable": overlap(
            set(aligned_structures["PRIMARY"]["task_indispensable_units"]),
            set(aligned_structures["C-R"]["task_indispensable_units"]),
        ),
        "per_obligation": {
            o: overlap(
                set(aligned_structures["PRIMARY"]["obligation_indispensable_units"][o]),
                set(aligned_structures["C-R"]["obligation_indispensable_units"][o]),
            )
            for o in obligations
        },
    }
    witness_pairs = []
    for a, b in itertools.product(pa, ca):
        if a["obligation"] != b["obligation"]:
            continue
        exact = set(a["resources"]) == set(b["resources"])
        rows = [
            x
            for x in alignments
            if any(
                a["obligation"] in u["obligations"]
                for u in x["primary_positions"] + x["c_r_positions"]
            )
        ]
        equivalent = all(
            x["classification"] == "SUBSTANTIALLY_EQUIVALENT" for x in rows
        )
        witness_pairs.append(
            {
                "primary": a["source_id"],
                "c_r": b["source_id"],
                "obligation": a["obligation"],
                "exact_resource_set_match": exact,
                "classification": "SUBSTANTIALLY_EQUIVALENT"
                if equivalent
                else "PARTIAL_OVERLAP",
                "evidence_sets": overlap(set(a["resources"]), set(b["resources"])),
                "aligned_rows": [x["identity"] for x in rows],
                "rationale": "Shared necessary claims subject to the cited unit hypotheses; equal resource sets alone do not establish equal witness semantics. ALL-member complementarity, admissible inference, completeness and minimality remain in both original positions.",
            },
        )
    pexact = {x["primary"] for x in witness_pairs if x["exact_resource_set_match"]}
    cexact = {x["c_r"] for x in witness_pairs if x["exact_resource_set_match"]}
    pdistinct = {encoded(x).decode() for x in ps["sufficient_resource_unions"]}
    cdistinct = {encoded(x).decode() for x in cs["sufficient_resource_unions"]}
    necessity_rows = [
        x
        for x in alignments
        if x["classification"]
        in {"PRIMARY_BROADER", "C_R_BROADER", "NO_SEMANTIC_MATCH"}
    ]
    uncertain = [
        x["identity"]
        for x in alignments
        if x["classification"]
        in {"PARTIAL_OVERLAP", "AMBIGUOUS_ALIGNMENT", "NO_SEMANTIC_MATCH"}
    ]
    pl = {x["identity"]: x for x in p["interpretation_limitations"]}
    cl = {x["id"]: x for x in c["limitations"]}
    limits = [
        {
            **row,
            "primary_positions": [pl[i] for i in row["primary"]],
            "c_r_positions": [cl[i] for i in row["c_r"]],
        }
        for row in authored["limitations"]
    ]
    require(
        set().union(*(set(x["primary"]) for x in limits)) == set(pl)
        and set().union(*(set(x["c_r"]) for x in limits)) == set(cl),
        "Limitation coverage",
    )
    gap_status = {
        "primary": {
            "TASK_GAP": p["task_gap"]["status"],
            "REPOSITORY_INFORMATION_GAP": p["repository_information_gap"]["status"],
            "TASK_INTERPRETATION_GAP": "NONE"
            if not p["task_interpretation_gaps"]
            else "PRESENT",
        },
        "c_r": {x["kind"]: x["status"] for x in c["gap_assessments"]},
    }
    severe: dict[str, dict[str, Any]] = {
        "qualified_REQUIRED_membership": {
            "trigger": any(x["required_membership_disagreement"] for x in disputed),
            "evidence": [
                x["identity"] for x in disputed if x["required_membership_disagreement"]
            ],
        },
        "substantive_task_or_repository_gap": {
            "trigger": gap_status["primary"] != gap_status["c_r"],
            "evidence": gap_status,
        },
        "added_omitted_necessary_unit": {
            "trigger": bool(necessity_rows),
            "evidence": [x["identity"] for x in necessity_rows],
            "qualification": "Explicit necessary-unit scope differences; not a reconciled determination of which claims are necessary.",
        },
        "complete_sufficient_resource_alternative_or_union": {
            "trigger": pdistinct != cdistinct,
            "evidence": overlap(pdistinct, cdistinct),
        },
        "witness_admission_inference_or_indispensability": {
            "trigger": ps["task_indispensable_resources"]
            != cs["task_indispensable_resources"]
            or any(x["reconciliation_needed"] for x in alignments),
            "evidence": "UA009, UA013, UA014, UA018, UA022, UA023, UA028, UA029; exact obligation and task intersections below",
        },
        "limitation_changes_feasibility_ownership_admissibility": {
            "trigger": None,
            "evidence": ["LA004", "LA005"],
            "qualification": "Uncertain cross-layer constraint equivalence; not silently classified equal or resolved.",
        },
        "applicability_changes_necessity_or_sufficiency": {
            "trigger": False,
            "evidence": "All nine identical applicable obligations",
        },
    }
    has_severe = any(x["trigger"] is True for x in severe.values())
    high = {
        "no_severe_trigger": not has_severe,
        "identical_applicability": True,
        "no_unresolved_cells": metrics["labels"]["UNRESOLVED"]["union_count"] == 0,
        "no_uncertain_semantic_alignments": not uncertain
        and not any(x["reconciliation_needed"] for x in limits),
        "equal_aligned_necessity": not necessity_rows and not uncertain,
        "equal_witness_sufficiency_indispensability": pdistinct == cdistinct
        and ps["task_indispensable_resources"] == cs["task_indispensable_resources"],
        "equal_substantive_gaps_constraints": gap_status["primary"] == gap_status["c_r"]
        and not any(x["reconciliation_needed"] for x in limits),
        "REQUIRED_Jaccard_eq_1": metrics["labels"]["REQUIRED"]["jaccard"] == 1,
        "overall_agreement_ge_0.98": metrics["agreement_rate"] >= 0.98,
        "every_obligation_agreement_ge_0.95": all(
            x["agreement_rate"] >= 0.95 for x in by.values()
        ),
        "HELPFUL_ONLY_Jaccard_ge_0.90": metrics["labels"]["HELPFUL_ONLY"]["jaccard"]
        >= 0.90,
    }
    outcome = (
        "SEVERE_ARCHITECTURE_RELEVANT_DISAGREEMENT"
        if has_severe
        else ("HIGH_RELIABILITY" if all(high.values()) else "MATERIAL_DISAGREEMENT")
    )
    result = {
        "schema": "case-0012-reliability-comparison-v1",
        "authority": "Neither PRIMARY nor C-R is truth; no reconciled unit or winner is created.",
        "authentication": load(SEALED / "INDEPENDENT_IMPORT.json"),
        "primary_source": load(SEALED / "IMPORT.json"),
        "protocol_sha256": PROTOCOL_HASHES,
        "case": payload["case"],
        "task_identity": payload["task_identity"],
        "task_text": payload["task_text"],
        "frame": payload["frame"],
        "frame_alignment": {
            "resources": 531,
            "qualified_cells": 4779,
            "obligations": 9,
            "duplicate": 0,
            "missing": 0,
            "unexpected": 0,
            "applicability": "IDENTICAL",
        },
        "overall": metrics,
        "per_obligation": by,
        "disputed_cells": disputed,
        "required_resources": required,
        "unit_alignments": alignments,
        "unit_alignment_statistics": {
            "primary_units": len(pu),
            "c_r_units": len(cu),
            "primary_mapped": len(pcovered),
            "c_r_mapped": len(ccovered),
            "primary_candidate_aligned": len(
                {i for x in alignments if x["c_r_units"] for i in x["primary_units"]},
            ),
            "c_r_candidate_aligned": len(
                {i for x in alignments if x["primary_units"] for i in x["c_r_units"]},
            ),
            "primary_substantially_equivalent_coverage": len(
                {
                    i
                    for x in alignments
                    if x["classification"] == "SUBSTANTIALLY_EQUIVALENT"
                    for i in x["primary_units"]
                },
            ),
            "c_r_substantially_equivalent_coverage": len(
                {
                    i
                    for x in alignments
                    if x["classification"] == "SUBSTANTIALLY_EQUIVALENT"
                    for i in x["c_r_units"]
                },
            ),
            "classification_counts": dict(
                Counter(x["classification"] for x in alignments),
            ),
            "primary_without_semantic_match": sorted(
                {
                    i
                    for x in alignments
                    if not x["c_r_units"]
                    for i in x["primary_units"]
                },
            ),
            "c_r_without_semantic_match": sorted(
                {
                    i
                    for x in alignments
                    if not x["primary_units"]
                    for i in x["c_r_units"]
                },
            ),
            "uncertain_rows": uncertain,
            "interpretation": "52 versus 34 is a mixture: pure grouping in tests/common guards, cross-obligation reuse, task versus repository evidence, extra current-contract necessity and uncertain admission equivalence. It is not demonstrated to be wording-only.",
        },
        "alternatives": {
            "primary": pa,
            "c_r": ca,
            "candidate_pairs": witness_pairs,
            "exact_resource_set_pair_count": sum(
                x["exact_resource_set_match"] for x in witness_pairs
            ),
            "semantic_equivalent_different_evidence": [
                x
                for x in witness_pairs
                if x["classification"] == "SUBSTANTIALLY_EQUIVALENT"
                and not x["exact_resource_set_match"]
            ],
            "primary_without_exact_resource_match": [
                a["source_id"] for a in pa if a["source_id"] not in pexact
            ],
            "c_r_without_exact_resource_match": [
                a["source_id"] for a in ca if a["source_id"] not in cexact
            ],
        },
        "sufficiency": {
            "aligned_units": aligned_unit_comparison,
            "primary": ps,
            "c_r": cs,
            "resource_unions": overlap(pdistinct, cdistinct),
            "task_indispensable_resources": overlap(
                set(ps["task_indispensable_resources"]),
                set(cs["task_indispensable_resources"]),
            ),
            "obligation_indispensability": {
                o: overlap(
                    set(ps["obligation_indispensable"][o]["resources"]),
                    set(cs["obligation_indispensable"][o]["resources"]),
                )
                for o in obligations
            },
            "unit_semantics": "Raw IDs are source-local. Proposed semantic coverage is exposed in unit_alignments. Full mapped coverage does not establish semantic equality; uncertain/broader/unmatched rows remain open.",
        },
        "gaps": gap_status,
        "limitations": limits,
        "severe_gates": severe,
        "high_gates": high,
        "outcome": outcome,
        "reconciliation_required": outcome != "HIGH_RELIABILITY",
        "stage_d": "BLOCKED",
        "status": {
            "PRIMARY_Stage_C": "COMPLETE",
            "independent_C_R": "COMPLETE",
            "reliability_comparison": "COMPLETE",
            "reviewed_reconciled_gold": "NOT AVAILABLE",
            "U2_effectiveness": "UNKNOWN",
            "final_U2_outcome": "NOT_SELECTED",
            "U3": "FUTURE",
            "R1.7": "RETAINED",
            "R2_true_BM25F": "MANDATORY",
        },
        "cohens_kappa": "Not computed: frozen protocol does not require it; class-wise exact sets remain primary descriptive evidence.",
        "access": {
            "Stage_B_contents": "NONE",
            "treatment_join": "NONE",
            "confirmation_reserve": "NONE",
            "reconciliation_performed": False,
        },
    }
    outputs = {
        "COMPARISON.json": encoded(result),
        "RELIABILITY_REVIEW.md": human(result),
    }
    return result, outputs


def human(result: dict[str, Any]) -> bytes:
    """Expose every disagreement and original position in readable sections."""
    lines = [
        "# Case 0012 blind-gold reliability review",
        "",
        result["outcome"],
        "",
        "Neither source is truth. Stage D is BLOCKED. U2 effectiveness UNKNOWN; final outcome NOT_SELECTED.",
        "This repository-side publication is not a blind reviewer. Semantic hypotheses are not reconciled gold.",
        "",
    ]
    sections = [
        (
            "Source authentication, physical hashes and blindness attestations",
            {
                "independent": result["authentication"],
                "primary": result["primary_source"],
                "frozen_protocol": result["protocol_sha256"],
            },
        ),
        (
            "Exact task and aligned frame",
            {
                k: result[k]
                for k in [
                    "case",
                    "task_identity",
                    "task_text",
                    "frame",
                    "frame_alignment",
                ]
            },
        ),
        ("Complete confusion matrix and every label set", result["overall"]),
        (
            "Per-obligation matrix, agreement and every label set",
            result["per_obligation"],
        ),
        (
            "REQUIRED resource unions and exact disputed obligation membership",
            result["required_resources"],
        ),
        (
            "Every disputed qualified cell, exact rationale and spans",
            result["disputed_cells"],
        ),
        ("Neutral unit alignment statistics", result["unit_alignment_statistics"]),
        (
            "Every unit alignment, original claims, scope, support and inference",
            result["unit_alignments"],
        ),
        (
            "Alternative/witness alignments and original completeness/minimality",
            result["alternatives"],
        ),
        (
            "Complete sufficiency combinations/unions and indispensability",
            result["sufficiency"],
        ),
        ("Independent gaps", result["gaps"]),
        ("Every limitation alignment", result["limitations"]),
        ("Every frozen severe gate", result["severe_gates"]),
        ("Every frozen HIGH gate", result["high_gates"]),
        (
            "Outcome, status and access boundaries",
            {
                k: result[k]
                for k in [
                    "outcome",
                    "stage_d",
                    "reconciliation_required",
                    "status",
                    "access",
                    "cohens_kappa",
                ]
            },
        ),
    ]
    # Full exact-set output is intentionally inspectable rather than truncated.
    for title, value in sections:
        lines.extend(
            ["## " + title, "", "```json", encoded(value).decode().rstrip(), "```", ""],
        )
    return ("\n".join(lines).rstrip() + "\n").encode()


def main() -> None:
    """Publish once, or reconstruct every comparison byte without mutation."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("mode", choices=("build", "verify"))
    args = parser.parse_args()
    result, outputs = reconstruct()
    _, again = reconstruct()
    require(outputs == again, "Deterministic double reconstruction")
    if args.mode == "build":
        require(
            not any((ROOT / name).exists() for name in outputs),
            "Overwrite refused",
        )
        for name, raw in outputs.items():
            with (ROOT / name).open("xb") as stream:
                stream.write(raw)
    else:
        for name, raw in outputs.items():
            require((ROOT / name).read_bytes() == raw, "Deterministic replay: " + name)
    sys.stdout.write(
        json.dumps(
            {
                "status": "PASS",
                "outcome": result["outcome"],
                "agreement": result["overall"]["agreement"],
                "disagreement": result["overall"]["disagreement"],
                "required_resource_overlap": {
                    k: result["required_resources"][k]
                    for k in ["intersection_count", "union_count", "jaccard"]
                },
                "sha256": {name: sha(raw) for name, raw in outputs.items()},
            },
            indent=2,
        )
        + "\n",
    )


if __name__ == "__main__":
    main()
