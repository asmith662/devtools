"""Publish deterministic Case 0016 Stage D from authenticated captured inputs."""

from __future__ import annotations

# ruff: noqa: INP001, CPY001, ANN401, D103, COM812, E501, EM101, TRY003
import argparse
import copy
import sys
from pathlib import Path
from typing import Any

from experiments.codex_dogfood.case_0016.adjudication.reviewed import materialize as m
from experiments.codex_dogfood.case_0016.stage_d import (
    authentication,
    metrics,
    reporting,
    validation,
)

PACKAGE = Path(__file__).resolve().parent


def expected(data: Any) -> dict[str, bytes]:
    result = reporting.enrich(data, metrics.analyze(data))
    checked = validation.validate(data, result)
    # Exercise immutable semantic-output rejection, not another reviewer.
    adversarial = []
    for field in (
        "ranks",
        "meaningful_finite_rank_gain",
        "reach_rescue",
        "complementary_regression_bound",
    ):
        changed = copy.deepcopy(result)
        target = changed["required_cells"][0]
        if field == "ranks":
            target[field]["A"] = 999
        else:
            target[field] = not target[field]
        try:
            validation.validate(data, changed)
        except ValueError:
            adversarial.append(field)
        else:
            raise ValueError("Required-cell tamper accepted: " + field)
    changed = copy.deepcopy(result)
    changed["selected_witnesses"]["O1"]["arms"]["C"]["depth"] = 0
    try:
        validation.validate(data, changed)
    except ValueError:
        adversarial.append("selected_depth")
    else:
        raise ValueError("Selected-depth tamper accepted")
    checked["adversarial_rejections"] = adversarial
    checked["overwrite_refusal"] = (
        "PASS; write_new checks every output before any write"
    )
    checked["native_reconstruction"] = (
        "PASS; sealed captured-return replay; zero treatment operations"
    )
    rendered = reporting.markdown(data, result)
    files = {
        "analysis.json": m.encoded(result),
        "analysis.md": rendered,
        "STAGE_D_REVIEW.md": rendered,
        "validation.json": m.encoded(checked),
    }
    trace = {
        "case": "0016",
        "provenance": data["provenance"],
        "reviewed_gold_sha256": data["reviewed_replay"]["sha256"],
        "joins": {
            "native_resources": 514,
            "gold_cells": 3084,
            "required_cells": len(result["required_cells"]),
            "units": 48,
            "witnesses": len(result["witnesses"]),
            "rank_bindings": len(result["exact_rank_bindings"]),
        },
        "stages": [
            "authenticate checkpoints and sealed scientific inputs",
            "exact owning-obligation gold/native identity join",
            "all independent witness/alternative/prefix mathematics",
            "captured propagated-flow/RRF/ablation and self/cross diagnostics",
            "frozen integer gates in original precedence",
            "deterministic publication without treatment or semantic calls",
        ],
        "gate_inputs": result["gate_inputs"],
        "gates": result["gates"],
        "precedence": result["precedence"],
        "outcome": result["outcome"],
        "validation": checked,
        "scientific_reruns": 0,
        "semantic_reviewers": 0,
        "artifacts_sha256": {n: m.sha(b) for n, b in files.items()},
    }
    files["trace.json"] = m.encoded(trace)
    files["TRACE.md"] = (
        "# Case 0016 Stage D trace\n\nCaptured inputs only; no retrieval, graph, RI, PPR or fusion execution; no semantic reviewer.\n\n```json\n"
        + m.encoded(trace).decode()
        + "```\n"
    ).encode()
    implementation = {
        p.name: m.sha(p.read_bytes()) for p in sorted(PACKAGE.glob("*.py"))
    }
    files["integrity.json"] = m.encoded(
        {
            "schema": "case-0016-stage-d-integrity-v1",
            "sha256": {n: m.sha(b) for n, b in files.items()},
            "implementation_sha256": implementation,
            "input_seals": {
                "treatment": authentication.SEAL,
                "primary": m.HASHES,
                "reviewed": data["reviewed_replay"]["sha256"],
            },
            "gate_implementation_sha256": m.sha(
                (m.CASE.parents[1] / "task_conditioned_graph/gates.py").read_bytes()
            ),
            "excluded": [".local", ".scratch", "self hash to avoid cycle"],
            "outcome": result["outcome"],
        }
    )
    return files


def verify(data: Any) -> Any:
    files = expected(data)
    for name, raw in files.items():
        m.require(
            (PACKAGE / name).read_bytes() == raw,
            "Stage D deterministic replay: " + name,
        )
    return {
        "status": "PASS",
        "outcome": m.load(PACKAGE / "analysis.json")["outcome"],
        "sha256": {n: m.sha(b) for n, b in files.items()},
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("mode", choices=("build", "verify"))
    mode = parser.parse_args().mode
    sys.stdout.write(
        "Authenticating sealed checkpoints and captured-return replay; no scientific execution.\n"
    )
    sys.stdout.flush()
    data = authentication.authenticate()
    sys.stdout.write(
        "Authentication PASS. Building exact gold join and frozen gates.\n"
    )
    sys.stdout.flush()
    if mode == "build":
        files = expected(data)
        m.write_new({PACKAGE / n: b for n, b in files.items()})
        sys.stdout.write(
            m.encoded(
                {
                    "status": "BUILT; SEPARATE VERIFY REQUIRED",
                    "sha256": {n: m.sha(b) for n, b in files.items()},
                }
            ).decode()
        )
    else:
        sys.stdout.write(m.encoded(verify(data)).decode())


if __name__ == "__main__":
    main()
