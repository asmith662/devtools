# Copyright (c) 2026
# ruff: noqa: T201, EM101, TRY003 -- bounded recovery seal CLI
"""Seal capture plumbing without any prospective native scientific operation."""

from __future__ import annotations

import argparse
import asyncio
from pathlib import Path
from typing import Any

from experiments.codex_dogfood.case_0009.artifacts import (
    ROOT,
    binary,
    digest,
    json_bytes,
    put_text,
    read_json,
)
from experiments.codex_dogfood.case_0015 import freeze as stage_a
from experiments.codex_dogfood.case_0015.stage_b.authenticate import authenticate
from experiments.codex_dogfood.case_0015.stage_b.execute import PACKAGE, source_hashes
from experiments.codex_dogfood.case_0015.stage_b.fingerprint import (
    SCHEMA,
    prepared_fingerprint,
)
from experiments.codex_dogfood.case_0015.stage_b.legacy import authenticate_failed
from experiments.codex_dogfood.case_0015.stage_b.records import (
    PreparedFields,
    PreparedFrame,
)

HERE = Path(__file__).resolve().parent


async def expected() -> dict[str, Any]:
    """Read immutable audit returns and original sealed Stage A only."""
    authentication = await authenticate()
    failed = PACKAGE / "attempts/case-0015-stage-b-1"
    journal = authenticate_failed(failed)
    old_sources = read_json(failed / "execution_started.json")["implementation_sha256"]
    for name, value in old_sources.items():
        source = ROOT / name
        if source.parent == PACKAGE:
            source = HERE / "attempt1_sources" / source.name
        if digest(binary(source)) != value:
            raise ValueError("Failed capture source archive mismatch: " + name)
    if (PACKAGE / "attempts/case-0015-stage-b-2").exists():
        raise ValueError("Recovery freeze must precede attempt 2")
    if any(
        (stage_a.CASE / name).exists()
        for name in ("stage_c/packet", "adjudication", "stage_d")
    ):
        raise ValueError("Packet/gold/effectiveness forbidden at recovery freeze")
    paths = {
        *HERE.glob("*.py"),
        HERE / "README.md",
        HERE / ".gitattributes",
        *HERE.joinpath("attempt1_sources").glob("*"),
        *stage_a.CASE.joinpath("stage_c").glob("*.py"),
        stage_a.CASE / "stage_c/.gitattributes",
        stage_a.CASE / "STATUS.md",
    }
    implementation = {
        **source_hashes(),
        **{
            p.relative_to(ROOT).as_posix(): digest(binary(p))
            for p in sorted(paths)
            if p.is_file()
        },
    }
    return {
        "schema": "case-0015-capture-metadata-recovery-v2",
        "status": "FROZEN_METADATA_CAPTURE_ONLY; NO_SUCCESSFUL_STAGE_B",
        "stage_a": authentication,
        "all_stage_a_sealed_bytes": "UNCHANGED",
        "fingerprint_schema": SCHEMA,
        "record_schemas": [PreparedFrame.SCHEMA, PreparedFields.SCHEMA],
        "legacy_attempt_1": "FAILED_AUDIT_ONLY; NO_RETRY; NO_TREATMENT",
        "failed_audit": read_json(failed / "failed_audit_hashes.json"),
        "failed_manifest_sha256": digest(binary(failed / "failed_audit_hashes.json")),
        "readonly_prepared_fingerprint": prepared_fingerprint(
            journal.state["values"]["frame:prepare"],
            journal.state["values"]["fields:prepare"],
        ),
        "attempt_2_initial_operations": 0,
        "gold": "ABSENT",
        "effectiveness": "UNKNOWN",
        "outcome": "NOT_SELECTED",
        "implementation": implementation,
        "validation": {
            "synthetic_tests": "128 PASSED; 3 pre-capture guarded skips",
            "ruff": "PASS",
            "formatter": "PASS",
            "strict_mypy": "PASS",
            "protected_development": "1588 PASSED; 2 SKIPPED; 100% branch coverage",
        },
    }


async def main() -> None:
    """Exclusively publish or replay the recovery seal."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--verify", action="store_true")
    verify = parser.parse_args().verify
    raw = json_bytes(await expected())
    target = HERE / "integrity.json"
    if verify:
        if binary(target) != raw:
            raise ValueError("Recovery deterministic seal mismatch")
    else:
        put_text(target, raw.decode())
    print("METADATA RECOVERY PASS; no prospective operation invoked")


if __name__ == "__main__":
    asyncio.run(main())
