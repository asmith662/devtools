# Copyright (c) 2026
# ruff: noqa: ANN401, T201, PLR0915, C901, PLR0911, PLR0912, PLC0415 -- frozen scientific adapter dispatch
"""Wire C-v2 into existing controller packet/C/import/D ownership."""

import argparse
import asyncio
import json
from dataclasses import asdict
from pathlib import Path
from typing import Any

from experiments.codex_dogfood.case_0009.artifacts import digest, json_bytes
from experiments.orchestration.adoption import load_branch
from experiments.orchestration.isolation import PRIMARY
from experiments.orchestration.storage import load, materialize, require
from experiments.orchestration.workers import accounting, evidence
from experiments.source_grounding import analysis, reviewer, workers
from experiments.source_grounding.chunked import (
    classification,
    disclosure,
    execution,
    fresh,
    packing,
)


def run(args: Any) -> Any:
    """Dispatch only frozen operations, without invoking science during imports."""
    root, stage, case, frame = (
        args.workspace,
        args.stage,
        args.case,
        json.loads(args.frame),
    )
    if stage == "B":
        fresh.run(root, args)
        return {"status": "PASS"}
    if stage == "packet":
        design, rows = workers.prepared(root, case, frame)
        protocol = load(root / "worker_configuration.json")
        packet = workers.gold_packet(design, rows)
        host = {
            "a1_partition": protocol["c2"]["partitions"][case],
            "a1_calls": execution.A1_CALLS[case],
            "semantic": protocol["c2"]["semantic"],
            "invocation_prefix": args.run_id + "/" + case + "/C2",
        }
        files = execution.packet_files(
            packet,
            (root / "reviewer_codec.py").read_bytes(),
            host,
        )
        workers.write_files(root, files)
        workers.candidate(root, case, frame, stage, files)
        return {"status": "PASS"}
    if stage == "packet_validate":
        p = reviewer.packet(root)
        host = load(root / "c2-host.json")
        part = packing.partition(p)
        require(
            p["case"] == case and p["frame"] == frame and part == host["a1_partition"],
            "C2 packet identity",
        )
        table = evidence.sources(p)
        for batch in part["batches"]:
            execution.check(
                host["semantic"],
                classification.render(p, batch["source_keys"], table),
                classification.contract(
                    batch["source_keys"],
                    [o["id"] for o in p["obligations"]],
                ),
            )
        require(
            len(disclosure.maximum_disclosure(p).decode()) * 10 <= 1048576 * 7,
            "C2 all-positive character maximum",
        )
        return {"status": "PASS"}
    if stage == "C2":
        asyncio.run(execution.execute(root))
        return {"status": "PASS"}
    if stage == "C_validate":
        return execution.validate(root)
    if stage in {"import", "import_validate"}:
        files = {
            **{p.name: p.read_bytes() for p in (root / "packet").iterdir()},
            **{p.name: p.read_bytes() for p in (root / "primary").iterdir()},
        }
        view = root / "verification-view"
        if not view.exists():
            materialize(view, files)
        require(
            all((view / n).read_bytes() == v for n, v in files.items()),
            "C2 import exact bytes",
        )
        receipt = execution.validate(view)
        gold = load(view / "stage_c_review.json")
        projection = {
            "case": case,
            "frame": frame,
            "cells": gold["cells"],
            "statistics": load(view / "stage_c_statistics.json"),
            "primary_sha256": {n: digest(files[n]) for n in PRIMARY},
        }
        if stage == "import":
            workers.write_files(
                root,
                {
                    "gold.json": json_bytes(projection),
                    "import_authentication.json": json_bytes(receipt),
                },
            )
            owned = {"primary/" + n: files[n] for n in (*PRIMARY, *execution.EXTRA)}
            owned.update(
                {
                    n: (root / n).read_bytes()
                    for n in ("gold.json", "import_authentication.json")
                },
            )
            workers.candidate(root, case, frame, "import", owned)
        else:
            require(load(root / "gold.json") == projection, "C2 exact gold projection")
        return {**receipt, "semantic_transformation": "NONE"}
    if stage in {"D", "D_validate"}:
        # Existing scientific comparisons are called unchanged; usage is separate.
        result = analysis.analyze(root)
        files = {
            "analysis.json": json_bytes(result),
            "analysis.md": analysis.render(result).encode(),
            "TRACE.md": analysis.render(result["trace"]).encode(),
            "trace.json": json_bytes(result["trace"]),
            "validation.json": json_bytes(
                {
                    "status": "PASS",
                    "join_defects": result["join_defects"],
                    "actual_rank_modifications": 0,
                },
            ),
        }
        records = []
        cases = {}
        from experiments.source_grounding.chunked.prospective import ADDRESS

        protocol = load(execution.ROOT / ADDRESS / "protocol.json")
        for identity in execution.A1_CALLS:
            gold_usage = load(root / "C" / identity / "primary/c2-usage.json")
            if identity in protocol["adopted_branches"]:
                binding = protocol["adopted_branches"][identity]
                treatment = accounting.adopted(
                    load_branch(execution.ROOT, binding).value["original_usage"],
                    binding["sha256"],
                )
            else:
                treatment = load(root / "B" / identity / "costs.json")[
                    "invocation_measurement"
                ]
            own = [treatment, *gold_usage["invocations"]]
            records.extend(own)
            cases[identity] = {
                "C2": gold_usage,
                "treatment": treatment,
                "totals": asdict(accounting.aggregate(tuple(own))),
            }
        files["semantic-usage.json"] = json_bytes(
            {"cases": cases, "cohort": asdict(accounting.aggregate(tuple(records)))},
        )
        files["integrity.json"] = json_bytes(
            {
                "sha256": {n: digest(v) for n, v in files.items()},
                "inputs": [c["input_hashes"] for c in result["cases"]],
            },
        )
        if stage == "D":
            workers.write_files(root, files)
            workers.candidate(root, case, frame, "D", files)
        else:
            require(
                all((root / n).read_bytes() == v for n, v in files.items()),
                "D exact comparison/usage replay",
            )
        return {"status": "PASS"}
    return workers.run_stage(args)


def main() -> None:
    """Execute only the operation supplied by a frozen approved controller."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("stage")
    parser.add_argument("--workspace", type=Path, required=True)
    parser.add_argument("--case", required=True)
    parser.add_argument("--frame", required=True)
    parser.add_argument("--run-id", required=True)
    parser.add_argument("--stage-a", required=True)
    parser.add_argument("--packet-commit", default="")
    print(json.dumps(run(parser.parse_args())))


if __name__ == "__main__":
    main()
