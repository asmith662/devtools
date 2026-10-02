# Copyright (c) 2026
# ruff: noqa: COM812, E501
"""Prepare safe validation metadata and a neutral pre-task adjudication frame."""

from __future__ import annotations

import argparse
import json
import shutil
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
HERE = Path(__file__).parent
EXCLUDED_COUNT = 22
BOUNDED_COUNT = 7


def prepare(*, bounded_copy_only: bool = False) -> None:
    """Write protocol inputs without touching ranks, traces, or outcomes."""
    boundary = json.loads(
        (HERE / "validation_boundary.json").read_text(encoding="utf-8")
    )
    if (
        len(boundary["excluded_tests"]) != EXCLUDED_COUNT
        or len(boundary["bounded_cwd_tests"]) != BOUNDED_COUNT
    ):
        msg = "Protected validation boundary differs from frozen exclusions."
        raise ValueError(msg)
    bounded_root = Path(tempfile.mkdtemp(prefix="devtools-case3-validation-"))
    for prefix in ("src", "tests", "docs", "experiments", "scripts"):
        for source in (ROOT / prefix).rglob("*"):
            if (
                source.is_file()
                and source.suffix.lower() in {".py", ".md", ".toml", ".yaml", ".yml"}
                and "__pycache__" not in source.parts
            ):
                target = bounded_root / source.relative_to(ROOT)
                target.parent.mkdir(parents=True, exist_ok=True)
                shutil.copyfile(source, target)
    for name in ("pyproject.toml", "AGENTS.md", "README.md"):
        source = ROOT / name
        if source.exists():
            shutil.copyfile(source, bounded_root / name)
    (ROOT / ".devtools/case3-bounded-root.txt").write_text(
        str(bounded_root), encoding="utf-8"
    )
    print(bounded_root)  # noqa: T201
    if bounded_copy_only:
        return
    if (HERE / "adjudication_input.json").exists():
        msg = "Neutral frame already exists; use --bounded-copy-only to refresh validation."
        raise ValueError(msg)
    freeze = json.loads((HERE / "pre_retrieval.json").read_text(encoding="utf-8"))
    frame = {
        "schema": "codex-neutral-adjudication-frame-v1",
        "case_number": "0003",
        "starting_commit": freeze["starting_head"],
        "snapshot_id": freeze["snapshot_id"],
        "task": freeze["task_full_prompt"],
        "resources": freeze["snapshot_resources"],
    }
    (HERE / "adjudication_input.json").write_text(
        json.dumps(frame, indent=2) + "\n", encoding="utf-8"
    )
    prompt = (
        """Independently assess repository resources needed to complete the exact frozen task below. You have only the PRE-TASK repository export and neutral eligible address/content-identity frame. Do not access the original working repository, post-task artifacts, retrieval results, agent traces, or judgments from other cases. Search/read any exported resources. You must assess task obligations, not equate opened or modified files with requirement. Categorize each eligible resource as required_for_understanding, required_for_implementation, required_for_api_contract, required_for_tests, required_for_configuration, required_for_validation, helpful_only, unnecessary, or unresolved. Required may have multiple obligation categories. Give concrete rationale per required/helpful/unresolved resource. For unnecessary resources you may explicitly affirm all unlisted eligible resources unnecessary. Record acceptable alternatives only if sound. This judgment is frozen before provenance join. Do not edit the export or run validation. Return JSON matching supplied schema.\n\n"""
        + json.dumps(frame, indent=2)
    )
    (HERE / "blind_prompt.txt").write_text(prompt, encoding="utf-8")
    states = [
        "required_for_understanding",
        "required_for_implementation",
        "required_for_api_contract",
        "required_for_tests",
        "required_for_configuration",
        "required_for_validation",
        "helpful_only",
        "unnecessary",
        "unresolved",
    ]
    schema = {
        "type": "object",
        "properties": {
            "snapshot_id": {"type": "string"},
            "judgments": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "address": {"type": "string"},
                        "states": {
                            "type": "array",
                            "items": {"type": "string", "enum": states},
                        },
                        "rationale": {"type": "string"},
                    },
                    "required": ["address", "states", "rationale"],
                    "additionalProperties": False,
                },
            },
            "unlisted_resources_are_unnecessary": {"type": "boolean"},
            "acceptable_alternatives": {"type": "array", "items": {"type": "string"}},
            "limitations": {"type": "string"},
        },
        "required": [
            "snapshot_id",
            "judgments",
            "unlisted_resources_are_unnecessary",
            "acceptable_alternatives",
            "limitations",
        ],
        "additionalProperties": False,
    }
    (HERE / "blind_schema.json").write_text(
        json.dumps(schema, indent=2) + "\n", encoding="utf-8"
    )


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--bounded-copy-only", action="store_true")
    prepare(bounded_copy_only=parser.parse_args().bounded_copy_only)
