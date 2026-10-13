# Copyright (c) 2026
# ruff: noqa: ANN401, E501 -- deterministic committed-input boundary
"""POST_HOC / ORACLE / NON_GATING / NOT_RUNTIME_AVAILABLE publication tooling."""

from __future__ import annotations

import argparse
import asyncio
import gzip
import json
from pathlib import Path
from typing import Any

from experiments.codex_dogfood.case_0009.artifacts import (
    ROOT,
    binary,
    digest,
    git,
    json_bytes,
    put_binary,
)
from experiments.structural_discrimination.post_hoc.source_quality import (
    analysis,
    reporting,
)
from experiments.structural_discrimination.stage_b.capture import (
    CASES,
    capture_root,
    case_root,
)
from experiments.structural_discrimination.stage_c.import_gold import require
from experiments.structural_discrimination.stage_d import analyze as published
from experiments.structural_discrimination.stage_d import join

CHECKPOINT = "2f902a117e89f71a6b86f27259702604c7612be4"
PUBLISHED_LOCAL_PAIR_COUNT = 121
PACKAGE = Path(__file__).resolve().parent
OUTPUT_NAMES = (
    "analysis.json",
    "analysis.md",
    "TRACE.md",
    "trace.json",
    "validation.json",
    "integrity.json",
)
EXPECTED_CATEGORIES = {
    "0017": "NO_MATERIAL_STRUCTURAL_DISCRIMINATION_SIGNAL",
    "0018": "STRUCTURAL_DISCRIMINATION_SIGNAL",
    "0019": "NO_MATERIAL_STRUCTURAL_DISCRIMINATION_SIGNAL",
}


async def committed(path: Path) -> bytes:
    """Read only an explicit published scientific path and authenticate exact bytes."""
    raw = await git("show", CHECKPOINT + ":" + path.relative_to(ROOT).as_posix())
    require(raw == binary(path), "Published input bytes changed: " + str(path))
    return raw


async def inputs() -> tuple[Any, Any, Any, Any, Any]:
    """Authenticate normal sealed projections without deep replay or acquisition."""
    receipt = await published.run("verify", CHECKPOINT)
    require(
        receipt["case_categories"] == EXPECTED_CATEGORIES,
        "Published categories changed",
    )
    cohort_path = published.OUTPUT / "analysis.json"
    raw_cohort = await committed(cohort_path)
    cohort = json.loads(raw_cohort)
    totals = cohort["cohort"]["totals"]
    require(
        totals["local_pairs"] == PUBLISHED_LOCAL_PAIR_COUNT
        and totals["pair_counts"]
        == {
            "BENEFICIAL": 7,
            "NEUTRAL": 110,
            "HARMFUL": 4,
            "STRONG_BENEFICIAL": 1,
            "STRONG_HARMFUL": 0,
        },
        "Published pair totals changed",
    )
    require(
        totals["supported_gold_labels"]
        == {"REQUIRED": 6, "HELPFUL_ONLY": 9, "UNNECESSARY": 106}
        and totals["required_in_A_support_coverage"] == join.rate(6, 39),
        "Published required support changed",
    )
    pairs, targets, unsupported = [], [], []
    hashes = {cohort_path.relative_to(ROOT).as_posix(): digest(raw_cohort)}
    for case, result in zip(CASES, cohort["cases"], strict=True):
        paths = {
            "published": case_root(case) / "stage_d/analysis.json",
            "stage_b": capture_root(case) / "trace.json.gz",
            "gold": case_root(case) / "adjudication/reviewed/gold.json",
            "design": case_root(case) / "protocol.json",
        }
        data = {}
        for key, path in paths.items():
            raw = await committed(path)
            hashes[path.relative_to(ROOT).as_posix()] = digest(raw)
            data[key] = json.loads(
                gzip.decompress(raw) if path.suffix == ".gz" else raw,
            )
        require(data["published"] == result, "Published case/cohort correspondence")
        p, t, u = analysis.extract(
            result,
            data["stage_b"],
            data["gold"],
            data["design"],
        )
        pairs.extend(p)
        targets.extend(t)
        unsupported.extend(u)
    require(
        cohort["cohort"]["source_label_diagnostics"][
            "distinct_source_target_obligation_pairs"
        ]
        == {"REQUIRED": 12, "HELPFUL_ONLY": 17, "UNNECESSARY": 189},
        "Published source-pair totals changed",
    )
    require(
        cohort["cohort"]["source_label_diagnostics"]["qualifying_occurrences"]
        == {"REQUIRED": 96, "HELPFUL_ONLY": 80, "UNNECESSARY": 1105},
        "Published source-occurrence totals changed",
    )
    return (
        pairs,
        targets,
        unsupported,
        cohort,
        {
            "status": analysis.STATUS,
            "published_stage_d_checkpoint": CHECKPOINT,
            "verification": receipt,
            "sha256": hashes,
            "mode": "NORMAL_SEALED; zero deep replay/scientific acquisition",
        },
    )


def source_hashes() -> Any:
    """Seal experiment implementation and documentation; no persistent trust cache."""
    paths = [
        *PACKAGE.glob("*.py"),
        PACKAGE / "README.md",
        PACKAGE / ".gitattributes",
        PACKAGE.parent / "__init__.py",
    ]
    return {p.relative_to(ROOT).as_posix(): digest(binary(p)) for p in sorted(paths)}


async def artifacts() -> dict[str, bytes]:
    """Reconstruct deterministic diagnostic output from authenticated projections."""
    pairs, targets, unsupported, cohort, authentication = await inputs()
    result = analysis.summarize(pairs, targets, unsupported, cohort)
    analysis.validate_summary(result, pairs, targets, unsupported, cohort)
    result["narrative_classification"] = "SOURCE_QUALITY_LOOKS_EXPLANATORY"
    result["non_gating_interpretation"] = reporting.INTERPRETATION
    result["limitations"] = reporting.LIMITATIONS
    result["input_authentication"] = authentication
    result["invariants"] = {
        "published_Stage_A_B_C_D_bytes": "UNCHANGED",
        "case_categories": "UNCHANGED",
        "cohort_totals": "UNCHANGED",
        "published_cohort_interpretation": "UNCHANGED",
        "production_behavior": "UNCHANGED",
        "SEARCH_POLICY_FAILURE": "NOT_ASSESSED",
        "confirmation_reserve": "NOT_ACCESSED",
        "historical_child_access": "NO",
        "retrieval_executions": 0,
        "RI_derivations": 0,
        "PPR_executions": 0,
        "RRF_executions": 0,
        "reranking": 0,
        "model_executions": 0,
    }
    trace = {
        "status": analysis.STATUS,
        "distinct_source_target_obligation_pairs": pairs,
        "target_source_quality_partition": targets,
    }
    files = {
        "analysis.json": json_bytes(result),
        "analysis.md": reporting.render(result).encode(),
        "trace.json": json_bytes(trace),
        "TRACE.md": reporting.trace(trace, result["strong_beneficial_trace"]).encode(),
        "validation.json": json_bytes(
            {
                "status": analysis.STATUS,
                "validation": "PASS",
                "exact_joins": "PASS",
                "published_inputs_unchanged": "PASS",
                "case_categories_unchanged": "PASS",
                "cohort_totals_unchanged": "PASS",
                "pair_occurrence_target_accounting": "PASS",
                "source_implementation_sha256": source_hashes(),
                "tests": "test_analysis.py; operational receipts separate",
                "separate_process_verification": "VERIFY freshly authenticates inputs and compares all generated bytes without overwrite",
            },
        ),
    }
    files["integrity.json"] = json_bytes(
        {
            "status": analysis.STATUS,
            "sha256": {n: digest(raw) for n, raw in files.items()},
            "input_authentication_sha256": digest(json_bytes(authentication)),
            "source_implementation_sha256": source_hashes(),
            "published_stage_d_checkpoint": CHECKPOINT,
            "self_hash": "EXCLUDED; anchored by external diagnostic Git checkpoint",
        },
    )
    return files


def publish(root: Path, files: Any) -> None:
    """Exclusively publish a complete deterministic diagnostic, refusing overwrites."""
    require(
        not any((root / name).exists() for name in files),
        "Diagnostic overwrite refused",
    )
    for name, raw in files.items():
        put_binary(root / name, raw)


def verify_bytes(root: Path, files: Any) -> None:
    """Reject cross-tab, group, outcome and integrity modifications by exact replay."""
    for name, raw in files.items():
        require(
            (root / name).read_bytes() == raw,
            "Diagnostic exact output/integrity differs: " + name,
        )


async def run(mode: str, checkpoint: str | None = None) -> Any:
    """Deterministic BUILD/VERIFY; neither mode writes any prior-stage artifact."""
    if mode == "build":
        require(
            not any((PACKAGE / n).exists() for n in OUTPUT_NAMES),
            "Diagnostic overwrite refused",
        )
    files = await artifacts()
    if mode == "build":
        publish(PACKAGE, files)
    verify_bytes(PACKAGE, files)
    if checkpoint:
        for name, raw in files.items():
            require(
                raw
                == await git(
                    "show",
                    checkpoint + ":" + (PACKAGE / name).relative_to(ROOT).as_posix(),
                ),
                "Committed diagnostic bytes differ",
            )
    result = json.loads(files["analysis.json"])
    return {
        "status": analysis.STATUS,
        "validation": "PASS",
        "mode": mode,
        "pair_weighted": result["cohort"]["pair_weighted"],
        "target_groups": result["cohort"]["target_source_quality"],
        "narrative_classification": result["narrative_classification"],
    }


def main() -> None:
    """Invoke only the post-hoc oracle diagnostic."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("mode", choices=("build", "verify"))
    parser.add_argument("--checkpoint")
    args = parser.parse_args()
    print(json.dumps(asyncio.run(run(args.mode, args.checkpoint)), indent=2))  # noqa: T201


if __name__ == "__main__":
    main()
