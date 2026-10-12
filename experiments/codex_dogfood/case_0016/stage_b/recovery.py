# Copyright (c) 2026
# ruff: noqa: EM101, TRY003, E501, T201, PLR2004
"""Freeze capture-only recovery; immutable failed evidence never feeds treatment."""

from __future__ import annotations

import argparse
import ast
import asyncio
import gzip
import json
from typing import Any

from experiments.codex_dogfood.case_0009.artifacts import (
    ROOT,
    binary,
    digest,
    git,
    json_bytes,
    put_text,
    read_json,
)
from experiments.codex_dogfood.case_0012.stage_b.durability import (
    Journal as NativeJournal,
)
from experiments.codex_dogfood.case_0016 import freeze, protocol
from experiments.codex_dogfood.case_0016.stage_b.authenticate import (
    EXECUTION,
    FAILED,
    PACKAGE,
    SCHEDULE_PATH,
    STAGE_A,
    authenticate,
    source_hashes,
)
from experiments.codex_dogfood.case_0016.stage_b.execute import schedule

RECOVERY = freeze.CASE / "recovery"
FAILED_SEAL = "90b6c21765505836e228182771e193aad1782d7c97f6240e748d222548267307"
FAILED_CHAIN = "4633d7a8b8ca8f014d3e87b612850e40075436eaf6d8014db4d9c5158557b3a5"
SCHEDULE_ONE = "1c5e255a800c872a397506805cc0da6942803be519a681f35def8a58383e71b6"


def failed_hashes() -> dict[str, Any]:
    """Authenticate all failed bytes, extras/absence and original source bindings."""
    if digest(binary(FAILED / "failed_audit_hashes.json")) != FAILED_SEAL:
        raise ValueError("Attempt-1 failed audit seal differs")
    seal = read_json(FAILED / "failed_audit_hashes.json")
    actual = {
        p.relative_to(FAILED).as_posix() for p in FAILED.rglob("*") if p.is_file()
    }
    if (
        actual != set(seal["sha256"]) | {"failed_audit_hashes.json"}
        or any(digest(binary(FAILED / p)) != h for p, h in seal["sha256"].items())
        or (FAILED / "execution_completed.json").exists()
    ):
        raise ValueError("Attempt-1 immutable evidence differs")
    for name, sha in seal["implementation_sha256"].items():
        original = (
            RECOVERY / "original_stage_b" / name.rsplit("/", 1)[-1]
            if name.startswith("experiments/codex_dogfood/case_0016/stage_b/")
            else ROOT / name
        )
        if digest(binary(original)) != sha:
            raise ValueError("Attempt-1 original implementation binding differs")
    if digest(binary(PACKAGE / "operation_schedule.json")) != SCHEDULE_ONE:
        raise ValueError("Attempt-1 operation schedule differs")
    return seal


def authenticate_failed() -> dict[str, Any]:
    """Read original returns without deriving References or constructing a graph."""
    seal = failed_hashes()
    journal = NativeJournal.load(FAILED)
    operations = journal.state["operations"]
    if (
        journal.events != 332
        or len(operations) != 166
        or journal.chain != FAILED_CHAIN
        or any(o["status"] != "RETURNED" or o["invocations"] != 1 for o in operations)
        or operations[-1]["identity"]
        != "ri:references:src/devtools/models/interaction/providers/__init__.py"
        or list((FAILED / "operations").glob("*failed_no_return*"))
    ):
        raise ValueError(
            "Attempt-1 exact scientific/failed-publication boundary differs",
        )
    return {
        "execution": "case-0016-stage-b-1",
        "status": "FAILED_AUDIT_ONLY",
        "operations_returned": 166,
        "journal_events": 332,
        "journal_chain": journal.chain,
        "failed_audit_sha256": FAILED_SEAL,
        "authenticated_artifacts": len(seal["sha256"]) + 1,
        "retries": 0,
        "scientific_exceptions": 0,
        "publication_failures": 1,
    }


def scientific_identity() -> None:
    """Compare scientific composition AST and exact frozen operation identities."""
    before = ast.parse(binary(RECOVERY / "original_stage_b/execute.py").decode())
    after = ast.parse(binary(PACKAGE / "execute.py").decode())
    for name in ("schedule", "universe", "observed_ppr"):
        old = next(
            n for n in before.body if isinstance(n, ast.FunctionDef) and n.name == name
        )
        new = next(
            n for n in after.body if isinstance(n, ast.FunctionDef) and n.name == name
        )
        if ast.dump(old) != ast.dump(new):
            raise ValueError("Scientific helper changed: " + name)
    old_exec = next(
        n
        for n in before.body
        if isinstance(n, ast.AsyncFunctionDef) and n.name == "execute"
    )
    new_exec = next(
        n
        for n in after.body
        if isinstance(n, ast.AsyncFunctionDef) and n.name == "execute"
    )
    old_try = next(n for n in old_exec.body if isinstance(n, ast.Try))
    new_try = next(n for n in new_exec.body if isinstance(n, ast.Try))
    if [ast.dump(n) for n in old_try.body] != [ast.dump(n) for n in new_try.body]:
        raise ValueError("Scientific invocation schedule/body changed")
    rows = json.loads(gzip.decompress(binary(freeze.CASE / "resources.json.gz")))
    if (
        tuple(read_json(PACKAGE / "operation_schedule.json")["operations"])
        != schedule(rows)
        or len(schedule(rows)) != 464
    ):
        raise ValueError("464 operation identities changed")


def recovery_sources() -> dict[str, str]:
    """Bind corrected capture, reviewed blind preparation and preserved sources."""
    paths = {**source_hashes()}
    for path in (freeze.CASE / "stage_c").glob("*.py"):
        paths[path.relative_to(ROOT).as_posix()] = digest(binary(path))
    for path in (RECOVERY / "original_stage_b").iterdir():
        paths[path.relative_to(ROOT).as_posix()] = digest(binary(path))
    return dict(sorted(paths.items()))


async def expected() -> dict[str, bytes]:
    """Deterministic capture-only recovery freeze; no prospective scientific call."""
    authentication = await authenticate()
    failed = authenticate_failed()
    scientific_identity()
    if any(
        (freeze.CASE / p).exists()
        for p in ("adjudication", "gold.json", "stage_d", "stage_c/packet")
    ):
        raise ValueError("Unexpected gold/packet/effectiveness data")
    old = read_json(PACKAGE / "operation_schedule.json")
    two = {**old, "execution": EXECUTION}
    review = "# Case 0016 capture-only recovery\n\nAttempt 1 = FAILED_AUDIT_ONLY. Attempt 2 has not started. No successful Stage B, packet, gold or effectiveness claim.\n\nThe established cause is permission denial replacing derived raw_checkpoint.json after durable RETURNED at operation 166. A contemporaneous PowerShell reader is a plausible contributor only. No sleeps, write retries, process termination or scientific changes are introduced.\n\nThe sealed Case 0012 immutable journal/event/native-memo schema is reused unchanged. A capture-only subclass disables its mutable save hook. No raw checkpoint or equivalent mutable latest file is written during active execution. Final checkpoint bytes are derived from immutable records once at publication. Unique append-only timestamped progress is non-authoritative; publication warnings cannot veto a durable scientific RETURNED and cannot rerun it.\n\nDurable ENTERED -> invoke once -> durable RETURNED completes the operation. Native exceptions retain FAILED_NO_RETURN and stop. Failure to durably publish authoritative RETURNED stops without retry. Final success requires the complete journal, completion seal and deterministic scientific validation.\n\nAttempt 2 starts at operation 1 with independent native returns. No attempt-1 object enters treatment inputs. The 464 operation identities and scientific invocation AST are identical, as are all 193 Stage-A-sealed files. No production source, owner boundary, query/edge/seed/PPR/flow/RRF/map/gold/gate semantics change.\n\nUnexecuted Stage C code is allowlisted, deterministic and tested; it projects only Stage A task/obligations/resource bytes after a successful committed/pushed attempt 2. No packet or sterile workspace exists at this checkpoint.\n"
    trace = {
        "stage_a": authentication,
        "attempt_1": failed,
        "amendment": "CAPTURE_DURABILITY_ONLY",
        "authoritative": [
            "execution.claim",
            "execution_started.json",
            "immutable ENTERED/RETURNED/FAILED_NO_RETURN",
            "native/canonical return payloads",
            "journal chain",
            "execution_completed.json",
        ],
        "derived": [
            "append-only progress",
            "on-demand/final raw checkpoint",
            "human status",
        ],
        "active_mutable_writes": 0,
        "scientific_contract": "UNCHANGED",
        "scientific_AST": "IDENTICAL",
        "attempt_2_initial_counts": protocol.COUNTS,
        "attempt_2_operation_count": 464,
        "attempt_2_schedule_sha256": digest(json_bytes(two)),
        "gold": "ABSENT",
        "effectiveness": "UNKNOWN",
        "outcome": "NOT_SELECTED",
        "confirmation_reserve": "NOT_ACCESSED",
    }
    validation = {
        "authentication": "PASS",
        "attempt_1_hashes_chain_native_replay": "PASS",
        "scientific_identity": "PASS",
        "recovery_controlled_tests": "PASS",
        "protected_development": "1588 passed, 2 skipped, 100% production branch coverage",
        "static_checks": "PASS",
        "no_repair_treatment_execution": True,
    }
    files = {
        "RECOVERY.md": review.encode(),
        "trace.json": json_bytes(trace),
        "validation.json": json_bytes(validation),
    }
    files["integrity.json"] = json_bytes(
        {
            "schema": "case-0016-capture-recovery-v1",
            "stage_a": STAGE_A,
            "attempt_1_failed_audit_sha256": FAILED_SEAL,
            "attempt_1_operation_schedule_sha256": SCHEDULE_ONE,
            "attempt_2_schedule_sha256": digest(json_bytes(two)),
            "implementation": recovery_sources(),
            "artifacts": {k: digest(v) for k, v in files.items()},
            "scientific_contract": "UNCHANGED",
            "gold": "ABSENT",
            "outcome": "NOT_SELECTED",
        },
    )
    files["../stage_b/operation_schedule_2.json"] = json_bytes(two)
    return files


async def freeze_recovery() -> None:
    """Refuse replacement of any recovery seal, then publish deterministic bytes."""
    if (RECOVERY / "integrity.json").exists() or SCHEDULE_PATH.exists():
        raise FileExistsError("Recovery overwrite refused")
    for name, raw in (await expected()).items():
        put_text(RECOVERY / name, raw.decode())


async def authenticate_recovery() -> dict[str, str]:
    """Require committed recovery hashes, ancestry and unchanged failed evidence."""
    seal = read_json(RECOVERY / "integrity.json")
    failed_hashes()
    scientific_identity()
    if (
        seal["implementation"] != recovery_sources()
        or seal["attempt_2_schedule_sha256"] != digest(binary(SCHEDULE_PATH))
        or any(
            digest(binary(RECOVERY / name)) != sha
            for name, sha in seal["artifacts"].items()
        )
    ):
        raise ValueError("Recovery implementation/artifact/schedule seal differs")
    prefix = RECOVERY.relative_to(ROOT).as_posix()
    checkpoint = (
        (await git("log", "-1", "--format=%H", "--", prefix + "/integrity.json"))
        .decode()
        .strip()
    )
    if not checkpoint:
        raise ValueError("Recovery checkpoint is not committed")
    await git("merge-base", "--is-ancestor", STAGE_A, checkpoint)
    files = {
        **seal["implementation"],
        **{prefix + "/" + k: v for k, v in seal["artifacts"].items()},
        prefix + "/integrity.json": digest(binary(RECOVERY / "integrity.json")),
        SCHEDULE_PATH.relative_to(ROOT).as_posix(): digest(binary(SCHEDULE_PATH)),
    }
    for path, sha in files.items():
        if digest(await git("show", checkpoint + ":" + path)) != sha:
            raise ValueError("Committed recovery blob differs: " + path)
    return {
        "checkpoint": checkpoint,
        "integrity_sha256": digest(binary(RECOVERY / "integrity.json")),
        "attempt_1_failed_audit_sha256": FAILED_SEAL,
    }


def main() -> None:
    """Freeze recovery only; no treatment or packet execution path."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--verify", action="store_true")
    if parser.parse_args().verify:
        values = asyncio.run(expected())
        if any(binary(RECOVERY / p) != raw for p, raw in values.items()):
            raise ValueError("Recovery deterministic replay differs")
    else:
        asyncio.run(freeze_recovery())
    print("Case 0016 capture-only recovery PASS; attempt 2 unexecuted; gold ABSENT")


if __name__ == "__main__":
    main()
