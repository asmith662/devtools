# Copyright (c) 2026
# ruff: noqa: ANN401, T201, PLR0915, PLC0415, C901, PLR0911, PLR0912, FBT001 -- bounded frozen adapter dispatch
"""Single-call gold lifecycle; old global-gold execution is never a fallback."""

import argparse
import asyncio
import json
from dataclasses import asdict
from pathlib import Path
from typing import Any

from experiments.codex_dogfood.case_0009.artifacts import digest, json_bytes
from experiments.orchestration import usage_budget
from experiments.orchestration.adoption import load_branch
from experiments.orchestration.isolation import PRIMARY
from experiments.orchestration.storage import load, materialize, require
from experiments.orchestration.workers import accounting
from experiments.source_grounding import workers
from experiments.source_grounding.chunked import fresh
from experiments.source_grounding.discrimination import analysis, execution


def run(args: Any) -> Any:
    """Route only the explicitly frozen deterministic/scientific operation."""
    root, stage, case, frame = (
        args.workspace,
        args.stage,
        args.case,
        json.loads(args.frame),
    )
    if stage == "prepare":
        workers.prepared(root, case, frame)
        files = {p.name: p.read_bytes() for p in root.iterdir() if p.is_file()}
        workers.candidate(root, case, frame, stage, files)
        return {"status": "PASS"}
    if stage in {"prepare_validate", "B_validate"}:
        return workers.run_stage(args)
    if stage == "B":

        def before(raw: bytes) -> None:
            usage_budget.verify(execution.ROOT, args.run_id, case, "B")
            # Invocation identity is run-dependent; only that fixed-width value
            # differs from the prospectively bound disclosure template.
            template = raw.replace(
                (args.run_id + "/0024/B/Sol").encode(),
                ("0" * 64 + "/0024/B/Sol").encode(),
            )
            require(
                digest(template)
                == load(root / "worker_configuration.json")["candidate_discrimination"][
                    "treatment_template_sha256"
                ],
                "Unchanged treatment disclosure template",
            )

        def after(accepted: bool, failure: str | None) -> None:
            usage_budget.capture(
                execution.ROOT,
                args.run_id,
                case,
                "B",
                root / "grounding-operation/worker/invocation-measurement.json",
                accepted=accepted,
                failure_class=failure,
            )

        fresh.run(root, args, before=before, after=after)
        return {"status": "PASS"}
    if stage == "packet":
        selection = load(root / "selection.json")
        require(selection["case"] == case, "Selected case identity")
        files = execution.packet_files(selection, frame, args.run_id)
        workers.write_files(root, files)
        workers.candidate(root, case, frame, stage, files)
        return {"status": "PASS"}
    if stage == "packet_validate":
        host = load(root / "candidate-host.json")
        require(
            host["selection"]["case"] == case
            and host["frame"] == frame
            and host["run_id"] == args.run_id,
            "Gold packet identity/frame",
        )
        execution.check(root)
        from experiments.orchestration.workers import codex

        version = asyncio.run(
            workers.command(
                [
                    codex.executable(execution.configuration()),
                    "--no-daemon",
                    "--version",
                ],
                root,
                root.parent / (case + "-candidate-cli-preflight"),
            ),
        )
        require(
            version.stdout.decode().strip() == "codex-cli 0.162.1",
            "Certified CLI version required before semantic entry",
        )
        return {"status": "PASS"}
    if stage == "C":
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
            all((view / n).read_bytes() == raw for n, raw in files.items()),
            "Immutable primary import",
        )
        receipt = execution.validate(view)
        gold = load(view / "stage_c_review.json")
        projection = {
            "case": case,
            "frame": frame,
            "judgments": gold["judgments"],
            "primary_sha256": {
                n: digest(files[n]) for n in (*PRIMARY, *execution.EXTRA)
            },
        }
        if stage == "import":
            products = {
                "gold.json": json_bytes(projection),
                "import_authentication.json": json_bytes(receipt),
            }
            workers.write_files(root, products)
            workers.candidate(
                root,
                case,
                frame,
                stage,
                {
                    **products,
                    **{"primary/" + n: files[n] for n in (*PRIMARY, *execution.EXTRA)},
                },
            )
        else:
            require(
                load(root / "gold.json") == projection,
                "Exact candidate gold projection",
            )
        return {**receipt, "semantic_transformation": "NONE"}
    require(
        stage in {"D", "D_validate"},
        "Unknown candidate-discrimination stage; no legacy fallback",
    )
    from experiments.source_grounding.discrimination.prospective import ADDRESS

    protocol = load(execution.ROOT / ADDRESS / "protocol.json")
    cases = {}
    usages = {}
    for identity in protocol["candidate_discrimination"]["cases"]:
        b = root / "B" / identity
        c = root / "C" / identity
        selected = load(execution.ROOT / ADDRESS / (identity + "-selection.json"))
        universe = load(execution.ROOT / ADDRESS / (identity + "-universe.json"))
        cases[identity] = (
            universe,
            selected,
            load(b / "grounding/review.json"),
            load(c / "gold.json"),
        )
        gold_usage = load(c / "primary/candidate-usage.json")
        if identity in protocol["adopted_branches"]:
            binding = protocol["adopted_branches"][identity]
            treatment_usage = accounting.adopted(
                load_branch(execution.ROOT, binding).value["original_usage"],
                binding["sha256"],
            )
        else:
            treatment_usage = load(b / "costs.json")["invocation_measurement"]
        usages[identity] = {
            "gold": gold_usage,
            "treatment": treatment_usage,
            "fresh": asdict(
                accounting.aggregate(
                    tuple(
                        v
                        for v in (gold_usage, treatment_usage)
                        if v["measurement"]["execution_origin"] == "EXECUTED"
                    ),
                ),
            ),
            "original_attributed": asdict(
                accounting.aggregate((gold_usage, treatment_usage)),
            ),
        }
    result = analysis.analyze(cases)
    products = {
        "analysis.json": json_bytes(result),
        "analysis.md": (
            "# Candidate-surface discrimination\n\n"
            + json.dumps(result, indent=2)
            + "\n"
        ).encode(),
        "validation.json": json_bytes(
            {"status": "PASS", "claim_boundary": analysis.CLAIM},
        ),
        "integrity.json": json_bytes(
            {
                "inputs": {
                    c: {"universe": u[0]["sha256"], "selection": u[1]["sha256"]}
                    for c, u in cases.items()
                },
            },
        ),
    }
    records = tuple(v[k] for v in usages.values() for k in ("gold", "treatment"))
    products["semantic-usage.json"] = json_bytes(
        {
            "cases": usages,
            "fresh_cohort": asdict(
                accounting.aggregate(
                    tuple(
                        v
                        for v in records
                        if v["measurement"]["execution_origin"] == "EXECUTED"
                    ),
                ),
            ),
            "original_attributed_cohort": asdict(accounting.aggregate(records)),
            "adopted_current_consumption": 0,
            "cost_or_subscription_units": "NOT_INFERRED",
        },
    )
    if stage == "D":
        workers.write_files(root, products)
        workers.candidate(root, case, frame, stage, products)
    else:
        require(
            all((root / n).read_bytes() == v for n, v in products.items()),
            "Exact design-aware Stage D replay",
        )
    return {"status": "PASS"}


def main() -> None:
    """Only an approved controller may request a scientific operation."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("stage")
    parser.add_argument("--workspace", type=Path, required=True)
    parser.add_argument("--case", required=True)
    parser.add_argument("--frame", required=True)
    parser.add_argument("--run-id", required=True)
    parser.add_argument("--stage-a", required=True)
    parser.add_argument("--packet-commit", default="")
    print(json.dumps(run(parser.parse_args())))
