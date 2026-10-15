# Copyright (c) 2026
# ruff: noqa: ANN401 -- finite experiment semantic workload certificate
"""Empirical profile compatibility, never maximum-capacity or execution authority."""

from __future__ import annotations

import gzip
import json
import platform
from pathlib import Path
from typing import Any

from devtools.agents.integrations.codex.parsing import parse_codex_turn_output
from devtools.agents.integrations.codex.usage import capture_codex_usage
from experiments.codex_dogfood.case_0009.artifacts import digest, json_bytes
from experiments.orchestration.storage import require
from experiments.orchestration.workers import runtime
from experiments.orchestration.workers.budget import BudgetError, FailureClass
from experiments.orchestration.workers.schema import (
    MAX_SEMANTIC_RESPONSE_UTF8_BYTES,
    canonical,
    validate,
)

SCHEMA = "semantic-workload-capacity-v1"
INPUT_CHARACTERS = 700000
INPUT_BYTES = 700000
TRANSPORT_CHARACTERS = 1048576
RECEIPT_ADDRESS = (
    "experiments/orchestration/engineering/host_disclosure/capacity-receipt.json"
)


def profile(configuration: Any) -> dict[str, Any]:
    """Bind transport/permission/measurement implementation, not future callers."""
    package = Path(__file__).parent
    source = package.parents[2] / "src/devtools"
    return {
        "os": platform.platform(),
        "python": platform.python_version(),
        "cli_version": "0.162.1",
        "model_id": configuration["model_id"],
        "reasoning": configuration["reasoning"],
        "execution_profile": "SEMANTIC_WORKER",
        "configuration": runtime.configuration(),
        "transport": "UTF8_STDIN; NATIVE_SCHEMA; SOLE_FINAL_MESSAGE",
        "empty_cwd_policy": "EMPTY_OUTSIDE_CHECKOUT",
        "implementation": {
            name: digest((package / name).read_bytes())
            for name in (
                "capacity.py",
                "budget.py",
                "schema.py",
                "measurement.py",
                "accounting.py",
                "semantic.py",
                "codex.py",
                "runtime.py",
                "process.py",
                "supervisor.py",
            )
        },
        "framework": {
            address: digest((source / address).read_bytes())
            for address in (
                "agents/integrations/codex/parsing.py",
                "agents/integrations/codex/usage.py",
                "models/interaction/usage.py",
                "observability/evidence/invocation.py",
            )
        },
    }


def authenticate(receipt: Any, configuration: Any) -> None:
    """Check empirical lower-bound evidence without inferring a runtime maximum."""
    require(
        configuration["model_id"] == "gpt-6-astra"
        and configuration["reasoning"] == "High"
        and configuration.get("bounded_response") is True
        and configuration["runtime"] == runtime.configuration(),
        "Exact Astra/High bounded semantic profile required",
    )
    current = profile(configuration)
    require(
        receipt["schema"] == SCHEMA
        and receipt["status"] == "PASS"
        and receipt["engineering_only"] is True
        and receipt["profile"] == current
        and receipt["profile_sha256"] == digest(json_bytes(current)),
        "Incompatible capacity profile receipt",
    )
    require(
        receipt["method_response_maximum_bytes"] == MAX_SEMANTIC_RESPONSE_UTF8_BYTES
        and receipt["input_characters"] >= INPUT_CHARACTERS
        and receipt["input_bytes"] >= INPUT_BYTES
        and receipt["input_characters"] < TRANSPORT_CHARACTERS
        and receipt["response_bytes"] * 10 >= MAX_SEMANTIC_RESPONSE_UTF8_BYTES * 9
        and receipt["response_bytes"] <= MAX_SEMANTIC_RESPONSE_UTF8_BYTES,
        "Insufficient tested workload envelope",
    )
    require(
        set(receipt["checks"])
        == {
            "process",
            "sole_response",
            "schema",
            "zero_tools",
            "empty_cwd",
            "final_agreement",
            "usage",
            "not_truncated",
            "single_invocation",
        }
        and all(receipt["checks"].values()),
        "Incomplete capacity evidence",
    )


def check_input(receipt: Any, configuration: Any, rendered: bytes) -> None:
    """Dynamic exact check before ENTERED; oversize never launches a model."""
    authenticate(receipt, configuration)
    chars = len(rendered.decode("utf-8", errors="strict"))
    if chars > receipt["input_characters"] or len(rendered) > receipt["input_bytes"]:
        raise BudgetError(
            FailureClass.WORKLOAD_CAPACITY_LIMIT,
            f"Input {chars} characters/{len(rendered)} bytes exceeds certified "
            f"{receipt['input_characters']}/{receipt['input_bytes']}; "
            "no semantic entry",
        )


def authenticate_files(
    root: Path,
    receipt: Any,
    *,
    folder: str = "capacity-evidence",
) -> None:
    """Authenticate the repository-owned exact capture closure, excluding secrets."""
    require(
        folder in {"capacity-evidence", "minimal-evidence"},
        "Engineering evidence owner",
    )
    evidence_root = (
        root / "experiments/orchestration/engineering/host_disclosure" / folder
    )
    require(
        set(receipt["evidence"])
        == {
            "response.json",
            "stdout.jsonl.gz",
            "process-exit.json",
            "preparation.json",
            "measurement.json",
            "response-schema.json",
            "invocation-claim.json",
            "semantic-receipt.json",
        },
        "Capacity artifact closure incomplete",
    )
    files = {name: (evidence_root / name).read_bytes() for name in receipt["evidence"]}
    require(
        all(digest(raw) == receipt["evidence"][name] for name, raw in files.items()),
        "Capacity artifact hash mismatch",
    )
    stdout = gzip.decompress(files["stdout.jsonl.gz"])
    turn = parse_codex_turn_output(stdout)
    usage = capture_codex_usage(stdout)
    require(len(usage) == 1, "Capacity usage turn count")
    response = json.loads(files["response.json"])
    validate(response, json.loads(files["response-schema.json"]))
    require(
        canonical(response) == files["response.json"]
        and canonical(json.loads(turn.final_message)) == files["response.json"]
        and digest(files["response.json"]) == receipt["response_sha256"],
        "Capacity final response agreement failed",
    )
    exit_record = json.loads(files["process-exit.json"])
    require(
        exit_record["exit_code"] == 0
        and not exit_record["stdout_truncated"]
        and not exit_record["stderr_truncated"],
        "Capacity process failed or truncated",
    )
