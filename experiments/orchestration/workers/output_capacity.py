# Copyright (c) 2026
# ruff: noqa: ANN401 -- bounded output-only engineering receipt
"""Certify observed output workload separately from large-input certification."""

import gzip
import json
from pathlib import Path
from typing import Any

from devtools.agents.integrations.codex.parsing import parse_codex_turn_output
from devtools.agents.integrations.codex.usage import capture_codex_usage
from experiments.codex_dogfood.case_0009.artifacts import digest, json_bytes
from experiments.orchestration.storage import require
from experiments.orchestration.workers import capacity, schema

SCHEMA = "semantic-output-capacity-v1"
ADDRESS = "experiments/orchestration/engineering/host_disclosure/output-receipt.json"
MINIMUM_BYTES = 63000


def authenticate(receipt: Any, config: Any, root: Path) -> None:
    """Require exact profile, actual output and immutable synthetic capture closure."""
    require(
        receipt["schema"] == SCHEMA
        and receipt["engineering_only"] is True
        and receipt["status"] == "PASS"
        and receipt["invocation"] == "SYNTHETIC-ASTRA-HIGH-OUTPUT-01"
        and receipt["profile"] == capacity.profile(config)
        and receipt["profile_sha256"] == digest(json_bytes(capacity.profile(config)))
        and MINIMUM_BYTES
        <= receipt["response_bytes"]
        <= schema.MAX_SEMANTIC_RESPONSE_UTF8_BYTES
        and all(receipt["checks"].values())
        and receipt["automatic_invocation_retries"] == 0,
        "Output capacity receipt incompatible/incomplete",
    )
    folder = root / Path(ADDRESS).parent / "output-evidence"
    required = {
        "response.json",
        "stdout.jsonl.gz",
        "process-exit.json",
        "preparation.json",
        "measurement.json",
        "response-schema.json",
        "invocation-claim.json",
        "semantic-receipt.json",
    }
    require(set(receipt["evidence"]) == required, "Output evidence closure")
    files = {name: (folder / name).read_bytes() for name in required}
    require(
        all(digest(raw) == receipt["evidence"][n] for n, raw in files.items()),
        "Output capture hash differs",
    )
    stdout = gzip.decompress(files["stdout.jsonl.gz"])
    turn = parse_codex_turn_output(stdout)
    events = [json.loads(line) for line in stdout.splitlines() if line.strip()]
    require(
        sum(e.get("type") == "turn.started" for e in events) == 1,
        "Output turn count",
    )
    usage = capture_codex_usage(stdout)
    require(len(usage) == 1, "Output usage count")
    payload = json.loads(files["response.json"])
    contract = json.loads(files["response-schema.json"])
    schema.validate(payload, contract)
    require(
        schema.canonical(payload)
        == files["response.json"]
        == schema.canonical(json.loads(turn.final_message))
        and len(files["response.json"]) == receipt["response_bytes"]
        and digest(files["response.json"]) == receipt["response_sha256"],
        "Output canonical/final agreement",
    )
    measured = json.loads(files["measurement.json"])["measurement"]
    require(
        measured == receipt["measurement"]["measurement"]
        and measured["accepted"]
        and all(
            measured["usage"][k] is not None
            for k in (
                "input_tokens",
                "cached_input_tokens",
                "cache_write_tokens",
                "output_tokens",
                "reasoning_tokens",
            )
        ),
        "Output mandatory usage",
    )
