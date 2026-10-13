# Copyright (c) 2026
# ruff: noqa: ANN401, E501 -- deterministic experiment artifact boundary
"""Authenticate committed captures/gold and exclusively publish deterministic Stage D."""

from __future__ import annotations

import argparse
import asyncio
import gzip
import json
from pathlib import Path
from statistics import median
from typing import Any

from experiments.codex_dogfood.case_0009.artifacts import (
    ROOT,
    binary,
    digest,
    git,
    json_bytes,
    put_binary,
)
from experiments.structural_discrimination.stage_b import authentication
from experiments.structural_discrimination.stage_b.capture import (
    CASES,
    STAGE_A,
    capture_root,
    case_root,
)
from experiments.structural_discrimination.stage_c import import_gold
from experiments.structural_discrimination.stage_c.import_gold import require
from experiments.structural_discrimination.stage_d import join, reporting

STAGE_C = "2a93f91d96ebd8deb927550822e4e2c40f2bd1db"
PACKAGE = Path(__file__).resolve().parent
OUTPUT = PACKAGE / "results"
PROTOCOL_SHA = "6167a9b28da52ce42ac7c9186fade322a078a3f5158ba87067b1c3cf4df0b52f"
STAGE_A_SEAL = "12be78dcf5f16838943cb07fe230af9174a5a3280ee0c5953db60c9b9d642041"


async def stage_a() -> Any:
    """Authenticate frozen byte scopes; no reconstruction or historical access."""
    prefix = "experiments/structural_discrimination/"
    seal = await git("show", STAGE_A + ":" + prefix + "integrity.json")
    require(
        digest(seal) == STAGE_A_SEAL
        and seal == binary(PACKAGE.parent / "integrity.json"),
        "Stage A integrity hash",
    )
    protocol = await git("show", STAGE_A + ":" + prefix + "protocol.json")
    require(
        digest(protocol) == PROTOCOL_SHA
        and protocol == binary(PACKAGE.parent / "protocol.json"),
        "Stage A protocol hash",
    )
    scopes = json.loads(seal)
    for path, sha in {**scopes["artifacts"], **scopes["implementation"]}.items():
        require(
            digest(binary(ROOT / path)) == sha,
            "Stage A artifact/source changed: " + path,
        )
    return {
        "checkpoint": STAGE_A,
        "protocol_sha256": PROTOCOL_SHA,
        "integrity_sha256": STAGE_A_SEAL,
        "status": "PASS",
    }


def indispensability(case: str, stats: Any, gold: Any) -> Any:
    """Translate primary resource IDs into exact packet addresses, preserving scope."""
    cells = [c for c in gold["cells"] if c["obligation"] == "O1"]

    def addresses(ids: Any) -> list[str]:
        return [
            cells[(i if isinstance(i, int) else int(i.removeprefix("R"))) - 1][
                "address"
            ]
            for i in ids
        ]

    task_ids = stats.get(
        "task_indispensable_resource_ids",
        stats.get("task_indispensable_resources"),
    )
    task = addresses(task_ids)
    result = {}
    for o in ("O1", "O2", "O3"):
        if case == "0017":
            obligation = stats["obligation_intersections"][o]["resource_ids"]
        elif case == "0018":
            obligation = stats["obligation_indispensable_resources"][o]
        else:
            obligation = stats["by_obligation"][o]["obligation_indispensable_resources"]
        result[o] = {"TASK": task, "OBLIGATION": addresses(obligation)}
    return result


def gold_summary(case: str, review: Any, stats: Any, gold: Any) -> Any:
    """Retain primary summaries and gap semantics without harmonizing judgments."""
    exclude = {
        "complete_task_combinations",
        "distinct_sufficient_resource_unions",
        "inclusion_minimal_sufficient_resource_unions",
        "sufficient_semantic_unit_unions",
    }
    return {
        "resources": gold["frame"]["resource_count"],
        "obligations": len(gold["obligations"]),
        "cells": len(gold["cells"]),
        "label_counts": gold["counts"],
        "required_resource_union": sorted(
            {c["address"] for c in gold["cells"] if c["label"] == "REQUIRED"},
        ),
        "sufficient_union_counts": {
            k: len(stats[k])
            for k in (
                "distinct_sufficient_resource_unions",
                "inclusion_minimal_sufficient_resource_unions",
            )
            if k in stats
        },
        "statistics": {k: v for k, v in stats.items() if k not in exclude},
        "semantic_units": [
            {
                "id": u["id"],
                "classification": u.get("evidence_class", u.get("classification")),
                "primary_pointer": f"/semantic_units/{i}",
            }
            for i, u in enumerate(review["semantic_units"])
        ],
        "gaps": review["gaps"],
        "limitations": review["limitations"],
        "indispensability": indispensability(case, stats, gold),
        "sufficiency_scope": "CONDITIONAL_REPOSITORY_INTEGRATION; unconditional future task has zero complete witnesses/combinations, empty unions, undefined range and indispensability"
        if case == "0019"
        else "FROZEN O1-O3 INTERPRETATION",
    }


def source_hashes() -> Any:
    """Bind explicit analyzer sources; never include unrelated historical fixtures."""
    paths = [
        *PACKAGE.glob("*.py"),
        PACKAGE / "README.md",
        PACKAGE / ".gitattributes",
        PACKAGE.parent / "stage_c/import_gold.py",
        PACKAGE.parent / "decision.py",
    ]
    return {p.relative_to(ROOT).as_posix(): digest(binary(p)) for p in sorted(paths)}


async def calculate() -> tuple[Any, Any]:
    """Consume only committed sealed captures and sole-primary gold."""
    inputs = {
        "stage_a": await stage_a(),
        "stage_b_checkpoint": import_gold.STAGE_B,
        "stage_c_checkpoint": STAGE_C,
        "cases": {},
    }
    results = []
    summaries = {}
    for case in CASES:
        sealed = await authentication.verify(case, import_gold.STAGE_B)
        primary = await import_gold.authenticate(case, STAGE_C)
        design = json.loads(binary(case_root(case) / "protocol.json"))
        trace = json.loads(
            gzip.decompress(binary(capture_root(case) / "trace.json.gz")),
        )
        review = json.loads(
            (import_gold.primary_root(case) / "stage_c_review.json").read_bytes(),
        )
        stats = json.loads(
            (import_gold.primary_root(case) / "stage_c_statistics.json").read_bytes(),
        )
        result = join.analyze_case(
            case,
            design,
            trace,
            primary["gold"],
            indispensability(case, stats, primary["gold"]),
        )
        summaries[case] = gold_summary(case, review, stats, primary["gold"])
        inputs["cases"][case] = {
            "stage_b": sealed,
            "stage_c": {k: v for k, v in primary.items() if k != "gold"},
        }
        results.append(result)
    aggregate = join.cohort(results)
    times = [
        {
            "case": c["case"],
            "obligation": q["obligation"],
            "complete_online_equivalent_ms": q["captured_timings_ns"][
                "complete_online_equivalent_ns"
            ]
            / 1e6,
            "components_ns": q["captured_timings_ns"],
        }
        for c in results
        for q in c["queries"]
    ]
    expected = [
        107.0191,
        106.7109,
        112.2989,
        123.2886,
        143.1456,
        122.9407,
        44.7253,
        51.2306,
        49.7056,
    ]
    require(
        [t["complete_online_equivalent_ms"] for t in times] == expected,
        "Captured performance samples",
    )
    values = sorted(t["complete_online_equivalent_ms"] for t in times)
    require(len(values) == 9, "Timing sample completeness")  # noqa: PLR2004
    performance = {
        "samples": times,
        "n": len(values),
        "median_ms": median(values),
        "nearest_rank_p95_max_nine_ms": values[-1],
        "median_le_250_ms": "PASS" if median(values) <= 250 else "FAIL",  # noqa: PLR2004 -- frozen Stage A performance descriptor
        "p95_gt_1s_concern": "YES" if values[-1] > 1000 else "NO",  # noqa: PLR2004 -- frozen Stage A performance descriptor
        "interpretation": "Nine single-run captured workload samples; no timing rerun or stable distribution claim",
    }
    invariants = {
        "actual_rank_modifications": 0,
        "PPR_executions": 0,
        "RRF_executions": 0,
        "graph_only_admissions": 0,
        "self_reference_contribution": 0,
        "A_ablation_identity": "PASS",
        "Stage_D_retrieval_executions": 0,
        "Stage_D_RI_derivations": 0,
        "semantic_model_calls": 0,
        "second_reviewers": 0,
        "reconciliations": 0,
        "historical_child_access": "NO",
        "confirmation_reserve": "NOT_ACCESSED",
    }
    return {
        "schema": "direct-structural-discrimination-stage-d-v1",
        "status": "COMPLETE",
        "cases": results,
        "cohort": aggregate,
        "gold_summaries": summaries,
        "performance": performance,
        "mechanical_invariants": invariants,
        "non_gating_interpretation": reporting.INTERPRETATION,
        "limitations": reporting.LIMITATIONS,
    }, inputs


def artifacts(analysis: Any, inputs: Any) -> dict[Path, bytes]:
    """Deterministic inspectable JSON/Markdown with acyclic source/input seals."""
    files = {}
    for case in analysis["cases"]:
        root = case_root(case["case"]) / "stage_d"
        files[root / "analysis.json"] = json_bytes(case)
        files[root / "analysis.md"] = reporting.case_markdown(case).encode()
        files[root / "trace.json"] = json_bytes(
            [t for q in case["queries"] for t in q["targets"]],
        )
        files[root / "TRACE.md"] = reporting.trace_markdown(case).encode()
        files[root / "validation.json"] = json_bytes(case["join_validation"])
    files[OUTPUT / "analysis.json"] = json_bytes(analysis)
    files[OUTPUT / "STAGE_D_REVIEW.md"] = reporting.cohort_markdown(analysis).encode()
    files[OUTPUT / "import_authentication.json"] = json_bytes(inputs)
    files[OUTPUT / "validation.json"] = json_bytes(
        {
            "status": "PASS",
            "join_defects": 0,
            "cases": {c["case"]: c["join_validation"] for c in analysis["cases"]},
            "deterministic_verification": "Reconstruction compares all artifact bytes; run separate-process verify after publication",
            "adversarial_tests": "stage_d/test_analysis.py and stage_c/test_import.py; test receipts are separate",
            "source_implementation_sha256": source_hashes(),
        },
    )
    for root in [*(case_root(c) / "stage_d" for c in CASES), OUTPUT]:
        scope = {
            p.relative_to(ROOT).as_posix(): digest(raw)
            for p, raw in files.items()
            if p.parent == root
        }
        files[root / "integrity.json"] = json_bytes(
            {
                "schema": "stage-d-integrity-v1",
                "sha256": scope,
                "inputs_sha256": digest(json_bytes(inputs)),
                "source_implementation_sha256": source_hashes(),
                "stage_c_checkpoint": STAGE_C,
                "self_hash": "EXCLUDED; external Git checkpoint anchors this manifest",
            },
        )
    return files


def publish(files: dict[Path, bytes]) -> None:
    """Preflight the complete output scope; refuse every existing artifact."""
    require(not any(p.exists() for p in files), "Stage D overwrite refused")
    for path, raw in files.items():
        put_binary(path, raw)


def verify_bytes(files: dict[Path, bytes]) -> None:
    """Reject any derived count/category, artifact or integrity byte modification."""
    for path, raw in files.items():
        require(
            path.read_bytes() == raw,
            "Stage D exact output/integrity differs: " + str(path),
        )
    for directory in {p.parent for p in files}:
        require(
            {p for p in directory.iterdir() if p.is_file()}
            == {p for p in files if p.parent == directory},
            "Stage D unexpected output member",
        )


async def run(mode: str, checkpoint: str | None = None) -> Any:
    """Separate BUILD/VERIFY modes; verification never overwrites scientific bytes."""
    if mode == "build":
        require(
            not OUTPUT.exists()
            and all(not (case_root(c) / "stage_d").exists() for c in CASES),
            "Stage D overwrite refused",
        )
    analysis, inputs = await calculate()
    files = artifacts(analysis, inputs)
    if mode == "build":
        require(
            files == artifacts(analysis, inputs),
            "Repeat deterministic output differs",
        )
        publish(files)
    verify_bytes(files)
    if checkpoint:
        for path, raw in files.items():
            require(
                raw
                == await git(
                    "show",
                    checkpoint + ":" + path.relative_to(ROOT).as_posix(),
                ),
                "Stage D committed output differs",
            )
    return {
        "status": "PASS",
        "mode": mode,
        "exact_output": True,
        "case_categories": analysis["cohort"]["case_categories"],
        "totals": analysis["cohort"]["totals"],
        "join_defects": 0,
    }


def main() -> None:
    """Invoke deterministic capture consumption, never an acquisition entry point."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("mode", choices=("build", "verify"))
    parser.add_argument("--checkpoint")
    args = parser.parse_args()
    print(json.dumps(asyncio.run(run(args.mode, args.checkpoint)), indent=2))  # noqa: T201


if __name__ == "__main__":
    main()
