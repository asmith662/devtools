"""Exact treatment-blind replay of Case 0011's bounded semantic decisions.

Experiment-local publication; no new adjudication, retrieval or production API.
Only load the explicit semantic input whitelist. Never import case protocol code.
"""

from __future__ import annotations

import argparse
import gzip
import hashlib
import importlib.util
import itertools
import json
import sys
from collections import Counter
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parent
BASE = ROOT.parent
PACKET = "c1ecca8aec6bb9cbfb09668a79054262d91e22cfad4adda686bdf97016476b9f"
IMPORTS = {
    "c5_reconciliation_v2_decisions.json": "fee631f986c1850bf300bef0c3fa0f9a0ee0f32da772cd3c06b69f274cd97750",
    "c5_reconciliation_v2_validation.json": "f9b972fd57605094f0d334abf77a19da5facb74c542ab76c0e288e866b300b75",
    "c5_reconciliation_v2_hashes.json": "f12149a2643fa988f85cfdde904ddefa9e878df8c2772b5d4a8ca4d0d555ed1e",
}
BINDINGS = {
    "frozen_needs_sha256": "8e951bc42ee08db656717ffb494880de26007c087d31f38657b421b8793c54aa",
    "reviewed_gold_sha256": "0d6f54a4ab1eed68b2deb4f4557ef767ff9f2a7771eebde534527c425ae34430",
    "reliability_comparison_sha256": "75c56552e97e3d86cc3a719fbb0214cbd76b86ca229e8abe5f5bc0b1b2573e2a",
}
LABELS = ["DIRECTLY_COVERS", "PARTIALLY_COVERS", "DOES_NOT_COVER", "AMBIGUOUS"]
STATUSES = ["COVERED", "PARTIAL_ONLY", "UNCOVERED", "AMBIGUOUS_ONLY"]
NEEDS = [
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
COLLECTIVE = [
    "VALID_MINIMAL_COLLECTIVE_SET",
    "INSUFFICIENT",
    "VALID_BUT_NOT_MINIMAL",
    "AMBIGUOUS",
]
DIAGNOSTIC = [
    "GRANULARITY_AWARE_COVERED",
    "GRANULARITY_AWARE_PARTIAL",
    "GRANULARITY_AWARE_UNCOVERED",
    "GRANULARITY_AWARE_AMBIGUOUS",
]
ALTERNATIVES = [
    "FULLY_DIRECTLY_COVERED",
    "FULLY_COVERED_ONLY_COLLECTIVELY",
    "INCOMPLETE",
    "AMBIGUOUS",
]
NAMES = [
    f"reviewed_c5_{name}_v1.json"
    for name in [
        "mappings",
        "unit_coverage",
        "need_classifications",
        "alternatives",
        "granularity",
        "collective_coverage",
        "statistics",
        "provenance",
        "validation",
        "output_digests",
    ]
] + ["REVIEWED_C5.md"]
DENIED = {
    "lexical_query",
    "lexical_queries",
    "query_strings",
    "analyzer_terms",
    "analyzed_terms",
    "retrieval_route",
    "retrieval_routes",
    "retrieval_results",
    "result_resources",
    "result_resource",
    "rank",
    "ranks",
    "score",
    "scores",
    "candidate_overlaps",
    "acquisition_cost",
    "acquisition_costs",
    "treatment",
    "treatment_results",
    "arm_identity",
    "arm_id",
    "treatment_arm",
    "treatment_outcomes",
    "confirmation_data",
    "stage_d_outcomes",
    "model",
    "model_identity",
    "costs",
}


def encode(value: Any) -> bytes:
    return (
        json.dumps(value, sort_keys=True, indent=2, ensure_ascii=False) + "\n"
    ).encode()


def sha(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def unique(items: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in items:
        assert key not in result, "duplicate JSON field"
        result[key] = value
    return result


def load(raw: bytes) -> Any:
    return json.loads(raw, object_pairs_hook=unique)


def reject_forbidden(value: Any) -> None:
    if isinstance(value, dict):
        assert not DENIED & {
            k.lower().replace("-", "_").replace(" ", "_") for k in value
        }, "forbidden field"
        for child in value.values():
            reject_forbidden(child)
    elif isinstance(value, list):
        for child in value:
            reject_forbidden(child)


def counts(
    rows: list[dict[str, Any]], field: str, vocabulary: list[str]
) -> dict[str, int]:
    counter = Counter(row[field] for row in rows)
    assert set(counter) <= set(vocabulary)
    return {label: counter[label] for label in vocabulary}


def index(rows: list[dict[str, Any]], *fields: str) -> dict[Any, Any]:
    result = {
        tuple(row[f] for f in fields) if len(fields) > 1 else row[fields[0]]: row
        for row in rows
    }
    assert len(result) == len(rows), "duplicate identity"
    return result


def validator(name: str) -> Any:
    # Existing closed reconciliation schema, loaded only from its permitted directory.
    path = BASE / "reconciliation_v2/packet" / f"{name}.py"
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


def source_inputs() -> dict[str, Any]:
    hashes: dict[str, str] = {}

    def read(relative: str) -> Any:
        raw = (BASE / relative).read_bytes()
        hashes[relative] = sha(raw)
        return load(gzip.decompress(raw) if relative.endswith(".gz") else raw)

    v = validator("validate_packet")
    r = validator("reconcile_c5_v2")
    packet_validation = v.validate(BASE / "reconciliation_v2/packet")
    packet = read("reconciliation_v2/packet/packet.json.gz")
    assert sha(encode(packet)) == PACKET
    assert packet["bindings"] == BINDINGS
    imported = {}
    for name, expected in IMPORTS.items():
        relative = f"reconciliation_v2/results/{name}"
        imported[name] = read(relative)
        assert hashes[relative] == expected, "immutable import hash"
    decision = imported["c5_reconciliation_v2_decisions.json"]
    assert (
        r.check_decisions(packet, decision)
        == imported["c5_reconciliation_v2_validation.json"]
    )
    for name, raw in r.replay(packet, decision).items():
        assert sha(raw) == IMPORTS[name], "immutable reconciliation replay"
    assert decision["decision_category_counts"] == {
        "ACCEPT_POSITION_1": 28,
        "ACCEPT_POSITION_2": 34,
        "CONFIRM_PROPOSITION": 32,
        "REPLACE_WITH_RECONCILED_JUDGMENT": 16,
    }
    assert decision["unresolved_count"] == 0
    primary = read("results/c5_mappings_v1.json")
    pn = read("results/c5_need_classifications_v1.json")
    pu = read("results/c5_unit_coverage_v1.json")
    ledger = read("results/c5_output_digests_v1.json")
    for name in (
        "c5_mappings_v1.json",
        "c5_need_classifications_v1.json",
        "c5_unit_coverage_v1.json",
    ):
        assert hashes[f"results/{name}"] == ledger["scientific_output_sha256"][name]
    independent = read("reliability/c5r_v1_adjudication.json")
    il = read("reliability/c5r_v1_hashes.json")
    assert (
        hashes["reliability/c5r_v1_adjudication.json"]
        == il["sha256"]["c5r_v1_adjudication.json"]
    )
    comparison = read("reliability/c5_reliability_comparison.json")
    assert (
        hashes["reliability/c5_reliability_comparison.json"]
        == BINDINGS["reliability_comparison_sha256"]
    )
    gold = read("../reviewed/reviewed_gold.json")
    assert hashes["../reviewed/reviewed_gold.json"] == BINDINGS["reviewed_gold_sha256"]
    semantics = packet["semantics"]
    projection = read("projection_audit.json")
    assert projection["reviewed_gold_sha256"] == BINDINGS["reviewed_gold_sha256"]
    assert projection["frozen_needs_sha256"] == BINDINGS["frozen_needs_sha256"]

    def projected_statement(statement: str) -> str:
        for original, replacement in projection["location_substitutions"].items():
            statement = statement.replace(original, replacement)
        return statement

    gold_units = {
        projection["unit_projection"][row["id"]]: projected_statement(row["statement"])
        for row in gold["units"]
    }
    assert gold_units == {
        row["identity"]: row["statement"] for row in semantics["units"]
    }
    assert semantics["units"] == independent["frozen_packet"]["units"]
    assert semantics["alternatives"] == independent["frozen_packet"]["alternatives"]
    projected_alts = {
        projection["alternative_projection"][a["id"]]: (
            g["obligation"],
            sorted(projection["unit_projection"][u] for u in a["units"]),
        )
        for g in gold["obligations"]
        for a in g["alternatives"]
    }
    assert projected_alts == {
        a["identity"]: (g["obligation"], sorted(a["units"]))
        for g in semantics["alternatives"]
        for a in g["alternatives"]
    }
    assert [
        (n["identity"], n["statement"]) for n in semantics["information_needs"]
    ] == [
        (n["identity"], n["statement"])
        for n in independent["frozen_packet"]["information_needs"]
    ]
    assert (
        independent["manifest"]["frozen_needs_sha256"]
        == BINDINGS["frozen_needs_sha256"]
    )
    assert (
        independent["manifest"]["reviewed_gold_sha256"]
        == BINDINGS["reviewed_gold_sha256"]
    )
    # Frozen-needs hash is an authenticated binding, not a hash of an invented projection.
    return {
        "packet": packet,
        "decision": decision,
        "primary": primary,
        "pn": pn,
        "pu": pu,
        "independent": independent,
        "comparison": comparison,
        "hashes": hashes,
        "packet_validation": packet_validation,
    }


def decision_provenance(row: dict[str, Any], kind: str | None = None) -> dict[str, Any]:
    return {
        "origin": kind
        or (
            "RECONCILED_SINGLE_POSITION"
            if row["kind"] in {"UNIT_GRANULARITY", "COLLECTIVE_COVERAGE"}
            else "RECONCILED_DISPUTE"
        ),
        "proposition": row["identity"],
        "decision": row["decision"],
        "evidence_references": row["evidence_references"],
    }


def unit_status(labels: set[str]) -> str:
    # Absence is UNCOVERED; explicit unresolved coverage is AMBIGUOUS_ONLY.
    return (
        "COVERED"
        if LABELS[0] in labels
        else "PARTIAL_ONLY"
        if LABELS[1] in labels
        else "AMBIGUOUS_ONLY"
        if "AMBIGUOUS" in labels
        else "UNCOVERED"
    )


def build(data: dict[str, Any]) -> dict[str, Any]:
    s = data["packet"]["semantics"]
    ns, us = index(s["information_needs"], "identity"), index(s["units"], "identity")
    aliases = s["display_aliases"]
    p = index(data["primary"]["mappings"], "need", "unit")
    i = index(data["independent"]["pairs"], "need", "unit")
    expected = set(itertools.product(ns, us))
    assert len(expected) == 576 and set(p) == set(i) == expected, "pair frame"
    decisions = data["decision"]["decisions"]
    by_kind = {
        kind: [row for row in decisions if row["kind"] == kind]
        for kind in {row["kind"] for row in decisions}
    }
    disputed = {
        (row["subject"]["need"], row["subject"]["unit"]): row
        for row in by_kind["PAIR_LABEL"]
    }
    shared = {
        (row["subject"]["need"], row["subject"]["unit"]): row
        for row in by_kind["DIRECT_RATIONALE"]
    }
    disagreements = {key for key in expected if p[key]["label"] != i[key]["label"]}
    assert (
        set(disputed)
        == disagreements
        == {
            (row["need"], row["unit"])
            for row in data["comparison"]["pair_disagreements"]
        }
    )
    assert set(shared) == {
        key
        for key in expected
        if p[key]["label"] == i[key]["label"] == "DIRECTLY_COVERS"
    }
    mapping = []
    for n, u in sorted(expected):
        key = (n, u)
        assert p[key]["need_fact_sought"] == ns[n]["statement"]
        assert p[key]["unit_fact_established"] == us[u]["statement"]
        assert (
            i[key]["need_statement"] == ns[n]["statement"]
            and i[key]["unit_statement"] == us[u]["statement"]
        )
        row = {
            "need": n,
            "unit": u,
            "label": p[key]["label"],
            "label_provenance": {
                "origin": "INHERITED_AGREEMENT",
                "source_pair": [n, u],
            },
            "source_rationales": [
                {"artifact": "source_mapping_1", "rationale": p[key]["rationale"]},
                {"artifact": "source_mapping_2", "rationale": i[key]["rationale"]},
            ],
        }
        if key in disputed or key in shared:
            decision = disputed[key] if key in disputed else shared[key]
            row.update(decision["payload"])
            row["rationale_provenance"] = decision_provenance(
                decision,
                "RECONCILED_SHARED_DIRECT_RATIONALE" if key in shared else None,
            )
            if key in disputed:
                row["label_provenance"] = decision_provenance(decision)
            else:
                assert row["label"] == p[key]["label"] == i[key]["label"]
        else:
            # Preserve both rationales and partial components; no source preference adjudication.
            row["rationale_provenance"] = {"origin": "INHERITED_AGREEMENT"}
            row["agreed_evidence"] = [
                {
                    "artifact": name,
                    **{
                        k: value[k]
                        for k in (
                            "rationale",
                            "covered_part",
                            "missing_part",
                            "complete_unit_bridge",
                            "counterfactual",
                        )
                        if k in value
                    },
                }
                for name, value in (
                    ("source_mapping_1", p[key]),
                    ("source_mapping_2", i[key]),
                )
            ]
        mapping.append(row)
    final = index(mapping, "need", "unit")
    unit_decisions = index(
        [{**row, "unit": row["subject"]["unit"]} for row in by_kind["UNIT_STATUS"]],
        "unit",
    )
    units = []
    for u in us:
        direct = sorted(n for n in ns if final[n, u]["label"] == "DIRECTLY_COVERS")
        partial = sorted(n for n in ns if final[n, u]["label"] == "PARTIALLY_COVERS")
        ambiguous = sorted(n for n in ns if final[n, u]["label"] == "AMBIGUOUS")
        status = unit_status({final[n, u]["label"] for n in ns})
        row = {
            "unit": u,
            "alias": aliases["units"][u],
            "statement": us[u]["statement"],
            "status": status,
            "direct_needs": direct,
            "partial_needs": partial,
            "ambiguous_needs": ambiguous,
            "provenance": {
                "origin": "DETERMINISTIC_DERIVATION",
                "rule": "strict_direct_then_partial_then_explicit_ambiguity_else_absence",
            },
        }
        if u in unit_decisions:
            assert unit_decisions[u]["payload"]["status"] == status, (
                "reconciled unit contradiction"
            )
            row["consistency_decision"] = unit_decisions[u]
        units.append(row)
    ui = index(units, "unit")
    pn = index(data["pn"]["needs"], "need")
    inn = index(data["independent"]["need_classifications"], "need")
    nd = index(
        [
            {**row, "need": row["subject"]["need"]}
            for row in by_kind["NEED_CLASSIFICATION"]
        ],
        "need",
    )
    assert set(pn) == set(inn) == set(ns)
    assert set(nd) == {n for n in ns if pn[n]["classification"] != inn[n]["label"]}
    needs = []
    for n in ns:
        direct = sorted(u for u in us if n in ui[u]["direct_needs"])
        partial = sorted(u for u in us if n in ui[u]["partial_needs"])
        unique_units = sorted(u for u in direct if ui[u]["direct_needs"] == [n])
        classification = (
            nd[n]["payload"]["classification"] if n in nd else pn[n]["classification"]
        )
        derived = (
            "NECESSARY"
            if unique_units
            else "USEFUL_REDUNDANT"
            if direct
            else "PARTIAL_ONLY"
            if partial
            else "UNNECESSARY"
        )
        if classification not in {"MISFORMULATED", "AMBIGUOUS"}:
            assert classification == derived, "need classification contradiction"
        needs.append(
            {
                "need": n,
                "alias": aliases["needs"][n],
                "statement": ns[n]["statement"],
                "classification": classification,
                "direct_units": direct,
                "partial_units": partial,
                "unique_units": unique_units,
                "mechanical_support": derived,
                "rationale": nd[n]["payload"]["rationale"]
                if n in nd
                else [pn[n]["rationale"], inn[n]["rationale"]],
                "provenance": decision_provenance(nd[n])
                if n in nd
                else {"origin": "INHERITED_AGREEMENT"},
                "support_provenance": {"origin": "DETERMINISTIC_DERIVATION"},
            }
        )
    granularity = [
        {
            "unit": row["subject"]["unit"],
            **row["payload"],
            "provenance": decision_provenance(row),
        }
        for row in by_kind["UNIT_GRANULARITY"]
    ]
    gi = index(granularity, "unit")
    assert set(gi) == set(us)
    collective = []
    for decision in by_kind["COLLECTIVE_COVERAGE"]:
        u = decision["subject"]["unit"]
        sets = decision["payload"]["sets"]
        assert len({tuple(row["needs"]) for row in sets}) == len(sets)
        accepted = [
            set(row["needs"])
            for row in sets
            if row["classification"] == "VALID_MINIMAL_COLLECTIVE_SET"
        ]
        assert not any(a < b for a in accepted for b in accepted), (
            "nonminimal accepted superset"
        )
        for row in sets:
            assert len(row["needs"]) == len(set(row["needs"])) >= 2
            assert set(row["needs"]) <= set(ns)
            assert {c["need"] for c in row["contributions"]} == set(row["needs"])
            if row["classification"].startswith("VALID_"):
                assert gi[u]["classification"] == "COLLECTIVELY_COVERABLE"
                assert all(
                    final[n, u]["label"] == "PARTIALLY_COVERS" for n in row["needs"]
                )
            collective.append(
                {
                    "unit": u,
                    **row,
                    "unit_rationale": decision["payload"]["rationale"],
                    "provenance": decision_provenance(decision),
                }
            )
    valid_units = {
        row["unit"] for row in collective if row["classification"].startswith("VALID_")
    }
    for row in units:
        u = row["unit"]
        state = (
            "GRANULARITY_AWARE_COVERED"
            if row["status"] == "COVERED"
            or (row["status"] == "PARTIAL_ONLY" and u in valid_units)
            else "GRANULARITY_AWARE_PARTIAL"
            if row["partial_needs"]
            else "GRANULARITY_AWARE_AMBIGUOUS"
            if row["ambiguous_needs"]
            or gi[u]["classification"] == "AMBIGUOUS_GRANULARITY"
            or any(
                c["unit"] == u and c["classification"] == "AMBIGUOUS"
                for c in collective
            )
            else "GRANULARITY_AWARE_UNCOVERED"
        )
        row["granularity_aware_status"] = state
        row["granularity_aware_provenance"] = {
            "origin": "DETERMINISTIC_DERIVATION",
            "rule": "strict_coverage_plus_validated_complete_collective_set",
        }
    ad = index(
        [
            {**row, "alternative": row["subject"]["alternative"]}
            for row in by_kind["ALTERNATIVE_COMPLETENESS"]
        ],
        "alternative",
    )
    alternatives = []
    for group in s["alternatives"]:
        for alt in group["alternatives"]:
            members = alt["units"]
            direct_complete = all(ui[u]["status"] == "COVERED" for u in members)
            strict = (
                "FULLY_DIRECTLY_COVERED"
                if direct_complete
                else "AMBIGUOUS"
                if any(ui[u]["status"] == "AMBIGUOUS_ONLY" for u in members)
                else "INCOMPLETE"
            )
            aware = (
                "FULLY_DIRECTLY_COVERED"
                if direct_complete
                else "FULLY_COVERED_ONLY_COLLECTIVELY"
                if all(
                    ui[u]["granularity_aware_status"] == "GRANULARITY_AWARE_COVERED"
                    for u in members
                )
                else "AMBIGUOUS"
                if any(
                    ui[u]["granularity_aware_status"] == "GRANULARITY_AWARE_AMBIGUOUS"
                    for u in members
                )
                else "INCOMPLETE"
            )
            a = alt["identity"]
            row = {
                "alternative": a,
                "obligation": group["obligation"],
                "units": members,
                "member_logic": alt["member_logic"],
                "alternative_logic": group["alternative_logic"],
                "strict_state": strict,
                "granularity_aware_state": aware,
                "missing_direct_members": [
                    u for u in members if ui[u]["status"] != "COVERED"
                ],
                "missing_diagnostic_members": [
                    u
                    for u in members
                    if ui[u]["granularity_aware_status"] != "GRANULARITY_AWARE_COVERED"
                ],
                "provenance": {"origin": "DETERMINISTIC_DERIVATION"},
            }
            if a in ad:
                payload = ad[a]["payload"]
                assert payload["strict_direct_complete"] == direct_complete, (
                    "strict alternative contradiction"
                )
                assert payload["granularity_aware_state"] in (None, aware), (
                    "diagnostic alternative contradiction"
                )
                row["consistency_decision"] = ad[a]
            alternatives.append(row)
    statistics: dict[str, Any] = {
        "pair_labels": counts(mapping, "label", LABELS),
        "strict_units": counts(units, "status", STATUSES),
        "needs": counts(needs, "classification", NEEDS),
        "strict_alternatives": counts(
            alternatives,
            "strict_state",
            ["FULLY_DIRECTLY_COVERED", "INCOMPLETE", "AMBIGUOUS"],
        ),
        "granularity": counts(granularity, "classification", GRANULARITY),
        "collective_sets": counts(collective, "classification", COLLECTIVE),
        "granularity_aware_units": counts(
            units, "granularity_aware_status", DIAGNOSTIC
        ),
        "granularity_aware_alternatives": counts(
            alternatives, "granularity_aware_state", ALTERNATIVES
        ),
    }
    for field, expected_counts in {
        "pair_labels": [15, 55, 506, 0],
        "strict_units": [15, 15, 2, 0],
        "needs": [10, 0, 8, 0, 0, 0],
        "strict_alternatives": [0, 12, 0],
        "granularity": [26, 6, 0, 0],
        "collective_sets": [3, 4, 0, 0],
        "granularity_aware_units": [18, 12, 2, 0],
        "granularity_aware_alternatives": [0, 0, 12, 0],
    }.items():
        assert list(statistics[field].values()) == expected_counts, (
            f"STOP: unexpected {field}: {statistics[field]}"
        )
    assert {
        (
            aliases["units"][row["unit"]],
            tuple(aliases["needs"][n] for n in row["needs"]),
        )
        for row in collective
        if row["classification"] == "VALID_MINIMAL_COLLECTIVE_SET"
    } == {(u, ("N09", "N10")) for u in ("U07", "U28", "U30")}
    comparisons = {}
    for name, pairs, source_units, source_needs, need_field in (
        ("primary", p, data["pu"]["units"], data["pn"]["needs"], "classification"),
        (
            "independent",
            i,
            data["independent"]["unit_coverage"],
            data["independent"]["need_classifications"],
            "label",
        ),
    ):
        sui, sni = index(source_units, "unit"), index(source_needs, "need")
        comparisons[name] = {
            "pair_label_counts": counts(list(pairs.values()), "label", LABELS),
            "pair_changes": [
                {
                    "need": n,
                    "unit": u,
                    "from": pairs[n, u]["label"],
                    "to": final[n, u]["label"],
                }
                for n, u in sorted(expected)
                if pairs[n, u]["label"] != final[n, u]["label"]
            ],
            "unit_changes": [
                {"unit": u, "from": sui[u]["status"], "to": ui[u]["status"]}
                for u in us
                if sui[u]["status"] != ui[u]["status"]
            ],
            "need_changes": [
                {
                    "need": row["need"],
                    "from": sni[row["need"]][need_field],
                    "to": row["classification"],
                }
                for row in needs
                if sni[row["need"]][need_field] != row["classification"]
            ],
        }
    statistics["comparisons"] = comparisons
    atomic_remaining = [
        u
        for u in us
        if gi[u]["classification"] == "ATOMIC_FOR_NEED_MAPPING"
        and ui[u]["status"] != "COVERED"
    ]
    failure_causes = {
        "INFORMATION_NEED_COVERAGE_FAILURE": {
            "status": "ESTABLISHED",
            "metrics": {
                "required_units": len(us),
                "strict_covered": statistics["strict_units"]["COVERED"],
                "missing_direct": sum(row["status"] != "COVERED" for row in units),
                "strict_complete_alternatives": statistics["strict_alternatives"][
                    "FULLY_DIRECTLY_COVERED"
                ],
            },
            "rationale": "The final semantic mapping fails the frozen every-required-unit direct rule. This establishes a coverage failure before retrieval, without selecting treatment effectiveness.",
        },
        "UNDER_SPECIFIED_INFORMATION_NEEDS": {
            "status": "POSSIBLE",
            "metrics": {
                "misformulated": statistics["needs"]["MISFORMULATED"],
                "ambiguous": statistics["needs"]["AMBIGUOUS"],
                "partial_only_needs": statistics["needs"]["PARTIAL_ONLY"],
            },
            "rationale": "Usable narrow questions leave complete-unit components unrequested. No need is adjudicated misformulated or ambiguous; a formulation defect is not established by partial coverage alone.",
        },
        "UNDER_DECOMPOSED_NEED_SET": {
            "status": "SUPPORTED",
            "metrics": {
                "atomic_not_directly_covered": len(atomic_remaining),
                "atomic_remaining_units": atomic_remaining,
                "diagnostic_missing": sum(
                    row["granularity_aware_status"] != "GRANULARITY_AWARE_COVERED"
                    for row in units
                ),
            },
            "rationale": "Reconciled atomic targets remain incomplete after the supplied complete collective sets. Missing focused acquisition questions are supported; no repaired need set or causal treatment attribution is tested.",
        },
        "NEED_TO_UNIT_GRANULARITY_MISMATCH": {
            "status": "SUPPORTED",
            "metrics": {
                "collectively_coverable_units": statistics["granularity"][
                    "COLLECTIVELY_COVERABLE"
                ],
                "accepted_minimal_sets": statistics["collective_sets"][
                    "VALID_MINIMAL_COLLECTIVE_SET"
                ],
                "rejected_sets": statistics["collective_sets"]["INSUFFICIENT"],
                "strict_covered": statistics["strict_units"]["COVERED"],
                "diagnostic_covered": statistics["granularity_aware_units"][
                    "GRANULARITY_AWARE_COVERED"
                ],
            },
            "rationale": "Three validated N09/N10 collective sets establish full units without a direct pair. Four proposed sets are insufficient. This diagnostic does not replace frozen direct coverage.",
        },
        "C5_SEMANTIC_ADJUDICATION_INSTABILITY": {
            "status": "ESTABLISHED",
            "metrics": {
                "pair_disagreements": len(disagreements),
                "shared_direct_pairs": len(shared),
                "unit_disagreements": len(by_kind["UNIT_STATUS"]),
                "need_disagreements": len(by_kind["NEED_CLASSIFICATION"]),
                "unresolved_decisions": data["decision"]["unresolved_count"],
            },
            "rationale": "Historical source disagreement materially affected direct facts and classifications. Exact bounded reconciliation resolves this checkpoint with zero unresolved decisions; it does not erase the observed instability or establish general reliability.",
        },
    }
    for row in failure_causes.values():
        row["provenance"] = {
            "origin": "DETERMINISTIC_DERIVATION",
            "scope": "descriptive_synthesis_of_reconciled_semantic_evidence",
        }
    statistics["failure_causes"] = failure_causes
    statistics["provenance"] = {"origin": "DETERMINISTIC_DERIVATION"}
    agreement_seal = [
        {"need": n, "unit": u, "label": p[n, u]["label"]}
        for n, u in sorted(expected - disagreements)
    ]
    provenance = {
        "packet_identity": PACKET,
        "bindings": BINDINGS,
        "input_sha256": data["hashes"],
        "source_mapping_1": "results/c5_mappings_v1.json",
        "source_mapping_2": "reliability/c5r_v1_adjudication.json",
        "agreed_pair_inheritance_seal_sha256": sha(encode(agreement_seal)),
        "agreed_pairs": len(agreement_seal),
        "disputed_pairs": len(disagreements),
        "shared_direct_rationales": len(shared),
        "materializer_sha256": sha(Path(__file__).read_bytes()),
        "frozen_needs_binding_limit": "Authenticated source declaration; semantic projection is not the original frozen-needs hash preimage.",
        "collective_validation_limit": "Exact supplied semantic decisions; membership, partial contributions, removal evidence and supplied-set antichain checked mechanically. No new sets or independent semantic sufficiency proof.",
        "derivation_origin": "DETERMINISTIC_DERIVATION",
        "stage_d": "READY BUT NOT PERFORMED",
        "u1_effectiveness": "UNKNOWN",
    }
    validation = {
        "status": "PASS",
        "propositions": 110,
        "proposition_counts": dict(Counter(row["kind"] for row in decisions)),
        "decision_counts": data["decision"]["decision_category_counts"],
        "pairs": len(mapping),
        "duplicate_pairs": 0,
        "missing_pairs": 0,
        "unexpected_pairs": 0,
        "checks": [
            "immutable_import_hashes",
            "packet_integrity_and_bindings",
            "exact_110_decisions",
            "source_frame_alignment",
            "agreement_inheritance_544",
            "dispute_application_32",
            "shared_direct_rationale_12",
            "unit_derivation_32",
            "unit_decision_consistency_11",
            "need_inheritance_11_and_decisions_7",
            "need_mechanical_consistency",
            "strict_alternatives_12",
            "alternative_decision_consistency_10",
            "granularity_decisions_32",
            "collective_propositions_6_sets_7",
            "collective_minimality_structure",
            "diagnostic_units_32",
            "diagnostic_alternatives_12",
            "failure_cause_metrics",
            "expected_count_checks",
        ],
        "provenance": {"origin": "DETERMINISTIC_DERIVATION"},
    }
    return {
        "mappings": mapping,
        "unit_coverage": units,
        "need_classifications": needs,
        "alternatives": alternatives,
        "granularity": sorted(granularity, key=lambda row: row["unit"]),
        "collective_coverage": collective,
        "statistics": statistics,
        "provenance": provenance,
        "validation": validation,
        "aliases": aliases,
    }


def render(result: dict[str, Any]) -> str:
    aliases = result["aliases"]
    ua, na = aliases["units"], aliases["needs"]
    lines = [
        "# Case 0011 final reviewed C.5",
        "",
        "Treatment-blind deterministic materialization of immutable bounded reconciliation-v2 decisions. No pair was adjudicated anew. Strict frozen-rule coverage and secondary granularity-aware coverage remain separate.",
        "",
        "## Exact final counts",
        "",
    ]
    stats = result["statistics"]
    for key in (
        "pair_labels",
        "strict_units",
        "needs",
        "strict_alternatives",
        "granularity",
        "collective_sets",
        "granularity_aware_units",
        "granularity_aware_alternatives",
    ):
        lines += [f"{key}: `{json.dumps(stats[key], sort_keys=True)}`", ""]
    for status in STATUSES:
        lines += [f"## {status} units", ""]
        for row in result["unit_coverage"]:
            if row["status"] != status:
                continue
            u = row["unit"]
            lines += [
                f"### {ua[u]}",
                "",
                row["statement"],
                "",
                f"Direct needs: {[na[n] for n in row['direct_needs']]}; partial needs: {[na[n] for n in row['partial_needs']]}; diagnostic: {row['granularity_aware_status']}.",
                "",
            ]
            for pair in result["mappings"]:
                if pair["unit"] == u and pair["label"] == "PARTIALLY_COVERS":
                    lines += [f"{na[pair['need']]} partial components:", ""]
                    if "missing_component" in pair:
                        lines += [
                            f"Covered: {pair['covered_component']}",
                            "",
                            f"Missing: {pair['missing_component']}",
                            "",
                        ]
                    else:
                        for evidence in pair["agreed_evidence"]:
                            lines += [
                                f"{evidence['artifact']} covered: {evidence.get('covered_part')}; missing: {evidence.get('missing_part')}",
                                "",
                            ]
    lines += ["## Final need classifications", ""]
    for row in result["need_classifications"]:
        lines += [
            f"### {row['alias']}: {row['classification']}",
            "",
            row["statement"],
            "",
            f"Direct: {[ua[u] for u in row['direct_units']]}; partial: {[ua[u] for u in row['partial_units']]}; unique: {[ua[u] for u in row['unique_units']]}",
            "",
            str(row["rationale"]),
            "",
        ]
    lines += ["## Every witness alternative", ""]
    for row in result["alternatives"]:
        lines += [
            f"### {row['obligation']} / {row['alternative']}",
            "",
            f"Members: {[ua[u] for u in row['units']]}; strict: {row['strict_state']}; diagnostic: {row['granularity_aware_state']}.",
            "",
            f"Missing direct: {[ua[u] for u in row['missing_direct_members']]}; missing diagnostic: {[ua[u] for u in row['missing_diagnostic_members']]}.",
            "",
        ]
        if "consistency_decision" in row:
            lines += [row["consistency_decision"]["payload"]["rationale"], ""]
            for member in row["consistency_decision"]["payload"]["members"]:
                lines += [f"{ua[member['unit']]}: {member['rationale']}", ""]
    lines += ["## All granularity decisions", ""]
    for row in result["granularity"]:
        lines += [
            f"{ua[row['unit']]}: **{row['classification']}**. {row['rationale']}",
            "",
        ]
    lines += [
        "## Every supplied collective set",
        "",
        result["provenance"]["collective_validation_limit"],
        "",
    ]
    for row in result["collective_coverage"]:
        lines += [
            f"### {ua[row['unit']]} ← {[na[n] for n in row['needs']]}: {row['classification']}",
            "",
            row["rationale"],
            "",
            row["minimality_analysis"],
            "",
        ]
        for c in row["contributions"]:
            lines += [
                f"{na[c['need']]}: {c['distinct_contribution']} Removal: {c['removal_analysis']}",
                "",
            ]
    lines += ["## Failure-cause synthesis", ""]
    for name, row in stats["failure_causes"].items():
        lines += [
            f"### {name}: {row['status']}",
            "",
            row["rationale"],
            "",
            f"Metrics: `{json.dumps(row['metrics'], sort_keys=True)}`",
            "",
        ]
    for name, comparison in stats["comparisons"].items():
        lines += [
            f"## {name} to reviewed changes",
            "",
            f"Source pair counts: {comparison['pair_label_counts']}",
            "",
        ]
        for key in ("pair_changes", "unit_changes", "need_changes"):
            lines += [f"{key}: {len(comparison[key])}", ""]
            for row in comparison[key]:
                subject = " / ".join(
                    na[row[k]] if k == "need" else ua[row[k]]
                    for k in ("need", "unit")
                    if k in row
                )
                lines += [f"- {subject}: {row['from']} → {row['to']}"]
            lines += [""]
    lines += [
        "## Provenance and limits",
        "",
        f"Packet identity: `{PACKET}`. Exact bindings: `{json.dumps(BINDINGS, sort_keys=True)}`.",
        "",
        "544 agreed labels are inherited; 32 disputed labels and 12 shared-direct rationales use exact decisions. Individual JSON rows retain source evidence, decision identity and origin. Statistics and diagnostics are deterministic derivations. Reviewed-gold statements and alternative memberships are unchanged. No model identity is included in reviewed mappings.",
        "",
        "Primary Stage C.5 = COMPLETE; Independent Stage C.5-R = COMPLETE; C.5 reliability comparison = COMPLETE; Reconciliation v1 = CONTRACT DEFECT / NO DECISIONS; Reconciliation v2 = COMPLETE; Final reviewed C.5 mapping = COMPLETE; Stage D = READY BUT NOT PERFORMED; U1 effectiveness = UNKNOWN.",
        "",
        "No treatment or confirmation data was accessed. Retrieval behavior, whole-task/obligation/need retrieval comparisons, strict frozen-rule treatment results, diagnostic treatment results and U1 effectiveness remain untested until Stage D. Semantic coverage failure alone does not select the final treatment outcome.",
        "",
        "Next step: Perform Case 0011 Stage D. Intentionally lift treatment blindness and compare whole-task retrieval, obligation-level retrieval and information-need retrieval against the final reviewed task gold and final reviewed C.5 semantic mapping. Report strict frozen-rule results and granularity-aware diagnostics separately.",
        "",
    ]
    return "\n".join(lines)


def replay(data: dict[str, Any]) -> dict[str, bytes]:
    result = build(data)
    files = {}
    for name in NAMES:
        if name.endswith(".json") and "output_digests" not in name:
            key = name.removeprefix("reviewed_c5_").removesuffix("_v1.json")
            value = {
                "schema": f"case-0011-reviewed-c5-v1/{key}",
                "packet_identity": PACKET,
                key: result[key],
            }
            reject_forbidden(value)
            files[name] = encode(value)
    files["REVIEWED_C5.md"] = render(result).encode()
    files["reviewed_c5_output_digests_v1.json"] = encode(
        {
            "schema": "case-0011-reviewed-c5-v1/output-digests",
            "files": {name: sha(raw) for name, raw in sorted(files.items())},
            "exclusions": [
                "reviewed_c5_output_digests_v1.json",
                ".local/codex-result.md",
            ],
            "provenance": "DETERMINISTIC_DERIVATION",
        }
    )
    return files


def publish(root: Path, data: dict[str, Any]) -> None:
    assert not any((root / name).exists() for name in NAMES), "OVERWRITE_REFUSED"
    files = replay(data)
    assert files == replay(data), "deterministic replay"
    root.mkdir(parents=True, exist_ok=True)
    for name, raw in files.items():
        with (root / name).open("xb") as stream:
            stream.write(raw)


def validate_completed(root: Path, data: dict[str, Any]) -> None:
    files = replay(data)
    assert files == replay(data)
    for name, raw in files.items():
        assert (root / name).read_bytes() == raw, f"replay mismatch: {name}"
    ledger = load((root / "reviewed_c5_output_digests_v1.json").read_bytes())
    for name, expected in ledger["files"].items():
        assert sha((root / name).read_bytes()) == expected


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--validate-completed", action="store_true")
    args = parser.parse_args()
    data = source_inputs()
    if not args.validate_completed:
        publish(ROOT, data)
    validate_completed(ROOT, data)
    print(json.dumps(build(data)["statistics"], sort_keys=True, indent=2))
