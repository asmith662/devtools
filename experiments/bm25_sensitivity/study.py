# Copyright (c) 2026
# ruff: noqa: C901, COM812, E501, EM101, EM102, TRY003, T201, PLR2004, PERF401 -- bounded scientific study and report

"""Full frozen factorial replay using R1.5 and native scoring oracles."""

from __future__ import annotations

import argparse
import asyncio
import gc
import json
import math
import statistics
import time
from dataclasses import replace
from itertools import product
from typing import Any

from devtools.context.retrieval.lexical.bm25 import (
    RepositoryTextLexicalBm25Settings,
    analyze_repository_text_lexical_query,
    retrieve_repository_text_documents_by_bm25,
)
from experiments.bm25_sensitivity.cases import Case, load
from experiments.bm25_sensitivity.metrics import measure, normalize
from experiments.bm25_sensitivity.protocol import (
    BASELINE,
    CASES,
    FILENAME,
    GRID,
    K1,
    B,
    key,
    select,
)
from experiments.bm25_sensitivity.storage import HERE, get, put
from experiments.codex_dogfood.case_0009.artifacts import (
    binary,
    digest,
    git,
    put_json,
    put_text,
)
from experiments.codex_dogfood.case_0009.freeze import canonical_index
from experiments.retrieval_diagnostics.adapters import canonical
from experiments.retrieval_diagnostics.comparison import compare
from experiments.retrieval_diagnostics.mechanics import Mechanics
from experiments.retrieval_diagnostics.serialization import encode


async def verify_protocol() -> str:
    """Require committed preregistration before any alternative scoring."""
    protocol_commit = (
        (
            await git(
                "log",
                "-1",
                "--format=%H",
                "--",
                "experiments/bm25_sensitivity/protocol.json",
            )
        )
        .decode()
        .strip()
    )
    await git("merge-base", "--is-ancestor", protocol_commit, "HEAD")
    for name in ("protocol.py", "protocol.json", "PROTOCOL.md", "VARIANTS.md"):
        path = "experiments/bm25_sensitivity/" + name
        if digest(await git("show", protocol_commit + ":" + path)) != digest(
            binary(HERE / name)
        ):
            raise ValueError("Pre-outcome protocol changed.")
    return protocol_commit


def baseline_engines(case: Case) -> dict[str, Mechanics]:
    """Replay native baseline once and prove historical rank/score equivalence."""
    index = case.index or canonical_index(case.documents)
    engines = {}
    for identity, ob, query in (("global", "global", case.task), *case.queries):
        result = retrieve_repository_text_documents_by_bm25(
            query=analyze_repository_text_lexical_query(text=query),
            index=index,
            maximum_results=len(case.documents.documents),
        )
        judgments = case.judgments.get(ob, ())
        capture = canonical(
            case.snapshot,
            identity,
            result,
            treatment=f"case-{case.number}-baseline",
            index_identity=case.hashes["inputs.pkl.gz"],
            filename_weight=BASELINE[2],
            obligation=judgments[0].obligation if judgments else None,
        )
        engine = Mechanics(capture, judgments)
        historical = case.historical[ob]
        actual = tuple((r.resource.address.value, r.score) for r in capture.rows)
        if len(actual) != len(historical) or any(
            a[0] != b[0] or not math.isclose(a[1], b[1], abs_tol=1e-10)
            for a, b in zip(actual, historical, strict=True)
        ):
            raise ValueError(
                f"Historical baseline parity differs: case {case.number}/{ob}"
            )
        engines[ob] = engine
    return engines


def configured(
    engines: dict[str, Mechanics], parameters: tuple[float, float, float]
) -> dict[str, Mechanics]:
    """Replay the R1.5 configuration, preserving every nonparameter choice."""
    return {
        ob: e.reconfigured(
            replace(
                e.capture.configuration,
                treatment="R1.6-" + key(parameters),
                k1=parameters[0],
                b=parameters[1],
                filename_weight=parameters[2],
            )
        )
        for ob, e in engines.items()
    }


def ranking_digest(engines: dict[str, Mechanics]) -> str:
    """Bind complete positive rank/score universes to reconstructable inputs."""
    return digest(
        encode(
            {
                ob: [
                    [r.resource.address.value, r.rank, r.score] for r in e.capture.rows
                ]
                for ob, e in engines.items()
            }
        )
    )


def run() -> tuple[dict[str, Any], dict[str, Any]]:
    """Execute all points; native oracle checks all fields and filename combinations."""
    protocol_commit = asyncio.run(verify_protocol())
    rows: dict[tuple[float, float, float], dict[str, Any]] = {
        p: {"parameters": p, "cases": []} for p in GRID
    }
    costs = {}
    for number in CASES:
        started = time.perf_counter()
        case = load(number)
        load_seconds = time.perf_counter() - started
        started = time.perf_counter()
        base = baseline_engines(case)
        base_seconds = time.perf_counter() - started
        base_metrics = measure(case, base)
        index = case.index or canonical_index(case.documents)
        oracle = {}
        scoring_started = time.perf_counter()
        for k1, b in product(K1, B):
            for ob, e in base.items():
                native_result = retrieve_repository_text_documents_by_bm25(
                    query=analyze_repository_text_lexical_query(text=e.capture.query),
                    index=index,
                    maximum_results=len(case.documents.documents),
                    settings=RepositoryTextLexicalBm25Settings(k1=k1, b=b),
                )
                oracle[k1, b, ob] = {
                    m.document_statistics.analysis.document.resource.address.value: (
                        m.content_score,
                        m.filename_score,
                    )
                    for m in native_result.matches
                }
        oracle_seconds = time.perf_counter() - scoring_started
        replay_started = time.perf_counter()
        for i, p in enumerate(GRID):
            engines = configured(base, p)
            for ob, e in engines.items():
                expected = {
                    address: content + p[2] * filename
                    for address, (content, filename) in oracle[p[0], p[1], ob].items()
                    if content + p[2] * filename > 0
                }
                actual = {address: r.score for address, r in e.rows.items()}
                if actual.keys() != expected.keys() or any(
                    not math.isclose(v, expected[a], abs_tol=1e-10)
                    for a, v in actual.items()
                ):
                    raise ValueError("Native oracle / R1.5 parameter score mismatch.")
                ordered = sorted(expected, key=lambda a: (-expected[a], e.positions[a]))
                if ordered != [r.resource.address.value for r in e.capture.rows]:
                    raise ValueError("Native oracle / parameter tie order mismatch.")
            metrics = measure(case, engines)
            metrics["selection_eligible"] = number != 8
            normalize(metrics, base_metrics)
            metrics["ranking_sha256"] = ranking_digest(engines)
            metrics["configuration_identity"] = {
                ob: e.capture.configuration.identity for ob, e in engines.items()
            }
            rows[p]["cases"].append(metrics)
            if i % 30 == 29:
                print(f"case {number}: {i + 1}/180 configurations verified", flush=True)
        costs[str(number)] = {
            "frozen_native_input_load_seconds": load_seconds,
            "baseline_validation_seconds": base_seconds,
            "native_30_field_parameter_oracles_seconds": oracle_seconds,
            "grid_analysis_replay_seconds": time.perf_counter() - replay_started,
            "note": "Development analysis cost, not production query latency. Retained historical index reused; Case 0009 content index reconstructed from frozen documents.",
        }
        del engines, base, index, case, oracle
        gc.collect()
    values = list(rows.values())
    for r in values:
        r["reach_safe"] = all(c["reach_safe"] for c in r["cases"])
        r["complete_for_selection"] = all(
            all(v is not None for v in c["normalized_exact"].values())
            for c in r["cases"]
            if c["selection_eligible"]
        )
        for metric in ("global", "max_own", "prefix_union", "prefix_occurrences"):
            v = [c["normalized"][metric] for c in r["cases"] if c["selection_eligible"]]
            r.setdefault("aggregates", {})[metric] = {
                "median": statistics.median(v)
                if all(x is not None for x in v)
                else None,
                "worst": max(v) if all(x is not None for x in v) else None,
            }
    data = {
        "schema": "r1.6-development-v1",
        "protocol_commit": protocol_commit,
        "protocol_sha256": digest(binary(HERE / "protocol.json")),
        "grid": GRID,
        "baseline": BASELINE,
        "cases": CASES,
        "rows": values,
        "selection": select(values),
        "source_evidence": "Pinned native corpus statistics, exact queries and independent gold from protocol.json; all scores reconstruct through R1.5 Mechanics.reconfigured. ranking_sha256 binds each complete positive universe.",
        "score_oracle": "Every k1/b pair checked against native content/filename scores; all six filename combinations and exact tie order checked.",
        "prospective_effectiveness": "UNKNOWN",
        "production_parameters_changed": False,
    }
    data["pareto"] = pareto(values)
    data["surfaces"] = surfaces(values)
    return data, costs


def pareto(rows: list[dict[str, Any]]) -> list[list[float]]:
    """Keep configurations not dominated across every case's four primary metrics."""
    safe = [r for r in rows if r["reach_safe"] and r["complete_for_selection"]]
    metrics = ("global", "max_own", "prefix_union", "prefix_occurrences")

    def vector(r: dict[str, Any]) -> tuple[int, ...]:
        return tuple(
            c[k] for c in r["cases"] if c["selection_eligible"] for k in metrics
        )

    vectors = [vector(r) for r in safe]
    return [
        list(r["parameters"])
        for i, r in enumerate(safe)
        if not any(
            all(a <= b for a, b in zip(v, vectors[i], strict=True))
            and any(a < b for a, b in zip(v, vectors[i], strict=True))
            for j, v in enumerate(vectors)
            if j != i
        )
    ]


def surfaces(rows: list[dict[str, Any]]) -> dict[str, Any]:
    """Retain main slices and interactions without a scalar quality optimizer."""
    output = {}
    for name, axis in (("k1", 0), ("b", 1), ("filename_weight", 2)):
        output[name] = [
            {
                "parameters": r["parameters"],
                "aggregates": r["aggregates"],
                "per_case": {str(c["case"]): c["normalized"] for c in r["cases"]},
            }
            for r in rows
            if all(r["parameters"][i] == BASELINE[i] for i in range(3) if i != axis)
        ]
    for a, b in ((0, 1), (0, 2), (1, 2)):
        output[f"interaction_{a}_{b}"] = [
            {
                "pair": [x, y],
                "remaining_parameter_slices": [
                    {"parameters": r["parameters"], "aggregates": r["aggregates"]}
                    for r in rows
                    if r["parameters"][a] == x and r["parameters"][b] == y
                ],
            }
            for x, y in product((K1, B, FILENAME)[a], (K1, B, FILENAME)[b])
        ]
    return output


def diagnostics(data: dict[str, Any]) -> dict[str, Any]:
    """Explain deterministic largest gain/regression for slices and selected roles."""
    configurations = {tuple(p) for p in data["selection"]["unique_challengers"]}
    configurations.update(
        p for p in GRID if sum(x != y for x, y in zip(p, BASELINE, strict=True)) == 1
    )
    output = []
    for number in CASES:
        case = load(number)
        base = baseline_engines(case)
        for p in sorted(configurations):
            changed = configured(base, p)
            paired = []
            for ob, js in case.judgments.items():
                for j in js:
                    if j.label == "REQUIRED":
                        a, b = (
                            base[ob].rows.get(j.resource.address.value),
                            changed[ob].rows.get(j.resource.address.value),
                        )
                        paired.append(
                            (b.rank - a.rank if a and b else 0, ob, j.resource)
                        )
            chosen = [
                min(paired, key=lambda r: (r[0], r[1], r[2].address.value)),
                max(paired, key=lambda r: (r[0], r[1], r[2].address.value)),
            ]
            for delta, ob, resource in chosen:
                output.append(
                    {
                        "case": number,
                        "parameters": p,
                        "rank_delta": delta,
                        "obligation": ob,
                        "resource": resource.address.value,
                        "A": base[ob].explain(resource),
                        "B": changed[ob].explain(resource),
                        "pair": compare(base[ob], changed[ob], resource),
                        "query_profile": changed[ob].query_profile(),
                    }
                )
        print(f"diagnostic representatives: case {number}", flush=True)
        del base, changed, case
        gc.collect()
    return {
        "schema": "r1.6-diagnostics-v1",
        "records": output,
        "rule": "Largest reached required gain/regression per case per baseline slice/selected challenger, deterministic obligation/address ties. Missing ranks retained in grid reach partitions; zero delta does not claim improvement.",
    }


def report(data: dict[str, Any]) -> str:
    """Report the complete cross-case development frame without adoption claims."""
    lines = [
        "# R1.6 canonical BM25 sensitivity development",
        "",
        "Development evidence only; prospective Case 0010 effectiveness remains UNKNOWN. Production parameters unchanged.",
        "",
        f"Protocol frozen at `{data['protocol_commit']}`; 180 configurations x six frozen cases, five selection-eligible and Case 0008 supplementary. Required-reach-safe configurations: {sum(r['reach_safe'] for r in data['rows'])}/180. Pareto configurations: {len(data['pareto'])}.",
        "",
        f"Selected roles: `{json.dumps(data['selection']['roles'], sort_keys=True)}`. Deduplicated challengers: `{data['selection']['unique_challengers']}`.",
        "",
        "## Per-case primary metrics",
        "",
        "| Config (k1,b,filename) | Case | Global | Max own | Prefix union | Occurrences | Required resources/cells/units |",
        "|---|---:|---:|---:|---:|---:|---|",
    ]
    selected = {BASELINE, *[tuple(p) for p in data["selection"]["unique_challengers"]]}
    for r in data["rows"]:
        if tuple(r["parameters"]) not in selected:
            continue
        for c in r["cases"]:
            lines.append(
                f"| {tuple(r['parameters'])} | {c['case']} | {c['global']} | {c['max_own']} | {c['prefix_union']} | {c['prefix_occurrences']} | {len(c['required_resource_reach'])}/{c['required_resource_total']}; {len(c['required_cells_reached'])}/{c['required_cells_total']}; {len(c['required_unit_judgments_reached'])}/{c['required_unit_judgments_total']} |"
            )
    for axis in ("k1", "b", "filename_weight"):
        lines += [
            "",
            f"## Baseline {axis} slice",
            "",
            "| Parameters | Median max-own ratio | Worst max-own ratio | Median union ratio | Worst union ratio |",
            "|---|---:|---:|---:|---:|",
        ]
        for s in data["surfaces"][axis]:
            a = s["aggregates"]
            lines.append(
                f"| {s['parameters']} | {a['max_own']['median']} | {a['max_own']['worst']} | {a['prefix_union']['median']} | {a['prefix_union']['worst']} |"
            )
    lines += [
        "",
        "Full absolute/per-obligation/top-K/partition data, exact normalized ratios and pair surfaces are in development.json.gz. Per-case tradeoffs and losing configurations are retained. Diagnostics retain query/term/source/overtaker mechanics in diagnostics.json.gz.",
        "",
        "Limitations: related in-repository development tasks, gold-version differences, one captured repository environment, no held-out outcomes. Development selection is not production adoption. Parameter interactions are not causally allocated. No query weighting, identifier treatment, BM25F or semantic-resolution work.",
        "",
        "BM25+/BM25L audit: VARIANTS.md. No R1.6b prerequisite justified on retained evidence; open variant questions remain recorded. R1.7 follows completed prospective R1.6; R2 remains mandatory.",
    ]
    return "\n".join(lines) + "\n"


def main() -> None:
    """Publish development evidence once or verify frozen analysis consistency."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("operation", choices=("run", "diagnostics", "verify"))
    args = parser.parse_args()
    if args.operation == "run":
        if (HERE / "development.json.gz").exists():
            raise FileExistsError("Development capture already exists.")
        data, costs = run()
        put(HERE / "development.json.gz", data)
        put_json(HERE / "costs.json", costs)
        put_text(HERE / "analysis.md", report(data))
        print(data["selection"])
    elif args.operation == "diagnostics":
        put(
            HERE / "diagnostics.json.gz", diagnostics(get(HERE / "development.json.gz"))
        )
    else:
        data = get(HERE / "development.json.gz")
        if (
            select(data["rows"]) != data["selection"]
            or pareto(data["rows"]) != data["pareto"]
            or surfaces(data["rows"]) != data["surfaces"]
            or report(data).encode() != binary(HERE / "analysis.md")
        ):
            raise ValueError("Development selection/surface/report replay differs.")
        if len(data["rows"]) != 180 or any(len(r["cases"]) != 6 for r in data["rows"]):
            raise ValueError("Grid/case partition differs.")
        print("deterministic selection/surface/report verified")


if __name__ == "__main__":
    main()
