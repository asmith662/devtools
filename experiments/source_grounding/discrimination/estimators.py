# Copyright (c) 2026
# ruff: noqa: ANN401, PLR2004, PLR0913, PLR0917, C901, PLR0912 -- explicit design-based finite-population arithmetic
"""Stratified ratio estimation and linearization, with explicit sparse outcomes."""

import math
from statistics import variance
from typing import Any

from experiments.orchestration.storage import require

MIN_DOMAIN = 10
MIN_OUTCOME = 5


def ratio(rows: Any, strata: Any, x: Any, y: Any) -> Any:
    """Estimate a ratio of HT totals; unknown labels are excluded explicitly."""
    terms = [(r, x(r), y(r)) for r in rows]
    numerator = sum(strata[r["stratum"]]["weight"] * v for r, _, v in terms)
    denominator = sum(strata[r["stratum"]]["weight"] * v for r, v, _ in terms)
    domain = [(r, a, b) for r, a, b in terms if a]
    weights = [strata[r["stratum"]]["weight"] * a for r, a, _ in domain]
    effective = sum(weights) ** 2 / sum(w * w for w in weights) if weights else 0
    result = {
        "numerator_HT": numerator,
        "denominator_HT": denominator,
        "sample_domain_n": len(domain),
        "effective_sample_n": effective,
        "estimate": numerator / denominator if denominator else None,
        "standard_error": None,
        "interval_95": None,
        "status": "UNDEFINED" if not denominator else "ESTIMATED",
        "uncertainty": "ZERO_DENOMINATOR" if not denominator else None,
    }
    if not denominator:
        return result
    census = all(s["N"] == s["n"] for s in strata.values())
    if census:
        result.update(
            status="CENSUS",
            standard_error=0.0,
            interval_95=[result["estimate"]] * 2,
            uncertainty="NO_SAMPLING_ERROR; SEMANTIC_UNCERTAINTY_SEPARATE",
        )
        return result
    # A normal approximation with only one or two observed domain outcomes is
    # not evidence of precision. Retain the point and explicitly withhold its CI.
    positives = sum(bool(b) for _, _, b in domain)
    if (
        len(domain) < MIN_DOMAIN
        or min(positives, len(domain) - positives) < MIN_OUTCOME
    ):
        result["uncertainty"] = "SPARSE_OR_DEGENERATE_DOMAIN; CI_UNAVAILABLE"
        return result
    rhat = result["estimate"]
    linear = {r["identity"]: b - rhat * a for r, a, b in terms}
    var = variance_total(rows, strata, linear)
    if var is None:
        result["uncertainty"] = "STRATUM_VARIANCE_UNAVAILABLE"
        return result
    se = math.sqrt(var) / denominator
    result.update(
        standard_error=se,
        interval_95=[max(0, rhat - 1.96 * se), min(1, rhat + 1.96 * se)],
        uncertainty="STRATIFIED_FPC_DELTA_NORMAL; APPROXIMATE",
    )
    return result


def variance_total(rows: Any, strata: Any, values: Any) -> float | None:
    """SRSWOR Neyman variance of an HT total; strata are case x obligation."""
    result = 0.0
    for identity, design in strata.items():
        selected = [values[r["identity"]] for r in rows if r["stratum"] == identity]
        require(len(selected) == design["n"], "Sample/stratum completeness")
        if design["N"] == design["n"]:
            continue
        if len(selected) < 2:
            return None
        result += (
            design["N"] ** 2
            * (1 - design["n"] / design["N"])
            * variance(selected)
            / design["n"]
        )
    return result


def contrast(
    rows: Any,
    strata: Any,
    left: Any,
    right: Any,
    xl: Any,
    yl: Any,
    xr: Any,
    yr: Any,
) -> Any:
    """Use joint linearization, retaining covariance between disjoint domains."""
    a, b = left["estimate"], right["estimate"]
    diff = a - b if a is not None and b is not None else None
    rr = a / b if a is not None and b is not None and b != 0 else None
    result = {
        "risk_difference": diff,
        "risk_ratio": rr,
        "ratio_status": "UNDEFINED" if rr is None else "DEFINED",
        "difference_standard_error": None,
        "difference_interval_95": None,
        "ratio_interval_95": None,
    }
    if (
        diff is None
        or left["standard_error"] is None
        or right["standard_error"] is None
    ):
        return result
    linear = {
        r["identity"]: (yl(r) - a * xl(r)) / left["denominator_HT"]
        - (yr(r) - b * xr(r)) / right["denominator_HT"]
        for r in rows
    }
    var = variance_total(rows, strata, linear)
    if var is not None:
        se = math.sqrt(var)
        result.update(
            difference_standard_error=se,
            difference_interval_95=[
                max(-1, diff - 1.96 * se),
                min(1, diff + 1.96 * se),
            ],
        )
    if rr is not None and a > 0 and b > 0:
        log_linear = {
            r["identity"]: (yl(r) - a * xl(r)) / (left["denominator_HT"] * a)
            - (yr(r) - b * xr(r)) / (right["denominator_HT"] * b)
            for r in rows
        }
        variance_log = variance_total(rows, strata, log_linear)
        if variance_log is not None:
            delta = 1.96 * math.sqrt(variance_log)
            result["ratio_interval_95"] = [
                math.exp(math.log(rr) - delta),
                math.exp(math.log(rr) + delta),
            ]
    return result


def inclusion(population: int, sample: int, multiplicity: int) -> float:
    """Probability at least one pair for a particular target is selected."""
    require(
        0 <= multiplicity <= population and 0 < sample <= population,
        "Target inclusion inputs",
    )
    return 1 - (
        math.comb(population - multiplicity, sample) / math.comb(population, sample)
        if population - multiplicity >= sample
        else 0
    )


def target_retention(full: Any, observed: Any, strata: Any) -> Any:
    """HT target-obligation ratio with exact induced target inclusion weights."""
    targets: dict[tuple[str, str], Any] = {}
    for row in full:
        key = row["stratum"], row["target"]["document_identity"]
        entry = targets.setdefault(key, {"multiplicity": 0, "qualified": False})
        entry["multiplicity"] += 1
        entry["qualified"] |= row["qualified"]
    selected: dict[tuple[str, str], str] = {}
    for row in observed:
        key = row["stratum"], row["target"]["document_identity"]
        label = row["gold"]["target_usefulness"]
        require(
            key not in selected or selected[key] == label,
            "Target usefulness inconsistency",
        )
        selected[key] = label
    contributions = {}
    numerator = denominator = 0.0
    unknown = 0
    for key, label in selected.items():
        spec = strata[key[0]]
        pi = inclusion(spec["N"], spec["n"], targets[key]["multiplicity"])
        useful = label == "USEFUL"
        denominator += useful / pi
        numerator += (useful and targets[key]["qualified"]) / pi
        unknown += label == "UNCERTAIN"
        contributions[key] = (
            pi,
            float(useful),
            float(useful and targets[key]["qualified"]),
        )
    rhat = numerator / denominator if denominator else None
    result = {
        "unit": "TARGET_OBLIGATION",
        "numerator_HT": numerator,
        "denominator_HT": denominator,
        "estimate": rhat,
        "sample_unique_targets": len(selected),
        "uncertain_sample_targets": unknown,
        "standard_error": None,
        "interval_95": None,
        "status": "UNDEFINED" if rhat is None else "ESTIMATED",
    }
    if rhat is None:
        return result
    if all(s["N"] == s["n"] for s in strata.values()):
        result.update(standard_error=0, interval_95=[rhat, rhat], status="CENSUS")
        return result
    useful_observed = [
        targets[k]["qualified"] for k, label in selected.items() if label == "USEFUL"
    ]
    if (
        len(useful_observed) < MIN_DOMAIN
        or min(sum(useful_observed), len(useful_observed) - sum(useful_observed))
        < MIN_OUTCOME
    ):
        result["uncertainty"] = "SPARSE_OR_DEGENERATE_TARGET_DOMAIN; CI_UNAVAILABLE"
        return result
    var = 0.0
    for key, (pi, x, y) in contributions.items():
        for other, (pj, a, b) in contributions.items():
            if key[0] != other[0]:
                continue
            s = strata[key[0]]
            if key == other:
                joint = pi
            else:
                joint = (
                    pi
                    + pj
                    - inclusion(
                        s["N"],
                        s["n"],
                        targets[key]["multiplicity"] + targets[other]["multiplicity"],
                    )
                )
            if joint <= 0:
                result["uncertainty"] = "JOINT_INCLUSION_UNAVAILABLE"
                return result
            var += (
                (joint - pi * pj)
                / joint
                * ((y - rhat * x) / pi)
                * ((b - rhat * a) / pj)
            )
    if var >= 0:
        se = math.sqrt(var) / denominator
        result.update(
            standard_error=se,
            interval_95=[max(0, rhat - 1.96 * se), min(1, rhat + 1.96 * se)],
            uncertainty="INDUCED_TARGET_HT_DELTA; APPROXIMATE",
        )
    else:
        result["uncertainty"] = "NEGATIVE_VARIANCE_ESTIMATE; CI_UNAVAILABLE"
    return result
