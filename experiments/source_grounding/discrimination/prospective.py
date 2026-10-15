# Copyright (c) 2026
# ruff: noqa: ANN401, T201, PLR0915, E501, PLR2004 -- deterministic prospective artifacts only
"""Freeze a four-call candidate-surface design; never approve or invoke models."""

import argparse
import asyncio
import copy
import gzip
import json
from dataclasses import asdict
from pathlib import Path
from typing import Any

from devtools.observability.usage.forecast import forecast
from devtools.observability.usage.ingestion import measurement
from experiments.codex_dogfood.case_0009.artifacts import (
    ROOT,
    digest,
    git,
    json_bytes,
    put_binary,
)
from experiments.orchestration.adoption import load_branch
from experiments.orchestration.controller import implementation
from experiments.orchestration.model import RunPlan
from experiments.orchestration.storage import load, require
from experiments.orchestration.workers import runtime, semantic
from experiments.source_grounding import contracts, freeze
from experiments.source_grounding import plan as maintained
from experiments.source_grounding.chunked import execution as compatible
from experiments.source_grounding.chunked import fresh
from experiments.source_grounding.chunked import prospective as prior
from experiments.source_grounding.discrimination import (
    analysis,
    execution,
    gold,
    sampling,
    universe,
)

ADDRESS = "experiments/source_grounding/stage_a/candidate-05"
PLAN = "experiments/source_grounding/plans/candidate-discrimination-run-plan.json"
OLD_PLAN = "7e2f4b1258bd6b432f4c5608be2ba34a06145fba4bee209985f45697bc561d53"
RETIREMENT = "experiments/orchestration/supersessions/" + OLD_PLAN + ".json"
CASES = ("0022", "0023", "0024")


def calibrations() -> tuple[Any, ...]:
    """Read published measurement metadata only, never semantic verdicts."""
    captures = [
        load(
            ROOT
            / f"experiments/orchestration/engineering/host_disclosure/{n}-receipt.json",
        )["measurement"]
        for n in ("minimal", "capacity", "output")
    ]
    captures.extend(
        load(
            ROOT
            / f"experiments/orchestration/engineering/adopted_branches/{prior.OLD_RUN}/{c}/seal.json",
        )["original_usage"]
        for c in ("0022", "0023")
    )
    return tuple(measurement(c) for c in captures)


def economics(calls: Any, baseline: Any) -> Any:
    """Publish only calibration-based estimates and a private snapshot digest."""
    measured = calibrations()
    values = []
    for identity, c in calls.items():
        values.append(
            asdict(
                forecast(
                    invocation=identity,
                    model=c["model"],
                    reasoning_effort="High",
                    execution_profile="SEMANTIC_WORKER",
                    disclosed_characters=c["characters"],
                    disclosed_bytes=c["bytes"],
                    disclosure_digest=c["sha256"],
                    response_maximum_bytes=c["response_maximum_bytes"],
                    calibrations=measured,
                ),
            ),
        )
    return {
        "schema": "semantic-economics-forecast-v1",
        "fresh_calls": 4,
        "maximum_fresh_calls": 4,
        "Astra": 3,
        "Sol": 1,
        "adopted_dependencies": 2,
        "adopted_new_consumption": 0,
        "calls": values,
        "input_range": [
            sum(v["input_tokens"][side] for v in values) for side in ("lower", "upper")
        ],
        "output_range": [
            sum(v["output_tokens"][side] for v in values) for side in ("lower", "upper")
        ],
        "confidence": "LOW; EMPIRICAL_ENVELOPES_NOT_CONFIDENCE_OR_TOKENIZER_BOUNDS",
        "weekly_numeric_limit": "UNSET",
        "private_observed_baseline": baseline,
        "observed_window_contribution": {
            "provenance": "DERIVED_PRIVATE_OBSERVED_SNAPSHOT",
            "local_report": ".local/usage/candidate-discrimination-economics.json",
            "input_share_formula": "100 * input_range / baseline.reported_input_subtotal",
            "fresh_call_share_formula": "100 * 4 / baseline.observed_fresh_invocations",
            "coverage": "PARTIAL_OBSERVED_USAGE_NOT_SUBSCRIPTION_QUOTA",
        },
        "budget_authorization": "EXACT_PLAN_APPROVAL_AND_PRELAUNCH_OBSERVED_BUDGET_CHECK_REQUIRED",
        "subscription_or_API_cost": "NOT_INFERRED",
    }


async def stage_a(engineering: str, baseline: Any) -> dict[str, bytes]:
    """Replay parent-only native candidates and freeze blind census/sample inputs."""
    require(
        (
            await git(
                "merge-base",
                "42b2590b8582e393b0761207775d0fd240840560",
                engineering,
            )
        )
        .decode()
        .strip()
        == "42b2590b8582e393b0761207775d0fd240840560",
        "Published engineering ancestry",
    )
    old = load(ROOT / prior.ADDRESS / "protocol.json")
    old_plan = load(ROOT / prior.PLAN)
    require(
        digest((ROOT / prior.PLAN).read_bytes())
        == "333b47321ba34a29183fcea29956e74b223f9526fa211d4ae71ba13ba3eb9389"
        and RunPlan.parse(old_plan).identity(old_plan["controller_implementation"])
        == OLD_PLAN,
        "Historical unapproved plan identity changed",
    )
    retired = ROOT / old_plan["publication"]["root"] / OLD_PLAN
    require(
        not (retired / "authorization").exists()
        and not list(retired.glob("journal/*/[BC]/ENTERED.json")),
        "Old 84-call plan must remain unapproved/unexecuted",
    )
    p = copy.deepcopy(old)
    p.pop("c2")
    p["schema"] = "purpose-relative-source-grounding-candidate-stage-a-v1"
    p["gold_labels"] = list(gold.LABELS)
    p["gold_judgments"] = ["source_usefulness", "target_usefulness", "pursuit_value"]
    p["gold_instructions_sha256"] = digest(gold.INSTRUCTION.encode())
    p["design"] = "discrimination/METHOD.md"
    p["design_sha256"] = digest((Path(__file__).parent / "METHOD.md").read_bytes())
    p["no_execution"] = {
        "fresh_model_calls": 0,
        "scientific_entered": 0,
        "new_gold": 0,
        "stage_d": 0,
        "approval": 0,
    }
    p["mechanical_native_candidate_replay"] = (
        "PERFORMED_WITHOUT_GROUNDING_OR_SCIENTIFIC_ENTRY"
    )
    p["worker_timeout"] = 21600
    p["scientific_method"] = ADDRESS + "/METHOD.md"
    p["design_scope"] = analysis.CLAIM
    p["supersession"] = {
        "prior_stage_a": "b1c0a573ec7dd64396bae49c2ef9f578c5a65433",
        "prior_plan": "42b2590b8582e393b0761207775d0fd240840560",
        "prior_run_id": OLD_PLAN,
        "reason": "84-call governed method economically unacceptable for narrower discrimination question; remains unapproved/unexecuted historical prospective work",
        "engineering_checkpoint": engineering,
        "historical_failed_run": prior.OLD_RUN,
        "B_semantics": "UNCHANGED",
        "child_access": False,
        "confirmation_reserve_access": False,
        "B_semantic_results_inspected": False,
    }
    p["workers"]["grounding"] = fresh.configuration()
    p["candidate_discrimination"] = {
        "cases": {},
        "seed": sampling.SEED,
        "planning_margin": sampling.MARGIN,
        "decision_protocol": analysis.DECISION,
        "claim_boundary": analysis.CLAIM,
        "fresh_calls": 4,
        "Astra": 3,
        "Sol": 1,
        "input_chars": 700000,
        "input_bytes": 700000,
        "output_method_bytes": 65536,
        "attained_output_bytes": 63357,
        "automatic_scientific_retry": 0,
        "usage": "FIVE_SEPARATE_CATEGORIES_OR_UNKNOWN; MANDATORY_BEFORE_PUBLICATION",
    }
    files = {}
    call_sizes = {}
    cohort = load(ROOT / prior.ADDRESS / "cohort.json")
    cards = await freeze.cards()
    for case, card in zip(CASES, cards, strict=True):
        base = ROOT / f"experiments/codex_dogfood/case_{case}"
        for name in (
            "protocol.json",
            "frame.json",
            "resources.json.gz",
            "task.txt",
            "README.md",
            ".gitattributes",
        ):
            require(
                (base / name).read_bytes()
                == await git(
                    "show",
                    prior.BASE + ":" + (base / name).relative_to(ROOT).as_posix(),
                ),
                "Original prospective authoring changed",
            )
        design = load(base / "protocol.json")
        rows = json.loads(gzip.decompress((base / "resources.json.gz").read_bytes()))
        require(
            design["population"] == card
            and design["frame"]
            == freeze.frame_contract(card, load(base / "frame.json"), rows),
            "Exact public parent frame",
        )
        broad = universe.mechanical(design, rows)
        population = universe.build(design, rows, broad)
        selected = sampling.design_sample(design, rows, population)
        compatible.check(
            execution.configuration(),
            gold.render(selected["packet"]),
            selected["response_schema"],
        )
        for suffix, value in (("universe", population), ("selection", selected)):
            files[f"{ADDRESS}/{case}-{suffix}.json"] = json_bytes(value)
        p["candidate_discrimination"]["cases"][case] = {
            "universe_sha256": population["sha256"],
            "selection_sha256": selected["sha256"],
            "population": len(population["units"]),
            "sample": len(selected["selected"]),
            "allocation": selected["allocation"],
            "input": selected["input"],
            "output_maximum": selected["output_maximum"],
        }
        call_sizes[case + "/C"] = {
            "model": "gpt-6-astra",
            "characters": selected["input"]["characters"],
            "bytes": selected["input"]["utf8_bytes"],
            "sha256": selected["input"]["sha256"],
            "response_maximum_bytes": selected["output_maximum"]["utf8_bytes"],
        }
        if case == "0024":
            payload = contracts.grounding_packet(design, rows, broad)
            raw = semantic.render_disclosure(
                fresh.configuration(),
                json_bytes(payload),
                (
                    ROOT / "experiments/source_grounding/INSTRUCTIONS_GROUNDING.md"
                ).read_bytes(),
                "0" * 64 + "/0024/B/Sol",
            )
            require(
                len(raw) <= 700000 and len(raw.decode()) <= 700000,
                "Fresh B exact input capacity",
            )
            files[f"{ADDRESS}/0024-treatment-template.bin"] = raw
            p["candidate_discrimination"]["treatment_template_sha256"] = digest(raw)
            call_sizes[case + "/B"] = {
                "model": "gpt-6-sol",
                "characters": len(raw.decode()),
                "bytes": len(raw),
                "sha256": digest(raw),
                "response_maximum_bytes": 63357,
            }
    prior.prove_capture_revision(
        await git(
            "show",
            prior.OLD_STAGE_A + ":experiments/source_grounding/capture.py",
        ),
    )
    for case, binding in p["adopted_branches"].items():
        branch = load_branch(ROOT, binding)
        require(
            binding["sha256"] == prior.SEALS[case]
            and branch.value["compatibility"]["scientific_contract"]
            == load(ROOT / binding["prospective_compatibility"]["path"])[
                "original_contract"
            ],
            "Adopted unchanged B compatibility",
        )
    for path, h in p["preserved_evidence"].items():
        require(digest((ROOT / path).read_bytes()) == h, "Historical journal mutation")
    econ = economics(call_sizes, baseline)
    p["economics"] = econ
    p["usage_budget"] = {
        "fresh_call_limit": 4,
        "model_call_limits": {"gpt-6-astra": 3, "gpt-6-sol": 1},
        "calls": {
            v["invocation"]: {
                "model": v["model"],
                "input_upper": v["input_tokens"]["upper"],
                "output_upper": v["output_tokens"]["upper"],
            }
            for v in econ["calls"]
        },
        "authorization": "EXACT_PLAN_EXECUTION_APPROVAL",
    }
    p["workers"]["gold"] = {
        **execution.configuration(),
        "kind": "process",
        "prompt_file": "INSTRUCTIONS.md",
        "environment_allowlist": list(runtime.ENVIRONMENT),
        "argv": [
            "{python}",
            "-B",
            "{repository}/experiments/source_grounding/discrimination/entry.py",
            "C",
            "--workspace",
            "{workspace}",
            "--case",
            "{case}",
            "--frame",
            "{frame}",
            "--run-id",
            "PACKET_BOUND",
            "--stage-a",
            engineering,
        ],
        "additional_artifacts": list(execution.EXTRA),
        "authorized_surface": execution.AUTHORIZED,
        "fresh_primary_thread": True,
    }
    p["semantic_execution"] = copy.deepcopy(p["workers"]["gold"])
    semantic_argv = p["semantic_execution"]["argv"]
    semantic_argv[semantic_argv.index("--stage-a") + 1] = "{stage_a_checkpoint}"
    files[ADDRESS + "/METHOD.md"] = (Path(__file__).parent / "METHOD.md").read_bytes()
    files[ADDRESS + "/cohort.json"] = json_bytes(cohort)
    files[ADDRESS + "/economics.json"] = json_bytes(econ)
    files[ADDRESS + "/protocol.json"] = json_bytes(p)
    files[RETIREMENT] = json_bytes(
        {
            "schema": "experiment-prospective-supersession-v1",
            "run_id": OLD_PLAN,
            "replacement_stage_a": ADDRESS,
            "status": "SUPERSEDED_UNAPPROVED_NEVER_EXECUTED",
            "reason": p["supersession"]["reason"],
        },
    )
    pinned = freeze.implementations()
    for address, h in load(ROOT / prior.ADDRESS / "integrity.json")[
        "implementation"
    ].items():
        if "/engineering/host_disclosure/" in address:
            require(
                digest((ROOT / address).read_bytes()) == h,
                "Capacity evidence changed",
            )
            pinned[address] = h
    files[ADDRESS + "/integrity.json"] = json_bytes(
        {
            "schema": "source-grounding-stage-a-integrity-v1",
            "artifacts": {n: digest(v) for n, v in files.items()},
            "implementation": pinned,
        },
    )
    return files


async def run_plan(checkpoint: str) -> Any:
    """Construct a new run identity with exactly four fresh semantic operations."""
    value = load(ROOT / prior.PLAN)
    p = load(ROOT / ADDRESS / "protocol.json")
    integrity = load(ROOT / ADDRESS / "integrity.json")
    value.update(
        name="purpose-relative-source-grounding-candidate-discrimination-05",
        attempt=5,
        stage_a={
            "checkpoint": checkpoint,
            "protocol": {
                "path": ADDRESS + "/protocol.json",
                "sha256": digest(json_bytes(p)),
            },
            "integrity": {
                "path": ADDRESS + "/integrity.json",
                "sha256": digest(json_bytes(integrity)),
            },
        },
        semantic=copy.deepcopy(p["semantic_execution"]),
        adopted_branches=p["adopted_branches"],
        implementation=integrity["implementation"],
        controller_implementation=implementation(),
        economics=p["economics"],
        usage_budget=p["usage_budget"],
    )
    for case in value["cases"]:
        for item in case["inputs"]:
            if item["name"] in {"implementation.json", "worker_configuration.json"}:
                item["path"] = ADDRESS + (
                    "/integrity.json"
                    if item["name"] == "implementation.json"
                    else "/protocol.json"
                )
                item["sha256"] = digest((ROOT / item["path"]).read_bytes())
        for suffix in ("selection", "universe"):
            path = ADDRESS + "/" + case["id"] + "-" + suffix + ".json"
            case["inputs"].append(
                {
                    "name": suffix + ".json",
                    "path": path,
                    "sha256": digest((ROOT / path).read_bytes()),
                },
            )
    for command in value["commands"].values():
        command[2] = "{repository}/experiments/source_grounding/discrimination/entry.py"
        command[command.index("--stage-a") + 1] = checkpoint
    value["semantic"]["argv"][value["semantic"]["argv"].index("--stage-a") + 1] = (
        checkpoint
    )
    checks = maintained.validation_commands(integrity["implementation"])
    checks[0].append("experiments/source_grounding/discrimination")
    value["validation"] = {
        "local": checks,
        "checkpoint": checks,
        # The controller supplies its mandatory protected/static floor once.
        "final": checks,
    }
    value["timeouts"]["worker"] = 21600
    RunPlan.parse(value)
    return value


async def main() -> None:
    """Write-once/replay artifacts; none of these modes authorize execution."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("mode", choices=("build", "verify", "plan", "verify-plan"))
    parser.add_argument("--checkpoint", required=True)
    parser.add_argument("--baseline", type=Path)
    args = parser.parse_args()
    if args.mode in {"plan", "verify-plan"}:
        files = {PLAN: json_bytes(await run_plan(args.checkpoint))}
    else:
        baseline = (
            load(args.baseline)
            if args.baseline
            else load(ROOT / ADDRESS / "protocol.json")["economics"][
                "private_observed_baseline"
            ]
        )
        if args.mode == "build":
            require(
                baseline["path"] == ".local/usage/rolling-7-days-baseline.json"
                and digest((ROOT / baseline["path"]).read_bytes())
                == baseline["sha256"],
                "Private baseline snapshot binding differs",
            )
        files = await stage_a(args.checkpoint, baseline)
    for path, raw in files.items():
        if args.mode in {"verify", "verify-plan"}:
            require(
                (ROOT / path).read_bytes() == raw,
                "Prospective replay differs: " + path,
            )
        else:
            require(not (ROOT / path).exists(), "Prospective overwrite refused")
            put_binary(ROOT / path, raw)
    print(
        json.dumps(
            {
                "status": "PASS",
                "artifacts": len(files),
                "execution_authorized": "NO",
                "scientific_ENTERED": 0,
            },
        ),
    )


if __name__ == "__main__":
    asyncio.run(main())
