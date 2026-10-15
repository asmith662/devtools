# Copyright (c) 2026
# ruff: noqa: ANN401, ASYNC240, PLC0415, E501 -- one bounded host-owned semantic operation
"""One blind Astra invocation per case; no A1/A2/consolidation fallback exists."""

import base64
import gzip
import json
import os
import sys
from collections import Counter
from pathlib import Path
from types import SimpleNamespace
from typing import Any

from devtools.core.time import Duration
from experiments.codex_dogfood.case_0009.artifacts import digest, json_bytes, put_binary
from experiments.orchestration import usage_budget
from experiments.orchestration.storage import load, materialize, require
from experiments.orchestration.workers import (
    accounting,
    measurement,
    runtime,
    schema,
    semantic,
)
from experiments.source_grounding import workers
from experiments.source_grounding.chunked import execution as compatible
from experiments.source_grounding.discrimination import gold

ROOT = compatible.ROOT
EXTRA = ("candidate-capture.json.gz", "candidate-usage.json")
AUTHORIZED = "TREATMENT_INDEPENDENT_BROAD_CANDIDATES"
BLINDNESS = (
    "repository",
    "git_history",
    "parent_siblings",
    "prior_session",
    "web",
    "queries",
    "ranks_scores",
    "grounding",
    "qualified",
    "treatment_results",
    "timings",
    "other_cases",
    "child",
    "prior_gold",
    "confirmation_reserve",
)
METHOD = (
    b"# Candidate-surface discrimination gold\n\nOne fresh blind Astra/High primary "
    b"per case. Local source/target usefulness and pursuit-value judgments only. "
    b"No global necessity, witness completeness, recall or sufficiency claim. "
    b"Own-source exact quote anchors are bounded at 64 Unicode characters; pursuit "
    b"reason at 32. Inadequate representation fails closed. No second reviewer, "
    b"reconciliation, semantic fallback or automatic retry.\n"
)
BUILDER = b"""# Host-only deterministic builder; never executed by the model.
import argparse,sys
p=argparse.ArgumentParser()
p.add_argument('command',choices=['build'])
p.add_argument('--root',required=True)
p.add_argument('--repository',required=True)
a=p.parse_args()
sys.path.insert(0,a.repository)
sys.path.insert(0,a.repository+'/src')
from pathlib import Path
from experiments.source_grounding.discrimination.execution import build
build(Path(a.root))
"""
CAPTURE_FILES = (
    "receipt.json",
    "response-schema.json",
    "final-response.txt",
    "invocation-measurement.json",
    "process/stdin.bin",
    "process/stdout.log",
    "process/stderr.log",
    "process/exit.json",
)


def configuration() -> Any:
    """Use the exact certified transport/profile, without changing pinned code."""
    return compatible.configuration()


def packet_files(selection: Any, frame: Any, run_id: str) -> dict[str, bytes]:
    """Separate host provenance/identities from the complete authorized disclosure."""
    host = {
        "selection": selection,
        "frame": frame,
        "invocation": run_id + "/" + selection["case"] + "/C",
        "run_id": run_id,
    }
    return {
        "packet.json": json_bytes(selection["packet"]),
        "INSTRUCTIONS.md": gold.INSTRUCTION.encode(),
        "stage_c_builder.py": BUILDER,
        "candidate-host.json": json_bytes(host),
    }


def check(root: Path) -> Any:
    """Exact planned packet/schema/input/output and capacity checks before entry."""
    host = load(root / "candidate-host.json")
    selection = host["selection"]
    raw = gold.render(load(root / "packet.json"))
    require(
        digest(raw) == selection["input"]["sha256"],
        "Frozen candidate disclosure differs",
    )
    require(
        (root / "stage_c_builder.py").read_bytes() == BUILDER
        and (root / "INSTRUCTIONS.md").read_bytes() == gold.INSTRUCTION.encode(),
        "Frozen candidate instruction/builder differs",
    )
    return compatible.check(configuration(), raw, selection["response_schema"])


def products(root: Path, payload: Any) -> dict[str, bytes]:
    """Serialize independently judged local labels and exact host-derived spans."""
    host = load(root / "candidate-host.json")
    selected = host["selection"]
    review = gold.project(
        selected["packet"],
        payload,
        selected["response_schema"],
        selected["host"]["resources"],
    )
    review.update(
        frame=host["frame"],
        selection_sha256=selected["sha256"],
        model="GPT-6 Astra",
        reasoning="High",
    )
    statistics = {
        "candidates": len(review["judgments"]),
        "labels": {
            role: dict(Counter(r[role] for r in review["judgments"]))
            for role in ("source_usefulness", "target_usefulness", "pursuit_value")
        },
    }
    files = {
        "stage_c_review.json": json_bytes(review),
        "stage_c_statistics.json": json_bytes(statistics),
        "STAGE_C_REVIEW.md": b"# Blind candidate discrimination\n\nExact local labels and anchors are in stage_c_review.json. No global gold claim.\n",
        "stage_c_validation.json": json_bytes(
            {
                "status": "PASS",
                "selection_sha256": selected["sha256"],
                "representation_complete": True,
            },
        ),
        "stage_c_method.md": METHOD,
        "stage_c_builder.py": BUILDER,
    }
    files["stage_c_hashes.json"] = json_bytes(
        {"sha256": {n: digest(v) for n, v in files.items()}},
    )
    return files


def build(root: Path) -> None:
    """Run the deterministic canonical artifact builder, preserving packet bytes."""
    captured = capture(root)
    for name, raw in products(root, captured["payload"]).items():
        target = root / name
        if target.exists():
            require(target.read_bytes() == raw, "Canonical candidate artifact mutation")
        else:
            put_binary(target, raw)


def capture(root: Path) -> Any:
    """Bound decompression of the exact retained host capture."""
    with gzip.open(root / EXTRA[0], "rb") as stream:
        raw = stream.read((128 << 20) + 1)
    require(len(raw) <= 128 << 20, "Candidate capture expansion bound")
    return json.loads(raw)


async def execute(root: Path, *, invoke: Any = None) -> None:
    """Exactly one logical primary; every failure remains terminal and retained."""
    check(root)
    packet = load(root / "packet.json")
    host = load(root / "candidate-host.json")
    selection = host["selection"]
    invocation = host["invocation"]
    folder = root / "semantic"
    require(not folder.exists(), "Entered semantic attempt cannot be retried")
    folder.mkdir()
    accepted = False
    failure = None
    try:
        if invoke is None:
            usage_budget.verify(ROOT, host["run_id"], packet["case"], "C")
            auth = folder / "auth"
            materialize(auth, {"auth.json": Path(workers.AUTH_FILE).read_bytes()})
            env = {k: os.environ[k] for k in runtime.ENVIRONMENT if k in os.environ}
            env["CODEX_HOME"] = str(auth)
            result = await semantic.primary(
                configuration(),
                json_bytes({"case": packet["case"], "frame": host["frame"]}),
                gold.INSTRUCTION.encode(),
                selection["response_schema"],
                invocation,
                folder / "worker",
                env,
                7200,
                10,
                rendered_input=gold.render(packet),
                empty_directory=folder / "empty-cwd",
            )
            measured = load(folder / "worker/invocation-measurement.json")
            retained = {
                n: base64.b64encode((folder / "worker" / n).read_bytes()).decode()
                for n in CAPTURE_FILES
            }
        else:
            result, measured = await invoke(
                gold.render(packet),
                selection["response_schema"],
                invocation,
            )
            retained = {}
        payload = result["payload"]
        products(root, payload)  # domain validity precedes accounting acceptance
        counted = accounting.accept(measured, "CANDIDATE_DISCRIMINATION_GOLD_VALID")
        captured = {
            "schema": "candidate-discrimination-capture-v1",
            "payload": payload,
            "receipt": result["provenance"],
            "measurement": counted,
            "files": retained,
            "input_sha256": digest(gold.render(packet)),
            "selection_sha256": selection["sha256"],
        }
        encoded = json_bytes(captured)
        require(len(encoded) <= 128 << 20, "EVIDENCE_REPRESENTATION_LIMIT")
        put_binary(root / EXTRA[0], gzip.compress(encoded, mtime=0))
        put_binary(root / EXTRA[1], json_bytes(counted))
        await workers.command(
            [
                sys.executable,
                "-B",
                str(root / "stage_c_builder.py"),
                "build",
                "--root",
                str(root),
                "--repository",
                str(ROOT),
            ],
            root,
            folder / "builder",
        )
        validate(root)
        accepted = True
    except BaseException as error:
        failure = type(error).__name__
        raise
    finally:
        if invoke is None:
            usage_budget.capture(
                ROOT,
                host["run_id"],
                packet["case"],
                "C",
                folder / "worker/invocation-measurement.json",
                accepted=accepted,
                failure_class=failure,
            )


def validate(root: Path) -> Any:
    """Replay exact disclosure, payload, canonical spans, raw usage and artifacts."""
    check(root)
    host = load(root / "candidate-host.json")
    captured = capture(root)
    require(
        captured["selection_sha256"] == host["selection"]["sha256"]
        and captured["input_sha256"]
        == digest(gold.render(host["selection"]["packet"])),
        "Capture disclosure binding",
    )
    require(
        all(
            (root / name).read_bytes() == raw
            for name, raw in products(root, captured["payload"]).items()
        ),
        "Canonical candidate gold replay",
    )
    require(
        load(root / EXTRA[1]) == captured["measurement"],
        "Candidate usage capture differs",
    )
    accounting.accept(captured["measurement"], "REPLAY")
    if not host["selection"]["case"].startswith("SYNTHETIC-"):
        raw = {
            n: base64.b64decode(v, validate=True) for n, v in captured["files"].items()
        }
        require(
            set(raw) == set(CAPTURE_FILES),
            "Complete native semantic capture required",
        )
        require(
            raw["process/stdin.bin"] == gold.render(host["selection"]["packet"])
            and json.loads(raw["receipt.json"]) == captured["receipt"],
            "Candidate process disclosure/provenance",
        )
        from devtools.agents.integrations.codex.parsing import parse_codex_turn_output

        turn = parse_codex_turn_output(raw["process/stdout.log"])
        expected_receipt = {
            "case": host["selection"]["case"],
            "frame": host["frame"],
            "invocation": host["invocation"],
            "model": "GPT-6 Astra",
            "reasoning": "High",
            "thread_id": turn.thread_id,
            "instruction_sha256": digest(gold.INSTRUCTION.encode()),
            "packet_sha256": digest(
                json_bytes({"case": host["selection"]["case"], "frame": host["frame"]}),
            ),
            "input_sha256": digest(raw["process/stdin.bin"]),
            "input_characters": len(raw["process/stdin.bin"].decode()),
            "input_bytes": len(raw["process/stdin.bin"]),
            "response_schema_sha256": digest(
                json_bytes(host["selection"]["response_schema"]),
            ),
            "response_sha256": digest(raw["final-response.txt"]),
            "process_exit": 0,
            "transport": "PASS",
            "schema_validation": "PASS",
        }
        require(
            all(captured["receipt"].get(k) == v for k, v in expected_receipt.items()),
            "Exact semantic runtime/input/schema provenance",
        )
        require(
            semantic.strict_object(turn.final_message)
            == captured["payload"]
            == semantic.strict_object(raw["final-response.txt"].decode()),
            "Sole final-message agreement",
        )
        require(
            raw["response-schema.json"]
            == json_bytes(schema.native(host["selection"]["response_schema"])),
            "Frozen native response schema",
        )
        exit_record = json.loads(raw["process/exit.json"])
        require(
            exit_record["exit_code"] == 0
            and not exit_record["stdout_truncated"]
            and not exit_record["stderr_truncated"],
            "Untruncated successful process required",
        )
        events = [
            semantic.strict_object(line)
            for line in raw["process/stdout.log"].decode().splitlines()
            if line.strip()
        ]
        items = [
            e.get("item", {}) for e in events if e.get("type", "").startswith("item.")
        ]
        require(
            sum(e.get("type") == "turn.completed" for e in events) == 1
            and sum(i.get("type") == "agent_message" for i in items) == 1
            and all(
                i.get("type") in {"agent_message", "reasoning", "error"} for i in items
            )
            and b"tools::router" not in raw["process/stderr.log"],
            "Tool-free sole semantic transport",
        )
        original = measurement.capture(
            configuration(),
            host["selection"]["case"],
            host["invocation"],
            gold.render(host["selection"]["packet"]),
            SimpleNamespace(
                stdout=raw["process/stdout.log"],
                duration=Duration.seconds(exit_record["duration_seconds"]),
            ),
            schema.canonical(captured["payload"]),
            validated=True,
            failure=None,
        )
        require(
            accounting.accept(original, "CANDIDATE_DISCRIMINATION_GOLD_VALID")
            == captured["measurement"],
            "Raw provider usage authentication",
        )
        require(
            captured["receipt"]["tool_calls"] == 0
            and captured["receipt"]["status"] == "PASS",
            "Tool-free completed transport required",
        )
    return {
        "status": "PASS",
        "model": "GPT-6 Astra",
        "reasoning": "High",
        "second_reviewer": False,
        "reconciliation": False,
        "host_routing_independently_verified": False,
        "blindness": dict.fromkeys(BLINDNESS, False),
        "authorized_surface": AUTHORIZED,
        "thread_id": captured["receipt"]["thread_id"],
    }
