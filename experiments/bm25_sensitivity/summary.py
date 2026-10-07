# Copyright (c) 2026
# ruff: noqa: COM812 -- formatter convention

"""Describe case/obligation sensitivity and finite contrasts, not parameter tuning."""

from __future__ import annotations

from itertools import combinations
from typing import Any

from experiments.bm25_sensitivity.protocol import BASELINE, GRID
from experiments.bm25_sensitivity.storage import HERE, get, put


def summarize(data: dict[str, Any]) -> dict[str, Any]:
    """Retain exact main slices and interaction contrasts per frozen case."""
    lookup = {
        tuple(r["parameters"]): {c["case"]: c for c in r["cases"]} for r in data["rows"]
    }
    main = []
    contrasts = []
    obligations = []
    for number, base in lookup[BASELINE].items():
        for axis, name in enumerate(("k1", "b", "filename_weight")):
            rows = [
                p
                for p in GRID
                if all(p[i] == BASELINE[i] for i in range(3) if i != axis)
            ]
            for metric in ("global", "max_own", "prefix_union", "prefix_occurrences"):
                series = [
                    {
                        "value": p[axis],
                        "absolute": lookup[p][number][metric],
                        "baseline_ratio": lookup[p][number]["normalized"][metric],
                    }
                    for p in rows
                ]
                main.append(
                    {
                        "case": number,
                        "parameter": name,
                        "metric": metric,
                        "series": series,
                    }
                )
        for ob, depth in base["own_depths"].items():
            values = [lookup[p][number]["own_depths"][ob] for p in GRID]
            reached = [v for v in values if v is not None]
            obligations.append(
                {
                    "case": number,
                    "obligation": ob,
                    "baseline": depth,
                    "minimum": min(reached) if reached else None,
                    "maximum": max(reached) if reached else None,
                    "miss_configurations": sum(v is None for v in values),
                }
            )
        for a, b in combinations(range(3), 2):
            for p in GRID:
                if any(p[i] != BASELINE[i] for i in range(3) if i not in (a, b)):
                    continue
                pa, pb = list(BASELINE), list(BASELINE)
                pa[a], pb[b] = p[a], p[b]
                effects = {}
                for metric in (
                    "global",
                    "max_own",
                    "prefix_union",
                    "prefix_occurrences",
                ):
                    observed = [
                        lookup[q][number][metric]
                        for q in (p, tuple(pa), tuple(pb), BASELINE)
                    ]
                    effects[metric] = (
                        observed[0] - observed[1] - observed[2] + observed[3]
                        if all(v is not None for v in observed)
                        else None
                    )
                contrasts.append(
                    {
                        "case": number,
                        "axes": [a, b],
                        "parameters": list(p),
                        "finite_interaction_contrast": effects,
                    }
                )
    return {
        "schema": "r1.6-sensitivity-details-v1",
        "main_slices": main,
        "obligation_ranges": obligations,
        "interactions": contrasts,
        "limit": (
            "Finite metric contrast joint-minus-single effects plus baseline; "
            "descriptive rank interactions, not additive score-causal allocation. "
            "No new configurations or selection rules."
        ),
    }


if __name__ == "__main__":
    put(HERE / "sensitivity_details.json", summarize(get(HERE / "development.json.gz")))
