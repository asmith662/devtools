# Copyright (c) 2026
# ruff: noqa: ANN401, E501 -- frozen candidate-discrimination analysis
"""Future deterministic join and design-aware analysis; never run during freeze."""

from collections import Counter
from typing import Any

from experiments.orchestration.storage import require
from experiments.source_grounding import contracts
from experiments.source_grounding.discrimination import estimators as stats

CLAIM = "CONDITIONAL_BROAD_CANDIDATE_DISCRIMINATION_ONLY; NO_REPOSITORY_RECALL_SUFFICIENCY_OR_PRODUCTION_ACCEPTANCE"
DECISION = "ESTIMATION_FIRST; NO_POST_HOC_THRESHOLDS_OR_P_VALUE_GATE"


def joined(universe: Any, selection: Any, treatment: Any, gold: Any) -> tuple[Any, Any]:
    """Only after independent treatment and gold completion may labels be joined."""
    statuses = {
        (c["obligation"], c["source"]["document_identity"]): c["verdict"]
        for c in treatment["cells"]
    }
    expected = {
        (u["obligation_id"], u["source"]["document_identity"])
        for u in universe["units"]
    }
    require(
        len(statuses) == len(treatment["cells"])
        and set(statuses) == expected
        and all(v in contracts.VERDICTS for v in statuses.values()),
        "Complete unchanged grounding universe",
    )
    gold_by = {
        selection["host"]["units"][c["candidate_id"]]: c for c in gold["judgments"]
    }
    require(
        len(gold_by) == len(gold["judgments"])
        and set(gold_by) == set(selection["selected"]),
        "Frozen gold sample identity",
    )
    full = []
    for unit in universe["units"]:
        status = statuses[unit["obligation_id"], unit["source"]["document_identity"]]
        row = {
            **unit,
            "grounding": status,
            "qualified": status == "GROUNDED_SOURCE",
            "stratum": unit["case"] + ":" + unit["obligation_id"],
        }
        if unit["identity"] in gold_by:
            row["gold"] = gold_by[unit["identity"]]
        full.append(row)
    strata = {universe["case"] + ":" + o: v for o, v in selection["allocation"].items()}
    return full, strata


def metrics(full: Any, strata: Any) -> Any:
    """Report raw counts beside weighted effects; uncertain is a separate state."""
    observed = [r for r in full if "gold" in r]
    output = {
        "population_pairs": len(full),
        "sample_pairs": len(observed),
        "strata": strata,
        "population_grounding": dict(Counter(r["grounding"] for r in full)),
        "sample_grounding": dict(Counter(r["grounding"] for r in observed)),
        "sample_pursuit_labels": dict(
            Counter(r["gold"]["pursuit_value"] for r in observed),
        ),
        "sample_gold_labels": {
            role: dict(Counter(r["gold"][role] for r in observed))
            for role in ("source_usefulness", "target_usefulness", "pursuit_value")
        },
        "candidate_reduction": sum(not r["qualified"] for r in full) / len(full),
    }
    comparisons = {}
    for kind in ("pursuit_value", "source_usefulness", "target_usefulness"):
        domains = {}
        functions = {}
        for status in contracts.VERDICTS:

            def x(r: Any, status: str = status, kind: str = kind) -> int:
                return int(r["grounding"] == status and r["gold"][kind] != "UNCERTAIN")

            def y(r: Any, status: str = status, kind: str = kind) -> int:
                return int(r["grounding"] == status and r["gold"][kind] == "USEFUL")

            estimate = stats.ratio(observed, strata, x, y)
            estimate["denominator_semantics"] = "RESOLVED_GOLD_ONLY"
            estimate["uncertain_sample_n"] = sum(
                r["grounding"] == status and r["gold"][kind] == "UNCERTAIN"
                for r in observed
            )
            estimate["population_grounding_n"] = sum(
                r["grounding"] == status for r in full
            )
            domains[status] = estimate
            functions[status] = (x, y)
        g, n = "GROUNDED_SOURCE", "NOT_GROUNDED_SOURCE"
        comparisons[kind] = {
            "by_grounding": domains,
            **stats.contrast(
                observed,
                strata,
                domains[g],
                domains[n],
                *functions[g],
                *functions[n],
            ),
        }
    output["discrimination"] = comparisons
    output["useful_pursuit_retention"] = stats.ratio(
        observed,
        strata,
        lambda r: int(r["gold"]["pursuit_value"] == "USEFUL"),
        lambda r: int(r["gold"]["pursuit_value"] == "USEFUL" and r["qualified"]),
    )
    output["useful_target_retention"] = stats.target_retention(full, observed, strata)
    targets = {(r["case"], r["target"]["document_identity"]) for r in full}
    retained = {
        (r["case"], r["target"]["document_identity"]) for r in full if r["qualified"]
    }
    output["unique_target_reduction"] = {
        "population": len(targets),
        "retained": len(retained),
        "fraction_removed": 1 - len(retained) / len(targets),
    }
    output["unknown_handling"] = (
        "UNCERTAIN reported separately and excluded from resolved-only densities; never NOT_USEFUL"
    )
    return output


def analyze(cases: Any) -> Any:
    """Aggregate only frozen finite candidate populations, not historical tasks."""
    results = {}
    cohort = []
    all_strata = {}
    for identity, (universe, selection, treatment, gold) in cases.items():
        full, strata = joined(universe, selection, treatment, gold)
        own = metrics(full, strata)
        own["obligations"] = {
            oid: metrics(
                [r for r in full if r["obligation_id"] == oid],
                {identity + ":" + oid: s},
            )
            for oid, s in selection["allocation"].items()
        }
        results[identity] = own
        cohort.extend(full)
        all_strata.update(strata)
    return {
        "schema": "candidate-discrimination-analysis-v1",
        "claim_boundary": CLAIM,
        "decision_protocol": DECISION,
        "cases": results,
        "cohort": metrics(cohort, all_strata),
        "directional_consistency": {
            c: v["discrimination"]["pursuit_value"]["risk_difference"]
            for c, v in results.items()
        },
        "no_causal_or_confirmation_inference": True,
    }
