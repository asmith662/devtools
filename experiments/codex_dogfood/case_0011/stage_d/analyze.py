# Copyright (c) 2026
# ruff: noqa: COM812 -- formatter owns scientific record commas
"""Publish or verify one Case 0011 Stage D artifact pipeline without retrieval."""

from __future__ import annotations

import argparse
import gzip
from pathlib import Path
from typing import Any

from experiments.codex_dogfood.case_0009.artifacts import (
    binary,
    digest,
    json_bytes,
    put_binary,
    put_text,
)
from experiments.codex_dogfood.case_0011.stage_d import inputs, metrics, reporting

ROOT = Path(__file__).resolve().parent
OUTPUTS = (
    "analysis.json",
    "analysis.md",
    "STAGE_D_REVIEW.md",
    "trace.json",
    "TRACE.md",
    "integrity.json",
    "r15_explanations.json.gz",
)


def artifacts(data: dict[str, Any]) -> dict[str, bytes]:
    """Produce all machine/human surfaces from one deterministic metric result."""
    analysis = metrics.evaluate(data, data["provenance"])
    analysis["diagnostic_replay"] = data["diagnostic_replay"]
    r15_payload = json_bytes(
        analysis["diagnostics"].pop("R1.5_reconstructed_explanations")
    )
    r15_archive = gzip.compress(r15_payload, mtime=0)
    analysis["diagnostics"]["R1.5_reconstructed_explanations"] = {
        "artifact": "r15_explanations.json.gz",
        "canonical_payload_sha256": digest(r15_payload),
        "archive_sha256": digest(r15_archive),
        "subjects": data["diagnostic_replay"]["representative_explanations"],
        "scope": (
            "Full reconstructed subject/term/overtaker records, stored once "
            "with deterministic lossless gzip."
        ),
    }
    trace = reporting.enrich(analysis, data)
    review = reporting.review(analysis, trace)
    files = {
        "r15_explanations.json.gz": r15_archive,
        "analysis.json": json_bytes(analysis),
        "analysis.md": reporting.report(analysis).encode(),
        "STAGE_D_REVIEW.md": review.encode(),
        "trace.json": json_bytes(trace),
        "TRACE.md": review.encode(),
    }
    sources = (
        "__init__.py",
        "inputs.py",
        "metrics.py",
        "diagnostics.py",
        "reporting.py",
        "analyze.py",
        "test_analysis.py",
        "pytest.ini",
        ".gitattributes",
    )
    files["integrity.json"] = json_bytes(
        {
            "schema": "case-0011-stage-d-integrity-v1",
            "sha256": {name: digest(raw) for name, raw in files.items()},
            "source_sha256": {name: digest(binary(ROOT / name)) for name in sources},
            "scope": (
                "Distinct Stage D layer; frozen inputs/traces unchanged; "
                "operational handoff and backup excluded."
            ),
        },
    )
    return files


def publish(files: dict[str, bytes], root: Path = ROOT) -> None:
    """Refuse every write if any declared destination already exists."""
    if any((root / name).exists() for name in files):
        msg = "Stage D overwrite refused"
        raise FileExistsError(msg)
    for name, raw in files.items():
        if name.endswith(".gz"):
            put_binary(root / name, raw)
        else:
            put_text(root / name, raw.decode())


def validate(files: dict[str, bytes], root: Path = ROOT) -> None:
    """Require byte-identical machine, Markdown, trace and digest replay."""
    inputs.require(
        all(binary(root / name) == raw for name, raw in files.items()),
        "Stage D published replay differs",
    )


def main() -> None:
    """Publish once or replay retained artifacts; no acquisition entry point."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("operation", choices=("build", "verify"))
    args = parser.parse_args()
    data = inputs.load()
    files = artifacts(data)
    inputs.require(files == artifacts(data), "Nondeterministic Stage D derivation")
    if args.operation == "build":
        publish(files)
    else:
        validate(files)
    print(  # noqa: T201 -- explicit scientific CLI
        {
            "operation": args.operation,
            "join": "PASSED",
            "R1.5": data["diagnostic_replay"]["status"],
        },
    )


if __name__ == "__main__":
    main()
