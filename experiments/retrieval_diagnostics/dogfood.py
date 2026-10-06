# Copyright (c) 2026
# ruff: noqa: COM812, E501, EM101, PLR2004, T201, TRY003 -- deterministic scientific capture CLI
"""Dogfood diagnostics on frozen Case 0009, without changing its conclusions."""

from __future__ import annotations

import argparse
import asyncio
import gzip
import json
from collections import Counter
from pathlib import Path
from typing import Any

from devtools.context.localization.identity import (
    LocalizationObligationIdentity,
    LocalizationTaskIdentity,
)
from devtools.core.paths import resolve_path
from devtools.resources.filesystem import TextFile, write
from experiments.codex_dogfood.case_0009.analyze import verify_commits
from experiments.codex_dogfood.case_0009.artifacts import (
    CASE,
    binary,
    digest,
    git,
    put_binary,
    read_json,
)
from experiments.codex_dogfood.case_0009.freeze import load_inputs
from experiments.retrieval_diagnostics.adapters import fields, from_rows
from experiments.retrieval_diagnostics.comparison import compare
from experiments.retrieval_diagnostics.mechanics import Mechanics
from experiments.retrieval_diagnostics.models import (
    Configuration,
    DiagnosticPolicy,
    Frame,
    Judgment,
)
from experiments.retrieval_diagnostics.serialization import encode

HERE = Path(__file__).resolve().parent
STAGE_D = "91f1d109d24e9a7f143989702936be93e231834b"


async def _verified_chain() -> dict[str, Any]:
    """Retain the original chain plus exact committed Stage D analysis bytes."""
    chain = await verify_commits()
    await git("merge-base", "--is-ancestor", STAGE_D, "HEAD")
    path = "experiments/codex_dogfood/case_0009/analysis.json"
    if digest(await git("show", STAGE_D + ":" + path)) != digest(
        binary(CASE / "analysis.json")
    ):
        raise ValueError("Frozen Stage D analysis bytes differ.")
    chain["stage_d_commit"] = STAGE_D
    return chain


def build() -> dict[str, Any]:  # noqa: C901 -- explicit frozen-chain and partition validation
    """Consume verified frozen captures and independent gold for all 37 cells."""
    chain = asyncio.run(_verified_chain())
    native = load_inputs()
    sealed = read_json(CASE / "stage_b_integrity.json")
    for name, expected in sealed["sha256"].items():
        if digest(binary(CASE / name)) != expected:
            raise ValueError("Dogfood frozen capture hash mismatch.")
    results = json.loads(gzip.decompress(binary(CASE / "results.json.gz")))
    gold = read_json(CASE / "adjudication/judgments.json")
    stage_d = read_json(CASE / "analysis.json")
    settings = read_json(CASE / "treatment.json")["settings"]
    frame = Frame(
        native["snapshot"].repository_id, native["snapshot"].id, native["corpus"].id
    )
    if (
        any(
            gold["frame"][key] != str(value)
            for key, value in (
                ("repository_id", frame.repository),
                ("snapshot_id", frame.snapshot),
                ("corpus_id", frame.corpus),
            )
        )
        or results["snapshot_id"] != str(frame.snapshot)
        or results["corpus_id"] != str(frame.corpus)
    ):
        raise ValueError("Dogfood frame identity differs.")
    resource_map = {
        d.resource.address.value: d.resource for d in native["documents"].documents
    }
    configs = {
        arm: Configuration(
            "case-0009-" + arm,
            digest(
                encode(
                    {
                        "inputs_sha256": digest(binary(CASE / "inputs.pkl.gz")),
                        "rankings_sha256": sealed["deterministic_rankings_sha256"],
                        "arm": arm,
                    }
                )
            ),
            "canonical" if arm == "A" else "identifier",
            settings["k1"],
            settings["b"],
            settings["filename_weight"],
        )
        for arm in ("A", "B")
    }
    states = {arm: fields(native["documents"], configs[arm]) for arm in ("A", "B")}
    cells = []
    profiles: dict[str, dict[str, Any]] = {"A": {}, "B": {}}
    for obligation in gold["obligations"]:
        key = obligation["identity"]
        native_obligation = LocalizationObligationIdentity(
            LocalizationTaskIdentity(gold["frame"]["task_identity"]), key
        )
        judgments = tuple(
            Judgment(
                frame,
                resource_map[c["resource"]["address"]],
                native_obligation,
                c["label"],
                tuple(c["required_units"]),
            )
            for c in gold["cells"]
            if c["obligation"] == key
        )
        engines = {}
        for arm in ("A", "B"):
            lane = results["arms"][arm][key + "-query"]
            capture = from_rows(
                native["snapshot"],
                native["documents"],
                key + "-query",
                lane["query_text"],
                tuple(lane["query_terms"]),
                lane["rows"],
                configs[arm],
                states[arm],
                complete=True,
                obligation=native_obligation,
            )
            engines[arm] = Mechanics(capture, judgments, DiagnosticPolicy())
            profiles[arm][key] = engines[arm].query_profile()
        for j in judgments:
            if j.label != "REQUIRED":
                continue
            a, b = (engines[arm].explain(j.resource) for arm in ("A", "B"))
            paired = compare(engines["A"], engines["B"], j.resource)
            prior = next(
                r
                for r in stage_d["required_attribution"]
                if r["lane"] == key and r["resource"] == j.resource.address.value
            )
            if (
                a["rank"],
                b["rank"],
                paired["rank_delta"],
                paired["new_overtakers"],
            ) != (
                prior["A_rank"],
                prior["B_rank"],
                prior["delta"],
                prior["new_overtakers"],
            ):
                raise ValueError("Diagnostic changed frozen R1 observations.")
            cells.append(
                {
                    "obligation": key,
                    "resource": j.resource.address.value,
                    "A": a,
                    "B": b,
                    "pair": paired,
                }
            )
    if len(cells) != 37 or len({(c["obligation"], c["resource"]) for c in cells}) != 37:
        raise ValueError("Required cell diagnostic partition differs.")
    summaries = {}
    for arm in ("A", "B"):
        summaries[arm] = {
            "statuses": dict(Counter(c[arm]["status"] for c in cells)),
            "primary_failures": dict(
                Counter(
                    c[arm]["failure_attribution"]["primary"] or "NOT_ESTABLISHED"
                    for c in cells
                )
            ),
            "score_reconstructions": sum(c[arm]["score_reconstructed"] for c in cells),
            "structural_support": "NOT_ASSESSED: no structural capture was supplied by frozen R1",
            "context_disclosure": "OUTSIDE_DIAGNOSTIC_SCOPE",
            "obligation_failure": "OUTSIDE_DIAGNOSTIC_SCOPE",
        }
    return {
        "schema": "retrieval-diagnostics-case-0009-v1",
        "ownership": "EXPERIMENTAL EVALUATION; NO RETRIEVAL POLICY",
        "chain": chain,
        "input_sha256": {
            name: digest(binary(CASE / name))
            for name in (
                "results.json.gz",
                "analysis.json",
                "treatment.json",
                "inputs.pkl.gz",
            )
        },
        "policy": {
            "substantial_unnecessary_ahead": 20,
            "common_fraction": 0.25,
            "low_idf": 1.5,
            "overtaker_limit": 5,
            "meaning": "Descriptive instrumentation thresholds, not frozen R1 decision gates or new query weights.",
        },
        "summaries": summaries,
        "paired_partial_hidden_match_cells": sum(
            bool(c["pair"]["representation"]["witnesses"]) for c in cells
        ),
        "paired_positive_reach_rescues": sum(
            c["pair"]["representation"]["positive_reach_rescue"] for c in cells
        ),
        "cells": cells,
        "query_profiles": profiles,
        "R1_outcome": stage_d["decision"]["outcome"],
        "no_tuning_no_reranking_no_production_change": True,
    }


def report(data: dict[str, Any]) -> str:  # noqa: C901 -- bounded scientific report sections
    """Summarize all cells and representative term effects from diagnostic output."""
    lines = [
        "# R1.5 Case 0009 diagnostic dogfood",
        "",
        "Development/dogfood instrumentation after the completed R1 evaluation. No new prospective treatment, parameter tuning or gold adjudication. Frozen R1 outcome remains **RETAIN AS SEPARATE RETRIEVAL VIEW**.",
        "",
        "Policy: a VERIFIED_RANKING_DISCRIMINATION_FAILURE requires independent REQUIRED gold, positive evidence and at least 20 judged UNNECESSARY overtakers. This descriptive threshold does not define a universal defect or reuse R1's 20% promotion criterion.",
        "",
        "| Arm | REQUIRED cells | Reached | Scores reproduced | Verified ranking discrimination | Not established |",
        "|---|---:|---:|---:|---:|---:|",
    ]
    for arm in ("A", "B"):
        s = data["summaries"][arm]
        lines.append(
            f"| {arm} | 37 | {s['statuses'].get('REACHED', 0)} | {s['score_reconstructions']} | {s['primary_failures'].get('RANKING_DISCRIMINATION_FAILURE', 0)} | {s['primary_failures'].get('NOT_ESTABLISHED', 0)} |"
        )
    lines += [
        "",
        f"Paired partial hidden lexical-match cells: {data['paired_partial_hidden_match_cells']}; positive-reach rescues: {data['paired_positive_reach_rescues']}. A hidden component match is not proof that a necessary information unit became newly reachable. All cells are positive in both arms, so possible vocabulary-semantic mismatch is not established here. Structural/role/exact support was not captured by R1 and is NOT_ASSESSED, not absent. Context and obligation failures remain outside lexical diagnosis.",
        "",
        "## Complete REQUIRED-cell summary",
        "",
        "| Obligation | Resource | A rank | B rank | A unnecessary ahead | B unnecessary ahead | A/B primary failure | Partial hidden match |",
        "|---|---|---:|---:|---:|---:|---|---|",
    ]
    for c in data["cells"]:
        a, b = c["A"], c["B"]
        lines.append(
            f"| {c['obligation']} | `{c['resource']}` | {a['rank']} | {b['rank']} | {a['ranking']['ahead_labels'].get('UNNECESSARY', 0)} | {b['ranking']['ahead_labels'].get('UNNECESSARY', 0)} | {a['failure_attribution']['primary'] or 'NOT_ESTABLISHED'} / {b['failure_attribution']['primary'] or 'NOT_ESTABLISHED'} | {bool(c['pair']['representation']['witnesses'])} |"
        )
    lines += ["", "## Requested mechanical examples", ""]
    examples = (
        ("package", "pyproject.toml"),
        ("frame", "src/devtools/context/repository/resource.py"),
        ("readiness", "src/devtools/context/localization/resolution/promotion.py"),
        ("tests", "tests/context/localization/resolution/test_resolution.py"),
    )
    for obligation, address in examples:
        c = next(
            c
            for c in data["cells"]
            if c["obligation"] == obligation and c["resource"] == address
        )
        p = c["pair"]
        lines += [
            f"### {obligation}: `{address}`",
            "",
            f"Rank {p['rank_A']} -> {p['rank_B']}; score {p['score_A']} -> {p['score_B']}; weighted field deltas {p['mechanics']['field_weighted_deltas']}. New overtakers {len(p['new_overtakers'])}; removed {len(p['removed_overtakers'])}; new overtaker labels {p['new_overtaker_labels']}.",
            "",
        ]
        for t in p["mechanics"]["term_deltas"]:
            if t["B"] and (t["A"] is None or t["tf_delta"]):
                b = t["B"]
                observed = [s["observed"] for s in b["source"]["examples"]]
                query = [s["observed"] for s in b["query_source"]["examples"]]
                lines.append(
                    f"- {t['field']} `{t['term']}`: sources {observed}; query {query}; TF {t['A']['tf'] if t['A'] else 0}->{b['tf']}; weighted contribution delta {t['weighted_delta']}; B contribution {b['weighted_contribution']}."
                )
        if obligation == "readiness":
            lines += [
                "",
                "`LocalizationAssessment` occurs in this lane's query, not in promotion.py: this is a query-side identifier gain. It exposes `localization` and `assessment` against the exact document forms listed above. `supported_witnesses` contributes one occurrence each of `supported` and `witnesses`; the `supported` BM25 term contribution aggregates all seven occurrences and cannot be additively assigned to one identifier.",
            ]
        lines += [
            "",
            "Shared-term TF/DF/IDF, document/average lengths and saturation changes are retained for every term, including unchanged TF. The field deltas and overtaker sets are exact; isolated causal allocation among interacting statistics requires a separately frozen ablation.",
        ]
    lines += [
        "",
        "## Query discrimination examples (content field)",
        "",
        "| Arm/lane | Term | DF | IDF | Fraction | REQUIRED | HELPFUL | UNNECESSARY | Required yield | Useful yield |",
        "|---|---|---:|---:|---:|---:|---:|---:|---:|---:|",
    ]
    for arm, lanes in data["query_profiles"].items():
        for lane, terms in lanes.items():
            for t in terms:
                if t["term"] not in {
                    "localization",
                    "frame",
                    "supported",
                    "package",
                    "tests",
                }:
                    continue
                f = next(f for f in t["fields"] if f["field"] == "content")
                labels = t["judged_labels"]
                lines.append(
                    f"| {arm}/{lane} | {t['term']} | {f['df']} | {f['idf']} | {f['fraction_of_frame']} | {labels.get('REQUIRED', 0)} | {labels.get('HELPFUL_ONLY', 0)} | {labels.get('UNNECESSARY', 0)} | {t['required_yield']} | {t['useful_yield']} |"
                )
    lines += [
        "",
        "Yields use the union of positive-weight content/filename matches, while the DF column is content-specific. Terms are descriptive, not automatically bad, removed or downweighted. Unjudged is never unnecessary. Source spans, complete term profiles, overtaker pair deltas and configuration identities are in case_0009.json.gz (deterministic gzip of stable JSON).",
        "",
        "Next: R1.6 scientifically frozen canonical BM25 sensitivity. No grid search, query weighting or BM25F implemented.",
    ]
    return "\n".join(lines) + "\n"


def main() -> None:
    """Publish or verify exact diagnostics from frozen inputs."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("operation", choices=("build", "verify"))
    args = parser.parse_args()
    data = build()
    artifacts = {
        "case_0009.json.gz": gzip.compress(encode(data), mtime=0),
        "case_0009.md": report(data).encode(),
    }
    for name, content in artifacts.items():
        if args.operation == "build":
            if name.endswith(".gz"):
                if not (HERE / name).exists():
                    put_binary(HERE / name, content)
                elif binary(HERE / name) != content:
                    raise ValueError(
                        "Existing diagnostic capture differs; publish a new version explicitly."
                    )
            else:
                write(
                    TextFile(resolve_path(HERE / name), content.decode()),
                    overwrite=True,
                )
        elif binary(HERE / name) != content:
            raise ValueError("Diagnostic deterministic replay differs.")
    print(
        json.dumps(
            {
                "summaries": data["summaries"],
                "hidden_match_cells": data["paired_partial_hidden_match_cells"],
                "positive_rescues": data["paired_positive_reach_rescues"],
            }
        )
    )


if __name__ == "__main__":
    main()
