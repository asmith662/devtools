"""Bounded packet-only comparison; no adjudication, acquisition or Stage D join."""

from __future__ import annotations

import argparse
import gzip
import hashlib
import itertools
import json
from collections import Counter
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parent
BASE = ROOT.parent
PAIR_LABELS = ["DIRECTLY_COVERS", "PARTIALLY_COVERS", "DOES_NOT_COVER", "AMBIGUOUS"]
UNIT_LABELS = ["COVERED", "PARTIAL_ONLY", "UNCOVERED", "AMBIGUOUS_ONLY"]
NEED_LABELS = [
    "NECESSARY",
    "USEFUL_REDUNDANT",
    "PARTIAL_ONLY",
    "UNNECESSARY",
    "MISFORMULATED",
    "AMBIGUOUS",
]
GRANULARITY = [
    "ATOMIC_FOR_NEED_MAPPING",
    "COLLECTIVELY_COVERABLE",
    "OVERCOMPOUND_FOR_PAIRWISE_MAPPING",
    "AMBIGUOUS_GRANULARITY",
]
DECISIONS = [
    "ACCEPT_POSITION_1",
    "ACCEPT_POSITION_2",
    "REPLACE_WITH_RECONCILED_JUDGMENT",
    "UNRESOLVED",
]


def encode(value: Any) -> bytes:
    return (
        json.dumps(value, sort_keys=True, indent=2, ensure_ascii=False) + "\n"
    ).encode()


def digest(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def read(path: Path) -> Any:
    return json.loads(path.read_bytes())


def exclusive(path: Path, raw: bytes) -> None:
    with path.open("xb") as stream:
        stream.write(raw)


def index(rows: list[dict[str, Any]], key: str) -> dict[str, Any]:
    result = {r[key]: r for r in rows}
    assert len(result) == len(rows), f"duplicate {key}"
    return result


def pair_index(rows: list[dict[str, Any]]) -> dict[tuple[str, str], Any]:
    result = {(r["need"], r["unit"]): r for r in rows}
    assert len(result) == len(rows), "duplicate pair"
    return result


def matrix(rows: list[tuple[str, str]], labels: list[str]) -> dict[str, Any]:
    counts = Counter(rows)
    assert all(a in labels and b in labels for a, b in rows)
    table = [[counts[a, b] for b in labels] for a in labels]
    total = len(rows)
    agreed = sum(table[i][i] for i in range(len(labels)))
    chance = (
        sum(sum(table[i]) * sum(row[i] for row in table) for i in range(len(labels)))
        / total**2
    )
    return {
        "rows": labels,
        "columns": labels,
        "matrix": table,
        "total": total,
        "agreement_count": agreed,
        "disagreement_count": total - agreed,
        "agreement_fraction": agreed / total,
        "expected_chance_agreement": chance,
        "descriptive_cohens_kappa": (agreed / total - chance) / (1 - chance)
        if chance < 1
        else None,
    }


def set_stats(left: set[Any], right: set[Any]) -> dict[str, Any]:
    common, union = left & right, left | right
    return {
        "primary_count": len(left),
        "review_count": len(right),
        "intersection": len(common),
        "union": len(union),
        "jaccard": len(common) / len(union) if union else None,
        "primary_retained_by_review": len(common) / len(left) if left else None,
        "review_retained_by_primary": len(common) / len(right) if right else None,
        "primary_only": sorted(left - right),
        "review_only": sorted(right - left),
    }


def claim_pair(row: dict[str, Any], primary: bool) -> dict[str, Any]:
    result = {
        "label": row["label"],
        "rationale": row["rationale"],
        "fact_sought": row["need_fact_sought" if primary else "fact_sought"],
        "fact_established": row[
            "unit_fact_established" if primary else "fact_established_by_unit"
        ],
    }
    # Preserve all supplied partial-facet explanation without source-specific field names.
    for name in ("covered_part", "missing_part"):
        if name in row:
            result[name] = row[name]
    return result


def load() -> dict[str, Any]:
    packet = json.loads(gzip.decompress((BASE / "packet.json.gz").read_bytes()))
    manifest = read(BASE / "manifest.json")
    review = read(ROOT / "c5r_v1_adjudication.json")
    provenance = read(BASE / "results/c5_method_provenance_v1.json")
    mappings = read(BASE / "results/c5_mappings_v1.json")["mappings"]
    units = read(BASE / "results/c5_unit_coverage_v1.json")["units"]
    needs = read(BASE / "results/c5_need_classifications_v1.json")["needs"]
    assert review["frozen_packet"] == packet, "semantic frame mismatch"
    assert review["manifest"] == manifest, "manifest mismatch"
    assert packet["frame"] == manifest["frame"] == provenance["frame"]
    assert provenance["decompressed_payload_sha256"] == digest(
        gzip.decompress((BASE / "packet.json.gz").read_bytes())
    )
    for name, sha in provenance["input_sha256"].items():
        assert digest((BASE / name).read_bytes()) == sha == review["input_sha256"][name]
    for key in ("reviewed_gold_sha256", "frozen_needs_sha256"):
        assert provenance["bindings"][key] == manifest[key]
    ns = index(packet["information_needs"], "identity")
    us = index(packet["units"], "identity")
    p, r = pair_index(mappings), pair_index(review["pairs"])
    expected = set(itertools.product(ns, us))
    assert len(expected) == 576 and set(p) == set(r) == expected
    pu, ru = index(units, "unit"), index(review["unit_coverage"], "unit")
    pn, rn = index(needs, "need"), index(review["need_classifications"], "need")
    assert set(pu) == set(ru) == set(us) and len(us) == 32
    assert set(pn) == set(rn) == set(ns) and len(ns) == 18
    for (n, u), row in p.items():
        assert row["need_fact_sought"] == ns[n]["statement"]
        assert row["unit_fact_established"] == us[u]["statement"]
        assert r[n, u]["need_statement"] == ns[n]["statement"]
        assert r[n, u]["unit_statement"] == us[u]["statement"]
    for u, row in pu.items():
        assert row["statement"] == us[u]["statement"]
        assert row["obligations"] == us[u]["obligations"]
        assert row["alternative_membership"] == us[u]["alternative_membership"]
    for n, row in pn.items():
        assert row["statement"] == rn[n]["statement"] == ns[n]["statement"]
        assert row["obligation"] == ns[n]["obligation"]
    for pairs, coverage in ((p, pu), (r, ru)):
        for u, row in coverage.items():
            labels = {pairs[n, u]["label"] for n in ns}
            status = next(
                (
                    s
                    for label, s in zip(PAIR_LABELS[:2], UNIT_LABELS[:2], strict=True)
                    if label in labels
                ),
                "AMBIGUOUS_ONLY" if "AMBIGUOUS" in labels else "UNCOVERED",
            )
            assert row["status"] == status
            for field, label in (
                ("direct_needs", "DIRECTLY_COVERS"),
                ("partial_needs", "PARTIALLY_COVERS"),
                ("ambiguous_needs", "AMBIGUOUS"),
            ):
                assert set(row[field]) == {
                    n for n in ns if pairs[n, u]["label"] == label
                }
    alternatives = {
        a["identity"]: {**a, "obligation": group["obligation"]}
        for group in packet["alternatives"]
        for a in group["alternatives"]
    }
    ra = index(review["alternative_coverage"], "alternative")
    assert len(alternatives) == len(ra) == 12 and set(alternatives) == set(ra)
    for a, row in ra.items():
        assert row["units"] == alternatives[a]["units"]
        assert row["obligation"] == alternatives[a]["obligation"]
        assert (
            row["member_logic"]
            == alternatives[a]["member_logic"]
            == "ALL_COMPLEMENTARY"
        )
    granularity = index(review["unit_granularity"], "unit")
    assert set(granularity) == set(us)
    for u, row in granularity.items():
        assert (
            row["statement"] == us[u]["statement"]
            and row["category"] in GRANULARITY
            and row["rationale"]
        )
    collective = index(review["collective_coverage"], "unit")
    assert set(collective) == {
        u
        for u, row in granularity.items()
        if row["category"] == "COLLECTIVELY_COVERABLE"
    }
    for u, row in collective.items():
        assert row["diagnostic_only"] and row["rationale"] and row["minimality"]
        sets = [frozenset(s) for s in row["minimal_need_sets"]]
        assert sets and len(sets) == len(set(sets))
        assert all(len(s) >= 2 and s <= ns.keys() for s in sets)
        assert all(not a < b for a in sets for b in sets)
        for need_set in sets:
            for n in need_set:
                pair = r[n, u]
                assert (
                    pair["label"] == "PARTIALLY_COVERS"
                    and pair["covered_part"]
                    and pair["missing_part"]
                )
                assert pair["covered_part"] != pair["missing_part"]
    return {
        "packet": packet,
        "manifest": manifest,
        "review": review,
        "p": p,
        "r": r,
        "pu": pu,
        "ru": ru,
        "pn": pn,
        "rn": rn,
        "ns": ns,
        "us": us,
        "alternatives": alternatives,
        "ra": ra,
        "granularity": granularity,
        "collective": collective,
    }


def build(data: dict[str, Any] | None = None) -> dict[str, Any]:
    d = data or load()
    p, r = d["p"], d["r"]
    stats = {
        label: set_stats(
            {k for k in p if p[k]["label"] == label},
            {k for k in r if r[k]["label"] == label},
        )
        for label in PAIR_LABELS
    }
    direct_groups: dict[str, Any] = {}
    selectors = {
        "need": {n: {(n, u) for u in d["us"]} for n in d["ns"]},
        "unit": {u: {(n, u) for n in d["ns"]} for u in d["us"]},
        "obligation": {
            o["identity"]: {
                k for k in p if o["identity"] in d["us"][k[1]]["obligations"]
            }
            for o in d["packet"]["obligations"]
        },
        "need_obligation": {
            o["identity"]: {
                k for k in p if o["identity"] == d["ns"][k[0]]["obligation"]
            }
            for o in d["packet"]["obligations"]
        },
        "alternative": {
            a: {k for k in p if k[1] in row["units"]}
            for a, row in d["alternatives"].items()
        },
    }
    for kind, groups in selectors.items():
        direct_groups[kind] = {
            name: set_stats(
                {k for k in group if p[k]["label"] == "DIRECTLY_COVERS"},
                {k for k in group if r[k]["label"] == "DIRECTLY_COVERS"},
            )
            for name, group in groups.items()
        }
    unit_rows = []
    for u in d["us"]:
        unit_rows.append(
            {
                **d["us"][u],
                "primary": d["pu"][u],
                "review": d["ru"][u],
                "mapping_rationales": [
                    {
                        "need": n,
                        "primary": claim_pair(p[n, u], True),
                        "review": claim_pair(r[n, u], False),
                    }
                    for n in d["ns"]
                    if p[n, u]["label"] != "DOES_NOT_COVER"
                    or r[n, u]["label"] != "DOES_NOT_COVER"
                ],
            }
        )
    need_rows = [
        {**d["ns"][n], "primary": d["pn"][n], "review": d["rn"][n]} for n in d["ns"]
    ]
    collective_rows = []
    for u, row in d["collective"].items():
        collective_rows.append(
            {
                **row,
                "statement": d["us"][u]["statement"],
                "strict_status": d["ru"][u]["status"],
                "sets": [
                    {
                        "needs": need_set,
                        "member_necessity": [
                            {
                                "need": n,
                                "covered_part": r[n, u]["covered_part"],
                                "missing_without_others": r[n, u]["missing_part"],
                            }
                            for n in need_set
                        ],
                        "sufficiency_rationale": row["rationale"],
                        "minimality_rationale": row["minimality"],
                    }
                    for need_set in row["minimal_need_sets"]
                ],
            }
        )
    primary_direct = {u for u in d["us"] if d["pu"][u]["status"] == "COVERED"}
    review_direct = {u for u in d["us"] if d["ru"][u]["status"] == "COVERED"}
    diagnostic = review_direct | set(d["collective"])
    alternatives = []
    for a, original in d["alternatives"].items():
        members = set(original["units"])
        rr = d["ra"][a]
        expected_status = (
            "FULLY_DIRECTLY_COVERED"
            if members <= review_direct
            else "FULLY_COVERED_ONLY_COLLECTIVELY"
            if members <= diagnostic
            else "AMBIGUOUS"
            if any(
                d["ru"][u]["status"] == "AMBIGUOUS_ONLY" for u in members - diagnostic
            )
            else "INCOMPLETE"
        )
        assert rr["status"] == expected_status
        assert set(rr["directly_covered_members"]) == members & review_direct
        assert set(rr["collectively_covered_members"]) == (
            members - review_direct
        ) & set(d["collective"])
        assert set(rr["incomplete_members"]) == members - diagnostic
        alternatives.append(
            {
                **original,
                "primary_direct_complete": members <= primary_direct,
                "review_direct_complete": members <= review_direct,
                "primary_missing_direct_members": sorted(members - primary_direct),
                "review_missing_direct_members": sorted(members - review_direct),
                "review": rr,
                "member_causes": [
                    {
                        "unit": u,
                        "statement": d["us"][u]["statement"],
                        "primary": d["pu"][u]["status"],
                        "review": d["ru"][u]["status"],
                        "granularity": d["granularity"][u]["category"],
                    }
                    for u in original["units"]
                ],
            }
        )
    disagreements = [
        {
            "need": n,
            "unit": u,
            "need_statement": d["ns"][n]["statement"],
            "unit_statement": d["us"][u]["statement"],
            "primary": claim_pair(p[n, u], True),
            "review": claim_pair(r[n, u], False),
        }
        for n, u in p
        if p[n, u]["label"] != r[n, u]["label"]
    ]
    direct_rationales = [
        {
            "need": n,
            "unit": u,
            "primary": claim_pair(p[n, u], True),
            "review": claim_pair(r[n, u], False),
        }
        for n, u in p
        if p[n, u]["label"] == r[n, u]["label"] == "DIRECTLY_COVERS"
        and claim_pair(p[n, u], True) != claim_pair(r[n, u], False)
    ]
    failures = {
        "INFORMATION_NEED_COVERAGE_FAILURE": {
            "evidence": "ESTABLISHED",
            "scope": "Both reviewers fail the frozen every-unit direct rule; exact failed membership is disputed. This is not a retrieval or effectiveness result.",
            "metrics": {
                "primary_missing_direct": len(d["us"]) - len(primary_direct),
                "review_missing_direct": len(d["us"]) - len(review_direct),
            },
        },
        "UNDER_SPECIFIED_INFORMATION_NEEDS": {
            "evidence": "POSSIBLE",
            "scope": "The three overcompound propositions identify purpose, admission and execution facets absent from the questions, but neither reviewer classifies a need MISFORMULATED or AMBIGUOUS. Broader intent versus unit bundling remains unresolved.",
            "metrics": {
                "primary_misformulated_or_ambiguous": sum(
                    x["classification"] in ("MISFORMULATED", "AMBIGUOUS")
                    for x in d["pn"].values()
                ),
                "review_misformulated_or_ambiguous": sum(
                    x["label"] in ("MISFORMULATED", "AMBIGUOUS")
                    for x in d["rn"].values()
                ),
            },
        },
        "UNDER_DECOMPOSED_NEED_SET": {
            "evidence": "SUPPORTED",
            "scope": "Three units have unrequested admission/execution facets and three other atomic units remain partial-only. Missing focused questions are plausible, but no need-set repair or attribution is selected.",
            "metrics": {
                "review_overcompound": sum(
                    x["category"] == "OVERCOMPOUND_FOR_PAIRWISE_MAPPING"
                    for x in d["granularity"].values()
                ),
                "review_atomic_partial_only": sum(
                    d["ru"][u]["status"] == "PARTIAL_ONLY"
                    and row["category"] == "ATOMIC_FOR_NEED_MAPPING"
                    for u, row in d["granularity"].items()
                ),
            },
        },
        "NEED_TO_UNIT_GRANULARITY_MISMATCH": {
            "evidence": "SUPPORTED",
            "scope": "Independent diagnostic proposes six collectively coverable and three overcompound units. Collective proofs are structurally validated semantic claims awaiting confirmation, not reviewed truth.",
            "metrics": {
                "collective_units": len(d["collective"]),
                "minimal_sets": sum(
                    len(x["minimal_need_sets"]) for x in d["collective"].values()
                ),
                "strict_review_covered": len(review_direct),
                "diagnostic_review_covered": len(diagnostic),
            },
        },
        "C5_SEMANTIC_ADJUDICATION_INSTABILITY": {
            "evidence": "ESTABLISHED",
            "scope": "Observed disagreements affect direct facts, required-unit coverage, need necessity and whole alternatives; class imbalance cannot make this architecture-safe.",
            "metrics": {
                "pair_disagreements": len(disagreements),
                "direct_intersection": stats["DIRECTLY_COVERS"]["intersection"],
                "direct_union": stats["DIRECTLY_COVERS"]["union"],
                "unit_disagreements": sum(
                    x["primary"]["status"] != x["review"]["status"] for x in unit_rows
                ),
                "need_disagreements": sum(
                    x["primary"]["classification"] != x["review"]["label"]
                    for x in need_rows
                ),
            },
        },
    }
    return {
        "schema": "case-0011-c5-reliability-v1",
        "frame_alignment": {
            "case_and_task": d["packet"]["frame"],
            "obligations": len(d["packet"]["obligations"]),
            "needs": 18,
            "units": 32,
            "pairs": 576,
            "alternatives": 12,
            "duplicate_pairs": 0,
            "missing_pairs": 0,
            "unexpected_pairs": 0,
            "semantic_packet_equal": True,
            "bindings": {
                k: d["manifest"][k]
                for k in ("frozen_needs_sha256", "reviewed_gold_sha256")
            },
            "binding_limit": "Authenticated source declarations; no invented preimage hashing.",
        },
        "pair_comparison": matrix(
            [(p[k]["label"], r[k]["label"]) for k in p], PAIR_LABELS
        ),
        "per_label": stats,
        "direct_by_owner": direct_groups,
        "pair_disagreements": disagreements,
        "agreed_direct_rationale_comparisons": direct_rationales,
        "unit_comparison": matrix(
            [(x["primary"]["status"], x["review"]["status"]) for x in unit_rows],
            UNIT_LABELS,
        ),
        "units": unit_rows,
        "need_comparison": matrix(
            [(x["primary"]["classification"], x["review"]["label"]) for x in need_rows],
            NEED_LABELS,
        ),
        "needs": need_rows,
        "alternative_direct_comparison": matrix(
            [
                (
                    "COMPLETE" if x["primary_direct_complete"] else "INCOMPLETE",
                    "COMPLETE" if x["review_direct_complete"] else "INCOMPLETE",
                )
                for x in alternatives
            ],
            ["COMPLETE", "INCOMPLETE"],
        ),
        "alternatives": alternatives,
        "granularity_counts": {
            k: sum(x["category"] == k for x in d["granularity"].values())
            for k in GRANULARITY
        },
        "granularity": list(d["granularity"].values()),
        "collective": collective_rows,
        "collective_validation_limit": "Every proposed set has unique frozen members, partial facets, nonempty sufficiency and singleton-removal rationales, and no subset redundancy. This validates the semantic proof structure, not semantic truth; fresh reconciliation must confirm sufficiency and minimality.",
        "coverage": {
            "primary_strict_direct": len(primary_direct),
            "review_strict_direct": len(review_direct),
            "total_units": len(d["us"]),
            "review_granularity_aware": len(diagnostic),
            "granularity_aware_remaining_units": sorted(set(d["us"]) - diagnostic),
            "frozen_direct_rule_passes_primary": primary_direct == set(d["us"]),
            "frozen_direct_rule_passes_review": review_direct == set(d["us"]),
            "secondary_diagnostic_only": True,
        },
        "failure_causes": failures,
        "reliability_conclusion": {
            "classification": "SEVERE_ARCHITECTURE_RELEVANT_DISAGREEMENT",
            "reason": "Only 12 of 22 distinct direct mappings are shared; 11 unit statuses and 7 need classifications change, and six alternatives change strict completeness. Several changes affect ownership, dependencies, exports, frame integrity and necessity. This joint pattern, not one arbitrary cutoff, requires reconciliation.",
            "primary_alone_safe_for_stage_d": False,
            "review_alone_safe_for_stage_d": False,
            "reconciliation_required": True,
            "strict_every_unit_failure_robust": True,
            "exact_failed_unit_set_robust": False,
            "exact_cause_disputed": True,
            "final_frozen_u1_outcome": "NOT_SELECTED",
            "stage_d": "BLOCKED",
            "u1_effectiveness": "UNKNOWN",
        },
    }


def neutral_packet(
    d: dict[str, Any], c: dict[str, Any]
) -> tuple[dict[str, Any], dict[str, Any]]:
    propositions: list[dict[str, Any]] = []
    audit: list[dict[str, Any]] = []

    def add(
        kind: str, subject: dict[str, Any], claims: list[tuple[str, dict[str, Any]]]
    ) -> None:
        identifier = digest(encode({"kind": kind, "subject": subject}))
        ordered = sorted(claims, key=lambda x: (digest(encode(x[1])), encode(x[1])))
        row = {
            "identity": identifier,
            "kind": kind,
            "subject": subject,
            "positions": {
                f"position_{i}": claim for i, (_, claim) in enumerate(ordered, 1)
            },
            "decisions": DECISIONS
            if len(ordered) == 2
            else [
                "CONFIRM_PROPOSITION",
                "REPLACE_WITH_RECONCILED_JUDGMENT",
                "UNRESOLVED",
            ],
        }
        if kind == "UNIT_GRANULARITY":
            row["permitted_categories"] = GRANULARITY
        if kind == "COLLECTIVE_COVERAGE":
            row["requires"] = (
                "Explicit sufficiency and minimality rationale for each set, with why removal of each member fails."
            )
        propositions.append(row)
        audit.append(
            {
                "identity": identifier,
                "kind": kind,
                "sources": {
                    f"position_{i}": source for i, (source, _) in enumerate(ordered, 1)
                },
            }
        )

    for row in c["pair_disagreements"]:
        add(
            "PAIR_LABEL",
            {"need": row["need"], "unit": row["unit"]},
            [("primary", row["primary"]), ("review", row["review"])],
        )
    for row in c["agreed_direct_rationale_comparisons"]:
        add(
            "DIRECT_RATIONALE",
            {"need": row["need"], "unit": row["unit"]},
            [("primary", row["primary"]), ("review", row["review"])],
        )
    for row in c["units"]:
        if row["primary"]["status"] != row["review"]["status"]:
            claims = []
            for source in ("primary", "review"):
                coverage = row[source]
                claims.append(
                    (
                        source,
                        {
                            "status": coverage["status"],
                            "direct_needs": coverage["direct_needs"],
                            "partial_needs": coverage["partial_needs"],
                            "ambiguous_needs": coverage["ambiguous_needs"],
                            "rationales": [
                                {"need": x["need"], **x[source]}
                                for x in row["mapping_rationales"]
                            ],
                        },
                    )
                )
            add("UNIT_STATUS", {"unit": row["identity"]}, claims)
    for row in c["needs"]:
        if row["primary"]["classification"] != row["review"]["label"]:
            add(
                "NEED_CLASSIFICATION",
                {"need": row["identity"]},
                [
                    (
                        "primary",
                        {
                            "classification": row["primary"]["classification"],
                            "rationale": row["primary"]["rationale"],
                            "formulation_rationale": row["primary"][
                                "reviewer_judgment"
                            ]["rationale"],
                            "direct_units": row["primary"]["direct_units"],
                        },
                    ),
                    (
                        "review",
                        {
                            "classification": row["review"]["label"],
                            "rationale": row["review"]["rationale"],
                            "formulation_rationale": row["review"][
                                "semantic_formulation_review"
                            ],
                            "direct_units": row["review"]["direct_units"],
                        },
                    ),
                ],
            )
    for row in c["alternatives"]:
        if (
            row["primary_missing_direct_members"]
            != row["review_missing_direct_members"]
            or row["review"]["status"] == "FULLY_COVERED_ONLY_COLLECTIVELY"
        ):
            add(
                "ALTERNATIVE_COMPLETENESS",
                {"alternative": row["identity"]},
                [
                    (
                        "primary",
                        {
                            "strict_direct_complete": row["primary_direct_complete"],
                            "missing_direct_members": row[
                                "primary_missing_direct_members"
                            ],
                            "rationale": "All complementary members must have at least one direct mapping; the listed members lack one.",
                        },
                    ),
                    (
                        "review",
                        {
                            "strict_direct_complete": row["review_direct_complete"],
                            "missing_direct_members": row[
                                "review_missing_direct_members"
                            ],
                            "diagnostic_state": row["review"]["status"],
                            "rationale": row["review"]["rationale"],
                            "collectively_covered_members": row["review"][
                                "collectively_covered_members"
                            ],
                            "incomplete_members": row["review"]["incomplete_members"],
                        },
                    ),
                ],
            )
    for row in c["granularity"]:
        add(
            "UNIT_GRANULARITY",
            {"unit": row["unit"]},
            [("review", {"category": row["category"], "rationale": row["rationale"]})],
        )
    for row in c["collective"]:
        add(
            "COLLECTIVE_COVERAGE",
            {"unit": row["unit"]},
            [("review", {"sets": row["sets"], "diagnostic_only": True})],
        )
    packet = d["packet"]
    # Field allowlist deliberately omits author, provenance, chronology and method metadata.
    semantics = {
        "case_identity": packet["frame"]["case_identity"],
        "task_identity": packet["frame"]["task_identity"],
        "task": packet["task"],
        "obligations": [
            {
                k: o[k]
                for k in (
                    "identity",
                    "predicate",
                    "criterion",
                    "requirement",
                    "applicability_condition",
                    "task_basis",
                )
            }
            for o in packet["obligations"]
        ],
        "information_needs": [
            {
                k: n[k]
                for k in ("identity", "obligation", "statement", "reason", "task_basis")
            }
            for n in packet["information_needs"]
        ],
        "units": packet["units"],
        "alternatives": packet["alternatives"],
        "mapping_labels": packet["mapping_labels"],
        "need_labels": packet["need_labels"],
        "direct_coverage_rule": packet["direct_coverage_rule"],
        "unit_coverage": packet["unit_coverage"],
        "display_aliases": {
            "needs": {
                n["identity"]: f"N{i:02d}"
                for i, n in enumerate(packet["information_needs"], 1)
            },
            "units": {
                u["identity"]: f"U{i:02d}" for i, u in enumerate(packet["units"], 1)
            },
        },
    }
    result = {
        "schema": "case-0011-neutral-c5-reconciliation-v1",
        "semantics": semantics,
        "bindings": c["frame_alignment"]["bindings"],
        "position_order": "Ascending SHA-256 of canonical sorted UTF-8 claim JSON, separately for each proposition; no global reviewer position.",
        "propositions": sorted(propositions, key=lambda x: x["identity"]),
        "rules": [
            "No majority voting.",
            "No automatic preference for more direct coverage.",
            "No automatic preference for smaller or broader need sets.",
            "Single-position audits are propositions requiring confirmation, not established truth.",
            "Strict direct coverage and secondary collective diagnostics remain separate.",
            "Do not alter semantic inputs or conclude effectiveness.",
        ],
    }
    return result, {
        "schema": "case-0011-c5-source-audit-v1",
        "outside_packet_only": True,
        "position_order": result["position_order"],
        "propositions": sorted(audit, key=lambda x: x["identity"]),
    }


def table(headers: list[str], rows: list[list[Any]]) -> str:
    return "\n".join(
        [
            "| " + " | ".join(headers) + " |",
            "| " + " | ".join("---" for _ in headers) + " |",
            *(
                "| "
                + " | ".join(str(v).replace("|", "\\|").replace("\n", " ") for v in row)
                + " |"
                for row in rows
            ),
        ]
    )


def render(c: dict[str, Any], d: dict[str, Any]) -> str:
    lines: list[str] = [
        "# Case 0011 C.5 reliability review",
        "",
        "SEVERE_ARCHITECTURE_RELEVANT_DISAGREEMENT. Neither adjudication alone is safe for Stage D. Reconciliation is required. Both fail the strict every-required-unit direct rule, but the exact failed units and causes are disputed. U1 effectiveness is UNKNOWN; no final U1 outcome is selected.",
        "",
        "This is a fully inspectable comparison of frozen claims, not reconciliation. The independent granularity and collective audits are diagnostics awaiting confirmation. No treatment or confirmation data was accessed.",
        "",
        "## Executive comparison",
        "",
    ]
    s = c["per_label"]
    lines += [
        table(
            ["Measure", "Primary C.5", "Independent C.5-R", "Agreement / implication"],
            [
                [
                    "Pair labels",
                    "13 direct; 59 partial; 504 noncoverage",
                    "21 direct; 41 partial; 514 noncoverage",
                    "544/576 = 94.4444%; 32 disagreements",
                ],
                ["Direct mappings", 13, 21, "12 shared / 22 union; Jaccard 54.5455%"],
                [
                    "Strict covered units",
                    "13/32",
                    "20/32",
                    "21/32 statuses agree; 11 disagree",
                ],
                [
                    "Need classifications",
                    "9 necessary; 9 partial-only",
                    "13 necessary; 1 redundant; 4 partial-only",
                    "11/18 agree; 7 disagree",
                ],
                [
                    "Direct-complete alternatives",
                    "0/12",
                    "6/12",
                    "6/12 direct-completeness agree",
                ],
                [
                    "Secondary granularity-aware coverage",
                    "not independently audited",
                    "26/32",
                    "8/12 alternatives diagnostic complete; never replaces strict U1",
                ],
            ],
        ),
        "",
        "## Exact pair-label confusion matrix",
        "",
        "Rows = primary; columns = independent. Cohen's kappa is descriptive only; these fixed semantic judgments are not a random sample.",
        "",
    ]
    for field, title in (
        ("pair_comparison", "Pair labels"),
        ("unit_comparison", "Unit statuses"),
        ("need_comparison", "Need classifications"),
        ("alternative_direct_comparison", "Alternative strict completeness"),
    ):
        m = c[field]
        lines += [
            f"### {title}",
            "",
            table(
                ["Primary / independent", *m["columns"]],
                [
                    [label, *row]
                    for label, row in zip(m["rows"], m["matrix"], strict=True)
                ],
            ),
            "",
            f"Exact agreement {m['agreement_count']}/{m['total']} ({m['agreement_fraction']:.6%}); disagreements {m['disagreement_count']}; descriptive kappa {m['descriptive_cohens_kappa']}.",
            "",
        ]
    lines += [
        "## Direct and partial mapping reliability",
        "",
        table(
            [
                "Label",
                "Primary",
                "Independent",
                "Intersection",
                "Union",
                "Jaccard",
                "Primary retained",
                "Independent retained",
            ],
            [
                [
                    label,
                    x["primary_count"],
                    x["review_count"],
                    x["intersection"],
                    x["union"],
                    x["jaccard"],
                    x["primary_retained_by_review"],
                    x["review_retained_by_primary"],
                ]
                for label, x in s.items()
            ],
        ),
        "",
        "DIRECT: primary-only = 1; review-only = 9. PARTIAL: primary-only = 25; review-only = 7. Partial→direct = 9; partial→noncoverage = 16; noncoverage→direct = 0; noncoverage→partial = 6; direct→partial = 1. The independent reviewer became more direct through nine promotions and more decisive through sixteen removals of weak partial relationships. No agreed noncoverage pool should hide direct instability.",
        "",
    ]
    for kind, groups in c["direct_by_owner"].items():
        lines += [
            f"### Direct reliability by {kind}",
            "",
            "Unit-obligation and alternative totals overlap when membership overlaps; need-obligation is reported separately.",
            "",
            table(
                [
                    "Owner",
                    "Primary",
                    "Independent",
                    "Shared",
                    "Union",
                    "Jaccard",
                    "Primary retained",
                    "Independent retained",
                ],
                [
                    [
                        name,
                        x["primary_count"],
                        x["review_count"],
                        x["intersection"],
                        x["union"],
                        x["jaccard"],
                        x["primary_retained_by_review"],
                        x["review_retained_by_primary"],
                    ]
                    for name, x in groups.items()
                ],
            ),
            "",
        ]
    lines += [
        "## Every pair-label disagreement, including every disputed direct mapping",
        "",
    ]
    for row in c["pair_disagreements"]:
        lines += [
            f"### {row['need']} × {row['unit']}",
            "",
            f"Need: {row['need_statement']}",
            "",
            f"Unit: {row['unit_statement']}",
            "",
            f"Owning need obligation: {d['ns'][row['need']]['obligation']}; unit obligations: {d['us'][row['unit']]['obligations']}; alternatives: {d['us'][row['unit']]['alternative_membership']}.",
            "",
        ]
        for source in ("primary", "review"):
            claim = row[source]
            lines += [
                f"**{source}: {claim['label']}**",
                "",
                f"Fact sought: {claim['fact_sought']}",
                "",
                f"Fact established: {claim['fact_established']}",
                "",
                claim["rationale"],
                "",
            ]
            for part in ("covered_part", "missing_part"):
                if part in claim:
                    lines += [f"{part}: {claim[part]}", ""]
    lines += [
        "## Shared direct mappings: both semantic rationales",
        "",
        "These agreed labels still receive a rationale review proposition; no agreed DOES_NOT_COVER mappings are added to inflate the packet.",
        "",
    ]
    for row in c["agreed_direct_rationale_comparisons"]:
        lines += [
            f"### {row['need']} × {row['unit']}",
            "",
            f"Need: {d['ns'][row['need']]['statement']}",
            "",
            f"Unit: {d['us'][row['unit']]['statement']}",
            "",
            f"Primary rationale: {row['primary']['rationale']}",
            "",
            f"Independent rationale: {row['review']['rationale']}",
            "",
        ]
    lines += [
        "## All 32 unit statuses",
        "",
        table(
            ["Unit", "Primary", "Independent", "Statement"],
            [
                [
                    x["identity"],
                    x["primary"]["status"],
                    x["review"]["status"],
                    x["statement"],
                ]
                for x in c["units"]
            ],
        ),
        "",
        "Eight units upgrade from PARTIAL_ONLY to COVERED; one downgrades from COVERED to PARTIAL_ONLY. Twelve are covered in both; nine are partial-only in both. Both primary UNCOVERED units become independent PARTIAL_ONLY, not directly covered.",
        "",
        "### Every unit-status disagreement and both rationales",
        "",
    ]
    for row in c["units"]:
        if row["primary"]["status"] == row["review"]["status"]:
            continue
        lines += [
            f"#### {row['identity']}",
            "",
            row["statement"],
            "",
            f"Primary: {row['primary']['status']}; independent: {row['review']['status']}.",
            "",
        ]
        for claim in row["mapping_rationales"]:
            lines += [
                f"Need {claim['need']}: {d['ns'][claim['need']]['statement']}",
                "",
                f"Primary {claim['primary']['label']}: {claim['primary']['rationale']}",
                "",
                f"Independent {claim['review']['label']}: {claim['review']['rationale']}",
                "",
            ]
    lines += [
        "## All 18 need classifications",
        "",
        table(
            ["Need", "Primary", "Independent", "Statement"],
            [
                [
                    x["identity"],
                    x["primary"]["classification"],
                    x["review"]["label"],
                    x["statement"],
                ]
                for x in c["needs"]
            ],
        ),
        "",
        "Primary-only NECESSARY: frame/items. Review-only NECESSARY: ownership/assembly-owner, ownership/dependencies, ceiling/rejection, exports/public-boundary, documentation/architecture. request/prompt changes PARTIAL_ONLY→USEFUL_REDUNDANT. frame/items changes NECESSARY→PARTIAL_ONLY. No MISFORMULATED or AMBIGUOUS classification or formulation disagreement is established.",
        "",
        "### Every need-classification disagreement",
        "",
    ]
    for row in c["needs"]:
        if row["primary"]["classification"] != row["review"]["label"]:
            lines += [
                f"#### {row['identity']}",
                "",
                row["statement"],
                "",
                f"Primary {row['primary']['classification']}: {row['primary']['rationale']}",
                "",
                f"Primary formulation: {row['primary']['reviewer_judgment']['rationale']}",
                "",
                f"Independent {row['review']['label']}: {row['review']['rationale']}",
                "",
                f"Independent formulation: {row['review']['semantic_formulation_review']}",
                "",
            ]
    lines += [
        "## Every witness alternative and member-level causes",
        "",
        "Members remain ALL complementary within an alternative; alternatives remain ANY per obligation. Members are never pooled across alternatives. Primary states are derived under the strict direct rule; collective completeness is a secondary independent diagnostic.",
        "",
    ]
    for row in c["alternatives"]:
        lines += [
            f"### {row['identity']} ({row['obligation']})",
            "",
            f"Primary direct complete: {row['primary_direct_complete']}; independent direct complete: {row['review_direct_complete']}; independent diagnostic: {row['review']['status']}.",
            "",
            row["review"]["rationale"],
            "",
            table(
                ["Member", "Primary", "Independent", "Granularity", "Statement"],
                [
                    [
                        x["unit"],
                        x["primary"],
                        x["review"],
                        x["granularity"],
                        x["statement"],
                    ]
                    for x in row["member_causes"]
                ],
            ),
            "",
        ]
    lines += [
        "## Independent unit-granularity audit",
        "",
        "Primary C.5 did not independently supply this audit. These are independent propositions awaiting confirmation; reviewed gold is unchanged.",
        "",
        table(
            ["Category", "Count"], [[k, v] for k, v in c["granularity_counts"].items()]
        ),
        "",
    ]
    for row in c["granularity"]:
        if row["category"] != "ATOMIC_FOR_NEED_MAPPING":
            lines += [
                f"### {row['unit']} — {row['category']}",
                "",
                row["statement"],
                "",
                row["rationale"],
                "",
                f"Primary: {d['pu'][row['unit']]['status']}; independent: {d['ru'][row['unit']]['status']}.",
                "",
                f"Proposed minimal sets: {d['collective'].get(row['unit'], {}).get('minimal_need_sets', [])}",
                "",
            ]
    lines += [
        "## Collective need sets and minimality",
        "",
        c["collective_validation_limit"],
        "",
    ]
    for row in c["collective"]:
        lines += [
            f"### {row['unit']}",
            "",
            row["statement"],
            "",
            f"{len(row['sets'])} proposed minimal set(s); remains {row['strict_status']} under the strict direct rule.",
            "",
            row["rationale"],
            "",
            row["minimality"],
            "",
        ]
        for need_set in row["sets"]:
            lines += [f"Set: {need_set['needs']}", ""]
            for member in need_set["member_necessity"]:
                lines += [
                    f"{member['need']}: {d['ns'][member['need']]['statement']}",
                    "",
                    f"Necessary contribution: {member['covered_part']}",
                    "",
                    f"Missing from this member alone: {member['missing_without_others']}",
                    "",
                ]
    lines += [
        "## Strict and granularity-aware coverage",
        "",
        "Strict primary: 13/32; strict independent: 20/32. Secondary independent GRANULARITY_AWARE_COVERED: 26/32 (20 direct plus six collective). Six still lack complete coverage: three overcompound propositions and three atomic partial-only units. The strict every-unit failure holds in both reviews; neither identifies the same exact failed set. Alternatives: six fully direct, two complete only collectively, four incomplete, zero ambiguous. Four alternatives are strictly incomplete in both but also remain incomplete in the independent diagnostic; two further alternatives are strictly incomplete in both and become diagnostic complete only collectively.",
        "",
        "Remaining diagnostic units:",
        "",
    ]
    for u in c["coverage"]["granularity_aware_remaining_units"]:
        lines += [f"- {u}: {d['us'][u]['statement']}"]
    lines += ["", "## Exact current failure-cause assessment", ""]
    for name, assessment in c["failure_causes"].items():
        lines += [
            f"### {name}: {assessment['evidence']}",
            "",
            assessment["scope"],
            "",
            f"Exact supporting metrics: {json.dumps(assessment['metrics'], sort_keys=True)}",
            "",
        ]
    lines += [
        "## Reliability conclusion and Stage D boundary",
        "",
        c["reliability_conclusion"]["reason"],
        "",
        "Neither primary C.5 alone nor independent C.5-R alone is safe for Stage D. Reconciliation is required. Strict direct-rule failure is robust as a Boolean, not as an exact missing-unit attribution. The exact cause remains disputed. Stage D has not occurred and remains BLOCKED. This checkpoint cannot conclude retrieval success, treatment effects, acquisition effectiveness, information-need authoring defect, a final frozen U1 outcome, or confirmation. The prepared packet authorizes only a future fresh semantic reconciliation session; this task performs none.",
        "",
    ]
    return "\n".join(lines)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    d = load()
    c = build(d)
    packet, audit = neutral_packet(d, c)
    args.output.mkdir(exist_ok=True)
    files = {
        "c5_reliability_comparison.json": encode(c),
        "C5_RELIABILITY_REVIEW.md": render(c, d).encode(),
        "neutral_packet.json.gz": gzip.compress(encode(packet), mtime=0),
        "source_audit.json": encode(audit),
    }
    assert all(not (args.output / name).exists() for name in files), "OVERWRITE_REFUSED"
    for name, raw in files.items():
        exclusive(args.output / name, raw)


if __name__ == "__main__":
    main()
