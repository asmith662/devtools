# Copyright (c) 2026
# ruff: noqa: EM101, TRY003, COM812, TRY301 -- bounded repository-local projection
"""Project allowlisted administrative metadata; never mutate source records."""

from __future__ import annotations

import argparse
import asyncio
import hashlib
import json
import re
from pathlib import Path
from typing import Any

from devtools.core.paths import resolve_path
from devtools.core.time import Timestamp
from devtools.resources.filesystem import (
    FileFormat,
    FilesystemError,
    TextFile,
    read,
    write,
)
from scripts.backlog.coordinator import git
from scripts.backlog.intake import Intake, load_json
from scripts.backlog.work import WorkCycle


def _text(path: Path) -> str:
    file = read(resolve_path(path), file_format=FileFormat.TEXT, max_bytes=2 << 20)
    if not isinstance(file, TextFile):
        raise TypeError("Expected text")
    return file.content


def _reference(path: Path) -> dict[str, str]:
    # References are plain text, never endpoints for reading arbitrary local files.
    # UTF-8 TEXT codec preserves CR/LF and BOM; encode without normalization.
    return {
        "path": str(path),
        "sha256": hashlib.sha256(_text(path).encode("utf-8")).hexdigest(),
    }


def _evidence_class(provenance: dict[str, Any]) -> str:
    if provenance.get("mode") == "SCRIPTED_HOST_TEST_ONLY":
        return "SCRIPTED_HOST_TEST_ONLY"
    if provenance.get("model") and provenance.get("profile"):
        return "LOCAL_MODEL_RECEIPT"
    return "UNCLASSIFIED_NOT_PROOF_OF_LIVE_INFERENCE"


def _worker_record(base: Path, path: Path) -> dict[str, Any]:
    if not resolve_path(path).value.is_relative_to(resolve_path(base).value):
        raise ValueError("Worker evidence escapes configured root")
    return load_json(path)


def _backlog_text(root: Path, path: Path) -> str:
    if not resolve_path(path).value.is_relative_to(root):
        raise ValueError("Backlog evidence escapes configured coordinator")
    return _text(path)


def project(
    root: Path, *, worker_roots: tuple[Path, ...] | None = None
) -> dict[str, Any]:
    """Read supported records and expose errors, missing values and provenance.

    A snapshot is historical evidence, never current authority. In particular a
    stored grant is not reauthenticated admission and legacy BACKLOG is not an
    intake-approved assignment. Raw prompts, stderr, tokens and credentials are
    deliberately not copied into the served directory.
    """
    root = resolve_path(root).value
    intake = Intake(root)
    queue = intake.queue()
    errors = list(queue["errors"])
    proposals = []
    for entry in queue["proposals"]:
        record = intake.get(entry["id"])
        payload = record["proposal"]["payload"]
        proposals.append(
            {
                **entry,
                "parent": payload["parent"],
                "discovery": payload["discovery"],
                "evidence": payload["evidence"],
                "reference": _reference(
                    intake.proposals / entry["id"] / "proposal.json"
                ),
            }
        )
    backlog = []
    for path in sorted((root / "docs/backlog/items").glob("B-*.md")):
        text = _backlog_text(root, path)
        status = re.search(r"^- status: (\w+)\s*$", text, re.MULTILINE)
        backlog.append(
            {
                "id": path.name[:6],
                "title": text.splitlines()[0].lstrip("# "),
                "status": status[1] if status else "UNKNOWN",
                "reference": _reference(path),
            }
        )
    work = []
    cycle = WorkCycle(root)
    for folder in sorted((root / ".local/backlog/work").glob("*")):
        if not folder.is_dir():
            continue
        try:
            state = cycle.status(folder.name)  # canonical receipt authentication
            work.append(
                {
                    "item": folder.name,
                    "disposition": state["disposition"],
                    "branch": state.get("branch"),
                    "base_head": state.get("base_head"),
                    "grant_record_present": (folder / "authorization.json").exists(),
                    "reference": _reference(folder / "assignment.json"),
                    "result_reference": _reference(folder / "result.json")
                    if (folder / "result.json").is_file()
                    else None,
                }
            )
        except (ValueError, KeyError, TypeError, OSError, FilesystemError) as error:
            errors.append({"path": str(folder), "error": str(error)})
    workers = []
    roots = (
        worker_roots
        if worker_roots is not None
        else (root / ".local/qwen-coding-worker",)
    )
    paths = sorted(
        {(base, path) for base in roots for path in base.glob("*/result.json")}
    )
    for base, path in paths:
        try:
            result = _worker_record(base, path)
            if result.get("schema") not in {
                "qwen-markdown-coding-loop-v1",
                "qwen-coding-loop-v2",
            }:
                raise ValueError("Unsupported worker result schema")
            turns = result.get("turns", [])
            last = turns[-1].get("validation", {}) if turns else {}
            if not isinstance(result.get("usage_totals", {}), dict):
                raise TypeError("Invalid usage observation")
            provenance = result.get("provenance") or {}
            workers.append(
                {
                    "id": path.parent.name,
                    "key": hashlib.sha256(
                        str(resolve_path(path.parent)).encode()
                    ).hexdigest(),
                    "task_key": result.get("task_name")
                    or next(iter(result.get("baseline", {})), "NOT_RECORDED"),
                    "task_name": result.get("task_name")
                    or (
                        "Markdown fence closing"
                        if any(
                            "markdown/file.py" in p for p in result.get("baseline", {})
                        )
                        else "Task NOT_RECORDED"
                    ),
                    "evidence_class": _evidence_class(provenance),
                    "disposition": result.get("disposition", "UNKNOWN"),
                    "accepted": result.get("accepted"),
                    "started_at": result.get("started_at"),
                    "finished_at": result.get("finished_at"),
                    "elapsed_seconds": result.get("elapsed_seconds"),
                    "model_calls": result.get("model_calls_attempted"),
                    "repair_cycles": result.get("repair_cycles"),
                    "usage": {
                        key: result.get("usage_totals", {}).get(key)
                        for key in (
                            "input_tokens",
                            "output_tokens",
                            "cached_input_tokens",
                            "reasoning_tokens",
                        )
                    },
                    "validation": {
                        key: last.get(key, {}).get("exit_code")
                        for key in ("tests", "oracle")
                    },
                    "reference": _reference(path),
                    "coverage": (
                        "Local worker receipt; provider categories may be unknown. "
                        "Not account-wide usage."
                    ),
                }
            )
        except (
            ValueError,
            KeyError,
            TypeError,
            AttributeError,
            OSError,
            FilesystemError,
        ) as error:
            errors.append({"path": str(path), "error": str(error)})
    return {
        "schema": "devtools-operator-snapshot-v1",
        "observed_at": str(Timestamp.now()),
        "source": str(root),
        "proposals": proposals,
        "backlog": backlog,
        "work": work,
        "workers": workers,
        "errors": errors,
        "limitations": [
            "Read-only observation, not worker liveness or execution authority.",
            (
                "Only .local/qwen-coding-worker/*/result.json is inventoried; "
                "missing receipts are not zero consumption."
            ),
            (
                "Stored grant presence is not current admission. "
                "Canonical BACKLOG status alone is not intake approval."
            ),
        ],
    }


async def main() -> None:
    """Export to this pilot's build directory, never an authoritative record."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source", type=Path, required=True)
    args = parser.parse_args()
    root = resolve_path(args.source, base_directory=Path.cwd()).value
    result = project(root)
    result["source_head"] = await git(root, "rev-parse", "HEAD")
    result["source_branch"] = await git(root, "branch", "--show-current")
    result["source_dirty"] = bool(await git(root, "status", "--porcelain"))
    output = Path(__file__).parent / "web/dist/data.json"
    if not output.parent.is_dir():
        raise ValueError("Build the frontend before exporting the snapshot")
    write(
        TextFile(resolve_path(output), json.dumps(result, indent=2) + "\n"),
        overwrite=True,
    )
    print(  # noqa: T201 -- operator CLI outcome
        f"Snapshot: {output}; {len(result['workers'])} worker receipts; "
        f"{len(result['errors'])} errors"
    )


if __name__ == "__main__":
    asyncio.run(main())
