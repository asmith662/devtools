# Copyright (c) 2026
# ruff: noqa: EM101, TRY003
"""Authenticate immutable scientific implementations and publication bytes."""

from __future__ import annotations

from experiments.codex_dogfood.case_0009.artifacts import digest, read_json
from experiments.codex_dogfood.case_0016.adjudication.reviewed import materialize
from experiments.codex_dogfood.case_0016.stage_d import analysis


def sealed_files() -> dict[str, str]:
    """Require the exact accepted Stage D seal, all artifacts, gold and gates."""
    root = analysis.PACKAGE
    seal_raw = (root / "integrity.json").read_bytes()
    if (
        digest(seal_raw)
        != "79474ae1a8688550b267bd88e856340204714b15f70bd8bbfc10e5ae90ff1125"
    ):
        raise ValueError("Accepted Stage D seal differs")
    seal = read_json(root / "integrity.json")
    files = {root / "integrity.json": digest(seal_raw)}
    files.update(
        {
            root / n: h
            for section in ("sha256", "implementation_sha256")
            for n, h in seal[section].items()
        },
    )
    files.update(
        {
            materialize.ADJ / "primary" / n: h
            for n, h in seal["input_seals"]["primary"].items()
        },
    )
    files.update(
        {materialize.ROOT / n: h for n, h in seal["input_seals"]["reviewed"].items()},
    )
    files[materialize.CASE.parents[1] / "task_conditioned_graph/gates.py"] = seal[
        "gate_implementation_sha256"
    ]
    for path, expected in files.items():
        if digest(path.read_bytes()) != expected:
            raise ValueError("Sealed historical file differs: " + str(path))
    return {str(p): h for p, h in files.items()}
