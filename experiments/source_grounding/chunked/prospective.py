# Copyright (c) 2026
# ruff: noqa: ANN401, PLR0915, E501, T201, ASYNC240, PLR2004 -- exact prospective artifacts, never science
"""Freeze existing cohort plus C-v2 procedure; build/verify never runs a model."""

import argparse
import ast
import asyncio
import base64
import copy
import gzip
import json
from pathlib import Path
from typing import Any

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
from experiments.orchestration.workers import (
    capacity,
    evidence,
    output_capacity,
    schema,
)
from experiments.source_grounding import capture, freeze, workers
from experiments.source_grounding import plan as old_plan
from experiments.source_grounding.chunked import (
    classification,
    disclosure,
    execution,
    fresh,
    packing,
    response,
)

BASE = "5f329373ed26933616d776726607a976a22cb77a"
OLD_STAGE_A = "f1c0839bba3e39bc3973099164c48d46e5bf631a"
OLD_RUN = "b6cd4408b4dbc86a50c335f4a364898ff3b45c123becb7b6865c34208d3e1982"
ADDRESS = "experiments/source_grounding/stage_a/chunked-04"
PLAN = "experiments/source_grounding/plans/bounded-chunked-run-plan.json"
EXPECTED = {
    "0022": "a8fb01d36ee067471754bdb19dc12f7f5a606e591264653ce4906743b2086ecb",
    "0023": "f22c6106f9dd6fa95ae05ba35bef2626cd872575db2132e52cc9af3a2e4b0653",
    "0024": "33ae06ed219ae01a876ae4f4783f30b3275cb35e5182e950cf226ecf2c256b73",
}
SEALS = {
    "0022": "12bb1f669bd4db7c1a0bdc83f072b0959949b778bc654cdf45c800420818f0f7",
    "0023": "91fb32bfd6ab8548fb9dba30a0cb1a80e8fb7ac2de40d2f78f384e8cdf674328",
}
JOURNALS = {
    "0022/B/ENTERED.json": "6c735ca13e0f88ffb861a6f42fc2f3548f20524212ca5173062090c0df18b593",
    "0022/B/RETURNED.json": "8bd14118d9bbd59158742fae103ae957769175e97f4a24cf556efc259ba006a5",
    "0022/C/ENTERED.json": "97ab56f5073a2f33d23897de0286b94651b7c378c5564153b347bf71e88f603e",
    "0022/C/FAILED.json": "966eeaa7eeb4e19479141a1fe7e928c57c93b199ee64f7854f4828cb7c2e3ee8",
    "0023/B/ENTERED.json": "da5dbe0b32271e43941561ba542ee45163f61299f6d59949cb6e1384c510a04a",
    "0023/B/RETURNED.json": "7d74efdee478c91871e9e0fb2f2dab0c5de19b2a42c56b3092e5cc594bd032f7",
}


def prove_capture_revision(original: bytes) -> None:
    """Only optional pre-entry callback and original proof-source attribution differ."""
    old = ast.parse(original)
    new = ast.parse(Path(capture.__file__).read_bytes())
    execute = next(
        n for n in new.body if isinstance(n, ast.FunctionDef) and n.name == "execute"
    )
    index = next(
        i
        for i, a in enumerate(execute.args.kwonlyargs)
        if a.arg == "grounding_preflight"
    )
    execute.args.kwonlyargs.pop(index)
    execute.args.kw_defaults.pop(index)
    removed = [
        n
        for n in execute.body
        if isinstance(n, ast.If)
        and ast.unparse(n.test) == "grounding_preflight is not None"
    ]
    require(
        len(removed) == 1
        and ast.unparse(removed[0].body[0]) == "grounding_preflight(grounding_input)",
        "Pre-entry hook shape",
    )
    execute.body.remove(removed[0])

    class OriginalVerifier(ast.NodeTransformer):
        def visit_Call(self, node: ast.Call) -> Any:
            """Restore only the original source-attribution expression for comparison."""
            if (
                isinstance(node.func, ast.Attribute)
                and node.func.attr == "get"
                and ast.unparse(node.func.value) == "marker['implementation']"
                and len(node.args) == 2
            ):
                require(
                    isinstance(node.args[0], ast.Constant)
                    and node.args[0].value == "experiments/source_grounding/capture.py",
                    "Verifier source key",
                )
                return node.args[1]
            return self.generic_visit(node)

    new = OriginalVerifier().visit(new)
    require(
        ast.dump(old) == ast.dump(new),
        "B scientific algorithm changed beyond declared operational bindings",
    )


async def stage_a(engineering: str) -> dict[str, bytes]:
    """Reuse exact original scientific authoring and authenticate complete parent bytes."""
    require(
        (await git("merge-base", BASE, engineering)).decode().strip() == BASE,
        "Engineering ancestry",
    )
    config = execution.configuration()
    capacity.authenticate(load(ROOT / capacity.RECEIPT_ADDRESS), config)
    capacity.authenticate_files(ROOT, load(ROOT / capacity.RECEIPT_ADDRESS))
    output_capacity.authenticate(load(ROOT / output_capacity.ADDRESS), config, ROOT)
    original = await git(
        "show",
        OLD_STAGE_A + ":experiments/source_grounding/capture.py",
    )
    prove_capture_revision(original)
    protocol = load(
        ROOT / "experiments/source_grounding/stage_a/host-disclosure-03/protocol.json",
    )
    protocol = copy.deepcopy(protocol)
    protocol.update(
        schema="purpose-relative-source-grounding-stage-a-v2",
        status="FROZEN / UNAPPROVED / NOT_EXECUTED",
        worker_timeout=216000,
    )
    protocol["historical_C_v1_gold_instructions_sha256"] = protocol.pop(
        "gold_instructions_sha256",
    )
    protocol["scientific_method"] = ADDRESS + "/method.md"
    protocol["design_scope"] = (
        "Original hypothesis/treatment/authoring/analysis retained; C-v1 procedure "
        "superseded only by the separately frozen C-v2 method"
    )
    protocol["no_execution_scope"] = (
        "NEW_PROSPECTIVE_RUN_ONLY; ORIGINAL_B22_B23_ENTERED"
    )
    protocol["supersession"] = {
        "prior_stage_a": OLD_STAGE_A,
        "historical_run": OLD_RUN,
        "engineering_base": BASE,
        "engineering_checkpoint": engineering,
        "C_v1": "0022 ENTERED; turn/start rejected before adjudication; DEAD; not retried",
        "C_v2": "DISTINCT_PROSPECTIVE_MEASUREMENT_PROCEDURE",
        "gold_definitions": "UNCHANGED",
        "B_scientific_semantics": "UNCHANGED",
        "cohort_and_authoring": "EXACT_REUSE_0022_0023_0024",
        "gold_access": False,
        "child_access": False,
        "confirmation_reserve_access": False,
        "failed_semantic_judgments_used": False,
    }
    protocol["workers"]["grounding"] = fresh.configuration()
    protocol["c2"] = {
        "semantic": config,
        "policy": execution.POLICY,
        "partitions": {},
        "A1_instruction_sha256": digest(classification.INSTRUCTION.encode()),
        "A2_instruction_sha256": digest(packing.INSTRUCTIONS.encode()),
        "GLOBAL_instruction_sha256": digest(disclosure.INSTRUCTION.encode()),
        "A2_partition_algorithm_sha256": digest(Path(packing.__file__).read_bytes()),
        "response_schema_implementation_sha256": digest(
            Path(response.__file__).read_bytes(),
        ),
        "input_budget": {
            "characters": 700000,
            "utf8_bytes": 700000,
            "dynamic_exact_gate": "BEFORE_SEMANTIC_ENTERED",
        },
        "response_method_bytes": 65536,
        "actual_certified_output_bytes": 63357,
        "uncertainty": "NEVER_NEGATIVE; REMAINING_UNCERTAINTY_FAILS_CANONICAL_ASSEMBLY",
        "A2_excess": "ENTIRE_CASE_STOPS_BEFORE_FIRST_A2_ENTERED; NO_SUBSET",
        "limitations": [
            "A1 false negatives unrecoverable; no per-cell rationale",
            "A2 cannot recover A1 NO_USEFUL",
            "Global cannot recover A2 omissions",
            "Representation/capacity/spend fail closed",
            "Multiple fresh calls increase burden",
            "No automatic scientific retry",
        ],
        "usage": "FIVE_REPORTED_CATEGORIES_OR_UNKNOWN; MANDATORY_BEFORE_PUBLICATION; NO_OVERLAPPING_TOTAL_OR_SUBSCRIPTION_COST",
    }
    files: dict[str, bytes] = {}
    cohort = []
    for card, case in zip(await freeze.cards(), execution.A1_CALLS, strict=True):
        base = f"experiments/codex_dogfood/case_{case}/"
        for name in (
            "protocol.json",
            "frame.json",
            "resources.json.gz",
            "task.txt",
            "README.md",
            ".gitattributes",
        ):
            require(
                (ROOT / base / name).read_bytes()
                == await git("show", BASE + ":" + base + name),
                "Scientific authoring changed",
            )
        design, metadata = (
            load(ROOT / base / "protocol.json"),
            load(ROOT / base / "frame.json"),
        )
        rows = json.loads(
            gzip.decompress((ROOT / base / "resources.json.gz").read_bytes()),
        )
        require(
            design["task_text"] == card["task_text"] and design["population"] == card,
            "Public task/cohort binding",
        )
        require(
            design["frame"] == freeze.frame_contract(card, metadata, rows),
            "Exact parent frame replay",
        )
        packet = workers.gold_packet(design, rows)
        require(
            json_bytes(packet)
            == (
                ROOT
                / f"experiments/source_grounding/runs/{OLD_RUN}/PACKET/{case}/packet.json"
            ).read_bytes(),
            "Blind semantic disclosure content changed",
        )
        part = packing.partition(packet)
        require(
            part["partition_sha256"] == EXPECTED[case]
            and len(part["batches"]) == execution.A1_CALLS[case],
            "Engineering A1 partition differs",
        )
        protocol["c2"]["partitions"][case] = part
        files[f"{ADDRESS}/{case}-A1-partition.json"] = json_bytes(part)
        worst = disclosure.maximum_disclosure(packet)
        require(len(worst.decode()) * 10 <= 1048576 * 7, "Worst-case B character fit")
        for batch in part["batches"]:
            execution.check(
                config,
                classification.render(
                    packet,
                    batch["source_keys"],
                    evidence.sources(packet),
                ),
                classification.contract(
                    batch["source_keys"],
                    [o["id"] for o in packet["obligations"]],
                ),
            )
        files[f"{ADDRESS}/{case}-budget.json"] = json_bytes(
            {
                "A1": part,
                "B_worst_chars": len(worst.decode()),
                "B_worst_bytes": len(worst),
                "B_actual_bytes_gate": 700000,
                "B_output_maximum": schema.envelope(
                    response.pass_b(
                        len(rows) * 2,
                        [o["id"] for o in packet["obligations"]],
                    ),
                ).__dict__,
            },
        )
        cohort.append(
            {
                "case": case,
                "population": card["case_id"],
                "task": card["task_text"],
                "parent_commit": card["frame"]["parent_commit"],
                "parent_tree": card["frame"]["parent_tree"],
                "frame": design["frame"],
                "resources": len(rows),
                "obligations_sha256": digest(json_bytes(design["obligations"])),
            },
        )
    protocol["adopted_branches"] = {}
    protocol["preserved_evidence"] = {
        f"experiments/source_grounding/runs/{OLD_RUN}/journal/{p}": h
        for p, h in JOURNALS.items()
    }
    journal_copy = {}
    durable = ROOT / ADDRESS / "historical-journals.json"
    for path, sha256 in protocol["preserved_evidence"].items():
        raw = (
            (ROOT / path).read_bytes()
            if (ROOT / path).exists()
            else base64.b64decode(load(durable)[path], validate=True)
        )
        require(digest(raw) == sha256, "Historical journal mutation")
        journal_copy[path] = base64.b64encode(raw).decode()
    files[f"{ADDRESS}/historical-journals.json"] = json_bytes(journal_copy)
    for case, expected in SEALS.items():
        path = f"experiments/orchestration/engineering/adopted_branches/{OLD_RUN}/{case}/seal.json"
        seal = load(ROOT / path)
        binding = {
            "path": path,
            "sha256": expected,
            "compatibility_sha256": seal["compatibility_sha256"],
        }
        branch = load_branch(ROOT, binding)
        original_contract = branch.value["compatibility"]["scientific_contract"]
        revised = {p: digest((ROOT / p).read_bytes()) for p in original_contract}
        require(
            {p for p in revised if revised[p] != original_contract[p]}
            == {"experiments/source_grounding/capture.py"},
            "Unexpected B compatibility change",
        )
        address = f"{ADDRESS}/{case}-adoption-compatibility.json"
        raw = json_bytes(
            {
                "schema": "prospective-completed-branch-compatibility-v1",
                "origin_seal_sha256": expected,
                "original_contract": original_contract,
                "prospective_contract": revised,
                "scientific_semantics": "UNCHANGED",
                "operational_changes": "Optional pre-entry callback only; original proof verifier source remains attributed to original implementation",
                "source_proof": "Exact AST comparison after removing only the two declared operational binding changes",
                "no_new_judgment_or_Sol_call": True,
                "no_retroactive_publication": True,
            },
        )
        files[address] = raw
        binding["prospective_compatibility"] = {"path": address, "sha256": digest(raw)}
        protocol["adopted_branches"][case] = binding
    protocol["workers"]["gold"] = {
        **config,
        "kind": "process",
        "prompt_file": "INSTRUCTIONS.md",
        "environment_allowlist": workers.ENVIRONMENT and list(workers.ENVIRONMENT),
        "argv": [
            "{python}",
            "-B",
            "{repository}/experiments/source_grounding/chunked/entry.py",
            "C2",
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
    }
    files[f"{ADDRESS}/protocol.json"] = json_bytes(protocol)
    files[f"{ADDRESS}/cohort.json"] = json_bytes(cohort)
    files[f"{ADDRESS}/method.md"] = (
        Path(execution.__file__).parent / "METHOD.md"
    ).read_bytes()
    pinned = freeze.implementations()
    for receipt_address, folder in (
        (capacity.RECEIPT_ADDRESS, "capacity-evidence"),
        (output_capacity.ADDRESS, "output-evidence"),
    ):
        receipt = load(ROOT / receipt_address)
        addresses = [
            receipt_address,
            *(
                str(Path(receipt_address).parent / folder / name).replace("\\", "/")
                for name in receipt["evidence"]
            ),
        ]
        for address in addresses:
            pinned[address] = digest((ROOT / address).read_bytes())
    for name in ("METHOD.md", "README.md"):
        address = f"experiments/source_grounding/chunked/{name}"
        pinned[address] = digest((ROOT / address).read_bytes())
    files[f"{ADDRESS}/integrity.json"] = json_bytes(
        {
            "schema": "source-grounding-stage-a-integrity-v1",
            "artifacts": {n: digest(v) for n, v in files.items()},
            "implementation": pinned,
        },
    )
    return files


async def run_plan(checkpoint: str) -> Any:
    """Derive a new unapproved plan without altering the old prospective bytes."""
    value = load(ROOT / old_plan.PLAN_ADDRESS)
    integrity = load(ROOT / ADDRESS / "integrity.json")
    protocol = load(ROOT / ADDRESS / "protocol.json")
    value.update(
        name="purpose-relative-source-grounding-bounded-chunked-04",
        attempt=4,
        stage_a={
            "checkpoint": checkpoint,
            "protocol": {
                "path": ADDRESS + "/protocol.json",
                "sha256": digest(json_bytes(protocol)),
            },
            "integrity": {
                "path": ADDRESS + "/integrity.json",
                "sha256": digest(json_bytes(integrity)),
            },
        },
        semantic=protocol["workers"]["gold"],
        adopted_branches=protocol["adopted_branches"],
        preserved_evidence=protocol["preserved_evidence"],
        implementation=integrity["implementation"],
        controller_implementation=implementation(),
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
    for command in value["commands"].values():
        command[2] = "{repository}/experiments/source_grounding/chunked/entry.py"
        command[command.index("--stage-a") + 1] = checkpoint
    checks = old_plan.validation_commands(integrity["implementation"])
    value["validation"] = {"local": checks, "checkpoint": checks, "final": checks}
    value["timeouts"]["worker"] = 216000
    value["semantic"]["argv"][value["semantic"]["argv"].index("--stage-a") + 1] = (
        checkpoint
    )
    RunPlan.parse(value)
    return value


async def main() -> None:
    """Write once or replay prospective bytes; never approve or execute a run."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("mode", choices=("build", "verify", "plan", "verify-plan"))
    parser.add_argument("--checkpoint", required=True)
    args = parser.parse_args()
    if args.mode in {"plan", "verify-plan"}:
        files = {PLAN: json_bytes(await run_plan(args.checkpoint))}
    else:
        files = await stage_a(args.checkpoint)
    for name, raw in files.items():
        if args.mode in {"verify", "verify-plan"}:
            require(
                (ROOT / name).read_bytes() == raw,
                "Prospective deterministic replay differs: " + name,
            )
        else:
            require(not (ROOT / name).exists(), "Prospective overwrite refused")
            put_binary(ROOT / name, raw)
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
